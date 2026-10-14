                                         Exo-GPU: Safe, Imperative, User-schedulable Programming
                                         for Tensor Cores
                                         DAVID ZHAO AKELEY, MIT CSAIL, USA
                                         YUKA IKARASHI, MIT CSAIL, USA
                                         JONATHAN RAGAN-KELLEY, MIT CSAIL, USA
                                         Modern GPUs require not only SIMT-style parallelism but also software-managed concurrency between com-
                                         pute and data movement to reach maximum performance. Performance engineers must reason about sub-
arXiv:2609.16389v1 [cs.PL] 14 Sep 2026




                                         dividing work into the hierarchy of computation resources (threads, warps, warpgroups, blocks, clusters),
                                         and, in many cases, also must use asynchronous tensor core and memcpy instructions on different levels of
                                         the memory hierarchy (registers, tensor core accumulators, shared memory, global memory). Unlike CPUs,
                                         where out-of-order execution is managed by hardware and hidden from programmers, GPUs expose explicit
                                         instruction reordering to software through these asynchronous instructions. Well-established GPU program-
                                         ming languages generally offer either direct low-level control without safety guarantees (e.g., CUDA C++
                                         inline assembly or intrinsics) or easier-to-analyze, high-level abstractions (e.g., Triton’s tile-based model)
                                         that hide asynchronous instructions in the compiler backend, which may prevent performance engineers
                                         from maximizing performance by tuning critical details.
                                            We propose Exo-GPU, an imperative, low-level language that creates minimal abstraction over CUDA. Our
                                         key idea is to treat parallelism and synchronization as mere annotations on sequential code rather than as
                                         fundamental control flow primitives, enabling verification that these constructs do not alter the program se-
                                         mantics. The benefit is two-fold: programmers can reason about code without hidden control flow or mutation,
                                         while allowing the Exo-GPU compiler to verify sequential-parallel equivalence—guaranteeing that parallel ex-
                                         ecution is functionally equivalent to its sequential interpretation. We used Exo-GPU to author GEMM kernels
                                         for the H100 GPU, using wgmma, TMA, and split-k. Our kernels achieved over 80% of theoretical peak on
                                         large problem sizes, in some cases outperforming the vendor-provided CUBLAS library.


                                         1 INTRODUCTION
                                         Starting with Tensor Cores introduced in NVIDIA’s Volta generation of GPUs [13], the menu of
                                         tensor-specialized features in NVIDIA GPUs has expanded to encompass automated bulk move-
                                         ment of multidimensional data, distributed shared memory, and new asynchronous tensor cores
                                         supporting large-scale (up to 64 × 256) matrix accumulation in a single instruction [18]. This poses
                                         ever-increasing challenges for authoring correct, top-performing CUDA code. Not only must algo-
                                         rithms be rewritten to migrate work from traditional SIMT-style code to target these specialized
                                         instructions, but also, these instructions expose explicit out-of-order instruction execution to the
                                         programmer, moving synchronization that was traditionally the responsibility of the hardware
                                         (e.g., through scoreboarding) to the programmer.
                                            High-level kernel programming languages, such as Triton [24], provide a popular approach
                                         for taming this complexity. Triton’s tile-based, automatically-parallelized programming model re-
                                         duces the risk of programmer error by moving responsibility for correct usage of bulk data move-
                                         ment and synchronization instructions into the compiler. However, in practice, groundbreaking
                                         algorithms, such as the original FlashAttention 3 [21], are often written directly in CUDA C++
                                         for greater control. On the one hand, CUDA C++ provides direct control over features such as
                                         asynchronous data movement and warp specialization required for optimal GPU usage. On the
                                         other hand, CUDA C++ exposes programmers to a variety of potential bugs, which we broadly
                                         categorize as:
                                             (1) Dataflow Logic Bugs: Program optimization usually requires changing the storage or com-
                                                 putation order of intermediate values, e.g. caching data in a faster memory, or reordering
                                                 instructions to hide latency. A flawed optimization, such as an indexing bug in copying a

                                                                                               1
                                               David Zhao Akeley, Yuka Ikarashi, and Jonathan Ragan-Kelley


       tile, or exchanging two statements that don’t commute safely, can change the functional
       behavior of the program.
   (2) Instruction Logic Bugs: Accelerator instructions won’t work as intended if not used as spec-
       ified by the hardware vendor. For example, wgmma tensor core instructions require data in
       a certain input format and uniform execution by a full warpgroup (128 aligned threads).
   (3) Inter-Thread Synchronization Bugs: Garden-variety synchronization bugs involve two threads
       accessing the same memory location (with one access being a write) without ordering en-
       forced by synchronization.
   (4) Intra-Thread Synchronization Bugs: If one thread issues an asynchronous (async) instruc-
       tion, and that same thread later issues another instruction (async or not) that operates on
       the same memory location, overlapped or reordered instruction execution can undermine
       correctness.
   Our goal is to provide a programming model that gives CUDA-like control without accepting the
risk of these bugs as a fact of life. Existing CUDA C++ libraries such as CuTe [14] and ThunderKit-
tens [22] provide close-to-the-metal abstractions that minimize the risk of logic bugs, particularly
data movement and instruction input format bugs; however, none of them support large-scale
program analysis and synchronization checking of arbitrary input programs.
   As a starting point for the Exo-GPU language design, we postulate that programs with se-
quential semantics are far easier to analyze, both by humans and by compilers. We define pro-
gram behavior using standard sequential semantics, treating language features for parallelism and
synchronization–including parallel for-loops across CUDA thread hierarchies and barrier statements–
simply as annotations on sequential code. This design provides two key benefits: programmers
can intuitively reason about their code without hidden control flow or side effects, and more im-
portantly, compilers can verify whether synchronizations are legal; that is, they can verify these
annotations do not alter the program behavior relative to its baseline sequential interpretation.
   The Exo-GPU program, interpreted sequentially, serves as as the semantic baseline—defining
what the user intends to compute. Parallelism annotations specify which threads execute which
statement instances, while synchronization constructs specify how the user intends to uphold base-
line behavior. This raises a question: what degree of safety and control does Exo-GPU provide?
We define safety as sequential-parallel equivalence–ensuring that the parallel interpretation of a
program matches the sequential one. Parallelism is explicitly controlled by the programmer’s an-
notations, rather than being hidden and automated by the compiler. The Exo-GPU compiler’s role
is limited to verifying that the user-provided synchronization ensures equivalence.
   Through collective analysis (Section 4), we annotate each statement with a collective tiling, spec-
ifying which thread(s) execute each statement instance. This enables static analysis of the thread
assignment counts, ensuring instructions with thread convergence requirements (e.g. warp MMA)
are used correctly. To ensure sequential-parallel equivalence, we simulate execution on an abstract
machine (Section 5). The Exo-GPU program converts to an Abstract Machine program where data
variables store access histories (reads and mutations) with their thread and async instruction vis-
ibility, rather than numeric values. Synchronization statements become meaningful only in the
abstract machine, conditionally expanding the visibility of all prior recorded accesses.
   We built Exo-GPU as an extension to Exo [7, 8], a user-schedulable language providing com-
posable, checked rewrite rules for transforming sequential programs. Exo lacks GPU support, and
we significantly extended its frontend language design, static analysis, semantics, and codegen to
enable safe parallel program transformation. Treating parallel constructs as annotations over a se-
quential semantic baseline enabled us to reuse Exo’s over 60 verified rewrites as-is, which allowed
us to transform a simple sequential GEMM program into a complex GEMM kernel for the NVIDIA

                                                2
Exo-GPU: Safe, Imperative, User-schedulable Programming for Tensor Cores


Hopper architecture, with every step of transformation verified via a chain of equivalence: Exo ver-
ified equivalence between the original 𝑝 1 and the final 𝑝𝑛 while ignoring all the synchronization
constructs, and Exo-GPU verified functional equivalence between the parallel and sequential in-
terpretations of 𝑝𝑛 , checking the legality of the parallel and synchronous annotations (Section 2.3).
Combining Exo’s pre-existing checked rewrite rules with Exo-GPU’s new language features and
synchronization checking, we created a GEMM kernel achieving over 80% of theoretical peak for
large problem sizes, in some cases outperforming the vendor-supplied CUBLAS library (Section 6).

2 EXAMPLES AND SYSTEM OVERVIEW
2.1   Exo-GPU Language Overview
Exo-GPU is built on fundamental design goals of safe, performance transparent, and imperative
GPU programming. Unlike other GPU abstractions that hide complexity, we make threads and
most CUDA instructions explicit in the IR. We introduce three first-class frontend language fea-
tures derived from our design principles: (i) parallel loops that explicitly map work to blocks, warps,
or threads, (ii) a distributed memory model with sharding and explicit memory space annotations,
and (iii) explicit synchronization, including fences, split-barriers, and asynchronous operations.
   Parallel loops. Exo-GPU exposes three kinds of loops.
(1) seq(𝑐𝑙𝑜 , 𝑐ℎ𝑖 ) is a sequential loop that iterates 𝑖 from 𝑐𝑙𝑜 to 𝑐ℎ𝑖 − 1.
(2) cuda_tasks(𝑙𝑜, ℎ𝑖) distributes iterations across CUDA clusters; on pre-sm_90 (H100) GPUs a
cluster coincides with a single CTA (thread block).
(3) cuda_threads(𝑙𝑜, ℎ𝑖, unit = 𝜏𝑢 ) assigns iterations to subsets of threads inside the current
cluster.
The unit takes a parameter 𝜏𝑢 that specifies the shape of the participating thread set but not con-
crete indices—for example, 𝜏𝑢 = cuda_warp denotes contiguous 32‑thread groups with thread IDs
0–31, 32–63, 64–95, etc. (inclusive), while 𝜏𝑢 = cuda_thread denotes a single thread (see Figure 11).
   Each loop body, conditional branch, with-block, or proce- for blk in cuda_tasks(0, 37):
dure defines a program scope. As part of collective analysis (Sec-         # scope-1 (CTA-scope)
tion 4), we annotate each scope with a collective tiling 𝜔 ∈ Ω.            for w in cuda_threads(0, 4,
                                                                                         unit=cuda_warp):
This describes a mapping between the control variable values                  # scope-2 (warp-scope)
and the thread collective (set of threads) assigned to execute                for t in cuda_threads(0, 32,
statement instances in the scope (i.e. which threads execute                             unit=cuda_thread):
which loop iterations). We say that a scope is a 𝜏𝑢 -scope when                 # scope-3 (thread-scope)
𝜏𝑢 accurately describes the thread sets produced by the mapping. In the inset figure, the outer-
most parallel loop cuda_tasks(0,37) creates scope�1 (which is a cluster scope, and, assum-
ing clusterDim=1, also a CTA scope); nesting cuda_threads(..., unit=cuda_warp) creates
scope�2 (warp scope); and nesting cuda_threads(..., unit=cuda_thread) creates scope�3
(single‑thread scope). Statement instances in scope�3 are executed by one thread.
   Distributed Memory: Exo-GPU exposes explicit allocation statements for data and barrier
variables, annotated by memory type, e.g. x : f32[8] @ CudaRmem allocates a data array x of
type f32 and size 8 in GPU register memory. Allocations can be distributed: a single logical object
may be sharded across threads at multiple CUDA levels (e.g., per-thread register shards or per-CTA-
in-cluster shared-memory shards). Threads must access only their owned shards except via explicit
communication instructions (e.g., warp shuffles) or TMA multicast. This sharding is not annotated
explicitly at the allocation, but deduced from the usage pattern of the variable; all deductions must
be consistent, as enforced by distributed memory analysis (Section 4.1).




                                                        3
                                                David Zhao Akeley, Yuka Ikarashi, and Jonathan Ragan-Kelley

                                                                    tmp: f32 @ CudaRmem     # Register
   Inset right illustrates the motivation for this design. If the for i in cuda_threads(0, 32,
first loop was executed sequentially, tmp would hold A[31]                     unit=cuda_thread):
                                                                      tmp = A[i]
after the first loop, so the second loop broadcasts that value for i in cuda_threads(0, 32,
to every B[i]. Languages like CUDA that implicitly duplicate                   unit=cuda_thread):
local variables per thread would interpret the same code as a         B[i] = tmp
vector copy (B[i] = A[i]). While not necessarily error-prone, this design would be inappropriate
for our goal of defining program behavior with sequential semantics. Hence, in Exo-GPU, storing
a temporary value per-thread requires a sharded allocation of tmp; as written, the program is re-
jected by the analysis because a register-resident tmp cannot be read by different threads without
(for example) a warp shuffle. If a user intends to express a vector copy (B[i] = A[i]) through reg-
ister tmp, tmp requires explicit distributed allocation per thread (tmp:f32[32]) and the accesses
must be per-thread (tmp[i]).
   Explicit Synchronization: Many GPU instructions require additional explicit synchronization,
but overly conservative barriers can cancel the performance benefits of concurrency. Exo-GPU
provides two forms of synchronization: a blocking barrier via Fence, and split barriers via paired
Arrive/Await. As with other statements, all synchronization statements execute in program order.
   A Fence causes all threads in the cur- # Code at CTA-scope, with blockDim=128
rent thread collective (warp, CTA, or clus- buf: f32[128] @ CudaSmemLinear
ter) to rendezvous. At warp scope it maps for tid in cuda_threads(0, 128,
to __syncwarp; at CTA scope it maps to ↩→ unit=cuda_thread):
                                                     buf[tid] = gmem[tid]
__syncthreads (as shown in the right-hand # __syncthreads
code inset). A Fence takes two synchronization– Fence(cuda_in_order,cuda_in_order)
                          pre    post
timeline parameters, 𝜏𝑠 and 𝜏𝑠 (Figure 16). for tid in cuda_threads(0, 128,
These timelines specify which memory opera- ↩→ unit=cuda_thread):
tions (sync and/or async) before and after the       accum: f32 # Each thread sums up buf[...]
                                                     accum = 0
fence must be ordered, and the compiler emits        for i in seq(0, 128):
the minimal combination of synchronization             accum += buf[i]
and memory-fence instructions required to sat-
isfy them. The cuda_in_order timeline specifies that the effects of async instructions are not
synchronized; only typical synchronous instruction effects are. If we were to, for example, re-
place the loads into shared memory with cp.async operations, the first parameter must be set to
Sm80_cp_async so that the copy operations preceding the fence are completed before execution
proceeds.
   Split barriers use a shared barrier-typed variable 𝑧, declared for tid in cuda_threads(0, 128,
as 𝑧: barrier @ 𝜋𝑏 , where 𝜋𝑏 selects the completion mecha-                       unit=cuda_thread):
nism (commit group, mbarrier, or cluster sync). Programmers            ...
express a split barrier statement pair with Arrive(𝜏𝑠pre ) >> 𝑧 bar: barrier @ CudaMbarrier
and Await(𝑧, 𝜏𝑠post ). The statement pairing is determined by Arrive(cuda_in_order) >> bar
                                                                     # ... insert work here
the shared barrier variable 𝑧. A matching pair orders memory Await(bar, cuda_in_order)
                                             pre
operations prior to Arrive (filtered by 𝜏𝑠 ) with those after for tid in cuda_threads(0, 128,
                      post
Await (filtered by 𝜏𝑠 ). The right-hand inset illustrates replac-                 unit=cuda_thread):
ing the earlier Fence example with an mbarrier-based split bar-        ...
rier.




                                                 4
Exo-GPU: Safe, Imperative, User-schedulable Programming for Tensor Cores


2.2   Exo-GPU Examples with Erroneous Synchronization
To motivate our language design, we build up a series of increasingly subtle, hard-to-identify inter-
and intra-thread synchronization bugs; all would be rejected by synchronization checking (Sec-
tion 5). Variables prefixed with some_* are allocated outside the code snippet, some_in_order_op
represents non-async work, and example_tma_multicast and example_wgmma are simplified place-
holders for actual TMA (tile copy) and wgmma (tensor core) instructions.
   The first example illustrates an inter-thread synchronization bug involving a cluster with 2
CTAs:
B: f32[2, 256, 32] @ CudaSmemLinear # Distributed mem: B[0,:,:] on CTA 0; B[1,:,:] on CTA 1
for cta in cuda_threads(0, 2, unit=cuda_cta_in_cluster):
    some_in_order_op(B[cta, :, :])
    Fence(cuda_in_order, cuda_in_order) # __syncthreads
example_tma_multicast(B[:,:,:], some_gmem[:,:]) # Copy some_gmem[:,:] to B[0,:,:] and B[1,:,:]

The example_tma_multicast instruction is implemented by threads in the 2 CTAs cooperating to
fill each others’ shared memory; however, this cooperation does not entail implicit synchronization
between the two CTAs. Since the Fence statement, as placed in CTA-scope, only synchronizes
threads within a CTA, it is possible that threads in CTA 0 proceed to the multicast instruction,
filling the SMEM of CTA 1 (B[1,:,:]), while threads in CTA 1 are still reading from it while
executing some_in_order_op. Although the TMA instruction is async, this is not relevant to the
bug illustrated here, as the TMA appears after the in-order operations upon which it races with.
    The next example illustrates an intra-thread synchronization bug:
D: f32[2, 2, 64, 256] @ Sm90_RmemMatrixD(64, 256) # Distributed: D[x,y,:,:] on CTA x, warpgroup y
for cta in cuda_threads(0, 2, unit=cuda_cta_in_cluster):
    for wg in cuda_threads(0, 2, unit=cuda_warpgroup):
        example_wgmma(D[cta, wg, :, :], some_A[:, :], some_B[:, :]) # D += matmul(A, B)
        some_in_order_op(D[cta, wg, :, :])

This code parallelizes across CTAs and warpgroups, with each warpgroup accessing only its own
shard D[cta, wg, :, :]. Nevertheless, the code is flawed, as the async example_wgmma instruc-
tion isn’t waited-for before some_in_order_op attempts to access its output.
   A more subtle bug arises when async instructions interact with inter-thread synchronization:
  B: f32[2, 256, 32] @ Sm90_SmemSwizzled(128)        # Distributed: B[x,:,:] on CTA x
  D: f32[2, 2, 64, 256] @ Sm90_RmemMatrixD(64, 256) # Distributed: D[x,y,:,:] on CTA x, warpgroup y
  cg: barrier[2, 2] @ CudaCommitGroup                # Distributed: cg[x,y] for CTA x, warpgroup y
  for cta in cuda_threads(0, 2, unit=cuda_cta_in_cluster):
      for wg in cuda_threads(0, 2, unit=cuda_warpgroup):
          some_in_order_op_1(B[cta, :, :])
          example_wgmma(D[cta, wg, :, :], some_A[:,:], B[cta, :, :]) # D += matmul(A, B)
          Arrive(wgmma_async) >> cg[cta, wg]
  cs: barrier @ CudaClusterSync
  Arrive(cuda_in_order) >> cs
  for cta in cuda_threads(0, 2, unit=cuda_cta_in_cluster):
      for wg in cuda_threads(0, 2, unit=cuda_warpgroup):
          Await(cg[cta, wg], cuda_in_order, 0)
          some_in_order_op_2(D[cta, wg, :, :])
  Await(cs, cuda_in_order, 0)
  example_tma_multicast(B[:,:,:], some_gmem[:,:]) # Copy some_gmem[:,:] to B[0,:,:] and B[1,:,:]
The statements connected in blue on the left illustrate safe synchronization in a situation similar
to our first example: the Arrive/Await pair using cs (cluster sync) ensures all accesses to B by
some_in_order_op_1 finish before any thread in the cluster overwrites B using TMA. The state-
ments connected in blue on the right illustrate safe synchronization in a situation similar to our

                                                        5
                                                 David Zhao Akeley, Yuka Ikarashi, and Jonathan Ragan-Kelley


second example: the Arrive/Await pair using cg (commit group) ensures each warpgroup waits
for its example_wgmma to finish before accessing D[cta, wg...] in some_in_order_op_2.
   However, the bolded access to B by example_wgmma is unsafe. Dotted red arrows illustrate syn-
chronization that does not happen. Because the Arrive on cs uses the timeline cuda_in_order,
the completion of the Arrive does not depend on the prior async wgmma instructions to retire.
Meanwhile, the Await on cg (commit group) occurs too late for it to interact transitively with the
prior cs (cluster sync) Arrive. Therefore, while all non-async accesses to B will retire before any
thread proceeds to the TMA multicast, this isn’t the case for the async wgmma instructions, whose
B operand could be overwritten unexpectedly by another CTA multicasting to its input memory.
Subtle bugs like this can be difficult to spot in optimized CUDA code.


2.3   Optimization Process and Equivalence Checking
Exo-GPU programmers can either directly write optimized object code or apply a sequence of
scheduling transformations to simple initial code. Both approaches grant full control over performance-
critical details. However, the scheduling approach offers significant practical advantages for per-
formance engineering: optimization strategies become reusable functions across similar kernels,
complex transformations decompose into sequences of verified primitives that enable rapid iter-
ation with correctness guarantees, and the compiler automatically handles complex index calcu-
lations for tiling strategies—especially valuable for GPU optimization. Below, we describe Exo-
GPU’s scheduling-based optimization process.
   The scheduling flow in Exo-GPU begins with a simple initial procedure 𝑝 1 . The programmer
issues a series of rewrite operations 𝑅1 … 𝑅𝑁 −1 to create transformed procedures 𝑝 2 ...𝑝 𝑁 .
                         𝑅1                    𝑅𝑁 −1
 Rewrites:       𝑝1      −−→  𝑝2      … −−−−→    𝑝𝑁      (Exo-GPU checks)                 𝑝𝑁
 Behavior:    seq J𝑝 1 K ≡ seq J𝑝 2 K …   ≡   seq J𝑝 𝑁 K        ≡                       par J𝑝 𝑁 K
Exo’s scheduling rewrite verifies functional equivalence of seq J𝑝 1 K ...seq J𝑝 𝑁 K under sequential se-
mantics (denoted seq J...K). Exo-GPU adds new scheduling operations for parallel and synchroniza-
tion constructs, but these non-semantics-altering annotations are ignored under seq J...K checks.
Then Exo-GPU performs additional verification on the final program 𝑝 𝑁 . Specifically, synchroniza-
tion checking ensures seq J𝑝 𝑁 K ≡ par J𝑝 𝑁 K, where par J...K denotes parallel semantics. Transitively,
this completes the chain of equivalence from seq J𝑝 1 K ≡ ... ≡ seq J𝑝 𝑁 K ≡ par J𝑝 𝑁 K, guaranteeing
that 𝑝 1 ’s behavior is preserved throughout all transformations.
   Equivalence checking relies on three categories of reasoning:
   Exo Rewrites: Exo’s existing rewrites implement dependency analysis-based equivalence check-
ing, which guards against dataflow logic bugs. For example, reorder_stmts, which reorders two
statements 𝑠 1 ; 𝑠 2 , is only permitted when the effects of the statements commute.
   Instruction Substitution: Explicit instruction selection rewrite (replace) lets programmers
substitute a code block with an accelerator instruction call. Exo-GPU models instructions via their
behavior (sequential semantics), per-parameter memory type (physical memory and layout), ex-
pected collective unit 𝜏𝑢 , and async annotations. Exo’s unification verifies that the replaced code
block’s behavior matches the instruction, while Exo-GPU’s static analysis ensures appropriate
threads execute it (Section 4.1); together preventing instruction logic errors.
   Exo-GPU Synchronization Check: Since parallel loops and synchronization statements (Fence,
Arrive, and Await) are ignored during sequential checks, synchronization checking must ensure
that their usage is valid and does not alter program behavior or introduce race conditions. We ver-
ify this via interpretation on the Abstract Machine (Section 5), which protects the program against
both inter- and intra-thread synchronization bugs for selected concrete problem sizes.

                                                   6
Exo-GPU: Safe, Imperative, User-schedulable Programming for Tensor Cores


      𝑣 : Var F 𝑥 ∈ X                               data variable
               | 𝑦∈Y                                control variable
               | 𝑧∈B                                barrier variable         𝑐 : CExpr F 𝑛                               integer
               | 𝑟 ∈W                               warp variable                       | 𝑦                              reads
                                                                                        | 𝑐 1 +𝑐 2 | 𝑐 1 −𝑐 2 | 𝑐∗𝑛      affine arith
  𝑒 : DExpr F 𝑑                                          data value
                                                                                        | 𝑐 / 𝑛 | 𝑐 mod 𝑛                quasi affine
             | 𝑥 | 𝑥[𝑤 ∗ ]                               reads
             | 𝑒 1 +𝑒 2 | 𝑒 1 −𝑒 2 | 𝑒 1 ∗𝑒 2 | 𝑒 1 /𝑒 2 compound expr       𝑏 : BExpr F 𝑡                                 boolean
                                                                                        | 𝑏 1 and 𝑏 2 | 𝑏 1 or 𝑏 2         logical ops
 𝑒z   : ZExpr F 𝑧 | 𝑧[𝑤 ∗ ]                         reads
                                                                                        | 𝑐 1 == 𝑐 2 | 𝑐 1 <𝑐 2 | 𝑐 1 ≤𝑐 2 relational ops
𝑒 w : WExpr F 𝑟 = (𝑛, 𝑛, 𝑛)                         warp config
                                                                         𝑤 : WinCoord F 𝑐                                point access
           𝑛   ∈ Z                                  integer                            | 𝑐 1 ..𝑐 2                       interval access
           𝑡   ∈ Bool                               boolean
           𝑑   ∈ D                                  data values

           Fig. 1. The syntax of variables and expressions of GPU IR. We use ·∗ to mean 0 or more.

3 GPU IR
GPU IR is the frontend language of Exo-GPU, and examples in Section 2 are written in GPU IR.
3.1     Variables and Expressions
Figure 1 defines the expression syntax of GPU IR. GPU IR explicitly distinguishes between control,
data, barrier, and warp expressions and is a static control program. We denote the sets of data,
control, barrier, and warp variables by X, Y, B, W, respectively. 𝑥 ∈ X is a data variable, 𝑦 ∈ Y
is a control variable, 𝑧 ∈ B is a barrier variable, and 𝑟 ∈ W is a warp variable. The truth values
Bool ≜ {true, false}. are ranged over by a metavariable 𝑡, and 𝑛 is the metavariable for Z ≜
{· · · , −1, 0, 1, 2, · · · }. The metavariable 𝑑 ∈ D ranges over data values, including 8-, 32-, and 64-bit
integers as well as single- and double-precision floating-points.
   Control expressions CExpr encompass integer, scalar read, and (quasi-) affine arithmetic opera-
tions. Boolean expressions BExpr define basic logical and relational operations on control expres-
sions. Data expressions DExpr are similarly defined, but operations need not be affine. Barrier
Expressions ZExpr are only allowed to read, but not composed. Window coordinates 𝑤 ∗ (we use
.∗ to denote a tuple) used in data and barrier read accesses are specified as a tuple of point-wise
or interval control expressions, expressing a windowed access to multi-dimensional arrays. Scalar
read is syntactic sugar for an array access of 𝑤 ∗ = h i (empty tuple).
3.2     Types
All types are fully defined in Appendix A. This section provides a general introduction to the dif-
ferent types in GPU IR. Figure 10 defines data and barrier types. Data types 𝜏𝑥 specify precisions
for data variables X, such as f32 and i32. Barrier types 𝜏𝑧 distinguish a non-explicitly guarded
barrier from an explicitly guarded barrier (barrier(z)); the explicitly guarded barrier case is re-
quired only for mbarriers.1 A collective type (𝛿 ∈ Δ) defines a tuple consisting of a domain and a
box, each representing 𝑑- dimensional natural numbers ((N𝑑 , N𝑑 )). Together, these define a 𝑑-level
thread hieararchy within a thread cluster, and a selection of a number of elements on each level.
An argument to cuda_threads loop 𝜏𝑢 is parameterized by a collective type 𝛿, which is defined in
Figure 11. Figures 12–14 classify three categories of memory spaces: 𝜋d for data memories (such
as CudaRmem for CUDA registers), 𝜋z for barrier completion mechanisms (such as mbarrier or
commit_group), and 𝜋w for special window aliasing (such as CUtensorMap). Similar to 𝜏𝑢 , 𝜋d is
parameterized by 𝛿.

1 This requirement has been removed from newer Exo-GPU versions.



                                                                   7
                                                       David Zhao Akeley, Yuka Ikarashi, and Jonathan Ragan-Kelley


        𝑠 : Stmt F 𝑠 1 ;𝑠 2                                          sequencing
                  | for 𝑦 in seq(𝑐 lo ,𝑐 hi ) do 𝑠                   sequential loop
                  | for 𝑦 in cuda_tasks(𝑐 lo ,𝑐 hi ) do 𝑠            cuda tasks
                  | for 𝑦 in cuda_threads(𝑐 lo ,𝑐 hi ,unit=𝜏𝑢 ) do 𝑠 cuda threads
                  | with CudaDeviceFunction(𝑛, 𝑒 w   ∗ ) do s        CUDA device function block
                  | with CudaWarps(𝑛, 𝑛, 𝑟 ) do s                    warp specialization block
                  | if 𝑏 then 𝑠                                      guard
                  | 𝑝 (𝑐 ∗ , 𝑒 ∗ )                                   non-instruction subprocedure call
                  | 𝑔 (𝑐 ∗ , 𝑒 ∗ ) >> 𝑒 z                            instruction subprocedure call
                  | 𝑥[𝑐 ∗ ] = 𝑒                                      write
                  | 𝑥[𝑐 ∗ ] += 𝑒                                     reduce
                  | 𝑥 = 𝑥 [𝑤 ∗ ] @ 𝜋w                                window statement
                  | 𝑥 : 𝜏𝑥 [𝑐 ∗ ] @ 𝜋d                               data alloc
                  | 𝑧 : 𝜏𝑧 [𝑐 ∗ ] @ 𝜋z                               barrier alloc
                  | free 𝑥                                           data free
                  | free 𝑧                                           barrier free
                  | Fence(𝜏𝑠 , 𝜏𝑠 )                                  non-split barriers
                  | Arrive(𝜏𝑠 , 𝑛) >> 𝑒 z∗                           arrive
                  | Await(𝑒 z , 𝜏𝑠 , 𝑛)                              await
         𝜏𝑎 : Arg F 𝜏𝑥                                                     data type (precision)
                   | 𝜋d                                                    data memory type
                   | out_of_order ∈ Bool                                   out-of-order execution flag
                   | convergent ∈ Bool                                     implicit thread sync flag
                   | 𝜏𝑢∗                                                   distributed collective units
                   | initial_qual_tl ∈ QualTL                              initial qualitative timeline
                   | ext_qual_tl ∈ P (QualTL)                              extended qualitative timeline set
                   | atomic_qual_tl ∈ P (QualTL)                           atomic qualitative timeline set
                       proc 𝑦 ∗ , (𝑥 : 𝜏𝑥 @ 𝜋𝑑 ) ∗                   proc 𝑦 ∗ , (𝑥 : 𝜏𝑎 ) ∗ , 𝑡, 𝜏𝑢 , 𝜋 z , 𝜏𝑢∗
          𝑝 : Proc F                                   𝑔 : Instr F
                       do 𝑠                                           do 𝑠

                                     Fig. 2. The syntax of GPU IR statements.
   A qualitative timeline 𝜏𝑞 annotates each runtime buffer access. We define distinct 𝜏𝑞 to dis-
tinguish between buffer accesses that require different synchronization mechanisms or memory
fences to resolve hazards. For example, we distinguish non-async copies from cp.async copies
(which require cp.async.wait_all or similar to wait for), and we distinguish register and SMEM
operands of wgmma instructions (which require wgmma.fence and fence.proxy.async, respec-
tively). Section 5 will formally define how a runtime buffer access instance 𝑥 [𝑖 1, . . . , 𝑖𝑛 ] tagged
with 𝑞 1 states that, at the program point and thread, the access to 𝑥 occurs under 𝑞 1 . Moreover, the
sync timelines SyncTL mentioned in Section 2.1, which parameterize synchronization statements,
are actually defined as compositions of qualitative timelines (QualTL), as shown in Figure 16.
3.3   Programs
Exo-GPU supports two types of procedures, 𝑝 : Proc, which models CPU functions (possibly
containing CUDA kernel launches), and 𝑔 : Instr, which models hardware instructions for either
CPU or CUDA. Both procedure types share three common components: a statement body that
defines sequential behavior, a tuple of control parameters 𝑦 ∗ , and a tuple of data parameters 𝑥 ∗ .
Each data parameter in Proc carries two annotations: 𝜏𝑥 , specifying the required data precision,
and 𝜋𝑑 , specifying the required memory type for the passed argument.
   Instruction parameters (𝜏𝑎 ) also carry both 𝜏𝑥 and 𝜋𝑑 annotations, as well as hardware-specific
information, namely: out-of-order, convergence, and qualitative timeline information, which all
affect only abstract machine semantics for checking (Section 5). The 𝜏𝑎 also contains a distributed
collective units tuple (𝜏𝑢∗ ) specifying the CUDA thread hierarchy at which each array dimension is

                                                        8
Exo-GPU: Safe, Imperative, User-schedulable Programming for Tensor Cores


sharded (checked by distributed memory analysis, Section 4.1). The instruction (𝑔) contains anno-
tations for 𝑡 (a CPU/CUDA flag), a collective unit 𝜏𝑢 specifying the convergent threads required,
and 𝜋𝑧 and 𝜏𝑢∗ .




3.4   Statements
Figure 2 defines statements 𝑠 ∈ Stmt. A statement can sequence (𝑠 1 ; 𝑠 2 ), iterate over loops (seq,
cuda_tasks, or cuda_threads), and guard (if 𝑏 then 𝑠). Data effects include indexed writes
𝑥 [𝑐 ∗ ] = 𝑒, reductions 𝑥 [𝑐 ∗ ]+= 𝑒, and window creation 𝑥 = 𝑥 [𝑐 lo : 𝑐 hi ] @ 𝜋w . CudaDeviceFunction
and CudaWarps control generation and selection of CUDA threads. Synchronization statements
Fence, Arrive, and Await get lowered to CUDA synchronization and proxy fence instructions.
   CUDA Kernel Structure: All Exo-GPU with CudaDeviceFunction(...):
code is compiled as CPU code by default. A                  for cta_m in cuda_tasks(...):
CudaDeviceFunction block specifies a CPU-                       for cta_n in cuda_tasks(...):
                                                                     # Device task starts here
side launch of a CUDA kernel. Its body must                          A_smem: f32[128, 32] @
contain only a single statement: a nest of one                       ↩→ CudaSmemLinear
or more cuda_tasks loops; cuda_tasks loops                           # ...
must not appear elsewhere. Each iteration of the inner-most cuda_tasks loop comprises a de-
vice task and is assigned to one CUDA cluster for execution. The device scope of a statement is
CPU if outside of a CudaDeviceFunction block, and CUDA if inside. At CPU scope, all loops
must have loop mode seq. The arguments of CudaDeviceFunction(𝑛, 𝑒 𝑤               ∗ ) respectively define the

clusterDim and, indirectly, the blockDim of the CUDA clusters launched. Each warp expression
𝑒 𝑤 : 𝑟 = (𝑛, 𝑛, 𝑛) defines a group of warps named 𝑟 , with the first 𝑛 parameter being the number of
warps. If nonzero, the latter two 𝑛 parameters specify that the warps will adjust the register count
down or up, respectively, using a setmaxnreg.dec or setmaxnreg.inc instruction [18]. We infer
that blockDim is 32 times the total number of warps named.
   Thread Control: Having described the
cuda_tasks loops (inter-cluster parallelism), my_warp_config = [
                                                        CudaWarpConfig("producer", 1, 40, 0),
we now describe cuda_threads loops and
                                                        CudaWarpConfig("unused",         3, 40, 0),
with CudaWarps (intra-cluster parallelism). A           CudaWarpConfig("consumer", 8, 0, 232)]
cuda_threads loop takes its executing thread with CudaDeviceFunction(clusterDim=2,
collective and sub-divides, assigning one subdi-           warp_config=my_warp_config):
vision of threads to execute each loop iteration Fig. 3. Launching clusters of 2 CTAs each, with 1 “pro-
(possibly with left-over, inactivated threads). ducer”, 3 “unused”, and 8 “consumer” warps per CTA
The unit parameter adjusts the number of (total blockDim=384). The consumer warps have 232
                                                      registers per thread, and the others only 40.
threads per iteration. The CudaWarps(𝑛, 𝑛, 𝑟 )
block restricts its body statement to execute only with threads residing in the warp variable named
by 𝑟 (which is defined in the CudaDeviceFunction); the numeric arguments further restrict the
warps selected.
   Proc & Instruction Calls: Calls to 𝑝 : Proc and 𝑔 : Instr are syntactically similar, distinguished
only by the callable’s type. Exo-GPU’s static analysis enforces that calls to 𝑝 : Proc only appear at
CPU scope, while calls to 𝑔 : Instr appear at CPU or CUDA scope as appropriate for 𝑔. For CUDA
instructions, calls to 𝑔 must only appear at 𝜏𝑢 -scope, where 𝜏𝑢 is the collective unit specified for
𝑔. Additionally, each data parameter must have the correct precision 𝜏𝑥 and memory type 𝜋𝑑 , and
the trailing barrier (if required) must have the correct 𝜋𝑧 .



                                                        9
                                                  David Zhao Akeley, Yuka Ikarashi, and Jonathan Ragan-Kelley


    Synchronization Statements: The user specifies synchronization between threads and/or be-
tween async accelerator instructions by inserting synchronization statements. They take synchro-
nization timeline (SyncTL) parameters, defined as compositions of qualitative timelines and a tran-
sitivity (trnstv?) flag (Figure 16). The transitivity flag controls interaction between synchronization
statements, detailed in Section 5.
    Each 𝜏𝑠 : SyncTL contains two QualTL sets: the full timeline set (indicated by “full” in (Fig-
                                                                                     pre post
ure 16), and a temporal timeline set (indicated by “full” or “temp.”). A Fence(𝜏𝑠 , 𝜏𝑠 ), or paired
            pre                     post
Arrive(𝜏𝑠 ,_) and Await(_, 𝜏𝑠 ,_) statements, resolves hazards between two accesses to the
same array element when: (1) the first access precedes synchronization and uses a QualTL from
  pre
𝜏𝑠 ’s full timeline set, and (2) the second access follows synchronization and uses a QualTL from
  post
𝜏𝑠 ’s full timeline set (for reads) or temporal timeline set (for writes). In hardware terms, the dis-
tinction between the full and temporal timeline sets is due to memory fences. If the prior value of a
buffer element is overwritten, without being read, we require only that the overwrite is temporally
ordered after prior accesses to that buffer element, and memory fences may be elided.
    Alloc & Free: An allocation statement begins the lifetime of a new data or barrier variable. For
data allocations, the data memory 𝜋𝑑 determines the physical backing memory (registers (RMEM),
shared memory (SMEM), or global memory (GMEM)) and the mapping between multidimensional
tensor coordinates and 1D memory offsets (Figure 12). It also carries an implicit collective type
𝛿, specifying which level of the thread hierarchy at which the physical memory type is allocated
(e.g. CTA for shared memory allocations); this is consumed by distributed memory analysis (Sec-
tion 4.1). For barrier allocations, the BarrierComp parameter 𝜋𝑧 controls the completion mecha-
nism used for CUDA code translated from Arrive and Await statements (Figure 13). The explicitly-
guarded barrier type is relevant only for certain configurations of mbarrier usage. A free state-
ment ends the lifetime of a data or barrier variable. Currently, we forbid the user from inserting
free statements manually; these are added automatically in a separate compiler pass.
    Window Statement: A window statement 𝑥 win = 𝑥 data [𝑤 ∗ ] @ 𝜋 𝑤 defines an alias to 𝑥 data . A
window into 𝑥 win can be passed as an instruction argument which requires special window type
𝜋 𝑤 . Currently, we only use this feature to construct CUtensorMap objects [18] required for TMA
instructions; we parameterize the CUtensorMap type with its swizzle mode and box shape.

4 COLLECTIVE ANALYSIS
Collective analysis is a static, forward dataflow analysis over a GPU IR procedure. Its results
are consumed by (1) a memory analysis, (2) code generation, and (3) an abstract‑machine in-
terpreter. The analysis annotates every GPU lexical scope with a collective tiling 𝜔 ∈ Ω. By
default, statements inherit their parent’s tiling unchanged; a new tiling is derived only at: de-
vice entry (CudaDeviceFunction), thread loops (cuda_threads), and warp‑specialization blocks
(CudaWarps). The purpose of this analysis is to statically reason about the mapping between work
and the threads within clusters, so here we ignore cuda_tasks loops, which distribute work across
clusters. We uniquely identify a thread within a cluster by its natural thread index; a set of such
indices comprises a thread collective 𝜇 ∈ T, where T ≜ P (N).

Definition 4.1 (Natural thread index). The natural thread index for a CUDA thread is cluster_ctarank
* blockDim.x + threadIdx.x. (Exo-GPU only parallelizes on the x dimension).

Definition 4.2 (Collective tiling). A collective tiling 𝜔 ∈ Ω for an 𝑀-dimensional domain is an
𝑀‑tuple of dimension descriptors

                       𝜔 = hD0, . . . , D𝑀 −1 i    with       D𝑚 = (𝐷𝑚 , O𝑚 ),

                                                  10
Exo-GPU: Safe, Imperative, User-schedulable Programming for Tensor Cores


where 𝐷𝑚 ∈ N is the extent of dimension 𝑚 and O𝑚 ∈ O ∗ is an ordered list of (possibly empty)
dimension operators O : Y × N3 . We write the thread pitch of dimension 𝑚 as
                                               Ö
                                               𝑀 −1
                                     𝑃𝑚 ≜             𝐷𝑖 where 𝑃𝑀 −1 = 1
                                              𝑖=𝑚+1

  The dimensions of a collective tiling 𝜔 capture how a cluster’s threads are partitioned into hi-
erarchical collectives (cluster, block, warp). We support reshape to introduce ad-hoc additional
hierarchy (e.g. pairs of warps). From there, each dimension’s dimension operators summarize the
control variables (identified by 𝑦 ∈ Y) that iterate on that dimension. The thread pitch of the di-
mension describes the distance, in units of natural thread indices, between adjacent elements (e.g.
a CTA dimension would have thread pitch blockDim).
  During forward dataflow analysis, new collective tilings are derived for the three special state-
ments mentioned above, while all other statements inherit their parent’s tiling. It produces a child
collective tiling through the following transformation:
                            derive𝜔 : (𝜔 env, 𝛿 stmt, 𝑦, lo, hi, tileCount) → 𝜔 0
where 𝜔 env is the parent scope’s collective tiling and 𝛿 stmt is the collective type from the state-
ment. The (optional) iterator 𝑦 and bounds [lo, hi) describe a regular slice of linear thread space;
tileCount ∈ N is the number of tiles for that slice. The details of derive𝜔 are left for future work.
   The cuda_threads loop and CudaWarps block use derive𝜔 to create a new collective tiling 𝜔
based on the one annotating the parent scope. The CudaDeviceFunction block derives 𝜔 based
on launch parameters: 𝜔 is 1‑D if clusterDim= 1 (domain 𝐷 0 =blockDim), otherwise 2‑D with
(𝐷 0, 𝐷 1 )=(clusterDim, blockDim); all operator lists start empty.
   The implementation of derive𝜔 proceeds in two steps:
    (1) Shape alignment. Make 𝜔 env and 𝛿 stmt compatible by reshaping via hierarchical splits so
        that their thread pitches 𝑃𝑚 align.
    (2) Single‑dimension refinement. After alignment, at most one dimension 𝑚 is newly tiled; the
        derivation appends exactly one operator to O𝑚 .
  Once a tiling 𝜔 is derived, it is compiled into a thread mapping: 𝑓𝜔 : Σ → T, where Σ ≜ (Y → Z)
which maps a control environment 𝜎 ∈ Σ to a runtime thread collective 𝜇 ∈ T. Equivalently, let
F ≜ { 𝑓 | 𝑓 : Σ → T } and 𝑓𝜔 ∈ F . During conversion, each Abstract Machine statement 𝑠 # is
annotated with its thread mapping 𝑓𝑠 # ∈ F . In Section 5.3 we write 𝑓𝑠 # for the thread mapping
associated with statement 𝑠 # .

4.1 Distributed Memory Analysis
Distributed memory analysis is a static, program-wide consistency check that ensures every use
of CUDA-scoped data and barrier variables is compatible with their memory definitions. Each
memory type 𝜋𝑑 specifies a collective type 𝛿 𝜋𝑑 . The analysis validates that allocation and use agree
on which threads “own” which memory slices, indexing respects that ownership, and all uses
induce the same mapping from logical indices to CUDA thread identifiers. Analysis runs in four
steps:
    (1) Desugaring instruction call. To expose the implicit collective requirement encoded by
        each hardware instruction to the collective analysis in step 2, we rewrite instruction calls
        𝑔(· · · ) into explicit loops. Each arguments to the instruction call are wrapped around with
        cuda_threads, with their collective units specified by 𝑔.𝜏𝑢∗ in the instruction specification.
    (2) Collective analysis. Run collective analysis and annotate each scope with 𝜔 ∈ Ω.

                                                        11
                                                  David Zhao Akeley, Yuka Ikarashi, and Jonathan Ragan-Kelley


   (3) Triple collection. For each data or barrier variable, record the access triple of all of use
       sites. We use T𝑣 to denote a set of those triples for a variable 𝑣; these sets for all the data and
       barrier variables are the sole inputs to step 4. Each triple (𝑛 ∗, 𝜔, 𝑐 ∗ ) denotes: the subdivided
       dimensions 𝑛 ∗ , the use-site tiling 𝜔, and observed index coordinates 𝑐 ∗ . For each use site:
          • Data. Compute 𝑛 ∗ from the memory’s collective type 𝛿 𝜋𝑑 and the use-site tiling 𝜔.
          • Barriers. Treat all dimensions as subdivided (every axis participates in distribution).
   (4) Triple analysis. For each CUDA-scoped data variable 𝑣, we require: (i) consistency of the
       allocation w.r.t. the memory’s 𝛿 𝜋𝑑 , (ii) consistency of data or barrier accesses across sites
       (by checking all triples in T𝑣 ), and (iii) all triples in T𝑣 must derive one and only one thread
       pitch tuple that summarizes how incrementing logical indices advances natural thread IDs.
       The derivation will be detailed in future work.

As a result, distributed memory analysis rejects programs that (i) mismatch allocation and accesses
with their memory declaration, (ii) inconsistently index the same data or barrier across sites, or
(iii) rely on missing/extra CUDA-thread iterators. Passing guarantees that the program’s memory
behavior is coherent with its collective structure and declared memory types.

4.2 Code Generation to CUDA Code
   Lowering cuda_threads Loops: The corre- if (int y = f(blockIdx, threadIdx); g(y)) {
spondence between parallel loops and threads               lower(s);}
has thus far been expressed in terms of thread mappings of type Σ → T, which infer a set of
active threads from the control environment 𝜎. However, the generated CUDA C++ implements
the inverse of this mapping, inferring the value of a control variable y from the thread index in-
stead. Each Exo-GPU loop of the form for y in cuda_threads(lo, hi, unit=𝜏𝑢 ) do s lowers
to CUDA C++ as shown in the inset right. Here, f is a function of CUDA’s built-in blockIdx and
threadIdx variables, and g is a boolean condition on y that disables threads not assigned to execute
any iteration of the body. Where possible, f is 0 and g is 1, to facilitate uniform branching.
   Warp Specialization: When a device function uses multiple warp variables 𝑟 1, ..., 𝑟𝑊 ∈ W,
we generate 𝑊 -many CUDA C++ code paths from a single Exo-GPU device function, each spe-
cialized for (and executed by) the threads assigned to one warp variable. Each path uses PTX’s
setmaxnreg instruction to vary per-thread register counts, and omits all code paths guarded by a
with CudaWarps block holding code not intended for the current warp. This allows the PTX assem-
bler to statically verify that register-heavy instructions (e.g. wgmma) don’t appear on low-register
code paths.
   Persistent Kernels and cuda_tasks Loops: The generated CUDA C++ device functions imple-
ment a persistent kernel design that launches exactly the number of thread block clusters needed
to saturate the device. Following the approach of CUTLASS grouped kernel schedulers [16], we
implement a C++ task generator object that generates a series of device task coordinates for thread
block clusters to execute. The current implementation orders tasks lexicographically and assigns
them round-robin to thread block clusters for execution. While we leave it as future work to pro-
vide a mechanism for programmers to customize this ordering, such customization would be un-
constrained by frontend’s quasi-affine indexing restrictions since cuda_tasks loops impose no
semantic ordering, thereby enabling techniques like Morton swizzling.
   Shared Memory Allocations: Device functions generated by Exo-GPU use only dynamic
shared memory for SMEM allocation. The Exo-GPU compiler deduces the required SMEM alloca-
tion size and statically assigns offsets into this allocation for each SMEM-backed variable. Variables
with non-overlapping lifetimes may share the same memory locations; to ensure safe aliasing, we
prohibit any thread in the cluster from passing an SMEM free statement until all reads and writes

                                                   12
Exo-GPU: Safe, Imperative, User-schedulable Programming for Tensor Cores


                          fully_ordered | temporally_ordered
           𝜏𝑣 : VL F                                                          visibility levels
                          | unordered | atomic_only | invisible
       𝑒 # : Expr# F 𝑒𝑑# | 𝑒𝑧#         where 𝑒𝑑# ≜ 𝑥 [𝑤 ∗ ]      𝑒𝑧# ≜ 𝑧 [𝑤 ∗ ] barrier and data accesses
       𝑠 # : Stmt# F 𝑠 1# ;𝑠 2#                                               sequencing
                    | for 𝑦 in loop(𝑐 lo , 𝑐 hi ) do 𝑠 #                      loop
                    | if 𝑏 then 𝑠 #                                           guard
                    | IncTaskID                                               increments the task ID
                    | Alloc(𝑒 # )                                             updates SyncEnv for Alloc
                    | RecordRead(𝜏𝑣 , 𝑡, 𝑒 # , 𝜏𝑞 , 𝜏𝑞∗ , 𝑒 z# )              updates SyncEnv with Read
                    | RecordMutate(𝜏𝑣 , 𝑡, 𝑒 # , 𝜏𝑞 , 𝜏𝑞∗ , 𝑒 z# )            updates SyncEnv with Mutate
                    | ClearReads(𝑒 # )                                        removes state added by RecordRead
                    | ClearMutates(𝑒 # )                                      removes state added by RecordMutate
                    | Fence(𝑡, 𝜏𝑞∗ , 𝜏𝑞∗ , 𝜏𝑞∗ )                              non-split barriers
                    | Arrive(𝑡, 𝜏𝑞∗ , 𝑒 z#∗ )                                 arrive
                    | Await(𝑒 z# , 𝜏𝑞∗ , 𝜏𝑞∗ , 𝑛)                             await
                    | CheckReads(𝜏𝑣 , 𝑡, 𝑒 # , 𝜏𝑞∗ )                          checks visibility of Reads in SyncEnv
                    | CheckMutates(𝜏𝑣 , 𝑡, 𝑒 # , 𝜏𝑞∗ )                        checks visibility of Mutates in SyncEnv
                    | CheckBarrier(𝑒 z# )                                     checks the consistency of arrive and await
                          proc 𝑦 ∗
       𝑝 # : Proc# F                                                          arguments are control-only
                          do 𝑠 #

Fig. 4. Syntax of Abstract Machine IR (AMIR). Variables, types, and expressions (𝑐, 𝑏, 𝑤) use the same defini-
tion as GPU IR. Visibility levels are denoted by the type 𝜏𝑣 ∈ VL and range over the five constructors listed
above.

to the freed variable have retired, as enforced by the Abstract Machine (Section 5). This is neces-
sary because freed SMEM may be immediately reused by any thread in the cluster. We note that
the compiler’s aliasing may be suboptimal, and the cluster-wide safety requirement may be overly
conservative (e.g., for CTA-local variables). Providing programmers explicit control over SMEM
lifetime and aliasing is left as future work.
5 ABSTRACT MACHINE
To guarantee sequential–parallel equivalence, Exo-GPU performs synchronization checking via
Abstract Machine interpretation. This section introduces the AMIR grammar (Section 5.1), the
translation from GPU IR (Section 5.2), and the AMIR execution semantics (Section 5.3). We trans-
late GPU IR into AMIR solely for validation: the frontend language remains simple, while synchro-
nization reasoning is factored into explicit AMIR operations that are orthogonal to value compu-
tation.
5.1 Abstract Machine Grammar
Figure 4 defines AMIR grammar. It follows GPU IR for control 𝑐, booleans 𝑏, window coordinates
𝑤, and all variable/type definitions (Figures 1, 2). AMIR defines only windowed access expres-
sions, written 𝑒𝑑# ≜ 𝑥 [𝑤 ∗ ] (data access) and 𝑒 z# ≜ 𝑧 [𝑤 ∗ ] (barrier access). AMIR introduces vis-
ibility levels 𝜏𝑣 ∈ VL, which are totally ordered: invisible ≺ atomic_only ≺ unordered ≺
temporally_ordered ≺ fully_ordered.
   AMIR has no hardware-instruction procedures (𝑔 in GPU IR) and no subprocedure calls. Proce-
dures 𝑝 # take control-only arguments. The statement (Figure 4) consists of: (i) structural statements–
sequencing, loop, and guard (ii) recording statements that update the synchronization environ-
ment SyncEnv–Alloc, RecordRead, RecordMutate, Fence, Arrive, and Await; and (iii) checking
statements that query SyncEnv and fail if the required visibility obligations are not met; otherwise
they are no-ops: CheckBarrier, CheckReads, and CheckMutates.

                                                                     13
                                                               David Zhao Akeley, Yuka Ikarashi, and Jonathan Ragan-Kelley


 GPU IR                                          Abstract Machine IR
 𝑠1 ; 𝑠2                                         𝑇𝑠 (𝑠 1 ); 𝑇𝑠 (𝑠 2 )
 for 𝑦 in seq(𝑐 lo , 𝑐 hi ) do 𝑠                 for 𝑦 in loop(𝑐 lo , 𝑐 hi ) do 𝑇𝑠 (𝑠 )
 for 𝑦 in cuda_tasks(𝑐 lo , 𝑐 hi ) do 𝑠          for 𝑦 in loop(𝑐 lo , 𝑐 hi ) do (IncTaskID; 𝑇𝑠 (𝑠 ))
 for 𝑦 in cuda_threads(𝑐 lo , 𝑐 hi , 𝜏𝑢 ) do 𝑠   for 𝑦 in loop(𝑐 lo , 𝑐 hi ) do 𝑇𝑠 (𝑠 )
 𝑥 [𝑐 ∗ ]    𝑒        where  ∈ {=, +=}         ;𝑒1# ∈𝑇ex (𝑒 ) CheckMutates(𝜏𝑣pre, false, 𝑒1#, {𝑇qin (𝑒1# ) }));
                                                                                 post                                        
                                                                RecordRead(𝜏𝑣           , false, 𝑒 1# ,𝑇qin (𝑒 1# ), ∅, ∅)
                                                 ;                                   pre
                                                  𝑒 2# ∈𝑇ex (𝑥 [𝑐 ∗ ]) CheckReads(𝜏 𝑣 , false, 𝑒 2 , {𝑇qin (𝑒 2 ) }));
                                                                                                 #            #
                                                                                        pre
                                                                       CheckMutates(𝜏𝑣 , false, 𝑒 2 , {𝑇qin (𝑒 2# ) }));
                                                                                                     #

                                                                       ClearReads(𝑒 2# );
                                                                       ClearMutates(𝑒 2# );
                                                                                        post                                
                                                                       RecordMutate(𝜏𝑣 , false, 𝑒 2# ,𝑇qin (𝑒 2# ), ∅, ∅));
                                                                post
                                                 , where 𝜏𝑣 = fully-ordered and
                                                   pre
                                                 𝜏𝑣 = fully-ordered if +=, else temporally-ordered
 if 𝑏 then 𝑠                                     if 𝑏 then 𝑇𝑠 (𝑠 )
                              ∗ ) do 𝑠
 with CudaDeviceFunction(𝑛, 𝑒 w                  Fence(true, Qcs ∪ {cpu_in_order_qual}, Qcs, Tcs);
                                                 𝑇𝑠 (𝑠 );
                                                 Fence(true, Qcs, Qcs, Tcs);
                                                 , where Qcs ≜ Tqfull (cuda_stream_sync), Tcs ≜ Tqtmp (cuda_stream_sync)
 with CudaWarps(𝑛, 𝑛, 𝑟 ) do 𝑠                   if true then 𝑇𝑠 (𝑠 )
 𝑔 (𝑐 ∗ , 𝑒 ∗ ) >> 𝑒   z                         ;𝑒 # ∈𝑇ex (𝑒𝑧 ) RecordRead(fully-ordered, false, 𝑒 #, ∅, ∅,𝑇𝑒 (𝑒z ))
                                                  len(𝑒 ∗ )
                                                 ;𝑖=0       𝑇arg (𝑔.𝑝𝑖 , 𝑒𝑖 , 𝑒 z )
 𝑥 : 𝜏𝑥 [𝑐 ∗ ] @ 𝜋d                              Alloc(𝑥 [𝑐 ∗ ])
 𝑧 : 𝜏𝑧 [𝑐 ∗ ] @ 𝜋z                              Alloc(𝑧 [𝑐 ∗ ])
 free 𝑥                                          ;𝑒 # ∈𝑇smem (𝑥 [:∗ ]) CheckReads(𝜏𝑣free, false, 𝑒 #, {𝑇qin (𝑒 # ) })); 
                                                                        CheckMutates(𝜏𝑣free , false, 𝑒 # , {𝑇qin (𝑒 # ) }));

 free 𝑧                                          CheckBarriers( 𝑇𝑒 (𝑧 [:∗ ] ) );
                                                 ;𝑒 # ∈𝑇smem (𝑧 [:∗ ]) CheckReads(𝜏𝑣free, false, 𝑒 #, {𝑇qin (𝑒 # ) })); 
                                                                       CheckMutates(𝜏𝑣free , false, 𝑒 # , {𝑇qin (𝑒 # ) }));
             pre   post                                           pre            pre               post               post
 Fence(𝜏𝑠 , 𝜏𝑠             )                     Fence(Ttr (𝜏𝑠 ), Tqfull (𝜏𝑠 ), Tqfull (𝜏𝑠                ), Tqtmp (𝜏𝑠           ))
 Arrive(𝜏𝑠 , 𝑛) >> 𝑒 z∗                          ;𝑒 # ∈𝑇ex (𝑒 z∗ ) RecordRead(fully-ordered, false, 𝑒 , Tqarr (𝜏𝑠 ), ∅, ∅)
                                                                                                     #
                                                                                       ∗
                                                 Arrive(Ttr (𝜏𝑠 ), Tqfull (𝜏𝑠 ), 𝑇𝑒 (𝑒 z ));
 Await(𝑒 z , 𝜏𝑠 , 𝑛)                             ;𝑒 # ∈𝑇ex (𝑒𝑧 ) RecordRead(fully-ordered, false, 𝑒 #,𝑇qin (𝑒 # ), ∅, ∅)
                                                 Await(Te (𝑒 z ), Tqfull (𝜏𝑠 ), Tqtmp (𝜏𝑠 ), 𝑛);

Fig. 5. 𝑇𝑠 : Stmt → Stmt# (statement conversion). All conversion functions use the 𝑇 _· prefix (Figures 18-20).
𝜏𝑣free = temporally-ordered


5.2 Conversion from GPU IR to Abstract Machine IR
We describe how GPU IR expressions (Section 5.2.1), statements (Section 5.2.2), and instruction
arguments (Section 5.2.3) are converted. Before conversion, we apply two trivial preprocessing
steps to GPU IR: (i) Inline all window statements, and (ii) Inline all subprocedure calls that oc-
cur outside any CudaDeviceFunction block. Throughout this section (and in figures) we use the
following notation. For a finite, ordered variables 𝑅 = h𝑟 0, . . . , 𝑟𝑘 −1 i and a statement template

                                                                14
Exo-GPU: Safe, Imperative, User-schedulable Programming for Tensor Cores


𝑆 (·), ;𝑘𝑖=0 𝑆 (𝑥) ≜ 𝑆 (𝑟 0 ) ; 𝑆 (𝑟 1 ) ; · · · ; 𝑆 (𝑟𝑘 −1 ). If 𝑅 = ∅, the result is no‑op. The intent
is purely left‑to‑right sequential composition at AMIR conversion time. When unambiguous, we
write 𝑓 (𝐴) = { 𝑓 (𝑎) | 𝑎 ∈ 𝐴 } for the pointwise image of a set.
5.2.1 Expression Conversion. Figure 17 defines 𝑇𝑒 : DExpr ∪ ZExpr → P (Expr# ), which extracts
the windowed AMIR accesses 𝑒 # ∈ {𝑥 [𝑤 ∗ ], 𝑧 [𝑤 ∗ ]}: scalars 𝑑 contribute nothing (∅); a bare name 𝑥
or 𝑧 yields the degenerate accesses 𝑥 [hi] or 𝑧 [hi]; explicit indexings 𝑥 [𝑤 ∗ ] and 𝑧 [𝑤 ∗ ] are preserved;
and for arithmetic 𝑒 1 op 𝑒 2 the sets union, 𝑇𝑒 (𝑒 1 ) ∪𝑇𝑒 (𝑒 2 ). 𝑇𝑒 is set-valued (order and duplicates are
irrelevant), leaves the value expression unchanged, and merely supplies the converted Expr# used
by RecordRead/RecordMutate and subsequent visibility checks.
5.2.2 Statement Conversion. Figure 5 gives a structural translation 𝑇𝑠 : Stmt → Stmt# from GPU
IR to AMIR. Helper functions referenced by Figure 5 are defined in Figure 18. Sequencing and
conditionals are preserved, while all loops are normalized to the abstract loop form. Warp/block
scopes are dropped and replaced with a guard whose condition is true. Assignments 𝑥 [𝑐 ∗ ]  𝑒
( ∈ {=, +=}) are lowered to explicit read/write effects. We expand source and destination with 𝑇𝑒
and remove sync‑exempt expressions via 𝑇ex . Sync‑exempt memories are those whose accesses can
be assumed safe without checking: CudaGridConstant, CudaClusterSync, and CudaCommitGroup.
Shared memories are the following: CudaBasicSmem, CudaSmemAtomicity16B, CudaSmemLinear,
Sm90_SmemSwizzled(B), or CudaMbarrier.
   Hardware instruction calls ignore control arguments and pair the instruction’s parameter defi-
nition and the arguments via 𝑇arg . The entry and exit of CudaDeviceFunction is bracketed with
fences with cuda_stream_sync, capturing both the CPU-to-GPU fence implied by the kernel
launch, and the serialization of the CUDA kernel with respect to prior and subsequent CUDA
kernels and API calls (Note that Exo-GPU currently uses only one CUDA stream). During the
conversion, we record the scope of each statement using a global environment Scope : Stmt# →
{CPU, CUDA}. Statements outside the CudaDeviceFunction block are CPU-scoped, while those
inside are GPU-scoped. The scope mapping is used in Definition 5.2. Fence, Arrive, and Await
translate a sync timeline (𝜏𝑠 ) into a qualitative timeline set (𝜏𝑞∗ ). 𝑇tr queries whether a sync timeline
is transitive; 𝑇qfull and 𝑇qtmp materialize the full and temporal QualTL sets, respectively. Arrive
selects its arrival qualitative timeline via 𝑇qarr to sync-check the barrier itself, thereby preventing
use-after-free bugs.
5.2.3 Instruction Argument Conversion. Figure 19 expands the conversion 𝑇arg (𝑔.𝑝𝑖 , 𝑒𝑖 , 𝑒𝑧 ) from a
GPU IR instruction call argument to the AMIR statements. The auxiliary projections and predicates
referenced in the figure—𝑇ext , 𝑇atom , 𝑇init , 𝑇ooo , and 𝑇cvg —are defined in Figure 20. For each non-sync
exempt expression 𝑒 # ∈ 𝑇ex (𝑒𝑖 ), the conversion emits a sequence of checks and effect-recording
operations which depends on two properties of the parameter 𝑔.𝑝𝑖 : its access mode (read-only vs.
write-only/read–write) and whether it is atomic. The access mode of 𝑔.𝑝𝑖 is determined by a simple
intraprocedural static analysis over instruction body (behavior) 𝑔.𝑠: if 𝑔.𝑝𝑖 is only read (and never
written or reduced), it is classified as read-only; if it is written but never read or reduced, it is
write-only; otherwise it is read–write. The atomic case is selected exactly when 𝑇atom (𝑔.𝑝𝑖 ) ≠ ∅.
5.2.4 Program Conversion. The GPU IR ’s program proc 𝑦 ∗, (𝑥 : 𝜏𝑥 ) ∗ ; do 𝑠 is translated into an
AMIR program proc 𝑦 ∗ ; do 𝑠 # where only control arguments are retained. Non-control arguments
(𝑥 : 𝜏𝑥 ) ∗ are ignored during the conversion. Control variables are preserved, since GPU IR and
AMIR share the same control variables set Y. 𝑇𝑠 is applied to the program body to convert 𝑠 to 𝑠 # .
5.3   Abstract Machine Semantics
Definition 5.1 (Control–Value Environment). Let Z be the set of control value and Y the set of
control variables. 𝜎 ∈ Σ ≜ Y → Z.

                                                       15
                                                               David Zhao Akeley, Yuka Ikarashi, and Jonathan Ragan-Kelley


                             𝜎 (𝑦) = 𝑛                     h𝑐 1, 𝜎i ⇓Z 𝑛 1         h𝑐 2, 𝜎i ⇓Z 𝑛 2         op ∈ {+, −, ∗, /}
              C-Int                         C-Read                                                                             C-Aff
h𝑛, 𝜎i ⇓Z 𝑛                 h𝑦, 𝜎i ⇓Z 𝑛                                      h𝑐 1 op 𝑐 2, 𝜎i ⇓Z (𝑛 1 op 𝑛 2 )

                                               h𝑏 1, 𝜎i ⇓Bool 𝑡 1       h𝑏 2, 𝜎i ⇓Bool 𝑡 2           op ∈ {and, or}
                         B-Const                                                                                         B-Log
      h𝑡, 𝜎i ⇓Bool 𝑡                                            h𝑏 1 op 𝑏 2, 𝜎i ⇓Bool oc
                                                                                       p(𝑡 1, 𝑡 2 )

     h𝑐 1, 𝜎i ⇓Z 𝑛 1      h𝑐 2, 𝜎i ⇓Z 𝑛 2          op ∈ {==, <, ≤}                                     h𝑐, 𝜎i ⇓Z 𝑖
                                                                     B-Rel                                              W-Point
                  h𝑐 1 op 𝑐 2, 𝜎i ⇓Bool (𝑛 1 op 𝑛 2 )                                                h𝑐, 𝜎i ⇓ I { 𝑖 }

       h𝑐 1, 𝜎i ⇓Z 𝑖 1       h𝑐 2, 𝜎i ⇓Z 𝑖 2                                 ∀𝑗 ∈ {1..𝑛}. h𝑤 𝑗 , 𝜎i ⇓ I 𝑊 𝑗
                                                   W-Range                                                              W-Tuple
    h𝑐 1 ..𝑐 2, 𝜎i ⇓ I { 𝑖 ∈ Z | 𝑖 1 ≤ 𝑖 ≤ 𝑖 2 }                       h𝑤 1, . . . , 𝑤𝑛 , 𝜎i ⇓ I𝑛 𝑊1 × · · · × 𝑊𝑛

                                     𝑎 ∈ X∪B            h𝑤 1, . . . , 𝑤𝑛 , 𝜎i ⇓ I𝑛 W
                                                                                          E#-Acc
                                  h𝑎[𝑤 1, . . . , 𝑤𝑛 ], 𝜎i ⇓Acc { {𝑎 ↦→ 𝑖®} | 𝑖® ∈ W }

                             Fig. 6. The big-step operational semantics for expressions.

Definition 5.2 (Global Threads Collective). Let I be the set of task IDs and T the set of all (local)
thread IDs (thread collective). The set of global thread IDs is G ≜ I × T. For each statement 𝑠 # ,
thread mapping 𝑓𝑠 # : Σ → T returns the set of local threads that execute 𝑠 # under 𝜎 (𝑓𝑠 # defined in
Section 4). The scope mapping scope : Stmt# → {CPU, CUDA} is initialized during the statement
conversion to indicate whether each statement belongs to the CPU or CUDA scope. Given 𝜎 and
𝚤 ∈ I, define the corresponding global threads
                                    (
                                      { (𝚤, 𝑡) | 𝑡 ∈ 𝑓𝑠 # (𝜎) } if scope(𝑠) = CUDA
                      𝑔𝑠 # (𝜎, 𝚤) ≜
                                      G                         if scope(𝑠) = CPU
Definition 5.3 (Synchronization Environment). Let B be the set of barrier names and X the set
of data variables. Define
                       P : B → Z𝑛 → P (N) and S : G → QualTL → VL,
where P(𝑏, 𝑐 ∗ ) is the set of observed arrive counts at barrier access 𝑏 [𝑐 ∗ ], and S(𝑔, 𝜏𝑞 ) is the visibility
level for the thread with global ID 𝑔 ∈ G on a qualitative timeline 𝜏𝑞 (Figure 4). Let
                                                    R ≜ QualTL × S × P
be the set of visibility records, written (q, ∫, p). The synchronization environment is the map
                                    𝜌 : (X ∪ B) → Z𝑛 → P (R) × P (R) × N2,
sending a name and index to a tuple of (read visibility record set 𝑟 : P (R), mutate visibility record
set 𝑚 : P (R), barrier count 𝑏 : N2 ).
  The semantics follows a standard big-step style where judgments take the form h𝑒 #, 𝜎i ⇓ 𝑣 for
expressions and h𝑠 #, 𝚤, 𝜎, 𝜌i ⇓ 𝚤 0, 𝜎 0, 𝜌 0 for statements, indicating that expression 𝑒 # evaluates to
value 𝑣 in state 𝜎, and statement 𝑠 # transforms state 𝜎 to 𝜎 0 , 𝜌 to 𝜌 0 , and 𝚤 to 𝚤 0 , respectively.
5.3.1 Expression semantics. Figure 6 gives big-step judgements h𝑒, 𝜎i ⇓𝜏 𝑣. Integer and boolean
literals evaluate to themselves (C-Int, B-Const); variables read from the store (C-Read). Arith-
metic evaluates both operands to integers and then applies op ∈ {+, −, ∗, /} (C-Aff). Boolean
connectives apply the usual truth functions for and/or (B-Log), and comparisons op ∈ {==, <, ≤}
compare integer results to yield booleans (B-Rel). Windows denote index sets I: a point yields {𝑖}
(W-Point); a range 𝑐 1 ..𝑐 2 yields the inclusive set { 𝑖 ∈ Z | 𝑖 1 ≤ 𝑖 ≤ 𝑖 2 } (W-Range); and an 𝑛-tuple

                                                                16
Exo-GPU: Safe, Imperative, User-schedulable Programming for Tensor Cores




            ∃(_, ∫, _) ∈ 𝜌 (𝑊𝑒 # ).𝑟 (𝑡 = false ∧ ∃𝑔 ∈ 𝑔𝑠 # (𝜎, 𝚤). ∀𝜏𝑞 ∈ 𝜏𝑞∗ | ∫ (𝑔, 𝜏𝑞 ) ⪰̸ 𝜏𝑣 )
                                                                                                  
h𝑒 #, 𝜎i ⇓Acc 𝑊𝑒 #                 ∨ (𝑡 = true ∧ ∀𝑔 ∈ 𝑔𝑠 # (𝜎, 𝚤). ∀𝜏𝑞 ∈ 𝜏𝑞∗ | ∫ (𝑔, 𝜏𝑞 ) ⪰̸ 𝜏𝑣 ) ⇓Bool true
                                                                                                               ChecKReads
                                hCheckReads(𝜏𝑣 , 𝑡, 𝑒 #, 𝜏𝑞∗ ), 𝚤, 𝜎, 𝜌i ⇓ error

           ∃(_, ∫, _) ∈ 𝜌 (𝑊𝑒 # ).𝑚 (𝑡 = false ∧ ∃𝑔 ∈ 𝑔𝑠 # (𝜎, 𝚤). ∀𝜏𝑞 ∈ 𝜏𝑞∗ | ∫ (𝑔, 𝜏𝑞 ) ⪰̸ 𝜏𝑣 )
                                                                                                 
  #
h𝑒 , 𝜎i ⇓Acc 𝑊𝑒 #                  ∨ (𝑡 = true ∧ ∀𝑔 ∈ 𝑔𝑠 # (𝜎, 𝚤). ∀𝜏𝑞 ∈ 𝜏𝑞∗ | ∫ (𝑔, 𝜏𝑞 ) ⪰̸ 𝜏𝑣 ) ⇓Bool true
                                                                                                               ChecKMutates
                               hCheckMutates(𝜏𝑣 , 𝑡, 𝑒 #, 𝜏𝑞∗ ), 𝚤, 𝜎, 𝜌i ⇓ error

          h𝑒𝑧#, 𝜎i ⇓Acc 𝑊𝑒𝑧#        (∃(𝑎, 𝑤) ∈ 𝜌 (𝑊𝑒𝑧# ).𝑏 | 𝑎 ≠ 𝑤) ⇓Bool true
                                                                                    ChecKBaRRieR
                          hCheckBarrier(𝑒𝑧# ), 𝚤, 𝜎, 𝜌i ⇓ error
Fig. 7. Big-step rules for access visibility and barrier consistency. Successful checks leave (𝚤, 𝜎, 𝜌) unchanged;
any violation reduces the configuration to error state.


of windows denotes the Cartesian product 𝑊1 × · · · × 𝑊𝑛 (W-Tuple). The only nonstandard part
is E#-Acc: given 𝑎 ∈ X ∪ B and a window tuple W, it unpacks the window into the set of concrete
accesses { {𝑎 ↦→ 𝑖®} | 𝑖® ∈ W } of type X ∪ B → Z∗ .
5.3.2 Statement semantics. Figure 21 gives big-step operational semantics for a loop, sequencing,
an explicit task–ID increment, and a guard. For for 𝑦 in loop(𝑐 lo, 𝑐 hi ) do 𝑠 # , the bounds evaluate
in 𝜎 to integers 𝑚 and 𝑛; the loop ranges over the half-open interval [𝑚, 𝑛): when 𝑚 < 𝑛 (LoopStep)
the body executes once with 𝑦 ↦→ 𝑚, producing (𝚤 0, 𝜎 0, 𝜌 0 ), and the loop recurs on (𝑚+1) . . . 𝑛; when
𝑚 ≥ 𝑛 (LoopDone) it terminates with no effect. Sequencing (Seq) threads the triple (𝚤, 𝜎, 𝜌) from
the first statement into the second. The guard (IF-TRue/IF-False) evaluates 𝑏 in 𝜎 and either exe-
cutes 𝑠 # or behaves as no-op. The only non-standard rule, InctasKID, increments the task identifier
(𝚤 0 = 𝚤 + 1) while leaving 𝜎 and 𝜌 unchanged.
     Figure 22 shows the rest of statement semantics. Alloc evaluates each extent 𝑐𝑖 to an integer
𝑛𝑖 (under ⇓Z ), forms the index set 𝐼 = {(𝑣 1, . . . , 𝑣𝑘 ) | 0 ≤ 𝑣𝑖 < 𝑛𝑖 }, and initializes the per-array-
element synchronization environment state for 𝑥 by updating 𝜌 so that, for every n ∈ 𝐼 , 𝜌 (𝑥, n) =
(∅, ∅, (0, 0)) (no visibility records, 0 arrives/awaits); the thread id 𝚤 and store 𝜎 are unchanged.
ClearReads first resolves the accessed locations via h𝑒 #, 𝜎i ⇓Acc 𝑊𝑒 # and, for each (𝑥, n) ∈ 𝑊𝑒 # ,
replaces 𝜌 (𝑥, n) = (𝑟, 𝑚, 𝑏) ∈ R with (∅, 𝑚, 𝑏). ClearMutates is analogous but replaces it with
(𝑟, ∅, 𝑏). RecoRdRead and RecoRdMutate first evaluate the accessor 𝑒 # and 𝑒𝑧# to access sets 𝑊𝑒 #
and 𝑊𝑒𝑧# (via ⇓Acc ). They then update the visibility map 𝜌 at each key (𝑥, n) ∈ 𝑊𝑒 # using the new
record constructor R defined in Appendix B.
     Fence, Arrive, and Await update 𝜌 solely via lift(𝜌, 𝜆) (defined in Appendix B), which applies
𝜆 pointwise to both the read and mutate visibility record sets. In the following, W decides when
augmentation is permitted, A raises visibility to fully_ordered              or temporally_ordered. For
             pre∗       temp∗                                   temp∗                                 pre∗ 
Fence(𝑡, 𝜏𝑞 , 𝜏𝑞full∗, 𝜏𝑞     ), 𝜆(𝑟 ) = A 𝑟, 𝑔exec∗, 𝜏𝑞full∗, 𝜏𝑞       iff the witness W 𝑡, 𝑔exec∗, 𝜏𝑞 , 𝑟
                                                                                                           pre∗
holds, otherwise 𝜆(𝑟 ) = 𝑟 ; thus visibility is raised by joining 𝑓 ∨ 𝑓aug . Arrive(𝑡, 𝜏𝑞 , 𝑒𝑧#∗ ) and
                     temp∗
Await(𝑒𝑧#, 𝜏𝑞full∗, 𝜏𝑞     , 𝑛) are defined similarly in Appendix B, updating the access visibility appro-
priately.

5.3.3 Checks. Figure 7 gives three pure checks that either signal error or leave (𝚤, 𝜎, 𝜌) unchanged.
ChecKReads evaluates 𝑒 # to accesses 𝑊𝑒 # and raises error when some (_, ∫, _) ∈ 𝜌 (𝑊𝑒 # ).𝑟 fails
to supply visibility at least 𝜏𝑣 for all timelines 𝜏𝑞 ∈ 𝜏𝑞∗ . ChecKMutates is analogous but ranges

                                                              17
                                                 David Zhao Akeley, Yuka Ikarashi, and Jonathan Ragan-Kelley




                    Fig. 8. Performance by varying problem size on a sm_90a GPU.


over mutate visibility record set 𝜌 (𝑊𝑒 # ).𝑚. ChecKBaRRieR evaluates 𝑒𝑧# and signals error iff some
(𝑎, 𝑤) ∈ 𝜌 (𝑊𝑒𝑧# ).𝑏 has 𝑎 ≠ 𝑤, i.e., the recorded arrive and await counts disagree.
5.3.4 Program semantics. Finally, abstract machine executes the program proc 𝑦 ∗ ; do 𝑠 # . The
synchronization check is exposed to the user, who invokes the abstract machine interpreter with
concrete integer values corresponding to the control variables 𝑦 ∗ . The control-value environment
𝜎 : Y → Z is initialized based on the user’s input. The statement 𝑠 # is then evaluated according to
the semantics defined previously. Note that the task id 𝚤 is initialized to 0, and the synchronization
𝜌 is initially empty.

6 PERFORMANCE RESULTS
We implemented tf32-precision GEMM kernels for the sm_90a architecture, using wgmma and TMA
instructions. We also implemented a full-precision fp32 GEMV kernel using warp shuffles and
scalar math [12]; this did not use the accelerator instructions. We compared the Exo-GPU kernels
to cuBLAS’s cublasSgemm, cublasSgemmStridedBatched, and cublasSgemv functions, all with
the math mode set to CUBLAS_TF32_TENSOR_OP_MATH. Our sm_90a-compatible test hardware con-
tained an NVIDIA H100 80GB SXM5 GPU and an AMD EPYC 9454 48-Core Processor, and we
used nvcc Build cuda_12.3.r12.3/compiler.33492891_0 to compile the CUDA C++ sources

                                                  18
Exo-GPU: Safe, Imperative, User-schedulable Programming for Tensor Cores


generated by Exo-GPU. For GEMM, a compute-bound workload, theoretical peak is 494.5 TFLOPS
[17]. For GEMV, a memory-bound workload, we derive the theoretical peak from the memory
bandwidth: 3.35 TB 𝑠
                     2 FLOP        TFLOP
                       4 B = 1.675 𝑠 , with one multiply and one add done for each 4 byte tf32
element loaded from the matrix (the bandwidth from loading the vector is amortized).
   We tested each problem size and hardware combination over 105 iterations: 5 warm-up itera-
tions, and 100 timed iterations, with the pcg3d hash algorithm [9] used to generate “random” input
matrices. Each iteration tested, in a randomized order, the cuBLAS kernel and all applicable Exo-
GPU kernel variants for that problem size. In particular, we tested non-split-k and split-k variants
of the GEMM kernel, with the split-k kernels using cp.reduce.async.bulk (TMA) and split fac-
tors of 1, 2, 4, 8, and 16. For each (problem size, hardware) combination, we collected 100 time
samples per tested kernel and reported the mean of the inter-quartile range (middle 50 samples).
For each plot in Figure 8, we report the best-performing Exo-GPU kernel for each problem size
(plotted as “Exo-GPU (specialized)”) and the single best-performing Exo-GPU kernel (“Exo-GPU
(one kernel)”).
   For large, square matrix GEMM problem sizes, we see very similar performance between Exo-
GPU and CUBLAS; this is expected, as Exo-GPU is able to express all optimizations required for
a peak-performance sm_90a gemm: warp specialization, cluster & TMA multicast support, wgmma
support, and split-barrier synchronization using commit group, mbarrier, and cluster sync mecha-
nisms. For more unusual GEMM problem sizes, such as small matrices and K=65536 workloads, we
see more variation between Exo-GPU and CUBLAS, possibly due to different problem size thresh-
olds for observing wave quantization effects. For GEMV, Exo-GPU and CUBLAS follow a similar
performance trend, with CUBLAS having an almost-consistent performance advantage.
   Abstract Machine performance. We report the performance of the synchronization check-
ing alone, which is implemented as an interpreter for the abstract machine (Section 5). We bench-
marked using only one thread of a laptop with an “11th Gen Intel(R) Core(TM) i7-11850H
@ 2.50GHz” CPU. In Figure 9, we report times for concrete square matrix problem sizes for the
GEMV kernel and the sm_90a GEMM kernel described earlier (both the split-k and non-split-k
versions). The batch size L is 1. We use one untimed warmup run for each problem size, and report
the average of five timed runs, as reported by the timeit module of Python 3.10.12.
   We observe that runtimes are linear in
the number of memory operations interpreted.
The number of memory operations is cubic in
the problem size for GEMM, and quadratic for
GEMV. We see this pattern followed cleanly by
the measured trend (e.g. 2/16/128 seconds for
GEMM for 1024/2048/4096 problem size), indi-
cating no unexpected overhead for large prob-
lem sizes. The bump for small GEMM problem
sizes is due to imperfect division by the per-
cluster tile size. Even if the expected problem
size for a deployed kernel is large, during de-         Fig. 9. Sync-check runtime by problem size.
velopment of an Exo-GPU kernel, it generally
suffices to test only with a small problem size (e.g. 768) for immediate feedback on bugs, with the
option of testing the finalized kernel with the true, larger problem size for additional confidence.




                                                       19
                                                  David Zhao Akeley, Yuka Ikarashi, and Jonathan Ragan-Kelley


7 RELATED WORK
7.1   GPU Kernel Authoring Languages
While CUDA offers fine-grained control, it remains low-level and error-prone. To address this,
various approaches have emerged at different abstraction levels.
   Higher-level abstractions: Tile-level DSLs like Triton [24] and Pallas [1] abstract away low-level
details by enabling programmers to express computations at the block level, with compilers auto-
matically handling the thread-level mapping. However, these abstractions can hide performance-
critical details. When Triton performance fell far behind state-of-the-art for Blackwell GPUs, they
had to invent Gluon, a lower-level language that gives users direct control over tile layouts, mem-
ory allocation, data movement, and asynchrony, essentially abandoning the higher-level automa-
tion to regain the fine-grained control necessary for peak performance. Rather than starting with
automation that may later prove inadequate, Exo-GPU deliberately maintains a thin abstraction
layer over CUDA. Performance-critical constructs, including control flow and data copies across
the memory hierarchy, are made explicit statements in Exo-GPU’s imperative object code.
   Template-based libraries: CUTLASS [15] and ThunderKittens [22] are C++ template-based li-
braries that raise the abstraction of GPU programming while preserving performance. Instead of
hiding CUDA behind rigid abstractions, they provide composable, architecture-aware primitives
that integrate with raw CUDA code. This approach lets programmers work at the tile level when
convenient, yet seamlessly drop to thread-level operations when fine control is needed. CuTe [14],
introduced in CUTLASS 3.0, offers flexible abstraction for defining tensor layouts and transforma-
tions. While these libraries are effective engineering toolkits, they do not provide safety guarantees
or whole-program analyses for asynchronous instructions and synchronization statements.
   Achieving both peak performance and safety remains a fundamental challenge. Existing ap-
proaches either provide limited safety guarantees or lack support for modern GPU features. For
instance, Descend [11] introduces Rust-like borrow checking to ensure race freedom but does not
support key GPU features such as tensor cores and split barriers. The aforementioned tile- and
template-based languages are practical tools, yet do not offer safety guarantees. This motivated
the collective analysis (Section 4) and synchronization checking via abstract machine (Section 5).

7.2   User-schedulable Languages
User-schedulable languages (USLs) describe optimization as rewriting programs into new pro-
grams that compute the same result, but execute much faster. Rather than relying on opaque com-
piler heuristics, programmers directly control these rewrites by specifying scheduling operations.
Halide [19, 20] popularized the idea of USLs, and subsequent Halide-inspired languages explored
different target applications and abstraction for a given domain [2, 3, 5–7, 10, 23, 25, 26, 28]. For in-
stance, TVM offers accelerator abstraction through tensorize, TACO separates tensor definitions
from sparse formats, and Taichi abstracts memory layout and management with fields.
   Several systems have extended user-scheduling to support modern GPU features. TVM’s Ten-
sorIR [4] provides intrinsics for manipulating low-level constructs like split barriers, while Cy-
press [27] lets programmers describe computations as tasks and map them to different resources.
Exo-GPU differs from these approaches in two key ways. First, Exo-GPU exposes low-level control
to the programmer; there is little hidden control flow in GPU IR. In this sense, Exo-GPU follows
a WYSIWYG (what you see is what you get) philosophy: the structure of the program directly
reflects its execution. This contrasts with Cypress, which hides warp specialization as an inter-
nal compiler optimization, and with TensorIR, which focuses on automatically generating sched-
ules with lowering-based intrinsics. Second, Exo-GPU guarantees sequential-parallel equivalence
through a synchronization checker that detects data races, hazards, and other concurrency bugs.

                                                   20
Exo-GPU: Safe, Imperative, User-schedulable Programming for Tensor Cores


7.3   Exo vs. Exo-GPU
Exo-GPU fundamentally extends existing the Exo language by introducing parallel semantics.
While Exo [7, 8] is a high-performance USL that achieves peak performance on many vector ma-
chines and accelerators, it was designed to exploit only the implicit parallelism exposed by hard-
ware. Exo’s scheduling reasoning operates exclusively under a sequential execution model. This
approach suffices for vector machines and matrix accelerators because CPU frontends maintain
instruction ordering; even with out-of-order execution and reorder buffers, the hardware guar-
antees that parallel execution produces results equivalent to sequential execution. Therefore, the
compiler needs only to verify program equivalence when interpreting object code sequentially.
Even within this sequential framework, Exo’s optimizations could exploit implicit hardware par-
allelism through techniques like software pipelining [7, 8].
   In contrast, GPUs expose explicit data- and instruction-parallelism to software. Unlike traditional
CPUs and accelerators that maintain the illusion of sequential execution through their frontend,
modern GPUs shift this responsibility entirely to software. For Exo, this shift requires reasoning
about parallel execution at the object code level and establishing equivalence not just within pro-
gramming models, but across sequential and parallel paradigms. We address this fundamental
challenge through two key contributions. First, we extend Exo’s object code and scheduling lan-
guage to expose user-controlled parallel loops and synchronization features. Second, we provide
safety guarantees by establishing sequential-parallel equivalence through the abstract machine.
This completes the equivalence chain from the simple, initial Exo program through to its opti-
mized, parallel implementation in Exo-GPU, ensuring correctness at every transformation step.


8 LIMITATIONS AND FUTURE WORK
   To optimize Hopper GEMMs (Figure 8), we had to apply two tmp : f32[8] @ tmp_mem
rewrite steps that were out-of-scope of Exo’s sequential safety for i in seq(0, 8):
checks. These patterns arise when modeling TMA’s asynchro-             if i < 6: # removing is
                                                                       ↩→ safe
nous copy instruction, which supports default behavior for out-
                                                                          tmp[i] = 0
of-bounds reads and writes. Inset right figure shows a minimal for i in seq(0, 8):
example that illustrates the problem. Even though removing the         if i < 6:
first guard is safe since the tmp[6] and tmp[7] are not being read        C[i] = tmp[i]
by C in the second loop thanks to the guard, Exo’s dependency-based checks treat these writes
as semantically relevant and cannot prove they are observationally redundant. We marked these
transformations as unsafe in our schedules, despite being semantically sound. To address this issue,
we need to extend Exo’s sequential scheduling rewrites with value-sensitivity.
   Our ability to reason about parallelism is incomplete in several ways. Our programming model
and output CUDA synchronization code is generated based on our understanding of PTX as doc-
umented by NVIDIA in natural language [18]. We do not show that our generated code is correct
with respect to any formal CUDA semantics. We currently do not support Blackwell Tensor Cores
(tcgen05), nor do we support platforms not providing CUDA C++ and inline PTX support. Finally,
our current synchronization checking approach – translation to abstract machine IR followed by
software interpretation – supports only concrete problem sizes and limits compiler performance.
This approach may be improved with static analysis of the abstract machine program.
   Nevertheless, we believe that our approach—exposing detailed control to programmers while
verifying its safety—offers a promising path forward for GPU programming. By treating paral-
lelism and synchronization as analyzable annotations on sequential code, Exo-GPU provides both
the transparency and static guarantees that high-performance GPU kernels demand.


                                                       21
                                                          David Zhao Akeley, Yuka Ikarashi, and Jonathan Ragan-Kelley


ACKNOWLEDGMENTS
We are thankful to William Brandon, Amanda Liu, Luca Musk, Jason Ng, Kevin Qian, and Philippe
Tillet for their insightful discussions and early feedback. This research was funded in part by the
U.S. Government under the DARPA MOCHA program (HR001125CE038) and NSF award CCF-
2217064, and by a gift from Jane Street.

REFERENCES
 [1] The JAX authors. 2024. Pallas: a JAX kernel language. https://docs.jax.dev/en/latest/pallas/index.html
 [2] Michael Bauer, Sean Treichler, Elliott Slaughter, and Alex Aiken. 2012. Legion: expressing locality and independence
     with logical regions. In SC Conference on High Performance Computing Networking, Storage and Analysis, SC ’12 (Salt
     Lake City, UT, USA). IEEE, Piscataway, NJ, USA, 66. https://doi.org/10.1109/SC.2012.71
 [3] Tianqi Chen, Thierry Moreau, Ziheng Jiang, Lianmin Zheng, Eddie Yan, Meghan Cowan, Haichen Shen, Leyuan
     Wang, Yuwei Hu, Luis Ceze, Carlos Guestrin, and Arvind Krishnamurthy. 2018. TVM: An Automated End-to-end
     Optimizing Compiler for Deep Learning. In Proceedings of the 12th USENIX Conference on Operating Systems Design
     and Implementation (Carlsbad, CA, USA) (OSDI’18). USENIX Association, Berkeley, CA, USA, 579–594. http://dl.acm.
     org/citation.cfm?id=3291168.3291211
 [4] Siyuan Feng, Bohan Hou, Hongyi Jin, Wuwei Lin, Junru Shao, Ruihang Lai, Zihao Ye, Lianmin Zheng, Cody Hao
     Yu, Yong Yu, and Tianqi Chen. 2023. TensorIR: An Abstraction for Automatic Tensorized Program Optimization.
     In Proceedings of the 28th ACM International Conference on Architectural Support for Programming Languages and
     Operating Systems, Volume 2 (Vancouver, BC, Canada) (ASPLOS 2023). Association for Computing Machinery, New
     York, NY, USA, 804–817. https://doi.org/10.1145/3575693.3576933
 [5] Bastian Hagedorn, Archibald Samuel Elliott, Henrik Barthels, Rastislav Bodík, and Vinod Grover. 2020. Fireiron: A
     Data-Movement-Aware Scheduling Language for GPUs. In PACT ’20: International Conference on Parallel Architectures
     and Compilation Techniques, Virtual Event, GA, USA, October 3-7, 2020, Vivek Sarkar and Hyesoon Kim (Eds.). ACM,
     71–82. https://doi.org/10.1145/3410463.3414632
 [6] Yuanming Hu, Tzu-Mao Li, Luke Anderson, Jonathan Ragan-Kelley, and Frédo Durand. 2019. Taichi: a language for
     high-performance computation on spatially sparse data structures. ACM Trans. Graph. 38, 6 (2019), 201:1–201:16.
     https://doi.org/10.1145/3355089.3356506
 [7] Yuka Ikarashi, Gilbert Louis Bernstein, Alex Reinking, Hasan Genc, and Jonathan Ragan-Kelley. 2022. Exocompila-
     tion for Productive Programming of Hardware Accelerators. In Proceedings of the 43rd ACM SIGPLAN International
     Conference on Programming Language Design and Implementation (San Diego, CA, USA) (PLDI 2022). Association for
     Computing Machinery, New York, NY, USA, 703–718. https://doi.org/10.1145/3519939.3523446
 [8] Yuka Ikarashi, Kevin Qian, Samir Droubi, Alex Reinking, Gilbert Louis Bernstein, and Jonathan Ragan-Kelley. 2025.
     Exo 2: Growing a Scheduling Language. In Proceedings of the 30th ACM International Conference on Architectural Sup-
     port for Programming Languages and Operating Systems, Volume 1 (Rotterdam, Netherlands) (ASPLOS ’25). Association
     for Computing Machinery, New York, NY, USA, 426–444. https://doi.org/10.1145/3669940.3707218
 [9] Mark Jarzynski and Marc Olano. 2020. A PCG3D Family of Hash Functions. https://github.com/markjarzynski/
     PCG3D
[10] Fredrik Kjolstad, Shoaib Kamil, Stephen Chou, David Lugato, and Saman Amarasinghe. 2017. The tensor algebra
     compiler. Proceedings of the ACM on Programming Languages 1, OOPSLA (oct 2017), 1–29. https://doi.org/10.1145/
     3133901
[11] Bastian Köpcke, Sergei Gorlatch, and Michel Steuwer. 2024. Descend: A Safe GPU Systems Programming Language.
     Proc. ACM Program. Lang. 8, PLDI, Article 181 (June 2024), 24 pages. https://doi.org/10.1145/3656411
[12] Bruce Lee. 2024. CUDA HGEMV. https://github.com/Bruce-Lee-LY/cuda_hgemv
[13] NVIDIA. 2017. NVIDIA Tesla V100 GPU Architecture. https://images.nvidia.com/content/volta-architecture/pdf/
     volta-architecture-whitepaper.pdf
[14] NVIDIA. 2025. CuTe. https://docs.nvidia.com/cutlass/media/docs/cpp/cute
[15] NVIDIA. 2025. CUTLASS 4.2.1. https://github.com/NVIDIA/cutlass
[16] NVIDIA. 2025. CUTLASS grouped kernel schedules.             https://docs.nvidia.com/cutlass/media/docs/cpp/grouped_
     scheduler.html
[17] NVIDIA. 2025. H100 GPU. https://www.nvidia.com/en-us/data-center/h100/
[18] NVIDIA. 2025. Parallel Thread Execution ISA Version 9.0. https://docs.nvidia.com/cuda/parallel-thread-execution/
[19] Jonathan Ragan-Kelley, Andrew Adams, Sylvain Paris, Marc Levoy, Saman P. Amarasinghe, and Frédo Durand. 2012.
     Decoupling algorithms from schedules for easy optimization of image processing pipelines. ACM Trans. Graph. 31, 4
     (2012), 32:1–32:12. https://doi.org/10.1145/2185520.2185528


                                                           22
Exo-GPU: Safe, Imperative, User-schedulable Programming for Tensor Cores


[20] Jonathan Ragan-Kelley, Andrew Adams, Dillon Sharlet, Connelly Barnes, Sylvain Paris, Marc Levoy, Saman P. Ama-
     rasinghe, and Frédo Durand. 2018. Halide: decoupling algorithms from schedules for high-performance image pro-
     cessing. Commun. ACM 61, 1 (2018), 106–115. https://doi.org/10.1145/3150211
[21] Jay Shah, Ganesh Bikshandi, Ying Zhang, Vijay Thakkar, Pradeep Ramani, and Tri Dao. 2024. FlashAttention-3: Fast
     and Accurate Attention with Asynchrony and Low-precision. arXiv:2407.08608 [cs.LG] https://arxiv.org/abs/2407.
     08608
[22] Benjamin F. Spector, Simran Arora, Aaryan Singhal, Daniel Y. Fu, and Christopher Ré. 2024. ThunderKittens: Simple,
     Fast, and Adorable AI Kernels. arXiv:2410.20399 [cs.LG] https://arxiv.org/abs/2410.20399
[23] Michel Steuwer, Toomas Remmelg, and Christophe Dubach. 2017. LIFT: A functional data-parallel IR for high-
     performance GPU code generation. In 2017 IEEE/ACM International Symposium on Code Generation and Optimization
     (CGO). IEEE, Piscataway, NJ, USA, 74–85. https://doi.org/10.1109/CGO.2017.7863730
[24] Philippe Tillet, H. T. Kung, and David Cox. 2019. Triton: an intermediate language and compiler for tiled neural
     network computations. In Proceedings of the 3rd ACM SIGPLAN International Workshop on Machine Learning and
     Programming Languages (Phoenix, AZ, USA) (MAPL 2019). Association for Computing Machinery, New York, NY,
     USA, 10–19. https://doi.org/10.1145/3315508.3329973
[25] Nicolas Vasilache, Oleksandr Zinenko, Theodoros Theodoridis, Priya Goyal, Zachary DeVito, William S. Moses,
     Sven Verdoolaege, Andrew Adams, and Albert Cohen. 2018. Tensor Comprehensions: Framework-Agnostic High-
     Performance Machine Learning Abstractions. arXiv:1802.04730 [cs.PL]
[26] Anand Venkat, Tharindu Rusira, Raj Barik, Mary Hall, and Leonard Truong. 2019. SWIRL: High-performance many-
     core CPU code generation for deep neural networks. The International Journal of High Performance Computing Appli-
     cations 33, 6 (2019), 1275–1289. https://doi.org/10.1177/1094342019866247
[27] Rohan Yadav, Michael Garland, Alex Aiken, and Michael Bauer. 2025. Task-Based Tensor Computations on Modern
     GPUs. Proc. ACM Program. Lang. 9, PLDI, Article 163 (June 2025), 25 pages. https://doi.org/10.1145/3729262
[28] Yunming Zhang, Mengjiao Yang, Riyadh Baghdadi, Shoaib Kamil, Julian Shun, and Saman P. Amarasinghe. 2018.
     GraphIt: a high-performance graph DSL. PACMPL 2, OOPSLA (2018), 121:1–121:30. https://doi.org/10.1145/3276491




                                                          23
                                                    David Zhao Akeley, Yuka Ikarashi, and Jonathan Ragan-Kelley


A GPU IR TYPE DEFINITIONS

                          𝜏𝑥 : DataType F f32             32-bit floating point
                                         | f64            64-bit floating point
                                         | f16            16-bit floating point
                                         | i32            32-bit integer
                                         | ui16           16-bit unsigned integer
                                         | i8             8-bit integer
                                         | ui8            8-bit unsigned integer
                        𝜏𝑧 : BarrierType F barrier     non-explicitly guarded barrier
                                          | barrier(z) explicitly guarded barrier


                                       Fig. 10. List of variable types



                                                          domain                            box
𝜏𝑢 : CollUnit F standalone_thread                         (1,)                              (1,)
               | 𝑛 1 * cuda_thread                        (blockDim,)                       (𝑛 1 ,)
               | cuda_quadpair                            (blockDim/16, 16)                 (2, 4)
               | 𝑛 1 * cuda_warp                          (blockDim,)                       (𝑛 1 * 32,)
               | 𝑛 1 * cuda_warpgroup                     (blockDim,)                       (𝑛 1 * 128,)
               | 𝑛 1 * cuda_threads_strided(𝑛 2 , 𝑛 3 )   (blockDim/𝑛 3 , 𝑛 3 )             (𝑛 1 , 𝑛 2 )
               | 𝑛 1 * cuda_warp_in_cluster               (clusterDim, blockDim)            (𝑛 1 , 32)
               | 𝑛 1 * cuda_cta_in_cluster                (clusterDim * blockDim,)          (𝑛 1 * blockDim,)
               | cuda_cluster                             (clusterDim * blockDim,)          (clusterDim * blockDim,)
               | 𝑛 1 * cuda_cta_in_cluster_strided(𝑛 3 ) (ClusterDim/𝑛 3 , 𝑛 3 , blockDim) (𝑛 1 , 1, blockDim)
               | 𝑛 1 * cuda_warp_in_cluster_strided(𝑛 3 ) (clusterDim/𝑛 3 , 𝑛 3 , blockDim) (𝑛 1 , 1, 32)
               | cuda_agnostic_sub_cta                    (clusterDim, blockDim)            (1, _)
               | cuda_agnostic_intact_cta                 (clusterDim, blockDim)            (_, blockDim)


Fig. 11. Collective units defined in the frontend language. These are parameterized by a collective type 𝛿,
which consists of the domain and box shown here.



𝜋d : DataMemory F CudaBasicDeviceVisible         base type for CUDA-visible allocations
                 | CudaBasicSmem                 base type for CUDA SMEM allocations
                 | CudaDeviceVisibleAtomicity16B base type for 16B-atomicity layout CUDA-visible allocations
                 | CudaDeviceVisibleLinear       base type for linear-order CUDA-visible allocations
                 | CudaGridConstant              CUDA grid constant memory
                 | CudaGmemLinear                CUDA global memory, linear-order
                 | CudaSmemAtomicity16B          any CUDA shared memory with 16B-atomicity layout
                 | CudaSmemLinear                CUDA shared memory with linear-order layout
                 | CudaRmem                      per-thread CUDA registers
                 | Sm80_RmemMatrixA(M, K)        matrix tile for sm_80+ warp MMA A operand
                 | Sm80_RmemMatrixB(N, K)        matrix tile for sm_80+ warp MMA B operand
                 | Sm80_RmemMatrixD(M, N)        matrix tile for sm_80+ MMA acumulator operands
                 | Sm90_SmemSwizzled(B)          B-byte swizzled shared memory, in TMA/wgmma-accepted format
                 | Sm90_RmemMatrixA(M)           register tile for wgmma A operand (not implemented)
                 | Sm90_RmemMatrixD(M, N)        register tile for wgmma D operand


          Fig. 12. CUDA Memory Types – Data Allocations (pre-existing Exo Memory not listed)




                                                     24
Exo-GPU: Safe, Imperative, User-schedulable Programming for Tensor Cores


                 𝜋z : BarrierComp F CudaDeviceBarrier base type for CUDA-allocated barriers
                                   | CudaMbarrier     CUDA mbarrier
                                   | CudaCommitGroup  CUDA commit_group mechanism
                                   | CudaClusterSync  barrier.cluster sync


                              Fig. 13. CUDA Barrier (completion) mechanisms


𝜋w : SpecialWindow F Sm90_tensorMap(swizzle, *smem_box) CUtensorMap parameterized by swizzle mode and box size


                       Fig. 14. CUDA Special Window Types (for Window Statement)


      𝜏𝑞 : QualTL F cpu_in_order_qual        Ordinary CPU reads/writes (cpu)
                   | cpu_cuda_stream_qual    Stream-ordered CUDA API calls (strm)
                   | cuda_in_order_rmem_qual non-async CUDA instrs’ accesses to registers (cuda1)
                   | cuda_in_order_ram_qual non-async CUDA instrs’ accesses to SMEM/GMEM (cuda2)
                   | Sm80_cp_async_qual      non-bulk cp.async memory accesses (Sm80)
                   | tma_to_smem_async_qual cp.async.bulk GMEM reads, SMEM writes (tmaS)
                   | tma_to_gmem_async_qual cp.async.bulk SMEM reads, GMEM writes/reduces (tmaG)
                   | wgmma_async_rmem_a_qual wgmma.mma_async reads from 𝐴 register parameter (wgA)
                   | wgmma_async_rmem_d_qual wgmma.mma_async accesses to 𝐷 (accumulator) (wgD)
                   | wgmma_async_smem_qual wgmma.mma_async access to SMEM, 𝐴 or 𝐵 (wgS)
                   | wgmma_zero_qual         special case used to model the wgmma scale-d parameter (wg0)


                                     Fig. 15. List of qualitative timelines

                 𝜏𝑠 : SyncTL trnstv? cpu strm cuda1 cuda2 Sm80 tmaS tmaG wgA wgD wgS wg0
              empty_sync_tl
               cpu_in_order y        full
           cuda_stream_sync y             full full   full  full full full    full full full
              cuda_in_order y             temp. full  full  temp. temp. temp. temp. temp. temp. temp.
              cuda_temporal               temp. temp. temp. temp. temp. temp. temp. temp. temp. temp.
              Sm80_cp_async                                 full
               Sm80_generic               temp. full  full  full temp. temp. temp. temp. temp. temp.
          tma_to_smem_async                                       full
          tma_to_gmem_async                                             full
           wgmma_async_smem                                                               full
              wgmma_fence_1                     full                          full full
              wgmma_fence_2                                                   full full
                wgmma_async                                                   full full full
           cuda_async_proxy                                       full full               full
     cuda_async_proxy_wgmma                                       full full   full full full
     cuda_generic_and_async               temp. full  full  full full full    temp. temp. full temp.

                           Fig. 16. SyncTL are defined as composition of QualTL.


B ABSTRACT MACHINE CONVERSION AND SEMANTICS DEFINITIONS
A new record Constructor R is used to define RecordRead and RecordMutate in Figure 22. RecoR-
dRead and RecoRdMutate first evaluate the accessor 𝑒 # and 𝑒𝑧# to access sets 𝑊𝑒 # and 𝑊𝑒𝑧# (via
⇓Acc ). They then update the visibility map 𝜌 at each key (𝑥, n) ∈ 𝑊𝑒 # using the new visibility
record constructor R defined below: RecoRdRead adds it to the read visibility record set, setting
𝜌 0 (𝑥, n).𝑟 = 𝜌 (𝑥, n).𝑟 ∪ R (· · · ) while leaving 𝜌 (𝑥, n).𝑚 and 𝜌 (𝑥, n).𝑏 unchanged; RecoRdMutate

                                                       25
                                                           David Zhao Akeley, Yuka Ikarashi, and Jonathan Ragan-Kelley


adds it to the mutate visibility record set, setting 𝜌 0 (𝑥, n).𝑚 = 𝜌 (𝑥, n).𝑚 ∪ R (· · · ) while preserving
𝜌 (𝑥, n).𝑟 and 𝜌 (𝑥, n).𝑏. In both cases, neither the control 𝚤 nor the store 𝜎 changes.
Definition B.1 (New Record Constructor R). Define R as follows:
               R : VL × Bool × QualTL × P (QualTL) × Expr# × 𝜌 × G −→ P (R)
                                                   (
                                  ∗ #
                                                     { (𝜏𝑞 , 𝑆𝐺 , 𝑃𝐸 #,𝜌 ) },              𝑡 = true,
                 R (𝜏𝑣 , 𝑡, 𝜏𝑞 , 𝜏𝑞 , 𝐸 , 𝜌, 𝐺) =
                                                     { (𝜏𝑞 , 𝑆 {𝑔} , 𝑃𝐸 #,𝜌 ) | 𝑔 ∈ 𝐺 }, 𝑡 = false,
where, for any 𝐻 ⊆ G, 𝑆𝐻 ∈ S and 𝑃𝐸 #,𝜌 ∈ P are given pointwise by
                                     (                                   (                                  !
            0 0                        atomic_only, 𝜏𝑞0 ∈ 𝜏𝑞∗,             𝜏𝑣 ,         𝑔0 ∈ 𝐻 ∧ 𝜏𝑞0 = 𝜏𝑞 ,
      𝑆𝐻 (𝑔 , 𝜏𝑞 ) = maxVL                                            ,                                       ,
                                       invisible,       otherwise          invisible, otherwise
                                            (
                                              {𝑎}, (𝑧, n) ∈ 𝐸 # where (𝑎, _) = 𝜌 (𝑧, n).𝑏,
                     𝑃𝐸 #,𝜌 (𝑧, n) =
                                              ∅,   otherwise.
   Fence, Arrive, and Await (Figure 22) update 𝜌 solely via lift(𝜌, 𝜆) (defined below), which ap-
                                                                             pre∗          temp∗
plies 𝜆 pointwise to both the read and mutate visibility sets. For Fence(𝑡, 𝜏𝑞 , 𝜏𝑞full∗, 𝜏𝑞     ), 𝜆(𝑟 ) =
                                                                
                       temp∗                                 pre∗
A 𝑟, 𝑔exec∗, 𝜏𝑞full∗, 𝜏𝑞       iff the witness W 𝑡, 𝑔exec∗, 𝜏𝑞 , 𝑟 holds, otherwise 𝜆(𝑟 ) = 𝑟 ; thus
                                                                     pre∗
visibility is raised by joining 𝑓 ∨ 𝑓aug . For Arrive(𝑡, 𝜏𝑞 , 𝑒𝑧#∗ ), the accessed sets yield a unique
                                Ñ
home barrier {(𝑧, n)} = 𝑖 𝑊𝑒𝑧𝑖# ; guarded by W, 𝜆 adds the existing arrive count 𝑎 from 𝜌 (𝑧, n)
into 𝑟 .𝑝 at every (𝑧, n) ∈ W, and home barrier’s arrive count is incremented by (𝑎 0 + 1, 𝑤 0 ).
                          temp∗
For Await(𝑒𝑧#, 𝜏𝑞full∗, 𝜏𝑞        , 𝑛), with (𝑎, 𝑤) = 𝜌 (𝑧, n).𝑏, compute Max and New as in the rule; set
                                          
                                     temp∗
𝜆(𝑟 ) = A 𝑟, 𝑔𝑠 # (𝜌), 𝜏𝑞 , 𝜏𝑞
                            full∗            iff some observed arrive count 𝑖 ∈ 𝑟 .𝑝 (𝑧, n) satisfies 𝑖 ≤ Max,
else 𝜆(𝑟 ) = 𝑟 ; after lift, update the wait count to (𝑎 0, New). In short, W decides when augmentation
is permitted, A raises visibility to fully_ordered or temporally_ordered.
Definition B.2 (Lift). For 𝜆 : R → R, define lift(𝜌, 𝜆) pointwise by
                                                                 
  lift(𝜌, 𝜆)(𝑥, v) = { 𝜆(𝑟 ) | 𝑟 ∈ 𝑅 }, { 𝜆(𝑟 ) | 𝑟 ∈ 𝑀 }, (𝑎, 𝑤) where (𝑅, 𝑀, (𝑎, 𝑤)) = 𝜌 (𝑥, v).
                                                                     orig
Definition B.3 (Synchronization helpers). Let 𝑟 = (𝜏𝑞 , ∫, 𝑝) ∈ R with ∫ ∈ S. For ∫ 1, ∫ 2 ∈ S,
define the pointwise join (∫ 1 ∨ ∫ 2 )(𝑔, 𝜏𝑞 ) = maxVL {∫ 1 (𝑔, 𝜏𝑞 ), ∫ 2 (𝑔, 𝜏𝑞 )}.
                                                     pre∗
  (i) Witness W. For 𝑡 ∈ Bool, 𝑔exec∗ ⊆ G, and 𝜏𝑞 ⊆ QualTL, set
                              (                    pre∗
            exec∗ pre∗
                                ∃𝑔 ∈ 𝑔exec∗ ∃𝜏𝑞 ∈ 𝜏𝑞 : ∫ (𝑔, 𝜏𝑞 )  unordered,            𝑡 = true,
    W (𝑡, 𝑔      , 𝜏𝑞 , 𝑟 ) =     orig   pre∗                           orig
                                 𝜏𝑞 ∈ 𝜏𝑞        ∧ ∃𝑔 ∈ 𝑔  exec∗ : ∫ (𝑔, 𝜏𝑞 )  unordered, 𝑡 = false.
                                                           temp∗
   (ii) Augment A. Given 𝑔exec∗ ⊆ G and 𝜏𝑞full∗, 𝜏𝑞                ⊆ QualTL, define
                                                       temp∗        orig            
                               A (𝑟, 𝑔exec∗, 𝜏𝑞full∗, 𝜏𝑞     )   = 𝜏𝑞 , ∫ ∨ ∫ aug, 𝑝 ,
                                
                                 fully_ordered,     𝑔 ∈ 𝑔exec∗ ∧ 𝜏𝑞 ∈ 𝜏𝑞full∗,
                                
                                
                                
                ∫ aug (𝑔, 𝜏𝑞 ) = temporally_ordered, 𝑔 ∈ 𝑔exec∗ ∧ 𝜏𝑞 ∈ 𝜏𝑞temp∗ \ 𝜏𝑞full∗,
                                
                                
                                 invisible,         otherwise.
                                




                                                            26
Exo-GPU: Safe, Imperative, User-schedulable Programming for Tensor Cores


                Data expressions 𝑒 ∈ DExpr                              P (Expr# )
               𝑑                                                       ∅
               𝑥                                                       { 𝑥 [hi] }
               𝑥 [𝑤 ∗ ]                                                { 𝑥 [𝑤 ∗ ] }
               𝑒 1 op 𝑒 2       (op ∈ {+, −, ∗, /})                    𝑇𝑒 (𝑒 1 ) ∪ 𝑇𝑒 (𝑒 2 )
                Barrier expressions 𝑒 z ∈ ZExpr
               𝑧                                                        { 𝑧[hi] }
               𝑧 [𝑤 ∗ ]                                                 { 𝑧 [𝑤 ∗ ] }


Fig. 17. Expression conversion 𝑇𝑒 : DExpr ∪ ZExpr → P (Expr# ) collects the distinct reads in an expression
and returns them as a set of AMIR reads (Expr# ).

Type                                    Definition
𝑇smem : Expr → P (Expr )    #
                                       𝑇smem (𝑒 ) ≜ { 𝑒 # ∈ 𝑇𝑒 (𝑒 ) | isSmem(𝑒 # ) }.
𝑇ex : Expr → P (Expr# )                𝑇ex (𝑒 ) ≜ { 𝑒 # ∈ 𝑇𝑒 (𝑒 ) | ¬ isEx(𝑒 # ) }.

isEx : Expr# → Bool                     isEx(𝑒 # ) ≜ true iff 𝑒 # is annotated as sync‑exempt memory; false otherwise.

isSmem : Expr# → Bool                   isSmem(𝑒 # ) ≜ true iff 𝑒 # is annotated as shared memory; false otherwise.

𝑇tr : SyncTL → Bool                    𝑇tr (𝜏𝑠 ) ≜ true iff 𝜏𝑠 is transitive; false otherwise.

𝑇qfull : SyncTL → P (QualTL)           𝑇qfull (𝜏𝑠 ) ≜ { 𝜏𝑞0 ∈ QualTL | 𝜏𝑞0 annotated as “full” in 𝜏𝑠 }.

𝑇qtmp : SyncTL → P (QualTL)            𝑇qtmp (𝜏𝑠 ) ≜ { 𝜏𝑞0 ∈ QualTL | 𝜏𝑞0 annotated as “temporal” or “full” in 𝜏𝑠 }.
                                                     (
                                                       Sm80_cp_async_qual, if Sm80_cp_async_qual ∈ 𝑇qfull (𝜏𝑠 ),
𝑇qarr : SyncTL → QualTL                𝑇qarr (𝜏𝑠 ) ≜
                                                       cuda_in_order_qual, otherwise.
                                                         
                                                          cpu_in_order_qual,             if 𝑒 # is host/CPU scoped,
                                                         
                                                         
                                                         
𝑇qin : Expr → QualTL
          #
                                       𝑇qin   (𝑒 # )   ≜ cuda_in_order_rmem_qual,         if 𝑒 # is register memory,
                                                         
                                                         
                                                          cuda_in_order_ram_qual,        otherwise.
                                                         

              Fig. 18. Helper functions used by Fig. 5 statement conversion. All sets are finite.




                                                                  27
                                                                             David Zhao Akeley, Yuka Ikarashi, and Jonathan Ragan-Kelley


Case for 𝑔.𝑝𝑖                               Abstract Machine IR
                                                           
Non-atomic read-only                              ; CheckMutates(full_ordered,𝑇cvg (𝑔.𝑝𝑖 ), 𝑒 #, 𝑇ext (𝑔.𝑝𝑖 ) );
                                            𝑒 # ∈𝑇ex (𝑒𝑖 )                                                                   
                                                                         post
                                                             RecordRead(𝜏𝑣 ,𝑇cvg (𝑔.𝑝𝑖 ), 𝑒 # , 𝑇init (𝑔.𝑝𝑖 ), ∅,𝑇𝑒 (𝑒 z ) )
                                                           
Non-atomic non-read-only                          ; CheckMutates(𝜏𝑣pre,𝑇cvg (𝑔.𝑝𝑖 ), 𝑒 #, 𝑇ext (𝑔.𝑝𝑖 ) );
                                            𝑒 # ∈𝑇ex (𝑒𝑖 )
                                                                 CheckReads(temporal_ordered,𝑇cvg (𝑔.𝑝𝑖 ), 𝑒 # , 𝑇ext (𝑔.𝑝𝑖 ) );
                                                                 ClearReads(𝑒 # );
                                                                 ClearMutates(𝑒 # );                                         
                                                                    post
                                                      RecordMutate(𝜏𝑣 ,𝑇cvg (𝑔.𝑝𝑖 ), 𝑒 # , 𝑇init (𝑔.𝑝𝑖 ), ∅,𝑇𝑒 (𝑒 z ) )
                                                      pre
                                               where 𝜏𝑣 = temporal_ordered if 𝑔.𝑝𝑖 is write-only, else full_ordered.
                                                             
Atomic                                            ;              CheckMutates(atomic_only,𝑇cvg (𝑔.𝑝𝑖 ), 𝑒 # , 𝑇ext (𝑔.𝑝𝑖 ) );
                                            𝑒 # ∈𝑇ex (𝑒𝑖 )
                                                                 CheckReads(temporal_ordered,𝑇cvg (𝑔.𝑝𝑖 ), 𝑒 # , 𝑇ext (𝑔.𝑝𝑖 ) );
                                                                 ClearReads(𝑒 # );(note lack of ClearMutates)                                              
                                                                                     post
                                                                 RecordMutate(𝜏𝑣            ,𝑇cvg (𝑔.𝑝𝑖 ), 𝑒 # , 𝑇init (𝑔.𝑝𝑖 ),𝑇atom (𝑔.𝑝𝑖 ),𝑇𝑒 (𝑒 z ) )

                                                                              post
  Fig. 19. Argument conversion 𝑇arg (𝑔.𝑝𝑖 , 𝑒𝑖 , 𝑒𝑧 ). 𝜏𝑣                            = unordered if 𝑇ooo (𝑔.𝑝𝑖 ), else full_ordered.

 Type                                           Definition
 𝑇ext : Expr → P (QualTL)                      𝑇ext (𝑒 ) ≜ { 𝜏𝑞 ∈ QualTL | 𝜏𝑞 ∈ 𝑒.ext_qual_tl }.

 𝑇atom : Expr → P (QualTL)                     𝑇atom (𝑒 ) ≜ { 𝜏𝑞 ∈ QualTL | 𝜏𝑞 ∈ 𝑒.atomic_qual_tl }.

 𝑇init : Expr → QualTL                         𝑇init (𝑒 ) ≜ 𝑒.initial_qual_tl.

 𝑇ooo : Expr → Bool                            𝑇ooo (𝑒 ) ≜ 𝑒.out_of_order

 𝑇cvg : Expr → Bool                            𝑇cvg (𝑒 ) ≜ 𝑒.convergent


                             Fig. 20. Helper functions used by Fig. 19 argument conversion.

                          h𝑐 lo, 𝜎i ⇓Z 𝑚 h𝑐 hi, 𝜎i ⇓Z 𝑛 𝑚 < 𝑛 h𝑠, 𝚤, 𝜎 [𝑦 ↦→ 𝑚], 𝜌i ⇓ 𝚤 0, 𝜎 0, 𝜌 0
                                      hfor 𝑦 in (𝑚+1) . . . 𝑛 do 𝑠 #, 𝚤 0, 𝜎 0, 𝜌 0 i ⇓ 𝚤 00 , 𝜎 00 , 𝜌 00
                                                                                                                                    LoopStep
                                        hfor 𝑦 in loop(𝑐 lo, 𝑐 hi ) do 𝑠 #, 𝚤, 𝜎, 𝜌i ⇓ 𝚤 00, 𝜎 00, 𝜌 00

                                        h𝑐 lo, 𝜎i ⇓Z 𝑚               h𝑐 hi, 𝜎i ⇓Z 𝑛 𝑚 ≥ 𝑛
                                                                                                          LoopDone
                                   hfor 𝑦 in loop(𝑐 lo, 𝑐 hi ) do 𝑠 #, 𝚤, 𝜎, 𝜌i ⇓ 𝚤, 𝜎, 𝜌

h𝑠 1#, 𝚤, 𝜎, 𝜌i ⇓ 𝚤 0, 𝜎 0, 𝜌 0         h𝑠 2#, 𝚤 0, 𝜎 0, 𝜌 0 i ⇓ 𝚤 00, 𝜎 00, 𝜌 00                                 𝚤0 = 𝚤 + 1
                                                                                  Seq                                                        InctasKID
                   h𝑠 1 ; 𝑠 2 , 𝚤, 𝜎, 𝜌i ⇓ 𝚤 00, 𝜎 00 , 𝜌 00
                      # #
                                                                                                     hInctaskID, 𝚤, 𝜎, 𝜌i ⇓ 𝚤 0, 𝜎, 𝜌

 h𝑏, 𝜎i ⇓Bool true            h𝑠 #, 𝚤, 𝜎, 𝜌i ⇓ 𝚤 0, 𝜎 0, 𝜌 0                                        h𝑏, 𝜎i ⇓Bool false
                                                                    IF-TRue                                                         IF-False
         hif 𝑏 then 𝑠 #, 𝚤, 𝜎, 𝜌i ⇓ 𝚤 0, 𝜎 0, 𝜌 0                                           hif 𝑏 then 𝑠 #, 𝚤, 𝜎, 𝜌i ⇓ 𝚤, 𝜎, 𝜌

     Fig. 21. Big-step semantics for a loop, sequencing, an explicit task–ID increment, and a guard.




                                                                              28
Exo-GPU: Safe, Imperative, User-schedulable Programming for Tensor Cores


                                            𝑐 ∗ = (𝑐 1, . . . , 𝑐𝑘 ) 𝑐𝑖 , 𝜎 ⇓Z 𝑛𝑖  for 𝑖 = 1..𝑘           
                         𝐼 = { (𝑣 1, . . . , 𝑣𝑘 ) | 0 ≤ 𝑣𝑖 < 𝑛𝑖 }          𝜌 0 = 𝜌 (𝑥, n) ↦→ (∅, ∅, (0, 0)) n∈𝐼
                                                                                                                                 Alloc
                                                        hAlloc(𝑥 [𝑐 ∗ ]), 𝚤, 𝜎, 𝜌i ⇓ 𝚤, 𝜎, 𝜌 0
                                                                                     
          h𝑒 #, 𝜎i ⇓Acc 𝑊𝑒 #           𝜌 0 = 𝜌 (𝑥, n) ↦→ ( ∅, 𝜌 (𝑥, n).𝑚, 𝜌 (𝑥, n).𝑏 ) (𝑥,n) ∈𝑊 #
                                                                                                                        𝑒
                                                                                                                            CleaRReads
                                       ClearReads(𝑒 # ), 𝚤, 𝜎, 𝜌 ⇓ 𝚤, 𝜎, 𝜌 0
                                                                                
     h𝑒 #, 𝜎i ⇓Acc 𝑊𝑒 #           𝜌 0 = 𝜌 (𝑥, n) ↦→ ( 𝜌 (𝑥, n).𝑟, ∅, 𝜌 (𝑥, n).𝑏 ) (𝑥,n) ∈𝑊 #
                                                                                                            𝑒
                                                                                                                   CleaRMutates
                               ClearMutates(𝑒 # ), 𝚤, 𝜎, 𝜌 ⇓ 𝚤, 𝜎, 𝜌 0

                               h𝑒 #, 𝜎i ⇓Acc 𝑊𝑒 # h𝑒𝑧#, 𝜎i ⇓Acc 𝑊𝑒𝑧#
                                                                                                     
  𝜌 = 𝜌 (𝑥, n) ↦→ ( 𝜌 (𝑥, n).𝑟 ∪ R (𝜏𝑣 , 𝑡, 𝜏𝑞 , 𝜏𝑞∗, 𝑊𝑒𝑧# , 𝜌, 𝑔𝑠 # (𝜎, 𝚤)), 𝜌 (𝑥, n).𝑚, 𝜌 (𝑥, n).𝑏 ) (𝑥,n) ∈𝑊 #
    0
                                                                                                                                    𝑒
                                                                                                                                         RecoRdRead
                                hRecordRead(𝜏𝑣 , 𝑡, 𝑒 #, 𝜏𝑞 , 𝜏𝑞∗, 𝑒𝑧# ), 𝚤, 𝜎, 𝜌i ⇓ 𝚤, 𝜎, 𝜌 0

                               h𝑒 #, 𝜎i ⇓Acc 𝑊𝑒 # h𝑒𝑧#, 𝜎i ⇓Acc 𝑊𝑒𝑧#
                                                                                                     
  𝜌 = 𝜌 (𝑥, n) ↦→ ( 𝜌 (𝑥, n).𝑟, 𝜌 (𝑥, n).𝑚 ∪ R (𝜏𝑣 , 𝑡, 𝜏𝑞 , 𝜏𝑞∗, 𝑊𝑒𝑧# , 𝜌, 𝑔𝑠 # (𝜎, 𝚤)), 𝜌 (𝑥, n).𝑏 ) (𝑥,n) ∈𝑊 #
    0
                                                                                                                                    𝑒
                                                                                                                                         RecoRdMutate
                               hRecordMutate(𝜏𝑣 , 𝑡, 𝑒 #, 𝜏𝑞 , 𝜏𝑞∗, 𝑒𝑧# ), 𝚤, 𝜎, 𝜌i ⇓ 𝚤, 𝜎, 𝜌 0

                                                             temp∗                           pre∗                  
           𝜆 = 𝑟 ↦→ A (𝑟, 𝑔𝑠 # (𝜎, 𝚤), 𝜏𝑞full∗, 𝜏𝑞                   ) if W (𝑡, 𝑔𝑠 # (𝜎, 𝚤), 𝜏𝑞     , 𝑟 ) else 𝑟
                                      pre∗                 temp∗
                                                                                                                       Fence
                        Fence(𝑡, 𝜏𝑞          , 𝜏𝑞full∗, 𝜏𝑞         ), 𝚤, 𝜎, 𝜌 ⇓ 𝚤, 𝜎, lift(𝜌, 𝜆)

                                                                                          𝑘
                                                                                          Ù                        𝑘
                                                                                                                   Ø
                   #             #
                hh𝑒𝑧1 , · · · , 𝑒𝑧𝑘 i, 𝜎i ⇓Acc 𝑊𝑒 # , · · · ,𝑊𝑒 #           {(𝑧, n)} =        𝑊𝑒 #       W=            𝑊𝑒 #
                                                      𝑧1              𝑧𝑘                          𝑧𝑖                        𝑧𝑖
                                                                           𝑖=1                 𝑖=1
                                                           (𝑎,_)=𝜌 (𝑧,n)                          pre∗            
 𝜆 = 𝑟 ↦→ 𝑟 .𝑞, 𝑟 .∫, 𝑟 .𝑝 [(𝑧, n) ↦→ 𝑟 .𝑝 (𝑧, n) ∪ {𝑎}] 𝑧,n∈W              if W (𝑡, 𝑔𝑠 # (𝜎, 𝚤), 𝜏𝑞 , 𝑟 ) else 𝑟
  𝜌 0 = lift(𝜌, 𝜆)    (𝑅 0, 𝑀 0, (𝑎 0, 𝑤 0 )) = 𝜌 0 (𝑧, n)      𝜌 00 = 𝜌 0 [(𝑧, n) ↦→ (𝑅 0, 𝑀 0, (𝑎 0 + 1, 𝑤 0 ))]
                                                                                                                                        ARRive
                                                                  , 𝑒𝑧#∗ ), 𝚤, 𝜎, 𝜌 ⇓ 𝚤, 𝜎, 𝜌 00
                                                           pre∗
                                       Arrive(𝑡, 𝜏𝑞

 h𝑒𝑧#, 𝜎i ⇓Acc {(𝑧, n)}
                    (𝑎, 𝑤) = 𝜌 (𝑧, n).𝑏        Max ≜ if 𝑛 ≥ 0 then 𝑎 − (𝑛 + 1) else 𝑤 + 𝑛 + 1
                                                                
                  New ≜ if 𝑛 ≥ 0 then max 𝑤, Max + 1 else 𝑤 + 1                           
                                           temp∗ 
         𝜆 = 𝑟 ↦→ A 𝑟, 𝑔𝑠 # (𝜌), 𝜏𝑞full∗, 𝜏𝑞       if ∃𝑖. 𝑖 ≤ Max ∧ 𝑖 ∈ 𝑟 .𝑝 (𝑧, n) else 𝑟
  𝜌 0 = lift(𝜌, 𝜆)         (𝑅 0, 𝑀 0, (𝑎 0, _)) = 𝜌 0 (𝑧, n)               𝜌 00 = 𝜌 0 [(𝑧, n) ↦→ (𝑅 0, 𝑀 0, (𝑎 0, New))]
                                                                                                                                  Await
                                                                     , 𝑛), 𝚤, 𝜎, 𝜌 ⇓ 𝚤, 𝜎, 𝜌 00
                                                             temp∗
                               Await(𝑒𝑧#, 𝜏𝑞full∗, 𝜏𝑞

Fig. 22. The big-step operational semantics for Abstract Machine statements with sync environment up-
dates.




                                                                            29
