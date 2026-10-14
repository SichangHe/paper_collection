                                         Towards Reliable Generation of Executable Workflows by
                                         Foundation Models
                                         SOGOL MASOUMZADEH, McGill University, Montréal, Canada
                                         KEHELIYA GALLABA, Centre for Software Excellence, Huawei Canada, Canada
                                         DAYI LIN, Centre for Software Excellence, Huawei Canada, Canada
                                         AHMED E. HASSAN, Queen’s University, Canada
                                         Recent advancements in Foundation Models (FMs) have demonstrated significant progress in processing
arXiv:2509.25117v2 [cs.SE] 17 Mar 2026




                                         complex natural language to perform intricate tasks. Successfully executing these tasks often requires or-
                                         chestrating calls to FMs alongside other software components. However, manually decomposing a task into
                                         a coherent sequence of smaller, logically aggregated steps, commonly referred to as workflows, demands
                                         considerable effort and specialized domain knowledge. While FMs can assist in generating such workflows
                                         specified in domain-specific languages (DSLs), achieving accuracy and reliability in this process remains a
                                         challenge.
                                            We introduce a framework that leverages static analysis feedback to enable FMs to detect and repair defects
                                         in the DSL-based workflows they generate. We begin by presenting an initial taxonomy of incidences of defects
                                         in FM-generated DSL workflows, categorizing them into 20 distinct types. Furthermore, we observe a high
                                         prevalence of defects across FM-generated DSL workflows, with 89.23% of the studied instances containing
                                         at least one defect. This high prevalence underscores the magnitude of the problem and the necessity for
                                         mitigation strategies. Following this, we demonstrate that nine types of these defects can be effectively
                                         identified through static analysis of the workflows. For this purpose, we develop Timon, the first-of-its-kind
                                         static analyzer specifically designed for FM-generated DSL workflows. Finally, we show that by incorporating
                                         feedback from Timon, we can guide Pumbaa, an FM-based tool, to repair the detected defect incidences. By
                                         systematically detecting and repairing defects, our work provides a crucial step towards the reliable and
                                         automated generation of executable workflows from natural language requirements.
                                         CCS Concepts: • Computing methodologies → Machine learning; • Software and its engineering →
                                         Software development techniques.
                                         Additional Key Words and Phrases: Program Synthesis, Program Translation, Domain-Specific Language
                                         Programs, Automated Program Repair, Automatic Defect Detection, Foundation Models

                                         1   Introduction
                                         Foundation Models (FMs), which are large-scale deep learning models trained on vast corpora, have
                                         recently demonstrated remarkable advancements in parsing, interpreting, and generating natural
                                         language to address complex tasks. From automated code generation [40, 41, 70] to question an-
                                         swering [43, 82], and large-scale document summarization, FMs exhibit an impressive capacity
                                         to handle diverse and intricate requirements. However, fully leveraging this capacity in software
                                         development scenarios often demands the orchestration of multiple calls to FMs alongside various
                                         software components and services. This orchestration is commonly specified as a workflow. In this
                                         context, a workflow is a sequence of smaller, atomic steps that are logically aggregated to create an
                                         automatable end-to-end process [60], wherein each step represents an invocation of an FM or a
                                         supporting software element (e.g., databases, external APIs, or transformation scripts).
                                            To reduce manual development effort while enabling autonomy and flexibility, developers have
                                         considered using conventional enterprise business process languages such as BPEL and BPMN for
                                         representing FM-powered workflows [27, 65]. Although effective up to the Software 2.0 era [24],
                                         Authors’ Contact Information: Sogol Masoumzadeh, sogol.masoumzadeh@mail.mcgill.ca, McGill University, Montréal, QC,
                                         Canada; Keheliya Gallaba, keheliya.gallaba@huawei.com, Centre for Software Excellence, Huawei Canada, ON, Canada;
                                         Dayi Lin, dayi.lin@huawei.com, Centre for Software Excellence, Huawei Canada, ON, Canada; Ahmed E. Hassan, ahmed@
                                         queensu.ca, Queen’s University, ON, Canada.


                                                                          ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
2                                                                                        Masoumzadeh et al.


these languages are not designed to target the special characteristics of rapidly emerging and
unavoidable FMs and FM-based software. This design mismatch, in turn, makes the representation
of FM-powered workflows using such notations infeasible. Specifying FM-powered workflows
using general-purpose programming languages is also impractical, as these workflows have their
unique semantics requiring verbose programs to handle all the edge cases or novel abstractions to
represent them. Community-led efforts, such as the LangChain Expression Language (LCEL) [33]
and GenAIScript [48], emphasizes the need for Domain-Specific Languages (DSLs) better suited for
novel semantics of FM-powered workflows.
   Representing FM-powered workflows through such FM-friendly DSLs serves two purposes.
First, this enables humans to communicate their intention when orchestrating a workflow to FMs
much more clearly and at a higher level of abstraction. Second, this increases the success rate
of FMs in synthesizing workflows and automatically executing them. Using a DSL simplifies the
generation of domain-specific program instances by omitting FMs’ domain-irrelevant, pre-learned
knowledge. Furthermore, using a DSL limits the action space of FMs by narrowing the multitude
of ways of conducting the same tasks to the most context-relevant ones [21]. As such, FMs are
ensured to synthesize programs that adhere to domain-specific constraints in domains such as data
management and computer-aided design [29].
   Following these observations, several efforts have emerged to create FM-friendly DSLs and
interfaces which enhance the FMs’ task execution capabilities by constraining their interaction
with execution environments. One example is the Office Domain-Specific Language [21], a language
designed to facilitate action execution within Office applications while minimizing ambiguous
and overly expansive language features, thereby simplifying API invocation semantics for FMs,
particularly Large Language Models (LLMs). A parallel line of work is SWE-agent [79], which also
provides a constrained interface, dubbed the agent-computer interface, that is tailored to the needs
and constraints of LLMs for software engineering tasks. Similarly, instead of having to extensively
train FMs to call all available tool types, the Model Context Protocol [47] enables LLM-based clients
to discover and execute tools at runtime via a unified interface. This enables expansion of the LLM’s
capabilities while reducing the likelihood of syntax errors in LLM-generated tool calls.
   Although these efforts enhance the reliability of FMs in automating processes within narrow
scopes of a particular application or tool invocation, their proposed DSL or interfaces are not
applicable for using FMs to generate general-purpose workflows beyond those restricted domains.
To advance beyond the current constrained application of FMs in automating processes, our
overarching goal is to build on the capabilities of FMs, particularly LLMs, to reliably generate FM-
powered workflows that meet user-provided requirements, regardless of domain. To achieve this
goal, two main challenges must be overcome: (1) identifying the user intent and their requirements
expressed in natural language and (2) then reliably synthesizing the workflows as FM-friendly
DSL program instances that can be executed by language models to fulfill the identified user
requirements.
   The first of these challenges, inferring user intent and refining the requirements, has already
been investigated by Gallaba et al. [20] in prior work. They explored the capabilities of FM-powered
agents in refining vague user requirements across a diverse set of user scenarios. They introduced
an interactive, multi-agent requirement refiner framework, named AlignMind, that is capable of
refining requirements and generating detailed, step-by-step natural language instructions from
an input user scenario. However, the subsequent challenge, reliably generating executable DSL
workflows from identified natural language instructions, with the help of FMs, largely remains
unsolved because FMs’ output often violates the specified DSL grammar.
   Even with recent advancements, LLMs are known to exhibit a tendency for hallucination, often
producing outputs that are inaccurate, incomplete, or inconsistent with prompts [28]. Such issues

ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
Towards Reliable Generation of Executable Workflows by Foundation Models                                                3


are especially troubling in code generation tasks (such as our case of synthesizing DSL workflow
programs), where syntactic and semantic correctness are paramount. Therefore, providing DSLs
which are specifically designed around LLM limitations (e.g., unambiguous function signatures,
streamlined syntax, and comprehensive error reporting), is necessary for language models to
operate more effectively and synthesize code that is robust or somewhat “FM-proof”. However,
even with such specialized DSLs carefully curated to meet language model constraints, LLMs
remain fallible and are likely to produce errors when generating DSL code [10].
   Indeed, there are success stories of using language models to synthesize DSL programs [83],
in which LLMs are used to directly generate GitHub Actions workflows. However, despite being
DSL program instances, GitHub Action Workflows are abundantly accessible to LLMs during their
training through open-source GitHub repositories. Hence, LLMs do not face the “low-resource
language” problem wherein the DSL or API is novel or not widely represented in standard LLM
training data. Therefore, in that instance, LLMs are successful in generating error-free GitHub
Action Workflows without the need for implementing post-generation strategies to mitigate possible
errors. On the other hand, synthesizing general-purpose workflows as program instances of low-
resource, custom DSLs has not been effective in practice. In spite of reducing the attack surface of
possible program synthesis mistakes through simplifying language constructs, it does not eradicate
all defects in FM-generated DSL workflows. Errors remain frequent, or even increase, in synthesized
DSL workflows because the LLM is effectively “guessing” the correct syntax or semantics without a
substantial training foundation. The desire for robust, secure, and maintainable systems underscores
the need for complementary measures, e.g., detection via static analysis and automated repairs, to
achieve truly reliable generation of FM-powered workflows.
   In this paper, we propose a novel framework that capitalizes on static analysis to detect and
repair defects in FM-generated DSL workflows to ensure reliable execution in enterprise settings.
Although prior research [56, 69] examined bugs introduced by FMs during code generation and code
translation, the defects generated by FMs during Natural-Language-to-DSL (NL-2-DSL) translation
remain unstudied. Therefore, we begin by creating an initial taxonomy of defect types in FM-
generated DSL workflows, revealing 20 distinct categories of mistakes that typically appear. We
then demonstrate how nine of these categories can be pragmatically detected via static analysis
without running the workflows. To facilitate this endeavor, we build a bespoke static analyzer
tailored to FM-generated DSL workflows, an area that has yet to be thoroughly explored. Lastly, our
approach leverages FMs once more to repair these defect types by incorporating direct feedback
from the implemented static analyses.
   Specifically, this paper investigates the following research questions: (RQ1) What are the char-
acteristics of defects in FM-generated DSL workflows? (RQ2) How accurately can these defects
be detected using static analysis? (RQ3) How effective are FMs at repairing these defects when
provided with static analysis feedback? Our contributions can be summarized as follows.
     • We introduce an initial taxonomy of 20 distinct defect types commonly arising in FM-
       generated DSL workflows.
     • We develop a specialized static analysis tool, Timon, capable of detecting nine of those defect
       types.
     • By implementing our repair tool for FM-generated DSL workflows, Pumbaa, we demonstrate
       that these defect types can be automatically repaired by invoking FMs with actionable
       feedback derived from the static analysis reports.
     • Analyzed FM-generated DSL workflows, ground-truth defect annotations, analysis results,
       and the prompts used during experiments are made available online for replicability. 1
1 https://doi.org/10.6084/m9.figshare.28600052



                                    ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
4                                                                                        Masoumzadeh et al.


   The remainder of this paper is organized as follows. Section 2 describes the background on
executable Workflow generation with FMs. Section 3 describes the design and results of our empirical
study on defects in FM-generated workflows. Section 4 describes the process for workflow defect
detection and repair. Section 5 discusses insights, limitations, and future directions. Section 6
describes threats to the validity of our study. Section 7 provides an overview of FMs and their role
in automated workflow generation. Finally, Section 8 concludes this work.


2     Executable Workflow Generation with FMs
Going from natural language requirements to executable workflows in an enterprise setting is
a multi-step process. In this section of the paper, we define our general-purpose workflow DSL
grammar, describe a computational environment for executing these workflows, and outline our
pipeline for generating the workflows in the defined DSL using FMs, such that these workflows
can be parsed and executed in the introduced execution environment. We conclude the section by
explaining a challenge in FM-powered workflow generation, which motivates our investigation
into detecting and fixing the defects.


2.1    Workflow DSL
Based on our prior experience in modeling processes of small and medium-sized enterprises, we
specify a DSL grammar such that it can represent a varying range of these processes as workflows,
from ones involving a single task to workflows consisting of multiple steps with complex control
flow. We refer to this language as WorkflowDSL in the remainder of this paper. While the primary
objective of the WorkflowDSL is to represent FM-based workflows, it is an extensible and flexible
grammar that adapts to any domain, whether generic or with a specific set of requirements and
characteristics, such as the medical domain.
   A synthesized workflow adhering to WorkflowDSL grammar consists of inputs field, outputs
field, and a list of task nodes. The inputs field captures global variables and user-set parameters,
including their type information. Similarly, the outputs field pertains to the expected outputs of the
workflow after execution, along with their types. The task nodes correspond to the smaller, atomic
steps of the workflow. We define WorkflowDSL as a procedural language with a diverse set of
control-flow constructs consisting of regular tasks, conditional branches, switch cases, and loops. A
regular task node is the equivalent of a statement in a general-purpose programming language.
Similarly, conditional branch, switch case, and loop nodes correspond to if-else, switch, and for-loop
syntax in a general-purpose programming language. We specify WorkflowDSL grammar as a
TypeScript type definition in a structured, strict JSON format.


2.2    Workflow Execution Environment
The general-purpose workflow execution environment that we consider in this work is capable of
executing WorkflowDSL programs by orchestrating skills, which are the most granular unit of
execution in the workflow. The execution environment can invoke four types of skills. Native skills
pertain to using local tools, sending requests to both local and external API endpoints, and executing
code snippets. Semantic skills pertain to prompting external or internal instances of FMs, such as
sending requests to OpenAI’s chat completion endpoint. Model skills are used for invoking any
machine learning model other than FMs, such as a model that was trained for sentiment analysis.
Finally, workflow skills are used to call other WorkflowDSL instances, which can orchestrate the
skills of all other types.

ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
Towards Reliable Generation of Executable Workflows by Foundation Models                                                       5


                                                                              B DSL Workflow Synthesis
                                                                            B.1
          User                             Refined      Step-by-step
         Scenario                        Requirements Natural Language                              DSL
                            A                                                 Converter Agent
                                                        Instructions                              Grammar
                       Requirements
                                                                            B.2
                        Refinement
                                                                                  Skill Chooser                 FM-generated
                                                                                                   Available
                                                                                                               DSL Workflows
                                                                                                    Skills




                    Fig. 1. Overview of workflow generation with FMs using NL-2-DSL pipeline


2.3   Natural-Language-to-DSL pipeline
Given a DSL grammar and the discussed execution environment with diverse capabilities, for a
specific user scenario, manually writing a detailed workflow in the defined DSL grammar that
can invoke the appropriate skill at each smaller, atomic step is a laborious endeavour. Therefore,
we implement a Natural-Language-to-DSL (NL-2-DSL) pipeline for automatically translating the
natural language user scenario to an executable workflow, as a DSL program instance, with the
assistance of FMs. Figure 1 illustrates the key steps involved in the process, which consists of two
main parts: Requirements Refinement A and DSL Workflow Synthesis B . We discuss these steps in
detail as follows.
Requirements Refinement A . In practice, it’s rare for people to outline the requirements they
want to automate as a workflow in sufficient detail on their initial attempt [50, 72]. Hence, the
NL-2-DSL pipeline should first refine the vague requirements provided by users. For this purpose,
a FM-powered, multi-agent, conversational system can be used. In this particular embodiment,
we use AlignMind [20] to interact with users to refine their initial set of requirements and to
generate a list of step-by-step natural language instructions corresponding to their intent, which
they describe as a user scenario.
DSL Workflow synthesis B . To synthesize DSL workflows, two main components interact
with each other: the Converter Agent B.1 and the Skill Chooser B.2 . The Converter Agent B.1
receives the user scenario provided by the user, the refined description of the requirements, and the
corresponding natural language instruction steps, generated from step A , as inputs. Including the
natural language instructions as an input to B.1 , helps the workflow synthesis in two ways. First,
it guides the converter agent in synthesizing the workflow, specifically including the actionable
steps necessary to achieve the input user scenario. Second, it helps validate the correctness and
completeness of the generated DSL workflow with respect to the refined requirements. Given
these inputs, the FM in this component is prompted to generate the corresponding workflow as a
valid JSON object that adheres to the WorkflowDSL grammar. Specifically, we prompt the FM
to generate the task nodes of the workflow in the same order as the steps outlined in the natural-
language instructions, while preserving their control-flow constructs. The steps in the natural
language instructions can be categorized as declarations, conditions, case distinctions, and iterations.
We map each step into WorkflowDSL’s corresponding task nodes using the same control-flow
construct. The declarations in the natural language instructions are mapped to regular task nodes
in WorkflowDSL. Conditional statements in natural language are mapped to conditional branch
nodes, while case distinctions map to switch case nodes. Finally, iterative instructions correspond
to loop nodes in WorkflowDSL.
   To generate the task nodes in the workflow as proper, executable counterparts to the steps of
natural language instructions, each task node should invoke a skill from the execution environment’s

                                      ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
6                                                                                                                                Masoumzadeh et al.


                                                                              t2                                 t3
                                                         True                                            Send Approval
       Workflow                                                        Approve User
        Inputs:                                                                                            Message
      name <str>                                                Inputs:             Outputs:           Inputs:
                            t1                                                                                        Outputs:
                                                              username:            approvalID:      messageID:
                                                                                                                       None
                                              t1.age   {{workflow.inputs.name}}       <str>      {{t2.approvalID}}
                    Gather User Info
                                               >= 18
               Inputs:                                                        t4                                 t5
                                  Outputs:               False
             username:                                                                                  Send Rejection
                                 age: <int>                             Reject User
      {{workflow.inputs.name}}                                                                            Message
                                                                Inputs:                                Inputs:
                                                                                    Outputs:                          Outputs:
                                                              username:                             messageID:
                                                                                     None                              None
                                                       {{workflow.inputs.name}}                  {{t2.approvalID}}




Fig. 2. An example of a defective workflow generated by an FM. Task t2 and Task t5, which are on different
                     branches, have an unsatisfiable data dependency between them.


skills database, matching the action described in its corresponding natural language instruction step,
along with correct input/output parameters. Skill Chooser B.2 enables this one-to-one mapping
during the workflow generation. In the Skill Chooser component, we augment the prompt to the
Converter Agent with the list of skills available in the skills database as context. For each skill,
we provide the skill name, accepted input fields with their types, expected output format, and
a natural-language description of the skill. There are three modes available to construct the list
of skills. In the first mode, the FM is provided with all available skills, along with input/output
as additional context in the prompt. The second mode queries the database for exact matches
of natural-language instruction steps among available skills to include in the prompt. In the last
mode, skills with the highest semantic similarity to steps in the natural language instructions
are appended as additional context. To mitigate FMs’ known limitation of getting distracted by
irrelevant context [61], after preliminary evaluations, we chose to use the third mode.

2.4      Motivating Example
Similar to observations from prior work [10], despite our best efforts in generating valid workflow
programs adhering to WorkflowDSL’s grammar, on several occasions, we observe that generated
workflows suffer from syntactic and semantic defect incidences. Figure 2 demonstrates a simplified
version of one such example we have observed in practice.
   In this example workflow, the requirement is to check if a user is old enough to be approved. If the
user is 18 years or older, their profile is approved, and an approval message is sent. Otherwise, the
request is rejected, and a rejection message is sent to the user. Although the generated workflow is
correct at a high level, the FM introduces a subtle bug during workflow generation as follows. Task t5
(Send Rejection Message step) accepts a messageID as input. The output of Task t2, ApprovalID, is
assigned to this messageID field, creating an unsatisfiable data dependency because these two nodes
are on mutually exclusive branches. We hypothesize that this error occurs in the FM-generated
workflow because the tokens in the DSL JSON representation are generated sequentially by the FM.
Due to the limitations of autoregressive generation, the FM cannot reason about data dependency
across nodes and assumes that the output of the t2 node is visible to the t5 node. Although this is
one example, there are many such defect patterns that require deeper reasoning on control flow and
data flow to identify. This problem is further exacerbated by the fact that, unlike general-purpose
programming languages, which FMs are well-trained on, DSLs are relatively unfamiliar to them.

3     Empirical Study of Defects in FM-generated DSL workflows
Ideally, for a given user scenario, after all the requirements are elicited and step-by-step instructions
are available in natural language, an FM-based agent should be able to synthesize a syntactically

ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
Towards Reliable Generation of Executable Workflows by Foundation Models                                                        7


                A Generation of Representative DSL Workflows
   Personas,             Simulated            FM               Simulated Scenario-
   Expertise,          User Scenarios    Role-playing           based Workflows
   Domains      FM          (200)         as Human                     (200)

                                                        NL-2-DSL                           B            Defect   Open-coded
                                                        Pipeline
                                                                                                      Taxonomy   Dataset (65)
                                                                                      Open-coding
                         OpenAGI                                     OpenAGI           Analysis
                       User Scenarios                              DSL Workflows
                            (185)                                      (185)




          Fig. 3. Overview depicting the empirical study of defects in FM-generated DSL workflows



and semantically valid workflow in the specified DSL. However, as shown in Section 2.4, defects
in FM-generated DSL workflows can affect robustness and reliability. Before we can effectively
address this issue, we must first identify the types of defects that are occurring in practice and
assess the prevalence of each defect type. To the best of our knowledge, there exists no prior study
exploring the ability of FMs in DSL program synthesis. The only similar study is the research
conducted by Pan et al. [56], which presents a taxonomy of defects when FMs are used for code
translation between pairs of general-purpose programming languages, including C, C++, Go, Java,
and Python. That study mainly differs from the problem we are tackling, which involves translating
natural language into workflows as program instances of a DSL (i.e., NL-2-DSL). Therefore, we
conduct an empirical study on plausible defects in FM-generated DSL workflows as this indicates
FM capabilities in synthesizing error-free DSL programs. We present the results of the study as
initial taxonomy of observed defects in FM-generated DSL workflows.

3.1    Empirical Study Design
Figure 3 illustrates the key steps of our empirical study, which consists of Generation of Representative
DSL Workflows A and Open-coding Analysis B . We discuss each step in detail as follows.
Generation of Representative DSL Workflows A . We use our NL-2-DSL pipeline discussed
in Section 2.3 to generate the dataset of DSL workflows for our empirical study. To effectively
identify all defect types that are likely to arise in real-world situations, it is essential that the
inputs of the NL-2-DSL pipeline, namely, the initial set of user scenarios, corresponding refined
requirements, and natural language instruction steps, are comprehensive and diverse. However,
due to data security and privacy regulations, the real-world artifacts obtained from our customers
cannot be directly used for experimentation. As an alternative, we create a set of scenarios and
simulate user conversations based on these scenarios to refine their corresponding requirements
and generate instruction steps with the assistance of FMs. We create the set of scenarios in two
steps. In the first step, we follow the approach described by Gallaba et al. [20] to generate a list of
user scenarios that we refer to as simulated scenarios as they closely approximate and follow the
characteristics of the authentic customer scenarios.
   To generate the simulated scenarios, we prompt a FM to generate 200 user scenarios correspond-
ing to a diverse set of user personas (specifically cordial, neutral, rude, and indecisive), their level of
expertise (namely novice, intermediate, and expert), and scenario domains (including data analytics,
automation, project management, customer engagement, customer support, process optimization, and
automated marketing). As an example, one user scenario generated from this process could be: “As

                                        ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
8                                                                                        Masoumzadeh et al.


an experienced data scientist, I would like to receive news about AI in my inbox
every morning”.
   In the second step of creating the set of scenarios, to overcome the limitation of relying solely on
synthetically generated user scenarios, we include a series of real-world, general-purpose scenarios.
We choose these real-world user scenarios from the OpenAGI dataset [22]. The OpenAGI dataset
contains 185 natural-language scenario descriptions that are queried by users to generate real-
world workflow processes. The dataset consists of 20 varying domains ranging from “academics”,
to “mathematics”, to “technical support for computer issues”, and “design”, demonstrating the
representativeness of the dataset across different areas. For instance, a sample OpenAGI scenario,
selected from the academics domain, is as follows: “Find papers on the effectiveness of
online learning platforms for language acquisition”.
   In the next step, we employ the FM to role-play as a human user and converse with AlignMind
to elicit and refine the requirements for our set of simulated and OpenAGI scenarios. We use
the approach from Gallaba et al. [20] following best practices [1, 67] to simulate the interactions
between the FM role-playing as the user and AlignMind, which is context-aware and semantically
conditioned, closely mirroring authentic human-FM dialogues. As such, we can ensure the pairs of
scenarios-requirements are clear, cohesive, and correct, which in turn, align their corresponding
FM-generated DSL workflows with their real-world counterpart processes. Finally, we use our
set of representative artifacts as the input to the NL-2-DSL pipeline and obtain a dataset of 385
diverse FM-generated DSL workflows (200 workflows corresponding to the simulated scenarios,
from here on referred to as simulated scenario-based workflows, and 185 workflows corresponding
to the OpenAGI user scenarios, from here on referred to as OpenAGI FM-generated DSL workflows)
to be further analyzed for their structural characteristics and possible defects. OpenAI’s GPT-4o-
mini-2024-07-18 model, with temperature set to 0.7 and 128, 000 tokens as the context window, is
used in this particular experiment.

Open-coding Analysis B . For creating the taxonomy of defect categories in FM-generated DSL
workflows, we conduct an open-coding analysis on the dataset of DSL workflows we constructed
in A .
   We start the analysis by open-coding the set of simulated scenario-based workflows in three
steps, carried out by one researcher and one industry engineer (i.e., two inspectors). In the first
step, ten workflows are randomly sampled from the initial population of 200 scenario-based
simulated workflows, with stratification used to ensure that each persona, expertise level, and
domain specification is selected at least once. This selected initial seed does not aim to provide
adequate representation across different characteristics of the population. Rather, the goal is to
calibrate inspectors’ perspectives on the various defect types that may occur in FM-generated DSL
workflows. For this purpose, at the second step, each inspector independently analyzes the selected
ten workflows and records any potential errors, their types, and their exact task node location
within the workflows. To do this, they compare each workflow against its corresponding user
scenario, the refined set of requirements, and the natural language instructions to identify, based on
their expertise, any discrepancies and errors. Inter-rater agreement reliability corresponding to the
annotation of these ten DSL workflows is calculated as a measure of Cohen’s kappa coefficient [17].
Cohen’s kappa quantifies the agreement between two inspectors by comparing the number of
annotations both inspectors agreed on against chance-expected agreements, with values ranging
from -1 (i.e., absolute disagreement) to 1 (i.e., perfect agreement), and 0 indicating agreement
expected by random chance. Calculated Cohen’s kappa is 0.55, indicating moderate agreement
between the two inspectors [46]. To resolve the discrepancies and alleviate potential examiner bias,
the inspectors meet to discuss disagreements. Identified defects by both inspectors are compared,

ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
Towards Reliable Generation of Executable Workflows by Foundation Models                                             9


and if they disagree on the presence or type of a defect, they discuss the discrepancy until an
agreement is reached. By conducting this meeting, inspector perceptions of possible defect types
align, ensuring a consolidated initial taxonomy as the baseline for continuing the next steps of the
analysis.
    At the third step, inspectors continue the resampling of the simulated scenario-based workflows,
adding to the set of ten initially labeled workflows, and analyze each newly sampled workflow for
its defect incidences independently. After labeling each workflow, the inspectors compare their
analyses to record the updated prevalence for defect categories and to extend the taxonomy when a
new defect category emerges. Sampling of simulated scenario-based workflows, and labeling them,
continues until no new defect types are identified. Beginning with the 50th sampled workflow,
we observe no new defect types, reaching a saturation point for 15 emergent defect categories
at 55 open-coded simulated scenario-based workflows. Cohen’s kappa across all 55 open-coded
workflows is 0.89, indicating almost perfect agreement between the two inspectors [46].
    To ensure the representativeness of the defect categories that emerge through open-coding
the simulated scenario-based workflows, we extend the analysis by open-coding the OpenAGI
FM-generated DSL workflows, following the same process described in the third labeling step. For
this purpose, we randomly select two scenarios from each of OpenAGI’s “academics”, “creation”,
“gaming”, “recommendation”, and “cooking” domains, and label their corresponding workflows
(i.e., a total of ten OpenAGI workflows) for defect incidences. During this analysis, we record the
prevalence of previously identified defect categories and investigate whether any new defect types
appear in the OpenAGI workflows. Open-coding the OpenAGI workflows does not reveal any new
defect category beyond those already identified in simulated scenario-based workflows. As such, a
taxonomy of 15 defects is created by combining the individual taxonomies developed by the two
inspectors through open-coding a total of 65 FM-generated DSL workflows.
    To ensure the completeness of the taxonomy, based on relevant literature on general-purpose
programming languages [63, 64, 78], we also include three additional defect types (i.e., violation of
concurrency constraints, unparsable JSON, and malformed expressions). This extension is motivated
by well-known struggles of FMs in generating structured outputs such as JSON objects [62] and
their limitations in generating correct mathematical expressions [37]. Additionally, based on the
observed behavior of the synthesizer FM in manipulating workflow logic (i.e., omission of logical
steps) and generating faulty outputs, we extend the taxonomy to account for the possibility of
FMs introducing incorrect logic or incorrect inputs in generated workflows. After this process, we
obtain a final taxonomy of 20 potential defect types in FM-generated DSL workflows.

3.2   Taxonomy of Defect Incidences in FM-generated DSL workflows
After conducting the empirical study in the previous section, we are able to address the first research
question regarding defects in FM-generated DSL workflows.
RQ1: What are the characteristics of defects in FM-generated DSL workflows?
   We characterize the discovered defects in FM-generated DSL workflows by categorizing them
into different types and calculating the prevalence of incidences for each defect type.
Defect categories. Figure 4 illustrates the taxonomy of defect categories in FM-generated DSL
workflows. There are 20 distinct types organized into three distinct groups: Data Errors, Logical
Errors, and Mismatch between Requirements and Workflows.
Data errors: Similar to general-purpose programming languages [56], workflows involve data
manipulation and propagation. Thus, many defect incidences in these FM-generated DSL workflows
are also caused by data-related issues.

                                 ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
10                                                                                                                                                                                                    Masoumzadeh et al.


                                                                                                Defect Categories


                             Mismatch between
                                                                                                  Logical Errors                                                                             Data Errors
                         Instructions and Workflows



                                                                                Omission                                                                                                          Violation of
     Incorrect Control                         Incorrect         Defective                         Inclusion of           Violation of                    Violation of         Incorrect                               Incorrect
                       Over-engineering                                         of Logic                                                                                                        Type Consistency
      Flow Construct                          Skill Usage        Structure                       Incorrect Logic     Reachability Constraints        Concurrency Constraints     Inputs                                 Outputs
                                                                                                                                                                                                   Constraints
                                 (3)                                                (1)                (0)                                                     (0)                (0)                                      (41)

                                                                                                                                                                                           Propagation
      Use of Defective                                                                                               Unreachable    Unused                                                                   Incorrect
                         Defective Ordering              Invalid    Unparsable        Malformed                                                                                            of Incorrect
       Control Flow                                                                                                   Variables     Variables                                                              Type Casting
                            of the Nodes                   DSL        JSON           Expressions                                                                                              Types
        Mechanism
                                                                                                                     (204)            (110)                                                    (22)              (2)
            (3)                  (2)                      (11)          (0)               (0)


                                                                              Correct Skill             Undefined                Defined but                                   Legend             Light Weight             Static
                              Incorrect   Inefficient   Hallucinated
                                 Skill       Skill          Skill
                                                                             With Defective              Variables           Unreachable Variables                                                  Analysis              Analysis
                                                                              Parameters
                                 (4)          (3)           (18)                 (528)




   Fig. 4. The taxonomy of 20 defect types in FM-generated DSL workflows, organized into three main
categories. Numbers in brackets indicate the total count of each defect found in our 65-sample open-coded
                                                 dataset.




       Incorrect Inputs in Workflows: The FM has hallucinated and has assigned faulty values
         to the inputs field of the FM-generated DSL workflow. For instance, FM has removed a
         user-specified parameter or has added an incorrect global variable in the inputs.
       Incorrect Outputs in Workflows: The FM has not adhered to the specific user instructions
         for structuring the outputs field of the FM-generated DSL workflow. For instance, while the
         user instructions require the outputs field to include only the output parameters of the last
         task node of the workflow, the outputs field includes the output parameters of some other
         node in the workflow.
       Violation of Type Consistency Constraints: The inputs to the workflow itself (global in-
         puts) can be assigned as inputs to any one of the task nodes. The output of any one of the
         preceding task nodes can also be assigned as inputs to the task nodes. If in any of these
         situations, an assignment leads to an incompatibility of types, we label it as a type consistency
         constraint violation. Situations where type casting can cause loss of precision (e.g., type
         casting from float to integer) are also labeled as defective.

Logical errors: These defects pertain to the logical mismatch between the user requirements and
their corresponding FM-generated DSL workflows.
       Violation of Reachability Constraints: The FM-generated DSL workflows could include
         erroneous data dependencies, which can be classified into two categories: (1) unreachable
         variables, i.e., variables that are used as inputs in a task node, but those variables do not have
         any values by the time that task node is executed, and (2) unused variables, i.e., variables
         produced as the outputs of one of the task nodes but never used anywhere else in the
         workflow.
       Omission of Logic: The FM-generated DSL workflow omits one or more steps of the corre-
         sponding natural language instructions.
       Inclusion of Incorrect Logic The FM-generated DSL workflow includes an additional incor-
         rect step compared to the corresponding natural language instructions.
       Violation of Concurrency Constraints: The FM-generated DSL workflow violates resource
         constraints and bound usage of its execution specifications. For instance, two task nodes in
         different branches are trying to write to the same variable concurrently.

ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
Towards Reliable Generation of Executable Workflows by Foundation Models                                            11


Mismatch between instructions & workflows: This category pertains to defect incidences caused by
semantic, syntactic, and structural differences between the natural language instructions and their
corresponding FM-generated DSL workflows.
    Incorrect Control Flow Construct: The FM-generated DSL workflow contains erroneous
      control-flow dependencies. These errors can occur due to two distinct situations. First, the
      FM-generated DSL workflow uses a different control flow construct compared to the corre-
      sponding step mentioned in the natural language instructions. Second, the FM-generated DSL
      workflow task nodes are ordered differently from the steps described within the corresponding
      natural language instructions.
    Over-engineering: The FM-generated DSL workflow includes additional nodes compared to
      the original natural-language instructions, which are inherently correct but not required in
      practice. These over-engineered nodes may include unnecessary validation steps or intricate
      analysis to satisfy rare edge cases.
    Defective Structure: The FM-generated DSL workflow is structured incorrectly. These errors
      occur due to three reasons. First, the FM-generated DSL workflow is structured as an un-
      parsable JSON object. Second, the workflow violates the specified DSL grammar. And lastly,
      the FM-generated DSL workflow includes malformed conditional or switch case expressions.
    Incorrect Skill Usage: The FM-generated DSL workflow implements a step specified in the
      natural-language instructions using an incorrect skill, manifesting as four distinct situations.
      First, the workflow implements the target step of the instructions using an incorrect action
      from the set of available skills. Second, the FM-generated DSL workflow implements the
      target step with a correct but suboptimal action. This means the decision of the FM for
      choosing that specific skill for implementing the corresponding natural language instruction
      step can be improved. Third, the FM-generated DSL workflow attempts to implement the
      target step with a non-existing action. This means the FM has hallucinated the skill while
      generating the workflow. Finally, the FM-generated DSL workflow implements the target
      step with a correct skill, but the skill is utilized with defective input and/or output parameters
      within the workflow. This could mean that, when generating the workflow, the FM has
      hallucinated the skill’s parameters and removed some of them, for example.

 RQ1: Observation 1. The taxonomy of defects in FM-generated DSL workflows comprises 20 categories,
 sorted into three distinct groups.


Prevalence of defects. Out of 65 open-coded FM-generated DSL workflows, only seven workflows
are not tainted with any incidences of defects, with the remaining 89.23% (58 out of 65) containing
at least one defect incident. On average, a workflow contains 15 defects (mean=14.65 rounded to 15,
accounting for the discrete nature of the prevalence of defects) while 24 incidences is the maximum
count of observed defects in a single workflow. The high prevalence of defects in DSL workflows,
evident by these statistics, underscores the magnitude of the problem and highlights the need for
effective mitigation strategies.
   Figure 4 also illustrates the prevalence of each of the defect types (below each category and
in brackets) across the open-coded dataset. The most frequent defect type corresponds to skills
with defective parameters with 528 defect incidences. Unreachable and unused variables are
the second and third most frequent defect types with 204 and 110 incidences, respectively. As
discussed in Section 3.1, none of the annotated workflows is tainted with unparsable JSON structure,
additional incorrect logic, malformed expressions, incorrect inputs field, or violation of concurrency
constraints. However, for completeness, and based on prior studies, we extend our taxonomy to

                                 ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
12                                                                                       Masoumzadeh et al.


include these defect types as well. The prevalence of these defect categories is noted as zero in
Figure 4.

 RQ1: Obesrvation 2. 89.23% of FM-generated DSL workflows contain at least one defect incident, with an
 average of 15 defects per workflow. Among all plausible defect types, mismatches between instructions
 and their corresponding generated workflows dominate defect incidences, while data errors are the least
 frequent defects tainting the workflows.



3.3    Generalizability of the Empirical Study
   In our empirical study (Section 3.1), we only open-code workflows that are generated by prompt-
ing OpenAI’s GPT-4o-mini-2024-07-18 model. Consequently, the observed defect incidences in
these FM-generated DSL workflows may not extend to workflows that are synthesized by other
models, such as Meta’s Llama. However, recent benchmarking results have shown that model per-
formances from all frontier labs have converged, which can be attributed to likely heavy overlaps
in their pre-training data [12]. Therefore, we hypothesize that using different FMs to generate DSL
workflows would have a negligible influence on the types of defects that may occur.
   To confirm our hypothesis, we investigate whether different synthesizer FMs generate workflows
that are tainted with defect types that are not included in our taxonomy. For this purpose, we
randomly selected ten scenarios from the population of 200 simulated user scenarios, alongside their
elicited requirements and natural language instructions used in the empirical study (Section 3.1). We
then employ two different workflow synthesizer FMs, Meta’s Llama-3-70B and Alibaba’s Qwen-7B
(hereafter referred to as Llama and Qwen, respectively) and follow the same procedure outlined
in Section 3.1 to generate DSL workflows for the selected simulated scenarios and annotate them
for their occurring defect types and their prevalence. We specifically choose these two models to
conduct a comprehensive analysis over the plausible confounding effects of varying characteristics
of synthesizer FMs (i.e., open-source or proprietary, different architectures, and number of learnable
parameters) on occurring defect types in FM-generated DSL workflows.
   Table 1 presents the identified defect types and their prevalence across DSL workflows generated
by Llama and Qwen. As can be observed from the table, defect types annotated in Llama- and
Qwen-generated workflows remain similar to the taxonomy of defect types created through
annotating GPT-generated workflows. Only the prevalence of defects varies across workflows
grouped by synthesizer FMs. Thus, we can conclude that our initial hypothesis on the consistency
of occurring defect types, regardless of the used synthesizer FM, holds true. This, in turn, confirms
the extensibility of our defect taxonomy to different synthesizer model families with varying
characteristics.
   Armed with our taxonomy of common defects, we then design and implement a toolchain to
automatically detect and repair the most frequent and programmatically identifiable issues.
4 Detection and Repair of Workflow Defects
In this section, we present Timon, a tool for detecting defects in FM-generated workflows and
Pumbaa, a tool for repairing workflow defects with the assistance of static analysis feedback in
DSL workflows.

4.1    Timon: The Static Analyzer for FM-generated DSL workflows
We develop Timon, as the first-of-its-kind static analyzer to automatically detect defect types
frequently observed in FM-generated DSL workflows. Timon’s novelty lies within the application
target, i.e., Timon is the first-ever tool that applies well-established defect detection techniques,

ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
Towards Reliable Generation of Executable Workflows by Foundation Models                                            13


         Table 1. Prevalence of defect types across DSL workflows generated by Llama and Qwen

                                                            Llama-generated Qwen-generated
                 Defect Categories
                                                             DSL Workflows DSL Workflows
                                                   Data Errors
                 Incorrect Inputs                                    5                    1
                 Incorrect Outputs                                   2                    7
                 Propagation of Incorrect Types                      7                    3
                                                  Logical Errors
                 Unreachable Variables                               51                  51
                 Unused Variables                                   N/A                  7
                 Inclusion of Incorrect Logic                         1                 N/A
                 Omission of Logic                                    1                 N/A
                 Use of Defective Control Flow Mechanism              4                  1
                                Mismatch between Instructions and Workflows
                 Over-engineering                                   N/A                  1
                 Incorrect Skill                                      4                  10
                 Hallucinated Skill                                 N/A                  11
                 Correct Skill with Defective Parameters             53                  75
                 Invalid DSL                                        N/A                  1
                 Unparsable JSON                                     10                  10



that are designed for general-purpose programming languages, to FM-generated DSL workflows
for detecting their defect incidences. Timon’s detectable defect types encompass all categories that
can be identified without human intervention or workflow execution. For instance, incidences of
defects such as over-engineering or inefficient skill cannot be detected without human intervention;
human judgment is required to determine whether a more optimal action exists for implementing
the target step within the workflow. Similarly, it is necessary to execute the workflows to detect
their violations of concurrency constraints. Thus, detecting these defect types is out of the scope of
Timon. As such, Timon is able to detect the following nine defect types from the defect taxonomy
in Section 3.2: unparsable JSON, invalid DSL, unreachable variables, unused variables, incorrect
data type propagation, hallucinated skills, skills with defective parameters, malformed expressions,
and incorrect outputs. These correspond to defects in our taxonomy (Figure 4) that are marked as
detectable via lightweight and static analyses. The former, i.e., lightweight analysis, corresponds to
detection techniques that do not rely on intermediate representations of the FM-generated DSL
workflows (for more details, please refer to Intermediate Representation Constructor B below).
The latter, i.e., static analysis, refers to detection techniques that operate on the intermediate
representations of the workflows. We illustrate an overview of the tool in Figure 5, which comprises
three key steps, namely: Structure Validator A , Intermediate Representation Constructor B , and
Defect Detector C . We describe each of these steps in detail below.
Structure Validator A . First, Timon receives a FM-generated DSL workflow as a string input and
attempts to parse it into a valid JSON A.1 . If the input FM-generated DSL workflow is successfully
parsed, then Timon attempts to instantiate the JSON object as a valid DSL program adhering
to our specified grammar A.2 , with the support of Pydantic [18] type checking library. If the
FM-generated DSL workflow cannot be parsed into a valid JSON or the instantiated DSL program
does not follow the grammar, Timon records a defect incident for unparsable JSON or invalid DSL,
respectively.

                                 ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
14                                                                                                                              Masoumzadeh et al.


                                                                                                                    C Defect Detector

                                                                                                              C.1                       C.2

                                                                      B Intermediate Representation       Unreachable              Unused
                                                                                   Constructor          Variable Detector      Variable Detector
                                A Structure Validator
      Workflow                                                               B.1                              C.3
                                                                                                              C.1                       C.4
                                                                                                                                        C.1
                        A.1                      A.2
                                                 A.1
                                                                             Control Flow Graph          Incorrect Type          Malformed
                                         Yes                    Yes
                       JSON                      DSL                            Constructor           Propagation Detector   Expression Detector
                                    ?                      ?
                       Parser                  Validator                     B.2                              C.5
                                                                                                              C.1                       C.6
                                                                                                                                        C.1

                                                                              Use-Def, Def-Use         Hallucinated Skill       Defective Skill
                                                                               Chains Builder              Detector           Parameter Detector


                                    No                     No                                                       Defective Outputs
                                                                                                              C.7
                                                                                                              C.1
                                                                                                                     Field Detector




                                                                            Defect Recorder




                 Fig. 5. The overview of Timon: The static analyzer for DSL workflow defect detection


Intermediate Representation Constructor B . As the next step, Timon constructs an inter-
mediate representation from the DSL workflow. Specifically, a control flow graph (CFG) [3] is
constructed B.1 by parsing the DSL representation of the workflow. Afterwards, from the con-
structed CFG Timon builds use-def and def-use chains B.2 .
Defect Detector C . Receiving the constructed intermediate representation as input, the defect
detector component is executed to identify incidences of various defects. Using the constructed
use-def chain, Timon tracks whether a used variable in a target node of the CFG is assigned with a
value (i.e. outputted) in a prior node C.1 . Similarly, using def-use chain, the tool evaluates whether
each defined variable in a target node is used in at least one following node C.2 . Furthermore,
using use-def and def-use chains, Timon analyzes the propagation of variables for ensuring the
consistency of their primitive data types between their definition and usage C.3 . Timon also
evaluates the well-formedness of existing expressions in conditions of loops and cases of switch
statements C.4 . For this purpose, the tool attempts to parse each expression into a valid abstract
syntax tree (AST). If the target expression is successfully parsed into an AST, reachability and usage
of the expression’s variables are further analyzed by adding them to use-def and def-use chains.
Timon can also detect whether task-corresponding actions in DSL workflows are hallucinated C.5 .
To do this, Timon compares each task-corresponding action used within the workflow against all
available skills stored in the skills database of the workflow execution environment. If the target
task-corresponding action does not exist within the database, that action is marked as hallucinated.
By conducting a similar comparison, Timon is able to identify existing task-corresponding actions
that are used with incorrect input and/or output parameters within the workflow C.6 . Finally,
Timon also detects whether the outputs field of the workflow adheres to the specific predefined
format passed as user instruction at the time of workflow generation C.7 .

4.2     Pumbaa: The FM-based Repair Tool for FM-generated DSL workflows
Next, we use Pumbaa to repair defective FM-generated DSL workflows. Pumbaa operates by
prompting a FM to repair defect incidences in an input workflow per defect type, incorporating
Timon’s report of detected defects as direct feedback for an accurate and effective repair. This key
idea of providing feedback from the defect detection step is inspired by prior work [15, 23] where
the structured output from a verifier component, such as a logic checker, code interpreter, or a test

ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
Towards Reliable Generation of Executable Workflows by Foundation Models                                                                                                15



        (55)                                          (10)                                                          No                           Yes
                                 (40)

   Simulated Scenario-                                                                                                         Yes
                                                                                             Compare                     ?                       ?        No   Finish
      based Dataset        Defective Ground     Defective Ground
                           Workflows Truths     Workflows Truths
       (185)                                                           Timon     Detection             Detection   Defective       Pumbaa        Valid
                          Simulated Scenario-       OpenAGI        (The Detector) Report               Accuracy    JSON/DSL     (The Repairer) JSON/DSL
                                based
      OpenAGI Dataset


      A Data Selection                                             B Detection                                     C Repair




                                                Fig. 6. The experiment design



suite, is used alongside the FM to increase the robustness of output generation, i.e., the application
of a verifier-in-the-loop for automatically repairing defects when FMs are used as synthesizers of
general-purpose programming languages. The intuition is that the direct, unambiguous feedback
from the defect detector precisely signals to the FM where its output deviates from the desired
criteria. As Timon can only automatically detect nine defect types, from the 20 emergent defect
categories in the created taxonomy, Pumbaa can also repair the incidences of these defect types
across the FM-generated DSL workflows. Similar to prior efforts implementing test-time iterative
strategy for improving the success rate of FMs [68, 74], Pumbaa also iteratively prompts the FM to
repair the input workflow’s defect incidences.
   To ensure the effectiveness of Pumbaa’s prompts, a series of prompt engineering investigations
is conducted. At each step, the improvement of Pumbaa’s repair performance is validated against
a set of ten defective FM-generated DSL workflows. First, a prompt is carefully crafted for each
specific defect type, tailored to repair instances of that defect category based on feedback from the
static analyzer report. For each target defect type, specific additional instructions are appended to
the prompt as context information. For instance, when repairing an invalid DSL, the DSL grammar
is provided as a TypeScript type definition. For correcting incorrect outputs, the specific user
instruction for formatting the outputs field is provided. To correct hallucinated skills and skills
with defective parameters, a list of available skills in the execution environment is appended to the
prompt. At the second step, spell and grammar checkers are used to improve clarity and minimize
any content ambiguities [30]. Next, few-shot prompting and in-context learning are applied to
guide the FM’s inference process [13]. Finally, OpenAI’s [53] and Anthropic’s [4] prompting guides
are consulted to refine the prompts such that their efficacy is maximized. The full prompts used by
Pumbaa are available in the replication package.

4.3       Experiment Setup
To evaluate the performance of our automatic detection and repair tools for defect incidences
in FM-generated DSL workflows, we set up an experiment with three key stages, namely Data
Selection A , Detection B , and Repair C , demonstrated in Figure 6 and discussed in detail next.
Data Selection A & Detection B . We investigate the performances of our tools in two folds. First,
from the total population of 55 open-coded simulated scenario-based workflows (Section 3.1 A ),
we randomly select 40 and evaluate defect detection and repair performances of Timon and Pumbaa
across them. We also investigate the performances of Timon and Pumbaa on DSL workflows that
are generated from real-world user scenarios. For this purpose, we use the same ten OpenAGI
FM-generated DSL workflows that are open-coded for creating the defect taxonomy. For more
details on OpenAGI user scenarios and their corresponding workflows, please refer to Section 3.1 A .
The selected 40 simulated scenario-based workflows alongside the ten OpenAGI workflows form
the evaluation set of our experiment.

                                     ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
16                                                                                       Masoumzadeh et al.


   For each sample in the evaluation set (either a simulated scenario-based or an OpenAGI workflow),
Timon is executed to record incidences of different defect types in that sample. We then compare
the result report of Timon for each sample against its open-coded ground truth. By conducting this
comparison, we can categorize the defect incidences into three groups. Defect instances in ground
truth and also the Timon’s identified set are true positives (TPs). Instances that only appear in the
Timon’s identified set are false positives (FPs), while instances only appearing in the ground truth
are false negatives (FNs). To evaluate the performance of Timon, we use the TPs, FPs, and FNs and
calculate the tool’s precision and recall.

Repair C . We start the repair of the FM-generated DSL workflows in the evaluation set with
unparsable JSON and invalid DSL defect types. If the FM-generated DSL workflow cannot be parsed
into a valid JSON or the generated program does not follow the specification of WorkflowDSL
grammar, analyzing it for incidences of other defect types is futile. Hence, if Timon detects either
of these defects for the sample workflow, it pauses the detection process and sends the invalid
workflow to Pumbaa. If Pumbaa is able to correct the input such that it can be successfully parsed
as a JSON object and instantiated as a valid DSL program, the corrected DSL program is sent
back to Timon to continue the defect detection process for other defect categories and produce a
comprehensive report for all incidences of nine defect types. Otherwise, that input workflow is
marked as “incomprehensible” and the rest of the detection and consequent repairs are skipped.
   After retrieving Timon’s report of defect incidences for each FM-generated DSL workflow in the
evaluation set, using Pumbaa, we attempt to repair the sample workflow incorporating Timon’s
report as direct feedback. To demonstrate the impact of inherent capabilities of the used FM on
the repair performance of Pumbaa, we design our experiment to include both proprietary and
open-source FMs. Used models are of varying parameter counts, ranging from smaller variants to
larger ones, and different architectures, both dense and mixture of experts (MoE). In particular, we
use and compare the repair performance of three different families of models including OpenAI’s
GPT-4o-2024-08-06 (as the proprietary model, with an estimation of 200 billion parameters and a
MoE architecture), Meta’s Llama-3-70B, and Alibaba’s Qwen-7B (both as open-source models, with
dense architectures and a medium and small count of learnable parameters, respectively). From
here on, we refer to these models as GPT-4o, Llama, and Qwen, respectively. To minimize any
confounding factors which may influence the performance of these models, we set their decoding
parameters to be similar, with their temperature set as 0.7 and their context window limit set as
the maximum which consists of 128, 000 tokens for GPT-4o and 8, 192 tokens for both Llama and
Qwen models.
   For each FM setting, Pumbaa iteratively prompts the model to repair the sample workflow for
its defect incidences per category till all reported incidences for the target defect type are repaired
or the maximum count of repair attempts is exhausted. This means that Pumbaa repairs defect
incidences across varying types sequentially. If Pumbaa is able to repair defect incidences of a
certain type before or by the time the maximum count of repair attempts is reached, the repair of
the target defect type is considered to be successful. Based on prior studies conducting iterative
examination to account for the stochasticity in FM completions [34, 42], we set the maximum count
of repair attempts for each defect type to ten and compare the performances of the used models
with each other in repairing incidences of each defect type as a value of pass@k accuracy [14]. In
this context, for each defect type, the model with the best repair capabilities is the one with the
highest number of correctly repaired defect incidences from the initial count of reported defects by
Timon given at most ten (i.e., k=10) repair attempts for that particular defect type.
   After identifying the best performing FM, we implement the test-time strategy for that specific
model. Specifically, Pumbaa iteratively prompts the selected FM to repair defect incidences of a

ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
Towards Reliable Generation of Executable Workflows by Foundation Models                                            17


particular type, while calculating the repair performance of the FM at each iteration using pass@k
accuracy. To evaluate the effect of increasing attempts on the FM’s repair capabilities we increase
k (ranging from one to ten) and investigate whether increasing the number of repair attempts
enhances the FM’s repair capabilities.
   To minimize the confounding factors and to be able to evaluate the effectiveness of Pumbaa in
correcting reported defect incidences, Pumbaa is executed for each defect category independently
from the rest of the defect types. This means, for instance, after the sample workflow is attempted
for the repair of all its unreachable variables, to repair the reported incidences of unused variables,
we use the initial defective workflow sample as Pumbaa’s input and not the version of the workflow
that has been repaired for its unreachable variable defects.
   Pumbaa can introduce new defects while repairing defective FM-generated DSL workflows. The
newly introduced defects by Pumbaa, however, will be detected by Timon as after each repair
attempt by Pumbaa, the target workflow is re-examined by the static analyzer to verify whether all
original defect incidences are resolved. As such, if Pumbaa generates new defects while trying to
repair the original incidents, the newly occurring defects will be detected and localized by Timon,
with their detection report sent back to Pumbaa for initiating their repair. Conceptually, Pumbaa
can also generate defects that are not detectable by Timon, i.e., defect types such as omission of
logic or violation of concurrency constraints that require human intervention or the execution of
workflows for their detection, respectively. However, we have yet to observe such errors caused by
Pumbaa in practice.
   Prior research demonstrated that FMs are incapable of conducting intrinsic self-correction
attempts, solely based on their inherent capabilities and no use of external feedback, for improving
their initial generation accuracy [26, 32]. Interestingly, the performances of these models are even
shown to degrade after a few iterations of self-correction attempts. Therefore, we design Pumbaa to
incorporate direct feedback from Timon’s defect reports for an accurate defect repair performance.
Nonetheless, we conduct an evaluation on the effectiveness of incorporated feedback from Timon
on the repair performance of Pumbaa. To do so, we directly prompt Pumbaa to analyze an input
FM-generated DSL workflow for existing defect incidences and repair them, if any, in place. The
definition of defect types and corresponding few-shot examples are appended as additional context
information to the prompt instructions. Similar to the incorporation of feedback, this setting is also
implemented as a test-time iterative strategy, with pass@k (k=10) calculated as the accuracy of
Pumbaa.

4.4   Experiment Results
In this section of the paper, we present the results of the experiment. We set out to find answers to
the following two research questions.
RQ2: How accurately can FM-generated DSL workflow defects be detected using static
analysis?
  We develop Timon as an automated detection tool assisting developers to identify defect inci-
dences in FM-generated DSL programs. Hence, we assess how accurately Timon can locate defects
within a FM-generated DSL workflow.
RQ3: How effective are FMs at repairing FM-generated DSL workflow defects when pro-
vided with static analysis feedback?
   We conclude our effort in automatic detection of defects in FM-generated DSL workflows by
attempting to repair them using our repair tool, Pumbaa. Hence, we also assess the effectiveness of
Pumbaa in repairing the detected defects by Timon.

                                 ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
18                                                                                       Masoumzadeh et al.


Accuracy of Detection (RQ2). The accuracy of Timon in detecting defect incidences in FM-
generated DSL workflows is demonstrated in Table 2. The accuracy of the tool varies across defect
categories, with 100% precision and recall for the detection of unparsable JSON, invalid DSL,
hallucinated skills, skills with defective parameters, malformed expressions, and incorrect outputs
across the 40 simulated scenario-based workflows. Similarly, across the OpenAGI workflows, Timon
is able to detect invalid DSL, hallucinated skills, skills with defective parameters, and incorrect
outputs with 100% precision and recall. It should be mentioned that, as no defect incidence of
unparsable JSON and malformed expressions exist across either of simulated scenario-based or
OpenAGI workflows, for the sake of conducting a complete evaluation of the detection capabilities
of Timon, we randomly choose ten simulated scenario-based workflows to change their structure
such that they do not parse into JSON objects anymore. As such, we can investigate Timon’s
performance in detecting unparsable JSONs. Similarly, we randomly select ten additional simulated
scenario-based workflows and inject them with malformed expressions (one incident per workflow)
to evaluate Timon’s detection performance for this defect type. We do not choose any of the
OpenAGI FM-generated DSL workflows to inject them with incidences of unparsable JSON or
malformed expressions, as these workflows are generated from real-world scenarios. Artificially
manipulating OpenAGI workflow structures compromises their representative nature of real-world
settings.
   Timon demonstrates an absolute recall and a high precision (75%) when attempting to detect
unused variables across simulated scenario-based workflows. Interestingly, Timon has almost
identical recall when detecting unreachable variables and incorrect data type propagation (71% and
72%, respectively) across the same workflows. However, its precision is different with 50% and 37%
for unreachable variables and incorrect data type propagation, respectively. Timon demonstrates
similar detection performance for unreachable and unused variables across simulated scenario-
based and OpenAGI workflows. For detecting unreachable and unused variables and incorrect data
type propagation, all program paths in the input FM-generated DSL workflows should be analyzed
to detect variable placements on infeasible paths. Analyzing the program paths for their feasibility
requires evaluating all possible combinations for input parameters, even when their values are only
known at runtime. Hence, additional measures alongside static analysis should be placed to enable
such an evaluation of program paths. This necessity is discussed in more detail in section 5.

 RQ2. Although having varied performance across different categories, Timon demonstrates an acceptable
 performance in detecting defect incidences of FM-generated DSL workflows, with a comparatively high recall
 of 80% and 87% across simulated scenario-based and OpenAGI workflows, respectively. This is particularly
 important, as Timon is designed to detect the majority of existing defects with high confidence.


Effectiveness of Repair (RQ3). Table 3 provides granular pass@10 metrics for the count of
repaired defect incidences across different splits of executing Pumbaa over the 40 simulated
scenario-based workflows, using GPT-4o, Llama, and Qwen models. As can be observed from the
table, the best collective performance belongs to GPT-4o, with Llama and Qwen performing 75.17%
and 85.66% worse, respectively.
   Llama cannot repair any incidences of incorrect data type propagation and skills with defective
parameters while the accuracy of GPT-4o for repairing these defects is 21.82% and 31.01%, respec-
tively. Although repairing some incidences of unused variables, Llama’s performance is 34.37%
points lower than GPT-4o’s. The performance of Llama is on par with GPT-4o’s, when repairing
incorrect outputs, hallucinated skills, invalid DSL, and unreachable variables.
   Compared to Llama, Qwen performs even worse. Qwen cannot repair any of incorrect data type
propagation, unused variables, skills with defective parameters, and invalid DSL. When repairing

ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
Towards Reliable Generation of Executable Workflows by Foundation Models                                                 19


                          Table 2. Timon accuracy across different defect categories

                       Workflow Type                            Shadow            OpenAGI
                       Defect Category                      Precision Recall Precision Recall
                       Unparsable JSON                           100%     100%         N/A    N/A
                       Invalid DSL                               100%     100%        100%   100%
                       Unreachable variables                      50%      71%         33%    58%
                       Unused variables                           75%     100%         53%    89%
                       Incorrect data type propagation            37%      72%         N/A    N/A
                       Hallucinated skills                       100%     100%        100%   100%
                       Skills with defective parameters          100%     100%        100%   100%
                       Malformed expressions                     100%     100%         N/A    N/A
                       Incorrect outputs                         100%     100%        100%   100%
                       Overall                                      56%    80%        67%    87%


 Table 3. Defect repair performance of Pumbaa using three different FMs (GPT-4o, Llama, Qwen). Results
                   demonstrate the improvement gained from static analysis feedback.

                                   Detection                Pass@10                                 Relative
                                    Count                 Repair Count                           Improvement (%)
Defect Categories                   Timon      Baseline   GPT-4o    Llama      Qwen   Baseline    GPT-4o     Llama    Qwen
Invalid DSL                                3          0         0          0      0         0%          0%       0%       0%
Unreachable variables                    254          7        20         21      7      2.76%       7.87%    8.27%    2.76%
Unused variables                         128          4        60         16      0      3.13%      46.88%   12.50%       0%
Incorrect data type propagation           55          0        12          0      0         0%      21.82%       0%       0%
Hallucinated skills                        3          3         3          3      3      100%        100%     100%     100%
Skills with defective parameters         516          0       160          0      0         0%      31.01%       0%       0%
Incorrect outputs                         31         31        31         31     31      100%        100%     100%     100%
All defect types                         990         45       286         71     41      4.55%      28.89%    7.17%    4.14%



unreachable variables, Qwen’s performance is 5.12% points lower compared to that of GPT-4o,
only repairing seven out of 254 detected incidences. Finally, Qwen’s performance is on par with
GPT-4o’s, when repairing incorrect outputs and hallucinated skills.
   Table 3 shows that regardless of the used FM, Pumbaa is incapable of repairing invalid DSLs.
The reason for this can be attributed to the limited capabilities of FMs in generating structured
outputs [62]. Although literature focuses on evaluating the abilities of FMs in directly synthesizing
structured outputs, repairing a defective DSL can also be considered as re-synthesizing the program
such that it correctly adheres to the structure of the specified grammar. This, in turn, explains
why Pumbaa does not repair invalid DSLs successfully. On the other hand, we observe that in all
settings of the underlying FM, Pumbaa repairs the incidences of hallucinated skills. Compared to
the repair of complex defects such as invalid DSLs, the repair of hallucinated skills is much simpler.
The incidences of hallucinated skills pertain to already existing actions in the skill database, that
are referenced with faulty names (i.e., spelling errors or incorrect format) in the workflows. In
other words, no hallucination occasion exists in the end where the synthesizer FM had fabricated
an action in the generated workflow in the beginning. As the existing skills are appended to the
context of the repair prompt (Section 4.2), Pumbaa’s underlying FM can compare the actions in the
target workflow with their actual forms, correcting the names of the hallucinated skills.
   From these results, we observe that model performance varies across models, which may be
attributed to factors such as model architecture (MoE vs. Dense), parameter count, and training

                                   ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
20                                                                                       Masoumzadeh et al.


data composition. For instance, the results demonstrate that the higher the count of the learnable
parameters in an LLM, the better its performance in repairing the defect incidences in FM-generated
DSL workflows.
   Table 3 also demonstrates the effectiveness of incorporated feedback from Timon’s defect in-
cidences report on the repair performance of Pumbaa. Specifically, the capabilities of GPT-4o in
directly detecting and repairing defect incidences in FM-generated DSL workflows are shown as
the baseline repair accuracy at pass@10. In this setting, Pumbaa is able to repair only 4.55% of all
defect incidences across the evaluation set which is 84.25% relatively lower repair performance
compared to when Timon’s feedback is also incorporated. According to these results and all prior
comparisons between different FMs’ capabilities in repairing defect incidences, GPT-4o with incor-
porated feedback from Timon is demonstrated to be Pumbaa’s best performing setting in repairing
defective FM-generated DSL workflows. Hence, the test-time iterative strategy is implemented for
this setting. Additionally, the same configuration (i.e., GPT-4o incorporated with Timon’s feedback)
is used for investigating Pumbaa’s repair performance across the OpenAGI workflows.
   Figure 7 illustrates the results of the test-time iterative strategy for GPT-4o as pass@k accuracies,
across different values of k ranging from one to ten. As observed from the figure, increasing k
improves the repair performance of Pumbaa. From the six repaired defect types, Pumbaa repairs
all of the incorrect outputs and hallucinated skills at pass@1. For the remaining four defect types,
Pumbaa’s performance saturates at pass@2, pass@3, pass@5, and pass@6 for unused variables,
unreachable variables, skills with defective parameters, and incorrect data type propagation, re-
spectively. Although Pumbaa’s performance does not saturate uniformly across different defect
types, the collective trend illustrates a direct relationship between iteration and performance.
Specifically, 27.07%, 28.08%, 28.59%, 28.59%, and 28.69% of all defect incidences are repaired at
pass@1, pass@2, pass@3, pass@4, and pass@5. Finally, the performance saturates by the 6th pass,
repairing 28.89% of all defect incidences which account for 10% of the population of simulated
scenario-based workflows as fully repaired programs.
   Figure 7 also demonstrates the corresponding costs for repairing the incidences of all defect types
across the simulated scenario-based workflows and varying repair attempts. The cost of each repair
attempt is calculated as the sum of the monetary cost corresponding to input token usage and
completion token count for that specific repair attempt. The inference cost of GPT-4o is USD 2.5 and
USD 10 per one million input and completion tokens, respectively [54]. As expected, increasing the
number of repair attempts directly increases costs (i.e., a linear relationship). Given the saturation
of repair performance at pass@6 and the ever-increasing token usage and corresponding costs, we
recommend setting Pumbaa’s maximum repair attempt count to six in practical settings. However,
based on their discretion, users may choose a different value for the maximum allowed repair
attempts.
   Table 4 demonstrates Pumbaa’s performance in repairing defect incidences of the OpenAGI FM-
generated DSL workflows. It is evident that the performance of Pumbaa in repairing hallucinated
skills and incorrect outputs is the same as the tool’s performance when repairing the same defect
types across the simulated scenario-based workflows. Additionally, Pumbaa’s repair performance
for unreachable variables in OpenAGI workflows is on par with the tool’s performance when
it is employed to repair the same defects in simulated scenario-based workflows. Compared to
Pumbaa’s performance in repairing incidences of skills with defective parameters and invalid
DSLs in simulated scenario-based workflows, the tool’s performance demonstrates considerable
enhancement when repairing the same defect types across the OpenAGI workflows. Particularly, the
tool’s performance increases from 31.01% to 100% and from 0% to 12.50% while repairing incidences
of skills with defective parameters and invalid DSLs, respectively. On the other hand, Pumbaa’s


ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
Towards Reliable Generation of Executable Workflows by Foundation Models                                                                                                                                                                                                                                                                                                                                                              21



                                                               Defect: Incorrect outputs                                                                               Defect: Propagation of incorrect types                                                                 Defect: Unused variables                                                                              Defect: Unreachable variables
                                                        34                                                                                                        15                                                                                                    63                                                                                                    23
                                                                                                                                                                                                                                                                        62                                                                                                    22




                                                                                                                                                                                                                Pass@k Repair Count, Total Defect Count=128




                                                                                                                                                                                                                                                                                                                                Pass@k Repair Count, Total Defect Count=254
                                                                                                                                                                  14
           Pass@k Repair Count, Total Defect Count=31




                                                                                                                     Pass@k Repair Count, Total Defect Count=55
                                                        33                                                                                                                                                                                                              61
                                                                                                                                                                                                                                                                                                                                                                              21
                                                                                                                                                                                                                                                                        60
                                                                                                                                                                  13                                                                                                                                                                                                          20
                                                                                                                                                                                                                                                                        59
                                                        32                                                                                                                                                                                                              58                                                                                                    19
                                                                                                                                                                  12
                                                                                                                                                                                                                                                                        57                                                                                                    18
                                                        31                                                                                                        11                                                                                                    56
                                                                                                                                                                                                                                                                        55                                                                                                    17
                                                                                                                                                                  10                                                                                                    54                                                                                                    16
                                                        30
                                                                                                                                                                                                                                                                        53                                                                                                    15
                                                                                                                                                                  9
                                                                                                                                                                                                                                                                        52
                                                        29                                                                                                                                                                                                                                                                                                                    14
                                                                                                                                                                  8                                                                                                     51
                                                                                                                                                                                                                                                                        50                                                                                                    13
                                                                                       Pass@k                                                                                                       Pass@k                                                                                              Pass@k                                                                                               Pass@k
                                                        28                                                                                                        7                                                                                                     49                                                                                                    12
                                                             1 2 3 4 5 K 6 7 8 9 10 11                                                                                   1 2 3 4 5 K6 7 8 9 10 11                                                                            1 2 3 4 5 K 6 7 8 9 10 11                                                                              1 2 3 4 5 K 6 7 8 9 10 11

                                                              Defect: Hallucinated skills                                                                          Defect: Skills with defective parameters                                                                       Defect: Invalid DSL                                                                                     All Defect Types
                                                        6                                                                                                   163                                                                                                         3                                                                                                     289
                                                                                                                                                                                                                                                                                                                                                                              288                                     2.32
                                                                                                                                                                                                                                                                                                                                                                              287
Pass@k Repair Count, Total Defect Count=3




                                                                                                                                                            162
                                                                                                Pass@k Repair Count, Total Defect Count=516




                                                                                                                                                                                                                                                                                                                 Pass@k Repair Count, Total Defect Count=990
                                                                                                                                                                                                                                                                                                                                                                              286

                                                                                                                                                                                                                            Pass@k Repair Count, Total Defect Count=3
                                                        5                                                                                                                                                                                                               2                                                                                                     285                                     2.09
                                                                                                                                                            161                                                                                                                                                                                                               284
                                                                                                                                                                                                                                                                                                                                                                              283                                     1.86
                                                                                                                                                                                                                                                                                                                                                                              282
                                                        4                                                                                                   160                                                                                                         1                                                                                                     281




                                                                                                                                                                                                                                                                                                                                                                                                                         Inference Price (USD)
                                                                                                                                                                                                                                                                                                                                                                              280                                     1.62
                                                                                                                                                            159                                                                                                                                                                                                               279
                                                                                                                                                                                                                                                                                                                                                                              278                                     1.39
                                                        3                                                                                                                                                                                                               0                                                                                                     277
                                                                                                                                                            158                                                                                                                                                                                                               276                                     1.16
                                                                                                                                                                                                                                                                                                                                                                              275
                                                                                                                                                                                                                                                                                                                                                                              274                                     0.93
                                                        2                                                                                                   157                                                                                                          1                                                                                                    273
                                                                                                                                                                                                                                                                                                                                                                              272
                                                                                                                                                            156                                                                                                                                                                                                               271                                     0.70
                                                                                                                                                                                                                                                                                                                                                                              270
                                                        1                                                                                                                                                                                                                2                                                                                                    269                                  0.46
                                                                                                                                                            155                                                                                                                                                                                                               268            Pass@k
                                                                                       Pass@k                                                                                                       Pass@k                                                                                              Pass@k                                                                267            Inference Price (USD) 0.23
                                                                                                                                                                                                                                                                                                                                                                              266
                                                        0                                                                                                   154                                                                                                          3                                                                                                    265
                                                             1 2 3 4 5 6 7 8 9 10 11                                                                                     1 2 3 4 5 6 7 8 9 10 11                                                                             1 2 3 4 5 6 7 8 9 10 11                                                                                1 2 3 4 5 6 7 8 9 10 11
                                                                      K                                                                                                           K                                                                                                   K                                                                                                       K




                                                                                                Fig. 7. Effect of test-time iterative strategy on Pumbaa

performance in repairing unused variables decreases 20.21% points, when the tool is applied to the
OpenAGI workflows instead of the simulated scenario-based ones. Generally, however, the repair
performance of Pumbaa increases 11.59% points when it is applied to the OpenAGI workflows
instead of the simulated scenario-based workflows, demonstrating its applicability in practical
settings.

                                                         Table 4. Defect repair performance of Pumbaa across the OpenAGI FM-generated DSL workflows

                                                                                                                                                                                             Detection Count                                                                           Pass@10                                                                                   Relative
                                                                   Defect Categories
                                                                                                                                                                                                 (Timon)                                                                             Repair Count                                                                             Improvement (%)
                                                                   Invalid DSL                                                                                                                                                                                                8                             1                                                                                   12.50%
                                                                   Unreachable variables                                                                                                                                                                                     33                             3                                                                                    9.09%
                                                                   Unused variables                                                                                                                                                                                          15                             4                                                                                   26.67%
                                                                   Hallucinated skills                                                                                                                                                                                       15                            15                                                                                    100%
                                                                   Skills with defective parameters                                                                                                                                                                          12                            12                                                                                    100%
                                                                   Incorrect outputs                                                                                                                                                                                          4                             4                                                                                    100%
                                                                   All defect types                                                                                                                                                                                          84                            34                                                                                   40.48%


   We also conduct token usage, monetary cost, and inference time analyses for the repair of
defective OpenAGI workflows by Pumbaa. As can be observed from Figure 8, similar to the case of
applying Pumbaa to repair defect incidences across the simulated scenario-based workflows, with
each repair attempt, the token usage and the corresponding cost increase linearly.
   Although not all existing defect incidences in the evaluation set are repaired, using Pumbaa
in a production setting can still be valuable. Pumbaa’s accuracy in repairing incorrect outputs
and hallucinated skills is 100% across both simulated scenario-based and real-world OpenAGI

                                                                                                                                                                        ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
22                                                                                                                                                                                                Masoumzadeh et al.



                                          Input Tokens                                                  1.61                                      798.2
                                350       Completion Tokens
                                          Inference Price (USD)                                         1.45                                      717.8
                                300
                                                                                                        1.29                                      643.9
     Mean Token Count (x10^3)




                                250




                                                                                                                          Inference Time (Sec.)
                                                                                                        1.13                                      558.0




                                                                                                           Average Cost
                                200                                                                     0.96                                      471.6
                                                                                                        0.80                                      393.9
                                150
                                                                                                        0.64                                      317.9
                                100
                                                                                                        0.48                                      237.8
                                50                                                                      0.32                                      164.7

                                 0                                                                      0.16                                       87.4
                                      1           2          3    4   5            6   7   8   9   10                                                     1   2   3      4   5            6   7     8   9   10
                                                                          Pass@K                                                                                                 Pass@K


                                                 (a) Token and monetary cost                                                                                          (b) Inference time

                        Fig. 8. Token, cost, and time analyses for the repair of the OpenAGI FM-generated DSL workflows


workflows. This is especially important as, in practice, not all FM-generated DSL workflows are
tainted with other defect types, for which Pumbaa’s repair performance may be lower, making
Pumbaa a practical tool for production settings. Additionally, Pumbaa is only one part of our
end-to-end pipeline for generating robust and executable workflows using FMs. If Pumbaa is not
able to repair all defect incidences in input FM-generated DSL workflows, to be feasibly used in
production, the system should incorporate fallback mechanisms. For instance, after showing a
detailed compilation of remaining defect types and their locations in the input FM-generated DSL
workflows, the system should defer to end users and their expertise for repairing them.

 RQ3. The ability of FMs to repair the defects of FM-generated DSL programs varies across different families of
 models and different defect types. Nonetheless, incorporating feedback from Timon’s defect incidence report
 and implementing a test-time iterative strategy have been shown to enhance Pumbaa’s repair performance.

5                    Discussion and Practical Implications
In this section of the paper, we discuss the results and their implications for researchers and
developers.

Implication 1: Practitioners should consider additional mechanisms to successfully
synthesize DSL program instances using FMs.
Our observations demonstrate that even the most powerful proprietary FMs, with MoE architec-
ture and a larger count of learnable parameters, are not successful in directly synthesizing DSL
workflows. Hence, employing additional guardrails for ensuring the FMs’ success in synthesizing
DSL program instances is inevitable. Specifying the DSL as a FM-friendly grammar should be
the initial consideration to be explored for enabling a successful synthesis of workflows by FMs.
Additionally, the results of our implemented test-time iterative strategy demonstrate the direct
relationship between the repair iteration attempts and the performance of FMs in repairing the
defect incidences in FM-generated DSL workflows. With more attempts, the FMs repair more defect
incidences until their performance is saturated. Similarly, it can be expected that implementing the
test-time iterative strategy can also result in FMs’ higher success rate in synthesizing DSL program
instances. Finally, based on the results of our study, even increasing the synthesis attempt may
not be enough for the state-of-the-art FMs to generate a correct DSL program instance without
any defect incidences. This emphasizes the need for implementing extra mechanisms such as
static and dynamic analyses to detect any defect incidences that may have found their way into

ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
     Towards Reliable Generation of Executable Workflows by Foundation Models                                            23


           Listing 1. A possibly unreachable variable in a simplified FM-generated DSL workflow instance
1    workflow : {
2    tasks : [
3      { id : " Multiply_or_Sum_Two_Values " ,
4        if : {
5           condition : " x > 10 && y < 5 " ,
6           then : [ " p = xy " ] ,
7           else : [ " q = x + y " ] } } ,
8      { id : " Multiply_or_Divide_by_2 " ,
9        if : {
10          condition : " x < 15 && y > 0 " ,
11          then : [ " s = p /2 " ] ,
12          else : [ " t =2 q " ] } } ] }



     the synthesized DSL program instance, despite capitalizing on FMs to achieve optimal synthesis
     accuracy.

     Implication 2: Static analyzers require additional support to effectively detect all defects
     in FM-generated DSL programs.
     Our defect detection tool Timon, detects incidences of nine defect categories in FM-generated DSL
     workflows by operating two components: Structure Validator and Defect Detector (modules A
     and C in Section 4.1, respectively). The former component examines whether a FM-generated DSL
     workflow is structured as a valid JSON and whether it adheres to the specified DSL grammar. This
     component is able to detect all incidences of the relevant defects with 100% accuracy. The latter
     component uses reconstructed complex CFG of FM-generated DSL workflows and the subsequent
     use-def and def-use chains to detect the defects in workflows. In contrast to the first component’s
     perfect performance, implemented static analyses in the current component are not able to detect
     all defect incidences. Further investigation of unsuccessful detection instances reveals that similar
     to programs written in general-purpose programming languages, FM-generated DSL programs
     are also prone to infeasible program execution paths when the program involves non-linear control
     flow constructs and variables whose values are only known at runtime. These incidences pertain
     to possibly unreachable and possibly unused variables or variables with definitions and use cases
     located in occasionally inaccessible program paths.
        Consider Listing 1 as an example. In this example, investigating the runtime bounds of variables
     and their relationships is necessary to detect mutually exclusive and contradictory conditions and
     to verify the satisfiability of all possible combinations for variable values. Loops are also affected
     by runtime bounds. Only at runtime can we determine whether a loop has at least one iteration
     or its termination condition is satisfied. The same applies to incorrect data type propagation. For
     instance, if variable “v” is defined as a float and then used as an integer in a subsequent node,
     Timon only detects the incorrect data type propagation with full confidence if the variable use
     occurs on a path that is always executed. Otherwise, Timon may miss the defect. Therefore, sole
     static analysis cannot confidently detect whether any defect exists. For detecting such defect
     occurrences in general-purpose programs, dynamic analysis or Satisfiability Modulo Theories (SMT)
     solvers [49, 51, 63] are applied to investigate whether the solution space can satisfy all possible
     combinations of runtime bounds and conditions. Similarly, to accommodate the detection of such
     defects in FM-generated DSL programs, we suggest incorporating SMT solvers alongside static
     analyzers.

                                      ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
24                                                                                       Masoumzadeh et al.


Implication 3: Prompting assistance is needed to improve the capabilities of FMs in DSL
synthesis.
We develop Pumbaa to repair defect incidences in FM-generated DSL programs with the assistance
of FMs. For this purpose, we provide Pumbaa’s FM with Timon’s defect reports as direct feedback
to repair defect incidences correctly and comprehensively. As Pumbaa’s FM, we settle on GPT-4o,
a FM with complex abilities, suitable for solving intricate problems such as program synthesis,
verification, and repair [71]. Furthermore, to ensure our choice for Pumbaa’s FM, we conduct
experiments comparing the performance of GPT-4o with other FMs, demonstrating the superior
performance of GPT-4o in repairing defect incidences compared to the rest of the investigated
FMs. Additionally, we ensure to improve Pumbaa’s performance by iteratively refining its prompts
starting from carefully handcrafted versions, rewriting for clarity, adding few-shot examples, and
refactoring them based on OpenAI’s and Anthropic’s guidelines, verifying that the performance is
increased on a subset of defective samples with every enhancement. Nevertheless, Pumbaa falls
short of our initial expectations in repairing FM-generated DSL programs (see Section 4.4). We
believe that prompts are one potential area for improvement to address this marginal performance.
Despite their proven effectiveness in similar problems [2, 6], no prior research has explored how
effective the current state-of-the-practice prompting techniques are in guiding FMs in repairing
FM-generated DSL programs. Hence, we conduct a pilot exploratory investigation on using auto-
mated prompt optimization tools, specifically Anthropic Prompt Improver [5], to improve Pumbaa’s
performance. Recent advancements in these optimization tools demonstrate promising trajectories
for improving the performance of FMs in tackling complex tasks. Hence, we hypothesize that
using these optimizers can also improve the performance of the FMs in repairing FM-generated
DSL programs. However, the results of our analysis of the effectiveness of the automated prompt
optimizer are mixed, ranging from a 38.33% decrease in repair capability for skills with defective
parameters, to no change for incorrect outputs, incorrect data type propagation, and hallucinated
skills, to a 55% improvement in repairing unreachable variables and invalid DSL. Consequently, we
suggest further exploration of the benefits of incorporating different prompt optimizers, such as
DSPy Optimizer [31] and TextGrad [80], for refining the FMs’ prompts to increase their capabilities
of repairing defective FM-generated DSL programs.



Implication 4: Minimal effort is needed to extend the application of Timon and Pumbaa
to DSL languages other than WorkflowDSL.
  To further investigate the generalizability of Timon and Pumbaa to workflows generated in DSLs
other than WorkflowDSL, we compare our DSL with other popular workflow generation languages.
Specifically, we compare WorkflowDSL with GitHub Actions and the LangChain Expression
Language (LCEL) [33] to identify their similarities and differences across various aspects, including,
but not limited to, syntax and control-flow constructs.
  As can be observed from Table 5, WorkflowDSL shares close similarities with GitHub Actions
and LCEL. With the exception of the primary purpose for generating the workflows and the
base language for doing so, across all other aspects, specifically the syntax characteristics and
available control flow constructs, WorkflowDSL shares the same qualities with at least one of
the other two DSLs. This means, with the exception of Structure Validator A and Intermediate
Representation Constructor B in Timon (Section 4.1), that directly operate on JSON objects and
instantiated WorkflowDSL programs, all other modules of Timon can be generalized to detect
defect incidences across GitHub Actions and LCEL workflows.


ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
Towards Reliable Generation of Executable Workflows by Foundation Models                                             25


                    Table 5. Comparison of WorkflowDSL with GitHub Actions and LCEL

           Aspect                   WorkflowDSL                   GitHub Actions                     LCEL
Primary Purpose of Workflows   General-purpose               CI/CD pipeline automation     FM application composition
Base Language                  JSON                          YAML                          Python
Syntax Style                   Action chaining               Action chaining               Action chaining
Has Composition?               Yes                           Yes                           Yes
Has Error Handling?            Yes                           Yes                           Yes
Has Conditionals/ Branches?    Yes                           Yes                           Yes
Has Loops?                     Yes                           Yes                           No
Has Parallelism?               Yes                           Yes                           Yes
Artifacts Are Reusable?        Yes                           Yes                           Yes
Type Safety                    Schema validation, Pydantic   Schema validation             Pydantic




  Similarly for Pumbaa, with the exception of specialized instructions for repairing unparsable
JSONs and invalid DSLs, all other prompts and Pumbaa’s feedback mechanism can be applied to
repair defective GitHub Actions and LCEL workflows. In other words, we can conclude that other
than building specialized intermediate representations for GitHub Actions and LCEL workflows,
not much effort is needed to extend the application of Timon and Pumbaa to workflows from DSLs
other than WorkflowDSL.
6 Threats to the Validity
In this section, we discuss threats to validity across three categories: construct, internal, and external
validity.

6.1   Threats to Construct Validity
These threats concern whether our measurements capture the intended concepts. In the empirical
study of defects, the identified 20 defect types may still miss rare or context-specific defects.
Although we conduct extensive manual analysis, we acknowledge that the taxonomy may not be
fully exhaustive. Because this is the first systematic effort to categorize these defects, we position
the taxonomy as an initial framework that future studies can refine, expand, and validate.

6.2   Threats to Internal Validity
These threats concern factors that may influence the validity of our procedures and findings. To
build the defect taxonomy, two experts conduct an open-coding analysis. As a result, inspector
bias may influence defect labeling. To reduce this risk, the inspectors first label an initial set of
FM-generated DSL workflows independently, then meet to resolve disagreements and align their
interpretations of defect categories. Prior work reports that this process reduces examiner bias [45].
In cases where the two inspectors do not reach consensus, a third inspector makes the final decision,
following recommendations from similar studies [45, 52].
   To reduce confounding factors in repair evaluation, we assess Pumbaa for each defect type
independently. However, real-world FM-generated DSL workflows can contain multiple interacting
defects. In such cases, repairing one defect can introduce a new defect or hide another one, which can
delay or prevent detection and repair. To mitigate this issue, we apply a test-time iterative strategy
that repeatedly executes Pumbaa until all detectable defect incidences are repaired, including
incidences introduced during prior repair attempts.

                                  ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
26                                                                                       Masoumzadeh et al.


6.3    Threats to External Validity
These threats concern the generalizability of our results. To derive the taxonomy of defects in FM-
generated DSL programs, we conduct open-coding on a dataset of 65 FM-generated DSL workflow
samples. This sample may not contain all possible defect types. To mitigate this risk, we augment
observed defect categories with defect types reported in programming languages and software
engineering literature. This allows us to include categories that may not be identifiable through
manual inspection alone or without workflow execution, but are observed in related artifacts such
as FM-generated general-purpose programs and traditional DSL programs.
    From our taxonomy, only one defect type (i.e., invalid DSL) is specific to FM-generated DSL work-
flows because it captures syntax violations tied to a particular DSL grammar (i.e., WorkflowDSL).
All remaining defect types can generalize to multi-step processes that are automated using FMs.
In addition, five defect types can apply to single-task processes automated by a single FM call:
over-engineering, incorrect inputs, incorrect outputs, all sub-categories of incorrect skill usage
(i.e., incorrect skills, inefficient skills, hallucinated skills, and skills with defective parameters),
and incorrect type casting. Therefore, as long as a particular DSL grammar can be parsed and
intermediate representations (e.g., a CFG) can be constructed, Timon and Pumbaa can be adapted
to real-world industrial workflows.
    If the target DSL grammar changes, some defect types may also change. However, when building
the taxonomy, we consolidate relevant literature to include plausible defect categories, including
those that are difficult to detect through manual open coding or prior to workflow execution. Hence,
except for grammar-specific syntax violations, core defect categories are expected to remain largely
consistent across grammars. Their prevalence, however, can vary by DSL grammar.

7     Related work
In this section, we situate our work with respect to literature on DSL program and workflow
synthesis by FMs, FMs for program repair, and static analysis of DSL programs.

7.1    FM-based Synthesis of DSL Programs and Workflows
Desai et al. [19] presented a framework for constructing program synthesizers that take natu-
ral language inputs and produce expressions in a target DSL. Their approach constructs these
synthesizers using three inputs, a DSL specification, a training data set, and a words-to-token
dictionary. Ghandhi et al. [21] proposed an Office Domain-Specific Language as an FM-friendly
DSL for Office Applications, enabling FMs to accurately translate natural language user queries
into DSL programs interpretable by Office applications. The key idea is that while FMs can produce
semantically or syntactically incorrect code, a high-level, FM-friendly language can help mitigate
program synthesis errors. However, due to the inherent nature of auto-regressive language models,
the synthesized program is not guaranteed to be error-free.
   Bassamzadeh and Methani [10] studied the ability of FMs to transform natural language into
DSLs. Their experiments showed that while a fine-tuned FM scored the best on the code similarity
metric, retrieval-augmented generation with optimizations can achieve parity. However, based on
the compilation rate, they demonstrated that both settings still got the syntax wrong many times.
Similarly, Ayala et al. [7] compared the performance of fine-tuned small language models (Mistral-
Nemo-12B-Base) against propriety (OpenAI’s GPT family of models and Google’s Gemini-2.0-Flash)
and open-source (Meta’s Llama-3.3-70B-Instruct) LLMs in synthesizing low-code workflows as
structured outputs. Although fine-tuned small language models demonstrated an average 10% better
performance in such synthesis compared to directly prompting LLMs, both settings still generated
defective workflows. Barke et al. [9] evaluated the performance of FMs in solving structured

ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
Towards Reliable Generation of Executable Workflows by Foundation Models                                            27


reasoning and data transformation tasks through Program By Example (PBE), searching for a DSL
that confines the direct transformation from the input to the output of the target reasoning task
at hand. They found that even the state-of-the-art proprietary GPT-4o model performs poorly,
solving only 10% of the tasks in the Abstraction and Reasoning Corpus, a benchmark targeted
towards human-like structured reasoning tasks. To enable the FMs to synthesize such PBE DSLs
successfully, the researchers implemented a correct-by-construction approach that constrains the
models’ generation by guiding them, using a context-free language model, through the execution
of combinatorial search algorithms to find the DSL that accurately captures the input-output pair
transformations. Liu et al. [39] investigated various workflow representation schemes, ranging from
pseudocode to general-purpose scripting languages such as Python and business process languages,
including BPMN, to identify the most effective structures for interpretation by LLMs. Despite using
different representations and even introducing a complex, multi-agent, self-evolving framework to
enhance the structure of synthesized workflows, the researchers found that a number of generated
workflows are not executable. Therefore, the implementation of additional workflow-structure
validation mechanisms is required. The results of these studies align with our observation that FMs
struggle to synthesize low-resource DSL programs, underscoring the need to enforce additional
guardrails for defect detection and repair.
   Several studies [8, 76, 77, 81] proposed automatic workflow generation using FMs. A key ob-
servation from all of these approaches is that although some form of functional verification and
simulations in real-world workflow execution engines has confirmed the effectiveness of these
tools, the specifics regarding syntax errors or semantic defects in their approach remain unclear.
In [83], researchers demonstrated the effectiveness of FMs in directly synthesizing GitHub Action
Workflows. Despite being a form of DSL, these workflows are readily accessible through GitHub
open-source repositories; thus, FMs are not faced with the low-resource-language problem during
program synthesis. Furthermore, the scope of these workflows is notably narrower compared to
general-purpose workflows, focusing solely on automating the CI/CD stages of the software release
pipeline. Therefore, the success of FMs in synthesizing these workflows, in contrast to their limited
ability to generate general-purpose workflows, is expected but restricts their use in general-purpose
applications.
   Based on the limitations of prior research, we recommend a more systematic method (i.e.,
static analysis), to assess the robustness of such automated workflow generation systems. This
will enhance the confidence in employing an FM-based workflow generation system within an
enterprise environment. While prior studies focus on generating DSLs for FM-based applications,
which is very similar to our setting, our emphasis in this paper is on detailing fully automatic defect
detection and repair after the workflow generation process rather than explaining the DSL design
or workflow generation phase.


7.2   Static Analysis of DSLs
Static analysis for detecting defects is not limited to source code. Mandal et al. [44] proposed
a generic static analysis framework for DSLs used in safety-critical software, based on abstract
interpretation. Their approach uses data flow analysis and pattern-based matching techniques to
identify domain-specific errors and coding violations for control languages. Ruiz-Rube et al. [59]
proposed a model-driven interoperability strategy that enables existing source code quality analysis
methods and tools to be applied to DSL artifacts. To detect anti-patterns in data science pipelines,
Rajbahadur et al. [58] analyzed the directed acyclic graph of the pipeline representing its control
flow.


                                 ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
28                                                                                       Masoumzadeh et al.


7.3    FMs for Program Repair
FMs have been extensively used in recent studies to repair defects in general-purpose programming
languages. In particular, the field of Automated Program Repair (APR) aims to fix bugs by generating
patches. Hossein et al. [25] proposed Toggle, a program repair framework that combines a bug
localization model, an adjustment model to resolve tokenizer inconsistencies, and a bug-fixing
model. Li et al. [36] showed that parameter-efficient fine-tuning can be used to reduce computing
resource consumption without compromising performance for APR tasks. Wadhwa et al. [66]
introduced CORE, an FM-based APR tool, for generating fixing patches and ranking them, based on
human-developer behavior rubric criteria, for assisting developers in code revision and improving
code quality issues. CORE involves a duo of LLMs, the first one in charge of generating code
patches, based on a list of developer-provided recommendations for addressing the issues flagged
by a static analyzer, and the latter assigning ranks to generated patches and ordering them based
on the ranks. Batole et al. [11] proposed LOCALIZEAGENT, a multi-agent framework, specifically
designed for executing program analysis tools for localizing design issues and then ranking them
based on their relevance in large codebases. Specifically, LOCALIZEAGENT is designed around
two main limitations of FMs: one is their limited context window, which makes analyzing large
codebases infeasible, and the other is their inability to understand non-FM-friendly content, such
as non-textual modality outputs from program analysis tools.
   The code in the existing APR benchmarks may have been included in the training data of existing
LLMs, making these language models suffer from the threat of “data leakage”, which in turn leads
them to demonstrate misleading optimistic performance metrics on the APR benchmark tasks. Wu
et al. [73] introduced ConDefects, a complimentary dataset developed on top of existing ones to
eliminate the possibility of overlap between existing APR datasets and the training data of LLMs.
This dataset contains 1, 254 Java faulty programs and 1, 625 Python faulty programs, all of which
are sourced from the online competition platform AtCoder.
   Chen et al. [16] investigated the performance of popular LLMs in handling repository-level
repair tasks. They proposed RepoBugs, a benchmark comprising 124 repository-level bugs from
open-source repositories. They then used GPT-3.5 to attempt to tackle their newly introduced
benchmark tasks. Using a function locating the errors, the repair rate of the used LLM on RepoBugs
is measured to be only 22.58%, considerably diverging from the performance of the same model on
function-level bugs as reported in related studies.
   To standardize the evaluation of APR approaches, Ouyang et al. [55] conducted a multidimen-
sional evaluation of nine learning-based and three traditional state-of-the-art APR techniques under
the same environment and settings. They employed Defects4J benchmark and a newly constructed
benchmark named MuBench, containing 1, 700 artificial bugs generated by mutating bugs in De-
fects4J. Furthermore, they highlighted the importance of using multi-dimensional metrics, including
comparability, plausibility, genuineness, syntactic equivalence, and trivial compiler equivalence
metrics. They observed that the LLM-based APR, AlphaRepair [75], can correctly fix the largest
number of bugs and demonstrates better adaptability and generalizability concerning overfitting
issues. While using FMs to repair general-purpose programming languages is common, the effec-
tiveness of applying FMs to repair DSL programs has not been explored, which we addressed in
this work.

8     Conclusion and Future Work
In this work, our goal is to improve the reliability and robustness of FM-generated DSL workflows.
Prior studies have demonstrated that relying solely on the generative capabilities of FMs, even
proprietary ones with a considerable number of learnable parameters and complex architectures, is

ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
Towards Reliable Generation of Executable Workflows by Foundation Models                                                29


insufficient to directly synthesize such workflows without defects. This, in turn, underscores the
need to implement additional guardrails to detect and repair defects in generated workflows.
   Although prior research examined the bugs introduced by FMs during code generation and
code translation, the defects generated by FMs during NL-2-DSL translation, such as synthesizing
workflows by FMs, have yet to be investigated.
   Hence, we start by conducting a manual analysis of FM-generated DSL workflows, open-coding
them for the types and prevalence of their defect incidences. Based on our findings, we introduce an
initial taxonomy of defect types within these DSL workflows, applicable not only to FM-generated
DSL workflows, but to any processes automatable using FMs, which may involve multiple dependent
steps or even be comprised of a single task. Our open-coding analysis identifies a high prevalence
of defect incidences across FM-generated DSL workflows, with 89.23% of them containing at least
one defect incident, which aligns with the prior studies demonstrating the inability of even the
most powerful FMs to directly synthesize non-defective workflows. Given the magnitude of the
problem and the necessity of addressing it, as the next step, we propose the application of static
analysis in FM-generated DSL program instances for detecting defects which may have found
their way into the synthesized programs, in spite of controlling the FMs to achieve the maximum
synthesis accuracy. Finally, we propose incorporating the results report of the static analyzer
as a direct feedback mechanism in a FM-based correction module, to iteratively repair detected
defect incidences. Our study verifies the limited capabilities of FMs in directly generating DSL
program instances without any defects even when the programs are synthesized iteratively through
implementing the test-time iterative strategy. The results of our study embody the initial steps
toward validating and repairing these programs with the assistance of established program analysis
techniques.
Future Work. We plan to further improve the detection performance of Timon by incorporating
dynamic analyses and SMT solvers, such as Z3 Theorem Prover [49], to precisely pinpoint defect
incidences arising due to erroneous, complex control flow structures and infeasible program paths in
FM-generated DSL workflows, which are only detectable at runtime. Despite Pumbaa’s lower than
expected accuracy in repairing incidences of some particular defect types, its varying performance
across other defect categories, which even maximizes as 100% accuracy for repairing incorrect
outputs and hallucinated skills, is a key finding for guiding the future research in how to benefit from
FMs’ capabilities for repairing program defects. Specifically, we plan to systematically explore the
benefits of incorporating different prompt optimization techniques to increase the effectiveness of
Pumbaa’s prompts, dynamically tailoring them towards each defect category and the FMs’ respective
abilities in repairing each specific defect type. Furthermore, we aim to provide more relevant context
and more appropriate examples of each defect category to Pumbaa by using retrieval-augmented
generation techniques [35]. Finally, similar to general-purpose programming languages, we aim
to use static analyzers not only for detecting defects in FM-generated DSL programs, but also for
detecting any potential incidences of security vulnerabilities [38], performance bottlenecks, and
other anti-patterns [57] in them. Our efforts will contribute to achieving robust FM-powered DSL
programs, enabling reliable workflow synthesis and execution in enterprise settings.

References
 [1] Zahra Abbasiantaeb, Yifei Yuan, Evangelos Kanoulas, and Mohammad Aliannejadi. 2024. Let the llms talk: Simulating
     human-to-human conversational qa via zero-shot llm-to-llm interactions. In Proceedings of the 17th ACM International
     Conference on Web Search and Data Mining. Association for Computing Machinery, New York, NY, USA, 8–17.
 [2] Toufique Ahmed and Premkumar Devanbu. 2022. Few-shot training llms for project-specific code-summarization. In
     Proceedings of the 37th IEEE/ACM international conference on automated software engineering. Association for Computing
     Machinery, New York, NY, USA, 1–5.
 [3] Frances E Allen. 1970. Control flow analysis. ACM Sigplan Notices 5, 7 (1970), 1–19.

                                    ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
30                                                                                                     Masoumzadeh et al.


 [4] Anthropic. 2024. Prompt Engineering Overview. https://docs.anthropic.com/en/docs/build-with-claude/prompt-
     engineering/overview Accessed: 2025-06-29.
 [5] Anthropic. 2025. Use our prompt improver to optimize your prompts. https://docs.anthropic.com/en/docs/build-with-
     claude/prompt-engineering/prompt-improver Accessed: 2025-03-14.
 [6] Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski, David Dohan, Ellen Jiang, Carrie
     Cai, Michael Terry, Quoc Le, et al. 2021. Program synthesis with large language models. arXiv preprint arXiv:2108.07732.
 [7] Orlando Marquez Ayala, Patrice Bechard, Emily Chen, Maggie Baird, and Jingfei Chen. 2025. Fine-Tune an SLM or
     Prompt an LLM? The Case of Generating Low-Code Workflows. arXiv preprint arXiv:2505.24189.
 [8] Orlando Marquez Ayala and Patrice Béchard. 2024. Generating a Low-code Complete Workflow via Task Decomposition
     and RAG. https://doi.org/10.48550/ARXIV.2412.00239
 [9] Shraddha Barke, Emmanuel Anaya Gonzalez, Saketh Ram Kasibatla, Taylor Berg-Kirkpatrick, and Nadia Polikarpova.
     2024. Hysynth: Context-free llm approximation for guiding program synthesis. Advances in Neural Information
     Processing Systems 37 (2024), 15612–15645.
[10] Nastaran Bassamzadeh and Chhaya Methani. 2024. A Comparative Study of DSL Code Generation: Fine-Tuning vs.
     Optimized Retrieval Augmentation. https://doi.org/10.48550/ARXIV.2407.02742
[11] Fraol Batole, David OBrien, Tien N Nguyen, Robert Dyer, and Hridesh Rajan. 2025. An LLM-Based Agent-Oriented
     Approach for Automated Code Design Issue Localization. In 2025 IEEE/ACM 47th International Conference on Software
     Engineering (ICSE). IEEE Computer Society, IEEE Press, 637–637.
[12] Nathan Benaich and Ian Hogarth. 2024. State of AI report. https://www.stateof.ai/
[13] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D. Kaplan, Prafulla Dhariwal, Arvind Neelakantan,
     Pranav Shyam, Girish Sastry, Amanda Askell, et al. 2020. Language Models are Few-Shot Learners. Advances in
     Neural Information Processing Systems (NeurIPS) 33 (2020), 1877–1901. https://doi.org/10.48550/arXiv.2005.14165
     arXiv:2005.14165 [cs.CL]
[14] Mark Chen, Jerry Tworek, Henry Jun, Qiming Yuan, Henrique P. de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri
     Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heewoo Jun, Prafulla
     Dhariwal, Matthew Knight, Benjamin Chess, John Schulman, Jakob Pachocki, Shen Li, Pawel Klimov, Miljan Martic,
     Long Ouyang, Neel Alex, Ryan Teehan, Xu Jiang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders,
     Christopher Hesse, Andrew N. Gomez, Tobias Unterthiner, Filip Pavlov, Jeff Clune, and Wojciech Zaremba. 2021.
     Evaluating Large Language Models Trained on Code. https://arxiv.org/abs/2107.03374
[15] Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny Zhou. 2024. Teaching Large Language Models to Self-
     Debug. In The Twelfth International Conference on Learning Representations (ICLR). https://openreview.net/forum?id=
     KuPixIqPiq
[16] Yuxiao Chen, Jingzheng Wu, Xiang Ling, Changjiang Li, Zhiqing Rui, Tianyue Luo, and Yanjun Wu. 2024. When Large
     Language Models Confront Repository-Level Automatic Program Repair: How Well They Done?. In Proceedings of the
     2024 IEEE/ACM 46th International Conference on Software Engineering: Companion Proceedings (ICSE-Companion ’24).
     ACM, 459–471. https://doi.org/10.1145/3639478.3647633
[17] Jacob Cohen. 1960. A coefficient of agreement for nominal scales. Educational & psychological measurement 20, 1
     (1960).
[18] Samuel Colvin. 2024. Pydantic: Data validation and settings management using Python type annotations. https:
     //docs.pydantic.dev/latest/ Accessed: March 8, 2025.
[19] Aditya Desai, Sumit Gulwani, Vineet Hingorani, Nidhi Jain, Amey Karkare, Mark Marron, Sailesh R, and Subhajit
     Roy. 2016. Program synthesis using natural language. In Proceedings of the 38th International Conference on Software
     Engineering (ICSE ’16). ACM, 345–356. https://doi.org/10.1145/2884781.2884786
[20] Keheliya Gallaba, Ali Arabat, Dayi Lin, Mohammed Sayagh, and Ahmed E Hassan. 2025. Towards Conversational
     Development Environments: Using Theory-of-Mind and Multi-Agent Architectures for Requirements Refinement.
     arXiv preprint arXiv:2505.20973.
[21] Apurva Gandhi, Thong Q. Nguyen, Huitian Jiao, Robert Steen, and Ameya Bhatawdekar. 2023. Natural Language
     Commanding via Program Synthesis. https://doi.org/10.48550/ARXIV.2306.03460
[22] Yingqiang Ge, Wenyue Hua, Kai Mei, jianchao ji, Juntao Tan, Shuyuan Xu, Zelong Li, and Yongfeng Zhang. 2023.
     OpenAGI: When LLM Meets Domain Experts. In Advances in Neural Information Processing Systems, Vol. 36. 5539–5568.
[23] Zhibin Gou, Zhihong Shao, Yeyun Gong, yelong shen, Yujiu Yang, Nan Duan, and Weizhu Chen. 2024. CRITIC:
     Large Language Models Can Self-Correct with Tool-Interactive Critiquing. In The Twelfth International Conference on
     Learning Representations (ICLR). https://openreview.net/forum?id=Sx038qxjek
[24] Ahmed E Hassan, Gustavo A Oliva, Dayi Lin, Boyuan Chen, Zhen Ming, et al. 2024. Rethinking software engineering
     in the foundation model era: From task-driven AI copilots to goal-driven AI pair programmers. arXiv preprint
     arXiv:2404.10225.



ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
Towards Reliable Generation of Executable Workflows by Foundation Models                                                 31


[25] Soneya Binta Hossain, Nan Jiang, Qiang Zhou, Xiaopeng Li, Wen-Hao Chiang, Yingjun Lyu, Hoan Nguyen, and Omer
     Tripp. 2024. A Deep Dive into Large Language Models for Automated Bug Localization and Repair. Proceedings of the
     ACM on Software Engineering 1, FSE (July 2024), 1471–1493. https://doi.org/10.1145/3660773
[26] Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, and Denny Zhou.
     2023. Large language models cannot self-correct reasoning yet. arXiv preprint arXiv:2310.01798.
[27] Andrzej Jasinski, Yuansong Qiao, Enda Fallon, and Ronan Flynn. 2022. Natural language processing applied to dynamic
     workflow generation for network management. In NOMS 2022-2022 IEEE/IFIP Network Operations and Management
     Symposium. IEEE, 1–6.
[28] Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii, Ye Jin Bang, Andrea Madotto, and
     Pascale Fung. 2023. Survey of Hallucination in Natural Language Generation. Comput. Surveys 55, 12 (March 2023),
     1–38. https://doi.org/10.1145/3571730
[29] Sathvik Joel, Jie JW Wu, and Fatemeh H Fard. 2024. A survey on llm-based code generation for low-resource and
     domain-specific programming languages. arXiv preprint arXiv:2410.03981.
[30] Gaurav Kamath, Sebastian Schuster, Sowmya Vajjala, and Siva Reddy. 2024. Scope ambiguities in large language
     models. Transactions of the Association for Computational Linguistics 12 (2024), 738–754.
[31] Omar Khattab, Arnav Singhvi, Paridhi Maheshwari, Zhiyuan Zhang, Keshav Santhanam, Sri Vardhamanan, Saiful Haq,
     Ashutosh Sharma, Thomas T. Joshi, Hanna Moazam, Heather Miller, Matei Zaharia, and Christopher Potts. 2024. DSPy:
     Compiling Declarative Language Model Calls into Self-Improving Pipelines. The Twelfth International Conference on
     Learning Representations.
[32] Geunwoo Kim, Pierre Baldi, and Stephen McAleer. 2023. Language models can solve computer tasks. Advances in
     Neural Information Processing Systems 36 (2023), 39648–39677.
[33] LangChain. 2025. LangChain Expression Language (LCEL). https://python.langchain.com/docs/concepts/lcel/
     Accessed 18-07-2025.
[34] Hung Le, Yue Wang, Akhilesh Deepak Gotmare, Silvio Savarese, and Steven C.H. Hoi. 2022. CodeRL: Mastering Code
     Generation Through Pretrained Models and Deep Reinforcement Learning. In Proceedings of the 36th International
     Conference on Neural Information Processing Systems (NIPS ’22). Article 1549, 15 pages.
[35] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler,
     Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, and Douwe Kiela. 2020. Retrieval-augmented generation
     for knowledge-intensive NLP tasks. In Proceedings of the 34th International Conference on Neural Information Processing
     Systems.
[36] Guochang Li, Chen Zhi, Jialiang Chen, Junxiao Han, and Shuiguang Deng. 2024. Exploring Parameter-Efficient
     Fine-Tuning of Large Language Model on Automated Program Repair. In Proceedings of the 39th IEEE/ACM International
     Conference on Automated Software Engineering (ASE ’24). ACM, 719–731. https://doi.org/10.1145/3691620.3695066
[37] Xiaoyuan Li, Wenjie Wang, Moxin Li, Junrong Guo, Yang Zhang, and Fuli Feng. 2024. Evaluating Mathematical
     Reasoning of Large Language Models: A Focus on Error Identification and Correction. In Findings of the Association for
     Computational Linguistics: ACL 2024. 11316–11360.
[38] Stephan Lipp, Sebastian Banescu, and Alexander Pretschner. 2022. An empirical study on the effectiveness of static C
     code analyzers for vulnerability detection. In Proceedings of the 31st ACM SIGSOFT international symposium on software
     testing and analysis. 544–555.
[39] Siwei Liu, Jinyuan Fang, Han Zhou, Yingxu Wang, and Zaiqiao Meng. 2025. SEW: Self-Evolving Agentic Workflows
     for Automated Code Generation. arXiv preprint arXiv:2505.18646 (2025).
[40] Anton Lozhkov, Raymond Li, Loubna Ben Allal, Federico Cassano, Joel Lamy-Poirier, Nouamane Tazi, Ao Tang, Dmytro
     Pykhtar, Jiawei Liu, Yuxiang Wei, Tianyang Liu, Max Tian, Denis Kocetkov, Arthur Zucker, Younes Belkada, Zijian
     Wang, Qian Liu, Dmitry Abulkhanov, Indraneil Paul, Zhuang Li, Wen-Ding Li, Megan Risdal, Jia Li, Jian Zhu, Terry Yue
     Zhuo, Evgenii Zheltonozhskii, Nii Osae Osae Dade, Wenhao Yu, Lucas Krauß, Naman Jain, Yixuan Su, Xuanli He,
     Manan Dey, Edoardo Abati, Yekun Chai, Niklas Muennighoff, Xiangru Tang, Muhtasham Oblokulov, Christopher Akiki,
     Marc Marone, Chenghao Mou, Mayank Mishra, Alex Gu, Binyuan Hui, Tri Dao, Armel Zebaze, Olivier Dehaene, Nicolas
     Patry, Canwen Xu, Julian McAuley, Han Hu, Torsten Scholak, Sebastien Paquet, Jennifer Robinson, Carolyn Jane
     Anderson, Nicolas Chapados, Mostofa Patwary, Nima Tajbakhsh, Yacine Jernite, Carlos Muñoz Ferrandis, Lingming
     Zhang, Sean Hughes, Thomas Wolf, Arjun Guha, Leandro von Werra, and Harm de Vries. 2024. StarCoder 2 and The
     Stack v2: The Next Generation. https://doi.org/10.48550/ARXIV.2402.19173
[41] Ziyang Luo, Can Xu, Pu Zhao, Qingfeng Sun, Xiubo Geng, Wenxiang Hu, Chongyang Tao, Jing Ma, Qingwei Lin,
     and Daxin Jiang. 2023. WizardCoder: Empowering Code Large Language Models with Evol-Instruct. arXiv preprint
     arXiv:2306.08568 (2023).
[42] Zhicun Lyu, Xinye Li, Zheng Xie, and Ming Li. 2025. Top Pass: Improve Code Generation by Pass@ k-maximized
     Code Ranking. Frontiers of Computer Science 19, 8 (2025), 198341.



                                    ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
32                                                                                                    Masoumzadeh et al.


[43] Kaixin Ma, Hao Cheng, Yu Zhang, Xiaodong Liu, Eric Nyberg, and Jianfeng Gao. 2023. Chain-of-Skills: A Configurable
     Model for Open-Domain Question Answering. In Proceedings of the 61st Annual Meeting of the Association for Compu-
     tational Linguistics (Volume 1: Long Papers). Association for Computational Linguistics, Toronto, Canada, 1599–1618.
     https://doi.org/10.18653/v1/2023.acl-long.89
[44] Avijit Mandal, Devina Mohan, Raoul Jetley, Sreeja Nair, and Meenakshi D’Souza. 2018. A Generic Static Analysis
     Framework for Domain-specific Languages. In 2018 IEEE 23rd International Conference on Emerging Technologies and
     Factory Automation (ETFA). IEEE, 27–34. https://doi.org/10.1109/etfa.2018.8502576
[45] Sogol Masoumzadeh, Nuno Saavedra, Rungroj Maipradit, Lili Wei, João F Ferreira, Dániel Varró, and Shane McIntosh.
     2025. Do Experts Agree About Smelly Infrastructure? IEEE Transactions on Software Engineering (2025).
[46] Mary L McHugh. 2012. Interrater reliability: the kappa statistic. Biochemia Medica 22 (2012), 276–282. https:
     //api.semanticscholar.org/CorpusID:5421278
[47] MCP. 2024. Introduction to Model Context Protocol. https://modelcontextprotocol.io/introduction Accessed:
     2025-03-13.
[48] Microsoft. 2025. Generative AI Scripting. https://microsoft.github.io/genaiscript/ Accessed 18-07-2025.
[49] Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An Efficient SMT Solver. In Proceedings of the 14th International
     Conference on Tools and Algorithms for the Construction and Analysis of Systems (TACAS). Springer, 337–340. https:
     //doi.org/10.1007/978-3-540-78800-3_24
[50] Fangwen Mu, Lin Shi, Song Wang, Zhuohao Yu, Binquan Zhang, ChenXue Wang, Shichao Liu, and Qing Wang. 2024.
     Clarifygpt: A framework for enhancing llm-based code generation via requirements clarification. Proceedings of the
     ACM on Software Engineering 1, FSE (2024), 2332–2354.
[51] Hoang Duong Thien Nguyen, Dawei Qi, Abhik Roychoudhury, and Satish Chandra. 2013. SemFix: Program Repair via
     Semantic Analysis. In Proceedings of the 35th International Conference on Software Engineering (ICSE). IEEE, 772–781.
     https://doi.org/10.1109/ICSE.2013.6606613
[52] Roberto Oliveira, Rafael de Mello, Eduardo Fernandes, Alessandro Garcia, and Carlos Lucena. 2020. Collaborative or
     individual identification of code smells? On the effectiveness of novice and professional developers. Information and
     Software Technology 120 (2020).
[53] OpenAI. 2024. Text Generation and Prompting. https://platform.openai.com/docs/guides/text?api-mode=responses
     Accessed: 2025-06-29.
[54] OpenAI. 2025. Pricing. https://platform.openai.com/docs/pricing. Accessed: 2026-01-10.
[55] Yicheng Ouyang, Jun Yang, and Lingming Zhang. 2024. Benchmarking Automated Program Repair: An Extensive
     Study on Both Real-World and Artificial Bugs. In Proceedings of the 33rd ACM SIGSOFT International Symposium on
     Software Testing and Analysis (ISSTA ’24). ACM, 440–452. https://doi.org/10.1145/3650212.3652140
[56] Rangeet Pan, Ali Reza Ibrahimzada, Rahul Krishna, Divya Sankar, Lambert Pouguem Wassi, Michele Merler, Boris
     Sobolev, Raju Pavuluri, Saurabh Sinha, and Reyhaneh Jabbarvand. 2024. Lost in Translation: A Study of Bugs Introduced
     by Large Language Models while Translating Code. In Proceedings of the IEEE/ACM 46th International Conference on
     Software Engineering (ICSE ’24). ACM, 1–13. https://doi.org/10.1145/3597503.3639226
[57] José Pereira dos Reis, Fernando Brito e Abreu, Glauco de Figueiredo Carneiro, and Craig Anslow. 2022. Code smells
     detection and visualization: a systematic literature review. Archives of Computational Methods in Engineering 29, 1
     (2022), 47–94.
[58] Gopi Krishnan Rajbahadur, Gustavo Ansaldi Oliva, Ahmed E. Hassan, and Juergen Dingel. 2019. Pitfalls Analyzer:
     Quality Control for Model-Driven Data Science Pipelines. In 2019 ACM/IEEE 22nd International Conference on Model
     Driven Engineering Languages and Systems (MODELS). IEEE, 12–22. https://doi.org/10.1109/models.2019.00-19
[59] Iván Ruiz-Rube, Tatiana Person, Juan Manuel Dodero, José Miguel Mota, and Javier Merchán Sánchez-Jara. 2019.
     Applying static code analysis for domain-specific languages. Software and Systems Modeling 19, 1 (April 2019), 95–110.
     https://doi.org/10.1007/s10270-019-00729-w
[60] Nick Russell, Wil Mp Van Der Aalst, and Arthur HM Ter Hofstede. 2016. Workflow patterns: the definitive guide. Mit
     Press.
[61] Freda Shi, Xinyun Chen, Kanishka Misra, Nathan Scales, David Dohan, Ed Chi, Nathanael Schärli, and Denny Zhou.
     2023. Large language models can be easily distracted by irrelevant context. In Proceedings of the 40th International
     Conference on Machine Learning (Honolulu, Hawaii, USA) (ICML’23). JMLR.org, Article 1291, 18 pages.
[62] Connor Shorten, Charles Pierse, Thomas Benjamin Smith, Erika Cardenas, Akanksha Sharma, John Trengrove, and
     Bob van Luijt. 2024. StructuredRAG: JSON Response Formatting with Large Language Models. arXiv preprint
     arXiv:2408.11061.
[63] Saurabh Srivastava, Sumit Gulwani, and Jeffrey S Foster. 2010. From program verification to program synthesis. In
     Proceedings of the 37th annual ACM SIGPLAN-SIGACT symposium on Principles of programming languages. 313–326.
[64] Zhihang Sun, Hongyu Fan, and Fei He. 2022. Consistency-preserving propagation for SMT solving of concurrent
     program verification. Proc. ACM Program. Lang. 6, OOPSLA2, Article 158 (Oct. 2022), 28 pages. https://doi.org/10.


ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
Towards Reliable Generation of Executable Workflows by Foundation Models                                              33


     1145/3563321
[65] Francesco Vinci and Massimiliano de Leoni. 2024. Repairing Process Models Through Simulation and Explainable AI.
     In International Conference on Business Process Management. Springer, 129–145.
[66] Nalin Wadhwa, Jui Pradhan, Atharv Sonwane, Surya Prakash Sahu, Nagarajan Natarajan, Aditya Kanade, Suresh
     Parthasarathy, and Sriram Rajamani. 2024. Core: Resolving code quality issues using llms. Proceedings of the ACM on
     Software Engineering 1, FSE (2024), 789–811.
[67] Ruiyi Wang, Haofei Yu, Wenxin Zhang, Zhengyang Qi, Maarten Sap, Yonatan Bisk, Graham Neubig, and Hao Zhu. 2024.
     SOTOPIA-𝜋 : Interactive Learning of Socially Intelligent Language Agents. In Proceedings of the 62nd Annual Meeting
     of the Association for Computational Linguistics (Volume 1: Long Papers). Association for Computational Linguistics,
     12912–12940. https://doi.org/10.18653/v1/2024.acl-long.698
[68] Xingyao Wang, Boxuan Li, Yufan Song, Frank F. Xu, Xiangru Tang, Mingchen Zhuge, Jiayi Pan, Yueqi Song, Bowen Li,
     Jaskirat Singh, Hoang H. Tran, Fuqiang Li, Ren Ma, Mingzhang Zheng, Bill Qian, Yanjun Shao, Niklas Muennighoff,
     Yizhe Zhang, Binyuan Hui, Junyang Lin, Robert Brennan, Hao Peng, Heng Ji, and Graham Neubig. 2025. OpenHands:
     An Open Platform for AI Software Developers as Generalist Agents. In The Thirteenth International Conference on
     Learning Representations. https://openreview.net/forum?id=OJd3ayDDoF
[69] Zhijie Wang, Zijie Zhou, Da Song, Yuheng Huang, Shengmai Chen, Lei Ma, and Tianyi Zhang. 2024. Where Do Large
     Language Models Fail When Generating Code? arXiv preprint arXiv:2406.08731.
[70] Yuxiang Wei, Zhe Wang, Jiawei Liu, Yifeng Ding, and Lingming Zhang. 2024. Magicoder: Empowering Code Generation
     with OSS-Instruct. In Proceedings of the 41st International Conference on Machine Learning (Proceedings of Machine
     Learning Research, Vol. 235). PMLR, 52632–52657. https://proceedings.mlr.press/v235/wei24h.html
[71] Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu, Shengchao Qin, Mengda He, Haokun Li, Shing-Chi Cheung, and Cong
     Tian. 2024. Enchanting program specification synthesis by large language models using static analysis and program
     verification. In International Conference on Computer Aided Verification. Springer, 302–328.
[72] Jie Jw Wu and Fatemeh H. Fard. 2025. HumanEvalComm: Benchmarking the Communication Competence of Code
     Generation for LLMs and LLM Agent. ACM Transactions on Software Engineering and Methodology (Jan. 2025).
     https://doi.org/10.1145/3715109
[73] Yonghao Wu, Zheng Li, Jie M. Zhang, and Yong Liu. 2024. ConDefects: A Complementary Dataset to Address
     the Data Leakage Concern for LLM-Based Fault Localization and Program Repair. In Companion Proceedings of the
     32nd ACM International Conference on the Foundations of Software Engineering (FSE ’24). ACM, 642–646. https:
     //doi.org/10.1145/3663529.3663815
[74] Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, and Lingming Zhang. 2024. Agentless: Demystifying llm-based software
     engineering agents. arXiv preprint arXiv:2407.01489.
[75] Chunqiu Steven Xia and Lingming Zhang. 2022. Less training, more repairing please: revisiting automated program
     repair via zero-shot learning. In Proceedings of the 30th ACM Joint European Software Engineering Conference and
     Symposium on the Foundations of Software Engineering (ESEC/FSE ’22). ACM, 959–971. https://doi.org/10.1145/3540250.
     3549101
[76] Jia Xu, Weilin Du, Xiao Liu, and Xuejun Li. 2024. LLM4Workflow: An LLM-based Automated Workflow Model
     Generation Tool. In Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering
     (ASE ’24). ACM, 2394–2398. https://doi.org/10.1145/3691620.3695360
[77] Shuyuan Xu, Zelong Li, Kai Mei, and Yongfeng Zhang. 2024. AIOS Compiler: LLM as Interpreter for Natural Language
     Programming and Flow Programming of AI Agents. https://doi.org/10.48550/ARXIV.2405.06907
[78] Jifeng Xuan, Matias Martinez, Favio Demarco, Maxime Clement, Sebastian Lamelas Marcote, Thomas Durieux, Daniel
     Le Berre, and Martin Monperrus. 2016. Nopol: Automatic repair of conditional statement bugs in java programs. IEEE
     Transactions on Software Engineering 43, 1 (2016), 34–55.
[79] John Yang, Carlos E Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik R Narasimhan, and Ofir Press.
     2024. SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering. In The Thirty-eighth Annual
     Conference on Neural Information Processing Systems. https://arxiv.org/abs/2405.15793
[80] Mert Yuksekgonul, Federico Bianchi, Joseph Boen, Sheng Liu, Zhi Huang, Carlos Guestrin, and James Zou. 2024.
     TextGrad: Automatic "Differentiation" via Text. (2024). arXiv:2406.07496
[81] Zhen Zeng, William Watson, Nicole Cho, Saba Rahimi, Shayleen Reynolds, Tucker Balch, and Manuela Veloso. 2023.
     FlowMind: Automatic Workflow Generation with LLMs. In 4th ACM International Conference on AI in Finance (ICAIF
     ’23). ACM, 73–81. https://doi.org/10.1145/3604237.3626908
[82] Jiahao Zhang, Haiyang Zhang, Dongmei Zhang, Yong Liu, and Shen Huang. 2024. End-to-End Beam Retrieval for
     Multi-Hop Question Answering. In 2024 Annual Conference of the North American Chapter of the Association for
     Computational Linguistics. https://arxiv.org/abs/2308.08973
[83] Xinyu Zhang, Siddharth Muralee, Sourag Cherupattamoolayil, and Aravind Machiry. 2024. On the Effectiveness of
     Large Language Models for GitHub Workflows. In Proceedings of the 19th International Conference on Availability,


                                   ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
34                                                                                                Masoumzadeh et al.


     Reliability and Security (ARES ’24). Association for Computing Machinery, New York, NY, USA, Article 32, 14 pages.
     https://doi.org/10.1145/3664476.3664497




ACM Trans. Softw. Eng. Methodol., Vol. , No. , Article . Publication date: March 2026.
