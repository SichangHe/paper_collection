                                                 LLM- ENABLED B EHAVIOR D RIVEN D EVELOPMENT
                                             W ORKFLOW FOR F ORMALLY V ERIFIED H ARDWARE D ESIGNS


                                                      Luca Müller                        Qian Liu                           Rolf Drechsler
                                                      DFKI GmbH                     University of Bremen               University of Bremen/DFKI
                                                    Bremen, Germany                  Bremen, Germany                       Bremen, Germany
arXiv:2609.15318v1 [cs.AR] 14 Sep 2026




                                                                                             A BSTRACT
                                                  Recently, the use of Large Language Models (LLMs) for different tasks in the Electronic Design
                                                  Automation (EDA) life-cycle has been studied extensively, but an integrated view is lacking. Spec-
                                                  ifications are the foundation of this life-cycle, but they suffer from ambiguity when written in nat-
                                                  ural language, which especially affects the quality of LLM output. Formal specifications mitigate
                                                  these ambiguities, but they come with their own challenges. On the other hand, Controlled Natural
                                                  Language (CNL) specifications can serve as a middle-ground, reducing ambiguity while retaining
                                                  interpretability.
                                                  In this work, we propose an integrated view on the use of LLMs for EDA and establish an LLM-
                                                  enabled behavior driven hardware development workflow. We introduce and define Formal Verifi-
                                                  cation Gherkin Scenarios (FV Gherkin Scenarios), unlocking CNL specifications as the foundation
                                                  for formally verified hardware designs via Formal Property Verification (FPV). Experimental evalu-
                                                  ation shows that our workflow is able to outperform other established LLM-based methods by 2.48x
                                                  in functional correctness of generated Register Transfer Level (RTL) designs and by 2.54x in formal
                                                  coverage of generated assertions for FPV.

                                         Keywords Behavior Driven Development, Formal Verification, Large Language Models, Assertions, Coverage

                                         1   Introduction
                                         LLMs have been a major focus of research since their advent some years ago and are being explored throughout
                                         various EDA tasks [36], including RTL design and assertion generation for FPV [3]. While some works review
                                         multiple parts of the EDA flow, we identify the lack of an integrated view on the use of LLMs for these tasks [36, 15].
                                         Ideally, we envision an integrated workflow spanning the entire EDA life-cycle, where agentic LLMs autonomously
                                         carry out streamlined processes under human supervision to produce hardware designs that are formally verified to
                                         provide correctness guarantees. Specifications are the foundation of this workflow, serving as the ground-truth for
                                         expected hardware functionality and behavior. Today, specifications are typically written in natural language, which
                                         inherently carries ambiguity that can lead to unexpected results [37], especially for LLMs, whose output heavily
                                         depends on the input format [23]. Previous works aim to mitigate this ambiguity by utilizing techniques like Chain of
                                         Thought (COT) [34] prompting or Retreival Augmented Generation (RAG) [11] to guide Natural Language Processing
                                         (NLP) of LLMs, but work that targets the refinement of the specification itself is sparse [18]. In this regard, formal
                                         specifications are one potential solution, but they can be difficult for humans to understand [30], hindering proper
                                         audition of LLM-generated artifacts. CNL [17] specifications pose a promising alternative, serving as a middle-
                                         ground and reducing ambiguity with their structure while retaining easy human interpretability through their roots
                                         in natural language. Initial attempts at CNL specifications for hardware design have been explored, e.g., PROSER
                                         for temporal model checking [12] and Gherkin embedded in Behavior Driven Development (BDD) for hardware
                                         design [8]. However, practical adoption of CNL specifications remains scarce, which we attribute to limitations with
                                         respect to expressiveness beyond temporal model checking and generalizability to FPV respectively.
                                         In this work, we propose an integrated view on the use of LLMs for EDA with the establishment of an LLM-enabled
                                         behavior driven hardware development workflow. Our workflow directly incorporates FPV evaluation tools, open-
                                         ing an end-to-end path from design requirements to formally verified hardware designs. We introduce and define
                                         FV Gherkin Scenarios, unlocking the potential of CNL specifications as the foundation of this integrated flow. Ex-
          LLM-enabled Behavior Driven Development Workflow for Formally Verified Hardware Designs


perimental evaluation confirms the effectiveness of our proposed workflow, demonstrating that it outperforms other
established LLM-based methods on contemporary benchmarks in both RTL design and assertion generation tasks.
Specifically, we make the following contributions:
       • Present an LLM-enabled behavior driven hardware development workflow, integrating specification, RTL
         design, and formal verification stages.
       • Introduce FV Gherkin Scenarios as a specification baseline for RTL design and formal verification.
       • Demonstrate how the integration of LLMs into our workflow can increase productivity and improve verifica-
         tion quality.
The remainder of this work is structured as follows. Section 2 introduces preliminary information to keep this work
self-contained. Section 3 presents our proposed workflow and introduces FV Gherkin Scenarios. Section 4 experimen-
tally evaluates our workflow, demonstrating its effectiveness. Section 5 concludes this work and provides an outlook
for future research directions.

2     Preliminaries
2.1   Behavior Driven Development

BDD [10] was originally introduced as an extension to test driven development [4] in the software world. The core
idea is to start development from a specification of system behavior in a CNL, commonly referred to as Gherkin [13].
Multiple scenarios describe how the system behaves under a given set of conditions and are written in a Given-
When-Then style, structuring pre-conditions, trigger conditions, and post-conditions. Logical operators increase the
expressiveness of scenarios. In addition, a general feature overview and background information may be given. The
adoption of BDD for hardware design was initially proposed by Diepenbeck et al. [8].

                             Listing 1: Specification of ADD operation in Gherkin syntax
@add @arithmetic
  Scenario Outline : Specify ADD operation
    Given the reset signal rst is low
    And I have operand A = <A >
    And I have operand B = <B >
    And the opcode is set to 0000
    When a rising edge occurs on the clk signal
    Then the result should be < Expected_Result >
    And the zero flag should be < Zero_Flag >
    And the overflow flag should be < Overflow >
    And the negative flag should be < Negative_Flag >

       Examples :
       ...

Listing 1 shows an example of a Gherkin scenario that specifies the addition operation of an Arithmetic Logic Unit
(ALU). The tags prefixed with @ annotate the scenarios according to their purpose in the specification. The Scenario
Outline keywords specify that multiple values are tested by this scenario and are followed by a name for the scenario.
After this metadata, the scenario definition follows in Given-When-Then style. The first pre-condition specifies that the
reset signal should be low to ensure normal operation. With the help of the logical operand And, operand A is specified
to have concrete value <A> and operand B is specified to have concrete value <B>. Additionally, the opcode should
be set to constant 0000 for the addition operation. Next, the trigger condition is specified with keyword When, which
signifies that the operation should occur on a rising clock edge. Finally, post-conditions that should hold after the
trigger condition are specified with keyword Then. Here, expected values for all outputs are specified by placeholders
<Expected_Result>, <Zero_Flag>, <Overflow>, and <Negative_Flag>. After the definition of a scenario outline,
an example table defines test cases in the form of values for each of the defined placeholders. Scenarios in this
style are defined until the given hardware has been exhaustively specified. As evident from Listing 1, this implicit
specification by example data imposes limitations regarding the generalizability of Gherkin scenarios to assertions for
FPV. Another downside of the current BDD approach introduced in [8] is the high manual effort required to write
scenario definitions for the complete system behavior. To combat this, first attempts to integrate LLMs for BDD-based
hardware development were recently explored [9]. However, formal verification was not targeted, and no end-to-end
workflow was proposed here.


                                                           2
            LLM-enabled Behavior Driven Development Workflow for Formally Verified Hardware Designs


                                           Table 1: Comparison to related work
                     Work            [9]   [15]   [18]    [24]    [35]   [36]    [42]    [43]    Ours
                     Spec?           ✓      ×      ✓       ✓       ×      ×       ×       ×       ✓
                     RTL?            ✓      ✓      ×       ×       ×      ✓       ✓       ✓       ✓
                     FPV?             ×     ✓      ×       ✓       ✓      ×       ×       ×       ✓
                     Workflow?        ×     ×      ×       ✓       ✓      ×       ✓       ✓       ✓


2.2    Large Language Models for Electronic Design Automation

LLMs are transformer-based Generative Artificial Intelligence (GenAI) models designed to generate human lan-
guage and are based on the self-attention mechanism [33]. They are trained on very large amounts of data, which
makes them proficient not only in natural language, but also in several programming and Hardware Description Lan-
guages (HDLs) [40, 31]. LLMs take inputs in the form of prompts, and predict output text based on their training. On
the other hand, agentic LLMs, also referred to as agents, can reason, act, and interact, gaining autonomous access to
tools [28]. LLMs can either be run locally or accessed via an Application Programming Interface (API). Recently,
both agentic and non-agentic LLMs have been considered for the automation of several EDA tasks, including speci-
fications generation [18], generating RTL code [14, 43, 42, 27, 1], and generating test cases [41]. Regarding formal
verification, the generation of SystemVerilog Assertions (SVAs) in particular has been studied [38, 35, 21, 3, 24, 22].
Some works consider the use of LLMs in multiple EDA tasks, but mostly focus on specific case studies rather than
introducing a comprehensive workflow [36, 15]. To evaluate the effectiveness and quality of using LLMs in EDA,
several benchmarks have been proposed [38, 16, 29, 35, 39, 26, 19, 20, 25].
Table 1 compares our proposed workflow to selected related works. Specifically, we bridge the current research gap
with an integrated view through the establishment of an end-to-end workflow from specification to a formally verified
implementation.


3     Workflow

Our proposed LLM-enabled behavior driven hardware development workflow is presented in Figure 1. It features a
three agent setup, with specialized agents for specification ⃝,
                                                              1 RTL design⃝,    2 and formal verification⃝. 3 Each agent
produces an artifact based on its purpose in the workflow, which is conveyed through a system prompt. Agents can
reason, act, and interact with the help of respective LLM and tool calls at their disposal. By default, the workflow starts
with the input design requirements, which may be provided as plain text, in Markdown, or in PDF format. From it, the
Gherkin Agent ⃝  1 generates a specification consisting of FV Gherkin Scenarios. Based on this FV Gherkin Scenario,
the Verilog Agent ⃝ 2 produces an RTL implementation, while the SVA Agent ⃝        3 produces a set of SVAs. Finally, the
RTL implementation and the SVAs are combined into a formal testbench and evaluated by an FPV tool ⃝.             5 Alter-
natively, the workflow may take the RTL path (⃝     1 →⃝ 2 → ⃝) 4 or the SVA path (⃝    1 →⃝   3 → ⃝),
                                                                                                     6 where only RTL
implementation or SVAs are generated based on the Gherkin specification, respectively. In this case, the generated
artifacts are scored against a suitable reference provided externally. In the following, we provide further detail on the
three agents and introduce the concept of FV Gherkin Scenarios.

3.1    FV Gherkin Specification

In the first step of our workflow ⃝,
                                  1 design requirements in unstructured natural language are translated to a complete
Gherkin specification. In order to enable formal verification based on the generated specification, we introduce the
concept of FV Gherkin Scenarios.

Definition 1 A Formal Verification Gherkin Scenario (FV Gherkin Scenario) must fulfill the following three require-
ments:

      R1: Any signal value present in the scenario must not be implicitly represented by example data (i.e., no <>
          placeholders).
      R2: Any signal value referenced in the post-condition of a scenario must be represented as a symbolic value over
          signals occurring in the pre-condition, or as a constant.
      R3: The scenario must not contain an example table for the definition of test cases.


                                                            3
                LLM-enabled Behavior Driven Development Workflow for Formally Verified Hardware Designs


                                                                                       RTL Design
                                                                                                                            2

                                                                                         Generate                 Refine
                                                                                          Verilog                 Verilog
                                                                                                                                                 Golden SVAs/   RTL Scoring       4
                                                                                                                                                  Testbench



                     Specification                                                                   Verilog
                                                            1
                                                                                                     Agent                                                        Verification Tool
                                                                                                                                     RTL
                          Generate              Refine
                                                                                                                                Implementation
                          Gherkin               Gherkin                                    Lint                  Simulate
                                                                                          Verilog                  RTL                                          Evaluation        5




                                      Gherkin                                          Formal Verification
                                                                                                                            3                                     Formal Property
                                       Agent
                                                                                                                                                                  Verification Tool
  Design                                         Validate                Gherkin                                                                   Formal
                          Validate                                                       Generate                 Refine
Requirements                                     Gherkin               Specification                                                              Testbench
                           Formal                                                         SVAs                    SVAs
                         Compliance             Coverage                                                                                                        SVA Scoring       6




                                                                                                    SVA Agent                                                     Formal Property
       Legend
                                                                                                                                                                  Verification Tool
                                                                                                                                    SVAs
                                                                                            Lint                  Check
                 Agent        Agent          Agent                                         SVAs                SVA Coverage
                                                            Artifact   Tool
                             LLM Call       Tool Call


                                                                                                                                                 Golden RTL


 Figure 1: Our proposed LLM-enabled BDD workflow is modeled after the standard hardware development process.


Constant values may be required for specific situations, e.g., specifying reset behavior. In all remaining cases, signal
values in the post-condition should be symbolic, i.e., representing the complete value range admissive after the trigger
condition.
In our workflow, the Gherkin agent receives the design requirements as input and outputs a specification consisting
completely of FV Gherkin Scenarios. To achieve this, it can freely make the following calls in any order:

          • Generate Gherkin: Generate Gherkin scenarios based on design requirements and signal names extracted
            from them
          • Refine Gherkin: Add, remove, or modify scenarios based on feedback from other LLM calls
          • Validate Formal Compliance: LLM judge that checks previously generated scenarios for compliance to FV
            Gherkin syntax as given by Definition 1, providing feedback to the agent
          • Validate Gherkin Coverage: LLM judge that validates the coverage of all design requirements by currently
            generated scenarios, providing a quality score and feedback on potential coverage holes

The agent may choose to converge and commit the current Gherkin specification based on LLM judge feedback
received from calls to Validate Formal Compliance and Validate Gherkin Coverage.


                                                        Listing 2: FV Gherkin specification of ADD operation
                @add @arithmetic
                FV Scenario : Specify ADD operation
                Given the reset signal rst is low
                And I have operand A
                And I have operand B
                And the opcode is set to 0000
                When a rising edge occurs on the clk signal
                Then the result should be A + B
                And the zero flag should be 1 if A + B =0 , else 0
                And the overflow flag should be 1 if the MSB of A and B are equal and the
                    MSB of A + B is different else 0
                And the negative flag should be 1 if the MSB of A + B is 1 , else 0




                                                                                            4
               LLM-enabled Behavior Driven Development Workflow for Formally Verified Hardware Designs


     Example 1 Listing 2 shows an example of a FV Gherkin Scenario for the specification of the addition operation of
     an ALU. The FV Scenario keywords indicate a FV Gherkin Scenario, in contrast to the Scenario Outline to be filled
     with example data in the specification depicted in Listing 1. In the pre-condition, operands A and B are not specified
     by concrete values but simply given for use in the post-condition (R1). The trigger condition stays the same as in
     Listing 1, whereas the post-condition differs the most. In the FV Gherkin Scenario, all four outputs are represented
     by symbolic values (R2). For example, the result output is specified to be equal to A + B according to the addition
     operation. Instead of dedicating a separate scenario for each combination of binary flags, which can take only values
     0 or 1, they are also specified symbolically, e.g., the zero flag should be 1 if A + B = 0 and 0 otherwise. This symbolic
     definition circumvents the need for an example table (R3).

     3.2   RTL Design


                                   Listing 3: RTL design for the given Gherkin specification
 1      module alu (
 2      input wire [15:0] a ,
 3      input wire [15:0] b ,
 4      input wire [3:0] opcode ,
 5      input wire              clk ,
 6      input wire              rst ,
 7      output reg [15:0] result ,
 8      output reg              zero ,
 9      output reg              overflow ,
10      output reg              negative
11      );
12      ...
13      always @ * begin
14      comb_result      = 16 ’ d0 ;
15      comb_overflow = 1 ’ b0 ;
16      ...
17      case ( opcode )
18      4 ’ b0000 : begin // ADD
19      comb_result = a + b ;
20      comb_overflow = ( a [15] == b [15]) && ( comb_result [15] != a [15]) ;
21      end
22      ...
23      assign comb_zero           = ( comb_result == 16 ’ d0 ) ;
24      assign comb_negative = comb_result [15];
25
26      always @ ( posedge clk ) begin
27      if ( rst ) begin
28      ...
29      end else begin
30      result <= comb_result ;
31      zero <= comb_zero ;
32      overflow <= comb_overflow ;
33      negative <= comb_negative ;
34      end
35      end
36      endmodule


     The Verilog agent is responsible for RTL design ⃝,
                                                     2 receiving the previously created Gherkin specification as input and
     producing an RTL implementation covering this specification as output. To do so, it may freely make the following
     calls:

            • Generate Verilog: Generate Verilog code based on the Gherkin specification, pinned to signal declarations
            • Refine Verilog: Fix Verilog against feedback provided by other calls
            • Lint Verilog: Use an EDA tool to lint the currently generated Verilog and return feedback on potential syntax
              errors


                                                                5
               LLM-enabled Behavior Driven Development Workflow for Formally Verified Hardware Designs


            • Simulate RTL: If a reference testbench is available, use an EDA tool to run it and return feedback on semantic
              mismatches

     The Verilog agent converges and commits the RTL implementation based on deterministic tool feedback from Lint
     Verilog and Simulate RTL calls.

     Example 2 Listing 3 shows an excerpt of the RTL design created from the Formal Verification Gherkin Specifica-
     tion (FV Gherkin Specification) for our running ALU example. The design starts with the module declaration, con-
     taining all inputs and outputs specified in the Gherkin specification, taken from the design requirements. After some
     default assignments, operations are defined based on the given opcode, modeled after the specific Gherkin scenario
     that describes its behavior. As can be seen, the result and overflow behavior are directly mapped from the example
     scenario given in Listing 2. The zero and negative flags can be mapped regardless of the operation, so this behavior
     is implemented after the case selection on the opcode. Finally, the module outputs are assigned synchronously on a
     rising clock edge, as given in the specification.

     As can be observed in Example 2, individual Gherkin scenarios do not necessarily need to be specified as one coherent
     code block, but may be split across the design. The important aspect of mapping the Gherkin specification to an RTL
     design is that all scenarios are mapped, and thus the complete behavior of the hardware is implemented.

     3.3   Formal Property Verification

     To enable FPV in our workflow, the SVA agent ⃝   3 produces assertions based on the Gherkin specification received as
     input. It reaches a set of output SVAs with the help of the following calls:

            • Generate SVAs: Generate SVAs from the FV Gherkin Specification and signal declarations extracted from
              previously generated or golden RTL
            • Refine SVAs: Refine SVAs against feedback received from other calls
            • Lint SVAs: Elaborate SVAs and a reference RTL with an EDA tool and receive feedback on lint errors
            • Check SVA Coverage: Evaluate SVA coverage with an FPV tool and receive feedback on coverage holes and
              failing properties

     The SVA agent converges and commits the set of SVAs based on deterministic tool feedback received from calls to
     Lint SVA and Check SVA Coverage.


                                       Listing 4: SVA for the given Gherkin specification
 1   // - - - - - - - - - - - - - - - - - - -
 2   // Formal Scenario : Perform ADD operation
 3   // - - - - - - - - - - - - - - - - - - -
 4   property p_add ;
 5      @ ( posedge clk ) disable iff ( rst )
 6          ( opcode == 4 ’ b0000 ) | - > ##1
 7              ( result            == ( a + b ) ) &&
 8              ( zero              == (( a + b ) == 16 ’ b0 ) ) &&
 9              ( overflow == (( a [15] == b [15]) && ( result [15] != a [15]) ) ) &&
10              ( negative == result [15]) ;
11   endproperty
12   assert property ( p_add ) else $error ( " ADD failed " ) ;



     Example 3 Listing 4 shows an asserted property which verifies the specification of the addition operation given in
     Listing 2. The property directly reflects the structure of the FV Gherkin Scenario with an overlapping implication
     operator |-> where the antecedent defines the pre-condition and the consequent defines the post-condition. For the
     antecedent, the opcode is set to 0000 according to the pre-condition of the Gherkin scenario to reflect the addition
     operation. The trigger condition of a rising clock edge is achieved by a combination of a clocking event @(posedge
     clk) and a cycle delay ##1. All post-conditions of the FV Gherkin Scenario are directly mapped in the consequent and
     connected with logical conjunctions &&. Finally, the property is asserted with a fitting error message in case it cannot
     be satisfied.


                                                                6
               LLM-enabled Behavior Driven Development Workflow for Formally Verified Hardware Designs


After the SVA agent converges, our end-to-end workflow directly carries out evaluation with the help of an FPV tool ⃝.
                                                                                                                    5
To this end, the generated set of assertions is merged into a formal testbench together with the RTL implementation
produced by the Verilog agent. This formal testbench is then executed by the FPV tool and filed for further inspection
and analysis.

4         Experimental Evaluation
We evaluate our workflow on two sets of experiments, each using separate benchmarks and comparing against differ-
ent baselines. Firstly, we run the RTL path (Requirements → FV Gherkin Specification → RTL Implementation) to
evaluate the quality of RTL designs generated based on the FV Gherkin Specification. Secondly, in our main experi-
ment, we run the SVA path (Requirements → FV Gherkin Specification → SVAs) to evaluate the quality of generated
SVAs and the suitability of FV Gherkin Specifications for FPV. We implement our workflow in Python [32] and use
Cadence Xcelium [6] for all RTL simulation tasks and Cadence JasperGold [5] for all FPV tasks. All evaluations are
strictly pass@1 [7] and metrics are retrieved using the aforementioned EDA tools. We use the recently released Claude
Sonnet 5 [2] as the model for all workflow runs and all baselines where applicable. For both sets of experiments, we
first pick a benchmark that fits our workflow structure, features sufficiently complex designs at an acceptable scale
and has baselines available that we can compare against. Then, we pick suitable baselines that are scorable against the
previously selected benchmarks, must be re-scorable to deal with LLM non-determinism, and are model-adaptable to
avoid bias by the choice of LLM in the best case. In the following sections, we provide rationale on the benchmarks
and baselines we pick to obtain the most realistic evaluation of our workflow. Chosen benchmarks and baselines are
highlighted in boldface. We note that the given publication dates refer to the publication of peer-reviewed works where
applicable, and else, the first mention in an otherwise published work. All evaluation artifacts are made available.1

4.1        RTL Design with our BDD Workflow

4.1.1       Benchmarks & Baselines

                                               Table 2: RTL Path Benchmarks
                                                            Complexity of                     Baselines
                       Benchmark             Publication                        Scale
                                                                Designs                       Available?
                       RTLLM 2.0 [19]         2025-04       Single-Module   Medium (50)           •
                                                          Non-Commercial+
                       CVDP [26]              2025-06                       Medium (63)*           ⊙
                                                              Commercial
                       VerilogEval v2 [25]    2025-10       Single-Module    Large (156)           •
                                                             Self-Contain+
                       ChipBench [39]         2026-01                       Medium (45)            •
                                                            Hierarchical+IP
                                                    *Agentic CID03+CID05
                                                 •: Yes    ⊙: Partial ◦: No

Table 2 compares four popular benchmarks targeted at RTL design. We choose VerilogEval v2 as the largest scale
benchmark that many baselines evaluate on, featuring over 150 designs to get a large sample size. To cover more
complex hierarchical and Intellectual Property (IP) designs, we pick ChipBench. We prefer it over CVDP, because it
was published more recently, reports baseline evaluations and is simpler to integrate and re-score against. All baselines
we pick also provide testbenches that can be scored against a golden reference RTL with Xcelium.
                                                 Table 3: RTL Path Baselines
                                                                                        Model      VerilogEval/
                  Baseline            Publication          Type        Re-Score?
                                                                                      Adaptable?   ChipBench
                  VerilogCoder [14]     2025-02          Workflow             •*          ◦             •/◦
                  CodeV [42]            2025-08            Model              •          N/A           •/⊙**
                  HDLCoRe [27]          2025-08          Workflow             ◦           •             ◦/◦
                  RTL++ [1]             2025-08            Model              ◦          N/A            •/◦
                  MAGE [43]             2025-09      Agentic Workflow         •           •            •/⊙
                                          *Trivial, ships artifacts   **Custom Adapter
                                                  •: Yes      ⊙: Partial ◦: No

The baselines available for our RTL experiment are compared in Table 3. VerilogCoder ships all generated artifacts
for VerilogEval v2, making it trivial to re-score. CodeV is chosen as a fine-tuned model, making integration with
      1
          https://github.com/lucamu/LLM-BDD-Workflow-Evaluation-Artifacts


                                                                  7
           LLM-enabled Behavior Driven Development Workflow for Formally Verified Hardware Designs


additional benchmarks, especially ChipBench, easier. For HDLCoRe and RTL++, unfortunately, no implementation
is openly available for re-scoring. As an additional baseline, we compare against MAGE, an agentic workflow that was
recently released, scores VerilogEval, and is reported on by ChipBench. We re-run or re-score all baselines with the
same Xcelium flow we use for our workflow, using Sonnet-5 where applicable.

4.1.2    Experimental Results

                                               Table 4: RTL Path Results
              Benchmark      Method              Source                      Syntax            Functional
                             VerilogCoder        Re-Score                96.6% (142/147)*   90.4% (141/156)
                             VerilogCoder
                                                 Self-Reported [14]                     -            94.2%
                             (GPT-4 Turbo)
                             CodeV                Re-Run                   85.3% (133/156)  35.9% (56/156)
              VerilogEval v2
                             CodeV (pass@1)       Self-Reported [42]**                   -          59.2%
                             MAGE (Sonnet-5)      Re-Run               99.2% (127/128)*** 76.3% (119/156)
                             MAGE                 Self-Reported [43]                     -          95.7%
                             BDD Workflow         Ours                     98.7% (154/156) 89.1% (139/156)
                             CodeV                Re-Run                     82.2% (37/45)     13.3% (6/45)
                                                  Reported
                             Opus 4.5 (pass@1)                                           -          30.7%
                                                  (LLM) [39]
              ChipBench                           Reported
                             MAGE                                                        -          37.4%
                                                  (Workflow) [39]
                             MAGE (Sonnet-5) Re-Run                     95.8% (23/24)**** 31.1% (14/45)%
                             BDD Workflow         Ours                       95.6% (43/45)   31.1% (14/45)
                                 *9 designs ship no design **CodeV-Verilog-QC (best)
                         ***Remaining 28 produced an error ****Remaining 21 produced an error

Table 4 shows the results of the experimental evaluation of our RTL path. Column Syntax reports the number of
designs which have valid Verilog syntax and column Functional reports the number of designs which pass the testbench
provided by the benchmark with 100% pass rate. For the VerilogEval v2 benchmark, our proposed workflow is able
to produce valid syntax on 154 out of 156 (98.7%) of designs, being outperformed only by MAGE on Sonnet-5,
which, as a caveat, produced errors on 28 designs. As for the functional pass rate on the provided testbench, our
workflow reaches almost 90% and performs similar to our highest re-score on VerilogCoder (90.4%), a difference
which may be neglected due to noise in the LLM generation. Compared to our CodeV re-run, our proposed workflow
improves the functional pass rate by 2.48x. Looking at the ChipBench benchmark, our workflow once again scores
very high on syntax, with over 95%. Regarding the functional pass rate, it performs the same as the MAGE re-run
on Sonnet-5 and outperforms both CodeV and the best stand-alone LLM reported in [39]. Overall, the results show
that our proposed workflow performs better than or on-par with previously released open-source baselines, indicating
a general suitability of FV Gherkin Specifications for RTL design.

4.2     SVA Generation for FPV with our BDD Workflow

4.2.1    Benchmarks & Baselines

                                             Table 5: SVA Path Benchmarks
                                                            Complexity of                             Baselines
         Benchmark             Publication    Req→SVA?                             Scale
                                                                Designs                               Available?
         AssertLLM [38]        2025-03          •             Industry IP        Small (20)               •
         AssertionBench [29]   2025-04          ◦*              Various         Large (100)               ⊙
         FVEval [16]           2025-05          ⊙**          Unit-Level IP     Medium (79)***             ⊙
                                                          Non-Commercial+
         CVDP [26]             2025-06          ◦****                        Medium (30)*****             ⊙
                                                             Commercial
         AssertLLM2[35]        2026-05          •             Industry IP       Medium (83)                   •
                           *RTL→SVA    **Assertion Description→SVA ***NL2SVA-Human
                                    ****Test Plan→SVA       *****Agentic CID14
                                           •: Yes    ⊙: Partial ◦: No

Suitable benchmarks for the SVA path are more limited, as can be seen in Table 5. Available benchmarks greatly
differ in the task they evaluate: AssertionBench considers RTL code for SVA generation, FVEval provides small
assertion descriptions that are translated to SVA one-by-one, and CVDP supplies a testplan for SVA generation. On


                                                            8
          LLM-enabled Behavior Driven Development Workflow for Formally Verified Hardware Designs


the other hand, AssertLLM and AssertLLM2 both benchmark SVA generation based on design specifications, provide
sufficiently complex designs, and have baselines that evaluate on them. Both of them also provide a golden RTL
against which generated SVAs can be evaluated using JasperGold.

                                             Table 6: SVA Path Baselines
                                                                                         Model        AssertLLM/
        Baseline                     Publication         Type        Re-Score?
                                                                                       Adaptable?     AssertLLM2
        ChIRAAG [21]                   2024-09        Workflow              •              ⊙              ◦/◦
        AssertionForge [3]             2025-08        Workflow              •              •              •/◦
        LISA [24]                      2025-08         Model                ◦              ◦              ◦/◦
        AssertLLM2 Plain [35]          2026-05        Method                •              •              ◦/•*
                                               *Shipped with Benchmark
                                              •: Yes  ⊙: Partial ◦: No


Table 6 compares potential baselines for the SVA path. ChIRAAG is publicly available but generates SVAs based on
on hand-crafted specifications, while LISA is not available for re-scoring at all. For AssertLLM, AssertionForge is a
very suitable candidate, as it scores directly on it and is also available to re-run. AssertLLM2 was only released very
recently, and thus, no external baselines natively support it yet. Instead, we make use of the AssertLLM2 Plain method
as a baseline, which is provided alongside the benchmark. Both baselines are re-run on the same model and with the
same evaluation flow as our proposed workflow using JasperGold.


4.2.2   Experimental Results


                                              Table 7: SVA Path Results

  Benchmark         Method                                      Source                        Proof    COI    Formal
                    AssertionForge (Sonnet-5)                   Re-Run                       19.0%    63.0%    36.7%
  AssertLLM         AssertionForge (GPT-4o)                     Self-Reported [3]*           18.6%    96.2%         -
                    BDD Workflow                                Ours                         43.2%    96.8%    44.1%
                    AssertLLM2 Plain (Sonnet-5)**               Re-run                       67.8%    99.9%    15.5%
                                                                Self-Reported
  AssertLLM2        AssertLLM2 Plain (Sonnet 4.5)                                            55.3%    65.7%   22.4%
                                                                (Average) [35]
                    BDD Workflow**                              Ours                         43.1%    92.9%   39.5%
                           *Extrapolated from reported five design subset       **23 design subset


The results of the experimental evaluation of our SVA path are shown in Table 7. For the AssertLLM2 benchmark, we
score a subset of 23 designs, with at least one design per category [35]. Column Proof reports the percentage of gener-
ated assertions that are successfully proven for the given design, column COI reports the Cone of Influence (COI) cov-
erage, and column Formal reports the formal coverage computed by JasperGold. For the AssertLLM benchmark, our
workflow performs best regarding proof rate, with a 2.3x improvement over AssertionForge for both the self-reported
and re-run results. As for formal coverage, our workflow performs best across both categories and baselines, where
AssertionForge only self-reports COI coverage. On the AssertLLM2 benchmark, proof percentage is very consistent
compared to AssertLLM for our workflow. COI coverage for our workflow is also very high, at over 90%. Formal
coverage is where our proposed workflow achieves the best results compared to the baselines, performing 2.54x better
than the re-run AssertLLM2 Plain. In total, our evaluation demonstrates the capability of FV Gherkin Specifications
to serve as the foundation for FPV, scoring very high across both COI and formal coverage.
Across the two sets of experiments, our overall results demonstrate the suitability of our proposed end-to-end workflow
to offer an integrated view on the use of LLMs for EDA. For both RTL design and assertion generation, our workflow
is able to outperform other established LLM-based methods in quality metrics such as functional correctness and
coverage. We acknowledge that some baselines were able to achieve results that are similar to those of our workflow,
but we point out that the integration of enhancements like COT prompting and RAG, or advanced techniques from
these baselines into our workflow may lead to further improvements, e.g. utilizing additional agents for RTL design
like MAGE or constructing knowledge graphs for assertion generation like AssertionForge.


                                                            9
          LLM-enabled Behavior Driven Development Workflow for Formally Verified Hardware Designs


5   Conclusion
In this work, we proposed an integrated view on the use of LLMs for EDA through the establishment of an LLM-
enabled behavior driven hardware development workflow. We introduced FV Gherkin Scenarios for CNL specifica-
tions as the foundation for the development of formally verified hardware designs. By experimental evaluation, we
confirmed that our proposed workflow can outperform established LLM-based methods for both RTL design and FPV
based on FV Gherkin Specifications. Future work may investigate whether the integration of further options for the
three agents leads to additional improvements of our workflow.

Acknowledgments
This research has been supported by the German Ministry for Research, Technology and Space (BMFTR) with project
ExaVerse (grant number 01IW25003).

References
 [1] M. Akyash, K. Azar, and H. Kamali. RTL++: Graph-enhanced LLM for RTL code generation. In 2025 IEEE
     International Conference on LLM-Aided Design (ICLAD), pages 44–50. IEEE, 2025.
 [2] Anthropic. Claude Sonnet 5. https://www.anthropic.com/claude/sonnet, 2026.
 [3] Y. Bai, G. B. Hamad, S. Suhaib, and H. Ren. Assertionforge: Enhancing formal verification assertion generation
     with structured representation of specifications and RTL. In 2025 IEEE International Conference on LLM-Aided
     Design (ICLAD), pages 85–92. IEEE, 2025.
 [4] K. Beck. Test-driven development: by example. Addison-Wesley Professional, 2003.
 [5] Cadence.                      JasperGold.                  https://www.cadence.com/en_US/home/tools/
     system-design-and-verification/formal-and-static-verification.html, 2026.
 [6] Cadence.                        Xcelium.                   https://www.cadence.com/en_US/home/tools/
     system-design-and-verification/simulation-and-testbench-verification/
     xcelium-simulator.html, 2026.
 [7] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. D. O. Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brock-
     man, et al. Evaluating large language models trained on code. arXiv:2107.03374, 2021.
 [8] M. Diepenbeck, U. Kühne, M. Soeken, D. Grosse, and R. Drechsler. Behaviour driven development for hardware
     design. IPSJ Transactions on System and LSI Design Methodology, 11:29–45, 2018.
 [9] R. Drechsler and Q. Liu. LLM-based behaviour driven development for hardware design, 2025.
[10] M. S. Farooq, U. Omer, A. Ramzan, M. A. Rasheed, and Z. Atal. Behavior driven development: A systematic
     literature review. IEEE access, 11:88008–88024, 2023.
[11] Y. Gao, Y. Xiong, X. Gao, K. Jia, J. Pan, Y. Bi, Y. Dai, J. Sun, M. Wang, and H. Wang. Retrieval-augmented
     generation for large language models: A survey. arXiv:2312.10997, 2023.
[12] C. Grover, A. Holt, E. Klein, and M. Moens. Designing a controlled language for interactive model checking. In
     Proceedings of the third international workshop on controlled language applications, pages 29–30, 2000.
[13] A. Hellesoy, S. Tooke, and M. Wynne. The cucumber book: behaviour-driven development for testers and
     developers. 2017.
[14] C.-T. Ho, H. Ren, and B. Khailany. VerilogCoder: Autonomous verilog coding agents with graph-based planning
     and abstract syntax tree (AST)-based waveform tracing tool. In Proceedings of the AAAI Conference on Artificial
     Intelligence, volume 39, pages 300–307, 2025.
[15] C. K. Jha, M. Hassan, K. Qayyum, S. Ahmadi-Pour, K. Xu, R. Qiu, J. Blocklove, L. Collini, A. Nakkab,
     U. Schlichtmann, G. Li Zhang, R. Karri, B. Li, S. Garg, and R. Drechsler. Large language models (LLMs)
     for verification, testing, and design. In 2025 IEEE European Test Symposium (ETS), pages 1–10, 2025.
[16] M. Kang, M. Liu, G. B. Hamad, S. M. Suhaib, and H. Ren. FvEval: Understanding language model capabilities
     in formal verification of digital hardware. In 2025 Design, Automation & Test in Europe Conference (DATE).
     IEEE, 2025.
[17] T. Kuhn. A survey and classification of controlled natural languages. Computational linguistics, 40(1):121–170,
     2014.


                                                        10
          LLM-enabled Behavior Driven Development Workflow for Formally Verified Hardware Designs


[18] M. Li, W. Fang, Q. Zhang, and Z. Xie. SpecLLM: Exploring generation and review of vlsi design specification
     with large language model. In 2025 International Symposium of Electronics Design Automation (ISEDA), pages
     749–755, 2025.
[19] S. Liu, Y. Lu, W. Fang, M. Li, and Z. Xie. OpenLLM-RTL: Open dataset and benchmark for LLM-aided design
     RTL generation. In Proceedings of the 43rd IEEE/ACM International Conference on Computer-Aided Design,
     ICCAD ’24, 2025.
[20] Y. Lu, S. Liu, Q. Zhang, and Z. Xie. RTLLM: An open-source benchmark for design RTL generation with
     large language model. In 2024 29th Asia and South Pacific Design Automation Conference (ASP-DAC), pages
     722–727, 2024.
[21] B. Mali, K. Maddala, V. Gupta, S. Reddy, C. Karfa, and R. Karri. ChIRAAG: Chatgpt informed rapid and
     automated assertion generation. In 2024 IEEE Computer Society Annual Symposium on VLSI (ISVLSI), pages
     680–683. IEEE, 2024.
[22] L. Müller, C. Kumar Jha, B. Arlt, M. Hassan, and R. Drechsler. Modular end-to-end pipeline for formal property
     verification using large language models. In 2026 IEEE Computer Society Annual Symposium on VLSI (ISVLSI).
     IEEE, 2026.
[23] L. Ngweta, K. Kate, J. Tsay, and Y. Rizk. Towards llms robustness to changes in prompt format styles. In
     Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational
     Linguistics: Human Language Technologies (Volume 4: Student Research Workshop), pages 529–537, 2025.
[24] S. Paul, A. Banerjee, S. Ghosh, S. Surendran, and R. K. Gajavelly. LISA: LLM informed systemverilog asser-
     tion generation with RAG and chain-of-thought. In 2025 IEEE Computer Society Annual Symposium on VLSI
     (ISVLSI). IEEE, 2025.
[25] N. Pinckney, C. Batten, M. Liu, H. Ren, and B. Khailany. Revisiting VerilogEval: A year of improvements in
     large-language models for hardware code generation. 30(6), Oct. 2025.
[26] N. Pinckney, C. Deng, C.-T. Ho, Y.-D. Tsai, M. Liu, W. Zhou, B. Khailany, and H. Ren. Comprehensive Verilog
     Design Problems: A next-generation benchmark dataset for evaluating large language models and agents on RTL
     design and verification, 2025.
[27] H. Ping, S. Li, P. Zhang, A. Cheng, S. Duan, N. Kanakaris, X. Xiao, W. Yang, S. Nazarian, A. Irimia, et al.
     HDLCoRe: A training-free framework for mitigating hallucinations in LLM-generated HDL. In 2025 IEEE
     International Conference on LLM-Aided Design (ICLAD), pages 108–116. IEEE, 2025.
[28] A. Plaat, M. van Duijn, N. Van Stein, M. Preuss, P. van der Putten, and K. J. Batenburg. Agentic large language
     models, a survey. Journal of Artificial Intelligence Research, 84, 2025.
[29] V. Pulavarthi, D. Nandal, S. Dan, and D. Pal. AssertionBench: A benchmark to evaluate large-language models
     for assertion generation. In Findings of the Association for Computational Linguistics: NAACL 2025, pages
     8058–8065, 2025.
[30] C. F. Snook. Exploring the barriers to formal specification. PhD thesis, University of Southampton, 2001.
[31] S. Thakur, J. Blocklove, H. Pearce, B. Tan, S. Garg, and R. Karri. Autochip: Automating HDL generation using
     LLM feedback. arXiv:2311.04887, 2023.
[32] G. Van Rossum and F. L. Drake. Python 3 Reference Manual. CreateSpace, Scotts Valley, CA, 2009.
[33] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin. Attention
     is all you need. Advances in neural information processing systems, 30, 2017.
[34] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou, et al. Chain-of-thought prompting
     elicits reasoning in large language models. Advances in neural information processing systems, 35:24824–24837,
     2022.
[35] Y. Wu, W. Fang, J. Wang, W. Li, Z. Guo, and Z. Xie. AssertLLM2: A comprehensive LLM benchmark for
     assertion generation from design specifications, 2026.
[36] K. Xu, D. Schwachhofer, J. Blocklove, I. Polian, P. Domanski, D. Pflüger, S. Garg, R. Karri, O. Sinanoglu,
     J. Knechtel, Z. Zhao, U. Schlichtmann, and B. Li. Large language models (llms) for electronic design automation
     (eda) : Special session paper. In 2025 IEEE 38th International System-on-Chip Conference (SOCC), pages 1–6,
     2025.
[37] A. Yadav, A. Patel, and M. Shah. A comprehensive review on resolving ambiguities in natural language process-
     ing. AI Open, 2:85–92, 2021.


                                                        11
          LLM-enabled Behavior Driven Development Workflow for Formally Verified Hardware Designs


[38] Z. Yan, W. Fang, M. Li, M. Li, S. Liu, Z. Xie, and H. Zhang. AssertLLM: Generating hardware verification
     assertions from design specifications via Multi-LLMs. In Proceedings of the 30th Asia and South Pacific Design
     Automation Conference, ASPDAC ’25, 2025.
[39] Z. Yu, C. Zhou, Y. Lin, H. Zhang, H. Ye, J. Cui, Z. Pan, J. Zhao, and Y. Ding. ChipBench: A next-step benchmark
     for evaluating LLM performance in AI-aided chip design, 2026.
[40] Y. Zhang, Y. Pan, Y. Wang, and J. Cai. Pybench: Evaluating LLM agent on various real-world coding tasks.
     arXiv:2407.16732, 2024.
[41] Z. Zhang, B. Szekely, P. Gimenes, G. Chadwick, H. McNally, J. Cheng, R. Mullins, and Y. Zhao. Llm4dv: Using
     large language models for hardware test stimuli generation. In 2025 IEEE 33rd Annual International Symposium
     on Field-Programmable Custom Computing Machines (FCCM), pages 133–137. IEEE, 2025.
[42] Y. Zhao, D. Huang, C. Li, P. Jin, M. Song, Y. Xu, Z. Nan, M. Gao, T. Ma, L. Qi, et al. CodeV: Empowering
     LLMs with HDL generation through multi-level summarization. IEEE Transactions on Computer-Aided Design
     of Integrated Circuits and Systems, 2025.
[43] Y. Zhao, H. Zhang, H. Huang, Z. Yu, and J. Zhao. MAGE: A multi-agent engine for automated RTL code
     generation. In 2025 62nd ACM/IEEE Design Automation Conference (DAC). IEEE, 2025.




                                                        12
