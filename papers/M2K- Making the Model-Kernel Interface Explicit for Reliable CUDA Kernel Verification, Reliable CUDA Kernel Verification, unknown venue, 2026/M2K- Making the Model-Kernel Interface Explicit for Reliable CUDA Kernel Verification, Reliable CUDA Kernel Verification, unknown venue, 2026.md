                                          M2K: Making the Model-Kernel Interface Explicit for
                                                 Reliable CUDA Kernel Verification
                                               Mengting He                    Shihao Xia                   Haomin Jia             Wenfei Wu                 Linhai Song
                                                   Penn State                  Penn State                SKLP, ICT, CAS         Peking University           SKLP, ICT, CAS
                                                      USA                         USA                        China                   China                      China
                                         Abstract                                                                  1    Introduction
                                         Large language model (LLM) inference systems rely on CUDA                 The rapid adoption of large language models (LLMs) has
                                         kernels for core GPU computations, yet the interface be-                  driven an explosion of inference workloads across chat-
                                         tween models and kernels is implicit and poorly specified.                bots [1, 2, 16], search [38, 86], recommendation [5, 75, 81],
                                         Models and kernels evolve independently and often make in-                copilots [12, 33, 85], scientific computing [7, 39, 74], and
arXiv:2603.24595v2 [cs.PL] 29 Aug 2026




                                         compatible assumptions about tensor shapes and input sizes,               countless other areas [8, 9, 79]. These services now operate
                                         leading to subtle memory bugs in CUDA kernels. These bugs                 at scale and serve real users, making LLM inference systems
                                         can crash inference services, corrupt model weights, or be                a critical part of modern computing infrastructure.
                                         exploited by remote adversaries. Existing techniques either                  LLM inference systems rely on a layered software archi-
                                         incur prohibitive runtime overhead, require specialized hard-             tecture. Model developers publish Python model files and
                                         ware, or fail to handle dynamic tensor shapes and variable                weights (via Hugging Face [24]), which inference frame-
                                         kernel launch configurations, leaving the CUDA memory                     works (e.g., vLLM [35], SGLang [82], Transformers [25]) load
                                         bugs largely unaddressed.                                                 and execute. These frameworks manage inference requests
                                             This paper presents M2K, a fully automated framework                  and map high-level tensor operations in Python model code
                                         that makes the model-kernel interface explicit and leverages              to host-side wrapper code. The wrapper code prepares CUDA
                                         it to detect memory bugs in CUDA kernels used in LLM in-                  kernel inputs and configures kernel launches. At the lowest
                                         ference systems. M2K consists of two components. HFProbe                  layer, CUDA kernels perform the core linear algebra com-
                                         traces model execution without GPU hardware, classifies                   putation on the GPU. This separation enables independent
                                         kernel arguments into model-fixed and user-variable, and                  development at each layer and accelerates system evolution.
                                         emits symbolic constraints that capture the interface. cuK-                  However, the layered architecture introduces a fragile,
                                         LEE then performs symbolic execution on CUDA kernels to                   implicit interface between models and CUDA kernels. The
                                         pinpoint memory bugs under the interface constraints, mod-                correctness of the system depends on assumptions made
                                         eling tensors as disjoint memory regions and treating thread              independently by the two sides, yet these assumptions are
                                         identifiers symbolically to scale to thousands of threads. In             neither explicitly specified nor consistently enforced. The
                                         the evaluation, M2K discovers 181 previously unknown bugs                 mismatch manifests in two ways. First, kernels may contain
                                         in real LLM inference systems, while producing only nine                  outright implementation errors in the intricate performance
                                         false positives, demonstrating its effectiveness.                         optimizations (e.g., vectorization, tiling), causing them to
                                                                                                                   produce correct results only for specific tensor shapes, while
                                         CCS Concepts: • Software and its engineering → Em-                        silently performing out-of-bounds accesses for others. Sec-
                                         pirical software validation; Software infrastructure.                     ond, kernels may impose implicit limits on input sizes (e.g.,
                                                                                                                   due to integer types used for index arithmetic or fixed-size
                                         ACM Reference Format:                                                     internal buffers) that were safe when the kernel was written
                                         Mengting He, Shihao Xia, Haomin Jia, Wenfei Wu, and Linhai Song.
                                                                                                                   but are increasingly violated as models grow larger [79] and
                                         2026. M2K: Making the Model-Kernel Interface Explicit for Reliable
                                         CUDA Kernel Verification. In ACM SIGOPS 32nd Symposium on
                                                                                                                   inference sequences become longer [17, 71]. Both classes of
                                         Operating Systems Principles (SOSP ’26), September 29-October 02,         mismatch lead to kernel memory bugs (e.g., buffer overflows,
                                         2026, Prague, Czech Republic. ACM, New York, NY, USA, 16 pages.           integer overflows) that are difficult to catch, because they sur-
                                         https://doi.org/10.1145/3830418.3843908                                   face only under specific combinations of model architecture,
                                                                                                                   runtime input, and kernel implementation.
                                                                                                                      These kernel memory bugs carry severe consequences.
                                                                                                                   Out-of-bounds accesses and data races trigger “illegal mem-
                                                                                                                   ory access” errors on the GPU, potentially crashing the en-
                                         This work is licensed under a Creative Commons Attribution 4.0 Interna-   tire inference service [60]. More critically, recent work has
                                         tional License.
                                                                                                                   shown that memory bugs on GPUs can be exploited to mod-
                                         SOSP ’26, Prague, Czech Republic
                                         © 2026 Copyright held by the owner/author(s).
                                                                                                                   ify arbitrary GPU memory or achieve arbitrary code execu-
                                         ACM ISBN 979-8-4007-2585-2/2026/09                                        tion [19, 27, 52]. Since inference systems are exposed to the
                                         https://doi.org/10.1145/3830418.3843908                                   Internet and process user-controlled prompts, attackers can
choose sequence length and influence server-side batching.
As a result, exploitable memory bugs in CUDA kernels form
a real attack surface that may allow attackers to compromise
the host system or affect other service users, as demonstrated
by our PoC exploits [28, 29].
   Existing techniques for detecting memory bugs in CUDA
kernels fall short in this setting. Dynamic methods track
metadata for GPU memory buffers and validate pointer deref-
erences at runtime [20–22, 37, 44, 54, 55, 69, 70, 77, 83, 84, 87].                    Figure 1. An overview of M2K.
However, they either incur high overhead or require hard-
                                                                      and supports the standard Hugging Face model format, cov-
ware extensions not yet widely available. More fundamen-
                                                                      ering the vast majority of publicly available LLMs. As shown
tally, they analyze kernels in isolation from the models that
                                                                      in Figure 1, M2K consists of two major components: HFProbe
invoke them, leading to both false positives and false neg-
                                                                      and cuKLEE.
atives. Static tools [6, 11, 40–42, 45, 46, 49, 62, 72] cannot
                                                                         HFProbe “executes” each model without requiring GPU
handle runtime-determined buffer sizes or the variability of
                                                                      hardware. It profiles kernel invocations by simulating exe-
kernel launch configurations, both of which are common
                                                                      cution without running the kernels, thereby achieving high
in inference systems. Techniques for testing machine learn-
                                                                      efficiency. It classifies kernel arguments into those fixed by
ing frameworks [48, 58] mainly target the framework layer
                                                                      the model architecture (e.g., hidden dimension) and those
and cannot pinpoint CUDA kernel bugs. In short, no exist-
                                                                      varying with user input (e.g., sequence length, batch size). HF-
ing technique bridges the gap between model-level usage
                                                                      Probe translates this classification into symbolic constraints
and kernel-level implementation to provide comprehensive
                                                                      that make the model-kernel interface explicit and passes
memory-bug detection for CUDA kernels.
                                                                      them to cuKLEE for bug detection. In addition, HFProbe stat-
   We make a key observation: the implicit, unspecified in-
                                                                      ically identifies all CUDA kernels reachable from a given
terface between models and CUDA kernels is not merely a
                                                                      model and automatically mutates the model’s configurations
source of kernel memory bugs—it is an architectural weakness
                                                                      to trigger more kernels, ensuring comprehensive analysis.
of current LLM inference stacks. Models and kernels evolve
                                                                         cuKLEE performs symbolic execution on CUDA kernels
on independent release cycles, maintained by different teams
                                                                      with the interface constraints from HFProbe. To handle input
with different assumptions, yet no contract governs what
                                                                      tensors whose memory layouts are determined at runtime,
one side may assume about the other. Effectively detecting
                                                                      cuKLEE models each tensor as a distinct, widely separated
memory-safety bugs in CUDA kernels therefore requires
                                                                      memory region. This abstraction simplifies pointer–tensor
making this interface explicit: we must understand how each
                                                                      association and makes bounds checking more tractable. cuK-
model invokes its kernels and use that information to system-
                                                                      LEE introduces symbolic variables to represent each tensor’s
atically verify two properties—whether model usage respects
                                                                      base address, element count, dimensions, and other proper-
kernel limitations, and whether kernel implementations are
                                                                      ties. With these variables, M2K can handle more than 100
safe under all inputs the model can produce.
                                                                      tensor API methods by adding the appropriate constraints
   Realizing this idea raises two key challenges. First, how to
                                                                      to its execution states. It also models CUDA thread iden-
automatically extract representative kernel usage patterns from
                                                                      tifiers symbolically, allowing a single pass to capture both
a model. Kernel arguments are jointly determined by model
                                                                      shared and thread-specific computations across thousands
architecture, runtime configuration, and user-controlled in-
                                                                      of threads. Finally, cuKLEE includes a memory usage model
puts (e.g., sequence length, batch size). A practical solution
                                                                      that accounts for the input token count, model size, and avail-
must effectively characterize this combinatorial space of pos-
                                                                      able GPU memory. It uses the model to determine whether
sible invocations to provide actionable guidance for CUDA
                                                                      a detected memory bug can actually occur on a target GPU,
kernel analysis. Second, how to accurately and scalably verify
                                                                      ensuring that reported bugs are actionable in practice.
CUDA kernels under the resulting usage conditions. Kernels op-
                                                                         We evaluate M2K on CUDA kernels and models from three
erate on tensors whose shapes are determined at runtime, a
                                                                      sources: all text-generation models in vLLM [35] and the re-
setting that existing static analyses handle poorly. Moreover,
                                                                      lated kernels, all Hugging Face models with custom kernels,
kernels execute across thousands of parallel threads, and
                                                                      and models and kernels from four recent research publica-
naïvely enumerating those threads causes state explosion,
                                                                      tions [32, 50, 61, 76]. In total, M2K identifies 181 memory
making exhaustive verification infeasible.
                                                                      bugs, including 162 integer overflows 1 and 19 out-of-bounds
   To address these challenges, we design M2K, a fully auto-
                                                                      accesses, with only nine false positives, demonstrating its
mated analysis framework that detects memory-safety issues
                                                                      effectiveness in detecting memory safety issues for CUDA
in CUDA kernels as they are used by a given LLM model. M2K
targets four types of bugs in CUDA kernels: buffer overflows,         1We suspect that integer overflows are prevalent in our detection results

integer overflows, data races, and null-pointer dereferences,         because they are more likely to cause silent data corruption than crashes.
 1   class Qwen2ForCausalLM(nn.Module):                                  1        void dynamic_scaled_fp8_quant(torch::Tensor& out, torch::Tensor
 2     def __init__(self, config):                                                const& input, torch::Tensor& scale) {
 3       decoder_layer_type = Qwen2DecoderLayer                          2          int64_t num_tokens = input.numel() / input.size(-1);
 4       self.layers = ...                                               3          int64_t num_elems = input.numel();
 5     def forward(self, input_ids, positions):                          4          dim3 grid(num_tokens);
 6       hidden_states, residual = ...                                   5          dim3 block(1024);
 7       for layer in self.layers:                                       6          using bf16 = at::BFloat16; using fp8 = at::Float8_e4m3fn;
 8         hidden_states, residual = layer(positions, hidden_states,     7          vllm::scaled_fp8_quant_kernel<bf16, fp8>
           residual)                                                     8            <<<grid, block, 0>>>(out.data_ptr<fp8>(),
 9       return hidden_states                                                         input.data_ptr<bf16>(), scale.data_ptr<float>(), num_elems);
10   class Qwen2DecoderLayer(nn.Module):                                 9        }
11     def __init__(self, config):
12       self.fp8_linear = Fp8LinearOp()                                                                (c) Wrapper function.
13     def forward(self, positions, x, residual):
14       out_dtype = torch.get_default_dtype()                           1        template <typename scalar_t, typename fp8_type>
15       hidden_states = self.fp8_linear.apply(x, out_dtype)             2        __global__ void scaled_fp8_quant_kernel(fp8_type* __restrict__
16       ...                                                                      out, const scalar_t* __restrict__ input, const float*
17       return hidden_states, residual                                           __restrict__ scale, int64_t num_elems) {
18   class Fp8LinearOp:                                                   3         int tid = blockDim.x * blockIdx.x + threadIdx.x; // overflow
19     def apply(self, input, out_dtype):                                 4         const float inverted_scale = 1.0f / (*scale);
20       in_2d = input.view(-1, input.shape[-1])                          5         int step = blockDim.x * gridDim.x; // overflow
21       qinput = torch.empty(in_2d.shape, dtype=out_dtype)               6
22       scale = torch.zeros(1, dtype=torch.float32)                      7           using float8x4_t = q8x4_t<fp8_type>;
23       torch.ops._C.dynamic_scaled_fp8_quant(qinput, in_2d, scale)      8           auto* v_in = reinterpret_cast<vec4_t<scalar_t> const*>(input);
24       return w8a8_scaled_mm_func(...)                                  9           auto* v_out = reinterpret_cast<float8x4_t*>(out);
                                                                         10           int64_t const num_vec_elems = num_elems >> 2;
     (a) The simplified Python model code of Qwen2ForCausalLM.           11
                                                                         12           for (int64_t i = tid; i < num_vec_elems; i += step) {
1    TORCH_LIBRARY_EXPAND(TORCH_EXTENSION_NAME, ops) {                   13             vec4_t<scalar_t> in_vec = v_in[i]; // OOB
2      ops.def("dynamic_scaled_fp8_quant(Tensor! result, Tensor input,   14             v_out[i] = scaled_fp8_conversion<fp8_type> // OOB
       Tensor! scale) -> ()");                                           15               (in_vec, inverted_scale);
3      ops.impl("dynamic_scaled_fp8_quant", torch::kCUDA,                16           }
       &dynamic_scaled_fp8_quant);                                       17           ...
4    }                                                                   18       }

          (b) The registration of a CUDA kernel in Python.                    (d) CUDA kernel. (Thread-dependent computations are in yellow.)
Figure 2. A CUDA kernel example, its wrapper function, its registration to vLLM, and a Hugging Face model using the kernel.
kernels. We have reported all 26 bugs detected in vLLM. So                    2        Background
far, eight bugs have been fixed in subsequent releases and ad-                This section provides background for the project, including
ditional four bugs have been confirmed by the programmers,                    Hugging Face models, the CUDA programming language,
underscoring M2K’s practicality. We further compare M2K                       and CUDA kernel memory bugs in LLM inference systems.
with Honeycomb [49], GKLEE [41], and ESBMC-GPU [62]
on 20 known vLLM CUDA kernel bugs. M2K successfully de-
tects 15 of these bugs, far more than the baseline techniques,                2.1       Hugging Face Models
highlighting its superior bug coverage and clear improve-                     Hugging Face is the largest platform for sharing pre-trained
ment over existing techniques. An ablation study shows that                   models [24], offering both a model marketplace and libraries
both HFProbe and cuKLEE are critical for M2K’s effective-                     that facilitate model integration into LLM inference frame-
ness. In sum, we make the following contributions:                            works (e.g., vLLM [35], SGLang [82], Transformers [25]). To-
   • We identify the implicit model-kernel interface as one                   day, it hosts millions of models, including major open-source
      source of memory bugs in CUDA kernels used in LLM                       foundation models (e.g., Qwen, LLaMA) and their variants,
      inference systems and argue that making this interface                  making it a central hub for the AI community.
      explicit is the key to effective bug detection.                            A model released on Hugging Face typically contains four
   • We develop HFProbe, a dynamic model profiler that                        types of files. The config.json file defines the model’s archi-
      traces how models invoke CUDA kernels and infers                        tecture, including layer number, hidden size, activation func-
      model-kernel interfaces, without GPU hardware.                          tions, and other structural parameters. The model-weight
   • We design cuKLEE, a symbolic execution engine spe-                       files store the trained parameters. The Python code files de-
      cialized for CUDA kernels that supports tensors with                    fine classes that extend nn.Module and implement the model
      dynamic shapes and scales to thousands of threads.                      architecture. One top-level class assembles all model compo-
   • By integrating HFProbe and cuKLEE, we build M2K, a                       nents, with its forward() method as the entry of the model’s
      fully automated framework for detecting CUDA mem-                       whole forward pass. For example, Figure 2a shows simplified
      ory bugs in LLM inference systems and demonstrate its                   model code for Qwen2ForCausalLM, and forward() on line
      effectiveness via thorough experiments.                                 5 begins the model’s inference process. Finally, documen-
   M2K is publicly available at https://github.com/system-                    tation files (e.g., README.md) provide instructions, usage
pclub/M2K.                                                                    examples, and licensing information.
2.2   The CUDA Programming Language                                 Table 1. Summary of 20 kernel memory bugs in vLLM.
CUDA is the dominant programming platform for exploiting               Dimension                 Breakdown                  Count
GPU computational power [15], and most GPU kernels in                                  User-reported (production failure)    13
inference systems are written in CUDA C++.                          How discovered                  Unit test                 6
                                                                                                  Code review                 1
   CUDA source files typically contain two types of code:
                                                                                         GPU global memory (tensors)         17
host wrapper functions and GPU kernel functions. Host               Memory location
                                                                                             GPU shared memory                3
wrappers run on the CPU and are exposed to Python code in                             Integer overflow → buffer overflow     10
inference systems via registration or binding macros [30, 64]           Bug type         Buffer overflow (other causes)       8
(e.g., Figure 2b). They process input tensors from Python                                  Null-pointer dereference           2
code into kernel arguments, configure launch parameters                                           Kernel code                18
                                                                     Patch location
                                                                                                Framework code                2
(e.g., number of thread blocks, threads per block, shared-
memory size), and call the kernels. CUDA kernels run on the
GPU. They define the computation performed by each par-
allel thread. Under CUDA’s execution model, a kernel runs
across many threads organized into blocks and grids. Each
thread uses built-in identifiers (e.g., blockIdx.x, threadIdx     constraints. The kernel uses signed 32-bit integers for tid
.x) to determine its location in this hierarchy and the portion   on line 3 and step on line 5. Both are computed as the prod-
of input data it processes.                                       uct of the token count (blockIdx.x or gridDim.x) and 1024
   Function dynamic_scaled_fp8_quant() in Figure 2c is            (blockDim.x), implicitly capping the safe token count at
a wrapper function. It first computes the token count and         221 − 1. Neither the model nor the inference framework en-
feature-element count in tensor input on lines 2–3. It then       forces this bound, as the kernel, model, and framework are de-
sets the number of blocks to the token count on line 4 and        veloped independently with no formal interface constraints
the number of threads per block to 1024 on line 5. Finally,       on valid input ranges. A combination of batch size 𝐵𝑆 and
it launches kernel function scaled_fp8_quant_kernel()             sequence length 𝑆𝐿 satisfying 𝐵𝑆 × 𝑆𝐿 > 221 (e.g., 𝐵𝑆 = 116,
with pointers to the underlying memory of the three input         𝑆𝐿 = 18,079) thus silently triggers overflow, making tid and
tensors and the feature-element count on lines 7–8.               step negative. The corrupted tid is then used as an index
   Figure 2d shows the CUDA kernel, which converts high-          to read and write the input/output buffers, turning a silent
precision element values in input into FP8 using the scaling      arithmetic error into out-of-bounds memory accesses. We
factor scale. To improve efficiency, the kernel applies vector-   reproduced this bug under vLLM on an NVIDIA B300 GPU:
ization. On lines 8–9, the pointers input and out are cast to     the overflowed read on line 13 lands on an unmapped vir-
vectorized types so each access processes four elements. Line     tual address, raising an “illegal memory access” fault and
10 computes the number of such accesses by dividing the           crashing the inference service.
element count by four. The loop on lines 12–16 distributes           To quantify the problem, we examine vLLM’s change logs
work across threads using a grid-stride pattern. Each thread      and identify 20 fixed memory bugs in CUDA kernels (Table 1).
starts from its global index (blockDim.x * blockIdx.x +           Four findings stand out. First, memory bugs in CUDA kernels
threadIdx.x, line 3) and moves with a stride equal to the         are common and costly. Of the 20 bugs, 13 were reported
total number of threads (blockDim.x * gridDim.x, line 5).         by users after causing failures in production; only six were
In each loop iteration, a thread loads four input elements on     caught by unit tests and one by code review. Second, nearly
line 13, converts them to FP8 using the reciprocal of scale,      all bugs involve tensors. 17 bugs occur on input tensors in
and writes the results back to the output buffer on line 14.      GPU global memory and three in GPU shared memory, con-
                                                                  firming that tensor shape and layout mismatches are the
                                                                  dominant root cause. Third, integer overflow is the leading
2.3   Kernel Memory Bugs in Inference Systems                     bug pattern. Ten of the 20 bugs are integer overflows in index
CUDA kernels in LLM inference systems are prone to mem-           computations that subsequently trigger buffer overflows, re-
ory bugs. Kernels perform index arithmetic over large multi-      flecting the growing risk as models and input sequences scale
dimensional tensors across thousands of threads; even small       up. Fourth, fixing these bugs is not always limited to chang-
indexing mistakes can cause out-of-bounds accesses or data        ing the kernel code. Two bugs were fixed by modifying the
races. Performance optimizations (e.g., vectorization, tiling)    framework’s kernel invocation instead. This shows that di-
further complicate this arithmetic. Moreover, because mod-        agnosing and fixing kernel memory bugs requires reasoning
els and kernels are developed independently with no formal        across the entire software stack, rather than analyzing the
interface contract, a kernel that is correct for one model may    CUDA kernel alone. These findings motivate M2K’s design:
silently produce memory errors for another.                       HFProbe makes tensor-level interface constraints explicit,
   Figure 2d illustrates a representative bug rooted in the       and cuKLEE uses symbolic execution to check index arith-
mismatch between model assumptions and kernel interface           metic and buffer bounds that existing testing misses.
3     Overview of M2K                                             1     class Fp8LinearOp:
                                                                  2       def apply(self, input, out_dtype):
M2K detects memory bugs in CUDA kernels used by LLM               3         in_2d = input.view(-1, input.shape[-1])
inference systems. As shown in Figure 1, it consists of two       4         qinput = torch.empty(in_2d.shape, dtype=out_dtype)
                                                                  5         scale = torch.zeros(1, dtype=torch.float32)
components: HFProbe, which constructs constraints that            6   -     torch.ops._C.dynamic_scaled_fp8_quant(qinput, in_2d, scale)
capture the model-kernel interface, and cuKLEE, which per-        7   +     stub_dynamic_scaled_fp8_quant(qinput, in_2d, scale)
                                                                  8         return w8a8_scaled_mm_func(...)
forms symbolic execution on CUDA kernels under these              9
constraints to identify memory bugs.                             10   +def stub_dynamic_scaled_fp8_quant(output, input, scale):
                                                                 11   + LOG('dynamic_scaled_fp8_quant')
   HFProbe supports two inference backends, vLLM [35] and        12   + LOG(retrieve_stack_info())
Transformers [25], covering most Hugging Face [24] models.       13   + LOG('output', type(output), output.shape, output.dtype)
                                                                 14   + LOG('input', type(input), input.shape, input.dtype)
Given a model, HFProbe traces its execution without launch-      15   + LOG('scale',type(scale), scale.shape, scale.dtype)
ing GPU kernels, and infers whether each kernel argument         16   + return None

is model-fixed or user-controlled and possible relationships                     Figure 3. A tracing stub example.
among the arguments. Then, it synthesizes interface con-
straints to encode the inference results. For example, when      assuming a model object has no aliases within its own im-
analyzing the model in Figure 2a with the CUDA kernel in         plementation). The analysis over-approximates the results
Figure 2d, HFProbe infers that tensors out and input in Fig-     and includes all kernels that may be invoked. These kernels
ure 2c share the same shape, with their last dimensions fixed    guide the subsequent model configuration mutation. During
at 896 (the model’s hidden size) and their first dimensions      dynamic profiling, HFProbe ignores any kernels that are not
equal to the number of user-input tokens.                        actually executed. Existing Python call-graph tools cannot
   cuKLEE takes the interface constraints as input and checks    correctly analyze Hugging Face models [31, 67, 78]. For ex-
for out-of-bounds accesses, integer overflows, data races, and   ample, PyCG does not handle __call__, preventing it from
null-pointer dereferences, reporting each bug’s line number      resolving calls to an nn.Module object—the standard way to
along with a triggering input. For example, for the CUDA         invoke a layer’s forward() method (e.g., line 8 in Figure 2a).
kernel in Figure 2d and its wrapper in Figure 2c, cuKLEE            Our analysis operates on the Abstract Syntax Tree (AST) of
reports that batch size 116 and sequence length 18,079 (whose    the input Python program. It maintains an execution context
product is the number of input tokens and equals the first       where each program object is represented as an instance,
dimension of input and out in Figure 2c) trigger integer         created when its class constructor is analyzed. Each instance
overflows on lines 3 and 5 of Figure 2d and out-of-bounds        stores its fields and their values in a dictionary. The analysis
accesses on lines 13 and 14.                                     processes each instruction with respect to this context and
   M2K serves two complementary usage scenarios. Model           also updates it based on the instruction’s semantics.
developers can run it to verify existing kernels correctly          Our analysis initializes the context from the model’s __-
support a new model architecture and expected token counts,      init__() method. It then analyzes the model’s forward()
while kernel developers can confirm that an optimized or         method to construct the call graph. For each field assignment
rewritten kernel remains safe across all deployed models.        (e.g., line 4 in Figure 2a), the analysis updates the left-hand
                                                                 instance’s dictionary with either the concrete value or the
                                                                 right-hand-side instance. For each function call, it performs
4     HFProbe: Dynamic Model Profiling                           interprocedural analysis by mapping the actual-argument in-
As illustrated in Figure 1, HFProbe operates in four stages.     stances to formal parameters. If the receiver’s type is known
It first performs static analysis to identify all CUDA ker-      only at the base class level, all possible subclasses’ methods
nels an input model may call. It then executes the model         are treated as potential callees. At each branch, the analysis
using mocked CUDA kernels with a real model configura-           inspects the context to decide feasible paths. If both paths
tion, recording how the kernels are actually invoked. Next,      may occur, it clones the context and analyzes each path in-
it mutates the model configuration to exercise additional        dependently. When encountering Python bindings to CUDA
kernels identified statically but not triggered dynamically.     kernels (e.g., line 23 in Figure 2a), it records that the model
Finally, it aggregates the collected information in a post-      calls the corresponding CUDA kernels. All Python bindings
mortem analysis to derive constraints that summarize the         and their links to CUDA kernels (e.g., Figure 2b) are identified
interface between the model and each kernel it uses.             separately using regular expressions.

                                                                 4.2     Profiling Backends
4.1   Static Call Graph Computation                              We modify the vLLM and Transformers inference frame-
Given a model’s Python implementation (e.g., Figure 2a), we      works to serve as HFProbe backends and record runtime
build a static call graph rooted at the model’s forward()        information during inference. To speed up profiling, we dis-
method. The analysis is path- and field-sensitive and lever-     able all GPU computations, allowing models to run without
ages common coding patterns of Hugging Face models (e.g.,        GPU hardware. Overall, we make four types of changes.
   First, for every registered CUDA kernel, we replace its         4.4   Interface Constraint Generation
Python binding with a tracing stub. As shown in Figure 3,          Given a configuration, HFProbe executes the model with
the stub function records the call stack and parameter types.      multiple combinations of batch size and sequence length,
For tensor inputs (e.g., input), it further records their shapes   whose product equals the number of input tokens. These two
and data types. For integer-valued tensors, it also records        parameters are varied because they are controlled by users.
the minimum and maximum values in the tensors to capture           HFProbe then uses the recorded dynamic information to
possible index ranges. For primitive-type parameters, the          construct the implicit interface between the model and each
stub records their concrete values. If the original binding        called CUDA kernel as the conjunction of a set of symbolic
returns a tensor, the stub returns a zero-filled tensor with       constraints. Because the same kernel may be invoked under
the same shape and data type.                                      different call contexts within a single forward pass, HFProbe
   Second, model-loading functions are modified to create          uses call-stack information to group invocations and infers
tensors with correct shapes without loading actual weights.        constraints independently for each group.
   Third, although no GPU computations are executed, we               For each kernel, HFProbe builds interface constraints over
ensure the frameworks follow the same control flow as with         its wrapper function’s arguments, including tensor dimen-
real GPUs. This involves replacing vllm._C with a fake mod-        sions, tensor value ranges, and primitive parameters. These
ule, since it cannot be imported without a real GPU, and           constraints fall into four categories.
adjusting tensors’ internal properties so the frameworks              Model-fixed constants. Some arguments are determined by
treat their data as GPU-resident.                                  the model architecture (e.g., hidden dimension). HFProbe
   Fourth, we optimize vLLM’s KV-cache management to               identifies them by checking whether a value is invariant
initialize tensors with minimal memory and expand them to          across all runs and constrains it to the observed constant.
the required shapes without more memory allocation. Extra             User-controlled linear arguments. Among the arguments
memory is allocated only when a tensor receives writes be-
                                                                   that change across runs, HFProbe isolates those that scale
yond its initial space. This lazy allocation strategy eliminates
                                                                   linearly with batch size, sequence length, or token count by
pre-allocated memory and reduces memory pressure.
                                                                   verifying that the ratio to the corresponding value is constant
4.3   Model Configuration Mutation                                 across runs. These arguments are directly controllable by
                                                                   end users, and cuKLEE treats them as the primary source of
For each input model, we mutate two types of execution
                                                                   attacker-controlled inputs during verification.
configuration parameters to trigger CUDA kernels identified
                                                                      Inter-argument equalities. Kernel semantics impose depen-
statically but not exercised during earlier profiling.
                                                                   dencies among arguments. For example, a matrix multiplica-
   First, several parameters in the model’s config.json gov-
                                                                   tion requires the inner dimensions of its operands to match.
ern which CUDA kernels are invoked during the forward
                                                                   HFProbe detects arguments that always share the same value
pass. For example, changing parameter quantization_con-
                                                                   and links them with equality constraints.
fig selects a different quantization kernel, while reducing
                                                                      Residual upper bounds. Remaining arguments may still de-
n_routed_experts from 256 to 128 alters the padding ker-
nel used for token routing from sgl_moe_align_block_-              pend on the model architecture indirectly. HFProbe bounds
size() to moe_align_block_size(). Because parameter                them using the maximum value observed across all runs.
names and semantics vary across models, we use an LLM                 For example, after profiling the model in Figure 2a with
in agent mode to generate modified config.json files: given        a configuration from [23], HFProbe generates constraints
the model’s Hugging Face repository URL and the name of a          stating that out and input in Figure 2c share the same shape,
target kernel, the LLM inspects the model code, references         that their second dimensions are model-fixed at 896 (the
the example config.json, and produces a new config.json file.      hidden size), that their first dimensions are linear in the
Not all generated config.json files are valid. For example, the    token count, and that scale contains exactly one element.
model in Figure 2a requires the activation function silu, and
changing the hidden_act field in config.json will cause an         5     cuKLEE: Symbolic Execution on CUDA
assertion error at runtime. We simply discard any modified         As shown in Figure 1, cuKLEE begins its analysis of a CUDA
config.json that results in a runtime failure.                     kernel (e.g., Figure 2d) from the kernel’s wrapper function
   Second, framework environment variables and startup             (e.g., Figure 2c), collecting information about how the kernel
parameters also affect which kernels are used. We maintain         is invoked. It then performs symbolic execution on the ker-
a one-time, framework-specific mapping from each CUDA              nel to detect potential memory bugs. cuKLEE allows users to
kernel to its required framework configuration. To trigger         specify constraints on the wrapper’s inputs, so that the inter-
a kernel, we retrieve and apply its configuration from this        face constraints generated by HFProbe can be incorporated,
mapping. If a kernel requires coordinated changes to both          improving both accuracy and efficiency of the symbolic exe-
framework settings and config.json, we apply the framework         cution. Furthermore, cuKLEE performs additional validation
settings first, then ask the LLM to modify config.json.            of detected bugs to ensure they can be triggered under the
      Table 2. Constraint variables defined for tensor t.              Table 3. Tensor-method handling examples. (’-’: ignored.)
           Tensor Fields             Description       Variables             Category   Tensor Methods            Constraints
      t.storage_.data_ptr_      base address            𝐵𝑡                       I         t.numel()                      𝑁𝑡
            t.numel_           # of elements            𝑁𝑡                       I        t.data_ptr()                    𝐵𝑡
   t.sizes_and_strides_.size_ # of dimensions          𝐷𝑡                                                        𝑁𝑡 2 = 𝑁𝑡 1 /𝑑𝑡01 ,
      t.sizes_and_strides_      dimensions    𝑑𝑡0 , 𝑑𝑡1 , ... 𝑑𝑡𝐷 −1            II        t2=t1.sum(0)     𝐷𝑡 2 = 𝐷𝑡 1 − 1, 𝑆𝑡 2 = 𝑆𝑡 1 ,
     t.data_type_.itemsize_     element size            𝑆𝑡                                                 𝑑𝑡02 = 𝑑𝑡11 , ..., 𝑑𝑡𝐷2 −1 = 𝑑𝑡𝐷1
                                                                                        check_dim_size
                                                                                III                             𝐷𝑡 = 𝑛, 𝑑𝑡𝑖 = 𝑒𝑥𝑝
                                                                                        (t, n, i, exp)
target inference framework and GPU environment. Overall,                        IV       t.toString()                     -
cuKLEE addresses three key challenges.
   First, prior symbolic execution techniques (e.g., KLEE [10])        cuKLEE uses these constraints to identify the source tensor
struggle to handle buffers whose sizes are determined at               and check the access against its bounds directly, without
runtime. In contrast, most CUDA kernels in LLM inference               scanning all allocated memory objects—as a conventional
systems operate on the raw memory of tensor objects (e.g.,             symbolic execution engine (e.g., KLEE) must do to determine
out and input on line 2 of Figure 2d), whose shapes vary               which object a pointer may reference. For example, when
depending on model architectures or user-provided tokens.              analyzing line 14 in Figure 2d, cuKLEE immediately deter-
How can cuKLEE analyze tensors with dynamic shapes and                 mines that the memory write must be checked against the
memory operations on the tensors?                                      bounds of out. This follows the constraint established on
   Second, wrapper functions often call tensor methods to set          line 9, which binds v_out to the base address of out.
up parameters (e.g., input.size(-1) on line 2 of Figure 2c)               Other Memory. For global and local memory allocated
for kernel launches. These methods often involve complex               inside wrapper and kernel functions, we use the contiguous
memory management, and analyzing them in full would sig-               memory model adopted by KLEE. CUDA shared memory
nificantly increase execution time and reduce precision. How           supports both dynamic allocation at kernel launch sites and
can we summarize these tensor methods to make cuKLEE                   static allocation inside kernels, and cuKLEE handles these
both efficient and accurate?                                           two cases separately. For dynamically allocated shared mem-
   Third, CUDA kernels run across many threads, and an-                ory, cuKLEE infers a concrete or symbolic size from the
alyzing each thread separately would result in redundant               kernel launch parameters. For statically allocated shared
work. How can we share symbolic execution results across               memory, cuKLEE obtains the fixed size directly from the
threads to avoid unnecessary computations?                             kernel declaration. cuKLEE models global, shared, and local
                                                                       memory as separate regions and resolves pointer targets
5.1    Memory Model of cuKLEE                                          only within the region to which they belong.
cuKLEE treats tensor memory separately from other memory
regions.                                                               5.2   Handling Tensor Methods
   Tensor Memory. All input tensors are stored in GPU                  To handle tensor methods, cuKLEE associates each tensor
global memory and allocated by the inference systems in-               with a set of symbolic constraint variables, representing its
dependently of the kernels. Therefore, kernel programmers              base address, element count, dimensions, and other proper-
cannot assume any specific memory layout among tensors.                ties in Table 2. Since the number of dimensions may remain
In practice, they never use a pointer to an element of one             unknown throughout the analysis, cuKLEE maintains a map
tensor to refer to an element of another tensor after arith-           to record all known dimensions, where the keys are dimen-
metic computations. We leverage this property by modeling              sion indices and the values are the corresponding symbolic
tensors’ underlying memory regions as discrete and far away            variables (e.g., 𝑑 1 , 𝑑 2 ). For example, input.size(-1) on line
from each other.                                                       2 of Figure 2c accesses the last dimension of tensor input.
   This design contrasts with KLEE’s memory model, which               cuKLEE processes this method by adding an entry to the
                                                                       map with key −1 and value 𝑑𝑖𝑛𝑝𝑢𝑡     𝐷 −1 .
treats the entire heap as a single continuous memory space.
In KLEE, if a buffer has a symbolic size, the base addresses              With the constraint variables, cuKLEE supports 140 Ten-
of all subsequent buffers become symbolic as well, making              sor and TensorIterator methods, grouped into four cat-
memory-access reasoning intractable. This is the fundamen-             egories. Table 3 shows examples. ○          1 Property queries (36
tal reason why KLEE cannot handle buffers whose sizes are              methods) return tensor metadata such as element count or
determined at runtime.                                                 shape. cuKLEE models their return values using the symbolic
   cuKLEE’s modeling strategy greatly simplifies the detec-            variables in Table 2. For example, input.numel() on line
tion of out-of-bounds accesses on tensor memory. Because               3 of Figure 2c returns 𝑁𝑖𝑛𝑝𝑢𝑡 . ○      2 Tensor-producing methods
each tensor occupies a distinct memory region, every pointer           (70 methods) create a new tensor or a sub-tensor. cuKLEE
derived from a tensor carries constraints that relate it to            introduces a set of fresh symbolic variables for the result
that tensor’s base address. When a pointer is dereferenced,            and adds constraints relating it to the original. For example,
 Table 4. Constraint variables defined for CUDA threads.
                                                                   5.4   Synthesizing Input and Buggy Constraints
               Variables       Description     Type                Input Constraints. Before analyzing each wrapper func-
             𝑏𝑙𝑜𝑐𝑘𝐼𝑑𝑥 .𝑥/𝑦/𝑧 block identifier    ID                tion, cuKLEE introduces three symbolic variables: 𝐵𝑆 (batch
            𝑡ℎ𝑟𝑒𝑎𝑑𝐼𝑑𝑥 .𝑥/𝑦/𝑧 thread identifier   ID
                                                                   size), 𝑆𝐿 (sequence length), and 𝑇𝐶 (token count), related
             𝑔𝑟𝑖𝑑𝐷𝑖𝑚.𝑥/𝑦/𝑧       grid size     launch
            𝑏𝑙𝑜𝑐𝑘𝐷𝑖𝑚.𝑥/𝑦/𝑧      block size     launch
                                                                   by 𝑇𝐶 = 𝐵𝑆 × 𝑆𝐿. In addition to the interface constraints
                                                                   from HFProbe, cuKLEE bounds these variables using two
                                                                   extra sources: ○ 1 Model-defined limits. Many models specify
                                                                   a maximum sequence length through fields such as “max_-
t2 = t1.sum(0) reduces t1 along its first dimension, so            position_embeddings”, “n_positions”, or “max_seq_len”
t2 has one fewer dimension and its 𝑖-th dimension equals           in their config.json files. HFProbe extracts these values from
the (𝑖+1)-th dimension of t1 (Table 3, Row 3). ○3 Property         each input model’s config.json and cuKLEE uses them to
checks (4 methods) inspect tensor properties (e.g., contigu-       upper-bound 𝑆𝐿. ○  2 Practical input limits. Even when a model
ity); cuKLEE encodes the success condition as a constraint.        does not specify a maximum, the sequence length is bounded
○4 Analysis-irrelevant methods (30 methods) do not affect          in practice. Current production models (e.g., GPT-5.4 [57],
bug detection and are skipped.                                     Claude Opus 4.6 [13], Gemini 3.1 [26]) support up to roughly
                                                                   one million tokens. We therefore impose default bounds of
                                                                   𝐵𝑆 ≤ 1,000 and 𝑆𝐿 ≤ 1,000,000, which can be adjusted for
5.3   Handling CUDA Threads
                                                                   specific deployment scenarios.
CUDA kernels execute across thousands of threads organized            Buggy Constraints. cuKLEE checks four types of mem-
into blocks and grids. All threads run the same code but           ory bugs (data-race detection is described in Section 5.3).
diverge based on their thread and block identifiers, which         For out-of-bounds accesses, cuKLEE adds a constraint at each
programmers also use to partition work over input data.            memory access via a pointer asserting that the pointer falls
   Rather than enumerating threads, cuKLEE models thread           outside the valid range of the accessed buffer. For integer
and block identifiers as symbolic variables, so that a single      overflows, cuKLEE adds a constraint at each 32-bit addi-
symbolic execution pass captures the behavior of all threads.      tion or multiplication asserting that the result exceeds the
As shown in Table 4, cuKLEE introduces six ID variables            type’s maximum value. For null-pointer dereferences, cuKLEE
(e.g., threadIdx.x, blockIdx.y) and six launch variables           adds constraints for each pointer dereference indicating the
(e.g., blockDim.x, gridDim.y). ID variables are bounded by         pointer may have been computed from an unknown base
launch variables following CUDA semantics (e.g., 𝑏𝑙𝑜𝑐𝑘𝐼𝑑𝑥          pointer. All input tensors are assumed to be valid with base
.𝑥 < 𝑔𝑟𝑖𝑑𝐷𝑖𝑚.𝑥), and launch variables are concretized or           addresses properly initialized by the inference frameworks.
constrained when cuKLEE analyzes kernel launch sites (e.g.,
𝑔𝑟𝑖𝑑𝐷𝑖𝑚.𝑥 = 𝑛𝑢𝑚_𝑡𝑜𝑘𝑒𝑛𝑠 in Figure 2c). With this approach,
thread-independent bugs are detected as in sequential pro-
grams; thread-dependent bugs (e.g., line 13 in Figure 2d) are      5.5   Bug Detection and Validation
captured through constraints over the ID variables.                cuKLEE begins symbolic execution from each wrapper func-
   For loops that distribute work across threads (e.g., the        tion under the input and interface constraints, processing
highlighted loop in Figure 2d), cuKLEE analyzes their loop         tensor methods (Section 5.2) and, upon each kernel launch,
bodies once and then adds the loops’ exit conditions to its        introducing thread ID variables and launch variables con-
execution states (e.g., 𝑖 ≥ 𝑛𝑢𝑚_𝑣𝑒𝑐_𝑒𝑙𝑒𝑚𝑠) for the remaining       strained by CUDA semantics (Section 5.3). cuKLEE then exe-
execution. This suffices because such loops follow a simple        cutes the kernel body instruction by instruction. At each po-
strided pattern: each thread starts at an offset given by its      tentially buggy instruction, it synthesizes buggy constraints
global thread index and advances by the thread count. A            (Section 5.4), conjoins them with existing constraints, and in-
single symbolic analysis of the loop body can capture every        vokes a solver. A satisfiable result yields concrete values for
loop index a thread may process, while the exit condition          all symbolic variables, including batch size 𝐵𝑆 and sequence
characterizes the post-loop state.                                 length 𝑆𝐿.
   To detect data races, cuKLEE introduces a second set of six        However, not every satisfiable assignment is triggerable
ID variables representing a distinct thread. It asserts that the   in practice. 𝐵𝑆 and 𝑆𝐿 are end-user inputs to the inference
two threads differ by negating the conjunction of pairwise         framework, but the framework may reject certain values, or
equality over their ID variables. For each global-memory ac-       the resulting memory footprint may exceed GPU capacity.
cess, cuKLEE checks whether the second thread may perform          cuKLEE checks both conditions to confirm a bug.
a conflicting write to the same address. cuKLEE performs a            We replay the (𝐵𝑆, 𝑆𝐿) pair via HFProbe’s profiling back-
similar check for shared memory but additionally constrains        end. If the kernel is still invoked and its arguments match the
the two threads’ block ID variables to be equal, since shared      interface constraints, the bug is confirmed to be reachable
memory is private to each block.                                   through the framework.
Table 5. Benchmark information and detection results. (
                                                                  6.1   Bug Detection in the Wild
IO: integer overflow, OOB: out-of-bounds, DR: data race, and
NULL: null-pointer dereference. 𝑥 𝑦 : x true positives, y false   6.1.1 Methodology. As shown in Table 5, we evaluate
positives. ’-’ indicates zero true and false positives.)          M2K on models and kernels from three real-world sources.
                                                                  First, we extract all text-generation models and their associ-
             Models Kernels   IO     OOB DR NULL Total            ated kernels from vLLM-0.9.0, the latest release at the start
    vLLM       62     50       72    195   02    -    269         of this project, yielding 62 models and 50 kernels, with sub-
    HF         54     117     1310    -     -    -    1310
                                                                  stantial kernel reuse across models. Because vLLM omits
    Papers     4       6      240     -     -    -    240
                                                                  config.json files, we retrieve them from Hugging Face by
    Total     120     173     1622   195   02    -    1819
                                                                  querying model IDs specified in vLLM’s tests, and select-
                                                                  ing the config.json from the top-ranked repository for each
                                                                  model. Second, we gather all Hugging Face models that con-
                                                                  tain custom CUDA kernels, resulting in 54 models and 117
   We estimate GPU memory consumption as model-weight             unique kernels. Third, we survey top-tier AI conference pa-
storage plus KV-cache size, scaled by a 1.25× fragmentation       pers from the past two years and identify four [32, 50, 61, 76]
factor for the vLLM backend and 1.45× for Transformers.           whose artifacts provide both Hugging Face models and cus-
Model-weight size is obtained directly from the weight files.     tom kernels, contributing four models and six kernels. In
KV-cache size is 2 × 𝐿 × 𝑇𝐶 × 𝐻 × sizeof (dtype), where 𝐿         total, our evaluation includes 120 models and 173 kernels,
is the number of layers, 𝑇𝐶 is the token count, 𝐻 is the          comprising 170,875 lines of Python model code and 139,951
hidden dimension, and dtype is the cache data type. Interme-      lines of CUDA code.
diate tensors and temporary buffers are negligible relative          We evaluate benchmarks from the first source using the
to weights and KV-cache and are omitted. If the estimated         vLLM backend and the remaining benchmarks using the
total exceeds the target GPU’s memory capacity, the bug           Transformers backend. For each model, we attempt config-
is marked as untriggerable. For the bug in Figure 2d, the         uration mutation only once for any CUDA kernel that is
solver reports 𝐵𝑆=116 and 𝑆𝐿=18,079; the estimated memory         statically reachable but not triggered by the collected con-
usage is 211.2GB, well within a B300 GPU’s 288GB memory           fig.json. For every configuration (both original and mutated),
capacity. We confirm the bug is triggerable on this hardware.     we test nine combinations of batch sizes {1, 3, 5} and se-
                                                                  quence lengths {1, 7, 17}, chosen to keep profiling short while
                                                                  remaining realistic and uncommon. Each CUDA kernel is
6    Evaluation                                                   analyzed by cuKLEE for up to one hour, following common
Implementation. HFProbe is implemented in Python. It per-         practice in prior symbolic-execution work [10, 34, 47].
forms call-graph analysis using the built-in AST module [65],        For each bug reported by cuKLEE, we examine the cor-
provides two profiling backends (vLLM-0.9.0 [35] and Trans-       responding CUDA code to verify that the reported tensor
formers v4.52.1 [25]), and employs ChatGPT agent [56] to          shapes and input values indeed trigger the issue and are
mutate config.json files. The agent has web search capabil-       semantically valid. To ensure objectivity, each bug is inde-
ity to retrieve relevant code. In total, HFProbe comprises        pendently reviewed by at least two authors. Because vLLM
18,453 lines of code, including both standalone modules and       kernels are shared across models, we count unique bugs by
framework modifications. cuKLEE is built on KLEE v3.1 and         kernel line number, even if they are triggered by different
operates on LLVM IR generated from CUDA source code. We           models. For out-of-bounds accesses resulting from a preced-
implement 19,572 lines of C++ to support tensor abstractions      ing integer overflow, we count only the integer overflow.
and enable symbolic execution on CUDA threads and GPU
instructions. cuKLEE uses Z3 [18] as its constraint solver.       6.1.2 Experimental Results. As shown in Table 5, M2K
   Research Questions. Our experiments aim to evaluate            detects 181 memory bugs in CUDA kernels, including 162
M2K’s effectiveness in detecting memory bugs in CUDA ker-         integer overflows and 19 out-of-bounds accesses. It also iden-
nels used by real-world inference systems (Section 6.1), its      tifies one benign race in vLLM, which we conservatively clas-
coverage of CUDA memory bugs (Section 6.2), its advan-            sify as a false positive. M2K does not report any null-pointer
tages over existing techniques (Section 6.2), and the ratio-      dereferences. The large number of bugs demonstrates M2K’s
nale behind combining dynamic model profiling with CUDA-          effectiveness in detecting memory bugs in CUDA kernels.
specific symbolic execution (Section 6.3).                            In addition, M2K detects bugs across benchmarks from
   Experimental Settings. Most experiments run on a server        all three sources, underscoring its ability to analyze diverse
with an Intel Xeon Silver 4110 CPU, 256GB RAM, and Red            models and kernels.
Hat Enterprise Linux 9. We compile CUDA code for CUDA                 We have reported all 26 bugs detected from vLLM, which
12.1 using clang++ 13.0.0 with “-emit-llvm” to generate           has an actively maintained GitHub repository. Of them, eight
LLVM IR for cuKLEE. Unless stated otherwise, we target an         have been fixed in the most recent version, and four extra
NVIDIA B300 GPU with 288GB memory for bug validation.             bugs have been confirmed by the developers. Among the 18
 1   // Qwen-1_8B-Chat: heads=16, height=128, hidden_size=heads*height
 2   // batch: batch_size, width: seq_len
 3   __global__ void VecQuant8BatchMatMulKernel_faster_old(const
     half* vec, const uint8_t* mat, half* mul, int batch, int width,
     int heads, int height) {
 4     int weight_total = batch * width * heads * height; // overflow
 5     int h = 128 * blockIdx.x;
 6     int w = 128 * blockIdx.y + threadIdx.x;
 7     int i = width * h + w;
 8     half2 weight[64];
 9     for (int b = 0; b < batch; ++b) {
10       for (int head = 0; head < heads; ++head) {                       Figure 5. How the number of bugs changes with GPU mem-
11         int shift = b * heads + head;                                  ory. (The vertical line represents NVIDIA B300.)
12         for (int k = 0; k < 64; ++k) {
13           int index1 = shift * height * width + i + (2 * k * width);
14           if (index1 >= weight_total || w >= width || ...)             kernel imposes any constraint to prevent this value from
15             weight[k] = __float2half2_rn(0);                           exceeding that limit. We count these bugs as separate bugs,
16           else
17             weight[k] = compute_weight(mat, ...);                      according to the methodology described in Section 6.1.1.
18     }}}                                                                    The proportion of integer overflows among the detected
19     compute_mul(mul, vec, weight,...);
20   }                                                                    bugs is markedly higher than in the bugs collected from
                                                                          vLLM’s change log in Section 2.3. We hypothesize that inte-
           Figure 4. A detected integer overflow bug.                     ger overflows are often under-reported because overflowed
unresolved bugs, the buggy code has been refactored for 13,               values are typically used in computations rather than as
while the other five are still in the codebase. We do not report          indices, causing silent result corruption instead of crashes.
bugs in Hugging Face models or research papers when the                       Buffer Overflows. Eight buffer overflows occur when data
corresponding GitHub repository is unavailable, has been                  is partitioned into blocks, but the final block is only partially
inactive for more than a year, or no contact email is found.              filled, yet kernels access it as if fully populated. The remain-
For the 36 remaining cases, we have contacted the authors                 ing 11 arise when input tensor values are used to compute
by email but haven’t received any response.                               indices into another tensor without adequate bounds check-
   Integer Overflows. Three detected integer overflows occur              ing. For them, we further confirm that the framework code
on unsigned 32-bit integers, and the rest occur on signed                 permits the buggy tensor content to pass into the kernel.
int32 values. In 15 cases, the overflowed value is later used                 Data Races. M2K detects a data race, where an array is
as an index, triggering subsequent out-of-bounds accesses.                used to count tokens assigned to each expert, with one ar-
Figure 2d shows one such example.                                         ray element per expert. The array elements are partitioned
   In terms of what is being computed, 36 of the overflows                among warps. During initialization, all 32 threads in a warp
come from multiplying the token count by the hidden size.                 write zero to all the elements in the warp’s partition, creating
For example, the kernel VecQuant8BatchMatMulKernel_-                      a race. We consider the race benign and classify it as a false
faster_old() in Figure 4 multiplies input matrices vec and                positive, as all conflicting threads write the same value to the
mat, and stores the result in mul. Since mat is quantized, the            same location. Nevertheless, this case demonstrates M2K’s
kernel dequantizes it on lines 9–18 before multiplying on line            capability to detect data races in CUDA kernels.
19. During dequantization, weight_total is used on line 14                    Security Impacts. As an initial exploration, we reproduce a
to determine whether a value should be zeroed. However,                   subset of the detected bugs and examine their potential secu-
the computation of weight_total can overflow. Specifically,               rity impacts. A systematic study is left for future work. Most
batch * width equals the token count, and heads * height                  reproduced integer overflows corrupt computation results
equals the hidden size. While the hidden size is fixed at                 and may affect downstream tasks. Most reproduced out-of-
16∗128, overflow can occur when the batch size is 128 and the             bounds accesses (e.g., Figure 2d) trigger crashes because they
sequence length is 8,192. When this happens, weight_total                 access unmapped memory. We also find one case in which a
becomes negative, zeroing all dequantized values on line                  signed-index overflow is used in a memory write, modifying
15 and corrupting the subsequent computation. Another 98                  a neighboring tensor and corrupting the inference results
integer overflows occur when computing the element count                  of other users in the same batch. We record a video demon-
in 𝑄𝐾 ⊤ , whose size is batch_size × num_heads × seq_len2                 strating this effect [29]. In a newer version of vLLM, we find
and can exceed the int32 limit. Four additional overflows                 a similar bug in which an overflowed unsigned index is used
arise when multiplying the token count by 1,024 (thread                   for a memory read, exposing another user’s inference output.
count), as shown in Figure 2d. The remaining 24 overflows                 This bug was introduced after vLLM-0.9.0 and is therefore
come from a single code fragment that appears 24 times at                 not included in Table 5. Our finding leads to a published
different stages of a long computation. In each fragment, a               security advisory [73], and we also record a demonstration
32-bit integer is shifted left by 10 bits and then cast to a 16-          video [28]. Finally, we find it difficult to exploit the detected
bit integer. When the original value exceeds 31, an overflow              out-of-bounds accesses for arbitrary code execution, since re-
occurs during the cast. Neither the model code nor the CUDA               turn addresses are typically stored in registers during CUDA
Table 6. Comparison with baseline techniques. (20 bugs are
                                                                   1   // num_thread = std::max(num_experts, 32)
for each row. ‘/’: not applicable.)                                2   // share_mem size: num_experts+1+(num_thread+1)*num_experts
                                                                   3   __global__ void moe_align_block_size_kernel(int32_t num_experts){
                   Honeycomb GKLEE ESBMC-GPU       cuKLEE          4     extern __shared__ int32_t shared_mem[];
                                                                   5   - int32_t* tokens_cnts = shared_mem + blockDim.x + 1;
      vLLM            /        /          /           15           6   + int32_t* tokens_cnts = shared_mem + num_experts + 1;
      Simplified      0        5          3           19           7     for (int i = 0; i < num_experts; ++i) {
                                                                   8       tokens_cnts[num_experts * (threadIdx.x + 1) + i] = 0; // OOB
function calls and are not easily overwritten unless register      9     }}

spilling occurs.                                                            Figure 6. An out-of-bounds bug from vLLM.
   False Positives. M2K reports nine false positives (false dis-
covery rate of 4.74%), arising from three sources. First, six      were reported by users without model information, we eval-
stem from HFProbe’s inability to track tensor values across        uate only cuKLEE. We retain inputs required by the model
kernels: it returns zero-value tensors for kernel binding func-    architecture, if any, and treat the rest as symbolic when run-
tions, so subsequent kernel bindings cannot track valid value      ning cuKLEE.
ranges for those tensors, causing two integer-overflows,              We compare cuKLEE with three static CUDA analysis
three out-of-bounds, and one data-race false positives. Sec-       tools: Honeycomb’s validator [49], GKLEE [41], and ESBMC-
ond, two involve kernels that index tensors using values           GPU [62]. These tools cannot run directly on vLLM kernels
loaded from model weights. As HFProbe does not load the            due to incompatibilities with modern C++, CUDA, and Py-
actual weights, it cannot accurately capture the indices; man-     Torch/vLLM libraries. Moreover, GKLEE and ESBMC-GPU
ual inspection confirms that the true weight values cannot         require a main() function as their entry point, which vLLM
trigger errors. Third, M2K identifies one benign race, as dis-     kernels lack. To enable comparison, we simplify the vLLM
cussed earlier.                                                    kernels by rewriting modern CUDA and C++ features with
   Memory Bugs vs. GPU Memory. Figure 5 shows how de-              legacy constructs, removing PyTorch and vLLM dependen-
tected bugs vary with GPU memory size, which cuKLEE                cies, and adding a main() function for each kernel that re-
uses to decide whether a bug can be triggered. Out-of-bounds       places the original wrapper and allocates GPU memory for
bugs plateau beyond 80GB, whereas integer overflows grow           tensors. The simplified kernels preserve the root causes of
with larger memory. On the NVIDIA H100 (80GB), M2K finds           the bugs. Because Honeycomb targets HIP kernels [4], we
68 integer overflows and 19 out-of-bounds bugs; on the H200        additionally translate CUDA APIs to HIP equivalents us-
(141GB), integer overflows rise to 119 while out-of-bounds         ing hipify-perl [3]. We do not compare with other related
bugs remain unchanged; on the B300 (288GB), integer over-          tools because they are not free [14, 59] or their code is not
flows further increase to 162. This trend suggests that future     available [11, 40, 42, 45].
GPUs with larger memory will expose more integer overflow          6.2.2 Experimental Results. As shown in Table 6, cuK-
bugs.                                                              LEE identifies 15 of the 20 known bugs, demonstrating strong
   Time and Monetary Cost. M2K takes 1,073.62 total hours          coverage of real memory errors in CUDA kernels. Specifically,
to complete its analysis: 1,032.99 for vLLM, 28.18 for Hugging     the detected bugs comprise nine integer overflows, five out-
Face, and 12.45 for research papers. Experiments run with          of-bounds accesses, and one null-pointer dereference, under-
multiple parallel processes, and the reported time reflects        scoring cuKLEE’s ability to detect the three bug classes.
their aggregate. Using GPT costs $442.16. Considering that             Figure 6 shows an out-of-bounds error. The wrapper func-
both the Python and CUDA codebases exceed 100,000 lines,           tion (omitted for brevity) allocates shared memory to record
M2K incurs moderate time and monetary costs.                       how threads assign tokens to experts. As shown on line 2,
   More specifically, cuKLEE consumes 979.86 hours, substan-       the first num_experts + 1 entries store the total token count
tially more than HFProbe (93.76 hours). HFProbe generates          and the per-expert counts. The remaining entries form a 2D
1,274 distinct model configurations. Because many vLLM             array storing per-thread, per-expert token routing plus one
kernels are shared across models, we merge identical anal-         slot per expert for the expert’s total. Line 5 attempts to skip
ysis contexts, yielding 8,562 unique contexts for cuKLEE.          this first region so that lines 7–9 operate on the second, but
Kernel analysis completes within one hour for 7,784 cases          incorrectly uses the thread count (blockDim.x), instead of
and reaches the limit for 778 cases. All kernels exceeding the     expert count, to compute the offset. As marked on line 1,
one-hour limit contain 600+ lines of CUDA code.                    when the expert count is below 32, the thread count exceeds
Answer to effectiveness: M2K can accurately detect inte-           it, leading to a buffer overflow on line 8. cuKLEE correctly
ger overflows and buffer overflows in CUDA kernels used within     reports this, with threadIdx.x=31 and num_experts=8.
LLM inference systems.                                                 The missed bugs arise for four reasons. First, one null-
                                                                   pointer dereference occurs because the kernel accesses data
6.2     Coverage and Advancement                                   on a different GPU, undetectable via static analysis. Second,
6.2.1 Methodology. We evaluate coverage using the 20               one out-of-bounds is caused by a mismatch between a ten-
known vLLM bugs from Section 2.3. Since most of the bugs           sor’s declared shape and the underlying memory layout;
cuKLEE assumes consistency between them and thus misses
the issue. Third, two bugs exceed the one-hour analysis limit
and remain undetected. Fourth, cuKLEE lacks support for
C++ std::map, causing it to miss one bug that depends on
this construct. For the simplified kernels, cuKLEE still misses
the first bug but successfully identifies the other four.
   Honeycomb detects no bugs because it only checks whether
memory accesses stay within one of four coarse memory             Figure 7. Contributions of M2K’s components. (26 bugs de-
regions (protected, read-only, read-write, and private). All      tected in vLLM. W.O.: without, C: cuKLEE, H: HFProbe, M:
tested out-of-bounds accesses fall inside the read-write re-      configuration mutation, and V: Validation.)
gion, so Honeycomb cannot catch them.
                                                                  However, this tensor always has one element in reality, mak-
   GKLEE detects four out-of-bounds accesses and one in-
                                                                  ing such a case infeasible. Second, cuKLEE may treat ten-
teger overflow, but misses the rest for three reasons. First,
                                                                  sor shape values or other parameters as having extremely
seven bugs require threadIdx.x or blockIdx.x to exceed
                                                                  large, unrealistic values (e.g., a hidden size of 2,147,483,640).
30, but GKLEE assumes small constant values for both. Sec-
                                                                  Moreover, without model-architecture information, all ten-
ond, GKLEE fully unrolls loops, causing the analysis of seven
                                                                  sor shapes become symbolic, forcing cuKLEE to explore far
bugs to hit the one-hour timeout. Third, GKLEE cannot de-
                                                                  more possibilities. As a result, it fails to complete the analysis
tect the bug due to the kernel and its data on different GPUs.
                                                                  of 25 kernels within one hour, 18 more than when archi-
   ESBMC-GPU identifies two out-of-bounds accesses and
                                                                  tecture information is available, and increases the average
one integer overflow. It misses nine, seven, and one bugs
                                                                  analysis time per kernel by 2.1×. The six missed bugs are
respectively for the same reasons as GKLEE.
                                                                  due to this reason.
Answer to coverage and advancement: cuKLEE detects                   With cuKLEE disabled, no runtime errors are detected, so
most of the tested known bugs, substantially more than the        this variant reports nothing. Our experiments use a maxi-
baselines, demonstrating its strong coverage of real CUDA         mum batch size of 5 and a sequence length of 17 (only 85
memory bugs and its advantages over existing techniques.          tokens in total), far too few to expose hidden bugs. This
                                                                  shows that M2K uncovers issues that would otherwise ap-
6.3   Rationality of Components                                   pear only at large production scales.
6.3.1 Methodology. We conduct an ablation study by dis-              Without configuration mutation, only 21 of the 50 CUDA
abling individual components of M2K and comparing each            kernels are exercised, leading M2K to miss 19 bugs.
variant against the full system. We use the same vLLM mod-           Disabling validation causes M2K to report 15 more false
els, kernels, and experimental setup as in Section 6.1, making    positives. Five are cases where the token count is too large,
the results directly comparable to those reported there. The      causing memory usage to exceed the B300’s memory size.
variants are: ○1 Without HFProbe. We run cuKLEE directly on       The remaining ten cases should be filtered out by rerunning
kernel wrapper functions without guidance from HFProbe.           the profiling backend with the batch size and sequence length
○2 Without cuKLEE. We execute each model on real GPUs             reported by the solver.
using both original and mutated configurations, and record        Answer to rationality: Each component of M2K plays a
runtime errors (e.g., “illegal memory access”). Experiments       distinct and essential role in its overall effectiveness.
are parallelized across four RTX 5090s and four H100s; since
only error occurrence is checked, hardware differences do         7    Limitations and Discussion
not affect results. ○
                    3 Without configuration mutation. We run
                                                                  M2K currently targets Hugging Face models and CUDA
M2K on the collected config.json files and frameworks’ de-
                                                                  kernels with tensor inputs, which together cover a large
fault configurations, without any mutations. ○  4 Without val-
                                                                  share of real-world usage. It profiles kernel usage without
idation. All bugs reported by symbolic execution are treated
                                                                  executing kernels on any specific GPU, making its effec-
as final outputs without validation.
                                                                  tiveness independent of any GPU hardware. M2K also sup-
6.3.2 Experimental Results. The full-featured version             ports GPU-dependent conditional compilation through cross-
of M2K detects the most bugs in Figure 7, demonstrating the       compilation and can handle fused kernels when the fused
value of each component.                                          source code is available. At present, M2K does not support
   Removing HFProbe causes cuKLEE to report 2,349 false           Triton kernels, NPU kernels, or TensorFlow models. How-
positives for two reasons. First, cuKLEE may infer tensor         ever, applying its core idea of an explicit model-kernel inter-
shapes that are theoretically possible but never occur in real-   face to these settings is promising for uncovering potential
ity, leading to incorrect out-of-bounds reports. For example,     issues.
in Figure 2c, cuKLEE incorrectly assigns tensor scale a zero         M2K mutates execution configurations to trigger addi-
size to trigger out-of-bounds access on line 4 of Figure 2d.      tional CUDA kernels. It does not aim to cover all possible
models, nor is this necessary. In practice, users care about         than cuKLEE. Commercial static tools also exist [14, 59], but
the specific model they deploy, rather than whether a kernel         their technical details are unavailable for analysis.
behaves correctly under every possible model. M2K there-                 Dynamic Techniques. NVIDIA provides several mecha-
fore focuses on the kernel shapes exercised by a given model.        nisms to enforce GPU memory safety. The GPU MMU reports
Although our results show that the mutation is effective,            “illegal memory access” errors when unmapped virtual ad-
it is far from a systematic inspection. Developing a more            dresses are accessed [51]. CUDA-MEMCHECK [54] and its
comprehensive inspection method remains future work.                 successor Compute Sanitizer [55] record metadata for GPU
    In our experiments, cuKLEE analyzes each kernel for up           buffers, enabling detection of a broader range of memory
to one hour. For certain kernels (e.g., gptq_marlin_gemm()),         errors at the cost of increased runtime overhead.
not all paths are explored, potentially missing memory bugs.             Researchers have also devoted efforts along this direc-
Since cuKLEE inherits KLEE’s path exploration strategies de-         tion. GPUShield [37], GPUArmor [87], cuCatch [70], and
signed for C/C++, optimizing them for CUDA code patterns             LAK [77] build on principles similar to Compute Sanitizer,
is key to improving effectiveness.                                   with the first three emphasizing lower runtime overhead
    Most bugs detected by M2K are integer overflows. Al-             and the latter using lock-key metadata to provide stronger
though such bugs look simple, we are not aware of a simpler          memory safety. GMOD [20, 21] pads memory buffers and
way to resolve them. First, a static technique must track the        detects overflows by monitoring changes to the padding.
numerical relations among variables, the path constraints            IMT [69] and LMI [36] ensure GPU memory safety with
under which these relations hold, and the constraints im-            ECC and unused upper bits of pointers, respectively. Race
posed by the model and the framework; without this infor-            detection tools, including BARRACUDA [22], GRace [83],
mation, it inevitably reports many false positives. Second,          GMRace [84], and LDetector [44], track the last-accessing
a dynamic technique must synthesize kernel inputs satis-             thread for each memory location and identify unsynchro-
fying the model’s constraints and run them on real GPU               nized concurrent accesses. Despite these advances, these
hardware, both of which are hard to automate. Moreover, as           techniques rely on specific inputs to trigger bugs, require
our experiments show, most overflows silently corrupt com-           instrumentation or hardware support, and many incur large
putation results, making them difficult to detect dynamically.       runtime overhead.
Third, simply using 64-bit integers everywhere is not an                 Fuzzing techniques have also been proposed for CUDA
ideal solution because it increases both runtime and memory          kernels and machine learning libraries [43, 48, 58, 68]. How-
overhead. M2K overcomes these difficulties by combining              ever, they overlook kernel usage context within LLM infer-
dynamic profiling with static symbolic execution, enabling           ence systems or target inference frameworks rather than
it to detect integer overflows both effectively and precisely.       CUDA kernels. They are ineffective in detecting memory
                                                                     bugs in CUDA kernels used in LLM inference systems.


8    Related Work
Exploiting CUDA Memory Bugs. Prior work shows that                   9   Conclusion
CUDA memory bugs are highly exploitable [27, 66]. They               This paper presents M2K, an automated tool combining dy-
can enable control-flow hijacking [19, 52], mind-control at-         namic model profiling with CUDA-specialized symbolic ex-
tacks [60], and side-channel attacks [53, 63, 80], leading to        ecution to detect CUDA memory bugs in LLM inference
severe inference degradation or arbitrary code execution.            systems. M2K identifies 181 CUDA memory bugs in popular
These findings motivate our systematic analysis of CUDA              LLM inference systems when they perform inference with
kernels to detect memory bugs in them.                               real models, demonstrating its practical effectiveness. Future
   Static techniques have been developed to analyze CUDA             work can improve the efficiency of symbolic execution for
kernels. ProofWright [11] verifies kernels against specifica-        CUDA kernels and extend M2K to support NPU kernels.
tions generated by LLMs. COVT [46] translates CUDA into
C/C++ and then detects integer and buffer overflows. Hon-
eycomb’s validator [49] ensures memory accesses remain
within predefined coarse-grained regions. Tong et al. ex-            Acknowledgments
tend Dartagnan with GPU consistency models [72]. Methods             We thank the anonymous reviewers and shepherd for their
based on symbolic execution have also been proposed [6, 40–          insightful feedback and valuable suggestions, and Yotta Labs
42, 45, 62]. Overall, these static techniques struggle with dy-      for providing the compute resources. This work was sup-
namically sized memory buffers, do not support the widely            ported in part by the U.S. National Science Foundation (NSF)
used Tensor library, and cannot handle varied kernel launch          under awards CNS-1955965 and CCF-2145394, and by the
configurations. We evaluate three of them [41, 49, 62] in Sec-       National Natural Science Foundation of China under grant
tion 6.2 and find they are limited in usability and less effective   92582108. Linhai Song is the corresponding author.
References                                                                       [21] Bang Di, Jianhua Sun, Dong Li, Hao Chen, and Zhe Quan. 2018. GMOD:
 [1] Eleni Adamopoulou and Lefteris Moussiades. 2020. Chatbots: History,              A Dynamic GPU Memory Overflow Detector. In Proceedings of the
     technology, and applications. Machine Learning with Applications 2               27th International Conference on Parallel Architectures and Compilation
     (2020), 100006.                                                                  Techniques (PACT ’18). Limassol, Cyprus.
 [2] Eleni Adamopoulou and Lefteris Moussiades. 2020. An overview                [22] Ariel Eizenberg, Yuanfeng Peng, Toma Pigli, William Mansky, and
     of chatbot technology. In Proceedings of the 16th IFIP International             Joseph Devietti. 2017. BARRACUDA: binary-level analysis of run-
     Conference on Artificial Intelligence Applications and Innovations (AIAI         time RAces in CUDA programs. In Proceedings of the 38th ACM SIG-
     ’20). Neos Marmaras, Greece.                                                     PLAN Conference on Programming Language Design and Implementa-
 [3] Advanced Micro Devices, Inc. 2025. hipify-perl. https://rocm.docs.               tion (PLDI ’17). Barcelona, Spain.
     amd.com/projects/HIPIFY/en/latest/hipify-perl.html.                         [23] Hugging Face. 2025. Qwen2-0.5B-Instruct/config.json.             https://
 [4] Advanced Micro Devices, Inc. 2025. What is HIP? https://rocm.docs.               huggingface.co/Qwen/Qwen2-0.5B-Instruct/blob/main/config.json.
     amd.com/projects/HIP/en/latest/index.html.                                  [24] Hugging Face. 2026. The AI community building the future. https:
 [5] Keqin Bao, Jizhi Zhang, Yang Zhang, Wenjie Wang, Fuli Feng, and                  //huggingface.co/.
     Xiangnan He. 2023. Large language models for recommendation:                [25] Hugging Face. 2026. Transformers. https://huggingface.co/docs/
     Progresses and future directions. In Proceedings of the 1st International        transformers/en/index.
     ACM SIGIR Conference on Research and Development in Information             [26] Google. 2026. Gemini 3.1 Pro Preview. https://ai.google.dev/gemini-
     Retrieval in the Asia Pacific Region (SIGIR-AP ’23). Beijing, China.             api/docs/models/gemini-3.1-pro-preview.
 [6] Adam Betts, Nathan Chong, Alastair Donaldson, Shaz Qadeer, and Paul         [27] Yanan Guo, Zhenkai Zhang, and Jun Yang. 2024. GPU memory ex-
     Thomson. 2012. GPUVerify: a verifier for GPU kernels. In Proceedings             ploitation for fun and profit. In Proceedings of the 33rd USENIX Security
     of the 27th ACM SIGPLAN Conference on Object-Oriented Programming,               Symposium (USENIX Security ’24). Philadelphia, PA, USA.
     Systems, Languages, and Applications (OOPSLA ’12). Tucson, AZ, USA.         [28] Mengting He and Linhai Song. 2026. TokenBleed: Cross-User Token
 [7] Daniil A Boiko, Robert MacKnight, and Gabe Gomes. 2023. Emergent                 Leakage via Integer Overflow in CUDA Kernels. https://youtu.be/F-
     autonomous scientific research capabilities of large language models.            SQ7ii7ob4.
     arXiv preprint arXiv:2304.05332 (2023).                                     [29] Mengting He and Linhai Song. 2026. TokenSmash: Exploiting CUDA
 [8] Rishi Bommasani. 2021. On the opportunities and risks of foundation              Kernel Buffer Overflows to Manipulate LLM Inference. https://www.
     models. arXiv preprint arXiv:2108.07258 (2021).                                  youtube.com/watch?v=ZhKBPK7BeZ0.
 [9] Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan, Johannes               [30] David Holtz and Daniël de Kok. 2025. From Zero to GPU: A Guide
     Gehrke, Eric Horvitz, Ece Kamar, Peter Lee, Yin Tat Lee, Yuanzhi Li,             to Building and Scaling Production-Ready CUDA Kernels. https:
     Scott Lundberg, et al. 2023. Sparks of artificial general intelligence:          //huggingface.co/blog/kernel-builder.
     Early experiments with GPT-4. arXiv preprint arXiv:2303.12712 (2023).       [31] Edmund Horner, David Fraser, Juha Jeronen, and Patrick Massot. 2020.
[10] Cristian Cadar, Daniel Dunbar, and Dawson Engler. 2008. KLEE: unas-              pyan: Static call-dependency graph generator for Python. https:
     sisted and automatic generation of high-coverage tests for complex               //github.com/davidfraser/pyan.
     systems programs. In Proceedings of the 8th USENIX Conference on            [32] Wei Huang, Yue Liao, Jianhui Liu, Ruifei He, Haoru Tan, Shiming
     Operating Systems Design and Implementation (OSDI ’08). San Diego,               Zhang, Hongsheng Li, Si Liu, and Xiaojuan Qi. 2025. Mixture Com-
     CA, USA.                                                                         pressor for Mixture-of-Experts LLMs Gains More. In Proceedings of the
[11] Bodhisatwa Chatterjee, Drew Zagieboylo, Sana Damani, Siva Hari,                  13th International Conference on Learning Representations (ICLR ’25).
     and Christos Kozyrakis. 2025. ProofWright: Towards Agentic Formal                Singapore.
     Verification of CUDA. arXiv preprint arXiv:2511.12294 (2025).               [33] Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim, and Sunghun Kim.
[12] Mark Chen. 2021. Evaluating large language models trained on code.               2024. A survey on large language models for code generation. arXiv
     arXiv preprint arXiv:2107.03374 (2021).                                          preprint arXiv:2406.00515 (2024).
[13] Claude. 2026. Models overview. https://platform.claude.com/docs/en/         [34] Yunho Kim, Moonzoo Kim, Young Joo Kim, and Yoonkyu Jang. 2012.
     about-claude/models/overview.                                                    Industrial application of concolic testing approach: A case study on
[14] The Qt Company. 2025. CUDA Code Verification for Safety-Critical                 libexif by using CREST-BV and KLEE. In Proceedings of the 34th Inter-
     Systems. https://www.qt.io/quality-assurance/axivion-for-cuda.                   national Conference on Software Engineering (ICSE ’12). Zurich, Switzer-
[15] NVIDIA Corporation. 2025. CUDA C++ programming guide. https:                     land.
     //docs.nvidia.com/cuda/pdf/CUDA_C_Programming_Guide.pdf.                    [35] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin
[16] Sumit Kumar Dam, Choong Seon Hong, Yu Qiao, and Chaoning Zhang.                  Zheng, Cody Hao Yu, Joseph E. Gonzalez, Hao Zhang, and Ion Sto-
     2024. A Complete Survey on LLM-based AI Chatbots. arXiv preprint                 ica. 2023. Efficient Memory Management for Large Language Model
     arXiv:2406.16937 (2024).                                                         Serving with PagedAttention. In Proceedings of the 29th ACM SIGOPS
[17] Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, and Christopher Ré.            Symposium on Operating Systems Principles (SOSP ’23). Koblenz, Ger-
     2022. FlashAttention: Fast and memory-efficient exact attention with             many.
     IO-awareness. In Advances in Neural Information Processing Systems          [36] Jaewon Lee, Euijun Chung, Saurabh Singh, Seonjin Na, Yonghae Kim,
     35 (NeurIPS ’22). New Orleans, LA, USA.                                          Jaekyu Lee, and Hyesoon Kim. 2025. Let-Me-In: (Still) Employing
[18] Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: an efficient SMT                In-pointer Bounds Metadata for Fine-grained GPU Memory Safety.
     solver. In Proceedings of the 14th International Conference on Tools and         In 2025 IEEE International Symposium on High Performance Computer
     Algorithms for the Construction and Analysis of Systems (ETAPS ’08).             Architecture (HPCA). IEEE, 1648–1661.
     Budapest, Hungary.                                                          [37] Jaewon Lee, Yonghae Kim, Jiashen Cao, Euna Kim, Jaekyu Lee, and
[19] Bang Di, Jianhua Sun, and Hao Chen. 2016. A study of overflow vulner-            Hyesoon Kim. 2022. Securing GPU via region-based bounds checking.
     abilities on GPUs. In Proceedings of the 13th IFIP WG 10.3 International         In Proceedings of the 49th Annual International Symposium on Computer
     Conference on Network and Parallel Computing (NPC ’16). Xi’an, China.            Architecture (ISCA ’22). New York, NY, USA.
[20] Bang Di, Jianhua Sun, Hao Chen, and Dong Li. 2020. Efficient buffer         [38] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir
     overflow detection on GPU. IEEE Transactions on Parallel and Dis-                Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih,
     tributed Systems 32, 5 (2020), 1161–1177.                                        Tim Rocktäschel, Sebastian Riedel, and Douwe Kiela. 2020. Retrieval-
                                                                                      augmented generation for knowledge-intensive NLP tasks. In Advances
     in Neural Information Processing Systems 33 (NeurIPS ’20). Vancouver,      [54] NVIDIA. 2022. CUDA-MEMCHECK. https://docs.nvidia.com/cuda/
     BC, Canada.                                                                     archive/11.4.4/cuda-memcheck/index.html.
[39] Aitor Lewkowycz, Anders Andreassen, David Dohan, Ethan Dyer,               [55] NVIDIA. 2025. NVIDIA Compute Sanitizer. https://developer.nvidia.
     Henryk Michalewski, Vinay Ramasesh, Ambrose Slone, Cem Anil,                    com/compute-sanitizer.
     Imanol Schlag, Theo Gutman-Solo, et al. 2022. Solving quantitative         [56] OpenAI. 2026. ChatGPT agent. https://chatgpt.com/features/agent/.
     reasoning problems with language models. In Advances in Neural             [57] OpenAI. 2026. GPT-5.4. https://developers.openai.com/api/docs/
     Information Processing Systems 35 (NeurIPS ’22). New Orleans, LA,               models/gpt-5.4.
     USA.                                                                       [58] Shiwen Ou, Yuwei Li, Lu Yu, Chengkun Wei, Tingke Wen, Qiangpu
[40] Guodong Li, Ganesh Gopalakrishnan, Robert M Kirby, and Dan Quin-                Chen, Yu Chen, Haizhi Tang, and Zulie Pan. 2025. MirrorFuzz: Leverag-
     lan. 2010. A symbolic verifier for CUDA programs. In Proceedings of             ing LLM and Shared Bugs for Deep Learning Framework APIs Fuzzing.
     the 15th ACM SIGPLAN Symposium on Principles and Practice of Parallel           IEEE Transactions on Software Engineering 52, 1 (2025), 360–375.
     Programming (PPoPP ’10). Bangalore, India.                                 [59] Parasoft. 2025. NVIDIA CUDA and Parasoft. https://www.parasoft.
[41] Guodong Li, Peng Li, Geof Sawaya, Ganesh Gopalakrishnan, Indradeep              com/integrations/nvidia-cuda/.
     Ghosh, and Sreeranga P Rajan. 2012. GKLEE: concolic verification and       [60] Sang-Ok Park, Ohmin Kwon, Yonggon Kim, Sang Kil Cha, and Hyunsoo
     test generation for GPUs. In Proceedings of the 17th ACM SIGPLAN                Yoon. 2021. Mind control attack: Undermining deep learning with
     Symposium on Principles and Practice of Parallel Programming (PPoPP             GPU memory exploitation. Computers & Security 102 (2021), 102115.
     ’12). New Orleans, LA, USA.                                                [61] Yeonhong Park, Jake Hyun, SangLyul Cho, Bonggeun Sim, and Jae W.
[42] Guodong Li, Sreeranga P. Rajan, and Indradeep Ghosh. 2013. Sym-                 Lee. 2024. Any-Precision LLM: Low-Cost Deployment of Multiple,
     bolic execution and test generation for GPU programs. U.S. Patent               Different-Sized LLMs. In Proceedings of the 41st International Conference
     US8595701B2. https://patents.google.com/patent/US8595701B2/en.                  on Machine Learning (ICML ’24). Vienna, Austria.
[43] Mingkai Li, Joseph Devietti, Suman Jana, and Tanvir Ahmed Khan.            [62] Phillipe Pereira, Higo Albuquerque, Hendrio Marques, Isabela Silva,
     2026. Challenges and Design Considerations for Finding CUDA Bugs                Celso Carvalho, Lucas Cordeiro, Vanessa Santos, and Ricardo Ferreira.
     Through GPU-Native Fuzzing. In Proceedings of the 2nd Workshop on               2016. Verifying CUDA programs using SMT-based context-bounded
     Ethical Systems and Architecture Design (HotEthics ’26). Pittsburgh, PA,        model checking. In Proceedings of the 31st ACM Symposium on Applied
     USA.                                                                            Computing (SAC ’16). Pisa, Italy.
[44] Pengcheng Li, Chen Ding, Xiaoyu Hu, and Tolga Soyata. 2014. LDetec-        [63] Roberto Di Pietro, Flavio Lombardi, and Antonio Villani. 2016. CUDA
     tor: A low overhead race detector for GPU programs. In Proceedings of           Leaks: A Detailed Hack for CUDA and a (Partial) Fix. ACM Transactions
     the 5th Workshop on Determinism and Correctness in Parallel Program-            on Embedded Computing Systems 15, 1 (2016), 1–25.
     ming (WoDet ’14). Salt Lake City, UT, USA.                                 [64] pybind11. 2025. pybind11 (v3) — Seamless interoperability between
[45] Peng Li, Guodong Li, and Ganesh Gopalakrishnan. 2014. Practical                 C++ and Python. https://pybind11.readthedocs.io/en/stable/.
     symbolic race checking of GPU programs. In Proceedings of the In-          [65] Python. 2026. ast — Abstract syntax trees. https://docs.python.org/3/
     ternational Conference for High Performance Computing, Networking,              library/ast.html.
     Storage and Analysis (SC ’14). New Orleans, LA, USA.                       [66] Jonas Roels, Adriaan Jacobs, and Stijn Volckaert. 2025. CUDA, Woulda,
[46] Wentao Li, Jianhua Sun, and Hao Chen. 2019. Detecting undefined                 Shoulda: Returning Exploits in a SASS-y World. In Proceedings of the
     behaviors in CUDA C. IEEE Access 7 (2019), 182559–182572.                       18th European Workshop on Systems Security (EuroSec ’25). Rotterdam,
[47] You Li, Zhendong Su, Linzhang Wang, and Xuandong Li. 2013. Steering             Netherlands.
     symbolic execution to less traveled paths. ACM SIGPLAN Notices 48,         [67] Vitalis Salis, Thodoris Sotiropoulos, Panos Louridas, Diomidis Spinellis,
     10 (2013), 19–32.                                                               and Dimitris Mitropoulos. 2021. PyCG: Practical Call Graph Genera-
[48] Jiawei Liu, Jinkun Lin, Fabian Ruffy, Cheng Tan, Jinyang Li, Auro-              tion in Python. In Proceedings of the 43rd International Conference on
     jit Panda, and Lingming Zhang. 2023. Nnsmith: Generating diverse                Software Engineering (ICSE ’21). Madrid, Spain.
     and valid test cases for deep learning compilers. In Proceedings of the    [68] Saurabh Singh, Ruobing Han, Jaewon Lee, Seonjin Na, Yonghae
     28th ACM International Conference on Architectural Support for Pro-             Kim, Taesoo Kim, and Hyesoon Kim. 2026. CuFuzz: Hardening
     gramming Languages and Operating Systems (ASPLOS ’23). Vancouver,               CUDA Programs through Transformation and Fuzzing. arXiv preprint
     Canada.                                                                         arXiv:2601.01048 (2026).
[49] Haohui Mai, Jiacheng Zhao, Hongren Zheng, Yiyang Zhao, Zibin Liu,          [69] Michael B Sullivan, Mohamed Tarek Ibn Ziad, Aamer Jaleel, and
     Mingyu Gao, Cong Wang, Huimin Cui, Xiaobing Feng, and Christos                  Stephen W Keckler. 2023. Implicit memory tagging: No-overhead
     Kozyrakis. 2023. Honeycomb: Secure and efficient GPU executions                 memory safety using alias-free tagged ECC. In Proceedings of the 50th
     via static validation. In Proceedings of the 17th USENIX Symposium on           Annual International Symposium on Computer Architecture (ISCA ’23).
     Operating Systems Design and Implementation (OSDI ’23). Boston, MA,             Orlando, FL, USA.
     USA.                                                                       [70] Mohamed Tarek Ibn Ziad, Sana Damani, Aamer Jaleel, Stephen W.
[50] Vladimir Malinovskii, Denis Mazur, Ivan Ilin, Denis Kuznedelev, Kon-            Keckler, and Mark Stephenson. 2023. cuCatch: A Debugging Tool for
     stantin Burlachenko, Kai Yi, Dan Alistarh, and Peter Richtárik. 2024.           Efficiently Catching Memory Safety Violations in CUDA Applications.
     PV-Tuning: Beyond Straight-Through Estimation for Extreme LLM                   In Proceedings of the 44th ACM SIGPLAN Conference on Programming
     Compression. In Advances in Neural Information Processing Systems 37            Language Design and Implementation (PLDI ’23). Orlando, Florida, USA.
     (NeurIPS ’24). Vancouver, Canada.                                          [71] Gemini Team, Petko Georgiev, Ving Ian Lei, Ryan Burnell, Libin Bai,
[51] Microsoft. 2025. GpuMmu model. https://learn.microsoft.com/en-                  Anmol Gulati, Garrett Tanzer, Damien Vincent, Zhufeng Pan, Shibo
     us/windows-hardware/drivers/display/gpummu-model.                               Wang, et al. 2024. Gemini 1.5: Unlocking multimodal understanding
[52] Andrea Miele. 2016. Buffer overflow vulnerabilities in CUDA: a prelim-          across millions of tokens of context. arXiv preprint arXiv:2403.05530
     inary analysis. Journal of Computer Virology and Hacking Techniques             (2024).
     12, 2 (2016), 113–120.                                                     [72] Haining Tong, Natalia Gavrilenko, Hernan Ponce de Leon, and Keijo
[53] Hoda Naghibijouybari, Ajaya Neupane, Zhiyun Qian, and Nael Abu-                 Heljanko. 2024. Towards Unified Analysis of GPU Consistency. In
     Ghazaleh. 2018. Rendered Insecure: GPU Side Channel Attacks are                 Proceedings of the 29th ACM International Conference on Architectural
     Practical. In Proceedings of the 2018 ACM SIGSAC Conference on Com-             Support for Programming Languages and Operating Systems (ASPLOS
     puter and Communications Security (CCS ’18) (Toronto, Canada).                  ’24). San Diego, CA, USA.
[73] vLLM. 2026. Cross-User Data Leak Vulnerability. https://github.com/
     vllm-project/vllm/security/advisories/GHSA-7m6h-x95x-82q5.
[74] Hanchen Wang, Tianfan Fu, Yuanqi Du, Wenhao Gao, Kexin Huang,
     Ziming Liu, Payal Chandak, Shengchao Liu, Peter Van Katwyk, An-
     dreea Deac, et al. 2023. Scientific discovery in the age of artificial
     intelligence. Nature 620, 7972 (2023), 47–60.
[75] Likang Wu, Zhi Zheng, Zhaopeng Qiu, Hao Wang, Hongchao Gu,
     Tingjia Shen, Chuan Qin, Chen Zhu, Hengshu Zhu, Qi Liu, Hui Xiong,
     and Enhong Chen. 2024. A survey on large language models for
     recommendation. World Wide Web 27, 5 (2024).
[76] Haoran You, Yipin Guo, Yichao Fu, Wei Zhou, Huihong Shi, Xiaofan
     Zhang, Souvik Kundu, Amir Yazdanbakhsh, and Yingyan Celine Lin.
     2024. ShiftAddLLM: Accelerating Pretrained LLMs via Post-Training
     Multiplication-less Reparameterization. In Advances in Neural Infor-
     mation Processing Systems 37 (NeurIPS ’24). Vancouver, Canada.
[77] Chaochao Zhang and Rui Hou. 2022. LAK: A low-overhead lock-and-
     key based schema for GPU memory safety. In Proceedings of the 2022
     IEEE 40th International Conference on Computer Design (ICCD ’22). Lake
     Tahoe, NV, USA.
[78] Gang Zhang and Jin Wuxia. 2019. Depends is a fast, comprehensive
     code dependency analysis tool. https://github.com/multilang-depends/
     depends.
[79] Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yu-
     peng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong, Yi-
     fan Du, Chen Yang, Yushuo Chen, Zhipeng Chen, Jinhao Jiang, Ruiyang
     Ren, Yifan Li, Xinyu Tang, Zikang Liu, Peiyu Liu, Jian-Yun Nie, and
     Ji-Rong Wen. 2023. A survey of large language models. arXiv preprint
     arXiv:2303.18223 (2023).
[80] Yu Zhao, Wenjie Xue, Weijie Chen, Weizhong Qiang, Deqing Zou, and
     Hai Jin. 2024. Owl: differential-based side-channel leakage detection
     for CUDA applications. In Proceedings of the 54th Annual IEEE/IFIP
     International Conference on Dependable Systems and Networks (DSN
     ’24). Brisbane, Queensland, Australia.
[81] Zihuai Zhao, Wenqi Fan, Jiatong Li, Yunqing Liu, Xiaowei Mei, Yiqi
     Wang, Zhen Wen, Fei Wang, Xiangyu Zhao, Jiliang Tang, et al. 2024.
     Recommender systems in the era of large language models (LLMs).
     IEEE Transactions on Knowledge and Data Engineering 36, 11 (2024),
     6889–6907.
[82] Lianmin Zheng, Liangsheng Yin, Zhiqiang Xie, Chuyue Sun, Jeff
     Huang, Cody Hao Yu, Shiyi Cao, Christos Kozyrakis, Ion Stoica,
     Joseph E. Gonzalez, Clark Barrett, and Ying Sheng. 2024. SGLang: effi-
     cient execution of structured language model programs. In Advances
     in Neural Information Processing Systems 37 (NeurIPS ’24). Vancouver,
     BC, Canada.
[83] Mai Zheng, Vignesh T. Ravi, Feng Qin, and Gagan Agrawal. 2011.
     GRace: a low-overhead mechanism for detecting data races in GPU
     programs. In Proceedings of the 16th ACM Symposium on Principles and
     Practice of Parallel Programming (PPoPP ’11). San Antonio, TX, USA.
[84] Mai Zheng, Vignesh T. Ravi, Feng Qin, and Gagan Agrawal. 2014.
     GMRace: Detecting Data Races in GPU Programs via a Low-Overhead
     Scheme. IEEE Transactions on Parallel and Distributed Systems 25, 1
     (2014), 104–115.
[85] Zibin Zheng, Kaiwen Ning, Yanlin Wang, Jingwen Zhang, Dewu Zheng,
     Mingxi Ye, and Jiachi Chen. 2023. A survey of large language models
     for code: Evolution, benchmarking, and future trends. arXiv preprint
     arXiv:2311.10372 (2023).
[86] Yutao Zhu, Huaying Yuan, Shuting Wang, Jiongnan Liu, Wenhan Liu,
     Chenlong Deng, Haonan Chen, Zheng Liu, Zhicheng Dou, and Ji-Rong
     Wen. 2025. Large language models for information retrieval: A survey.
     ACM Transactions on Information Systems 44, 1 (2025), 1–54.
[87] Mohamed Tarek Ibn Ziad, Sana Damani, Mark Stephenson, Stephen W
     Keckler, and Aamer Jaleel. 2025. GPUArmor: A Hardware-Software
     Co-design for Efficient and Scalable Memory Safety on GPUs. arXiv
     preprint arXiv:2502.17780 (2025).
