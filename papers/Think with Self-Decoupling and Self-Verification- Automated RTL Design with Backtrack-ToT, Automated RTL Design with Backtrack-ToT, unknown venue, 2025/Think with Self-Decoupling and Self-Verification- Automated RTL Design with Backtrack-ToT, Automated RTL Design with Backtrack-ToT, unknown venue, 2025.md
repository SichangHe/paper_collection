                                            Think with Self-Decoupling and Self-Verification:
                                              Automated RTL Design with Backtrack-ToT
                                          Zhiteng Chao1 , Yonghao Wang1† , Xinyu Zhang1,2 , Jiaxin Zhou3 , Tenghui Hua1,2 , Husheng Han1 , Tianmeng Yang2 ,
                                                                  Jianan Mu1† , Bei Yu5 , Rui Zhang1 , Jing Ye1,2 and Huawei Li1,2
                                                                1
                                                               State Key Lab of Processors, Institute of Computing Technology, CAS, Beijing, China
                                                                           2
                                                                             University of Chinese Academy of Sciences, Beijing, China
                                                   3
                                                     Beijing Normal University, China; 4 Peking University, China; 5 Chinese University of Hong Kong, Hongkong
                                                                         {chaozhiteng, wangyonghao22s, mujianan, lihuawei}@ict.ac.cn
arXiv:2511.13139v1 [cs.AR] 17 Nov 2025




                                            Abstract—Large language models (LLMs) hold promise for                                         Top Module: adder_pipe_64bit
                                                                                                                                                                                                 CoT_Input
                                         automating integrated circuit (IC) engineering using register                               adder_stage

                                         transfer level (RTL) hardware description languages (HDLs)
                                                                                                                                                                                             module adder_pipe_64bit ();
                                         like Verilog. However, challenges remain in ensuring the quality                data
                                                                                                                                                                                                 Step1: Define Registers
                                         of Verilog generation. Complex designs often fail in a single                                                          multi_stage_adder                ......
                                         generation due to the lack of targeted decoupling strategies,                                                                                           Step2: Pipeline Logic
                                                                                                                                                                                                 ......
                                         and evaluating the correctness of decoupled sub-tasks remains                                                                                           Step3: Output Logic
                                                                                                                                   pipeline_control
                                         difficult. While the chain-of-thought (CoT) method is commonly                                                                                          ......
                                                                                                                                                                                             endmodule
                                         used to improve LLM reasoning, it has been largely ineffective
                                                                                                                         control
                                         in automating IC design workflows, requiring manual inter-
                                         vention. The key issue is controlling CoT reasoning direction
                                         and step granularity, which do not align with expert RTL                                                                                            RTL                Testbench
                                         design knowledge. This paper introduces VeriBToT, a specialized
                                         LLM reasoning paradigm for automated Verilog generation.                                                     (a)                                                 (b)
                                         By integrating Top-down and design-for-verification (DFV) ap-                  Top-Down Modular Design Flow
                                         proaches, VeriBToT achieves self-decoupling and self-verification               with Submodule-Level Verify                                adder_pipe_64bit.v
                                         of intermediate steps, constructing a Backtrack Tree of Thought
                                         with formal operators. Compared to traditional CoT paradigms,                  Step 1: Decompose Submodules
                                         our approach enhances Verilog generation while optimizing token                Step 2: Implementation                     adder_stage.v    multi_stage_adder.v     pipeline_control.v
                                         costs through flexible modularity, hierarchy, and reusability.
                                            Index Terms—Backtrack Tree, ToT, DFV, Top-down                              Step 3: Verify Submodules

                                                                                                                        Step 4: Integrate Submodules
                                                                 I. I NTRODUCTION
                                                                                                                        Step 5: Verify Design
                                            Digital circuits lie at the core of modern computing systems,
                                         yet their design remains a demanding process. Engineers
                                         rely on register transfer level (RTL) hardware description                                                                          (c)
                                         languages (HDLs) to translate functional requirements into                     Fig. 1: The modular concurrency in circuit design is illustrated
                                         logic gate combinations, which are then verified and mapped                    in (a), (b) presents common scenarios for the CoT paradigm
                                         into transistor-level designs for fabrication. Although the                    in generating an RTL module’s Verilog code step by step, (c)
                                         downstream tasks of verification and transistor mapping have                   depicts the human circuit design paradigm.
                                         been largely automated, the initial writing of HDL code still
                                         demands significant human effort. This deficiency represents
                                         a pressing bottleneck in chip design workflows, inflating costs                   A pivotal factor enabling the success of LLMs in software
                                         and undermining efficiency [1].                                                code generation is the “chain-of-thought” (CoT) reasoning
                                            Recent advances in artificial intelligence, notably in large                paradigm [13]–[15], which decomposes intricate problems
                                         language models (LLMs) [2], present an encouraging avenue                      into smaller, sequential steps. By enhancing the accuracy and
                                         for mitigating this challenge. In fields like natural language                 logical consistency of generated outputs, CoT significantly
                                         processing (NLP), LLMs have achieved remarkable success                        advances automated code generation. However, directly ap-
                                         in software [3] and hardware code generation [4]–[12]. This                    plying CoT methods to the domain of automated RTL design
                                         triumph underscores their potential to automate and streamline                 has yielded limited results as sequence reasoning process is
                                         complex workflows.                                                             vulnerable and hard to capture hierarchical dependencies of
                                                                                                                        complex submodules.
                                           † Corresponding Author
                                         This paper has been published in the 29th Design, Automation and Test in          We conducted a task-specific analysis to better understand
                                         Europe Conference (DATE 2026), April 20-22, 2026, Verona, Italy.               the challenges of naive CoT in automated RTL design. Circuit



                                                                                                                    1
design is fundamentally different from describing sequential              Input-Output Chain-of-Thought Chain-of-Thought with SC                      Tree-of-Thought
functional behaviors in programming languages like C or                      Input          Input                         Input                              Input
Python. As illustrated in Fig. 1a, all functional modules in
RTL design are implemented as concrete hardware circuits and                                                   ……          ……            ……
                                                                                            ……
operate in parallel to achieve the desired functionality. This
parallelism introduces numerous interdependencies between                                                                                               ……      Vote/Best of N
modules. For LLMs, generating RTL requires considering a                                                                       Vote/Best of N
significantly broader range of contextual information across                Output         Output                     Output                           Output

multiple RTL modules, as well as achieving precise cycle-level                (a)            (b)                               (c)                           (d)
                                                                                                     Dependencies                    Unevaluated    Passed            Failed
design coupling. Consequently, reasoning and decision-making                                       Between Thoughts                   Thought      Thought           Thought

in RTL design are considerably more complex than in software
code generation, which typically involves understanding only a          Fig. 2: The comparison between traditional CoT paradigms.
limited range of and coarse grained preceding contexts. When
naive CoT is applied to enhance LLMs for generating RTL as
shown in Fig. 1b, it is often observed that the generated results            lar verification and design-verification co-iteration in
are uncontrollable, producing unnecessary and meaningless                    thought process, granting the intermediate thought steps
content, without improving the generation capability of LLMs.                the capability of self-verification.
   The RTL design process by which human engineers write                  4) Extensive experimental results show that the proposed
code is illustrated in Fig. 1c and exhibits two key characteris-             VeriBToT significantly improves code correctness, with
tics from an engineering design perspective. Firstly, engineers              a significant improvement on the benchmark compared
consider factors such as circuit complexity and adopt a Top-                 to existing CoT methods.
down approach [16] to partition the design into modules. This
ensures that each module remains highly cohesive internally                           II. M OTIVATION AND R ELATED W ORK
while maintaining low coupling with other modules, thereby
reducing both the difficulty of developing individual modules              CoT-based prompt engineering [13] is used to improve
and the complexity of integrating them. Secondly, during the            reasoning and problem-solving performance for LLMs. The
coding process, engineers verify each module’s functionality            core idea is to explicitly guide the model through a multi-
before merging them, iterating layer by layer [17]. This ap-            step reasoning by breaking down a complex task into smaller,
proach significantly lowers the overall debugging complexity.           sequential steps. This approach mimics human thought pro-
Together, these two practices facilitate efficient iteration and        cesses. Numerous variants have been developed around CoT,
integration in modular design.                                          such as CoT-SC [19], tree of thoughts (ToT) [20], [21], and
   In this paper, we introduce VeriBToT, a novel Backtrack-             graph of thoughts (GoT) [22]. The comparison of different
Tree-of-Thought framework for modular RTL design, inspired              CoT reasoning paradigms is illustrated in the Fig. 2. The
by human IC design methods. Our approach divides the                    traditional CoT method offers some degree of assistance in
LLM reasoning process into two cognitive pathways: self-                the field of code generation [15], [23]–[26].
decoupling for partition refinement, and self-verification for             However, there are obstacles to enhancing RTL generation
ensuring the correctness of generated code. To implement                capabilities by directly applying any traditional CoT. Current
these pathways, we design five prompt generation opera-                 CoT approaches lack the modular design and verification prac-
tors based on human IC design interactions, integrated into             tices essential for hardware code development. These methods
a Backtrack Tree of Thought. Experiments on open-source                 follow a linear, unidirectional flow, where large functional
benchmarks show that VeriBToT enhances code correctness                 modules are decomposed without reconsidering the reason-
compared to existing CoT methods. The main contributions                ableness of the partitioning. This often leads to overly complex
of this work are as follows:                                            modules or excessive inter-module interactions, making it
   1) We propose a novel Backtrack-Tree-of-Thought frame-               difficult for LLMs to generate correct and integrable code.
       work that integrates IC design methodologies (e.g., Top-         Moreover, CoT lacks single step verification, relying instead
       down and DFV), achieving refined control over the                on functional validation after completing the entire code.
       thought process for LLM automatic RTL generation.                This approach results in unclear feedback, making it hard to
   2) By leveraging the modular and hierarchical principles             pinpoint and address specific issues. The lack of fine-grained
       of the Top-down methodology, we decouple the ToT                 control in current CoT methods also can lead to a significant
       thought step nodes into corresponding RTL submodules             increase in token consumption. As demonstrated by traditional
       within the IC design. The leaf nodes, representing fron-         ToT in Fig. 2d, both the tree depth and the number of child
       tier thought steps, are empowered to self-decouple their         nodes for each node are hyperparameters, and setting these
       leaf-module designs into lower-level submodules.                 values too large can incur substantial computational costs.
   3) By leveraging Top-down and DFV methodologies, we                  Consequently, the absence of modular thinking and iterative
       decouple common self-refinement operations found in              verification are key challenges that limit CoT’s effectiveness
       traditional prompt engineering [18], achieving modu-             in RTL generation.



                                                                    2
   Top module                            Input                          Self Decouple：Split the undetermined module             these two cognitive pathways. Inspired by the practical IC
                                                                                                                 Passed
Sub-module Layer 1
                                                                        Self Verify：         Unevaluated
                                                                                                                 Failed
                                                                                                                                design process, we define five specific operations that structure
Sub-module Layer 2
                                                                                Reserved           Removed                      the entire reasoning process.
                                                                 Thought
                                                                 Please decompose the current module into an
Sub-module Layer 3                                               appropriate combination of submodules based on its
                                                                                                                                B. Operator Design
                                                      Thought    natural language description, and provide the natural
                                                                 language descriptions, RTL design code, and testbench
          module Top
                                                      frontier   verification code for the individual submodules.                  We have designed five operators to perform VeriBToT.
          Sub1A a (..);
                                      Collect when
          Sub1B b (..);
                                      all modules e              Thought
                                                                                                                                These operators structure the reasoning process into a tree
  module Sub1A        module Sub1B                               Based on the previously generated testbench
  Sub2A a (..);       Sub2C c (..);                              verification code, please analyze whether the sub-
                                                                                                                                of thought, and the interactions between the operators can be
  Sub2B b (..);       Sub2D d (..);                              circuit design, with the current module as the top
                  ......                Output                   module and the child modules as submodules,                    abstracted as collaboration among different design personnel
                                                                 successfully passes functional correctness verification.
                                                                                                                                in an IC company design workflow, with the entire process
Fig. 3: The motivation of VeriBToT: each node in the diagram                                                                    adhering to the principles of Top-down and DFV design.
represents a thought step, which is limited to a module                                                                            1) Branch Generator: Under a correct Top-down design
within the hierarchical RTL design (including natural language                                                                        module decomposition plan created by the product man-
descriptions, RTL design Verilog, and testbench Verilog).                                                                             ager, RTL designers and testers will break down a com-
                                                                                                                                      plex design into appropriate submodules and separately
                                                                                                                                      design the RTL and testbench for each submodule.
   Inspired by human-centric IC design methodologies (Top-                                                                         2) Node Evaluator: Testers follow the module decompo-
down, DFV), we introduce a dedicated ToT paradigm,                                                                                    sition plan designed by the product manager to create
VeriBToT, for automatic RTL generation by LLMs as shown                                                                               separate test plans for different levels of modules accord-
in Fig. 3. The Top-down [16] approach is a hierarchical                                                                               ing to their specifications. Once the RTL designs for all
design methodology that starts with system-level requirements                                                                         submodules under the current subtree are completed, the
and progressively refines the design to lower abstraction                                                                             tester uses the pre-designed testbench to verify whether
levels, promoting early validation, design reuse, and team                                                                            the RTL functionality of the current subsystem is correct.
collaboration. Design-for-verification (DFV) [17] enhances the                                                                     3) Node Rethinker: When a single bottom-level module
verifiability of designs by incorporating verification-friendly                                                                       designed by an engineer fails through the testbench,
features early in the development process, aiming to reduce                                                                           the tester requests the design engineer to immediately
verification complexity and improve efficiency through mod-                                                                           redesign the RTL of this module.
ularization and better test planning. The process begins at                                                                        4) Backtrack Executor: An engineer responsible for a
inputting the natural language description of top-level module                                                                        middleware module composed of lower-level modules
design. Then, self-decoupling thought prompt is designed                                                                              discovers during the actual development process that the
for hierarchical sub-module decomposition to minimize inter-                                                                          product manager’s module decomposition plan contains
module dependencies, thereby enabling each sub-module to                                                                              errors, making it impossible to produce middleware
be designed and verified independently without affecting the                                                                          that meets overall design requirements. The engineer
others. Each thought step generates a complete design flow for                                                                        requests that the product manager revise the module
a sub-module, including natural language descriptions, RTL                                                                            decomposition plan to determine whether the next step
design Verilog, and testbench Verilog. For instance, a top-level                                                                      should involve redesigning based on the current middle-
module Top may be decomposed into multi-layer lower level                                                                             ware or modifying the design of the layer above.
sub-modules (e.g., Sub1A could contain Sub2A and Sub2B,                                                                            5) Code Aggregator: The product manager ultimately as-
and Sub1B could contain Sub2C and Sub2D). When to                                                                                     sembles all the validated hierarchical modules into a
invoke the self-decoupling thought requires the LLM to self-                                                                          complete design for approval.
assess the complexity of the current design.                                                                                       By implementing these operators, each intermediate thought
   The self-verify thought prompt is designed to verify the                                                                     step can achieve self-decoupling and self-validation, enhancing
correctness of the RTL code generated for each sub-module.                                                                      the overall design ability of LLMs.
Based on the already generated testbench, LLMs assess
whether the RTL code for the sub-design rooted at the current                                                                   C. Reasoning Process
node is functionally correct. Starting from the leaf node,                                                                         We define several notions used in this paper based on
the process iterates upward. If the LLMs determine that the                                                                     concepts from previous methods to facilitate the formalization
implementation at the current node is incorrect, the existing                                                                   of the problem. We use lowercase letters x, y, z to repre-
sub-design is discarded and rewritten.                                                                                          sent language sequences. Here, x denotes the original natural
            III. T HE P ROPOSED V ERI BT OT F RAMEWORK                                                                          language description of the RTL design, serving as the input
                                                                                                                                for the entire problem; y represents the final answer to the
A. Overview                                                                                                                     problem, including the complete Verilog code as the output;
   We designed VeriBToT, a specialized LLM ToT reasoning                                                                        and z1 , . . . , zn denotes a chain of thoughts that bridges x and
paradigm for automated RTL design, featuring thought-step                                                                       y, where each zi is a intermediate thought step that guides the
self-decoupling and self-verification capabilities. As shown in                                                                 process of RTL generation. In the ToT paradigm, LLMs are
Fig. 3, the core of VeriBToT lies in how to formally define                                                                     permitted to explore multiple reasoning paths across the nodes



                                                                                                                            3
       si         si+1                    si                     si+1
                                                                              .......                      module+testbench                                  module+testbench
                                                                          K             1. Call: B E       adder_pipe_64bit();
                                                                                                                                              4. Call: B     adder_pipe_64bit();
  B                             K                                 or
                                                                  B                         module+testbench           module+testbench           module+testbench       module+testbench
                                                       .......
                                                                                            control_logic();           multi_stage_adder();       controller();          ripple_carry_adder();
       si                si+1              si                    si+1
  R                             E                                or
                                                                                                           module+testbench                                  module+testbench
                                                                                        2. Call: R E       adder_pipe_64bit();                5. Call: E     adder_pipe_64bit();

                                                                                            module+testbench           module+testbench           module+testbench       module+testbench
  A                                             Verilog                                     control_logic();           multi_stage_adder();       controller();          ripple_carry_adder();


                                                                                        3. Call: K E       module+testbench        Failed     6. Call: K E A module+testbench            Pass
         Dependencies                Unevaluated                       Passed                              adder_pipe_64bit();                               adder_pipe_64bit();
       Between Thoughts               Thought                         Thought
             Failed                 Defined                                                 module+testbench           module+testbench           module+testbench       module+testbench
                    ABEKR                          Refuse               Choose              control_logic();           multi_stage_adder();       controller();          ripple_carry_adder();
            Thought                 Operator


Fig. 4: The left side of the figure illustrates a schematic representation of how pre-defined operators control the thought
process. The right side depicts how a 64-bit adder is generated through the thought process of VeriBToT, achieved through
the combination of these operators; to differentiate among the five operators we have defined, we employ the following
abbreviations: Branch Generator is represented by B, Node Evaluator by E, Node Rethinker by R, Backtrack Executor by
K, and Code Aggregator by A.


of a tree, where an intermediate state in the tree is represented                                          to invoke Backtrack Executor, which we will discuss next.
as s = [x, z1 , . . . , zi ], a node of thought is represented as n                                        Backtracking. The invocation of the Backtrack Executor
sampled from the current state s, and a collection of all states                                           can occur not only after the failure of leaf node generation
for ToT is denoted by S = [s1 , . . . , sn ].                                                              mentioned above but also when all the leaf nodes of any
   The formal representation of the five operators and a                                                   subtree pass self-validation through the Node Evaluator. At
complete example of the VeriBToT reasoning process are                                                     this point, VeriBToT begins backtracking towards the root
illustrated in Fig. 4. To formalize the discussion of the ex-                                              node. For each non-leaf node encountered during this process,
ploration process of VeriBToT, we use uppercase letters: L                                                 the Node Rethinker is called based on the submodules of
to denote natural language, D to denote RTL design, and V                                                  this node that have already passed validation, generating new
to denote testbench for verification. From the perspective of                                              [nD , nV ], followed by self-validation. During this process, if
the content of language sequences, each intermediate thought                                               any non-leaf node fails validation again, backtracking occurs
step zi can be split into three parts: the RTL design language                                             at that node. At this moment, two choices arise. If the LLM
description ziL , the Verilog code for the current module RTL                                              determines that there are issues with the submodule divisions
design ziD , and the testbench for the current design ziV . The                                            of the current node, it uses a “removing prompt” to clear
entire process can be broadly categorized into the following                                               all sub-nodes in the subtree rooted at this node and restarts
key components, organized according to the depth-first search                                              branching from the backtracked node. Conversely, if the LLM
(DFS) traversal method of the Backtrack Tree algorithm:                                                    believes that the design of the current node itself is sound but
Tree Initialization. The process begins with a root node s0 =                                              that the task decomposition of the parent node’s higher-level
x, n0 = x. The input sequence x = [xL , xV ] represents a                                                  module is erroneous, it will continue backtracking to the parent
natural language description of the overall RTL design and                                                 node, removing the backtracked node and its sibling nodes.
the testbench used for final functionality testing.                                                        The LLM will then evaluate in the same manner iteratively
Branching. For a newly generated leaf node n =                                                             until it backtracks to a node where the submodule division is
[nL , nD , nV ], VeriBToT calls Node Evaluator for self-                                                   valid and recommences branching.
verifying nD by nV , both of which are generated at the                                                    Tree Finality. When the evaluator believes that the entire RTL
same step for n. If the LLM determines that the validation                                                 design has been correctly completed, the Code Aggregator
is successful, it proceeds to the next node. If the validation                                             operation is executed to return the final RTL Verilog output
fails again, the node faces two choices. If the LLM deter-                                                 y, and EDA tools are invoked to verify whether it passes the
mines that the current design is still relatively complex, it                                              top-level testbench xV .
decides to invoke the Branch Generator. The LLM, using                                                        Fig. 4 illustrates how a practical RTL design example is
a “branching prompt,” decomposes the current leaf node’s                                                   developed using the VeriBToT framework. For a 64-bit adder,
design into several new leaf nodes, each of which describes                                                referred to as adder pipe 64bit, the LLM initially cannot
the complete design requirements n′L , implementation n′D ,                                                complete a correct design within a single Verilog module.
and validation n′V for a bottom-level module. If the LLM                                                   As a result, it decomposes this into two submodules: the
considers the current design to be simple enough, it decides                                               control module control logic and the multi-stage adder module



                                                                                                       4
           TABLE I: Reasoning paradigm evaluation on the full benchmark about functional Pass@1 and Pass@5.
             Reasoning                           VerilogEval-Human                                                   RTLLM
             Paradigm
                                       DeepSeek                    ChatGPT-4                         DeepSeek                        ChatGPT-4
                             pass@1         pass@5         pass@1          pass@5            pass@1         pass@5           pass@1           pass@5
             IO              0.27           0.36           0.34            0.45              0.34           0.46             0.42             0.56
             CoT             0.29           0.37           0.33            0.47              0.30           0.40             0.38             0.50
             CoT-SC          0.27           0.37           0.38            0.50              0.24           0.38             0.40             0.46
             ToT             0.26           0.39           0.35            0.48              0.28           0.48             0.38             0.48
             VeriBToT        0.32           0.44           0.43            0.58              0.42           0.56             0.48             0.62
             VeriBToT-       0.29           0.36           0.36            0.52              0.26           0.44             0.41             0.57
             Domain                    Thakur                      RTLCoder                           Thakur                         RTLCoder
             Specific
                             pass@1         pass@5         pass@1          pass@5            pass@1         pass@5           pass@1           pass@5
             IO              30.3           43.9           36.7            45.5              14.9           24.1             39.8             48.3
  Domain specific models lack the ability to follow instructions based on different reasoning paradigms; the light green indicates that the current result
  surpasses one domain-specific fine-tuned model, while the dark green indicates that it surpasses two.

TABLE II: The performance of the Deepseek-Coder-V2 in generating Verilog for different hard cases under various reasoning
paradigms is measured by the number of successful attempts out of five trials (#pass@5), assessing syntax correctness (Syn.)
and functional correctness (Fun.); the average token consumption (Tok., the unit is thousand, k) is used to evaluate the resource
expenditure of the reasoning paradigms, Bold values indicate results from our method that are the best.
                                           IO                     CoT                       CoT-SC                   ToT                       VeriBToT
         Design
                                Syn.     Fun.     Tok.   Syn.     Fun.    Tok.       Syn.    Fun.    Tok.   Syn.     Fun.     Tok.     Syn.      Fun.   Tok.
         adder 16bit            3        3        1.11   5        3       1.35       4       3       2.62   4        3        1.39     5         5      1.88
         adder pipe 64bit       5        1        0.67   5        1       0.82       4       2       1.47   5        3        1.94     5         2      2.34
         multi pipe 8bit        0        0        0.94   0        0       1.26       0       0       2.03   3        0        1.86     4         0      1.41
         multi 16bit            1        1        1.1    3        0       1.02       1       0       1.92   4        2        1.45     4         1      1.58
         barrel shifter         5        0        0.62   5        0       0.67       4       0       1.65   4        1        1.41     5         1      2.12
         width 8to16            5        0        0.53   2        1       1.01       2       1       0.97   5        1        0.99     4         3      1.62
         calendar               5        0        0.52   5        0       0.98       2       0       1.38   5        0        1.1      5         5      1.45
         freq div               5        0        0.74   5        1       1.16       5       2       1.08   3        0        1.78     5         4      1.44
         dff8r                  3        0        0.43   4        4       0.65       0       0       1.41   3        0        1.23     5         5      1.21
         fsm2s                  0        0        0.64   0        0       0.78       0       0       1.52   0        0        1.10     2         1      1.82
         fsm3comb               0        0        0.63   1        1       0.90       1       1       1.68   0        0        1.34     5         3      2.56
         gates4                 5        1        0.42   5        4       0.65       4       3       1.36   5        4        1.24     5         5      1.49
         popcount3              0        0        0.57   3        1       0.76       0       0       1.25   1        0        1.77     2         2      1.77
         m2014 q4i              0        0        0.13   0        0       0.35       0       0       0.82   3        2        1.06     4         4      0.42
         ringer                 0        0        0.39   0        0       0.71       0       0       0.91   0        0        1.06     4         3      2.53
         timer                  0        0        0.47   2        2       0.68       0       0       1.29   2        1        1.15     4         3      1.77

TABLE III: The performance of the ChatGPT-4 in generating Verilog for different hard cases under various reasoning paradigms,
the various metrics are the same as those in Table II.
                                           IO                     CoT                       CoT-SC                   ToT                       VeriBToT
         Design
                                Syn.     Func.    Tok.   Syn.     Func.   Tok.       Syn.    Func.   Tok.   Syn.     Func.    Tok.     Syn.      Func. Tok.
         adder 16bit            4        3        0.85   4        4       1.88       5       5       3.04   4        4        2.73     5         5      1.76
         adder 32bit            5        3        1.37   3        3       1.93       3       3       2.26   2        0        2.19     5         2      2.01
         adder pipe 64bit       5        1        1.07   3        0       1.80       5       1       2.62   4        0        2.65     5         4      2.37
         multi pipe 8bit        5        0        1.97   3        0       1.37       5       0       2.51   2        0        2.58     4         0      0.57
         barrel shifter         1        0        0.74   5        0       1.2        5       0       1.54   5        0        2.3      5         0      2.62
         width 8to16            5        3        0.85   5        4       1.45       4       3       1.61   5        3        1.78     5         3      2.32
         freq div               5        1        0.89   5        4       1.70       5       3       3.12   5        4        2.05     5         5      1.99
         sequence detector      0        0        1.03   0        0       1.67       1       0       2.13   1        0        2.93     5         2      1.84
         dff8r                  5        0        0.43   0        0       0.90       0       0       1.46   0        0        1.38     3         3      1.65
         fsm2s                  0        0        0.70   4        2       1.00       1       1       1.75   0        0        1.52     4         3      1.77
         fsm3comb               0        0        0.66   0        0       0.98       0       0       1.71   3        3        1.81     5         5      1.95
         gates4                 5        3        0.42   5        5       0.80       5       5       1.42   3        3        1.33     5         5      1.82
         popcount3              5        0        0.45   3        0       0.70       4       1       1.27   1        1        1.40     4         2      1.75
         lemmings1              0        0        0.88   2        2       1.38       0       0       1.85   0        0        1.51     5         3      1.77
         rule90                 3        3        0.76   2        1       1.09       2       2       1.54   3        1        1.49     5         5      1.65
         vector3                3        1        0.50   1        1       0.95       4       2       1.65   2        0        1.70     5         3      1.75



multi stage adder. After both submodules are designed and                            introducing a control module controller and a new adder
validated through self-validation, the LLM backtracks to the                         submodule ripple carry adder. Using the testbench, the LLM
root node and recognizes that they cannot produce a functional                       verifies that the revised design is correct, after which the final
adder. It then backtracks further to redefine the submodules,                        RTL code is collected and returned.




                                                                                 5
                       IV. E XPERIMENTS
   Our proposed method is compared with standard IO prompt-
ing and several common CoT prompting paradigms. To bet-
ter illustrate the versatility of our approach, we consider
four models. Two of them are general-purpose commercial
LLMs with strong code generation capabilities: ChatGPT-4
and DeepSeek-Coder-V2 [27]. The other two are domain-
specific open-source LLMs fine-tuned for Verilog generation:
RTLCoder [6] and Thakur [28]. 1 We utilized two NL2V
(natural language to Verilog code) benchmarks, RTLLM [10]
and VerilogEval-Human [8], for our experiments. VerilogEval-
Machine, due to its focus on circuit component connections
and truth tables, is not considered as it lacks the flexibility
for module decomposition. The key performance indicators
used for performance measurement are syntactic correctness,
functional correctness, the number of tokens consumed, first           Fig. 5: The token consumption comparison between different
pass rate (Pass@1) five pass rate (Pass@5), and the number             CoT paradigms for RTL generation.
of successful attempts in the five (#Pass@5).

A. Full Benchmark Experimental Results
                                                                       in hard cases. Hard cases are defined as those circuits for
  Table I presents the experimental results for pass@1 and             which the direct IO prompt failed in the functional pass@1
pass@5 across the entire dataset of two common academic                experiment of Table I. Due to space limitations, we only
benchmarks. The results indicate that our method effectively           present 8 cases each for RTLLM and VerilogEval-Human.
enhances model performance, both with the state-of-the-art             The results, as shown in Tables II and III, demonstrate that
model ChatGPT-4 and the open-source model Deepseek.                    our method encourages deeper model reasoning, leading to
We did not conduct experiments with different inference                improvements in both syntactic and functional correctness
paradigms for the domain-specific fine-tuned models (Thakur            compared to IO and other CoT modes. Moreover, token
and RTLCoder), as we observed a significant decline in their           consumption does not increase significantly; in some instances,
general instruction-following ability after fine-tuning. These         it is even lower than that of ToT and CoT-SC.
models were unable to comprehend and adhere to the reason-
ing paradigms for generation.                                          D. Token Consumption Evaluation
                                                                          To assess VeriBToT’s token overhead, we analyzed token
B. Ablation Study
                                                                       usage across reasoning paradigms, as shown in Fig. 5. The
   We removed the prompt for generating testbenches and self-          results indicate that although VeriBToT increases prompt token
validation based on them from the original VeriBToT, leaving           consumption, the tokens generated in context remain compara-
the LLM to reflect only on the Verilog generated for each              ble to those of CoT-SC and ToT. Given the additional context
node and determine whether backtracking is necessary, labeled          introduced—such as testbench code and natural language sub-
as VeriBToT- in Table I. The experimental results show a               module descriptions—the overall increase is relatively small.
significant performance drop, highlighting the effectiveness           This demonstrates the efficiency of the backtracking mecha-
of the self-validation backtracking mechanism we proposed.             nism in controlling token usage.
ToT can be seen as an ablation of VeriBToT-, where the
backtracking mechanism is removed and the model is forced                                    V. C ONCLUSION
to perform reasoning up to a predetermined depth. As another              In this paper, we present VeriBToT, a novel CoT architecture
ablation experiment, the results show that ToT performs worse          for automating RTL design with LLMs. Inspired by top-
than VeriBToT-, proving the effectiveness of the backtracking          down IC design and Design for Verification (DFV), VeriBToT
mechanism. This also partially demonstrates that excessive             enables self-decoupling and self-verification of thought nodes,
reasoning in LLMs may not necessarily improve perfor-                  represented through a BackTrack Tree. This improves the
mance [29], particularly when CoTs leads to performance                model’s understanding of Verilog design workflows, and our
degradation compared to IO in the case of RTLLM.                       experiments show the broad applicability of the approach. We
                                                                       believe VeriBToT can serve as a unified reasoning paradigm
C. Hard Case Experimental Results                                      for large-scale circuit generation with LLMs.
  We conducted a detailed case analysis on the function and
syntax pass rates (#pass@5) described in the RTLCoder pa-
per [6], specifically focusing on the relatively low performance
  1 Experiments were conducted between March 1–20, 2025.




                                                                   6
                              R EFERENCES                                            [20] S. Yao, D. Yu, J. Zhao, I. Shafran, T. Griffiths, Y. Cao, and
                                                                                          K. Narasimhan, “Tree of thoughts: Deliberate problem solving with large
 [1] L. Chen, Y. Chen, Z. Chu, W. Fang, T.-Y. Ho, Y. Huang, S. Khan,                      language models,” Advances in Neural Information Processing Systems,
     M. Li, X. Li, Y. Liang et al., “The dawn of ai-native eda: Promises and              vol. 36, 2024.
     challenges of large circuit models,” arXiv preprint arXiv:2403.07257,           [21] J. Long, “Large language model guided tree-of-thought,” arXiv preprint
     2024.                                                                                arXiv:2305.08291, 2023.
 [2] J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman,             [22] M. Besta, N. Blach, A. Kubicek, R. Gerstenberger, M. Podstawski,
     D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat et al., “Gpt-4                    L. Gianinazzi, J. Gajda, T. Lehmann, H. Niewiadomski, P. Nyczyk
     technical report,” arXiv preprint arXiv:2303.08774, 2023.                            et al., “Graph of thoughts: Solving elaborate problems with large
 [3] X. Hou, Y. Zhao, Y. Liu, Z. Yang, K. Wang, L. Li, X. Luo, D. Lo,                     language models,” in Proceedings of the AAAI Conference on Artificial
     J. Grundy, and H. Wang, “Large language models for software engi-                    Intelligence, vol. 38, no. 16, 2024, pp. 17 682–17 690.
     neering: A systematic literature review,” ACM Transactions on Software          [23] D. Huang, Q. Bu, and H. Cui, “Codecot and beyond: Learning to
     Engineering and Methodology, 2023.                                                   program and test like a developer,” arXiv preprint arXiv:2308.08784,
 [4] K. Chang, K. Wang, N. Yang, Y. Wang, D. Jin, W. Zhu, Z. Chen,                        2023.
     C. Li, H. Yan, Y. Zhou et al., “Data is all you need: Finetuning llms           [24] H. Wang, Z. Liu, S. Wang, G. Cui, N. Ding, Z. Liu, and G. Yu,
     for chip design via an automated design-data augmentation framework,”                “INTERVENOR: Prompting the Coding Ability of Large Language
     in Proceedings of the 61st ACM/IEEE Design Automation Conference,                    Models with the Interactive Chain of Repair,” in Findings of the
     2024, pp. 1–6.                                                                       Association for Computational Linguistics ACL 2024, 2024, pp. 2081–
 [5] X. Wang, G.-W. Wan, S.-Z. Wong, L. Zhang, T. Liu, Q. Tian,                           2107.
     and J. Ye, “ChatCPU: An Agile CPU Design and Verification                       [25] Z. Ni, Y. Li, N. Yang, D. Shen, P. Lv, and D. Dong, “Tree-of-code: A
     Platform with LLM,” in Proceedings of the 61st ACM/IEEE Design                       tree-structured exploring framework for end-to-end code generation and
     Automation Conference, ser. DAC ’24. New York, NY, USA:                              execution in complex task handling,” arXiv preprint arXiv:2412.15305,
     Association for Computing Machinery, 2024. [Online]. Available:                      2024.
     https://doi.org/10.1145/3649329.3658493                                         [26] Y. Zhou, R. Chen, X. Li, J. Wang, Z. Fang, B. Wang, W. Bai, Q. Cao,
 [6] S. Liu, W. Fang, Y. Lu, J. Wang, Q. Zhang, H. Zhang, and Z. Xie,                     and L. Wang, “Vtot: Automatic verilog generation via llms with tree
     “RTLCoder: Fully Open-Source and Efficient LLM-Assisted RTL Code                     of thoughts prompting,” in 2025 Design, Automation & Test in Europe
     Generation Technique,” IEEE Transactions on Computer-Aided Design                    Conference (DATE), 2025, pp. 1–2.
     of Integrated Circuits and Systems, pp. 1–1, 2024.                              [27] Q. Zhu, D. Guo, Z. Shao, D. Yang, P. Wang, R. Xu, Y. Wu, Y. Li, H. Gao,
 [7] M. DeLorenzo, A. B. Chowdhury, V. Gohil, S. Thakur, R. Karri, S. Garg,               S. Ma et al., “Deepseek-coder-v2: Breaking the barrier of closed-source
     and J. Rajendran, “Make every move count: Llm-based high-quality rtl                 models in code intelligence,” arXiv preprint arXiv:2406.11931, 2024.
     code generation using mcts,” arXiv preprint arXiv:2402.03289, 2024.             [28] S. Thakur, B. Ahmad, Z. Fan, H. Pearce, B. Tan, R. Karri, B. Dolan-
 [8] M. Liu, N. Pinckney, B. Khailany, and H. Ren, “Verilogeval: Evaluating               Gavitt, and S. Garg, “Benchmarking Large Language Models for
     large language models for verilog code generation,” in 2023 IEEE/ACM                 Automated Verilog RTL Code Generation,” 2022. [Online]. Available:
     International Conference on Computer Aided Design (ICCAD). IEEE,                     https://arxiv.org/abs/2212.11140
     2023, pp. 1–8.                                                                  [29] Z. Wu, L. Qiu, A. Ross, E. Akyürek, B. Chen, B. Wang, N. Kim,
 [9] S. Thakur, B. Ahmad, Z. Fan, H. Pearce, B. Tan, R. Karri, B. Dolan-                  J. Andreas, and Y. Kim, “Reasoning or reciting? exploring the
     Gavitt, and S. Garg, “Benchmarking Large Language Models for Auto-                   capabilities and limitations of language models through counterfactual
     mated Verilog RTL Code Generation,” in 2023 Design, Automation &                     tasks,” 2024. [Online]. Available: https://arxiv.org/abs/2307.02477
     Test in Europe Conference & Exhibition (DATE), 2023, pp. 1–6.
[10] Y. Lu, S. Liu, Q. Zhang, and Z. Xie, “Rtllm: An open-source benchmark
     for design rtl generation with large language model,” in 2024 29th Asia
     and South Pacific Design Automation Conference (ASP-DAC). IEEE,
     2024, pp. 722–727.
[11] Y. Zhao, D. Huang, C. Li, P. Jin, Z. Nan, T. Ma, L. Qi, Y. Pan, Z. Zhang,
     R. Zhang et al., “Codev: Empowering llms for verilog generation
     through multi-level summarization,” arXiv preprint arXiv:2407.10424,
     2024.
[12] S. Thakur, B. Ahmad, H. Pearce, B. Tan, B. Dolan-Gavitt, R. Karri,
     and S. Garg, “VeriGen: A Large Language Model for Verilog Code
     Generation,” ACM Trans. Des. Autom. Electron. Syst., vol. 29, no. 3,
     Apr. 2024. [Online]. Available: https://doi.org/10.1145/3643681
[13] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le,
     D. Zhou et al., “Chain-of-thought prompting elicits reasoning in large
     language models,” Advances in neural information processing systems,
     vol. 35, pp. 24 824–24 837, 2022.
[14] J. Li, G. Li, Y. Li, and Z. Jin, “Structured Chain-of-Thought Prompting
     for Code Generation,” ACM Trans. Softw. Eng. Methodol., Aug. 2024,
     just Accepted. [Online]. Available: https://doi.org/10.1145/3690635
[15] H. Le, H. Chen, A. Saha, A. Gokul, D. Sahoo, and S. Joty, “Codechain:
     Towards modular code generation through chain of self-revisions with
     representative sub-modules,” arXiv preprint arXiv:2310.08992, 2023.
[16] H. Kaeslin, Top-down digital VLSI design: from architectures to gate-
     level circuits and FPGAs. Morgan Kaufmann, 2014.
[17] F. Sforza, L. Battu, M. Brunelli, A. Castelnuovo, and M. Magnaghi,
     “A ”design for verification” methodology,” in Proceedings of the IEEE
     2001. 2nd International Symposium on Quality Electronic Design, 2001,
     pp. 50–55.
[18] A. Madaan, N. Tandon, P. Gupta, S. Hallinan, L. Gao, S. Wiegreffe,
     U. Alon, N. Dziri, S. Prabhumoye, Y. Yang et al., “Self-refine: Iter-
     ative refinement with self-feedback,” Advances in Neural Information
     Processing Systems, vol. 36, 2024.
[19] X. Wang, J. Wei, D. Schuurmans, Q. Le, E. Chi, S. Narang, A. Chowdh-
     ery, and D. Zhou, “Self-consistency improves chain of thought reasoning
     in language models,” arXiv preprint arXiv:2203.11171, 2022.




                                                                                 7
