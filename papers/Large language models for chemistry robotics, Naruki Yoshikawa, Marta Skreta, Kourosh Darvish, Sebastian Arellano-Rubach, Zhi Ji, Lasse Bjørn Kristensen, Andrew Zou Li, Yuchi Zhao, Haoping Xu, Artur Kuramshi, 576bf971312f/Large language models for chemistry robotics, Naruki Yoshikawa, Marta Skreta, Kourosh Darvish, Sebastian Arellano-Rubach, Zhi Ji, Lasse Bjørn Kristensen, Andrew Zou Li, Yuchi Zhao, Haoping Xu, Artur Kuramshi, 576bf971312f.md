Autonomous Robots (2023) 47:1057–1086
https://doi.org/10.1007/s10514-023-10136-2




Large language models for chemistry robotics
Naruki Yoshikawa1,2 · Marta Skreta1,2 · Kourosh Darvish1,2 · Sebastian Arellano-Rubach3 · Zhi Ji1 ·
Lasse Bjørn Kristensen1 · Andrew Zou Li1 · Yuchi Zhao4 · Haoping Xu1,2 · Artur Kuramshin1 ·
Alán Aspuru-Guzik1,2,5 · Florian Shkurti1,2 · Animesh Garg1,2,6

Published online: 25 October 2023
© The Author(s) 2023


Abstract
This paper proposes an approach to automate chemistry experiments using robots by translating natural language instructions
into robot-executable plans, using large language models together with task and motion planning. Adding natural language
interfaces to autonomous chemistry experiment systems lowers the barrier to using complicated robotics systems and increases
utility for non-expert users, but translating natural language experiment descriptions from users into low-level robotics lan-
guages is nontrivial. Furthermore, while recent advances have used large language models to generate task plans, reliably
executing those plans in the real world by an embodied agent remains challenging. To enable autonomous chemistry exper-
iments and alleviate the workload of chemists, robots must interpret natural language commands, perceive the workspace,
autonomously plan multi-step actions and motions, consider safety precautions, and interact with various laboratory equip-
ment. Our approach, CLAIRify, combines automatic iterative prompting with program verification to ensure syntactically
valid programs in a data-scarce domain-specific language that incorporates environmental constraints. The generated plan is
executed through solving a constrained task and motion planning problem using PDDLStream solvers to prevent spillages of
liquids as well as collisions in chemistry labs. We demonstrate the effectiveness of our approach in planning chemistry experi-
ments, with plans successfully executed on a real robot using a repertoire of robot skills and lab tools. Specifically, we showcase
the utility of our framework in pouring skills for various materials and two fundamental chemical experiments for materials
synthesis: solubility and recrystallization. Further details about CLAIRify can be found at https://ac-rad.github.io/clairify/.

Keywords Large language models · Constrained task and motion planning · Plan generation verification · Self-driving labs ·
Chemistry lab automation


                                                                      1 Introduction

                                                                      The execution of chemistry experiments, which represents a
                                                                      crucial stage in the process of material discovery, typically
                                                                      relies on human experts. This manual experimentation poses
Naruki Yoshikawa, Marta Skreta and Kourosh Darvish have contributed
equally to this work.                                                 a number of significant challenges, such as difficulties in
                                                                      reproducibility, high resource requirements, and limited scal-
B Kourosh Darvish                                                     ability. To address these obstacles, the concept of self-driving
    kdarvish@cs.toronto.edu                                           labs (SDLs) has emerged (Seifrid et al., 2022). Although
1   University of Toronto, Toronto, ON, Canada
                                                                      specialized hardware for chemistry experiments has been
2
                                                                      proposed and used in modern labs, we argue that using
    Vector Institute for Artificial Intelligence, Toronto, ON,
    Canada
                                                                      general-purpose robots is beneficial in developing SDLs that
3
                                                                      maximize the use of existing resources and are more con-
    University of Toronto Schools, Toronto, ON, Canada
                                                                      figurable. The functionality of general-purpose robots can
4   University of Waterloo, Waterloo, ON, Canada                      be expanded by programming them to interact with exist-
5   CIFAR Artificial Intelligence Research Chair, Toronto, ON,        ing chemistry instruments designed for humans. This feature
    Canada                                                            contributes to reducing the cost related to introducing addi-
6   NVIDIA, Santa Clara, CA, USA


                                                                                                                           123
1058                                                                                                 Autonomous Robots (2023) 47:1057–1086


                                                                          language models (LLMs) can assist robots to reason with
                                                                          common sense (Huang et al., 2022; Singh et al., 2022). LLMs
                                                                          have been used to generate structured outputs (Devlin et al.,
                                                                          2019; Brown et al., 2020; Chowdhery et al., 2022), includ-
                                                                          ing code generation (Chen et al., 2021; Wang et al., 2021;
                                                                          Li et al., 2022) and robot programming (Liang et al., 2022).
                                                                          Nevertheless, the application of LLMs to task-plan genera-
                                                                          tion for chemistry robots presents two key challenges. Just
                                                                          like with all machine-executable code, generated plans must
                                                                          adhere to strict syntax rules in order to be executed by a robot.
                                                                          In robotics, task-plan verification is often desired, because it
                                                                          increases the likelihood that a robot can reach the desired
                                                                          goal (Garrett et al., 2020; Ahn et al., 2022). Furthermore,
                                                                          LLMs may perform poorly in generating task plans in a zero-
                                                                          shot manner for data-scarce, domain-specific languages, such
                                                                          as the ones in robot planning, and thus require fine-tuning,
                                                                          or in technical scientific domains (Gu et al., 2021), or scien-
                                                                          tific coding (Liu et al., 2023). Several approaches have been
                                                                          proposed in the literature to address these issues. One promis-
                                                                          ing technique is iterative prompting, which has an advantage
Fig. 1 Task plans generated by LLMs may contain syntactical errors in     over fine-tuning LLMs, as the latter requires access to the
domain-specific languages. By using verifier-assisted iterative prompt-   model weights and training datasets to learn domain-specific
ing, CLAIRify can generate a valid program. Once the program has          languages reasonably well and incurs high computational
been verified, it is passed on to a task and motion planner (TAMP) for
execution by a robot                                                      costs (Mishra et al., 2021; Wang et al., 2011; Wu et al.,
                                                                          2022). Iterative prompting enables the LLM to verify can-
                                                                          didate plans while providing the rules of structured language
tional hardware for specific purposes. Therefore, this study              as input, thereby leveraging in-context learning.
discusses the use of general-purpose robots for building                      The planning component of the robotic system takes
chemistry SDLs.                                                           as input perception, vision-based outcome evaluation of
   One of the principal obstacles in effectively using robots in          experiments and natural language instructions, and solves
chemistry labs is to ensure that they are natural and intuitive           a constrained task and motion planning (TAMP) problem.
for chemists to operate. An approach to achieving a natural               To do so, the robot must possess both general and chemistry
and intuitive interface between chemists and robots is through            domain-specific perception and manipulation skills, includ-
the use of natural language as a communication medium. This               ing recognizing transparent and opaque objects (Xu et al.,
approach enables users to instruct robots in an efficient and             2021; Wang et al., 2023), estimating object poses, and mon-
effective manner.                                                         itoring the state of materials synthesis, such as detecting if a
   This work aims to facilitate autonomous and safe execu-                solution is dissolved (Shiri et al., 2021). Dexterous manipu-
tion of chemistry experiments using general-purpose robot                 lation and handling are also necessary, such as constrained
manipulators. This is accomplished through natural language               motion for picking and transporting objects without spilling
instructions to generate plans. Several challenges must be                their contents, pouring skills, and manipulation of tools and
addressed at both the natural language processing (NLP) and               objects. Additionally, high precision and repeatability are
robotic planning levels for this purpose. At the NLP level, the           crucial for reproducible and reliable results in robot-executed
robot must be capable of converting natural language instruc-             chemistry experiments.
tions into executable robot instructions (Fig. 1). At the robotic             Ensuring safety during experiments and interactions is
planning level, the robotic system should be capable of plan-             another challenge (Ménard & Trant, 2020). Multi-layered
ning robot tasks and motions that take safety considerations              safety requirements are necessary, including high-level con-
into account, using intermediate goals identified by NLP and              straints on material synthesis order in experiment description
perceptual information of the robot workspace.                            and task planning, and low-level manipulation and perception
   Natural language has been used in the literature to over-              skills to prevent spilling during transportation of chemistry
come the communication barrier between humans and robots,                 vials and beakers.
for example in navigation tasks (Tellex et al., 2011). More
recently, numerous studies have demonstrated that large



123
Autonomous Robots (2023) 47:1057–1086                                                                                            1059


Contributions We introduce an autonomous robotic sys-             execution time using visual feedback. As a proof of concept
tem for chemistry lab automation, an end-to-end closed-loop       for chemistry lab automation, we achieved results that are
robotic framework that translates natural language into struc-    comparable to the literature ground truth for the solubility
tured long-horizon task plans and then executes them by a         experiment, with a 7.2% error rate for the solubility of salt,
constrained task and motion planning solver, integrated with      and successful recrystallization of alum.
perception and manipulation skills, and vision-based evalua-         The paper is organized as follows: Section 2 reviews the
tion of experiment outcomes (Fig. 1). Our approach consists       state of the art. Section 3 defines the problem and presents
of two modules. The first is CLAIRify, which translates a         the proposed end-to-end approach, covering natural language
natural language input into a structured plan. The second         and perceptual inputs to robot task and motion planning and
is the translation of the plan to low-level robot actions. To     skill execution. Experiments and results are presented in Sec-
evaluate the framework, we use a domain-specific language         tion 4. Discussion of the results is provided in Section 5, and
called Chemical Description Language (XDL) (Mehr et al.,          conclusions are drawn in Section 6.
2020). XDL is an XML-based domain-specific language
used to describe action plans for chemistry experiments in
a structured format, and is suitable for commanding robots        2 Related work
in self-driving laboratories (Seifrid et al., 2022). XDL is
hardware-agnostic, meaning that it can be executed on many        This section describes recent advancements in lab automa-
robot platforms and lab setups. We showcase an example            tion, specifically focusing on robotics and the methods
of how XDL can be executed on a Franka robot in a chem-           through which large language models (LLMs) can be incor-
istry lab setting by converting XDL to low-level robot actions    porated into these systems. Furthermore, the section high-
using TAMP. Our method includes (I) a rule-based iterative        lights the challenges associated with generating verifiable
verifier to check for syntax correctness and environment con-     task plans from LLMs, which are necessary to generate robot
straints, which improves zero-shot task plan generation in a      tasks and motion plans. Lastly, the section outlines recent
data-scarce domain. (II) At the TAMP level, constrained task      efforts that focus on identifying the essential robot skills
and motion planning is incorporated via a PDDLStream (Gar-        required to execute lab automation tasks effectively.
rett et al., 2020) solver to avoid spillage when transporting
liquids and powders. When adding constraints to the robot’s       2.1 Lab automation
degrees of freedom, the motion planning success rate was
lower compared to unconstrained planning. To overcome             Lab automation aims to introduce automated hardware in a
this difficulty, we introduced a new degree of freedom to         laboratory to improve the efficiency of scientific discovery.
our robot. We demonstrate that an 8-DoF robot has 97%             It has been applied to high-throughput screening (Pereira
success rate in constrained TAMP compared to 84% of a             & Williams, 2007) (Macarron et al., 2011) to discover
7-DoF robot. Moreover, we present accurate and efficient          desired materials from a pool of candidates. With the rise
pouring skills inspired by human motions with an average          of AI technologies, the concept of a self-driving laboratory
relative error of 8.1% and 8.8% for pouring water and salt,       (SDL) (Häse et al., 2019; Seifrid et al., 2022) that combines
respectively, compared to a baseline method with 81.4% and        experiment planning by AI and automated experimentation
24.1% errors. Our method achieves comparable results to           platforms has emerged. A review on SDL can be found in
recent studies (Kennedy et al., 2019; Huang et al., 2021),        (Abolhasani & Kumacheva, 2023). Different hardware for
yet it stands out for its simplicity and the reduced need for     lab automation has been utilized in SDLs to meet the needs
complex sensor feedback.                                          of individual laboratories, such as pipetting robots (Higgins
    Our evaluation results demonstrate that CLAIRify outper-      et al., 2021) or flow reactors (Epps et al., 2020; Li et al., 2020).
forms the current state-of-the-art model for XDL generation       The Chemputer (Mehr et al., 2020) is an example of a special-
presented in (Mehr et al., 2020). Additionally, our frame-        ized machine for automated chemistry experiments. In the
work represents an advancement from the approach in               corresponding paper, the authors demonstrated an automated
(Fakhruldeen et al., 2022), which relied on a finite state        workflow that translates organic chemistry literature into a
machine with fixed objects in a static workspace. Our frame-      structured language called XDL and synthesized the speci-
work perceives the environment and plans long-horizon             fied molecules. While specialized hardware for chemistry is
trajectories to perform multistep chemistry experiments. It       widely used in lab automation, general-purpose robots have
can close the loop at two levels. The first is at the chemistry   also been applied to chemistry because of their flexibility,
task level, where online visual feedback is used to estimate      mobility, and dexterous manipulation capabilities. The utility
the progress of task execution. The second is at the robot        of mobile general-purpose robots for discovering improved
motion planning and skill level, where the robot is able to       photocatalysts for hydrogen production was demonstrated in
adapt to uncertainties, for example, by refining its plan at      (Burger et al., 2020). ARChemist (Fakhruldeen et al., 2022),


                                                                                                                          123
1060                                                                                         Autonomous Robots (2023) 47:1057–1086


a lab automation system, was developed to conduct exper-          2.3 Leveraging language models with external
iments, including solubility screening and crystallization,           knowledge
without human intervention. Another work (Knobbe et al.,
2022) endowed a collaborative robot with a force-sensitive        A challenge with LLMs generating code is that the cor-
pipetting skill by extending the robot with a pipetting fin-      rectness of the code is not assured. There have been many
ger system. Differently from other works where pick, place,       interesting works on combining language models with exter-
insertion, or liquid handling, were the focus of robot skills,    nal tools to improve the reliability of the output. Mind’s
in (Pizzuto et al., 2022), the robot learns to scrape pow-        Eye (Liu et al., 2023) attempts to ground large language
ders from vials for crystallization experiments. During the       model’s reasoning with physical simulation. They trained
experiment, crystallized materials tend to adhere to the inner    LLM with pairs of language and codes and used the simula-
wall of the vial. Acquiring these crystals necessitates physi-    tion results to prompt an LLM to answer general reasoning
cal interaction between the crystals and the vial using a robot   questions.
arm, which is unattainable with a valve-pump-based system.            Toolformer (Schick et al., 2023) incorporates API calls
These examples demonstrate the potential utilization of a         into the language model to improve a downstream task, such
versatile robot in expanding the scope of tasks automated         as question answering, by fine-tuning the model to learn how
within chemistry laboratories. Similarly, an automated chem-      to call the API. LEVER (Ni et al., 2023) improves LLM
istry experiment system that mimics the motions of human          prompting for SQL generation by using a model-based ver-
chemists has been proposed in (Lim et al., 2020). Addition-       ifier trained to verify the generated programs. As SQL is a
ally, The properties of thin-film materials were optimized        common language, the language model is expected to under-
using a robot arm in (MacLeod et al., 2020). Although these       stand its grammar. However, for domain-specific languages,
major steps towards chemistry lab automation have been            it is difficult to acquire training datasets and expensive to
made, their dependence on predefined tasks and on motion          execute the plans to verify their correctness. Our method
plans without constraint satisfaction guarantees limits their     does not require fine-tuning any models. Furthermore, there
flexibility in new and dynamic workspaces. In those works,        is no need for prior knowledge of the target language within
pick & place was the primary task that the manipulators           the language model obtained during the training phase. Our
were carrying out. Those works were tested in hand-tuned          idea is perhaps closest to LLM-Augmenter (Peng et al.,
and static environments to avoid occurrences of unsatisfied       2023), which improves LLM outputs by giving it access
task constraints and the associated problems, such as chem-       to external knowledge and automatically revising prompts
ical spills during the transfer of vessels filled with liquid.    in natural language question-answering tasks. Our method
Our framework resolves these gaps through using large lan-        similarly encodes external knowledge in the structure of the
guage models to generate long-horizon machine-readable            verifier and prompts, but for a structured and formally ver-
instructions and passing them to a constraint satisfaction and    ifiable domain-specific language. A review on augmenting
scene-aware planning system with a variety of skills.             LLMs with external tools is found in (Mialon et al., 2023).

                                                                  2.4 Task planning with large language models

                                                                  High-level task plans are often generated from a limited set of
                                                                  actions (Garrett et al., 2020), because task planning becomes
2.2 Large language models for chemistry                           intractable as the number of actions and time horizon grows
                                                                  (Kaelbling & Lozano-Pérez, 2011). One approach to do task
Several language models specialized for the chemistry or sci-     planning is using rule-based methods (Mehr et al., 2020;
ence domain have been proposed, such as MolT5 (Edwards            Baier et al., 2009). More recently, it has been shown that
et al., 2022), Chemformer (Irwin et al., 2022), and Galactica     models can learn task plans from input task specifications
(Taylor et al., 2022). After the release of GPT-3, chem-          (Sharma et al., 2021; Mirchandani et al., 2021; Shah et al.,
istry applications were attempted without further training        2021), for example using hierarchical learning (Xu et al.,
(Jablonka et al., 2023). The abilities to do Bayesian opti-       2018; Huang et al., 2019), regression based planning (Xu et
mization (Ramos et al., 2023), to use external chemistry tools    al., 2019), or reinforcement learning (Eysenbach et al., 2019).
(Bran et al., 2023), and to synthesize molecules by reading       However, to effectively plan tasks using learning-based tech-
documentation (Boiko et al., 2023) were explored. Our work        niques, large datasets are required that are hard to collect in
focuses on increasing the reliability of the output of LLMs       many real-world domains.
without further training by introducing iterative prompting           Recently, many works have used LLMs to translate natu-
and low-level planning through a task and motion planning         ral language prompts to robot task plans (Ahn et al., 2022;
framework.                                                        Huang et al., 2022; Liang et al., 2022; Singh et al., 2022). For


123
Autonomous Robots (2023) 47:1057–1086                                                                                         1061


example, Inner Monologue (Huang et al., 2022) uses LLMs            motions for the action, such as trajectory generation. Dif-
in conjunction with environment feedback from various per-         ferent approaches have been proposed in the literature to
ception models and state monitoring. However, because the          solve the TAMP problem. For example, (Toussaint, 2015)
system has no constraints, it can propose plans that are non-      proposed a non-linear constrained programming formula-
sensical. SayCan (Ahn et al., 2022), on the other hand,            tion for TAMP problems. In another work from the same
grounds task plans generated by LLMs in the real world             group, (Toussaint et al., 2018) integrated TAMP with kine-
by providing a set of low-level skills the robot can choose        matic or dynamic constraints for tool-use and manipulation.
from. A natural way of generating task plans is using code-        Another TAMP solver, PDDLStream (Garrett et al., 2020),
writing LLMs because they are not open-ended (i.e., they           extends PDDL (Ghallab et al., 1998), a common language to
have to generate code in a specific manner in order for it to      describe a planning problem mainly targeting discrete actions
be executable) and are able to generate policy logic. Sev-         and states, by introducing streams, a declarative procedure
eral LLMs trained on public code are available, such as            via sampling procedures. PDDLStream reduces a continuous
Codex (Chen et al., 2021), CodeT5 (Wang et al., 2021),             problem to a finite PDDL problem and invokes a classi-
AlphaCode (Li et al., 2022) and CodeRL (Le et al., 2022).          cal PDDL solver as a subroutine. Although pure-planning
LLMs can be prompted in a zero-shot way to generate                approaches to TAMP is general, it is computationally ineffi-
task plans. For example, Huang et al. (2022) analyzed the          cient. To accelerate the planning, an approach to incorporate
planning ability of LLM in virtual environment, Code as            geometric information has been proposed (Dantam et al.,
Policies (Liang et al., 2022) repurposes code-writing LLMs         2018). Recently, geometric information also has been used
to write robot policy code, and ProgPrompt (Singh et al.,          with learning-based approaches to improve planning effi-
2022) generates plans that take into account the robot’s cur-      ciency (Khodeir et al., 2023; Kim et al., 2022). In (Driess
rent state and the task objectives. PaLM-E is an embodied          et al., 2020), an initial scene image is inputted to a neural
LLM that translates visual, state estimates, sensory data, and     network that predicts the robot’s discrete action, and subse-
language domains into embodied reasoning for robot plan-           quently, a motion planning problem is solved.
ning (Driess et al., 2023). Text2Motion (Lin et al., 2023)            Another important aspect to take into account when solv-
combines LLM with skill feasibility heuristics to guide task       ing a TAMP problem is the incorporation of safety measures
planning. LLM-GROP (Ding et al., 2023) demonstrated                and constraints. Since PDDLStream verifies the feasibility
human-aligned object rearrangement from natural-language           of action execution during planning time, it can inherently
commands combined with TAMP. Inagaki et al. (2023) gen-            enhance safety by avoiding unfeasible plans or plans that
erated Python code for an automated liquid-handling robot          may lead to unsafe situations. Nonetheless, PDDLStream
from natural language instructions. However, these methods         does not yet account for constraints in the planning process,
generate Pythonic code, which is abundant on the Internet.         for example, to avoid material spillage from beakers during
For domain-specific languages, naive zero-shot prompting is        transportation, which impedes its deployment in real-world
not enough; the prompt has to incorporate information about        lab environments. For this purpose, sampling-based motion
the target language so that the LLM can produce outputs            constraint adherence (Berenson et al., 2011) or model-based
according to its rules.                                            motion planning (Muchacho et al., 2022) are possible stream
   Our approach, on the other hand, generates a task plan          choices. To overcome this shortcoming, our work extends
directly from an LLM in a zero-shot way on a constrained           PDDLStream with a projection-based sampling technique
set of tasks that are directly translatable to robot actions. We   (Kingston et al., 2019) to provide constraint satisfaction,
ensure that the plan is syntactically valid and meets envi-        completeness, and global optimality. The proposed PDDL-
ronment constraints using iterative error checking. However,       Stream takes intermediate goals generated by LLMs in a
while the generated plan is verified for syntax and constraint     structured language as its input.
satisfaction, it does not consider the robot embodiment and
workspace scene, making its execution on a robot uncerti-          2.6 Skills and integration of chemistry lab tools
fied. To address this issue, we integrate the generated task
plans as intermediate goals into a certifiable task and motion     In the process of lab automation, robots interact with tools
planner framework, which produces executable trajectories          and objects within the workspace and require a repertoire of
for the robot.                                                     many laboratory skills. Some skills can be completed with
                                                                   existing heterogeneous instruments and sensors in chem-
2.5 Task and motion planning with constraints                      istry labs, such as scales, stir plates, pH sensors, and heating
                                                                   instruments. Other skills are currently done either manually
Task and motion planning (TAMP) (Garrett et al., 2021)             by humans in the lab or with expensive special instru-
simultaneously determines the sequence of high-level sym-          ments. In a self-driving lab, robots should acquire those
bolic actions, such as picking and placing, and low-level          skills by effectively using different sensory inputs to compute


                                                                                                                        123
1062                                                                                         Autonomous Robots (2023) 47:1057–1086


appropriate robot commands. Pouring is a common skill in          ator output follows all the rules and specifications of the target
chemistry labs. Recent work (Kennedy et al., 2019; Huang          structured language and can be compiled without errors. If
et al., 2021) used vision and weight feedback to pour liquid      it cannot, the verifier returns error messages stating where
with manipulators. (Kennedy et al., 2019) proposed using          the errors were found and what they were. These are then
optimal trajectory generation combined with system identi-        appended to the generator output and added to the prompt
fication and model priors. To achieve milliliter accuracy in      for the next iteration. This process is repeated until a valid
water pouring tasks with a variety of vessels at human-like       program is obtained, or until the timeout condition is reached.
speeds, (Huang et al., 2021) used self-supervised learning        Algorithm 1 describes our proposed method.
from human demonstrations. In this work, we have reached              Once the generator output passes through the verifier with
similar results for pouring, using commercial scales that have    no errors, we are guaranteed that it is a syntactically valid
delayed feedback. Our approach is model-free, and it can          structured language. This output will then be translated into
pour granular solids as well. Granular solids have different      lower-level robot actions by passing it through TAMP for
dynamics from liquids, similar to the avalanche phenomenon.       robot execution. Each component of the pipeline is described
Lastly, while executing a chemistry experiment, the robot         in more detail below.
should possess perception skills to measure progress toward
completing the task. For example, in solubility experiments,      3.1.1 Generator
the robot should perceive when the solution is fully dissolved,
and therefore stop pouring the solvent into the solution. There   The generator takes a user’s instruction and generates unver-
are different ways to measure solubility. In our work, we use     ified structured language using an LLM. The input prompt
the turbidity measure (Shiri et al., 2021), which is based on     to the LLM is composed of a description of the target lan-
optical properties of light scattering and absorption by sus-     guage, a sentence specifying what the LLM should do (i.e.
pended sediment (Kitchener et al., 2017).                         “Convert to XDL”), the command to the LLM, and the nat-
                                                                  ural language instruction for which the task plan should be
                                                                  created. The description of the XDL language includes its
3 Methods                                                         file structure and lists of the available actions (which can
                                                                  be thought of as functions), their allowed parameters, and
We propose an automated robotic experiment platform that          their documentation. The input prompt skeleton is shown in
takes instructions from a human in natural language and exe-      Snippet 1, Fig. 3.
cutes the corresponding experiment. The natural language              Although the description of the target structured language
input is converted into a sequence of robot plans written in      is provided, the output may contain syntactic errors. To
a structured language by an LLM-based system, CLAIRify.           ensure syntactical correctness, the generator is iteratively
XDL (Steiner et al., 2019) was used as the robot programming      prompted by the automated interaction with the verifier. The
language. The task and motion planning module generates           generated code is passed through the verifier, and if no errors
the robot motion from the generated XDL. The overview of          are generated, then the code is syntactically correct. If errors
the proposed method is shown in Fig. 2.                           are generated, we re-prompt the LLM with the incorrect task
                                                                  plan from the previous iteration along with the list of errors
3.1 CLAIR IFY: natural language to structured                     indicating why the generated steps were incorrect. The skele-
    programs                                                      ton of the iterative prompt is shown in Snippet 2, Fig. 3. The
                                                                  feedback from the verifier is used by the LLM to correct the
CLAIRify takes a chemistry experiment description in nat-         errors from the previous iteration. This process is continued
ural language and generates a structured experiment plan in       until the generated code is error-free or a timeout condition
XDL format, which will be fed into the subsequent module to       is reached, in which case the system reports not being able
generate robot motions. A general overview of the CLAIRify        to generate a task plan.
pipeline is given in Fig. 2a.
   CLAIRify generates XDL with an automated iterative             3.1.2 Verifier
prompting between a generator and a verifier. The generator
outputs XDL from a prompt that combines the experiment            The verifier works as a syntax checker and static analyzer to
description and the target language format description. How-      check the output of the generator and send feedback to the
ever, we cannot guarantee the output from the generator is        generator. It first checks whether the input can be parsed as
syntactically valid, meaning that it would definitely fail to     correct XML and then checks the allowance of action tags,
compile into lower-level robot actions. To generate syntac-       the existence of mandatory properties, and the correctness
tically valid programs, we pass the output of the generator       of optional properties using a rule-based method that checks
through a verifier. The verifier determines whether the gener-    for permissible functions and parameters in the XDL docu-


123
Autonomous Robots (2023) 47:1057–1086                                                                                                            1063




Fig. 2 Our framework. a CLAIRify: LLM-based natural language pro-             adding them to the robot network through ROS. The robot is equipped
cessing module. The LLM takes the input (1), structured language              with an additional DoF at the end-effector, allowing it to perform con-
definition, and (optionally) resource constraints and generates unver-        strained motions. Our framework receives the chemical synthesis goal
ified structured language (2). The output is examined by the verifier         in XDL format. The procedure component is converted into correspond-
and is passed to LLM with feedback (3). The LLM-generated outputs             ing PDDL goals, and hardware and reagents components identify the
pass through the verifier (4). The correct output (5) is passed to the task   required initial condition for synthesis. Perception detects objects and
and motion planning module (6) to generate robot trajectories. b Robot        estimates their positions, contents in the workspace, and task progress.
planning module, which is composed of Perception, Task and Motion             PDDLStream generates a sequence of actions for the robot execution
Planning, and Skills blocks. Our framework enables the robot to lever-        (7)
age available chemistry lab devices (including sensors and actuators) by




                                                                                                                                         123
1064                                                                                                    Autonomous Robots (2023) 47:1057–1086


Algorithm 1 CLAIRify: Verifier-Assisted Iterative Prompts
Input: Structured language description L, instruction x
Output: Structured language task plan, y S L
  procedure IterativePrompting(L, x)
    yS L  = Generator(L, x)
    errors = Verifier(yS L  )
    while len(errors) > 0 and timeout condition != True do
        y S L  = Generator(L, x, yS L  , errors)
       errors = Verifier(y S L  )
    end while
    yS L = yS L 
  end procedure




                                                                            Fig. 4 Web interface for CLAIRify. Users input natural language
                                                                            descriptions of the experiment in the left column. XDL is generated
                                                                            in the right column when the user pushes the Translate button



                                                                            from the verifier. The error message is designed to be concise
                                                                            to save the context length of LLM.


                                                                            3.1.3 Incorporating environment constraints

                                                                            Because resources in a robot workspace are limited, we need
                                                                            to consider those constraints when generating task plans. If
                                                                            specified, we include the available resources in the gener-
                                                                            ator prompt. The verifier also catches if the candidate plan
                                                                            uses any resources aside from those mentioned among the
                                                                            available robot resources. Those errors are included in the
                                                                            generator prompt for the next iteration. If a constraint list is
                                                                            not provided, we assume the robot has access to all resources.
                                                                            In the case of chemistry lab automation, those resources
Fig. 3 Prompt skeleton: (1) At the initial generation, we prompt the        include experiment hardware and reagents.
LLM with a description of XDL and the natural language instruction.
(2) After the LLM generates structured-language-like output, we pass
it through our verifier. If there are errors in the generated program, we
concatenate the initial prompt with the XDL from the previous iteration     3.1.4 User interface
and a list of the errors. The full prompt can be viewed in “Appendix B”
                                                                            We provide a graphical user interface for CLAIRify to
                                                                            increase accessibility. Users can access it via a web browser
mentation. This evaluates if the input is syntactically correct             and CLAIRify is called by the Python backend implemented
XDL. The verifier also checks the existence of definitions of               in Flask (Grinberg, 2018). In Fig. 4, we show the user inter-
hardware and reagents used in the procedure or provided as                  face. The user enters an experiment (in the figure, we show
environment constraints, which works as a basic static anal-                Experiment 0 from the Chem-EDU dataset). After pressing
ysis of necessary conditions for executability. If the verifier             the Translate button, the interface shows the execution log
catches any errors, the candidate task plan is considered to                and generated XDL in the right panel with syntax highlight-
be invalid. In this case, the verifier returns a list of errors it          ing. The time taken to generate XDL from a natural language
found, which is then fed back to the generator. The role of the             using CLAIRify is mainly dependent on the OpenAI server
verifier is limited to pointing out the errors, and it does not             response time and the number of times the generator is called.
propose how to fix them. To propose a correct modification,                 For the experiment in Fig. 4, we measured the translation
the verifier requires an understanding of the meaning of the                time. These measurements were performed on three separate
input. However, semantic understanding is beyond the ability                occasions, spanning different days and times. On average, the
of a rule-based system. Therefore, in CLAIRify, the LLM-                    generation process took approximately 33 ± 3 s per iteration
based generator fixes the errors using the feedback messages                and required two generator calls.


123
Autonomous Robots (2023) 47:1057–1086                                                                                                         1065


Algorithm 2 TampForLabAutomation()                                                until all goals are satisfied, ensuring that the returned plan is
Input: A XDL recipe χ , sensory input H, PDDLStream domain D                      valid and executable by the robot. We define four types of
Output: Reference plan to execute
1: Goals, O ←xdlParser(χ )                                             Objects   actions in our PDDLStream domain: pick, move, place, and
2: I ← perception(H, O)                                     Initial conditions   pour. For example, the move action translates the robot end-
3: if not passConditions(I, O) then return
4: plan = ∅, P = ∅                                                                effector from a grasping pose to a placing or pouring pose
5: for all G ∈ Goals do                                                           using constrained motion planning. PDDLStream handles
6: while time() ≤ tmax do
7:       P = optimisticPddlStreamPlan(I, G, D)                                    continuous motion using streams. Streams generate objects
8:       if P = ∅ and isStreamFeasible(P) then break
9: end while
                                                                                  from continuous variables that satisfy specified conditions,
10: if P = ∅ then return                                                          such as feasible grasping pose and collision-free motion. An
11: plan ← plan ∪ P
12: I = updateSceneRepresentation(I , P)                                          instance of a stream has a set of certified predicates that
13: end for                                                                       expands I and functions as preconditions for other actions.
14: return plan
                                                                                     A PDDLStream problem is solved by invoking a classical
                                                                                  PDDL planner, such as Fast Downward (Helmert, 2006), with
                                                                                  optimistic instantiation of streams (line 7, Algorithm 2). If a
3.2 Task and motion planning for chemistry                                        plan for the PDDL problem is found, the optimistic stream
    experiments                                                                   instances s ∈ S in the plan are evaluated to determine the
                                                                                  actual feasibility (line 8). If no plan was found or the streams
Our task plan execution framework consists of three com-                          are not feasible, other plans are explored with a larger set of
ponents: perception, task and motion planning (TAMP), and                         optimistic stream instances.
a set of manipulation skills, as shown in Fig. 2b. XDL input
coming from CLAIRify provides a high-level description of                         Chemical description language (XDL) XDL is based on
experiment instructions to the TAMP module. The percep-                           XML syntax and is mainly composed of three mandatory
tion module updates the scene description by detecting the                        sections: Hardware, Reagents, and Procedure. We parse XDL
objects and estimating their positions using fiducial markers.                    instructions and pass them to the TAMP module. The Hard-
We used AprilTag (Olson, 2011). Currently, we assume prior                        ware and Reagents sections are parsed as initial objects O.
knowledge of vessel contents and sizes, and each vessel is                        Procedure is translated into a set of goals Goals (line 1, Algo-
mapped to a unique marker ID. Given the instructions from                         rithm 2). I is generated from O and sensory inputs (line 2).
XDL and the instantiated workspace state information from                         Each intermediate goal G ∈ Goals is processed by PDDL-
perception, a sequence of high-level actions and robot tra-                       Stream (line 5). If a plan to attain G is found, it is stored
jectories are simultaneously generated by our PDDLStream                          (line 10) and I is updated according to the plan (line 11).
TAMP solver (Yoshikawa et al., 2023). The resulting plan                          After a set of plans to attain all goals is found, we obtain a
is then realized by the manipulation module and robot con-                        complete motion plan (line 12).
troller, while closing the loop with perception feedback, such
as updated object positions and status of the solution.
                                                                                  Plan refinement at execution time We adopt two consid-
    The TAMP module converts experiment instructions given
                                                                                  erations for the dynamic nature of chemistry experiments:
by XDL into PDDLStream goals and generates a motion plan.
                                                                                  motion plan refinement and task plan refinement.
The TAMP algorithm is shown in Algorithm 2.
                                                                                     The generated motion plan is refined to reflect the updated
                                                                                  status of the scene and to overcome perception errors. The
3.2.1 PDDLStream                                                                  initial object pose detection may contain errors, therefore,
                                                                                  the object may not be present in the expected position during
A PDDLStream problem described by a tuple (P, A, S, O, I,                         execution. This error arises for two reasons. First, when the
G) is defined by a set of predicates P, actions A, streams                        robot interacts with the objects in the workspace, their posi-
S, initial objects O, an initial state I, and a goal state G.                     tion changes, for example when regrasping an object after
A predicate is a boolean function that describes the logical                      placing it in the workspace. This change is not always fore-
relationship of objects. A logical action a ∈ A has a set                         seeable by the planner ahead of time. Second, the perception
of preconditions and effects. The action a can be executed                        error is lower when the grasping pose is estimated when the
when all the preconditions are satisfied. After execution, the                    robot in-hand camera is closer to the target object, consider-
current state changes according to the effects. The set of                        ing the hand-eye calibration error. Lowering the perception
streams, S, distinguishes a PDDLStream problem from tra-                          error makes the execution more robust to grasping failures.
ditional PDDL. Streams are conditional samplers that yield                        Therefore, to improve the success rate, the object pose is
objects that satisfy specific constraints. The goal of PDDL-                      estimated just before grasping, and the trajectory is refined.
Stream planning is to find a sequence of logical actions and                      We assume that the perturbation of the perceived state of
a continuous motion trajectory starting from the initial state                    the objects is bounded so that it does not cause a change


                                                                                                                                        123
1066                                                                                          Autonomous Robots (2023) 47:1057–1086


in the logical state of the system, which would necessitate        The implicit nature of the manifold prevents planners from
task-level replanning.                                             directly sampling since the distribution of valid states is
   In addition to motion refinement, we consider task plan         unknown. Further, since the constraint manifold resides in
refinement. Task execution can be repeated using the feed-         a lower dimension than the configuration space, sampling
back from perception modules at execution time to support          valid states in the configuration space is highly improbable
conditional operations in chemistry experiments, such as           and thus impractical. Following the constrained motion plan-
adding acid until pH reaches 7. The number of repetitions          ning framework developed in (Kingston et al., 2019, 2018),
required to satisfy conditions is unknown at planning time,        our framework integrates the projection-based method for
so the task plan is refined at execution time.                     finding constraint-satisfying configurations during sampling
                                                                   as described in Algorithm 3. In this work, the constraints are
3.2.2 Motion constraints for spillage prevention                   set to the robot end-effector, hence they can be described with
                                                                   geometric forward kinematics, with its Jacobian defined as
                                                                               F
Unlike pick-and-place of solid objects, robots in a chemistry      J (q) = δδq   . After sampling from Q f r ee in line 5, projected
lab need to carry beakers that contain liquids, powders, or        configurations q are found by minimizing F (q) iteratively
granular materials. These chemicals are sometimes harmful,         using Newton’s method (highlighted in grey). We use prob-
so the robot motion planner should incorporate constraints         abilistic roadmap methods (PRM ) to plan efficiently in the
to prevent spillage. To this end, an important requirement for     8-DoF configuration space found in our chemistry laboratory
robot motion is the orientation constraints of the end-effector.   domain (Karaman & Frazzoli, 2011; Kavraki et al., 1996).
To avoid spillage, the end-effector orientation should be kept        The constrained path planning problem is sensitive to
in a limited range while beakers are grasped. We incorpo-          the start and end states of the requested path, since paths
rated constrained motion planning in the framework to meet         between joint states may not be possible under strict or mul-
these safety requirements, under the assumption of velocity        tiple constraints. If constrained planning is executed with
and acceleration upper bounds. Moreover, we introduced an          any arbitrary valid solution from the IK solver, the planner
additional (8th) degree of freedom to the robot arm, in order      typically fails. To address this shortcoming, three consider-
to increase the success rate of constrained motion planning.       ations are made. First, a multi-threaded IK solver with both
We empirically observed no spillage as long as orientation         iterative and random-based techniques is executed, and the
constraints are satisfied in the regular acceleration and veloc-   solution that minimizes an objective function φ is returned
ity of the robot end-effector, particularly since beakers are      with TRAC-IK, proposed in (Beeson & Ames, 2015). Dur-
typically not filled to their full capacity in a chemistry lab.    ing grasping and placing, precision is paramount, and we
                                                                   only seek to minimize the sum-of-squares error between
                                                                   the start and goal Cartesian poses. Second, depending on
Algorithm 3 ConstrainedMotionPlanning()                            the robot task, the objective function is extended to maxi-
1: for all i ∈ trials do
2: q g ← solveIK((I pB ,I RB ))                                    mize the manipulability ellipsoid as described in (Yoshikawa,
3: pathPlanner← init(q 0 , q g )                                   1985), which is applied for more complicated maneuvers,
4: while path is ∅ do                                              such as transferring liquids across the workspace. Finally,
5:       q ← sample()
6:       while F (q) >  do                                        note that configuration sampling must account for the fact
7:          δq ← J † (q)F (q)
8:           q ← q − δq
                                                                   that multiple goal configurations are possible. For this pur-
9:       end while                                                 pose, Algorithm 3 can iterate several times to find various
10:        path ← pathPlanner(q)
11: end while                                                      goal configurations in line 2.
12: if path = ∅ then return path
13: end for
14: return path                                                    8-DoF robot arm To increase the success rate of planning
                                                                   and grasping under non-spillage constraints, we introduced
                                                                   an additional degree of freedom to the 7-DoF Franka robot
                                                                   and mounted the end-effector parallel to the floor as shown
Constrained motion planning Given a robot with n degrees           in the bottom right of Fig. 2b. The parallel grasping and
of freedom in the workspace Q ∈ Rn with obstacle regions           introduction of a revolute joint facilitate the manipulation
Qobs ∈ Rn , the constrained planning problem can be                of liquids within beakers. Parallel grasping, where the grip-
described as finding a path in the manipulator’s free con-         per is horizontal, is advantageous over top-down grasping to
figuration space Q f r ee = Q − Qobs that satisfies initial        pour liquids because the robot hand does not touch the rim
configuration q 0 ∈ Rn , end-effector goal pose (I pB ∈            of a beaker and does not block the flow of liquid. Frequently,
R3 ,I RB ∈ S O(3)), and equality path constraints F (q) :          when planning constrained motion, the initial 7-DoF robot
Q → Rk . The constrained configuration space can be repre-         arm would encounter joint limit issues with parallel grasping
sented by the implicit manifold M = {q ∈ Q | F (q) = 0}.           poses, rendering the subsequent pouring action impractical.


123
Autonomous Robots (2023) 47:1057–1086                                                                                                1067


It is possible to achieve parallel grasping by adjusting the
angle of the end-effector without adding an extra revolute
joint by connecting the end-effector with a rigid link to the
robot. However, the integration of a servo motor directly
before the gripper facilitates pouring control, as it enables
the accomplishment of pouring actions using a single motor.
Limiting the pouring motion to the last joint is also advan-
tageous for the safety of humans near the robot because
pouring motion sometimes entails quick rotations. Mount-
ing the robot base on the wall instead of the default tabletop
placement is another possible solution to parallel grasping,
but it is not supported by the manufacturer. In addition to the
advantage in pouring, the 8-DoF robot has a higher empiri-
cal success rate in constrained motion planning in the parallel    Fig. 5 Pouring skill controller: given the XDL and TAMP reference
grasping pose, as shown in Sect. 4.4.2, which leads to a higher    values and sensor feedback, the pouring controller computes the end-
success rate in total task and motion planning. As a result,       effector velocity for the robot by blending a shaping function s(t) and
                                                                   a PD control output v P D (t)
adding one degree of freedom was the most suitable solution
for our purpose.

3.2.3 Manipulation and perception skills

Chemistry lab skills require a particular suite of sensors,
algorithms, and hardware. We provide an interface for
instantiating different skill instances through ROS and simul-
taneously commanding them. For instance, recrystallization
experiments in chemistry require pouring, heating, and stir-
ring, which uses both weight feedback for volume estimation
and skills for interacting with the liquid using available hard-
ware.
                                                                   Fig. 6 An example of pouring control. The velocity of the end-effector
                                                                   is controlled based on the feedback error and shaping function
Pouring controller In chemistry labs, a frequently used skill
in chemical experiments is pouring. Pouring involves high
intra-class variations depending on the underlying objective       to stabilize, and pouring is a non-reversible action, chemists
(e.g., reaching a desired weight or pH value); the substances      tend to conservatively pour a small amount of content from
and material types being handled (e.g., granular solids or         the pouring vessel into the target vessel. They periodically
liquids); the glassware being used (e.g., beakers and vials);      wait for some time to observe any effects and then pour
the overall required precision; and the availability of accu-      micro-amounts again. In our approach, we use a shaping
rate and fast feedback. Pouring is a closed-loop process, in       function s(t) to guide the direction and frequency of this
which feedback should be continuously monitored. Among             oscillatory pouring behavior, while a PD controller lowers the
these pouring actions, in our work, we consider the follow-        pouring error. The end-effector velocity vector is computed
ing variations: pouring of liquids and pouring of granular         by blending the shaping function s(t) over the PD control sig-
solids. Note that, in contrast to many control problems, pour-     nal, v PD (t) = k p e + kd ė, where e(t) = xr e f − x f b . Figure 6
ing is a non-reversible process where we cannot compensate         shows an example of the angular velocity of the end-effector
for overshoot (as the poured material cannot go back to the        and the error during actual pouring. More information about
pouring beaker if mixed with another material).                    the pouring skill method can be found in “Appendix A”.
   Inspired by observations of chemists pouring reagents, we
propose a controller that allows the robot to perform differ-      Turbidity-based solubility measurement The solubility of a
ent pouring actions. As shown in Fig. 5, the proposed method       solute is measured by determining the minimum amount of
takes sensor measurements (e.g., weight feedback from the          solvent (water) required to dissolve all solutes at a given tem-
scale) as feedback and a reference pouring target. The algo-       perature when the overall system is in equilibrium (Shiri et
rithm outputs a robot end-effector joint velocity describing       al., 2021). Since the solutions get transparent when all solutes
oscillations of the arm’s wrist. Since sensors are character-      dissolve into water, turbidity, or opaqueness of the solution,
ized by measurement delays, chemical reactions require time        is used as the metric to determine the completion of the exper-


                                                                                                                              123
1068                                                                                                       Autonomous Robots (2023) 47:1057–1086


                                                                               4.1.1 Datasets

                                                                               We evaluated our method on two different datasets (Table 1):

                                                                               Chem-RnD (chemistry research and development) This
                                                                               dataset consists of 108 detailed chemistry-protocols for
                                                                               synthesizing different organic compounds in real-world
                                                                               chemistry labs, sourced from the Organic Syntheses dataset
                                                                               (volume 77) (Mehr et al., 2020a). Due to GPT-3 token limits,
                                                                               we only use experiments with less than 1000 characters. We
                                                                               use Chem-RnD as a proof-of-concept that our method can
                                                                               generate task plans for complex chemistry methods. We do
                                                                               not aim to execute the plans in the real world, and so we do
Fig. 7 An example of automated turbidity measurement. The cam-                 not include any constraints.
era detects the Petri dish using Hough Circle Transform. The average
brightness of the detected area (red square) is used as a proxy of turbidity
(Color figure online)                                                          Chem-EDU (everyday educational chemistry) We evaluate
                                                                               the integration of CLAIRify with real-world robots through
                                                                               a dataset of 42 natural language instructions containing
iment. The average brightness of the solution was used as a
                                                                               only safe (edible) chemicals and that are, in principle, exe-
proxy for the relative turbidity, inspired by HeinSight (Shiri
                                                                               cutable by our robot. The dataset consists of basic chemistry
et al., 2021). That work compared the current measured
                                                                               experiments involving edible household chemicals, includ-
turbidity value with a reference value (coming from pure sol-
                                                                               ing acid–base reactions and food preparation procedures.1
vent) to determine when the solute was dissolved. Differently
                                                                               We show some data samples in “Appendix C”. When gen-
from them, we use the relative turbidity changes between
                                                                               erating the XDL, we also included environment constraints
the current and previous measurement values to detect when
                                                                               based on what equipment our robot had access to (for exam-
the solution is dissolved. Moreover, to make the perception
                                                                               ple, our robot only had access to a mixing container called
pipeline autonomous, when the robot with an in-hand camera
                                                                               “beaker”).
observes the dish containing the solution, it detects the largest
circular shape as the dish using a Hough Circle Transform
implemented in OpenCV. The square region containing the                        4.1.2 Metrics and results
dish is converted into the HSV color space, and the average
Value (brightness) of the region is used as a turbidity value.                 The results section is organized based on the four perfor-
Figure 7 shows an example of the automated turbidity mea-                      mance metrics that we will consider, namely: Ability to
surement. Although the detected area contains the dish and                     generate structured-language output, Quality of the gener-
stir bar, they do not affect the relative value because these are              ated plans, Number of interventions required by the verifier,
a constant bias in all measurements.                                           and Robotic validation capability. We compared the perfor-
                                                                               mance of our method with SynthReader, a state-of-the-art
                                                                               XDL generation algorithm which is based on rule-based tag-
4 Experiments                                                                  ging and grammar parsing of chemical procedures (Mehr et
                                                                               al., 2020).
                                                                               1. Ability to generate a structured language plan. First,
4.1 XDL generation                                                             we investigate the success probability for generating plans.
                                                                               For CLAIRify, if it is in the iteration loop for more than
We conducted experiments to evaluate the following hypothe-                    x steps (here, we use x = 10), we say that it is unable to
ses: i) Automated iterative prompting increases the success                    generate a plan and we exit the program. When compar-
rate of unfamiliar language generation, ii) The quality of                     ing with SynthReader, we consider that approach unable to
generated task plans is better than existing methods. To gen-                  generate a structured plan if the SynthReader IDE (called
erate XDL plans, we use text-davinci-003, the most                             ChemIDE) throws a fatal error when asked to create a plan.2
capable GPT−3.5 model accessible using the OpenAI API                          For both models, we also consider them unable to generate
at the time of performing experiments (February 2023). We                      a plan if the generated plan only consists of empty XDL
chose to use this instead of code-davinci-002 due to
                                                                               1 CLAIRify Data & code: https://github.com/ac-rad/xdl-generation/.
query and token limits. Additionally, ChatGPT was not yet
available through the API at that time.                                        2 ChemIDE using XDL: https://croningroup.gitlab.io/chemputer/xdlapp/.




123
Autonomous Robots (2023) 47:1057–1086                                                                                                          1069


Table 1 Comparison of our
                                      Dataset             Method                                  Number generated ↑            Expert preference↑
method with existing methods
on the number of successfully         Chem-RnD            SynthReader (Mehr et al., 2020)         92/108                        13/108
generated valid XDL plans and
their quality on 108 organic                              CLAIRify [ours]                         105/108                       75/108
chemistry experiments from            Chem-EDU            SynthReader (Mehr et al., 2020)         0/42                          –
(Mehr et al., 2020a) by 10                                CLAIRify [ours]                         42/42                         –
expert chemists
                                      Results of the best-performing models for a given metric and dataset are given in bold




Fig. 8 Violin plots showing distributions of different error categories     half showing the number of errors in plans generated from CLAIRify
in XDL plans generated for experiments for the Chem-RnD (left) and          (teal) and the right half showing those from SynthReader (navy). For
Chem-EDU (right) datasets. The x-axis shows the error categories and        the Chem-EDU dataset, we only show the distributions for CLAIRify.
the y-axis shows the number of errors for that category (lower is bet-      In both plots, we show the mean of the distribution with a gold dot (and
ter). For the Chem-RnD dataset, we show the error distributions for both    the number beside in gold) and the median with a grey dot (Color figure
CLAIRify and SynthReader. Each violin is split in two, with the left        online)



tags (i.e., no experimental protocol). For all experiments, we              action, Wrong parameter, Ambiguous value, Other error.
count the total number of successfully generated language                   Here, actions refer to high-level steps in the procedure
plans divided by the total number of experiments. Using                     (e.g., <Add reagent=“acetic acid”> is an action)
this methodology, we tested the ability of the two models                   and parameters refer to reagents, hardware, quantities and
to generate output on both the Chem-RnD and Chem-EDU                        experiment descriptors (e.g., in <HeatChill vessel
datasets. The results for both models and both datasets are                 =“beaker” temp=“100C”>, vessel and temp are both
shown in Table 1. We find that out of 108 Chem-RnD exper-                   parameters).
iments, CLAIRify successfully returned a plan 97% of the                       The chemists were 10 graduate students and postdoctoral
time, while SynthReader returned a plan 85% of the time. For                fellows from the University of Toronto and ETH Zürich.
the Chem-EDU dataset, CLAIRify generated a plan for all                     For the first 20 experiments, the chemists labelled them
instructions. SynthReader was unable to generate any plans                  together as a group to resolve any labelling ambiguities and
for that dataset, likely because the procedures are different               then labelled the rest individually (approximately 9 experi-
from typical chemical procedures (they use simple action                    ments per chemist). The annotations were performed using
statements). This demonstrates the generalizability of our                  the LightTag Text Annotation Tool (Perry, 2021).
method: we can apply it to different language styles and
domains and still obtain coherent plans.
2. Quality of the predicted plan (without executing the
plan). To determine if the predicted task plans actually                    Chem-RnD dataset The results for the Chem-RnD dataset
accomplish every step of their original instructions, we                    with respect to expert preference are reported in the last col-
report the number of actions and parameters that do not                     umn of Table 1. We found that out of 108 experiments,
align between the original and generated plan, as anno-                     experts preferred the XDL plan generated from CLAIRify
tated by expert experimental chemists. To compare the                       75 times and the one from SynthReader 13 times (the remain-
quality of the generated plans between CLAIRify and                         ing 20 were considered to be of similar quality).
SynthReader, we ask expert experimental chemists to,                           The distributions of the annotated errors are shown in
given two anonymized plans, either pick a preferred plan                    Fig. 8. We find that for 4 out of 6 error categories, our model
among them or classify them as equally good. We also                        does at least as well as or better than the baseline method
ask them to annotate errors in the plans in the follow-                     when considering the mean and median of the distributions.
ing categories: Missing action, Missing parameter, Wrong                    We also find that for those categories, our method produces
                                                                            more experiments with 0 errors.


                                                                                                                                         123
1070                                                                                                         Autonomous Robots (2023) 47:1057–1086


   One advantage of our method is that it generates less plans                    For example, given the instruction “Dry solution over mag-
with missing actions compared with the baseline. As XDL                           nesium sulfate”, our model inserts a <Dry.../> into the
generation in SynthReader is implemented by rule-based                            XDL plan, dbut the instruction is actually referring to a
pattern-matching techniques, any actions that do not match                        procedure where one passes the solution through a short car-
those templates would not appear in the final XDL. For exam-                      tridge containing magnesium sulphate, a procedure which
ple, for the protocol:                                                            seems to be encoded in SynthReader. Another wrong action
To a s o l u t i o n of m - CPBA (200 mg , 0.8 mmol )                             our model performs is reusing vessels. In chemistry, one
in d i c h l o r o m e t h a n e (10 mL ) , c o o l e d to 0 ◦ C ,                needs to ensure a vessel is uncontaminated before using it.
was a d d e d d r o p w i s e a s o l u t i o n of 5 - chloro
-10 - oxa -3 - thia - t r i c y c l o [5.2.1.01 , 5] dec -8 -                     However, our model generates plans that can use the same
ene (150 mg , 0.8 mmol ) in d i c h l o r o m e t h a n e
(10 mL ) .                                                                        vessel in two different steps without washing it in between.
                                                                                  Our model also sometimes generates plans with ambigu-
the plan generated by CLAIRify was                                                ous values. For example, many experiment descriptions
< Add v e s s e l = " V1 " r e a g e n t = "m - CPBA " a m o u n t = "            include conditional statements such as “Heat the solution
200 mg " / >
< Add v e s s e l = " V1 " r e a g e n t = " d i c h l o r o m e t h a n e "      at the boiling point until it becomes white”. Conditions
v o l u m e = " 10 mL " / >                                                       in XDL need a numerical condition as a parameter. Our
< H e a t C h i l l v e s s e l = " V1 " temp = " 0 ◦ C " time = " 3
min " / >                                                                         model tries to incorporate them by including actions such
< Add v e s s e l = " V2 " r e a g e n t = " 5 - chloro -10 - oxa -3 -
thia - t r i c y c l o [5 ,2 ,1 ,0*1 ,5*] dec -8 - ene " a m o u n t              as <HeatChill temp=“boiling point” time =
= " 150 mg " / >                                                                  “until it becomes white”/>, but they are ambigu-
< Add v e s s e l = " V2 " r e a g e n t = " d i c h l o r o m e t h a n e "
v o l u m e = " 10 mL " / >                                                       ous. We can make our model better in the future by
< T r a n s f e r f r o m _ v e s s e l = " V2 " t o _ v e s s e l = " V1 " / >   incorporating more domain knowledge into our structured
while the plan generated from SynthReader was                                     language description and improving our verifier with real-
< Add v e s s e l = " r e a c t o r " r e a g e n t = " 5 - chloro -10 -
                                                                                  world constraints. For example, we can incorporate visual
oxa -3 - thia - t r i c y c l o " v o l u m e = " 0 " speed = " 40.0 "            feedback from the environment, include look-up tables for
/>
                                                                                  common boiling points, and ensure vessels are not reused
   Our model is able to decompose a complicated procedure                         before cleaning. Other errors include misunderstanding nota-
into simpler actions by making two solutions in separate                          tions commonly used in chemistry experiments. For instance,
beakers and combining them with a Transfer procedure. It                          instructions such as “Wash with EtOAc (2 × 10 mL)” indi-
also assumes that the solutions don’t already exist as mix-                       cate the need for two separate WashSolid() actions in
tures and creates them from scratch. This is another benefit                      XDL. However, the large language model often struggles to
of our model, as it is able to understand implicit actions. For                   parse the (2 × 10 mL) notation correctly, resulting in either
example, given the prompt                                                         performing a single WashSolid() action with 10 mL (or
L - O r n i t h i n e ( 3 1 . 9 2 g , 120 mmol ) was added to                     occasionally 20 mL if a multiplication action is inferred) or
  a m i x t u r e of KOH ( 6 . 7 2 g , 120 mmol ) , water                         (more rarely) omitting the action entirely.
(200 ml ) and THF (100 ml )
                                                                                     Another cause of errors occurs when a specific value is
SynthReader considers a mixture of three chemicals as a sin-                      not provided in the instruction. For example, if an instruc-
gle solution and creates the action:                                              tion states “wash product in EtOAc” without specifying a
< Add v e s s e l = " r e a c t o r " r e a g e n t = " a m i x t u r e of        volume, the model is unable to generate a reasonable value
KOH (6.72 g , 120 mmol ) , water (200 ml ) and
THF (100 ml ) " v o l u m e = " 0 " speed = " 40.0 " / >                          and defaults to writing 0 mL in the generated plan.
< A d d S o l i d v e s s e l = " r e a c t o r " r e a g e n t = "L -               Despite the XDL plans generated by our method contain-
O r n i t h i n e " mass = " 31.92 g " / >
                                                                                  ing errors, we found that the experts placed greater emphasis
On the other hand, CLAIRify correctly understand the                              on missing actions than ambiguous or wrong actions when
implicit action to mix them beforehand and generates an                           picking the preferred output, indicating larger severity of this
appropriate XDL:                                                                  class of error for the tasks and outputs investigated here.
< Add v e s s e l = " V1 " r e a g e n t = "L - O r n i t h i n e "
a m o u n t = " 31.92 g " / >                                                     Chem-EDU dataset We annotated the errors in the Chem-
< Add v e s s e l = " V1 " r e a g e n t = " KOH " a m o u n t = " 6.72
g"/>                                                                              EDU datasets using the same annotation labels as for the
< Add v e s s e l = " V1 " r e a g e n t = " Water " a m o u n t = " 200
  ml " / >                                                                        Chem-RnD dataset. The breakdown of the errors is in the
< Add v e s s e l = " V1 " r e a g e n t = " THF " a m o u n t = " 100            right plot of Fig. 8. Note that we did not perform a comparison
ml " / >
                                                                                  with SynthReader as no plans were generated from it. We find
   However, our model produced plans with a greater num-                          that the error breakdown is similar to that from Chem-RnD,
ber of wrong actions than SynthReader. This is likely because                     where we see amibiguous values in experiments that have
our model is missing domain knowledge on certain actions                          conditionals instead of precise values. We also encounter
that would need to be included in the prompt or verifier.                         a few wrong parameter errors, where the model does not


123
Autonomous Robots (2023) 47:1057–1086                                                                                                    1071


Table 2 Verifier analysis
                                  Dataset           Average num.         Max/min            Error type caught by verifier [count]
                                                    verifier calls       verifier calls

                                  Chem-RnD          2.58 ± 2.00          10/1               Missing property in action [306]
                                                                                            Property not allowed [174]
                                                                                            Wrong tag [120]
                                                                                            Action does not exist [21]
                                                                                            Item not defined in hardware or reagents list [15]
                                                                                            Plan cannot be parsed as XML [6]

                                  Chem-EDU          1.14 ± 0.47          3/1                Item not defined in hardware or reagents list [47]
                                                                                            Property not allowed [26]
                                                                                            Wrong tag [40]
                                                                                            Missing property in action [3]

                                  We report the average number of times CLAIRify calls the verifier for the experiments in a given dataset, as
                                  well as the minimum and maximum number of times. We also report the type of error encountered by the
                                  verifier and the number of times it caught that type




include units for measurements. This can be fixed in future            XM540-W150 servo motor. Figure 2 shows the hardware
work by improving the verifier to check for these constraints.         setup.
3. Number of interventions required by the verifier. To
better understand the interactions between the generator and           Lab tools integration The robot framework is expanded
verifier in CLAIRify, we analyzed the number of interac-               by incorporating lab tools. We used an IKA RET control-
tions that occur between the verifier and generator for each           visc device, which works as a scale, hotplate, and stir plate,
dataset to understand the usefulness of the verifier. In Table 2,      and a Sartorius BCA2202-1 S Entris, which works as a high-
we show that each experiment in the Chem-RnD dataset                   precision weighing scale. The devices communicate with the
runs through the verifier on average 2.6 times, while the              TAMP solver to execute chemistry specific skills.
Chem-EDU dataset experiments runs through it 1.15 times
on average. The difference between the two datasets likely
                                                                       Software The robot is controlled using FrankaPy (Zhang
exists because the Chem-EDU experiments are shorter and
                                                                       et al., 2020). We implemented a ROS wrapper for the
less complicated. The top Chem-EDU error encountered by
                                                                       servo motor (8th DoF). To detect fiducial markers, we use
the verifier was that an item in the plan was not defined in
                                                                       the AprilTag library (Olson, 2011). We use the MoveIt
the Hardware or Reagents list, mainly because we included
                                                                       motion planning framework (Coleman et al., 2014) for our
hardware constraints for this dataset that we needed to match
                                                                       TAMP solver and its streams. The constrained planning func-
in our plan. In Fig. 9, we show a sample loop series between
                                                                       tion (Kingston et al., 2019) is an extension of elion.3
the generator and verifier.

4.2 Robot execution                                                    4.2.2 Solution color change based on pH

To analyze how well our system performs in the real world,             As a basic chemistry experiment, we demonstrated the color
we execute a few experiments from the Chem-EDU dataset                 change of a solution containing red cabbage juice. This is a
on our robot. Three experiments from the Chem-EDU dataset              popular introductory demonstration in chemistry education,
were selected to be executed.                                          as the anthocyanin pigment in red cabbage can be used as a
                                                                       pH indicator (Fortman & Stubbs, 1992). We prepared red cab-
4.2.1 Experiment setup                                                 bage solution by boiling red cabbage leaves in hot water. The
                                                                       colour of the solution is dark purple/red. Red cabbage juice
Hardware The proposed lab automation framework has                     changes its color to bright pink if we add an acid and to blue
been evaluated using the Franka Emika Panda arm robot,                 if we add a base, and so we acquired commercially-available
equipped with a Robotiq 2F-85 gripper and an Intel RealSense           vinegar (acetic acid, an acid) and baking soda (sodium bicar-
D435i stereo camera mounted on the gripper to allow for                bonate, a base).
active vision. The robot’s DoF has been extended by one
degree (in total 8-DoF) at its end-effector using a Dynamixel          3 https://github.com/JeroenDM/elion.




                                                                                                                                    123
1072                                                                                                    Autonomous Robots (2023) 47:1057–1086




Fig. 9 Feedback loop between the Generator and Verifier. The input        that previous errors were fixed and the tags could be processed, new
text is converted to structured-like language via the generator and is    errors were found (including a constraint error that the plan uses a ves-
then passed through the verifier. The verifier returns a list of errors   sel not in the environment). These errors are denoted with a blue 2. This
(marked with a yellow 1). The feedback is passed back to the generator    feedback loop is repeated until no more errors are caught, which in this
along with the erroneous task plan, generating a new task plan. Now       case required 3 iterations (Color figure online)



  In this experiment, we generated XDL plans using                        4.2.4 Solubility measurement
CLAIRify from two language inputs:
                                                                          We finally measured the solubility of household solutes as
[1] Add 40 g of red c a b b a g e s o l u t i o n into a
beaker . Add 10 g of acetic acid into the                                 an example of basic educational chemistry experiments for
beaker , then stir the s o l u t i o n for 10                             students (Wolthuis et al., 1960). Measuring solubility has
seconds .
                                                                          desirable characteristics as a benchmark for automated chem-
[2] Add 40 g of red c a b b a g e s o l u t i o n into a                  istry experiments: (i) it requires basic chemistry operations,
beaker . Add 10 g of baking soda into the                                 such as pouring, solid dispensing, and observation of the
beaker , then stir the s o l u t i o n for 10
seconds .                                                                 solution status, (ii) solubility can be measured using ubiqui-
                                                                          tous food-safe materials, such as water, salt, sugar, and (iii)
   Figure 10 shows the flow of the experiment. Our system                 the accuracy of the measurement can be evaluated quantita-
generated a XDL plan that correctly captured the experiment;              tively by comparing with literature values. We measured the
the plan was then passed through TAMP to generate a low-                  solubility of three solutes: table salt (sodium chloride), sugar
level action plan and was then executed by the robot.                     (sucrose), and alum (aluminum potassium sulfate).
                                                                              The robot estimates the amount of water to make a satu-
                                                                          rated solution by repeatedly pouring a small amount of water.
4.2.3 Kitchen chemistry                                                   After pouring, the solution is stirred and the turbidity before
                                                                          and after stirring was compared. The turbidity decreases by
We then tested whether our robot could execute a plan                     stirring if the remaining solutes dissolved into water, whereas
generated by our model for a different application of house-              it stays at a constant value if there are no residues. If the tur-
hold chemistry: food preparation. We generated a plan using               bidity decrease after the N -th pouring is smaller than 5%,
CLAIRify for the following lemonade beverage, which can                   we assume there were no residues at the beginning of N -th
be viewed on our website:                                                 pouring and that the amount of water required to dissolve all
                                                                          solutes is between the volume of water added at the (N − 2)-
Add 15 g of lemon j u i c e and s u g a r m i x t u r e to
 a cup c o n t a i n i n g 30 g of s p a r k l i n g water .              th and (N − 1)-th pouring. We use the average of the two
Stir v i g o r o u s l y for 20 sec .                                     for simplicity of presentation. Figure 13 shows an example
                                                                          of turbidity change during the experiment.
   Figure 11 shows the flow of an experiment. Since we                        A natural language explanation for the above solubility
deal with edible material, we implemented a different stir-               measurement protocol is as follows:
ring motion that does not touch the content of the container.


123
Autonomous Robots (2023) 47:1057–1086                                                                                                       1073




Fig. 10 Robot execution: The robot executes the motion plan generated from the XDL for given natural language input. a CLAIRify converts the
natural language input from the user into XDL. b The robot interprets XDL and performs the experiment. Stirring is done by a rotating stir bar
inside the beaker




Fig. 11 Kitchen chemistry: The robot executes the motion plan generated from the XDL for given natural language input. a CLAIRify converts
the natural language input from the user into XDL. b The robot interprets XDL and performs the experiment. Stirring is done by shaking a cup with
the robot arm


Add 10 g of salt to the beaker .                                             The primary reason for the difference from the literature
R e p e a t the f o l l o w i n g steps for five times .
Add 10 g of water into the beaker , and                                   value is the range of minimum amount of water required
m e a s u r e the t u r b i d i t y .                                     for dissolving. In an example of turbidity change shown in
After s t i r r i n g for 90 seconds , m e a s u r e the
t u r b i d i t y again .                                                 Fig. 13, the robot can only tell the second pouring is insuffi-
                                                                          cient and the third pouring is sufficient to dissolve all solutes,
                                                                          but it cannot tell the exact required amount. As a result, the
    Note that we extended the XDL to allow turbidity as a mea-
                                                                          solubility measurement inherently includes error caused by
surable quantity of <Monitor> since the XDL standard at
                                                                          the resolution of pouring. We can reduce the error by pouring
the time of writing (XDL 2.0.1) only supports temperature
                                                                          a smaller amount of water at once, but pouring less than 10 g
and pH. We added this skill to our defintion of XDL that we
                                                                          is difficult because of the delayed feedback of the scale and
input to the LLM in CLAIRify. The amount of solute and
                                                                          the scale minimum resolution. We can improve the accuracy
stirring time were changed for different solutes. The work-
                                                                          of solubility measurements by developing a pipette designed
flow of the solubility experiments is shown in Fig. 12.
                                                                          for a robot.
    The measured solubility for three solutes is shown in
Table 3. The robot framework managed to measure the sol-
ubility with sufficient accuracy that they are comparable to
solubility values found in the literature (NAOJ, 2022).


                                                                                                                                     123
1074                                                                                                          Autonomous Robots (2023) 47:1057–1086




Fig. 12 Workflow of solubility experiment. a We translate a natural            into the dish. The solution is mixed with the magnetic stirrer. After stir-
language input to XDL using CLAIRify. b We then execute the plan               ring, the turbidity of the solution is measured to check dissolvement.
on a robot using TAMP. First, a fixed amount of the solute is added to         If undissolved, another 10 g of water is added until no solutes remain.
the dish on the weighing scale and stirrer. The robot pours 10 g of water      The experiment was conducted at room temperature (25◦ C)



Table 3 Results of the solubility experiments                                  temperatures. Typically, solutes have higher solubility at high
Solute    Solute (g)     Water (g)     Solubility    Lit.      % error         temperatures, meaning hot solvents will dissolve more solute
                                                                               than cool solvents. The excess amount of solute that cannot
Salt      13.9           41.8          33.2           35.8     7.2             be dissolved anymore while cooling the solvent precipitates
Sugar     60.00          26.46         226.8         203.9     11.2            and forms crystals. We tested the recrystallization of alum by
Alum      3.00           29.87         10.0          11.4      12.3            changing the temperature of the water. Alum was chosen as
Amount of solute in the beaker, amount of water to dissolve all solute,        the target solute since its solubility greatly changes accord-
calculated solubility (the amount of solute dissolved per 100 g of water),     ing to water temperature. The recrystallization experiment
and literature data (lit.) for solubility at 20◦ C is shown. Literature data   setup extends the solubility test by pre-heating the solvent.
are taken or calculated from (NAOJ, 2022)
                                                                               A natural language explanation for the above recrystalliza-
                                                                               tion experiment protocol is as follows:

4.2.5 Recrystallization experiment

Recrystallization is a purifying technique to obtain crystals
of a solute by using the difference in solubility at different


123
Autonomous Robots (2023) 47:1057–1086                                                                                                        1075


                                                                            i n i t i a l _ p r o m p t = """
                                                                            C o n v e r t to XDL :
                                                                            # < N a t u r a l l a n g u a g e i n s t r u c t i o n > """

                                                                                The LLM was unable to generate XDL for any of the
                                                                            inputs from the small validation set that contains 10 chem-
                                                                            istry experiments. For most experiments, when asked to
                                                                            generated XDL, the model output a rephrased version of
                                                                            the natural language input. In the best case, it output some
                                                                            notion of structure in the form of S-expressions or XML tags,
                                                                            but the outputs were very far away from correct XDL and
                                                                            were not related to chemistry. We tried the same experiment
                                                                            with code-davinci-002; the outputs generally had more
                                                                            structure but were still nonsensical. This result suggests the
Fig. 13 Turbidity change during experiment. Water is poured into the        LLM does not have the knowledge of the target language and
dish during pouring (grey) and turbidity is measured during observation     including the language description in the prompt is essential
(blue). The end of the experiment is determined by turbidity comparison.    to generate an unfamiliar language.
In this example, all solutes are dissolved at the third pouring because
the turbidity change after the fourth pouring is below the threshold. The
average weight of the second and third pouring is used to calculate the     4.3.2 Feedback design
solubility (Color figure online)
                                                                            We experimented with prompts in our iterative prompting
Fig. 14 Recrystallization of
                                                                            scheme containing various levels of detail about the errors.
alum inside the water. After
heating water by putting a                                                  The baseline prompt contains a description as well as the
beaker with water on a hotplate,                                            natural language instruction. We wanted to investigate how
the robot poured alum into a                                                much detail is needed in the error message for the generator
dish. The robot then poured hot
                                                                            to be able to fix the errors in the next iteration. For example,
water, and the solution was
heated and stirred. The                                                     is it sufficient to write “There was an error in the generated
formation of a precipitate is                                               XDL", and do we need to include a list of errors from the
observed after the dish is cooled                                           verifier (such as “Quantity is not a permissible attribute for
down. The dried crystals in a
                                                                            the Add tag"), or do we also need to include the erroneous
vial are shown
                                                                            XDL from the previous iteration? We also wanted to keep any
                                                                            feedback messages as general as possible to reduce prompt
Add 50 g of w a t e r to b e a k e r .                                      lengths, considering there is a limit for how many tokens we
H e a t the b e a k e r f i l l e d w i t h w a t e r for 1 min             can query OpenAI models with.
to 60 C .
Add 20 g of alum into an e m p t y beaker , and
                                                                                The XDL generation success rate for different error mes-
add 50 g of the h e a t e d w a t e r i n t o the b e a k e r .             sage designs is shown in Table 4. We find that including the
C o o l the b e a k e r for 30 min to 20 C .                                erroneous XDL from the previous iteration and specifying
                                                                            why it was wrong resulted in the highest number of success-
   Figure 14 shows the result of the experiment.
                                                                            fully generated XDL plans. Including a list of errors was
                                                                            better than only writing “This XDL was not correct. Please
4.3 Ablation studies                                                        fix the errors”, which was not informative enough to fix any
                                                                            errors. Including the erroneous XDL from the previous iter-
We assess the impact of various components in our prompt                    ation is also important; we found that including only a list
designs and feedback messaging from the verifier. We per-                   of the errors without the context of the XDL plan resulted in
formed these tests on a small validation set of 10 chemistry                low success rates.
experiments from Chem-RnD (not used in the test set) and
report the number of XDL plans successfully generated (i.e.,                4.4 Component analysis for robot execution
was not in the iteration loop for x = 10 steps).
                                                                            4.4.1 Pouring skill evaluation
4.3.1 Prompt design
                                                                            We evaluated the accuracy and efficiency of the pouring skill
To evaluate the prior knowledge of the GPT-3 on XDL, we                     for liquid and powder. To evaluate the effect of our pro-
first tried prompting the generator without a XDL descrip-                  posed pouring method, we implemented a PD control pouring
tion, i.e., with the input:                                                 method where end-effector angular velocity is proportional to


                                                                                                                                            123
1076                                                                                                       Autonomous Robots (2023) 47:1057–1086


Table 4 Number of XDL plans successfully generated for different error message designs in the iterative prompting scheme on a validation set
from Chem-RnD consisting of 10 experiments
Variations of iterative prompt design using verifier error messages                                              Plan’s generated success rate (%)↑

Naive: XDL from previous iteration and string “This XDL was not correct. Please fix the errors.”                 0
Last error: Error list from verifier from previous iteration                                                     30
All errors cumulative: Accumulated error list from all previous iterations                                       50
XDL + Last error: XDL and error list from verifier from previous iteration                                       100



the difference between target and feedback weight as a base-                 are randomly sampled. Scenario (2) extends the first with
line. Figure 15 shows the pouring experiment results. The                    an additional intermediate sampled waypoint. For each sce-
results show that the shaping function contributed to reduc-                 nario, we run 50 trials in Algorithm 3 with random seeding
ing the overshooting compared to PD control pouring. The                     of the IK solver.
overshoot of the PD control pouring is mainly because of
the scale’s delayed feedback (∼3 s). The intermittent pour-
ing caused by the shaping function compensated for the delay
and improved the overall pouring accuracy. On average, the
pouring errors using the shaping approach for water and salt
were 2.2 ± 1.5 g (8.1 ± 4.8 %) and 2.1 ± 1.4 g (8.8 ± 6.2 %).
The errors for PD control were 24.5 ± 12.0 g (81.4 ± 4.5 %)
and 7.7 ± 4.3 g (24.1 ± 5.2 %). Moreover, as we can see both
the error and relative error stay approximately constant with
respect to the target amount when using the shaping method,
in contrast to the PD controller. The average pouring times
with the shaping function for 50 g water and salt were 25.1
s and 36.8 s, respectively. Our results are comparable with
previous work (Kennedy et al., 2019; Huang et al., 2021)
in terms of pouring error and time, without using a learned,
vision-based policy, or expensive equipment setup.
   In order to assess the pouring skill more effectively, a
series of experiments were carried out involving three human
subjects. The experiments aimed to measure both the accu-
racy and speed of pouring, with each experiment being
repeated five times. The average errors for 50 g of water and
salt were 0.8 g and 1.0 g, and the average pouring times were
16.4 s and 18.6 s respectively. The main factor causing the dis-
parity in pouring time between human subjects and the robot
stems from their distinct behaviors during the pre-pouring
phase. Humans have the ability to quickly rotate a beaker
during the pre-pouring stage by relying on visual cues to
determine when the pouring begins. Conversely, the robot’s
movements during the pre-pouring stage were deliberately
slow to prevent overshooting. On average, the pre-pouring
stage of the robot took approximately 6 s, whereas it was
negligible for humans.

4.4.2 Constrained motion planning in 7/8-DoF robot

                                                                             Fig. 15 Evaluation of pouring error. The pouring errors of our shaping
The constrained motion planning performance of 7-DoF and
                                                                             pouring and PD control baseline pouring are compared using a water and
8-DoF robots is evaluated in two scenarios: (1) single step,                 b salt. The bar plot shows the error (poured amount—target amount) and
(2) two steps. In scenario (1), robots find a constrained path               the line plot shows the relative error. The error bars show the standard
with a fixed orientation from initial to final positions that                deviation (Color figure online)


123
Autonomous Robots (2023) 47:1057–1086                                                                                           1077


Table 5 Success rate comparison of 7 and 8-DoF robot                the beaker content may help to have higher flexibility in robot
              Scenario 1 (%)               Scenario 2 (%)           manipulation (Muchacho et al., 2022). Although our skill
              IK          Plan             IK          Plan         has currently attained 8% error for liquid and powder pour-
                                                                    ing, higher accuracy is desirable for precise experiments in a
7-DoF         99         84                99          70
                                                                    chemistry lab. We used a scale with integrated functionality
8-DoF         100        97                100         84
                                                                    for stirring and heating, but its measurement is delayed for 3 s.
                                                                    Higher precision pouring can be attained using a scale with a
                                                                    shorter response time; also, it can be achieved by specialized
    In scenario (2), we restart the sequence planning from the      tools, such as a pipette (Yoshikawa et al., 2023). In addition,
first step if a step fails. Constraints are set to the robot end-   visual feedback during pouring may lead to faster and more
effector pitch and roll ( θ, φ ≤ 0.1 rad).                          accurate pouring and be helpful in avoiding spillage.
    The performance of the 7-DoF and 8-DoF robot arms for              Moreover, CLAIRify was successful in generating plans
the two scenarios are shown in Table 5. The results show that       beyond the state-of-the-art method for the chemistry domain-
the IK and constrained motion planning have higher success          specific structured language XDL. Although the generated
rates in 8-DoF compared with the 7-DoF robot.                       plans were syntactically correct and satisfied the constraints,
                                                                    they contained errors. However, experts placed greater
                                                                    emphasis on missing actions than on ambiguous or incor-
5 Discussion                                                        rect actions when selecting the preferred output, indicating
                                                                    that this class of error is more severe for the tasks and
In this paper, we demonstrate how LLMs are effective tools          outputs investigated here. These results demonstrate the gen-
for translating natural language inputs into domain-specific        eralizability of our method, which uses zero-shot iterative
target languages without any fine-tuning. We find that by           prompting verification. We can apply it to different language
prompting an LLM with errors that it makes, it is able              styles and domains and still obtain coherent plans. While
to correct its own output and generate syntactically valid          our approach, which combines LLMs and TAMP, showed
plans. We also tested the ability of CLAIRify to generate           promising results in generating feasible and executable plans,
plans for the same experiment written in different ways (see        as evidenced by our evaluation, the capabilities of pure LLMs
“Appendix D”), which is important for generalizability since        in generating semantically correct plans remain limited. The
humans have different writing styles. We find that LLMs are         limitation in task planning abilities has been highlighted in
robust to variations in natural language, which is important        a recent study (Bubeck et al., 2023) as well. To address this
for lowering the barrier to successful user interaction. The        shortcoming, an alternative approach could be to incorpo-
XDL plans generated by CLAIRify can then be combined                rate human-in-the-loop planning or to utilize multi-modal
with our TAMP pipeline to effectively perform multistep             foundation model that consider the surrounding scene of the
chemistry experiments in the real world. However, the cur-          robot.
rent study is limited to a few types of chemistry experiments          Another important consideration to address is the tradeoff
because the number of skills incorporated in the framework is       between the human interpretability and expressive power of
limited. Increasing the repertoire of skills, such as glassware     the target structured language. Our approach to using inter-
perception in 3D and clutter, without fiducial markers (Eppel       mediate language enables users to ensure the LLM’s natural
et al., 2020), can improve the framework scalability. As we         language interpretation is reasonable; however, the expres-
develop more and more skills, we can append their descrip-          sive power of XDL imposed limitations on the framework’s
tions to the language model input. We demonstrated this by          abilities. The robot framework can conduct more diverse
appending a new skill, <Monitor>, to the XDL description,           actions than XDL can express, but the use of XDL limits the
and the LLM was able to accurately incorporate it into the          available actions. This problem may be alleviated by gener-
plan. Another issue is that the inefficiency of PDDLStream          ating the robot program directly, but human interpretability
inhibits the framework from being reactive in a dynamic envi-       may be decreased as a result.
ronment. Incorporating the learning-based search heuristics
for PDDLStream (Khodeir et al., 2023, 2022) may overcome
this limitation. Constrained motion planning was shown to           6 Conclusions
effectively avoid spillage of the beaker contents during trans-
fer in our experiments. We have also shown that adding an           In this paper, we presented a framework for automat-
extra 8th DoF to the robot enabled more flexibility and a           ing chemistry lab experiments using general-purpose robot
higher success rate for constrained motion planning. How-           manipulators and natural language commands. In order to
ever, the proposed constrained motion planning embedded in          facilitate the closed-loop execution of long-horizon chem-
TAMP cannot run in real-time. Considering the dynamics of           istry experiments, CLAIRify maps natural language com-


                                                                                                                          123
1078                                                                                                      Autonomous Robots (2023) 47:1057–1086


mands to XDL, a human-interpretable intermediate language                   s(t) = u(t) − 2 u(t − t0 )
                                                                                    N
that standardizes chemistry experiment descriptions. Sub-                         + k=1   {u(t − (t0 + k Tdeactive ))
sequently, XDL instructions are converted into a sequence                         +u(t − (t0 + k (Tdeactive + Tidle )))
of subgoals for a constrained task and motion plan solver,                       −2 u(t − (t0 + k (Tdeactive + Tidle + Tactivate )))}
and the robot executes those plans using its diverse set of                                                                                     (2)
skills. Finally, the robot visually monitors the progress of the
tasks. We demonstrated that our approach lowers the bar-                    where t0 is the moment in which e(t) starts to change, mean-
riers to instructing robots by non-experts to execute robot                 ing that the material is getting added to the target dish.
task plans. The robot handles solubility and recrystallization              Tdeactive , Tidle , and Tactive are the parameters set by the user
experiments autonomously when provided with natural lan-                    to describe the periodic motion of the robot end-effector. This
guage inputs.                                                               motion continues till the material transferred to the target dish
                                                                            reaches the desired amount.
Acknowledgements We thank members of the Matter Lab for annotat-
ing task plans. We would also like to thank the Acceleration Consortium
and Google Inc. for their generous support (NSERC-Google Industrial
Research Chair Award). L.B.K. acknowledges generous support from            Appendix B: Full prompt
the Carlsberg Foundation.

Author Contributions NY, MS, KD, SA-R, ZJ, LBK worked on                    The full XDL description and an experiment description from
CLAIRify; NY, KD, AZL, YZ, HX, AK worked on robotic experiments.            the Chem-EDU dataset are shown as an example of a full
NY, MS, KD wrote the initial draft. LBK, AA-G, FS, AG proof-read            prompt to the LLM.
the manuscript, and AA-G, FS, AG supervised the project.
                                                                            i n i t i a l _ p r o m p t = """
                                                                            XDL files will follow XML s y n t a x and c o n s i s t
Funding L.B.K. has received funding from the Carlsberg Foundation             of three m a n d a t o r y s e c t i o n s : Hardware ,
under grant ID CF21-0669.                                                   w h e r e v i r t u a l v e s s e l s that the r e a c t i o n
                                                                            m i x t u r e can r e s i d e in are d e c l a r e d . Reagents
                                                                            , where all r e a g e n t s that are used in the
Declarations                                                                p r o c e d u r e are declared , and Procedure , where
                                                                              the s y n t h e t i c a c t i o n s i n v o l v e d in the
                                                                            p r o c e d u r e are l i n e a r l y d e c l a r e d .
Conflict of interest The authors have no relevant financial or non-
financial interest to disclose.                                             XDL File Stub :
                                                                            < XDL >
Open Access This article is licensed under a Creative Commons                  < Synthesis >
                                                                                    < Hardware >
Attribution 4.0 International License, which permits use, sharing, adap-                 <! - - ... - - >
tation, distribution and reproduction in any medium or format, as                   </ Hardware >
long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons licence, and indi-                    < Reagents >
                                                                                          <! - - ... - - >
cate if changes were made. The images or other third party material                  </ Reagents >
in this article are included in the article’s Creative Commons licence,
unless indicated otherwise in a credit line to the material. If material             < Procedure >
is not included in the article’s Creative Commons licence and your                        <! - - ... - - >
                                                                                     </ Procedure >
intended use is not permitted by statutory regulation or exceeds the           </ Synthesis >
permitted use, you will need to obtain permission directly from the copy-   </ XDL >
right holder. To view a copy of this licence, visit http://creativecomm
ons.org/licenses/by/4.0/.                                                   Hardware :
                                                                            Each i n d i v i d u a l reagent , u n l e s s o t h e r w i s e
                                                                            s t a t e d s h o u l d be c o n t a i n e d w i t h i n t h e i r own
                                                                            vessels .

                                                                            ( f o r m a t is ( Property , Type , D e s c r i p t i o n ) )
Appendix A: Pouring policy                                                  id , str , Name of h a r d w a r e

The pouring policy is the blending of a shaping function                    Reagents :
                                                                            The R e a g e n t s s e c t i o n c o n t a i n s R e a g e n t
s(t) and a model-free PD controller v PD (t), expressed as                  e l e m e n t s with the props below .
v PD (t) × s(t). The PD controller is defined as:                           Any r e a g e n t s which were c o m b i n e d b e f o r e the
                                                                            e x p e r i m e n t s h o u l d be c o m b i n e d as one r e a g e n t
                                                                              b e f o r e the p r o c e d u r e . ( i . e . ’ lime juice
                                                                            mixed with sugar ’ = < R e a g e n t name = ’ lime
                                                                            juice mixed with sugar ’)
v PD (t) = k p e + kd ė,                                            (1)
                                                                            Reagent :
                                                                            R e a g e n t used by p r o c e d u r e .
where e(t) = xr e f − x f b . The shaping function is imple-                ( f o r m a t is ( Property , Type , D e s c r i p t i o n ) )
mented via the summation of several unit functions u(t) as                  name , str , Name of r e a g e n t
follows:


123
Autonomous Robots (2023) 47:1057–1086                                                                                                              1079


Procedure :                                                                    format ( P r o p e r t y Type         Description )
All steps i n c l u d e d in the Full Steps                                    vessel     vessel        V e s s e l to s t i r .
S p e c i f i c a t i o n may be g i v e n w i t h i n the                     time       float         Time to stir vessel for .
P r o c e d u r e block of a XDL f i l e . A d d i t i o n a l l y ,
  the P r o c e d u r e block may be , but does not                            StopStir :
have to be , d i v i d e d up into Prep , Reaction ,                           Stop s t i r r i n g given vessel .
W o r k u p and P u r i f i c a t i o n blocks , each of                       format ( P r o p e r t y Type         Description )
w h i c h can c o n t a i n any of the s t e p s in the                        vessel     vessel        V e s s e l to s t o p s t i r r i n g .
specification .
                                                                               Temperature Control :
Here is a list of tags that can be used in                                     HeatChill :
this l a n g u a g e :                                                         Heat or chill vessel to given temp for given
L i q u i d H a n d l i n g : Add , Separate , Transfer ,                       time .
S t i r r i n g : StartStir , Stir , StopStir ,                                format ( P r o p e r t y Type            Description )
T e m p e r a t u r e C o n t r o l : HeatChill ,                              vessel       vessel      V e s s e l to h e a t or c h i l l .
HeatChillToTemp , StartHeatChill ,                                             temp         float       T e m p e r a t u r e to heat or chill
StopHeatChill                                                                   v e s s e l to .
Inert Gas : E v a c u a t e A n d R e f i l l , Purge ,                        time         float       Time to heat or chill vessel
StartPurge , S t o p P u r g e                                                  for .
F i l t r a t i o n : Filter , F i l t e r T h r o u g h , W a s h S o l i d
S p e c i a l : Wait , Repeat ,                                                C o n v e r t to XDL :
O t h e r : C l e a n V e s s e l , C r y s t a l l i z e , Dissolve ,         Add 30 g of red c a b b a g e soup into a b e a k e r .
Dry , Evaporate , Irradiate , Precipitate ,                                    Add 10 g of acetic acid into the beaker ,
ResetHandling , RunColumn                                                      then stir the s o l u t i o n for 10 s e c o n d s .
                                                                               """
Steps :
Liquid Handling :
Add l i q u i d or s o l i d r e a g e n t . R e a g e n t
i d e n t i t y ( ie l i q u i d or solid ) is d e t e r m i n e d
by the solid p r o p e r t y of a r e a g e n t in the
Reagent section .
                                                                               Appendix C: Chem-EDU dataset
The q u a n t i t y of the r e a g e n t can be s p e c i f i e d
  u s i n g e i t h e r v o l u m e ( l i q u i d u n i t s ) or               We show some examples of experiments in the Chem-EDU
a m o u n t ( all a c c e p t e d units e . g . ’g ’, ’ mL ’, ’                dataset.
eq ’, ’ mmol ’) .
                                                                               Add 30 g of red c a b b a g e soup into a b e a k e r .
f o r m a t ( P r o p e r t y Type         Description )                       Add 10 g of acetic acid into the beaker ,
vessel          vessel        V e s s e l to add r e a g e n t to .            then stir the s o l u t i o n for 10 s e c o n d s .
r e a g e n t r e a g e n t R e a g e n t to add .
                                                                               Experiment 0
Separate :
Perform separation .                                                           Acacia Honey Syrup
f o r m a t ( P r o p e r t y Type D e s c r i p t i o n )                     Add 200 g of hot w a t e r to a b e a k e r . Add 430 g
Property                Type       Description                                 a c a c i a h o n e y to the b e a k e r . S t i r for 10
p u r p o s e str ’ wash ’ or ’ e x t r a c t ’. ’ wash ’                      minutes while heating .
means that p r o d u c t p h a s e will not be the
a d d e d s o l v e n t phase , ’ e x t r a c t ’ m e a n s p r o d u c t      Experiment 13
  phase will be the added s o l v e n t p h a s e . If
no s o l v e n t is added just use ’ e x t r a c t ’.
product_phase                 str ’ top ’ or ’ b o t t o m ’. Phase            Add 250 g water to beaker . Heat until it
  that p r o d u c t will be in .                                              r e a c h e s 100 d e g r e e s C . Add 40 g of p a s t a .
from_vessel vessel                 C o n t e n t s of f r o m _ v e s s e l    Heat for 6 m i n u t e s at 100 d e g r e e s C .
are t r a n s f e r r e d to s e p a r a t i o n _ v e s s e l and
s e p a r a t i o n is p e r f o r m e d .                                     Experiment 30
separation_vessel                  vessel         V e s s e l in w h i c h
s e p a r a t i o n of p h a s e s will be c a r r i e d out .
to_vessel               vessel     V e s s e l to send p r o d u c t
phase to .

Transfer :
                                                                               Appendix D: Variations in natural language
T r a n s f e r l i q u i d from one vessel to a n o t h e r .

The q u a n t i t y to t r a n s f e r can be s p e c i f i e d
                                                                               Since humans have different writing styles, we wanted to
u s i n g e i t h e r v o l u m e ( l i q u i d u n i t s ) or a m o u n t     determine if our model is able to generate consistent XDL
  ( all a c c e p t e d units e . g . ’ g ’, ’ mL ’, ’ eq ’, ’
mmol ’) .                                                                      plans from natural language descriptions written in differ-
                                                                               ent ways. We took two experiments from Chem-EDU and
f o r m a t ( P r o p e r t y Type         Description )
from_vessel vessel                 V e s s e l to t r a n s f e r              prompted ChatGPT to rewrite the experiment. We ran all
liquid from .                                                                  experiments through CLAIRify and examined the outputs.4
to_vessel               vessel     V e s s e l to t r a n s f e r
l i q u i d to .                                                               We find that CLAIRify can generate the same XDL plans
Stirring :
                                                                               with different natural language descriptions.
StartStir :
Start s t i r r i n g v e s s e l .
f o r m a t ( P r o p e r t y Type         Description )
vessel          vessel        V e s s e l to s t a r t s t i r r i n g .

Stir :
Stir vessel for given time .                                                   4 https://beta.openai.com.




                                                                                                                                           123
1080                                                                                               Autonomous Robots (2023) 47:1057–1086




Fig. 16 XDL generated for different writing styles for Experiment     XDL plan. The output is semantically the same for both (note that the
0 from Chem-EDU. The first writing style (writing style 1) is taken   extra <StartSir> and <StopStir> actions in (d) are redun-
directly from Chem-EDU. For the second writing style (writing style
                                                                      dant, as the presence of the <Stir> action automatically does a
2), we asked ChatGPT to rewrite it. For both prompts, we generate a
                                                                       <StartSir> and <StopStir> action)




123
Autonomous Robots (2023) 47:1057–1086                                                                                                     1081




Fig. 17 XDL generated for different writing styles for Experiment 30 from Chem-EDU. The first writing style (writing style 1) is taken directly
from Chem-EDU. For the second writing style (writing style 2), we asked ChatGPT to rewrite it. For both prompts, we generate a XDL plan. The
output is identical for both




                                                                                                                                   123
1082                                                                                                        Autonomous Robots (2023) 47:1057–1086


References                                                                        An embodied multimodal language model. arXiv preprint. https://
                                                                                  doi.org/10.48550/arXiv.2303.03378
Abolhasani, M., & Kumacheva, E. (2023). The rise of self-driving labs         Edwards, C., Lai, T., Ros, K., Honke, G., & Ji, H. (2022). Translation
     in chemical and materials sciences. Nature Synthesis 1–10.                   between molecules and natural language. arXiv preprint. https://
Ahn, M., Brohan, A., Brown, N., Chebotar, Y., Cortes, O., David, B.,              doi.org/10.48550/arXiv.2204.11817
     Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., et al.            Eppel, S., Xu, H., Bismuth, M., & Aspuru-Guzik, A. (2020). Computer
     (2022). Do As I Can, Not As I Say: Grounding language in robotic             vision for recognition of materials and vessels in chemistry lab set-
     affordances. arXiv preprint. https://doi.org/10.48550/arXiv.2204.            tings and the vector-labpics data set. ACS Central Science, 6(10),
     01691 .                                                                      1743–1752.
Baier, J. A., Bacchus, F., & McIlraith, S. A. (2009). A heuristic search      Epps, R. W., Bowen, M. S., Volk, A. A., Abdel-Latif, K., Han, S., Reyes,
     approach to planning with temporally extended preferences. Arti-             K. G., Amassian, A., & Abolhasani, M. (2020). Artificial chemist:
     ficial Intelligence, 173(5–6), 593–618.                                      An autonomous quantum dot synthesis bot. Advanced Materials,
Beeson, P. & Ames, B. (2015) TRAC-IK: An open-source library                      32(30), 2001626.
     for improved solving of generic inverse kinematics. In 2015              Eysenbach, B., Salakhutdinov, R. R., & Levine, S. (2019). Search on
     IEEE-RAS 15th international conference on humanoid robots                    the replay buffer: Bridging planning and reinforcement learning.
     (humanoids).                                                                 Advances in Neural Information Processing Systems, 32.
Berenson, D., Srinivasa, S., & Kuffner, J. (2011). Task space regions:        Fakhruldeen, H., Pizzuto, G., Glowacki, J., & Cooper, A. I. (2022).
     A framework for pose-constrained manipulation planning. The                  ARChemist: Autonomous robotic chemistry system architecture.
     International Journal of Robotics Research, 30(12), 1435–1460.               arXiv preprint. https://doi.org/10.48550/arXiv.2204.13571
     https://doi.org/10.1177/0278364910396389                                 Fortman, J. J., & Stubbs, K. M. (1992). Demonstrations with red cab-
Boiko, D. A., MacKnight, R., & Gomes, G. (2023). Emergent                         bage indicator. Journal of Chemical Education, 69(1), 66.
     autonomous scientific research capabilities of large language mod-       Garrett, C. R., Chitnis, R., Holladay, R., Kim, B., Silver, T., Kael-
     els. arXiv preprint. https://doi.org/10.48550/arXiv.2304.05332               bling, L. P., & Lozano-Pérez, T. (2021). Integrated task and motion
Bran, A. M., Cox, S., White, A. D., & Schwaller, P. (2023). ChemCrow:             planning. Annual Review of Control, Robotics, and Autonomous
     Augmenting large-language models with chemistry tools. arXiv                 Systems, 4, 265–293.
     preprint. https://doi.org/10.48550/arXiv.2304.05376                      Garrett, C. R., Lozano-Pérez, T., & Kaelbling, L. P. (2020). PDDL-
Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal,             Stream: Integrating symbolic planners and blackbox samplers via
     P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., et al. (2020).       optimistic adaptive planning. In Proceedings of the 30th interna-
     Language models are few-shot learners. Advances in Neural Infor-             tional conference on automated planning and scheduling (ICAPS),
     mation Processing Systems, 33, 1877–1901.                                    (pp. 440–448). AAAI Press.
Bubeck, S., Chandrasekaran, V., Eldan, R., Gehrke, J., Horvitz, E.,           Ghallab, M., Howe, A., Knoblock, C, McDermott, D. Ram, A., Veloso,
     Kamar, E., Lee, P., Lee, Y. T., Li, Y., Lundberg, S., et al. (2023).         M., Weld, D., Wilkins, D. (1998). PDDL - The Planning Domain
     Sparks of artificial general intelligence: Early experiments with            Definition Language. Technical Report CVC TR98003/DCS
     gpt-4. arXiv preprint. https://doi.org/10.48550/arXiv.2303.12712             TR1165. New Haven, CT: Yale Center for Computational Vision
Burger, B., Maffettone, P. M., Gusev, V. V., Aitchison, C. M., Bai, Y.,           and Control.
     Wang, X., Li, X., Alston, B. M., Li, B., Clowes, R., et al. (2020).      Grinberg, M. (2018). Flask web development: Developing web appli-
     A mobile robotic chemist. Nature, 583(7815), 237–241.                        cations with python. “ O’Reilly Media, Inc.”.
Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H. P. O., Kaplan, J.,         Gu, Y., Tinn, R., Cheng, H., Lucas, M., Usuyama, N., Liu, X., Nau-
     Edwards, H., Burda, Y., Joseph, N., Brockman, G., et al.(2021).              mann, T., Gao, J., & Poon, H. (2021). Domain-specific language
     Evaluating large language models trained on code. arXiv preprint.            model pretraining for biomedical natural language processing.
     https://doi.org/10.48550/arXiv.2107.03374                                    ACM Transactions on Computing for Healthcare, 3(1), 1–23.
Chowdhery, A., Narang, S., Devlin, J., Bosma, M., Mishra, G., Roberts,            https://doi.org/10.1145/3458754
     A., Barham, P., Chung, H. W., Sutton, C., Gehrmann, S., et al.           Häse, F., Roch, L. M., & Aspuru-Guzik, A. (2019). Next-generation
     (2022). PaLM: Scaling language modeling with pathways. arXiv                 experimentation with self-driving laboratories. Trends in Chem-
     preprint. https://doi.org/10.48550/arXiv.2204.02311                          istry, 1(3), 282–291.
Coleman, D., Sucan, I., Chitta, S., & Correll, N. (2014). Reducing the        Helmert, M. (2006). The fast downward planning system. Journal of
     barrier to entry of complex robotic software: A MoveIt! case study.          Artificial Intelligence Research, 26, 191–246.
     arXiv preprint. https://doi.org/10.48550/arXiv.1404.3785                 Higgins, K., Ziatdinov, M., Kalinin, S. V., & Ahmadi, M. (2021).
Dantam, N. T., Kingston, Z. K., Chaudhuri, S., & Kavraki, L. E. (2018).           High-throughput study of antisolvents on the stability of multicom-
     An incremental constraint-based framework for task and motion                ponent metal halide perovskites through robotics-based synthesis
     planning. The International Journal of Robotics Research, 37(10),            and machine learning approaches. Journal of the American Chem-
     1134–1151.                                                                   ical Society, 143(47), 19945–19955.
Devlin, J., Chang, M., Lee, K., & Toutanova, K. (2019). BERT:                 Huang, D. A., Nair, S., Xu, D., Zhu, Y., Garg, A., Fei-Fei, L., Savarese,
     Pre-training of deep bidirectional transformers for language under-          S., & Niebles, J. C. (2019). Neural task graphs: Generalizing to
     standing. In North American chapter of the association for                   unseen tasks from a single video demonstration. In IEEE Computer
     computational linguistics.                                                   Vision and Pattern Recognition.
Ding, Y., Zhang, X., Paxton, C., & Zhang, S. (2023). Task and motion          Huang, W., Abbeel, P., Pathak, D., & Mordatch, I. (2022). Language
     planning with large language models for object rearrangement.                models as zero-shot planners: Extracting actionable knowledge for
     arXiv preprint. https://doi.org/10.48550/arXiv.2212.09672                    embodied agents. In International Conference on Machine Learn-
Driess, D., Ha, J. S., & Toussaint, M. (2020). Deep visual reasoning:             ing, (pp. 9118–9147). PMLR.
     Learning to predict action sequences for task and motion plan-           Huang, W., Xia, F., Xiao, T., Chan, H., Liang, J., Florence, P.,
     ning from an initial scene image. arXiv preprint. https://doi.org/           Zeng, A., Tompson, J., Mordatch, I., Chebotar, Y., et al. (2022).
     10.48550/arXiv.2006.05398                                                    Inner monologue: Embodied reasoning through planning with
Driess, D., Xia, F., Sajjadi, M. S., Lynch, C., Chowdhery, A., Ichter, B.,        language models. arXiv preprint. https://doi.org/10.48550/arXiv.
     Wahid, A., Tompson, J., Vuong, Q., Yu, T., et al. (2023). Palm-e:            2207.05608



123
Autonomous Robots (2023) 47:1057–1086                                                                                                            1083


Huang, Y., Wilches, J., & Sun, Y. (2021). Robot gaining accurate                  programs for embodied control. arXiv preprint. https://doi.org/10.
     pouring skills through self-supervised learning and generalization.          48550/arXiv.2209.07753
     Robotics and Autonomous Systems, 136, 103692. https://doi.org/          Lim, J. X. Y., Leow, D., Pham, Q. C., & Tan, C. H. (2020). Development
     10.1016/j.robot.2020.103692                                                  of a robotic system for automatic organic chemistry synthesis.
Inagaki, T., Kato, A., Takahashi, K., Ozaki, H., & Kanda, G. N. (2023).           EEE Transactions on Automation Science and Engineering, 18(4),
     LLMs can generate robotic scripts from goal-oriented instructions            2185–2190.
     in biological laboratory automation. arXiv preprint. https://doi.       Lin, K., Agia, C., Migimatsu, T., Pavone, M., & Bohg, J. (2023).
     org/10.48550/arXiv.2304.10267                                                Text2Motion: From natural language instructions to feasible plans.
Irwin, R., Dimitriadis, S., He, J., & Bjerrum, E. J. (2022). Chemformer:          arXiv preprint. https://doi.org/10.48550/arXiv.2303.12153
     A pre-trained transformer for computational chemistry. Machine          Liu, R., Wei, J., Gu, S.S., Wu, T.Y., Vosoughi, S., Cui, C., Zhou, D., &
     Learning: Science and Technology, 3(1), 015022.                              Dai, A.M. (2023). Mind’s eye: Grounded language model reason-
Jablonka, K. M., Schwaller, P., Ortega-Guerrero, A., & Smit, B. (2023).           ing through simulation. In The eleventh international conference
     Is gpt-3 all you need for low-data discovery in chemistry? Chem-             on learning representations.
     Rxiv. https://doi.org/10.26434/chemrxiv-2023-fw8n4                      Macarron, R., Banks, M. N., Bojanic, D., Burns, D. J., Cirovic, D.
Kaelbling, L. P., & Lozano-Pérez, T. (2011). Hierarchical task and                A., Garyantes, T., Green, D. V., Hertzberg, R. P., Janzen, W. P.,
     motion planning in the now. In IEEE International Conference                 Paslay, J. W., et al. (2011). Impact of high-throughput screening
     on Robotics and Automation (pp. 1470–1477). IEEE.                            in biomedical research. Nature Reviews Drug discovery, 10(3),
Karaman, S., & Frazzoli, E. (2011). Sampling-based algorithms for                 188–195.
     optimal motion planning. The International Journal of Robotics          MacLeod, B. P., Parlane, F. G., Morrissey, T. D., Häse, F., Roch, L. M.,
     Research, 30(7), 846–894.                                                    Dettelbach, K. E., Moreira, R., Yunker, L. P., Rooney, M. B., Deeth,
Kavraki, L. E., Svestka, P., Latombe, J. C., & Overmars, M. H. (1996).            J. R., et al. (2020). Self-driving laboratory for accelerated discov-
     Probabilistic roadmaps for path planning in high-dimensional con-            ery of thin-film materials. Science Advances, 6(20), eaaz8867.
     figuration spaces. IEEE Transactions on Robotics and Automation,        Mehr, H., Craven, M., Leonov, A., Keenan, G., & Cronin, L. (2020a).
     12(4), 566–580.                                                              Benchmarking results and the XDL XML schema. https://zenodo.
Kennedy, M., Schmeckpeper, K., Thakur, D., Jiang, C., Kumar, V.,                  org/record/3955107
     & Daniilidis, K. (2019). Autonomous precision pouring from              Mehr, S. H. M., Craven, M., Leonov, A. I., Keenan, G., & Cronin,
     unknown containers. IEEE Robotics and Automation Letters, 4(3),              L. (2020). A universal system for digitization and automatic exe-
     2317–2324. https://doi.org/10.1109/LRA.2019.2902075                          cution of the chemical synthesis literature. Science, 370(6512),
Khodeir, M., Agro, B., & Shkurti, F. (2023). Learning to search in task           101–108.
     and motion planning with streams. IEEE Robotics and Automation          Ménard, A. D., & Trant, J. F. (2020). A review and critique of academic
     Letters, 8(4), 1983–1990.                                                    lab safety research. Nature Chemistry, 12(1), 17–25.
Khodeir, M., Sonwane, A., & Shkurti, F. (2022). Policy-guided lazy           Mialon, G., Dessì, R., Lomeli, M., Nalmpantis, C., Pasunuru, R.,
     search with feedback for task and motion planning. arXiv preprint.           Raileanu, R., Rozière, B., Schick, T., Dwivedi-Yu, J., Celikyil-
     https://doi.org/10.48550/arXiv.2210.14055                                    maz, A., et al. (2023). Augmented language models: a survey.
Kim, B., Shimanuki, L., Kaelbling, L. P., & Lozano-Pérez, T. (2022).              arXiv preprint. https://doi.org/10.48550/arXiv.2302.07842
     Representation, learning, and planning algorithms for geometric         Mirchandani, S., Karamcheti, S., & Sadigh, D. (2021). ELLA: Explo-
     task and motion planning. The International Journal of Robotics              ration through learned language abstraction. Advances in Neural
     Research, 41(2), 210–231.                                                    Information Processing Systems, 34, 29529–29540.
Kingston, Z., Moll, M., & Kavraki, L. E. (2018). Sampling-based              Mishra, S., Khashabi, D., Baral, C., & Hajishirzi, H. (2021). Cross-task
     methods for motion planning with constraints. Annual Review of               generalization via natural language crowdsourcing instructions.
     Control, Robotics, and Autonomous Systems, 1, 159–185.                       arXiv preprint. https://doi.org/10.48550/arXiv.2104.08773
Kingston, Z., Moll, M., & Kavraki, L. E. (2019). Exploring implicit          Muchacho, R. I. C., Laha, R., Figueredo, L. F., & Haddadin, S. (2022).
     spaces for constrained sampling-based planning. The International            A solution to slosh-free robot trajectory optimization. In 2022
     Journal of Robotics Research, 38(10–11), 1151–1178. https://doi.             IEEE/RSJ international conference on intelligent robots and sys-
     org/10.1177/0278364919868530                                                 tems (IROS), (pp. 223–230). IEEE.
Kitchener, B. G., Wainwright, J., & Parsons, A. J. (2017). A review          National Astronomical Observatory of Japan. (2022). Handbook of sci-
     of the principles of turbidity measurement. Progress in Physical             entific tables. World Scientific.
     Geography, 41(5), 620–642.                                              Ni, A., Iyer, S., Radev, D., Stoyanov, V., Yih, W. T., Wang, S. I., &
Knobbe, D., Zwirnmann, H., Eckhoff, M., & Haddadin, S. (2022). Core               Lin, X. V. (2023). Lever: Learning to verify language-to-code gen-
     processes in intelligent robotic lab assistants: Flexible liquid han-        eration with execution. arXiv preprint. https://doi.org/10.48550/
     dling. In 2022 IEEE/RSJ international conference on intelligent              arXiv.2302.08468
     robots and systems (IROS), pp. 2335–2342.                               Olson, E. (2011). Apriltag: A robust and flexible visual fiducial sys-
Le, H., Wang, Y., Gotmare, A. D., Savarese, S., & Hoi, S. C. H. (2022).           tem. In 2011 IEEE the international conference on robotics and
     CodeRL: Mastering code generation through pretrained models                  automation.
     and deep reinforcement learning. Advances in Neural Information         Peng, B., Galley, M., He, P., Cheng, H., Xie, Y., Hu, Y., Huang, Q.,
     Processing Systems, 35, 21314–21328.                                         Liden, L., Yu, Z., Chen, W., & Gao, J. (2023). Check your facts and
Li, J., Li, J., Liu, R., Tu, Y., Li, Y., Cheng, J., He, T., & Zhu, X.             try again: Improving large language models with external knowl-
     (2020). Autonomous discovery of optically active chiral inorganic            edge and automated feedback. arXiv preprint. https://doi.org/10.
     perovskite nanocrystals through an intelligent cloud lab. Nature             48550/arXiv.2302.12813
     Communications, 11(1), 2046.                                            Pereira, D., & Williams, J. (2007). Origin and evolution of high through-
Li, Y., Choi, D., Chung, J., Kushman, N., Schrittwieser, J., Leblond,             put screening. British Journal of Pharmacology, 152(1), 53–61.
     R., Eccles, T., Keeling, J., Gimeno, F., Dal Lago, A., et al.           Perry, T. (2021). LightTag: Text annotation platform. In Proceedings of
     (2022). Competition-level code generation with alphacode. Sci-               the EMNLP conference, (pp. 20–27).
     ence, 378(6624), 1092–1097.                                             Pizzuto, G., Wang, H., Fakhruldeen, H., Peng, B., Luck, K. S., & Cooper,
Liang, J., Huang, W., Xia, F., Xu, P., Hausman, K., Ichter, B., Flo-              A.I . (2022). Accelerating laboratory automation through robot
     rence, P., & Zeng, A. (2022). Code as policies: Language model


                                                                                                                                          123
1084                                                                                                         Autonomous Robots (2023) 47:1057–1086


     skill learning for sample scraping. arXiv preprint. https://doi.org/      Xu, D., Martín-Martín, R., Huang, D. A., Zhu, Y., Savarese, S., &
     10.48550/arXiv.2209.14875                                                     Fei-Fei, L. F. (2019). Regression planning networks. Advances
Ramos, M. C., Michtavy, S. S., Porosoff, M. D., & White, A. D. (2023).             in Neural Information Processing Systems, 32.
     Bayesian optimization of catalysts with in-context learning. arXiv        Xu, D., Nair, S., Zhu, Y., Gao, J., Garg, A., Fei-Fei, L., & Savarese, S.
     preprint. https://doi.org/10.48550/arXiv.2304.05341                           (2018). Neural task programming: Learning to generalize across
Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettle-           hierarchical tasks. In 2018 IEEE international conference on
     moyer, L., Cancedda, N., & Scialom, T. (2023). Toolformer:                    robotics and automation (ICRA) (pp. 3795–3802). IEEE.
     Language models can teach themselves to use tools. arXiv preprint.        Xu, H., Wang, Y. R., Eppel, S., Aspuru-Guzik, A., Shkurti, F., & Garg,
     https://doi.org/10.48550/arXiv.2302.04761                                     A. (2021). Seeing glass: Joint point-cloud and depth completion
Seifrid, M., Pollice, R., Aguilar-Granda, A., Morgan Chan, Z., Hotta,              for transparent objects. In Annual conference on robot learning.
     K., Ser, C. T., Vestfrid, J., Wu, T. C., & Aspuru-Guzik, A. (2022).       Yoshikawa, N., Darvish, K., Garg, A., & Aspuru-Guzik, A. (2023). Dig-
     Autonomous chemical experiments: Challenges and perspectives                  ital pipette: Open hardware for liquid transfer in self-driving lab-
     on establishing a self-driving lab. Accounts of Chemical Research,            oratories. Digital Discovery. https://doi.org/10.1039/d3dd00115f
     55(17), 2454–2466.                                                        Yoshikawa, N., Li, A. Z., Darvish, K., Zhao, Y., Xu, H., Kuramshin,
Shah, D., Xu, P., Lu, Y., Xiao, T., Toshev, A., Levine, S., & Ichter, B.           A., Aspuru-Guzik, A., Garg, A., & Shkurti, F. (2023). Chemistry
     (2021). Value function spaces: Skill-centric state abstractions for           lab automation via constrained task and motion planning. arXiv
     long-horizon reasoning. arXiv preprint. https://doi.org/10.48550/             preprint. https://doi.org/10.48550/arXiv.2212.09672
     arXiv.2111.03189                                                          Yoshikawa, T. (1985). Manipulability of robotic mechanisms. The Inter-
Sharma, P., Torralba, A., & Andreas, J. (2021). Skill induction and                national Journal of Robotics Research, 4(2), 3–9. https://doi.org/
     planning with latent language. arXiv preprint. https://doi.org/10.            10.1177/027836498500400201
     48550/arXiv.2110.01517                                                    Zhang, K., Sharma, M., Liang, J., & Kroemer, O. (2020). A modu-
Shiri, P., Lai, V., Zepel, T., Griffin, D., Reifman, J., Clark, S., Grunert,       lar robotic arm control stack for research: Franka-Interface and
     S., Yunker, L. P., Steiner, S., Situ, H., et al. (2021). Automated sol-       FrankaPy. arXiv preprint. https://doi.org/10.48550/arXiv.2011.
     ubility screening platform using computer vision. iscience, 24(3),            02398
     102176.
Singh, I., Blukis, V., Mousavian, A., Goyal, A., Xu, D., Tremblay, J.,
     Fox, D., Thomason, J., & Garg, A. (2022). Progprompt: Generat-            Publisher’s Note Springer Nature remains neutral with regard to juris-
     ing situated robot task plans using large language models. arXiv          dictional claims in published maps and institutional affiliations.
     preprint. https://doi.org/10.48550/arXiv.2209.11302
Steiner, S., Wolf, J., Glatzel, S., Andreou, A., Granda, J. M., Keenan,
     G., Hinkley, T., Aragon-Camarasa, G., Kitson, P. J., Angelone,
     D., et al. (2019). Organic synthesis in a modular robotic system                                               Naruki Yoshikawa is a Ph.D. stu-
     driven by a chemical programming language. Science, 363(6423),                                                 dent at the Department of Com-
     eaav2211.                                                                                                      puter Science of the University
Taylor, R., Kardas, M., Cucurull, G., Scialom, T., Hartshorn, A., Saravia,                                          of Toronto. He is working on
     E., Poulton, A., Kerkez, V., & Stojnic, R. (2022). Galactica: A                                                automation of chemistry experi-
     large language model for science. arXiv preprint. https://doi.org/                                             ments under the supervision of
     10.48550/arXiv.2211.09085                                                                                      Alán Aspuru-Guzik. He received
Tellex, S., Kollar, T., Dickerson, S., Walter, M., Banerjee, A., Teller, S.,                                        his master’s degree in 2020 at The
     & Roy, N. (2011). Understanding natural language commands for                                                  University of Tokyo and his bach-
     robotic navigation and mobile manipulation. In Proceedings of the                                              elor’s degree in 2018 at the same
     AAAI conference on artificial intelligence, vol. 25, pp. 1507–1514.                                            institution.
Toussaint, M. (2015). Logic-geometric programming: An optimization-
     based approach to combined task and motion planning. In IJCAI,
     pp. 1930–1936.
Toussaint, M. A., Allen, K. R., Smith, K. A., & Tenenbaum, J. B. (2018).
     Differentiable physics and stable modes for tool-use and manipu-
     lation planning.                                                                                               Marta Skreta is a Computer Sci-
Wang, S., Liu, Y., Xu, Y., Zhu, C., & Zeng, M. (2021). Want to reduce                                               ence PhD student under the super-
     labeling cost? GPT-3 can help. In Proceedings of the EMNLP Con-                                                vision of Alán Aspuru-Guzik at
     ference, pp. 4195–4205.                                                                                        the University of Toronto work-
Wang, Y., Wang, W., Joty, S., & Hoi, S. C. (2021). CodeT5: Identifier-                                              ing at the intersection of machine
     aware unified pre-trained encoder-decoder models for code under-                                               learning, chemistry, and self-driving
     standing and generation. arXiv preprint. https://doi.org/10.48550/                                             labs. Previously, she completed a
     arXiv.2109.00859                                                                                               MSc in Computer Science at the
Wang, Y. R., Zhao, Y., Xu, H., Eppel, S., Aspuru-Guzik, A., Shkurti, F.,                                            University of Toronto and a HBSc
     & Garg, A. (2023). MVTrans: Multi-view perception of transpar-                                                 in Chemical Biology at McMaster
     ent objects. arXiv preprint. https://doi.org/10.48550/arXiv.2302.                                              University.
     11683
Wolthuis, E., Pruiksma, A. B., & Heerema, R. P. (1960). Determina-
     tion of solubility: A laboratory experiment. Journal of Chemical
     Education, 37(3), 137.
Wu, C. J., Raghavendra, R., Gupta, U., Acun, B., Ardalani, N., Maeng,
     K., Chang, G., Aga, F., Huang, J., Bai, C., et al. (2022). Sustainable
     AI: Environmental implications, challenges and opportunities.
     Proceedings of Machine Learning and Systems, 4, 795–813.


123
Autonomous Robots (2023) 47:1057–1086                                                                                                      1085


                                    Kourosh Darvish is a postdoc-                                           Andrew Zou Li is a senior under-
                                    toral researcher at the Computer                                        graduate student studying robotics
                                    Science and Robotics Institute of                                       in the Division of Engineering
                                    the University of Toronto (UofT)                                        Science at the University of
                                    and a member of the Vector Insti-                                       Toronto. His research experience
                                    tute. Before joining UofT in 2022,                                      includes state estimation for
                                    he was a postdoctoral researcher                                        autonomous driving, task and
                                    at the Italian Institute of Tech-                                       motion planning, and machine
                                    nology (IIT). In 2019, he com-                                          learning compiler optimization.
                                    pleted his PhD in Bioengineer-
                                    ing and Robotics from the Univer-
                                    sity of Genoa, Italy. Previously,
                                    he received his B.Sc. and M.Sc.
                                    degrees in Aerospace Engineer-
                                    ing from K.N. Toosi University of
Technology and Sharif University of Technology (Tehran, Iran) in
2012 and 2014, respectively. His research focuses on robotics for sci-                                      Yuchi Zhao is a research assistant
entific discoveries, shared autonomy, and humanoid robotics.                                                in the Computer Science Depart-
                                                                                                            ment of the University of Toronto.
                                   Sebastian Arellano-Rubach is in                                          His research mainly focuses on
                                   grade 11 at the University of                                            robot manipulation, perception and
                                   Toronto Schools. In 2023, he spent                                       tactile sensing for self-driving labs.
                                   the summer working for the Com-                                          He received his B.A.Sc degree
                                   puter Science Department at UofT.                                        in Mechatronics Engineering from
                                   His work focuses mostly on web-                                          the University of Waterloo in 2023.
                                   site design, front-end development,
                                   back-end development, develop-
                                   ment tools, performance optimiza-
                                   tion, responsiveness, and SEO.


                                                                                                            Haoping Xu is a senior Ph.D.
                                                                                                            student from RA2D : Robotics-
                                                                                                            assisted Accelerated Discovery lab
                                   Zhi Ji is a dedicated Engineer-                                          at the Acceleration Consortium.
                                   ing Science student at the Uni-                                          He is supervised by Prof Alán
                                   versity of Toronto, specializing in                                      Asupuru-Guizk, Prof Animesh Grag
                                   Machine Intelligence (AI) and minor-                                     and Prof Florian Shkurti. RA2 D
                                   ing in Engineering Business. She                                         lab is focused on building univer-
                                   is very passionate about AIMLDL.                                         sal robot for lab automation and
                                                                                                            accelerating science discoveries.
                                                                                                            Haoping’s research focus is com-
                                                                                                            puter vision and robotics control
                                                                                                            related to lab automation. In par-
                                                                                                            ticular, he is interested in percep-
                                                                                                            tion and vision guided robot plan-
                                                                        ning and control for transparent objects. He has publications in top-
                                                                        ics of 2D perception, depth completion, multiview 3D perception and
                                                                        robot manipulations for transparent objects in lab settings.
                                   Lasse Bjørn Kristensen is a
                                   postdoctoral researcher working in                                       Artur Kuramshin recieved the
                                   Alán Aspuru-Guzik’s lab on quan-                                         HBSc degree in Computer Sci-
                                   tum computing, machine learning,                                         ence with a specialization in Com-
                                   and algorithms at the intersection                                       puter Vision from the University
                                   of the two. He obtained his PhD                                          of Toronto (UofT) in 2023. Dur-
                                   from Aarhus University in 2020,                                          ing his time at UofT, he was part
                                   where his research focus was on                                          of the Robot Vision and Learning
                                   the use of superconducting cir-                                          (RVL) lab.
                                   cuits and their quantum dynamics
                                   for quantum computing. Before
                                   this, he received his MSc in 2017
                                   and his BSc in 2015 at the same
                                   institution, both within the field of
                                   Physics.



                                                                                                                                    123
1086                                                                          Autonomous Robots (2023) 47:1057–1086


                                     Alán Aspuru-Guzik research lies               Animesh Garg received the PhD
                                     at the interface of computer sci-             degree from University of Califor-
                                     ence with chemistry and physics.              nia, Berkeley and was a postdoc
                                     He integrates robotics, machine               at Stanford AI lab. He is a CIFAR
                                     learning and quantum chemistry                chair Assistant Professor of com-
                                     to develop “self-driving laborato-            puter science with the University
                                     ries”, accelerating rates of scien-           of Toronto, a faculty member with
                                     tific discovery. He develops quan-            the Vector Institute, and a senior
                                     tum computer algorithms and has               research scientist with Nvidia. He
                                     pioneered quantum algorithms for              works on the Algorithmic Foun-
                                     the simulation of matter. He is a             dations for Generalizable Auton-
                                     Professor of Chemistry and Com-               omy, to enable AI-based robots to
                                     puter Science at the University of            work alongside humans.
                                     Toronto, faculty member at the
                                     Vector Institute for Artificial Intel-
ligence and Director of the Acceleration Consortium, a University of
Toronto-based strategic initiative that aims to gather researchers from
industry, government and academia around topics related to the labs
of the future. He was previously a full professor at Harvard Univer-
sity where he started his career in 2006. He is currently the Canada
150 Research Chair in Theoretical Chemistry, CIFAR AI Chair at the
Vector Institute and co-founder of Zapata Computing and Kebotix, two
early-stage ventures in quantum computing and self-driving laborato-
ries.

                                  Florian Shkurti is an Assistant Pro-
                                  fessor in the Department of Com-
                                  puter Science at the University of
                                  Toronto, where he also serves as
                                  a Faculty Member at the UofT
                                  Robotics Institute and a Faculty
                                  Affiliate at the Vector Institute. He
                                  earned his Ph.D. in Computer Sci-
                                  ence and Robotics from McGill
                                  University in 2018. He leads the
                                  Robot Vision and Learning (RVL)
                                  lab, focusing on robotics research
                                  encompassing machine learning,
                                  perception, planning, and control.
                                  Florian’s research has been applied
to environmental monitoring by autonomous robots, visual navigation
for autonomous vehicles, and mobile manipulation.




123
