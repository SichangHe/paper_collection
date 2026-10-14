                                                  Ave: Guiding Agentic GPU Optimization Using
                                                              Data-Flow Invariants
                                                      Haohui Maiˇ ( , 1 Xiaoyan Guo4 Xiangyun Dingˇ ( , 5 Daifeng Li1 Qiuchu Yu4
                                                                            “                                                   “

                                                  Chenzhun Guo4 Cong Wang2 Jiacheng Zhao4 Christos Kozyrakis3 Binhang Yuan1
                                                                                HKUST1     Tsinghua University2         Stanford University3      UCAS4     UC Riverside5
                                                                        “
                                                     CausalFlow Inc.ˇ (

                                         Abstract                                                                      three attempts for 100% of Level 1 and 88% of Level 2 prob-
                                         LLM coding agents can generate correct GPU kernels, yet                       lems. Ave is open source at https://github.com/causalflow-
                                         their performance still lags behind expert libraries. Achiev-                 ai/avelang.
                                         ing peak GPU throughput requires coordinating low-level                       CCS Concepts: • Software and its engineering → Com-
arXiv:2604.18616v2 [cs.DC] 14 Sep 2026




                                         transformations such as shared-memory staging, software                       pilers; Automated static analysis; • Computing method-
                                         pipelining, and instruction scheduling. Unit tests and per-                   ologies → Artificial intelligence.
                                         formance profiles provide only sparse end-to-end feedback,
                                         leaving agents unable to localize violations of the global                    Keywords: GPU kernel optimization, LLM coding agents,
                                         constraints that these transformations must preserve.                         data-flow invariants, static analysis
                                            We present Ave, an agentic framework that uses data-flow                   ACM Reference Format:
                                         invariants as compile-time guardrails for kernel optimiza-                    Haohui Mai, Xiaoyan Guo, Xiangyun Ding, Daifeng Li, Qiuchu Yu,
                                         tion. These invariants specify relationships among data val-                  Chenzhun Guo, Cong Wang, Jiacheng Zhao, Christos Kozyrakis,
                                         ues that must hold throughout execution. Ave’s tile-based                     and Binhang Yuan. 2026. Ave: Guiding Agentic GPU Optimization
                                         Pythonic DSL exposes hardware instructions and compiler                       Using Data-Flow Invariants. In Symposium on Operating Systems
                                         policies while abstracting complex memory layout encodings                    Principles (SOSP ’26), September 29–October 2, 2026, Prague, Czech
                                         as tiles. Tag functions assign symbolic labels derived from                   Republic. ACM, New York, NY, USA, 15 pages. https://doi.org/10.1
                                                                                                                       145/3830418.3843902
                                         selected logical coordinates and expressions. The compiler
                                         propagates these labels through data and control flow, and
                                         tag assertions enforce required relationships among them                      1    Introduction
                                         at use sites. The compiler checks these assertions with a                     Modern large language models (LLMs) [55] increasingly ex-
                                         tractable, flow-sensitive, path-insensitive analysis backed                   hibit broad, human-level capabilities and may be approach-
                                         by an SMT solver, returning concrete assignments that wit-                    ing a tipping point for recursive self-improvement. GPU
                                         ness abstract violations and guide repairs with no runtime                    kernel optimization lets LLMs improve software governing
                                         overhead. An in-context reinforcement learning (ICRL) plan-                   their own execution efficiency [14, 16].
                                         ner proposes optimizations from a curated knowledge base.                        LLMs can now generate functionally correct kernels for
                                         A lowering agent implements them and instantiates their                       diverse workloads [6, 9, 18, 25, 26, 32, 43, 56, 64, 70, 78],
                                         invariants.                                                                   but their performance remains unsuitable for production.
                                            We evaluate Ave on AMD MI300X across GEMM, flash                           With GPT-5.6 Sol on AMD MI300X, existing agentic har-
                                         attention, and MoE, which together account for up to 90% of                   ness systems produce GEMM kernels that are 1.8–14.3×
                                         GPU time in LLM inference. With GPT-5.6 Sol, its optimized                    slower than hipBLASLt [4], AMD’s state-of-the-art GEMM
                                         kernels achieve 89–99% of the effective throughput of state-                  library. Closing this gap requires more than functional cor-
                                         of-the-art hand-optimized libraries and improve geometric-                    rectness: agents must coordinate optimizations across the
                                         mean throughput by 1.62–1176× over uncontaminated agen-                       software-hardware stack while preserving program seman-
                                         tic baselines. On 200 KernelBench tasks, with GPT-5.6 Sol and                 tics. For example, a high-performance GEMM implementa-
                                         in-context DSL examples, Ave produces valid kernels within                    tion combines matrix cores [45], software pipelining [38],
                                                                                                                       memory-hierarchy optimizations [42], and instruction sched-
                                                                                                                       uling [34], many of which require low-level assembly. Kernel-
                                                                                                                       design agents [30, 72] combine expert knowledge bases with
                                                                                                                       powerful models and iterate using unit-test outcomes and
                                                                                                                       performance profiles, yet they struggle to apply performance-
                                         This work is licensed under a Creative Commons Attribution 4.0 Interna-       critical, low-level optimizations for two reasons. First, vali-
                                         tional License.
                                         SOSP ’26, Prague, Czech Republic
                                                                                                                       dating such transformations requires reasoning about non-
                                         © 2026 Copyright held by the owner/author(s).                                 trivial properties, including memory aliasing [60] and data
                                         ACM ISBN 979-8-4007-2585-2/26/09                                              races [7], at the assembly level. This reasoning consumes
                                         https://doi.org/10.1145/3830418.3843902                                       many tokens and expands the context, ultimately degrading
                                                                                                                   1
model performance [44]. Second, unit tests and performance             elements and propagate them through control and data flow.
profiling only provide sparse, end-to-end feedback. These              Tag assertions require tags at a use site either to match or to
signals reveal that a kernel is incorrect or slow but do not           differ. Conformity assertions encode alignment constraints,
identify the responsible transformation or ordering.                   such as requiring paired matrix-multiplication operands to
   One alternative is to trade optimization control for com-           carry compatible tags. Non-conformity assertions encode
piler automation by targeting a higher-level language such             separation constraints, such as ensuring that concurrent pro-
as Triton [66], which delegates many low-level decisions to a          ducers do not overwrite the same shared-memory region.
tensor compiler [14, 29, 46, 66, 69, 71, 80]. In our evaluation,          Second, Ave uses static analysis to enforce these invariants
the ROCm Triton baseline narrows the gap to approximately              entirely at compile time and turn failures into actionable feed-
2×. However, this baseline does not expose fine-grained con-           back for the LLM coding agent. The tags are purely symbolic
trol over instruction scheduling or wavefront specialization,          and never materialized at runtime. The Ave compiler tracks
preventing agents from closing the remaining gap.                      their propagation using the abstract interpretation [17] over
   In this paper, we present Ave, an agentic framework for             a layout algebra [52] and leverages an SMT solver [20] to
automating complex, multilevel GPU kernel optimizations.               solve the resulting integer constraints. To remain tractable
Ave uses data-flow invariants to validate transformations and          for heavily optimized kernels, the analysis is path-insensitive.
provide guardrails as LLMs apply them. These compile-time              When an assertion fails, the compiler reports a concrete as-
assertions specify relationships among data values that must           signment witnessing the violating abstract state, including
hold throughout kernel execution, even across multiple lay-            the thread ID, data element, and program point, thereby
ers of optimization. Data-flow invariants are an established           guiding the agent’s next revision.
concept in information-flow security [50, 73, 75]. Ave adapts             Third, Ave uses ICRL [26, 49] to adapt a planner that pro-
them to GPU kernel optimization. For example, a GEMM                   poses optimizations and their corresponding invariant tem-
kernel tiles and stages matrices A and B in shared memory              plates. The planner observes the kernel implementation, the
before passing them to hardware matrix fused multiply-add              compile-time invariant violations, and the runtime profiles,
(MFMA) instructions, which expect the operands in a partic-            retrieves applicable optimizations from a persistent knowl-
ular swizzled layout. A data-flow invariant can assert that            edge base, and proposes optimization instructions with their
these instructions always receive correctly paired elements            templates (Figure 1). A lowering agent binds the selected
of A and B, regardless of the transformations applied. By              instructions to code and instantiates the templates as tag
making such requirements explicit, Ave gives the agent con-            functions and assertions. Each invariant specifies a property
crete correctness constraints for intrusive transformations            that its transformation must preserve. Ave makes planner
such as software pipelining and data-layout reorganization.            prompts learnable, uses invariant violations and runtime per-
   Three challenges arise in realizing this approach. First,           formance as reward signals, and applies text gradients [74]
the invariant language must express global properties con-             to improve subsequent optimization plans.
cisely in one place while producing concrete violation re-                These three ideas reinforce one another. Tag functions
ports that guide repairs, such as the thread holding a mis-            alone provide only declarative specifications. Static analysis
matched element and the program point where the mismatch               can check properties but cannot repair violations, and an
occurs. Second, enforcing invariants must incur zero runtime           ICRL agent alone lacks the structured feedback needed to
overhead. Optimized kernels saturate hardware units, tailor            navigate a vast optimization space. Together, they form a
access patterns to the memory hierarchy, and depend on                 closed loop: tag functions express correctness properties,
precise instruction schedules. The analysis must therefore             static analysis checks them at compile time, and concrete
operate entirely at compile time across tiling, staging, and           assignments witnessing abstract violations provide dense
layout transformations, without perturbing the generated               feedback. This feedback lets the agent reason about abstract
code. Third, application-specific invariant templates must be          correctness properties instead of repairing implementations
instantiated automatically. The assignment of A and B tiles            through trial and error. Ave thereby applies complex, multi-
to wavefronts, their staging in shared memory, and their               level optimizations more reliably while reducing the effort
eventual consumption by MFMA instructions vary across                  required to preserve correctness. Discovering new algorith-
GEMM kernels, so Ave must instantiate the corresponding                mic optimizations [30] and fully verifying implementation
invariants without per-kernel human intervention.                      correctness [7, 11] remain outside its scope.
   Ave combines three ideas: tag functions, static analysis,              We evaluate Ave on three production-level kernel families
and an in-context reinforcement learning (ICRL) agent.                 using GPT-5.6 Sol, including general matrix multiplications
   First, Ave introduces tag functions and tag assertions, a           (GEMM) [4], flash attention [19], and mixture-of-experts
concise language for expressing data-flow invariants. It gen-          (MoE) feed-forward networks [62]. On AMD MI300X, these
erates and optimizes kernels in a tile-based, Pythonic DSL             kernels account for up to 90% of GPU execution time dur-
inspired by CuTe [52] and TileLang [69]. Tag functions at-             ing LLM inference [27]. Kernels optimized by Ave achieve
tach symbolic values, such as logical coordinates, to tensor
                                                                   2
89–99% of the effective throughput of state-of-the-art hand-           fused multiply-add instructions, and Vector Accumulation
optimized libraries [1, 4]. Across the evaluated workloads,            Registers (AGPRs) that expand the available register pool.
Ave improves geometric-mean throughput by 1.62–1176×                   These features require explicit compiler support.
over uncontaminated agentic baselines. For flash attention,               Achieving peak performance on a GPU requires exploit-
Ave outperforms KernelFalcon [70] by 3×. Beyond these ker-             ing this architecture along three axes. First, kernels balance
nel families, Ave can also generalize to KernelBench [56]:             per-workgroup register and shared-memory use against oc-
with in-context DSL examples, it solves all 100 Level 1 and            cupancy. Second, MI300X’s arithmetic-to-bandwidth ratio
88 Level 2 tasks within three attempts.                                of ∼250 demands vectorized accesses, shared-memory reuse,
  Concretely, we make the following contributions:                     and software pipelining to overlap computation with trans-
    • We introduce data-flow invariants for agentic GPU                fers. Third, instruction scheduling and register allocation
      kernel optimization, improving the reliability and per-          matter at the assembly level: poor schedules stall in-order
      formance of generated kernels.                                   pipelines, while excessive register use causes spills [58].
    • We design a tile-based DSL with tag functions and                Optimizing Flash Attention on MI300X. Turning flash atten-
      assertions, together with a static analysis that validates       tion into a kernel reaching peak throughput requires a cas-
      invariants at compile time with zero runtime overhead.           cade of hardware-specific optimizations. Figure 1 shows a
    • We build an agentic optimization harness with an ICRL            simplified Ave DSL implementation with 512 threads, 𝑑=128,
      planner that proposes optimization candidates, a se-             𝐵𝑟 =256, and 𝐵𝑐 =64, embodying these optimizations. The
      lector that constructs plans, and a lowering agent that          pseudocode focuses on layouts and operand pairing, eliding
      implements them and instantiates their invariants in             the full pipeline schedule and wavefront-group control flow.
      the Ave DSL.                                                        The kernel executes two GEMMs S = QK𝑇 and O =
    • We evaluate Ave on GEMM, flash attention, MoE, and               PV on matrix cores via MFMA instructions. Each 32×32×8
      KernelBench, demonstrating substantial gains over                MFMA expects column-major input operands A and B and
      existing agentic baselines.                                      accumulator C in hardware-specific swizzled layouts. Each
                                                                       thread contributes 4 elements from each input. Adapting
2   Motivating Example                                                 row-major attention to these layouts requires operand re-
   We use flash attention [19] on the AMD MI300X GPU as                ordering and transposition. Reaching peak throughput also
a running example to illustrate why high-performance ker-              requires shared-memory reuse, software pipelining to over-
nel development demands tightly coupled algorithmic and                lap global memory loads with MFMA computation, partition-
hardware-level reasoning. Together with GEMM and MoE                   ing data-flow across disjoint wavefront groups, and careful
layers, attention accounts for up to 90% of GPU execution              instruction scheduling to keep the in-order cores busy with-
time in LLM serving [27], making its optimization critical.            out pipeline stalls while staying within the register budget
   The standard attention mechanism operates on three input            to avoid spills. For example, AITER’s handwritten assembly
matrices Q, K, V ∈ R𝑁 ×𝑑 , where 𝑁 is the sequence length              kernel uses 11 pipeline stages across two wavefront groups.
and 𝑑 is the head dimension. It computes S = QK𝑇 , applies             Section 4 details how the DSL expresses these optimizations.
softmax row-wise to obtain P = softmax(S), and produces                   The data shuffling and layout transformations are error-
O = PV. A naïve implementation materializes the 𝑁 × 𝑁                  prone: mismatches between expected and actual data layouts
score matrix S, requiring (𝑁 2 ) memory, prohibitive for              cause correctness bugs. Ensuring correctness of these global
long contexts (e.g., 𝑁 = 256K). Flash attention avoids this            properties is time-consuming when drafting and debugging
by tiling: it loads a 𝐵𝑟 × 𝑑 block of Q into registers, then           optimizations. Ave introduces tag functions and data-flow
streams through K and V in 𝐵𝑐 × 𝑑 blocks staged in shared              invariants, expressed as assert statements in Figure 1, to
memory, accumulating into O via online softmax [48] to                 check that values are correctly paired at each use site. Sec-
achieve (𝑁 ) memory. The tile sizes 𝐵𝑟 and 𝐵𝑐 are chosen              tion 4 describes these mechanisms in detail.
so the working set fits in registers and shared memory.
                                                                       3   Overview of Ave
GPU Architecture. Ave targets the AMD MI300X GPU, which
implements the CDNA3 architecture [2]. Like other mod-                 Ave combines three components to generate and optimize
ern GPUs, the MI300X follows a Single Instruction, Multiple            GPU kernels: (i) a tile-based, Pythonic DSL with tag functions
Threads (SIMT) design. Each Compute Unit (CU) contains                 and assertions (§4), (ii) compile-time invariant analysis with
in-order execution cores, a shared register file, and Local            zero runtime cost (§5), and (iii) an agentic harness guided
Data Share (LDS), or shared memory, and is analogous to                by invariant feedback (§6). The implementation primarily
an NVIDIA streaming multiprocessor. A 64-thread wave-                  targets AMD MI300X and generalizes to AMD MI350X and
front (AMD’s warp) executes in lockstep on a 16-lane vec-              NVIDIA H200 (§9.3).
tor unit. Several wavefronts form a workgroup sharing LDS.             Ave DSL. The Pythonic, tile-based DSL resembles CuTe and
MI300X also provides MFMA matrix cores, 2-wide vector                  Triton and adds tag functions and assertions for data-flow
                                                                   3
1 def attn(d:const,gqa:const,Q:Tensor((sq,hq ,d),bf16),K:Tensor((sq,hkv ,d),bf16),                 Kernel description                                      HW specifications
2    V:Tensor((sq,hkv ,d),bf16),O:Tensor((sq,hq ,d),bf16), . . .):
3    # Assign tags to QKV
4    TQ ,TK ,TV = Q[sq,hq ,d]→(hq /gqa,d), K[sq,hkv ,d]→(hkv ,d), V[sq,hkv ,d]→(hkv ,sq)                                                     Initial kernel
5    # Vectorize and tile memory access for MFMA
6    idxq ,idxh ,tid = blockIdx.x, blockIdx.y, threadIdx.x
                                                                                                                                      Learnable Planner




                                                                                                                                                                               Knowledge Base
7    wid,wtid,nw,rO = tid/64,tid%64,(wid&2)*2+wid/4*2+wid%2,make_local((4,),u256)
                                                                                                                                          (via ICRL)
8    gQ,rQ = Q.view((sq/Br,Br,hq ,d/8),u128), make_local((8,),u128)




                                                                                                   Compile-time & runtime feedback
9    gK,sK = K.view((sq/Bc,Bc,hkv ,d/8),u128), make_shared((512,2),u128)                                                                            Optimization
10   gV,sV = V.view((sq/Bc,Bc,hkv ,d/2),u32), make_shared((2,2,4,4,32),u64)                                                                          candidates
11   sK,
     e sVe = sK.view((2,32,8,2),u128), sV.view((2,2,4,4,16),u128)
                                                                                                                                     Optimization Selector
12   rS,rS,tU
         e      = make_local((2,),u256),rS.view((4,8),bf16),make_local((2,4,),u32)
13   ∀𝑖 ∈ [0, 8): rQ[i] = gQ[idxq ,wid*32+wtid%32,idxh ,i*2+wtid/32]                                                                             Instructions +
14   for i in range(sq/Bc):                                                                                                                   invariant templates
15      for j in range(2):




                                                                                                                                                                           Runtime Libraries
                                                                                                                                       Lowering Agent
16        sK[tid,j] = gK[i,j*32+tid/16,idxh /gqa,tid%16]
17        # Vectorize VT via bit rearrangements
                                                                                                                                                      Ave DSL
18       ∀𝑘 ∈ [0, 4): tU[j,k] = gV[i,j*32+wid*4+k,idxh /gqa,wtid]
19                                                         3 (tU[j,k] )
             sV[0,j,wtid/16,nw%4,(wtid%16)*2+nw/4] = concat𝑘=0                                                                       Invariant Validation
                                                                     lo
                                                                                                                                      Testing & Profiling
20                                                         3 (tU[j,k] )
             sV[1,j,wtid/16,nw%4,(wtid%16)*2+nw/4] = concat𝑘=0       hi                                                                              Agentic Harness
21     syncthreads()
22     T e = rS[x,y]→(
                       idxh
                            ,i*Bc+ x *32+x%2*16+ y *8+ wtid *4+y%4)                                                                        Optimized kernel
                                    2             4     32
             e
        rS                gqa
23     for j in range(16):
24         tK,tQ = sK[j/8,wtid%32,j%8,wtid/32], rQ[j%8]                                    Global memory
                    e
25         tK,
           e tQe = tK.view((8,),bf16), tQ.view((8,),bf16)                                         d                                            lo




                                                                                                                                                                                                memory
                                                                                                                                                                                                Shared
26         assert tag(tK[.
                       e . .]) == tag(tQ[.
                                      e . .]) # tQ
                                                 e and tK
                                                        e should match
                                e . .) # FP32 accumulate and pack S=QKT                                                               r0
27         rS[j/8] = matmul(tK,
                             e tQ,.
                                                                                                                                               hi
28     . . . # Online softmax: overwrite rS with packed P and rescale rO
29     for j in range(16): # PV, V is transposed due to MFMA
                                                                                                                                                        wid=0          wid=2
30          tV = sV[wtid%2,j/8,j%4,j%8/4*2+wtid/32,(wtid/2)%16]
                                                                                        sq




                  e
                                                                                              ..
31         tV
            e = tV.view((8,),bf16)                                                             .
                                                                                                                                      r8
32         assert tag(tV[.
                       e . .]) == tag(rS[.
                                      e . .]) # tV e and rS
                                                          e should match




                                                                                                                                                                                                 Registers
                                                                                                                                            tid
33         rO[j%4] = matmul(tV,
                             e rS[j/4],.
                                e        . .) # FP32 accumulate and pack O
34       syncthreads()
35   . . . # Normalize, pack, and store O


Figure 1. Overview of Ave. Left: Simplified DSL implementation of flash attention (𝑑=128, 𝐵𝑟 =256, 𝐵𝑐 =64, 512 threads). Top right: Ave’s
workflow for agentic optimization. Bottom right: Tag propagation for 𝑉 across memory levels. Each color represents a unique sequence-
coordinate tag, and background shading links code regions to memory access patterns. r0 and r8 represent row 0 and row 8.



invariants. It exposes hardware instructions and compiler                        a planner retrieves optimization knowledge, a selector or-
policies while abstracting complex memory layout encodings                       ders compatible proposals, and a lowering agent implements
as tiles (§4).                                                                   them. Validation checks invariants and tests before profiling.
                                                                                 Invariant violations and performance update the benchmark-
Invariant Validation. Ave validates data-flow invariants at
                                                                                 local planner through ICRL (§6).
compile time with zero runtime overhead. The compiler
lowers the DSL to MLIR [40] and propagates tags across
assignments and shared memory using flow-sensitive, path-                        4    The Ave DSL
insensitive analysis. Path-insensitive merging keeps solving
                                                                                 Layouts and Tiles. The Ave DSL models all memory accesses
tractable. An SMT solver checks tag assertions and returns
                                                                                 via tiles [24, 41, 52, 69]. A tile is a memory region paired with
concrete assignments that witness violations and guide the
                                                                                 a layout function [10] that maps multi-dimensional logical
agent [20] (§5).
                                                                                 coordinates to one-dimensional physical offsets. A layout
Agentic Optimization Harness. Ave adopts an agentic work-                        function  (s,t) is parameterized by two tuples: shapes s =
flow to iteratively optimize kernels, as shown at the top                        (𝑠 1, . . . , 𝑠𝑛 ) and strides t = (𝑡 1, . . . , 𝑡𝑛 ). It maps an 𝑛-element
right of Figure 1. Starting from a DSL kernel and unit tests,                    coordinate c = (𝑐 1, . . . , 𝑐𝑛 ) to a linear index. Following the
                                                                             4
CuTe layout algebra, when all elements of s and t are integers,                helper combines two MFMAs along the reduction dimen-
the layout computes                                                            sion to perform a 32×32×16 operation per wavefront. Each
                                                                               thread holds 8 BF16 elements from each input and 16 FP32
                                               𝑛
                                              ∑︁                               accumulator elements.
                      (𝑐 1, . . . , 𝑐𝑛 ) =         𝑐 𝑖 𝑡𝑖
                                              𝑖=1
                                                                                  In Figure 1, matmul accumulates S in FP32 and packs it
                                                                               into the BF16 rS tile. The elided online softmax computes P
For a contiguous row-major tensor, 𝑡𝑖 = 𝑛𝑗=𝑖+1 𝑠 𝑗 : each                      row-wise, overwrites rS with the packed probabilities, and
                                             Î
stride is the product of the dimensions that follow it, and                    rescales rO. To transpose V, each thread loads a 4×2 sub-
𝑡𝑛 = 1. For brevity, these strides are omitted. For example,                   tile into tU (line 18) and scatters its low and high halves
the Q:Tensor((sq,hq ,d),bf16) in Figure 1 has the layout                       into transposed positions in sV (lines 19–20). This organiza-
                                                                               tion uses 4-byte global loads, 8-byte shared-memory stores,
                Q (𝑐 1, 𝑐 2, 𝑐 3 ) = 𝑐 1 hq d + 𝑐 2 d + 𝑐 3 .                 and 16-byte swizzled shared-memory loads that feed the
                                                                               PV loop directly (lines 29–33, highlighted in gray). matmul
The subscript operator in Figure 1 maps coordinates to a lin-
                                                                               accumulates the output in FP32 and packs it into rO. After
ear index and accesses the corresponding memory location.
                                                                               all sequence tiles, the kernel normalizes, packs, and stores
   Following CuTe, a nested layout represents its shape, stride,
                                                                               O. The final steps and lane-to-output mapping are elided in
and natural coordinate as congruent hierarchical tuples: ev-
                                                                               the figure.
ery coordinate leaf pairs with the stride leaf at the same
position. A scalar coordinate for a nested mode is first con-                  Tag Functions and Assertions. A tag function annotates tensor
verted to this hierarchical form by mixed-radix division and                   elements with symbolic tags: tuples of constants, symbolic
remainder using the mode’s shape. The layout recursively                       expressions of coordinates, or the special symbols ⊥ and ⊤.
sums the coordinate–stride products. For example, for the                      Tags propagate through assignments.
first nested coordinate c1 = (𝑐 1,1, 𝑐 1,2 ), with shape (𝑠 1,1, 𝑠 1,2 )          For example, TQ , TK , and TV in Figure 1 assign tags to el-
and stride (𝑡 1,1, 𝑡 1,2 ), the corresponding sub-layout computes              ements of Q, K, and V based on their coordinates (the type
1 (c1 ) = 𝑐 1,1𝑡 1,1 + 𝑐 1,2𝑡 1,2 . Nested layouts primarily repre-           bf16 is omitted for brevity):
sent hardware-swizzled layouts used by tensor cores and                                      TQ = Q[sq,hq ,d] → (hq /gqa, d)
matrix cores. Layout algebras further define composition,                                    TK = K[sq,hkv ,d] → (hkv , d)
logical division, and logical projection over layout functions                               TV = V[sq,hkv ,d] → (hkv , sq)
to represent operations such as data shuffling and dispatch-                   Tag assertions require conformity or non-conformity be-
ing disjoint work to warps (wavefronts on AMD) and threads.                    tween tags. The assertion on line 26 in Figure 1 requires
We refer the reader to [10] for details.                                       matching tags for elements of Q and K:
   DSL programs use make_local() and make_shared() to                                      assert tag(f
                                                                                                      tK[. . .]) == tag(f
                                                                                                                        tQ[. . .])
allocate a tile backed by registers and shared memory. DSL
programs may use the view() function to reinterpret a tile                     Computing S = QK𝑇 requires each wavefront to multiply
under a different logical layout. For example, line 8 of Figure 1              its 32 rows of Q with two 32×128 blocks of K per iteration.
derives gQ to logically partition Q by 𝐵𝑟 and access data in                   The tag functions TQ and TK return the attention-head and
16-byte chunks:                                                                reduction-dimension indices, so their tags match only when
                                                                               the operands belong to the same head and represent the same
            gQ = Q.view((sq/Br,Br,hq ,d/8),u128)
                                                                               position along the reduction dimension. A passing assertion
Vectorizing loads in 16-byte chunks is a common optimiza-                      confirms that the implementation preserves this operand-
tion to fully utilize GPU memory bandwidth. However, Ave                       pairing requirement across optimizations such as shared-
requires tiles to express all memory accesses and restricts                    memory staging or software pipelining. Similarly, the tag
layout operations. For example, view() requires source and                     functions TV and TrS
                                                                                                 e return the attention-head and reduction-
destination layouts to cover identical memory sizes. These                     dimension indices. The assertion on line 32 therefore checks
constraints simplify program analysis and eliminate the need                   that the operands of O = PV belong to the same head and
for full-scale alias analysis.                                                 represent the same position along their shared reduction
   Continuing with the flash attention example in Figure 1,                    dimension, without equating their independent output di-
the kernel maps work across 8 wavefronts. Each wavefront                       mensions. Figure 1 (bottom right) visualizes V’s sequence-
owns 32 rows of Q and produces the corresponding rows of                       coordinate tags as data propagate from global memory to
O, while all wavefronts share 𝐵𝑐 ×𝑑 tiles of K and V in shared                 shared memory and registers.
memory. MFMA expects column-major input operands A
and B and accumulator C. In attention, S must be row-major                     Compiler and Hardware Primitives. The DSL exposes compiler
because P=softmax(S) is computed row-wise, and O must                          and hardware primitives that enable agents to explore low-
also be row-major. The kernel therefore swaps Q and K for                      level optimizations. The DSL operates at the thread level:
QK𝑇 and transposes V during staging for PV. The matmul                         kernels manage thread indices and synchronization (e.g.,
                                                                           5
syncthreads()) directly, enabling the topology-aware dis-             analysis bounded, it does not model the full heap or track
patch optimizations [69].                                             tags written to global memory. The trade-off is that Ave can-
   Ave also exposes the eager materializations and compiler           not express invariants depending on heap-resident values.
scheduling barriers for tuning instruction scheduling in the          For example, in MoE sorting, where global <expert,token>
backend. These compiler barriers constrain instruction place-         tuples are grouped by expert ID, Ave cannot assert that each
ment around runtime synchronization primitives such as                tuple reaches the correct bucket in shared memory. Once
s_barrier. Unlike s_barrier, they emit no synchroniza-                data is in shared memory or registers, Ave can assign address-
tion instruction. These interfaces provide LLMs explicit con-         derived labels and track transformations such as swizzling.
trol over hardware features that are critical for reaching peak       Multi-GPU MoE kernels such as COMET [77] exchange data
performance on GPUs [33, 67].                                         via global cross-GPU buffers, which Ave does not currently
   Additionally, Ave exposes vectorized instructions for ex-          track. Modeling these buffers as explicit producer–consumer
plicit use in the DSL. For example, the AMD MI300X issues             queues remains future work.
one 2-way vectorized FMA per cycle on packed registers,                  Ave encodes propagated tags and tag assertions as sat-
doubling scalar FMA throughput. The AMD GPU backend                   isfiability modulo theories (SMT) constraints and uses the
can emit these instructions, but suboptimal register alloca-          solver to reason about the resulting layout algebra. The goal
tion often prevents it, so explicit vectorization in the DSL          is to validate data-flow invariants, not to construct full for-
sidesteps this limitation. Ave further exposes instructions           mal proofs. In particular, path-insensitive merging avoids
such as buffer_load_dwordx4 for branchless memory ac-                 enumerating branch conditions and keeps analysis tractable
cess with hardware out-of-bounds (OOB) protection, and al-            for optimized kernels. When an assertion fails, the solver
lows selecting the accumulator register class (AGPR) directly         returns a concrete assignment witnessing the violating ab-
in buffer load and MFMA instructions, practically doubling            stract state, including values for symbolic program variables
available vector registers over off-the-shelf toolchains.             such as thread IDs, loop indices, and tensor coordinates.
                                                                         Tags are purely compile-time constructs: all tracking and
5   Validating Data-Flow Invariants                                   validation occur within the compiler and incur no runtime
Ave validates data-flow invariants by tracking tags through           overhead. The current prototype requires workgroup dimen-
control and data flow at compile time. The compiler low-              sions known at compile time, allowing Ave to model regis-
ers DSL programs to MLIR and performs a flow-sensitive,               ters as a fixed-size array indexed by thread ID. It also unrolls
path-insensitive analysis that propagates tags through as-            loops before analysis.
signments and shared-memory accesses. At control-flow
joins, Ave merges incoming tags in a lattice with the partial         6    Agentic Optimization Harness
order ⊥ < 𝑡 < ⊤ for every concrete tag 𝑡:                             The Ave harness starts from a compile-and-test-passing DSL
                                                                      kernel and retains the fastest candidate that passes auto-
                                       if 𝑡 2 ≤ 𝑡 1                   mated invariant checks and unit tests. In each round, a plan-
                                1
                                
                                
                                 𝑡
              merge(𝑡 1, 𝑡 2 ) = 𝑡 2
                                
                                       if 𝑡 1 < 𝑡 2                   ner proposes optimization candidates, a selector constructs
                                       otherwise                      an ordered plan, and a lowering agent implements it. Only a
                                
                                ⊤
                                
                                                                      measured speedup replaces the current kernel.
                                
Constants carry ⊥. Consider the guarded selection rQ = 0
if isOOB(...) else Q[...], where isOOB prevents an                    Persistent Expert Knowledge. The knowledge base  contains
out-of-bounds access. The zero-valued branch contributes              auditable, expert-curated hardware facts, DSL references,
⊥, so rQ retains the tag of Q[...] because merge(⊥, 𝑡) = 𝑡.           and optimization recipes. Recipes specify applicability, trans-
Conversely, merging different concrete tags yields ⊤, denot-          formations, hardware controls, and invariant templates. We
ing non-conformity. Accordingly, == requires the merge to             curate entries from KernelWiki-style documentation [36],
be below ⊤, whereas != requires ⊤: ⊥ conforms with any                vendor examples, public pull requests, and microbenchmarks.
concrete tag, while ⊤ does not conform even with itself. Ave          Retrieve filters them by the request, GPU, and current ker-
can reset shared-memory tags to ⊥, permitting storage to              nel to produce 𝐾𝑡 .
be reused safely across pipeline stages without disabling             Local Planner State. For a request denoted by 𝑞, the fixed LLM
subsequent tag tracking.                                              𝜋𝜙 uses a benchmark-local prompt 𝜃𝑞,𝑡 updated after each
   The analysis tracks memory at byte granularity. This               optimization round through in-context reinforcement learn-
granularity covers the evaluated byte-aligned accesses and            ing (ICRL) [26, 49]. In round 𝑡, it observes 𝑥𝑡 = ⟨𝑞, 𝑠 ★, 𝐾𝑡 , 𝐹 ⟩:
supports packed storage for formats such as mxfp4 and                 the best kernel 𝑠 ★, retrieved knowledge 𝐾𝑡 , and feedback
nvfp4, although we do not evaluate FP4 kernels. Ave models            history 𝐹 . The initial history entry contains the initial kernel
global and shared memory as typed chunks and automat-                 𝑠 0 and its profile. Later entries record candidates, validation
ically propagates tags across accesses of different widths,           feedback, and profiles. The LLM produces ranked proposals
such as loads vectorized into 16-byte chunks. To keep the             𝑃𝑡 specifying optimizations, preconditions, target regions,
                                                                  6
invariant templates, and expected benefits. Select orders                   Algorithm 1: ICRL-guided optimization.
compatible proposals into 𝑎𝑡 = (𝑎𝑡,1, . . . , 𝑎𝑡,𝑚𝑡 ).                       Input: Query 𝑞, initial compile-and-test-passing kernel 𝑠 0 ,
Lowering and Validation. Lower invokes the lowering agent                              fixed knowledge base , fixed LLM 𝜋𝜙 , initial
                                                                                       prompt 𝜃𝑞,0 , optimization rounds 𝑁
to apply every optimization in 𝑎𝑡 to 𝑠 ★. The agent binds                    𝑠 ★ ← 𝑠 0 ; (ℓ ★, 𝑓−1 ) ← Profile(𝑠 0, ⟨𝑠 0 ⟩); 𝐹 ← ⟨𝑓−1 ⟩;
each selected instruction to code, specializes its parameters,               for 𝑡 = 0, 1, . . . , 𝑁 − 1 do
and materializes its invariant templates as tag functions and                    𝐾𝑡 ← Retrieve(, 𝑞, 𝑠 ★);
assertions, returning 𝑠ˆ𝑡 . Validation compiles this candidate,                  𝑥𝑡 ← ⟨𝑞, 𝑠 ★, 𝐾𝑡 , 𝐹 ⟩;
checks every generated invariant (the set may be empty),                         𝑃𝑡 ← 𝜋𝜙 (𝑥𝑡 ; 𝜃𝑞,𝑡 );
and runs unit tests. Validate returns compilation status 𝐶𝑡 ,                    𝑎𝑡 ← Select(𝑃𝑡 );
source-level assertion sites 𝐴𝑡 , failed sites 𝑉𝑡 , test status 𝑈𝑡 ,             𝑠ˆ𝑡 ← Lower(𝑠 ★, 𝑎𝑡 );
and record 𝑓𝑡 . For a passing candidate, Profile returns its                      𝑓𝑡 ← ⟨𝑎𝑡 , 𝑠ˆ𝑡 ⟩;
                                                                                  (𝐶𝑡 , 𝐴𝑡 , 𝑉𝑡 , 𝑈𝑡 , 𝑓𝑡 ) ← Validate(𝑠ˆ𝑡 , 𝑓𝑡 );
latency and appends the runtime profile to 𝑓𝑡 . Appending 𝑓𝑡
                                                                                  (𝐼𝑡 , Δ𝑡 ) ← (0, 0);
to 𝐹 gives the next round its transformation and outcome.                         if 𝐶𝑡 = 1 ∧ 𝐴𝑡 ≠ ∅ then
Reward Function. Let 𝐶𝑡 ∈ {0, 1} indicate successful compila-                           𝐼𝑡 ← 1 − |𝑉𝑡 |/|𝐴𝑡 |;
tion and 𝑈𝑡 ∈ {0, 1} indicate that all unit tests pass. Let 𝐴𝑡 be                 end
the source-level assertion sites in 𝑠ˆ𝑡 , and let 𝑉𝑡 ⊆ 𝐴𝑡 be those                if 𝐶𝑡 = 1 ∧ 𝑉𝑡 = ∅ ∧ 𝑈𝑡 = 1 then
                                                                                         ( ℓˆ𝑡 , 𝑓𝑡 ) ← Profile(𝑠ˆ𝑡 , 𝑓𝑡 );
with at least one failing check. Thus, compiler unrolling does
                                                                                        Δ𝑡 ← (ℓ ★ − ℓˆ𝑡 )/ℓ ★;
not change the number of assertions. If compilation succeeds
                                                                                  end
and 𝐴𝑡 ≠ ∅, the invariant score is 𝐼𝑡 = 1 − |𝑉𝑡 |/|𝐴𝑡 |. Other-                   (𝑅𝑡 , 𝐹 ) ← (𝐶𝑡 + 𝐼𝑡 + 𝑈𝑡 + Δ𝑡 , 𝐹 ∥ ⟨𝑓𝑡 ⟩);
wise, 𝐼𝑡 = 0. If compilation fails, invariant checking does not                  𝑑𝑡 ← ⟨𝑥𝑡 , 𝑓𝑡 , 𝐶𝑡 , 𝐴𝑡 , 𝑉𝑡 , 𝑈𝑡 , Δ𝑡 , 𝑅𝑡 ⟩;
run, and we define 𝑉𝑡 = ∅. Unit tests run only when 𝐶𝑡 = 1                        if Δ𝑡 > 0 then
and 𝑉𝑡 = ∅. If they do not run, 𝑈𝑡 = 0. For a kernel that                                (𝑠 ★, ℓ ★) ← (𝑠ˆ𝑡 , ℓˆ𝑡 );
compiles, passes every invariant check, and passes all unit                       end
tests, let ℓˆ𝑡 be its measured latency and ℓ ★ the latency of the                 𝐸𝑡 ← PolicyEval(𝑑𝑡 );
current best kernel. Runtime improvement is defined as:                          𝑔𝑡 ← Analyze(𝐸𝑡 );
                                                                                 𝜃𝑞,𝑡 +1 ← ParameterUpdate(𝜃𝑞,𝑡 , 𝑔𝑡 );
                                                                             end
              ℓ ★ − ℓˆ𝑡
                         , 𝐶𝑡 = 1 ∧ 𝑉𝑡 = ∅ ∧ 𝑈𝑡 = 1,                         Output: Best kernel 𝑠 ★
             
             
        Δ𝑡 =
             
             
                  ℓ★
              0,          otherwise.
             
             
             
                                                                           action. Lowering preserves existing assertions and adds this
Thus, a positive Δ𝑡 denotes lower latency, while a validated               one with the prompt:
slowdown receives a negative performance term. The com-                          Tile the scalar 𝑄𝐾 𝑇 dot products into 32×32×16 accu-
plete reward is 𝑅𝑡 = 𝐶𝑡 + 𝐼𝑡 + 𝑈𝑡 + Δ𝑡 . The replay record                       mulations, using two 32×32×8 BF16 MFMA instruc-
stores the planner input 𝑥𝑡 , candidate record 𝑓𝑡 , validation                   tions per accumulation. Pass BF16 views of tK and tQ
outcomes 𝐶𝑡 , 𝐴𝑡 , 𝑉𝑡 , and 𝑈𝑡 , performance term Δ𝑡 , and re-                   to matmul, which accumulates in FP32 and packs the
ward 𝑅𝑡 . We denote this record by 𝑑𝑡 .                                          result into BF16 scores.
Text-Gradient Planner Update. Algorithm 1 summarizes the                      The lowering agent materialized the tags and assertion
planner update. After each optimization round, PolicyE-                    and staged 𝐾 in sK, but formed tK from the original (512, 2)
val summarizes 𝑑𝑡 as 𝐸𝑡 , Analyze converts it into a textual               layout. The kernel compiled, but the tags of f       tK and f
                                                                                                                                       tQ dis-
critique 𝑔𝑡 , and ParameterUpdate applies a constrained                    agreed at the matmul use site, so tests and profiling did not
text-gradient edit to produce 𝜃𝑞,𝑡 +1 [74]. Neither the LLM                run. Thus, (𝐶𝑡 , 𝑈𝑡 , Δ𝑡 ) = (1, 0, 0), 𝐼𝑡 < 1, and 𝑅𝑡 = 1 + 𝐼𝑡 < 2.
weights nor  change.                                                      The validator added the following witness to 𝑓𝑡 , which the
Example. We provide a concrete example to illustrate the pro-              harness subsequently appended to 𝐹 :
cess. On AMD MI300X, hardware entries cover MFMA, buffer                         Assertion failed at attn:26: tag( f
                                                                                                                   tK[0]) ≠ tag( f
                                                                                                                                 tQ[0]).
operations, data parallel primitive (DPP) instructions, and                      Witness: i=0, j=1, tid=0, wid=wtid=0, idxq =idxh =0.
LDS, vector general-purpose register (VGPR), and AGPR lim-                    The witness identified the mismatched MFMA operands.
its. The omitted matmul helper in Figure 1 uses two 32×32×8                PolicyEval summarized 𝑑𝑡 , including the candidate code
BF16 MFMA instructions for a 32×32×16 operation. For row-                  and witness, as 𝐸𝑡 . Analyze then traced the mismatch to the
major 𝑄𝐾 𝑇 , it swaps 𝑄 and 𝐾 as detailed in §4. Figure 1 keeps            flattened LDS access and produced the critique 𝑔𝑡 . Parame-
𝑄 in rQ and stages 𝐾 in sK, read through f    sK. The planner              terUpdate applied 𝑔𝑡 to produce 𝜃𝑞,𝑡 +1 . In the next round,
targets this region with a recipe whose templates define the               the planner proposed the following revision, which Select
𝑄/𝐾 tags and operand assertion. Here, 𝑎𝑡 contains only this                placed at 𝑎𝑡 +1,1 :
                                                                       7
      Stage 𝐾 in sK with 16-byte cooperative loads, synchro-           MoE routing and multi-GPU communication, require new ab-
      nize, and reinterpret its (512, 2) layout as (2, 32, 8, 2)       stractions. The tensor memory (TMEM) extension discussed
      u128. For MFMA-loop index 𝑗 ∈ [0, 16), let 𝑙 = wtid.             below illustrates one such extension [53]. Additionally, the
      Read tK from fsK at ( 𝑗/8, 𝑙%32, 𝑗%8, 𝑙/32), pair it with        analysis tracks memory at byte granularity. It treats two
      tQ = rQ[ 𝑗%8], and view both as 8 BF16 elements. Up-             packed FP4 values within a byte as one unit, so permutations
      date rS[j/8] with matmul, which accumulates these
                                                                       of individual nibbles are invisible to data-flow invariants.
      views in FP32 and packs the result into rS[j/8].
                                                                       Using More Tokens and Stronger Models. As shown in Sec-
  The revised binding reads 𝐾 through f  sK and leaves rQ              tion 9, stronger models often improve generated GPU ker-
unchanged. It passed all checks and was profiled.                      nels, but higher token use alone does not close the gap with
                                                                       expert libraries: without invariants, lowering agents can still
7   Implementation                                                     exhaust their contexts through trial-and-error repairs.
The Ave prototype comprises approximately 22,000 lines                    Unguided agentic optimization is vulnerable to reward
of C++ and 7,000 lines of Python across the DSL compiler,              hacking, which can inflate measured speedups without yield-
program analysis, agentic harness, and JIT infrastructure.             ing useful kernels [30]. Our manual inspection is qualitative
We use Codex as the harness runtime [54] and configure                 and targets known shortcut patterns that bypass the main
the planner, lowering agent, PolicyEval, Analyze, and Pa-              computation, including PyTorch fallbacks, precomputed or
rameterUpdate with the same selected model. Ave retains                zeroed outputs, and branches on benchmark values. We do
the current best kernel and summaries of prior candidates,             not classify semantics-preserving changes within a convolu-
validation outcomes, and profiles. The harness periodically            tion kernel, such as strength reduction for fixed filter dimen-
compacts the feedback history. The Python front-end parses             sions, as reward hacking. Data-flow invariants additionally
DSL programs into an AST, which the C++ compiler lowers                reject shortcuts that violate declared use-site relationships.
to an extended MLIR dialect encoding layout algebras, then             Neither mechanism is exhaustive: inspection may miss sub-
to LLVM IR and GPU executables. We extend the LLVM 20                  tler shortcuts outside known patterns, and invariants cannot
AMDGPU backend with explicit synchronization barrier                   detect behavior outside their vocabulary.
scheduling, register-class selection for buffer load and MFMA          Compiler and Language Design. Higher-level DSLs such as
instructions, and eager materialization through phantom                Triton automate layouts and thread scheduling, eliminat-
uses in inline assembly.                                               ing several manual optimizations. Peak performance still
   Tag propagation and invariant checking use custom passes            requires low-level controls such as inline assembly, explicit
built on MLIR’s pass infrastructure. These passes traverse the         register-class selection, and scheduling barriers [1, 67]. Be-
IR and emit SMT constraints encoding data-flow invariants,             cause compiler stacks often lag behind new hardware, ven-
which Z3 solves [20].                                                  dors rely on leaky language abstractions [67], or just ship
   The JIT layer follows Triton’s model: generics propagate            hand-optimized assembly. Ave exposes these controls as
compile-time constants into GPU kernels, compiled binaries             policies chosen by LLMs and implemented by the compiler.
are cached, and Python bindings expose kernel invocation.                 Ave remains syntactically close to existing DSLs so that
                                                                       LLMs can generalize from their training data via in-context
8   Discussion                                                         learning [49], enabling adoption of new frontier models
Limitations of Data-Flow Invariants. Data-flow invariants val-         without retraining. Better compiler automation could ab-
idate concrete transformations but do not propose algorith-            sorb more low-level decisions, while a more radical LLM-
mic changes, such as restructuring standard attention into             oriented language could improve token efficiency and sup-
tiled flash attention with online softmax [19], or selecting           port stronger code generation.
search-space parameters such as tile sizes and warp/wave-              Generalizing across Hardware Architectures. Porting Ave to
front specialization. The planner and knowledge base handle            a new GPU requires (i) integrating the target toolchain and
these decisions. Applying invariants while the algorithm is            exposing its low-level intrinsics and (ii) adding hardware-
still changing could also constrain exploration. A full op-            specific optimizations to the knowledge base. ICRL binds
timization can be separated into two stages: algorithm se-             these entries to new kernels without model retraining, but
lection and initial kernel generation occur first, after which         experts must encode new techniques.
data-flow invariants guard low-level optimizations.                       We added NVIDIA Hopper and AMD CDNA4 backends
   Full formal verification can establish stronger properties,         with localized changes. Initial support for both architectures
but requires substantial proof engineering [7, 31, 37] and pro-        took approximately one person-week. For CDNA4, we ex-
duces implementation-specific proofs. Ave instead checks               posed FP4 intrinsics. For Hopper, we exposed warp-group
shared-memory layouts and operand pairing with tractable,              matrix multiply-accumulate (WGMMA) and mbarrier. We
flow-sensitive, path-insensitive analysis. As Section 5 de-            then added architecture-specific knowledge entries. NVIDIA
tails, properties involving global-memory writes, such as              Blackwell requires one further abstraction because its kernels
                                                                   8
                                 GPT-5.6 Sol                                  DeepSeek V4 Pro                                 DeepSeek V4 Flash

Method         Perf       Time       Turns     Tok.    Cost      Perf        Time        Turns   Tok.     Cost    Perf       Time        Turns    Tok.    Cost

 GEMM
Ave            0.89 2552/185/107      12        0.70    $6.49    0.88     2809/191/96     17      0.93    $1.16   0.90    3947/187/112    13       1.00   $0.61
KernelFalcon   0.55 1507/81/337       12        0.14    $2.92    0.39    1327/137/353     12      0.10    $0.23   0.49     306/21/51       8       0.05   $0.04
KSearch        0.36 802/127/209       12        0.16    $2.09    0.06     3399/220/97     20      0.41    $0.81   0.30    5621/326/117    20       0.86   $0.71
CUDAForge      0.07 752/294/919       11        0.11    $1.86    0.01    1789/159/512     19      0.17    $0.34   0.03    489/238/776     17       0.13   $0.08
Atrex          0.51 11201/1/465       327      60.56   $46.26    0.24     9980/0/123      524    105.54   $8.17   0.88    2033/13/295     207     22.64   $0.56

 Attention
Ave            0.99 1999/16/63         6        0.44    $4.67    0.94     1175/14/66       5      0.35    $0.51   0.94   2569/18/67        7      0.70    $0.40
KernelFalcon   0.33 1570/215/336      12        0.14    $2.93    0.09     1958/50/175     13      0.13    $0.27   0.10   523/23/54        10      0.11    $0.07
KSearch        0.15 1237/121/130      19        0.31    $4.06    0.03    2891/211/130     14      0.34    $0.68   0.03  3812/31/133       10      0.62    $0.51
CUDAForge      0.001 681/271/896      11        0.12    $2.08    0.01    1648/344/1123    14      0.20    $0.44   0.01  615/187/314       17      0.17    $0.10
Atrex          0.91 9477/2/660        347      49.68   $34.55    0.68     8524/6/153      356    60.47    $4.35   1.01 4350/6404/1254     720    112.21   $1.57

 Fused MoE
Ave            0.94 2651/17/57         9        0.75   $7.01     0.91     2400/26/80      10      0.77    $1.10   0.92    3416/67/224     11      1.02    $0.56
KernelFalcon   0.12  725/23/54         8        0.11   $1.80    0.0002   1282/130/321     12      0.18    $0.29   0.02    764/123/231     13      0.16    $0.10
KSearch        0.07 2111/113/110      14        0.39   $5.71     Fail    5829/484/579     20      0.83    $1.38   0.002   937/379/367     14      0.27    $0.14
CUDAForge      0.02 676/272/1375      10        0.11   $2.03    0.001    1135/156/357     19      0.16    $0.30   Fail    4320/461/640    20      0.70    $0.57
Atrex          0.32 14084/14/670      265      196.98 $146.77    Fail    9723/61/2129    1170    145.34   $9.20   0.01      7706/6/4      556    193.98   $2.71
                      Table 1. Optimization performance and resource costs across workloads, frameworks, and models.



dynamically manage TMEM. We plan to model TMEM as                                   runs within GPU graphs, pinning each process to the GPU-
shared memory using a simple lifetime heuristic: optimized                          local CPU socket. We evaluate all agentic frameworks with
kernels typically allocate TMEM near entry and release it                           GPT-5.6 Sol (GPT) [55], DeepSeek V4 Pro (DSv4) [23], and
near exit. This abstraction would propagate tags through                            DeepSeek V4 Flash (DSv4F) [23], adapting their prompts for
TMEM reads and writes without modifying the core analy-                             MI300X. For Ave, the selected model drives every Codex-
sis.                                                                                based harness stage, including planning, lowering, policy
                                                                                    evaluation, analysis, and prompt updates.
                                                                                       Turns, Tok., Cost, and Time are averages over attempted
9     Evaluation                                                                    problems. Pass@𝑘 generation entries are per attempt. A turn
Our evaluation answers the following research questions:                            is an LLM-generation segment between tool calls. Tok. is
                                                                                    in millions, Cost is the API charge in U.S. dollars, and Time
    Q1. How effectively does Ave optimize high-performance                          splits LLM/compile/evaluate wall time in seconds. DeepSeek
        GPU kernels? (§9.1)                                                         Cost averages on- and off-peak prices.
    Q2. How do ICRL and data-flow invariants affect an agent’s                         Unless noted, throughput is normalized to hipBLASLt for
        ability to apply optimizations? (§9.2)                                      MI300X GEMM, AITER for MI300X attention and MoE, and
    Q3. How well does Ave generalize across kernel families                         the PyTorch reference supplied by KernelBench. We con-
        and GPU architectures? (§9.3)                                               sider a kernel valid if it compiles, passes all invariant checks,
    Q4. How do data-flow invariants affect optimization suc-                        correctness tests, and a manual reward-hacking review (§8).
        cess and cost? (§9.4)                                                       Only valid kernels contribute to performance. Perf. and Mean
                                                                                    are geometric means of normalized throughput. Min and Max
Experimental Environment. Our primary server has two 64-
                                                                                    are extrema, and >1× counts ratios above parity. Pass@𝑘
core AMD EPYC 9554 CPUs, 2 TB of DDR5, and eight 192 GB
                                                                                    counts tasks solved within 𝑘 attempts. KernelBench genera-
AMD MI300X GPUs. It runs Ubuntu 22.04.5, Linux 5.15.0,
                                                                                    tion is a separate first phase that stops at the first test-passing
and ROCm 7.2.2 [5], whose LLVM 20.0 fork underlies our
                                                                                    candidate. Optimization starts from that candidate. Post-hoc
compiler extensions. Our portability server has two 48-core
                                                                                    rejection counts as failure without resuming. Fail means
Intel Xeon Platinum 8558 CPUs, 2 TB of DDR5, and eight
                                                                                    no valid implementation while we report the costs for refer-
141 GB NVIDIA H200 GPUs. It runs Ubuntu 24.04.1, CUDA
                                                                                    ences. Success requires every requested transformation.
12.8, and driver 570.148.08. We warm up each kernel for
one second and report its mean latency over at least 100
                                                                              9
                                                                                          KernelFalcon


                                                                                                                   CUDAForge
                                        hipBLASLt
                                                    HipKittens
                                                                                                                                                                     Ave              AITER          KernelFalcon




                                                                                                         KSearch
                                                                                                                                                               hipBLASLt              Triton             KSearch




                                                                 AITER
                                                                         Triton
                                                                                  Atrex
                                                                                                                                                               HipKittens              Atrex          CUDAForge




                                  Ave




                                                                                                                                    (hipBLASLt = 1.0 × )
                                                                                                                                    Normalized FLOPS
                                                                                                                                                              1
 Global intrusive changes
  Software pipelining              ✓      ✓           ✓          ✓       ✓        ✓        ✓               -          -                                      0.1

  Split K                          -       -            -        ✓         -       -          -            -          -                                     0.01

  MFMA matrix multiplication       ✓      ✓           ✓          ✓       ✓        ✓        ✓              ✓           -                                    0.001
                                                                                                                                                                       1024       2048     4096      8192      16384
  Stagger K                        ✓      ✓           ✓          ✓       ✓         -          -            -          -
                                                                                                                                                                       (a) BF16 Square GEMM Matrix size (𝑀 = 𝑁 = 𝐾 )
  Async memcpy                     ✓      ✓           ✓          ✓         -      ✓           -            -          -




                                                                                                                                    Normalized FLOPS
 Local source changes                                                                                                                                         1




                                                                                                                                     (AITER = 1.0 × )
  Tile-size specialization         ✓      ✓           ✓          ✓       ✓         -       ✓               -          -                                      0.1

  Bank conflict mitigation         ✓      ✓           ✓          ✓       ✓        ✓           -            -         ✕                                      0.01
  Vectorized loads                 ✓      ✓           ✓          ✓       ✓        ✓        ✓               -          -                                    0.001
  Loop unrolling                   ✓      ✓           ✓          ✓       ✓        ✓        ✓              ✓           -                                                1024       2048        4096      8192      16384
                                                                                                                                                                      (b) GQA Flash Attention (𝐷 = 128) Sequence length
  Workgroup swizzling              ✓      ✓           ✓          ✓       ✓         -       ✓               -          -




                                                                                                                                    Normalized FLOPS
 ISA-specific optimizations                                                                                                                                   1




                                                                                                                                     (AITER = 1.0 × )
  HW OOB-guarded loads             ✓      ✓           ✓          ✓         -      ✓           -            -          -                                      0.1
  Use AGPRs                        ✓      ✓           ✓          ✓         -      ✓           -            -          -                                     0.01
  Explicit instruction scheduling ✓ ✓ ✓ ✓                                  -      ✓           -            -          -
                                                                                                                                                           0.001
Table 2. GEMM optimizations implemented by Ave and other                                                                                                               1024       2048      4096     8192           16384
                                                                                                                                                                               (c) Fused MoE Sequence length
agentic frameworks using GPT-5.6 Sol, alongside hand-optimized
libraries. ✓, -, and ✕ denote implemented, absent, and incorrectly                                                                  Figure 2. Optimization performance on MI300X using GPT-5.6 Sol.
implemented optimizations.                                                                                                          Dashed lines denote parity. Vertical axes are logarithmic.



9.1   Kernel Performance                                                                                                            from HipKittens or AITER. HipKittens GQA lacks MI300X
To answer Q1, we evaluate five configurations each of three                                                                         support. We enable available autotuning.
LLM-inference kernels. GEMM multiplies square BF16 ma-                                                                                 In Figure 2, hipBLASLt for GEMM and AITER for atten-
trices with normally distributed entries. Flash attention uses                                                                      tion and MoE serve as the expert references for each work-
causal BF16 grouped-query attention (GQA) with batch 16,                                                                            load. With GPT, Ave’s normalized throughput is 0.89–0.99×
eight query heads, one key-value head, and head dimen-                                                                              relative to these references and 1.62–1176× relative to un-
sion 128, matching LLaMA-3 70B prefill under eight-way                                                                              contaminated agentic baselines. Atrex uses many more turns
tensor parallelism. Fused MoE uses DeepSeek-V3.2’s block-                                                                           than Ave and the other agentic frameworks because it relies
quantized FP8 configuration [22]: model dimension 7168,                                                                             on coding agents such as Codex and Claude Code for long
intermediate dimension 2048, top-𝑘 4, 32 experts per GPU,                                                                           optimization trajectories.
and expert parallelism of eight. Each workload starts from a
naïve implementation. Table 1 covers the complete optimiza-                                                                         GEMM. Table 2 groups optimizations by implementation
tion process, including costs for failed attempts.                                                                                  difficulty for an LLM, not performance impact. Global in-
   Expert-optimized baselines include hipBLASLt [4], HipKit-                                                                        trusive changes are hardest because they coordinate control
tens [33], AITER [1], and Triton [66]. Agentic baselines in-                                                                        flow, data movement, and layouts across a kernel. These
clude Atrex [72], KernelFalcon [70], KSearch [9], and CUDA-                                                                         include pipelining, Split 𝐾, MFMA layouts, Stagger 𝐾 for
Forge [78]. We run Ave, KernelFalcon, KSearch, and CUDA-                                                                            memory-controller hotspots [3], and asynchronous copies.
Forge for up to ten optimization trials and Atrex for up to                                                                         Local changes need only small patches for tile specialization,
five because of its API cost, reporting the best valid result.                                                                      bank-conflict mitigation, vectorization, unrolling, or work-
Each trial is one optimization round and may contain multi-                                                                         group swizzling. ISA-specific optimizations require architec-
ple LLM turns. These limits may leave some opportunities                                                                            tural knowledge and low-level support for hardware OOB
unexplored. In our experiments, we adopt hipBLASLt from                                                                             protection, AGPRs, and explicit scheduling. AMD intrinsics
ROCm 7.2.2, AITER 0.1.10post3, and the ROCm Triton fork                                                                             cover guarded loads and scheduling, while AGPR allocation
3.6.0+rocm7.2.2.git4ed88892. For each workload, the Triton                                                                          requires assembly or whole-kernel register management, as
baseline adopts the faster available Triton implementation                                                                          in HipKittens.
                                                                                                                               10
                             Naïve            +Async           +Pipe.                      instructions. The evaluated ROCm Triton baseline cannot
                              𝑉𝑇               +Bank        +Schedule
                                                                                           express wavefront specialization or fine-grained pipeline
                       800                                                                 scheduling. When paired with DSv4F, Atrex also spends sub-
    Effective TFLOPS




                       600                                                                 stantial compilation time in a trial-and-error search for a
                       400                                                                 working compiler configuration.
                       200
                                                                                           Fused MoE. Ave and AITER partition tokens and experts,
                         0
                             1024       2048       4096       8192      16384              use matrix cores, and quantize up-projection intermediates
                             GQA Flash Attention Optimization Sequence length              to FP8, enabling FP8 matrix cores with 16× the throughput
                                     (a) Optimization performance.
                                                                                           of scalar units. Ave’s normalized throughput is 8× relative
                                                                                           to KernelFalcon and 51× relative to CUDAForge. A correct
  Ablation                                     Optimization outcome        TFLOPS          fused MoE kernel must preserve blockwise quantization,
  (i) Runtime feedback only    +Async and +Bank ineffective                     190
                                                                                           route tokens through sorted expert maps, and group accesses
  (ii) +KB +invariants, -ICRL  VT , +Async, +Bank, +Schedule                    255        for coalescing. With DeepSeek V4 Pro, Atrex and KSearch
                               attempted (+Pipe not reached)                               fail to produce stable kernels.
  (iii) +KB +ICRL, -invariants VT fails                                         194           KernelFalcon uses one stage with DSv4 and two with GPT
  (iv) Full Ave                All five applied                                 588        and DSv4F. Successful KSearch and CUDAForge kernels
                                                                                           also fuse the up projection and activation before writing
                                         (b) Harness ablations.
                                                                                           a workspace. These two-stage designs omit FP8 requantiza-
Figure 3. Flash attention optimization. Panel (a) applies stages                           tion before the down projection and therefore cannot use
cumulatively in legend order. Panel (b) reports geometric-mean                             FP8 matrix cores. They also omit expert parallelism and full
effective TFLOPs across sequence lengths.
                                                                                           vectorization despite 16-byte alignment.
                                                                                              Table 1 shows that Ave remains effective across models,
                                                                                           whereas competing frameworks are more model-sensitive.
   Ave’s normalized throughput is 0.89× relative to hip-                                   GPT usually produces higher-throughput kernels but can
BLASLt. Atrex and KernelFalcon are the strongest agentic                                   generate excessive code, causing instruction-cache thrash-
competitors, while among the agentic baselines, KernelFal-                                 ing in CUDAForge attention. DSv4 and DSv4F more often
con is the only framework that completes every workload                                    omit optimizations or choose ineffective strategies. For exam-
with every model. Among direct CUDA/HIP frameworks,                                        ple, DSv4 gives KernelFalcon a low-occupancy, single-stage
only KSearch requests and uses MFMA.                                                       MoE kernel. Attention invariant checks take only 10–40 ms,
   KernelFalcon relies on Triton for pipelining, vectorization,                            negligible beside LLM inference.
unrolling, and tile autotuning, but lacks Stagger 𝐾 and low-
level scheduling. Ave’s normalized throughput is 1.62× rela-
                                                                                           9.2   Ablation Study of Ave’s Optimization
tive to KernelFalcon and 1.76× relative to Atrex’s CuTe-like
FlyDSL [41] kernel. Atrex applies most listed transformations                              To answer Q2, we use GPT and the same five attention con-
but misses workgroup swizzling, while incomplete FlyDSL                                    figurations as Q1. We cumulatively apply five optimizations
autotuning prevents tile specialization. Ave’s normalized                                  to naïve flash attention: on-demand VT materialization, asyn-
throughput is also 1.6× relative to expert Triton. The eval-                               chronous loads of Q and K (+Async), bank-conflict mitigation
uated ROCm Triton baseline cannot express asynchronous                                     (+Bank), pipelining with wavefront specialization (+Pipe.),
copies, explicit AGPR allocation, hardware-guarded loads,                                  and instruction scheduling (+Schedule). Ave also exposes
or explicit scheduling, which contribute to this gap. AITER                                fine-grained register allocation and data-flow invariants.
is near parity with hipBLASLt at 𝑀 = 𝑁 = 𝐾 = 1024, but its                                    Figure 3(a) shows throughput increasing monotonically
normalized throughput decreases at larger sizes as Split 𝐾                                 across all five stages. +Pipe gives the largest incremental
becomes less effective than grid partitioning.                                             gain: 75–116% across sequence lengths and 100% by geomet-
                                                                                           ric mean. The final configuration reaches 2.7–3.6× Naïve
Flash Attention. Ave matches AITER’s handwritten assem-
                                                                                           throughput. Effective TFLOPS use dense-attention FLOPs,
bly. Atrex reaches 0.91× through the contaminated retrieval
1 . Among uncontaminated agentic baselines, Ave’s normal-                                  including the causally skipped upper triangle. Figure 3(b) iso-
                                                                                           lates harness components while retaining unit tests and run-
ized throughput is 6.6× and 1176× relative to KSearch and
                                                                                           time feedback in every configuration. Because each knowl-
CUDAForge, respectively, and 3× relative to KernelFalcon.
                                                                                           edge base (KB) entry normally pairs an optimization recipe
KSearch and CUDAForge omit matrix cores for QK𝑇 and PV.
                                                                                           with invariant templates, the no-invariant ablation uses the
KernelFalcon’s Triton kernel neither reorganizes and stages
                                                                                           same KB after stripping those templates. In (i), feedback
V for an on-the-fly transpose nor pipelines and interleaves
                                                                                           prompts +Async and +Bank but cannot diagnose their inef-
1 Atrex copies the AITER reference kernel from its knowledge base rather                   fective implementations, leaving performance near Naïve.
than deriving it through optimization.                                                     In (ii), the KB provides optimization recipes and invariant
                                                                                      11
                            Syntax reference only                    In-context examples                       In-context optimization

      Dataset–Model Pass@1/3 Turns Tok. Cost      Time      Pass@1/3 Turns Tok. Cost       Time     >1× Mean/Min/Max Turns Tok. Cost        Time

      L1-GPT             96/99 19.20 0.81 $0.85 156/18/3      98/100 16.71 0.63 $0.73 158/15/6       54 1.10/0.12/25.56   4.11 0.10 $0.67 319/42/5
      L1-DSv4            94/96 22.45 1.21 $0.13 190/28/14      95/95 19.69 0.76 $0.09 226/25/35      40 0.64/0.01/29.23   4.18 0.14 $0.18 782/41/18
      L1-DSv4F          97/100 17.71 0.94 $0.05 137/17/4     100/100 15.64 0.70 $0.04 97/14/6        50 0.99/0.09/30.45   4.52 0.25 $0.16 1481/43/5

      L2-GPT             82/87 37.59 1.96 $1.81 289/41/4         84/88 34.30 1.94 $1.78 312/38/18    29 1.03/0.07/19.80   5.62 0.20 $1.46 605/54/11
      L2-DSv4            82/86 41.60 3.25 $0.30 287/58/23        83/86 30.78 1.82 $0.19 258/35/61    18 0.47/0.03/6.52    4.92 0.17 $0.24 968/39/14
      L2-DSv4F           77/86 40.07 3.79 $0.13 281/24/14        79/84 30.31 2.63 $0.10 170/20/13    34 0.99/0.05/41.66   5.59 0.34 $0.23 2043/44/10
 Table 3. KernelBench generation under syntax-reference and in-context prompting, followed by optimization of the in-context results.



      Dataset–Model   Success   Turns   Tok.   Cost       Time                   each model. Because the Ave DSL is absent from their train-
                                                                                 ing corpora, Table 3 compares prompting with only a com-
      No invariants
                                                                                 pact syntax reference against prompting with in-context
        L1-GPT              8    7.00   0.24   $1.74     607/45/1
                                                                                 examples. Generation uses only unit-test feedback and stops
        e
        L1-DSv4             1    4.00   0.19   $0.28   1105/40/2
                                                                                 at the first test-passing candidate. Among generations using
        e
        L1-DSv4F            1   12.00   0.86   $0.58   4968/99/6
                                                                                 in-context examples, manual review flags direct PyTorch
        e
        L2-GPT             12    6.50   0.25   $1.73    719/60/2
                                                                                 calls or input-specific shortcuts in 3 L1-DSv4, 6 L2-GPT, 13
        e
        L2-DSv4             7    6.43   0.28   $0.44   1763/71/2
                                                                                 L2-DSv4, and 5 L2-DSv4F cases. Optimization starts from this
        e
        L2-DSv4F            7    6.57   0.37   $0.23   1963/67/10
                                                                                 candidate and runs only for the in-context condition. One
        e
      With invariants
                                                                                 L2-DSv4 optimization ignores instructions and falls back to
        L1-GPT             18    6.06   0.22   $1.54    679/40/2
                                                                                 PyTorch. The reported pass rates count these outputs as fail-
        e
        L1-DSv4            16    5.88   0.26   $0.43   1956/38/2
                                                                                 ures. In-context examples improve Pass@1 while reducing
        e
        L1-DSv4F           19    6.47   0.39   $0.26   2313/43/2
                                                                                 turns, tokens, and API cost.
        e
        L2-GPT             25    6.12   0.22   $1.61    656/56/6
                                                                                    During optimization, Ave applies layout transformations,
        e
        L2-DSv4            26    5.54   0.22   $0.34   1273/43/4
                                                                                 fusion, vectorized loads, shared-memory staging, and instruc-
        e
        L2-DSv4F           23    5.74   0.37   $0.26   2100/50/4
                                                                                 tion scheduling. Some kernels remain below parity because
        e

Table 4. Effect of data-flow invariants on optimizing 60 selected                their references call hipBLASLt or MIOpen. DSv4 and DSv4F
KernelBench tasks.                                                               have lower aggregate pass rates and mean throughput than
                                                                                 GPT, partly because they more often omit transformations
                                                                                 such as im2col [12].

templates, but without ICRL, the planner attempts +Schedule                      9.4   Effectiveness and Cost of Data-Flow Invariants
before +Pipe. Scheduling has no effect, leaving performance
                                                                                 To isolate the impact of data-flow invariants (Q4), we com-
at +Bank. In (iii), ICRL orders the steps, but without invari-
                                                                                 pare the full system with an ablation that removes invariant
ants the agent cannot diagnose and repair a VT layout that
                                                                                 templates and, consequently, generates no tag functions,
mispairs reduction coordinates, so performance remains near
                                                                                 assertions, or invariant-violation feedback. We select Kernel-
Naïve. The full system in (iv) completes the sequence: VT ,
                                                                                 Bench GEMM and convolution tasks from L1 (L1)  e and L2 (L2).
+Async, +Bank, +Pipe., and +Schedule.
                                                                                                                                           e
                                                                                 Each task requests MFMA matrix multiplication, software
9.3   Generality Across Architectures and Kernels                                pipelining, and HW OOB-guarded loads. Success requires
                                                                                 applying all three.
To answer Q3, we evaluate both cross-architecture portabil-                         Table 4 shows that invariants improve success in every
ity and generality beyond the production kernels in §9.1. For                    dataset–model pair. They generally reduce turns, tokens,
portability, we add an NVIDIA Hopper backend and use GPT                         and API cost, while their effect on wall time is mixed. Thus,
to optimize the same five configurations of each workload on                     invariants consistently make intrusive transformations more
H200. Against cuBLASLt [51], vLLM’s FlashAttention-3 fork                        reliable.
(b3964b1) [68], and vLLM’s DeepGEMM fork (a6b593d) [21],
Ave achieves geometric-mean normalized throughputs of                            10    Related Work
0.98×, 1.00×, and 0.99× over the five GEMM, attention, and
fused-MoE configurations, respectively.                                          Synthesizing GPU Kernels with LLMs. Frontier coding mod-
   To assess cross-kernel generality, we evaluate 100 Level 1                    els [23, 55] combined with agentic workflows [6, 9, 15, 18,
(L1) and 100 Level 2 (L2) KernelBench tasks on MI300X with                       25, 26, 30, 32, 56, 70, 72, 76, 78] have made generating GPU
                                                                            12
kernels from natural language specifications practical. These          tensor core utilization, efficient memory layout, software
workflows differ along three axes: reward signals, optimiza-           pipelining, operator fusion, and overlapping computation
tion knowledge, and execution quality. Most use correctness            with memory access. They rely on heuristics and exhaus-
and relative performance gains as rewards, which are sus-              tive search to find efficient schedules. Note that Ave com-
ceptible to reward hacking [39]. The concurrent 𝜇CUTLASS               plements these compilers: we expose the hardware SIMT
system instead uses Speed-of-Light guidance, penalizing                programming model along with low-level intrinsics in the
claims that exceed hardware capabilities to reduce reward              DSL, and delegate schedule exploration to LLMs.
hacking [30]. Sources include fine-tuning and reinforcement            Invariants and Information Flow Systems. Invariants provide
learning [64], world models [9], and evolutionary search [43].         a concise way to specify and reason about end-to-end prop-
   Reliable execution of complex optimizations is essential            erties across multi-layered systems [47, 65, 73]. Information
for meaningful performance gains on production kernels.                flow analysis enforces such invariants at the system level.
Ave incorporates data-flow invariants as dense process re-             HiStar [75] assigns security labels to data, defines a partial
wards that guide optimization. Exposing low-level hardware             order on labels, tracks their propagation, and permits infor-
and compiler intrinsics further enables optimizations such             mation flow only along that order. JFlow [50] augments Java
as instruction scheduling, distinguishing Ave from systems             with information labels and enforces information flows at
limited to end-to-end correctness and performance rewards.             the language level. These prior systems focus on enforcing
ICL and ICRL. In-context learning (ICL) enables LLMs to                security policies. Ave adapts the same tracking and enforce-
adapt to new downstream tasks from examples provided in                ment mechanisms to GPU kernel optimization, using tag
the prompt without model parameter updates [49]. Further-              propagation to check correct operand pairings and giving
more, in-context reinforcement learning (ICRL) extends ICL             LLMs a cross-layer view of relevant data-flow constraints.
by treating the prompt as a dynamic learnable policy and up-              Formal verification [11, 13, 37, 63] can detect invariant
dating it based on reward signals. For example, TextGrad [74]          violations precisely, but multiplies development effort by
provides a general framework for computing text-based gra-             2–6× [37] for sequential programs. Verifying concurrent
dients over LLM outputs. In terms of kernel code generation,           GPU kernels demands additional modeling effort [7]. Ave
KernelBlaster [26] applies ICRL to CUDA kernel optimiza-               instead adopts lightweight static analysis to report action-
tion, maintaining a memory of past optimization trajectories           able validation failures, enabling the agentic loop to iterate
and using them to improve cross-task generalization. Ave               automatically. The current prototype uses Z3 [20] to rea-
builds on these techniques: we use ICRL to learn planner               son about layout algebra. A refined version could leverage
prompts that bind optimization knowledge to concrete ker-              polyhedral analysis [8, 28, 57] for faster validation.
nels, with data-flow invariant violations serving as process
rewards alongside runtime performance.                                 11    Conclusion
DSL Designs for GPU Kernels. GPU DSLs balance productivity             We introduced Ave, an agentic framework that uses compile-
against low-level control through their choice of abstraction.         time data-flow invariants to make LLM-generated GPU opti-
Triton describes workloads at the block level, hiding ex-              mizations more reliable. Its tile-based DSL and static analysis
plicit memory layouts and synchronization. Halide [59] and             turn invariant violations into concrete witnesses, guiding
Exo [35] separate algorithm specification from scheduling              agents through intrusive transformations without runtime
policy for tensor workloads. Tile-based DSLs [24, 30, 52, 69]          overhead. With ICRL, Ave reaches near-library performance
further structure programs around tiles as primitives for data         on AMD MI300X and generalizes to NVIDIA H200. More
movement and matrix multiplication, shifting implementa-               broadly, pairing domain abstractions with actionable correct-
tion complexity to compilers. This convenience can impose              ness feedback offers a path to reliable agentic optimization
an abstraction tax. Triton extensions such as Gluon [67] re-           wherever correctness depends on cross-layer data flow.
cover performance by exposing direct control over memory
layouts, warp specialization, register allocation, and instruc-        Acknowledgments
tion scheduling.                                                       We thank our shepherd, the anonymous reviewers, and Mark
   The Ave DSL combines tile abstractions with explicit com-           Hill for their thoughtful feedback. We also thank InnoMa-
piler controls for LLM-driven development. Its restricted              trix for providing the evaluation servers. This work was
memory model keeps static analysis tractable, while compile-           partially supported in part by donation grant PD26EG02 to
time data-flow invariants provide dense structural feedback            CSE HKUST, HKUST startup grant R9895, RGC-ECS project
during optimization. Its Triton-like syntax lets LLMs reuse            26218024, RGC-NSFC project CRS_HKUST601/24, and Na-
knowledge from training.                                               tional Natural Science Foundation of China grant 62232015.
Optimizing Compilers for Tensor Programs. Tensor compil-
ers [14, 29, 42, 46, 61, 71, 79, 80] lower DSLs and tensor
programs to GPU binaries. Their optimizations target high
                                                                  13
References                                                                  [20] Leonardo de Moura and Nikolaj Bjørner. Z3: An Efficient SMT
 [1] AMD. AITER: AI Tensor Engine for ROCm. https://github.c                     Solver (TACAS’08).
     om/ROCm/aiter.                                                         [21] DeepSeek-AI. DeepGEMM: A High-Performance Tensor Core
 [2] AMD. AMD Instinct MI300 Instruction Set Architecture. https:                Kernel Library. https://github.com/deepseek-ai/DeepGEMM.
     //www.amd.com/content/dam/amd/en/documents/instinct-                   [22] DeepSeek-AI. DeepSeek-V3.2: Pushing the Frontier of Open
     tech- docs/instruction- set- architectures/amd- instinct-                   Large Language Models. arXiv:2512.02556.
     mi300-cdna3-instruction-set-architecture.pdf.                          [23] DeepSeek-AI, Anyi Xu, Bangcai Lin, et al. DeepSeek-V4: To-
 [3] AMD. AMD Instinct MI300X workload optimization. https:                      wards Highly Efficient Million-Token Context Intelligence.
     //rocm.docs.amd.com/en/latest/how-to/rocm-for-ai/inferen                    arXiv:2606.19348.
     ce-optimization/workload.html.                                         [24] Yaoyao Ding, Bohan Hou, Xiao Zhang, et al. Tilus: A Tile-Level
 [4] AMD. hipBLASLt: General Matrix-Matrix Operations Library                    GPGPU Programming Language for Low-Precision Computa-
     for AMD GPUs. https://rocm.docs.amd.com/projects/hipBL                      tion (ASPLOS ’26).
     ASLt/en/latest.                                                        [25] Juncheng Dong, Yang Yang, Tao Liu, et al. STARK: Strategic
 [5] AMD. ROCm Software. https://github.com/ROCm/ROCm.                           Team of Agents for Refining Kernels (ICLR’26).
 [6] Carlo Baronio, Pietro Marsella, Ben Pan, et al. Kevin: Multi-          [26] Shengjun Kris Dong, Sahil Modi, Dima Nikiforov, et al. Ker-
     Turn RL for Generating CUDA Kernels (ICLR’26).                              nelBlaster: Continual Cross-Task CUDA Optimization via
 [7] Adam Betts, Nathan Chong, Alastair Donaldson, et al. GPU-                   Memory-Augmented In-Context Reinforcement Learning.
     Verify: a verifier for GPU kernels (OOPSLA ’12).                            arXiv:2602.14293.
 [8] Uday Bondhugula, Albert Hartono, J. Ramanujam, et al. A                [27] GLM-5-Team. GLM-5: from Vibe Coding to Agentic Engineer-
     practical automatic polyhedral parallelizer and locality opti-              ing. arXiv:2602.15763.
     mizer (PLDI ’08).                                                      [28] Tobias Grosser, Armin Groesslinger, and Christian Lengauer.
 [9] Shiyi Cao, Ziming Mao, Joseph E. Gonzalez, et al. K-Search:                 Polly - Performing polyhedral optimizations on a low-level
     LLM Kernel Generation via Co-Evolving Intrinsic World                       intermediate representation. Parallel Processing Letters 22, 4
     Model. arXiv:2602.19128.                                                    (2012), 1250010.
[10] Jack Carlisle, Jay Shah, Reuben Stern, et al. Categorical Foun-        [29] Yue Guan, Xinwei Qiang, Zaifeng Pan, et al. Mercury: Unlock-
     dations for CuTe Layouts. arXiv:2601.05972.                                 ing Multi-GPU Operator Optimization for LLMs via Remote
[11] Bodhisatwa Chatterjee, Drew Zagieboylo, Sana Damani, et al.                 Memory Scheduling (SOSP ’25).
     ProofWright: Towards Agentic Formal Verification of CUDA.              [30] Siva Kumar Sastry Hari, Vignesh Balaji, Sana Damani, et al.
     arXiv:2511.12294.                                                           Improving Efficiency of GPU Kernel Optimization Agents us-
[12] Kumar Chellapilla, Sidd Puri, and Patrice Simard. High Per-                 ing a Domain-Specific Language and Speed-of-Light Guidance.
     formance Convolutional Neural Networks for Document Pro-                    arXiv:2603.29010.
     cessing (IWFHR’06).                                                    [31] Chris Hawblitzel, Jon Howell, Manos Kapritsos, et al. IronFleet:
[13] Haogang Chen, Daniel Ziegler, Tej Chajed, et al. Using Crash                proving practical distributed systems correct (SOSP ’15).
     Hoare Logic for Certifying the FSCQ File System (USENIX                [32] Bodun Hu, Yoga Sri Varshan V, Saurabh Agarwal, et al. CUCo:
     ATC’16).                                                                    An Agentic Framework for Compute and Communication
[14] Tianqi Chen, Thierry Moreau, Ziheng Jiang, et al. TVM: An                   Co-design. arXiv:2603.02376.
     Automated End-to-End Optimizing Compiler for Deep Learn-               [33] William Hu, Drew Wadsworth, Sean Siddens, et al. HipKittens:
     ing (OSDI’18).                                                              Fast and Furious AMD Kernels. arXiv:2511.08083.
[15] Terry Chen, Zhifan Ye, Bing Xu, et al. AVO: Agentic                    [34] Rodrigo Huerta, Mojtaba Abaie Shoushtary, José-Lorenzo
     Variation Operators for Autonomous Evolutionary Search.                     Cruz, et al. Dissecting and Modeling the Architecture of Mod-
     arXiv:2603.24517.                                                           ern GPU Cores (MICRO ’25).
[16] Xinhao Cheng, Zhihao Zhang, Yu Zhou, et al. MPK: A Com-                [35] Yuka Ikarashi, Kevin Qian, Samir Droubi, et al. Exo 2: Growing
     piler and Runtime for Mega-Kernelizing Tensor Programs                      a Scheduling Language (ASPLOS ’25).
     (OSDI’26).                                                             [36] KernelWiki. KernelWiki — Blackwell & Hopper Kernel Op-
[17] Patrick Cousot and Radhia Cousot. Abstract interpretation: a                timization Knowledge Base. https://github.com/mit-han-
     unified lattice model for static analysis of programs by con-               lab/KernelWiki.
     struction or approximation of fixpoints (POPL’77).                     [37] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, et al. seL4:
[18] Weinan Dai, Hanlin Wu, Qiying Yu, et al. CUDA Agent: Large-                 formal verification of an OS kernel (SOSP ’09).
     Scale Agentic RL for High-Performance CUDA Kernel Gener-               [38] Monica Lam. Software pipelining: an effective scheduling
     ation. arXiv:2602.24286.                                                    technique for VLIW machines (PLDI ’88).
[19] Tri Dao. Flashattention-2: Faster attention with better paral-         [39] Robert Tjarko Lange, Qi Sun, Aaditya Prasad, et al. Towards
     lelism and work partitioning. arXiv:2307.08691.                             Robust Agentic CUDA Kernel Benchmarking, Verification, and
                                                                                 Optimization. arXiv:2509.14279.
                                                                       14
[40] Chris Lattner, Mehdi Amini, Uday Bondhugula, et al. MLIR:                [62] Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, et al.
     Scaling Compiler Infrastructure for Domain Specific Compu-                    Outrageously Large Neural Networks: The Sparsely-Gated
     tation (CGO’21).                                                              Mixture-of-Experts Layer (ICLR’17).
[41] Felix Li, Shijie Feng, Carlus Huang, et al. FlyDSL. https:               [63] Helgi Sigurbjarnarson, James Bornholt, Emina Torlak, et al.
     //github.com/ROCm/FlyDSL.                                                     Push-Button Verification of File Systems via Crash Refinement
[42] Yijin Li, Jiacheng Zhao, Sun Qianqi, et al. SIRIUS: Harvest-                  (OSDI’16).
     ing Whole-Program Optimization Opportunities for DNNs                    [64] Songqiao Su, Xiaofei Sun, Xiaoya Li, et al. CUDA-L2: Surpass-
     (MLSys’23).                                                                   ing cuBLAS Performance for Matrix Multiplication through
[43] Gang Liao, Hongsen Qin, Ying Wang, et al. KernelEvolve: Scal-                 Reinforcement Learning. arXiv:2512.02551.
     ing Agentic Kernel Coding for Heterogeneous AI Accelerators              [65] Shuo Tang, Haohui Mai, and Samuel T. King. Trust and pro-
     at Meta. arXiv:2512.23236.                                                    tection in the Illinois browser operating system (OSDI’10).
[44] Nelson F. Liu, Kevin Lin, John Hewitt, et al. Lost in the Middle:        [66] Philippe Tillet, H. T. Kung, and David Cox. Triton: an in-
     How Language Models Use Long Contexts (TACL’24).                              termediate language and compiler for tiled neural network
[45] Weile Luo, Ruibo Fan, Zeyu Li, et al. Benchmarking and                        computations (MAPL’19).
     Dissecting the Nvidia Hopper GPU Architecture (IPDPS’24).                [67] Triton. Gluon. https://github.com/triton-lang/triton/tree/mai
[46] Lingxiao Ma, Zhiqiang Xie, Zhi Yang, et al. Rammer: Enabling                  n/lib/Dialect/Gluon.
     Holistic Deep Learning Compiler Optimizations with rTasks                [68] vllm-project. Fast and memory-efficient exact attention. https:
     (OSDI’20).                                                                    //github.com/vllm-project/flash-attention.
[47] Haohui Mai, Edgar Pek, Hui Xue, et al. Verifying security                [69] Lei Wang, Yu Cheng, Yining Shi, et al. TileLang: Bridge Pro-
     invariants in ExpressOS (ASPLOS ’13).                                         grammability and Performance in Modern Neural Kernels
[48] Maxim Milakov and Natalia Gimelshein. Online normalizer                       (ICLR’26).
     calculation for softmax. arXiv:1805.02867.                               [70] Laura Wang and PyTorch Team. KernelFalcon: Autonomous
[49] Giovanni Monea, Antoine Bosselut, Kianté Brantley, et al.                     GPU Kernel Generation via Deep Agents. https://pytorch.org/
     LLMs Are In-Context Bandit Reinforcement Learners                             blog/kernelfalcon-autonomous-gpu-kernel-generation-via-
     (COLM’25).                                                                    deep-agents.
[50] Andrew C. Myers. JFlow: practical mostly-static information              [71] Mengdi Wu, Xinhao Cheng, Shengyu Liu, et al. Mirage: a
     flow control (POPL ’99).                                                      multi-level superoptimizer for tensor programs (OSDI ’25).
[51] NVIDIA. cuBLAS Library Documentation. https://docs.nvidi                 [72] Lingyun Yang, Yuxiao Wang, Shenghao Liang, et al. Are LLM-
     a.com/cuda/archive/12.8.0/cublas.                                             Generated GPU Kernels Production-Ready? A Trace-Driven
[52] NVIDIA. CUTLASS: CUDA Templates for Linear Algebra                            Benchmark and Optimization Agent. arXiv:2607.14541.
     Subroutines and Solvers. https://github.com/NVIDIA/cutlass.              [73] Alexander Yip, Xi Wang, Nickolai Zeldovich, et al. Improving
[53] NVIDIA. Parallel Thread Execution ISA Version 9.3. https:                     application security with data flow assertions (SOSP ’09).
     //docs.nvidia.com/cuda/parallel-thread-execution.                        [74] Mert Yuksekgonul, Federico Bianchi, Joseph Boen,
[54] OpenAI. Lightweight coding agent that runs in your terminal.                  et al.    TextGrad: Automatic "Differentiation" via Text.
     https://github.com/openai/codex.                                              arXiv:2406.07496.
[55] OpenAI. GPT-5.6: Frontier intelligence that scales with your             [75] Nickolai Zeldovich, Silas Boyd-Wickizer, Eddie Kohler, et al.
     ambition. https://openai.com/index/gpt-5-6.                                   Making Information Flow Explicit in HiStar (OSDI’06).
[56] Anne Ouyang, Simon Guo, Simran Arora, et al. KernelBench:                [76] Yi Zhai, Sijia Yang, Keyu Pan, et al. Enabling Tensor Language
     Can LLMs Write Efficient GPU Kernels? (ICML’25).                              Model to Assist in Generating High-Performance Tensor Pro-
[57] Benoît Pradelle, Benoît Meister, Muthu Baskaran, et al. Poly-                 grams for Deep Learning (OSDI’24).
     hedral Optimization of TensorFlow Computation Graphs (Pro-               [77] Shulai Zhang, Ningxin Zheng, Haibin Lin, et al. COMET:
     Tools’18).                                                                    Fine-grained Computation-communication Overlapping for
[58] Fernando Magno Quintão Pereira and Jens Palsberg. Register                    Mixture-of-Experts (MLSys’25).
     allocation by puzzle solving (PLDI ’08).                                 [78] Zijian Zhang, Rong Wang, Shiyang Li, et al. CudaForge: An
[59] Jonathan Ragan-Kelley, Connelly Barnes, Andrew Adams, et al.                  Agent Framework with Hardware Feedback for CUDA Kernel
     Halide: a language and compiler for optimizing parallelism,                   Optimization. arXiv:2511.01884.
     locality, and recomputation in image processing pipelines                [79] Jie Zhao, Bojie Li, Wang Nie, et al. AKG: automatic kernel
     (PLDI ’13).                                                                   generation for neural processing units using polyhedral trans-
[60] G. Ramalingam. The undecidability of aliasing. ACM Trans.                     formations (PLDI’21).
     Program. Lang. Syst. 16, 5 (Sept. 1994), 1467–1471.                      [80] Lianmin Zheng, Chengfan Jia, Minmin Sun, et al. Ansor: Gen-
[61] Amit Sabne. XLA: Compiling Machine Learning for Peak                          erating High-Performance Tensor Programs for Deep Learning
     Performance (DEEM’20).                                                        (OSDI’20).


                                                                         15
