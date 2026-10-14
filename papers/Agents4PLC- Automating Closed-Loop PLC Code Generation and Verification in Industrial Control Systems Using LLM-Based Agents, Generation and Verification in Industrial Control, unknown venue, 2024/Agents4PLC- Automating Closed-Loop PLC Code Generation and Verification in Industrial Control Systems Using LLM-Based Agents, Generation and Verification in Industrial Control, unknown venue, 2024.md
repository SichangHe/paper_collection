                                            Agents4PLC: Automating Closed-loop PLC Code
                                            Generation and Verification in Industrial Control
                                                   Systems using LLM-based Agents
                                                 Zihan Liu*                 Ruinan Zeng*              Dongxia WangB               Gengyun Peng                 Jingyi Wang
                                             Zhejiang University         Zhejiang University          Zhejiang University        Zhejiang University       Zhejiang University
                                            zihanliu@zju.edu.cn        zengruinan@zju.edu.cn         dxwang@zju.edu.cn         pgengyun@zju.edu.cn        wangjyee@zju.edu.cn

                                                Qiang Liu                                 Peiyu Liu                                   Wenhai WangB
arXiv:2410.14209v2 [cs.SE] 25 Dec 2024




                                           Zhejiang University                        Zhejiang University                    UWin Tech & Zhejiang University
                                         22460396@zju.edu.cn                        liupeiyu@zju.edu.cn                           zdzzlab@zju.edu.cn




                                            Abstract—In industrial control systems, the generation and           transportation [24]. Among others, ST language, as a text-
                                         verification of Programmable Logic Controller (PLC) code are            based language, is most similar to other popular high-level
                                         critical for ensuring operational efficiency and safety. While          languages (in terms of syntax and program structure) and is
                                         Large Language Models (LLMs) have made strides in automated
                                         code generation, they often fall short in providing correctness         thus suitable for code generation.
                                         guarantees and specialized support for PLC programming. To                 In ICSs, automatic generation of control code can greatly
                                         address these challenges, this paper introduces Agents4PLC, a           reduce repetitive tasks, significantly enhancing engineers’
                                         novel framework that not only automates PLC code generation             productivity. With the rapid advancement of large language
                                         but also includes code-level verification through an LLM-based          models (LLMs), automatic code generation has gained much
                                         multi-agent system. We first establish a comprehensive bench-
                                         mark for verifiable PLC code generation area, transitioning from        attention across various programming languages (e.g., C [55],
                                         natural language requirements to human-written-verified formal          C++ [10], Python [56], Java [11], etc) due to its potential to
                                         specifications and reference PLC code. We further enhance our           automate software development and reduce costs. It is thus
                                         ‘agents’ specifically for industrial control systems by incorporat-     desirable to explore LLM-based automated code generation
                                         ing Retrieval-Augmented Generation (RAG), advanced prompt               methods for industrial control code development.
                                         engineering techniques, and Chain-of-Thought strategies. Eval-
                                         uation against the benchmark demonstrates that Agents4PLC                  Emerging LLMs for code generation (a.k.a. code LLMs),
                                         significantly outperforms previous methods, achieving superior          such as Openai Codex [9], AlphaCode [33], CodeLlama [42],
                                         results across a series of increasingly rigorous metrics. This          may not be ideal for PLC code generation due to the fol-
                                         research not only addresses the critical challenges in PLC              lowing critical reasons. Firstly, these code LLMs may excel
                                         programming but also highlights the potential of our framework          at generating code in mainstream high-level languages such
                                         to generate verifiable code applicable to real-world industrial
                                         applications.                                                           as C or Python, but mostly perform poorly for industrial
                                            Index Terms—Code Generation, Code Validation, PLC Code,              control code. Indeed, it is notoriously challenging to collect
                                         LLM-based Agents, Multi Agents, Industrial Control System               sufficient data for fine-tuning a specialized model for industrial
                                                                                                                 code due to the proprietary and specialized nature of PLC
                                                                I. I NTRODUCTION                                 code. Secondly, as the control code is used to manage the
                                                                                                                 operation of industrial sectors, it is of vital importance to
                                            Programmable Logic Controllers (PLCs) are essential com-
                                                                                                                 guarantee their functional correctness, which is far more
                                         ponents of Industrial Control Systems (ICSs), playing a crucial
                                                                                                                 challenging than generating executable code. There exist some
                                         role in industrial automation and management of key industrial
                                                                                                                 efforts towards achieving specialized PLC code generation,
                                         processes. The global PLC market is projected to reach USD
                                                                                                                 such as LLM4PLC [14] and the work of Koziolek [27] either
                                         12.20 billion by 2024, with a compound annual growth rate
                                                                                                                 by finetuning or Retrieval-Augmented Generation (RAG) en-
                                         (CAGR) of 4.37% from 2024 to 2029 [36], [48]. This growth
                                                                                                                 hancements. LLM4PLC [14] also incorporates workflows for
                                         is largely driven by the increasing reliance on industrial control
                                                                                                                 syntax and functional verification at the design-level beyond
                                         programming languages based on IEC 61131-3 standard [20],
                                                                                                                 code generation to improve the code quality. However, the
                                         such as Structured Text (ST) and Function Block Diagram
                                                                                                                 correctness of specifications is only verified at the design
                                         (FBD), to oversee and regulate critical infrastructure systems
                                                                                                                 level while the correctness of the LLM-generated code remains
                                         across key sectors like energy [51], manufacturing [43], and
                                                                                                                 questionable. Moreover, their model-centred architecture lacks
                                           Co-first authors: Zihan Liu and Ruinan Zeng; Corresponding authors:   agility in integrating the whole development pipeline to
                                         Dongxia Wang and Wenhai Wang                                            achieve full automation. On the other hand, there is a growing
trend in automated LLM-based development workflows aimed                 control of mechanical equipment and production processes.
to further refine or validate code generated by LLMs using a             PLCs are widely utilized in manufacturing, transportation,
multi-agent system architecture. For instance, ChatDev [39]              energy, and other sectors due to their high reliability, ease
and MapCoder [22] implement software development systems                 of programming, and scalability. The IEC 61131-3 standard
composed of multiple intelligent agents, each with distinct              [20] specifies five standard programming languages for PLCs,
roles and tasks, with the goal of generating high-quality                which include three graphical languages: Ladder Diagram
code in a closed-loop manner. Notably, such an agent-based               (LAD), Function Block Diagram (FBD), and Sequential Func-
framework is flexible to implement multiple relevant software            tion Chart (SFC), as well as two textual languages: Structured
engineering tasks like validation and debugging, which are               Text (ST) and Instruction List (IL). The structured text (ST)
crucial in improving the quality of generated code.                      language, similar in syntax and structure to traditional pro-
   In this work, we present a novel LLM-based multi-agent                gramming languages such as C and Pascal, offers significant
framework designed to address the limitations of current PLC             flexibility and readability. It supports common programming
code generation solutions, namely Agents4PLC. Our system                 structures, including loops and conditional statements, making
comprises multiple agents, each tailored to specific tasks               it widely used in scenarios that require complex mathematical
such as PLC code generation, syntax validation, functional               calculations, data processing, and advanced control algorithms.
verification and debugging (in case of failures). Such a closed-         With the development of Industry 4.0 and intelligent manufac-
loop workflow allows Agents4PLC to effectively coordinate                turing, the prospects for ST language are extremely promising,
different agents to automatically generate high-quality code             as it can complement other programming languages to enhance
(verifiable correct in the ideal case). Note that different from         the flexibility and efficiency of PLC systems.
LLM4PLC which only verified the correctness of the spec-
ification, we directly verify the correctness of the generated
code. Meanwhile, by leveraging advanced multi-agent archi-               B. Syntax Checking and Functional Verification
tectures like LangGraph and MetaGPT, Agents4PLC is highly
adaptable to a wide range of PLC code generation tasks and                  Code generated by LLMs often exhibits considerable uncer-
incorporate different base code LLMs.                                    tainty and may sometimes fail to compile or meet specified
                                                                         requirements [45]. Syntax checking ensures that the generated
   • We establish a comprehensive benchmark that transitions
                                                                         ST code is executable, while functional verification ensures
      from natural language requirements to formal specifi-
                                                                         that the code realizes the expected functionality and avoids
      cations, utilizing verified reference code with human-
                                                                         potential logic flaws or vulnerabilities [15].
      checked labels, to facilitate future research in the field
      of PLC code generation.                                               1) Syntax Checking: A piece of code first needs to conform
   • We introduce Agents4PLC, the first LLM-based multi-
                                                                         to the standards of a programming language before it can be
      agent system for fully automatic PLC code genera-                  compiled into an executable program. Many PLC Integrated
      tion that surpasses purely LLM-based approaches (e.g.,             Development Environments (IDEs), such as CODESYS and
      LLM4PLC [14]) by emphasizing code-level over design-               TwinCAT, can perform syntax checking for ST code. These
      level verification, and flexibility to incorporate various         IDEs conform to the IEC 61131-3 standard and provide
      base code generation models (in both black-box and                 functionalities such as programming, debugging, and simu-
      white-box settings) and supporting an array of tools for           lation. However, due to the limitations of their platforms,
      compilation, testing, verification and debugging.                  these IDEs are not convenient for direct integration into
   • We enhance our agents specifically for PLC code gen-
                                                                         automated code generation pipelines. Some command-line
      eration by implementing techniques such as Retrieval-              tools can also perform syntax checking and compilation of
      Augmented Generation (RAG), advanced prompt engi-                  ST code. MATIEC [2] is an open-source compiler capable
      neering, and Chain-of-Thought methodologies, improving             of refactoring or compiling ST code into C language, widely
      their adaptability and effectiveness in generating reliable        used in the design and maintenance of industrial automation
      PLC code.                                                          systems. RuSTy [6] is an open-source project based on LLVM
   • We rigorously evaluate Agents4PLC against the largest
                                                                         and Rust, aimed at creating a fast, modern, and open-source
      benchmark available, demonstrating superior perfor-                industry-grade ST compiler for a wide range of platforms,
      mance across a series of increasingly stringent metrics.           providing comprehensive compilation feedback.
      We also deploy and validate our generated code on                     2) Functional Verification: Functional verification is crucial
      multiple practical scenarios, highlighting its potential for       for PLC code, ensuring that the generated ST code can
      generating verifiable PLC code that meets the demands              accurately and reliably implement the intended control logic
      of practical industrial control systems.                           and operations in real-world applications, thereby preventing
                                                                         equipment failures or production interruptions due to logical
                     II. BACKGROUND
                                                                         errors or unforeseen circumstances. There exist some formal
A. PLC Programming Language                                              verification tools such as nuXmv [8] and PLCverif [12] for
   PLCs are computer systems specifically designed for indus-            functional validation of ST code, which are serving as the
trial automation control, enabling real-time monitoring and              backend verifier of our validation agent.



                                                                     2
                                                                                    various aspects of the software development life cycle. Recent
                                                                                    advancements in this field such as ChatDev [39], MetaGPT
                                                                                    [17] and CodeAgent [47], showcase the potential of integrating
                                 LLM-based Agent
                                                                                    AI-driven agents to enhance collaborative software devel-
Observation             Memory                     Thought           Action         opment frameworks, automate code review processes, and
                                                                                    support contextual conversation within software development
                                                                                    environments. These studies indicate a shift towards more
                                                                                    interactive and intelligent software development tools that can
                                                                                    adapt to the dynamic nature of development projects, providing
                                                                                    developers with context-aware assistance and streamlining
                                                                                    tasks through autonomous agents. The integration of advanced
               Inputs                                        Tools
                                   Environment                                      human processes within multi-agent systems emphasizes the
                                                                                    potential of agent-based software development to revolutionize
              Fig. 1: Basic portrait of LLM-based agents                            traditional software engineering practices.

                                                                                                III. AGENTS 4PLC M ETHODOLOGY
C. LLM-based Agents
                                                                                       We propose Agents4PLC, an LLM-based multi-agent
   The rapid advancement of LLMs has elevated traditional AI
                                                                                    framework for automating the generation and verification pro-
agents, which relied on reinforcement learning and symbolic
                                                                                    cess of ST code. The framework includes a set of agents with
logic [21], [23], [34], [35], [41], [53], to a new level, i.e., LLM-
                                                                                    our defined roles and division of work, which automatically
based agents. With the assistance of LLMs, these agents have
                                                                                    cooperate based on our defined workflow for the generation of
a strong ability to understand language, generate content, and
                                                                                    reliable ST code. The whole framework is presented in Fig-
utilize external knowledge and tools. They can perform com-
                                                                                    ure 2. Below we present the detailed design of Agents4PLC.
plex tasks and make decisions through collaboration among
agents and interaction with their environments.
                                                                                    A. Agents4PLC Framework
   There exist various definitions of what comprises an LLM-
based agent, and we present some common components here.                               As shown in Fig. 3, Agents4PLC takes an user input of ST
Typically, an LLM-based agent consists of five key compo-                           coding requirement, e.g., to control an LED, and outputs the
nents: LLM, observation, memory, thought and action [17].                           formally verified ST code. In this process, multiple agents
Figure 1 presents its basic framework1 . Each component can                         with different roles cooperate to complete this task based
be analogized to human cognition for better understanding.                          on our carefully designed workflow. First, the retrieval agent
LLMs serve as part of an agent’s “brain”, enabling it to com-                       analyzes the user input, based on which it retrieves the relevant
prehend information, learn from interactions, make decisions,                       information about ST codes, such as books and documents.
and perform actions. It perceives the environment with the                          Then it sends the retrieved information alongside with the
observation component, e.g., receiving multimodal informa-                          user input (task instructions) to the planning agent, which
tion from the others. It uses memory component to store                             is responsible to generate and rank the actionable plans for
past interactions and observations. It retrieves and analyzes                       code generation, subsequently sent to the Coding Agent. The
information with thought component, to infer the next action.                       Coding Agent generates ST code accordingly to the received
And it execute actions using the LLMs or some external tools.                       plans, and later a compiler checks whether there are syntax
   There are mainstream agent frameworks that can support                           errors. If no error occurs, the validation agent (the verifier)
the development of LLM-based multi-agent workflows, such                            will verify the functional correctness of the generated code.
as MetaGPT [17], LangGraph [5], and AutoGen [52]. These                             Otherwise, the error information will be delivered to the
frameworks provide libraries that enable developers to create                       debugging agent who will return the fixing advice to the
and manage multiple agents seamlessly. They facilitate the                          Coding Agent. If validation succeeds, the generation process
integration of large language models into complex work-                             is considered completed. Otherwise, the above workflow will
flows, allowing for efficient communication and collaboration                       iterate until it exceeds a predefined loop threshold, where the
among agents. Additionally, these frameworks often come                             planning agent provides another plan for code generation.
with features like natural language processing capabilities, task
orchestration, and easy scalability, making them ideal choices                      B. Detailed Agents Design and Optimization
for building sophisticated multi-agent systems.                                        The primary components of Agent4PLC are a group of au-
D. Agent-based Software Development                                                 tonomous agents powered by Large Language Models (LLMs)
                                                                                    or analysis tools. These agents are meticulously designed to
   Agent-based software development is an emerging field that                       perform specialized tasks that collectively contribute to the
integrates autonomous and communicative agents to enhance                           efficient generation, validation, and iterative refinement of ST
   1 More details about different definitions and the components can be found       code. Each agent operates within a well-defined functional
in [17], [50], [57]                                                                 scope, allowing for the delegation of specific responsibilities



                                                                                3
                                                                                      Retrieval Agent                                                        Debugging Agent


                                                                                                                                                 Generated                     Generated Fixed
                                                                                                                                                 Fix Patch                        ST Code
                      Problem                                                        Knowledge Database

                                                                                                       Retrieve
                                                                                                                                                            Validation Agent
                                                                                                                                            Stage 1: Syntax Checking


   User Input                  Structured Text                                   Relevant                Relevant




                                                                                                                                                                                                 Iterative turn < T
                                                                                 Solutions            Knowledge Points                                              Unpassed Syntax-checked
       Use structured text to                                                                                                                                         Code and Feedback
    design a PLC function block                                                                                                              Syntax Check

    “ E.g., the function block should                                                                                                                                 Syntax-checked Code
    represent a simple control system
    where PB1 and PB2 determine
    whether LED is on or off based on                                  Planning Agent                      Coding Agent                     Stage 2: Functional Verification
    the specified logic.”

                                                                                                              Generated                     Generated Properties      Functional Verification
                                                                         Sorted N Plans                       ST Code                                                                                                 Final ST Code

                                                                                                                 Iterative turn = T, back to planning agent and select next plan



                                                                                           Fig. 2: Overview of Agents4PLC.

                                                Problem               [start_scl]
                                                                                                               Coding Agent            Retrieval Agent primarily focuses on searching for the relevant
                                                                      FUNCTION_BLOCK LED_Control
  Design a PLC function block named `LED_Control`
  using structured text (ST code).The function block
                                                                         VAR_INPUT
                                                                           PB1 : BOOL; (* Input Push Button 1 *)
                                                                                                                                       industrial control documents, PLC programming references,
  should contain:                                                          PB2 : BOOL; (* Input Push Button 2 *)
  # - Two Boolean input variables: PB1 and PB2                           END_VAR
                                                                         VAR_OUTPUT
                                                                                                                                       and ST code from a vector database for the reference of
  # - One Boolean output variable: LED                                     LED : BOOL; (* Output LED *)
  # Implement logical operations such that `LED` is                      END_VAR                                                       the following planning process. It can access both web-based
                                                                         LED := PB1 AND NOT PB2;
  assigned the value ...                                              END_FUNCTION_BLOCK
                                                                      [end_scl]
                                                                                                                                       search tools and also internal databases to extract pertinent
                                            Retrieval Agent
 Boolean logic is fundamental in control systems and PLC                      Stage 1: Syntax Checking
                                                                                                             Validation Agent          information.
 programming. Here’s a high-level overview of how to                ST code Compilation success, waiting for validation
 implement Boolean logic in Structured Text:                                      Stage 2: Functional Verification
                                                                                                                                           2) Planning Agent: The Planning Agent receives the user
 1. **Understanding Boolean Variables**: In PLC
 programming, Boolean variables are used to represent two
                                                               'property 1: job_req: pattern is satisfied by the program.pattern
                                                               details: If "instance.PB1 = TRUE AND instance.PB2 = FALSE" is
                                                                                                                                       input and the information retrieved by the retrieval agent,
 states: TRUE (1) and FALSE (0). These variables are           true at the end of the PLC cycle, then "instance.LED = TRUE"
 crucial for making decisions within the control system. ...   should always be true at the end of the same cycle.'                    based on which it generates actionable plans using a structured
                                                                       [start_scl]                             Final ST Code
                                                                                                                                       automata-like format. Each plan represents a sequence of steps
                                            Planning Agent
                                                                       FUNCTION_BLOCK LED_Control
  Given a competitive programming problem, generate a
                                                                          VAR_INPUT                                                    required to achieve the task. The planning agent ranks these
                                                                            PB1 : BOOL; (* Input Push Button 1
  concrete planning to solve the problem.                              *)                                                              plans, which later will get executed sequentially, based on their
  1. Define the function block `LED_Control`.                               PB2 : BOOL; (* Input Push Button 2
                                                                       *)
  2. Declare the input variables `PB1` and `PB2` as Boolean.              END_VAR                                                      ranking, help identify the most suitable solution.
  3. Declare the output variable `LED` as Boolean.                        VAR_OUTPUT
  4. Implement the logical operation inside the function                    LED : BOOL; (* Output LED *)
                                                                                                                                           3) Coding Agent: The Coding Agent is pivotal in con-
  block where `LED` is assigned the result of `PB1`                       END_VAR
                                                                          LED := PB1 AND NOT PB2;
  AND (NOT `PB2`) AND end the function block.                          END_FUNCTION_BLOCK                                              verting the detailed plans from the upstream agent into ST
                                                                       [end_scl]

                                                                                                                                       code, ensuring compliance with both syntactic and semantic
Fig. 3: An example of generating LED Control ST code with                                                                              requirements. By utilizing a RAG block, the agent accesses a
                       Agents4PLC.                                                                                                     comprehensive database of PLC documentation and validated
                                                                                                                                       ST code samples. RAG enables the agent to learn from
such as code generation, debugging and validation. In particu-                                                                         the established experience and domain-specific knowledge,
lar, the LLM-based agents excel at tasks such as understanding                                                                         thus making informed decisions based on the provided PLC
user specifications provided in natural language, retrieving                                                                           resources, help improve the reliability of the generated code.
relevant information, and generating ST code. Meanwhile,                                                                                   In addition, prompts for the Coding Agent play a crucial role
tool-based agents are designed to address domain-specific                                                                              in steering the Coding Agent throughout the code generation
tasks, such as syntax checking and verification of ST code. The                                                                        process. These prompts encapsulate domain-specific rules and
cooperation workflow among agents within this architecture                                                                             constraints, to guide the Coding Agent to follow the com-
not only enhances the scalability and adaptability but also                                                                            piler requirements and the predefined validation criteria. The
facilitates collaborative interactions, creating a continuous                                                                          Coding Agent operates iteratively alongside debugging and
feedback loop that improves the overall code development.                                                                              validation agents, fostering a collaborative loop that facilitates
  1) Retrieval Agent: The Retrieval Agent is responsible for                                                                           continuous feedback. This interaction enables the early iden-
gathering relevant information for reference based on user in-                                                                         tification and resolution of syntactic, logical, and functional
put. Although some key agents in the framework are equipped                                                                            errors, significantly improving the overall code quality.
with a RAG module to enhance task-specific abilities, the                                                                                  Optimization: To further improve the quality of the gen-



                                                                                                                                   4
erated code, the guiding prompts for the Coding Agent are               the repair process becomes more intuitive and responsive.
meticulously refined. These prompts include critical elements           This structured reflection fosters a deeper understanding of the
of PLC coding, such as defining the roles and responsibilities          issues at hand, resulting in more precise and effective fixes.
of various code modules, enforcing action constraints for                  Furthermore, providing contextual information, such as
compliance with system safety and operational regulations,              formal verification properties and validation outcomes helps
and leveraging insights from the detailed plans provided by the         the code repair model generate more accurate and targeted
Planning Agent. These help the Coding Agent meet not only               corrections. This strategy significantly enhances the repair
the structural requirements but also the operational constraints,       process, particularly for errors that cannot be resolved solely
improving code reliability and practicability.                          through an examination of the source code.
   4) Debugging Agent: The Debugging Agent is essential for                The use of RAG for code generation also proves effective
analyzing errors and inconsistencies that emerge during the             during the debugging phase. Employing previously generated
compilation of the ST code. It interprets feedback from the             patches in a self-RAG context can improve the effectiveness
ST compiler and utilizes RAG tools alongside the prompts                of repair, capitalizing on the wealth of information contained
designed for patch generation to produce the revised code.              in the generated outputs. By continuously refining and vali-
The revised code is then relayed to the Validation Agent                dating code through this advanced debugging framework, the
for syntactic and semantic verification. The Debugging Agent            Debugging Agent not only enhances the quality of the final
consists of three components as follows.                                output but also optimizes the overall development workflow.
                                                                           5) Validation Agent: The Validation Agent is responsible
  • Syntactic Fixing Advice Generation. With the input                  for verifying the functional correctness of ST code. Different
    from the compilation results of the ST compiler within              from LLM4PLC [14], it offers code-level verification for the
    the validation agent, it generates fixing advice based on           ST code, which is necessary for the industrial control systems.
    the syntactic checking results including the error locations        The agent is composed of several specialized sub-components,
    and reasons. The fixing employs a structured patch gener-           each tasked with specific validation responsibilities:
    ation process, utilizing a step-by-step Chain-of-Thought               • ST Code Compilation. The first step in the validation
    (CoT) methodology that analyzes the origin of error                       process is to run the received ST code through a compiler
    code, its info and description respectively. This thorough                to verify its syntactic correctness. This step ensures the
    analysis leads to accurate identification of the reasons                  generated code conforms to the syntactical rules of ST.
    of error and generation of fixing advice, significantly                   If the compilation is successful, the process advances to
    enhancing the accuracy and efficiency of error fixing.                    the verification phase. Otherwise, the compiler provides
  • Semantic Fixing Advice Generation. This component
                                                                              detailed error information, which is then fed into the
    is to address semantic errors identified during formal                    Debugging Agent for code correction. By automating
    verification. Similar to the syntactic process, the semantic              this initial verification step, the Validation Agent helps
    fixing process is also based on CoT, which guides the                     streamline the debugging cycle and reduces manual in-
    LLM to assess the violated property and the reason of                     tervention.
    violation, pinpoint potential code segments responsible                • Property Generation. In cases where formal speci-
    for the property violations, and generate fixing advice.                  fications are not explicitly provided by the user, the
  • Fixed Code Generation. This component accepts the
                                                                              agent uses a subcomponent that leverages an LLM-driven
    fixing advice from the previous processes, along with                     mechanism to generate a set of formal specifications
    the generated code and the currently active plan from                     automatically. These specifications are derived from user
    the Planning Agent, based on which it repairs the code.                   input, industry standards, and general safety require-
    Its design mirrors that of the Coding Agent, leveraging                   ments, and they are structured to meet the format required
    RAG to access the same comprehensive database of the                      by formal verification tools. This process help make
    reference resources. By integrating this information, the                 the validation process efficient, especially in complex or
    Debugging Agent can refine its output before relaying                     large-scale systems where manual specification writing
    them to the Validation Agent.                                             can be time-consuming and error-prone.
   Optimization The Debugging Agent serves as a critical                   • Translation-based ST Code Analysis. This subcompo-
module for rectifying code errors. Inspired by existing work                  nent translates the generated ST code into formats or
in automated code repair [54], which utilizes the generated                   languages compatible with formal verification tools such
dialogue history and real-time feedback for corrective sugges-                as SMV or CBMC [29]. The translation process is either
tions, we develop a comprehensive workflow for patch analysis                 managed by LLM-driven agents or by specialized tools
and generation within the Debugging Agent. We adopt the CoT                   like PLCverif [12].
methodology to guide code repair through the patch generation              Optimization One primary challenge with LLM-guided
process. Compared to the traditional fine-tuning methods for            verification is the potential of inconsistencies between the
code repair, our approach enhances the effectiveness and                original ST code and the translated version used for formal
adaptability of the repair process. By encouraging the LLM to           verification. Also, automatically translated code may lead
reflect on error messages, relevant code lines, and test names,         to state explosion, a common problem in model checking



                                                                    5
where the state space grows exponentially, making verification         [16], GPT-4o [3] and GPT-4o-mini [4] to evaluate our method.
computationally expensive or infeasible. To address these,             For the retrieval model, we utilize text-embedding-ada-002, an
we integrate advanced translation-based verification tools like        advanced model developed by OpenAI.
PLCverif, which has been optimized for translating ST code             Evaluation Metrics. Following previous work [14], we em-
into SMV or CBMC formats for model checking and bounded                ploy the 1) pass rate, 2) syntax compilation success rate
model checking (BMC), and may help alleviate the problem               and 3) verification success rate (or verifiable rate) as metrics
of state explosion. Our design of the Validation Agent allows          to evaluate the effectiveness of code generation. The syntax
for easy incorporation of new verification tools as they be-           compilation success rate serves as a preliminary validation
come available, future-proofing the framework and ensuring             of the syntactic correctness of the generated ST code. A
that it remains adaptable to advances in the field of formal           high syntax compilation success rate indicates fewer syntax
verification.                                                          errors, thereby reducing subsequent debugging efforts. The
   Another challenge is that in real-world applications, users         pass rate is derived from the pass@k metric, where the model
often struggle to define formal properties for verification. To        is considered successful if at least one of the k generated
address this, we develop a specification generation tool within        results that not only compile successfully but also adhere to the
the Validation Agent. It helps users automatically generate            specified functional requirements of the PLC program, which
formal properties in a format suitable for verification tools,         is the most challenging task. The verifiable rate quantifies
leveraging the chain-of-thought (CoT) methodology to guide             the proportion of the generated ST code segments that can
the process. This automated approach not only provide conve-           pass syntax check of target verification language, e.g. nuXmv
nience for users but also ensures that the generated properties        or cbmc. A high verifiable rate reflects the effectiveness of
are tailored to formal verification.                                   the approach in generating executable code for verification.
                                                                       We calculate it as the proportion of code segments that
             IV. E XPERIMENTAL E VALUATION
                                                                       successfully compile out of the total number of generated code
   To systematically evaluate the effectiveness, efficiency, and       segments.
other key aspects of our framework for PLC code generation,
we design a series of experiments aimed at answering the                                             V. R ESULTS
following research questions (RQs):                                    A. RQ1: Effectiveness study
   • RQ1: Can Agents4PLC generate PLC code more effec-                    In this experiment, we systematically compare our frame-
     tively compared to the existing approaches?                       work with other code generation frameworks based on several
   • RQ2: How efficient Agent4PLC is in PLC code genera-               base LLMs for generating reliable ST code. Our evaluation
     tion?                                                             is based on a set of benchmark cases designed to reflect
   • RQ3: How effective are the designs in agents, e.g., RAG           varying levels of complexity, from relatively straightforward
     and prompt design in the Coding Agent?                            control sequences (labeled as “Easy”) to more sophisticated
   • RQ4: How useful is the generated code in practical PLC            logic processes (labeled as “Medium”). Note that LLM4PLC
     production environments?                                          is designed to be a half-automated framework with human
Benchmark Construction. To accurately evaluate our                     interactions, we write an extra automation program to drive the
Agents4PLC system, we constructed the first benchmark                  components of the LLM4PLC framework. More experiment
dataset focused on the task of generating ST code from natural         details are included in our github link 2 and our site.3
language specification, and we assess the correctness of code             The models evaluated in this experiment include CodeLlama
samples automatically through formal verification methods.             34B, GPT-4o, GPT-4o-mini, and DeepSeek V2.5. Among
This dataset comprises 23 programming tasks along with                 these, the CodeLlama 34B model is run on a single NVIDIA
corresponding formal verification specifications, including 58         A800 80GB PCIe GPU with pre-trained LoRAs from the
properties in easy set with 53 non-trivial property over 16 easy       LLM4PLC framework, while the other models are tested
programming tasks and 43 in medium set with 38 non-trivial             via their respective online APIs. Each model is provided
property over 7 medium programming tasks, where trivial                with user requirements, code skeletons, and natural language
property means ”assertion” property without corresponding as-          specifications to generate ST code. This setup mirrors real-
sertion sentences in ST code for reference. These programming          world coding scenarios where the models function as code
problems cover various aspects of industrial programming in-           generation agents without detailed control over the underlying
cluding Logical Control, Mathematical Operations, Real-time            logic design. Additionally, to assess the potential of non-
Monitoring, Process Control and other fields, which effectively        specialized models for PLC code generation, we also evaluated
simulate the genuine requirements found in industrial control          the performance of the ChatDev framework [40] with GPT-4o
systems.                                                               base model on our benchmark.
                                                                          The experiment results is shown in Table III, which il-
Base LLMs and Retrieval Model. For a comprehensive
                                                                       lustrates the performance of different frameworks based on
evaluation of Agents4PLC against different base models, we
investigated the capabilities of several popular code LLMs.              2 https://github.com/Luoji-zju/Agents4PLC release

In particular, we adopt CodeLlama 34B [42], DeepSeek V2.5                3 https://hotbento.github.io/Agent4PLC/




                                                                   6
different models across both “Easy” and “Medium” benchmark           able rate, 43.8% pass rate on the Easy category and 28.6%
levels. The table presents the pass rates for both compilation       syntax compilation, 14.3% verifiable rate, and 28.6% pass
and verification stages, with the format X Y Z%, where X             rate on medium category, showing that most compilable code
represents the number of successful passes on corresponding          from ChatDev are correct in semantics. However, it is also
metrics, Y indicates the total number of programming prob-           worth noting that despite explicitly prompting the ChatDev
lems, and Z% denotes the pass rate percentage. For instance,         framework to generate ST code, it occasionally produces
LLM4PLC/GPT-4o achieves a syntax compilation pass rate               code in unrelated languages, such as Python or C++. This
of 14 16 87.5%, meaning the generated result of LLM4PLC              highlights a limitation of general-purpose code generation
on the GPT-4o model successfully compiles for 14 out of              frameworks in specialized industrial domains.
16 programming problems, yielding an 87.5% success rate.
                                                                     B. RQ2: Efficiency study
We record syntax compilation success rate, verifiable rate and
pass rate for both systems, where “verifiable rate” means the           To evaluate the efficiency of our framework in generating
framework can generate verifiable model for at least 80% of          verifiable st code, we measured the time taken for each
the given properties, and “pass rate” means that least 80% of        model to successfully generate a syntactically correct and
the generated code can compile.                                      semantically verified ST code. Considering in our validation
   The results highlight the effectiveness of our Agents4PLC         process, PLCverif is not supported for efficiency evaluation,
framework which outperforms other software development               we categorize the results based on how many attempts it takes
frameworks across different benchmark levels. In the “Easy”          for each model to pass the syntactic compilation stage. The
category, the performance of LLM4PLC on different mod-               categories are as follows:
els demonstrates notable variability. The GPT-4o-mini model             • 1 Attempt: The code passes syntactic compilation stage
achieves the highest syntax compilation pass rate of 93.8%,                on the first try.
successfully compiling 15 out of 16 code segments. In con-              • 2 Attempts: The code passes syntactic compilation stage
trast, the CodeLlama 34B model, based on the original ex-                  on the second attempt after a failure.
perimental setting has the lowest performance, with a syntax            • 3 or more than 3 Attempts: The framework takes more
compilation pass rate of only 68.8%. Notably, the verifiable               than three attempts to succeed.
rate and pass rate for all LLM4PLC models are significantly             The experimental results are presented in Table I, where
low, with both GPT-4o and DeepSeek V2.5 recording a verifi-          the data format represents the number of generation attempts
able rate of 12.5% on the Easy problems. Only DeepSeek V2.5          required / total cases passing syntactic compilation / ratio. The
achieves a pass rate of 12.5% on these problems, indicating          experimental setup is identical to that of Experiment 1.
that the LLM-based automative generation of SMV models                  The results demonstrate that our framework, when paired
requires further improvement.                                        with the base models DeepSeek V2.5, GPT-4o, and GPT-
   On the contrary, Agents4PLC framework exhibits more               4o-mini, consistently achieved successful ST code generation
consistent performance across different models in the Easy           in a single attempt, regardless of whether the problems are
category. Except for CodeLlama 34B, they all achieve a syntax        classified as easy or medium. In contrast, the CodeLlama
compilation pass rate of 100%, successfully compiling all gen-       34B model within our framework exhibited instances of re-
erated code for the programming problems. Our Agents4PLC             quiring code repair after the initial attempt. In comparison,
framework across different models achieves a maximum                 the LLM4PLC framework showed multiple instances across
verifiable rate of 68% and a pass rate of 50% with the               all tested models where two or more attempts are necessary
GPT-4o model, indicating the superior capability of our              to produce compilable code. This stark contrast in perfor-
framework in generating verifiable code.                             mance underscores that our Agents4PLC framework not
   For the Medium benchmark level, both systems main-                only delivers higher code generation success rates but
tain their respective performance patterns, with Agents4PLC          also significantly improves efficiency, particularly when
consistently outperforming LLM4PLC. All models from                  compared to LLM4PLC, which required more frequent
Agents4PLC manage to achieve a syntax compilation rate of            code corrections.
100% on “Medium” problems, contrasting sharply with the
variable results from LLM4PLC, where the highest syntax              C. RQ3: Ablation study
compilation pass rate is again recorded by GPT-4o and GPT-             The ablation study aims to evaluate the influence of specific
4o-mini at 57.1%. Our Agents4PLC framework achieves                  design choices within our framework on the performance
a maximum verifiable rate of 42.3% with GPT-4o and                   of code generation. Our ablation experiments are organized
DeepSeek V2.5, and a maximum pass rate of 28.6% with                 around two primary domains:
GPT-4o, demonstrating that our framework can effectively               • Coding Agent: We investigate the effects of three sig-
handle tasks involving complex coding problems.                           nificant enhancements: syntax hints in prompts, retrieval-
   We also conduct experiments on ST code generation using                augmented generation (RAG), and one-shot prompting on
ChatDev, a general-purpose software development platform                  the ST code generation process. The following configu-
based on multi-agent systems. This software development                   rations are examined, with each enhancement systemati-
framework achieve 43.8% syntax compilation, 43.8% verifi-                 cally removed to assess its impact on the pass rates:



                                                                 7
         TABLE I: Efficiency evaluation: ST code generation times over all attempts passing syntactic compilation
       Benchmark Level                                     Easy Problems                                               Medium Problems
Framework     Base Model                 1 time                2 time              3 or more              1 time            2 time                 3 or more
              CodeLlama 34B          8 11 72.7%           0 11 0.0%            3   11 27.3%         2   4 50.0%         2 4 50.0%              0   4 0.0%
              DeepSeek V2.5          12 13 92.3%          1 13 7.7%            0   13 0.0%          6   7 85.7%         1 7 14.3%              0   7 0.0%
LLM4PLC
              GPT-4o                 13 14 92.9%          1 14 7.1%            0   14 0.0%          3   4 75.0%         1 4 25.0%              0   4 0.0%
              GPT-4o-mini            15 15 100.0%         0 15 0.0%            0   15 0.0%          3   4 75.0%         0 4 0.0%               1   4 25.0%
              CodeLlama 34B          4 5 80.0%            1 5 20.0%            0   5 0.0%           1   1 100.0%        0 1 0.0%               0   1 0.0%
              DeepSeek V2.5          16 16 100.0%         0 16 0.0%            0   16 0.0%          7   7 100.0%        0 7 0.0%               0   7 0.0%
Agents4PLC
              GPT-4o                 16 16 100.0%         0 16 0.0%            0   16 0.0%          7   7 100.0%        0 7 0.0%               0   7 0.0%
              GPT-4o-mini            16 16 100.0%         0 16 0.0%            0   16 0.0%          7   7 100.0%        0 7 0.0%               0   7 0.0%
        Note: The format of data represents the number for corresponding generation times / total cases passing syntactic compilation / ratio.

                           TABLE II: Ablation Experiment with Designs on Coding and Fixing Agents
               Benchmark Level                                          Easy Problems                                       Medium Problems

Framework       Base Model                              Syntax             Pass Rate       Verifiable Rate      Syntax             Pass Rate       Verifiable Rate
                                                      Compilation                                             Compilation
                One-shot + RAG + Syntax Hint         16 16 100.0%       8 16 50.0%         11 16 68.8%        7 7 100.0%       2   7   28.6%       3   7   42.9%
                One-shot + Syntax Hint               16 16 100.0%       11 16 68.8%        12 16 75.0%        7 7 100.0%       1   7   14.3%       3   7   42.9%
Coding Agent    One-shot + RAG                       16 16 100.0%       6 16 37.5%         9 16 56.2%         7 7 100.0%       1   7   14.3%       1   7   14.3%
                One-shot                             16 16 100.0%       6 16 37.5%         9 16 56.2%         7 7 100.0%       0   7   0.0%        1   7   14.3%
                Zero-shot                            16 16 100.0%       7 16 43.8%         8 16 50.0%         7 7 100.0%       0   7   0.0%        1   7   14.3%
Debugging
                Without CoT / Patch Template         16 16 100.0%       10 16 62.5%        10 16 50.0%        7 7 100.0%       0 7 0.0%            1 7 14.3%
Agent
 Note: The format of data represents number of successful passes on corresponding metrics / total number of programming problems / passing rate.



     – Full Configuration: The complete framework incor-                           with 28.6% pass rate and 42.9% verifiable rate). The
       porating syntax hints, RAG, and one-shot prompting.                         impact for each configuration analysis is:
     – Intermediate Configuration without RAG: The                                   – RAG: The application of RAG provides noticeable
       framework utilizing one-shot prompting and syntax                               improvements for medium-level problems, but its
       hints, but excluding RAG.                                                       impact on easy problems is less pronounced, and in
     – Intermediate Configuration without Syntax hint:                                 some cases, it may even have unintended negative
       The framework utilizing simple one-shot prompting                               effects.
       and RAG, but excluding syntax hints.                                          – Syntax Hint: Detailed syntax hints significantly en-
     – Simplified Configuration: A streamlined version                                 hance the effectiveness of code generation, especially
       using only plain one-shot prompting.                                            for easy problems. The provision of syntax guidance
     – Baseline Configuration: The foundational setup                                  helps improve both the syntactical correctness and
       with zero-shot prompting and no supplementary aids                              the overall quality of generated code.
       (syntax hints and RAG).                                                       – One shot: In our experiments, we observe that
•   Debugging Agent: In this segment, we assess the impor-                             one-shot prompting do not lead to a substantial
    tance of two critical components of the Debugging agent:                           improvement in performance. This is likely because
    chain-of-thought (CoT) reasoning and patch templates.                              the one-shot method merely provides a reference ST
    We compare the framework’s performance when both                                   code template, which has limited effectiveness in
    components are disabled, effectively operating without                             improving the overall quality of code generation.
    CoT reasoning and patch templates. This allows us to                             – CoT in Debugging agent: For easy problems, the
    quantify the degradation in code correction capabilities                           results show no significant difference between using
    resulting from their absence.                                                      the standard debugging agent and that with CoT.
    Table II summarizes the findings from this ablation                                However, for medium-level problems, the removal of
    study, showcasing the ST code verification pass rates and                          CoT noticeably reduce the framework’s performance,
    compilation pass rates across various configurations. The                          indicating that CoT is crucial for handling more
    configuration of experiment and table content is similar                           complex debugging tasks.
    to those in effectiveness study, including metrics and                      The results indicate that the inclusion of syntax hints
    data format. The configuration that on Easy Problem                       improves performance across all metrics, while the impact
    set, the setting combining One-shot and Syntax Hint                       of one-shot prompting remains unclear. However, the effects
    yields the highest overall pass rates (68.8%) and verifiable              of more advanced optimization techniques, such as RAG and
    rates (75.0%). However, the results for medium problems                   CoT, warrant further investigation. These methods significantly
    mirror the full configuration, One-shot + RAG + Syn-                      enhance the framework’s ability to handle complex problems,
    tax Hint configuration, demonstrate superior performance                  but when not carefully designed, they may interfere with the



                                                                          8
reasoning process on simpler tasks. Additionally, considering
Section V-B, our framework can often generate correct code
in a single attempt. As a result, the current experiments may
not fully capture the effectiveness of the debugging agent.
D. RQ4: Case study in practical control environment
   To evaluate how Agent4PLC performs in practical industrial
control environment, we conduct case studies utilizing the                        Fig. 4: LED control with Agents4PLC.
UWinTech Control Engineering Application Software Plat-
form, developed by Hangzhou UWNTEK Automation System
Co., Ltd. UWinTech is a software package designed for using
the UW series control system [1]. It integrates a wide range
of functionalities, including on-site data collection, algorithm
execution, real-time and historical data processing, alarm and
safety mechanisms, process control, animation display, trend
curve analysis, report generation, and network monitoring. The
engineer station configuration software, operator station real-
time monitoring software, and on-site control station real-time
                                                                            Fig. 5: Motor triggering control with Agents4PLC.
control software operate on different levels of hardware plat-
forms. Its components interact via control networks and system
networks, coordinating the exchange of data, management,               code) that incorporates pressure sensors, temperature sensors,
and control information to ensure the successful execution of          relays, counters, error codes, and error flags as inputs. The
various functions within the control system.                           program must loop through the pressure sensor, adjust the
   Our experiments involve several steps: first, we constructed        temperature sensor based on specific conditions, and update
the operation station and the control station, then we config-         the relay status according to the value of GT1-OUT. Ensure
ured the attributes of the monitoring and control points. These        that the program checks for conditions to avoid overflow
points are linked to the simulation model, and the generated           and maintains the error flag state. Return a Boolean value
ST code from Agent4PLC were uploaded to the control station            indicating the completion of the operation. The results show
to conduct the experiment. We perform four control tasks:              that low or high limit alarms and different error codes are
site monitoring and alarm light flashing, low voltage limit            provided when pressure and temperature are abnormal. When
and motor start/stop, temperature and pressure monitoring, and         an abnormality occurs, the alarm light will flash. If the pressure
specific node delay monitoring.                                        exceeds the upper limit, the error code is 1. If the temperature
   Figure 4 denotes an LED Control task. The prompt is:                is above the high limit, the error code is 3. If the temperature
design a PLC function block named LED-Control using struc-             is below the lower limit, the error code is 4. These comply
tured text (ST) code. The function block should contain two            with the requirements in the prompt.
Boolean input variables (PB1 and PB2) and one Boolean
output variable (LED). Implement logical operations such that                              VI. R ELATED WORKS
LED is assigned the value resulting from a logical AND
operation between PB1 and the negation of PB2. The function               There are significantly increasing interests from both the in-
block should represent a simple control system where PB1               dustry and academia in LLM-based code generation, including
and PB2 determine whether LED is on or off based on the                those LLMs specifically designed for code generation such as
specified logic. The results show that with the generated ST           DeepSeek-Coder [16], StarCoder [32], and CodeLlama [42].
code uploaded, when PB1 is true (1) and PB2 is false (0),              However, most of them focus on high-level languages such
namely the the AND operation between PB1 and the negation              as C, Python and only a very small portion considers PLC
of PB2 output 1, the light is green, and otherwise, it is red.         code in control engineering. Here, we mainly review those
This complies with the requirement in the prompt.                      works considering PLC code from the aspects of its generation,
                                                                       testing and verification. We also seperatly review the existing
   Figure 5 denotes a motor control task. The Prompt is:
                                                                       LLM-based multi-agent frameworks for code generation.
Design a PLC function block in Structured Text (ST) that
evaluates whether the critical motor should be triggered based
on the given low pressure value compared to a threshold of
36464. The state of Motor-Critical is determined based on
this evaluation. The results show that when the input voltage
is below the threshold 36464, the motor stops; otherwise, the
motor starts.
   Figure 6 denotes a temperature and relay update task. The
prompt is: Design a PLC program using structured text (ST
                                                                               Fig. 6: Temperature update with Agents4PLC.

                                                                   9
                               TABLE III: Compilation and Verification Metrics for Different Models
       Benchmark Level                                     Easy Problems                                             Medium Problems
 Framework    Base Model                  Syntax           Verifiable Rate        Pass Rate           Syntax          Verifiable Rate         Pass Rate
                                        Compilation                                                 Compilation
                  CodeLlama 34B       11 16 68.8%         0 16 0.0%            0 16 0.0%          4 7 57.1%           0 7 0.0%            0 7 0.0%
                  DeepSeek V2.5       13 16 81.3%         2 16 12.5%           2 16 12.5%         7 7 100.0%          0 7 0.0%            0 7 0.0%
 LLM4PLC
                  GPT-4o              14 16 87.5%         0 16 0.0%            2 16 12.5%         4 7 57.1%           0 7 0.0%            0 7 0.0%
                  GPT-4o-mini         15 16 93.8%         0 16 0.0%            0 16 0.0%          4 7 57.1%           0 7 0.0%            0 7 0.0%
                  CodeLlama 34B        5 16 31.3%         2 16 12.5%           1 16 6.3%          1 7 14.3%           0 7 0.0%            0 7 0.0%
                  DeepSeek V2.5       16 16 100.0%        10 16 62.5%          7 16 43.8%         7 7 100.0%          3 7 42.9%           1 7 14.3%
 Agents4PLC
                  GPT-4o              16 16 100.0%        11 16 68.8%          8 16 50.0%         7 7 100.0%          3 7 42.9%           2 7 28.6%
                  GPT-4o-mini         16 16 100.0%        8 16 50.0%           7 16 43.8%         7 7 100.0%          1 7 14.3%           0 7 0.0%
 ChatDev          GPT-4o              7 16 43.8%          NA                   NA                 2 7 28.6%           NA                  NA
   Note: The format of data represents number of successful passes on corresponding metrics / total number of programming problems / passing rate.



A. LLM-based Automated PLC Code Generation                                    Agents4PLC is the first LLM-agent-based system covering the
                                                                              whole lifecycle of ST control engineering.
   There exist a few works studying the LLM-based generation
of PLC programming code like ST. For instance, Koziolek et                    B. PLC Code Testing and Verification
al. [26] create 100 prompts across 10 categories to evaluate the                 Due to the fact that PLC programming is often performed in
ability of the existing LLMs to produce syntactically correct                 low-level programming languages, which typically use bitwise
control logic code in ST language. Later, they introduce a                    and boolean operations, it becomes very difficult to understand
retrieval-augmented generation method [27] and an image-                      and debug PLC programs. This increases the need for testing
recognition-based generation method [28]. These methods in-                   and verification of PLC programs [38], [46]. Existing methods
tegrate proprietary function blocks into the generated code and               for the automated generation of PLC test cases mainly include
utilize GPT-4 Vision to generate control logic code for indus-                symbolic execution [44], concolic testing [7] and search-based
trial automation from Piping-and-Instrumentation Diagrams                     techniques [13]. However, these approaches can produce test
(P&IDs), respectively. However, they do not consider testing or               cases that are difficult to maintain, making them challenging
verification of the generated code, and thus cannot ensure code               to use. Koziolek et al. [25] propose to automatically generate
correctness. Fakih et al. [14] introduce an LLM-based PLC                     PLC test cases as a csv file by querying an LLM with a
code generation pipeline named LLM4PLC, which integrates                      prompt to synthesize code test cases. And they found in
the fine-tuned LLMs with external verification tools. Though                  experiments that many generated test cases contain incorrect
it takes formal verification into consideration, it only achieves             assertions and require manual correction. The multi-agent
design-level verification (instead of the ST code level) and the              based generation approaches Mapcoder [22], AutoSafeCoder
generation process can not achieve full automation. Witnessing                [37] and AgentCoder [19] all consider code testing, but ignore
these limitations of existing works, we aim to achieve closed-                formal verification of the generated code.
loop and fully automated PLC code generation and verification                    In terms of PLC code verification, there exist tools like
with our designed multi-agent system Agents4PLC, paving a                     nuXmv [8] and PLCverif [12] applicable for functional veri-
way for evolving, efficient, trustworthy and intelligent coding               fication of ST code, which are serving as the backend verifier
for industrial control systems.                                               in Agents4PLC. Besides, several recent works aim to establish
   Our work is also inspired by the recent trend in code                      formal semantics for IEC 61131-3 languages like ST with
generation approaches which rely on the cooperation of LLM-                   more recent language framework like K framework [30], [49],
based agents. ChatDev [18], a virtual software development                    facilitating testing or verification of ST code [31].
company composed of multiple agents, features clearly defined
roles and divisions of labor, aiming to collaboratively generate                       VII. C ONCLUSION AND F UTURE W ORKS
high-quality software code. However, ChatDev still shows                         In this paper, we presented Agents4PLC, the first LLM-
limitations when it comes to generating software code for                     based multi-agent framework that addresses the critical chal-
industrial control systems without formal verification support.               lenges of automated Programmable Logic Controller (PLC)
Mapcoder [22] consists of four LLM-based agents for the tasks                 code generation and verification. By establishing a compre-
of recalling relevant examples, planning, code generation,                    hensive benchmark that transitions from natural language
and debugging respectively, relying on multi-agent prompting                  requirements to formal specifications, we laid the groundwork
for code generation. AutoSafeCoder [37] consists of three                     for future research in the field of PLC code generation. Our
agents responsible for code generation, static analysis and                   framework not only emphasizes code-level verification and full
fuzzing to detect runtime errors respectively. AgentCoder [19]                automation, but also is flexible to incorporate various base
consists of three agents responsible for code generation and                  code generation models and development modules. Extensive
refinement, test case generation, test execution and feedback                 evaluation demonstrates that Agents4PLC significantly outper-
reporting respectively. These approaches all focus on Python                  forms the previous approaches, achieving high automation and
language which is fundamentally different to ST for PLC.                      verifiability for PLC code generation.



                                                                         10
   In the future, we plan to expand the framework to sup-                             [20] International Electrotechnical Commission (IEC), “IEC 61131-
port additional PLC programming languages and standards                                    3:2013 Programmable controllers - Part 3: Programming languages,”
                                                                                           https://webstore.iec.ch/en/publication/4552, 2013, edition 3.0, ISBN:
to enhance its applicability across various industrial contexts.                           9782832206614.
Moreover, we will explore user feedback mechanisms within                             [21] C. Isbell, C. R. Shelton, M. Kearns, S. Singh, and P. Stone, “A social
the multi-agent system to help refine the generated code                                   reinforcement learning agent,” in Proceedings of the fifth international
                                                                                           conference on Autonomous agents, 2001, pp. 377–384.
and the agents based on real-world usage, thereby further                             [22] M. A. Islam, M. E. Ali, and M. R. Parvez, “Mapcoder: Multi-
enhancing its usability and reliability.                                                   agent code generation for competitive problem solving,” arXiv preprint
                                                                                           arXiv:2405.11403, 2024.
                              R EFERENCES                                             [23] L. P. Kaelbling, M. L. Littman, and A. W. Moore, “Reinforcement
                                                                                           learning: A survey,” Journal of artificial intelligence research, vol. 4,
 [1] “Uwintech control engineering application software platform,” https://                pp. 237–285, 1996.
     www.uwntek.com/product/2.html, accessed: 2024-10-10.                             [24] M. Kornaszewski, “The use of programmable logic controllers in railway
 [2] “Matiec,” 2017. [Online]. Available: https://github.com/nucleron/matiec               signaling systems,” in ICTE in Transportation and Logistics 2019.
 [3] “Gpt-4o,” 2024. [Online]. Available: https://platform.openai.com/docs/                Springer, 2020, pp. 104–111.
     models/gpt-4o                                                                    [25] H. Koziolek, V. Ashiwal, S. Bandyopadhyay et al., “Automated control
 [4] “Gpt-4o-mini,” 2024. [Online]. Available: https://platform.openai.com/                logic test case generation using large language models,” arXiv preprint
     docs/models/gpt-4o-mini                                                               arXiv:2405.01874, 2024.
 [5] “Langgraph,” 2024. [Online]. Available: https://github.com/langchain-ai/         [26] H. Koziolek, S. Gruener, and V. Ashiwal, “Chatgpt for plc/dcs control
     langgraph                                                                             logic generation,” in 2023 IEEE 28th International Conference on
 [6] “Rusty,” 2024. [Online]. Available: https://github.com/PLC-lang/rusty                 Emerging Technologies and Factory Automation (ETFA). IEEE, 2023,
 [7] D. Bohlender, H. Simon, N. Friedrich, S. Kowalewski, and S. Hauck-                    pp. 1–8.
     Stattelmann, “Concolic test generation for plc programs using coverage           [27] H. Koziolek, S. Grüner, R. Hark, V. Ashiwal, S. Linsbauer, and N. Es-
     metrics,” in 2016 13th International Workshop on Discrete Event Sys-                  kandani, “Llm-based and retrieval-augmented control code generation,”
     tems (WODES). IEEE, 2016, pp. 432–437.                                                in Proceedings of the 1st International Workshop on Large Language
 [8] R. Cavada, A. Cimatti, M. Dorigatti, A. Griggio, A. Mariotti, A. Micheli,             Models for Code, 2024, pp. 22–29.
     S. Mover, M. Roveri, and S. Tonetta, “The nuxmv symbolic model                   [28] H. Koziolek and A. Koziolek, “Llm-based control code generation using
     checker,” in Computer Aided Verification: 26th International Confer-                  image recognition,” in Proceedings of the 1st International Workshop on
     ence, CAV 2014, Held as Part of the Vienna Summer of Logic, VSL                       Large Language Models for Code, 2024, pp. 38–45.
     2014, Vienna, Austria, July 18-22, 2014. Proceedings 26. Springer,               [29] D. Kroening and M. Tautschnig, “Cbmc–c bounded model checker:
     2014, pp. 334–342.                                                                    (competition contribution),” in Tools and Algorithms for the Construc-
 [9] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. D. O. Pinto, J. Kaplan,                    tion and Analysis of Systems: 20th International Conference, TACAS
     H. Edwards, Y. Burda, N. Joseph, G. Brockman et al., “Evaluating large                2014, Held as Part of the European Joint Conferences on Theory and
     language models trained on code,” arXiv preprint arXiv:2107.03374,                    Practice of Software, ETAPS 2014, Grenoble, France, April 5-13, 2014.
     2021.                                                                                 Proceedings 20. Springer, 2014, pp. 389–391.
[10] Z. Chen, S. Fang, and M. Monperrus, “Supersonic: Learning to generate
                                                                                      [30] J. Lee and K. Bae, “Formal semantics and analysis of multitask plc
     source code optimizations in c/c++,” IEEE Transactions on Software
                                                                                           st programs with preemption,” in International Symposium on Formal
     Engineering, 2024.
                                                                                           Methods. Springer, 2024, pp. 425–442.
[11] V. Corso, L. Mariani, D. Micucci, and O. Riganelli, “Generating java
                                                                                      [31] J. Lee, S. Kim, and K. Bae, “Bounded model checking of plc st
     methods: An empirical assessment of four ai-based code assistants,”
                                                                                           programs using rewriting modulo smt,” in Proceedings of the 8th ACM
     in Proceedings of the 32nd IEEE/ACM International Conference on
                                                                                           SIGPLAN International Workshop on Formal Techniques for Safety-
     Program Comprehension, 2024, pp. 13–23.
                                                                                           Critical Systems, 2022, pp. 56–67.
[12] D. Darvas, E. Blanco Vinuela, and B. Fernández Adiego, “Plcverif: A
     tool to verify plc programs based on model checking techniques,” in              [32] R. Li, L. B. Allal, Y. Zi, N. Muennighoff, D. Kocetkov, C. Mou,
     Proceedings of the 15th International Conference on Accelerator and                   M. Marone, C. Akiki, J. Li, J. Chim et al., “Starcoder: may the source
     Large Experimental Physics Control Systems. IEEE, 2015, pp. 1–6.                      be with you!” arXiv preprint arXiv:2305.06161, 2023.
[13] M. Ebrahimi Salari, E. P. Enoiu, W. Afzal, and C. Seceleanu, “Pylc: A            [33] Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond,
     framework for transforming and validating plc software using python                   T. Eccles, J. Keeling, F. Gimeno, A. Dal Lago et al., “Competition-
     and pynguin test generator,” in Proceedings of the 38th ACM/SIGAPP                    level code generation with alphacode,” Science, vol. 378, no. 6624, pp.
     Symposium on Applied Computing, 2023, pp. 1476–1485.                                  1092–1097, 2022.
[14] M. Fakih, R. Dharmaji, Y. Moghaddas, G. Quiros, O. Ogundare, and                 [34] J. Liu, K. Wang, Y. Chen, X. Peng, Z. Chen, L. Zhang, and Y. Lou,
     M. A. Al Faruque, “Llm4plc: Harnessing large language models for                      “Large language model-based agents for software engineering: A sur-
     verifiable programming of plcs in industrial control systems,” in Pro-                vey,” arXiv preprint arXiv:2409.02977, 2024.
     ceedings of the 46th International Conference on Software Engineering:           [35] M. Minsky, “Steps toward artificial intelligence,” Proceedings of the
     Software Engineering in Practice, 2024, pp. 192–203.                                  IRE, vol. 49, no. 1, pp. 8–30, 1961.
[15] E. First and Y. Brun, “Diversity-driven automated formal verification,”          [36] Mordor Intelligence, “Programmable logic controller (plc) market
     in Proceedings of the 44th International Conference on Software Engi-                 - share, size & growth,” 2024, accessed: 2024-10-08. [On-
     neering, 2022, pp. 749–761.                                                           line]. Available: https://www.mordorintelligence.com/industry-reports/
[16] D. Guo, Q. Zhu, D. Yang, Z. Xie, K. Dong, W. Zhang, G. Chen,                          programmable-logic-controller-plc-market
     X. Bi, Y. Wu, Y. Li et al., “Deepseek-coder: When the large language             [37] A. Nunez, N. T. Islam, S. K. Jha, and P. Najafirad, “Autosafecoder: A
     model meets programming–the rise of code intelligence,” arXiv preprint                multi-agent framework for securing llm code generation through static
     arXiv:2401.14196, 2024.                                                               analysis and fuzz testing,” arXiv preprint arXiv:2409.10737, 2024.
[17] S. Hong, X. Zheng, J. Chen, Y. Cheng, J. Wang, C. Zhang, Z. Wang,                [38] T. Ovatman, A. Aral, D. Polat, and A. O. Ünver, “An overview of model
     S. K. S. Yau, Z. Lin, L. Zhou et al., “Metagpt: Meta programming for                  checking practices on verification of plc software,” Software & Systems
     multi-agent collaborative framework,” arXiv preprint arXiv:2308.00352,                Modeling, vol. 15, no. 4, pp. 937–960, 2016.
     2023.                                                                            [39] C. Qian, W. Liu, H. Liu, N. Chen, Y. Dang, J. Li, C. Yang, W. Chen,
[18] X. Hou, Y. Zhao, Y. Liu, Z. Yang, K. Wang, L. Li, X. Luo, D. Lo,                      Y. Su, X. Cong et al., “Chatdev: Communicative agents for software
     J. Grundy, and H. Wang, “Large language models for software engi-                     development,” in Proceedings of the 62nd Annual Meeting of the
     neering: A systematic literature review,” ACM Transactions on Software                Association for Computational Linguistics (Volume 1: Long Papers),
     Engineering and Methodology, 2023.                                                    2024, pp. 15 174–15 186.
[19] D. Huang, Q. Bu, J. M. Zhang, M. Luck, and H. Cui, “Agentcoder:                  [40] C. Qian, W. Liu, H. Liu, N. Chen, Y. Dang, J. Li, C. Yang,
     Multi-agent-based code generation with iterative testing and optimisa-                W. Chen, Y. Su, X. Cong, J. Xu, D. Li, Z. Liu, and M. Sun,
     tion,” arXiv preprint arXiv:2312.13010, 2023.                                         “Chatdev: Communicative agents for software development,” arXiv




                                                                                 11
     preprint arXiv:2307.07924, 2023. [Online]. Available: https://arxiv.org/
     abs/2307.07924
[41] C. Ribeiro, “Reinforcement learning agents,” Artificial intelligence re-
     view, vol. 17, pp. 223–250, 2002.
[42] B. Roziere, J. Gehring, F. Gloeckle, S. Sootla, I. Gat, X. E. Tan, Y. Adi,
     J. Liu, R. Sauvestre, T. Remez et al., “Code llama: Open foundation
     models for code,” arXiv preprint arXiv:2308.12950, 2023.
[43] M. Schreyer and M. M. Tseng, “Design framework of plc-based control
     for reconfigurable manufacturing systems,” in Proceedings of interna-
     tional conference on flexible automation and intelligent manufacturing
     (FAIM 2000), vol. 1, 2000, pp. 33–42.
[44] J. Shi, Y. Chen, Q. Li, Y. Huang, Y. Yang, and M. Zhao, “Automated test
     cases generator for iec 61131-3 structured text based dynamic symbolic
     execution,” IEEE Transactions on Computers, 2024.
[45] M. L. Siddiq, B. Casey, and J. Santos, “A lightweight framework for
     high-quality code generation,” arXiv preprint arXiv:2307.08220, 2023.
[46] A. Singh, “Taxonomy of machine learning techniques in test case gen-
     eration,” in 2023 7th International Conference on Intelligent Computing
     and Control Systems (ICICCS). IEEE, 2023, pp. 474–481.
[47] D. Tang, Z. Chen, K. Kim, Y. Song, H. Tian, S. Ezzini, Y. Huang, and
     J. K. T. F. Bissyande, “Collaborative agents for software engineering,”
     arXiv preprint arXiv:2402.02172, 2024.
[48] Technavio, “Programmable logic controller (plc) market analysis apac,
     north america, europe, middle east and africa, south america - us,
     china, japan, germany, uk - size and forecast 2024-2028,” 2024,
     accessed: 2024-10-08. [Online]. Available: https://www.technavio.com/
     report/programmable-logic-controller-plc-market-industry-analysis
[49] K. Wang, J. Wang, C. M. Poskitt, X. Chen, J. Sun, and P. Cheng, “K-st:
     A formal executable semantics of the structured text language for plcs,”
     IEEE Transactions on Software Engineering, 2023.
[50] L. Wang, C. Ma, X. Feng, Z. Zhang, H. Yang, J. Zhang, Z. Chen,
     J. Tang, X. Chen, Y. Lin et al., “A survey on large language model based
     autonomous agents,” Frontiers of Computer Science, vol. 18, no. 6, p.
     186345, 2024.
[51] M. Wang, “Application of plc technology in electrical engineering and
     automation control,” in Application of Intelligent Systems in Multi-
     modal Information Analytics: Proceedings of the 2020 International
     Conference on Multi-model Information Analytics (MMIA2020), Volume
     2. Springer, 2021, pp. 131–135.
[52] Q. Wu, G. Bansal, J. Zhang, Y. Wu, B. Li, E. Zhu, L. Jiang, X. Zhang,
     S. Zhang, J. Liu, A. H. Awadallah, R. W. White, D. Burger, and
     C. Wang, “Autogen: Enabling next-gen llm applications via multi-agent
     conversation framework,” in COLM, 2024.
[53] Z. Xi, W. Chen, X. Guo, W. He, Y. Ding, B. Hong, M. Zhang, J. Wang,
     S. Jin, E. Zhou et al., “The rise and potential of large language model
     based agents: A survey,” arXiv preprint arXiv:2309.07864, 2023.
[54] C. S. Xia and L. Zhang, “Keep the conversation going: Fixing
     162 out of 337 bugs for $0.42 each using chatgpt,” arXiv preprint
     arXiv:2304.00385, 2023.
[55] K. Xu, G. L. Zhang, X. Yin, C. Zhuo, U. Schlichtmann, and B. Li,
     “Automated c/c++ program repair for high-level synthesis via large
     language models,” in Proceedings of the 2024 ACM/IEEE International
     Symposium on Machine Learning for CAD, 2024, pp. 1–9.
[56] K. Zhang, J. Li, G. Li, X. Shi, and Z. Jin, “Codeagent: Enhancing code
     generation with tool-integrated agent systems for real-world repo-level
     coding challenges,” arXiv preprint arXiv:2401.07339, 2024.
[57] Z. Zhang, X. Bo, C. Ma, R. Li, X. Chen, Q. Dai, J. Zhu, Z. Dong,
     and J.-R. Wen, “A survey on the memory mechanism of large language
     model based agents,” arXiv preprint arXiv:2404.13501, 2024.




                                                                                  12
