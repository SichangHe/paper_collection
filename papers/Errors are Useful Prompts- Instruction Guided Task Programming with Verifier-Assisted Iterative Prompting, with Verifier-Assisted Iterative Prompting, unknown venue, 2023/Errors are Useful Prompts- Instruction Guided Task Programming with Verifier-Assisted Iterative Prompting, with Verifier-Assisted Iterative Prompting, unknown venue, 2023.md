                                              Errors are Useful Prompts: Instruction Guided Task Programming
                                                          with Verifier-Assisted Iterative Prompting
                                              Marta Skreta∗1,2 , Naruki Yoshikawa∗1,2 , Sebastian Arellano-Rubach3 , Zhi Ji1 , Lasse Bjørn Kristensen1 ,
                                                       Kourosh Darvish1,2 , Alán Aspuru-Guzik1,2 , Florian Shkurti1,2 , Animesh Garg1,2,4

                                            Abstract— Generating low-level robot task plans from high-                                                 Chemistry experiment
                                         level natural language instructions remains a challenging prob-
                                                                                                                                                         Repeat this 2 times:
                                         lem. Although large language models have shown promising
                                                                                                                                                    Add 15 g acetic acid to beaker.
                                         results in generating plans, the accuracy of the output remains
arXiv:2303.14100v1 [cs.RO] 24 Mar 2023




                                                                                                                                                         Stir for 20 seconds.
                                         unverified. Furthermore, the lack of domain-specific language                       Structured language generation                         Structured language generation
                                         data poses a limitation on the applicability of these models.                                by CLAIRify                                     without iterative prompting
                                         In this paper, we propose CLAIR IFY, a novel approach that                           <XDL>                                                  <XDL>
                                                                                                                              <Hardware>                                             <Hardware>
                                         combines automatic iterative prompting with program verifica-                          <Component id="beaker">       Error: Hardware
                                                                                                                                                                                       <Vessel id="beaker">
                                                                                                                                                              can only contain
                                         tion to ensure programs written in data-scarce domain-specific                       </Hardware>
                                                                                                                              ...
                                                                                                                                                              Component tags
                                                                                                                                                                                     </Hardware>
                                                                                                                                                                                     ...
                                         language are syntactically valid and incorporate environment                         <Procedure>                                            <Procedure>
                                                                                                                                ...                                                    ...
                                         constraints. Our approach provides effective guidance to the                           <Repeat repeats="2">
                                                                                                                                                              Error: Steps attri-
                                                                                                                                                              bute not defined         <Repeat steps="2">
                                         language model on generating structured-like task plans by                               <Add vessel="beaker"
                                                                                                                                     reagent="acetic acid"    Error: "beaker1"
                                                                                                                                                                                         <Add vessel="beaker1"
                                                                                                                                                                                            reagent="acetic acid"
                                         incorporating any errors as feedback, while the verifier ensures                            amount="15 g"/>          not defined in                amount="15 g"/>
                                                                                                                                  <Stir vessel="beaker"       Hardware                   <Stir vessel="beaker1"
                                         the syntactic accuracy of the generated plans. We demon-                                    time="20 s"/>                                          time="20 s"/>
                                                                                                                                </Repeat>                                              </Repeat>
                                         strate the effectiveness of CLAIR IFY in planning chemistry                          </Procedure>                                           </Procedure>
                                         experiments by achieving state-of-the-art results. We also show                      </XDL>                                                 </XDL>

                                         that the generated plans can be executed on a real robot by
                                         integrating them with a task and motion planner.                                                                                                  Not executable

                                                                   I. I NTRODUCTION                                               TAMP

                                            Leveraging natural language instruction to create a plan
                                         comes naturally to humans. However, when a robot is
                                                                                                                                                   Heterogeneous lab
                                         instructed to do a task, there is a communication barrier:                                                 devices & robots
                                         the robot does not know how to convert the natural language
                                                                                                                          Fig. 1: Task plans generated by LLMs may contain syntactical errors
                                         instructions to lower-level actions it can execute, and the
                                                                                                                          in domain-specific languages. By using verifier-assited iterative
                                         human cannot easily formulate lower-level actions. Large                         prompting, CLAIR IFY can generate a valid program, which can be
                                         language models (LLMs) can fill this gap by providing a rich                     executed by a robot.
                                         repertoire of common sense reasoning to robots [1, 2].
                                            Recently, there has been impressive progress in using                         information about the world state and robot capabilities, as
                                         LLMs [1, 3, 4] for problems involving structured outputs,                        well as general reasoning about the physical world [10].
                                         including code generation [5–7] and robot programming [8].                          Data scarcity for domain-specific languages – It is
                                         These code generation models are often trained on code that is                   difficult for LLMs to generate task plans in a zero-shot
                                         widely available on the Internet and perform well in few-shot                    manner for domain-specific languages (DSLs), such as those
                                         settings for generating code in those languages. However, to                     in chemistry and physics because there is significantly less
                                         employ LLMs for task-plan generation there are two main                          data on the Internet for those specific domains, so LLMs
                                         issues to address: (1) lack of task-plan verification and (2)                    are unable to generalize well with no additional information
                                         poor performance for data-scarce domain-specific languages.                      [11, 12]. It is possible to address this by fine-tuning models
                                            Lack of task plan verification – Task plans generated by                      on pairs of natural-language inputs and structured-language
                                         LLMs, often, cannot be executed out-of-the-box with robots.                      outputs, but it is very difficult to acquire training datasets large
                                         There are two reasons for that. First, machine-executable                        enough for the model to learn a DSL reasonably well [13],
                                         languages are bound by strict rules [9]. If the generated                        and there is a large computation cost for fine-tuning LLMs
                                         task plan does not adhere to them, it will not be executable.                    [14]. However, it has been shown that LLMs can adapt to
                                         Hence, we need a way to verify the syntactic correctness of the                  new domains with effective prompting [15]. Our insight is to
                                         structured task plan. Second, LLMs might generate a task plan                    leverage the in-context ability of an LLM by providing the
                                         that looks reasonable (i.e. is syntactically correct) but is not                 rules of a structured language as input, to generate a plan
                                         actually executable by a robot. Avoiding this problem requires                   according to the template of the target DSL.
                                                                                                                             In this work, we propose to address the verification and
                                            ∗ Authors contributed equally, 1 University of Toronto, 2 Vector Institute,
                                                                                                                          data-scarcity challenges. We introduce CLAIR IFY1 , a frame-
                                         3 University of Toronto Schools, 4 NVIDIA
                                           Email: {martaskreta,naruki}@cs.toronto.edu
                                           Email: {kdarvish,garg}@cs.toronto.edu                                            1 CLAIR IFY website: https://ac-rad.github.io/clairify/
work that translates natural language into a domain-specific      example, Inner Monologue [27] uses LLMs in conjunction
structured task plan using an automated iterative verification    with environment feedback from various perception models
technique to ensure the plan is syntactically valid in the        and state monitoring. However, because the system has
target DSL (Figure 1) by providing the LLM a description          no constraints, it can propose plans that are nonsensical.
of the target language. Our model also takes into account         SayCan [10], on the other hand, grounds task plans generated
environment constraints if provided. The generated structured-    by LLMs in the real world by providing a set of low-level
language-like output is evaluated by our verifier, which          skills the robot can choose from. A natural way of generating
checks for syntax correctness and for meeting environment         task plans is using code-writing LLMs because they are not
constraints. The syntax and constraint errors are then fed        open-ended (i.e. they have to generate code in a specific
back into the LLM generator to generate a new output. This        manner in order for it to be executable) and are able to
iterative interaction between the generator and the verifier      generate policy logic. Several LLMs trained on public code
leads to grounded syntactically correct target language plans.    are available, such as Codex [5], CodeT5 [6], AlphaCode [7]
   We evaluate the capabilities of CLAIR IFY using a domain-      and CodeRL [28]. LLMs can be prompted in a zero-shot way
specific language called Chemical Description Language            to generate task plans. For example, Code as Policies [8]
(XDL) [16] as the target structured language unfamiliar to the    repurposes code-writing LLMs to write robot policy code and
LLM. XDL is an XML-based DSL to describe action plans             ProgPrompt [2] generates plans that take into account the
for chemistry experiments in a structured format, and can         robot’s current state and the task objectives. However, these
be used to command robots in self-driving laboratories [17].      methods generate Pythonic code, which is abundant on the
Converting experiment descriptions to a structured format         Internet. For DSLs, naive zero-shot prompting is not enough;
is nontrivial due to the large variations in the language         the prompt has to incorporate information about the target
used. Our evaluations show that CLAIR IFY outperforms             language so that the LLM can produce outputs according to
the current state-of-the-art XDL generation model in [16].        its rules.
We also demonstrate that the generated plans are executable       C. Leveraging Language Models with External Knowledge
by combining them with an integrated task and motion                 A challenge with LLMs generating code is that the
planning (TAMP) framework and running the corresponding           correctness of the code is not assured. There have been many
experiments in the real world. Our contributions are:             interesting works on combining language models with external
• We propose a framework to produce task plans in a DSL
                                                                  tools to improve the reliability of the output. Mind’s Eye [12]
   using an iterative interaction of an LLM-based generator       attempts to ground large language model’s reasoning with
   and a rule-based verifier.                                     physical simulation. They trained LLM with pairs of language
• We show that the interaction between the generator and
                                                                  and codes and used the simulation results to prompt an
   verifier improves zero-shot task plan generation.              LLM to answer general reasoning questions. Toolformer [29]
• Our method outperforms the existing XDL generation
                                                                  incorporates API calls into the language model to improve a
   method in an evaluation by human experts.                      downstream task, such as question answering, by fine-tuning
• We integrate our generated plans with a TAMP framework,
                                                                  the model to learn how to call API. LEVER [30] improves
   and demonstrate the successful translation of elementary       LLM prompting for SQL generation by using a model-based
   chemistry experiments to a real robot execution.               verifier trained to verify the generated programs. As SQL
                    II. R ELATED WORK                             is a common language, the language model is expected to
A. Task Planning                                                  understand its grammar. However, for DSLs, it is difficult to
   High-level task plans are often generated from a limited       acquire training datasets and expensive to execute the plans
set of actions [9], because task planning becomes intractable     to verify their correctness. Our method does not require fine-
as the number of actions and time horizon grows [18]. One         tuning any models or prior knowledge on the target language
approach to do task planning is using rule-based methods [16,     within the language model. Our idea is perhaps closest to
19]. More recently, it has been shown that models can learn       LLM-AUGMENTER [31], which improves LLM outputs by
task plans from input task specifications [20–22], for example    giving it access to external knowledge and automatically
using hierarchical learning [23, 24], regression based planning   revising prompts in natural language question-answering tasks.
[25], reinforcement learning [26]. However, to effectively        Our method similarly encodes external knowledge in the
plan task using learning-based techniques, large datasets are     structure of the verifier and prompts, but for a structured and
required that are hard to collect in many real-world domains.     formally verifiable domain-specific language.
Our approach, on the other hand, generates a task plan directly          III. TASK P ROGRAMMING WITH CLAIR IFY
from an LLM in a zero-shot way on a constrained set of tasks      CLAIR IFY Overview – We present a system that takes as
which are directly translatable to robot actions. We ensure       input the specifications of a structured language (i.e. all its
that the plan is syntactically valid and meets environment        rules and permissible actions) as well as a task we want to
constraints using iterative error checking.                       execute written in natural language and outputs a syntactically
B. Task Planning with Large Language Models                       correct task plan. A general overview of the CLAIR IFY
   Recently, many works have used LLMs to translate natural       pipeline is in Figure 2. We combine input instruction and
language prompts to robot task plans [2, 8, 10, 27]. For          language description into a prompt and pass the prompt into
                                                                                                                                                  Fig. 2: System overview:
                                                                 Available hardware: beaker V1                                                    The LLM takes the input
                             Structured                          Available reagents: acetic acid
                              language                                                                                                            (1), structured language
                             definition                                      Environment                                                          definition, and (optionally)
                                                                              constraints                         Pass
      Add 40 g acetic
                        1
                                                                                                                                      5           resource constraints and
                                               Feedback                                            <Add vessel="V1" reagent="acetic
      acid to beaker
                                                                       3                                acid" amount="40 g"/>                     generates unverified struc-
                                       Quantity is not a permissible
        Natural
                                        attribute for the Add tag.                                                                                tured language (2). The
                                                                              Structured             Structured                         Robot     output is examined by the
       language                 LLM                                        language verifier          language           TAMP
         input                                                                                                                        execution
                                                                                                                                                  verifier, and is passed to
                                              Unverified                                                                 6                        LLM with feedback (3).
                                              structured                                                                                          The LLM-generated out-
                                               language
                                                                                            2
                                                                                                                                                  puts passes through the
                            Wrong output     <Add vessel="V1" reagent="acetic                                                                     verifier (4). The correct
                                                 acid" quantity="40 g"/>
                                                                                                                                                  output (5) is passed to the
                                 OR
                                                                                            4                                                     task and motion planner
                            Correct output   <Add vessel="V1" reagent="acetic                                                                     to generate robot trajecto-
                                                   acid" amount="40 g"/>
                                                                                                                                                  ries. The robot executes
                                                                                                                                                  the planned trajectory (6).

the structured language generator (here we use GPT-3 [1],                                           Algorithm 1 CLAIR IFY: Verifier-Assisted Iterative Prompts
a large language model). However, we cannot guarantee the                                           Input: Structured language description L, instruction x
output from the generator is syntactically valid, meaning                                           Output: Structured language task plan, ySL
                                                                                                      procedure I TERATIVE P ROMPTING(L, x)
that it would definitely fail to compile into lower-level robot                                          ySL0 = Generator(L, x)
actions. To generate syntactically valid programs, we pass                                               errors = Verifier(ySL0 )
the output of the generator through a verifier. The verifier                                             while len(errors) > 0 or timeout condition != True do
                                                                                                             ySL0 = Generator(L, x, ySL0 , errors)
determines whether the generator output follows all the rules                                                errors = Verifier(ySL0 )
and specifications of the target structured language and can                                             ySL = ySL0
be compiled without errors. If it cannot, the verifier returns
error messages stating where the error was found and what                                           is as “structured-language-like”). To ensure the syntactical
it was. This is then appended to the generator output and                                           correctness of the generated code, the generator is iteratively
added to the prompt for the next iteration. This process is                                         prompted by the automated interaction with the verifier. The
repeated until a valid program is obtained, or until the timeout                                    generated code is passed through the verifier, and if no errors
condition is reached (if that happens, an error is thrown for                                       are generated, then the code is syntactically correct. If errors
the user). Algorithm 1 describes of our proposed method.                                            are generated, we re-prompt the LLM with the incorrect
   Once the generator output passes through the verifier with                                       task plan from the previous iteration along with the list of
no errors, we are guaranteed that it is syntactically valid                                         errors indicating why the generated steps were incorrect.
structured language. This program can then be translated into                                       The skeleton of the iterative prompt is shown in Snippet 2,
lower-level robot actions by passing through TAMP for robot                                         Figure 3. Receiving the feedback from the verifier is used
execution. Each component of the pipeline is described in                                           by the LLM to correct the errors from the previous iteration.
more detail below.                                                                                  This process is continued until the generated code is error-free
CLAIR IFY in Chemistry Lab Automation – While our                                                   or a timeout condition is reached, in which case we say we
pipeline can in theory be applied to any structured language,                                       were not able to generate a task plan.
we demonstrate it using the chemical description language                                           B. Verifier
(XDL) [16] as an example of a structured language. XDL
                                                                                                       The verifier works as a syntax checker and static analyzer
describes the hardware and reagents to be used in the experi-
                                                                                                    to check the output of the generator and send feedback
ment, and the experimental procedures in chronological order.
                                                                                                    to the generator. It first checks whether the input can be
Note that chemistry proceures are not well standardized; there
                                                                                                    parsed as a correct XML and then checks the allowance of
is a lot of variation, and so translating them to a structured
                                                                                                    action tags, the existence of mandatory properties, and the
plan that can be executed by a robot is nontrivial [32].
                                                                                                    correctness of optional properties. This evaluates if the input
A. Generator                                                                                        is syntactically correct XDL. It also checks the existence of
   The generator takes a user’s instruction and generates                                           definitions of hardware and reagents used in the procedure or
structured-language-like output using a large language model                                        provided as environment constraints, which works as a simple
(LLM) using a description of the structured language. The                                           static analysis of necessary conditions for executability. If
input prompt skeleton is shown in Snippet 1, Figure 3. The                                          the verifier catches any of these errors, the candidate task
description of the XDL language includes its file structure and                                     plan is considered to be an invalid. The verifier returns a list
lists of the available actions (can be thought of as functions),                                    of errors it found, which is then fed back to the generator.
their allowed parameters and their documentation.
   Although the description of the target structured language                                       C. Incorporating Environment Constraints
information is provided, the candidate task plan is not                                               Because resources in a robot workspace are limited, we
guaranteed to be syntactically correct (hence we refer to                                           need to consider those constraints when generating task
initial_prompt = """                                                TABLE I: Comparison of our method with existing methods on the
                                         Fig.      3:    Prompt
# <Description of XDL>                                              number of successfully generated valid XDL plans and their quality
                                         skeleton: (1) At the
                                                                    on 108 organic chemistry experiments from [34].
# <Hardware constraints(optional)>       initial generation, we
# <Reagent constraints (optional)>
                                         prompt the LLM with a        Dataset         Method        Number generated ↑   Expert preference ↑
Convert to XDL:                          description of XDL and      Chem-RnD    SynthReader [16]         92/108               13/108
# <Natural language instruction>
"""
                                         the natural language                    CLAIR IFY [ours]        105/108               75/108
                                         instruction. (2) After      Chem-EDU    SynthReader [16]          0/40                   -
       Snippet 1: Initial prompt         the LLM generates                       CLAIR IFY [ours]         40/40                   -
                                         structured-language-
iterative_prompt = """                   like output, we pass       chose to use this instead of code-davinci-002 due to
# <Description of XDL>                   it through our verifier.   query and token limits.
# <Hardware constraints(optional)>       If there are errors in        To execute the plans in the real world, we use an altered
# <Reagent constraints (optional)>       the generated program,
                                         we concatenate the
                                                                    version of Franka Emika Panda arm robot, equipped with
Convert to XDL:
# <Natural language instruction>         initial prompt with the    a Robotiq 2F-85 gripper, to handle vessels. The robot also
# <XDL from previous iteration>          XDL from the previous      communicates with instruments in the chemistry laboratory,
This XDL was not correct.
There were the errors                    iteration and a list of    such as a weighing scale and a magnetic stirrer. These devices
# <List of errors, one per line>         the errors.                are integrated to enable pouring and stirring skills.
Please fix the errors
"""
                                                                    Datasets – We evaluated our method on two different datasets:
      Snippet 2: Iterative prompt                                      (1) Chem-RnD [Chemistry Research & Development]:
                                                                    This dataset consists of 108 detailed chemistry-protocols
plans. If specified, we include the available resources into the    for synthesizing different organic compounds in real-world
generator prompt. The verifier also catches if the candidate        chemistry labs, sourced from the Organic Syntheses dataset
plan uses any resources aside from those mentioned among            (volume 77) [34]. Due to GPT-3 token limits, we only use
the available robot resources. Those errors are included in         experiments with less than 1000 characters. We use Chem-
the generator prompt for the next iteration. If a constraint        RnD as a proof-of-concept that our method can generate task
list is not provided, we assume the robot has access to all         plans for complex chemistry methods. We do not aim to
resources. In the case of chemistry lab automation, those           execute the plans in the real world, and so we do not include
resources include experiment hardware and reagents.                 any constraints.
D. Interfacing with Planner on Real Robot                              (2) Chem-EDU [Everyday Educational Chemistry]:
   In many cases, the target DSL is not embodied, and it is         We evaluate the integration of CLAIR IFY with real-world
hardware independent. Our verified task plan only contains          robots through a dataset of 40 natural language instructions
high-level descriptions of actions. To execute those actions by     containing only safe (edible) chemicals and that are, in
a robot, we need to map them to low-level actions and motion        principle, executable by our robot. The dataset consists
that the robot can execute. To ensure the generated structured      of basic chemistry experiments involving edible household
language is executable by the robot, we employ a task and           chemicals, including acid-base reactions and food preparation
motion planning (TAMP) framework. In our case, we use               procedures2 . When generating the XDL, we also included
PDDLStream [9] to generate robot action and motion plans            environment constraints based on what equipment our robot
simultaneously. In this process, visual perception information,     had access to (for example, our robot only had access to a
coming from the robot camera, grounds the predicates for            mixing container called “beaker").
PDDLStream, and verified task plans are translated into             B. Metrics and Results
problem definitions in PDDLStream.                                     The results section is organized based on the four per-
   For the chemistry lab automation domain, high-level actions      formance metrics that we will consider, namely: Ability to
in XDL are mapped to intermediate goals in PDDLStream,              generate structured-language output, Quality of the generated
resulting in a long-horizon multistep planning problem              plans, Number of interventions required be the verifier, and
definition. To also incorporate safety considerations for robot     Robotic validation capability. We compared the performance
execution, We use a constrained task and motion planning            of our method with SynthReader, a state-of-the-art XDL
framework for lab automation [33] to execute the XDL                generation algorithm which is based on rule-based tagging
generated by CLAIR IFY.                                             and grammar parsing of chemical procedures [16]
           IV. E XPERIMENTS AND E VALUATION                            (1) Ability to generate a structured language plan. First,
  Our experiments are designed to evaluate the following            we investigate the success probability for generating plans. For
hypotheses: i) Automated iterative prompting increases the          CLAIR IFY, if it is in the iteration loop for more than x steps
success rate of unfamiliar language generation, ii) The quality     (here, we use x = 10), we say that it is unable to generate
of generated task plans is better than existing methods, iii)       a plan and we exit the program. When comparing with
Generated plans can be executed by actual hardware.                 SynthReader, we consider that approach unable to generate a
                                                                    structured plan if the SynthReader IDE (called ChemIDE3 )
A. Experimental Setup
  To generate XDL plans, we use text-davinci-003,                     2 CLAIR IFY Data & code: https://github.com/ac-rad/xdl-generation/

the most capable GPT-3 model at the time of writing. We               3 ChemIDE using XDL: https://croningroup.gitlab.io/chemputer/xdlapp/
Fig. 4: Violin plots showing distributions of different error categories in XDL plans generated for experiments for the Chem-RnD
(left) and Chem-EDU (right) datasets. The x-axis shows the error categories and the y-axis shows the number of errors for that category
(lower is better). For the Chem-RnD dataset, we show the error distributions for both CLAIR IFY and SynthReader. Each violin is split in
two, with the left half showing the number of errors in plans generated from CLAIR IFY (teal) and the right half showing those from
SynthReader (navy). For the Chem-EDU dataset, we only show the distributions for CLAIR IFY. In both plots, we show the mean of the
distribution with a gold dot (and the number beside in gold) and the median with a grey dot.

throws a fatal error when asked to create a plan. For both           20 were considered to be of similar quality).
models, we also consider them unable to generate a plan if              The distributions of the annotated errors are shown in
the generated plan only consists of empty XDL tags (i.e. no          Figure 4. We find that for 4 out of 6 error categories, our
experimental protocol). For all experiments, we count the total      model does at least as well as or better than the baseline
number of successfully generated language plans divided by           method when considering the mean and median of the
the total number of experiments. Using this methodology, we          distributions. We also find that for those categories, our
tested the ability of the two models to generate output on both      method produces more experiments with 0 errors.
the Chem-RnD and Chem-EDU datasets. The results for both                One advantage of our method is that it generates less
models and both datasets are shown in Table I. We find that          plans with missing actions compared with the baseline. As
out of 108 Chem-RnD experiments, CLAIR IFY successfully              XDL generation in SynthReader is implemented by rule-
returned a plan 97% of the time, while SynthReader returned a        based pattern-matching techniques, any actions that do not
plan 85% of the time. For the Chem-EDU dataset, CLAIR IFY            match those templates would not appear in the final XDL.
generated a plan for all instructions. SynthReader was unable        For example, for the protocol:
to generate any plans for that dataset, likely because the           To a solution of m-CPBA (200 mg, 0.8 mmol) in dichloromethane
                                                                     (10 mL), cooled to 0 ◦ C, was added dropwise a solution of 5-
procedures are different from typical chemical procedures            chloro-10-oxa-3-thia-tricyclo [5.2.1.01, 5] dec-8-ene (150 mg,
                                                                     0.8 mmol) in dichloromethane (10 mL).
(they use simple action statements). This demonstrates the
generalizability of our method: we can apply it to different         the plan generated by CLAIR IFY was
language styles and domains and still obtain coherent plans.         <Add vessel="V1" reagent="m-CPBA" amount="200 mg"/>
                                                                     <Add vessel="V1" reagent="dichloromethane" volume="10 mL"/>
   (2) Quality of the predicted plan (without executing              <HeatChill vessel="V1" temp="0 ◦ C" time="3 min"/>
                                                                     <Add vessel="V2" reagent="5-chloro-10-oxa-3-thia-tricyclo
the plan). To determine if the predicted task plans actually         [5,2,1,0*1,5*]dec-8-ene" amount="150 mg"/>
accomplish every step of their original instructions, we report      <Add vessel="V2" reagent="dichloromethane" volume="10 mL"/>
                                                                     <Transfer from_vessel="V2" to_vessel="V1"/>
the number of actions and parameters that do not align
between the original and generated plan, as annotated by             while the plan generated from SynthReader was
                                                                     <Add vessel="reactor" reagent="5-chloro-10-oxa-3-thia-tricyclo"
expert experimental chemists. To compare the quality of the           volume="0" speed="40.0"/>
generated plans between CLAIR IFY and SynthReader, we
ask expert experimental chemists to, given two anonymized               Our model is able to decompose a complicated procedure
plans, either pick a preferred plan among them or classify           into simpler actions by making two solutions in separate
them as equally good. We also ask them to annotate errors in         beakers and combining them with a Transfer procedure. It
the plans in the following categories: Missing action, Missing       also assumes that the solutions don’t already exist as mixtures
parameter, Wrong action, Wrong parameter, Ambiguous                  and creates them from scratch. This is another benefit of
value, Other error. Here, actions refer to high-level steps in       our model, as it is able to understand implicit actions. For
the procedure (e.g., <Add reagent="acetic acid">                     example, given the prompt
                                                                     L-Ornithine (31.92 g, 120 mmol) was added to a mixture of KOH
is an action) and parameters refer to reagents, hardware,            (6.72 g, 120 mmol), water (200 ml) and THF (100 ml)
quantities and experiment descriptors (e.g., in <HeatChill
vessel="beaker" temp="100C">, vessel and temp                        SynthReader considers a mixture of three chemicals as a
are both parameters). The annotations were performed using           single solution and creates the action:
                                                                     <Add vessel="reactor" reagent="a mixture of KOH (6.72 g, 120
the LightTag Text Annotation Tool [35].                              mmol), water (200 ml) and THF (100 ml)" volume="0" speed="40.0"
                                                                     />
Chem-RnD dataset – The results for the Chem-RnD dataset              <AddSolid vessel="reactor" reagent="L-Ornithine" mass="31.92 g"
                                                                     />
with respect to expert preference are reported in the last
column of Table I. We found that out of 108 experiments,             On the other hand, CLAIR IFY correctly understand the
experts preferred the XDL plan generated from CLAIR IFY 75           implicit action to mix them beforehand and generates an
times and the one from SynthReader 13 times (the remaining           appropriate XDL:
TABLE II: Verifier Analysis. We report the average number of                           TABLE III: Number of XDL plans successfully generated for
times CLAIR IFY calls the verifier for the experiments in a given                      different error message designs in the iterative prompting scheme
dataset, as well as the minimum and maximum number of times.                           on a validation set from Chem-RnD.
We also report the type of error encountered by the verifier and the
number of times it caught that type.                                                    Variations of Iterative Prompt Design using Verifier   Plan’s generated
                                                                                        Error Messages                                         success rate (%) ↑
   Dataset   Average num.      Max/min         Error type caught by verifier [count]
             verifier calls   verifier calls
                                                                                        Naive: XDL from previous iteration and string “This    0
                                                                                        XDL was not correct. Please fix the errors.”
  Chem-RnD    2.58 ± 2.00         10/1          - missing property in action [306]
                                               - property not allowed [174]             Last Error: Error List from verifier from previous     30
                                               - wrong tag [120]                        iteration
                                               - action does not exist [21]             All Errors cumulative: Accumulated error List from     50
                                               - item not defined in Hardware or        all previous iterations
                                                Reagents list [15]
                                               - plan cannot be parsed as XML [6]       XDL + Last Error: XDL and Error List from verifier     100
 Chem-EDU     1.15 ± 0.45          3/1          - item not defined in Hardware or
                                                                                        from previous iteration
                                                Reagents list [47]
                                               - property not allowed [26]             that the error breakdown is similar to that from Chem-RnD,
                                               - wrong tag [40]                        where we see amibiguous values in experiments that have
                                               - missing property in action [3]
                                                                                       conditionals instead of precise values. We also encounter
<Add vessel="V1" reagent="L-Ornithine" amount="31.92 g"/>                              a few wrong parameter errors, where the model does not
<Add vessel="V1" reagent="KOH" amount="6.72 g"/>
<Add vessel="V1" reagent="Water" amount="200 ml"/>                                     include units for measurements. This can be fixed in future
<Add vessel="V1" reagent="THF" amount="100 ml"/>
                                                                                       work by improving the verifier to check for these constraints.
                                                                                          (3) Number of interventions required by the verifier. To
   However, our model produced plans with a greater number
                                                                                       better understand the interactions between the generator and
of wrong actions than SynthReader. This is likely because
                                                                                       verifier in CLAIR IFY, we analyzed the number of interactions
our model is missing domain knowledge on certain actions
                                                                                       that occur between the verifier and generator for each dataset
that need to be included in the prompt or verifier. For
                                                                                       to understand the usefulness of the verifier. In Table II,
example, given the instruction "Dry solution over magnesium
                                                                                       we show that each experiment in the Chem-RnD dataset
sulfate", our model inserts a <Dry .../> into the XDL
                                                                                       runs through the verifier on average 2.6 times, while the
plan, but the instruction is actually referring to a procedure
                                                                                       Chem-EDU dataset experiments runs through it 1.15 times
where ones passes the solution through a short cartridge
                                                                                       on average. The difference between the two datasets likely
containing magnesium sulphate, which seems to be encoded
                                                                                       exists because the Chem-EDU experiments are shorter and
in SynthReader. Another wrong action our model performs is
                                                                                       less complicated. The top Chem-EDU error encountered by
reusing vessels. In chemistry, one needs to ensure a vessel is
                                                                                       the verifier was that an item in the plan was not define in
uncontaminated before using it. However, our model generates
                                                                                       the Hardware or Reagents list, mainly because we included
plans that can use the same vessel in two different steps
                                                                                       hardware constraints for this dataset that we needed to match
without washing it in between. Our model also sometimes
                                                                                       in our plan. In Figure 5, we show a sample loop series
generates plans with ambiguous values. For example, many
                                                                                       between the generator and verifier.
experiment descriptions include conditional statements such
                                                                                          (4) Robotic validation (Chem-EDU only). To analyze
as “Heat the solution at the boiling point until it becomes
                                                                                       how well our system performs in the real world, we execute
white”. Conditions in XDL need a numerical condition
                                                                                       a few experiments from the Chem-EDU dataset on our robot.
as a parameter. Our model tries to incorporate them by
                                                                                       Three experiments from the Chem-EDU dataset were selected
including actions such as <HeatChill temp="boiling
                                                                                       to be executed.
point" time="until it becomes white"/>, but
they are ambiguous. We can make our model better in the                                Solution Color Change Based on pH – As a basic chemistry
future by incorporating more domain knowledge into our                                 experiment, we demonstrated the color change of a solution
structured language description and improving our verifier                             containing red cabbage juice. This is a popular introductory
with real-world constraints. For example, we can incorporate                           demonstration in chemistry education, as the anthocyanin
visual feedback from the environment, include look-up tables                           pigment in red cabbage can be used as a pH indicator [36]. We
for common boiling points, and ensure vessels are not reused                           prepared red cabbage solution by boiling red cabbage leaves
before cleaning.                                                                       in hot water. The colour of the solution is dark purple/red.
                                                                                       Red cabbage juice changes its color to bright pink if we add
   Despite the XDL plans generated by our method containing
                                                                                       an acid and to blue if we add a base, and so we acquired
errors, we found that the experts placed greater emphasis
                                                                                       commercially-available vinegar (acetic acid, an acid) and
on missing actions than ambiguous or wrong actions when
                                                                                       baking soda (sodium bicarbonate, a base).
picking the preferred output, indicating larger severity of this
                                                                                          In this experiment, we generated XDL plans using CLAIR-
class of error for the tasks and outputs investigated here.
                                                                                       IFY from two language inputs:
Chem-EDU dataset – We annotated the errors in the Chem-                                [1] Add 40 g of red cabbage solution into a beaker. Add 10 g of
                                                                                        acetic acid into the beaker, then stir the solution for 10
EDU datasets using the same annotation labels as for the                               seconds.
Chem-RnD dataset. The breakdown of the errors is in the left                           [2] Add 40 g of red cabbage solution into a beaker. Add 10 g of
                                                                                        baking soda into the beaker, then stir the solution for 10
plot of Figure 4. Note that we did not perform a comparison                            seconds.
with SynthReader as no plans were generated from it. We find
                                               Unveriﬁed structured language                                                                   Veriﬁed structured language
                                                                                                        Feedback, iteration 1
                                             <XDL>                                              1                                           <XDL>
                                               <Synthesis>                                          The Hardware section should only          <Synthesis>
                                                 <Hardware>   [unavailable]                          contain Component tags
                                                                                                                                                <Hardware>
                                              1    <Vessel id="container"/>
                                                                                                    The solid property in Reagent is not
                                                                                                                                                    <Component id="beaker"/>
                                                   <StirBar/>                                                                                       <Component id="stir bar"/>
                                                                                                     allowed
                                                 </Hardware>   3       2                                                                        </Hardware>
                                                                                   Veriﬁer          container is not defined in Hardware
            Initial prompt
            The available Hardware is:
                                                <Reagents>                              Fail            Feedback, iteration 2
                                                                                                                                               <Reagents>
            beaker, stir bar
                                                   <Reagent name="acetic acid"                  2                                                  <Reagent name="acetic
                                                1    solid="true"/>
                                                                                                    The Hardware section should only                 acid"/>
                                                   <Reagent name="red cabbage                                                                      <Reagent name="red
            Convert to XDL:                                                                          contain Component tags
                                                     solution" solid="false"/>                                                                       cabbage solution"/>
            Add 15 g of acetic acid to          </Reagents>                                         container is not defined in the given
                                                                                                                                               </Reagents>
            container. Add 30 g red                                  1                               Hardware list.
            cabbage solution to container.       <Procedure>                                        The available Hardware is: beaker,
                                                                                                                                                <Procedure>
            Stir for 20 seconds.                     <Add vessel="container"                         stir bar
                                                                                                                                                    <Add vessel="beaker"
                                                       reagent="acetic acid"
                                                       amount="15 g" />                         3       Feedback, iteration 3                         reagent="acetic acid"
                                                                                                                                                      amount="15 g"/>
                                                     <Add vessel="container"
                                                                                                    The Hardware section should only                <Add vessel="beaker"
                                                       reagent="red cabbage
                                                                                                     contain Component tags                           reagent="red cabbage
                                                       solution" amount="30 g"/>
                                                                                                                                                     solution" amount="30 g"/>
                                                     <Stir vessel="container"
                                                                                                                                                    <Stir vessel="beaker"
                                                       time="20"/>
                                                  </Procedure>                                                                                        time="20"/>
                                                                                                           Veriﬁer                               </Procedure>
                                               </Synthesis>
                                             </XDL>
                                                                                                                 Pass                         </Synthesis>
                                                                                                                                            </XDL>



Fig. 5: Feedback loop between the Generator and Verifier. The input text is converted to structured-like language via the generator
and is then passed through the verifier. The verifier returns a list of errors (marked with a yellow 1). The feedback is passed back to
the generator along with the erroneous task plan, generating a new task plan. Now that previous errors were fixed and the tags could be
processed, new errors were found (including a constraint error that the plan uses a vessel not in the environment). These errors are denoted
with a blue 2. This feedback loop is repeated until no more errors are caught, which in this case required 3 iterations.

   Figure 6 shows the flow of the experiment. Our generated                                  Feedback Design – We experimented with prompts in our
a XDL plan that correctly captured the experiment; the plan                                  iterative prompting scheme containing various levels of detail
was then passed through TAMP to generate a low-level action                                  about the errors. The baseline prompt contains a description as
plan and was then executed by the robot.                                                     well as natural language instruction. We wanted to investigate
Kitchen Chemistry – We then tested whether our robot                                         how much detail is needed in the error message for the
could execute a plan generated by our model for a different                                  generator to be able to fix the errors in the next iteration.
application of household chemistry: food preparation. We                                     For example, is it sufficient to write “There was an error
generated a plan using CLAIR IFY for the following lemonade                                  in the generated XDL", or do we need to include a list of
beverage, which can be viewed on our website:                                                errors from the verifier (such as “Quantity is not a permissible
Add 15 g of lemon juice and sugar mixture to a cup containing                                attribute for the Add tag"), or do we also need to include the
30 g of sparkling water. Stir vigorously for 20 sec.                                         erroneous XDL from the previous iteration?
C. Ablation Studies                                                                             We find that including the erroneous XDL from the
  We assess the impact of various components in our                                          previous iteration and saying why it was wrong resulted
prompt designs and feedback messaging from the verifier. We                                  in the high number of successfully generated XDL plans.
performed these tests on a small validation set of 10 chemistry                              Including a list of errors was better than only writing “This
experiments from Chem-RnD (not used in the test set) and                                     XDL was not correct. Please fix the rrors", which was not
report the number of XDL plans successfully generated (i.e.,                                 informative enough to fix any errors. Including the erroneous
was not in the iteration loop for x = 10 steps).                                             XDL from the previous iteration is also important; we found
Prompt Design – To evaluate the prior knowledge of the GPT-                                  that including only a list of the errors without the context of
3 on XDL, we first tried prompting the generator without a                                   the XDL plan resulted in low success rates.
XDL description, i.e., with the input:                                                                           V. C ONCLUSION AND F UTURE W ORK
initial_prompt = """
Convert to XDL:                                                                                 In this paper, we introduce CLAIR IFY to generate struc-
# <Natural language instruction>"""
                                                                                             tured language task plans in a DSL by providing an LLM
   The LLM was unable to generate XDL for any of the                                         with a description of the language in a zero-shot manner. We
inputs from the small validation set that contains 10 chemistry                              also ensure that the task plan is syntactically correct in the
experiments. For most experiments, when asked to generated                                   DSL by using a verifier and iterative prompting. Finally, we
XDL, the model output a rephrased version of the natural                                     show that our plans can incorporate environmental constraints.
language input. In the best case, it output some notion of                                   We evaluated the performance of CLAIR IFY on two datasets
structure in the form of S-expressions or XML tags, but                                      and find that our method was able to generate better plans
the outputs were very far away from correct XDL and                                          than existing baselines. Finally, we translate a select number
were not related to chemistry. We tried the same experiment                                  of these plans to real-world robot demonstrations.
with code-davinci-002; the outputs generally had more                                           In the future, we will incorporate feedback from the robot
structure but were still nonsensical. This result suggests the                               planner and environment into our plan generation process.
LLM does not have the knowledge of the target language and                                   We will also improve the verifier to encode knowledge of
including the language description in the prompt is essential                                the target domain nuances. With these technical refinements,
to generate an unfamiliar language.                                                          we expect our system can become integrated even better in
                                                                                      Structured Language
                                                                  <XDL>
                  Natural Language                                ...
           Add 40g of red cabbage solution
                                                                  <Procedure>
                                                                    <Add vessel="beaker" reagent="red cabbage solution"            Fig. 6: Robot execution: The
 (a)       into a beaker. Add 10 g of baking                             amount="40 g"/>
                                                                                                                                   robot executes the motion plan
           soda into the beaker, then stir the
                                                 CLAIRify           <Add vessel="beaker" reagent="baking soda" amount="10 g"/>
                                                                    <Stir vessel="beaker" time="10 s"/>
           solution for 10 seconds.                               </Procedure>
                                                                  </XDL>
                                                                                                                                   generated from the XDL for
                                                                                                                                   given natural language input. (a)
                                                                                                                                   CLAIR IFY converts the natural
 (b)
       1
           <Add vessel="beaker"
                                                    2                                        3                                     language input from the user into
                                                     <Add vessel="beaker"
           reagent="red cabbage
            solution" amount=
                                                        reagent="baking
                                                                                              <Stir vessel="beaker"
                                                                                                  time="10 s"/>
                                                                                                                                   XDL. (b) The robot interprets
                                                     soda" amount="10 g"/>
                 "40 g"/>                                                                                                          XDL and performs the experi-
                                                                                                                                   ment. Stirring is done by a ro-
                                                                                                                                   tating stir bar inside the beaker.



robotic task planning for different domains.                                                          Chem. Res., 2022.
                               VI. ACKNOWLEDGEMENTS                                              [18] L. P. Kaelbling and T. Lozano-Pérez, “Hierarchical task and
                                                                                                      motion planning in the now,” in IEEE Inter. Conf. Robot. Autom.
  We would like to thank members of the Matter Lab for                                                IEEE, 2011, pp. 1470–1477.
annotating task plans. We would also like to thank the                                           [19] J. A. Baier, et al., “A heuristic search approach to planning
Acceleration Consortium for their generous support, as well                                           with temporally extended preferences,” Artif. Intell., 2009.
as the Carlsberg Foundation.                                                                     [20] P. Sharma, et al., “Skill induction and planning with latent
                                                                                                      language,” arXiv:2110.01517, 2021.
                                             R EFERENCES
                                                                                                 [21] S. Mirchandani, et al., “ELLA: Exploration through learned
 [1] T. Brown, et al., “Language models are few-shot learners,”                                       language abstraction,” Adv. Neural. Inf. Process. Syst., 2021.
     Adv. Neural. Inf. Process. Syst., vol. 33, pp. 1877–1901, 2020.
                                                                                                 [22] D. Shah, et al., “Value function spaces: Skill-centric state
 [2] I. Singh, et al., “Progprompt: Generating situated robot task                                    abstractions for long-horizon reasoning,” arXiv:2111.03189,
     plans using large language models,” in IEEE Int. Conf. Robot.                                    2021.
     Autom., 2023.
                                                                                                 [23] D. Xu, et al., “Neural task programming: Learning to generalize
 [3] J. Devlin, et al., “BERT: Pre-training of deep bidirectional                                     across hierarchical tasks,” in IEEE Int. Conf. Robot. Autom.,
     transformers for language understanding,” in North American                                      2018.
     Chapter of the Association for Computational Linguistics,
                                                                                                 [24] D.-A. Huang, et al., “Neural Task Graphs: Generalizing to
     2019.
                                                                                                      unseen tasks from a single video demonstration,” in IEEE
 [4] A. Chowdhery, et al., “PaLM: Scaling language modeling with                                      Comput. Vis. Pattern Recognit., 2019.
     pathways,” arXiv:2204.02311, 2022.
                                                                                                 [25] D. Xu, et al., “Regression planning networks,” Adv. Neural.
 [5] M. Chen, et al., “Evaluating large language models trained on                                    Inf. Process. Syst., vol. 32, 2019.
     code,” arXiv:2107.03374, 2021.
                                                                                                 [26] B. Eysenbach, et al., “Search on the replay buffer: Bridging
 [6] Y. Wang, et al., “CodeT5: Identifier-aware unified pre-trained                                   planning and reinforcement learning,” Adv. Neural. Inf. Process.
     encoder-decoder models for code understanding and genera-                                        Syst., vol. 32, 2019.
     tion,” arXiv:2109.00859, 2021.
                                                                                                 [27] W. Huang, et al., “Inner monologue: Embodied reasoning
 [7] Y. Li, et al., “Competition-level code generation with alpha-                                    through planning with language models,” arXiv:2207.05608,
     code,” Science, vol. 378, no. 6624, pp. 1092–1097, 2022.                                         2022.
 [8] J. Liang, et al., “Code as policies: Language model programs                                [28] H. Le, et al., “CodeRL: Mastering code generation through
     for embodied control,” arXiv:2209.07753, 2022.                                                   pretrained models and deep reinforcement learning,” in Adv.
 [9] C. R. Garrett, et al., “PDDLStream: Integrating symbolic plan-                                   Neural. Inf. Process. Syst., 2022.
     ners and blackbox samplers via optimistic adaptive planning,”                               [29] T. Schick, et al., “Toolformer: Language models can teach
     in Proc. ICAPS Conf. AAAI Press, 2020, pp. 440–448.                                              themselves to use tools,” arXiv:2302.04761, 2023.
[10] M. Ahn, et al., “Do As I Can, Not As I Say: Grounding                                       [30] A. Ni, et al., “Lever: Learning to verify language-to-code
     language in robotic affordances,” arXiv:2204.01691, 2022.                                        generation with execution,” arXiv:2302.08468, 2023.
[11] Y. Gu, et al., “Domain-specific language model pretraining for                              [31] B. Peng, et al., “Check your facts and try again: Improving
     biomedical natural language processing,” ACM Trans. Comput.                                      large language models with external knowledge and automated
     Healthcare, vol. 3, no. 1, pp. 1–23, 2021.                                                       feedback,” arXiv:2302.12813, 2023.
[12] R. Liu, et al., “Mind’s eye: Grounded language model                                        [32] A. C. Vaucher, et al., “Automated extraction of chemical syn-
     reasoning through simulation,” arXiv:2210.05359, 2022.                                           thesis actions from experimental procedures,” Nat. Commun.,
[13] S. Wang, et al., “Want to reduce labeling cost? GPT-3 can                                        2020.
     help,” in Proc. EMNLP Conf., 2021, pp. 4195–4205.                                           [33] N. Yoshikawa, et al., “An adaptive robotics framework for
[14] N. Bannour, et al., “Evaluating the carbon footprint of NLP                                      chemistry lab automation,” arXiv:2212.09672, 2022.
     methods: a survey and analysis of existing tools,” in SustaiNLP,                            [34] H. Mehr, et al., “Benchmarking results and the XDL XML
     Nov. 2021, pp. 11–21.                                                                            schema.” 2020. [Online]. Available: https://zenodo.org/record/
[15] S. Mishra, et al., “Cross-task generalization via natural                                        3955107
     language crowdsourcing instructions,” arXiv:2104.08773, 2021.                               [35] T. Perry, “LightTag: Text annotation platform,” in Proc.
[16] S. H. M. Mehr, et al., “A universal system for digitization                                      EMNLP Conf., Nov. 2021, pp. 20–27.
     and automatic execution of the chemical synthesis literature,”                              [36] J. J. Fortman and K. M. Stubbs, “Demonstrations with red
     Science, vol. 370, no. 6512, pp. 101–108, 2020.                                                  cabbage indicator,” J. Chem. Educ., vol. 69, no. 1, p. 66, 1992.
     lenges and perspectives on establishing a self-driving lab,” Acc.
[17] M. Seifrid, et al., “Autonomous chemical experiments: Chal-
