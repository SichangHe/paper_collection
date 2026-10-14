                                                    CuBridge: An LLM-Based Framework for Understanding and
                                                       Reconstructing High-Performance Attention Kernels

                                                  Xing Ma1,2∗ , Yangjie Zhou3∗† , Wu Sun1 , Zihan Liu1,2 , Jingwen Leng1,2 ,
                                                          Yun Lin1† , Shixuan Sun1 , Minyi Guo1 , Jin Song Dong3
                                        1
                                          Shanghai Jiao Tong University, 2 Shanghai Qi Zhi Institute, 3 National University of Singapore
                                              {maxing1207, by5892q, altair.liu, lin_yun, sunshixuan}@sjtu.edu.cn
                                                 {leng-jw, guo-my}@cs.sjtu.edu.cn, {yj_zhou, dcsdjs}@nus.edu.sg


                                                                  Abstract                          a one-off engineering task, but an ongoing systems
                                                                                                    challenge.
                                                Efficient CUDA implementations of attention
arXiv:2605.05023v1 [cs.LG] 6 May 2026




                                                                                                       Existing approaches expose a fundamental trade-
                                                mechanisms are critical to modern deep learn-
                                                ing systems, yet supporting diverse and evolv-      off between generality and performance. High-
                                                ing attention variants remains challenging. Ex-     level frameworks (Paszke et al., 2019) and com-
                                                isting frameworks and compilers trade perfor-       pilers (Guessous et al., 2024) provide flexible ex-
                                                mance for flexibility, while expert-written ker-    pression of new attention semantics but rely on
                                                nels achieve high efficiency but are difficult to   generic and inefficient implementations, while ex-
                                                adapt. Recent work explores large language          pert libraries (Dao, 2024; Shah et al., 2024) achieve
                                                models (LLMs) for GPU kernel generation, but        strong efficiency through carefully engineered ker-
                                                prior studies report unstable correctness and
                                                                                                    nels that are difficult to adapt. As a result, ex-
                                                significant performance gaps for complex oper-
                                                ators such as attention.                            tending high-performance attention kernels to new
                                                                                                    variants often requires substantial manual effort.
                                                We present CuBridge, an LLM-based frame-
                                                work that adapts expert-written attention ker-
                                                                                                       Large language models (LLMs) offer a promis-
                                                nels through a structured lift–transfer–lower       ing direction for reducing the manual effort in-
                                                workflow. CuBridge starts from expert-written       volved in GPU kernel development, and recent
                                                CUDA attention kernels and lifts them into          benchmarks have explored their use for kernel gen-
                                                an executable intermediate representation that      eration (Ouyang et al., 2025; Li et al., 2025a). How-
                                                makes execution orchestration explicit while        ever, for complex operators such as attention, prior
                                                abstracting low-level CUDA syntax. Given a          studies report unstable correctness and substan-
                                                user-provided PyTorch specification, CuBridge
                                                                                                    tial performance gaps relative to optimized base-
                                                generates and verifies a target IR program,
                                                then reconstructs optimized CUDA code via           lines (Ouyang et al., 2025), indicating that directly
                                                reference-guided lowering. Across diverse at-       applying LLMs to attention kernels remains unreli-
                                                tention variants and GPU platforms, CuBridge        able in practice.
                                                consistently produces correct kernels and sub-         A key observation underlying this work is that
                                                stantially outperforms general frameworks,          expert-written CUDA kernels already encode cor-
                                                compiler-based approaches, and prior LLM-           rect and efficient execution behavior. Rather than
                                                based methods.
                                                                                                    generating attention kernels from scratch, we treat
                                        1       Introduction                                        these expert implementations as performance ref-
                                                                                                    erences and focus on enabling controlled semantic
                                        Attention kernels are a central performance com-            adaptation while preserving their execution struc-
                                        ponent in modern deep learning systems (Paszke              ture. This perspective motivates a workflow that
                                        et al., 2019; Abadi et al., 2016; Chen et al., 2018).       separates semantic reasoning from low-level code
                                        As model architectures evolve, beyond standard              manipulation, allowing modifications to be ex-
                                        softmax attention, attention increasingly appears in        pressed at an appropriate level of abstraction.
                                        customized forms, including new masking behav-                 Guided by this insight, we present CuBridge, an
                                        iors, modified score computations, alternative nor-         LLM-based framework that adapts expert-written
                                        malization rules, and fused pipelines. Efficiently          attention kernels through a structured lift-transfer-
                                        supporting these variants on GPUs is therefore not          lower workflow. CuBridge first lifts source CUDA
                                            ∗
                                                Equal contribution.                                 code into a structured intermediate representation
                                            †
                                                Corresponding authors.                              CuIR, which makes execution orchestration ex-
plicit while retaining performance-critical infor-                                                                  Grid
                                                                                 DRAM
mation. It then transfers the lifted IR program to                    SHMEM                SHMEM                   Block
match user-specified attention semantics, and fi-               Reg            Reg   Reg            Reg

nally lowers the transformed representation back                      Cuda                 Cuda                   Warpgroup
                                                                      Core                 Core
into optimized CUDA code via reference-guided re-
                                                                                                                   Warp
construction. Crucially, the intermediate represen-                   Tensor
                                                                       Core
                                                                                           Tensor
                                                                                            Core
tation is executable, enabling verification at each                    SM                   SM                    Thread
stage and ensuring semantic correctness.
                                                        Figure 1: Hardware architecture and execution model
   We implement and evaluate CuBridge on
                                                        of modern GPUs.
NVIDIA A100 and H100 across a range of atten-
tion variants and real-model configurations. Our        2.1   GPU Architecture and Execution Model
results show that CuBridge consistently produces
                                                        Modern GPUs expose a hierarchical organization
correct kernels and achieves, on average, speedups
                                                        of both execution units and memory resources, as
of 16.03× over general frameworks, 1.39× over
                                                        shown in Figure 1. CUDA kernels run under the
template-based compilers, and 3.33× over prior
                                                        SIMT model (Luebke, 2008), where threads are
LLM-based approaches. These results demonstrate
                                                        grouped into warps and scheduled in thread blocks,
the effectiveness of our approach for supporting
                                                        while data resides in a memory hierarchy includ-
evolving attention mechanisms with both correct-
                                                        ing global memory, shared memory, and registers.
ness and high performance.
                                                        High-performance CUDA kernels depend on care-
    Our contributions are summarized as follows:        fully coordinating computation and data movement
• We propose a new LLM-assisted paradigm for            across these execution units and memory levels.
  adapting expert-written attention kernels that        We refer to this coordination as execution orches-
  avoids end-to-end code generation, and instead        tration, which determines how work is assigned
  performs semantic adaptation through a struc-         to parallel units, how operations are ordered with
  tured lift–transfer–lower workflow.                   synchronization, and how data is moved across the
• We design CuIR, an executable intermediate rep-       memory hierarchy, all of which directly impact
  resentation that makes performance-critical ex-       performance.
  ecution orchestration explicit while abstracting         Modern hardware features such as tensor
  low-level CUDA syntax, and build an end-to-end        cores (NVIDIA, 2017), asynchronous memory
  system CuBridge on top of it to enable reliable se-   copies (NVIDIA, 2021), and pipelined execution
  mantic adaptation, intermediate verification, and     (NVIDIA, 2023) further increase the complexity
  reference-guided kernel reconstruction.               of execution orchestration. For example, warp-
• We evaluate CuBridge across a wide range of           specialized (NVIDIA, 2025a; Bauer et al., 2014)
  attention variants and GPU platforms, showing         pipelines assign different roles to different warps
  that it consistently produces correct kernels and     within a thread block and rely on explicit synchro-
  outperforms general frameworks, template-based        nization to coordinate data movement and compu-
  compilers, and prior LLM-based approaches.            tation. As a result, execution orchestration plays a
                                                        central role in determining the performance charac-
                                                        teristics of CUDA kernels.
2    Preliminaries                                      2.2   Attention Variants
                                                        Given query, key, and value matrices Q, K, V ∈
The goal of this work is to efficiently support high-   RL×d , the standard scaled dot-product atten-
performance CUDA (NVIDIA, 2025b) kernels for            tion (Vaswani et al., 2017) is defined as:
diverse attention variants. Achieving high perfor-
                                                                                                  QK T
                                                                                                         
mance on GPUs relies on complex and carefully en-
                                                                       O = Softmax                 √          V               (1)
gineered coordination across multiple levels of par-                                                 d
allelism and memory hierarchies (NVIDIA, 2021,
2023). As attention mechanisms continue to evolve,        A wide range of attention variants have been pro-
supporting new semantics with high-performance          posed to support different modeling requirements.
CUDA kernels becomes increasingly challenging.          At a semantic level, many of these variants can be
__device__ void flash_gemm(…) {                                                   Verifier via CuIR Executor
    ...
                                                        Evaluate            Fix                            Evaluate   Fix
    asm volatile("wgmma.fence.sync.…”);
    cute::gemm(…); // use wgmma ptx                      Src CuBridge IR                IR Transfer        Tgt CuBridge IR
    asm volatile("wgmma.commit_group…”);
                                                                                                             IR Differencer
}




                                                                                        Ground Truth
…




                                                                                          Verifier
                                                                   Lifter




                                                                                                                                Refiner
// async gemm to compute S = Q * K                                                                            Code Patch
flash_gemm(…);
                                                                                                                Rewriter
// other operations overlap with compute S                                                   nn.Module
…                                                                                                                             GPU &
                                                              Src CUDA                                         Tgt CUDA
Mask(S); // mistake point                                                                     User Input                      Profiler
wait_group<1>( ); // wait for async gemm
Mask(S); // correct point                                                    Figure 3: Overview of CuBridge.
softmax( );
                                                        result, non-standard attention variants either suf-
Figure 2: Failure case of directly applying LLM to
                                                        fer from noticeable performance degradation or
modify FlashAttention-3 CUDA code for the PrefixLM
mask variant with GPT-5.                                demand significant manual engineering.
                                                           Recent work has explored the use of large lan-
                                                        guage models (LLMs) to automate GPU kernel gen-
understood as modifying different semantic com-         eration. Benchmark studies (Ouyang et al., 2025)
ponents of the attention computation. In particular,    show that while LLM-generated CUDA kernels can
attention can be viewed as a sequence of score          perform competitively on simple operators, their
computation, masking, and normalization:                correctness becomes unstable and performance de-
                       
                               QK T
                                                      grades significantly for complex kernels such as
   O = Norm Mask Score( √ )                V (2)        attention, with slowdowns of up to 34.9× relative
                                   d
                                                        to optimized baselines. Several recent efforts ex-
Under this view, variants commonly modify the           plore LLM-based code generation and optimiza-
score function (Shaw et al., 2018), the masking         tion, including multi-agent collaboration (Chen
rules (Wang et al., 2025; Pal et al., 2023; Zaheer      et al., 2025b; Huang et al., 2024; Zhang et al., 2024)
et al., 2020; Ouyang et al., 2022; Bertsch et al.,      , profiler-driven feedback (Dong et al., 2025; Is-
2025), or the normalization behavior (Dao et al.,       lam et al., 2024; Chen et al., 2024), and natural
2022; Ramapuram et al., 2025).                          language-based planning (Zhou et al., 2025a). De-
   While these semantic changes appear localized        spite their promise, these approaches do not yet
at the algorithmic level, their realization in GPU      provide a reliable way to realize expert-level exe-
kernels often requires conditional execution, bound-    cution orchestration for complex kernels.
ary handling, or changes in loop structure. Such           A natural attempt to improve flexibility is to
control-flow and data-dependence changes directly       directly modify expert-written CUDA kernels using
affect how computation, synchronization, and data       LLMs. However, as shown in Figure 2, expert
movement are orchestrated on the GPU, making            kernels often rely on complex syntax and implicit
correct and efficient kernel implementation signifi-    asynchronous execution. Even when the intended
cantly more challenging.                                semantic modification is clear, locating the correct
2.3   Current Support for Attention Variants            code region to update can be error-prone, making
                                                        direct code-level adaptation unreliable.
Existing systems for supporting attention variants
exhibit a fundamental trade-off between generality      3     Method
and performance. General frameworks (e.g., Py-
Torch (Paszke et al., 2019)) allow new attention        3.1        Overview
semantics to be expressed easily at a high level, but   We present CuBridge, an LLM-powered framework
do not provide expert-level CUDA kernels for most       for adapting expert-written CUDA attention kernels
variants. Template-based compilation approaches         to new algorithmic variants while preserving high-
(e.g., FlexAttention (Guessous et al., 2024)) allow     performance execution orchestration. Instead of
limited customization within fixed templates, while     generating kernels from scratch, CuBridge follows
expert libraries (e.g., FlashAttention (Dao, 2024;      a lift–transfer–lower workflow centered on an exe-
Shah et al., 2024)) achieve high efficiency but re-     cutable intermediate representation, CuIR, which
quire substantial manual effort to extend. As a         supports both understanding and reconstruction of
                    Source CUDA                                             Lifter                                   Source IR
      1 // Emitting declaration and Initialization                                                     1 def producer(…):
                                                                               Role
      2 if (threadIdx.x < 128) { // Producer                 You are a CUDA expert, your task is to    2    for tile in range(k_tiles):
      3 for (auto tile : k_tiles) {                          extract high-level semantics from a       3      empty.wait()
    4     wait(empty[…]);                                    source CUDA implementation, try to lift    4     # copy global to share with TMA
    5     if (threadIdx.x == 0) {                            the statements to given high-level IR.     5     copy_async(gA, sA, “TMA”, full)
    6       cde::cp_async_bulk_2d(A/B, …, full);                       Task Instructions:               6     copy_async(gB, sB, “TMA”, full)
    7       full[…].arrive_expect_tx(A/B.size);}             Step 1: Commenting the code                7     full.arrive()
          else {                                             Step 2: Analyzing the task mapping
    8                                                                                                   8 def consumer(…):
    9       full[…].arrive(); } } }                          Step 3: Lift statements to primitive,          for tile in range(k_tiles):
                                                                                                        9
   10 else { // Consumer
                                                             and output according to [Rules]
                                                                                                       10     full.wait()
   11   for (auto tile : k_tiles) {                                              IR                    11     rC = gemm_async(sA, sB, “WGMMA”)
   12     wait(full[…]);                                     1. wait_for / barrier signal : …                 wait_group(0)# wait for gemm_async
                                                                                                       12
                                                             2. copy / compute : …
   13     wgmma::mma_async(C_frag, A_buf, B_buf);                                                      13     empty.arrive()
                                                             3. bind/commit:…
   14     wgmma::commit_group();                                                                       14   # instruction: 16-bytes vectorized
   15     wgmma::wait_group<0>();
                                                                              Rules                         copy(rC, gC, “store.128”)
                                                                                                       15
                                                             1. Use memory primitive to represent
   16     empty[…].arrive(); } }                                                                       16 def run(…):
                                                             tile shape, hierarchy, instruction
   17 for (auto m, n : TILE_M, TILE_N) {                     2. Use compute primitive to represent     17   bind(producer, Warp Group 0)
   18   *(int4*)(&C[…]) = *(int4*)(&C_frag[…]); } }          …, Output Format: …                       18   bind(consumer, Warp Group 1)


Figure 4: The Semantic Lifting Process. The left panel shows the complex Source CUDA, and the right panel
displays the lifted Source IR, where code blocks of the same color represent mapping relationships. The center
shows the modularized prompt, consisting of the CuIR documentation and the Chain-of-Thought reasoning process.

 Category    Primitives                 Exposed Information                     Design Rationale. High-performance CUDA ker-
 Memory      alloc, copy, copy_async    Tile Shape, Memory                      nels derive their efficiency from carefully struc-
                                        Hierarchy
                                                                                tured execution orchestration, rather than from indi-
 Compute     gemm_async, gemm           Instruction Selection,                  vidual instructions in isolation. Accordingly, CuIR
                                        Operand
                                                                                is designed to explicitly preserve three classes of
 Sync.       barrier.{wait, arrive}     Data Dependency
                                                                                information: the operations invoked by the kernel,
 Control     bind, commit               Execution Granularity
                                                                                the ordering and data dependencies among these
Table 1: CuIR Primitives and Exposed Hardware Se-                               operations, and the execution granularity and syn-
mantics.                                                                        chronization scope at which they are performed.
                                                                                As summarized in Table 1, Memory and Compute
expert CUDA kernels.                                                            primitives make operations explicit, including tile-
   As shown in Figure 3, given a high-performance                               level data movement and instruction-level choices,
source CUDA kernel and a user-provided PyTorch                                  while Synchronization and Control primitives en-
reference specifying target semantics, CuBridge                                 code dependencies, execution ordering, and col-
proceeds in three stages. (1) Lifting: CuBridge                                 lective execution granularity. These preserved el-
lifts the Source kernel into CuIR, which abstracts                              ements are directly linked to correctness and per-
away low-level syntactic details while retaining                                formance, as GPU efficiency hinges on latency hid-
performance-critical execution orchestration. (2)                               ing and data locality. Conversely, CuIR abstracts
Transform: guided by Target semantics, CuBridge                                 away low-level implementation details such as frag-
generates the Target CuIR from the lifted Source                                mented thread-level indexing and verbose CUDA
CuIR, jointly reasoning about semantic correct-                                 syntax, which are not essential to reasoning about
ness and performance optimization. (3) Lowering:                                execution structure.
CuBridge lowers the Target CuIR back to CUDA by                                 Key Capabilities. CuIR provides two capabilities
differencing the Source and Target CuIR programs                                that are essential to CuBridge.
and generating minimal patches that update the cor-                             1) Kernel Understanding and Reconstructing. By
responding code regions in the Source kernel to                                 making execution orchestration explicit through
reconstruct the target kernel.                                                  structured primitives, CuIR exposes the execution
                                                                                logic of a CUDA kernel as a composition of well-
3.2       CuIR Design                                                           defined operations and dependencies, rather than
To enable effective LLM-based understanding and                                 low-level syntax. This structured representation
reconstruction of expert CUDA kernels, we de-                                   allows an LLM to understand and reason kernel
sign CuIR, a Pythonic and executable intermediate                               behavior, enabling semantic changes to be captured
representation that explicitly captures execution                               in the generated Target CuIR and localized via IR
orchestration. Structurally, CuIR is expressed in                               differencing for Target CUDA reconstruction.
Python syntax and built on a set of custom primi-                               2) Intermediate Verification. CuIR is designed to
tives that operate on data tiles as PyTorch tensors.                            be executable and verifiable through a dedicated
                                                       for tile in range(…):        # Full (Un-Masked) Loop
IR backend executor, enabling validation of al-          # …                        for tile in range(…):
gorithmic logic and data dependencies at the IR          S = gemm(Q, K, MMA)          # Same as origin
                                                         P = Softmax(S)
level. To ensure semantic alignment with CUDA            # …                                Target IR
                                                        Source IR                   # Partial (Masked) Loop
execution, the executor explicitly models the ker-                  Transferring    for tile in range(…):
                                                         Variant           Full       # …
nel’s parallel structure and synchronization behav-                                   S = gemm(Q, K, MMA)
                                                        PrefixLM          Blocks
ior. Independent parallel tasks are executed sequen-                                  S = Mask(S)
                                                        Transfer          Partial     P = Softmax(S)
tially without affecting correctness, while depen-      Splitting         Blocks      # …

dent tasks are ordered to respect synchronization      Figure 5: Performance-Aware Transformation for Pre-
and data-dependence constraints. This execution        fixLM. The IR Transfer performing Loop Splitting to
model allows IR-level verification to faithfully re-   confine mask checks exclusively to boundary tiles.
flect CUDA kernel behavior.
                                                       access patterns, and surrounding control structure.
3.3   Semantic Lifting                                 The generated CuIR program explicitly encodes the
The first stage of CuBridge lifts an expert-written    execution orchestration of the original kernel and
CUDA kernel into CuIR, extracting its high-level       serves as the input to subsequent transformation
execution orchestration while abstracting away low-    and lowering stages.
level implementation complexity. As illustrated        Post-Lifting Verification & Refinement. The gen-
in Figure 4, the Lifter performs a single LLM in-      erated CuIR program is executed by the backend
vocation with structured chain-of-thought (CoT)        executor and its output is compared against the
reasoning, organized into three sub-tasks.             source CUDA within a numerical tolerance (e.g.,
1) Syntax Annotation. This step resolves low-          10−2 for fp16), following CUTLASS (NVIDIA,
level syntactic ambiguity by annotating CUDA op-       2025a). On mismatch, the executor log is used to
erations with explicit semantic comments. Expert       diagnose errors such as incorrect tile parameters or
CUDA kernels often rely on low-level PTX intrin-       missing synchronization, and guides the regenera-
sics or library-specific APIs (e.g., CuTe), whose      tion of the IR. This closed-loop refinement ensures
semantics are implicit in the source code and not      that the final Source IR faithfully preserves the
directly exposed. The Lifter augments such opera-      source kernel semantics.
tions with concise semantic descriptions grounded
in official CUDA and CuTe documentation, produc-       3.4     Semantic Transformation
ing an annotated CUDA representation that makes        In this stage, the IR Transfer transforms the lifted
the intent of low-level instructions explicit.         Source IR into a Target IR that implements the
2) Code-to-Worker Mapping Analysis. This step          target operator semantics specified by a user-
identifies which code regions in the source CUDA       provided PyTorch reference, while enabling the
kernel are executed by which parallel execution        performance-critical execution orchestration.
units, making implicit execution relationships ex-     1) Semantic Alignment. The IR Transfer first ana-
plicit. Here, we use the term worker to denote a       lyzes the PyTorch reference to identify the semantic
cooperative CUDA execution unit, such as a thread      difference between source IR and target operator.
block, warp group, or warp. Specifically, the Lifter   Guided by this gap, it maps the required seman-
analyzes control-flow predicates over thread in-       tics to CuIR primitives and determines where the
dices and attributes guarded code regions to the       source orchestration must be extended or modi-
corresponding workers. For example, as shown in        fied. In this way, the generated Target IR program
Figure 4 (Source CUDA, Line 2), the branch if          matches the target computation while remaining
(threadIdx.x < 128) partitions the kernel into         structurally aligned with the Source IR.
two worker-aligned regions, which are later bound      2) Performance-Aware Transformation. A
to different warp groups in the generated IR.          semantics-correct Target IR can still be inefficient.
3) Primitive Lifting. In the final step, the Lifter    To maintain efficiency, the IR Transfer further ana-
translates each worker-aligned code region into a      lyzes the performance implications of the required
sequence of CuIR primitives and constructs the         semantic changes during Target IR generation. For
corresponding Source IR. This process recovers         PrefixLM (Pal et al., 2023), the validity of the atten-
primitive parameters such as tile shapes, memory       tion mask correlates with the nested loop iteration
placement, instruction variants, and synchroniza-      space: element-wise checks are required only for
tion scope by analyzing index expressions, memory      partial blocks, whereas other blocks are fully valid.
As shown in Figure 5, the IR Transfer applies loop       context-length limitations of full-file rewriting.
splitting to construct a check-free Full Loop for
full blocks and a Partial Loop that applies masking      4     Experiment
for partial blocks, thereby avoiding unnecessary
                                                         4.1    Experiment Setup
element-wise checking in the full-loop region.
Post-Transformation Verification. The generated          We evaluate CuBridge along three aspects: (1) end-
Target IR is executed by the CuIR backend execu-         to-end kernel correctness and performance across
tor and validated against the user-provided PyTorch      representative model configurations, (2) robustness
reference implementation, using the same verifi-         across diverse attention semantics, including previ-
cation procedure as in Sec. 3.3. Any mismatch            ously unsupported variants, and (3) the impact of
triggers iterative refinement.                           key design choices via ablation studies.
                                                         GPU platforms. All experiments are conducted
3.5   Kernel Reconstruction                              on NVIDIA GPUs from two widely deployed ar-
The final stage lowers the transformed Target            chitectures: A100 (Ampere) (NVIDIA, 2021) and
IR into high-performance Target CUDA code.               H100 (Hopper) (NVIDIA, 2023).
CuBridge reconstructs the target implementation by       LLM Backends. We evaluate CuBridge using di-
applying localized, IR-guided code patches within        verse SOTA LLMs, including the closed-source
a structured ReAct workflow (Yao et al., 2023).          models of GPT-5 (OpenAI, 2025), Claude-3.5-
1) Differential Analysis. Reconstruction begins by       Sonnet (Anthropic, 2025), as well as open-source
comparing the Source IR and the Target IR to iden-       models of DeepSeek-V3 (DeepSeek-AI, 2024),
tify semantic differences introduced during trans-       Qwen-3-235B (Team, 2025), Qwen-3-32B (Team,
formation. Leveraging the region-level correspon-        2025).
dence established in the lifting stage, these IR-level   Attention Variants. We focus our evaluation on
changes are traced back to their corresponding lo-       attention mechanisms that are currently not sup-
cations in the Source CUDA code, precisely identi-       ported in the standard FlashAttention (Dao et al.,
fying the code regions that require modification.        2022; Dao, 2024; Shah et al., 2024) library. Our
2) Reference-Guided Lowering. To translate the           test suite encompasses a diverse set of variants,
Target CuIR program into CUDA code, CuBridge             including PrefixLM (Pal et al., 2023), Global Slid-
performs reference-guided lowering by using the          ing Window (Zaheer et al., 2020), Share Question
Source CUDA kernel as an implementation refer-           Mask (Ouyang et al., 2022), Causal Blockwise
ence for the Source IR. This reference specifies         Mask (Bertsch et al., 2025), Relative Position Em-
how abstract IR primitives should be concretely          beddings (Shaw et al., 2018), ReLU Attention (Dao
realized in CUDA, ensuring consistency with the          et al., 2022), and Sigmoid Attention (Ramapuram
original kernel’s implementation style. The lower-       et al., 2025). To assess robustness under unseen
ing process focuses on two tasks:                        compositions, we additionally evaluate a compos-
• Primitive Lowering: Lowering abstract IR prim-         ite variant that combines PrefixLM, Softcap, and
   itives (e.g., copy_async) to concrete hardware        Sigmoid attention. All hyper-parameters follow the
   intrinsics (e.g., cp.async.ca) used in the source     configurations reported in the original works.
   kernel.                                               Comparison Baselines. CuBridge adopts FlashAt-
• Index Mapping: Expanding tile-level operations         tention v2.8.0 (Dao, 2024) as the source expert
   into thread-level indexing that follows the data      kernel reference. We compare CuBridge with three
   layout and indexing patterns in the source kernel.    representative state-of-the-art baselines represent-
3) Iterative Patching. Finally, the Rewriter recon-      ing different paradigms currently explored in the
structs the target CUDA kernel by applying local-        literature: (1) PyTorch (Paszke et al., 2019) atten-
ized and minimal code patches to the source imple-       tion implementations built from standard opera-
mentation. These updates are realized through a          tors; (2) FlexAttention (Guessous et al., 2024), a
line-level editing action (Edit_Line) that supports      compiler-based framework for attention generation;
insertion, deletion, and modification of code lines      and (3) Qimeng-Attention (Zhou et al., 2025a), an
within identified regions. By restricting changes        LLM-based attention kernel generation approach.
to affected code segments, this patch-based recon-       Additionally, we compare CuBridge against Flash-
struction ensures faithful alignment between the         Infer (Ye et al., 2025), a high-performance expert-
Target IR and CUDA code, while avoiding the              hand-tuned library.
                                PyTorch        FlexAttention          Qimeng-Attention         CuBridge      No Support       OOM
               A100 | Llama2-7b(q_head=32, kv_head=32)           A100 | Qwen2.5 72B(q_head=64, kv_head=8)     A100 | Llama3.1 405B(q_head=128, kv_head=8)
         200                                               200                                              200
         150                                               150                                              150
TFLOPs




         100                                               100                                              100
          50                                                50                                               50
           0                                                 0                                                0
                 pl gsw sq cb       rp relu sig comb                pl gsw sq cb         rp relu sig comb         pl gsw sq cb      rp relu sig comb
         800
             H100 | Llama2-7b(q_head=32, kv_head=32)             H100 | Qwen2.5 72B(q_head=64, kv_head=8)    H100 | Llama3.1 405B(q_head=128, kv_head=8)
                                                           600                                              600
         600
                                                           400                                              400
TFLOPs




         400
         200                                               200                                              200

           0                                                      0                                                0
                 pl gsw sq cb          rp relu sig comb                pl gsw sq cb rp relu sig comb                    pl gsw sq cb rp relu sig comb
                   Abbreviations: plrp == PrefixLM  | gsw = Global Sliding Window | sq = Share Question Mask | cb = Causal Blockwise Mask
                                          Relative Position | relu = ReLU Attention | sig = Sigmoid Attention | comb = PrefixLM + SoftCap + Sigmoid
                     Figure 6: End-to-end performance comparison across attention variants and GPU platforms.

Benchmark Configurations.                                                                brary. CuBridge achieves comparable performance
   We benchmark attention configurations derived                                         to FlashInfer on its natively supported variants (av-
from three representative real-world LLMs:                                               erage 1.07×) and substantial speedups (average
Llama2-7B (MHA, 32/32/128) (Touvron et al.,                                              3.49×) on variants beyond FlashInfer’s native sup-
2023), Qwen2.5-72B (GQA, 64/8/128) (Yang                                                 port. Detailed results and per-variant comparisons
et al., 2025), and Llama3.1-405B (GQA,                                                   are provided in Appendix C.
128/8/128) (Team, 2024), where the tuple denotes                                            Compared to PyTorch, CuBridge achieves signif-
(query heads / key-value heads / head dimension).                                        icantly higher performance. PyTorch realizes atten-
Sequence length varies over {1k, 2k, 4k, 8k}, with                                       tion variants by composing multiple fine-grained
batch size adjusted to maintain a constant total of                                      operators into separate CUDA kernels, leading to
16k tokens per batch (Dao et al., 2022). For all                                         frequent kernel launches, redundant global memory
LLM-driven approaches, we set the generation                                             accesses, and occasional out-of-memory failures.
temperature to zero (Ouyang et al., 2025) and adopt                                      By generating a single fused kernel that integrates
a best-of-k strategy with k = 10 (Stiennon et al.,                                       the full attention computation, CuBridge avoids
2020), reporting the best achieved performance.                                          these overheads and enables efficient data reuse.
                                                                                            Compared to FlexAttention, CuBridge demon-
4.2            Overall Performance                                                       strates superior performance while supporting a
Figure 6 compares the performance of CuBridge                                            broader range of attention variants. As shown
against all baselines on NVIDIA A100 and H100                                            in Figure 6, CuBridge outperforms FlexAttention
GPUs. We report results at sequence length N =                                           across all evaluated model configurations, with
8k across diverse attention variants and model con-                                      speedups of 1.05×–1.22× on A100 and 1.26×–
figurations. Due to space constraints, the full re-                                      1.66× on H100. Notably, the performance gap
sults are provided in Appendix B. Both CuBridge                                          widens on H100, indicating that CuBridge bet-
and the Qimeng-Attention baseline use GPT-5 as                                           ter adapts to newer GPU architectures. This ad-
the underlying LLM backend.                                                              vantage stems from preserving expert-optimized,
   Across all evaluated tasks, CuBridge supports                                         hardware-specific execution orchestration. Beyond
all tested attention variants, achieves 100% correct-                                    performance, CuBridge supports a broader set of
ness, and consistently outperforms all state-of-the-                                     attention variants that are not covered by FlexAtten-
art baselines. On A100, CuBridge achieves aver-                                          tion, including ReLU Attention, Sigmoid Attention,
age speedups of 12.69×, 1.18× and 2.54× over                                             and complex composite patterns, while maintaining
PyTorch, FlexAttention, and Qimeng-Attention,                                            high performance.
respectively; on H100, these speedups further                                               Compared to Qimeng-Attention, CuBridge con-
increase to 19.82×, 1.62×, 4.35×. Beyond                                                 sistently achieves higher performance across at-
these generative baselines, we also benchmark                                            tention variants of varying complexity. On A100,
CuBridge against the hand-optimized FlashInfer li-                                       CuBridge attains speedups ranging from 1.18× to
                          PyTorch         Qimeng-Attention         applies iterative reasoning and code editing with-
                          FlexAttention   CuBridge
                                                                   out CuIR; and (3) CuBridge. We report Pass@k
                       A100                       H100       600   (whether at least one of k samples passes correct-
     150
                                                                   ness checking) and the geometric mean speedup of
                                                             400
     100
TFLOPs




                                                                   successful cases, normalized to Vanilla GPT-5.
         50                                                  200      Table 2 presents the results. Vanilla GPT-5 ex-
                                                                   hibits low success rates, which saturates quickly
              1k      2k     4k    8k 1k    2k     4k    8k 0      even with increased sampling (Pass@5 reaches
                   Sequence Length       Sequence Length           only 0.38). Adding ReAct reasoning improves
 Figure 7: Performance comparison for the PrefixLM                 correctness (Pass@1: 0.21 → 0.41), but the gain
 variant (Llama2-7B config) across different sequence              plateaus as k increases and yields only limited
 lengths on A100 (left) and H100 (right) GPUs.
                                                                   speedup (1.23×). In contrast, CuBridge achieves
 10.56×, while on H100 the speedups further in-                    perfect correctness (Pass@5 = 1.00), and substan-
 crease to 1.43×–20.3×. As shown in Figure 6,                      tially higher performance, with a 4.19× speedup.
 on simpler variants such as relative position at-                    This confirms that the structured IR provides
 tention, CuBridge achieves performance compara-                   essential support for reliable code modification.
 ble to Qimeng-Attention on A100 (average 1.24×                    By lifting the source CUDA to the CuIR level,
 speedup). In contrast, for variants with com-                     CuBridge makes execution orchestration explicit
 plex masking or irregular execution patterns (e.g.,               and enables structured transformation and verifica-
 share_question_mask and comb), CuBridge de-                       tion before lowering, leading to more stable cor-
 livers substantially larger gains, reaching 5.37× on              rectness and higher performance.
 A100. For the same comb variants, speedups fur-
 ther increase to 11.47× on H100, indicating that                   Method             Pass@1   Pass@3   Pass@5   Norm. Speedup
                                                                    GPT-5               0.21     0.33     0.38        1.00×
 CuBridge better exploits the execution capabilities                GPT-5 + ReAct       0.41     0.54     0.58        1.23×
 of newer GPU architectures. By examining the                       GPT-5 + CuBridge    0.70     0.85     1.00        4.19×
 generated kernels, we observe that while Qimeng-
 Attention introduces limited performance optimiza-                Table 2: Comparison of correctness and performance for
                                                                   different llm-based kernel modification methods across
 tion, it does not construct explicit warp-specialized
                                                                   96 test cases on H100. Performance is reported as the
 and tensor/cuda-core overlap execution orchestra-                 geometric mean of speedup normalized to the Vanilla
 tion. These results suggest that relying solely on                GPT-5 baseline.
 the LLM’s internal knowledge makes it challeng-
 ing to perform efficient execution orchestration for
                                                                   4.4   Impact of Different LLM Backends
 complex tasks, leading to the generated kernels
 only functional but inefficient.                                  To evaluate the generality of CuBridge, we bench-
    Figure 7 reports performance across varying se-                mark it using five representative LLM backends:
 quence lengths for the PrefixLM variant under the                 GPT-5, Claude, DeepSeek-V3, Qwen-3-235B and
 Llama2-7B configuration. Across all evaluated                     Qwen-3-32B. Table 3 reports the achieved through-
 sequence lengths, CuBridge consistently achieves                  put (TFLOPS) on the H100 GPU for the PrefixLM
 higher throughput than SOTA baselines, indicating                 task under the Llama2-7B attention configuration.
 robust scalability with respect to sequence length.                  The results demonstrate that CuBridge achieves
                                                                   stable, expert-level performance once the back-
 4.3          Ablation Study on System Components                  end reaches a baseline CUDA reasoning capabil-
 To validate the effectiveness of our system com-                  ity. Specifically, substituting GPT-5 with Claude,
 ponents, we conduct an ablation study on the task                 DeepSeek-V3, or Qwen-3-235B results in less
 of rewriting expert-written FlashAttention kernels                than 5% performance variation across all se-
 into target attention variants, guided by a user-                 quence lengths. This indicates that our through-
 provided PyTorch reference. Experiments are con-                  put gains primarily stem from the structured
 ducted on H100 across 96 test cases (8 variants                   lift–transfer–lower workflow and CuIR alignment,
 × 12 sequence lengths). We compare three meth-                    rather than reliance on a specific model.
 ods: (1) Vanilla GPT-5, which performs single-shot                   However, we observe a distinct capability thresh-
 code rewriting of the source kernel based solely on               old for code reconstruction. While the larger mod-
 the PyTorch reference; (2) GPT-5 + ReAct, which                   els succeed, Qwen-3-32B fails to produce valid ker-
nels. This suggests that reliable low-level CUDA         JYB2025XDXM113), the National Natural Sci-
generation requires a baseline level of reasoning        ence Foundation of China (Nos. 62532006,
ability. While different frameworks may vary in ro-      62572300), the Shanghai Qi Zhi Institute Innova-
bustness, insufficient model capacity can become a       tion Program (SQZ202316), the Ministry of Edu-
limiting factor for complex kernel generation tasks.     cation, Singapore (Nos. MOE-T2EP20124-0017,
                                                         MOET32020-0004), and the CyberSG R&D Cyber
 LLM Backends    Seq=1k    Seq=2k    Seq=4k   Seq=8k     Research Programme Office (A-8002767-00-00).
 GPT-5            304.35    426.82   577.03   551.73        Any opinions, findings, and conclusions in this
 Claude           292.87    428.64   562.91   569.02     paper are those of the authors only and do not nec-
 DeepSeek-V3      294.12    424.05   557.03   549.73
                                                         essarily reflect the views of our sponsors.
 Qwen-3-235B      295.04    421.63   558.74   542.61
 Qwen-3-32B         N/A       N/A      N/A      N/A

Table 3: Performance comparison (TFLOPS) across          References
different LLM backends on H100 (PrefixLM, Llama2-        Martín Abadi, Paul Barham, Jianmin Chen, Zhifeng
7b attention config).                                     Chen, Andy Davis, Jeffrey Dean, Matthieu Devin,
                                                          Sanjay Ghemawat, Geoffrey Irving, Michael Isard,
                                                          Manjunath Kudlur, Josh Levenberg, Rajat Monga,
5   Conclusion                                            Sherry Moore, Derek Gordon Murray, Benoit Steiner,
                                                          Paul A. Tucker, Vijay Vasudevan, Pete Warden, and
We present CuBridge, an LLM-based framework               3 others. 2016. Tensorflow: A system for large-
for efficiently adapting expert-written attention ker-    scale machine learning. In 12th USENIX Sympo-
                                                          sium on Operating Systems Design and Implemen-
nels to new semantic variants. CuBridge is built          tation, OSDI 2016, Savannah, GA, USA, November
on CuIR, an executable intermediate representation        2-4, 2016, pages 265–283. USENIX Association.
that makes execution orchestration explicit while
abstracting low-level CUDA details, and uses a           Anthropic. 2025. Claude 3.7 sonnet and claude code.
structured lift–transfer–lower workflow for reliable     Carlo Baronio, Pietro Marsella, Ben Pan, Simon Guo,
kernel adaptation. Across diverse real-world atten-        and Silas Alberti. 2025. Kevin: Multi-turn RL for
tion variants on A100 and H100 GPUs, CuBridge              generating CUDA kernels. CoRR, abs/2507.11948.
consistently produces correct kernels and signifi-       Michael Bauer, Sean Treichler, and Alex Aiken. 2014.
cantly outperforms general frameworks, template-           Singe: leveraging warp specialization for high per-
based compilers, and prior LLM-based approaches.           formance on gpus. In ACM SIGPLAN Symposium on
                                                           Principles and Practice of Parallel Programming,
Limitations                                                PPoPP ’14, Orlando, FL, USA, February 15-19,
                                                           2014, pages 119–130. ACM.
Our work has two main limitations. First, CuBridge       Amanda Bertsch, Maor Ivgi, Emily Xiao, Uri Alon,
relies on the availability of high-quality expert ker-    Jonathan Berant, Matthew R. Gormley, and Graham
nels as source references. While such optimized im-       Neubig. 2025. In-context learning with long-context
plementations are widely available in the NVIDIA          models: An in-depth exploration. In Proceedings
                                                          of the 2025 Conference of the Nations of the Amer-
platform, they are often lacking on non-mainstream        icas Chapter of the Association for Computational
customized hardware (e.g., FPGAs). This may               Linguistics: Human Language Technologies, NAACL
limit the effectiveness of our framework in those         2025 - Volume 1: Long Papers, Albuquerque, New
environments. Second, our current evaluation fo-          Mexico, USA, April 29 - May 4, 2025, pages 12119–
                                                          12149. Association for Computational Linguistics.
cuses primarily on attention variants, as they high-
light the complexity of execution orchestration. We      Feiyang Chen, Yu Cheng, Lei Wang, Yuqing Xia, Zim-
have not yet extended our validation to other high-        ing Miao, Lingxiao Ma, Fan Yang, Jilong Xue, Zhi
performance computing tasks, such as scientific            Yang, Mao Yang, and Haibo Chen. 2025a. Attentio-
                                                           nengine: A versatile framework for efficient attention
computing, which remains a promising direction             mechanisms on diverse hardware platforms. CoRR,
for future work.                                           abs/2502.15349.

Acknowledgements                                         Terry Chen, Bing Xu, and Kirthi Devleker. Automat-
                                                           ing GPU kernel generation with DeepSeek-R1 and
This work was supported by the Fundamental                 inference-time scaling.
and Interdisciplinary Disciplines Breakthrough           Tianqi Chen, Thierry Moreau, Ziheng Jiang, Lianmin
Plan of the Ministry of Education of China (No.            Zheng, Eddie Q. Yan, Haichen Shen, Meghan Cowan,
  Leyuan Wang, Yuwei Hu, Luis Ceze, Carlos Guestrin,       Ziyu Huang, Yangjie Zhou, Zihan Liu, Xinhao Luo, Yi-
  and Arvind Krishnamurthy. 2018. TVM: an auto-              jia Diao, Minyi Guo, Jidong Zhai, Yu Feng, Chen
  mated end-to-end optimizing compiler for deep learn-       Zhang, Anbang Wu, and Jingwen Leng. 2026. Flash-
  ing. In 13th USENIX Symposium on Operating Sys-            fuser: Expanding the scale of kernel fusion for
  tems Design and Implementation, OSDI 2018, Carls-          compute-intensive operators via inter-core connec-
  bad, CA, USA, October 8-10, 2018, pages 578–594.           tion. In IEEE International Symposium on High
  USENIX Association.                                        Performance Computer Architecture, HPCA 2026,
                                                             Sydney, Australia, January 31 - Feb. 4, 2026, pages
Wentao Chen, Jiace Zhu, Qi Fan, Yehan Ma, and                1–14. IEEE.
 An Zou. 2025b. CUDA-LLM: llms can write ef-
 ficient CUDA kernels. CoRR, abs/2506.09092.               Md. Ashraful Islam, Mohammed Eunus Ali, and
                                                            Md Rizwan Parvez. 2024. MapCoder: Multi-agent
Xinyun Chen, Maxwell Lin, Nathanael Schärli, and            code generation for competitive problem solving. In
  Denny Zhou. 2024. Teaching large language models          Proceedings of the 62nd Annual Meeting of the As-
  to self-debug. In The Twelfth International Confer-       sociation for Computational Linguistics (Volume 1:
  ence on Learning Representations, ICLR 2024, Vi-          Long Papers), pages 4912–4944, Bangkok, Thailand.
  enna, Austria, May 7-11, 2024. OpenReview.net.            Association for Computational Linguistics.
Tri Dao. 2024. Flashattention-2: Faster attention with     Changxin Ke, Rui Zhang, Shuo Wang, Li Ding, Guangli
   better parallelism and work partitioning. In The          Li, Yuanbo Wen, Shuoming Zhang, Ruiyuan Xu, Jin
  Twelfth International Conference on Learning Rep-          Qin, Jiaming Guo, Chenxi Wang, Ling Li, Qi Guo,
   resentations, ICLR 2024, Vienna, Austria, May 7-11,       and Yunji Chen. 2025. Mutual-supervised learning
   2024. OpenReview.net.                                     for sequential-to-parallel code translation. CoRR,
                                                             abs/2506.11153.
Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra,
   and Christopher Ré. 2022. Flashattention: Fast and      Denis Kocetkov, Raymond Li, Loubna Ben Allal, Jia Li,
   memory-efficient exact attention with io-awareness.       Chenghao Mou, Yacine Jernite, Margaret Mitchell,
   In Advances in Neural Information Processing Sys-         Carlos Muñoz Ferrandis, Sean Hughes, Thomas Wolf,
   tems 35: Annual Conference on Neural Information          Dzmitry Bahdanau, Leandro von Werra, and Harm
  Processing Systems 2022, NeurIPS 2022, New Or-             de Vries. 2023. The stack: 3 TB of permissively li-
   leans, LA, USA, November 28 - December 9, 2022.           censed source code. Trans. Mach. Learn. Res., 2023.
DeepSeek-AI. 2024. Deepseek-v3 technical report.           Jianling Li, Shangzhan Li, Zhenye Gao, Qi Shi, Yux-
  CoRR, abs/2412.19437.                                       uan Li, Zefan Wang, Jiacheng Huang, WangHaojie
                                                              WangHaojie, Jianrong Wang, Xu Han, Zhiyuan Liu,
Juncheng Dong, Yang Yang, Tao Liu, Yang Wang, Feng            and Maosong Sun. 2025a. Tritonbench: Benchmark-
  Qi, Vahid Tarokh, Kaushik Rangadurai, and Shuang            ing large language model capabilities for generating
  Yang. 2025. STARK: strategic team of agents for             triton operators. In Findings of the Association for
  refining kernels. CoRR, abs/2510.16996.                     Computational Linguistics, ACL 2025, Vienna, Aus-
                                                              tria, July 27 - August 1, 2025, pages 23053–23066.
Driss Guessous, Yanbo Liang, Joy Dong, and Ho-                Association for Computational Linguistics.
  race He. 2024. Flexattention: The flexibility of py-
  torch with the performance of flashattention. https:     Xiaoya Li, Xiaofei Sun, Albert Wang, Jiwei Li, and
  //pytorch.org/blog/flexattention/. PyTorch                 Chris Shum. 2025b. CUDA-L1: improving CUDA
  Blog.                                                      optimization via contrastive reinforcement learning.
                                                             CoRR, abs/2507.14111.
Cong Guo, Yangjie Zhou, Jingwen Leng, Yuhao Zhu,
  Zidong Du, Quan Chen, Chao Li, Bin Yao, and Minyi        Zihan Liu, Xinhao Luo, Junxian Guo, Wentao Ni,
  Guo. 2020. Balancing efficiency and flexibility for        Yangjie Zhou, Yue Guan, Cong Guo, Weihao Cui,
  dnn acceleration via temporal gpu-systolic array inte-     Yu Feng, Minyi Guo, Yuhao Zhu, Minjia Zhang,
  gration. In 2020 57th ACM/IEEE Design Automation           Chen Jin, and Jingwen Leng. 2025. VQ-LLM: high-
  Conference (DAC), pages 1–6. IEEE.                         performance code generation for vector quantization
                                                             augmented LLM inference. In IEEE International
Weiming Hu, Zihan Zhang, Haoyan Zhang, Chen Zhang,           Symposium on High Performance Computer Archi-
  Cong Guo, Yu Feng, Tianchi Hu, Guanglin Li,                tecture, HPCA 2025, Las Vegas, NV, USA, March 1-5,
  Guipeng Hu, Junsong Wang, and 1 others. 2026.              2025, pages 1496–1509. IEEE.
  M2xfp: A metadata-augmented microscaling data
  format for efficient low-bit quantization. In Proceed-   David P. Luebke. 2008. CUDA: scalable parallel pro-
  ings of the 31st ACM International Conference on           gramming for high-performance scientific comput-
 Architectural Support for Programming Languages             ing. In Proceedings of the 2008 IEEE International
  and Operating Systems, Volume 2, pages 1151–1167.          Symposium on Biomedical Imaging: From Nano to
                                                             Macro, Paris, France, May 14-17, 2008, pages 836–
Dong Huang, Jie M. Zhang, Michael Luck, Qingwen              838. IEEE.
  Bu, Yuhao Qing, and Heming Cui. 2024. Agentcoder:
  Multi-agent-based code generation with iterative test-   Xinhao Luo, Zihan Liu, Yangjie Zhou, Shihan Fang,
  ing and optimisation. Preprint, arXiv:2312.13010.          Ziyu Huang, Yu Feng, Chen Zhang, Shixuan Sun,
  Zhenzhe Zheng, Jingwen Leng, and Minyi Guo. 2025.       Jason Ramapuram, Federico Danieli, Eeshan Gunesh
  Clusterfusion: Expanding operator fusion scope for         Dhekane, Floris Weers, Dan Busbridge, Pierre Ablin,
  LLM inference via cluster-level collective primitive.      Tatiana Likhomanenko, Jagrit Digani, Zijin Gu, Ami-
  CoRR, abs/2508.18850.                                      tis Shidani, and Russell Webb. 2025. Theory, analy-
                                                             sis, and best practices for sigmoid self-attention. In
Meta PyTorch. 2025. KernelAgent: Autonomous GPU             The Thirteenth International Conference on Learning
 kernel generation via deep agents. https://github.          Representations, ICLR 2025, Singapore, April 24-28,
 com/meta-pytorch/KernelAgent.                               2025. OpenReview.net.

NVIDIA. 2021.   Nvidia a100 tensor core gpu               Morgane Rivière, Shreya Pathak, Pier Giuseppe Sessa,
 architecture.      https://www.nvidia.com/                and 1 others. 2024. Gemma 2: Improving open
 content/dam/en-zz/Solutions/Data-Center/                  language models at a practical size. arXiv preprint
 nvidia-ampere-architecture-whitepaper.                    arXiv:2408.00118.
 pdf.
                                                          Jay Shah, Ganesh Bikshandi, Ying Zhang, Vijay
NVIDIA. 2023. Nvidia h100 tensor core gpu architec-         Thakkar, Pradeep Ramani, and Tri Dao. 2024.
 ture. Technical report.                                    Flashattention-3: Fast and accurate attention with
                                                            asynchrony and low-precision. In Advances in Neu-
NVIDIA. 2025a. CUDA Templates for Linear Al-                ral Information Processing Systems 38: Annual Con-
 gebra Subroutines. https://github.com/NVIDIA/              ference on Neural Information Processing Systems
 cutlass.                                                   2024, NeurIPS 2024, Vancouver, BC, Canada, De-
                                                            cember 10 - 15, 2024.
NVIDIA. 2025b.     NVIDIA CUDA Compiler
 Driver NVCC. https://docs.nvidia.com/cuda/               Peter Shaw, Jakob Uszkoreit, and Ashish Vaswani. 2018.
 cuda-compiler-driver-nvcc/.                                Self-attention with relative position representations.
                                                            In Proceedings of the 2018 Conference of the North
Tesla NVIDIA. 2017. Nvidia tesla v100 gpu architec-         American Chapter of the Association for Computa-
  ture.                                                     tional Linguistics: Human Language Technologies,
                                                            NAACL-HLT, New Orleans, Louisiana, USA, June
OpenAI. 2025. Introducing gpt-5.                            1-6, 2018, Volume 2 (Short Papers), pages 464–468.
                                                            Association for Computational Linguistics.
Anne Ouyang, Simon Guo, Simran Arora, Alex L.
  Zhang, William Hu, Christopher Ré, and Azalia           Nisan Stiennon, Long Ouyang, Jeffrey Wu, Daniel M.
  Mirhoseini. 2025. Kernelbench: Can llms write             Ziegler, Ryan Lowe, Chelsea Voss, Alec Radford,
  efficient GPU kernels? In Forty-second Interna-           Dario Amodei, and Paul F. Christiano. 2020. Learn-
  tional Conference on Machine Learning, ICML 2025,         ing to summarize with human feedback. In Advances
  Vancouver, BC, Canada, July 13-19, 2025. OpenRe-          in Neural Information Processing Systems 33: An-
  view.net.                                                 nual Conference on Neural Information Processing
                                                            Systems 2020, NeurIPS 2020, December 6-12, 2020,
Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida,           virtual.
  Carroll L. Wainwright, Pamela Mishkin, Chong
  Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray,      Llama Team. 2024. The llama 3 herd of models. CoRR,
  John Schulman, Jacob Hilton, Fraser Kelton, Luke           abs/2407.21783.
  Miller, Maddie Simens, Amanda Askell, Peter Welin-
                                                          Qwen Team. 2025. Qwen3 technical report. CoRR,
  der, Paul F. Christiano, Jan Leike, and Ryan Lowe.
                                                           abs/2505.09388.
  2022. Training language models to follow instruc-
  tions with human feedback. In Advances in Neural        Hugo Touvron, Louis Martin, Kevin Stone, Peter Al-
  Information Processing Systems 35: Annual Confer-         bert, Amjad Almahairi, Yasmine Babaei, Nikolay
  ence on Neural Information Processing Systems 2022,       Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti
  NeurIPS 2022, New Orleans, LA, USA, November 28           Bhosale, Dan Bikel, Lukas Blecher, Cristian Canton-
  - December 9, 2022.                                       Ferrer, Moya Chen, Guillem Cucurull, David Esiobu,
                                                            Jude Fernandes, Jeremy Fu, Wenyin Fu, and 49 oth-
Kuntal Kumar Pal, Kazuaki Kashihara, Ujjwala Anan-          ers. 2023. Llama 2: Open foundation and fine-tuned
  theswaran, Kirby C. Kuznia, Siddhesh Jagtap, and          chat models. CoRR, abs/2307.09288.
  Chitta Baral. 2023. Exploring the limits of trans-
  fer learning with unified model in the cybersecurity    Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob
  domain. CoRR, abs/2302.10346.                             Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz
                                                            Kaiser, and Illia Polosukhin. 2017. Attention is all
Adam Paszke, Sam Gross, Francisco Massa, Adam               you need. In Advances in Neural Information Pro-
  Lerer, James Bradbury, Gregory Chanan, Trevor             cessing Systems 30: Annual Conference on Neural
  Killeen, Zeming Lin, Natalia Gimelshein, Luca             Information Processing Systems 2017, December 4-9,
  Antiga, and 1 others. 2019. Pytorch: An impera-           2017, Long Beach, CA, USA, pages 5998–6008.
  tive style, high-performance deep learning library.
  Advances in neural information processing systems,      Guoxia Wang, Jinle Zeng, Xiyuan Xiao, Siming Wu,
  32.                                                       Jiabin Yang, Lujing Zheng, Zeyu Chen, Jiang Bian,
  Dianhai Yu, and Haifeng Wang. 2025. Flashmask:            Yangjie Zhou, Mengtian Yang, Cong Guo, Jingwen
  Efficient and rich mask extension of flashattention. In     Leng, Yun Liang, Quan Chen, Minyi Guo, and Yuhao
  The Thirteenth International Conference on Learning         Zhu. 2021. Characterizing and demystifying the im-
  Representations, ICLR 2025, Singapore, April 24-28,         plicit convolution algorithm on commercial matrix-
  2025. OpenReview.net.                                       multiplication accelerators. In 2021 IEEE Inter-
                                                              national Symposium on Workload Characterization
Anjiang Wei, Tianran Sun, Yogesh Seenichamy, Hang             (IISWC), pages 214–225. IEEE.
  Song, Anne Ouyang, Azalia Mirhoseini, Ke Wang,
  and Alex Aiken. 2025. Astra: A multi-agent system         Yangjie Zhou, Honglin Zhu, Qian Qiu, Weihao Cui, Zi-
  for GPU kernel performance optimization. CoRR,              han Liu, Peng Chen, Mohamed Wahib, Cong Guo,
  abs/2509.07506.                                             Siyuan Feng, Jintao Meng, and 1 others. 2025b. A
                                                              sample-free compilation framework for efficient dy-
An Yang, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei            namic tensor computation. In Proceedings of the
  Huang, Haoyan Huang, Jiandong Jiang, Jianhong Tu,           International Conference for High Performance Com-
  Jianwei Zhang, Jingren Zhou, Junyang Lin, Kai Dang,         puting, Networking, Storage and Analysis, pages 167–
  Kexin Yang, Le Yu, Mei Li, Minmin Sun, Qin Zhu,             184.
  Rui Men, Tao He, and 9 others. 2025. Qwen2.5-1m
  technical report. CoRR, abs/2501.15383.                   Xinguo Zhu, Shaohui Peng, Jiaming Guo, Yunji Chen,
                                                              Qi Guo, Yuanbo Wen, Hang Qin, Ruizhi Chen,
Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak              Qirui Zhou, Ke Gao, and 1 others. 2025. Qimeng-
  Shafran, Karthik R. Narasimhan, and Yuan Cao. 2023.         kernel: Macro-thinking micro-coding paradigm for
  React: Synergizing reasoning and acting in language         llm-based high-performance gpu kernel generation.
  models. In The Eleventh International Conference            arXiv preprint arXiv:2511.20100.
  on Learning Representations, ICLR 2023, Kigali,
  Rwanda, May 1-5, 2023. OpenReview.net.

Zihao Ye, Lequn Chen, Ruihang Lai, Wuwei Lin, Yi-
  neng Zhang, Stephanie Wang, Tianqi Chen, Baris
  Kasikci, Vinod Grover, Arvind Krishnamurthy, and
  Luis Ceze. 2025. Flashinfer: Efficient and customiz-
  able attention engine for LLM inference serving.
  CoRR, abs/2501.01005.

Manzil Zaheer, Guru Guruganesh, Kumar Avinava
 Dubey, Joshua Ainslie, Chris Alberti, Santiago On-
 tañón, Philip Pham, Anirudh Ravula, Qifan Wang,
 Li Yang, and Amr Ahmed. 2020. Big bird: Trans-
 formers for longer sequences. In Advances in Neural
 Information Processing Systems 33: Annual Confer-
 ence on Neural Information Processing Systems 2020,
 NeurIPS 2020, December 6-12, 2020, virtual.

Huan Zhang, Wei Cheng, Yuhan Wu, and Wei Hu. 2024.
  A pair programming framework for code generation
  via multi-plan exploration and feedback-driven re-
  finement. In Proceedings of the 39th IEEE/ACM
  International Conference on Automated Software En-
  gineering, ASE ’24, page 1319–1331, New York, NY,
  USA. Association for Computing Machinery.

Zijian Zhang, Rong Wang, Shiyang Li, Yuebo Luo,
   Mingyi Hong, and Caiwen Ding. 2025. Cudaforge:
   An agent framework with hardware feedback for
   CUDA kernel optimization. CoRR, abs/2511.01884.

Qirui Zhou, Shaohui Peng, Weiqiang Xiong, Haixin
  Chen, Yuanbo Wen, Haochen Li, Ling Li, Qi Guo,
  Yongwei Zhao, Ke Gao, Ruizhi Chen, Yanjun Wu,
  Zhao Chen, and Yunji Chen. 2025a. Qimeng-
  attention: SOTA attention operator is generated by
  SOTA attention algorithm. In Findings of the As-
  sociation for Computational Linguistics, ACL 2025,
  Vienna, Austria, July 27 - August 1, 2025, pages 8491–
  8505. Association for Computational Linguistics.
A     Definitions of Attention Variants                  Global Sliding Window (Zaheer et al., 2020)
                                                         Tokens attend to neighbors within a window w
In this section, we provide the mathematical defini-
                                                         and specific global tokens (G).
tions and configurations for the attention variants
used in our evaluation. To encompass various mod-                     
ifications to the scoring logic and normalization,                    0
                                                                                     if |i − j| ≤ w
we formulate the general attention computation as:               Mij = 0              if i ∈ G or j ∈ G
                                                                      
                                                                       −∞             otherwise
                                                                      
                                 QK T
                                    
  O = Norm Mask Score √                      V (3)
                                    d
                                                         Share Question Mask (Ouyang et al., 2022)
where Q, K, V    ∈ RL×d . The components are de-         Commonly used in Reward Models and DPO, this
fined as follows:                                        mask allows multiple candidate responses (sets Ak )
• Score(·): Adjustments on raw attention scores          to attend to a single shared prompt (Q) to eliminate
  (e.g., relative bias, softcapping).                    redundant computation.
• Mask(·): Visibility constraints (e.g., causal, slid-        
   ing window).                                               
                                                              0          if i, j ∈ Q and j ≤ i
                                                              
                                                              
• Norm(·): Normalization functions (e.g., Soft-               
                                                              
                                                                         (Prompt self-attn)

   max, ReLU).                                           Mij = 0          if i ∈ Ak , j ∈ Q ∪ Ak and j ≤ i
Unless otherwise specified, for the mask M , Mij =
                                                              
                                                              
                                                              
                                                                         (Response → Prompt + Self)
0 indicates visible, and Mij = −∞ indicates
                                                              
                                                              
                                                               −∞         otherwise
                                                              
masked.

A.1    Score Modifications                               Causal Blockwise Mask (Bertsch et al., 2025)
Adjustments applied before√masking. In the for-          Isolates demonstration examples based on docu-
mulas below, Sij = qi kjT / d represents the raw         ment IDs (D) while granting the test query (starting
attention score.                                         at Lq ) visibility over the full context.

Relative Position Embeddings (Shaw et al., 2018)                    
                                                                    0            if j ≤ i and Di = Dj
Injects positional information by directly adding
                                                                    
                                                                    
                                                                    
                                                                                 (Demonstration isolation)
the relative index difference between the query (i)
                                                                    
                                                                    
and key (j) to the score.                                      Mij = 0            if j ≤ i and i ≥ Lq
                                                                    
                                                                    
                                                                    
                                                                                 (Test query visibility)
            Score(Sij ) = Sij + (i − j)                             
                                                                    
                                                                     −∞           otherwise
                                                                    
Softcap Attention (Rivière et al., 2024) Applies
a ‘tanh‘ cap with a scaling factor C to stabilize        A.3   Normalization Variants
logits.
                                                       Replacements for the standard Softmax function.
                                    Sij                  In these variants, normalization logic often uses
         Score(Sij ) = C · tanh
                                    C                    sequence length L for scaling.
A.2    Mask Variants
                                                         ReLU Attention (Dao et al., 2022) Applies
These variants define the visibility pattern Mij be-     ReLU activation and scales by sequence length.
tween query i and key j.
                                                                                       1
PrefixLM (Pal et al., 2023) Combines bi-                             Norm(S) =           ReLU(S)
directional attention for the prefix (length Lp ) and                                  L
causal attention for generated tokens.
                                                         Sigmoid Attention (Ramapuram et al., 2025)
                                                         Applies Sigmoid activation and scales by sequence
                  
                  
                   0       if j ≤ Lp
                  
                                                        length.
                  
                  
                           (Prefix visibility)

          Mij = 0           if Lp < j ≤ i                                            1
                  
                                                                   Norm(S) =          Sigmoid(S)
                  
                  
                           (Causal generation)                                      L
                  
                    −∞ otherwise
                  
                                             Llama2-7b                           Qwen2.5 72B                         Llama3.1 405B
                                           (q = 32, k = 32)                      (q = 64, k = 8)                     (q = 128, k = 8)

 Task Variant     Method             1k       2k         4k      8k       1k       2k         4k      8k       1k       2k         4k      8k
                  Torch            12.36    10.99    13.12     14.56    14.58    10.88     13.08    14.51    14.64    10.93    13.03     14.53
                  FlexAttention    77.09   110.44   131.67    142.77    99.82   121.96    137.52   146.68   107.89   128.63   140.49    148.55
 PrefixLM
                  Qimeng Attn      44.46    79.37   105.55    122.44    72.37    99.92    120.37   129.07    76.01   101.05   118.83    130.03
                  CuBridge         92.50   116.69   145.69    163.70   103.61   138.70    159.97   172.98   122.22   149.36   166.34    176.39
                  Torch            10.61     5.04     3.15      1.72    12.74     5.14      3.11     1.72    12.82     5.16     3.14      1.71
 Global Sliding   FlexAttention    56.96    85.24    87.67     88.87    92.52    92.09     92.32    92.78    96.40    94.23    92.47     91.40
 Window           Qimeng Attn      29.82    28.11    19.88     11.86    47.55    34.92     22.14    12.43    49.95    35.44    21.81     12.46
                  CuBridge         67.36    80.77    98.56    103.05    94.80   102.50    110.08   112.75   110.95   111.42   113.23    112.23
                  Torch             5.37     3.72     3.52      3.84     5.67     3.69      3.80     3.82     6.19     3.71     3.81      3.83
 Share            FlexAttention    29.86    84.32   108.10    128.78    64.44    92.66    112.75   130.71    76.01    95.16   116.07    131.24
 Question Mask    Qimeng Attn      12.27    14.36    14.54     14.43    15.77    16.61     15.60    14.88    18.54    16.90    15.65     14.88
                  CuBridge         39.81    88.62   122.31    147.61    73.96   107.88    135.07   154.98    90.18   116.09   138.86    157.26
                  Torch             4.85     3.67     3.89      4.00     6.31     3.72      3.86     3.97     6.33     3.75     3.89      3.98
 Causal           FlexAttention    31.77    62.96    87.36    110.96    59.41    79.85    100.77   120.91    70.30    87.45   108.47    126.37
 Blockwise Mask   Qimeng Attn      16.91    25.43    30.93     27.49    26.73    33.81     34.98    34.75    32.58    34.43    34.75     34.90
                  CuBridge         35.12    54.27    86.21    116.82    57.67    85.10    114.39   139.24    76.49   102.34   127.40    148.91
                  Torch            14.70    13.72    13.82     OOM      16.27    13.70     15.90    OOM      16.34    13.61    15.82     OOM
                  FlexAttention   114.85   144.68   149.75    157.08   131.96   142.19    152.02   154.73   134.26   147.91   152.28    154.91
 Relative Pos.
                  Qimeng Attn      71.05   112.10   130.56    138.79   105.91   126.59    139.74   142.81   109.04   127.91   135.62    143.22
                  CuBridge        105.80   151.28   162.47    172.53   137.92   154.96    166.21   169.39   146.46   161.65   167.97    170.50
                  Torch            31.16    36.59    33.63    OOM       32.35    36.44   38.28      39.98    33.79    37.38    39.73    OOM
                  FlexAttention                                                   no support
 ReLU Attn
                  Qimeng Attn      88.56   142.67   140.83    186.76   134.64   168.17 186.99      193.01   137.73   168.23   182.67    191.71
                  CuBridge        150.88   203.30   219.46    232.19   181.02   204.08 225.00      229.70   192.73   216.88   225.96    229.92
                  Torch            30.48    35.99    31.95    OOM       30.94    35.80   37.46      39.14    33.37    36.70    38.91    OOM
                  FlexAttention                                                   no support
 Sigmoid Attn
                  Qimeng Attn      45.05    62.92    66.33     75.16    54.36    71.15   74.58      77.51    64.54    71.05    74.98     76.87
                  CuBridge        134.56   183.33   196.13    207.63   165.47   185.36 201.14      205.59   173.81   195.33   201.92    205.62
 Combo            Torch             8.33     9.41      9.46   OOM        9.11     9.38    9.45       9.62     9.18     9.50      9.63   OOM
 (PrefixLM+       FlexAttention                                                   no support
 Softcap+         Qimeng Attn      17.78    26.12    29.39     32.60    25.46    29.37   31.83      33.44    26.90    29.98    32.13     33.39
 Sigmoid)         CuBridge         80.03   120.02   155.65    175.34   106.20   144.75 167.16      180.89   124.73   154.32   172.60    183.61


Table 4: Performance benchmark (TFLOPS) of attention variants across varying sequence lengths and real-world
model attention configurations on NVIDIA A100. (For each backbone the best result are marked in bold, and the
second best result are underlined.)


B     Detailed Experimental Results                                     Hand-optimized kernels for four built-in variants
                                                                        (Causal, Sliding Window, ALiBi, and Softcap). (2)
This section provides the complete numerical data                       Block-Sparse (BSR) Wrapper: A block-sparse
for the performance benchmarks discussed in Sec-                        mask API (BlockSparseAttentionWrapper) that
tion 4. Table 4 and Table 5 detail the TFLOPS                           enables sparse mask but does not support score
achieved by CuBridge and baselines across all                           modification or non-Softmax normalization. (3)
evaluated attention variants, sequence lengths, and                     JIT Templating: A Python JIT compilation
model attention configurations on NVIDIA A100                           API (gen_customize_batch_prefill_module)
and H100 GPUs, respectively.                                            that allows users to inject custom C++ attention
                                                                        logic while keeping the execution schedule fixed.
C     Comparison With Expert Libraries
                                                                           All experiments were conducted on an NVIDIA
We compare CuBridge with FlashInfer(v0.6.0) (Ye                         H100 GPU using the Llama 3.1-405B attention
et al., 2025) to evaluate its performance relative                      configuration (Q/KV heads: 128/8, Head dim:
to expert-level manual optimization. FlashInfer is                      128). We evaluate sequence lengths ranging from
widely recognized as a performance benchmark                            1k to 8k, with the batch size dynamically adjusted
due to its expert-optimized, hand-tuned kernels.                        to maintain a constant total of 16k tokens per batch.
                                                                           For each evaluated variant, we benchmark all
C.1     Experiment Setup                                                applicable FlashInfer interfaces and report the best
FlashInfer provides three distinct interfaces for im-                   FlashInfer performance (the maximum TFLOPS
plementing attention variants: (1) Native APIs:                         achieved among the available implementations) to
                                             Llama2-7b                           Qwen2.5 72B                         Llama3.1 405B
                                           (q = 32, k = 32)                      (q = 64, k = 8)                     (q = 128, k = 8)

 Task Variant     Method             1k       2k         4k      8k       1k       2k         4k      8k       1k       2k         4k      8k
                  Torch            27.22    19.72    25.48     29.61    28.40    19.99     25.67    29.77    29.03    20.06    25.67     29.66
                  FlexAttention   211.17   319.03   374.71    404.09   248.79   333.70    382.13   402.38   280.66   335.76   377.96    400.05
 PrefixLM
                  Qimeng Attn      81.07   126.08   175.60    215.75   113.24   163.79    207.47   232.61   124.68   173.70   214.14    238.76
                  CuBridge        304.35   414.05   577.03    551.73   304.35   486.19    599.14   615.26   383.51   548.49   532.16    597.61
                  Torch            23.65     9.25     6.00      3.40    24.70     9.36      6.05     3.41    25.23     9.40     6.05      3.41
 Global Sliding   FlexAttention   109.37   111.62   113.39    115.70   125.13   136.57    136.69   136.88   152.07   153.13   152.25    152.01
 Window           Qimeng Attn      65.43    53.43    38.77     24.62    86.25    66.80     44.85    26.45    92.97    70.25    46.23     26.85
                  CuBridge        137.80   176.88   182.44    151.90   197.82   214.90    211.71   202.74   239.29   249.16   199.39    214.46
                  Torch            11.28     6.66     7.32      7.61    11.76     6.74      7.37     7.62    12.02     6.76     7.38      7.63
 Share            FlexAttention   118.28   188.58   278.01    333.53   143.24   224.59    293.34   343.28   174.97   272.52   287.31    337.92
 Question Mask    Qimeng Attn      20.93    23.83    24.43     24.93    28.74    27.41     26.75    26.22    30.88    28.84    27.45     26.58
                  CuBridge        205.51   298.34   398.49    407.32   176.67   292.36    437.08   501.42   286.09   402.16   422.20    536.37
                  Torch            11.31     6.77     7.56      8.10    12.10     6.84      7.62     8.14    12.46     6.88     7.63      8.10
 Causal           FlexAttention   115.00   179.56   245.89    306.93   136.82   202.30    262.61   321.27   164.82   213.50   270.69    319.44
 Blockwise Mask   Qimeng Attn      37.26    47.03    57.88     66.07    53.20    62.07     69.33    71.82    58.53    66.18    71.22     72.95
                  CuBridge        157.27   177.58   340.00    388.39   161.75   277.11    441.31   498.62   240.40   366.02   418.17    530.28
                  Torch            31.85    26.07    32.06     35.61    32.75    26.27     32.13    35.70    33.45    26.50    32.52         –
                  FlexAttention   301.57   401.78   420.14    429.61   328.40   403.19    416.66   428.74   334.10   380.00   407.89    429.10
 Relative Pos.
                  Qimeng Attn     143.41   199.26   242.67    266.63   184.73   231.65    264.98   279.89   193.11   238.75   265.39    281.31
                  CuBridge        458.23   527.63   659.35    568.84   393.74   519.15    622.47   592.46   471.97   595.68   540.23    589.83
                  Torch            69.58    81.21    87.45     91.27    72.52    82.30   88.87      92.94    74.31    83.03    88.86     92.87
                  FlexAttention                                                   no support
 ReLU Attn
                  Qimeng Attn     182.51   280.51   364.83    424.78   253.49   346.74 415.00      443.19   268.86   357.82   418.74    451.79
                  CuBridge        509.02   605.51   639.66    764.12   521.33   632.60 622.52      637.52   593.97   615.01   604.02    648.54
                  Torch            69.14    80.58    86.69     90.35    71.92    81.76   88.04      92.04    73.71    82.32    88.00     91.84
                  FlexAttention                                                   no support
 Sigmoid Attn
                  Qimeng Attn      87.16   105.95   117.36    123.61   101.46   115.04 122.90      127.11   104.72   117.21   124.36    128.04
                  CuBridge        432.58   584.86   626.22    630.25   474.39   626.13 647.87      648.71   532.27   635.80   629.88    514.04
 Combo            Torch            18.19    19.58    19.87     20.25    18.60    19.76   20.03      20.42    18.94    19.84    20.01     20.40
 (PrefixLM+       FlexAttention                                                   no support
 Softcap+         Qimeng Attn      34.80    40.97    45.98     49.91    39.30    44.81   48.55      51.39    41.15    45.94    49.30     51.90
 Sigmoid)         CuBridge        273.45   411.90   533.12    572.94   321.80   490.90 546.66      524.12   380.78   532.47   536.65    555.81


Table 5: Performance benchmark (TFLOPS) of attention variants across varying sequence lengths and real-world
model attention configurations on NVIDIA H100. (For each backbone the best result are marked in bold, and the
second best result are underlined.)


ensure a rigorous comparison.                                            activations, and JIT allows semantic modification
                                                                         but fails to enable block-level sparse optimization,
C.2     Results and Discussion                                           resulting in unnecessary computation. And nei-
Table 6 presents the average throughput across se-                       ther BSR nor JIT currently supports H100-specific
quence lengths from 1k to 8k. The results indi-                          optimizations like warpgroup specialization, WG-
cate that CuBridge matches the performance of                            MMA, and TMA. In contrast, CuBridge recon-
native expert kernels (0.99×–1.22×) and signifi-                         structs kernels from a semantic specification via
cantly outperforms FlashInfer’s extension mecha-                         CuIR and re-derives the execution structure while
nisms on non-native variants (2.73×–5.59×).                              preserving expert orchestration, enabling schedule-
    For variants beyond FlashInfer’s native sup-                         level adaptation for each variant.
port, CuBridge achieves higher TFLOPS than the
                                                                         D      Case Study: GEMM-based Operators
best FlashInfer configuration at every evaluated
sequence length. The gap arises from how new                            To demonstrate the generality of CuBridge beyond
semantics are realized. FlashInfer extensions at-                       attention mechanisms, we conducted an additional
tach additional semantics onto a fixed execution                        case study on GEMM-based operators. While at-
template without restructuring the schedule for the                     tention was chosen as the primary focus due to its
modified computation. Specifically, the BSR mech-                       complexity, this study validates the broader appli-
anism introduces extra global memory mask reads.                        cability of our reference-driven paradigm.
Moreover, while BSR enables block-level skipping,                          Specifically, we use the open-source CUT-
it does not support score transforms or non-softmax                     LASS GEMM kernel as the source expert ref-
            Attention Variant           FI (Native)      FI (BSR)     FI (JIT)     CuBridge         vs. Best FI
            Causal Mask                   551.62          110.95         176.54        546.18            0.99×
            Sliding Window                276.12          78.92          38.27         282.60            1.02×
            Softcap                       383.90           N/A           91.20         466.85            1.22×
            ALiBi                         412.12           N/A           85.37         442.71            1.07×
            PrefixLM                       N/A            111.10         171.56        515.44            3.00×
            Global Sliding Window          N/A             82.61          68.28        225.25            2.73×
            Share Question Mask            N/A             99.28          11.89        411.71            4.15×
            Causal Blockwise Mask          N/A            125.00          35.67        388.72            3.11×
            Relative Position              N/A              N/A          163.61        549.43            3.36×
            ReLU Attention                 N/A              N/A          197.06        615.39            3.12×
            Sigmoid Attention              N/A              N/A          158.25        578.00            3.65×
            Combo                          N/A              N/A           89.76        501.43            5.59×

Table 6: Performance comparison (Avg TFLOPS) between CuBridge and FlashInfer (FI) on H100 GPU (Llama
3.1-405B configuration).

      Implementation     Metric             (4k,4k,4k)      (1k,1k,1k)      (4k,4k,1k)     (2k,4k,1k)        (4k,2k,1k)
      PyTorch            Latency (ms)         0.2495         0.0319           0.0802            0.0505           0.0498
                         TFLOPS               550.86         67.32            428.43            340.20           344.98
      CuBridge (Ours)    Latency (ms)         0.2425         0.0245           0.0580            0.0445           0.0384
                         TFLOPS               566.76         87.65            592.41            386.06           447.39

Table 7: Performance comparison between PyTorch and CuBridge for the GEMM+ReduceSum operator on H100
GPU. Shape are denoted as (M, N, K).


erence and apply CuBridge to generate a fused                 Within this landscape, the support for diverse atten-
GEMM+ReduceSum variant. This transformation                   tion variants has emerged as a particularly signifi-
involves cross-thread accumulation and non-trivial            cant challenge, as it requires balancing algorithmic
epilogue modification.                                        flexibility with the need for hardware-specific op-
   Table 7 summarizes the results on H100 GPU.                timization. Current systems for attention variants
Across multiple common shapes, the generated                  mainly fall into two categories.
GEMM+ReduceSum kernel consistently outper-                       The first category is Expert Libraries. Libraries
forms PyTorch, achieving 1.03×–1.30× speedups.                like FlashAttention (Dao et al., 2022) achieve state-
The performance improvement arises from ker-                  of-the-art performance through heavy manual tun-
nel fusion: while PyTorch executes GEMM and                   ing. However, they lack flexibility and only support
Reduce-Sum as separate kernels, requiring inter-              a few variants (e.g., ALiBi, sliding window, causal
mediate results to be written to and read from                mask, softcap). Similarly, FlashInfer (Ye et al.,
global memory. In contrast, CuBridge directly                 2025) applies these techniques to speed up LLM in-
modifies the expert reference kernel, enabling ex-            ference. FlashMask (Wang et al., 2025) introduces
ecution within a single fused kernel and eliminat-            a structural sparse mask representation, allowing it
ing intermediate global memory round-trips. This              to support a wider range of mask variants.
case study demonstrates that CuBridge’s reference-
driven transformation mechanism and CuIR ab-                     The second category is Compiler-based Ap-
straction generalize to other core operator families.         proaches (e.g., FlexAttention (Guessous et al.,
                                                              2024), AttentionEngine (Chen et al., 2025a)).
E     Related Work                                            These methods improve programmability through
                                                              template-based design. Specifically, FlexAttention
E.1    Current support for attention variants                 allows users to write simple PyTorch functions
The surge in large-scale models has driven exten-             for score and mask computations. It then com-
sive GPU research, ranging from high-performance              piles these functions and injects them into fixed
algorithms (Liu et al., 2025; Luo et al., 2025;               slots within a pre-written attention template. While
Zhou et al., 2021) and software stacks (Huang                 this offers some flexibility, it suffers from struc-
et al., 2026; Zhou et al., 2025b) to innovative hard-         tural rigidity. Users cannot change logic outside
ware utilization (Guo et al., 2020; Hu et al., 2026).         these designated slots (e.g., they cannot replace
the Softmax operator), which limits the types of       low-level CUDA details and use lift–transfer–lower
algorithms it can support. Moreover, the fixed ex-     workflow. This enables the model to understand
ecution pipeline prevents adaptation to hardware-      and modify the kernel’s logical structure and data
specific opportunities like overlapping Tensor Core    flow, ensuring that complex orchestration patterns
and CUDA Core workloads. As a result, these            are correctly handled.
systems often still lag behind hand-tuned expert
libraries in performance.                              F       Lifter Agent System Prompt

E.2   LLM for CUDA Code Generation                     The complete system prompt of Lifter Module is
                                                       presented below.
Recently, with the continuous improvement of
                                                           Lifter Agent System Prompt
LLMs, there is growing interest in using them to au-
tomatically generate GPU kernels. However, SOTA         # Role
                                                        You are an expert CUDA System Engineer specializing in Semantic
models perform poorly on benchmarks like Kernel-        Lifting. Your goal is to transform low-level, expert-optimized CUDA
                                                        kernels into CuIR, a Pythonic IR designed to capture Execution
Bench (Ouyang et al., 2025) and TritonBench (Li         Orchestration while abstracting away implementation complexity.
et al., 2025a). This stems from the complexity
of parallel programming models (e.g., managing          # Task: The Semantic Lifting Process
                                                        You must process the CUDA kernel step-by-step to ensure semantic
hierarchical execution units and memory system)         reliability:
                                                        1. Step 1: Low-level Annotation. Begin by commenting all ptx usages
combined with the extreme rarity of high-quality            and CuTe APIs. You must refer to the technical document to explain
                                                            the exact hardware behavior of each instruction.
GPU code in pre-training corpora (less than 0.1%        2. Step 2: Worker Identification. Analyze the kernel’s parallel
in The Stack (Kocetkov et al., 2023)). Existing             hierarchy to identify distinct execution units (e.g., warp, warpgroup,
                                                            threadblock) and their code snippet.
research generally falls into two categories.           3. Step 3: CuIR construction. Before writing any CuIR, reason about
                                                            how these workers are synchronized. Identify the specific barriers and
   Training-based Methods. These approaches                 arrival counts that manage the execution pipeline. Based on the
try to improve the model’s mastery of CUDA                  analysis above, map the logic into CuIR primitives. You must ensure
                                                            that the lifted representation strictly preserves the original
code through additional training. Methods like              asynchronous dataflow and synchronization logic.
Kevin (Baronio et al., 2025) and CUDA-L1 (Li            # CuIR Specification
et al., 2025b) apply reinforcement learning to this     ## 1. Runtime System
                                                        The runtime defines the virtual execution environment for the IR.
domain, using generated samples for training to         class KernelBase Represents the context of a Single Thread Block.
help with the lack of data. Additionally, QiMeng-            • __init__(self, *args): Initialize primitives and allocate Shared
                                                               Memory here.
MuPa (Ke et al., 2025) uses a mutual supervision               Critical: You MUST calculate self.gridDim (e.g., M // BM) based
framework where a code generator and a test case               on input shapes to configure the simulator.
                                                             • self.blockIdx: A Dim3 object mimicking CUDA’s blockIdx.
generator improve together. However, these meth-             • bind(self, func, role_name): Control Primitive. Maps a
ods require high training costs to modify the un-              Python method to a virtual hardware worker.
                                                             • commit(self): Control Primitive. Triggers the parallel execution of
derlying model. Our framework is orthogonal to                 bound workers.
training-based approaches and can be used in con-          ## 2. CuIR Primitives
                                                           ### Memory & Data Movement
junction with them.                                        • alloc(tile_shape, hierarchy, dtype):
   Workflow-based Methods. This category treats              Allocates a memory tile on the specified hierarchy (e.g., "shared",
                                                             "register").
the LLM as a modular component within a sys-                 Returns: A Tensor-like object that supports direct indexing, slicing, and
                                                             standard PyTorch math operations.
tem and focuses on the design of systemic work-
                                                           • copy_async(dst, src, barrier, instruction):
flows to complete complex tasks. (Wei et al., 2025;          Performs an asynchronous copy from src to dst.
Chen et al.). Some use execution-guided feedback             – The barrier will be updated when transaction completion.
                                                             – instruction: (String) Annotation tag (e.g., "cp.async", "tma").
pipelines (Chen et al., 2025b), while others employ            Purely for Semantic Lifting info; does not affect simulation logic.
multi-agent frameworks (such as Astra (Wei et al.,         • copy(dst, src, instruction):
                                                             Performs a synchronous copy from src to dst.
2025), CUDA-LLM (Chen et al., 2025b), and Cud-
                                                             – instruction: (String) Annotation tag (e.g., "ldmatrix", "stsw").
aForge (Zhang et al., 2025)) that separate planning,           Purely for Semantic Lifting info.
generation, and debugging into distinct roles. Sim-        ### Compute
ilar pipelines have also been explored for Triton          • gemm_async(A, B, instruction):
                                                             Performs an asynchronous matrix multiplication (A @ B).
kernel generation (Meta PyTorch, 2025; Zhu et al.,           – Synchronization: Execution logic assumes results are not
2025). However, these frameworks typically treat               immediately available; completion MUST be managed via
                                                               wait_group primitives.
code as plain text, lacking insight into the complex         – instruction: (String) Annotation tag (e.g., "wgmma.mma_async").
execution orchestration required for performance.              Purely for Semantic Lifting info.

In contrast, CuBridge uses a structured IR to make         • gemm(A, B, instruction):
                                                             Performs a synchronous matrix multiplication (A @ B).
execution orchestration explicit while abstracting
   – instruction: (String) Annotation tag (e.g., "mma.sync"). Purely             G      IR Transfer Implementation Details
     for Semantic Lifting info.
 • CUDA Core Operations:                                                         IR Transfer is implemented as an iterative
   For standard ALU/SFU operations (Add, Mul, Exp, etc.), use native
   PyTorch operators directly on the Tensors (e.g., C = A + B,                   transformation-and-validation loop. Given an Ori-
   torch.exp(x)).                                                                gin CuIR, an Origin PyTorch specification, and
 ### Synchronization
 Models the mbarrier hardware primitive. It tracks two distinct goals:
                                                                                 a Target PyTorch specification, CuBridge gener-
 Thread Arrivals (persistent) and Transaction Bytes (transient).                 ates a Target CuIR under explicit transformation
 • barrier.init(expected_threads):
   Sets the persistent base_goal (number of participating threads).              constraints, validates it against the Target PyTorch
   – Call this once in __init__ or before the main loop.                         reference, and iteratively refines it if needed. The
 • barrier.arrive_expect_tx(bytes_count):                                        core logic is defined in the following procedure:
   1. Signals thread arrival (increments current_threads).                          The generation stage is LLM-driven and explic-
   2. Increases the transaction goal by bytes_count (increments
      tx_goal).                                                                  itly rule-constrained. Similar to the lifting stage, IR
   Use this immediately before issuing a copy_async (TMA) operation.             Transfer uses a structured chain-of-thought prompt
 • barrier.arrive():                                                             with ordered reasoning steps. The LLM is in-
   – Signals thread arrival (increments current_threads) without
     modifying transaction expectations.                                         structed to: (1) identify the semantic delta between
 • barrier.wait(parity):                                                         the Origin and Target PyTorch specifications, (2)
   – Blocks the thread until the barrier completes the phase associated          localize the affected region in the Origin CuIR,
     with parity.
                                                                                 and (3) apply predefined transformation rules to
 # Lifting Rule                                                                  construct the Target CuIR.
 ### 1. Worker-Logic Disentanglement
 • Role Identification: Analyze control flow (e.g., if warp_group_idx
                                                                                    The explicit rule taxonomy, as detailed in Ta-
   == 0) to distinguish roles.                                                   ble 8, serves two purposes: it constrains modifi-
 • Logic Merging: If multiple hardware units perform the same logical
   task, merge them into a single logic method.
                                                                                 cations to prevent unintended disruption of expert
 ### 2. Logical Tile Allocation (Memory)                                         scheduling structure, and it makes the transfer pro-
 • Shared Memory: Allocate in __init__ using                                     cedure compositional and reproducible rather than
   alloc(scope="shared").
 • Register File: When allocating accumulators, derive the shape from the        free-form code synthesis. After generation, verifi-
   Logical Tile View (e.g., [BM, BN]) rather than the fragmented
   thread-level view.
                                                                                 cation is performed via the CuIR runtime before
 ### 3. Preservation of Execution Orchestration (Crucial)                        CUDA reconstruction. Failed cases trigger struc-
 • Instruction Scheduling: You MUST preserve the exact relative order of         tured diagnostics and bounded refinement.
   Memory, Compute, and Barriers.
 • Latency Hiding: If the CUDA source interleaves computation with
   pipeline stages, you must replicate this sequence 1:1. Do not reorder         Algorithm: IR Transfer Loop
   instructions.
                                                                                  target_cuir = GenerateTargetCuIR(origin_cuir,
 # Example                                                                            origin_pytorch, target_pytorch)
 ...                                                                              is_valid, diagnostics = VerifyAgainstReference(
                                                                                      target_cuir, reference=target_pytorch)
 # Output Format (Strict)
 Your output MUST be a single executable Python code block.
 1. Define one Python class inheriting from KernelBase.                           while not is_valid and iteration <
 2. Implement __init__, run, and logic methods.                                        max_iterations:
 3. Do NOT include explanations or markdown text outside the code                     target_cuir = RefineCuIR(target_cuir,
    block.
                                                                                           diagnostics)
                                                                                      is_valid, diagnostics =
                                                                                           VerifyAgainstReference(target_cuir,
                                                                                           reference=target_pytorch)
                                                                                      iteration += 1




  Rule         Transformation Category                                    Core Action
  R1           Iteration domain transformation                            Modify loop bounds/iteration space while preserving tiling.
  R2           Execution structure preservation                           Retain async pipeline and scheduling patterns.
  R3           Computation injection or modification                      Insert or adapt intermediate computations.
  R4           Reduction or normalization replacement                     Modify accumulation or normalization strategy.
  R5           Data dependency extension                                  Introduce additional inputs or memory staging.
  R6           Auxiliary structure adaptation                             Adjust code logic to match control-flow changes.
  R7           Unaffected region preservation                             Preserve IR regions not implicated by semantic delta.

Table 8: Taxonomy of IR Transformation Rules. These rules constrain the LLM to preserve the expert execution
structure while adapting to new attention semantics.
