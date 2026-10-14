                                                                FormalRTL: Verified RTL Synthesis at Scale
                                                            Kezhi Li                                       Min Li                                  Xiangyu Wen
                                             The Chinese University of Hong Kong                   South East University              The Chinese University of Hong Kong
                                                     Hong Kong, China                                 Nanjing, China                          Hong Kong, China

                                                          Shibo Zhao                                    Jieying Wu                                Junhua Huang
                                                      South East University                        South East University                   Huawei Technologies Co. Ltd.
                                                         Nanjing, China                               Nanjing, China                           Shenzhen, China

                                                                                                         Qiang Xu
                                                                                          The Chinese University of Hong Kong
arXiv:2603.08738v1 [cs.AR] 25 Feb 2026




                                                                                                  Hong Kong, China

                                         Abstract                                                                       thousands of lines of RTL code. Although planning-based
                                         Large language models (LLMs) have demonstrated significant po-                 approaches [18, 22] attempt modular decomposition, their
                                         tential in automating hardware synthesis, yet substantial barriers             effectiveness is limited by incomplete or ambiguous natural
                                         remain for industrial-scale, datapath-centric designs due to ambigu-           language specifications [19] and the inherent difficulty of
                                         ous specifications and a lack of formal correctness guarantees. In             LLMs in making sound architectural decisions for complex
                                         this work, we present FormalRTL, a novel end-to-end multi-agent                design.
                                         framework that systematically integrates software reference mod-           (2) Intricate Arithmetic and Logical Structures. Unlike sim-
                                         els as formal, executable specifications to guide register-transfer            ple open source benchmarks, industrial IPs often feature deep
                                         level (RTL) code generation and verification. By tightly coupling              nested datapaths [36] and custom data types (e.g. bfloat16 [6],
                                         planning, synthesis, and formal equivalence checking, FormalRTL                hifloat8 [25]). Simulation-based verification [40] frequently
                                         achieves scalable and reliable hardware code generation that ad-               fails to cover corner cases, particularly in datapath-heavy
                                         dresses the critical challenges faced in industrial contexts. The              designs [5].
                                         comprehensive evaluation of a new suite of complex industrial-
                                         grade benchmarks demonstrates the effectiveness and robustness            These limitations in automated hardware generation stem from
                                         of our approach. We will open-source the FormalRTL framework           the inherent difficulty of directly synthesizing RTL code from
                                         and the benchmark suite to facilitate future research in this area.    natural language specifications. Specifications with only natural
                                                                                                                language often fail to capture the complex structural, temporal,
                                                                                                                and arithmetic requirements necessary for hardware implementa-
                                         1    Introduction
                                                                                                                tion [37]. In conventional industrial practice, hardware design and
                                         As AI workloads continue to scale, the design of computation-          verification engineers instead rely heavily on software reference
                                         intensive chips such as GPUs, NPUs and TPUs has become a major         models, typically written in C/C++, as executable golden specifica-
                                         engineering bottleneck [8, 16, 24]. This challenge originates from     tions and formal verification artifacts [9, 28]. Commercial hardware
                                         their intricate computational logic and relentless pursuit of ex-      formal verification tools such as Synopsys HECTOR [31] and Ca-
                                         treme power, performance and area (PPA) targets [4, 26], which         dence Jasper C Apps [32] leverage them to perform high-level
                                         have significantly prolonged the design cycle and increased the de-    equivalence checking (EC), mathematically proving that the final
                                         velopment cost of new chips. Nevertheless, with the advancement        RTL implementation is functionally equivalent to the trusted C/C++
                                         of AI, large language models (LLMs) have demonstrated impressive       reference model. Despite their industry-standard role, prior LLM-
                                         capabilities in natural language understanding and code genera-        driven hardware synthesis approaches have largely overlooked this
                                         tion [15, 27], which presents new opportunities for automated and      valuable resource.
                                         agile hardware synthesis.                                                 Building on these observations, we introduce FormalRTL (see
                                            Recently, a growing body of studies have investigated the use of    Fig. 1), a novel multi-agent pipeline that systematically addresses
                                         LLMs to generate hardware register-transfer level (RTL) code [2, 22,   the key challenges of industrial-grade hardware synthesis with
                                         34, 43]. Approaches based on fine-tuning strategies [11, 12, 30, 42]   LLMs. Unlike previous approaches that relied solely on potentially
                                         and multi-agent collaboration [14, 18, 22, 41] have demonstrated       ambiguous natural language specifications, FormalRTL leverages
                                         encouraging results on simple open source benchmarks [21, 23, 33]      the software reference model as an executable formal specification
                                         (e.g. adders and FIFOs with fewer than 100 lines of code). How-        to guide and anchor the entire synthesis process.
                                         ever, these advances highlight the substantial gap between current        Specifically, our pipeline begins with a planning agent, which
                                         research prototypes and industrial-scale applications.                 performs static analysis on the C reference model to reliably decom-
                                            We argue that existing methods for industrial-grade RTL synthe-     pose the complex design into modular subtasks, thereby mitigating
                                         sis face two fundamental challenges:                                   architectural ambiguities often found in purely LLM-based planning.
                                             (1) Large-Scale Design Complexity. Developing an industrial        For each subtask, the initializing agent generates the RTL code
                                                 hardware intellectual property (IP) core typically requires    and a verification harness directly anchored to the reference model.
,,                                                                         Kezhi Li, Min Li, Xiangyu Wen, Shibo Zhao, Jieying Wu, Junhua Huang, and Qiang Xu


To guarantee correctness, FormalRTL applies rigorous EC (i.e. hw-           on unstructured natural language specifications, which are often
cbmc [28]) between the software and hardware models. Crucially,             ambiguous and lack the precision to define complex datapath logic.
the debugging agent closes the loop utilizing counterexamples               Second, their debugging depends on simulation-based feedback.
from the EC tool to efficiently guide automated code refinement and         This approach is inherently constrained by testbench coverage and
error resolution. This tightly integrated workflow enables scalable         cannot provide the formal guarantee of functional correctness—an
RTL generation with formal correctness guarantees, substantially            important requirement for industrial hardware development.
narrowing the gap between LLM-based prototyping and real-world
hardware development.                                                       2.3      Software in Hardware Development
   In summary, our main contributions are as follows.                       To overcome the limitations mentioned above, we are motivated
     • We pioneer a software reference model-driven methodol-               by the reliance of the software reference model in the hardware
       ogy for agile hardware development, ensuring scalability and         industry, a practice now embedded in many established workflows.
       correctness by planning via static analysis and equivalence             High-level synthesis (HLS) requires designers to write C/C++
       checking.                                                            programs augmented with pragmas that guide the synthesis process,
     • We develop an end-to-end, multi-agent engine that au-                such as loop unrolling, pipelining, and interface specification [29].
       tomates the entire workflow, from planning, synthesis, and           This workflow is primarily targeted at FPGA development, enabling
       debugging to formal verification.                                    rapid prototyping and design-space exploration. Recent advances,
     • We construct and release a set of industrial-grade bench-            including C2HLSC [10] and HLSPilot [39], extend HLS workflows
       marks, complete with specifications and software reference           by leveraging LLMs to transform unconstrained C programs into
       models. Extensive experiments on these benchmarks show               synthesis-friendly C code.
       the effectiveness and robustness of our approach.                       In contrast, ASIC designs, especially those with intensive algo-
                                                                            rithm and datapath, rely on software models not only as synthesis
2 Related Work                                                              inputs but also as golden specifications for architectural exploration
2.1 LLM for RTL Synthesis                                                   and RTL verification. Architects typically encode the intended func-
                                                                            tionality in C++ or SystemC, which verification engineers then use
Early work shows that supervised fine-tuning (SFT) can substan-
                                                                            to generate expected outputs for regressions. ARM, for example,
tially improve the RTL code generation capabilities of LLMs [11,
                                                                            provides cycle-accurate SystemC models of its processor IP [3],
12, 21, 30, 42]. To this end, significant effort has focused on gener-
                                                                            while tools such as Cadence Jasper C2RTL [32] support formal
ating high-quality training data: CodeV [42] proposes multi-level
                                                                            equivalence between RTL datapaths and high-level C/C++ logic.
summarization data synthesis, OriGen [11] adopts a self-reflection
                                                                            By grounding verification in these trusted reference models, de-
framework with compiler feedback, and BetterV [30] uses domain-
                                                                            signers can clarify intent early, expose subtle corner-case bugs, and
specific instruct-tuning with generative discriminators.
                                                                            streamline functional sign-off.
    To further enhance reasoning and code generation, recent work
has introduced reinforcement learning (RL) mechanisms [7, 44].
ChipSeek-R1 [7], for example, integrates direct feedback from sim-          3     Proposed Methods
ulators, compilers, and electronic design automation (EDA) tools            The general workflow of FormalRTL is illustrated in Fig. 1. Formal-
during the training process. Similarly, CodeV-R1 [44] annotates             RTL is designed as a unified multi-agent framework that seamlessly
its training data with pass/fail feedback from an RTL equivalence           transforms high-level design intent into verified RTL implemen-
checking tool.                                                              tations. By explicitly taking both the C reference model and the
    However, these SFT and RL approaches remain constrained by              accompanying specification as inputs, the system orchestrates plan-
the quality of dataset and the scale of the LLMs. Moreover, the             ning, synthesis, debugging, and formal verification in an automated
fundamental method of direct RTL synthesis from natural language            pipeline. This integrated approach can enable scalable, reliable, and
specifications is often unstable and fails to scale to industrial-grade     efficient hardware development, ensuring that the generated RTL
cases. In addition, none of these methods can formally guarantee            faithfully adheres to both the intended functionality and the formal
the correctness of the generated code, even those trained with              specification. In addition, we build a new benchmark that provides
equivalence checking feedback.                                              both a specification and a software reference model for each case
                                                                            to test our engine.
2.2    Multi-agent Approaches for RTL Synthesis
Multi-agent collaborative systems offer more scalable and robust            3.1      Planning Agent
RTL synthesis compared to single-LLM methods [14, 18, 22, 41, 43].          The planning agent first partitions the C reference code into sub-
These frameworks typically adopt a three-agent architecture for             functions using static analysis from a C compiler. The compiler
the core pipeline: task planning, execution/generation, and de-             analyzes function dependencies via the abstract syntax tree (AST),
bugging/optimization. For example, VerilogCoder [14] employs                bundling each C function with its required dependencies (e.g. macros,
a graph-based task planning approach using Task and Circuit Rela-           enum types, and constant variables). Following partitioning, the
tion Graphs (TCRG), while MAGE [43] introduces a Verilog-state              LLM refactors the main design specification into a targeted specifi-
checkpoint mechanism to improve its debugging agent.                        cation for each individual submodule based on the C subfunction.
   However, these frameworks face two fundamental limitations                  The generation process then proceeds strictly following the topo-
that hinder their industrial applicability. First, their planning relies    logical order of the function dependencies derived from the AST.
FormalRTL: Verified RTL Synthesis at Scale                                                                                                                                 ,,



                            ...                                                                  RTL               C        Spec

                 syntax            counter-                                                  combine
                  error            example          Multi-agent Pipeline                                                                          Planning
                                                                                                  R
                                                                                                                        Planning                   Agent
                 Bug                 CE
                                                                                                  CTL                    Agent
                Locator           Simplifier           Counter                                                  generate submodules
                                                       example
                                                               +     ...               if fail      if pass
                                                                                                                                            CC              Spec
                                                                                                                                                            C
                                                                                        Soft-Hard
                    LLM            Location                                                                        CC       Spec
                                                                                           EC
                          apply                                                                                                                  topological refactor
                 Fixed             Patches                                                  initial RTL                                             order
                 Code                                                      fixed RTL        & harness
                                                                                                                                            Static
                                                             Debugging                           Initializing                                                 LLM
                          Debugging                           Agent                                Agent         for each submodule
                                                                                                                                           Division
                            Agent                                                                                 in topological order


                                                                                                                                            C              Spec


Figure 1: The general workflow of FormalRTL. The central pipeline (middle) takes a C model and specification, then iteratively
generates, verifies, and debugs RTL code on a per-submodule basis. The planning agent (right) uses C static analysis (AST)
to intelligently partition the main task. The debugging agent (left) leverages feedback from equivalence checking, using
counterexamples to automatically guide an LLM in generating code patches.


                                                                                                      3.2       Initializing Agent
        Static Analysis-based                 Software AST
         Implementation Flow                                                                          The initializing agent takes each submodule’s reference model and
                                                               Hardware
                                                   4         Dependencies                             specification as input and generates both an initial RTL file and
            C Reference Model                                                                         a corresponding verification harness. The harness establishes
                                                                    Top                               the verification environment for the RTL and C codes by assuming
            Module Under Generation
                                               3       2                                              identical inputs and asserting output equivalence [28]. To ensure
            Verified Dependent Module                                                                 reliability, we adopt a few-shot prompting strategy that guides the
               Mapping Relation                               Mid          Leaf                       agent in producing the necessary components for a structurally
                                               1                                                      correct harness.
         1..4 Topological Order
                                                                                                         Subsequently, the agent examines whether the submodule re-
                                                             Leaf
                                                                                                      quires sequential logic as specified. If so, it determines the appropri-
                                                                                                      ate timeframe of the harness, i.e., the exact number of clock cycles
                                                                                                      required for the hardware to yield final results. This parameter plays
Figure 2: Submodule implementation flow guided by C func-                                             a dual role: it governs the activation of transactional equivalence
tion dependencies.                                                                                    checking [9, 31, 32], while simultaneously serving as a design knob
                                                                                                      to regulate the depth and granularity of the RTL pipelining. By
                                                                                                      explicitly encoding the timeframe, pipeline stages are aligned with
                                                                                                      latency requirements, enabling systematic verification of sequential
                                                                                                      behavior and offering designers precise control over the generated
                                                                                                      timing behavior.
As illustrated in Fig. 2, when implementing a given submodule,
the agent receives its C reference and all previously verified RTL
modules on which it depends.                                                                          3.3       Debugging Agent
   This partitioning strategy offers three key benefits. First, by                                    The EC tool provides two types of feedback: syntax errors and
explicitly leveraging the functional hierarchy of the C reference                                     counterexamples. For syntax errors, we use a bug locator to first
model, our planning is more reliable than planning based on the                                       identify the error’s position. We then extract the code lines sur-
specification alone. Second, the decomposition limits the scope of                                    rounding the error to explicitly show the agent the erroneous code.
EC to an acceptable scale, ensuring that the verification tool can                                    This reduces the LLM’s burden of locating the error solely from a
efficiently process the task and provide rapid feedback. Third, it                                    line number, which is often difficult without the full code structure.
enables a bottom-up verification philosophy: each RTL submodule                                       For counterexamples, we use a simplifier that simplifies the report
is formally checked for equivalence against its corresponding C                                       to show only the information about the problematic function and
function. This incremental verification ensures the correctness of                                    the mismatching signals. This helps the agent quickly identify the
the dependent components, which in turn reduces the debugging                                         source of the logic mismatch. A qualitative demonstration of these
burden when building the top modules.                                                                 two tools is shown in Fig. 3. Finally, the LLM generates the location
,,                                                                       Kezhi Li, Min Li, Xiangyu Wen, Shibo Zhao, Jieying Wu, Junhua Huang, and Qiang Xu


                                                                          pipeline’s applicability to the agile development of state-of-the-art
            Bug Locator                   top.v                           chip designs.
                                          54 fracA = uiA[9:0];
       file /tmp/tmpy0t2qdg/top.v         55 fracB = uiB[9:0];
       : syntax error in line 56          56 if ((uiA^uiB)[15]) begin
       file /tmp/tmpy0t2qdg/main.c
                                                                          4 Experiments
                                          57 expA_loc = expA_u;
       : syntax error in line 12          58 sigA_loc = fracA;            4.1 Experimental Setup
                                          main.c
                                          ...                             We build FormalRTL using Langchain [35]. After considering fac-
                                                                          tors such as cost-effectiveness and task complexity, we select dif-
            CE Simplifier                 input for function              ferent base LLMs for different agents. Candidate LLMs are GPT-4.1
                                          hifloat8: ...                   and GPT-5. Their application is agent-specific:
        ...                               mismatched values:
        State 134 function hifloat8_mul   C reference model
          status_c=0 (00000000)           status_c = 0                        (1) The planning agent utilizes GPT-4.1, as this stage primarily
        State 136 function hifloat8_mul   z_c = 128
          z_c=128 (10000000)              ---                                     involves refining the initial natural language specifications
        State 137 function hifloat8_mul   Verilog implementation                  according to the C subfunctions—a task that requires only
          status_c=4 (00000100)           c = 1
        ...                               z_c = 127                               moderate reasoning ability.
                                                                              (2) The initializing agent employs GPT-5, which is better suited
                                                                                  to generate correct, reasonable, and high-quality RTL code.
Figure 3: Qualitatively demonstrate bug localization and                          This step requires advanced reasoning capabilities of the
counterexample simplification.                                                    model.
                                                                              (3) The debugging agent initially uses GPT-4.1 for rapid code
of the erroneous code and a corresponding patch, which is then                    fixes. If persistent issues remain after five iterations, the
applied to the original file to produce the fixed code.                           process escalates to GPT-5 to take advantage of its stronger
   In this agent, the EC tool plays an important role as both a syntax            reasoning for more complex debugging tasks.
checker and a counterexample provider. Counterexample-guided              We conducted all experiments using LLMs with default configura-
debugging is significantly more efficient than binary “pass/fail”         tions.
feedback. Furthermore, the tool guarantees a counterexample upon             Furthermore, we use Clang as the compiler choice for static
any equivalence failure. This automated approach effectively re-          analysis. For verification of software/hardware equivalence, we use
places the laborious process of manual testbench creation, thereby        an academic C-RTL EC tool, i.e., hw-cbmc [28].
avoiding the common pitfalls of insufficient coverage and high
engineering effort.                                                       4.2      Metrics
3.4    Benchmark Curation                                                 We define several key metrics to evaluate FormalRTL.
                                                                             Initial Success Rate (ISR, Eq. 1): This is equivalent to the
Current open source benchmarks for RTL generation often lack
                                                                          pass@1 metric in code generation benchmarks, which measures
industrial-grade specifications and corresponding reference C mod-
                                                                          the percentage of runs that pass equivalence checking on the first
els. Therefore, a contribution of this work is the collection and
                                                                          attempt (i.e. without any debugging iterations).
curation of a benchmark suite derived from both academic and
industrial scenarios. For this initial work, we primarily focus on
datapath-intensive modules, deferring the integration of more com-                                                𝑁 pass
                                                                                                      ISR =               × 100%,                      (1)
plex control-logic components to future research.                                                                 𝑁 total
   Academic Cases. Our academic cases are 16-bit floating-point
                                                                          where 𝑁 pass is the number of runs that pass after the initial gen-
(FP16) operators (e.g. FP16 adder and FP16 mulitiplier) derived from
                                                                          eration and 𝑁 total is the total number of runs, which is 20 in the
the Berkeley “softfloat” repository [13], which provides C imple-
                                                                          following experiment.
mentations of IEEE 754 computation units [17]. To prepare inputs
                                                                             # of Iterations: For the debugging phase, we set a maximum
for FormalRTL, we first use the static analysis of a C compiler, i.e.,
                                                                          iteration limit (𝐼 limit ) of 20. If the agent fails to fix the error within 20
Clang, to merge all scattered subfunctions for a given top-level
                                                                          iterations, the run is marked as a failure. To penalize failure cases,
module into a single file. Then, the file is manually cleaned to en-
                                                                          we treat the iteration count for any failed run as double the limit.
sure that it could be compiled independently. Finally, we author an
                                                                             We record the Average Fixing Iterations (𝐼 avg , Eq. 2) and the
industrial-style specification for each module, detailing necessary
                                                                          Standard Deviation (𝐼 std , Eq. 3).
information such as special case handling and sequential require-
ments to simulate a real-world development process. Each top-level
                                                                                                                              𝑁∑︁
module and its specification constitute a single test case.                                                             1       total

   Industrial Cases. For industrial cases, we manually implement                                      𝐼 avg =                           𝐼 𝑗′ ,         (2)
                                                                                                                    𝑁 total       𝑗=1
C reference models for the multiplication and addition functions of
Hifloat8 [25], an 8-bit floating-point datatype featured in the recent
Ascend AI Chip [20]. We also write a detailed specification for this
                                                                                                          v
                                                                                                          u
                                                                                                          t             𝑁∑︁
                                                                                                                          total
datatype and define its computational behavior with reference to                                                1
                                                                                                𝐼 std =                           (𝐼 𝑗′ − 𝐼 avg ) 2,   (3)
the IEEE 754 standard [17]. These cases serve to demonstrate our                                              𝑁 total       𝑗=1
FormalRTL: Verified RTL Synthesis at Scale                                                                                                                                                                             ,,


where 𝐼 𝑗′ is the adjusted iteration count for the run 𝑗 as shown in                                       60      Ours                      60                                100




                                                                            Total # of Fixing Iterations
                                                                                                                   Baseline                                                      100%




                                                                                                                                                      Final Success Rate (%)
Eq. 4:                                                                                                     50                                                                                 95%        95%
                                                                                                                                                                               80
                                                                                                                                                                                                                 81%
                     (
                       𝐼𝑗          if run 𝑗 passes (𝐼 𝑗 ≤ 𝐼 limit )                                        40                     34.1
              𝐼 𝑗′ =                                                . (4)                                                                                                      60             65%
                       2 × 𝐼 limit if run 𝑗 fails                                                          30          24.2                                                                              40%
                                                                                                                                             28                                40
   Final Success Rate (FSR): Finally, we record the FSR, which                                             20          22.4       23.9
measures the total percentage of designs that were successfully                                            10 5                                                                20
fixed by our agent within the iteration limit.                                                                                                                                            Ours                   0%
                                                                                                           0     0.6                                                            0         Baseline
                                                                                                           design 1 design 2 design 3 design 4                                  design 1 design 2 design 3 design 4
4.3     Performance on Module-level Cases                                                                  210 lines 685 lines 818 lines 1130 lines                             210 lines 685 lines 818 lines 1130 lines
                                                                                                                  Increasing Design Complexity                                         Increasing Design Complexity
Table 1 presents the module-level results. Although FormalRTL
processes a complete design, including multiple submodules and a                      Figure 4: Comparison of planning methods on fixing itera-
specification, as a single input, we report metrics for each individual               tions and FSR.
submodule for better demonstration. The modules labeled “top”
represent the top-level module of their respective design. To avoid
redundancy, the submodules shared between different designs are                       engine (i.e. the same initializing and debugging agents) instead
tested only once. The last column records the RTL code lines of a                     of the testbench-based verification or different EDA tools found
submodule and the total lines, including all its dependencies. Based                  in their pipelines. This configuration ensures that any observed
on the results, we draw the following conclusions.                                    performance difference is attributable only to the planning method
    Our benchmark cases are challenging, reflecting industrial-                       itself.
level complexity, and this is demonstrated in two ways. First, the                       We quantify the total implementation effort (𝐼 total , Eq. 5) for
total length of the RTL code shows that the scale of the task is                      FormalRTL by summing the average fixing iterations of the top
significant, with the hardest case requiring generating more than                     module and all its dependent submodules, as follows:
1000 lines of code. Second, the ISR for many modules is low, un-
derscoring that current commercial LLMs struggle to produce a                                                                   module     module
                                                                                                                                                                                     ∑︁
                                                                                                                                                                                                 𝑖
correct module on the first attempt.                                                                                          𝐼 total  = 𝐼 avg    +                                            𝐼 avg .                (5)
                                                                                                                                                                  𝑖 ∈dependencies
    The debugging agent is effective in fixing errors. All sub-
modules achieve a high FSR within iteration limits. This highlights                     The FSR of FormalRTL for a given design is defined as the product
the efficiency of our counterexample-guided debugging approach.                    of the FSR of its top-level module and the FSRs of all its dependent
    The planning agent effectively distributes implementation                      submodules.
complexity, and this is demonstrated in two ways. First, the agent                      The baseline approach must debug the entire design as a single,
balances the implementation load. The partitioned submodules                       monolithic task, making it impossible to formally verify individual
are kept within a reasonable and evenly distributed code length,                   sub-components against a C reference. Consequently, the iteration
avoiding any single monolithic bottleneck. Second, the bottom-up                   budget for the baseline must be compared with our total summed
verification strategy is highly effective. Counter-intuitively, the                effort (𝐼 total ). For a fair comparison, we set the maximum fixing
average ISR for the top-level modules is higher than that of the                   iteration limit for each baseline task to be close to the calculated
leaf or mid-level modules. This is because, when generating the top                𝐼 total from Table 1. Specifically, we choose four designs with vary-
module, the agent has already implemented and formally verified                    ing complexity and set the maximum iteration limits as follows:
all its dependencies, reducing the implementation burden.                          “f16_roundToInt” (Design 1, limit: 5), “hifloat8_mul” (Design 2, limit:
    FormalRTL is effective in handling sequential logic. To                        25), “hifloat8_add” (Design 3, limit 25) and “f16_add” (Design 4,
demonstrate compatibility with sequential circuits, we introduce                   limit: 30).
specific sequential requirements into the specifications of some                        As shown in Fig. 4, the performance changes significantly with
designs. Generating sequential logic is inherently more difficult and              the design scale. For the small-scale Design 1 (“f16_roundToInt”),
requires correct identification of sequential requirements and the                 the baseline method requires fewer fixing iterations, as it benefits
use of transactional equivalence checking. Despite these challenges,               from generating fixes for all submodules in a single iteration. How-
the engine still achieved a high FSR for these sequential circuits.                ever, this advantage rapidly diminishes as the complexity increases.
                                                                                   For larger designs, the burden of managing the entire design state
4.4     Ablation Study of Planning Methods                                         overwhelms the LLM. In Design 4 (“f16_add”), the baseline method
To demonstrate the effectiveness of our reference-code-based plan-                 fails to generate a single correct output with 0% success rate. In con-
ning, we compare it against a baseline that represents the current                 trast, our reference-code-based planning pipeline maintains a high
paradigm of specification-only RTL generation [14, 41, 43]. Al-                    success rate across all designs, demonstrating superior stability and
though these contemporary approaches do not support C reference                    scalability in handling complex industrial-level RTL generation.
models as a structured input, we design this baseline to strictly
emulate their methodology. We first treated the C reference model                     4.5                         Ablation Study of Debugging Tools
as an unstructured text within the specification, rather than using it               To evaluate the components of the debugging agent, we perform
for static analysis. Second, to ensure a fair comparison and control                 an ablation study on the leaf module “normalize”. We compare
for backend differences, this baseline uses our formal verification                  FormalRTL with three baseline configurations: (1) without the bug
,,                                                                      Kezhi Li, Min Li, Xiangyu Wen, Shibo Zhao, Jieying Wu, Junhua Huang, and Qiang Xu


                                    Table 1: Performance of our pipeline on module-level cases.

                                             Initial Success Rate     # of Iterations                                 Module / Total RTL Length
Design         Module Name          Type                                                    Final Success Rate
                                                   (pass@1)           𝐼 avg         𝐼 std                                (Average # of Lines)

            countLeadingZeros16     leaf             90%              0.25         0.77             100%                        48.55 / 48.55
                  packToF16         leaf             40%              2.50         2.40             100%                        27.45 / 27.45
               shiftRightJam32      leaf             50%              0.90          1.26            100%                        38.45 / 38.45
              propagateNaNF16       leaf             45%              1.75         1.89             100%                        57.50 / 57.50
             normSubnormalF16       mid              30%              5.00         9.05              95%                        37.70 / 86.25
Softfloat     roundPackToF16        mid              50%              3.45          4.60            100%                       146.30 / 173.70
IEEE754          addMagsF16         mid              35%              8.85         14.04             85%                       345.15 / 576.35
  FP16           subMagsF16         mid               5%              9.25         8.69              95%                       370.00 / 700.25
                     f16_le         top              50%              3.15         8.63              95%                        62.05 / 62.05
               f16_roundToInt       top              80%              0.70          1.58            100%                       124.70 / 209.60
                    f16_add         top              65%              1.00         1.84             100%                       46.15 / 1129.95
                    f16_sub         top              90%              0.30          1.10            100%                       43.75 / 1127.60
                   f16_mul          top              15%              7.30         8.45              95%                       209.85 / 565.75
             calculate_dot_and_m    leaf             75%              0.55         1.12             100%                        48.25 / 48.25
                   normalize        leaf             15%              6.40         8.88              95%                        67.50 / 67.50
                      lzc           leaf             35%              1.45         1.63             100%                        24.10 / 24.10
                decode_hifloat8     leaf             50%              3.30         4.83             100%                       134.40 / 134.40
                encode_hifloat8     mid              25%              4.20         5.14             100%                       153.40 / 201.65
HiFloat8
             round_half_to_away     mid              45%              4.75         6.25             100%                       140.75 / 189.00
                 hifloat8_add       top              70%              0.45         0.80             100%                       257.00 / 818.35
                 hifloat8_add
                                     top             20%              16.00        16.25             70%                       420.64 / 981.99
                  (sequential)
                 hifloat8_mul        top             95%              0.05         0.22             100%                       147.05 / 684.35
                 hifloat8_mul
                                     top             60%              9.65         15.67             80%                       220.10 / 757.35
                  (sequential)


        Table 2: Ablation study of the Debugging Agent.                             Table 3: QoR Comparison with Manual Designs.

            Methods            Average # of Iterations     FSR                                    hifloat8_mul                     f16_mul
         w/o bug locator                   14.15           80%                               Area (𝜇𝑚 2 )   Delay (𝑛𝑠)     Area (𝜇𝑚 2 )     Delay (𝑛𝑠)
         w/o CE simplifier                 9.55            90%                FormalRTL         1015           3.29            1629            3.54
     w/o CE-guided debugging               21.30           55%                Engineer           743           1.78            1343            2.50
           FormalRTL                       6.40            95%


locator, (2) without the counterexample simplifier, and (3) without           in area and delay, which is consistent with our emphasis on func-
counterexample-guided debugging.                                              tional correctness over immediate PPA optimization. Nevertheless,
   As shown in Table 2, all baseline methods require more fixing              verified RTL provides tangible benefits for engineers: a correct, ex-
iterations and achieve a lower Final Success Rate (FSR) than our              ecutable baseline facilitates agile development and offers a reliable
complete agent, where the absence of counterexample-guided de-                foundation for RTL design. Furthermore, a stable golden reference
bugging causes the most significant performance degradation.                  enables systematic PPA iteration and ensures the validity of opti-
                                                                              mizations.
4.6     Quality of Result (QoR) Comparison
We compare the designs generated by FormalRTL with their manual,              5   Conclusion and Future Work
engineer-optimized counterparts. All designs are evaluated using          This paper presents FormalRTL, a scalable multi-agent engine for
Yosys [38] for synthesis with the Nangate45 library and Open-             LLM-based RTL synthesis. Our pipeline utilizes software reference
ROAD [1] for placement and routing.                                       models to guide the generation of formally verified hardware. The
   Table 3 reports two representative cases: “hifloat8_mul” and           system employs static analysis for task planning and formal EC
“f16_mul”. Similar trends are observed in the evaluation of other         counterexamples to guide automated debugging. Experiments on a
modules. The LLM-generated RTL typically trails manual designs            new suite of industrial-grade benchmarks indicate that FormalRTL
FormalRTL: Verified RTL Synthesis at Scale                             ,,


can generate and verify complex and datapath-heavy designs. De-
spite these advances, several limitations remain and point toward
avenues for future work.
   Scalability to Industrial-Scale RTL. Our pipeline has been val-
idated on RTL generation tasks exceeding 1000 lines, significantly
narrowing the gap between academic prototypes and industrial
needs. Although a gap remains for full industrial-scale designs,
our effective decomposition strategy enables the construction of
verified large-scale systems from manageable subtasks.
   Specialized LLMs for Debugging. While our pipeline is de-
signed to be model-agnostic, its effectiveness heavily relies on the
model’s ability to understand debugging feedback (e.g. counterex-
amples). Future work could focus on training small and specialized
models specifically for this counterexample-guided fixing task to
reduce the reliance on large-scale, proprietary commercial models.
   Robust Open Source Equivalence Checking. We observe a
scarcity of actively maintained open source tools for C-RTL EC.
The community would greatly benefit from the development of
new open source EC tools that support modern RTL syntax and
offer more efficient performance.
,,                                                                                       Kezhi Li, Min Li, Xiangyu Wen, Shibo Zhao, Jieying Wu, Junhua Huang, and Qiang Xu


References                                                                                [23] Yao Liu, Lu, Wenji Fang, Mengming Li, and Zhiyao Xie. 2024. Openllm-rtl: Open
 [1] Tutu Ajayi and David Blaauw. 2019. OpenROAD: Toward a self-driving, open-                 dataset and benchmark for llm-aided design rtl generation. In Proceedings of the
     source digital layout implementation tool chain. In Proceedings of Government             43rd IEEE/ACM International Conference on Computer-Aided Design. 1–9.
     Microcircuit Applications and Critical Technology Conference.                        [24] Tao Luo, Shaoli Liu, Ling Li, Yuqing Wang, Shijin Zhang, Tianshi Chen, Zhi-
 [2] Ahmed Allam, Youssef Mansour, and Mohamed Shalan. 2025. ASIC-Agent: An                    wei Xu, Olivier Temam, and Yunji Chen. 2016. DaDianNao: A neural network
     Autonomous Multi-Agent System for ASIC Design with Benchmark Evaluation.                  supercomputer. IEEE Trans. Comput. 66, 1 (2016), 73–88.
     In 2025 IEEE International Conference on LLM-Aided Design (ICLAD). IEEE, 23–29.      [25] Yuanyong Luo, Zhongxing Zhang, Richard Wu, Hu Liu, Ying Jin, Kai Zheng,
 [3] Arm. 2021. Introduction to Cycle Model reference platforms. https://developer.            Minmin Wang, Zhanying He, Guipeng Hu, Luyao Chen, et al. 2024. Ascend
     arm.com/documentation/101497/1105/Introduction-to-Cycle-Model-reference-                  hifloat8 format for deep learning. arXiv preprint arXiv:2409.16626 (2024).
     platforms/Introduction-to-Cycle-Model-reference-platforms?lang=en. SystemC           [26] Stefano Markidis, Steven Wei Der Chien, Erwin Laure, Ivy Bo Peng, and Jeffrey S
     Cycle Models Reference Platform Getting Started Guide, Version 11.5.                      Vetter. 2018. Nvidia tensor core programmability, performance & precision. In
 [4] Akhil Arunkumar, Evgeny Bolotin, Benjamin Cho, Ugljesa Milic, Eiman Ebrahimi,             2018 IEEE international parallel and distributed processing symposium workshops
     Oreste Villa, Aamer Jaleel, Carole-Jean Wu, and David Nellans. 2017. MCM-GPU:             (IPDPSW). IEEE, 522–531.
     Multi-chip-module GPUs for continued performance scalability. ACM SIGARCH            [27] Antonio Mastropaolo, Luca Pascarella, Emanuela Guglielmi, Matteo Ciniselli,
     Computer Architecture News 45, 2 (2017), 320–332.                                         Simone Scalabrino, Rocco Oliveto, and Gabriele Bavota. 2023. On the robustness
 [5] Manuel Blum and Hal Wasserman. 2002. Reflections on the Pentium division                  of code generation techniques: An empirical study on github copilot. In 2023
     bug. IEEE Trans. Comput. 45, 4 (2002), 385–393.                                           IEEE/ACM 45th International Conference on Software Engineering (ICSE). IEEE,
 [6] Neil Burgess, Jelena Milanovic, Nigel Stephens, Konstantinos Monachopoulos,               2149–2160.
     and David Mansell. 2019. Bfloat16 processing for neural networks. In 2019 IEEE       [28] Rajdeep Mukherjee, Mitra Purandare, Raphael Polig, and Daniel Kroening. 2017.
     26th Symposium on Computer Arithmetic (ARITH). IEEE, 88–91.                               Formal techniques for effective co-verification of hardware/software co-designs.
 [7] Zhirong Chen, Kaiyan Chang, Zhuolin Li, Xinyang He, Chujie Chen, Cangyuan                 In Proceedings of the 54th Annual Design Automation Conference 2017. 1–6.
     Li, Mengdi Wang, Haobo Xu, Yinhe Han, and Ying Wang. 2025. ChipSeek-R1:              [29] Declan O’Loughlin, Aedan Coffey, Frank Callaly, Darren Lyons, and Fearghal
     Generating Human-Surpassing RTL with LLM via Hierarchical Reward-Driven                   Morgan. 2014. Xilinx vivado high level synthesis: Case studies. In 25th IET Irish
     Reinforcement Learning. arXiv preprint arXiv:2507.04736 (2025).                           Signals & Systems Conference 2014 and 2014 China-Ireland International Conference
 [8] Jack Choquette, Wishwesh Gandhi, Olivier Giroux, Nick Stam, and Ronny                     on Information and Communications Technologies (ISSC 2014/CIICT 2014). IET,
     Krashinsky. 2021. Nvidia a100 tensor core gpu: Performance and innovation.                352–356.
     IEEE Micro 41, 2 (2021), 29–35.                                                      [30] Zehua Pei, Hui-Ling Zhen, Mingxuan Yuan, Yu Huang, and Bei Yu. 2024. BetterV:
 [9] Edmund Clarke, Daniel Kroening, and Karen Yorav. 2003. Behavioral consistency             controlled verilog generation with discriminative guidance. In Proceedings of the
     of C and Verilog programs using bounded model checking. In Proceedings of the             41st International Conference on Machine Learning. 40145–40153.
     40th annual Design Automation Conference. 368–371.                                   [31] Synopsys. 2025. VC Formal Datapath Validation. https://www.synopsys.com/
[10] Luca Collini, Siddharth Garg, and Ramesh Karri. 2024. C2HLSC: Leveraging                  verification/static-and-formal-verification/vc-formal/vc-formal-datapath-
     large language models to bridge the software-to-hardware design gap. ACM                  validation.html.
     Transactions on Design Automation of Electronic Systems (2024).                      [32] Cadence Design Systems. 2025.                   Jasper C Formal Verification.
[11] Fan Cui, Chenyang Yin, Kexing Zhou, Youwei Xiao, Guangyu Sun, Qiang Xu,                   https://www.cadence.com/en_US/home/tools/system-design-and-
     Qipeng Guo, Yun Liang, Xingcheng Zhang, Demin Song, et al. 2024. Origen: En-              verification/formal-and-static-verification/jasper-c-formal-verification.html.
     hancing rtl code generation with code-to-code augmentation and self-reflection.      [33] Shailja Thakur, Baleegh Ahmad, Zhenxing Fan, Hammond Pearce, Benjamin Tan,
     In Proceedings of the 43rd IEEE/ACM International Conference on Computer-Aided            Ramesh Karri, Brendan Dolan-Gavitt, and Siddharth Garg. 2023. Benchmarking
     Design. 1–9.                                                                              large language models for automated verilog rtl code generation. In 2023 Design,
[12] Mingzhe Gao, Jieru Zhao, Zhe Lin, Wenchao Ding, Xiaofeng Hou, Yu Feng, Chao               Automation & Test in Europe Conference & Exhibition (DATE). IEEE, 1–6.
     Li, and Minyi Guo. 2024. Autovcoder: A systematic framework for automated            [34] Shailja Thakur, Baleegh Ahmad, Hammond Pearce, Benjamin Tan, Brendan Dolan-
     verilog code generation using llms. In 2024 IEEE 42nd International Conference on         Gavitt, Ramesh Karri, and Siddharth Garg. 2024. Verigen: A large language model
     Computer Design (ICCD). IEEE, 162–169.                                                    for verilog code generation. ACM Transactions on Design Automation of Electronic
[13] John R. Hauser. 2018. Berkeley SoftFloat Release 3e: Library Interface. https:            Systems 29, 3 (2024), 1–31.
     //www.jhauser.us/arithmetic/SoftFloat-3/doc/SoftFloat.html.                          [35] Oguzhan Topsakal and Tahir Cetin Akinci. 2023. Creating large language model
[14] Chia-Tung Ho, Haoxing Ren, and Brucek Khailany. 2025. Verilogcoder: Au-                   applications utilizing langchain: A primer on developing llm apps fast. In Interna-
     tonomous verilog coding agents with graph-based planning and abstract syntax              tional conference on applied engineering and natural sciences, Vol. 1. 1050–1056.
     tree (ast)-based waveform tracing tool. In Proceedings of the AAAI Conference on     [36] Swagath Venkataramani, Vijayalakshmi Srinivasan, Wei Wang, Sanchari Sen,
     Artificial Intelligence, Vol. 39. 300–307.                                                Jintao Zhang, Ankur Agrawal, Monodeep Kar, Shubham Jain, Alberto Mannari,
[15] Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu             Hoang Tran, et al. 2021. RaPiD: AI accelerator for ultra-low precision training and
     Liu, Jiajun Zhang, Bowen Yu, Keming Lu, et al. 2024. Qwen2. 5-coder technical             inference. In 2021 ACM/IEEE 48th Annual International Symposium on Computer
     report. arXiv preprint arXiv:2409.12186 (2024).                                           Architecture (ISCA). IEEE, 153–166.
[16] Norm Jouppi, George Kurian, Sheng Li, Peter Ma, Rahul Nagarajan, Lifeng Nai,         [37] Yangbo Wei, Zhen Huang, Huang Li, Wei W Xing, Ting-Jung Lin, and Lei He.
     Nishant Patil, Suvinay Subramanian, Andy Swing, Brian Towles, et al. 2023.                2025. Vflow: Discovering optimal agentic workflows for verilog generation. arXiv
     Tpu v4: An optically reconfigurable supercomputer for machine learning with               preprint arXiv:2504.03723 (2025).
     hardware support for embeddings. In Proceedings of the 50th annual international     [38] Clifford Wolf, Johann Glaser, and Johannes Kepler. 2013. Yosys-a free Verilog
     symposium on computer architecture. 1–14.                                                 synthesis suite. In Proceedings of the 21st Austrian Workshop on Microelectronics
[17] William Kahan. 1996. IEEE standard 754 for binary floating-point arithmetic.              (Austrochip), Vol. 97.
     Lecture Notes on the Status of IEEE 754, 94720-1776 (1996), 11.                      [39] Chenwei Xiong, Cheng Liu, Huawei Li, and Xiaowei Li. 2024. Hlspilot: Llm-based
[18] Cangyuan Li, Chujie Chen, Yudong Pan, Wenjun Xu, Yiqi Liu, Kaiyan Chang,                  high-level synthesis. In Proceedings of the 43rd IEEE/ACM International Conference
     Yujie Wang, Mengdi Wang, Huawei Li, Yinhe Han, et al. 2025. Autosilicon: Scaling          on Computer-Aided Design. 1–9.
     up rtl design generation capability of large language models. ACM Transactions       [40] Zhiyuan Yan, Wenji Fang, Mengming Li, Min Li, Shang Liu, Zhiyao Xie, and
     on Design Automation of Electronic Systems 30, 6 (2025), 1–21.                            Hongce Zhang. 2025. Assertllm: Generating hardware verification assertions
[19] Mengming Li, Wenji Fang, Qijun Zhang, and Zhiyao Xie. 2025. Specllm: Exploring            from design specifications via multi-llms. In Proceedings of the 30th Asia and
     generation and review of vlsi design specification with large language model. In          South Pacific Design Automation Conference. 614–621.
     2025 International Symposium of Electronics Design Automation (ISEDA). IEEE,         [41] Zhongzhi Yu, Mingjie Liu, Michael Zimmer, Yingyan Celine, Yong Liu, and Haox-
     749–755.                                                                                  ing Ren. 2025. Spec2RTL-Agent: Automated Hardware Code Generation from
[20] Heng Liao, Jiajin Tu, Jing Xia, Hu Liu, Xiping Zhou, Honghui Yuan, and Yuxing             Complex Specifications Using LLM Agent Systems. In 2025 IEEE International
     Hu. 2021. Ascend: a scalable and unified architecture for ubiquitous deep neural          Conference on LLM-Aided Design (ICLAD). IEEE, 37–43.
     network computing: Industry track paper. In 2021 IEEE International Symposium        [42] Yang Zhao, Di Huang, Chongxiao Li, Pengwei Jin, Muxin Song, Yinan Xu, Ziyuan
     on High-Performance Computer Architecture (HPCA). IEEE, 789–801.                          Nan, Mingju Gao, Tianyun Ma, Lei Qi, et al. 2025. Codev: Empowering llms
[21] Mingjie Liu, Nathaniel Pinckney, Brucek Khailany, and Haoxing Ren. 2023. Ver-             with hdl generation through multi-level summarization. IEEE Transactions on
     ilogEval: Evaluating Large Language Models for Verilog Code Generation. In                Computer-Aided Design of Integrated Circuits and Systems (2025).
     2023 IEEE/ACM International Conference on Computer-Aided Design (ICCAD).             [43] Yujie Zhao, Hejia Zhang, Hanxian Huang, Zhongming Yu, and Jishen Zhao. 2025.
[22] Shang Liu, Wenji Fang, Yao Lu, Jing Wang, Qijun Zhang, Hongce Zhang, and                  Mage: A multi-agent engine for automated rtl code generation. In 2025 62nd
     Zhiyao Xie. 2024. Rtlcoder: Fully open-source and efficient llm-assisted rtl code         ACM/IEEE Design Automation Conference (DAC). IEEE, 1–7.
     generation technique. IEEE Transactions on Computer-Aided Design of Integrated       [44] Yaoyu Zhu, Di Huang, Hanqi Lyu, Xiaoyun Zhang, Chongxiao Li, Wenxuan
     Circuits and Systems (2024).                                                              Shi, Yutong Wu, Jianan Mu, Jinghua Wang, Yang Zhao, et al. 2025. CodeV-R1:
                                                                                               Reasoning-Enhanced Verilog Generation. arXiv preprint arXiv:2505.24183 (2025).
