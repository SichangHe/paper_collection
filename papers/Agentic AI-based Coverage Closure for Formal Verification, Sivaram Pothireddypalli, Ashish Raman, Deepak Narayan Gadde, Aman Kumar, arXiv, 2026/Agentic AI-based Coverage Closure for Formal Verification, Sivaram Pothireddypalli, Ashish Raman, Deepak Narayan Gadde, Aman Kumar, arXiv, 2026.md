                                              To appear at the IEEE International Conference on Intelligent Processing, Hardware, Electronics, and Radio Systems
                                                                            (CIPHER), February 13-15, 2026, NIT Jalandhar, India


                                                 Agentic AI-based Coverage Closure for Formal
                                                                  Verification
                                                                Sivaram Pothireddypalli1 , Ashish Raman2 , Deepak Narayan Gadde3 , Aman Kumar1
                                                                                          1 Infineon Technologies India Private Limited, India
                                                                              2 Dr. B R Ambedkar National Institute of Technology Jalandhar, India
                                                                                     3 Infineon Technologies Dresden AG & Co. KG, Germany




                                            Abstract—Coverage closure is a critical requirement in Inte-                     overcome the above challenge, this study explores the applica-
                                         grated Chip (IC) development process and key metric for verifi-                     tion of LLM-enabled GenAI, which demonstrates contextual
arXiv:2603.03147v2 [cs.AI] 24 Mar 2026




                                         cation sign-off. However, traditional exhaustive approaches often                   reasoning and can translate natural-language descriptions into
                                         fail to achieve full coverage within project timelines. This study
                                         presents an agentic AI-driven workflow that utilizes Large Lan-                     executable artifacts. This approach includes context-sensitive
                                         guage Model (LLM)-enabled Generative AI (GenAI) to automate                         query solutions and automated code generation [4], [5]. Both
                                         coverage analysis for formal verification, identify coverage gaps,                  formal specification documents and design artifacts, including
                                         and generate the required formal properties. The framework accel-                   RTL code, cover properties and assertions that are inherently
                                         erates verification efficiency by systematically addressing coverage                textual. Therefore, they are well-suited for language-based
                                         holes. Benchmarking open-source and internal designs reveals
                                         a measurable increase in coverage metrics, with improvements                        processing by LLMs.
                                         correlated to the complexity of the design. Comparative analysis                       Recent advances in agentic AI frameworks have automated
                                         validates the effectiveness of this approach. These results highlight               key aspects of hardware design and verification. These frame-
                                         the potential of agentic AI-based techniques to improve formal                      works can interpret natural language specifications, generate
                                         verification productivity and support comprehensive coverage                        RTL code, and perform design verification. One automatic
                                         closure.
                                            Index Terms—Agentic AI, LLM, Hardware Design, Formal                             assertion-generation framework uses LLMs to generate as-
                                         Verification, Coverage                                                              sertions by analyzing natural-language specifications for each
                                                                                                                             architectural signal. This framework incorporates three cus-
                                                                     I. I NTRODUCTION                                        tomized LLMs to extract structural specifications, map signal
                                            Hardware design verification plays a vital role in the Very                      definitions, and generate assertions. This approach provides
                                         Large Scale Integration (VLSI) development cycle, ensur-                            substantial advantages for preventing bugs during design and
                                         ing that the implemented design accurately meets its in-                            detecting bugs during verification [6]. Another framework that
                                         tended specifications. The most widely used methods in in-                          uses a Multi-Agent System (MAS) to support collaborative
                                         dustry are simulation-based verification and formal methods.                        code generation, iterative RTL refinement, and dynamic prop-
                                         In simulation-based verification, input stimuli are applied to                      erty generation for language-based processing by LLMs. In
                                         the design, and the resulting outputs are analyzed to verify                        such an automated environment, specialized agents are capable
                                         functional correctness. This method takes significant time to                       of generating RTL codes and interfacing with sophisticated
                                         time to verify Register Transfer Level (RTL) designs and also                       Electronic Design Automation (EDA) tools for validation and
                                         risks omitting corner cases [1]. Formal methods are an alter-                       verification [7]. Similarly, Saarthi (ScalAble ARTificial and
                                         native to simulation, in which RTL designs are checked for all                      Human Intelligence) is a fully autonomous Artificial Intelli-
                                         possible input cases using mathematical modeling. In a formal                       gence (AI) formal verification engineer designed to verify RTL
                                         environment, there are various tasks, such as planning, property                    designs end-to-end through an agentic workflow [8]. Saarthi
                                         development, proof execution, and formal sign-off. During the                       uses agentic reasoning patterns in conjunction with human
                                         property development phase, SystemVerilog assertions are used                       supervision to achieve robust verification results. Starting with
                                         to verify the design’s functional correctness. In addition, it has                  the initial design specification, it sequentially handles verifica-
                                         the potential to simplify the verification process and improve                      tion planning, assertion generation, property proving, Counter
                                         the overall productivity [2].                                                       Examples (CEXs) analysis, and formal coverage evaluation to
                                            The entire process of verification even using the traditional                    support verification sign-off.
                                         exhaustive methods of study takes up to 60 % of the project                            Even with these automated assertion generation and verifi-
                                         time [3]. The primary feature of the effort is the realization                      cation execution runs, existing workflows frequently result in
                                         of functional coverage because the coverage is often used to                        residual coverage gaps. This work introduces an agentic AI
                                         measure the progress in verification. It shows that the pre-                        method, building on Saarthi, to address the coverage gaps.
                                         determined verification plan is to be implemented and satisfied.                       The main contributions of this paper are as follows:
                                            Achieving formal coverage closure within a set project time-                        • Automated gap classification: Analyzes coverage report
                                         line is a persistent challenge in hardware design verification. To                        generated by a formal verification tool to partition uncov-



                                         ©2026 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including
                                         reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or
                                                                                        reuse of any copyrighted component of this work in other works.
      ered RTL regions into control flow branches (case, if/else)                      • Invocation of external tools or APIs: Agentic AI enables
      and statement level gaps.                                                          the use of outside tools and APIs to perform tangible ac-
   • Targeted property generation: An LLM generates Sys-                                 tivities and judge their effectiveness as opposed to making
      temVerilog properties (assertions and covers) using RTL                            use of language-based reasoning only. This feedback pro-
      and specification context to verify the intended behavior                          cess enhances precision and reliability, thereby increasing
      for each uncovered location.                                                       autonomous operation in the course of complex operational
   • Iterative agentic AI coverage closure: New properties are                           processes [14].
      incorporated, and the coverage report is re-evaluated in a                       The characteristics given above increase the independence
      loop until predefined thresholds are met.                                     and capability of an agentic AI to solve difficult tasks. Such
   This method precisely targets uncovered RTL code sections                        systems in formal verification speed up the signoff verification
and automatically generates SystemVerilog properties. As a                          process. The processes involved are to produce the verification
result, coverage gaps are effectively reduced, and the overall                      plan based on the natural-language specification, produce Sys-
verification effort required to achieve the desired coverage                        temVerilog properties and systematically fills if coverage gaps
within a defined timeframe is minimized.                                            are present. As the flow goes on, the critic agent checks the
                                                                                    property correctness, whereas the executor agent communicates
                            II. BACKGROUND                                          with the formal verification tool to establish the properties and
   This section introduces agentic AI patterns and their ability                    review the CEXs. Therefore, it offers a scalable verification
to handle complex tasks, followed by an overview of coverage                        framework of a complex RTL code, correspondence with the
principles within the context of formal verification.                               design intent, and quicken the process to formal verification.
A. Agentic Workflows                                                                B. Formal Coverage
   The implementation of Multi-Agent System (MAS), which                               Formal coverage quantifies the extent to which verification
interacts and communicates among several special software                           objectives are rigorously exercised within a given set of en-
agents to accomplish complicated tasks, is known as agentic                         vironmental assumptions. The most common coverage metric
AI. These agents usually utilize LLMs, and they have tool-                          is checker coverage, including line, expression, and toggle
awareness to perform the task. Task scheduling, task allocation,                    coverage. Line coverage specifically reports the percentage of
and establishment of feedback are parts of workflow to enhance                      synthesizable RTL statements within the Design Under Verifi-
the quality of the response. A logging mechanism guarantees                         cation (DUV) that have been mathematically proven reachable
the possibility to generate all the system processes through-                       and subsequently exercised by a specified property set within
out the working process. Further, Human-in-the-Loop (HIL)                           the formal verification environment.
checkpoints: these are checkpoints that provide monitoring of
the model drift, output hallucinations, and workflow decision                                        Listing 1: Consider the following RTL block
making where these are deemed essential.                                           1    always @(posedge clk) begin
                                                                                   2     if (a && b)
   The major benefits of the agentic patterns are as follows:                      3      c <= d1;
   • Dynamic Task Decomposition: Dynamic breakdown of a                            4     else
                                                                                   5      c <= d2;
     complex and multi-stage problem to a set of simpler                           6    end
     sub problems thus maximizing scalability and execution
     efficiency [9].
                                                                                             Listing 2: SVA property exercising the line 3 of RTL block
   • Deliberation loops make performance better: Built-in
                                                                                   1       property branch_captures_d1;
     propose-critique-repair cycles in the system inherently                       2        @(posedge clk)
     limit hallucinations, certify in-between results, and hence                   3         (a && b) |=> (c == $past(d1));
                                                                                   4       endproperty
     provide evaluative feedback of refinements, leading to                        5       assert property (branch_captures_d1);
     much better performance [10].
   • Self-Refinement Mechanisms: Structured self-reflection                            Consider a minimal example that yields two distinct line
     greatly improves problem-solving accuracy across models                        coverage targets, corresponding to lines 3 and 5, as detailed
     and benchmarks [11].                                                           in Listing 1. Listing 2 illustrates a formal property that, when
   • Multi-Agent workflow: Multi-objectives are broken down                         (a && b) holds at a rising clock edge, checks that c captures
     to form smaller tasks and the allocation to agents is                          the prior value of d1 in n cycles. This specific statement is
     determined by their expertise which makes them superior                        marked as covered once the formal tool successfully identifies a
     in reasoning and also makes the system stable [12].                            witnessing trace or inductively proves the implication holds uni-
   • Orchestration: It dictates the way tasks are carried out,                      versally. If the formal environment is over-constrained (thereby
     it regulates the sharing of data between agents and also                       preventing the antecedent (a && b) from ever being satisfied)
     dictates dependencies between agents that are interdepen-                      or if the proof/search depth parameters are insufficient, the
     dent. This kind of coordination can provide a high level                       target statement may remain unexercised, and coverage remains
     of reliability in operations and avoid possible conflicts in                   incomplete. If a comprehensive test suite fails to exercise
     workflow definitions [13].                                                     line 5, the aggregate line coverage for that specific suite is



©2026 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including
reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or
                                               reuse of any copyrighted component of this work in other works.
reported as 50 %. Consequently, line coverage metrics provide                                   Planning                        Generation                                       Execution
a direct indication of whether a specific coverage target has been                        Design Specification +
                                                                                                  RTL                           Generate SVA                                    Prove Properties
successfully exercised or not. The systematic incorporation of
targeted assertions and cover properties for previously uncov-
ered branches of RTL code can substantially improve coverage
                                                                                            Formal Verification
in formal verification [15].                                                                      Lead
                                                                                                                                 Update SVA                                       Analyze CEX



                          III. M ETHODOLOGY
   This section outlines the methodology for achieving cov-                                                                                                                    Sign-Off with
                                                                                             Task Dispatcher                 Compile ready SVA
erage closure in formal verification using agentic AI. First,                                                                                                                 Formal Coverage

an overview of the agentic AI-driven workflow for formal
verification is presented. Subsequently, the systematic approach                                                                                            LLM Agent

employed to ensure comprehensive coverage is discussed.                                                                                              GPT-4.1, GPT-5, Llama3.3 etc.,   Human-in-the-Loop AI




                                                                                               Fig. 1. Agentic AI methodology for formal verification [8]
A. Overview of Saarthi Workflow
   Saarthi uses a sophisticated agentic AI-based workflow that
makes use of multi-agent collaboration to enable formal veri-                       over again. A feedback loop that can only go through five times
fication, as shown in the Fig. 1. The formal verification lead                      causes humans to step in when progress stops, which cuts down
agent starts the process by parsing the available RTL and the                       on hallucination and keeps cycles from being unproductive. By
design specification to create a structured Verification Plan                       combining automated agent collaboration with strategic human
(vPlan). Specialized verification agents follow project conven-                     oversight, this architecture creates a scalable, auditable, and
tions and coding templates while translating each vPlan item                        high-confidence verification workflow for next-generation IC
into compile-ready SystemVerilog Assertions (SVAs) under                            design.
the direction of a task dispatcher. Critic agents give specific
feedback to help properties get better while always check-                           Verification     Group Chat Manager
ing the generated SVAs for syntax errors, completeness, and
semantic accuracy. As the flow progress toward high-quality,
tool-acceptable SVAs, the iterative loop represented in the
planning and generation stages, ensures alignment with the
                                                                                                                                                 Executor                           Formal
initial requirements. Before proceeding further, Saarthi refers                                                                                                                   Verification
                                                                                      Lead Agent                            Critic Agent          Agent
the task to human experts for disambiguation if predetermined                                          Verification Agent                                                            Tool
iteration thresholds are not met without resolution.
                                                                                          Fig. 2. Depiction of agentic AI performing workflow execution [7]
   In order to prove properties, gather CEXs, and facilitate
automated repair cycles, the code executor agent interfaces
with industry-standard formal verification tools such as Cadence
                                                                                    B. Agentic AI based coverage closure
Jasper Gold [16] during execution. Agents for verification and
criticism examine CEX traces to identify underlying issues,                            The methodology begins with the RTL specification and an
revise SVAs or RTL constraints as necessary, and submit                             initial SVA file, which are processed by a formal verification
proofs again until convergence. The following section presents                      tool to generate a coverage report after proof process. If no
a detailed explanation of how coverage agents incorporate                           coverage holes, such as uncovered or unreachable sections of
additional properties when coverage gaps remain, ensuring                           the RTL codebase, are discovered, the design proceeds directly
alignment with vPlan targets.                                                       to formal sign-off, as illustrated in Fig. 3. When gaps are
   The suggested framework, as shown in the Fig. 2, uses a                          present, the procedure transfers control to an agentic AI stage
multi-agent group chat where specialized roles, such as veri-                       that creates LLM-generated properties aimed at the uncovered
fication lead, formal verification engineer, and SystemVerilog                      areas in order to make ready for iterative closure in the next
expert, work together on verification tasks defined by the                          stages.
user through a shared event-driven mechanism. A HIL agent                              The agentic AI methodology addresses coverage gaps in
continuously supervises the workflow to ensure that automated                       formal verification by ingesting the coverage report generated
decisions are consistent with expert domain knowledge. In                           by a formal verification tool and automatically producing a
an event-driven architecture, a Group Chat Manager uses                             modified SVA file. This process is orchestrated by two coop-
AutoGen’s Core API to make sure that only one agent can                             erating agents: (i) a Coverage Hole Analyzer that characterizes
talk at a time and that everyone follows the rules of interaction                   the RTL context of uncovered code and (ii) an SVA Property
[17]. To get around some of the common problems with LLMs,                          Generator that generates targeted, LLM-generated properties
complicated goals are broken down into smaller tasks that are                       to address the identified gaps. The updated SVA properties are
given to different agents. At the same time, critic agents check                    incorporated into the SVA file and then reintroduced to the
the quality and accuracy of the SVAs that are made over and                         formal verification tool, thereby closing the feedback loop. The



©2026 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including
reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or
                                               reuse of any copyrighted component of this work in other works.
                                                                                 Updated                maintains records of the preconditions and reset logic for each
                                                                               SVA Properties
              RTL Specification                          SVA File                                       area that is found. It also picks the type of enclosing block, like
                                                                                                        always_ff, always_comb, if/else, or case, to show
                                                                                                        how the design operates and the way it fits into the design
                                                                                                        hierarchy. This detailed context is encoded into a short JSON
                                                                                                        format, which eliminates the need for extra RTL parsing and
                                  Formal Verification
                                         Tool
                                                                                                        lets downstream agents easily figure out properties. A sample
                                                                                                        definition and goal utilized by the Coverage Hole Analyzer
                                                                                                        agent are detailed in Listing 3, while the corresponding output
                                                                                                        generated is presented in Listing 4.
                                   Coverage Report

                                                                                                            Listing 3: Concise definition and targets for Coverage Hole Analyzer
                                                                                                       1    coverage_hole_analyzer:
                                                        Yes                                            2     system_prompt: > You are the RTL coverage hole analyzer
                                      Coverage                        Agentic AI
                                                                                                                   with mandatory code-extarction capabilities.
                                       Holes?                      Generated Properties
                                                                                                       3
                                            No                                                         4     goal: > Transform coordinate-based location data into
                                                                                                                  detailed RTL behaviour analysis. Follow the steps
                                                                                                                  below
                                    Sign-Off with                                                       5
                                   Formal Coverage                                                      6       STEP 1: RTL CODE EXTARCTION
                                                                                                        7       -For every location,extract the exact RTL slice
                 Fig. 3. Basic flow diagram of coverage pipeline                                        8
                                                                                                        9       STEP 2: SINGLE BEHAVIOUR CLASSIFICATION
                                                                                                       10       -One location -> one behaviour -> one future property.
                                                                                                       11
                                                                                                       12       STEP 3: LOGIC PATTERN and CONSOLIDATION ANALYSIS
iterative process continues until all required coverage goals are                                      13
                                                                      -For each location,derive a logic_signature:
fully met.                                                                                             14
                                                                       {opeartion_pattern, signal_realtion,
                                                                            timing_pattern}            15
   Coverage analysis data is obtained from the formal veri-
fication tool. Following the required preprocessing and nor-
malization steps, exact RTL locations of uncovered regions Listing 4: Response generated from Coverage Hole Analyzer in JSON format
are extracted for each module, including any preconditions 1 {
identified by the tool. These locations are then classified 23        "module": "alu",
                                                                      "input_type": "BRANCH_STRUCTURE|ISOLATED_STRUCTURE",
into two groups: (i) isolated locations, representing standalone 4    "locations": [
sections with minimal structural context, and (ii) branch and 56         {
                                                                            "start": [60, 34],
statement locations, which are related to control flow, such as 7           "end": [60, 39]
case, if/else, and always blocks. This classification ensures that 89 ],
                                                                         }

attributes are properly targeted for coverage closure by influenc- 10 "type": "BRANCH",
ing downstream agents’ reasoning regarding reachability and 11     12
                                                                      "code": "c <= a + b",
                                                                      "behavior": "Mode-based state machine branch selection,
timing considerations. The preprocessed locations are input to 13      "statement_type": "case_statement",
the Coverage Hole Analyzer, and its output is subsequently 14      15
                                                                       "signals": {
                                                                           "in": ["a", "b"],
provided to the SVA Property Generator, which generates the 16             "out": ["c"]
                                                                   17  },
required SVA properties, as shown in Fig. 4.                       18  "timing": "always_ff"
                                                                                                       19   }

                                        Coverage Analysis Agents                                           The SVA Property Generator processes the JSON output
                                         Agent 1                Agent 2                                 data and extracts macro definitions from the main SVA file to
                                      Coverage Hole           SVA Property                  SVA
                                                                                                        generate SVAs. It applies templates specific to each construct
                                        Analyzer               Generator                  Properties    and timing class to produce SystemVerilog properties that target
   Coverage         Pre                                                                                 unexercised branches and assertions that formalize intended
    Report       Processing
                                                                                                        behavior under the specified preconditions. Clocking and reset
                Fig. 4. Overview of the coverage agent workflow                                         semantics are determined by the timing class, and signals
                                                                                                        are mapped to the appropriate interfaces. During property
   The Coverage Hole Analyzer agent is a core component of                                              generation, the agent reuses an existing property name if it
our methodology that systematically identifies areas within the                                         is present in the SVA file; otherwise, it generates a random
design that show insufficient coverage. The structural and se-                                          property name to minimize duplication. The agent then merges
mantic context surrounding every coverage hole is reconstructed                                         these properties with the existing properties, maintains naming
through static code analysis by interpreting preprocessed loca-                                         conventions, and inserts traceability comments linking each
tions and their corresponding preconditions with relevant RTL                                           property to its original coverage location. The resulting SVA
files. It extracts the name of the module being analyzed, checks                                        file is immediately prepared for re-execution within the formal
the timing behavior, gets the input and output signals, and                                             verification tool environment. A sample definition and goal



©2026 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including
reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or
                                               reuse of any copyrighted component of this work in other works.
                                                                                                                        TABLE I
 utilized by the SVA Property Generator agent are detailed in                                    Saarthi performance across designs with coverage agents
 Listing 5, while the extracted code from the JSON response of
                                                                                                                             Without coverage agents   With coverage agents
 the agent is presented in Listing 6.                                                  Design                Metric
                                                                                                                            GPT-4.1 GPT-5 Llama3.3 GPT-4.1 GPT-5 Llama3.3

                                                                                                             # Properties     40      23      15        110     35      41
       Listing 5: Concise definition and targets for SVA Property Genertor             ECC                   Proven (%)       90     95.65   73.33     83.36    80     60.97
                                                                                                             Coverage (%)    61.72   70.30   70.71     89.30   92.11   89.60
1      sva_property_generator:
2       system_prompt: > You are Expert in generating                                                        # Properties     13      28      10        28      33      17
3          SystemVerilog properties for uncovered RTL                                  CIC Decimator [18]    Proven (%)      61.5    53.57    50       82.14   78.78   52.94
                                                                                                             Coverage (%)    63.98   71.54   52.38     74.32   81.04   66.39
4          locations based on the JSON output.
5                                                                                                            # Properties     35      38      20        101     80      77
6        goal: > Transform location analysis into compliant SVA                        AXI4LITE [18]         Proven (%)      57.14   55.26    20       64.35   42.45   51.94
                                                                                                             Coverage (%)    27.87   45.85   24.82     36.63   53.59   51.29
              properties using only available signals.
7                                                                                                            # Properties     27      35       2        53      89      19
8        STEP 1: Resource scan:                                                        Automotive IP         Proven (%)      74.07   62.22    50       77.35   51.68   26.31
                                                                                                             Coverage (%)    80.48   72.67   5.81      83.04   79.05   38.87
9           -Extract the signals, macros, and parameters/
                 constants available at the SVA file.                                                        # Properties     28      22      30        53      103     47
10                                                                                     Memory Scheduler [18] Proven (%)      53.57   45.45   26.66     73.58   90.29   29.78
                                                                                                             Coverage (%)    50.88   46.39   46.45     68.82   67.91   49.41
11       STEP 2: Single-statement enforcement:
12          -Allowed forms are (antecedent) |-> (single_outcome)
                 , |=>, or
13         |-> ##N, matching the existing style
14
15       STEP 3: Timing style match:                                                    Across various models, the Saarthi workflow with our cover-
16          -For always_ff, prefer |=> if an antecedent exists;
                 otherwise replicate the observed
                                                                                     age agents achieved the highest performance with OpenAI’s
17           form |-> ##1)                                                           GPT-5 [19], moderate performance with OpenAI’s GPT-4.1
18          -For always_comb or continuous assignments, use |->
                  (single cycle).
                                                                                     [19], and the lowest performance with Meta’s Llama3.3 [20].
                                                                                     The incorporation of our coverage agents consistently increases
                                                                                     the coverage metrics by approximately 10 % to 20 %, with the
     Listing 6: Code extracted from SVA Property Generator’s JSON response           largest gains observed in the more complex designs. Specifi-
1        property sum_of_a_and_b;                                                    cally, in the case of the ECC design, coverage surpassed 80 %
2        @(posedge clk) disable iff (!rst)                                           when the coverage agents were employed. Also, considerable
3        1’b1 |=> c == $past(a + b);
4        endproperty                                                                 enhancement in coverage were recorded for the AXI4LITE,
5        assert property (sum_of_a_and_b);                                           CIC Decimator, and Memory Scheduler designs. The most
                                                                                     significant change was observed in the Automotive IP, where
    The workflow operates iteratively; after each update to the                      the baseline coverage without agents was low but increased sig-
 SVA file, the formal verification tool is re-executed to generate                   nificantly after the incorporating of coverage agents. Although
 a new coverage report. Autonomous agents update or append                           GPT-5 exhibited superior performance due to its advanced rea-
 the formal properties set in response to any coverage gaps until                    soning capabilities, but exhibited higher latency in comparision.
 the target coverage metrics are met. When the design intent
 cannot be verified using purely static analysis, an expert agent
                                                                                        In some cases, especially within a subset of designs, the
 gets involved at each iteration to validate property intent, avoid
                                                                                     proven rate for generated properties decreased after the cover-
 over-constraint of the specification, and resolve complex edge
                                                                                     age agents’ workflow, even though overall coverage increased.
 cases. This iterative process thus facilitates the faster closure
                                                                                     This divergence arises because introducing new properties can
 of coverage, traceably reducing the manual verification effort
                                                                                     enhance coverage, but may also result in formal properties that
 through systematic consistency throughout the process.
                                                                                     are more challenging to verify. Furthermore, the effectiveness
                                                                                     of the generated properties is closely tied to the extraction
                           IV. B ENCHMARKING                                         of accurate RTL code by the Coverage Hole Analyzer agent.
    To evaluate the effectiveness and capabilities of the proposed                   Imperfections at this stage, along with the occasional generation
 methodology for coverage closure in formal verification, we                         of incorrect or duplicate properties by LLMs, can negatively
 benchmark the updated Saarthi framework, integrated with our                        impact the proven rate. The above problems are methodically
 coverage agents, on a diverse set of RTL designs. The bench-                        handled through an HIL review stage, guaranteeing that only
 mark suite includes both open-source and in-house industry-                         valid and verifiable properties are retained in the final verifica-
 grade design spanning various complexity levels. Table I high-                      tion environment.
 lights performance of the Saarthi framework with and without                           Importantly, these results were obtained without any HIL
 proposed coverage agents. To compare performance across vari-                       in the flow. Based on these benchmarking results, integrating
 ous LLMs, we employ two Key Performance Indicators (KPIs).                          HIL in the Saarthi flow, specifically after the coverage agents
 The first is the proven percentage, defined as the percentage of                    have performed their tasks, is likely to further boost coverage
 properties successfully proven among all properties generated                       metrics, as new properties have been generated for previously
 by the LLM; the second is coverage, quantified as the formal                        uncovered regions. This enhancement may speed up the formal
 coverage achieved following an end-to-end formal verification                       verification sign-off stage in the IC design process and lower
 flow.                                                                               the overall time required for completion.



 ©2026 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including
 reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or
                                                reuse of any copyrighted component of this work in other works.
                 (a) Design: ECC                                    (b) Design: CIC Decimator                                 (c) Design: AXI4LITE




                                                                                                                             Coverage metrics without Coverage Agents

                                                                                                                             Coverage metrics with Coverage Agents




            (d) Design: Automotive IP                             (e) Design: Memory Scheduler
                                       Fig. 5. Coverage metrics comparison across various designs using different models



                            V. C ONCLUSION                                                                         R EFERENCES
   This paper presented an automated workflow that leverages                         [1]   A. Leventi-Peetz1, “Formal Methods for Safe and Secure Computer
                                                                                           Systems,” Tech. Rep., 2013.
agentic AI enabled LLM to accelerate coverage in the formal                          [2]   C. Kern et al., “Formal verification in hardware design: a survey,” 1999.
verification. The proposed approach strategically targets uncov-                     [3]   H. Foster, Wilson Research Group IC/ASIC functional verification trend
ered RTL regions, enabling the automatic generation of formal                              report, Siemens Blog, 2024.
                                                                                     [4]   M. Abdollahi et al., “Hardware Design and Verification with Large
properties. Experimental results from both open-source and                                 Language Models: A Scoping Review, Challenges, and Open Issues,”
internal RTL designs confirm that the framework consistently                               Electronics, 2025.
enhances formal coverage. The target of the approach is formal                       [5]   DeepSeek-AI et al., DeepSeek-R1: Incentivizing Reasoning Capability
                                                                                           in LLMs via Reinforcement Learning, arXiv, 2025.
property generation and the passing rate of generated properties,                    [6]   W. Fang et al., “AssertLLM: Generating Hardware Verification Asser-
each further impacting the coverage rate. Even though the                                  tions from Design Specifications via Multi-LLMs,” in LAD, 2024.
proven rate is mostly dependent on the quality of LLMs’                              [7]   D. N. Gadde et al., “Hey AI, Generate Me a Hardware Code! Agentic
                                                                                           AI-based Hardware Design & Verification,” in SBCCI, 2025.
outputs, the findings show that the LLM-guided verification                          [8]   A. Kumar et al., Saarthi: The First AI Formal Verification Engineer,
is a promising route to automated coverage closure in formal                               arXiv, 2025.
verification. This approach substantially reduces manual effort                      [9]   S. K. Jeyakumar et al., Advancing Agentic Systems: Dynamic Task
                                                                                           Decomposition, Tool Integration and Evaluation using Novel Metrics
in the formal verification process and provides a strong method-                           and Dataset, arXiv, 2024.
ological basis for future advancements in AI-assisted coverage                      [10]   S. Chen et al., A Survey on LLM-based Multi-Agent System: Recent
closure.                                                                                   Advances and New Frontiers in Application, arXiv, 2025.
                                                                                    [11]   M. Renze et al., “Self-Reflection in Large Language Model Agents:
                         ACKNOWLEDGEMENT                                                   Effects on Problem-Solving Performance,” in FLLM, 2024.
                                                                                    [12]   Z. Li et al., Know the Ropes: A Heuristic Strategy for LLM-based Multi-
                                                                                           Agent System Design, arXiv, 2025.
                                                                                    [13]   C. Yu et al., “A Survey on Agent Workflow – Status and Future,” in
                                                                                           ICAIBD, 2025.
                                                                                    [14]   W. Zhang et al., AgentOrchestra: Orchestrating Hierarchical Multi-
                                                                                           Agent Intelligence with the Tool-Environment-Agent(TEA) Protocol,
                                                                                           arXiv, 2025.
   Under grant 101194371, Rigoletto is supported by the Chips                       [15]   E. Seligman et al., Formal Verification: An Essential Toolkit for Modern
                                                                                           VLSI Design. Morgan Kaufmann, 2015.
Joint Undertaking and its members, including the top-up fund-                       [16]   Cadence Design Systems, Inc., Jasper Formal Verification Platform,
ing by the National Funding Authorities from involved coun-                                2025.
tries.                                                                              [17]   Microsoft Research, AutoGen: Framework for Multi-Agent Systems,
                                                                                           2024.
   Rigoletto is also funded by the Federal Ministry of Research,                    [18]   N. Pinckney et al., Comprehensive Verilog Design Problems: A Next-
Technology and Space under the funding code 16MEE0548S.                                    Generation Benchmark Dataset for Evaluating Large Language Models
The responsibility for the content of this publication lies with                           and Agents on RTL Design and Verification, arXiv, 2025.
                                                                                    [19]   OpenAI, GPT-4.1 and GPT-5, 2024.
the author.                                                                         [20]   Meta AI, LLaMA 3.3 Model Card and Prompt Formats, 2024.




©2026 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including
reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or
                                               reuse of any copyrighted component of this work in other works.
