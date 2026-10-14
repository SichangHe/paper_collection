                                           SpecLoop: An Agentic RTL-to-Specification
                                        Framework with Formal Verification Feedback Loop
                                                       Fu-Chieh Chang1 , Yu-Hsin Yang1 , Hung-Ming Huang1 , Yun-Chia Hsu2 , Yin-Yu Lin2 ,
                                                                      Ming-Fang Tsai2 , Chun-Chih Yang2 , Pei-Yuan Wu1
                                                            1
                                                                Graduate Institute of Communication Engineering, National Taiwan University, Taipei, Taiwan
                                                                                           2
                                                                                             MediaTek Inc, Hsinchu, Taiwan


                                           Abstract—RTL implementations frequently lack up-to-date or
                                        consistent specifications, making comprehension, maintenance,
                                        and verification costly and error-prone. While prior work has
arXiv:2603.02895v1 [cs.AR] 3 Mar 2026




                                        explored generating specifications from RTL using large language               Original
                                        models (LLMs), ensuring that the generated documents faithfully                 RTL               Spec generator           Candidate
                                                                                                                                                                                         Spec verifier
                                        capture design intent remains a major challenge. We present                                           (LLM)               specification
                                        SpecLoop, an agentic framework for RTL-to-specification gen-
                                                                                                                                                      Stop when spec verification passes
                                        eration with a formal-verification-driven iterative feedback loop.                                            or max iters reached
                                        SpecLoop first generates candidate specifications and then recon-                Task
                                        structs RTL from these specifications; it uses formal equivalence               prompt
                                                                                                                                                                                        Counterexample/
                                        checking tools between the reconstructed RTL and the original                                                                                     diagnostics
                                        design to validate functional consistency. When mismatches are
                                        detected, counterexamples are fed back to iteratively refine the       (a) The SpecLoop: iteratively generates and refines a candidate
                                        specifications until equivalence is proven or no further progress      specification using verifier feedback.
                                        can be made. Experiments across multiple LLMs and RTL
                                        benchmarks show that incorporating formal verification feedback            Stop when compile success
                                        substantially improves specification correctness and robustness                  or max iters reached     Compile error                   Compiler
                                        over LLM-only baselines, demonstrating the effectiveness of
                                        verification-guided specification generation.
                                           Index Terms—Verilog, Large Language Models, Formal Veri-
                                        fication, Design Automation                                                        Candidate            RTL reconstructor            Reconstructed
                                                                                                                          specification              (LLM)                       RTL



                                                                I. I NTRODUCTION
                                                                                                                            Original          Formal equivalence            report           Counterexample/
                                           Large language models (LLMs) have recently shown strong                           RTL                  checker                 [pass/fail]          diagnostics

                                        capabilities in hardware design automation, covering RTL
                                                                                                               (b) The spec verifier: reconstructs RTL from the specification and
                                        generation from specifications as well as RTL debugging                checks equivalence against the original design, returning diagnostics
                                        and rewriting. Prior works [1]–[5] improve RTL generation              for refinement.
                                        quality through an agentic, tool-augmented framework, pro-
                                        viding semantics-level signals for evaluating and correcting               Fig. 1: The architecture of SpecLoop and the spec verifier.
                                        generated designs. In the reverse direction, RTL-to-text tasks
                                        such as RTL understanding have also been studied [6]–[8],
                                        and early efforts have begun to explore RTL-to-specification           • We introduce an agentic RTL-to-specification generation
                                        generation [9]–[11].                                                     framework driven by a verification-guided loop, leveraging
                                           However, generating high-quality specifications from RTL              formal equivalence checking as semantics-level feedback.
                                                                                                               • We develop a strategy that separates compilation errors and
                                        remains challenging: specifications require high-level abstrac-
                                        tion of design intent and constraints, yet their quality is              functional mismatches, then uses actionable diagnostics to
                                        hard to measure and improve automatically. Inspired by the               improve the specification.
                                                                                                               • Our experiments show the framework benefits multiple
                                        reconstruction-based evaluation protocol of Huang et al. [11],
                                        we propose an agentic framework that integrates LLMs with                LLMs and RTL benchmarks, outperforming prior work [11].
                                        formal equivalent checking tools, enabling verification-guided           The approach achieves state-of-the-art RTL-to-specification
                                        RTL-to-specification generation that iteratively refines a can-          performance.
                                        didate specification using feedback from RTL reconstruction            Overall, our agentic verification-guided approach turns specifi-
                                        and formal equivalence checking against the original design.           cation generation into an iterative, checkable process, enabling
                                        Figure 1 provides an overview of the architecture. Our core            systematic improvement of spec quality beyond single-round
                                        contributions are:                                                     prompting.
TABLE I: Illustrative contrast between RTL understanding and                      modalities but remains largely qualitative. Huang et al. [11]
specification generation outputs of a given RTL snippet.                          evaluate RTL-to-spec generation extensively, yet focus only on
 Type            Example                                                          benchmarking. Unlike prior work, we are the first to explicitly
 RTL snippet     module HalfAdder (input a, input b, output
                 sum, output cout); assign {cout, sum} =
                                                                                  study how to improve spec quality using formal-verification-
                 a+b; endmodule                                                   guided iterative refinement.
 RTL             This Verilog code defines a module named HalfAdder that
 understanding   implements a basic half adder circuit. The module takes two
 (narrative)     single-bit inputs (a and b) and produces two outputs: sum                        III. S YSTEM A RCHITECTURE
                 (the result of the addition) and cout (carry out). The assign
                 statement uses concatenation to calculate both the sum bit and      Inspired by Huang et al. [11], we use an iterative
                 carry bit from the binary addition of inputs a and b.
 Specification   Top Module: HalfAdder. Inputs: a (1-bit), b (1-bit). Out-
                                                                                  reconstruction-and-check method. Figure 1 summarizes our
 generation      puts: sum (1-bit), cout (1-bit). Functional Description: This    agentic verification-guided RTL-to-specification framework.
 (structured)    module implements a half adder circuit that performs binary
                 addition of two 1-bit operands. The module takes two single-
                                                                                  Fig. 1a shows the architecture of SpecLoop, where the spec
                 bit inputs and produces a 1-bit sum output along with a 1-bit    generator produces a candidate specification from the input
                 carry-out output.
                                                                                  RTL code and task prompt. This candidate specification
                                                                                  is then passed to a spec verifier to check its correctness.
                                                                                  If verification fails, the resulting counterexamples and di-
                       II. R ELATED W ORK
                                                                                  agnostics are fed back to the spec generator to produce a
A. Agentic Tool-Use and Iterative Refinement in LLMs                              revised specification. This process iterates until equivalence is
   Recent work shows that LLM inference improves with                             proven or the maximum iteration budget is reached. Fig. 1b
external tools and feedback. Agentic tool-augmented methods                       shows the architecture of the spec verifier. It translates the
invoke compilers and analyzers [12]–[14], which are particu-                      candidate specification into reconstructed RTL via an RTL
larly effective in verifiable domains like programming. Sepa-                     reconstructor, then compiles it. If compilation fails, the com-
rately, LLMs can enhance responses via iterative refinement—                      pile errors are fed back to the reconstructor to regenerate a
reflection or self-correction [15]–[17]. Whether feedback is                      compilable design. The compilable RTL is then compared with
self- or tool-generated, both paradigms replace single-pass                       the original RTL using a formal equivalence checker, which
generation with multi-step error reduction. These findings mo-                    returns a report (pass/fail). On failure, the counterexamples
tivate our approach: tool-derived signals (compilation, equiva-                   and diagnostics are fed back to the spec generator to refine
lence checking) offer objective feedback, and iterative refine-                   the specification.
ment improves results across rounds.
                                                                                  A. Spec Generator
B. Agentic Tool Use for LLM-Based RTL Generation
                                                                                     Huang et al. [11] show that prompt design strongly in-
   Recent work has advanced agentic LLM frameworks that
                                                                                  fluences RTL-to-spec generation. We adapt and extend their
leverage external tools for RTL generation, debugging, and
                                                                                  multi-step reasoning prompt to enable reasoning and self-
rewriting. Compilation and simulation tools are used to im-
                                                                                  reflection before finalizing the specification and to enforce
prove RTL generation [3]–[5] and syntax repair [1]. Equiv-
                                                                                  a structured output format, as illustrated in Fig. 2. (1) The
alence checking tools are also integrated to rewrite RTL
                                                                                  left block shows our first-round prompt. It uses three steps:
while preserving behavior for better PPA [2], and to support
                                                                                  (a) analyze the RTL (signals, data/control flow, clock/reset);
dataset construction [18] and evaluation [19] in spec-to-RTL
                                                                                  (b) write a structured specification with fixed fields; and (c)
workflows. However, these methods do not transfer straight-
                                                                                  self-check for completeness and RTL consistency. (2) The
forwardly to the reverse task—RTL-to-specification—which
                                                                                  right block shows our refinement-round prompt. It asks the
remains challenging because specification quality is difficult
                                                                                  model to (a) summarize the verification report, (b) identify
to evaluate, limiting their direct applicability.
                                                                                  the likely root cause (see Sec. III-B and Sec. III-C), and (c)
C. RTL Understanding and Specification Generation                                 decide whether (and how) to revise only the affected spec-
   Prior RTL-to-text studies largely split into RTL understand-                   ification fields. This makes feedback actionable and enables
ing and specification generation. RTL understanding produces                      incremental improvements. At the bottom of these prompts,
narrative, often line-by-line explanations, whereas specifi-                      the output rules make our reconstruction-and-check pipeline
cation generation requires higher-level, structured semantics                     more robust. First, explicit reasoning steps improve correctness
(e.g., explicit port names). Table I gives a concrete contrast.                   and interpretability. Second, markers like [SPEC_START]
We summarize related work below. (i) RTL understanding.                           and [SPEC_END] keep specs easy to parse and tolerant of
Pinckney et al. [6] introduced CVDP. Liu et al. [7], [8]                          extra text. Third, forbidding Verilog code in specs pushes the
proposed DeepRTL and DeepRTL2. Both mainly target code-                           model toward generating abstract and concise specs.
level comprehension, not spec derivation; Pinckney et al. [6]
further note spec generation is a more challenging problem                        B. RTL Reconstructor
than comprehension. (ii) Specification generation. He et                             We use an LLM-based RTL reconstructor to turn each
al. [9] use synthetic specs to improve RTL generation, but                        natural-language specification into compilable RTL. Although
they focus on RTL quality. SpecLLM [10] categorizes spec                          this step enables semantics-level validation, reconstruction
   Prompt for spec generator (first round)                                                   Prompt for spec generator (refinement rounds with verification feedback)
   You are a senior hardware design engineer specializing in RTL design analysis             When spec verification fails, follow these steps carefully.
   and documentation. Your task is to interpret a Verilog RTL module between
   [RTL START] and [RTL END] and produce a precise, human-readable functional                Recall how verification works:
   specification.                                                                               1) An LLM reconstructs RTL code solely from your spec.
   Stage 1 — Internal Analysis (Reasoning): Internally, analyze the RTL step by                 2) A formal equivalence checker compares the reconstructed RTL against the
   step. You may reason through: (1) Signal definitions and bit widths (2) Data                     original RTL.
   dependencies between inputs, outputs, and internal logic (3) Sequential versus            Failure means the reconstructed RTL is NOT equivalent to the original — which
   combinational behavior (4) Control flow, counters, FSM transitions, and enable            may be caused by an ambiguous/incorrect spec OR by the reconstruction LLM’s
   signals (5) Clocking, reset conditions, and timing dependencies (6) Special or            misinterpretation.
   exceptional signal behaviors Use these reasoning steps to construct a correct and
   complete specification.                                                                   Step 1 — Summarize Verification Report: Concisely summarize the verification
   Stage 2 — Structured Specification Output: After reasoning, write the final               report between [REPORT START] and [REPORT END], including: (1) Which
   specification using the following format:                                                 output signals or properties were proven equivalent and which were not. (2) The
   [SPEC START]                                                                              specific counter-examples, mismatched signals, or logic discrepancies reported.
   Summary:                                                                                  (3) Any other issues beyond equivalent-checking that may have been discovered,
                                                                                             such as RTL syntax errors or multiple edge sensitive events.
       • Provide a concise overview of the design’s primary
           objective and overall functionality.                                              Step 2 — Root-Cause Analysis: For each equivalence failure, determine the
       • If multiple modules are present, first identify the                                 most likely cause: (1) Spec inaccuracy — the spec itself is wrong or incomplete
           top module and explicitly state its name in this                                  (e.g., wrong bit-width, missing signal, incorrect logic description, wrong clock/reset
           section.                                                                          polarity), so any faithful reconstruction would diverge from the original RTL.
   Module Name: <exact name from the RTL>                                                    (2) Spec ambiguity — the spec is technically consistent with the original RTL
   Inputs:                                                                                   but is worded ambiguously enough that the reconstruction LLM produced a valid
       • <signal_name> (<bit-width>): <concise purpose>
                                                                                             but different interpretation. (3) Reconstruction limitation — the spec is clear and
                                                                                             correct, but the reconstruction LLM failed to translate it accurately into RTL.
   Outputs:                                                                                  State your conclusion for each failure with a brief justification.
       • <signal_name> (<bit-width>): <concise purpose>

   Detailed Functional Description:                                                          Step 3 — Decision (1) If any failure is attributed to (a) spec inaccuracy, revise
                                                                                             the spec only to fix all identified errors. (2) If any failure is attributed to (b) spec
       • Describe the module’s purpose and how outputs are
                                                                                             ambiguity, revise the spec only to make the relevant description more precise
           derived from inputs.                                                              and unambiguous, without changing the intended meaning. (3) If all failures are
       • Explain internal logic, sequential behavior, and
                                                                                             attributed to (c) reconstruction limitation, output the spec from the previous
           control mechanisms coherently.                                                    iteration unchanged and stop.
       • Highlight any counters, state machines, arithmetic
           logic, or handshake signals.                                                      Output Rules: (1) You must clearly present your step-by-step reasoning pro-
   Clocking and Reset Behavior:                                                              cess before providing the final specification. (2) Enclose your final spec with
       • Specify active clock edge, reset polarity, and
                                                                                             [SPEC_START] and [SPEC_END]. (3) Do NOT output Verilog code within your
           initialization sequence.                                                          final spec. (4) Maintain a clear, formal, and technical tone appropriate for spec.
   Notes (if applicable):                                                                    [REPORT START]
       • Mention parameters, default values, pipeline
           latency, or exceptional conditions.                                               Spec Verification [pass/fail].

   [SPEC END]                                                                                # Reconstruction RTL:
   If multiple modules exist, describe each module separately using the structure above.
                                                                                             ...(omitted)...
   Stage 3 — Self-Reflection & Consistency Check: Before finalizing your answer:
   (1) Internally verify that all input/output signals mentioned exist in the RTL.
   (2) Ensure every output is explained in the Functional Description. (3) Verify
   clock and reset behavior are correctly identified. (4) If uncertainty remains, make       # Logs of equivalent-checking tool:
   reasonable inferences explicitly stated in the Notes section.                             ...(omitted, e.g. Mismatched Signals)...
   Output Rules: (1) You must clearly present your step-by-step reasoning process
   before providing the final specification. (2) Enclose your spec with [SPEC START]         [REPORT END]
   and [SPEC END]. (3) Do not output Verilog code within your final spec. (4) Main-
   tain a clear, formal, and technical tone appropriate for spec.
   [RTL START] . . . (omitted). . . [RTL END]


Fig. 2: Multi-step prompt templates for the specification generator. (Left) First round: analyze RTL, write a structured
specification, and self-check. (Right) Refinement: use verifier diagnostics (e.g., compiler errors or counterexamples) to edit
only affected fields and keep the rest unchanged. Some line breaks are omitted due to page limits.


may fail: the model can misinterpret underspecified require-                               tion is correct (see Sec. III-C and Sec. VI).
ments, miss corner cases, or produce syntactically invalid RTL.
                                                                                           C. Formal Equivalence Checker
As a result, an equivalence-check failure cannot be attributed
solely to the spec generator. To mitigate this confounder, we                                 We use a FEC tool to compare the original RTL with
separate reconstruction validity from functional equivalence.                              the reconstructed RTL. Compared to simulation, equivalence
Before formal equivalence checking (FEC), we compile the                                   checking provides an exhaustive, semantics-level criterion:
reconstructed RTL with a lightweight compiler; if compilation                              when it succeeds, it shows the specification is detailed enough
fails, we rerun reconstruction based on compile errors. If it                              for the reconstructed RTL to be functionally equivalent to the
compiles yet equivalence still fails, we consider the specifi-                             original. When the check fails, it may do so for several reasons:
cation incomplete or incorrect and feed back counterexamples                               E.1 Invalid original RTL. If the original RTL fails to compile
for refinement. Even so, reconstructor capacity may still bound                                 or cannot be parsed by the FEC tool, the checker may be
end-to-end performance, including cases where the specifica-                                    unable to produce a meaningful verdict. In this case, we
                                                                                                stop the iteration.
           TABLE II: Verifier error handling policy.                         is model-agnostic and requires no fine-tuning; we directly plug
  Error   To Reconstructor   To Spec Generator                               in existing LLMs. Accordingly, we evaluate a wide range
  E.1     Stop iteration     Non-verifiable; no feedback loop                of existing LLMs including Llama4-Scout, Llama4-Maverick,
  E.2     Reconstruct with   After reconstruct budget, send compile error
          compile errors                                                     Qwen3-Coder-30B, Qwen3-Coder-480B, DeepSeek-v3.1, and
  E.3     Reconstruct        After reconstruct budget, send counterexample   GLM-4.6, and observe consistent gains across model sizes and
  E.4     Reconstruct        After reconstruct budget, send error message
                                                                             architectures.

                                                                             B. Benchmarks and Metrics
E.2 Non-compilable reconstructed RTL. If the recon-
    structed RTL does not compile, we regard it as a re-                        We evaluate on two representative RTL benchmarks: Ver-
    construction failure and re-run the reconstructor with                   ilogEval [20] and RTLLM [21]. VerilogEval contains toy-
    compiler errors. Since such errors can also stem from                    level modules, whereas RTLLM includes larger designs. Since
    spec inaccuracy (e.g., missing widths), after a fixed retry              these benchmarks were originally designed for spec-to-RTL
    budget we attribute persistent failures to specification                 evaluation, we follow the RTL-to-spec protocol of Huang et
    quality and feed the compile error to the specification                  al. [11]: for each input RTL, we generate a natural-language
    generator.                                                               specification and evaluate it using the RTL Reconstruction
E.3 Functional mismatch. A true mismatch yields a coun-                      Score (RR score) [11]. RR checks whether RTL recon-
    terexample where output signals diverge. Since mis-                      structed from the specification passes the testbenches, with
    matches can also stem from reconstructor imperfections,                  reconstruction performed by GPT-5 Codex [22]. We choose
    we may repeat reconstruction up to a fixed budget; if                    RR over semantic-level alternatives such as GPT-Score [7]
    mismatches persist, we feed back the counterexample to                   because it is more sensitive to specification flaws [11] than
    the specification generator to amend the specification.                  semantic-level metrics. Although RR also includes an RTL-
E.4 Inconclusive failures. FEC may return inconclusive re-                   reconstruction step, it does not inherently favor our method:
    sults due to timeouts or other tool issues. We first re-run              (1) RR uses frontier reconstructors (e.g., the GPT-5 series)
    the reconstructor; if inconclusive outcomes persist, we                  for reconstruction fidelity, whereas SpecLoop uses the same
    attribute them to an ill-posed specification and send an                 (often weaker) model for both generation and reconstruction to
    error message to the spec generator requesting refinement.               avoid confounding extra capacity; and (2) RR evaluates recon-
                                                                             structed RTL with testbenches rather than formal equivalence,
                                                                             measuring behavior under the provided environments rather
Design choice—information hiding: To fairly assess the
                                                                             than our equivalence-checking objective.
information contained in the specification, we deliberately
do not feed FEC logs back to the reconstructor, because                      C. Baselines
they can reveal details of the original RTL (an input to the
                                                                                We consider two baselines. (1) Single Round: This follows
checker) and effectively bypass the specification. The only
                                                                             prior work [11]: the LLM produces a specification in a single
exception is compilation failures: we provide compiler errors
                                                                             pass from the input RTL, without verifier-guided refinement.
to the reconstructor because they do not directly leak original
                                                                             We reproduce their results with a minor prompt change
RTL semantics and are necessary to produce a compilable
                                                                             (enabling intermediate reasoning outputs) to make the outputs
design. We summarize the actions to the reconstructor and
                                                                             more interpretable. (2) Pass/Fail-only verifier: we run the
spec generator in Table II.
                                                                             same reconstruction and equivalence-checking pipeline, but
                   IV. E XPERIMENT S ETTINGS                                 the verifier only returns a binary decision (pass/fail) without
   We conduct experiments to evaluate our system along three                 diagnostic messages (e.g., compiler errors or counterexam-
questions: (1) whether verifier-guided refinement improves                   ples). On failure, we prompt the LLM to retry with no extra
RTL-to-specification generation over a single-round baseline;                signals, using the same retry budget as the full-feedback
(2) whether diagnostic feedback (compiler errors and coun-                   method.
terexamples) is more effective than a binary pass/fail signal;
                                                                             D. Other Implementation Details
and (3) how robust the pipeline is across different LLM
backbones and benchmarks.                                                       For equivalence checking, we use Yosys EQY [23] with a
                                                                             SAT backend and a depth bound of 10. We build a lightweight
A. LLM Candidates                                                            log parser that maps EQY outcomes to error types (E.1–
   We have two LLM roles in our pipeline: a specification gen-               E.4), and a VCD parser that extracts counterexamples for
erator and an RTL reconstructor. In principle, using a stronger              E.3. When error E.1 occurs, we terminate the feedback loop
reconstructor could reduce reconstruction-induced errors and                 since the case cannot benefit from verifier feedback. We
improve end-to-end success rates; however, it would also                     allow up to two retries for the spec generator, for three spec
confound comparisons by injecting additional model capacity.                 generations total including the initial round. Each spec allows
To isolate the contribution of our verification-guided loop, we              up to two RTL reconstructor retries. We call LLM APIs
use exactly the same LLM for both roles. Thus, any gain over                 through OpenRouter [24] and use a temperature of 0.4 to trade
single-round reflects verifier integration. Besides, our method              off stochastic decoding and correctness. To reduce statistical
TABLE III: Experimental results (mean ± std) on VerilogEval                        reflecting on reasoning steps or outcomes remains beneficial.
and RTLLM with RR-Score; darker tone indicates higher                              (iii) Richer diagnostics help the most. Full Diagnosis delivers
ranking. Verifier-guided variants (Pass/Fail-Only and Full Di-                     the strongest performance, indicating that detailed feedback
agnosis) outperform the Single-Round baseline; overall, Full                       (e.g., counterexamples) enables models to make more precise
Diagnosis ranks best, with Pass/Fail-Only ranks second.                            refinements. Overall, these results suggest that making RTL-to-
     Model\Method
                           Single Round         Pass/Fail-Only    Full Diagnosis   spec generation iterative and checkable improves end-to-end
                              ( [11])               (Ours)            (Ours)
                               Dataset: VerilogEval
                                                                                   correctness and achieves state-of-the-art performance over the
   Qwen3-Coder-30B       0.722 ± 0.016        0.759 ± 0.017      0.795 ± 0.021     prior single-round baseline.
  Qwen3-Coder-480B       0.885 ± 0.016        0.878 ± 0.009      0.912 ± 0.012
    DeepSeek-V3.1        0.865 ± 0.019        0.908 ± 0.011      0.940 ± 0.003
   Llama4-Scout-16E      0.686 ± 0.009        0.722 ± 0.016      0.705 ± 0.019     B. Verified vs. Unverified Specifications
 Llama4-Maverick-128E    0.818 ± 0.006        0.812 ± 0.017      0.842 ± 0.015
       GLM-4.6           0.906 ± 0.021        0.921 ± 0.006      0.934 ± 0.020        We further analyze the impact of the spec verifier in the
                                 Dataset: RTLLM                                    feedback loop. Figure 3 reports, for each model, the fraction
   Qwen3-Coder-30B       0.733 ± 0.009        0.747 ± 0.019      0.747 ± 0.019
  Qwen3-Coder-480B       0.767 ± 0.025        0.787 ± 0.019      0.767 ± 0.041     of samples achieving RR=1 and RR=0 in two groups: spec-
    DeepSeek-V3.1        0.767 ± 0.025        0.793 ± 0.025      0.800 ± 0.016     ifications verified (i.e., passing the spec verifier’s FEC) within
   Llama4-Scout-16E      0.667 ± 0.025        0.727 ± 0.034      0.687 ± 0.025
 Llama4-Maverick-128E    0.793 ± 0.034        0.767 ± 0.009      0.813 ± 0.009     the budget and those left unverified after budget exhaustion.
       GLM-4.6           0.813 ± 0.034        0.847 ± 0.009      0.880 ± 0.000
                                                                                   Each pie chart summarizes the verified vs. unverified split,
                                                                                   averaged over benchmarks and feedback variants (Pass/Fail-
                Llama4            Llama4             Qwen3            Qwen3        Only and Full Diagnosis). Two observations follow. (i) Verified
               Scout-16E       Maverick-128E        Coder-30B       Coder-480B
                                                                                   specifications are more likely to achieve RR=1. (ii) Stronger
                                                                                   RTL reconstructors yield a higher RR=1 ratio among verified
 Verified        81.3%             88.7%              85.5%             91%        specifications, as shown by Qwen3-Coder-480B and Llama4-
                                                                                   Maverick compared with Qwen3-Coder-30B and Llama4-
                                                                                   Scout. These observations suggest that verified specifications
                                                                                   are higher quality (by RR score), with larger gains for stronger
 Unverified      34.6%              45%               45.2%            42.8%       models.

                                                                                   C. Qualitative Study
                             RR=1            RR=0                                     Figure 4 presents a qualitative example. (i) The original
                                                                                   RTL design is a counter that increments from 0 to 999 with
Fig. 3: Ratio of verified specifications vs. unverified for
                                                                                   a synchronous reset. (ii) In the first LLM response, however,
different models and RR scores averaged over benchmarks and
                                                                                   the model incorrectly infers that the reset is asynchronous.
verifier variants. Verified specs show higher RR=1 proportions
                                                                                   (iii) Our spec-verification process then reconstructs RTL from
than unverified ones across models, especially for stronger
                                                                                   this incorrect specification; because the reconstructed design
models.
                                                                                   contains an asynchronous reset, the equivalence checker flags
                                                                                   a mismatch. (iv) We feed the resulting diagnosis back to the
                                                                                   LLM, and in the second round it correctly identifies that the
variance, we run each experiment three times and report the
                                                                                   mistake stems from mischaracterizing the reset behavior and
mean and standard deviation.
                                                                                   revises the specification to use a synchronous reset. (v) In the
                    V. E XPERIMENT R ESULTS                                        next verification round, the reconstructor produces a counter
                                                                                   with a synchronous reset and the design passes equivalence
A. Overall Quantitative Results                                                    checking. This example illustrates how the spec-verification
   Table III reports the RTL reconstruction score (mean ±                          loop can detect errors in generated specifications and guide
std) for three settings: Single Round, Pass/Fail-Only verifier,                    the LLM to fix them.
and Full Diagnosis. We highlight the following observa-
tions. (i) Iterative Loop consistently improves over Single-                                  VI. L IMITATIONS AND F UTURE W ORK
Round generation. Across results, adding the verification                             Our work has several limitations that fall into two cat-
loop (Pass/Fail-Only or Full Diagnosis) outperforms Single                         egories. Fundamental limitations of the reconstruction-
Round, indicating that verifier feedback—either a pass/fail                        based paradigm and metric: end-to-end results depend on
outcome or full diagnostic information (ranking highest in 4                       the RTL reconstructor and the equivalence-checking setup, so
and 9 among the 12 model/dataset settings, respectively)—is                        failures in reconstruction or resource-bounded checking (e.g.,
a valuable inference-time signal. (ii) Even a Pass/Fail-only                       fixed depth) can block useful feedback on harder designs.
verifier can outperform Single-Round generation. Despite                           Moreover, evaluation with the RR score also depends on the
lacking detailed diagnostics, Pass/Fail-only achieves more top                     reconstruction capabilities of frontier models. Engineering
rankings than Single-Round (4 vs. 0 across 12 model/dataset                        gaps that can be improved: feedback parsing and prompting
settings). This reflects observations from prior work [16], [17]                   remain heuristic, and scaling to large industrial RTL codebases
that, without external guidance, repeatedly self-correcting and                    will require multi-agent system [3]–[5] (e.g., planning, tool
   Prompt at first round                                                                    Report from spec verifier at first round
   You are a senior hardware design engineer specializing in RTL design analysis            Spec Verification fail.
   and documentation. Your task is to interpret a Verilog RTL module between
   [RTL START] and [RTL END] and produce a precise, human-readable func-                    # Reconstruction RTL:
   tional specification. . . . (omitted). . .
   [RTL START]                                                                              module TopModule (input wire clk, input wire reset,
                                                                                            output reg [9:0] q);
   module TopModule (input clk,                                                                 always @(posedge clk or posedge reset) begin
   input reset, output reg [9:0] q);                                                                if (reset) begin
       always @(posedge clk)                                                                            q <= 10’d0;
           if (reset || q == 999) q <= 0;                                                           end else if (q == 10’d999) begin
           else q <= q+1;                                                                               q <= 10’d0;
   endmodule                                                                                        end else begin
   [RTL END]                                                                                            q <= q + 1’b1;
                                                                                                    end
   LLM response at first round                                                                  end
                                                                                            endmodule
   Stage 1 — Internal Analysis (Reasoning) . . . (omitted). . . Control Logic: (i) Sim-
   ple counter with a terminal count of 999. (ii) Reset condition is synchronous            # Logs of verification tool:
   in behavior but uses an OR condition that includes an input reset. Since
   reset is not synchronized with the clock in the sensitivity list, it behaves as          Mismatched Signal:
   an asynchronous reset in practice due to the OR logic being evaluated inside the         t=11 sig=q
   clocked block. Clocking and Reset: (i) Clock: Positive edge triggered. (ii) Reset:       rtl_reconstruct: 0000000000
   Appears to be asynchronous due to if (reset — ...)— inside the always block.             rtl_original: 0000001010
   . . . (omitted). . .                                                                     ...(omitted)...
   [SPEC START]
   Summary:
   This module implements a 10-bit up-counter that counts                                   LLM response at second round
   from 0 to 999 and then wraps around. It supports an                                      . . . (omitted). . . Stage 2 — Root-Cause Analysis . . . (omitted). . . Summary of
   asynchronous reset that clears the counter immediately                                   Verification Report: (i) The verification tool found a mismatch in signal q at
   when asserted.                                                                           time t=11. (ii) At that moment: Original RTL: q = 10 (binary: 0000001010).
   Module Name: TopModule                                                                   Reconstructed RTL: q = 0 (binary: 0000000000). Root-Cause Analysis: The
   Inputs:                                                                                  issue lies in the reset behavior interpretation. . . . (omitted). . .
      • clk (1-bit): Clock signal, positive edge triggered.
      • reset (1-bit): Asynchronous reset signal; when                                      [SPEC START]
        high, resets the counter immediately.                                               ...(omitted)...
                                                                                            Clocking and Reset Behavior:
   Outputs:
                                                                                               • Clock: Positive edge of clk.
      • q (10-bit): Output of the counter, increments on
                                                                                               • Reset: Synchronous --- reset takes effect on the
        every clock cycle unless reset or limit reached.
                                                                                                 next rising edge of clk when reset is high.
   Detailed Functional Description:                                                            • Initial state after reset: q = 0.
   The module functions as a 10-bit synchronous up-counter.
                                                                                            ...(omitted)...
   On every rising edge of clk:
                                                                                            [SPEC END]
      • If reset is asserted (high) or the current value of
        q equals 999, the output q is reset to 0.
      • Otherwise, q is incremented by 1.
                                                                                            Report from spec verifier at second round
   This ensures the counter cycles from 0 to 999 and then                                   Spec Verification pass.
   wraps around to 0.
   Clocking and Reset Behavior:                                                             # Reconstruction RTL:
      • Clock: Positive edge of clk.
      • Reset: Asynchronous --- when reset is high, q is                                    module TopModule (input wire clk, input wire reset,
        immediately set to 0 regardless of the clock.                                       output reg [9:0] q);
      • Initial state after reset: q = 0.                                                       always @(posedge clk) begin
   Notes:                                                                                           if (reset || (q == 10’d999)) begin
                                                                                                        q <= 10’d0;
      • The counter uses a 10-bit register, allowing values
                                                                                                    end else begin
        from 0 to 1023, but is functionally constrained to                                              q <= q + 1’b1;
        0--999.                                                                                     end
      • Reset takes precedence over increment behavior.
                                                                                                end
   [SPEC_END]                                                                               endmodule



Fig. 4: Qualitative Analysis. Selected text segments are highlighted in red for clarity. This example shows how SpecLoop fixes
a spec error: the first-round spec wrongly states an asynchronous reset, reconstruction then fails equivalence checking, and the
diagnosis guides the next round to revise the spec to a synchronous reset, after which the verifier passes.


selection, and handling IP dependencies). Future work in-                                 RTL from candidate specifications and using formal equiv-
cludes strengthening reconstruction and verification pipelines                            alence checking to produce semantics-level feedback, our
and developing multi-agent system for handling more complex                               approach systematically refines specifications beyond one-shot
designs.                                                                                  prompting. Experiments show verifier guidance improves spec
                                                                                          quality, as evidenced by reconstruction success on frontier
                             VII. C ONCLUSION
                                                                                          models, and that richer diagnostics are beneficial. We believe
  We presented a agentic verification-guided framework for                                this direction can make RTL-to-spec generation a practical
RTL-to-specification generation that turns the problem into                               component in real hardware documentation workflows.
an iterative reconstruction-and-check loop. By reconstructing
                              R EFERENCES                                              Benchmarking verilog generation models with real-world ip designs,”
                                                                                       2025.
 [1] Y. Tsai, M. Liu, and H. Ren, “Rtlfixer: Automatically fixing rtl syntax      [20] M. Liu, N. Pinckney, B. Khailany, and H. Ren, “Verilogeval: Evaluating
     errors with large language model,” in Proceedings of the 61st ACM/IEEE            large language models for verilog code generation,” in 2023 IEEE/ACM
     Design Automation Conference, pp. 1–6, 2024.                                      International Conference on Computer Aided Design (ICCAD), pp. 1–8,
 [2] X. Yao, Y. Wang, X. Li, Y. Lian, R. Chen, L. Chen, M. Yuan, H. Xu,                IEEE, 2023.
     and B. Yu, “Rtlrewriter: Methodologies for large models aided rtl            [21] Y. Lu, S. Liu, Q. Zhang, and Z. Xie, “Rtllm: An open-source benchmark
     code optimization,” in 2024 IEEE/ACM International Conference on                  for design rtl generation with large language model,” in 2024 29th Asia
     Computer Aided Design (ICCAD), 2024.                                              and South Pacific Design Automation Conference (ASP-DAC), pp. 722–
 [3] C.-T. Ho, H. Ren, and B. Khailany, “Verilogcoder: Autonomous verilog              727, IEEE, 2024.
     coding agents with graph-based planning and abstract syntax tree (ast)-      [22] OpenAI, “Gpt-5 codex.” OpenAI model documentation. Accessed: 2026-
     based waveform tracing tool,” in Proceedings of the AAAI Conference               02-24.
     on Artificial Intelligence, vol. 39, pp. 300–307, 2025.                      [23] “Equivalence checking with yosys (eqy) documentation.” https://
                                                                                       yosyshq.readthedocs.io/projects/eqy/en/latest/. Accessed: 2026-02-21.
 [4] Z. Yu, M. Liu, M. Zimmer, Y. Celine, Y. Liu, and H. Ren, “Spec2rtl-
                                                                                  [24] “Openrouter.” https://openrouter.ai/. Accessed: 2026-02-21.
     agent: Automated hardware code generation from complex specifications
     using llm agent systems,” in 2025 IEEE International Conference on
     LLM-Aided Design (ICLAD), pp. 37–43, IEEE, 2025.
 [5] Y. Zhao, H. Zhang, H. Huang, Z. Yu, and J. Zhao, “Mage: A multi-agent
     engine for automated rtl code generation,” in Proceedings of the 62nd
     Annual ACM/IEEE Design Automation Conference, DAC ’25, IEEE
     Press, 2025.
 [6] N. Pinckney, C. Deng, C.-T. Ho, Y.-D. Tsai, M. Liu, W. Zhou,
     B. Khailany, and H. Ren, “Comprehensive verilog design problems:
     A next-generation benchmark dataset for evaluating large language
     models and agents on rtl design and verification,” arXiv preprint
     arXiv:2506.14074, 2025.
 [7] Y. Liu, C. XU, Y. Zhou, Z. Li, and Q. Xu, “DeepRTL: Bridging verilog
     understanding and generation with a unified representation model,” in
     The Thirteenth International Conference on Learning Representations,
     2025.
 [8] Y. Liu, H. Zhang, Y. Zhou, Z. Shi, C. Xu, and Q. Xu, “Deeprtl2: A
     versatile model for rtl-related tasks,” in Findings of the Association for
     Computational Linguistics: ACL 2025, pp. 6485–6500, 2025.
 [9] S. He, C. Chen, X. Zheng, Z. Liu, and C. Wang, “Refining specs for
     LLM-based RTL agile design,” 2026.
[10] M. Li, W. Fang, Q. Zhang, and Z. Xie, “Specllm: Exploring generation
     and review of vlsi design specification with large language model,”
     in 2025 International Symposium of Electronics Design Automation
     (ISEDA), pp. 749–755, IEEE, 2025.
[11] H.-M. Huang, Y.-H. Yang, F.-C. Chang, Y.-C. Hsu, Y.-Y. Lin, M.-F.
     Tsai, C.-C. Yang, and P.-Y. Wu, “Assessing large language models in
     generating rtl design specifications,” arXiv preprint arXiv:2512.00045,
     2025.
[12] Q. Wu, W. Liu, J. Luan, and B. Wang, “ToolPlanner: A tool augmented
     LLM for multi granularity instructions with path planning and feedback,”
     in Proceedings of the 2024 Conference on Empirical Methods in Natural
     Language Processing, pp. 18315–18339, Association for Computational
     Linguistics, Nov. 2024.
[13] K. Zhang, J. Li, G. Li, X. Shi, and Z. Jin, “Codeagent: Enhancing code
     generation with tool-integrated agent systems for real-world repo-level
     coding challenges,” in Proceedings of the 62nd Annual Meeting of the
     Association for Computational Linguistics (Volume 1: Long Papers),
     pp. 13643–13658, 2024.
[14] Q. Wu, G. Bansal, J. Zhang, Y. Wu, B. Li, E. Zhu, L. Jiang, X. Zhang,
     S. Zhang, J. Liu, et al., “Autogen: Enabling next-gen llm applications via
     multi-agent conversations,” in First conference on language modeling,
     2024.
[15] D. J. Shah, P. Rushton, S. Singla, M. Parmar, K. Smith, Y. Vanjani,
     A. Vaswani, A. Chaluvaraju, A. Hojel, A. Ma, et al., “Rethinking
     reflection in pre-training,” arXiv preprint arXiv:2504.04022, 2025.
[16] Y.-T. Lee, F.-C. Chang, H.-Y. Shih, and P.-Y. Wu, “Intrinsic self-
     correction in LLMs: Towards explainable prompting via mechanistic
     interpretability,” in 4th Deployable AI Workshop, 2026.
[17] F.-C. Chang, Y.-T. Lee, and P.-Y. Wu, “Unveiling the latent directions
     of reflection in large language models,” in Mechanistic Interpretability
     Workshop at NeurIPS 2025, 2025.
[18] P. Yubeaton, A. Nakkab, W. Xiao, L. Collini, R. Karri, C. Hegde, and
     S. Garg, “Verithoughts: Enabling automated verilog code generation
     using reasoning and formal verification,” in The Thirty-ninth Annual
     Conference on Neural Information Processing Systems Datasets and
     Benchmarks Track, 2025.
[19] P. Jin, D. Huang, C. Li, S. Cheng, Y. Zhao, X. Zheng, J. Zhu,
     S. Xing, B. Dou, R. Zhang, Z. Du, Q. Guo, and X. Hu, “Realbench:
