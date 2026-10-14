                                              V ERI -S URE: A Contract-Aware Multi-Agent Framework with Temporal
                                                 Tracing and Formal Verification for Correct RTL Code Generation


                                                                                  Jiale Liu 1 Taiyu Zhou 2 Tianqi Jiang 3


                                                                  Abstract                                    bar for productivity and correctness in Electronic Design
                                                                                                              Automation (EDA). In practice, the central artifact in the
                                              In the rapidly evolving field of Electronic De-
                                                                                                              design flow is the Register-Transfer Level (RTL) descrip-
arXiv:2601.19747v1 [cs.AR] 27 Jan 2026




                                              sign Automation (EDA), the deployment of Large
                                                                                                              tion, typically written in Hardware Description Languages
                                              Language Models (LLMs) for Register-Transfer
                                                                                                              (HDLs) such as Verilog and SystemVerilog, which specifies
                                              Level (RTL) design has emerged as a promising
                                                                                                              clocked state and the combinational logic between registers,
                                              direction. However, silicon-grade correctness re-
                                                                                                              precisely capturing concurrent circuit behavior under strict
                                              mains bottlenecked by (i) limited test coverage
                                                                                                              timing constraints and enabling downstream synthesis and
                                              and reliability of simulation-centric evaluation,
                                                                                                              implementation. As a result, writing high-quality, synthe-
                                              (ii) regressions and repair hallucinations intro-
                                                                                                              sizable RTL remains an indispensable yet costly step in
                                              duced by iterative debugging, and (iii) semantic
                                                                                                              modern chip development.
                                              drift as intent is reinterpreted across agent hand-
                                              offs. In this work, we propose V ERI -S URE, a                  Large language models (LLMs) have recently made rapid
                                              multi-agent framework that establishes a design                 progress in software code generation (Jiang et al., 2026;
                                              contract to align agents’ intent and uses a patching            Guo et al., 2024; Huang et al., 2025), suggesting a com-
                                              mechanism guided by static dependency slicing to                pelling opportunity to generate RTL code directly from
                                              perform precise, localized repairs. By integrating              natural-language specifications. However, RTL code gener-
                                              a multi-branch verification pipeline that combines              ation poses requirements that are completely different from
                                              trace-driven temporal analysis with formal verifi-              software, since HDL describes concurrent hardware behav-
                                              cation consisting of assertion-based checking and               ior with strict cycle-level timing, protocol semantics, and
                                              boolean equivalence proofs, V ERI -S URE enables                hierarchical structural constraints (Akyash & Mardani Ka-
                                              functional correctness beyond pure simulations.                 mali, 2025). As a result, general-purpose coding models,
                                              We also introduce V ERILOG E VAL - V 2-EXT, ex-                 which are optimized for autoregressive, sequential text gen-
                                              tending the original benchmark with 53 more                     eration, often achieve surface-level syntactic correctness yet
                                              industrial-grade design tasks and stratified dif-               fail to reliably preserve temporal intent, handshake proto-
                                              ficulty levels, and show that V ERI -S URE achieves             cols, or globally consistent structure (Thakur et al., 2024).
                                              state-of-the-art verified-correct RTL code gener-               These failures are worsened by the scarcity of high-quality
                                              ation performance, surpassing standalone LLMs                   HDL data relative to software corpora, which limits the
                                              and prior agentic systems. Code and dataset are                 models’ exposure to high-quality RTL patterns and actual
                                              available at GitHub.                                            verification-driven development practices (Liu et al., 2024;
                                                                                                              Zhu et al., 2025).
                                                                                                              To bridge this gap, recent methods have strengthened LLM-
                                         1. Introduction                                                      based RTL code generation through domain adaptation
                                         The explosive demand for computing power in the era of               and tool augmentation, including supervised fine-tuning
                                         artificial intelligence and digital transformation continues         (SFT) (Thakur et al., 2024; Lu et al., 2024; Liu et al., 2024)
                                         to push chip designs to billions of transistors, raising the         and reinforcement learning (RL) (Zhu et al., 2025; Min et al.,
                                                                                                              2025b) on curated HDL corpora, retrieval of reference im-
                                            1
                                              School of Physics and Astronomy, The University of Ed-          plementations (Gao et al., 2024; Liu et al., 2023), and tool-
                                         inburgh, Edinburgh, UK 2 State Key Laboratory of Analog and          in-the-loop prompting with simulation feedback (Thakur
                                         Mixed-Signal VLSI, University of Macau, Macau 3 School of Sci-       et al., 2023; Ho et al., 2025; Zhao et al., 2025). While
                                         ence and Engineering, The Chinese University of Hong Kong,
                                         Shenzhen, Shenzhen, China. Correspondence to: Jiale Liu              these techniques improve compile rates and module-level
                                         <Jiale.Liu@ed.ac.uk>.                                                functional pass rates compared to baselines, they remain in-
                                                                                                              sufficient for industrial-scale RTL blocks where correctness
                                         Preprint. January 28, 2026.

                                                                                                          1
                                 V ERI -S URE: Multi-Agent Framework for Correct RTL Code

depends on subtle temporal corner cases and multi-iteration              • We integrate a multi-branch verification and debugging
refinements. In particular, we identify that existing LLM-                 pipeline that goes beyond simulation by combining
based pipelines are still bottlenecked by (i) limited test case            trace-driven temporal analysis with formal verification,
coverage and code reliability due to simulation-centric eval-              including assertion-based checking and Boolean equiv-
uations, (ii) regression risk, potential hallucinations, and               alence proofs, improving overall code reliability and
inefficiency caused by whole-file regeneration during de-                  correctness.
bugging, and (iii) semantic drift as cycle-accurate intent is
gradually reinterpreted across iterations or agent handoffs.             • We introduce V ERILOG E VAL - V 2-EXT, extending the
Given that hardware bugs can survive simulation and lead                   original benchmark with expanded task coverage and
to costly tape-out failures, an effective RTL code genera-                 stratified difficulty levels, and demonstrate state-of-the-
tion system should not only be able to generate HDL code                   art verified-correct RTL code generation performance
but also independently perform verification, debugging to                  against standalone LLMs and agentic baselines.
ensure the realiability and correctness of the whole design.
Moreover, progress toward industrial-grade RTL code gen-              2. Related Work
eration is difficult to measure with existing public bench-
marks. Widely used datasets such as VerilogEval-v2 (Pinck-            2.1. Automatic RTL Code Generation
ney et al., 2025) are dominated by short, pedagogical mod-            Early studies explored open-loop RTL code generation with
ules and under-represent key industrial needs like advanced           general-purpose LLMs via zero-shot or few-shot prompt-
arithmetic units, communication protocols, buffer/memory              ing. Systems such as ChatEDA (Wu et al., 2024) and
control, Clock Domain Crossing (CDC) related patterns,                ChipNeMo (Liu et al., 2023) demonstrated the promise
and pipeline-style designs. They also lack difficulty stratifi-       of natural-language-to-RTL workflows, but also highlighted
cation for diagnosing the failure modes of systems.                   a recurring gap: models may produce syntactically plausi-
To address these challenges, we propose V ERI -S URE, a               ble Verilog code while violating cycle-accurate behavior,
contract-aware multi-agent framework with trace-driven                protocol semantics, or synthesizability constraints.
temporal analysis and formal verification. V ERI -S URE first         To improve domain alignment, subsequent work moved be-
distills the natural language specification into a structured         yond vanilla prompting toward domain-adapted training and
design contract that fixes interface semantics and cycle ac-          generation scaffolding. Fine-tuning on curated HDL cor-
curate intent, then uses this contract as the shared source of        pora, as demonstrated by VeriGen (Thakur et al., 2024) and
truth across agents. It then generates candidate RTL code             RTLLM (Lu et al., 2024), improves syntax validity and ba-
and validates it through simulation. When simulation fails,           sic module-level functionality. RTLCoder (Liu et al., 2024)
V ERI -S URE performs diagnosis using the temporal analy-             further filters examples through verification to reduce noisy
sis and contract derived formal checks, including assertion           RTL patterns. BetterV (Pei et al., 2024) introduces a genera-
checking and Boolean equivalence proofs. Guided by the                tive discriminator to steer outputs toward more verifiable im-
diagnosis, it applies dependency-slicing-guided patching to           plementations, while CodeV-R1 (Zhu et al., 2025) couples
perform precise, localized repairs, avoiding unstable whole           fine-tuning with multi-level code summarization to improve
file rewrites. Finally, we introduce V ERILOG E VAL - V 2-            long-range coherence. Orthogonally, AutoVCoder (Gao
EXT, which extends VerilogEval-v2 with 53 industry-grade              et al., 2024) leverages retrieval-augmented generation to
tasks and a structure-based difficulty level classification to        condition synthesis on relevant reference designs.
enable finer-grained evaluation. Our main contributions are
summarized as follows:                                                Despite steady progress, these methods still struggle with
                                                                      concurrent circuit behavior and strict timing requirements,
                                                                      largely because they lack iterative fixing that is central to
   • We design V ERI -S URE, a multi-agent framework for              real-world EDA workflows.
     RTL code generation that tightly couples LLM code
     synthesis with an automated generate-verify-debug                2.2. Tool-Integrated LLM Systems for HDL
     loop, leveraging simulation, trace-driven temporal anal-
     ysis, and formal verification.                                   Recent work has moved toward tool-in-the-loop and agentic
                                                                      pipelines that iteratively generate RTL, run simulation, and
   • We propose a dependency-slicing-guided patching                  repair failures. AutoChip (Thakur et al., 2023) closes the
     mechanism that leverages static dependency slicing               loop using simulator feedback, and RTLFixer (Tsai et al.,
     over signal relationships to localize failing behav-             2024) supports iterative debugging with error-driven edits.
     iors and apply precise, minimal edits, avoiding costly           These approaches reduce syntax errors and shallow func-
     whole-file regeneration and reducing regression risks            tional bugs; however, their debugging signals are dominated
     and repair hallucinations.                                       by sparse pass/fail outcomes or textual logs, which pro-

                                                                  2
                                               V ERI -S URE: Multi-Agent Framework for Correct RTL Code

                                                                                  Design                                                                                                                      Initial
                                   Contract                                                                                                                              Testbench                          Simulation
                                    Linter             Lint                      Contract
                                                      Check
                                                                           I/O                                                                                           code tb.sv                                      Main
                                                                                                     Function
                                                                         Defines
                                                                                                                Stick to      Verifier Agent    Initial                                                                  Flow
                                                                                                                Contract                       Version
                                                                         Timing/                      Corner                                                                                                             Debug
      Natural                                                            Latency                      cases                                                                      DUT                                      Flow
     Language                      Architect                                                                                                                                                                              Final
                                                                         Clock/Reset Semantics                                                                          code rtl.sv
        Spec                        Agent                                                                                                                                                                                Output
                                                                                                                              Coder Agent

           The Agents                                                                                                                                                 Simulation                                Pass
                                                       Asserter Agent                                                         Localized
                                                                                                                              Patching         Fail                  （Verilator）
                                                          Triggered Assertions for Debugging

                                                       { "id": "NO_NEGEDGE_UPDATE",
                                                         "t": "20",

     Architect      Verifier            Sequential       "msg": "predict_history
                                                       changed on negedge clk (wrong                                                           Trace-driven Temporal Analysis
                                          Logic
                                                       edge?). prev=00000000
                                                       now=00000001" }                                                                                VCD Waveform
                                                                                                                                                                                                                         Verified-
                                                                                                                                                                                        Trace Report
                                                                                                          Formal                                                                  { "sig": "q",
                                                                                                                                                                                    "expected": "1000",
                                                                                                                                                                                                                          Correct
                                                                                                                                                                                                                         RTL code
                                                                                                                                                                                    "actual": "1100" }
                                                                                                           Hints
                                                 Boolean Proofer Agent
      Coder        Debugger
                                                                                                                                                 Static Dependency Slicing
                                                             Boolean Logic Expressions

                                                        −𝐴 7 ⋅ 2! + ∑%"#$ 𝐴 𝑖 ⋅ 2" ×*−𝐵 7 ⋅ 2! +
                                                       ∑%&#$ 𝐵 𝑗 ⋅ 2& +
                                                                        %             !
                                                                                                                   Debugger                            Dependency Analysis                Localized Fault                Log & VCD
                                        Combina-        −𝐴 7 ⋅ 2! + ∑"#$  𝐴 𝑖 ⋅ 2" × ∑&#$ 𝐵 𝑗 ⋅ 2&
                                                                                                                    Agent
                                                                                                                                                 if (shift_ena) begin
                                                                                                                                                   q <= {data, q[3:1]};
                                                                                                                                                                                        Target: Block A1
                                                                                                                                                                                              Code:                      Waveform
                                       tional Logic
                                                                                                                                                      ...
                                                                                                                                                                                       “Start_line": 9,
                                                                   Equal?
                                                                                                                                                 end else if (count_ena) begin
                                                                                                                                                                                       “End_line": 19,
     Asserter    Boolean Proofer
                                                                                                                                                   q <= q - 4'd1;




                                                      Figure 1. An overview of our V ERI -S URE framework.


vide limited observability for diagnosing timing-dependent                                                                 driven temporal diagnosis, localized patching, and formal
failures and localizing root causes in multi-cycle designs.                                                                checking, as well as our benchmark extension designed to
                                                                                                                           better reflect industrial task distributions and difficulty.
A complementary line of work strengthens RTL code
generation by learning from structured supervision.
VeriSeek (Wang et al., 2025) incorporate structure-aware                                                                   3. The V ERI -S URE Framework
objectives (e.g., AST-based signals) to encourage hardware-
                                                                                                                           We propose V ERI -S URE, a multi-agent framework that
consistent patterns beyond test pass rates, while QiMeng-
                                                                                                                           brings a real EDA-style closed loop for development and
SALV (Zhang et al., 2025) introduces signal-aware learn-
                                                                                                                           testing to RTL synthesis from natural language. Rather than
ing to emphasize critical control-signal behavior. VeriL-
                                                                                                                           treating generation as a one-shot translation problem, V ERI -
ogos (Min et al., 2025b) combines synthetic augmenta-
                                                                                                                           S URE tightly couples code synthesis with automated valida-
tion with reinforcement learning to improve both diversity
                                                                                                                           tion and actionable debugging signals. Unlike prior multi-
and correctness, and DeepRTL (Liu et al., 2025) explores
                                                                                                                           agent systems that primarily coordinate through natural-
curriculum-style training to better align natural-language
                                                                                                                           language context and thus risk specification drift and coarse,
intent with RTL semantics. While these methods improve ro-
                                                                                                                           regression-prone rewrites, V ERI -S URE uses trace-driven
bustness, the supervision is still typically simulation-centric,
                                                                                                                           analysis to localize failures to concrete time windows, sig-
leaving coverage gaps on rare temporal corner cases and
                                                                                                                           nals, and violated requirements, enabling targeted fixes and
complex protocol behaviors.
                                                                                                                           improving robustness on multi-cycle corner cases. It also
As tasks scale to larger subsystems and multi-module de-                                                                   integrates simulation with formal checks to continuously
signs, multi-agent frameworks have been proposed to de-                                                                    enforce design requirements and help debugging.
compose the workflow into planning, coding, and checking.
REvolution (Min et al., 2025a) frames generation as an                                                                     3.1. Overall Architecture
evolutionary search with LLM-driven mutations, Verilog-
Coder (Ho et al., 2025) coordinates collaborative agents for                                                               Figure 1 shows the workflow of V ERI -S URE. The process
generation and validation, and MAGE (Zhao et al., 2025)                                                                    starts with (1) an Architect agent, which distills the user
improves candidate quality via diversified sampling and tar-                                                               prompt into a structured JSON-format design contract, cap-
geted debugging. AssertLLM (Yan et al., 2025) highlights                                                                   turing the Device Under Test (DUT) interface (ports, clock-
assertions as a mechanism to better encode architectural                                                                   /reset conventions), key parameters, and cycle-accurate be-
intent. Despite this progress, most agentic systems remain                                                                 havioral requirements. When a reference testbench is avail-
heavily dependent on test coverage, often apply coarse-                                                                    able, the Architect cross-checks interface and timing details
grained edits that risk regressions, and can accumulate se-                                                                to reduce ambiguity. Based on this specification, (2) a Veri-
mantic drift across iterations and agent handoffs; evaluation                                                              fier agent produces a self-checking testbench whose stimuli
also commonly relies on short, pedagogical benchmarks.                                                                     and checkers are aligned with the specified requirements.
These gaps motivate our V ERI -S URE that combines trace-                                                                  In parallel, (3) a Coder agent generates synthesizable RTL
                                                                                                                           code conditioned on the same specification. We then invoke

                                                                                                                     3
                                 V ERI -S URE: Multi-Agent Framework for Correct RTL Code

Verilator to compile and simulate the code against testbench;          (a) Failure Detection & Trace Analysis

                                                                                Simulation Log                                                         VCD Waveform
designs are accepted only if all checks pass.
                                                                               "data": "0",
                                                                               "q_dut": "1100",
When compilation or simulation fails, V ERI -S URE enters an                   "q_ref": "1000",
                                                                                                               Inspect

                                                                                                   UR      E
autonomous debugging loop led by (4) a Debugger agent.                                        FAIL
Rather than relying solely on textual error messages, the              (b) Static Slicing & Localization
Debugger leverages trace-driven temporal diagnosis: it an-                 Localized Fault                         Dependency Analysis                                     Trace Report
alyzes logs and waveforms via our slicing mechanism to                          Target:            Slicing     always_ff @(posedge clk) begin
                                                                                                                                                                       "fail_time": 370,
                                                                                                                                                                       "total_mismatches": 1572,
                                                                             Block ID A1                            if (shift_ena) begin                               "fail_outputs": [{

localize failures to concrete time windows and a minimal                         Code:
                                                                                                                        q <= {data, q[3:1]};
                                                                                                                        ...
                                                                                                                                                                           "sig": "q",
                                                                                                                                                                           "expected": "1000",
                                                                           “Start_line": 9,                         end else if (count_ena) begin                          "actual": "1100" }]

set of relevant signals. To further sharpen the feedback                   “End_line": 19,                              q <= q - 4'd1;



signal, (5) an Asserter agent generates targeted temporal              (c) Patching & Fixed
assertions to expose sequential/protocol violations, while                                          RTL File                                        RTL File
(6) a Boolean Proofer agent performs a checking of local-                                      Unchanged Code                                  Unchanged Code                          _________
                                                                                                                                                                                       Patched
ized combinational constraints to validate candidate fixes                                   14：if (shift_ena) begin
                                                                                             15：    q <= {data, q[3:1]};
                                                                                                                           Patching
                                                                                                                           (only Block A1)
                                                                                                                                             14：if (shift_ena) begin
                                                                                                                                             15：    q <= {q[2:0], data};
                                                                                                                                                                                         RTL

                                                                       Debugger Agent
and prevent regressions. The Debugger aggregates these                                         Unchanged Code                                   Unchanged Code

signals to apply minimal, localized edits to the RTL code
and iterates until all verification checks are satisfied.               Figure 2. The tracing, static slicing and patching mechanism.


3.2. Contract Design
                                                                      We then extract a short waveform window ending at tf from
Natural-language RTL specifications are often underspec-              the Value Change Dump (VCD) file and sample it on the
ified in details like reset polarity, sampling edge, or cycle         contract-defined clocking scheme. In addition to raw values,
latency, which easily leads to inconsistent interpretations           the trace reporter runs a lightweight alignment check to
across agents. V ERI -S URE mitigates this by having the Ar-          detect systematic off-by-one-cycle or wrong-edge bugs by
chitect agent compile the prompt into a compact, structured           testing small shifts and reporting the best-matching offset
design contract that makes such choices explicit before any           as a timing hint. All findings are summarized into a trace
code is written.                                                      report, including failing signals, the failure cycle, and the
                                                                      relevant trace slice.
The resulting contract is intentionally compact yet sufficient
to drive the pipeline: it records the chosen source of truth, a
typed module interface, clock/reset and sequential seman-             Static Dependency Slicing To avoid unfocused edits, the
tics, per-output latency, a precise functional summary with           trace slicer restricts attention to the cone of logic that can
corner cases, a directed test plan, and guidance for the veri-        influence the failing outputs. We parse the RTL into seman-
fier, coder, and debugger. When the prompt underspecifies             tic blocks, for example using continuous assignments and
details, the Architect makes assumptions explicit so they be-         always blocks, and compute per-block read/write sets R(B)
come checkable requirements. A lightweight contract linter            and W (B). A dependency edge exists when a block reads
then validates the schema and basic consistency, preventing           what another writes:
malformed or contradictory contracts from propagating into
code generation and verification.                                                  Bj ← Bi                     ⇔              R(Bj ) ∩ W (Bi ) ̸= ∅.                                               (2)

                                                                      Starting from the failing signals as seeds, we perform a
3.3. Tracing, Static Slicing & Patching
                                                                      bounded backward traversal to obtain a small suspect set
When simulation fails, the main challenge is to turn an               Bsus with block identifiers and line ranges. This converts
opaque mismatch count into a minimal, actionable edit with-           “the output mismatched” into “these few blocks are the plau-
out destabilizing unrelated logic. V ERI -S URE addresses this        sible causes,” dramatically shrinking the search space pre-
with a closed-loop debugging pipeline that couples dynamic            sented to the Debugger.
evidence (i.e. waveforms) with static structure (i.e. code
dependencies), producing a patching task for the Debugger             Localized Patching The Debugger is only allowed to edit
rather than a full-file rewrite, as shown in Figure 2.                blocks in Bsus via block-level read/replace operations; the
                                                                      rest of the file is preserved verbatim. Each patch is immedi-
Trace-driven Temporal Analysis From the simulator log                 ately checked by recompilation and re-simulation, and we
we identify the earliest divergence time and the signals              apply a simple rollback rule to prevent regressions. Writ-
responsible. Let ODUT (t) and Oexp (t) denote the observed            ing σ(RTL) = (tf , m) for the first-failure time and total
and expected output vectors at time t; we define                      mismatch count, we keep a patch only if it improves the
                                                                      failure signature, which means later first failure, or fewer
          tf = min{ t | ODUT (t) ̸= Oexp (t) }.            (1)        mismatches at the same tf ; otherwise we revert. This loop

                                                                  4
                                 V ERI -S URE: Multi-Agent Framework for Correct RTL Code

                                                                                                           System
grounds the repair process in concrete traces while main-                                      DSP &       Control             Finite State
                                                                                                                                Machines
taining stability across iterations.                                              Storage
                                                                                                DIP




                                                                                                             4.8%
                                                                                  & CDC




                                                                                                                                .3%
                                                                                                    4.8
                                                                                                       %




                                                                                                                              15
3.4. Formal Verification                                                 Communication




                                                                                             4.
                                                                                               8%
                                                                           Protocols




                                                                                                  4% d
                                                                                     4.8




                                                                                                5. de
Simulation provides concrete counterexamples but offers                                 %




                                                                                                    )
                                                                                              (2 ten
limited coverage and often weak diagnostic signal. V ERI -              Advanced




                                                                                                Ex
                                                                                                                                                      Basic Comb
                                                                        Arithmetic 6.2%
                                                                                                                                                         Logic
S URE therefore augments the debugging loop with a two-                                                    VERILOGEVAL
                                                                                                                                              14.8%
branch, contract-driven verification pipeline: an Asserter                                                  V2-EXT
                                                                          Basic    3.8%
                                                                        Arithmetic




                                                                                                                               6% l
for sequential/timing obligations and a Boolean Proofer for




                                                                                                                             4. na
                                                                                                                                 )
                                                                                                                           (7 rigi
                                                                                         %
combinational equivalence. From the design contract C,
                                                     b we                             4.8
                                                                            Shift                                                      8.1




                                                                                                                             O
                                                                                                                                          %
                                                                          Registers
derive a small set of checkable obligations:                                                 5.
                                                                                               3%
                                                                                                                                               Multiplexing
                                                                                                                                               & Decoding




                                                                                                                               7.7
                                                                                 Circuit




                                                                                                       %
                                                                                                    7.2
              Φ = P(C)
                    b = Φseq ∪ Φcomb ,




                                                                                                                    7.7%
                                                          (3)




                                                                                                                                  %
                                                                               Algorithms

                                                                                             Flip-ﬂops                          Vector & Bit
which are then discharged by the two verifiers and translated                                & Latches         Counters         Operations
                                                                                                               & Timing
into structured hints for the Debugger.
                                                                         Figure 3. V ERILOG E VAL - V 2-EXT problem taxonomy.
Asserter for Timing Supervision Using clock/reset se-
mantics and latency annotations in C,
                                    b the Asserter generates
a small set of non-intrusive SystemVerilog assertions and            interface, and an executable testbench used for functional
attaches them to the DUT via binding. Assertions run under           checking, enabling direct comparison with prior results.
Verilator and report violations with type, implicated signals,
and time, effectively diagnosing issues such as wrong-edge
                                                                     4.1. Industrial-Grade Extension
sampling, reset mismatches, and off-by-one-cycle latency.
                                                                     VerilogEval-v2 offers strong coverage of basic digital logic
Boolean Proofer for Combinational Equivalence For                    problems, but it under-represents modules that dominate
purely combinational obligations, the Boolean Proofer first          real RTL development (e.g., protocol controllers, buffering,
infers candidate combinational targets from C  b (where la-          and multi-cycle datapaths). As a result, models may achieve
tency = 0) and filters out sequentially-driven signals via           high scores while still failing on engineering-critical behav-
a dependency analysis, avoiding invalid proofs on stateful           iors such as latency alignment, corner-case handling, and
logic. It then synthesizes a compact reference combina-              stateful control logic.
tional model from the contract’s functional summary and
                                                                     To address these gaps, we curated 53 new problems that
constructs a standard miter that compares DUT and refer-
                                                                     reflect common Intellectual Property (IP) blocks and sys-
ence under identical inputs. Writing the miter error as:
                                                                     tem components, including communication protocols and
                    _                                               buffering (e.g., Universal Asynchronous Receiver Transmit-
                                                 
        e(x) =              yDUT (x) ̸= yspec (x) ,      (4)
                                                                     ter (UART) interfaces and First-In-First-Out (FIFO) queues),
                  y∈Ycomb
                                                                     control-dominated designs (e.g., nontrivial Finite State Ma-
the goal is to prove ∀x, e(x) = 0 using SymbiYosys. If the           chines (FSMs), and richer datapath modules (e.g., advanced
proof fails, the resulting counterexample is distilled into a        arithmetic and DSP-style kernels). Figure 3 summarizes the
concrete input assignment.                                           resulting benchmark composition and details are provided
                                                                     in Appendix A.
The formal hints produced by the branches are injected into
the Debugger prompt, separating timing faults from pure
                                                                     4.2. Difficulty Annotations
Boolean faults and improving repair generalization.
                                                                     To support finer-grained analysis beyond an aggregate pass
4. The V ERILOG E VAL - V 2-EXT Benchmark                            rate, we stratify the 209 problems into Easy/Medium/Hard
                                                                     using a rule-based complexity score derived from observ-
We introduce V ERILOG E VAL - V 2-EXT, an expanded bench-            able structural signals, including lines of code, counts of
mark for evaluating LLMs on realistic RTL code generation.           assign/always/case constructs, and datapath width, supple-
It extends VerilogEval-v2 (Pinckney et al., 2025) with 53            mented with manual review. Full scoring details and thresh-
new, industrial-grade design tasks, increasing the total from        olds are provided in subsection A.3. Figure 4 shows that
156 to 209 problems. All tasks follow the same evalua-               the extension increases structural complexity, especially
tion protocol as VerilogEval-v2: each problem provides               within the Hard subset (e.g., longer solutions with more
a natural-language specification, a fully specified module           sequential structure and wider datapaths, up to 1024-bit).

                                                                 5
                                                         V ERI -S URE: Multi-Agent Framework for Correct RTL Code


       Non-empty RTL lines




                                                                    #assign statements
                             150                                                           16                                                      5




                                                                                                                                  #always blocks
                                                                                           14
                                                                                           12                                                      4
                             100                                                           10                                                      3
                                                                                            8
                                                                                            6                                                      2
                             50                                                             4                                                      1
                                                                                            2
                                 0                                                          0                                                      0
                                       Easy    Medium        Hard                                   Easy    Medium      Hard                            Easy     Medium         Hard

                                       (a) Code Length                                              (b) Assign Count                                   (c) Sequential Structure




                                                                    Max bit-width (bits)
                             5                                                             1024                                          always                   62%           70%
       #case statements




                                                                                                                                         assign                   63%           55%
                             4                                                                                                                                    47%           55%
                                                                                            128                                    nonblocking
                             3                                                                                                             case                   29%           29%
                                                                                             32                                      parameter                    20%           15%
                             2                                                                                                                                     3%            5%
                                                                                                                                       for-loop
                             1                                                                                                         function                    0%            5%
                                                                                                                                         signed                    0%            4%
                             0                                                                  1
                                     Easy     Medium         Hard                                    Easy   Medium       Hard                                   Original      Ours

                                     (d) Control Branching                                           (e) Data Width                                    (f) Construct Coverage
Figure 4. Dataset complexity statistics comparing the original one and ours (full extended dataset). (a–e) show distributions over problems
for different metrics and (f) reports the Verilog construct coverage.


Together, these additions make V ERILOG E VAL - V 2-EXT a                                                       et al., 2025) with the latest backbone model and report all
more discriminative and industry-aligned testbed for evalu-                                                     of the comparisons in Table 1.
ating end-to-end RTL code generation and debugging.
                                                                                                                Toolchain and Computing All methods use the same
5. Experiments                                                                                                  testbenches and verification toolchain. We use Verilator
                                                                                                                for syntax checking and simulation, chosen for its better
5.1. Experimental Setup                                                                                         support of SystemVerilog assertion-style checks used by our
Benchmark We evaluate on our V ERILOG E VAL - V 2-                                                              Asserter. For Boolean proof, we use SymbiYosys with a
EXT benchmark and report Pass@1 for syntax and func-                                                            Z3 backend. Commercial models are queried via official
tional correctness. Syntax success means the simulator                                                          APIs; open-weight models are run locally on NVIDIA A100
compiles the generated RTL code without errors. Func-                                                           80GB GPUs. Iterative methods are capped at most K=10
tional success means the compiled DUT passes the provided                                                       repair iterations.
testbench.
                                                                                                                5.2. Main Results
Baselines We compare V ERI -S URE against 15 standalone                                                         Table 1 reports the Pass@1 for syntax and functional cor-
LLMs1 , covering both commercial closed-source and re-                                                          rectness on V ERILOG E VAL - V 2-EXT, further broken down
cent open-weight models, that generate the DUT in a single                                                      by difficulty. We observe these key things:
attempt. We also include single-agent simulator-feedback
                                                                                                                Frontier closed models are strong out of the box: Among
baselines that wraps most2 models with an iterative com-
                                                                                                                standalone LLMs, commercial closed-source models deliver
pile/simulate loop, feeding Verilator logs back for regenera-
                                                                                                                consistently high syntax success and strong functional accu-
tion. Finally, we evaluate representative multi-agent frame-
                                                                                                                racy, especially on Medium and Hard tasks. This suggests
works, MAGE (Zhao et al., 2025) and VerilogCoder (Ho
                                                                                                                that large-scale general pretraining already confers substan-
   1                                                                                                            tial competence in RTL code generation and code-level
      For better clarity, we cite the models here rather than in the
tables: GPT-5.2 (OpenAI, 2026); Claude-4.5-Sonnet (Anthropic,                                                   reasoning, even without hardware-specific fine-tuning.
2025); Gemini-3-Pro (Google Deepmind, 2025); Qwen3-Max,
Qwen3-Coder-Plus (Qwen AI, 2025b;a; Yang et al., 2025); Mistral-                                                Specialized small models lag behind general large mod-
Medium-3.1, Ministral-3-14B, Devstral-2 (Mistral AI, 2025b; Liu                                                 els: In contrast, smaller models that are fine-tuned for RTL
et al., 2026; Mistral AI, 2025a); DeepSeek-3.2 (DeepSeek-AI et al.,                                             code generation do not necessarily outperform state-of-the-
2025); LLaMA-4-Maverick (Meta AI, 2025); GLM-4.7 (Zhipu
                                                                                                                art general-purpose large models. While these models often
AI, 2025; Team et al., 2025); QiMeng-SALV (Zhang et al., 2025);
RTL-Coder (Liu et al., 2024); CodeV-R1 (Zhu et al., 2025); VeriL-                                               achieve reasonable syntax rates, their functional pass rates
ogos (Min et al., 2025b).                                                                                       are markedly lower on the harder tasks, indicating that pa-
    2
      Sadly, we cannot afford to run Claude as an agentic system.                                               rameter scale and broad pretraining remain critical for multi-

                                                                                                            6
                                 V ERI -S URE: Multi-Agent Framework for Correct RTL Code

Table 1. Performance comparison on V ERILOG E VAL - V 2-EXT (Pass@1, %). Params reports total (active) parameters for MoE
models, and total for dense models; “w.” denotes “with” the specified backbone. Background colors indicate rankings in each column:
 1st , 2nd , and 3rd denote the Global Performance across all methods. Blue highlights the Group Best performance if they are not
in the global top-3. We assign these badges for standalone LLMs:  Best Open-Source: Top performing open-weights model. Ç High
Potential: Largest relative gain when enhanced by agents. W Efficiency King: Best performance-to-parameter ratio. j Reasoning
Expert: Best performance on the “Hard” subset. 8 Robust Performer: Minimal gap between Syntax and Functional scores.

                                                  Easy (n = 51)       Medium (n = 91)        Hard (n = 67)          Overall
Method                             Params
                                                  Syn.      Func.      Syn.       Func.       Syn.      Func.     Syn.     Func.
  Standalone LLMs
GPT-5.2                               -          100.00     94.12     100.00      79.12      100.00     59.70    100.00    76.56
Claude-4.5-Sonnet                     -          100.00     90.20     100.00      74.73       97.01     53.73     99.04    71.77
Gemini-3-Pro j                        -          100.00     94.12     100.00      85.71      100.00     62.69    100.00    80.38
Qwen3-Max                             -           96.08     86.27     93.41       54.95       86.57     37.31     91.87    56.94
Mistral-Medium-3.1                    -          100.00     78.43     87.91       52.75       77.61     19.40     87.56    48.33
DeepSeek-3.2                     685B (37B)       96.08     80.39     96.70       64.84       85.07     41.79     92.82    61.24
Qwen3-Coder-Plus                 480B (35B)       92.16     80.39      91.21      60.44       77.61     29.85     87.08    55.50
LLaMA-4-Maverick                 402B (17B)      100.00     86.27     85.71       53.85       76.12     32.84     86.12    55.02
GLM-4.7  8                      358B (32B)       96.08     90.20     86.81       70.33       71.64     44.78     84.21    66.99
Devstral-2                          123B          98.04     80.39     91.21       58.24       67.16     25.37     85.17    53.11
Ministral-3-14B Ç                    14B         94.12      70.59     71.43       29.67       55.22     11.94     71.77    33.97
QiMeng-SALV                          7B           96.08     66.67     95.60       53.85       88.06     22.39     93.30    46.89
RTL-Coder                           6.7B          94.12     64.71      83.52      29.67       65.67      5.97     80.38    30.62
CodeV-R1 W                           7B           88.24     74.51      92.31      54.95      64.18      23.88    82.30     49.76
VeriLogos                            7B           86.27     49.02      90.11      26.37       71.64      1.49     83.25    23.92
  Single Agent Systems (w. Simulator Feedback & Iterative Fix)
w. GPT-5.2                             -         100.00     96.08     100.00      81.32      100.00     59.70    100.00    77.99
w. Gemini-3-Pro                        -         100.00     96.08     100.00      86.81      100.00     70.15    100.00    83.73
w. Qwen3-Max                           -         100.00     94.12      92.31      68.13       89.55     44.78     93.30    66.99
w. Mistral-Medium-3.1                  -          98.04     78.43     95.60       56.04       89.55     31.34     94.26    53.59
w. DeepSeek-3.2                  685B (37B)      100.00     84.31      97.80      67.03       94.03     44.78     97.13    64.11
w. Qwen3-Coder-Plus              480B (35B)       98.04     80.39     93.41       63.74       88.06     31.34     92.82    57.42
w. LLaMA-4-Maverick              402B (17B)      100.00     92.16     91.21       59.34       79.10     32.84     89.47    58.85
w. GLM-4.7                       358B (32B)       98.04     94.12      96.70      81.32       92.54     58.21     95.69    77.03
w. Devstral-2                       123B         100.00     78.43     94.51       57.14       88.06     34.33     93.78    55.02
w. Ministral-3-14B                   14B          94.12     76.47      79.12      48.35       55.22     19.40     75.12    45.93
w. QiMeng-SALV                       7B           98.04     74.51     94.51       51.65       88.06     17.91     93.30    46.41
w. RTL-Coder                        6.7B          84.31     56.86      80.22      38.46       70.15      8.96     77.99    33.49
w. CodeV-R1                          7B           98.04     84.31      97.80      61.54       85.07     32.84     93.78    57.89
w. VeriLogos                          7B          96.08     56.86     86.81       24.18       82.09      4.48     87.56    25.84
  Multi Agents Systems
MAGE (w. GPT-5.2)                    -           100.00     96.08     100.00      95.60       98.51     77.61     99.52    89.95
VerilogCoder (w. GPT-5.2)            -           100.00     94.12     100.00      90.11      100.00     68.66    100.00    84.21
V ERI -S URE (w. DS-3.2)         685B (37B)      100.00    90.20       98.90      73.63       97.01     53.73     98.56    71.29
V ERI -S URE (w. GPT-5.2)            -           100.00    100.00     100.00      95.60      100.00     85.07    100.00    93.30


step temporal reasoning, corner cases, and control-heavy            Simply feeding simulator logs back to the same model,
designs. Practically, this gap is difficult to close by fine-       improves syntax and functional accuracy across all tested
tuning alone because training large backbones is compute            backbones, but the magnitude is model-dependent. Stronger
intensive.                                                          models tend to benefit modestly, while weaker or less robust
                                                                    models can gain substantially.
Feedback improves results, but gains vary by backbone:

                                                                7
                                              V ERI -S URE: Multi-Agent Framework for Correct RTL Code

          Spec (Contract Form)                                                  Spec Boolean Logic
  8x8        two’s-complement        signed                                         %                         %
  multiplication as a purely combinational                                                                                                                           Fixed RTL Code
                                                                    𝑃 = −𝐴 7 ⋅ 2! + ) 𝐴 𝑖 ⋅ 2" × −𝐵 7 ⋅ 2! + ) 𝐵 𝑗 ⋅ 2&
  sum of eight sign-extended-and-shifted
                                                                                   "#$                       &#$
  16-bit partial products gated by b[i]          Boolean                                                                                                 for (i = 0; i < 7; i = i + 1) begin
                                                 Proofer                                                                           Proof                   partial[i] = b[i] ? (a_ext <<< i) : 16'sd0;
                                                                                                                                (SymbiYosys)             end
             Wrong RTL Code                   Extract their                                                                                              partial[7] = b[7] ? - (a_ext <<< 7) : 16'sd0;
  always_comb begin                              logical                        Code Boolean Logic
      a_ext = { {8{a[7]}}, a };                expressions                               %              !
      for (i = 0; i < 8; i = i + 1) begin
        if (b[i])                             and compare                𝑃 = −𝐴 7 ⋅ 2! + ) 𝐴 𝑖 ⋅ 2" × ) 𝐵 𝑗 ⋅ 2&
          partial[i] = a_ext <<< i;                                                      "#$           &#$
                                                                                                                               Formal Hints                   Debugger                    Patching & Fix
                                                                                                                                                           Fix the problems
                    Failure Log                                              Inserted Assertion
                      & VCD                                                                                                     Simulation
                    Waveform                                       assertion
                                                                    always @(negedge clk) begin                                 (Verilator)                           Fixed RTL Code
                                                                       ph_prev_negedge <= predict_history;
                                                                       if (!areset) begin                                                                end else if (predict_valid) begin
            Wrong RTL Code                                               if (predict_history !==                                 Triggered Assertions
                                                                                                                                                                 GH <= {GH[30:0], predict_taken};
                                                 Asserter          ph_prev_negedge) begin                                                                    end
 end else if (predict_valid) begin                                                                                        { "id": "NO_NEGEDGE_UPDATE",
         GH <= {GH[30:0], predict_taken};                                  asserter_log("NO_NEGEDGE_UPDATE",                                                 // else: hold value implicitly
     end                                          Insert           $sformatf("predict_history changed on                    "t": "20",
                                                                                                                                                         end
                                                                   negedge clk (wrong edge?). prev=%h                       "msg": "predict_history
     // else: hold value implicitly           assertions and                                                              changed on negedge clk
                                                                                                                                                         assign predict_history = areset ? 32'h0 : GH;
                                                                   now=%h",
 end                                             examine             ph_prev_negedge, predict_history));                  (wrong edge?).
 assign predict_history = GH;
                                                problems                 end ... end ... end                              prev=00000000
                                                                                                                          now=00000001" }



Figure 5. Case study: formal-hint-guided debugging in V ERI -S URE. Boolean Proofer and Asserter agents help generate correct RTL
code.


Table 2. Ablation results of V ERI -S URE on V ERILOG E VAL -                                       largest drop, showing that precise localization and targeted
V 2-EXT (Func. Pass@1, %). Base model: GPT-5.2. Subscripts
                                                                                                    repairs dominate end-to-end accuracy. For Hard problems,
denote absolute drop in percentage points vs. the full framework.
                                                                                                    Formal Verification is also important: removing it reduces
 Variant                                                    Hard        Overall                     pass rate from 85.07% to 73.13% (-11.9 pp), indicating that
                                                                                                    proof-based feedback could help debug deep logical bugs
 GPT-5.2 (Standalone)                                59.70↓25.4 76.56↓16.7
 + Simulator Feedback & Fix                          59.70↓25.4 77.99↓15.3                          that may not surface under finite simulation.
 V ERI -S URE (full)                                   85.07      93.30
   w/o Contract (Architect Agent)                    82.09↓3.0 90.43↓2.9
                                                                                                    5.4. Case Study
   w/o Tracing, Slicing & Patching                   68.66↓16.4 82.30↓11.0                          In Figure 5, we illustrate how V ERI -S URE converts fail-
   w/o Formal Verification                           73.13↓11.9 89.47↓3.8
                                                                                                    ing executions into formal-hint-guided repairs. For an 8×8
                                                                                                    two’s-complement multiplier (top), the Boolean Proofer
                                                                                                    derives the contract-level Boolean model and proves in-
Multi-agent approaches are effective; V ERI -S URE per-                                             equivalence against the generated RTL via a SymbiYosys
forms best: Multi-agent frameworks (MAGE and Verilog-                                               miter, pinpointing the missing sign-bit contribution of b[7]
Coder, controlled to use GPT-5.2) generally outperform                                              and enabling a minimal patch to the partial-product logic.
both standalone inference and single-agent feedback, high-                                          For a control-heavy history-register block (bottom), the As-
lighting the value of curated tool use and role specialization.                                     serter injects a clock/reset assertion that triggers at the first
V ERI -S URE achieves the best overall functional Pass@1                                            violating cycle and reports the implicated signals/values,
(93.30%) with perfect syntax, and the largest advantage on                                          guiding the Debugger to fix the edge/reset handling without
Hard tasks (85.07% functional). It also boosts the open-                                            regenerating the whole module. More detailed case studies
weight MoE backbone DeepSeek-3.2 to 71.29% overall                                                  can be found in Appendix C.
functional Pass@1 (+10.05 pp over standalone; +7.18 pp
over single-agent feedback).
                                                                                                    6. Conclusion
5.3. Ablation Results                                                                               In this work, we present V ERI -S URE, a contract-aware
Table 2 isolates the contribution of each major V ERI -S URE                                        multi-agent framework that closes the RTL development
component. Overall, V ERI -S URE achieves 93.30% func-                                              loop by aligning generation with verification and localized
tional pass rate, improving substantially over GPT-5.2 stan-                                        repair. By distilling natural-language intent into a shared
dalone (76.56%) and simulator-feedback loop (77.99%),                                               design contract, V ERI -S URE mitigates semantic drift across
especially on hard problems (85.07% vs. 59.70%). Results                                            agents, while its waveform tracing and static slicing mecha-
also indicate that feedback alone is insufficient for hard RTL                                      nisms enable precise patching that avoids whole-file rewrites
tasks, and that most gains come from structured agentic                                             and reduces regression risk. Beyond simulation-centric eval-
verification and repair.                                                                            uation, we integrated formal verification to achieve better
                                                                                                    debugging capability. To measure progress on realistic RTL
Generally, removing any major component of V ERI -S URE                                             tasks, we also introduced V ERILOG E VAL - V 2-EXT, includ-
degrades performance. The most critical part is the Trac-                                           ing 53 more industrial-grade problems and difficulty stratifi-
ing, Slicing & Patching mechanism, disabling it causes the

                                                                                               8
                                  V ERI -S URE: Multi-Agent Framework for Correct RTL Code

cation. Experiments show that V ERI -S URE achieves state-               Huang, Z., Wu, Z., Li, Z., Zhang, Z., Xu, Z., Wang, Z.,
of-the-art verified-correct performance, reaching 93.30%                 Gu, Z., Zhu, Z., Li, Z., Zhang, Z., Xie, Z., Gao, Z., Pan,
overall functional pass rate; ablations confirm that the gains           Z., Yao, Z., Feng, B., Li, H., Cai, J. L., Ni, J., Xu, L., Li,
come primarily from our debugging pipeline. Overall, V ERI -             M., Tian, N., Chen, R. J., Jin, R. L., Li, S. S., Zhou, S.,
S URE demonstrates that the proposed methods can effec-                  Sun, T., Li, X. Q., Jin, X., Shen, X., Chen, X., Song, X.,
tively aid LLMs in generating RTL code, moving automated                 Zhou, X., Zhu, Y. X., Huang, Y., Li, Y., Zheng, Y., Zhu,
design closer toward silicon-grade correctness.                          Y., Ma, Y., Huang, Z., Xu, Z., Zhang, Z., Ji, D., Liang, J.,
                                                                         Guo, J., Chen, J., Xia, L., Wang, M., Li, M., Zhang, P.,
References                                                               Chen, R., Sun, S., Wu, S., Ye, S., Wang, T., Xiao, W. L.,
                                                                         An, W., Wang, X., Sun, X., Wang, X., Tang, Y., Zha, Y.,
Akyash, M. and Mardani Kamali, H. SimEval: Investigating                 Zhang, Z., Ju, Z., Zhang, Z., and Qu, Z. DeepSeek-V3.2:
  the Similarity Obstacle in LLM-based Hardware Code                     Pushing the Frontier of Open Large Language Models,
  Generation. In Proceedings of the 30th Asia and South                  December 2025. URL http://arxiv.org/abs/
  Pacific Design Automation Conference, ASPDAC ’25, pp.                  2512.02556. arXiv:2512.02556 [cs].
 1002–1007, New York, NY, USA, March 2025. Associa-
  tion for Computing Machinery. ISBN 979-8-4007-0635-                  Gao, M., Zhao, J., Lin, Z., Ding, W., Hou, X., Feng, Y., Li,
  6. doi: 10.1145/3658617.3697624. URL https://dl.                       C., and Guo, M. Autovcoder: A systematic framework
  acm.org/doi/10.1145/3658617.3697624.                                   for automated verilog code generation using llms. In
                                                                         2024 IEEE 42nd International Conference on Computer
Anthropic. Introducing Claude Sonnet 4.5, Septem-                        Design (ICCD), pp. 162–169. IEEE, 2024.
  ber 2025. URL https://www.anthropic.com/
  news/claude-sonnet-4-5.                                              Google Deepmind.    A new era of intelligence
                                                                        with Gemini 3, November 2025. URL https:
DeepSeek-AI, Liu, A., Mei, A., Lin, B., Xue, B., Wang,                  //blog.google/products-and-platforms/
  B., Xu, B., Wu, B., Zhang, B., Lin, C., Dong, C., Lu, C.,              products/gemini/gemini-3/.
  Zhao, C., Deng, C., Xu, C., Ruan, C., Dai, D., Guo, D.,
                                                                       Guo, D., Zhu, Q., Yang, D., Xie, Z., Dong, K., Zhang, W.,
 Yang, D., Chen, D., Li, E., Zhou, F., Lin, F., Dai, F., Hao,
                                                                         Chen, G., Bi, X., Wu, Y., Li, Y. K., Luo, F., Xiong, Y., and
  G., Chen, G., Li, G., Zhang, H., Xu, H., Li, H., Liang, H.,
                                                                         Liang, W. DeepSeek-Coder: When the Large Language
 Wei, H., Zhang, H., Luo, H., Ji, H., Ding, H., Tang, H.,
                                                                         Model Meets Programming – The Rise of Code Intel-
  Cao, H., Gao, H., Qu, H., Zeng, H., Huang, J., Li, J., Xu,
                                                                         ligence, January 2024. URL http://arxiv.org/
  J., Hu, J., Chen, J., Xiang, J., Yuan, J., Cheng, J., Zhu, J.,
                                                                         abs/2401.14196. arXiv:2401.14196 [cs].
  Ran, J., Jiang, J., Qiu, J., Li, J., Song, J., Dong, K., Gao,
  K., Guan, K., Huang, K., Zhou, K., Huang, K., Yu, K.,                Ho, C.-T., Ren, H., and Khailany, B. Verilogcoder: Au-
 Wang, L., Zhang, L., Wang, L., Zhao, L., Yin, L., Guo,                  tonomous verilog coding agents with graph-based plan-
  L., Luo, L., Ma, L., Wang, L., Zhang, L., Di, M. S., Xu,               ning and abstract syntax tree (ast)-based waveform trac-
  M. Y., Zhang, M., Zhang, M., Tang, M., Zhou, M., Huang,                ing tool. In Proceedings of the AAAI Conference on
  P., Cong, P., Wang, P., Wang, Q., Zhu, Q., Li, Q., Chen,              Artificial Intelligence, volume 39, pp. 300–307, 2025.
  Q., Du, Q., Xu, R., Ge, R., Zhang, R., Pan, R., Wang, R.,
 Yin, R., Xu, R., Shen, R., Zhang, R., Liu, S. H., Lu, S.,             Huang, S., Cheng, T., Liu, J. K., Hao, J., Song, L.,
  Zhou, S., Chen, S., Cai, S., Chen, S., Hu, S., Liu, S., Hu,           Xu, Y., Yang, J., Liu, J., Zhang, C., Chai, L., Yuan,
  S., Ma, S., Wang, S., Yu, S., Zhou, S., Pan, S., Zhou, S.,             R., Zhang, Z., Fu, J., Liu, Q., Zhang, G., Wang, Z.,
  Ni, T., Yun, T., Pei, T., Ye, T., Yue, T., Zeng, W., Liu, W.,          Qi, Y., Xu, Y., and Chu, W. OpenCoder: The Open
  Liang, W., Pang, W., Luo, W., Gao, W., Zhang, W., Gao,                 Cookbook for Top-Tier Code Large Language Mod-
  X., Wang, X., Bi, X., Liu, X., Wang, X., Chen, X., Zhang,              els, March 2025. URL http://arxiv.org/abs/
  X., Nie, X., Cheng, X., Liu, X., Xie, X., Liu, X., Yu, X.,             2411.04905. arXiv:2411.04905 [cs].
  Li, X., Yang, X., Li, X., Chen, X., Su, X., Pan, X., Lin, X.,        Jiang, J., Wang, F., Shen, J., Kim, S., and Kim, S. A Survey
  Fu, X., Wang, Y. Q., Zhang, Y., Xu, Y., Ma, Y., Li, Y., Li,             on Large Language Models for Code Generation. ACM
 Y., Zhao, Y., Sun, Y., Wang, Y., Qian, Y., Yu, Y., Zhang,                Transactions on Software Engineering and Methodology,
 Y., Ding, Y., Shi, Y., Xiong, Y., He, Y., Zhou, Y., Zhong,               35(2):1–72, February 2026. ISSN 1049-331X, 1557-
 Y., Piao, Y., Wang, Y., Chen, Y., Tan, Y., Wei, Y., Ma, Y.,              7392. doi: 10.1145/3747588. URL http://arxiv.
  Liu, Y., Yang, Y., Guo, Y., Wu, Y., Wu, Y., Cheng, Y., Ou,              org/abs/2406.00515. arXiv:2406.00515 [cs].
 Y., Xu, Y., Wang, Y., Gong, Y., Wu, Y., Zou, Y., Li, Y.,
  Xiong, Y., Luo, Y., You, Y., Liu, Y., Zhou, Y., Wu, Z. F.,           Liu, A. H., Khandelwal, K., Subramanian, S., Jouault, V.,
  Ren, Z. Z., Zhao, Z., Ren, Z., Sha, Z., Fu, Z., Xu, Z., Xie,           Rastogi, A., Sadé, A., Jeffares, A., Jiang, A., Cahill,
  Z., Zhang, Z., Hao, Z., Gou, Z., Ma, Z., Yan, Z., Shao, Z.,            A., Gavaudan, A., Sablayrolles, A., Héliou, A., You,

                                                                   9
                                  V ERI -S URE: Multi-Agent Framework for Correct RTL Code

  A., Ehrenberg, A., Lo, A., Eliseev, A., Calvi, A., Soori-              Min, K., Cho, K., Jang, J., and Kang, S. Revolution: An evo-
  yarachchi, A., Bout, B., Rozière, B., Monicault, B. D.,                lutionary framework for rtl generation driven by large lan-
  Lanfranchi, C., Barreau, C., Courtot, C., Grattarola, D.,               guage models. arXiv preprint arXiv:2510.21407, 2025a.
  Dabert, D., Casas, D. d. l., Chane-Sane, E., Ahmed, F.,
  Berrada, G., Ecrepont, G., Guinet, G., Novikov, G., Kun-               Min, K., Park, S., Park, H., Cho, J., and Kang, S. Improving
  sch, G., Lample, G., Martin, G., Gupta, G., Ludziejewski,               llm-based verilog code generation with data augmentation
  J., Rute, J., Studnia, J., Amar, J., Delas, J., Roberts, J. S.,         and rl. In 2025 Design, Automation & Test in Europe
  Yadav, K., Chandu, K., Jain, K., Aitchison, L., Fainsin,                Conference (DATE), pp. 1–7. IEEE, 2025b.
  L., Blier, L., Zhao, L., Martin, L., Saulnier, L., Gao, L.,            Mistral AI. Introducing: Devstral 2 and Mistral Vibe
  Buyl, M., Jennings, M., Pellat, M., Prins, M., Poirée,                 CLI. | Mistral AI, December 2025a. URL https://
  M., Guillaumin, M., Dinot, M., Futeral, M., Darrin, M.,                 mistral.ai/news/devstral-2-vibe-cli.
  Augustin, M., Chiquier, M., Schimpf, M., Grinsztajn, N.,
  Gupta, N., Raghuraman, N., Bousquet, O., Duchenne,                     Mistral AI. Medium is the new large. | Mistral AI,
  O., Wang, P., Platen, P. v., Jacob, P., Wambergue, P.,                  May 2025b. URL https://mistral.ai/news/
  Kurylowicz, P., Muddireddy, P. R., Chagniot, P., Stock,                 mistral-medium-3.
  P., Agrawal, P., Torroba, Q., Sauvestre, R., Soletskyi, R.,
  Menneer, R., Vaze, S., Barry, S., Gandhi, S., Waghjale, S.,            OpenAI.    Introducing GPT-5.2, January 2026.
  Gandhi, S., Ghosh, S., Mishra, S., Aithal, S., Antoniak,                 URL           https://openai.com/index/
  S., Scao, T. L., Cachet, T., Sorg, T. S., Lavril, T., Saada,             introducing-gpt-5-2/.
  T. N., Chabal, T., Foubert, T., Robert, T., Wang, T., Law-
                                                                         Pei, Z., Zhen, H.-L., Yuan, M., Huang, Y., and Yu, B. Bet-
  son, T., Bewley, T., Bewley, T., Edwards, T., Jamil, U.,
                                                                           terv: Controlled verilog generation with discriminative
  Tomasini, U., Nemychnikova, V., Phung, V., Maladière,
                                                                           guidance. arXiv preprint arXiv:2402.03375, 2024.
  V., Richard, V., Bouaziz, W., Li, W.-D., Marshall, W.,
  Li, X., Yang, X., Ouahidi, Y. E., Wang, Y., Tang, Y., and              Pinckney, N., Batten, C., Liu, M., Ren, H., and Khailany,
  Ramzi, Z. Ministral 3, January 2026. URL http://                         B. Revisiting VerilogEval: A Year of Improvements
  arxiv.org/abs/2601.08584. arXiv:2601.08584                               in Large-Language Models for Hardware Code Gener-
  [cs].                                                                    ation, February 2025. URL http://arxiv.org/
                                                                           abs/2408.11053. arXiv:2408.11053 [cs].
Liu, M., Ene, T.-D., Kirby, R., Cheng, C., Pinckney, N.,
  Liang, R., Alben, J., Anand, H., Banerjee, S., Bayrak-                 Qwen AI. Qwen3-Coder: Agentic Coding in the World,
  taroglu, I., et al. Chipnemo: Domain-adapted llms for                   July 2025a. URL https://qwen.ai/blog?id=
  chip design. arXiv preprint arXiv:2311.00176, 2023.                     qwen3-coder.

                                                                         Qwen AI. Qwen3-Max: Just Scale it, September 2025b.
Liu, S., Fang, W., Lu, Y., Wang, J., Zhang, Q., Zhang, H.,
                                                                          URL https://qwen.ai/blog?id=qwen3-max.
  and Xie, Z. Rtlcoder: Fully open-source and efficient llm-
  assisted rtl code generation technique. IEEE Transactions              Team, G.-. ., Zeng, A., Lv, X., Zheng, Q., Hou, Z., Chen, B.,
  on Computer-Aided Design of Integrated Circuits and                      Xie, C., Wang, C., Yin, D., Zeng, H., Zhang, J., Wang, K.,
  Systems, 2024.                                                           Zhong, L., Liu, M., Lu, R., Cao, S., Zhang, X., Huang,
                                                                           X., Wei, Y., Cheng, Y., An, Y., Niu, Y., Wen, Y., Bai,
Liu, Y., Xu, C., Zhou, Y., Li, Z., and Xu, Q. Deeprtl: Bridg-              Y., Du, Z., Wang, Z., Zhu, Z., Zhang, B., Wen, B., Wu,
  ing verilog understanding and generation with a unified                  B., Xu, B., Huang, C., Zhao, C., Cai, C., Yu, C., Li, C.,
  representation model. arXiv preprint arXiv:2502.15832,                   Ge, C., Huang, C., Zhang, C., Xu, C., Zhu, C., Li, C.,
  2025.                                                                    Yin, C., Lin, D., Yang, D., Jiang, D., Ai, D., Zhu, E.,
                                                                           Wang, F., Pan, G., Wang, G., Sun, H., Li, H., Li, H., Hu,
Lu, Y., Liu, S., Zhang, Q., and Xie, Z. Rtllm: An open-                    H., Zhang, H., Peng, H., Tai, H., Zhang, H., Wang, H.,
  source benchmark for design rtl generation with large                    Yang, H., Liu, H., Zhao, H., Liu, H., Yan, H., Liu, H.,
  language model. In 2024 29th Asia and South Pacific                      Chen, H., Li, J., Zhao, J., Ren, J., Jiao, J., Zhao, J., Yan,
  Design Automation Conference (ASP-DAC), pp. 722–727.                     J., Wang, J., Gui, J., Zhao, J., Liu, J., Li, J., Li, J., Lu,
  IEEE, 2024.                                                              J., Wang, J., Yuan, J., Li, J., Du, J., Du, J., Liu, J., Zhi,
                                                                           J., Gao, J., Wang, K., Yang, L., Xu, L., Fan, L., Wu, L.,
Meta AI.    The Llama 4 herd: The beginning of                             Ding, L., Wang, L., Zhang, M., Li, M., Xu, M., Zhao,
 a new era of natively multimodal AI innovation,                           M., Zhai, M., Du, P., Dong, Q., Lei, S., Tu, S., Yang,
 April 2025. URL https://ai.meta.com/blog/                                 S., Lu, S., Li, S., Li, S., Shuang-Li, Yang, S., Yi, S., Yu,
 llama-4-multimodal-intelligence/.                                         T., Tian, W., Wang, W., Yu, W., Tam, W. L., Liang, W.,

                                                                    10
                                V ERI -S URE: Multi-Agent Framework for Correct RTL Code

  Liu, W., Wang, X., Jia, X., Gu, X., Ling, X., Wang, X.,               arxiv.org/abs/2505.09388. arXiv:2505.09388
  Fan, X., Pan, X., Zhang, X., Zhang, X., Fu, X., Zhang,                [cs].
  X., Xu, Y., Wu, Y., Lu, Y., Wang, Y., Zhou, Y., Pan, Y.,
  Zhang, Y., Wang, Y., Li, Y., Su, Y., Geng, Y., Zhu, Y.,             Zhang, Y., Zhang, R., Guo, J., Huang, L., Huang, D., Zhao,
  Yang, Y., Li, Y., Wu, Y., Li, Y., Liu, Y., Wang, Y., Li, Y.,          Y., Cheng, S., Jin, P., Li, C., Du, Z., et al. Qimeng-salv:
  Zhang, Y., Liu, Z., Yang, Z., Zhou, Z., Qiao, Z., Feng,               Signal-aware learning for verilog code generation. arXiv
  Z., Liu, Z., Zhang, Z., Wang, Z., Yao, Z., Wang, Z., Liu,             preprint arXiv:2510.19296, 2025.
  Z., Chai, Z., Li, Z., Zhao, Z., Chen, W., Zhai, J., Xu, B.,         Zhao, Y., Zhang, H., Huang, H., Yu, Z., and Zhao, J. Mage:
  Huang, M., Wang, H., Li, J., Dong, Y., and Tang, J. GLM-              A multi-agent engine for automated rtl code generation.
  4.5: Agentic, Reasoning, and Coding (ARC) Foundation                  In 2025 62nd ACM/IEEE Design Automation Conference
  Models, August 2025. URL http://arxiv.org/                            (DAC), pp. 1–7. IEEE, 2025.
  abs/2508.06471. arXiv:2508.06471 [cs].
                                                                      Zhipu AI. GLM-4.7: Advancing the Coding Capability, De-
Thakur, S., Blocklove, J., Pearce, H., Tan, B., Garg, S., and           cember 2025. URL https://z.ai/blog/glm-4.
  Karri, R. Autochip: Automating hdl generation using llm               7.
  feedback. arXiv preprint arXiv:2311.04887, 2023.
                                                                      Zhu, Y., Huang, D., Lyu, H., Zhang, X., Li, C., Shi, W.,
Thakur, S., Ahmad, B., Pearce, H., Tan, B., Dolan-Gavitt,
                                                                        Wu, Y., Mu, J., Wang, J., Zhao, Y., et al. Codev-r1:
  B., Karri, R., and Garg, S. Verigen: A large language
                                                                        Reasoning-enhanced verilog generation. arXiv preprint
  model for verilog code generation. ACM Transactions
                                                                        arXiv:2505.24183, 2025.
  on Design Automation of Electronic Systems, 29(3):1–31,
  2024.
Tsai, Y., Liu, M., and Ren, H. Rtlfixer: Automatically
  fixing rtl syntax errors with large language model. In
  Proceedings of the 61st ACM/IEEE Design Automation
  Conference, pp. 1–6, 2024.
Wang, N., Yao, B., Zhou, J., Hu, Y., Wang, X., Jiang, Z.,
 and Guan, N. Large language model for verilog genera-
 tion with code-structure-guided reinforcement learning.
 In 2025 IEEE International Conference on LLM-Aided
 Design (ICLAD), pp. 164–170. IEEE, 2025.
Wu, H., He, Z., Zhang, X., Yao, X., Zheng, S., Zheng,
 H., and Yu, B. Chateda: A large language model pow-
 ered autonomous agent for eda. IEEE Transactions on
 Computer-Aided Design of Integrated Circuits and Sys-
 tems, 43(10):3184–3197, 2024.
Yan, Z., Fang, W., Li, M., Li, M., Liu, S., Xie, Z., and
  Zhang, H. Assertllm: Generating hardware verification
  assertions from design specifications via multi-llms. In
  Proceedings of the 30th Asia and South Pacific Design
  Automation Conference, pp. 614–621, 2025.
Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B.,
  Yu, B., Gao, C., Huang, C., Lv, C., Zheng, C., Liu, D.,
  Zhou, F., Huang, F., Hu, F., Ge, H., Wei, H., Lin, H.,
  Tang, J., Yang, J., Tu, J., Zhang, J., Yang, J., Yang, J.,
  Zhou, J., Zhou, J., Lin, J., Dang, K., Bao, K., Yang, K.,
  Yu, L., Deng, L., Li, M., Xue, M., Li, M., Zhang, P.,
  Wang, P., Zhu, Q., Men, R., Gao, R., Liu, S., Luo, S.,
  Li, T., Tang, T., Yin, W., Ren, X., Wang, X., Zhang, X.,
  Ren, X., Fan, Y., Su, Y., Zhang, Y., Zhang, Y., Wan, Y.,
  Liu, Y., Wang, Z., Cui, Z., Zhang, Z., Zhou, Z., and Qiu,
  Z. Qwen3 Technical Report, May 2025. URL http://

                                                                 11
                                         V ERI -S URE: Multi-Agent Framework for Correct RTL Code

Appendices
We supplement some additional technical content here in the appendices. Specifically, Appendix A presents additional details
of the V ERILOG E VAL - V 2-EXT benchmark; Appendix B documents implementation details of the V ERI -S URE framework;
Appendix C reports three case studies; and Appendix D offers a detailed comparison with other related frameworks.

A. The V ERILOG E VAL - V 2-EXT Benchmark
This appendix provides additional details for V ERILOG E VAL - V 2-EXT, including (i) a full taxonomy and coverage analysis
of the original VerilogEval-v2 tasks, (ii) the motivations and design targets of our 53 newly added industrial-grade tasks, and
(iii) the rule-based difficulty grading scheme used in the paper.

A.1. Summary of Existing Problems
The original VerilogEval-v2 benchmark contains 156 RTL code generation tasks. While it offers a strong coverage of
basic digital logic problems, we find it under-represents the types of modules that dominate real RTL development, such
as protocol controllers, buffering, and multi-cycle datapaths. As a result, models can achieve high scores by mastering
local syntax patterns and short combinational reasoning, while still failing on engineering-critical behaviors like latency
alignment, corner-case handling, and stateful control logic. To make this limitation explicit and to identify concrete coverage
gaps, we manually reviewed all 156 problems and grouped them into nine categories, summarized in Table 3.


Taxonomy Methodology Each problem is assigned to the category that most strongly determines its implementation
structure (e.g., whether the solution is dominated by combinational datapath wiring, sequential state machines, or algorithmic
transformations). When a problem touches multiple concepts, we classify it by the dominant design pattern required to pass
the golden testbench.

Table 3. Full taxonomy of the original VerilogEval-v2 benchmark. We group problems into nine categories to reveal coverage biases and
industrial blind spots.

  Category                          #    Problem IDs                                    Description & Limitations

  I. Basic Logic Gates              16   Prob001, Prob005, Prob007, Prob011, Prob012,   Gate-level/bit-level Boolean logic. Limited depth and
                                         Prob013, Prob014, Prob019, Prob026, Prob043,   limited temporal reasoning.
                                         Prob051, Prob052, Prob059, Prob077, Prob087,
                                         Prob092
  II. Vectors & Bit Manipulation    14   Prob004, Prob006, Prob015, Prob023, Prob025,   Concatenation, slicing, bit-reversal, and parity. Does not
                                         Prob032, Prob042, Prob044, Prob055, Prob062,   cover real numeric formats (fixed-/floating-point).
                                         Prob064, Prob070, Prob094, Prob097
  III. Mux & Decoding               11   Prob017, Prob018, Prob021, Prob022, Prob039,   Standard mux/decoder/encoder usage. Mostly textbook
                                         Prob071, Prob076, Prob093, Prob104, Prob112,   patterns; little parameterization.
                                         Prob114
  IV. Basic Arithmetic              9    Prob009, Prob016, Prob024, Prob027, Prob030,   Mostly add/sub/popcount. Notably lacks multipliers/di-
                                         Prob033, Prob065, Prob081, Prob123             viders, saturation, and complex datapaths.
  V. Latches & Flip-Flops           14   Prob002, Prob003, Prob008, Prob028, Prob029,   Basic sequential primitives (DFF/latch). Almost entirely
                                         Prob031, Prob034, Prob041, Prob046, Prob047,   single-clock; does not test CDC patterns.
                                         Prob048, Prob049, Prob053, Prob073
  VI. Counters, Timers & Edge       15   Prob035, Prob037, Prob038, Prob040, Prob045,   Counting/timing logic. Typically linear control, limited
  Det.                                   Prob054, Prob066, Prob067, Prob068, Prob075,   handshake or flow-control complexity.
                                         Prob078, Prob080, Prob141, Prob151, Prob156
  VII. Shift Registers              12   Prob060, Prob061, Prob063, Prob082, Prob084,   Shifting/LFSR/pattern detection. Does not include
                                         Prob085, Prob086, Prob095, Prob096, Prob105,   streaming buffers (FIFO) or backpressure.
                                         Prob115, Prob118
  VIII. Finite State Machines       42   Prob036, Prob056, Prob072, Prob074, Prob079,   Largest category. Many are variants of tutorial sequence
  (FSMs)                                 Prob088, Prob089, Prob091, Prob099, Prob100,   detectors; few reflect on-chip protocols.
                                         Prob106, Prob107, Prob108, Prob109, Prob110,
                                         Prob111, Prob119, Prob120, Prob121, Prob124,
                                         Prob127, Prob128, Prob129, Prob133, Prob134,
                                         Prob135, Prob136, Prob137, Prob138, Prob139,
                                         Prob140, Prob142, Prob143, Prob144, Prob146,
                                         Prob147, Prob148, Prob149, Prob150, Prob152,
                                         Prob154, Prob155
  IX. Interpretation & Algorithms   23   Prob010, Prob020, Prob050, Prob057, Prob058,   Algorithmic “translation” tasks (e.g., Game of Life,
                                         Prob069, Prob083, Prob090, Prob098, Prob101,   waveform interpretation). Less representative of microar-
                                         Prob102, Prob103, Prob113, Prob116, Prob117,   chitecture.
                                         Prob122, Prob125, Prob126, Prob130, Prob131,
                                         Prob132, Prob145, Prob153




                                                                        12
                                 V ERI -S URE: Multi-Agent Framework for Correct RTL Code

Key Observations and Limitations This taxonomy highlights why simulation-only pass rates on VerilogEval-v2 can
overestimate progress toward silicon-grade RTL code generation:

   • Over-emphasis on short, textbook patterns: A large fraction of tasks are small-scale logic exercises (Categories
     I–III) or repetitive FSM variants (Category VIII).

   • Severe under-coverage of industrial datapaths: “Basic Arithmetic” comprises only 9/156 tasks, largely limited to
     simple integer operations.

   • Missing protocol and buffering semantics: The original set does not systematically test standard communication
     protocols (UART/SPI/I2 C) or ubiquitous flow-control primitives (FIFOs, skid buffers).

   • Limited exposure to CDC and multi-clock assumptions: Most tasks assume a single clock domain, ignoring
     reset-domain reasoning and CDC safety.

A.2. New Problems
To address the coverage gaps above, we introduce V ERILOG E VAL - V 2-EXT by adding 53 new industrial-grade tasks,
bringing the total to 209 problems. The new problems are designed to be industry-aligned, specifically targeting multi-cycle
behaviors and synthesizable constructs. We aim cover the missing areas detailed in Table 4

Table 4. Classifications of the 53 new tasks in V ERILOG E VAL - V 2-EXT. The categories are chosen to reflect common IP/SoC RTL
development patterns that are sparse or absent in the original VerilogEval-v2 benchmark.

Category                           Motivation                                      Representative RTL requirements
Advanced Arithmetic & Math         Modern AI/DSP chips depend on rich nu-          Multi-operator datapaths, corner-case handling (over-
                                   meric kernels; original is dominated by ad-     flow/saturation), and defined latency.
                                   d/sub tasks.
Standard Communication Proto-      Real chips communicate via standardized         Framing/encoding, CRC/parity, start/stop conditions,
cols                               serial protocols; absent in original set.       and valid-ready handshakes.
Memory, CDC & Flow Control         Buffering is ubiquitous; single-clock primi-    FIFO logic, full/empty semantics, backpressure, and
                                   tives are insufficient for system robustness.   safe control signaling.
DSP & Image Processing             Accelerators frequently embed DSP kernels;      Windowed/streaming computation, pipeline align-
                                   original tasks ignore structured data flow.     ment, and boundary handling.
Advanced Timing & System Con-      Timing/latency errors are common tape-out       Multi-stage pipelines, coordinated enables, complex
trol                               bugs; benchmarks need multi-cycle com-          FSM + datapath interaction.
                                   plexity.


A.3. Grading Scheme
To enable a more fine-grained analysis, we stratify the 209 problems into Easy/Medium/Hard using a rule-based structural
complexity score computed from the canonical RTL implementation. The complexity of hardware description language
(HDL) code can be systematically decomposed into three orthogonal dimensions: (i) structural complexity, which is
measured by the number of code lines (LOC) to reflect the scale and modularity of the design; (ii) data complexity, usually
reflected by the bit width for processing data to indicate numerical precision and storage requirements; and (iii) temporal
complexity, which is characterized by the diversity of temporal structures and nesting depth to represent the complexity of
temporal logic such as clock domains, state machines, and pipelines.
These three dimensions jointly determine the difficulty of understanding, implementing, and verifying the design. During
the construction process, these three dimensions are scored, with structural complexity mapped to the macroscopic indicator
of lines of code (LOC); data complexity is mainly represented by the maximum bit width (Max Width); and timing
complexity is jointly characterized by the complexity of assignment statements (#assign), the number of blocks (#always),
and conditional branches (#case) among other syntactic elements.
Therefore, the complexity score S is the sum of sub-scores derived from five metrics:

                                       S = sloc + sassign + salways + scase + swidth                                                (5)

                                                                13
                                V ERI -S URE: Multi-Agent Framework for Correct RTL Code

The scoring rules are detailed in Table 5. We map the total score S to difficulty labels:

                               Easy : S ≤ 1         Medium : 2 ≤ S ≤ 3              Hard : S ≥ 4.



                               Table 5. Scoring rules based on the structural complexity of designs.

                                   Metric          Thresholds                         Points
                                   LOC             ≤ 10 / 11–30 / 31–60 / > 60      0/1/2/3
                                   #Assign         ≤ 1 / 2–4 / ≥ 5                   0/1/2
                                   #Always         0/1/2/≥3                         0/1/2/3
                                   #Case           0/1/2/≥3                         0/1/2/3
                                   Max Width       ≤ 32 / 33–128 / > 128             0/1/2



Task Lists Applying this grading scheme, we obtain an initial difficulty label for each problem. We then did a manual
review of the resulting split to ensure the final annotations are consistent with human-perceived implementation and
verification difficulty. The final difficulty lists are:

   Easy (51 tasks)
   Prob001, Prob002, Prob003, Prob004, Prob005, Prob006, Prob007, Prob008, Prob009, Prob010, Prob011, Prob012,
   Prob013, Prob014, Prob015, Prob016, Prob019, Prob020, Prob022, Prob023, Prob024, Prob025, Prob027, Prob028,
   Prob029, Prob031, Prob034, Prob042, Prob043, Prob050, Prob055, Prob056, Prob057, Prob062, Prob083, Prob090,
   Prob098, Prob101, Prob102, Prob103, Prob131, Prob169, Prob188, Prob191, Prob194, Prob195, Prob197, Prob201,
   Prob202, Prob203, Prob207.




   Medium (91 tasks)
   Prob017, Prob018, Prob021, Prob026, Prob030, Prob032, Prob033, Prob035, Prob036, Prob037, Prob038, Prob039,
   Prob040, Prob041, Prob044, Prob045, Prob046, Prob047, Prob048, Prob049, Prob051, Prob052, Prob053, Prob054,
   Prob059, Prob060, Prob061, Prob063, Prob064, Prob065, Prob066, Prob067, Prob068, Prob069, Prob070, Prob071,
   Prob072, Prob073, Prob074, Prob075, Prob076, Prob077, Prob080, Prob081, Prob082, Prob084, Prob085, Prob091,
   Prob092, Prob093, Prob097, Prob099, Prob100, Prob104, Prob105, Prob106, Prob112, Prob113, Prob114, Prob116,
   Prob117, Prob118, Prob122, Prob123, Prob125, Prob126, Prob130, Prob132, Prob135, Prob141, Prob145, Prob163,
   Prob165, Prob168, Prob170, Prob171, Prob176, Prob178, Prob182, Prob183, Prob184, Prob186, Prob190, Prob193,
   Prob196, Prob198, Prob199, Prob200, Prob205, Prob208, Prob209.




   Hard (67 tasks)
   Prob058, Prob078, Prob079, Prob086, Prob087, Prob088, Prob089, Prob094, Prob095, Prob096, Prob107, Prob108,
   Prob109, Prob110, Prob111, Prob115, Prob119, Prob120, Prob121, Prob124, Prob127, Prob128, Prob129, Prob133,
   Prob134, Prob136, Prob137, Prob138, Prob139, Prob140, Prob142, Prob143, Prob144, Prob146, Prob147, Prob148,
   Prob149, Prob150, Prob151, Prob152, Prob153, Prob154, Prob155, Prob156, Prob157, Prob158, Prob159, Prob160,
   Prob161, Prob162, Prob164, Prob166, Prob167, Prob172, Prob173, Prob174, Prob175, Prob177, Prob179, Prob180,
   Prob181, Prob185, Prob187, Prob189, Prob192, Prob204, Prob206.




A.4. Issues with Prob099
During the construction and revision of our V ERILOG E VAL - V 2-EXT Benchmark, we have spotted some issues with the
original Prob099 design from VerilogEval-v2 under our Verilator environment. Specifically, when we attempted to compile
and run the Prob099 harness under Verilator, the build failed during elaboration with fatal named-port connection errors, so
the simulation never started and no functional comparison could be performed. In the Verilator log, the failure presents as
repeated PINNOTFOUND diagnostics indicating that the testbench tries to connect ports Y2 and Y4 on both the reference
instance and the DUT instance, even though those formal port names do not exist on the corresponding module definitions.
A representative excerpt is:

                                                                14
                                 V ERI -S URE: Multi-Agent Framework for Correct RTL Code


 1    %Error-PINNOTFOUND: ...Prob099_m2014_q6c_test.sv:74:4: Pin not found: ’Y2’
 2    %Error-PINNOTFOUND: ...Prob099_m2014_q6c_test.sv:75:4: Pin not found: ’Y4’
 3    %Error-PINNOTFOUND: ...Prob099_m2014_q6c_test.sv:80:4: Pin not found: ’Y2’
 4    %Error-PINNOTFOUND: ...Prob099_m2014_q6c_test.sv:81:4: Pin not found: ’Y4’
 5    %Error: Exiting due to 4 error(s)


The root cause is an interface mismatch between the testbench and the provided reference/DUT module definitions. The
reference module RefModule (and the auto-generated TopModule wrapper used for validation) exports outputs named
Y1 and Y3, but the testbench file instantiates both modules as if they exported Y2 and Y4. Verilator resolves named port
connections strictly: when it sees an instantiation such as .Y2(Y2 ref), it searches the callee’s port list for a formal named
Y2; if no such formal exists, it raises PINNOTFOUND and terminates. Conceptually, this is consistent with a naming/offset
confusion in the problem statement text: the prompt mentions “Y2 and Y4 corresponding to y[1] and y[3],” while the
actual reference implementation uses the convention “Y1 corresponds to the next-state signal for y[1] and Y3 corresponds
to the next-state signal for y[3].” In other words, the authoritative artifacts (reference module + wrapper) define Y1/Y3,
but the testbench was written against the inconsistent Y2/Y4 naming.
To fix the issue, we made the testbench consistent with the reference/DUT interface and with the benchmark’s intended
observation points. We renamed the internal signals and updated the named port connections in both instantiations
accordingly. We also aligned the testbench’s declaration of the state vector to the canonical module interface by changing
it from a 1-based range (logic [6:1] y) to the conventional 0-based range (logic [5:0] y) in both the stimulus
generator and the top-level testbench. After these changes, Verilator is able to compile the testbench successfully and
execute the simulation, and the DUT (when wrapped to mirror the reference) produces matching Y1 and Y3 outputs over the
randomized one-hot stimulus set.

B. V ERI -S URE: Additional Implementation Details
This appendix documents additional implementation-level details of V ERI -S URE that are omitted from the main paper
for clarity, including the design contract schema, linting rules, static dependency graph construction for localization, trace
alignment/slicing for temporal debugging, and formal miter generation for Boolean equivalence checking.

B.1. Contract Schema
As described in subsection 5.1, each benchmark task provides a fixed module interface and an executable testbench.
Nevertheless, the intent behind cycle-accurate behaviors (reset conventions, sampling edge, output latency, corner cases) is
frequently under-specified in natural language and can drift across iterations or agent handoffs. V ERI -S URE addresses this
by introducing a design contract as a structured intermediate representation (IR) shared across agents.

Required Fields      In our implementation, the contract is a JSON object with five required top-level sections:

     • module name: (string) The top-level DUT module identifier.

     • io: (list) An ordered list of port objects. Each port entry contains:
         – name: (string) Signal identifier (SystemVerilog identifier constraints).
         – dir: (string) One of {input, output, inout}.
         – width: (int) Positive integer bit-width (scalars use 1).
         – description: (string) Natural-language semantic summary.

     • clocking: (object) Global clock/reset semantics:
         – clock.name: clock signal name (must appear in io).
         – clock.edge: posedge or negedge.
         – reset.name: reset signal name (must appear in io).
         – reset.active: high or low.

                                                             15
                                 V ERI -S URE: Multi-Agent Framework for Correct RTL Code

       – reset.kind: sync or async.

   • timing: (object) A mapping from each output to its expected latency, in cycles, relative to contract-defined
     sampling:
       – timing.outputs[signal].latency cycles: (int) non-negative; 0 denotes combinational-by-
         contract.

   • functional summary: (object) A compact functional description used to ground verification, including
     Boolean/combinational obligations:
       – Typically contains a high-level overview plus a machine-readable list of rules describing input/output
         relations and corner cases.

Optional Fields To support richer tasks, the implementation also allows optional keys (ignored if absent), such as
parameters (typed module parameters), and test plan (directed stimulus/check intent).

Schema Usage The same contract instance is injected into: (i) the Coder prompt (to enforce interface/timing consistency),
(ii) the Verifier prompt (to generate a self-checking testbench consistent with the contract), (iii) the Asserter prompt (to
generate temporal assertions for the clock/reset/latency obligations), and (iv) the Boolean Proofer (to extract combinational
obligations for formal equivalence when applicable).

B.2. Contract Linting
To prevent malformed or hallucinated contracts from propagating into RTL code generation and verification, V ERI -S URE
applies a straightforward linter to every Architect-produced JSON before invoking downstream agents.

Linting Objectives     The linter enforces three classes of constraints:

 1. Schema validity (structure and typing): The linter checks presence of required keys (module name,
    io, clocking, timing, functional summary), validates that types are correct (e.g., width and
    latency cycles are integers), and rejects contracts with invalid enumerations (e.g., dir not in
    {input,output,inout}).

 2. Signal consistency and referential integrity: The linter ensures: (i) all port names are unique, (ii) all names match
    SystemVerilog identifier rules (no whitespace, no illegal characters), (iii) all signals referenced by clocking and
    timing.outputs exist in io, and (iv) widths are positive (scalar normalized to 1).

 3. Clock/reset integrity and canonicalization: Sequential semantics depend on consistent clock/reset conventions. If the
    contract indicates sequential behavior, the linter verifies that clock/reset are present in io. When the Architect omits
    clocking but the port list contains standard names (e.g., clk, rst, rst n), the linter infers missing clock/reset
    entries and makes these assumptions explicit in the canonicalized contract.

Canonicalization In addition to validation, the linter normalizes contracts to a canonical form to reduce downstream
ambiguity:

   • normalizes scalar widths to 1;

   • ensures timing.outputs exists for all outputs (defaulting missing entries to latency cycles = 0 unless
     otherwise implied);

   • preserves the io order (important for consistent rendering and debugging reports), while enabling fast name-to-port
     lookup via an internal dictionary.

If linting fails, V ERI -S URE does not attempt generation; instead the Architect is re-invoked with the lint error report to fix
the contract.

                                                               16
                                 V ERI -S URE: Multi-Agent Framework for Correct RTL Code

B.3. Static Dependency Graph Construction
V ERI -S URE localizes repairs using a static dependency slice over the RTL source (subsection 3.3). This slice is computed
from a dependency graph built directly from the SystemVerilog AST, rather than fragile regex matching.

Parsing Frontend We use tree-sitter-verilog to parse the generated RTL into an AST and extract semantic
units. This provides stable node spans (start/end line ranges) required by our block-level patching mechanism.

Block Granularity The RTL is decomposed into atomic RtlBlock units. A block is any semantic unit that can drive
signals:

   • Procedural blocks: always/always comb/always ff/always latch.

   • Continuous assignments: assign statements.

   • Submodule instances: treated as blocks to account for hierarchical wiring when present.

Each block stores a unique identifier, its source span (line range), its raw text, and statically extracted read/write sets.

Read/Write Extraction       For each block B, we compute:

   • W (B) (write set): all L-values written by the block (e.g., left-hand sides of = or <=, including bit/part selects mapped
     to their base identifiers).

   • R(B) (read set): all identifiers used as R-values in RHS expressions and control predicates (e.g., if conditions, case
     selectors), as well as explicit sensitivity list identifiers when present.

For module instances, W (B) and R(B) are inferred from the port connections when directionality is unambiguous;
otherwise, the instance is conservatively treated as reading all connected signals, and writing those connected to nets whose
names match the instance’s output connections in the AST.

Driver Map and Dependency Relation           We build a global driver map:

                                                 D(s) = { B | s ∈ W (B) },                                                     (6)

which maps each signal s to the set of blocks that may drive it. A directed dependency edge exists from Bi to Bj iff Bj
reads a signal written by Bi :
                                        Bj ← Bi ⇔ W (Bi ) ∩ R(Bj ) ̸= ∅,                                             (7)

Backward Depedency Slicing Given a failing output set Yfail identified by simulation/trace analysis, we compute the
suspect block set Bsus using a bounded backward BFS:
                                                         [
                                                 B0 =             D(y),                                                        (8)
                                                        y∈Yfail
                                                                   [      [
                                              Bd+1 = Bd ∪                       D(r),                                          (9)
                                                                  B∈Bd r∈R(B)


and finally Bsus = Bdmax . We use a small fixed depth bound dmax to balance localization precision and completeness:
deeper slices increase recall but also inflate the Debugger context window, which can reduce the precision of LLM-guided
patches.
The resulting Bsus is then used to enforce edit locality: the Debugger is only allowed to modify blocks within Bsus , while all
other lines are preserved verbatim, reducing regressions and “repair hallucinations”.

                                                                  17
                                 V ERI -S URE: Multi-Agent Framework for Correct RTL Code

B.4. Trace Alignment & Slicing
Simulation feedback is often too coarse (pass/fail or a single mismatch) to support reliable multi-cycle repairs. V ERI -S URE
therefore converts raw simulation artifacts into an LLM-consumable trace report that localizes failures in both time and
signal space.

Failure Localization The Verilator harness captures stdout/stderr and parses for the earliest failure event, including
assertion failures emitted by the Asserter or explicit mismatch diagnostics (e.g., “Mismatch at time . . . ”). This produces the
first failing timestamp tf (or equivalently a failure cycle index under the contract-defined sampling scheme).

Windowed Waveform Extraction              We extract a short window ending at the failure:

                                                W(tf ; K) = [tf − K · Tclk , tf ],                                           (10)

where Tclk is the clock period inferred from the testbench and K is a small constant (typically K=8 cycles). Using a VCD
parser, we sample signal values at the contract-specified clock edge (posedge or negedge) and record:

 1. the failing output signals Yfail (and their expected values when available),

 2. all top-level inputs (for context),

 3. internal state signals identified by the static slice (signals appearing in R(B) or W (B) for B ∈ Bsus ).

To keep reports compact, wide vectors are formatted in hexadecimal when possible, and stable signals may be elided if they
do not change throughout the window.

Alignment Diagnosis for off-by-one Timing Bugs Pipeline and handshake designs frequently fail due to a one-cycle
latency mismatch or sampling-edge errors. To provide actionable timing hints, the tracing mechanism performs a lightweight
alignment check by testing small cycle shifts δ ∈ {−2, −1, 0, +1, +2} between observed and expected outputs and
computing a mismatch score:
                                                   X
                                    score(δ) =         I[ODUT (t) ̸= Oexp (t + δ)] .                                  (11)
                                                       t∈W

If arg minδ score(δ) occurs at δ ̸= 0 with a significant score reduction, the report emits an explicit hint (e.g., “best alignment
at δ= + 1: output appears 1 cycle late”). This signal is complementary to assertion failures generated by the Asserter and is
particularly effective for diagnosing systematic latency shifts that may not be obvious from single-cycle mismatches.

Trace Report Format The final trace report includes: (i) the failure cycle/time, (ii) the set of failing outputs, (iii) the best
alignment hint (if any), and (iv) the windowed trace slice. This report is injected into the Debugger prompt together with the
localized suspect blocks Bsus , enabling the Debugger to propose minimal edits grounded in concrete temporal evidence.

B.5. Formal Miter Construction
The Boolean Proofer targets purely combinational logics by proving equivalence between (i) the DUT implementation and
(ii) a compact specification model synthesized from the contract. This is implemented using an automatically generated
miter.

Selecting Targets of Proof     From the contract timing map, we identify candidate combinational outputs:

                                  Ycomb = { y ∈ Outputs | latency cycles(y) = 0 }.                                           (12)

To avoid unsound proofs on stateful logic, we further filter Ycomb by dependency analysis: any output driven by an
always ff (or a clocked always) in the current RTL is excluded from combinational proving. This conservative rule
ensures the miter remains purely combinational.

                                                               18
                                V ERI -S URE: Multi-Agent Framework for Correct RTL Code

Model Synthesis and Wrapping We compile functional summary into a synthesizable SystemVerilog specification
module that computes each yspec in Ycomb from the shared inputs x. For simple Boolean expressions, this is emitted as
assign statements; for piecewise logic, it is emitted as always comb with if/case.
We generate then a wrapper that instantiates the DUT and module in parallel, ties their inputs, and asserts equality on
selected outputs. A simplified schematic is like:

        Example

  1    module Miter(/* shared inputs */);
  2      // shared inputs: declared here
  3      // dut/spec outputs
  4      logic [W-1:0] y_dut, y_spec;
  5
  6       dut_top dut (/* .a(a), .b(b), ... */, .y(y_dut));
  7       SpecModule spec (/* .a(a), .b(b), ... */, .y(y_spec));
  8
  9      always @* begin
 10        assert (y_dut == y_spec);
 11      end
 12    endmodule



Running SymbiYosys The DUT, specification module, and Miter are passed to SymbiYosys using an SMT-based proving
flow (Z3 backend in our setup). Since the miter is combinational, the proof reduces to a SAT/SMT validity query over ∀x. If
the proof fails, sby produces a counterexample assignment x⋆ ; we parse this model and translate it into a concrete input
vector (and, when applicable, a directed stimulus snippet) that is fed back to the Debugger. This provides a precise, minimal
witness of the Boolean mismatch and helps disambiguate pure logic faults from timing/latency faults already handled by the
trace and assertion branches.

C. Case Studies
C.1. Case Study 1: Boolean Proofer for an 8-bit Signed Multiplier
This case study evaluates the effectiveness of the Boolean Proofer on an 8-bit parallel multiplier (Prob157) designed using
two’s-complement arithmetic. The objective is to implement a purely combinational multiplier that calculates the product of
two 8-bit signed integers, a and b, by summing eight sign-extended and shifted 16-bit partial products. This corresponds to
the first case in Figure 5.

Problem Description Initially, a candidate implementation was tested against the formal specification. During Boolean
equivalence checking, the proofer identified a fundamental mismatch between the implementation logic and the mathematical
specification of signed multiplication.

Formal Specification and Counterexample The Boolean Proofer identified that the implementation treated the multiplier
b as an unsigned value, failing to account for the negative weight of the Most Significant Bit (MSB). The logical divergence
is summarized below:

      • Erroneous Implementation Logic:
                                                                                 !                 
                                                              6
                                                              X                        X7
                                       P =   −a[7] · 27 +            a[i] · 2i       ×   b[j] · 2j 
                                                               i=0                       j=0


      • Correct Specification Logic:
                                                                        !                                   
                                                      6
                                                      X                                        6
                                                                                               X
                               P =     −a[7] · 27 +         a[i] · 2i       × −b[7] · 27 +          b[j] · 2j 
                                                      i=0                                      j=0


                                                                 19
                                V ERI -S URE: Multi-Agent Framework for Correct RTL Code

Root Cause identification The error stemmed from a common misconception in signed arithmetic. In a two’s-complement
multiplier, the MSB of the multiplier, b[7], carries a negative weight (−27 ).

 1. Unsigned Weight Assumption: The original logic treated all bits of b as positive weights, effectively calculating
    A × Bunsigned .

 2. Partial Product Sign Error: For a correct signed product, the 8th partial product must be subtracted (or added as a
    two’s-complement negation) to account for the negative weight:
                                                   6
                                                   X
                                      P roduct =         (b[i] · (a ≪ i)) − (b[7] · (a ≪ 7))
                                                   i=0


Code Patching Following the feedback from the Boolean Proofer, the Verilog implementation was refined. The logic for
generating the 8th partial product was adjusted to handle the negative weight of the sign bit as shown in Listing 1.

Listing 1 C1 code correction.
--- buggy_multiplier.sv
+++ corrected_multiplier.sv
@@ -1,10 +1,8 @@
-// BUGGY: All bits treated as positive weights (unsigned multiplication)
-a_ext = { {8{a[7]}}, a };                 // Sign-extend a to 16 bits
-for (i = 0; i < 8; i = i + 1) begin       // Loop over all 8 bits
-    if (b[i])                             // If bit is set
-         partial[i] = a_ext <<< i;        // Add positive shifted value
-    else
-         partial[i] = 16’sd0;             // Otherwise add zero
-end
+// CORRECTED: b[7] treated as negative weight (signed multiplication)
+a_ext = { {8{a[7]}}, a };                     // Sign-extend a to 16 bits
+for (i = 0; i < 7; i = i + 1) begin           // Bits 0-6: positive weights
+    partial[i] = b[i] ? (a_ext <<< i) : 16’sd0;
+end
+partial[7] = b[7] ? -(a_ext <<< 7) : 16’sd0; // Bit 7: negative weight


The correction ensures that the last stage of the Wallace tree or adder array performs a subtraction for the MSB partial
product. The fix was validated using an exhaustive formal check, confirming that the implementation’s logical functions
perfectly matched the mathematical specification across all input spaces.

C.2. Case Study 2: Assertion Violation in Global History Register
This case study examines a timing violation detected during the formal verification of Pro118, involving improper state
updates in the Global History (GH) register logic. The violation stems from a signal transition occurring on the negative
edge of the clock, thereby breaching the synchronous design principle. This corresponds to the second case in Figure 5.

Problem Description During assertion-based verification, the monitor flagged a violation of the NO NEGEDGE UPDATE
property. This assertion enforces that the signal predict history must remain stable during the negative edge of the
clock (negedge clk), as any update at this phase indicates either asynchronous behavior or combinational leakage into
the sequential domain.

Formal Property and Counterexample The verification environment employs an Assertion-Based Verification monitor
with the following assertion shown in Listing 2
A counterexample was generated by the formal solver at simulation cycle t = 30 , where predict history changed
from 0x01 to 0x03 precisely on negedge clk. This illegal transition suggests the presence of either a combinational
path influencing the output or an asynchronous reset hazard coinciding with the assertion’s sampling window.

                                                              20
                                  V ERI -S URE: Multi-Agent Framework for Correct RTL Code

Listing 2 Formal property for negative-edge stability check.
always @(negedge clk) begin
    ph_prev <= predict_history;
    if (!areset) begin
        assert(predict_history === ph_prev)
        else $ error("Violation: predict_history toggled on negedge clk.");
    end
// Assertion: Signal stability on inactive clock edge
asserter_log("NO_NEGEDGE_UPDATE",
$sformatf("predict_history changed on negedge clk (wrong edge?). prev=%
  ph_prev_negedge, predict_history));
end



Root Cause Identification       Two flaws were identified in the original RTL implementation:

    1. Implicit Latch Risk: The sequential logic relied on implicit state retention (i.e., missing else clauses or default
       assignments). Under certain synthesis or formal analysis conditions, particularly during reset recovery, this can manifest
       as non-deterministic latch-like behavior.
    2. Reset-to-Output Combinational Path: The continuous assignment assign predict history = GH; created
       a transparent combinational path from the internal register GH to the observed output. When the asynchronous reset
       signal areset de-asserts asynchronously relative to clk, a transient glitch on predict history may occur
       exactly during the negedge clk sampling instant, triggering the assertion failure.

Code Patching To eliminate the violation, the design was refactored to enforce explicit state preservation and isolate
asynchronous reset effects from the observation point. The revised implementation uses a fully specified always ff block
with synchronous reset semantics and masks combinational glitches via a ternary operator as shown in Listing 3.

Listing 3 C2 code correction.
--- buggy_register.sv
+++ corrected_register.sv
@@ -1,12 +1,19 @@

+        // BUG: Incomplete case statement -> latch inference
         always @(posedge clk or posedge areset) begin
             if (areset) begin
                 GH <= 32’h0;
             end else begin
+                // Missing default case -> implicit latch
                 if (train_mispredicted)
                     GH <= {train_history[30:0], train_taken};
                 else if (predict_valid)
                     GH <= {GH[30:0], predict_taken};
             end
         end

-       // BUG: Direct combinational path
-       assign predict_history = GH; // Glitch propagates immediately
+       // FIX: Conditional assignment breaks combinational path
+       assign predict_history = areset ? 32’h0 : GH; // Safe observation
    endmodule


The correction ensures that predict history is driven only by a registered value (GH) when not in reset, and forced to
zero during reset, thereby eliminating any race between asynchronous reset release and clock edges. The fix was validated
using a Formal Equivalence Check , confirming functional equivalence while satisfying the NO NEGEDGE UPDATE assertion
across all reachable states.

                                                                21
                                 V ERI -S URE: Multi-Agent Framework for Correct RTL Code

C.3. Case Study 3: Automated Repair of Shift Direction Mismatch
This case study illustrates a common logical discrepancy between intended Register-Transfer Level (RTL) behavior and
the actual implementation within a multi-functional sequential circuit in Prob063. The target design is a 4-bit register
integrating two primary operations: (i) a left-shift with serial input data, and (ii) a modulo-16 decrement counter.

Problem Description A functional mismatch was identified when both control signals, shift ena and count ena,
were asserted. Per the specification, shift ena has higher priority; therefore, the register must perform a left shift
regardless of count ena.

Trace Analysis & Localization The failure was captured at simulation timestamp t = 370 ns. Inputs are sampled at
negedge clk and the register updates at the subsequent posedge clk. The trace log (summarized in Table 6) records
the pre-state q(t) at the sampling edge and the observed/expected next-state values at the following update edge.
As shown in the trace, the design is in state q(t)=4’b1100 with shift ena=1 and data=0. Under the required
left-shift specification, the next state must be {q[2:0], data} = {100, 0} = 4’b1000. However, the DUT pro-
duces 4’b0110, which corresponds to a right-shift style concatenation {data, q[3:1]}. The automated debugger
localized the failure to the shift transition logic via trace-driven temporal diagnosis, highlighting a bit-ordering error in the
concatenation.
Table 6. Failing transaction captured at t = 370 ns (inputs sampled at negedge clk; next state observed at the following posedge
clk).

                      Signal / State    Value             Description
                      clk               0 (negedge)       Sampling point for input vectors
                      shift ena         1                 Shift operation enabled (higher priority)
                      count ena         1                 Decrement enabled (masked by shift ena)
                      data              0                 Serial input bit for shifting
                      q(t)              1100              Register state before update
                      qref (t+1)        1000              Expected next state: {q[2:0], data}
                      qdut (t+1)        0110              Observed next state: {data, q[3:1]}


Root Cause Identification The localization tool identified the suspect logic within the always ff block. Inspection
of the RTL source confirms a directional implementation error: the design specification requires a left shift, but the
implementation used a right-shift concatenation, placing data at the MSB rather than the LSB.

Code Patching To resolve the discrepancy, the framework applied a localized patch that re-orders the concatenation to
match the left-shift specification (placing data at the LSB), as shown in Listing 4.

Listing 4 Localized code correction for the shift-direction bug.
--- buggy_shift.v
+++ corrected_shift.v
@@ -2,7 +2,7 @@
  always_ff @(posedge clk) begin
      if (shift_ena) begin
          // Shift operation
-         q <= {data, q[3:1]};      // Right-shift (BUG)
+         q <= {q[2:0], data};      // Left-shift (FIXED)
      end else if (count_ena) begin
          q <= q - 4’d1;
      end else begin


Subsequent re-simulation confirmed that the revised logic matches the golden model for all exercised traces, including
cases where shift ena and count ena are simultaneously asserted. By using localized patching instead of full-file
regeneration, the framework eliminated the mismatch while preserving the stability of the remaining logic.

                                                               22
                                V ERI -S URE: Multi-Agent Framework for Correct RTL Code

D. Detailed Framework Comparison
This appendix provides a comparison between V ERI -S URE and state-of-the-art frameworks, analyzing architectural
differences, capability gaps, and performance characteristics.
Table 7 provides a systematic comparison of core architectural features and capabilities across leading frameworks. The
table uses the following notation: ✓: Fully supported / High capability, ◦: Partially supported / Medium capability, ✗: Not
supported / Low capability, – : Not applicable.

                  Table 7. Comprehensive architectural and capability comparison of RTL generation frameworks.

Feature / Capability                 V ERI -S URE             MAGE            VerilogCoder        AutoChip         Single-Agent
  Core Architecture
Core Philosophy                Contract & Verification       Sampling        Planning & AST       Feedback          Feedback
Agents                             6 Specialized           4 Specialized      4 Specialized       2 General         1 General
Communication                   Structured Contract       Shared Context     Shared Context     Shared Context    Single Prompt
  Test & Verification
Testing Approach               Hybrid (Sim+Formal)        Simulation-only    Simulation-only    Simulation-only   Simulation-only
Formal Verification                     ✓                       ✗                  ✗                  ✗                 ✗
Assertion Generation                    ✓                       ✗                  ✗                  ✗                 ✗
Testbench Generation                    ✓                        ◦                  ◦                 ✗                 ✗
  Debugging & Repair
Repair Strategy                       Patching              Whole-file         Whole-file         Whole-file        Whole-file
Error Localization                   Block-level           Module-level       Module-level        File-level        File-level
  Performance & Efficiency
Token Efficiency                   Medium to Low               Low                Low                High              High
Iteration Efficiency                   High                   Medium              Low                Low               Low
Regression Safety                      High                   Medium              Low                Low               Low



E. Prompts of Agents
For a better presentation, please kindly refer to GitHub for this.




                                                              23
