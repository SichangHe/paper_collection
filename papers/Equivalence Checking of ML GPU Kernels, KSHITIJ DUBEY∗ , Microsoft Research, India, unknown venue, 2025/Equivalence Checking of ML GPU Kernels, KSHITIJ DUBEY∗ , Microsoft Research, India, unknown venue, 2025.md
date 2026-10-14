                                         Equivalence Checking of ML GPU Kernels
                                         BENJAMIN DRISCOLL∗✉ , Stanford University, USA
                                         KSHITIJ DUBEY∗ , Microsoft Research, India
                                         ANJIANG WEI, Stanford University, USA
                                         NEERAJ KAYAL, Microsoft Research, India
                                         RAHUL SHARMA† , Google DeepMind, India
                                         ALEX AIKEN, Stanford University, USA
                                         With the rapid progress of deep learning and large language models (LLMs), companies spend enormous
                                         sums executing GPU kernels. These kernels have become prime targets for aggressive optimization. Recent
                                         efforts increasingly leverage LLMs to generate GPU kernels, but make no formal guarantees about the
                                         generated kernels. We present the first equivalence checker for GPU kernels and use it to formally verify the
                                         correctness of machine learning (ML) kernels optimized by hand, by LLM, and by compiler. We show that our
                                         equivalence checker is sound and, for a well-defined class of GPU kernels which includes many programs of
arXiv:2511.12638v3 [cs.PL] 16 Aug 2026




                                         interest, complete. Our implementation, Volta, can verify ML computations such as convolutions, matrix
                                         multiplications, and various attention mechanisms.
                                         CCS Concepts: • Theory of computation → Program verification.
                                         Additional Key Words and Phrases: equivalence checking, data races, GPU kernels, machine learning
                                         ACM Reference Format:
                                         Benjamin Driscoll, Kshitij Dubey, Anjiang Wei, Neeraj Kayal, Rahul Sharma, and Alex Aiken. 2026. Equivalence
                                         Checking of ML GPU Kernels. 1, 1 (August 2026), 29 pages. https://doi.org/10.1145/3839470

                                         1    Introduction
                                         Given two GPU kernels—a reference implementation and an optimized counterpart—our goal is to
                                         prove their extensional equivalence, i.e., that they produce identical outputs on all valid inputs,
                                         and, thereby, to verify the correctness of the optimized implementation. Equivalence checking has
                                         been extensively studied for over half a century [51] and recent works, such as Gupta et al. [29],
                                         have successfully proven the correctness of optimized CPU code. However, GPU programming
                                         introduces unique challenges arising from fine-grained synchronization among a massive number
                                         of threads and, to date, the literature proffers no equivalence checker for GPU programs.
                                            In the past few years, companies have begun to spend enormous sums executing the GPU
                                         kernels for deep learning and large language models. These kernels have become prime targets
                                         ∗ Both authors contributed equally to this research.
                                         † This work was done while the author was at Microsoft Research.


                                         Authors’ Contact Information: Benjamin Driscoll, Stanford University, Stanford, USA, bdrisc@cs.stanford.edu; Kshi-
                                         tij Dubey, Microsoft Research, Bengaluru, India, t-ksdubey@microsoft.com; Anjiang Wei, Stanford University, Stan-
                                         ford, USA, anjiang@cs.stanford.edu; Neeraj Kayal, Microsoft Research, Bengaluru, India, neeraka@microsoft.com; Rahul
                                         Sharma, Google DeepMind, Bengaluru, India, simplyrahul@google.com; Alex Aiken, Stanford University, Stanford, USA,
                                         aiken@cs.stanford.edu.

                                         Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee
                                         provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the
                                         full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored.
                                         Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires
                                         prior specific permission and/or a fee. Request permissions from permissions@acm.org.
                                         © 2026 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                         ACM XXXX-XXXX/2026/8-ART
                                         https://doi.org/10.1145/3839470


                                                                                                               , Vol. 1, No. 1, Article . Publication date: August 2026.
2                              Benjamin Driscoll, Kshitij Dubey, Anjiang Wei, Neeraj Kayal, Rahul Sharma, and Alex Aiken


for aggressive optimization, performed fully automatically by agents [5, 59, 75], or even the old-
fashioned way, manually [11] or by compilers [73]. Recent efforts increasingly leverage large
language models to generate GPU kernels. For example, NVIDIA has used DeepSeek-R1,1 Stanford
researchers have used OpenAI o3 and Gemini 2.5 Pro,2 the Kevin-32B model was trained with
reinforcement learning for kernel generation,3 Feature Search and Reinforcement combines search
with reinforcement learning to derive kernels [14], Standard Kernel is building AI infrastructure for
kernel generation,4 and mako offers an interface for generating GPU kernels with different LLMs.5
Some of these efforts, such as Standard Kernel and mako, subject kernels to a range of empirical
correctness checks, program analyses, and/or agent review, but none currently provides formal
correctness guarantees. Such guarantees offer greater confidence than empirical validation alone,
which can be valuable before deployment in a production setting, where bugs can be costly.
   GPU kernels execute thousands of threads in parallel on runtimes such as NVIDIA’s CUDA [55]
or AMD’s ROCm [1], which can introduce subtle concurrency errors that testing alone cannot
reliably detect. One major source of such errors is data races, which may appear only in extremely
rare executions or may remain latent when kernels rely on implicit synchronization that happens
only for a specific version of the test runtime or the test hardware but that is not guaranteed
to hold in general. For example, a widely cited GPU programming tutorial [30] relies on warp-
level synchronization that was removed after CUDA 9.0 [9]. Testing-based correctness checking
is further complicated by floating-point arithmetic. GPU optimizations often reorder arithmetic
operations, causing small numerical differences between the outputs of the reference and optimized
implementations. Such variations are usually tolerated in tests, yet similar deviations can arise
from genuine semantic bugs. For instance, an unsound optimization that omits a clipping operation
may seem acceptable for some test inputs even though it reduces overall model accuracy. While
compilers rarely introduce such mistakes, they are plausible when kernels are hand-optimized by
human programmers or generated by agents.
   State-of-the-art equivalence checking supports single-threaded integer programs [29] and high-
level tensor operations [3, 78], but it is not obvious how to decompose the equivalence checking of
GPU kernels into single-threaded sub-tasks. In an optimized kernel, there may be no one-to-one
correspondence between its threads and the threads in the reference implementation. In addition,
existing techniques have no support for synchronization among multiple threads.
   Although equivalence checking is undecidable in general and GPUs allow programmers to write
arbitrary code, efficient GPU kernels typically follow structural patterns that, incidentally, make
formal reasoning feasible. We assume that the programs analyzed by our equivalence checker are
structured-CTAs. Importantly, the number of threads, the sizes of tensors, the targets of pointers,
and the values of any expressions that are branched on must be statically known. Although it is
easy to construct programs that violate these assumptions and render our techniques inapplicable,
we and others [39, 46, 67] observe that these assumptions very often hold in practice (Section 3.2).
For example, JAX, a popular ML framework, requires tensor dimensions to be fixed6 ; the underlying
XLA compiler requires tensor sizes and data flow graphs to be known a priori to perform aggressive
optimizations. We discuss structured-CTAs further in Section 3.2 and formally define them in
Section 4.1. Our implementation, Volta,7 checks that its input is a structured-CTA and raises an

1 https://developer.nvidia.com/blog/automating-gpu-kernel-generation-with-deepseek-r1-and-inference-time-scaling
2 https://crfm.stanford.edu/2025/05/28/fast-kernels.html
3 https://cognition.ai/blog/kevin-32b
4 https://standardkernel.com
5 https://generate.mako.dev
6 https://docs.jax.dev/en/latest/notebooks/Common_Gotchas_in_JAX.html#dynamic-shapes
7 Verification Of Large Thread Arrays



, Vol. 1, No. 1, Article . Publication date: August 2026.
Equivalence Checking of ML GPU Kernels                                                                           3


exception if it is not. Finally, we note that, while our work focuses on kernels targeting NVIDIA
GPUs due to their widespread adoption, the techniques are also applicable to other GPU runtimes.
    The core of our equivalence checker is symbolic evaluation. Consider a tensor computation—a
workload that dominates machine learning. We symbolically execute the reference computation
under an arbitrary, fixed schedule to derive an expression over R that represents the output tensor
as a function of the input tensors, discovering any races or deadlocks as we go. Our main technical
result, confluence, which we formally verify in the Agda [54] proof assistant, guarantees that all
symbolic evaluator schedules lead to the same expression or report a race or deadlock. The same
procedure is applied to the optimized computation. Finally, we apply a procedure to decide equality
of the two symbolic expressions and, if they are equal, we conclude that the optimized kernel is
semantically equivalent to the reference kernel, for all schedules.
    We are not aware of a proof in the literature that the symbolic identities we encounter are
decidable, though there is work on related problems, e.g., [43, 49]. In particular, in Section 4.4, we
                                                           ¯ ℎ𝑖 (𝑥¯ ) = 0, given multivariate polynomials
                                                 Í
prove decidability for equalities of the form 𝑚    𝑖=1 𝑝𝑖 (𝑥)𝑒
                    ¯ It is worth noting that optimized kernels are almost never bit-wise equivalent
𝑝 1, ℎ 1, . . . ∈ R[𝑥].
to the reference implementation in floating-point arithmetic, since most optimizations reorder
arithmetic operations when distributing work among GPU threads.
    Although there is no prior equivalence checker for GPU programs, there are prior verification
frameworks that check weaker properties such as data race freedom [46]. Our equivalence checker,
Volta, soundly verifies data race and deadlock freedom of kernels utilizing barrier synchronization
(Theorem 1) in time proportional to the number of instructions. It satisfies a true positives property,
which guarantees that every reported data race or deadlock corresponds to a concrete schedule that
triggers erroneous behavior (Theorem 2). Barrier synchronization operations include mma.sync and
syncwarp, which programmers commonly employ when accelerating machine learning workloads
with tensor cores [56]. We compare with data race checking tools in Section 6.4 and Section 7.
    Volta checks the identities output by its symbolic executor in less than 3 minutes on all evaluated
benchmarks, including convolution, matrix multiplication, and attention (Section 6). Volta operates
as a black-box equivalence checker, requiring no information about how an optimized kernel was
produced; it verifies correctness solely from the assembly corresponding to the optimized program
itself. In particular, Volta analyzes PTX assembly, the lowest documented level of the stack for
NVIDIA GPUs [58]. Operating at the PTX level enables our approach to handle various developer
front-ends. For example, GPU programmers can write CUDA kernels or CUTLASS templates [19].
NVIDIA’s nvcc compiler translates both into PTX.
    In sum, we make the following contributions:

    • A linear time algorithm for detecting races and deadlocks for a class of GPU kernels, structured
      CTAs, utilizing barrier synchronization.
                                                                     ¯ ℎ𝑖 (𝑥¯ ) = 0, given multivariate
                                                           Í
    • A proof of decidability for equalities of the form 𝑚   𝑖=1 𝑝𝑖 (𝑥)𝑒
                                      ¯
      polynomials 𝑝 1, ℎ 1, . . . ∈ R[𝑥].
    • The first equivalence checker for a practical class of GPU kernels (again, structured CTAs),
      Volta, that can verify the correctness of optimized convolutions, matrix multiplications,
      reductions, and attention mechanisms. We prove that Volta guarantees data race freedom
      and satisfies a true positives property, and we formalize the key, constituent lemma in Agda.

  The rest of the paper is as follows. Section 2 shows, at a high-level, how Volta verifies a
motivating example. Section 3 provides background on GPU architecture, synchronization, and ML
GPU kernels. Section 4 describes our symbolic execution algorithm formally. Section 4.3 establishes
our main technical results. Section 5 describes Volta’s implementation and Section 6 evaluates it

                                                          , Vol. 1, No. 1, Article . Publication date: August 2026.
4                             Benjamin Driscoll, Kshitij Dubey, Anjiang Wei, Neeraj Kayal, Rahul Sharma, and Alex Aiken


across a diverse set of GPU kernels, demonstrating its ability to verify realistic programs and detect
bugs. Section 7 reviews related work and Section 8 concludes with directions for future research.

2   Motivating Example

                                                            __global__ void
                                                            online_softmax ( float *x , float *y , int N ) {
__global__ void                                                 int tid = threadIdx . x ;
softmax ( float *x , float *y , int N ) {
    extern __shared__ float buf [];                             float m = - INFINITY ;   // running max
                                                                float d = 0.0 f ;        // running denom
     int tid = threadIdx . x ;
     buf [ tid ] = expf ( x [ tid ]);                           for ( int i = 0; i < N ; i ++) {
     __syncthreads ();                                                float v = x [ i ];
                                                                      float new_m = fmaxf (m , v );
     float sum = 0.0 f ;                                              d = d * expf ( m - new_m ) + expf ( v - new_m );
     for ( int i = 0; i < N ; i ++)                                   m = new_m ;
          sum += buf [i ];                                      }
     y[ tid ] = buf [ tid ] / sum ;                             y [ tid ] = expf ( x [ tid ] - m ) / d ;
     return ;                                                   return ;
}                                                           }

                  (a) Naive Softmax                                    (b) Online Softmax (FlashAttention)

Fig. 1. Naive softmax (left) requires materializing all exponentiations in shared memory; online softmax (right,
used in FlashAttention) maintains a running max and normalization factor, enabling numerically stable and
memory-efficient streaming.

   As a motivating example, consider the softmax computation, which appears in the attention
mechanism of large language models (LLMs). Attention is the primary performance bottleneck
during LLM inference with long contexts [21]. Listing 1a presents a naive reference implementation
of softmax in CUDA. In this example, we use 𝑁 = 4, meaning that four GPU threads operate on a
vector [𝑥 1, 𝑥 2, 𝑥 3, 𝑥 4 ] to compute [𝑦1, 𝑦2, 𝑦3, 𝑦4 ], where
                                                           Í         
                                               𝑦𝑖 = 𝑒 𝑥𝑖 / 4𝑗=1 𝑒 𝑥 𝑗                           (1)
   The parameter 𝑁 is typically known at compile time. Kernels are often specialized for particular
values of 𝑁 , since a single CUDA kernel rarely achieves optimal performance across all possible
configurations.
   Listing 1a uses an array, buf, stored in shared memory, a software-managed cache accessible to
all threads within a thread block. Each thread has a unique identifier, tid, and thread 𝑖 stores 𝑒 𝑥𝑖 in
buf. The syncthreads call is a barrier primitive that synchronizes all the threads, ensuring that all
shared memory writes are visible before any thread proceeds. After synchronization, each thread 𝑖
                                                              𝑒 𝑥𝑖
sums the elements of buf into the variable sum and writes sum      to 𝑦𝑖 .
   Listing 1b gives a softmax implementation used in FlashAttention [21], a major advance in
the implementation of attention mechanisms. It employs an online softmax computation that is
both numerically stable and avoids the use of shared memory. This formulation enables tiling
optimizations that are key to FlashAttention’s performance. The two softmax implementations
shown in Figure 1 are not bit-wise identical due to floating-point rounding differences, yet both are
intended to compute the mathematical expression in Equation 1. Volta is designed to verify that
they both, in fact, compute this expression.
   Conceptually, our analysis expands the softmax kernel into a list of per-thread programs, where
the 𝑖 𝑡ℎ program represents the code executed by thread 𝑖.

, Vol. 1, No. 1, Article . Publication date: August 2026.
Equivalence Checking of ML GPU Kernels                                                                                           5


                            tid=0                   tid=1                 tid=2                 tid=3
                      buf[0] = exp(x[0]);     buf[1] = exp(x[1]);   buf[2] = exp(x[2]);   buf[3] = exp(x[3]);
                       __syncthreads();        __syncthreads();      __syncthreads();      __syncthreads();
                           sum = 0;                sum = 0;              sum = 0;              sum = 0;
                        sum += buf[0];          sum += buf[0];        sum += buf[0];        sum += buf[0];
                        sum += buf[1];          sum += buf[1];        sum += buf[1];        sum += buf[1];
                        sum += buf[2];          sum += buf[2];        sum += buf[2];        sum += buf[2];
                        sum += buf[3];          sum += buf[3];        sum += buf[3];        sum += buf[3];
                      y[0] = buf[0]/sum;      y[1] = buf[1]/sum;    y[2] = buf[2]/sum;    y[3] = buf[3]/sum;


Fig. 2. Naive softmax execution for N=4 threads. Each column shows the code executed by a single thread
indexed by tid.


   Figure 2 illustrates the expanded program. Observe that the code executed by each thread is
straight-line, containing no branches or loops. Moreover, the addresses corresponding to all memory
accesses are statically known.
   Note that this representation is shown only for clarity of exposition. In fact, the actual imple-
mentation (Section 5) never constructs the fully expanded program, nor does it perform other AST
transformations. It operates over the original program, requiring that values are sufficiently static
such that the symbolic executor can resolve all control flow.
   Given the program, Volta performs simple round-robin scheduling: it iterates over each column
until a thread encounters a syncthreads barrier and blocks. For each thread, all shared memory
locations that are read or written are recorded. When a thread is blocked, Volta proceeds to the
next active thread. If the recorded accesses reveal any data races, Volta generates an error report.
Once all threads reach the corresponding barrier, the recorded information is cleared, and all threads
become active. If all threads become blocked, there is a deadlock and Volta also generates an error
report. In Figure 2, if the syncthreads barrier is missing, Volta reports data races. For example,
when analyzing the thread with tid 0, the analysis records a read from buf[1]. Subsequently, when
analyzing the thread with tid 1, it reports a data race between the read of buf[1] in thread 0 and
the write to buf[1] in thread 1.
   Given Listing 1a, the executor produces the following, symbolic output state:8
              𝑒 𝑥0                𝑒 𝑥1                𝑒 𝑥2                𝑒 𝑥3
  𝑦naive [0] =     , 𝑦naive [1] =      , 𝑦naive [2] =      , 𝑦naive [3] =      , 𝐷 = ((𝑒 𝑥 0 + 𝑒 𝑥 1 ) + 𝑒 𝑥 2 ) + 𝑒 𝑥 3
               𝐷                   𝐷                   𝐷                   𝐷
   Confluence (Lemma 1) guarantees that, since we did not detect a data race, if we had used some
other schedule different from the round-robin scheduling of Volta, we would still end up with an
identical output state. Likewise, since we did not encounter a deadlock, no schedule will deadlock.
Repeating the same process for the online softmax in Listing 1b produces the following output:
                              𝑒 𝑥 0 −𝑀3              𝑒 𝑥 1 −𝑀3              𝑒 𝑥 2 −𝑀3              𝑒 𝑥 3 −𝑀3
                 𝑦opt [0] =             , 𝑦opt [1] =           , 𝑦opt [2] =           , 𝑦opt [3] =
                                  𝐷                      𝐷                      𝐷                      𝐷
where
                         𝑀1 = max(𝑥 0, 𝑥 1 ), 𝑀2 = max(𝑀1, 𝑥 2 ), 𝑀3 = max(𝑀2, 𝑥 3 )
and                                                                      
                        𝐷=        𝑒 𝑥 0 −𝑀1 + 𝑒 𝑥 1 −𝑀1 𝑒 𝑀1 −𝑀2 + 𝑒 𝑥 2 −𝑀2 𝑒 𝑀2 −𝑀3 + 𝑒 𝑥 3 −𝑀3
Finally, we create the following decision problem,
                                            ∀𝑖 ∈ {0, 1, 2, 3}. 𝑦naive [𝑖] = 𝑦opt [𝑖]
8We add the subscript “naive” in 𝑦
                                     naive to disambiguate it from the output of the optimized computation.


                                                                          , Vol. 1, No. 1, Article . Publication date: August 2026.
6                             Benjamin Driscoll, Kshitij Dubey, Anjiang Wei, Neeraj Kayal, Rahul Sharma, and Alex Aiken


  Our decision procedure (Section 4.4) successfully validates these identities, allowing Volta to
conclude that the two programs in Figure 1 are equivalent. As an additional contribution, we
demonstrate the decidability of such identities (Section 4.4).

3     Background
We begin with necessary background on GPUs. To execute a task on a GPU, the CPU host launches
a grid of cooperative thread arrays (CTAs), also known as thread-blocks. All CTAs share access
to global memory (HBM), typically sized in gigabytes. Different CTAs in a grid usually write to
disjoint regions of global memory due to the cost of inter-CTA synchronization, which was not
even possible for many GPU generations. The GPU hardware schedules each CTA on a streaming
multiprocessor (SM); a modern GPU may contain hundreds of SMs. The resources assigned to each
SM are limited and hence each CTA is tasked to compute only a tile of the output tensor. Each
CTA consists of 128 to 1024 threads, depending on the hardware generation. Within a CTA, threads
are grouped into warps, each consisting of 32 threads. Every thread maintains its own registers for
local storage, while shared memory serves as a software-managed cache accessible to all threads in
the same CTA. To coordinate access to shared memory, threads must use explicit synchronization
operations. Missing synchronization leads to data races and over synchronization leads to loss of
performance. The shared memory available per CTA ranges from 48 KB to 256 KB, depending on the
GPU architecture. In a typical CTA, threads first load data from global memory into shared memory,
perform arithmetic operations while keeping intermediate values in registers or shared memory,
and finally write the results back to global memory. Writing code for efficient CTAs is challenging
because programmers must reason about massive thread-level parallelism and low-level hardware
details. Volta aims to statically identify incorrect or unsafe optimizations. We next describe the
synchronization mechanisms available on GPUs.

3.1    Synchronization Operations
NVIDIA GPUs support independent thread scheduling, meaning that in the absence of explicit
synchronization, each thread executes independently. The fundamental synchronization primitive
is syncthreads, a barrier that spans all threads within a CTA. Threads that reach the barrier earlier
are suspended until all threads in the CTA arrive or exit, at which point execution resumes for all
of the threads blocked at the barrier.
   Another synchronization primitive is syncwarp, which operates on a user-specified subset of
threads within a single warp. This mechanism is commonly used when programming tensor cores—
CUDA intrinsics such as wmma::mma_sync synchronize all threads in a warp to perform matrix
multiplication. Most prior verification techniques for GPU kernels support only syncthreads and
therefore cannot reason about machine learning kernels that rely on warp-level synchronization.
While syncthreads is deadlock free (per the CUDA documentation, it can only be placed under
conditionals that evaluate uniformly across the entire CTA), syncwarp can introduce deadlocks.
   In summary, the synchronization mechanisms we consider are barriers that block subsets of the
available threads. Asynchronous producer-consumer-style primitives such as arrive are beyond
the scope of this paper. The race checking mechanism of Volta could potentially be swapped out
for a more general, if less efficient, mechanism such as a happens-before analysis in the style of
Sharma et al. [67], without disrupting the rest of the system, but we leave this for future work.

3.2    Why Structured-CTAs?
In this section, we discuss, at a high level, the assumptions that Volta makes about input kernels.
We first state our assumptions, then motivate them. Note that these assumptions are checked:
Volta raises an exception if a kernel does not satisfy our requirements (Section 5).

, Vol. 1, No. 1, Article . Publication date: August 2026.
Equivalence Checking of ML GPU Kernels                                                                          7


   To be checked for equivalence, a program must operate on a known number of CTAs and threads
per CTA. Each CTA must operate over tensor tiles whose sizes are statically known. In each thread
of each CTA, given the tid (thread ID), all branch targets and addresses used in memory accesses
must be statically known. We compare kernels CTA-to-CTA, so we do not support equivalence
checking of optimizations that mix responsibilities between CTAs. In Section 4.1, we define a
language of structured-CTAs, formally encoding these assumptions, and, in Section 4.3, prove the
completeness of Volta for such programs.
   Structured-CTAs reflect well-established best practices for achieving high GPU performance,
as supported by empirical study. A large-scale analysis of GPGPU kernels in the wild found that
most memory accesses are control independent and data independent [46] (59.5% of 2770 programs).
Similarly, a study of the CUDA SDK showed that most programs exhibit access invariance [39],
meaning that threads perform the same memory accesses for all inputs (52 out of 76). Weft [67],
a race detector for scientific and cudaDMA kernels, makes all of the above assumptions—all 26
scientific computations studied by Weft fall into the aforementioned class.
   Moreover, we are focused on the kernels that are performance bottlenecks in the training or
inference of machine learning (ML) models, such as matrix multiplications, convolutions, and
multi-head attention. In these workloads, the structure of the ML model is fixed: tensor entries
depend on runtime inputs, but tensor sizes are statically known. Kernels are therefore specialized
for particular tensor dimensions to achieve maximum performance. In fact, JAX [12], a popular ML
framework, only permits tensors with fixed dimensions.
   Once tensor shapes are known, loop bounds can also be determined, since the bounds in ten-
sor operations depend only on tensor shapes. Volta can statically evaluate these loops to “flat”
expressions that do not contain conditionals, effectively unrolling them. We also require that the
targets of conditional branches can be statically resolved; note this restriction exploits the fact that
efficient machine learning kernels do not make truly data dependent runtime decisions. Under
these assumptions, the code executed by each individual thread can be represented as straight-line,
no dynamic branches or loops. It is common for threads to branch on predicates of their thread
index or of a loop index (counting up to some tensor dimension); however, such control flow still
preserves the straight-line property for each thread’s execution. For example, causal masking in
FlashAttention [21] branches on whether an array index is above or below the diagonal, but this is
a static condition given the tensor shape.
   Efficient GPU kernels carefully orchestrate memory transfers by coalescing accesses to global
memory and avoiding shared memory bank conflicts. As a result, GPU programmers typically
define memory access patterns statically, making memory addresses independent of the tensor
contents. Consequently, when a straight-line thread accesses an array element, both the base array
and the exact index can be determined statically. This property allows the symbolic evaluator to
record memory accesses precisely and to detect data races accurately.
   Typically, ML kernels launch a grid of CTAs where the code of each CTA is identical and differs
only in the instantiation of free variables blockIdx.x, blockIdx.y, and blockIdx.z. Each CTA is
responsible for computing a fixed-size tile of the output tensor. Many GPU optimizations focus on
this CTA-level code. For instance, the CTA code can be modified to use tensor cores. When checking
a reference kernel against an optimized kernel, we focus on proving equivalence between the code
of a CTA from the reference kernel and the code of the corresponding CTA in the optimized kernel.
Hence, correctness checking of optimizations that change the number of CTAs launched in a grid
is beyond the scope of this work. Since each pair of CTAs can be checked independently of one
another, following prior work [67], our evaluation simply checks the equivalence of the CTAs with
blockIdx.x = blockIdx.y = blockIdx.z = 0 in the reference and the optimized kernels.


                                                         , Vol. 1, No. 1, Article . Publication date: August 2026.
8                             Benjamin Driscoll, Kshitij Dubey, Anjiang Wei, Neeraj Kayal, Rahul Sharma, and Alex Aiken



           Statement                𝑠      F 𝑟 := 𝑐 | 𝑟 := 𝑟 1 ⊕ 𝑟 2 | 𝑟 := 𝑟 ′ | 𝑟 := ∗𝑔 | ∗𝑔 := 𝑟 | sync 𝐼
           Thread Program 𝑇                F        return | 𝑠 # 𝑇
           Program                  𝑃      F        ⋄|𝑃 ∥𝑇

                                Fig. 3. Syntax of L, the language of structured-CTAs.




   Which practical kernels fall outside the class of structured-CTAs? Notably, top-𝑘/argsort kernels
do, as commonly used for expert selection in mixture-of-experts models, beam search, and rank-
ing. Their control flow is data dependent—comparison results determine swap operations—and
implementations often use atomic operations for parallel reductions across CTAs.
   Finally, a sound equivalence checker operating over floating-point arithmetic would likely reject
many aggressively optimized kernels; IEEE-754 is not even associative. In practice, both developers
and domain-specific compilers treat tensor values as real numbers when applying optimizations.
Such transformations, similar in spirit to the –ffast-math option in gcc, are unsound for floating-
point arithmetic. Volta follows the same convention as existing optimizers and models tensor
elements as reals.

4     Algorithm
Our equivalence checker proceeds in two phases. The first phase symbolically executes a pair of
programs, determining whether they are data race free and, if so, expresses their output values
as terms of symbolic input tensors. If both programs are data race free, we proceed to the second
phase, which verifies that, for each output element, the symbolic terms derived for both programs
are equal. For example, when analyzing Listing 1a, the symbolic evaluator starts with environment
{𝑥 [0] := 𝛼, 𝑥 [1] := 𝛽, 𝑥 [2] := 𝛾, 𝑥 [3] := 𝛿 } for fresh symbols 𝛼, 𝛽, 𝛾, 𝛿. It determines there is no data
race and outputs a symbolic state with 𝑦 [0] := 𝑒 𝛼 /(𝑒 𝛼 + 𝑒 𝛽 + 𝑒𝛾 + 𝑒 𝛿 ).

4.1    Formal Setting
As a setting to formalize our analysis, we develop a simple language L of structured-CTAs capturing
the relevant aspects of PTX. The syntax of L programs is given in Figure 3 in terms of registers 𝑟 ,
constants 𝑐, shared memory addresses 𝑔, and sets of thread IDs (TIDs) 𝐼 . We give L a dynamics via
a pair of small-step relations, (G, R, 𝑃) → (G, R, 𝑃) and (G, 𝑅,𝑇 ) → (G, 𝑅,𝑇 ):


                                     Schd
                                               (G, R (𝑖), 𝑃 (𝑖)) → (G ′, 𝑅 ′,𝑇 ′ )
                                        (G, R, 𝑃) → (G ′, R [𝑖 ↦→ 𝑅 ′ ], 𝑃 [𝑖 ↦→ 𝑇 ′ ])



           Sync
                                             ∀𝑖 ∉ 𝐼 . 𝑃 ′ (𝑖) = 𝑃 (𝑖)
            ∀𝑖 ∈ 𝐼 . (𝑃 (𝑖) = return ∧ 𝑃 (𝑖) = return) ∨ (∃𝑇𝑖 . 𝑃 (𝑖) = sync 𝐼 # 𝑇𝑖 ∧ 𝑃 ′ (𝑖) = 𝑇𝑖 )
                                                ′

                                                    (G, R, 𝑃) → (G, R, 𝑃 ′ )

, Vol. 1, No. 1, Article . Publication date: August 2026.
Equivalence Checking of ML GPU Kernels                                                                                 9

Const                                              BinOp

(G, 𝑅, 𝑟 := 𝑐 # 𝑇 ) → (G, 𝑅 [𝑟 ↦→ 𝑐],𝑇 )           (G, 𝑅, 𝑟 := 𝑟 1 ⊕ 𝑟 2 # 𝑇 ) → (G, 𝑅 [𝑟 ↦→ 𝑅(𝑟 1 ) ⊕ 𝑅(𝑟 2 )],𝑇 )

      RdReg                                                  RdMem

      (G, 𝑅, 𝑟 := 𝑟 ′ # 𝑇 ) → (G, 𝑅 [𝑟 ↦→ 𝑅(𝑟 ′ )],𝑇 )        (G, 𝑅, 𝑟 := ∗𝑔 # 𝑇 ) → (G, 𝑅 [𝑟 ↦→ G(𝑔)],𝑇 )

                                  WrMem

                                  (G, 𝑅, ∗𝑔 := 𝑟 # 𝑇 ) → (G [𝑔 ↦→ 𝑅(𝑟 )], 𝑅,𝑇 )

   The top-level small-step relation is indexed by configurations (G, R, 𝑃) where G models shared
memory and is a map from addresses to values, R models the threads’ register files and is a map
from TIDs to registers to values, and 𝑃 is the current program. We will consider both concrete
program executions, where values are drawn from R, and abstract program executions, where
values are symbolic.
   Schd allows any thread 𝑖 (which is not blocked at a sync) to be advanced, modeling the non-
deterministic execution of the machine. We use 𝑓 [𝑥 ↦→ 𝑦] to denote the function which takes
value 𝑦 at 𝑥 and is 𝑓 elsewhere. The second top-level rule, Sync, advances the threads blocked
at a sync 𝐼 , but only if every thread in 𝐼 is at a sync 𝐼 or return. When 𝐼 = {1, . . . , 𝑁 } for 𝑁 the
size of a thread block, sync models the PTX instruction syncthreads. When 𝐼 ⊆ {𝑘, . . . , 𝑘 + 31}
with 𝑘 mod 32 = 1, sync models the warp-level barriers, e.g., syncwarp with a mask or tensor core
mma.sync. Permitting threads in 𝐼 to be at a return captures the flexibility of PTX, which allows
threads to terminate early. The program is stuck if a thread 𝑖 1 synchronizes on 𝐼 1 and another 𝑖 2
on 𝐼 2 , where 𝐼 1 ≠ 𝐼 2 and 𝑖 1, 𝑖 2 ∈ 𝐼 1 ∩ 𝐼 2 . Although some GPU architectures may permit specific
combinations of 𝐼 1 and 𝐼 2 to proceed without deadlock, we conservatively treat all such cases as
stuck. Finally, note that sync operations are not named: as with syncthreads in CUDA, whichever
sync instances happen to align in the dynamics are matched with one another. (In fact, because
control flow in a structured-CTA cannot depend on runtime values, the same instances align in
every execution.)
   The other small-step relation given above is a thread-level relation indexed by configurations
(G, 𝑅,𝑇 ). G is, again, a map from addresses to values, modeling shared memory, 𝑅 is the current
thread’s register file, and 𝑇 is the current thread’s program. Const, BinOp, RdReg, RdMem, and
WrMem perform the obvious updates to G and 𝑅. ⊕ models the various arithmetic operations
handled by the real implementation, Volta. Note that there is no thread-level small-step rule for a
thread program of the form sync 𝐼 # 𝑇 ′ —one must use the top-level Sync rule.
   Note that, for confluence (Lemma 1), it will be essential that (dynamic) control flow cannot affect
whether a sync executes or the set of addresses read and written, which is why thread programs
are straight-line sequences of statements. That said, the formalism is more permissive than it may
first appear: the operators ⊕ are black boxes, assumed only to be pure functions of their register
operands, and can therefore “hide” control flow. For example, ⊕ could be max implemented via a
branch.

4.2     Symbolic Execution
A program trace is a derivation of the reflexive, transitive closure of (G, R, 𝑃) → (G, R, 𝑃), which
we denote (G, R, 𝑃) →∗ (G, R, 𝑃). A data race occurs between two memory accesses 𝑎𝑖 and 𝑎 𝑗
when at least one is a write (a Schd of a WrMem) and there exist two traces, one in which 𝑎𝑖 is
directly followed by 𝑎 𝑗 and another in which 𝑎 𝑗 is directly followed by 𝑎𝑖 . This is the definition

                                                                , Vol. 1, No. 1, Article . Publication date: August 2026.
10                            Benjamin Driscoll, Kshitij Dubey, Anjiang Wei, Neeraj Kayal, Rahul Sharma, and Alex Aiken


used by, e.g., Brookes [13].9 Since data races are typically bugs and it is not clear, in general, how
equivalence should be defined for programs that race, we extend the dynamics of L to return error
value ⊥ if the program has a data race and use this extended dynamics when performing symbolic
execution.
  Concretely, we maintain an extra context X tracking: (1) for each address 𝑔 and each thread 𝑖, all
threads 𝑗 that have not performed a sync with 𝑖 since it last read 𝑔; (2) for each address 𝑔, the last
writer 𝑖 and all threads 𝑗 that have not performed a sync with 𝑖 since it wrote 𝑔. That is,

                       X : MemEvs ≜ Addr → (TID → 𝒫(TID)) × (TID × 𝒫(TID))

Races arise because a thread reads an address before synchronizing with its last writer, or writes
an address before synchronizing with its previous readers and its last writer. We define a predicate
noRacingRd taking a thread 𝑖 and the read data of X(𝑔) and determining whether 𝑖 has synchronized
with all other readers of 𝑔 as required. Likewise, we define a predicate noRacingWr taking a thread
𝑖 and the write data of X(𝑔) and determining whether 𝑖 is or has synchronized with the last writer
of 𝑔 as required.

                                noRacingRd : TID → (TID → 𝒫(TID)) → Prop
                                noRacingRd(𝑖, rd) ≜ ∀𝑗 . 𝑖 = 𝑗 ∨ 𝑖 ∉ rd( 𝑗)
                                noRacingWr : TID → TID × 𝒫(TID) → Prop
                                noRacingWr(𝑖, ( 𝑗, 𝐽 )) ≜ 𝑖 = 𝑗 ∨ 𝑖 ∉ 𝐽

We can now refine our thread-level small-step relation. The new relation (X, G, 𝑅,𝑇 ) ↩→𝑖
(X ′, G ′, 𝑅,𝑇 ) tracks the TID of the thread 𝑖 being executed, and includes an X in its configurations.
The non-trivial changes are to RdMem and WrMem. Letting I be the set of all TIDs:

                     RdMem’
                      (rd, wr) = X(𝑔)             noRacingWr(𝑖, wr)          𝑥 ′ = (rd[𝑖 ↦→ I], wr)
                          (X, G, 𝑅, 𝑟 := ∗𝑔 # 𝑇 ) ↩→𝑖 (X [𝑔 ↦→ 𝑥 ′ ], G, 𝑅 [𝑟 ↦→ G(𝑔)],𝑇 )

          WrMem’
           (rd, wr) = X(𝑔)            noRacingRd(𝑖, rd)          noRacingWr(𝑖, wr)             𝑥 ′ = (rd, (𝑖, I))
                          (X, G, 𝑅, ∗𝑔 := 𝑟 # 𝑇 ) ↩→𝑖 (X [𝑔 ↦→ 𝑥 ′ ], G [𝑔 ↦→ 𝑅(𝑟 )], 𝑅,𝑇 )

Next, we must adjust Sync so that X is updated appropriately:
           Sync’
                                             ∀𝑖 ∉ 𝐼 . 𝑃 ′ (𝑖) = 𝑃 (𝑖)
            ∀𝑖 ∈ 𝐼 . (𝑃 (𝑖) = return ∧ 𝑃 (𝑖) = return) ∨ (∃𝑇𝑖 . 𝑃 (𝑖) = sync 𝐼 # 𝑇𝑖 ∧ 𝑃 ′ (𝑖) = 𝑇𝑖 )
                                              ′

                                     (X, G, R, 𝑃) ↩→ (syncMem(𝐼, X), G, R, 𝑃 ′ )

             syncMemRd(𝐼, rd) (𝑖) ≜ (rd(𝑖) \ 𝐼 ) if 𝑖 ∈ 𝐼 else rd(𝑖)
             syncMemWr(𝐼, ( 𝑗, 𝐽 )) ≜ ( 𝑗, 𝐽 \ 𝐼 ) if 𝑗 ∈ 𝐼 else ( 𝑗, 𝐽 )
             syncMem(𝐼, X) (𝑔)            ≜ (syncMemRd(𝐼, 𝜋1 (X(𝑔))), syncMemWr(𝐼, 𝜋 2 (X(𝑔))))

9We could define a data race without requiring that 𝑎
                                                       𝑖 and 𝑎 𝑗 follow each other directly. There exist traces in which they
occur in different orders and follow each other directly iff there exist traces in which they occur in different orders.


, Vol. 1, No. 1, Article . Publication date: August 2026.
Equivalence Checking of ML GPU Kernels                                                                                 11


Finally, we would like symbolic execution to error when a race is detected rather than getting stuck:
                                  RdMemBad
                                  (rd, wr) = X(𝑔)          ¬noRacingWr(𝑖, wr)
                                          (X, G, 𝑅, 𝑟 := ∗𝑔 # 𝑇 ) ↩→𝑖 ⊥

  WrMemBad                                                                            SchdBad
  (rd, wr) = X(𝑔)          ¬noRacingRd(𝑖, rd) ∨ ¬noRacingWr(𝑖, wr)                     (X, G, R (𝑖), 𝑃 (𝑖)) ↩→𝑖 ⊥
                        (X, G, 𝑅, ∗𝑔 := 𝑟 # 𝑇 ) ↩→𝑖 ⊥                                      (X, G, R, 𝑃) ↩→ ⊥
  We write the reflexive, transitive closure of (X, G, R, 𝑃) ↩→ (X ′, G ′, R ′, 𝑃 ′ ) as (X, G, R, 𝑃) ↩→∗
(X ′, G ′, R ′, 𝑃 ′ ).
  Note that the formalism assumes all addresses are valid, though validity could be tracked by
enriching the codomain of G and 𝑅 and adding a check in RdMem’ and WrMem’.

4.3   Guarantees
We prove the soundness (Theorem 5) and completeness (Theorem 6) of our symbolic evaluation
based equivalence checking. For soundness, we prove that if execution of two programs under
the checked dynamics · ↩→ · with symbolic inputs produces equal terms, then those programs
evaluate to the same expression under the usual, unchecked dynamics · → · for all inputs in R. The
central challenge lies in reasoning about the apparent non-determinism introduced by Schd’. Since
symbolic execution selects an arbitrary unblocked thread of the program for execution at each step,
we must show that, for all programs, all possible schedules either produce the same output G, R,
raise an error ⊥ (indicating a data race), or become stuck (indicating a deadlock). Our key lemma is
the following, which we verify in the Agda [54] proof assistant:
  Lemma 1 (Confluence). If (X, G, R, 𝑃) ↩→∗ (X1, G1, R 1, 𝑃1 ) and (X, G, R, 𝑃) ↩→∗ (X2, G2, R 2, 𝑃2 )
then there exists X ′, G ′, R ′, 𝑃 ′ such that (X1, G1, R 1, 𝑃1 ) ↩→∗ (X ′, G ′, R ′, 𝑃 ′ ) and (X2, G2, R 2, 𝑃2 ) ↩→∗
(X ′, G ′, R ′, 𝑃 ′ ).
   Proof. In our Agda development, we apply the standard technique for obtaining confluence
results. Namely, we show a one-step confluence/diamond property and use it to tile the desired,
many-step diamond. While · ↩→ · does not satisfy a one-step diamond property (consider the case
where one of the initial steps is SchdBad), its reflexive closure does, which suffices. The proof has
a large number of cases, but most boil down to commutativity lemmas such as: Sync’ for 𝐼 followed
by Sync’ for 𝐽 produces the same configuration as Sync’ for 𝐽 followed by Sync’ for 𝐼 , assuming all
necessary hypotheses for these Sync’ steps hold.                                                   □

    We will use confluence to prove soundness and completeness of equivalence checking. But first,
we take a brief detour to prove data race freedom and the true positives property for · ↩→ ·, our
checked dynamics.
    We will need some notation. Let (G, R, 𝑃) ↓ (G ′, R ′ ) denote that (G, R, 𝑃) →∗ (G ′, R ′, return ∥
· · · ∥ return), (G, R, X, 𝑃) (G ′, R ′ ) denote that (G, R, X, 𝑃) ↩→∗ (X ′, G ′, R ′, return ∥ · · · ∥
                                  ↩→




return) for some X ′ , and (G, R, X, 𝑃) ⊥ denote that (G, R, X, 𝑃) ↩→∗ ⊥. Let X∅ denote the initial
                                             ↩→




context of memory events 𝜆 _. ((𝜆 _. ∅), (0, ∅)) (the choice of 0 here is arbitrary), and let (V, ⊕V )
denote the collection (free algebra) of symbolic terms. We will sometimes drop the subscript on
⊕V where it is obvious. Finally, we define a map 𝜑 : (𝐴, ⊕𝐴 ) → (𝐵, ⊕𝐵 ) to be a function 𝜑 : 𝐴 → 𝐵
between the collections of program values 𝐴 and 𝐵 such that 𝜑 (𝑣 1 ⊕𝐴 𝑣 2 ) = 𝜑 (𝑣 1 ) ⊕𝐵 𝜑 (𝑣 2 ).
    Now we are ready to proceed with our proofs. For every unchecked trace, there is a checked
trace that reaches the same result, or detects a data race:

                                                                 , Vol. 1, No. 1, Article . Publication date: August 2026.
12                            Benjamin Driscoll, Kshitij Dubey, Anjiang Wei, Neeraj Kayal, Rahul Sharma, and Alex Aiken


     Lemma 2. If (G, R, 𝑃) →∗ (G ′, R ′, 𝑃 ′ ) then, for all X, (X, G, R, 𝑃) ↩→∗ (X ′, G ′, R ′, 𝑃 ′ ) for some
X ′ or (X, G, R, 𝑃) ↩→∗ ⊥
     Proof. By induction on (G, R, 𝑃) →∗ (G ′, R ′, 𝑃 ′ ).                                                               □
     Conversely, for every checked trace, there is an unchecked trace that reaches the same result.
     Lemma 3. If (X, G, R, 𝑃) ↩→∗ (X ′, G ′, R ′, 𝑃 ′ ) then (G, R, 𝑃) →∗ (G ′, R ′, 𝑃 ′ ).
     Proof. By induction on (X, G, R, 𝑃) ↩→∗ (X ′, G ′, R ′, 𝑃 ′ ).                                                      □
     The initial values of shared memory and registers do not affect whether a data race is detected:
                                      ↩→




                                                                     ↩→
     Lemma 4. If (X, G1, R 1, 𝑃)            ⊥ then (X, G2, R 2, 𝑃)        ⊥.
  Proof. By induction we can prove that, for all X, G1, R 1, 𝑃, X ′, G1′, R 1′ , 𝑃 ′, G2, R 2 , if we have
(X, G1, R 1, 𝑃) ↩→∗ (X ′, G1′, R 1′ , 𝑃 ′ ), then (X, G2, R 2, 𝑃) ↩→∗ (X ′, G2′, R 2′ , 𝑃 ′ ) for some G2′, R 2′ . Hence,
the desired result follows from the fact that RdMemBad and WrMemBad depend only on the
context of memory events and the program.                                                                              □
     The next theorem proves that if there is a data race, then the symbolic evaluation detects it:




                                                                                                  ↩→
     Theorem 1 (Data Race Freedom). If 𝑃 has a data race, then (X, G, R, 𝑃)                            ⊥.
   Proof. The fact that 𝑃 has a data race implies there are two traces—that is, derivations of
(G𝑜 , R𝑜 , 𝑃) →∗ (G ′, R ′, 𝑃 ′ ) for some G𝑜 , R𝑜 , G ′ , R ′ , 𝑃 ′ —with a common prefix 𝛼 followed by
conflicting accesses 𝑎𝑖 , 𝑎 𝑗 in one case, and, in the other, 𝑎 𝑗 , 𝑎𝑖 . By Lemma 2 on 𝛼, either we can obtain
a derivation of (X, G𝑜 , R𝑜 , 𝑃) ↩→∗ (X𝛼 , G𝛼 , R𝛼 , 𝑃𝛼 ) for some X𝛼 , G𝛼 , R𝛼 , 𝑃𝛼 , or (X, G𝑜 , R𝑜 , 𝑃) ⊥




                                                                                                                    ↩→
and, by Lemma 4, we are done. In the former case, without loss of generality, let 𝑎 𝑗 be a write.
Either we can append 𝑎𝑖 to our (X, G𝑜 , R𝑜 , 𝑃) ↩→∗ (X𝛼 , G𝛼 , R𝛼 , 𝑃𝛼 ) without obtaining ⊥, or we are
done by Lemma 4. In the former case, the write 𝑎 𝑗 now induces a ¬noRacingRd if 𝑎𝑖 is a read or a
¬noRacingWr if 𝑎𝑖 is a write, completing the proof by Lemma 4.                                               □
   The next theorem proves that if the symbolic evaluation detects a data race, then there is actually
a data race:
                                                                               ↩→




     Theorem 2 (True Positives Property). If (X∅, G, R, 𝑃)                          ⊥ then 𝑃 has a data race.
                                       ↩→




   Proof. Since (X∅, G, R, 𝑃) ⊥, the last step of our derivation is a read or a write for which we
have a ¬noRacingRd or ¬noRacingWr for some 𝑖, X(𝑔). Call this step 𝑎𝑖 . Without loss of generality,
we consider the case where 𝑎𝑖 is a write. There must also be a write to 𝑔 by some 𝑗 ≠ 𝑖, lest, by
induction, our derivation does not hit ⊥. Say the last such write, 𝑎 𝑗 , occurs at step 𝑛 of the derivation.
After the last write 𝑎 𝑗 , it grows monotonically easier to read/write 𝑔. Hence, there cannot be a
sync 𝐼 at any step 𝑚 > 𝑛 such that 𝑖, 𝑗 ∈ 𝐼 , since it would be possible for 𝑖 to read 𝑔 immediately
after the sync and, therefore, at all following steps. Hence, there is no sync 𝐼 at step 𝑚 > 𝑛 on
thread 𝑖 such that 𝑗 ∈ 𝐼 or vice-versa, since that would induce a deadlock, but the hypothesis
                 ↩→




(X∅, G, R, 𝑃) ⊥ entails that the dynamics run to completion, producing ⊥—in particular, they do
not get stuck. From this fact, we conclude that we can shift our derivation so that 𝑎 𝑗 and 𝑎𝑖 are
next to each other. After all, the only steps from other threads that cannot be shifted past 𝑎𝑖 are
those Sync’ where the set includes 𝑖 and the only steps from other threads that cannot be shifted
past 𝑎 𝑗 (i.e., deleted from the end of the trace) are those Sync’ where the set includes 𝑗. Now, we
can transform the piece of the trace before 𝑎 𝑗 , 𝑎𝑖 from a · ↩→∗ · into a · →∗ · by Lemma 3. Finally,
we can append 𝑎 𝑗 , 𝑎𝑖 to the result and, separately, 𝑎𝑖 , 𝑎 𝑗 to the result to obtain the desired two
traces.                                                                                                   □

, Vol. 1, No. 1, Article . Publication date: August 2026.
Equivalence Checking of ML GPU Kernels                                                                                13




                                                                                                        ↩→
  The theorems above characterize executions that run to completion (note the use of ); the next
two theorems account for executions that get stuck. We say that a program is deadlocked if no step
can be taken, but the program is not of the form return ∥ · · · ∥ return and, in the checked case,
the machine is not in state ⊥.
  Theorem 3 (Sound Deadlock Detection). If any · ↩→ · trace deadlocks from some initial state,
then all such traces from that state deadlock. Furthermore, if any · ↩→ · trace deadlocks, then some
· → · trace deadlocks.
  Proof. The first statement is immediate from confluence, noting that, definitionally, the machine
cannot step from a deadlocked state. The second statement is immediate from Lemma 3.              □
   Theorem 4 (Complete Deadlock Detection). If some · → · trace deadlocks, then, for all initial
states, all · ↩→ · traces deadlock or reach error state ⊥.
  Proof. That, for each initial state X, some · ↩→ · trace deadlocks or reaches error state ⊥ is
immediate from Lemma 2. Furthermore, again by confluence, all such traces must deadlock.      □
  One subtlety of the above theorems is that, if the unchecked semantics both races and deadlocks,
the checked semantics might detect one error or the other, though it always detects the same error
once we fix the initial state, X∅ in the implementation since we want the true positives property. We
now prove a few more lemmas characterizing · ↩→ · and · → · to build up to a proof of soundness
and completeness for our equivalence checker.
  The unchecked dynamics commutes with application of a map to shared memory and the
registers. Together Lemmas 3 and 5 (below) should be thought of as a “sound abstraction” result:
they say that running the checked semantics on a symbolic input tells us everything there is to
know about running the unchecked semantics on concrete inputs, as we can take 𝜑 : V → R in
Lemma 5:
  Lemma 5. For all maps 𝜑, if (G, R, 𝑃) →∗ (G ′, R ′, 𝑃 ′ ) then (𝜑 (G), 𝜑 (R), 𝑃) →∗ (𝜑 (G ′ ), 𝜑 (R ′ ), 𝑃 ′ ).
  Proof. By induction on (G, R, 𝑃) →∗ (G ′, R ′, 𝑃 ′ ).                                                               □
  Lemma 6. If (G, R, 𝑃) ↓ (G1, R 1 ) and (G, R, 𝑃) ↓ (G2, R 2 ), then (G1, R 1 ) = (G2, R 2 ) or, for all X,
             ↩→




(X, G, R, 𝑃) ⊥.
  Proof. By Lemma 2, either (X, G, R, 𝑃) ↩→∗ ⊥ and we are done, or we have (X, G, R, 𝑃) ↩→∗
(X1, G1, R 1, return ∥ · · · ∥ return) and (X, G, R, 𝑃) ↩→∗ (X2, G2, R 2, return ∥ · · · ∥ return) for
some X1, X2 . But, in the latter case, confluence yields a contradiction if (G1, R 1 ) ≠ (G2, R 2 ). □
   Letting Eq denote our procedure for deciding equality between symbolic terms, we are finally
ready to state soundness and completeness of equivalence checking. Soundness says that, if Eq
decides that the outputs of the checked dynamics on two programs are equal on appropriate
symbolic inputs, then the outputs of the unchecked dynamics on the two programs are equal for
all real inputs (since we can write any real inputs as symbolic inputs under a substitution 𝜑):
   Theorem 5 (Soundness of Eqivalence Checking). For all 𝑃, 𝑄 : L, contexts G, R over V,
                                                     ↩→




                                                                                      ↩→




and maps 𝜑 : (V, ⊕) → (R, ⊕), if (X∅, G, R, 𝑃) (G𝑃 , R𝑃 ), (X∅, G, R, 𝑄) (G𝑄 , R𝑄 ), Eq(G𝑃 , G𝑄 ),
Eq(R𝑃 , R𝑄 ), (𝜑 (G), 𝜑 (R), 𝑃) ↓ (G𝑃′ , R𝑃′ ), and (𝜑 (G), 𝜑 (R), 𝑄) ↓ (G𝑄′ , R𝑄′ ), then G𝑃′ = G𝑄′ and
R𝑃′ = R𝑄′ .
   Proof. By Lemmas 3 and 5, (𝜑 (G), 𝜑 (R), 𝑃) ↓ (𝜑 (G𝑃 ), 𝜑 (R𝑃 )) and (𝜑 (G), 𝜑 (R), 𝑄) ↓
(𝜑 (G𝑄 ), 𝜑 (R𝑄 )). By Lemma 6, either 𝜑 (G𝑃 ) = G𝑃′ and 𝜑 (R𝑃 ) = R𝑃′ or (X∅, 𝜑 (G), 𝜑 (R), 𝑃) ⊥
                                                                                                                 ↩→




and thus, by Lemma 4, (X∅, G, R, 𝑃) ⊥, a contradiction. Hence, 𝜑 (G𝑃 ) = G𝑃′ and 𝜑 (R𝑃 ) = R𝑃′ .
                                          ↩→




                                                              , Vol. 1, No. 1, Article . Publication date: August 2026.
14                            Benjamin Driscoll, Kshitij Dubey, Anjiang Wei, Neeraj Kayal, Rahul Sharma, and Alex Aiken


By the same argument, 𝜑 (G𝑄 ) = G𝑄′ and 𝜑 (R𝑄 ) = R𝑄′ . Hence, if Eq indeed decides mathematical
equality of the symbolic terms (see Section 4.4), we have G𝑃′ = 𝜑 (G𝑃 ) = 𝜑 (G𝑄 ) = G𝑄′ and
R𝑃′ = 𝜑 (R𝑃 ) = 𝜑 (R𝑄 ) = R𝑄′ , as desired.                                                   □
  Conversely, completeness says that, if Eq decides the outputs of the checked dynamics on two
programs are not equal on symbolic inputs, then the outputs of the unchecked dynamics on the
two programs are not equal for some real input (namely the symbolic input under substitution 𝜑):
  Theorem 6 (Completeness of Eqivalence Checking). For all 𝑃, 𝑄 : L and contexts G, R over
                        ↩→




                                                            ↩→
V, if (G, R, X∅, 𝑃) (G𝑃 , R𝑃 ), (G, R, X∅, 𝑄) (G𝑄 , R𝑄 ), and ¬Eq(G𝑃 , G𝑄 ) or ¬Eq(R𝑃 , R𝑄 ), there
exists a map 𝜑 : (V, ⊕) → (R, ⊕) such that, if (𝜑 (G), 𝜑 (R), 𝑃) ↓ (G𝑃′ , R𝑃′ ) and (𝜑 (G), 𝜑 (R), 𝑄) ↓
(G𝑄′ , R𝑄′ ), then G𝑃′ ≠ G𝑄′ or R𝑃′ ≠ R𝑄′ .
   Proof. Without loss of generality, ¬Eq(G𝑃 , G𝑄 ); the cases are symmetric. As we shall show in
Section 4.4, ∀𝑎, 𝑏 : V such that 𝑎 ≠ 𝑏 there exists a map 𝜑 : (V, ⊕) → (R, ⊕) such that 𝜑 (𝑎) ≠ 𝜑 (𝑏).
From this fact, we can obtain 𝜑 such that 𝜑 (G𝑃 ) ≠ 𝜑 (G𝑄 ). By the same argument that we used
in the proof of Theorem 5, if (𝜑 (G), 𝜑 (R), 𝑃) ↓ (G𝑃′ , R𝑃′ ) and (𝜑 (G), 𝜑 (R), 𝑄) ↓ (G𝑄′ , R𝑄′ ), then
𝜑 (G𝑃 ) = G𝑃′ and 𝜑 (G𝑄 ) = G𝑄′ . If G𝑃′ = G𝑄′ , then 𝜑 (G𝑃 ) = G𝑃′ = G𝑄′ = 𝜑 (G𝑄 ), a contradiction.
Hence, G𝑃′ ≠ G𝑄′ as desired.                                                                            □
  In fact, we only care about equality (or the lack thereof) on a subset of G𝑃 , G𝑄 and R𝑃 , R𝑄 ,
namely the designated program outputs. Fortunately, the same steps prove the desired versions of
Theorems 5 and 6, though their statements become ever more unwieldy.

4.4    Decision Procedure
Thus far in the formalism, we have assumed, without loss of generality, a single binary operator
⊕. In the decision procedure, we support expressions involving additions, multiplications, and
exponentiations over reals and, in this section, we show that it is possible to decide equalities of
the form 𝑓1 (𝑥 1, . . . , 𝑥𝑛 ) = 𝑓2 (𝑥 1, . . . , 𝑥𝑛 ) where 𝑓1 and 𝑓2 involve such expressions. Although we do
not give a formal account of other functions such as max, the implementation supports them. In
principle, min and max could be handled by case splits without affecting decidability. In the ML
kernels we verify, max and min arise only in restricted patterns, such as the max-subtraction of
softmax, so we are able to sufficiently normalize them and do not split. We are not aware of a
proof of decidability for our desired equalities, though there is work on related problems, such as
on Tarski’s exponential function problem [49]. Closest to our result is Lemma 16 of Li and Wu
[43] (the basis of Mirage’s verifier [76]), a univariate analogue that additionally permits ratios of
polynomials in the exponents. However, its proof invokes the Lindemann–Weierstrass theorem
and, consequently, applies only when the coefficients involved are algebraic numbers. Our proof is
direct, avoids heavy number-theoretic machinery, and handles arbitrary real coefficients.
    If there were no exponentiations, decidability would be immediate. Because 𝑓1 = 𝑓2 iff 𝑓1 − 𝑓2 is
identically zero, and 𝑓1 − 𝑓2 can be rewritten as a sum of monomials and such a sum is identically
zero iff the coefficients of all the monomials are zero. We show that even with exponentiations,
identities 𝑓1 = 𝑓2 are decidable.
    Without loss of generality, we assume that the polynomial in the exponent of terms 𝑝 (𝑥)𝑒 ℎ (𝑥 )
                                                                                                      ′
has a zero constant, i.e., ℎ(0) = 0. If ℎ(0) ≠ 0 then we can rewrite 𝑝 (𝑥)𝑒 ℎ (𝑥 ) as 𝑝 ′ (𝑥)𝑒 ℎ (𝑥 ) where
  ′
𝑝 (𝑥) = 𝑝 (𝑥)𝑒  ℎ (0)          ′
                        and ℎ (𝑥) = ℎ(𝑥) − ℎ(0).
    Theorem 7. Let 𝑚 ≥ 1 be an integer. Suppose that R[𝑥] polynomials 𝑝 1 (𝑥), . . . , 𝑝𝑚 (𝑥) and
                                                            Í
ℎ 1 (𝑥), . . . , ℎ𝑚 (𝑥) satisfy ∀𝑖 ≠ 𝑗 .ℎ𝑖 (𝑥) ≠ ℎ 𝑗 (𝑥) and 𝑚           ℎ𝑖 (𝑥 ) = 0 then it must be that
                                                             𝑖=1 𝑝𝑖 (𝑥)𝑒
𝑝 1 (𝑥) = 𝑝 2 (𝑥) = . . . = 𝑝𝑚 (𝑥) = 0.

, Vol. 1, No. 1, Article . Publication date: August 2026.
Equivalence Checking of ML GPU Kernels                                                                                      15


   Proof. Proof by induction on 𝑚. For the base case with 𝑚 = 1, we have 𝑝 1 (𝑥)𝑒 ℎ1 (𝑥 ) = 0. Since
𝑒 ℎ1 (𝑎) > 0 for all 𝑎, it must be that ∀𝑎.𝑝 1 (𝑎) = 0 and hence 𝑝 1 (𝑥) = 0.
  For the induction case, assume that the result holds for (𝑚 − 1). Suppose WLOG that the leading
coefficient of ℎ𝑚 (𝑥) is the largest among the leading coefficients of the ℎ𝑖 (𝑥)’s. Then the leading
coefficient of ℎ𝑖 (𝑥) − ℎ𝑚 (𝑥) is negative for all 𝑖 < 𝑚. This implies, ∀𝑖 < 𝑚. lim𝑥→∞ 𝑒 ℎ𝑖 (𝑥 ) −ℎ𝑚 (𝑥 ) = 0.
  We are given, 𝑝 1 (𝑥)𝑒 ℎ1 (𝑥 ) −ℎ𝑚 (𝑥 ) + 𝑝 2 (𝑥)𝑒 ℎ2 (𝑥 ) −ℎ𝑚 (𝑥 ) + . . . + 𝑝𝑚−1 (𝑥)𝑒 ℎ𝑚−1 (𝑥 ) −ℎ𝑚 (𝑥 ) + 𝑝𝑚 (𝑥) = 0.
Taking limits as 𝑥 approaches ∞, we have:
                                                                    !
                                ∑︁
                                                   ℎ𝑖 (𝑥 ) −ℎ𝑚 (𝑥 )
                                     lim 𝑝𝑖 (𝑥)𝑒                      + lim 𝑝𝑚 (𝑥) = 0
                                       𝑥→∞                               𝑥→∞
                                 𝑖<𝑚

Therefore, lim𝑥→∞ 𝑝𝑚 (𝑥) = 0. But for a non-zero polynomial 𝑝, lim𝑥→∞ 𝑝 (𝑥) is either ∞ if the
leading coefficient of 𝑝 is positive and −∞ if negative. Hence, 𝑝𝑚 (𝑥) = 0.                  □

  Hence, in the uni-variate case, identity checking with exponentiations reduces to identity check-
ing without exponentiations, which is decidable as discussed earlier. The above theorem for uni-
variates generalizes to multi-variate polynomials.
    Corollary 8. Let 𝑚 ≥ 1 be an integer. Suppose that R[𝑥]¯ multivariate polynomials 𝑝 1 (𝑥),  ¯ . . . , 𝑝𝑚 (𝑥)
                                                                                                              ¯
         ¯ . . . , ℎ𝑚 (𝑥)
and ℎ 1 (𝑥),           ¯ satisfy ∀𝑖 ≠ 𝑗 .ℎ𝑖 (𝑥)
                                             ¯ ≠ ℎ 𝑗 (𝑥)
                                                            Í
                                                      ¯ and 𝑚    𝑝   ( ¯
                                                                       𝑥)𝑒 ℎ𝑖 (𝑥¯ ) = 0 then it must be that
                                                             𝑖=1   𝑖
     ¯ = 𝑝 2 (𝑥)
𝑝 1 (𝑥)       ¯ = . . . = 𝑝𝑚 (𝑥)
                              ¯ = 0.
   Proof. Consider the substitution 𝑥 1 = 𝛼 1𝑦, 𝑥 2 = 𝛼 2𝑦, . . ., 𝑥𝑛 = 𝛼𝑛𝑦 where each 𝛼𝑖 ∈ R are chosen
independently at random. Making this substitution, we get a univariate functional identity of the
form
                                    ˆ                ˆ                         ˆ
                          𝑝ˆ1 (𝑦)𝑒 ℎ1 (𝑦) + 𝑝ˆ2 (𝑦)𝑒 ℎ2 (𝑦) + . . . + 𝑝ˆ𝑚 (𝑦)𝑒 ℎ𝑚 (𝑦) = 0                             (2)
where for each 𝑖 ∈ {1, . . . , 𝑚}, 𝑝ˆ𝑖 (𝑦) = 𝑝𝑖 (𝛼 1𝑦, 𝛼 2𝑦, . . . , 𝛼𝑛𝑦) and ℎˆ𝑖 (𝑦) = ℎ𝑖 (𝛼 1𝑦, 𝛼 2𝑦, . . . , 𝛼𝑛𝑦).
   From our convention, ℎˆ𝑖 (0) = ℎ𝑖 (0, 0, . . . , 0) ≠ 0. For 𝑖 ≠ 𝑗, consider
                            ℎˆ𝑖 (𝑦) − ℎˆ 𝑗 (𝑦) = ℎ𝑖 (𝛼 1𝑦, . . . , 𝛼𝑛𝑦) − ℎ 𝑗 (𝛼 1𝑦, . . . , 𝛼𝑛𝑦)
Let the degree of ℎ𝑖 (𝑥) ¯ −ℎ 𝑗 (𝑥)¯ be 𝑑 and the largest degree homogeneous component of ℎ𝑖 (𝑥)          ¯ −ℎ 𝑗 (𝑥)
                                                                                                                  ¯
be 𝑔𝑑 (𝑥)                 ˆ           ˆ
          ¯ ≠ 0. Then, ℎ𝑖 (𝑦) − ℎ 𝑗 (𝑦) is a polynomial of degree at most 𝑑 and the coefficient of 𝑦𝑑
in ℎ𝑖 (𝑦) − ℎˆ 𝑗 (𝑦) is 𝑔𝑑 (𝛼 1, 𝛼 2, . . . , 𝛼𝑛 ). By Schwartz Zippel Lemma, 𝑔𝑑 (𝛼 1, 𝛼 2, . . . , 𝛼𝑛 ) ≠ 0 almost
      ˆ
surely and so almost surely (over the random choice of 𝛼¯ = (𝛼 1, . . . , 𝛼𝑛 )) we have ∀𝑖 ≠ 𝑗 : ℎˆ𝑖 (𝑦) ≠
ℎˆ 𝑗 (𝑦). Applying the theorem to Equation 2, we get almost surely (over the random choice of
 ¯ 𝑝ˆ1 (𝑦) = . . . = 𝑝ˆ𝑚 (𝑦) = 0). But 𝑝ˆ𝑖 (𝑦) = 𝑝𝑖 (𝛼 1𝑦, . . . , 𝛼𝑚𝑦) and this must imply that 𝑝𝑖 (𝑥)
𝛼,                                                                                                           ¯ =0
(via Schwartz Zippel Lemma applied to the largest homogeneous component of 𝑝𝑖 (𝑥)).                       ¯ Thus,
∀1 ≤ 𝑖 ≤ 𝑚.𝑝𝑖 (𝑥) = 0.                                                                                             □

   Note that the theorem and corollary require the exponents ℎ𝑖 to be polynomials. Nested exponen-
tials, as would arise, for example, if one softmax were composed with another, are not covered by
our decidability proof. Our implementation simplifies nested exponentials and ratios of functions
in exponents if they arise, but it may not be complete for such expressions.
   Given our interest in proving completeness of the overall equivalence checking procedure, we do
not focus on the computational complexity of the decision procedure and leave it for future work.
Our implementation (Section 5) is able to handle ML kernels that arise in practice (Section 6). Finally,
to make good on our claim in the proof of completeness for equivalence checking that ∀𝑎, 𝑏 : V such
that 𝑎 ≠ 𝑏 there exists a map 𝜑 : (V, ⊕) → (R, ⊕) (more precisely (V, +, ·, exp) → (R, +, ·, exp))
such that 𝜑 (𝑎) ≠ 𝜑 (𝑏), we remark that 𝑎, 𝑏 can be viewed as polynomials in R[𝑥]   ¯ for some 𝑥. ¯ By

                                                                      , Vol. 1, No. 1, Article . Publication date: August 2026.
16                            Benjamin Driscoll, Kshitij Dubey, Anjiang Wei, Neeraj Kayal, Rahul Sharma, and Alex Aiken


contraposition of the above theorem, recalling that each 𝑝𝑖 can be written as a sum of monomials,
if 𝑎 ≠ 𝑏 (that is, 𝑎 − 𝑏 is not formally 0), they must be unequal on some input 𝑟¯. Then,
                                          (
                                           𝑟𝑖 if 𝑥 = 𝑥𝑖 for some 𝑥𝑖 ∈ 𝑥¯
                                  𝜑 (𝑥) =
                                           𝑥 otherwise
can be extended in the obvious way to the desired map (V, +, ·, exp) → (R, +, ·, exp).

5    Implementation
We implement our techniques in a proof-of-concept tool, Volta, written in Rust.10 Volta operates
on CTAs written in PTX ISA 9.111 . In addition to the PTX program, it accepts specification of
parameters such as the grid dimensions and the locations and sizes of input tensors as well as
the output tensors that should be compared for equivalence. Volta is comprised of two main
components: a simulator that performs symbolic execution to generate verification conditions
(VCs), and a decision procedure that resolves them. For a program where each thread runs at most
𝑁 statements, the simulator’s runtime is linear in 𝑁 , whereas the decision procedure exhibits
superlinear complexity in 𝑁 . The rest of this section will relay the key details of symbolic execution
and the decision procedure, though it does not exhaustively describe their implementations.
   Before symbolic execution, the input PTX is lowered, resolving variable, parameter, and register
names, as well as labels. During symbolic execution, for each shared or global memory cell that
has been written, we track an expression and the value of X (see Section 4.2) at that cell, where
𝒫(TID) is implemented via a fixed-width bitset. In fact, memory cells additionally track the width
of the last store and require (to a first approximation) that reads are of the same width—it is not
clear what it means to read half of a real valued symbolic expression. Each expression is passed
around as a 4-byte index into a bump allocator holding a 16-byte representation of the expression.
Constant folding, including simplification of min(∞, 𝑥), min(𝑥, ∞), max(−∞, 𝑥), and max(𝑥, −∞),
is performed eagerly as expressions are constructed, with floating-point constants represented via
GMP’s [28] arbitrary precision rationals. Then, it is a trivial matter to resolve branches and memory
accesses as they occur, should they be fully statically determined, or else to return an error.
   Threads are scheduled in a round-robin fashion, with each selected thread being run until it
blocks at a barrier or exits. If all threads are blocked, the scheduler checks whether any barriers can
be released because all threads that are expected to reach them have done so. If not, a deadlock is
reported—a strategy justified by Theorems 3 and 4. At any point, a race might be detected via X, it
might be decided that the program is not a structured-CTA because it attempts to branch or index
memory using a symbolic value, or some other violation might be detected such as an out-of-bounds
read. If the symbolic execution succeeds, the verification conditions (VCs) corresponding to the
output tensors are given to a decision procedure. In particular, for each pair of corresponding
output tensor elements 𝑝 1 and 𝑝 2 , the decision procedure checks whether 𝑝 1 − 𝑝 2 is identically zero.
   Volta currently assumes that CTAs behave uniformly and simply checks CTA 0 of the reference
against CTA 0 of the optimized program. If the optimizations are intra-CTA, checking multiple
CTAs is embarrassingly parallel, but it might become intractably expensive for real, multi-billion
parameter models. It is worth noting that, while the number of CTAs grows, the per-CTA tensor
size does not.
   The decision procedure consists of a canonicalizer producing a ratio of polynomials (rational
function), each polynomial consisting of a sorted list of terms along with their coefficients, each
term consisting of a sorted list of factors along with their exponents, optionally multiplied by
10 https://github.com/willtunnels/volta
11 https://docs.nvidia.com/cuda/parallel-thread-execution/



, Vol. 1, No. 1, Article . Publication date: August 2026.
Equivalence Checking of ML GPU Kernels                                                                        17


𝑒 to some (non-zero) polynomial, each factor consisting of a symbolic input, an uninterpreted
function of rational functions, or a min or max of rational functions. Min and max factors store their
arguments sorted and deduplicated, and nested min and, respectively, max factors are flattened.
Everything is hash-consed, providing an arbitrary but stable sort order. Rational functions are not
reduced to lowest terms; equality of two canonical ratios is decided by a monomial-quotient test that
handles softmax-style rescalings, or, in general, by cross-multiplication, which reduces the question
to equality of canonical polynomials. The results of canonicalization are memoized/cached based
on the generation time indices that represent expressions, but only if an expression is referenced
by multiple other expressions, where reference counts are determined by a walk of the generation
phase expression store (the bump allocator) before running the decision procedure. This check
significantly reduces the size of the memoized data, e.g., in the presence of accumulation chains,
and the memoized data is not incrementally collected.
   The content of Corollary 8 is that the above procedure is complete for the subclass of expressions
          ¯ ℎ𝑖 (𝑥¯ ) . It says such functions are determined by their polynomial coefficients (which
Í𝑚
  𝑖=1 𝑝𝑖 (𝑥)𝑒
are themselves determined by their monomial coefficients). Canonicalization requires distributing
multiplication over addition to find the coefficient of each monomial term. This operation, in
principle, may cause exponential blowup. Since machine learning workloads do not typically have
computations with high multiplicative depth, this blowup does not happen in practice.
   It is worth noting that Volta’s implementation is currently single-threaded. One could try to
parallelize VC generation by simulating the CUDA parallel machine with a parallel machine. The
decision procedure would be a more interesting task because of canonical form memoization, out
of which the implementation gets quite a bit of mileage, as we shall see (Section 6.5). We leave
parallelization to future work.
   Finally, we give an inventory of the PTX operations Volta currently supports. It supports
collective operations bar.sync, bar.warp.sync, shfl.sync, activemask, ldmatrix, mma.sync,
and wmma. It can symbolically compute addition, multiplication, division, reciprocal, fused multiply-
add, and exponentiation along with max and min, float-width conversions (modeled as the identity),
and floating-point saturation and ReLU clamps (modeled via min/max). Some additional operations
can be performed on statically known values. We do not support square root or trigonometric
functions. These operations are tricky because they place requirements on their arguments, e.g.,
square root requires a positive argument. If the set of operations appearing in expressions grows
sufficiently complex, an SMT solver might be necessary.



6   Evaluation
There are three main ways to create efficient GPU kernels for machine learning workloads: manual
optimization (Section 6.1), generation by LLMs (Section 6.2), and compilation by domain-specific
compilers (Section 6.3). Since our equivalence checker operates as a black box and makes no
assumptions about the optimization process, it can verify the correctness of optimized kernels
produced by all three approaches. We evaluate on reductions, matrix multiplications, convolutions,
and various attention mechanisms. We report the time to generate the verification conditions (VCs),
which includes symbolically executing both kernels (“VC Gen”), and the time to solve them (“VC
Time”), measured on a machine with a 128-core 2.25 GHz AMD EPYC 7742 processor and 995 GB of
RAM. We show that Volta scales to realistic machine learning workloads and effectively identifies
correctness issues when they exist. In particular, Volta detects data races that have been previously
reported in open-source GitHub repositories (Section 6.4).


                                                        , Vol. 1, No. 1, Article . Publication date: August 2026.
18                            Benjamin Driscoll, Kshitij Dubey, Anjiang Wei, Neeraj Kayal, Rahul Sharma, and Alex Aiken


6.1    Human-generated Kernels
6.1.1 Reduction. “Optimizing Parallel Reduction in CUDA” by Harris [30] is a well-cited tutorial
that introduces a sequence of progressively optimized reduction kernels. It begins with a baseline
implementation, Red-1, and presents seven versions, each achieving higher performance than
the previous one. Each CTA reduces 128 values using up to 128 threads. The first optimization,
Red-2, removes divergent branching and achieves more than a 2× speedup. The next version,
Red-3, mitigates shared-memory bank conflicts for another 2× improvement. Red-4, which further
reduces the number of idle threads, yields an additional reported speedup of 1.78×. The subsequent
optimizations rely on warp-synchronous execution, which was later deprecated by NVIDIA. Volta
detects data races in these versions, Red-5, Red-6, and Red-7, and correctly rejects them, and Volta
proves that the other kernels are equivalent to Red-1.
   Table 1 reports the running time of Volta and other key statistics, such as the number of CTA-
wide synchronization operations and PTX instructions, for the optimized kernels. Red-1 through
Red-4 were checked for equivalence with Red-1; for the racy versions, we report the time for
symbolic execution to detect the race. “#Block Sync” represents the total number of bar.sync PTX
instructions executed across all threads. Finally, verifying the equivalence of a kernel against itself,
here Red-1 vs. Red-1, serves as a sanity check, confirming that the reference implementation is free
of synchronization errors.

Table 1. Time to symbolically execute and check verification conditions (VCs) for kernels from NVIDIA’s
reduction tutorial [30]. Each kernel runs as a single CTA of 128 threads; Red-1–Red-4 reduce 128 elements
and were checked for equivalence with Red-1. Volta rejects the racy Red-5–Red-7 during symbolic execution,
before any VCs are generated, so their VC Gen entries report the time to detect the race.

                           Kernel      VC Gen (s)     VC Time (s)    #Block Sync   PTX LOC
                           Red-1          0.0038            0.0005       1k           76
                           Red-2          0.0023            0.0004       1k           79
                           Red-3          0.0022            0.0004       1k           73
                           Red-4          0.0022            0.0004       896          75
                           Red-5          0.0011              —           —           156
                           Red-6          0.0007              —           —           104
                           Red-7          0.0010              —           —           98



6.1.2 MatMul. “How to Optimize a CUDA Matmul Kernel for cuBLAS-like Performance” by Boehm
is a widely referenced tutorial in the GPU community [11] presenting SGEMM (single-precision
general matrix multiplication) implementation techniques. Similar to the reduction tutorial, it
presents a series of kernels, each achieving progressively higher performance: starting from 1%
of the performance of NVIDIA’s cuBLAS (proprietary and not open source) and reaching 95%.
Each CTA computes a 64 × 64 tile of the output matrix using up to 512 threads. Starting from
a baseline implementation, MatMul-1, the subsequent versions, MatMul-2 through MatMul-7,
apply a sequence of standard optimizations, including coalesced global-memory accesses, use
of shared-memory for caching, reducing bank conflicts, multiple levels of tiling (including warp
tiling), vectorized memory operations, and auto-tuning to determine the optimal sub-tile sizes for
intermediate computations. As with the reduction kernels, Table 2 reports the running time, the
number of CTA-wide synchronization operations, and the number of PTX instructions for each
optimized variant. All kernels were checked for equivalence with MatMul-1. In contrast to the
reduction tutorial, all MatMul kernels pass the equivalence check without data races.

, Vol. 1, No. 1, Article . Publication date: August 2026.
Equivalence Checking of ML GPU Kernels                                                                              19


Table 2. Symbolic execution and VC checking time for kernels from matrix multiplication tutorial [11]. All
kernels were checked for equivalence with MatMul-1. Each CTA computes a 64 × 64 tile of 𝐶 = 𝛼𝐴𝐵 + 𝛽𝐶
with 𝑀=𝑁 =𝐾=4096; MatMul-1 and MatMul-2 use 512 threads per CTA, MatMul-3 through MatMul-5 use
128, and MatMul-6 and MatMul-7 use 256.

                      Kernel      VC Gen (s)    VC Time (s)    #Block Sync      PTX LOC
                      MatMul-1       45.4          89.4            524k             185
                      MatMul-2       38.5          90.2            524k             269
                      MatMul-3       30.4          90.5            131k             325
                      MatMul-4       30.7          91.7            131k             323
                      MatMul-5       30.6          92.8            131k             320
                      MatMul-6       34.7          94.0            262k             307
                      MatMul-7       34.5          93.5            262k             307



6.1.3 FlashAttention. The performance of LLM inference is often bottlenecked by the attention
operation. Consequently, optimizing attention has become a central topic in the performance
engineering of LLMs. We start from a naive reference implementation, √Attention, that uses a
single thread to compute the full attention operation, i.e., softmax (𝑄𝐾 𝑇 / 𝑑)𝑉 . We evaluate the
setup where each CTA computes an attention head with standard matrix dimensions 𝑄 : (16, 64),
𝐾 : (512, 64), and 𝑉 : (512, 64). The optimized implementations we consider next use 128 threads.
   FA1 applies the FlashAttention [21] tiling strategy to reduce global-to-shared memory transfers
and adopts the online softmax formulation to enable streaming. FA1-TC further accelerates FA1 by
leveraging tensor cores. Finally, FA2-TC also uses tensor cores and incorporates the techniques of
FlashAttention-2 [20], such as deferring softmax normalization and improving work partitioning
among warps. Table 3 reports the checker runtime and statistics for these optimized variants,
including the number of CTA-level barriers (bar.sync), warp-level barriers, PTX instruction counts,
and the number of threads. “#Warp Sync" represents the total number of warp-level synchronization
PTX instructions such as bar.warp.sync, mma.sync, etc., executed across all threads. Note that
kernels in Table 1, Table 2, Attention, and FA1 do not use tensor cores. Thus, they have zero
warp-level synchronization operations. All kernels were checked for equivalence with Attention.
The Attention row checks the reference against itself—a sanity check as in Table 1. Its two sides
canonicalize to identical expressions, so their equality is immediate. The FlashAttention rows
instead reconcile two different representations of each output element as a rational function—the
naive softmax against the online-softmax accumulation—and deciding these equalities dominates
their VC Times.

Table 3. VC generation and checking time for attention kernels. All kernels were checked for equivalence
with Attention. Each kernel computes one attention head with 𝑄 : (16, 64), 𝐾 : (512, 64), and 𝑉 : (512, 64)
using a single CTA with the listed number of threads.

         Kernel      VC Gen (s)   VC Time (s)   #Block Sync     #Warp Sync        PTX LOC       #Threads
         Attention      3.9           3.0             0                0              477            1
         FA1            6.7          153.8          187k               0             1138           128
         FA1-TC         8.1          154.5          801k             204k            1237           128
         FA2-TC         4.1          154.0          210k             13k             2048           128


 Versions of attention which feature causal masking are commonly used in auto-regressive models.
We verify that the efficient “fused” implementation of causal masking, wherein we skip any blocks

                                                              , Vol. 1, No. 1, Article . Publication date: August 2026.
20                            Benjamin Driscoll, Kshitij Dubey, Anjiang Wei, Neeraj Kayal, Rahul Sharma, and Alex Aiken


such that all the column indices are more than the row indices, is equivalent to a naive approach
implemented via an element-wise product with a constant triangular matrix. See Table 4.
  VC checking time for these benchmarks is significantly lower than the VC checking time for
the benchmarks in Table 3. The symbolic expressions are smaller due to masking and time is
non-linear in expression size. Moreover, the two expressions being compared are actually precisely
the same—since the only difference is the method of filtering and this difference evaporates during
symbolic evaluation—allowing the implementation to avoid work via the cache.

Table 4. VC generation and checking time for causal attention kernels with a lower triangular mask. For all
kernels, a fused version of the kernel was checked against a naive version of the kernel. The first element of PTX
LOC is the for the fused implementation, and second element is for the naive implementation. Dimensions
and launch configurations match those of Table 3.

      Kernel               VC Gen (s)      VC Time (s)       #Block Sync    #Warp Sync      PTX LOC        #Threads
      Causal-Attention         3.9              0.05                0              0         (483, 480)        1
      Causal-FA1               9.4              0.08              187k             0        (1141, 1142)      128
      Causal-FA1-TC            11.8             0.13              801k           204k       (1241, 1242)      128
      Causal-FA2-TC            4.3              0.07              210k            13k       (2081, 2088)      128



6.2    LLM-generated Kernels
In a recent blog post, Stanford researchers demonstrated how LLMs can generate optimized GPU
kernels for 2D convolution [59]. We verify the equivalence of the final LLM-generated kernel after
13 rounds of optimization with a reference implementation. The applied optimizations include
transforming the convolution into a matrix multiplication to leverage tensor cores, pre-computing
intermediate values to eliminate redundant arithmetic, caching indices in shared-memory, employ-
ing software pipelining, reusing address computations, and applying vectorization. Overall, the
final kernel achieves 179.9% of PyTorch performance. In this setup, each CTA uses 256 threads
to compute a 128 × 128 output tile. Table 5 reports Volta’s running time and other key statistics.
The use of tensor cores significantly increases the code size of the optimized kernel compared to
the reference. The reference has no synchronization operations whereas the final version has 6.4k
CTA-wide and 102k warp-level barriers.

Table 5. Symbolic execution and VC checking time for the LLM-generated 2D convolution [59], checked
against a naive reference implementation. In the pairs (−, −), the first element is for the reference implemen-
tation, and the second element is for the optimized implementation. The kernels compute a 2D convolution
(batch 100, 3 × 224 × 224 inputs, 96 11 × 11 filters, stride 4, padding 2) expressed as an implicit GEMM with
𝑀=96, 𝑁 =302,500, 𝐾=363; each CTA uses 256 threads and computes a 128 × 128 output tile.

           Kernel      VC Gen (s)      VC Time (s)      #Block Sync      #Warp Sync     PTX LOC       #Threads
           Conv2D          32.0             14.3            (0, 6.4k)      (0, 102k)    (463, 1312)   (256, 256)


   Through the course of this verification, we discovered interesting undocumented behaviors. For
example, out-of-bounds reads from shared-memory arrays may not cause a crash and may also go
undetected by NVIDIA’s Compute Sanitizer [57]. The following code segment—which uses two
warps (64 threads) to read 48 elements of the shared-memory array A into registers v—runs without
raising any exceptions on the Ampere, Hopper, and Blackwell GPUs we tested on, even though it
performs out-of-bounds accesses.

, Vol. 1, No. 1, Article . Publication date: August 2026.
Equivalence Checking of ML GPU Kernels                                                                             21


__shared__ int A [48];
...
v = A[ tid ]; // threads 48 to 63 read out - of - bound
if ( tid < 48){
  use V
...

The out-of-bounds reads store zeros in register v and do not crash the tests. Volta (correctly)
catches them and raises exceptions. An appropriate fix is to rewrite the code, as shown below:
__shared__ int A [48];
...
if ( tid < 48){
   v = A[ tid ]; // all accesses within bounds
   use V
...

Although the two programs behave identically on current GPUs, there is no guarantee that future
GPU hardware would continue to tolerate out-of-bounds reads to shared memory. The latter code
segment is correct for future hardware as well and, hence, preferable. Thus, even though we focus
on verifying correctness of optimizations in this paper, we believe Volta can also help improve
code quality.
  Next, we use Claude Code (Anthropic’s LLM-based coding tool) to improve performance through
an agentic setup that automatically generates and runs tests for correctness checking [2]. In Table 6,
we start with a reference implementation for a matrix multiplication, MatMul-1, adapted from [11],
where the CTAs output 32 × 32 tiles. Claude Code is able to generate various kernels where GEMM-
1 and GEMM-2 have shared-memory optimizations, and GEMM-3 uses tensor cores. Volta is
successfully able to prove the equivalence of all three with the reference implementation.

Table 6. Symbolic execution and VC checking time for matrix multiplication kernels generated by Claude
Code. All kernels were checked for equivalence with MatMul-1. Each CTA uses 512 threads to compute a
32 × 32 tile of 𝐶 = 𝐴𝐵 with 𝑀=𝑁 =𝐾=4096.

         Kernel     VC Gen (s)   VC Time (s)   #Block Sync     #Warp Sync       PTX LOC        #Threads
         GEMM-1        36.4          13.2         524k               0              562           512
         GEMM-2        39.9          13.1         262k               0              587           512
         GEMM-3        28.4          13.1         263k              98k             771           512



6.3   Compiler-generated Kernels
TileLang [74] is a compiler that takes as input Python code that uses TileLang’s DSL API and
generates CUDA kernels under different configuration settings. We use it to produce multiple imple-
mentations of matrix multiplication and verify their pairwise equivalence. Any equivalence failure
would indicate a correctness bug in the TileLang compiler. Table 7 shows that the running time of
Volta scales gracefully with increasing tile sizes. Note that these tiles cannot grow unbounded
in size as then they would exceed the resource limits that the hardware imposes on each CTA.
Hence, Table 7 evaluates on some common tile sizes, where 𝐴 × 𝐵 × 𝐶 indicates a multiplication of
a matrix with dimensions 𝐴 × 𝐵 with a matrix of dimensions 𝐵 × 𝐶. Table 7 also reports detailed
statistics for each pair of programs under verification. In all cases, the optimized implementations
use tensor cores whereas their reference counterparts do not. The first elements of the pairs in
Table 7 refer to the statistics for the reference implementations and the second elements correspond
to the optimized implementations. The optimized implementations call into CUTLASS templates,
thus demonstrating Volta’s abilities to handle PTX assembly arising from CUTLASS [19].

                                                             , Vol. 1, No. 1, Article . Publication date: August 2026.
22                            Benjamin Driscoll, Kshitij Dubey, Anjiang Wei, Neeraj Kayal, Rahul Sharma, and Alex Aiken


Table 7. VC generation and checking time for matrix multiplication kernels generated by TileLang [74].
In each pair (−, −), first element is the reference implementation, and second element is the optimized
implementation. All kernels multiply f16 matrices with 𝑀=𝑁 =𝐾=4096; each CTA computes one output tile of
the listed size using the listed number of threads.

         Tile size        VC Gen (s)     VC Time (s)        #Block Sync       #Warp Sync   PTX LOC      #Threads
         32 × 32 × 32          1.1            2.5               (8k, 8k)        (0, 32k)   (322, 455)   (128, 128)
         64 × 32 × 32          4.5            10.9             (16k, 16k)      (0, 115k)   (531, 537)   (128, 128)
         64 × 64 × 32         18.6            60.4             (32k, 32k)      (0, 393k)   (632, 842)   (128, 128)


Table 8. Racy FaialAA GitHub benchmarks; races are also detected by Volta before the fix, and not detected
after the fix. BucketPositions, ComputeRange, and ReduceValue run as a single CTA of 64 threads; LayerNorm
runs as a single warp (32 threads); GradInput runs with 32 × 4 threads before the fix and 32 × 1 after.

                            Kernel                   Library        PTX LOC      Bug Fix Commit
                            BucketPositions      OpenMM                 94          9abaa587c
                            ComputeRange         OpenMM                132          65caf22b4
                            ReduceValue          OpenMM                1190         de666e305
                            LayerNorm           Megatron-LM            924          4831071c9
                            GradInput           Megatron-LM            546          f1295380c



6.4    Data Race Detection Baseline
FaialAA is the state-of-the-art data race checker for GPU programs [46]. Its canonical failure case,
as described by the authors, is the following pattern:
1. M [ tid ] = tid ;
2. x = M [ tid ];
3. M [ x ] = ...;
FaialAA cannot track the concrete value of x at line 2 and, therefore, models it as non-deterministic.
Subsequently, line 3 is reported as a (spurious) data race. Since we use symbolic evaluation, and
M[x] is constant (since tid is constant), we don’t report an error and declare the write in line 3
correctly as data race free.
  FaialAA evaluates on GitHub commits that fix data races. These programs come from well-used
open-source repositories OpenMM12 and NVIDIA’s Megatron-LM13 . Empirically, on the programs
where FaialAA successfully detects data races, Volta succeeds as well, i.e., the data races are caught
by the symbolic evaluation. Volta also successfully proves data race freedom for the versions of
these kernels after the bug-fixing commits. These programs are shown in Table 8 for completeness.

6.5    Equivalence Checking Baseline
To check that our decision procedure yields some benefit, we compare it to the Z3 [23] SMT solver,
an “off-the-shelf” solution, giving each the VC for a single element of each benchmark’s output
tensor. Table 9 reports the running time of Volta’s decision procedure and of Z3, with and without
the exponential-product axiom, ∀𝑥, 𝑦. 𝑒 𝑥 𝑒 𝑦 = 𝑒 𝑥+𝑦 , on the benchmarks of Section 6. The Z3 times
and the Volta “First” times are for verifying the VC of a single element of the output tensor in

12 https://github.com/openmm/openmm
13 https://github.com/NVIDIA/Megatron-LM



, Vol. 1, No. 1, Article . Publication date: August 2026.
Equivalence Checking of ML GPU Kernels                                                                          23


isolation. The Volta “Median” column reports the median per-element time from the full-footprint
runs of Section 6, in which Volta checks every output element.
   On the 18 benchmarks whose VCs contain no exponentials (the reduction, matrix multiplication,
and convolution kernels), Z3 succeeds. On the eight attention benchmarks, whose VCs contain
exponentials by way of softmax, Z3 succeeds only on those VCs which are trivial after symbolic
execution (exactly the form 𝑝 − 𝑝 for some 𝑝). Adding the axiom does not help—Z3 simply runs
longer before giving up. The gap between Volta’s first and median solve times has two sources.
First, the initial check of a run performs a one-time analysis of both kernels’ full expression graphs
to determine expression reference counts (see Section 5); for the matrix multiplications, whose
elements share little structure, this is essentially the entire gap. Second, an element checked after its
neighbors reuses cached canonical forms for structure it shares with them; for the attention kernels,
a row’s softmax normalization chain is canonicalized by the row’s first element and reused by the
remaining 63 elements of the row. Z3, by contrast, solves each element’s VC as an independent
query at unchanged cost. Hence, Volta’s first solve time is often significantly higher than Z3’s, but
its median solve time is significantly lower.

7   Related Work
Prior work on equivalence checking does not support GPU parallelism or synchronization [6, 15,
29, 35, 47, 52, 53, 63, 65, 66, 68, 69, 72, 76]. Alive [48] symbolically evaluates straight-line single-
threaded programs over bit-vectors to generate decision problems for equivalence checking that
can be handed over to SMT solvers. Volta can be seen as generalizing this mechanism to many
threads running in parallel that synchronize with each other to perform computations over the reals.
Treating floating-point operations as uninterpreted functions renders standard GPU optimizations
unsound [4, 18], while fully modeling IEEE-754 semantics is known to cause equivalence checking
failures for such optimizations [38]. Mirage [76] operates at a higher level than Volta, directly on
a language of multi-linear operators, division, and exponentiation. Ultimately, the final verification
conditions look quite similar to Volta’s, but with the allowance of rational functions. Mirage
tackles these conditions via the identity-testing procedure of Li and Wu [43], which, unlike our
algorithm, lacks provable soundness (see Section 4.4).
   Several existing approaches bound the worst-case numerical error in floating-point implementa-
tions [22, 36, 37, 60, 71]. However, the worst-case errors when arithmetic operations are reordered
in tensor computations (as in GPU optimization) are huge for contrived inputs and do not provide
useful insights. For ensuring memory safety in floating-point programs, enforcing non-interference
between floating-point and non-floating-point values has proven useful [27].
   During its operation, the equivalence checker also establishes well-synchronization, guaranteeing
both deadlock freedom and the absence of data races. There is a rich body of work that focuses
exclusively on data race detection in GPU programs. Traditional data race analyses consider only
where memory accesses occur, ignoring what data is being accessed, whereas an equivalence
checker must reason about both. FaialAA [46] represents the state of the art in sound data race
freedom checking, but, like most prior work, supports only basic synchronization primitives such as
syncthreads and does not support syncwarp. A notable exception is Weft [67], which addresses
producer-consumer synchronization that lies outside the scope of our work. Volta achieves higher
precision than FaialAA because its symbolic evaluation aggressively propagates constant values;
for example, it does not report the spurious data race identified by FaialAA in its Alarm 4, Figure
1 [46] (Section 6.4). However, FaialAA provides sound (though incomplete) analysis for GPU
kernels beyond structured-CTAs, including kernels with non-trivial control flow and statically
unknown array indices, which Volta rejects outright. The primary advantages of Volta’s race
checker are its simplicity and efficiency: it runs online during symbolic execution, maintaining

                                                          , Vol. 1, No. 1, Article . Publication date: August 2026.
24                            Benjamin Driscoll, Kshitij Dubey, Anjiang Wei, Neeraj Kayal, Rahul Sharma, and Alex Aiken


Table 9. Per-element VC times using Volta’s decision procedure and Z3, without and with the axiom
∀𝑥, 𝑦. 𝑒 𝑥 𝑒 𝑦 = 𝑒 𝑥+𝑦 . “Volta First” solves the VC of one output tensor element in isolation; “Volta Median” is the
median per-element time when solving the VCs of all output elements in one pass, which amortizes one-time
setup and shared canonicalization work across the elements. For the reductions, whose output is a single
element, the two Volta columns measure the same work in different runs. The axiom is relevant only when a
VC contains exponentials, so it is omitted for the other benchmarks. “Unknown” indicates that Z3 returned
unknown after the parenthesized time. Both Volta and Z3 version 4.8.12 were given a single thread and a 10
minute timeout, running on a 128-core 2.25 GHz AMD EPYC 7742 processor with 995 GB of RAM.

          Kernel               Volta First (ms)      Volta Median (ms)      Z3 (ms)        Z3 + Axiom (ms)
          Red-1                        <1                   <1                 3.6                 —
          Red-2                        <1                   <1                 3.6                 —
          Red-3                        <1                   <1                 3.6                 —
          Red-4                        <1                   <1                 3.6                 —
          MatMul-1                     435                  18                 45                  —
          MatMul-2                     358                  17                 47                  —
          MatMul-3                     385                  17                 47                  —
          MatMul-4                     383                  17                 49                  —
          MatMul-5                     383                  17                 48                  —
          MatMul-6                     385                  18                 50                  —
          MatMul-7                     388                  18                 47                  —
          Conv2D                       313                  <1                 5.1                 —
          GEMM-1                       165                  10                 50                  —
          GEMM-2                       163                  10                 49                  —
          GEMM-3                       162                  10                 47                  —
          32 × 32 × 32                  16                  1.9                9.3                 —
          64 × 32 × 32                  46                  4.4                17                  —
          64 × 64 × 32                 217                  12                 45                  —
          Attention                   141                   1.3               395                388
          FA1                         6385                  90           Unknown (3.0 s)    Unknown (319 s)
          FA1-TC                      6481                  88           Unknown (3.0 s)    Unknown (319 s)
          FA2-TC                      6382                  89           Unknown (3.0 s)    Unknown (317 s)
          Causal-Attention             11                   <1                3.7                3.6
          Causal-FA1                   33                   <1                3.8                3.8
          Causal-FA1-TC                98                   <1                3.8                3.8
          Causal-FA2-TC                20                   <1                3.9                3.8



only the small additional context X of Section 4.2, and adds time linear in the number of executed
instructions. Other approaches either suffer from exponential blowup [42, 45], fail to detect certain
data races [26, 31, 32, 44, 61, 62, 77, 79, 80], or exhibit high false positive rates [10, 34]. Several
analyses rely on reductions [7, 16, 17, 40, 41, 46] that are sound only when the synchronization
primitive is a barrier across all threads. In these methods, the kernel analysis can be partitioned into
barrier intervals, defined as code segments between two consecutive executions of syncthreads.
However, in the presence of syncwarp and tensor core operations, which synchronize only subsets
of threads, the barrier interval assumption no longer holds. Finally, test amplification [39] can be
seen as a special case of Volta’s data race checking, where all threads run identical commands and
synchronize exclusively with barriers across all threads.
   Lifting systems seek to translate code in low-level, typically general purpose, languages into code
in higher-level, typically domain specific, languages so that code can be more easily maintained
and better re-optimized, retargeted, or parallelized by compilers. C2TACO [50] lifts C to TACO, as
its name suggests, STNG [33] lifts Fortran to a stencil DSL and then translates to Halide, Tenspiler

, Vol. 1, No. 1, Article . Publication date: August 2026.
Equivalence Checking of ML GPU Kernels                                                                                 25


[64] lifts C, C++, or Python to a tensor IR and then translates to various backends, such as PyTorch,
and LLMLift [8] lifts C, C++, or Python to a custom Python DSL and then translates to a similar
set of backends. C2TACO does not provide formal guarantees about its output, instead relying
on random testing. However, the latter three systems do verify equivalence of the lifted code and
the original code. The fact that these approaches rely on recovering a high-level IR complicates
the kinds of VCs they must generate—all of them make non-trivial use of general purpose SMT
solvers—and the process of generating the VCs itself, which is done, e.g., in the case of STNG, by
counterexample-guided inductive synthesis [70]. Moreover, these systems lift sequential code—C,
C++, Fortran, or Python loop nests—whereas a GPU kernel comprises hundreds or thousands of
concurrent threads. Applying lifting in our setting would additionally require modeling shared
memory, barrier and warp-level synchronization, and the attendant possibility of data races and
deadlocks.

8 Conclusion and Future Work
We have presented Volta, the first equivalence checker for ML GPU kernels. Volta operates
directly on low-level PTX, taking advantage of known tensor sizes and thread IDs to simplify the
space of expressions it must support. PTX is currently the lowest-level, public-facing language for
NVIDIA GPUs and, therefore, the ultimate target of open-source compilation pipelines.
   Volta interprets kernels to obtain a symbolic expression for each output tensor element and
checks the implied verification conditions using a specialized canonicalization procedure. Soundness
and completeness are guaranteed by virtue of the semantics given in this paper and the Agda-
verified confluence theorem. We also prove the decidability of identities between certain polynomials
with exponentials over the reals.
   This paper focuses on verification of programs that synchronize with blocking operations. We
leave asynchronous CUDA intrinsics such as pipeline and tma for future work.

Data-Availability Statement
The kernels we used in our benchmarks and the Agda code that proves Lemma 1 are available
via Zenodo [24], and were submitted for artifact evaluation. Our implementation is available at
https://github.com/willtunnels/volta or as another Zenodo upload [25].

Acknowledgments
This material is based upon work supported by the Defense Advanced Research Projects Agency
(DARPA) under Contract HR0011-25-2-0039, as part of the MOCHA program. We would like to
thank the following people for their helpful discussions: Jubi Taneja, Madanlal Musuvathi, Aditya
Nori, Ashish Panwar, Aseem Rastogi, Tyler Sorensen, Nikhil Swamy, Srikar Veluvali, Hari VK,
Michael Bauer, Manolis Papadakis, and Sean Treichler.

References
 [1] AMD. 2025. What is ROCm? https://rocm.docs.amd.com/en/docs-6.4.2/what-is-rocm.html
 [2] Anthropic. 2025. Claude Code. Agentic coding assistant built on the Claude model. Retrieved August 15, 2026 from
     https://www.anthropic.com/claude-code
 [3] Jai Arora, Sirui Lu, Devansh Jain, Tianfan Xu, Farzin Houshmand, Phitchaya Mangpo Phothilimthana, Mohsen Lesani,
     Praveen Narayanan, Karthik Srinivasa Murthy, Rastislav Bodík, Amit Sabne, and Charith Mendis. 2025. TensorRight:
     Automated Verification of Tensor Graph Rewrites. Proc. ACM Program. Lang. 9, POPL, Article 29 (2025), 32 pages.
     doi:10.1145/3704865
 [4] Seongwon Bang, Seunghyeon Nam, Inwhan Chun, Ho Young Jhoo, and Juneyoung Lee. 2022. SMT-Based Translation
     Validation for Machine Learning Compiler. In CAV. doi:10.1007/978-3-031-13188-2_19


                                                                 , Vol. 1, No. 1, Article . Publication date: August 2026.
26                            Benjamin Driscoll, Kshitij Dubey, Anjiang Wei, Neeraj Kayal, Rahul Sharma, and Alex Aiken


 [5] Carlo Baronio, Pietro Marsella, Ben Pan, Simon Guo, and Silas Alberti. 2025. Kevin: Multi-Turn RL for Generating
     CUDA Kernels. In Proceedings of the Efficient Systems for Foundation Models (ES-FoMo-III) Workshop, ICML 2025.
     doi:10.48550/arXiv.2507.11948
 [6] Péter Bereczky, Dániel Horpácsi, and Simon Thompson. 2024. Program Equivalence in the Erlang Actor Model.
     Computers 13, 11 (2024), 276. doi:10.3390/computers13110276
 [7] Adam Betts, Nathan Chong, Alastair F. Donaldson, Shaz Qadeer, and Paul Thomson. 2012. GPUVerify: a verifier for
     GPU kernels. In OOPSLA, Gary T. Leavens and Matthew B. Dwyer (Eds.). doi:10.1145/2384616.2384625
 [8] Sahil Bhatia, Jie Qiu, Niranjan Hasabnis, Sanjit A. Seshia, and Alvin Cheung. 2024. Verified Code Transpilation with
     LLMs. In Advances in Neural Information Processing Systems, A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet,
     J. Tomczak, and C. Zhang (Eds.), Vol. 37. Curran Associates, Inc., 41394–41424. doi:10.52202/079017-1310
 [9] NVIDIA Developer Blog. 2017. Implicit Warp-Synchronous Programming Is Unsafe. NVIDIA Developer Blog.
     https://developer.nvidia.com/blog/using-cuda-warp-level-primitives
[10] Stefan Blom, Marieke Huisman, and Matej Mihelcic. 2014. Specification and verification of GPGPU programs. Sci.
     Comput. Program. 95 (2014). doi:10.1016/j.scico.2014.03.013
[11] Simon Boehm. 2022. How to Optimize a CUDA Matmul Kernel for cuBLAS-like Performance: a Worklog. https:
     //siboehm.com/articles/22/CUDA-MMM
[12] James Bradbury, Roy Frostig, Peter Hawkins, Matthew James Johnson, Chris Leary, Dougal Maclaurin, George Necula,
     Adam Paszke, Jake VanderPlas, Skye Wanderman-Milne, and Qiao Zhang. 2018. JAX: composable transformations of
     Python+NumPy programs. http://github.com/jax-ml/jax
[13] Stephen Brookes. 2007. A semantics for concurrent separation logic. Theoretical Computer Science 375, 1 (2007),
     227–270. Festschrift for John C. Reynolds’s 70th birthday. doi:10.1016/j.tcs.2006.12.034
[14] Wentao Chen, Jiace Zhu, Qi Fan, YeHan Ma, and An Zou. 2025. CUDA-LLM: LLMs Can Write Efficient CUDA Kernels.
     arXiv preprint arXiv:2506.09092 (2025). doi:10.48550/arXiv.2506.09092
[15] Berkeley Churchill, Oded Padon, Rahul Sharma, and Alex Aiken. 2019. Semantic Program Alignment for Equivalence
     Checking. In PLDI. 1027–1040. doi:10.1145/3314221.3314596
[16] Tiago Cogumbreiro, Julien Lange, Dennis Liew, and Hannah Zicarelli. 2024. Memory access protocols: certified
     data-race freedom for GPU kernels. Formal Methods Syst. Des. 63, 1 (2024). doi:10.1007/s10703-023-00415-0
[17] Tiago Cogumbreiro, Julien Lange, Dennis Liew Zhen Rong, and Hannah Zicarelli. 2021. Checking Data-Race Freedom
     of GPU Kernels, Compositionally. In CAV, Alexandra Silva and K. Rustan M. Leino (Eds.). 403–426. doi:10.1007/978-3-
     030-81685-8_19
[18] Peter Collingbourne, Cristian Cadar, and Paul H.J. Kelly. 2011. Symbolic crosschecking of floating-point and SIMD
     code. In Proceedings of the Sixth Conference on Computer Systems (EuroSys ’11). doi:10.1145/1966445.1966475
[19] NVIDIA Corporation. 2025. CUTLASS: CUDA Templates and Python DSLs for High-Performance Linear Algebra.
     Available from https://github.com/NVIDIA/cutlass.
[20] Tri Dao. 2023. FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning. arXiv preprint
     arXiv:2307.08691 (2023). doi:10.48550/arXiv.2307.08691
[21] Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, and Christopher Ré. 2022. FlashAttention: Fast and Memory-
     Efficient Exact Attention with IO-Awareness. In Advances in Neural Information Processing Systems. 16344–16359.
     doi:10.52202/068431-1189
[22] Eva Darulova and Viktor Kuncak. 2014. Sound compilation of reals. In POPL. 235–248. doi:10.1145/2535838.2535874
[23] Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: an efficient SMT solver. In Proceedings of the Theory and Practice of
     Software, 14th International Conference on Tools and Algorithms for the Construction and Analysis of Systems (Budapest,
     Hungary) (TACAS’08/ETAPS’08). Springer-Verlag, Berlin, Heidelberg, 337–340.
[24] Benjamin Driscoll, Kshitij Dubey, Anjiang Wei, Neeraj Kayal, Rahul Sharma, and Alex Aiken. 2026. Equivalence
     Checking of ML GPU Kernels. doi:10.5281/zenodo.21529230
[25] Benjamin Driscoll, Kshitij Dubey, Anjiang Wei, Neeraj Kayal, Rahul Sharma, and Alex Aiken. 2026. Volta. doi:10.5281/
     zenodo.21945204
[26] Ariel Eizenberg, Yuanfeng Peng, Toma Pigli, William Mansky, and Joseph Devietti. 2017. BARRACUDA: binary-
     level analysis of runtime RAces in CUDA programs. In PLDI, Albert Cohen and Martin T. Vechev (Eds.). 126–140.
     doi:10.1145/3062341.3062342
[27] Patrice Godefroid and Johannes Kinder. 2010. Proving memory safety of floating-point computations by combining
     static and dynamic program analysis. In ISSTA. doi:10.1145/1831708.1831710
[28] Torbjörn Granlund and the GMP development team. 2023. GNU MP: The GNU Multiple Precision Arithmetic Library.
     Retrieved August 15, 2026 from https://gmplib.org/
[29] Shubhani Gupta, Abhishek Rose, and Sorav Bansal. 2020. Counterexample-guided correlation algorithm for translation
     validation. Proc. ACM Program. Lang. 4, OOPSLA, Article 221 (2020), 29 pages. doi:10.1145/3428289



, Vol. 1, No. 1, Article . Publication date: August 2026.
Equivalence Checking of ML GPU Kernels                                                                                    27


[30] Mark Harris. 2013. Optimizing Parallel Reduction in CUDA. https://developer.download.nvidia.com/assets/cuda/files/
     reduction.pdf
[31] Anup Holey, Vineeth Mekkat, and Antonia Zhai. 2013. HAccRG: Hardware-Accelerated Data Race Detection in GPUs.
     In Proceedings of the 2013 42nd International Conference on Parallel Processing. 60–69. doi:10.1109/ICPP.2013.15
[32] Aditya K. Kamath, Alvin A. George, and Arkaprava Basu. 2020. ScoRD: A Scoped Race Detector for GPUs. In ISCA.
     1036–1049. doi:10.1109/ISCA45697.2020.00088
[33] Shoaib Kamil, Alvin Cheung, Shachar Itzhaky, and Armando Solar-Lezama. 2016. Verified lifting of stencil computations.
     SIGPLAN Not. 51, 6 (June 2016), 711–726. doi:10.1145/2980983.2908117
[34] Kensuke Kojima, Akifumi Imanishi, and Atsushi Igarashi. 2018. Automated Verification of Functional Correctness of
     Race-Free GPU Programs. J. Autom. Reason. 60, 3 (2018). doi:10.1007/s10817-017-9428-2
[35] Shuvendu K. Lahiri, Chris Hawblitzel, Ming Kawaguchi, and Henrique Rebêlo. 2012. SYMDIFF: A Language-Agnostic
     Semantic Diff Tool for Imperative Programs. In CAV. 712–717. doi:10.1007/978-3-642-31424-7_54
[36] Wonyeol Lee, Rahul Sharma, and Alex Aiken. 2016. Verifying bit-manipulations of floating-point. In PLDI, Chandra
     Krintz and Emery D. Berger (Eds.). doi:10.1145/2908080.2908107
[37] Wonyeol Lee, Rahul Sharma, and Alex Aiken. 2018. On automatically proving the correctness of math.h implementations.
     Proc. ACM Program. Lang. 2, POPL, Article 47 (2018), 32 pages. doi:10.1145/3158135
[38] Miriam Leeser, Saoni Mukherjee, Jaideep Ramachandran, and Thomas Wahl. 2014. Make it real: Effective floating-point
     reasoning via exact arithmetic. In DATE. doi:10.7873/DATE.2014.130
[39] Alan Leung, Manish Gupta, Yuvraj Agarwal, Rajesh Gupta, Ranjit Jhala, and Sorin Lerner. 2012. Verifying GPU kernels
     by test amplification. In PLDI. doi:10.1145/2254064.2254110
[40] Guodong Li and Ganesh Gopalakrishnan. 2010. Scalable SMT-based verification of GPU kernel functions. In FSE,
     Gruia-Catalin Roman and André van der Hoek (Eds.). doi:10.1145/1882291.1882320
[41] Guodong Li and Ganesh Gopalakrishnan. 2012. Parameterized Verification of GPU Kernel Programs. In IPDPS.
     doi:10.1109/IPDPSW.2012.302
[42] Guodong Li, Peng Li, Geoffrey Sawaya, Ganesh Gopalakrishnan, Indradeep Ghosh, and Sreeranga P. Rajan. 2012.
     GKLEE: concolic verification and test generation for GPUs. In PPoPP, J. Ramanujam and P. Sadayappan (Eds.). doi:10.
     1145/2145816.2145844
[43] Jiatu Li and Mengdi Wu. 2026. Identity Testing for Circuits with Exponentiation Gates. In ITCS.
[44] Pengcheng Li, Xiaoyu Hu, Dong Chen, Jacob Brock, Hao Luo, Eddy Z. Zhang, and Chen Ding. 2017. LD: Low-Overhead
     GPU Race Detection Without Access Monitoring. ACM Trans. Archit. Code Optim. 14, 1 (2017). doi:10.1145/3046678
[45] Peng Li, Guodong Li, and Ganesh Gopalakrishnan. 2014. Practical Symbolic Race Checking of GPU Programs. In SC,
     Trish Damkroger and Jack J. Dongarra (Eds.). doi:10.1109/SC.2014.20
[46] Dennis Liew, Tiago Cogumbreiro, and Julien Lange. 2024. Sound and Partially-Complete Static Analysis of Data-Races
     in GPU Programs. Proc. ACM Program. Lang. 8, OOPSLA2 (2024), 2434–2461. doi:10.1145/3689797
[47] Nuno P. Lopes, Juneyoung Lee, Chung-Kil Hur, Zhengyang Liu, and John Regehr. 2021. Alive2: bounded translation
     validation for LLVM. In PLDI. 65–79. doi:10.1145/3453483.3454030
[48] Nuno P. Lopes, David Menendez, Santosh Nagarakatte, and John Regehr. 2015. Provably correct peephole optimizations
     with alive. In PLDI, David Grove and Stephen M. Blackburn (Eds.). ACM, 22–32. doi:10.1145/2737924.2737965
[49] Angus Macintyre and Alex Wilkie. 1996. On the Decidability of the Real Exponential Field. In Kreiseliana. A K Peters,
     441–467.
[50] José Wesley de Souza Magalhães, Jackson Woodruff, Elizabeth Polgreen, and Michael F. P. O’Boyle. 2023. C2TACO:
     Lifting Tensor Code to TACO. In Proceedings of the 22nd ACM SIGPLAN International Conference on Generative
     Programming: Concepts and Experiences (Cascais, Portugal) (GPCE 2023). Association for Computing Machinery, New
     York, NY, USA, 42–56. doi:10.1145/3624007.3624053
[51] John McCarthy and James Painter. 1967. Correctness of a Compiler for Arithmetic Expressions. In Mathematical Aspects
     of Computer Science (Proceedings of Symposia in Applied Mathematics, Vol. 19). 33–41. doi:10.1090/psapm/019/0242403
[52] Dragana Milovančević and Viktor Kuncak. 2023. Proving and Disproving Equivalence of Functional Programming
     Assignments. Proc. ACM Program. Lang. 7, PLDI, Article 144 (2023), 24 pages. doi:10.1145/3591258
[53] George C. Necula. 2000. Translation Validation for an Optimizing Compiler. In PLDI. 83–94. doi:10.1145/349299.349314
[54] Ulf Norell. 2009. Dependently typed programming in Agda. In Proceedings of the 4th International Workshop on Types
     in Language Design and Implementation (Savannah, GA, USA) (TLDI ’09). Association for Computing Machinery, New
     York, NY, USA, 1–2. doi:10.1145/1481861.1481862
[55] NVIDIA. 2024. CUDA Toolkit Documentation. https://docs.nvidia.com/cuda/
[56] NVIDIA Corporation. 2017. NVIDIA Tesla V100 GPU Architecture: The World’s Most Advanced Data Center GPU. Technical
     Report. NVIDIA. https://images.nvidia.com/content/volta-architecture/pdf/volta-architecture-whitepaper.pdf
[57] NVIDIA Corporation. 2025. NVIDIA Compute Sanitizer. https://developer.nvidia.com/compute-sanitizer. CUDA
     correctness and memory checking tool.


                                                                    , Vol. 1, No. 1, Article . Publication date: August 2026.
28                            Benjamin Driscoll, Kshitij Dubey, Anjiang Wei, Neeraj Kayal, Rahul Sharma, and Alex Aiken


[58] NVIDIA Corporation. 2025. PTX: Parallel Thread Execution ISA. NVIDIA. Version 9.0. https://docs.nvidia.com/cuda/
     parallel-thread-execution/index.html
[59] Anne Ouyang, Azalia Mirhoseini, and Percy Liang. 2025. Surprisingly Fast AI-Generated Kernels We Didn’t Mean to
     Publish (Yet). https://crfm.stanford.edu/2025/05/28/fast-kernels.html
[60] Pavel Panchekha, Alex Sanchez-Stern, James R. Wilcox, and Zachary Tatlock. 2015. Automatically improving accuracy
     for floating point expressions. SIGPLAN Not. 50, 6 (2015). doi:10.1145/2737924.2737959
[61] Yuanfeng Peng, Vinod Grover, and Joseph Devietti. 2018. CURD: a dynamic CUDA race detector. In PLDI, Jeffrey S.
     Foster and Dan Grossman (Eds.). 390–403. doi:10.1145/3192366.3192368
[62] Phillipe A. Pereira, Higo F. Albuquerque, Hendrio Marques, Isabela da Silva, Celso B. Carvalho, Lucas C. Cordeiro,
     Vanessa Santos, and Ricardo Ferreira. 2016. Verifying CUDA programs using SMT-based context-bounded model
     checking. In Symposium on Applied Computing, Sascha Ossowski (Ed.). 1648–1653. doi:10.1145/2851613.2851830
[63] Amir Pnueli, Michael Siegel, and Eli Singerman. 1998. Translation Validation. In TACAS. 151–166. doi:10.1007/
     BFb0054170
[64] Jie Qiu, Colin Cai, Sahil Bhatia, Niranjan Hasabnis, Sanjit A. Seshia, and Alvin Cheung. 2024. Tenspiler: A Verified-
     Lifting-Based Compiler for Tensor Operations. In 38th European Conference on Object-Oriented Programming (ECOOP
     2024) (Leibniz International Proceedings in Informatics (LIPIcs), Vol. 313), Jonathan Aldrich and Guido Salvaneschi (Eds.).
     Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl, Germany, 32:1–32:28. doi:10.4230/LIPIcs.ECOOP.2024.32
[65] David A. Ramos and Dawson Engler. 2011. Practical, Low-Effort Equivalence Verification of Real Code. In CAV. 669–685.
     doi:10.1007/978-3-642-22110-1_55
[66] Eric Schkufza, Rahul Sharma, and Alex Aiken. 2013. Stochastic Superoptimization. In ASPLOS. 305–316. doi:10.1145/
     2451116.2451150
[67] Rahul Sharma, Michael Bauer, and Alex Aiken. 2015. Verification of Producer-Consumer Synchronization in GPU
     Programs. In Proceedings of the 36th ACM SIGPLAN Conference on Programming Language Design and Implementation
     (PLDI). doi:10.1145/2737924.2737962
[68] Rahul Sharma, Eric Schkufza, Berkeley Churchill, and Alex Aiken. 2013. Data-Driven Equivalence Checking. In
     OOPSLA. 391–406. doi:10.1145/2544173.2509509
[69] Rahul Sharma, Eric Schkufza, Berkeley Churchill, and Alex Aiken. 2015. Conditionally Correct Superoptimization. In
     OOPSLA. 147–162. doi:10.1145/2814270.2814278
[70] Armando Solar-Lezama, Liviu Tancau, Rastislav Bodik, Sanjit Seshia, and Vijay Saraswat. 2006. Combinatorial sketching
     for finite programs. In Proceedings of the 12th International Conference on Architectural Support for Programming
     Languages and Operating Systems (San Jose, California, USA) (ASPLOS XII). Association for Computing Machinery,
     New York, NY, USA, 404–415. doi:10.1145/1168857.1168907
[71] Alexey Solovyev, Marek S. Baranowski, Ian Briggs, Charles Jacobsen, Zvonimir Rakamaric, and Ganesh Gopalakrishnan.
     2019. Rigorous Estimation of Floating-Point Round-Off Errors with Symbolic Taylor Expansions. ACM Trans. Program.
     Lang. Syst. 41, 1 (2019). doi:10.1145/3230733
[72] Ofer Strichman and Benny Godlin. 2005. Regression Verification - A Practical Way to Verify Programs. In Verified
     Software: Theories, Tools, Experiments (VSTTE 2005). Springer, 496–501. doi:10.1007/978-3-540-69149-5_54
[73] Philippe Tillet, H. T. Kung, and David Cox. 2019. Triton: An Intermediate Language and Compiler for Tiled Neural
     Network Computations. In Proceedings of the 3rd ACM SIGPLAN International Workshop on Machine Learning and
     Programming Languages (MAPL ’19). doi:10.1145/3315508.3329973
[74] Lei Wang, Yu Cheng, Yining Shi, Zhengju Tang, Zhiwen Mo, Wenhao Xie, Lingxiao Ma, Yuqing Xia, Jilong Xue,
     Fan Yang, and Zhi Yang. 2025. TileLang: A Composable Tiled Programming Model for AI Systems. arXiv preprint
     arXiv:2504.17577 (2025). doi:10.48550/arXiv.2504.17577
[75] Anjiang Wei, Tianran Sun, Yogesh Seenichamy, Hang Song, Anne Ouyang, Azalia Mirhoseini, Ke Wang, and Alex
     Aiken. 2025. Astra: A Multi-Agent System for GPU Kernel Performance Optimization. arXiv preprint arXiv:2509.07506
     (2025). doi:10.48550/arXiv.2509.07506
[76] Mengdi Wu, Xinhao Cheng, Shengyu Liu, Chunan Shi, Jianan Ji, Man Kit Ao, Praveen Velliengiri, Xupeng Miao,
     Oded Padon, and Zhihao Jia. 2025. Mirage: a multi-level superoptimizer for tensor programs. In Proceedings of the
     19th USENIX Conference on Operating Systems Design and Implementation (Boston, MA, USA) (OSDI ’25). USENIX
     Association, USA, Article 13, 18 pages. https://www.usenix.org/conference/osdi25/presentation/wu-mengdi
[77] Mingyuan Wu, Yicheng Ouyang, Husheng Zhou, Lingming Zhang, Cong Liu, and Yuqun Zhang. 2020. Simulee:
     detecting CUDA synchronization bugs via memory-access modeling. In ICSE, Gregg Rothermel and Doo-Hwan Bae
     (Eds.). 937–948. doi:10.1145/3377811.3380358
[78] Jiaqi Yin, Zhan Song, Nicolas Bohm Agostini, Antonino Tumeo, and Cunxi Yu. 2025. HEC: Equivalence Verification
     Checking for Code Transformation via Equality Saturation. In 2025 USENIX Annual Technical Conference (USENIX ATC
     25). USENIX Association, 1181–1196. https://www.usenix.org/conference/atc25/presentation/yin



, Vol. 1, No. 1, Article . Publication date: August 2026.
Equivalence Checking of ML GPU Kernels                                                                                 29


[79] Mai Zheng, Vignesh T. Ravi, Feng Qin, and Gagan Agrawal. 2011. GRace: a low-overhead mechanism for detecting data
     races in GPU programs. In PPoPP, Calin Cascaval and Pen-Chung Yew (Eds.). 135–146. doi:10.1145/1941553.1941574
[80] Mai Zheng, Vignesh T. Ravi, Feng Qin, and Gagan Agrawal. 2014. GMRace: Detecting Data Races in GPU Programs
     via a Low-Overhead Scheme. IEEE Trans. Parallel Distributed Syst. 25, 1 (2014), 104–115. doi:10.1109/TPDS.2013.44




                                                                 , Vol. 1, No. 1, Article . Publication date: August 2026.
