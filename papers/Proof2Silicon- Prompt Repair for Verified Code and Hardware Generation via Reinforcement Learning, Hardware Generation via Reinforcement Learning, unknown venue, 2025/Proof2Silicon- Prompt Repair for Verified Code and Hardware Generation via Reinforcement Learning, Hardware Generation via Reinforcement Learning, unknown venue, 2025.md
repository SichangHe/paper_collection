                                         Proof2Silicon: Prompt Repair for Verified Code and
                                          Hardware Generation via Reinforcement Learning
                                                         Manvi Jha                                  Jiaxin Wan                               Deming Chen
                                          Electrical and Computer Engineering     Electrical and Computer Engineering     Electrical and Computer Engineering
                                         University of Illinois Urbana-Champaign University of Illinois Urbana-Champaign University of Illinois Urbana-Champaign
                                                  Urbana, Illinois, USA                   Urbana, Illinois, USA                   Urbana, Illinois, USA
                                                   manvij2@illinois.edu                     wan25@illinois.edu                      dchen@illinois.edu



                                            Abstract—Large Language Models (LLMs) have demonstrated         output to fail verification, or worse, introduce undetected
arXiv:2509.06239v2 [cs.AI] 20 Oct 2025




                                         impressive capabilities in automated code generation but fre-      unsoundness.
                                         quently produce code that fails formal verification, an essen-        Traditional solutions to enhance LLM performance in such
                                         tial requirement for hardware and safety-critical domains. To
                                         overcome this fundamental limitation, we previously proposed       specialized contexts involve fine-tuning [5], which adapts
                                         PREFACE, a model-agnostic framework based on reinforcement         models to domain-specific tasks. However, fine-tuning large
                                         learning (RL) that iteratively repairs the prompts provided to     models requires substantial computational resources, extensive
                                         frozen LLMs, systematically steering them toward generating        annotated data, and risks overwriting beneficial pre-trained
                                         formally verifiable Dafny code without costly fine-tuning. This    capabilities, leading to brittleness and inefficiency.
                                         work presents Proof2Silicon, a novel end-to-end synthesis frame-
                                         work that embeds the previously proposed PREFACE flow to              In contrast, we argue that the latent reasoning abilities
                                         enable the generation of correctness-by-construction hardware      inherent within LLMs are sufficient to address many domain-
                                         directly from natural language specifications. Proof2Silicon op-   specific tasks if effectively guided through prompts. The qual-
                                         erates by: (1) leveraging PREFACE’s verifier-driven RL agent to    ity of the prompts significantly impacts the effectiveness of
                                         optimize prompt generation iteratively, ensuring Dafny code cor-   LLM in formal verification tasks. Constructing these prompts
                                         rectness; (2) automatically translating verified Dafny programs
                                         into synthesizable high-level C using Dafny’s Python backend       manually is arduous, particularly when feedback from verifi-
                                         and PyLog; and (3) employing Vivado HLS to produce RTL             cation engines needs to be integrated into subsequent attempts.
                                         implementations. Evaluated rigorously on a challenging 100-        However, this structured feedback from formal verifiers offers
                                         task benchmark, PREFACE’s RL-guided prompt optimization            precisely the actionable insights needed to refine model be-
                                         consistently improved Dafny verification success rates across      havior more systematically.
                                         diverse LLMs by up to 21%. Crucially, Proof2Silicon achieved
                                         an end-to-end hardware synthesis success rate of up to 72%,           Motivated by this insight, we introduced PREFACE [6],
                                         generating RTL designs through Vivado HLS synthesis flows.         our lightweight and scalable RL framework in which a Small
                                         These results demonstrate a robust, scalable, and automated        Language Model (SLM) is trained to generate optimized
                                         pipeline for LLM-driven, formally verified hardware synthesis,     prompts for a fixed, general-purpose LLM, allowing accurate,
                                         bridging natural-language specification and silicon realization.   formally verified code synthesis without costly fine-tuning
                                            Index Terms—Large Language Models (LLMs), Microproces-
                                         sor, Verilog                                                       of the base model. Building on PREFACE, we then present
                                                                                                            Proof2Silicon, which embeds this same RL-driven prompt
                                                               I. I NTRODUCTION                             adaptation mechanism into a full-stack high-level synthesis
                                                                                                            pipeline: it takes the verified code output from the LLM and
                                            Large Language Models (LLMs) have significantly ad-
                                                                                                            automatically transforms it into synthesizable HLS C (via
                                         vanced automated code generation from natural language
                                                                                                            Dafny’s Python backend and PyLog [7]) and ultimately into
                                         prompts [1]. Although large language models can sometimes
                                                                                                            RTL through Vivado HLS. The details of PREFACE and its
                                         produce syntactically valid code, they still fall short of guar-
                                                                                                            integration into the Proof2Silicon workflow are described in
                                         anteeing complete correctness. This shortcoming affects every
                                                                                                            Sections III and IV.
                                         application, but it is particularly unacceptable in contexts
                                                                                                               Focusing on Dafny, a verification-aware programming lan-
                                         where undetected errors can have catastrophic consequences
                                                                                                            guage that facilitates formal specifications through built-in
                                         (for example, cryptographic libraries, aerospace control soft-
                                                                                                            constructs such as preconditions, postconditions, invariants,
                                         ware, automotive safety systems, and hardware design [2] [3]).
                                                                                                            and lemmas, we bridge verified software generation with hard-
                                         In such domains, formal methods and provable correctness are
                                                                                                            ware design workflows. Dafny automatically translates formal
                                         essential to ensure reliability and security. When LLMs are
                                                                                                            specifications into verification conditions checked by SMT
                                         tasked with generating code in formally verified languages
                                                                                                            solvers, thereby enabling correctness-by-construction software
                                         such as Dafny [4], even small mismatches in the specified
                                                                                                            development. Given the scarcity of domain-specific datasets
                                         contracts or the omission of critical invariants can cause the
                                                                                                            (for example, DafnyBench [8] has only ~700 tasks), conven-
                                           This work was presented at SRC TECHCON 2025.                     tional fine-tuning is impractical. Proof2Silicon addresses this
challenge by taking advantage of the existing capabilities of      compiles these specifications into first-order verification condi-
a frozen LLM and steering it through an RL-driven prompt           tions, subsequently discharged automatically by Satisfiability
refinement loop (via the embedded PREFACE flow), allowing          Modulo Theories (SMT) solvers such as Z3 [10]. This en-
efficient verified code generation. Verified Dafny programs        sures correctness-by-construction, making Dafny particularly
are systematically translated into HLS code, bridging formal       suitable for high-assurance, LLM-driven hardware synthesis
methods directly into hardware synthesis workflows, building       tasks.
on decades of HLS advancements [9].
                                                                   B. Dafny Generation & Verification with LLMs
A. Contributions
                                                                      Recent studies have explored LLM capabilities in generating
    This work presents a novel reinforcement learning-based        formally verified Dafny programs [2], [11], [12]. Misu et
framework for guiding LLMs toward generating formally ver-         al. [13] leveraged structured chain-of-thought prompting with
ified code without requiring fine-tuning. Our key contributions    GPT-4, enhancing Dafny program verification rates by me-
are as follows.                                                    thodically guiding the model through logical deduction paths,
 • End-to-end verified hardware code generation: We pro-           significantly outperforming naive prompting methods that lack
   pose a full-stack pipeline—from natural language speci-         structured reasoning.
   fications to verified Dafny code, systematically translated        Poesia et al. [14] proposed Dafny-Annotator, an iterative
   into HLS C code, ensuring correctness-by-construction for       annotation refinement framework combining LLM predictions
   hardware implementation without the need for costly fine-       with greedy search methods to determine logical annotations.
   tuning or a dedicated dataset.                                  To tackle data scarcity, they further introduced DafnySynth, an
 • Verifier-guided prompt refinement via RL: A small, RL-          automated dataset generation pipeline that produces synthetic
   trained agent iteratively optimizes prompts based on formal     Dafny tasks to augment training data, enabling fine-tuned
   verification feedback, significantly enhancing verification     models to achieve substantial improvements on benchmarks
   success without modifying the underlying LLM. This uti-         like DafnyBench [8].
   lizes the PREFACE model previously proposed by us.                 Li et al. [15] presented an end-to-end pipeline treating
 • A formal verification feedback loop: We design a genera-        Dafny as a verification-aware intermediate language. Their
   tion verification loop that uses structured feedback from an    framework generates Dafny programs directly from natural
   integrated Dafny verifier. The RL agent interprets the error    language prompts, facilitating iterative refinement through
   metadata and learns to iteratively refine the commands to       formal verification feedback loops. Verified Dafny code is then
   improve the success of the verification.                        automatically compiled into Python, significantly simplifying
 • Formal verification integrated into hardware synthesis:         specification-coding interactions and improving user accessi-
   Verified Dafny code is converted through a Dafny → Python       bility.
   → Customized Python → HLS C pipeline, validated with               Proof2Silicon builds on these developments by embedding
   Vivado HLS, thus closing the gap between software correct-      PREFACE, which introduces reinforcement learning (RL)-
   ness and hardware design.                                       driven prompt optimization. Differing from direct fine-tuning
 • Significant empirical improvements and synthesis suc-           approaches, it trains an RL-based small language model
   cess: Our framework achieves up to a 21% increase in verifi-    (SLM) to iteratively refine prompts, effectively steering frozen,
   cation success rates across diverse LLMs on a benchmark of      general-purpose LLMs toward generating formally verified
   100 tasks, with upto 72% of verified programs successfully      Dafny code. Embedding this novel integration of reinforce-
   synthesized into RTL through Vivado HLS.                        ment learning and formal verification frameworks with our
    Collectively, these contributions establish Proof2Silicon as   Dafny to RTL workflow, distinctly positions Proof2Silicon as a
a scalable and efficient alternative to traditional fine-tuning    robust, scalable solution to generating formally verified Dafny
approaches, enabling robust, formally verified hardware gen-       code for hardware design.
eration directly from natural language specifications.
                                                                   C. LLMs for RL and Prompt Optimization
          II. BACKGROUND AND R ELATED W ORK
                                                                      Recent research incorporates LLMs into reinforcement
A. Dafny: Syntax and Verification Workflow                         learning workflows, manifesting primarily as either high-level
   Dafny [4] is a verification-aware imperative programming        policy guidance or direct RL-driven prompt optimization.
language integrating formal specifications directly into its          Du et al. [16] leveraged LLMs as high-level reasoning
syntax. Methods define explicit contracts through precon-          modules within RL systems, guiding RL agents through sub-
ditions (requires) and postconditions (ensures), establishing      goal generation and exploration strategies to accelerate and
strict adherence to specifications. Loop constructs enforce        enhance learning outcomes. In multi-agent scenarios, frame-
properties using invariants, which must hold true throughout       works like YOLO-MARL [17] and LERO [18] utilize LLMs to
loop iterations, providing rigorous runtime correctness guar-      produce strategic policy sketches or dynamic reward functions,
antees. Dafny utilizes ghost variables and lemma functions to      significantly improving collaborative task performance.
support purely logical reasoning constructs, enabling verifi-         In contrast, Proof2Silicon focuses specifically on RL-driven
cation without incurring runtime overhead. Internally, Dafny       prompt optimization. It formulates prompt generation as
Fig. 1: Overview of the PREFACE [6] framework-forming the prompt-optimization core embedded within the Proof2Silicon
pipeline.


an iterative RL problem, employing verifier feedback as a        Algorithm 1 PREFACE Prompt Adaptation Loop
direct reward signal. By continuously optimizing prompts,        Require: Specification τ Initial prompt p0 ← φ(τ ) Max
Proof2Silicon efficiently leverages the latent reasoning capa-       iterations Tmax = 7
bilities of frozen LLMs, thereby achieving high verification      1: for t = 0 . . . Tmax − 1 do
rates without expensive retraining or fine-tuning.                2:     ct ← M(pt )
D. LLM-assisted Hardware Code Generation                          3:     et ← Verify(ct , τ )
                                                                  4:     if et = 0 then
   Integrating LLMs into hardware design automation, es-          5:         return ct
pecially for Register Transfer Level (RTL) and High-Level         6:     end if
Synthesis (HLS), has attracted significant research attention.    7:     st ← ψ(pt , ct , et )
Early works primarily targeted direct RTL generation from         8:     Sample prompt edit: ∆pt ∼ πθ ( · | st )
natural language prompts or structured specifications [19],       9:     pt+1 ← pt ⊕ ∆pt
[20]. However, direct RTL generation methods frequently en-      10: end for
countered semantic ambiguities, limiting practical scalability
and correctness [21].
   Advanced frameworks, such as Spec2RTL-Agent [20] and          coupled with formal verification and HLS tools. This com-
HLSPilot [21], proposed sophisticated multi-stage generation     prehensive integration facilitates the direct translation from
pipelines. These approaches first translate natural language     natural language to verified Dafny code, and ultimately to
descriptions into structured, synthesizable intermediate lan-    synthesizable hardware descriptions, positioning Proof2Silicon
guages (e.g., synthesizable C++), then utilize conventional      as a state-of-the-art methodology for reliable, formally verified
HLS tools to ensure accurate hardware realization. RTLCoder      hardware synthesis.
[19] further enhanced these pipelines by introducing auto-
mated dataset generation techniques specifically designed for                     III. PREFACE OVERVIEW
RTL synthesis tasks, significantly surpassing general-purpose
                                                                 A. Pipeline Architecture
models such as GPT-3.5.
   VerilogReader [22] pioneered an advanced, coverage-              PREFACE [6] is an RL-guided pipeline developed to syn-
directed hardware test generation strategy, utilizing LLMs       thesize formally verified Dafny code, a language designed for
to parse RTL descriptions precisely and enhance testbench        rigorous specification and automated verification. It centers
coverage dramatically compared to traditional random testing.    on an RL-driven Small Language Model (SLM) that refines
FormalEval [2] introduced automated formal verification us-      the prompts to a frozen LLM M for the synthesis of Dafny
ing sequential equivalence checking, offering accurate, fully    code. Given task specifications τ (pre / postconditions), a
automated verification for RTL code generated by LLMs,           handcrafted prompt p0 = φ(τ ) is submitted to M, producing
significantly enhancing verification robustness.                 a candidate code ct . The Dafny verifier then computes the
   CreativEval [23] provided a novel approach to assess the      error count et and feedback ot . On success (et = 0), the loop
creativity of LLM-generated hardware designs. It established     terminates; otherwise, the SLM ingests (pt , ct , ot ) to sample a
comprehensive cognitive evaluation metrics—including flu-        prompt edit ∆pt , yielding pt+1 = pt ⊕∆pt . This cycle repeats
ency, flexibility, originality, and elaboration—beyond tradi-    for up to Tmax iterations.
tional correctness measures, highlighting LLM potential for
innovative and robust hardware design.                           B. MDP Formulation
   Proof2Silicon uniquely integrates these advancements, em-       We formalize prompt refinement as an MDP G                   =
ploying an RL-driven prompt optimization pipeline tightly        (S, A, P, R, γ):
                                   Fig. 2: Overview of the proposed Proof2Silicon framework.


  • State st = ψ(pt , ct , ot ) encodes the current prompt,          A. Dafny to Python Translation
    generated code, and verifier feedback. (st ∈ S)
                                                                        Upon successful obtaining formally verified Dafny code
  • Action at is a discrete, token-level modification ∆pt
                                                                     through the PREFACE pipeline, the verified Dafny code under-
    drawn from the SLM’s vocabulary. (at ∈ A)
                                                                     goes a transformation into Python code using Dafny’s native
  • Transition Dynamics The distribution P (st+1 | st , at )
                                                                     compiler with the command: dafny build -target py
    is implicitly defined by the combined generative and ver-
                                                                     verified.dfy
    ification steps. Each state transition results from prompt
                                                                        This transformation is necessary as direct translation from
    modifications and their verification outcomes, implicitly
                                                                     Dafny to C incurs critical issues, particularly concerning
    defining the probabilistic transition model.
                                                                     integer overflow and limited support for various mathematical
  • Reward
                           (                                         constructs required for accurate hardware synthesis.
                            +Rsucc ,         et+1 = 0,
             R(st , at ) =
                            −α et+1 − β, et+1 > 0,                   B. Removing Dafny-Specific Dependencies
    with α = 0.2, β = 0.5, and a large penalty for empty                The generated Python code contains significant dependen-
    outputs.                                                         cies on Dafny’s internal libraries, specifically designed for
  • γ = 0.99 emphasizes long-term verification success.              mathematical operations and array manipulations that adhere
                                                                     strictly to Dafny semantics. These dependencies introduce
C. Policy Optimization via PPO                                       complexity that complicates HLS translation due to the incom-
   PREFACE employs Proximal Policy Optimization (PPO)                patible semantics and the inclusion of empty class wrappers
to train the SLM agent. The actor maximizes the clipped              generated by Dafny’s Python backend.
surrogate objective                                                     To address this challenge, we implemented an automated
                                                                     script that systematically removes Dafny-specific library im-
                                                               
Lactor (θ) = −Et min rt (θ) Ât , clip(rt (θ), 1 − ϵ, 1 + ϵ) Ât ,
                                                                   ports and eliminates redundant class structures and wrap-
while the critic minimizes Lcritic (ϕ) = Et (Vϕ (st ) − Gt )2 .      pers. The script replaces Dafny-based mathematical operations
We use Adam with gradient-norm clipping for stable con-              with equivalent Python-native implementations, leveraging the
vergence. By restricting training to the lightweight SLM,            NumPy library for numerical operations. This meticulous
PREFACE achieves formally verified code synthesis without            removal ensures syntactic simplicity and semantic clarity
fine-tuning the base LLM, forming the core of Proof2Silicon.         required for downstream synthesis.
        IV. T HE C OMPLETE P ROOF 2S ILICON F LOW
                                                                     C. Customization with PyLog Decorators
   The Proof2Silicon method embeds the previously developed
PREFACE [6] framework to facilitate hardware realization                The sanitized Python code undergoes further refinement
through the conversion of formally verified Dafny code to            through integration with PyLog - an algorithm-centric Python-
High-Level Synthesis (HLS) C code and further to RTL. Over-          based FPGA programming and synthesis tool [7]. PyLog
all, Proof2Silicon encompasses a sophisticated, automated            facilitates the translation of Python to high-quality synthe-
pipeline from Dafny code verification to FPGA hardware               sizable HLS C through an intermediate representation (IR),
designs. Below, we detail each step of this advanced pipeline,       extensive compiler optimizations, and automated design space
emphasizing the intricate technicalities involved to ensure the      exploration [24]. Specifically, PyLog employs a pragma-based
generation of robust, verifiable, and synthesizable hardware         optimization mechanism that enables loop transformations,
code. The overview of the Proof2Silicon flow is shown in             memory optimizations, and resource management to ensure
Figure 2                                                             efficient FPGA hardware synthesis.
Fig. 3: Proof2Silicon end-to-end workflow: an RL-driven Small Language Model (SLM) iteratively refines meta-prompts to a
frozen LLM under guidance from the integrated Dafny verifier, producing formally verified Dafny code. Verified code is then
compiled to Python, transformed into hardware-aware C via the PyLog backend, and synthesized to RTL with Vivado HLS
on a Zynq-7000 SoC.


   We augment the Python scripts with PyLog decorators              we manually crafted test cases for each DafnyBench [8]
that explicitly annotate functions intended for hardware ac-        benchmark used in our evaluations. These cases thoroughly
celeration, allowing precise control over synthesis directives,     exercise the synthesized designs, validating both functional
including loop pipelining, unrolling, and array partitioning.       correctness and FPGA resource optimization.
These decorators guide the PyLog compiler toward generating
                                                                    D. Python to Synthesizable C via PyLog
optimized HLS code aligned closely with FPGA hardware
execution models.                                                      After preparation with PyLog decorators and numerical op-
                                                                    timizations, the refined Python code is translated into synthe-
     a) Ensuring Numerical and Data Type Compatibility:
                                                                    sizable C (HLS C) using PyLog’s compilation engine. PyLog
Incorporating NumPy library calls, all numerical data types
                                                                    optimizes the generated HLS C through aggressive pragma
and operations in the Python code are explicitly converted to
                                                                    insertion, loop restructuring, and memory customization strate-
NumPy types (e.g., np.int32, np.float32). This rigorous type
                                                                    gies, complementing scalability-oriented frameworks such as
annotation is vital for numerical stability, predictable hardware
                                                                    ScaleHLS [25]. This comprehensive optimization ensures that
performance, and compatibility with the fixed-point arithmetic
                                                                    the resulting HLS C efficiently maps onto FPGA hardware
typically utilized in FPGA designs and for ease of conversion
                                                                    resources, enhancing throughput and minimizing latency.
via the PyLog tool.
     b) Manual Test Case Development: Effective synthesis           E. FPGA Hardware Synthesis and Verification
via PyLog necessitates the explicit presence of test cases             The final stage uses Xilinx Vivado HLS to synthesize
to validate synthesized designs and to ensure correctness in        the generated C kernel into RTL, producing detailed reports
hardware execution. Given the limited availability of auto-         on timing (clock-period estimates, initiation interval) and
mated test generation tools suitable for this specific context,     resource utilization. Although we do not perform functional
co-simulation, this step verifies that the design is structurally
FPGA-compatible and meets target performance and area
constraints.
   In this way, Proof2Silicon seamlessly bridges
formally-verified Dafny specifications with practical hardware
synthesis—automatically generating synthesizable RTL from
natural language descriptions while providing confidence in
timing and resource metrics.
   Figure 3 illustrates the end-to-end Proof2Silicon workflow.
First, the embedded PREFACE framework uses a trained
Small Language Model (SLM) to generate meta-prompts that
guide a frozen LLM in producing candidate Dafny programs.                   (a) Value Loss × 1000 and Policy Loss vs. episode
Each program is immediately checked by an integrated Dafny
verifier, and only those that pass formal verification proceed.
Verified Dafny code is then compiled to Python using Dafny’s
compiler, yielding code that still contains Dafny-specific con-
structs. This Python code is then reformatted via our automa-
tion script to be converted to a PyLog-friendly script. It is then
fed into our PyLog transformation pipeline, which rewrites
it into HLS C kernels. Finally, these kernels are synthesized
with Vivado HLS (10 ns target clock) on the xc7z020clg484-1
device, producing RTL IP cores along with detailed timing and
resource utilization reports. By coupling RL-driven prompt
optimization with formal verification and automated high-level                        (b) Episode reward vs. episode
synthesis, Proof2Silicon delivers correctness-by-construction        Fig. 4: Training curves for the PREFACE pipeline over more
hardware directly from high-level algorithmic descriptions.          than 2000 episodes: (a) Value Loss × 1000 and Policy Loss,
                                                                     we scale up the Value loss for a better visualization; (b)
               V. R ESULTS AND E VALUATION                           Episode Reward, illustrates the pipeline’s verification perfor-
                                                                     mance improving over time.
   In this section, we provide an end-to-end evaluation of the
Proof2Silicon workflow, beginning with PREFACE’s formally
verified Dafny code synthesis results and concluding with the        B. HLS Synthesis and Performance Results
synthesis readiness and performance metrics of the generated
HLS C codes. We evaluated the performance of several                    Extending beyond formal verification, we evaluated the
state-of-the-art language models in a representative subset of       Proof2Silicon pipeline’s ability to translate verified Dafny
100 tasks sampled from DafnyBench [8]. The models tested             code into synthesizable HLS C and validate synthesis on
include ChatGPT-4o [26], ChatGPT-o1 [27], Qwen2.5-Coder-             FPGA platforms. We analyzed hardware compilation success,
14B [28], Qwen2.5-7B [29] and Gemini-2-Flash.                        resource utilization, and performance metrics for each LLM
                                                                     and feedback setting. For our experiments, we simulate the
                                                                     synthesis of the HLS code on Zynq-7000 All Programmable
A. Embedded PREFACE results
                                                                     SoC family (device: xc7z020clg484-1). The xc7z020 is a mid-
   PREFACE was trained for approximately 100 h on two                range Zynq FPGA widely used in embedded applications
NVIDIA H100 GPUs, during which shaped rewards, policy                requiring tight integration between programmable logic and
loss, and value loss were recorded over 2000+ episodes (Fig-         embedded processors. It is well-suited for prototyping DSP,
ure 4). Both policy and value losses steadily declined, while        image processing, or control algorithms. For our experiment,
episode rewards rose despite early-stage penalties, indicating       the TCL scripts define a 10 ns clock period.
effective convergence and improved prompt optimization.                 The results are presented in Table II, demonstrating the
   On a 100-task DafnyBench subset (Table I), static prompt-         effectiveness of the Proof2Silicon framework in translating
ing baselines were outperformed by SLM-tuned prompting               verified Dafny programs into synthesizable hardware. The first
even without feedback, achieving 23% for both ChatGPT-4o             stage reports the number of Dafny codes that successfully pass
and ChatGPT-o1, 16% for Qwen2.5-Coder-14B, 3% for                    formal verification, establishing functional correctness. These
Qwen2.5-7B, and 29% for Gemini-2-Flash. Enabling the full            verified programs are then translated to Python and passed
verifier feedback loop further boosted these rates to 50%, 52%,      through PyLog to produce HLS-compatible C, a stage we
31%, 11%, and 55%, respectively, demonstrating PREFACE’s             denote as Compiled to HLS.
consistent, model-agnostic enhancements in formal verifica-             At this stage, many programs are excluded because PyLog
tion success.                                                        does not support certain Dafny-derived constructs, most no-
TABLE I: Verification success rates on a 100-task benchmark for various LLMs using prompts through PREFACE pipeline
from both untrained and 100-hr-trained small language model, comparing single-shot (W/O Feedback) versus iterative error-
feedback (With Feedback) modes. We employ the "One-line and Detailed Description" prompting mechanism; values are
color-coded green for improvements and red for degradations relative to their respective baseline values.
       Model                    Without SLM (baseline)                Without Trained SLM                With Trained SLM
                             W/O Feedback  With Feedback          W/O Feedback    With Feedback     W/O Feedback   With Feedback
       ChatGPT-4o                 25%                36%           10% (-15%)      44% (+8%)            23% (-2%)     50% (+14%)
       ChatGPT-o1-mini            23%                35%            8% (-14%)      42% (+7%)            23% (±0%)     52% (+17%)
       Qwen2.5-Coder-14B          15%                21%            2% (-13%)      12% (-9%)            16% (+1%)     31% (+10%)
       Qwen2.5-7B                 3%                 7%             0% (-3%)        4% (-3%)            3% (±0%)       11% (+4%)
       Gemini-2-Flash             20%                33%            3% (-17%)      32% (-1%)            29% (+9%)     55% (+21%)


TABLE II: Proof2Silicon Hardware Synthesis Results: Compilation and synthesis statistics for verified Dafny programs across
LLMs and verifier feedback settings.
    Model                  Feedback     Verified Count   Compiled to HLS    HLS Synthesized    Avg. Elpased Time    Avg. Peak Memory
    ChatGPT-4o                No               23              17             12 (52.1%)            32.98 sec           705.41 MB
    ChatGPT-4o                Yes              50              29              25 (50%)             32.96 sec           678.51 MB
    ChatGPT-o1-mini           No               23              17             12 (52.1%)            32.83 sec           677.47 MB
    ChatGPT-o1-mini           Yes              52              35             29 (55.8%)            32.84 sec           682.46 MB
    Qwen2.5-Coder-14B         No               16              12             10 (62.5%)            33.98 sec           678.56 MB
    Qwen2.5-Coder-14B         Yes              31              23             17 (54.8%)            33.47 sec           681.97 MB
    Qwen2.5-7B                No               3                3             2 (66.67%)            33.51 sec           685.46 MB
    Qwen2.5-7B                Yes              11               7              6 (54.54)            32.76 sec          677.746 MB
    Gemini-2-Flash            No               29              24             21 (72.4%)            33.88 sec           679.98 MB
    Gemini-2-Flash            Yes              55              44             38 (69.1%)            34.21 sec           683.36 MB

            TABLE III: Performance and resource results for selected benchmarks on the Xilinx Zynq-7000 SoC.
                                                                           Benchmark Tasks
 Model (Feedback)                            Cube                           TriangleNumber                     TriangularPrismVolume
                              Latency      LUTs   DSPs      FFs     Latency    LUTs    DSPs       FFs     Latency    LUTs     DSPs   FFs
 ChatGPT-4o (No)               60 ns        685    6        789      50 ns      511     3         436       60 ns     456      6     807
 ChatGPT-4o (Yes)              60 ns        685    6        789      50 ns      511     3         436       60 ns     546      6     807
 ChatGPT-o1-mini (No)          70 ns        305    6        538      50 ns      576     3         436       60 ns     546      6     807
 ChatGPT-o1-mini (Yes)         60 ns        685    6        789      40 ns      462     3         437      250 ns     2127     11    908
 Gemini-2-Flash (No)           70 ns        798    6        880      50 ns      576     3         436       60 ns     546      6     807
 Gemini-2-Flash (Yes)          80 ns        381    6        572      40 ns      462     3         437      290 ns     1051     11    838
 Qwen2.5-Coder-14B (No)        70 ns        798    6        880      50 ns      576     3         436       60 ns     546      6     807
 Qwen2.5-Coder-14B (Yes)       60 ns        685    6        789      50 ns      576     3         436      290 ns     1051     11    838
 Qwen2.5-7B (No)               80 ns        381    6        572      50 ns      576     3         436       60 ns     546      6     807
 Qwen2.5-7B (Yes)              60 ns        685    6        789      40 ns      462     3         437      290 ns     1051     11    838


tably recursion, dynamic memory usage, or while-loops, all of           complete RTL synthesis, and the average per-kernel runtime
which violate the requirement of acyclic and static control flow        and memory footprint. All experiments were conducted using
for hardware synthesis. Additional incompatibilities arise from         unmodified TCL scripts with a fixed 10 ns target clock,
Dafny-specific data structures and strict typing conventions,           and detailed resource and timing reports were collected from
which, even after automated sanitization, may still produce             the Vivado HLS reporting interface. Together, these results
kernels that cannot be transformed into valid HLS C. Among              highlight both the promise of Proof2Silicon in establishing a
the codes that do compile, not all complete RTL synthesis in            correctness-by-construction synthesis flow and the current lim-
Vivado HLS, which imposes further restrictions such as pro-             itations that must be addressed to improve alignment between
hibiting recursive function calls, requiring consistent function        verification and hardware realization.
signatures, and rejecting kernels with subtle type mismatches
(e.g., functions declared as void despite computing integer                As shown in Table II, Proof2Silicon achieves robust syn-
outputs).                                                               thesis readiness across diverse LLMs and feedback modes.
                                                                        Without verifier feedback, the pipeline synthesizes 52.1%
   These issues account for the observed discrepancy between            of ChatGPT-o1-mini’s verified codes and up to 72.4% for
Compiled to HLS and HLS Synthesized, with approximately                 Gemini-2-Flash, with mean synthesis times of 32.8–33.9 s
30% of otherwise verified programs excluded during this                 and peak memory under 705 MB. Enabling the full verifier
stage. For the designs that do pass through to full synthesis,          feedback loop further improves synthesis rates—ChatGPT-o1-
we report three metrics: the total number of programs that              mini rises to 55.8%, while synthesis latencies remain stable
successfully parse and elaborate in Vivado HLS, the subset that         (32.8–34.2 s) and memory usage exhibits minimal variance
(678–683 MB). These results demonstrate that embedding              with practical hardware efficiency, ultimately enabling the
PREFACE’s prompt-optimization core within a hardware syn-           generation of high-quality FPGA implementations.
thesis pipeline yields high end-to-end success: the majority of
formally verified algorithms not only translate cleanly to HLS                               VI. C ONCLUSION
C but also compile and synthesize into FPGA-ready RTL with             We present Proof2Silicon, a comprehensive pipeline that ex-
predictable performance and resource consumption. Such con-         tends PREFACE’s reinforcement learning–based prompt repair
sistency underlines Proof2Silicon’s potential for automated,        framework toward hardware synthesis. By coupling formally
correctness-driven hardware generation in safety-critical and       verified Dafny code generation with automated translation
high-throughput applications.                                       to synthesizable HLS C via PyLog, and validating synthesis
   It is important to note that the current results represent       with Vivado HLS, Proof2Silicon bridges formal methods and
initial demonstrations of the Proof2Silicon flow rather than        hardware design automation.
a fully optimized end-to-end solution. While the framework             Our experiments show that PREFACE’s prompt refinement
shows promising potential by achieving a high hardware              significantly increases verified Dafny code generation, while a
synthesis success, several synthesis failures highlight the need    meaningful subset of this verified code successfully compiles
for further refinement of the pipeline. In future work, we plan     and synthesizes into hardware accelerators. We identify current
to enhance compatibility between Dafny translation, PyLog           limitations due to unsupported recursion and control flow
optimizations, and Vivado HLS, ensuring that the number of          structures in HLS, and highlight ongoing efforts to enhance
verified programs successfully synthesized into RTL aligns          pipeline robustness.
more closely with the number of verified inputs.                       Proof2Silicon thus establishes a scalable, model-agnostic,
   Table III summarizes the performance and resource results        and formally verified approach to trustworthy AI-assisted
for selected benchmark tasks across different LLMs and              hardware synthesis, charting a promising path forward for
verifier feedback settings, demonstrating that the successfully     next-generation EDA tools and AI-driven design automation.
synthesized designs are executable on FPGA hardware. While
our current focus is on correctness and verifiability, these pre-                         ACKNOWLEDGEMENT
liminary numbers also confirm that the generated HLS C codes
can be mapped onto the FPGA fabric with consistent resource            This work is supported by the AMD Center of Excel-
utilization. Future work will extend beyond correctness to ex-      lence grant at UIUC and Semiconductor Research Corporation
plicitly optimize synthesis performance metrics such as latency     (SRC) 2023-CT-3175 grant.
and resource utilization, enabling the generation of hardware-
                                                                                                R EFERENCES
aware code that balances verification guarantees with practical
throughput and efficiency in FPGA implementations.                  [1] H. Koziolek, S. Grüner, R. Hark, V. Ashiwal, S. Linsbauer, and
                                                                        N. Eskandani, “Llm-based and retrieval-augmented control code
                                                                        generation,” in Proceedings of the 1st International Workshop on Large
C. Implementation Details                                               Language Models for Code, ser. LLM4Code ’24. New York, NY,
                                                                        USA: Association for Computing Machinery, 2024, p. 22–29. [Online].
   All experiments were conducted on a dedicated workstation            Available: https://doi.org/10.1145/3643795.3648384
equipped with two NVIDIA H100 GPUs, running Ubuntu                  [2] S. Yang and Y. Yang, “Formaleval: A method for automatic evaluation of
20.04 and Python 3.10. Evaluation was done on the Dafny-                code generation via large language models,” in 2024 2nd International
                                                                        Symposium of Electronics Design Automation (ISEDA), 2024, pp. 660–
Bench suite- 100 test tasks covering algorithms such as sorting,        665.
arithmetic operations, and list manipulations.                      [3] W. Murphy, N. Holzer, F. Qiao, L. Cui, R. Rothkopf, N. Koenig,
                                                                        and M. Santolucito, “Combining llm code generation with formal
                                                                        specifications and reactive program synthesis,” 2024. [Online].
D. Future Work                                                          Available: https://arxiv.org/abs/2410.19736
   A key direction for future work is to enhance the com-           [4] K. R. M. Leino, “Dafny: An automatic program verifier for functional
                                                                        correctness,” in Logic for Programming, Artificial Intelligence, and
patibility between Dafny verification, PyLog translation, and           Reasoning, E. M. Clarke and A. Voronkov, Eds. Berlin, Heidelberg:
Vivado HLS synthesis. We plan to refine the translation flow            Springer Berlin Heidelberg, 2010, pp. 348–370.
to proactively avoid unsupported constructs such as recursion,      [5] Y. Ren and D. J. Sutherland, “Learning dynamics of llm finetuning,”
                                                                        2025. [Online]. Available: https://arxiv.org/abs/2407.10490
dynamic loops, and other control-flow patterns that currently       [6] M. Jha, J. Wan, H. Zhang, and D. Chen, “Preface - a
hinder hardware generation, thereby reducing synthesis fail-            reinforcement learning framework for code verification via llm
ures and narrowing the gap between the number of verified               prompt repair,” in Proceedings of the Great Lakes Symposium on
                                                                        VLSI 2025, ser. GLSVLSI ’25. New York, NY, USA: Association
programs and those successfully synthesized. Furthermore,               for Computing Machinery, 2025, p. 547–553. [Online]. Available:
we aim to extend the framework beyond correctness by                    https://doi.org/10.1145/3716368.3735300
integrating hardware-aware optimizations directly into the          [7] S. Huang, K. Wu, H. Jeong, C. Wang, D. Chen, and W.-M. Hwu, “Pylog:
                                                                        An algorithm-centric python-based fpga programming and synthesis
PREFACE agent, enabling it to generate Dafny code that is               flow,” IEEE Transactions on Computers, vol. 70, no. 12, pp. 2015–2028,
both verification-friendly and synthesis-ready. Incorporating           2021.
synthesis performance metrics such as latency, resource uti-        [8] C. Loughridge, Q. Sun, S. Ahrenbach, F. Cassano, C. Sun, Y. Sheng,
                                                                        A. Mudide, M. R. H. Misu, N. Amin, and M. Tegmark, “Dafnybench: A
lization, and throughput into the optimization objectives will          benchmark for formal software verification,” 2024. [Online]. Available:
allow Proof2Silicon to balance formal verification guarantees           https://arxiv.org/abs/2406.08467
 [9] D. Chen, J. Cong, Y. Fan, G. Han, W. Jiang, and Z. Zhang, “xpilot:
     A platform-based behavioral synthesis system,” in Proceedings of SRC
     Techcon Conference, October 2005.
[10] A. Reynolds and V. Kuncak, “Induction for smt solvers,” in Verification,
     Model Checking, and Abstract Interpretation, D. D’Souza, A. Lal, and
     K. G. Larsen, Eds. Berlin, Heidelberg: Springer Berlin Heidelberg,
     2015, pp. 80–98.
[11] J. Liu, C. S. Xia, Y. Wang, and L. ZHANG, “Is your code generated
     by chatgpt really correct? rigorous evaluation of large language models
     for code generation,” in Advances in Neural Information Processing
     Systems, A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt, and
     S. Levine, Eds., vol. 36. Curran Associates, Inc., 2023, pp. 21 558–
     21 572.
[12] L. Ma, S. Liu, Y. Li, X. Xie, and L. Bu, “Specgen: Automated
     generation of formal program specifications via large language models,”
     2025. [Online]. Available: https://arxiv.org/abs/2401.08807
[13] M. R. H. Misu, C. V. Lopes, I. Ma, and J. Noble, “Towards ai-assisted
     synthesis of verified dafny methods,” Proc. ACM Softw. Eng., vol. 1, no.
     FSE, Jul. 2024. [Online]. Available: https://doi.org/10.1145/3643763
[14] G. Poesia, C. Loughridge, and N. Amin, “dafny-annotator: Ai-
     assisted verification of dafny programs,” 2024. [Online]. Available:
     https://arxiv.org/abs/2411.15143
[15] Y. C. Li, S. Zetzsche, and S. Somayyajula, “Dafny as verification-aware
     intermediate language for code generation,” 2025. [Online]. Available:
     https://arxiv.org/abs/2501.06283
[16] Y. Du, O. Watkins, Z. Wang, C. Colas, T. Darrell, P. Abbeel,
     A. Gupta, and J. Andreas, “Guiding pretraining in reinforcement
     learning with large language models,” 2023. [Online]. Available:
     https://arxiv.org/abs/2302.06692
[17] Y. Zhuang, Y. Shen, Z. Zhang, Y. Chen, and F. Miao, “Yolo-marl: You
     only llm once for multi-agent reinforcement learning,” 2024. [Online].
     Available: https://arxiv.org/abs/2410.03997
[18] Y. Wei, X. Shan, and J. Li, “Lero: Llm-driven evolutionary
     framework with hybrid rewards and enhanced observation for
     multi-agent reinforcement learning,” 2025. [Online]. Available:
     https://arxiv.org/abs/2503.21807
[19] S. Liu, W. Fang, Y. Lu, J. Wang, Q. Zhang, H. Zhang,
     and Z. Xie, “Rtlcoder: Fully open-source and efficient llm-
     assisted rtl code generation technique,” 2024. [Online]. Available:
     https://arxiv.org/abs/2312.08617
[20] Z. Yu, M. Liu, M. Zimmer, Y. C. Lin, Y. Liu, and H. Ren,
     “Spec2rtl-agent: Automated hardware code generation from complex
     specifications using llm agent systems,” 2025. [Online]. Available:
     https://arxiv.org/abs/2506.13905
[21] C. Xiong, C. Liu, H. Li, and X. Li, “Hlspilot: Llm-based high-level
     synthesis,” in Proceedings of the 43rd IEEE/ACM International
     Conference on Computer-Aided Design, ser. ICCAD ’24. New York,
     NY, USA: Association for Computing Machinery, 2025. [Online].
     Available: https://doi.org/10.1145/3676536.3676781
[22] R. Ma, Y. Yang, Z. Liu, J. Zhang, M. Li, J. Huang, and G. Luo,
     “Verilogreader: Llm-aided hardware test generation,” in 2024 IEEE LLM
     Aided Design Workshop (LAD), 2024, pp. 1–5.
[23] M. DeLorenzo, V. Gohil, and J. Rajendran, “Creativeval: Evaluating
     creativity of llm-based hardware code generation,” in 2024 IEEE LLM
     Aided Design Workshop (LAD), 2024, pp. 1–5.
[24] A. Papakonstantinou, K. Gururaj, J. A. Stratton, D. Chen, J. Cong, and
     W.-M. W. Hwu, “Fcuda: Enabling efficient compilation of cuda kernels
     onto fpgas,” in 2009 IEEE 7th Symposium on Application Specific
     Processors, 2009, pp. 35–42.
[25] H. Ye, C. Hao, J. Cheng, H. Jeong, J. Huang, S. Neuendorffer, and
     D. Chen, “Scalehls: A new scalable high-level synthesis framework
     on multi-level intermediate representation,” in 2022 IEEE International
     Symposium on High-Performance Computer Architecture (HPCA), 2022,
     pp. 741–755.
[26] OpenAI et al., “Gpt-4 technical report,” 2024. [Online]. Available:
     https://arxiv.org/abs/2303.08774
[27] T. Zhong and Others, “Evaluation of openai o1: Oppor-
     tunities and challenges of agi,” 2024. [Online]. Available:
     https://arxiv.org/abs/2409.18486
[28] B. Hui and Others, “Qwen2.5-coder technical report,” 2024. [Online].
     Available: https://arxiv.org/abs/2409.12186
[29] Qwen and Others, “Qwen2.5 technical report,” 2025. [Online].
     Available: https://arxiv.org/abs/2412.15115
