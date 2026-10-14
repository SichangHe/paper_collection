                                                     The Output-Space Hypothesis: Enumerative
                                                     Equivalence Checking for Tensor Programs
                                                      Paul Biberstein                             Joseph Devietti                                  Mayur Naik
                                                  paulbib@seas.upenn.edu                      devietti@seas.upenn.edu                       mhnaik@seas.upenn.edu
                                                 University of Pennsylvania                  University of Pennsylvania                    University of Pennsylvania
                                                   Philadelphia, PA, USA                       Philadelphia, PA, USA                         Philadelphia, PA, USA

                                         Abstract                                                                     Differential              Dirigo
                                         Tensor programs, as used in deep learning models, are a                        Testing                 (ours)
                                         prime target for optimization, as small performance improve-                                                             input   output
arXiv:2609.19611v1 [cs.PL] 17 Sep 2026




                                         ments can have a large impact across training or inference                                                              tensor   tensor
                                         workloads. However, such optimizations are complicated
                                         and can produce subtle bugs. Traditionally, correctness is
                                         assumed when differential testing against a reference on
                                         random inputs fails to reveal bugs. However, the inputs to                     space of all possible input tensors
                                         these programs are massive tensors, and finding bugs can
                                         require generating extremely low likelihood inputs with pre-            Figure 1. Differential testing (left) samples sparsely (blue
                                         cise relationships among their values.                                  squares) from a large input space, often missing bugs (in
                                            We propose a novel way to find bugs more consistently by             red). Dirigo starts from one output location ℓ (purple) and
                                         flipping the quantifiers. Rather than generating a single in-           works backwards to find the input locations (blue) that affect
                                         put and checking all output tensor locations for equivalence,           ℓ, checking them across all possible inputs.
                                         what if you could check a single output tensor location’s
                                         equivalence for all inputs? We implement this idea in a sys-
                                                                                                                 miss bugs triggered by specific inputs and deem a buggy
                                         tem, Dirigo, by using a novel symbolic execution strategy.
                                                                                                                 kernel correct. Moreover, KernelBench is also the primary
                                         We demonstrate that Dirigo can find bugs effectively in a
                                                                                                                 benchmark used by the burgeoning field of agentic kernel
                                         public dataset of 6,988 AI-written CUDA kernels that are all
                                                                                                                 optimization [5, 18, 19, 23, 24, 31], and agents frequently
                                         marked correct by differential testing. Of these, Dirigo finds
                                                                                                                 “reward-hack” [20, 28] and produce fast but incorrect kernels
                                         600 kernels that are actually buggy, and finds 97.3% of those
                                                                                                                 that slip past differential testing. Formal verification is a nat-
                                         bugs within two minutes.
                                                                                                                 ural antidote, but formal techniques struggle to scale to real
                                                                                                                 tensor programs, even though these are generally specialized
                                         1   Introduction                                                        to fixed input and output shapes and lack data-dependent
                                         Deep learning models are generally written in tensor pro-               control-flow or indirect memory accesses.
                                         gramming frameworks like PyTorch, which offer the flexi-                   Our key insight is that, while bugs are sparse in the input
                                         bility of a high-level language while maintaining workable              space, they are often dense in the output space of a tensor
                                         performance. If more performance is needed, these frame-                program—a buggy input will trigger incorrect values at many
                                         works allow parts of the program to be replaced with highly-            output locations, not just one. We call this the Output-Space
                                         optimized GPU kernels. To avoid bugs when writing low-                  Hypothesis: bugs are much denser in the output space of a
                                         level GPU kernels, we need automated systems that can                   tensor program than in input space. But how can we leverage
                                         perform end-to-end equivalence-checking on tensor pro-                  this insight to find bugs more efficiently?
                                         grams even in the presence of these custom kernels. While                  Our system, Dirigo, uses a scalable symbolic execution
                                         many works port traditional CPU testing methods to the                  framework to enumerate the dataflow within a mixed Py-
                                         GPU [6, 12, 22], they take a per-kernel view and do not scale           Torch/CUDA tensor program, allowing us to work backwards
                                         or support heterogeneous programs that mix high-level Py-               from one output location to all the input locations that can
                                         Torch operations with custom kernels.                                   affect it (right side of Figure 1). Dirigo assembles an equiva-
                                            In the absence of suitable equivalence-checking, the stan-           lence condition and uses SMT solving to check whether an
                                         dard benchmark for tensor program optimization, Kernel-                 optimized kernel and a reference implementation produce
                                         Bench [29], adopts a simple correctness check based on dif-             the same values, at a given output location, for all possi-
                                         ferential testing—comparing the optimized kernel’s output               ble values of the upstream inputs. Checking a handful of
                                         against a reference implementation’s up to a hand-tuned                 output locations offers a huge tractability advantage when
                                         tolerance. As the left side of Figure 1 illustrates, differential       output tensors have millions of elements. Thanks to the
                                         testing checks few of the many possible inputs, so it can               Output-Space Hypothesis, sparse checking suffices to find
                                                                                                             1
                                                                                                                   Paul Biberstein, Joseph Devietti, and Mayur Naik

Reference program (PyTorch)                                   Optimized program — host                         Optimized program — CUDA kernel
    x = conv_transpose2d(x, W, b,                             x = at::conv_transpose2d(x, W, b,                __global__ void fused_min_sum_kernel_shared(    1
         stride=2, pad=1, out_pad=1)                               stride=2, pad=1, out_pad=1);                    const float* in, float* out,                2
    x = torch.min(x, dim=1, keepdim=True)[0]                  // x is [N,C,H,W] = [128,16,64,64]                   int N, int C, int H, int W) {               3
    x = torch.sum(x, dim=2, keepdim=True)                     auto out = torch::zeros({N,1,1,W}, opts);          int n = blockIdx.x, w = blockIdx.y;           4
                                                              fused_min_sum_kernel_shared<<<dim3(N,W),           int tid = threadIdx.x, nT = blockDim.x;       5
    x = F.gelu(x)
    x = x + bias                                                   256, 256*4>>>(x.data_ptr<float>(),            // one block per (n,w)                        6
                                                                   out.data_ptr<float>(), N,C,H,W);              float psum = 0.0f;                            7
                                                              out = at::gelu(out);                               for (int h = tid; h < H; h += nT) {           8
                                                              out = out + bias;                                    float m = FLT_MAX;                          9
                                                                                                                   for (int c = 0; c < C; ++c)                10
      conv(𝑥 ) [𝑛, ·, ·, 𝑤 ]                                                                                         m = fminf(m, in[((n*C+c)*H+h)*W+w]);     11
                                                                                                                   psum += m;                                 12
                                                                                                                 }                                            13
                                                                                                                 // tree-reduce partials in shared memory     14
                                                                                                                 extern __shared__ float sdata[];             15
                                                                                                                 sdata[tid] = psum; __syncthreads();          16
                                                                                                                 // BUG: stops one step early; fix: s ≥ 32    17
                                                                                                                 for (unsigned s = nT/2; s > 32; s >>= 1) {   18
                               min    opt: sum ℎ<32                gelu(𝑠 )                                        if (tid < s) sdata[tid] += sdata[tid+s];   19
                                                      −5.1                                                         __syncthreads();                           20
                                                                                                  difference
                                                                                                                 }                                            21
                                                                                                    visible      // warp 0 finishes the sum with shuffles     22
                                                                                                                 if (tid < 32) {                              23
                                                                                                                   float v = sdata[tid];                      24
                                                                              −8          −4            0          for (int off = 16; off > 0; off /= 2)      25
                                                                                                                     v += __shfl_down_sync(0xffffffff,v,off); 26
                                     ref: sum ℎ<64                                                                 if (tid == 0) out[n*W + w] = v;            27
                                                      −10.5                                                      }                                            28
                                                                                                               }                                              29


Figure 2. A worked example of a real bug (KernelBench level-2 task 36, AI CUDA Engineer dataset row 5354). Above: The
reference program is optimized by fusing two operations into a custom kernel, but the kernel has an incorrect loop bound.
Below: Random inputs are highly unlikely to expose the bug because the min and sum operations conspire to produce values
that are in the flat region of GELU, masking the bug.

many bugs. Checking can also be parallelized across output                                     from the KernelBench level-2 benchmark. The program is
locations, offering a path to full equivalence-checking with                                   representative of typical deep learning workloads: it takes
sufficient compute.                                                                            an input tensor x and weights and biases W and b and com-
   We use Dirigo to search for bugs in the 6,988 agent-                                        putes their convolution, then a channel-wise minimum and
generated KernelBench level-2 solutions in the AI CUDA                                         a height-wise sum, and finally applies GELU (an activation
Engineer dataset [19] that KernelBench’s differential test-                                    function) [17] and adds the bias.
ing marks correct. We find that 600 (8.6%) are in fact buggy,                                     This program is a good example of the restricted subset of
revealing the brittleness of differential testing in practice.                                 programs we target: control flow, memory access addresses,
   This paper makes the following contributions:                                               and shapes of all intermediate tensors are data independent.
      1. The Output-Space Hypothesis: the bugs likely to arise                                 In other words, the order of operations executed and shapes
         in tensor programs are sparse in the input-value space                                of their results are constant under any input data, so long as
         but dense in the output-location space.                                               the input shapes are unchanged. This is a common pattern
      2. Dirigo, a scalable method for symbolic execution and                                  in deep learning workloads:
         equivalence-checking that makes per-location equiv-                                      1. KernelBench, the dominant benchmark in kernel opti-
         alence checks feasible for tensor programs.                                                 mization, exhibits this property for all level-1, level-2,
      3. 600 new bugs in the AI CUDA Engineer dataset’s solu-                                        and level-3 tasks (level-4 has only a specification, no
         tions to the KernelBench level-2 problems, alongside                                        stable implementation).
         1,646 solutions shown to be fully correct across all                                     2. PyTorch and JAX, the two most popular deep learn-
         output locations.                                                                           ing frameworks, only accelerate a computation (with
      4. Experimental evidence that the Output-Space Hypoth-                                         torch.compile and jax.jit respectively) if it has
         esis holds for our dataset.                                                                 this property, indicating the prevalence of code that
                                                                                                     matches this restriction.
2      Illustrative Overview                                                                     Now compare the reference program with the optimized
We now walk through an illustrative example of tensor pro-                                     version of the same computation taken from the AI CUDA
gram optimization via custom kernels to show how our hy-                                       Engineer Dataset. Here, the optimized implementation calls
pothesis plays out on a real optimization trajectory. Con-                                     the same PyTorch function in three out of five cases, but fuses
sider the reference program in Figure 2, which is task 36                                      the min and sum calls into an optimized kernel in CUDA to
                                                                                      2
The Output-Space Hypothesis: Enumerative Equivalence Checking for Tensor Programs


                                (1) Trace              (2) Merge                  (3) Execute                      (4) Check
                                instrument              SSA; trim                  symbolic tid,                   per-location
                                a GPU run             shared prefix                 bid, tensors                    Z3 queries
 Reference program                                                                                                           unsat at every visited
                                         trace B: 5 ATen
 conv_transpose2d → min →                                                                                                    location ⇒
                                         events                 merged trace: shared         write sets per launch,
 sum → gelu → + bias                                                                                                         equivalent
                                                                conv_transpose2d             symbolic over tid, bid;
 Optimized program                       trace A: 3 ATen        trimmed, inputs and          lowered min, sum,
                                                                                                                             sat ⇒ GPU replay ⇒
 conv_transpose2d →                      events + 1             outputs unified              gelu, add
                                                                                                                             confirmed bug
 fused_min_sum_kernel                    launch (args,
 <<<. . . >>> → gelu → + bias            grid, PTX)


Figure 3. The running example’s path through Dirigo. (1) Each program is run on the GPU to extract its trace. (2) The two
traces are merged into one equivalence-checking input. (3) Each kernel launch is lowered to symbolic expressions by a scalable
PTX-level symbolic execution. (4) The expressions are specialized to individual output locations and checked for equivalence
over all inputs.

avoid a round-trip to global memory. The kernel showcases                   0.13. The channel-wise min over 16 channels produces val-
features unique to GPU programming that pose challenges                     ues that are largely in the range [−0.4, −0.1], and the sum,
for analysis:                                                               even operating on only half the column, produces a nega-
                                                                            tive value in the range [−10, −4]. For the difference to clear
    1. Large Thread Grid. The kernel is launched with a                     KernelBench’s 10−2 tolerance, the half-column sum must
       grid of 128 × 64 blocks, each with 256 threads, for a                exceed about −2.7, where GELU stops being flat (see Figure 2,
       total of 2,097,152 threads. This is common in GPU                    bottom). In our simulation, across 400,000 sampled output
       programming, but makes it infeasible to analyze each                 locations the half-column sum never exceeded −3.7 and the
       thread individually.                                                 largest per-location difference between the two programs
    2. Shared Memory. The kernel uses shared memory                         was 5 × 10−4 .
       (a programmer-managed scratchpad backed by the                          To find such bugs efficiently we must shift our frame of
       same memory as the L1 cache) to hold each thread’s                   reference: rather than checking all output locations for a
       partial sum of channel-wise minimums while they                      single input, what if we could check a single output location
       are reduced across the block. This is a common opti-                 for all inputs? Our bug is not specific to one output location:
       mization, and is challenging to analyze since shared                 any location can be wrong given sufficiently positive input
       memory is shared across threads in a block, but not                  values. So we select an arbitrary location, say (0, 0, 0, 0), and
       between blocks.                                                      construct symbolic expressions for the value of this output
    3. Warp-Level Reductions. The kernel finishes the sum                   location in the reference and optimized implementations:
       with a warp-level reduction across 32 threads (a warp).
       Again, cross-thread communication poses a challenge.                                               ?              
                                                                                      gelu 𝑆 (64) + 𝑏 [0] = gelu 𝑆 (32) + 𝑏 [0]
As a result the optimized kernel is not equivalent to the                                    Í
                                                                            where 𝑆 (𝐻 ) = ℎ<𝐻 min𝑐<16 𝑀 [0, 𝑐, ℎ, 0] and 𝑀 is the post-
reference implementation: the first loop that accumulates                   convolution tensor. Since the shapes are statically known,
the sum in shared memory has the following configuration:                   a chosen location fixes the bounds of the summation and
   for (unsigned s = nT/2; s > 32; s >>= 1)                                 minimum, and an off-the-shelf SMT solver can find a witness
                                                                            to inequivalence. We can even push additional constraints to
But it should have the adjusted stop condition:
                                                                            the solver to find a counterexample that makes the difference
   for (unsigned s = nT/2; s >= 32; s >>= 1)                                visible above a given tolerance.
Without this fix, the loop misses the last step of accumulating                The natural question, then, is does this property generalize
64 partial results into 32 partial results, so the final intra-             to other tensor programs, and how can we efficiently gen-
warp summation only reads half-sums from shared memory,                     erate symbolic expressions for arbitrary tensor programs?
resulting in a final sum that is incorrect.                                 Next, we describe Dirigo, a system that lets us answer these
   This bug is simple, but proves very challenging for differ-              questions.
ential testing, since exposing it requires complicated rela-
tionships among the tensor’s elements. Informally, running                  3    Dirigo
the reference PyTorch with KernelBench’s default input dis-                 Dirigo is a system for equivalence-checking of tensor pro-
tribution produces a post-convolution tensor whose values                   grams based on the Output-Space Hypothesis that supports
are roughly Gaussian with mean 0 and standard deviation                     analysis of both high-level PyTorch operations and low-level
                                                                        3
                                                                                             Paul Biberstein, Joseph Devietti, and Mayur Naik


CUDA kernels. It is organized into four stages, as depicted              memory copies, and symbols. Since Torch is the only pro-
in Figure 3: (1) Trace in which the trace of each program is             ducer of tensors, we can keep a live list of tensor pointer
extracted via runtime instrumentation, (2) Merge in which                addresses to map kernel arguments to tensors. Since Torch
the traces are combined and optimized by discharging trivial             operations call the CUDA runtime internally, we suppress
equivalence obligations, (3) Execute in which the kernels                the shim during Torch calls. The process is depicted in the
and Torch operations are lowered to symbolic expressions,                top right of Figure 4.
and (4) Check in which the symbolic expressions are con-                    To verify that programs exhibit “traceable behavior”, we
cretized for specific output tensor locations and passed to              run them multiple times with different tensors and check
the Z3 SMT solver to look for counterexamples.                           that the trace is the same. Running torch.compile could
                                                                         also be used to verify the desired behavior.
3.1     Trace
The first step is to extract a representation of the program.            3.2   Merge
We consider only programs that take tensors as inputs and                Once both purportedly equivalent programs are traced, we
produce tensors as output (possibly aliased from the inputs).            combine them into a single equivalence-checking obligation.
We also require that given the same input tensor shapes, the             The first step is to convert them to SSA form to make rea-
program exhibits the same control flow and intermediate                  soning about aliasing and mutation easier. Then we match
tensor shapes regardless of the input values. Further, our               the input and output tensors of the two traces to encode the
prototype assumes the only producers of tensors are Torch                goal that the same inputs should produce the same outputs.
APIs (across Python and C++), and the only consumers are                 This is illustrated in the bottom of Figure 4.
Torch APIs and CUDA runtime APIs, although this could                       Two further optimizations make equivalence-checking
extend to kernel DSLs like Triton and libraries such as JAX.             easier: if the two traces share a common prefix or suffix of
   These assumptions are not particular to Dirigo: the com-              Torch operations, we can trim it to reduce the operations
pilation paths of the major tensor frameworks already im-                replayed by the next stage, Execute. This only preserves
pose them, so programs written to be compiled satisfy them               equivalence under certain conditions: the trimmed prefix
as a matter of course. JAX [7] traces a function once on                 must be surjective, and the suffix injective. However, even
shape-only values and reuses the resulting trace for every               when they don’t meet these conditions, trimming does not
input of that shape. Using a Python conditional on a tensor              change Dirigo’s output, since the spurious counterexample
value is a trace-time error (data-dependent control needs                found by Check still produces equivalent results on the orig-
an explicit lax.cond). PyTorch’s torch.compile [4] takes                 inal programs, so Dirigo will not alert the user. In practice
the same position: TorchDynamo captures a graph special-                 we enable prefix trimming, since nearly all prefix operations
ized to the input shapes, graph-breaks or fails when Python              are surjective, but not suffix trimming, since few suffix oper-
control flow depends on tensor values, and requires explicit             ations are injective.
torch.cond where such dependence is intended. Requiring
the same of the programs we analyze therefore costs nothing              3.3   Execute
for the large body of code that already targets these systems,
                                                                         The Execute stage is a core contribution of Dirigo, as it
including the KernelBench benchmark [29].
                                                                         demonstrates a novel technique for applying symbolic execu-
   With these assumptions in mind, the program’s behavior
                                                                         tion to CUDA kernels, where methods designed for CPU code
is exactly the set of Torch operations and CUDA runtime
                                                                         fail. Intuitively, traditional CPU-focused symbolic executors
events that are executed. Intuitively, this is because:
                                                                         consider each thread individually, but abstract over many
      1. We disregard side-effects (beyond internal mutation),           executions of that thread, such as differing loop bounds and
         so the only data we care about is the output tensors.           dynamic branching. From this perspective, the GPU code we
      2. The only way for output tensors to be modified is via           consider is much simpler as the loops and branches are static
         Torch operations and CUDA runtime events.                       with respect to our symbolic variables. Instead, our complex-
      3. The same set of operations must be executed regard-             ity comes from abstracting over the many threads executing
         less of the input values, since the control flow is data-       the same code in parallel, and their interactions. Concretely,
         independent.                                                    we treat the thread ID and block ID (tid and bid), the only
                                                                         data threads can use to distinguish themselves, as symbolic
  To extract these events, we use a combination of tricks:               values. A single logical thread of symbolic execution then
for Python, TorchDispatchMode records all PyTorch invo-                  captures an unbounded number of physical GPU threads,
cations; for C++, at::RecordFunction records all ATen op-                and we recover a single thread’s behavior by substituting
erations (the C++ bindings to Torch); for CUDA, we use an                concrete tid and bid. The natural question, then, is how to
LD_PRELOAD shim to interpose on the CUDA runtime APIs                    handle interactions between threads, such as shared memory
and record all kernel launches (along with the PTX blob),                and warp-level reductions, which we address next.
                                                                     4
The Output-Space Hypothesis: Enumerative Equivalence Checking for Tensor Programs

Reference program (Python)
 x = conv_transpose2d(x, W, b)        Trace
 x = min(x, dim=1)                             x, W, b      conv_transpose2d     min(dim=1)    sum(dim=2)          gelu   + bias    output
 x = sum(x, dim=2)
 x = gelu(x) + bias                             same
                                                                                      no match: kernel is opaque                   compared
                                               sources
Optimized program (C++ host)
 x = conv_transpose2d(x, W, b);       Trace
                                               x, W, b      conv_transpose2d     fused_min_sum_kernel_shared       gelu   + bias    output
 out = torch::zeros({N,1,1,W});
 fused_min_sum_kernel_shared
   <<<(N,W), 256>>>(x, out);                               Merge
                                                                                 fused_min_sum_kernel_shared       gelu   + bias
 out = gelu(out) + bias;
                                                           conv_output                                                               output
    ATen op           tensor
                                                                                 min(dim=1)    sum(dim=2)          gelu   + bias    compared
    CUDA kernel launch

Figure 4. Trace and Merge on the running example. Left: the reference and optimized programs. Top right: Trace records
each program’s Torch dispatches and CUDA events via TorchDispatchMode, at::RecordFunction, and CUDA-runtime
LD_PRELOAD. Bottom: Merge trims pure prefix operations when they’re common between both programs.

3.3.1 Setup. The CUDA kernel symbolic execution prob-                        Inserting a conditional into the symbolic expression to exe-
lem statement is as follows: given a program text 𝑃 that reads               cute the setp line would leave us stuck at the branch, since
a set of input tensors 𝑥¯ and writes a set of output tensors                 we require a concrete value to determine the branch target
¯ as well as a block count 𝑏 and a threads-per-block count
𝑦,                                                                           (existing methods handle symbolic branch conditions, but
𝑡, we want to produce, for each output tensor 𝑦 ∈ 𝑦, ¯ a map                 concrete targets are much simpler). Instead, at setp instruc-
𝑅 𝑦 : [0, |𝑦|) → S from a flat index into 𝑦 to a symbolic                    tions that only depend on tid and bid, we split our logical
expression over the inputs such that                                         symbolic execution thread into two, one with the tid and bid
                                                                             values satisfying the predicate and one with their comple-
     ∀¯  ¯ [[𝑃]] (𝑥,
      𝑥, 𝑦.       ¯ 𝑏, 𝑡) = 𝑦¯ ⇐⇒ ∀𝑦 ∈ 𝑦.
                                       ¯ ∀𝑖 ∈ [0, |𝑦|),
                                                                             ment (Figure 5a). This way, when we arrive at the branch the
                                       [[𝑅 𝑦 (𝑖)]] 𝑥¯ = 𝑦 [𝑖]                predicate is a uniform concrete value. We do not attempt to
where [[𝑃]] is the semantics of the program 𝑃, S is the set of               later coalesce these threads if their executions converge. This
symbolic expressions over the elements of 𝑥,  ¯ and [[𝑒]] 𝑥¯ eval-           could hypothetically explode the number of logical threads,
uates a symbolic expression 𝑒 by substituting the concrete                   but in practice branching is manageable: we observe a me-
elements of 𝑥¯ for the corresponding symbolic variables.                     dian of 3 logical threads per kernel and a 90th percentile of
   We model integers as bitvectors, since bitwise operations                 15 across the kernels in our evaluation. For setp instructions
are prevalent in GPU kernels, but floats as reals, since we                  that depend on tensor values we do create a symbolic condi-
deem precision errors as out of scope for this work. This                    tional, since our data-independence assumption guarantees
is both desirable, as optimized kernels may not be bitwise                   the predicate is never used for branching.
equivalent, and undesirable, as it doesn’t let us reason about
properties like numerical stability.                                         3.3.3 Shared memory and thread barriers. Most high-
   We accomplish this by tracking an environment that maps                   performance kernels use shared memory to share interme-
registers to symbolic expressions. This allows us to easily                  diate results between threads in a block and eliminate re-
execute instructions like add r1, r2, r3 by looking up                       dundant global memory reads. For shared memory stores to
the symbolic expressions for r2 and r3 and producing a new                   be visible across threads, all threads must synchronize at a
symbolic expression for r1. More complicated are expres-                     barrier, __syncthreads() in CUDA and bar.sync in PTX.
sions that involve the special registers tid and bid, which we               The code we must support looks like
now cover.
                                                                                smem[tid] = gmem_in[tid];
3.3.2 Branching on tid and bid. When execution of a                             __syncthreads();
kernel begins, one logical symbolic execution thread captures                   for (int s = 0; s < blockDim.x; s++)
the behavior of all kernel threads, with constant scaling in                      gmem_out[tid] += smem[s];
the number of threads. However, many kernels branch on                       To capture this behavior, the execution context contains both
tid or bid to for instance mask out certain threads, generally               a symbolic expression representing the current content of
with a setp (“set predicate”) instruction and a predicated                   shared memory, and the set of pending writes to shared mem-
jump, such as                                                                ory (suppose without loss of generality that there is exactly
   setp.lt.u32 p1, %tid, 128                                                 one shared memory region per kernel). When a symbolic
   @!p1 bra label_1                                                          execution thread bundle reaches a barrier, it cannot step until
                                                                         5
                                                                                                                    Paul Biberstein, Joseph Devietti, and Mayur Naik


                       tid 0              64           128           192              256       ■ bitvector ■ real ■ predicate ⊥ indeterminate
                   entry                one logical thread: tid ∈ [0, 256)                      𝑒 |𝜙 : value of 𝑒 in the bundle cut by 𝜙
       bid is never tested
       setp.ge tid,64 [0, 64): loop                                                             thread identity
                                                         [64, 256): partial = 0
           h < H (H=64)                                                                         mov.u32 %r1, %tid;                    𝑟 1 = tid
                bar.sync                                                                        mov.u32 %r2, %ctaid;                  𝑟 2 = bid
  race check; snapshot 𝑆 1                                                                      loop guard
      setp.lt tid,128            no split       [64, 128)     [128, 256): skips the add
           tid < s (s=128)                                                                      setp.ge.s32 %p1, %r1, 64;             𝑝 1 = 0| tid<64 , 1| tid ≥64
                                                                                                @%p1 bra L_zero;
               bar.sync
             snapshot 𝑆 2                                                                       tensor loads
       setp.lt tid,64            no split       no split              no split                  mad.lo.s32 %r4, %r2, 1024, %r1;       𝑟 4 = 1024 bid + tid
uniform on every interval
                                                                                                mad.wide.s32 %rd2, %r4, 4, %rd1;      rd 2 = rd 1 + 4 𝑟 4
              bar.sync                                                                          ld.global.f32 %f1, [%rd2];            𝑓1 = 𝑀 [bid, 0, tid ]
            snapshot 𝑆 3
       setp.lt tid,32 [0, 32) exit                                                              ld.global.f32 %f2, [%rd2+256];        𝑓2 = 𝑀 [bid, 1, tid ]
             warp stage                           exit                  exit
                                                                                                min.f32 %f3, %f1, %f2;                𝑓3 = ite( 𝑓1 < 𝑓2 , 𝑓1 , 𝑓2 )
                                                                                                guarded store
                                                ×8: lanes tid ∈ [0, 32)
                                                                                                setp.ne.s32 %p2, %r1, 0;              𝑝 2 = 0| tid=0 , 1| tid≠0
                             0              8              16           24               32
         setp.ne tid,0                                                                          @%p2 bra L_end;                       bundle tid ≠ 0 exits
                                                      [1, 32): exit                                                                                             
             store guard                                                                        st.global.f32 [%rd6], %f15;           W += rd 6 − out, 𝑓15 tid=0

(a) Depiction of how thread bundles split and exit as symbolic execution                        (b) Abridged PTX of the same kernel, annotated with the symbolic
proceeds. Branching on predicates causes the bundle to split.                                   register values.

                                       Figure 5. Running Execute on the kernel in the running example.

all bundles have reached the barrier. At that point, the ex-                                  r1 = 𝛼 tid is
isting shared memory content is updated with the pending                                                      (
writes, and the pending writes are cleared. One situation                                                      𝛼 tid+𝑐    if (tid mod 32) + 𝑐 < 32
                                                                                                         r2 =
complicates this: a buggy program may race, reading shared                                                     𝛼 tid      otherwise
memory over a pending write. However, not every read with                                     However, this rests on the faulty assumption that every lane
pending writes is a race, since a thread may be reading a                                     of the warp is in the same thread bundle. After a split on tid,
value it wrote itself (which can never race, by program or-                                   lanes 0–15 and lanes 16–31 may be held by different logical
der). To solve this, we use an SMT solver to check for overlap                                threads with different expressions for r1, making the above
between pending read and write sets at each barrier. Dirigo                                   expression incorrect. Instead, we treat intra-warp primitives
also performs out-of-bounds access checks for shared and                                      as a barrier, waiting for all threads to arrive before resolving
global memory.                                                                                r2 for each lane.
                                                                                                 We compute r2 as follows: let a reader have partner lane
                                                                                              𝜋 (tid), and for each member 𝑆 of the group we form the
                                                                                              predicate valid 𝑆 (𝜋 (tid)) over the reader’s tid obtained by
                                                                                              substituting 𝜋 (tid) into 𝑆’s domain, and keep 𝑆 when that
3.3.4 Intra-Warp Reduction. The shared memory exam-
                                                                                              guard is satisfiable together with the reader’s domain. The
ple shows one way to perform a block-wide reduction, but
                                                                                              valid members become the arms of a conditional expres-
reducing across 32 or fewer threads is faster with intra-warp
                                                                                              sion, each substituting 𝜋 (tid) into that member’s value of
primitives, intrinsics that let threads in a warp communicate
                                                                                              the source register. Writing 𝛼 𝑆 for the value of r1 held by
without shared memory. A common example is shfl.down,
                                                                                              member 𝑆, the example above with 𝑐 = 16 becomes
which lets each thread read a value from another thread a
                                                                                                                     𝑆0
fixed offset away. The following snippet from the running                                                      
                                                                                                               
                                                                                                                𝛼 tid    if (tid mod 32) + 16 ≥ 32
example sums a value among 32 threads:
                                                                                                                    𝑆1
                                                                                                               𝛼 tid+16 if valid 𝑆1 (tid + 16)
                                                                                                               
                                                                                                               
                                                                                                               
                                                                                                        r2 = 𝑆2
   float val = sdata[tid];                                                                                     
                                                                                                                𝛼 tid+16 if valid 𝑆2 (tid + 16)
   for (int offset = 16; offset > 0; offset /= 2) {                                                            
                                                                                                                ...      ..
                                                                                                               
                                                                                                               
     val += __shfl_down_sync(0xffffffff, val, offset);                                                                    .
   }
                                                                                              where 𝑆 0 is the reader itself. This is the fully general form, but
On each iteration, each thread reads a value from another                                     in practice Dirigo detects when a warp is entirely contained
thread in the warp and adds it to its own. By the CUDA                                        in one bundle and uses the simpler formula above.
specification, a thread reading from a lane outside the warp                                     Finally, an intra-warp primitive may read from an exited
instead reads its own value. Therefore, an implementation                                     thread, or from a thread beyond the end of the block when the
of shfl.down r2, r1, 𝑐 in the symbolic executor with                                          block size is not a multiple of 32. This is not itself an error and
                                                                                     6
The Output-Space Hypothesis: Enumerative Equivalence Checking for Tensor Programs


produces an undefined value, modeled as ⊥, but if it reaches              produces a set of symbolic writes (𝜙, 𝑎, 𝑣): under path con-
an observable sink—a memory write, a memory address,                      dition 𝜙 (tid, bid), a thread writes the value 𝑣 (tid, bid) to the
or a branch predicate—we flag a bug. Figure 5b annotates                  address 𝑎(tid, bid). To obtain 𝑓𝑘 (ℓ) we invert the write: we
some of the running example’s PTX with the symbolic values                find the (tid, bid) satisfying 𝑎(tid, bid) = ℓ ∧ 𝜙 (tid, bid) and
produced by Execute, ending in the predicated write that                  substitute it into 𝑣. Since ℓ is concrete and 𝑎 is affine in tid
only the bundle holding tid = 0 performs.                                 and bid for the kernels we encounter, this is a small integer
                                                                          problem.
3.3.5 Torch Operations. Unlike kernels, which we must                     Back-projection. A concrete output location is resolved
consider at the PTX level, Torch operations have a pre-                   to an expression over the inputs alone by substituting per-
defined mapping to symbolic expressions.                                  element equations backwards through the program:

3.4   Check                                                                          res(𝑥 [ℓ]) = 𝑥 [ℓ]
                                                                                    res(𝑇𝑘 [ℓ]) = 𝑓𝑘 (ℓ) 𝑇 𝑗 [ℓ ′ ] ↦→ res(𝑇 𝑗 [ℓ ′ ])
                                                                                                                                      
After Execute, every operation in both programs has a sym-
bolic description, which we must turn into equivalence condi-
                                                                          where 𝑥 ranges over input tensors and the substitution is
tions a solver can find counterexamples to. Ideally we would
                                                                          applied to every element 𝑇 𝑗 [ℓ ′ ] occurring in 𝑓𝑘 (ℓ). Every
generate one formula per program capturing its full behavior
                                                                          ℓ ′ that appears is itself concrete, so the recursion touches
and ask the solver whether the two agree over entire output
                                                                          finitely many elements and terminates by the SSA ordering.
tensors. But such formulas are dominated by conditionals on
                                                                          Applying res to 𝑦 [ℓ] in each program yields 𝑒𝐴 and 𝑒𝐵 , two
thread indices and bit-vector address arithmetic, on which
                                                                          expressions over the same input variables (Figure 6).
SMT solvers like Z3 [13] either time out or return unknown.
                                                                          Solving. The solver checks 𝑒𝐴 ≠𝑒𝐵 . An unsat result means
Instead, Check takes advantage of the Output-Space Hy-
                                                                          the location is equivalent: ∀¯       ¯ [ℓ] = 𝐵(𝑥)
                                                                                                         𝑥 . 𝐴(𝑥)        ¯ [ℓ] holds up
pothesis to reduce the problem to equivalence at a single
                                                                          to our modeling assumptions. A sat result yields a witness
output location.
                                                                          𝑥¯∗ , a concrete input where the programs disagree at ℓ.
Flipping the quantifiers. Let 𝐴 and 𝐵 be the two programs
                                                                          Enumeration and budgets. Repeating this process for every
(the optimized and reference programs, respectively), 𝑥¯ their
                                                                          ℓ ∈ dom(𝑦) discharges the outer quantifier and verifies the
(shared) input tensors, and 𝑦 an output tensor with index
                                                                          programs in full, up to our modeling assumptions. However,
domain dom(𝑦), and write 𝐴(𝑥)  ¯ [ℓ] for the value 𝐴 stores at
                                                                          this is not always pragmatic. The Output-Space Hypothesis
location ℓ ∈ dom(𝑦). Equivalence is the statement
                                                                          says we should expect to find a bug, if one exists, after only
                                                                          a few locations. So where fast iteration matters, it is more
            ∀ℓ ∈ dom(𝑦). ∀¯     ¯ [ℓ] = 𝐵(𝑥)
                          𝑥 . 𝐴(𝑥)        ¯ [ℓ].
                                                                          useful to set a time budget and check as many locations as
Differential testing fixes an input 𝑥¯ and checks every ℓ con-            possible within it. This lets a human kernel author iterate
cretely. Check does the opposite: it fixes a concrete ℓ and asks          quickly (running Dirigo on each compilation) and an agen-
a solver to decide the inner formula ∀¯          ¯ [ℓ] = 𝐵(𝑥)
                                           𝑥 . 𝐴(𝑥)        ¯ [ℓ]          tic system spend its limited compute budget effectively. A
symbolically. This is what makes the query tractable. With ℓ              budget therefore adds a third outcome, unknown, when it is
concrete and shapes static, every index computation, thread-              exhausted before the solver has checked at least 𝑛 locations
index conditional, and bit-vector operation evaluates to a                (in practice, we set 𝑛 = 5). Finally, budgeted checking im-
constant, since memory access and control flow are data-                  proves further with a good order for checking locations. This
independent by assumption. What remains is a quantifier-                  heuristic can be quite rich, incorporating path conditions
free formula over real arithmetic and uninterpreted functions             gathered during symbolic execution to catch pathological
(one per transcendental, e.g. tanh), with conditionals only               bugs that occur at only a few locations; we defer discussing
for data-dependent operations like max and clamping, which                it to § 4.3.
is much easier for Z3 to solve.
Per-element equations. After Merge, each program is a                     4     Implementation
sequence of operations op1, . . . , op𝑚 in SSA form. For simplic-         We now discuss Dirigo implementation details that matter
ity, assume op𝑘 writes exactly one tensor 𝑇𝑘 and reads only               for effectiveness in practice.
input tensors and tensors 𝑇 𝑗 with 𝑗 < 𝑘. We treat every ten-
sor element 𝑇 [ℓ] as a distinct symbolic variable. Abstractly,            4.1   PTX-Level Transcendental Rollup
Execute produces a per-element equation for each opera-                   Like most GPU compilers, the CUDA compiler nvcc does
tion: a function 𝑓𝑘 mapping a concrete location ℓ ∈ dom(𝑇𝑘 )              not compute exact results for transcendental functions like
to a symbolic expression over elements of earlier tensors,                tanh and log, which activation functions commonly use. In-
such that 𝑇𝑘 [ℓ] = 𝑓𝑘 (ℓ). For Torch operations, 𝑓𝑘 is given              stead it emits an approximation: a polynomial, or a piecewise
directly by the lowering of § 3.3; in the running example,                method that chooses between two approximations based on
𝑓add (𝑛, 𝑐, 𝑤) = 𝐺 [𝑛, 𝑤] + 𝑏 [𝑐]. For kernels, Execute instead           the magnitude of the input. This is problematic for Dirigo:
                                                                      7
                                                                                                               Paul Biberstein, Joseph Devietti, and Mayur Naik


                                                       program A: optimized                                                program B: reference
                     𝑤 (64 columns)
                                                          ℓ = 𝑌 [11, 5, 12]                                                  ℓ = 𝑌 [11, 5, 12]

                                      aten::add 𝑌 [𝑛, 𝑐, 𝑤 ] = 𝐺 [𝑛, 𝑤 ] + 𝑏 [𝑐 ]                        aten::add 𝑌 [𝑛, 𝑐, 𝑤 ] = 𝐺 [𝑛, 𝑤 ] + 𝑏 [𝑐 ]
                                                         𝐺 [11, 12] + 𝑏 [5]                                                 𝐺 [11, 12] + 𝑏 [5]
                                      aten::gelu 𝐺 [𝑛, 𝑤 ] = gelu(𝑆 [𝑛, 𝑤 ] )                            aten::gelu 𝐺 [𝑛, 𝑤 ] = gelu(𝑆 [𝑛, 𝑤 ] )
                                                                                                                     gelu(𝑆 [11, 12] ) + 𝑏 [5]
                                                      gelu(𝑆 [11, 12] ) + 𝑏 [5]
      𝑛 (128 rows)




                                                                                                                              Í
                                                                                                         aten::sum 𝑆 [𝑛, 𝑤 ] = ℎ<64 𝑅 [𝑛, ℎ, 𝑤 ]
                                      fused_min_sum_kernel                                                            Í                   
                                                                                                                gelu ℎ<64 𝑅 [11, ℎ, 12] + 𝑏 [5]
                                      𝑆 [bid 𝑥 , bid 𝑦 ] = ℎ<32 min𝑐 ′ 𝑀 [bid 𝑥 , 𝑐 ′ , ℎ, bid 𝑦 ]
                                                          Í
                                                                                                         aten::min 𝑅 [𝑛, ℎ, 𝑤 ] = min𝑐 ′ 𝑀 [𝑛, 𝑐 ′ , ℎ, 𝑤 ]
                                                  reads 𝑀 [11, 𝑐 ′ , ℎ, 12], ℎ < 32
                                                                                                                     reads 𝑀 [11, 𝑐 ′ , ℎ, 12], ℎ < 64
                                                         𝑀 (source tensor)                                                  𝑀 (source tensor)


                                                                                                               ′
                                                                                      Í                                
                                                                        𝑒𝐴 = gelu        ℎ< 32 min𝑐 ′ 𝑀 [11, 𝑐 , ℎ, 12] + 𝑏 [5]
                                                                                                               ′ , ℎ, 12] + 𝑏 [5]
                                                                                      Í                                  
                                                                        𝑒𝐵 = gelu        ℎ< 64 min𝑐 ′ 𝑀 [11, 𝑐
                                                                         check 𝑒𝐴 = 𝑒𝐵 for all 𝑀, 𝑏


Figure 6. Illustration of the Check phase generating equivalence conditions for the running example. A heuristic searches
concrete output locations, here ℓ = 𝑌 [11, 5, 12] (left), and walks both programs backwards from ℓ using Execute results to
specialize each block’s symbolic equation to the chosen location (right). An SMT solver searches for counterexamples to
equivalence of the two resulting expressions.

it creates data-dependent control flow where none existed                             Approximation equivalences are approximations that can
and obscures the source program’s mathematical meaning.                            optionally be marked as equivalent to enable a more permis-
To solve this, Dirigo pre-processes the PTX code to rec-                           sive notion of program equivalence. The AI CUDA Engineer
ognize nvcc approximation idioms and convert them to a                             dataset needs only one: geluerf = gelutanh , which equates
single pseudo-instruction that represents the mathematical                         the tanh approximation of GELU with the exact erf-based
function called in the source. In practice, this is not too chal-                  GELU. Similarly, we can optionally assume that fast-math
lenging: in the entire AI CUDA Engineer dataset, the only                          variants are equivalent to their non-fast-math counterparts.
transcendental functions are exp, log, log1p, tanh, erf, and                       Unless otherwise specified, evaluations of Dirigo assume
pow. Including fast math variants, Dirigo needs only eleven                        both these equivalences are enabled.
pattern matchers to handle these.
                                                                                   4.3     Search Heuristic
                                                                                   Instead of exploring output locations randomly, the white-
4.2           Transcendental Approximation Axioms                                  box nature of Dirigo’s symbolic execution, combined with
                                                                                   priors about where bugs manifest in deep learning kernels,
Commonly, a programmer might optimize a tensor program
                                                                                   allows for richer heuristics. From the path conditions that
by replacing a slower, more mathematically precise transcen-
                                                                                   Execute produced (each of which has its own symbolic write
dental function implementation with a faster, less accurate
                                                                                   address and value), we rank a prefix of candidate locations
approximation. Dirigo includes a pluggable set of axioms
                                                                                   in three tiers:
that can be applied to the equivalence-checking phase to al-
low the user to specify which approximations are acceptable.                             1. Corners. For every kernel launch, the locations writ-
We distinguish two kinds of rules.                                                          ten by the first and last thread of the first and last
   Sound identities are two implementations of a single math-                               block, (tid, bid) ∈ {0, 𝑡−1} × {0, 𝑏−1}, as well as the
ematical function and are always on. They are needed be-                                    warp-boundary lanes tid ∈ {31, 32} of block 0, where
cause Torch operations and kernels produce different sym-                                   warp-reductions might contain bugs. Later kernels are
bolic expressions for activation functions: for example, ker-                               ranked above earlier kernels.
nels would produce 1/(1 + 𝑒 −𝑥 ) to represent sigmoid, and                               2. Path-condition coverage. For each unique thread
Torch operations would produce an uninterpreted function                                    bundle write not already covered by corner check-
sigmoid. Dirigo runs a pass over both final expressions to                                  ing, we use Z3 to find a satisfying assignment of tid
normalize uninterpreted functions to a common vocabulary.                                   and bid that falls within that write’s path condition.
                                                                              8
The Output-Space Hypothesis: Enumerative Equivalence Checking for Tensor Programs

                                                                                                 (a) distinct kernels per program                 (b) source lines per program
         This ensures coverage of piecewise behavior that only




                                                                                                                             % of programs
                                                                                           6k         5,431                                  30
         exists in small portions of the output tensor.                                                                                                          median 92




                                                                          programs
      3. Tensor boundaries. The first and last element of                                  4k                                                20
         every output tensor.                                                              2k                                                10
                                                                                                 89       451 238 93 10 55
                                                                                            0                                                0
After these, we fall back to a random permutation of the                                             0 1 2 3 4 5 6+                               0    100       200        300
unchecked locations. We evaluate this heuristic against a
                                                                                                 (c) thread bundles per kernel                          (d) programs using . . .
baseline sequential order in § 5.3.
                                                                                           60




                                                                            % of kernels
                                                                                                                           shared memory                                 2,630
                                                                                           40                                 warp shuffle                       1,206
4.4    Parallelization
                                                                                           20                                      atomics                 236
Dirigo’s structure exposes natural parallelism: Execute                                                                >32       torch ops                          1,778
                                                                                            0
analyzes trace operations independently, so symbolic ex-                                         1       11    21     31                               0     1k 2k 3k
ecution can be parallelized across operations, and Check                                                                                                     programs
analyzes output locations independently, so checking can
be parallelized across locations. We evaluate the effect of                           Figure 7. Statistics about the programs in our dataset.
location-level parallelism on Dirigo’s ability to fully check
all locations for equivalence in § 5.5.
                                                                          RQ4: Can Dirigo fully verify kernels by checking all loca-
4.5    Modeling Gaps and Limitations                                      tions?
Dirigo models floating point values as reals, a common
abstraction used with SMT solvers [14]. This masks floating-              5.1                   Setup
point behavior like non-associativity, and means that Dirigo              We evaluate Dirigo on the AI CUDA Engineer dataset, one of
cannot find bugs that manifest through insufficient precision.            the only large, public collections of optimized KernelBench
Supporting floating-point arithmetic is beyond the scope of               implementations. We focus on KernelBench level-2, since
this work but an interesting open problem: work on hard-                  it has the complexity of multiple operators (unlike level-1)
ening KernelBench shows that global absolute and relative                 while still having many tasks (unlike level-3). KernelBench
tolerances cannot separate acceptable approximation from                  level-2 programs consist of 3-6 Torch operators and the AI
numerical error [20, 28].                                                 CUDA Engineer dataset versions are C++ functions calling
   Dirigo only models a subset of PTX instructions. That                  Torch functions and custom CUDA kernels. Since we seek
subset is enough to run the majority of the AI CUDA En-                   bugs that differential testing misses, we consider only the
gineer dataset programs, but with more engineering effort                 6,988 AI CUDA Engineer dataset programs it marks correct.
we could incorporate the remaining missing operators like                 All experiments ran on a workstation with two Intel Xeon
__syncwarp and __ballot_sync into Dirigo’s design.                        Gold 6248 CPUs (20 physical cores each), 754 GB of DRAM,
                                                                          and NVIDIA GeForce RTX 2080 Ti GPUs (11 GB) with CUDA
4.6    Counterexample Verification                                        12.5 and driver 555.42.02. Unless otherwise noted, Dirigo
When Dirigo finds an inequivalence, it appends constraints                runs with a 2 minute timeout on Execute and a 4 minute
to the SMT query to find a counterexample that produces                   timeout on Check. An overview of the dataset’s key fea-
large differences between the two programs, and uses Py-                  tures is in Figure 7. Note that most programs have a single
Torch’s auto-differentiation to invert witnesses back through             kernel, are approximately 100 lines, exhibit very little thread-
any prefix operations Merge trimmed. This allows us to con-               splitting, and use shared memory and at least one torch
firm the counterexample on the real programs, avoiding any                operation.
modeling limitations.
                                                                          5.2 RQ1: Does the Output-Space Hypothesis discover
5     Evaluation                                                              more bugs?
We evaluate both the validity of the Output-Space Hypoth-                 To gauge the validity of the Output-Space Hypothesis, we
esis and its effectiveness (via Dirigo) as a practical bug-               run Dirigo across the 6,988 AI CUDA Engineer dataset level-
finding tool by answering the following questions:                        2 kernels that differential testing marks correct. Over these
RQ1: Does searching across output locations instead of input              programs, Dirigo reports four outcomes:
values discover more bugs?                                                                 • Buggy (600, 8.6%). Which shows that differential test-
RQ2: Among buggy kernels, how many locations do bugs                                         ing alone is not enough.
appear at?                                                                                 • Checked Locations Correct (3,341). Every output
RQ3: Among buggy kernels, how quickly does output loca-                                      location Dirigo reached within its budget was proved
tion search discover the bugs?                                                               equivalent to the reference, with at least 5 locations
                                                                      9
                                                                                                                                Paul Biberstein, Joseph Devietti, and Mayur Naik


Table 1. The 600 bugs Dirigo reports in the AI CUDA Engi-                                                                heuristic order




                                                                                buggy programs
                                                                                                                                                                                     213 213
neer dataset by category. “Programs” counts dataset entries,                                                             sequential order
                                                                                                 100
“Sanitizer” entries on which compute-sanitizer reports an
error/warning, and “Tasks” distinct KernelBench tasks.                                            10                                                                             65
                                                                                                                                                4
                                                                                                               2
                                                                                                   1                                                      1
Defect                                        Programs Sanitizer Tasks                                             0                                 0        0

Synchronization (Execute)                                                                                  0       .01     .1        .2   .3   .4     .5      .6   .7    .8     .9   .99    1
  Cross-warp shared-memory race                    131      131    26                                          fraction of output locations that reveal the Check bug
  Warp-synchronous programming                      80       80    27
  Barrier under divergent control flow               9        9     1         Figure 8. The 226 programs with a bug found by Check
Warp shuffle (Execute)                                                        organized by how prevalent the bug is with sequential versus
 Full mask under a predicated warp                  67       11    24         our heuristic search.
 Shuffle partner outside the block                   6        3     1
Memory safety (Execute)
                                                                                                 600                                                                      all bugs (600)
 Global OOB: shape or layout mismatch               56       56     6




                                                                               bugs found
 Global OOB: boundary off-by-one                    11        1     8                                                                                                    Execute (374)
                                                                                                 400
 Uninitialized shared-memory read                   14        1     5
                                                                                                                                                                              Check (226)
Wrong computation (Check)                                                                        200
 Dropped, added, or reordered op                   135        0     3
 Wrong math function or constant                    12        0     4                             0
                                                                                                       0                        60                  120                 180                240
 Wrong layout, thread mapping, or reduction         79        3     6
                                                                                                                                           time to bug (s)
Total                                              600      295    68
                                                                              Figure 9. The number of bugs found versus wall-clock time
                                                                              thresholds, counted from the start of Trace (compilation
      checked. While this is evidence of correctness, it is                   excluded).
      not a guarantee.
    • Timeout (1,175). The 120 s Execute or 240 s Check                       Dirigo catches many low-level safety bugs that the sanitizers
      budget expired before a verdict.                                        miss, in addition to higher-level bugs outside their scope.
    • Unsupported (1,872). Programs that either violate
      Dirigo’s assumptions or use features absent from our                    5.3                RQ2: Are bugs dense in output-space?
      prototype, such as __syncwarp.                                          Of the 600 bugs we find, we filter to the 226 found at the
A taxonomy of the types of bugs found is shown in Table 1.                    per-location checking stage rather than during symbolic ex-
374 are reported by Execute as violations of the CUDA pro-                    ecution, and ask how many output locations reveal each bug.
gramming model (shared-memory races, shuffles whose part-                     For each, we check locations in random order for 600 s and
ner lane has exited, out-of-bounds and uninitialized reads),                  extrapolate the fraction that differ to the total number of
and 226 by Check as inequivalences, which are proved with                     buggy locations. The results are shown in Figure 8. In all but
a concrete witness that is replayed on the original program                   13 cases, the bugs are present at every location sampled. Con-
and produces differences well above tolerances. Requiring                     sistent with this, 218 of the 226 bugs are exposed by the very
a verified counterexample for every reported bug makes                        first location Dirigo samples. This provides strong empirical
Dirigo complete (it only reports real bugs) at the cost of                    evidence of the validity of the Output-Space Hypothesis on
soundness (it may miss bugs when no convincing counterex-                     this dataset. Further, the two bugs with the lowest preva-
ample is found). When Check finds a bug with no verifiable                    lences (0.003 and 0.001) were found by the heuristic search
counterexample, Dirigo cannot tell whether the refinement                     after 32 and 1,289 locations respectively, whereas the se-
heuristic simply failed, or the inequivalence is spurious and                 quential order checked 668 and 9,083 locations of the same
exposes a gap in Dirigo’s modeling assumptions. On the AI                     programs without reaching either bug.
CUDA Engineer dataset, Dirigo produces 221 such unverifi-
able inequivalence results (over 32 tasks).                                   5.4                RQ3: Is output-space search wall-clock efficient?
   Note that the counts are dominated by certain tasks: the                   While confidence that bugs are dense in output-space is
AI CUDA Engineer dataset contains many near-duplicate                         useful, we also want to know whether Dirigo can sit inside
optimizations of each task, so the 600 buggy programs span                    a developer’s loop as an interactive bug-finder. Across the
68 of the 100 level-2 tasks, and we report both.                              600 faulty programs, we track the time from the start of
   For each bug category, Table 1 also shows how many                         Trace to the bug report. The results are shown in Figure 9.
of those bugs were caught by Nvidia’s compute-sanitizer.                      93.2% of bugs are found within the first minute and 97.3%
                                                                         10
The Output-Space Hypothesis: Enumerative Equivalence Checking for Tensor Programs


                                                                                                even one thread block of the last kernel commonly requires
  programs (cumulative, %)
                             100
                                    projected from 120 s                                        many thread blocks of the prior kernel, as with reductions
                              75    measured, full check
                                                                                                that collapse many inputs to one output.
                              50                                58 % of programs                   Despite this, we explore what applying Volta to the AI
                                                                projected under 1 h             CUDA Engineer dataset might look like. The smallest change
                              25                                                                would be support for checking kernels against individual
                              0                                                                 PyTorch operations, similar to the kernel-to-kernel checking
                                   1s         1 min        1h        1d      1 mo     1y        Volta already supports. With it, one could check the subset
                                        time to check every output location (40 workers)        of the AI CUDA Engineer dataset where the agent optimizes
                                                                                                each reference PyTorch operation into its own kernel: ap-
Figure 10. The share of programs with no bugs found for                                         proximately 242 entries out of 6,988. Volta is not open source,
which Dirigo can check every output location within a given                                     so unfortunately we cannot run it on those entries.
wall-clock time.
                                                                                                6   Related Work
within two, evidence that Dirigo could be used interactively.                                   A large body of work verifies CPU programs via symbolic
Execute completes quickly, so those bugs are found early,                                       execution and SMT solving, but for brevity we limit our
whereas Check continues indefinitely and finds a long tail.                                     discussion to techniques targeting GPU programs.
The time to a bug is dominated by Trace, which adds a                                              Work on GPU equivalence-checking is most similar to
median of 18 s per program (the reference and optimized                                         Dirigo: it establishes the correctness of an optimized GPU
programs are traced concurrently). Counting only the search                                     kernel by showing equivalence to a trusted baseline. Differ-
itself, the median time to a bug is 1.9 s and 95.7% of bugs are                                 ential testing is the basic but popular approach, though it
found within a minute. Execute is cheap for most programs,                                      samples very sparsely from a large input space and misses
with a median of 0.6 s and 10 s at the 90th percentile.                                         many bugs. Volta [14], which we compare to in § 5.6, adopts
                                                                                                a more principled approach and uses SMT solving to prove
5.5                          RQ4: Is full verification of programs feasible?                    equivalence, though it requires the baseline kernel be written
We measure Dirigo over a 120 s window with 40 threads                                           in CUDA and does not support kernel fusion. ProofWright
and extrapolate to find the latency of full verification of all                                 [8] can prove equivalence between PyTorch and CUDA code
output locations. To check these numbers, we also run full                                      via LLM-written Rocq proofs, but currently only produces
verification for every program estimated to take under 60                                       proofs for a subset of KernelBench level-1 kernels. Likewise
minutes. The results are presented in Figure 10. While 58%                                      Kuiper, a verified GPU programming framework [26], has
are projected to be fully verifiable in under 60 minutes, full                                  implemented KernelBench level-1 kernels [27]. These ap-
verification is generally hard: some kernels are estimated at                                   proaches require the kernel to be written or proved in a
up to 61,440 hours (7.0 years). The extrapolation is generally                                  proof assistant, whereas Dirigo checks existing, unanno-
accurate, with a median ratio of predicted-to-actual of 1.03.                                   tated CUDA against the PyTorch reference directly.
                                                                                                   GPU symbolic execution systems [11, 12, 15, 22, 32] de-
5.6                          Comparison to Volta                                                tect a variety of correctness and performance bugs. Dirigo
                                                                                                uses symbolic execution not only for bug detection but also
Volta [14], a system for automated kernel equivalence-checking,
                                                                                                to enable equivalence-checking. Dirigo’s per-location con-
is the most similar work to Dirigo: both use symbolic execu-
                                                                                                cretization step (§ 3.4) in particular takes inspiration from
tion to accumulate equivalence conditions as SMT formulas
                                                                                                concolic execution systems [16, 22].
passed to Z3. However, its limitations inhibit applicability
                                                                                                   Many GPU static analyses [1–3, 9, 10, 21, 30] detect data
to tasks like KernelBench. Volta only supports what it terms
                                                                                                races, barrier divergence and other GPU correctness and
“Structured CTA” kernels, limited to data-independent con-
                                                                                                performance bugs. The state-of-the-art FaialAA system [25]
trol flow and memory access, constraints Dirigo shares.
                                                                                                verifies that a kernel is DRF and identifies any data races it
Volta is also restricted to checking two CUDA kernels against
                                                                                                contains, so long as the kernel is control-independent (CI)
each other, and cannot check a kernel against a PyTorch
                                                                                                and data-independent (DI). Such CIDI kernels are similar
operator. Additionally, Volta requires the baseline and op-
                                                                                                to the kernels that Dirigo supports, as they both lack data-
timized kernels to have identical grids, and compares one
                                                                                                dependent control flow and indirect memory accesses.
CTA (thread block) in the baseline to the corresponding CTA
in the optimized kernel, checking that the output locations
written by each CTA are equivalent. Checking one CTA’s                                          7   Conclusion
outputs is consistent with the Output-Space Hypothesis, but                                     We have presented the Output-Space Hypothesis and used
requiring CTA alignment precludes changing grid dimen-                                          Dirigo to validate it on a large corpus of optimized deep
sions and kernel fusion. In multi-kernel programs, analyzing                                    learning kernels. Moreover, while many kernel bugs are
                                                                                           11
                                                                                                             Paul Biberstein, Joseph Devietti, and Mayur Naik


simple safety violations, there is a long tail of complicated                       [11] Peter Collingbourne, Cristian Cadar, and Paul H.J. Kelly. 2014. Sym-
correctness violations that differential testing struggles to                            bolic Crosschecking of Data-Parallel Floating-Point Code. IEEE Trans-
catch. Dirigo provides rich feedback and finds bugs quickly,                             actions on Software Engineering 40, 7 (2014), 710–737. doi:10.1109/TSE.
                                                                                         2013.2297120
accelerating both human and agentic kernel authors.                                 [12] Peter Collingbourne, Cristian Cadar, and Paul H. J. Kelly. 2012. Sym-
                                                                                         bolic Testing of OpenCL Code. In Hardware and Software: Verification
References                                                                               and Testing (Lecture Notes in Computer Science), Kerstin Eder, João
                                                                                         Lourenço, and Onn Shehory (Eds.). Springer Berlin Heidelberg, Berlin,
 [1] Rajeev Alur, Joseph Devietti, Omar S. Navarro Leija, and Nimit Sing-                Heidelberg, 203–218. doi:10.1007/978-3-642-34188-5_18
     hania. 2017. GPUDrano: Detecting Uncoalesced Accesses in GPU                   [13] Leonardo de Moura and Nikolaj Bjørner. 2008. Z3: An Efficient SMT
     Programs. In Computer Aided Verification (CAV) (Lecture Notes in                    Solver. In Tools and Algorithms for the Construction and Analysis of Sys-
     Computer Science). Springer International Publishing, Cham, 507–525.                tems (Lecture Notes in Computer Science). Springer Berlin Heidelberg,
     doi:10.1007/978-3-319-63387-9_25                                                    Berlin, Heidelberg, 337–340. doi:10.1007/978-3-540-78800-3_24
 [2] Rajeev Alur, Joseph Devietti, Omar S. Navarro Leija, and Nimit Singha-         [14] Benjamin Driscoll, Kshitij Dubey, Anjiang Wei, Neeraj Kayal, Rahul
     nia. 2022. Static Detection of Uncoalesced Accesses in GPU Programs.                Sharma, and Alex Aiken. 2025. Equivalence Checking of ML GPU
     Formal Methods in System Design 60, 1 (2022), 1–32. doi:10.1007/s10703-             Kernels. arXiv:2511.12638 [cs.PL] v3, August 2026.
     021-00362-8                                                                    [15] Naila Farooqui, Karsten Schwan, and Sudhakar Yalamanchili. 2014.
 [3] Rajeev Alur, Joseph Devietti, and Nimit Singhania. 2018. Block-Size
                                                                                         Efficient Instrumentation of GPGPU Applications Using Information
     Independence for GPU Programs. In Static Analysis Symposium (SAS)                   Flow Analysis and Symbolic Execution. In Proceedings of Workshop
     (Lecture Notes in Computer Science). Springer International Publishing,             on General Purpose Processing Using GPUs (Salt Lake City, UT, USA)
     Cham, 107–126. doi:10.1007/978-3-319-99725-4_9                                      (GPGPU-7). Association for Computing Machinery, New York, NY,
 [4] Jason Ansel, Edward Yang, Horace He, Natalia Gimelshein, Animesh                    USA, 19–27. doi:10.1145/2588768.2576782
     Jain, Michael Voznesensky, Bin Bao, Peter Bell, David Berard, Evgeni           [16] Patrice Godefroid, Nils Klarlund, and Koushik Sen. 2005. DART: di-
     Burovski, Geeta Chauhan, Anjali Chourdia, Will Constable, Alban                     rected automated random testing. In Proceedings of the 2005 ACM
     Desmaison, Zachary DeVito, Elias Ellison, Will Feng, Jiong Gong,                    SIGPLAN Conference on Programming Language Design and Implemen-
     Michael Gschwind, Brian Hirsh, Sherlock Huang, Kshiteej Kalam-                      tation (Chicago, IL, USA) (PLDI ’05). Association for Computing Ma-
     barkar, Laurent Kirsch, Michael Lazos, Mario Lezcano, Yanbo Liang,                  chinery, New York, NY, USA, 213–223. doi:10.1145/1065010.1065036
     Jason Liang, Yinghai Lu, C. K. Luk, Bert Maher, Yunjie Pan, Christian          [17] Dan Hendrycks and Kevin Gimpel. 2016. Gaussian Error Linear Units
     Puhrsch, Matthias Reso, Mark Saroufim, Marcos Yukio Siraichi, Helen                 (GELUs). arXiv:1606.08415 [cs.LG]
     Suk, Shunting Zhang, Michael Suo, Phil Tillet, Xu Zhao, Eikan Wang,            [18] Charles Hong, Sahil Bhatia, Alvin Cheung, and Yakun Sophia Shao.
     Keren Zhou, Richard Zou, Xiaodong Wang, Ajit Mathews, William                       2025. Autocomp: A Powerful and Portable Code Optimizer for Tensor
     Wen, Gregory Chanan, Peng Wu, and Soumith Chintala. 2024. Py-                       Accelerators. arXiv:2505.18574 [cs.PL] https://arxiv.org/abs/2505.
     Torch 2: Faster Machine Learning Through Dynamic Python Bytecode                    18574
     Transformation and Graph Compilation. In Proceedings of the 29th               [19] Robert Tjarko Lange, Aaditya Prasad, Qi Sun, Maxence Faldor, Yujin
     ACM International Conference on Architectural Support for Program-                  Tang, and David Ha. 2025. The AI CUDA Engineer: Agentic CUDA Ker-
     ming Languages and Operating Systems, Volume 2 (La Jolla, CA, USA)                  nel Discovery, Optimization and Composition. https://huggingface.co/
     (ASPLOS ’24). Association for Computing Machinery, New York, NY,                    datasets/SakanaAI/AI-CUDA-Engineer-Archive. Sakana AI technical
     USA, 929–947. doi:10.1145/3620665.3640366                                           report and kernel archive.
 [5] Carlo Baronio, Pietro Marsella, Ben Pan, Simon Guo, and Silas Al-              [20] Robert Tjarko Lange, Qi Sun, Aaditya Prasad, Maxence Fal-
     berti. 2025. Kevin: Multi-Turn RL for Generating CUDA Kernels.                      dor, Yujin Tang, and David Ha. 2025. Towards Robust Agen-
     arXiv:2507.11948 [cs.LG]                                                            tic CUDA Kernel Benchmarking, Verification, and Optimization.
 [6] Adam Betts, Nathan Chong, Alastair F. Donaldson, Shaz Qadeer, and                   arXiv:2509.14279 [cs.SE]
     Paul Thomson. 2012. GPUVerify: A Verifier for GPU Kernels. In
                                                                                    [21] Guodong Li and Ganesh Gopalakrishnan. 2010. Scalable SMT-based
     Proceedings of the ACM International Conference on Object Oriented                  verification of GPU kernel functions. In Proceedings of the Eighteenth
     Programming Systems Languages and Applications (Tucson, Arizona,                    ACM SIGSOFT International Symposium on Foundations of Software
     USA). Association for Computing Machinery, New York, NY, USA,                       Engineering (Santa Fe, New Mexico, USA) (FSE ’10). Association for
     113–132. doi:10.1145/2384616.2384625                                                Computing Machinery, New York, NY, USA, 187–196. doi:10.1145/
 [7] James Bradbury, Roy Frostig, Peter Hawkins, Matthew James Johnson,                  1882291.1882320
     Chris Leary, Dougal Maclaurin, George Necula, Adam Paszke, Jake                [22] Guodong Li, Peng Li, Geof Sawaya, Ganesh Gopalakrishnan, Indradeep
     VanderPlas, Skye Wanderman-Milne, and Qiao Zhang. 2018. JAX:                        Ghosh, and Sreeranga P. Rajan. 2012. GKLEE: Concolic Verification
     composable transformations of Python+NumPy programs. http://                        and Test Generation for GPUs. In Proceedings of the 17th ACM SIGPLAN
     github.com/jax-ml/jax.                                                              Symposium on Principles and Practice of Parallel Programming (New
 [8] Bodhisatwa Chatterjee, Drew Zagieboylo, Sana Damani, Siva Hari,                     Orleans, Louisiana, USA) (PPoPP ’12). Association for Computing Ma-
     and Christos Kozyrakis. 2025. ProofWright: Towards Agentic Formal                   chinery, New York, NY, USA, 215–224. doi:10.1145/2145816.2145844
     Verification of CUDA. arXiv:2511.12294 [cs.SE] https://arxiv.org/abs/          [23] Xiaoya Li, Albert Wang, Guoyin Wang, Jiwei Li, and Chris Shum.
     2511.12294                                                                          2026. CUDA-L1: Improving CUDA Optimization via Contrastive Re-
 [9] Tiago Cogumbreiro, Julien Lange, Dennis Liew, and Hannah Zicarelli.                 inforcement Learning. In Proceedings of the Fourteenth International
     2021. Checking Data-Race Freedom of GPU Kernels, Compositionally.                   Conference on Learning Representations (Rio de Janeiro, Brazil) (ICLR
     In Computer Aided Verification (Lecture Notes in Computer Science),                 ’26). OpenReview.net. arXiv:2507.14111 [cs.AI]
     Alexandra Silva and K. Rustan M. Leino (Eds.). Springer International          [24] Gang Liao, Hongsen Qin, Ying Wang, Alicia Golden, Michael Kuchnik,
     Publishing, Cham, 403–426. doi:10.1007/978-3-030-81685-8_19                         Yavuz Yetim, Jia Jiunn Ang, Chunli Fu, Yihan He, Samuel Hsia, Zewei
[10] Tiago Cogumbreiro, Julien Lange, Dennis Liew, and Hannah Zicarelli.                 Jiang, Dianshi Li, Uladzimir Pashkevich, Varna Puvvada, Feng Shi,
     2024. Memory access protocols: certified data-race freedom for GPU                  Matt Steiner, Ruichao Xiao, Liyuan Li, Nathan Yan, Xiayu Yu, Zhou
     kernels. Formal Methods in System Design 63, 1–3 (2024), 134–171.                   Fang, Roman Levenstein, Kunming Ho, Haishan Zhu, Alec Hammond,
     doi:10.1007/s10703-023-00415-0
                                                                               12
The Output-Space Hypothesis: Enumerative Equivalence Checking for Tensor Programs


     Richard Li, Ajit Mathews, Kaustubh Gondkar, Abdul Zainul-Abedin,            [29] Anne Ouyang, Simon Guo, Simran Arora, Alex L. Zhang, William Hu,
     Ketan Singh, Hongtao Yu, Wenyuan Chi, Barney Huang, Sean Zhang,                  Christopher Ré, and Azalia Mirhoseini. 2025. KernelBench: Can LLMs
     Noah Weller, Zach Marine, Wyatt Cook, Carole-Jean Wu, and Gaox-                  Write Efficient GPU Kernels? arXiv:2502.10517 [cs.LG]
     iang Liu. 2025. KernelEvolve: Scaling Agentic Kernel Coding for             [30] Phillipe Pereira, Higo Albuquerque, Hendrio Marques, Isabela Silva,
     Heterogeneous AI Accelerators at Meta. arXiv:2512.23236 [cs.LG]                  Celso Carvalho, Lucas Cordeiro, Vanessa Santos, and Ricardo Ferreira.
[25] Dennis Liew, Tiago Cogumbreiro, and Julien Lange. 2024. Sound                    2016. Verifying CUDA programs using SMT-based context-bounded
     and Partially-Complete Static Analysis of Data-Races in GPU Pro-                 model checking. In Proceedings of the 31st Annual ACM Symposium on
     grams. Proc. ACM Program. Lang. 8, OOPSLA2, Article 357 (Oct. 2024),             Applied Computing (Pisa, Italy) (SAC ’16). Association for Computing
     28 pages. doi:10.1145/3689797                                                    Machinery, New York, NY, USA, 1648–1653. doi:10.1145/2851613.
[26] Guido Martínez, Bastian Köpcke, Jonáš Fiala, Gabriel Ebner, Tahina               2851830
     Ramananandro, Michel Steuwer, Tyler Sorensen, and Nikhil Swamy.             [31] Tara Saba, Zhiyang Chen, Jikai Jason Li, Anne Ouyang, Xujie Si, and
     2026. Kuiper: Correct and Efficient GPU Programming with Dependent               Fan Long. 2026. CuTeGen: An LLM-Based Agentic Framework for
     Types and Separation Logic. Proc. ACM Program. Lang. 10, PLDI (June              Generation and Optimization of High-Performance GPU Kernels using
     2026), 830–854. doi:10.1145/3808280                                              CuTe. arXiv:2604.01489 [cs.LG]
[27] Guido Martínez and Tyler Sorensen. 2026. The Next Frontier for              [32] Mingyuan Wu, Yicheng Ouyang, Husheng Zhou, Lingming Zhang,
     AI-Generated Kernels: Correctness. In Proceedings of the 2026 ACM                Cong Liu, and Yuqun Zhang. 2020. Simulee: detecting CUDA syn-
     SIGPLAN International Workshop on Principles of Agentic Engineering              chronization bugs via memory-access modeling. In Proceedings of
     (Boulder, CO, USA) (PAgE ’26). Association for Computing Machinery,              the ACM/IEEE 42nd International Conference on Software Engineering
     New York, NY, USA, 25–37. doi:10.1145/3819802.3820580                            (Seoul, South Korea) (ICSE ’20). Association for Computing Machinery,
[28] METR. 2025. Measuring Automated Kernel Engineering. https://metr.                New York, NY, USA, 937–948. doi:10.1145/3377811.3380358
     org/blog/2025-02-14-measuring-automated-kernel-engineering/.




                                                                            13
