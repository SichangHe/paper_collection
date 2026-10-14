                                                      KF ORGE : P ROGRAM S YNTHESIS FOR D IVERSE AI H ARDWARE
                                                                           ACCELERATORS

                                                                                                     A P REPRINT



                                                    Taras Sereda 1 Tom St. John 1 Burak Bartan 1 Natalie Serrino 1 Sachin Katti 1 2 Zain Asgar 1 3
arXiv:2511.13274v1 [cs.LG] 17 Nov 2025




                                                                                                    A BSTRACT
                                                 GPU kernels are critical for ML performance but difficult to optimize across diverse accelerators. We present
                                                 KForge, a platform-agnostic framework built on two collaborative LLM-based agents: a generation agent that
                                                 produces and iteratively refines programs through compilation and correctness feedback, and a performance
                                                 analysis agent that interprets profiling data to guide optimization. This agent-based architecture requires only a
                                                 single-shot example to target new platforms.
                                                 We make three key contributions: (1) introducing an iterative refinement system where the generation agent
                                                 and performance analysis agent collaborate through functional and optimization passes, interpreting diverse
                                                 profiling data (from programmatic APIs to GUI-based tools) to generate actionable recommendations that guide
                                                 program synthesis for arbitrary accelerators; (2) demonstrating that the generation agent effectively leverages
                                                 cross-platform knowledge transfer, where a reference implementation from one architecture substantially improves
                                                 generation quality for different hardware targets; and (3) validating the platform-agnostic nature of our approach by
                                                 demonstrating effective program synthesis across fundamentally different parallel computing platforms: NVIDIA
                                                 CUDA and Apple Metal.

                                         1       I NTRODUCTION                                                synthesis or recognition systems.
                                         Writing high-performance compute kernels requires master-            Compilers such as torch.compile (Ansel et al., 2024)
                                         ing domain-specific languages such as CUDA (NVIDIA),                 and TensorRT-LLM (NVIDIA, 2023) greatly speed up neu-
                                         OpenCL (Khronos Group), Metal (Apple Inc., 2014), or Tri-            ral computation graphs by leveraging automatic kernel fu-
                                         ton (Tillet et al., 2019). Porting kernels across accelerators       sion, dynamic shape specialization, and graph optimiza-
                                         is extremely challenging and requires fundamental algorith-          tions.
                                         mic restructuring. A kernel optimized for NVIDIA’s H100              Nevertheless, building high-performance kernels, as demon-
                                         cannot be easily adapted for AMD’s MI300X or Apple’s M-              strated by FlashAttention (Dao et al., 2022; Dao, 2023),
                                         series chips, as each platform demands architecture-specific         requires combining clever algorithmic techniques with care-
                                         optimizations.                                                       ful hardware utilization. Specifically, integrating online
                                         Most models have optimized implementations for NVIDIA’s              softmax (Milakov & Gimelshein, 2018) with tiled attention
                                         hardware because training is usually conducted on NVIDIA             computation, while leveraging hardware-specific instruc-
                                         accelerators. However, a growing number of neural net-               tions, enables superior performance. Together, these opti-
                                         work workloads are running on various accelerators both              mizations reduce kernel scheduling overhead and optimize
                                         in the cloud and on edge devices, such as smartphones or             memory access patterns, maximizing arithmetic intensity
                                         laptops, where users increasingly run inference tasks, such          while minimizing memory pipeline bubbles.
                                         as on-device language models, computer vision, and speech            This work explores whether large language models (LLMs)
                                             1
                                               Gimlet Labs, San Francisco, California, USA 2 Department       can generate kernel programs for multiple hardware acceler-
                                         of Electrical Engineering, Stanford University, Stanford, Califor-   ators, leveraging both algorithmic and hardware-specific op-
                                         nia, USA 3 Department of Computer Science, Stanford Univer-          timizations. We target two distinct ecosystems: NVIDIA’s
                                         sity, Stanford, California, USA. Correspondence to: Taras Sereda     CUDA with its mature tooling and comprehensive Py-
                                         <taras@gimletlabs.ai>.
                                                                                                              Torch (Paszke et al., 2019) support, and Apple’s Metal for
                                                                                                              Silicon GPUs with limited programmatic profiling capabili-
                                                                                                              ties.
                                KForge: Program Synthesis for Diverse AI Hardware Accelerators




Figure 1. Iterative program synthesis and optimization loop using LLMs. The workflow consists of two main phases: (1) a functional pass
that iteratively refines synthesized programs until the code compiles, executes without errors, and produces correct output, and (2) an
optimization pass that provides performance feedback to the LLM for iterative performance improvement.


We propose an agentic program synthesis framework, de-               Liger Kernel (Hsu et al., 2025) provides production-ready
scribed in Figure 1 to mirror the real-world workflow of             Triton kernels for LLM training, achieving 20% throughput
kernel engineers, who typically first make sure that kernel          increase and 60% memory reduction through kernel fusion
implementation is functionally correct. The kernel is then it-       and optimization. Unlike automated approaches, it offers
eratively optimized using hardware utilization metrics such          curated, hand-optimized kernels for common operations like
as memory bandwidth utilization, warp occupancy, or ker-             RMSNorm and SwiGLU.
nel arithmetic intensity. This setup allows the model to first
                                                                      KernelLLM (Fisches et al., 2025) fine-tuned an 8B param-
arrive at a functionally correct program that is later incre-
                                                                      eter model based on Llama 3.1 Instruct specifically for
mentally improved based on previous attempts, simulating
                                                                      translating PyTorch modules into Triton kernels, achieving
a practical development loop.
                                                                      competitive performance on KernelBench-Triton despite its
                                                                      smaller size compared to general-purpose models.
2    R ELATED W ORK
                                                                     FlashInfer (Ye et al., 2025) demonstrates automated ker-
Recent work has explored using LLMs to automate GPU                  nel generation through Just-In-Time (JIT) compilation that
kernel generation and optimization, addressing the challenge         translates high-level attention specifications into optimized
of writing efficient kernels for machine learning workloads.         CUDA kernels, achieving 29-69% latency reductions in
                                                                     LLM serving benchmarks. Their system uses a unified
KernelBench (Ouyang et al., 2025) introduced a benchmark
                                                                     block-sparse format and dynamic scheduling to handle di-
framework with 250 PyTorch workloads to evaluate LLMs’
                                                                     verse attention patterns, with successful integration into
ability to generate efficient GPU kernels. The benchmark
                                                                     production frameworks such as SGLang (Zheng et al.,
uses a f astp metric measuring both correctness and speedup
                                                                     2024) and vLLM (Kwon et al., 2023). The template-
over baseline implementations. Results show that even fron-
                                                                     based approach separates algorithmic logic from hardware-
tier reasoning models match PyTorch baseline performance
                                                                     specific optimizations, providing valuable insights for cross-
in fewer than 20% of cases, revealing a critical trade-off
                                                                     platform kernel generation beyond NVIDIA hardware.
between optimization complexity and correctness.
                                                                      CUDA-LLM (Chen et al., 2025) suggests a Feature Search
Sakana AI’s CUDA Engineer (Lange et al., 2025) presented
                                                                      and Reinforcement (FSR) framework that addresses the
an agentic framework for automatic CUDA kernel discovery
                                                                      challenge of LLM-generated CUDA kernels often being
using evolutionary optimization. Initially claiming 10-100x
                                                                      syntactically correct but performance suboptimal. The FSR
speedups over PyTorch operations, the system was later
                                                                      framework employs a multidimensional validation pipeline
found to exploit evaluation framework vulnerabilities (“re-
                                                                      consisting of compilation verification, functional correct-
ward hacking”), leading to inflated performance claims. The
                                                                      ness testing through reference output comparison, and em-
project released a dataset of 30,000+ generated kernels, but
                                                                      pirical performance profiling on target hardware. The sys-
highlighted the challenges of robust evaluation in automated
                                                                      tem iteratively refines prompts by incorporating compilation
optimization.
                                KForge: Program Synthesis for Diverse AI Hardware Accelerators

error messages when kernels fail to compile, or by adding           as input and returns the generated code k ∈ T . The gener-
performance optimization hints when kernels are function-           ated code is expected to contain: a kernel program, a ker-
ally correct but slow.                                              nel scheduling code, a JIT-library compilation code, and a
                                                                    PyTorch model class NewModel(nn.Module) with
3     KF ORGE : AUTONOMOUS P ROGRAM                                 def forward(self, *inputs) method that imple-
                                                                    ments the module’s forward pass.
      S YNTHESIS
                                                                    We use the Jinja2 template engine to parameterize the
We propose KForge, a multi-stage autonomous program                 prompts. Listing 1 contains an example of the prompt tem-
synthesis framework, described in Figure 1. Our approach            plate that we send to the program synthesis agent F . The
is versatile and supports iterative refinement, single-shot         resulting prompt p contains a high-level task description, a
program synthesis, as well as repetitive sampling, where the        single-shot architecture in PyTorch and the corresponding
mode of operation is directed by prompt construction.               implementation for the target accelerator, an input problem
Repeated sampling has been extensively explored in multi-           in PyTorch and a task description in natural language.
ple previous works (Chen et al., 2021; Ouyang et al., 2025),
specifically HumanEval (Chen et al., 2021) reports that gen-
                                                                           You write custom {{ accelerator }} kernels to replace
erating 100 samples helps solve 70.2% of problems. Hence,                 ,→ the pytorch operators in the given architecture to
                                                                          ,→ get speedups...
we focus on comparing single-shot and iterative refinement
experiments, bypassing repeated sampling.                                  Here's an example to show you the syntax of inline
                                                                          ,→ embedding custom {{ accelerator }} operators...

Within the scope of this work, we focus on the following                  {{ example_arch_src }}

three strategies that we employ for program synthesis. Each                The example new arch with custom {{ accelerator }}
                                                                          ,→ kernels looks like this:
of these strategies is complementary to each other, allow-
ing one to build dynamic configurations based on available                {{ example_new_arch_src }}

sources of supervision and computational resource budgets.                You are given the following architecture:

                                                                          {{ arc_src }}

    • Iterative refinement: It allows the model to make                    Optimize the architecture named Model with custom {{
                                                                          ,→ accelerator }} operators ...
      error corrections from the previous run or optimize
                                                                          Output the new code in codeblocks ...
      the performance of the correctly generated kernel,
      taking into account the program synthesized in the
      previous iteration. Specifically, for each iteration
      i ∈ {1, . . . , N − 1} we add evaluation results from iter-            Listing 1: Program synthesis prompt template
      ation i − 1 to the model’s prompt, with a corresponding
      instruction to fix the error or improve program perfor-       We use vector addition as the single-shot example for both
      mance.                                                        the CUDA and MPS backends. The example consists of
                                                                    kernel definition, kernel scheduling logic, JIT-compilation
    • Reference implementation: We provide the model                via torch.utils.cpp extension.load inline,
      with a functional reference implementation for other ac-      and binding with torch.nn.Module. Full code listings
      celerator(s), enabling kernel translation. For example,       with custom kernel integration for CUDA and MPS are
      when we generate Metal kernels, we provide CUDA               provided in Sections A and B.
      kernels as reference implementations.
                                                                    We also explored the interfaces for adding custom kernels in
    • Profiling information: It is crucial for pinpointing bot-     the MLX (Hannun et al., 2023) Deep Learning framework.
      tlenecks and provides comprehensive information on            MLX is developed at Apple for training and inference on
      hardware resource usage for a specific computational          Apple Silicon, so Metal kernels are its default. Although
      workload. The timeline view assists in identifying            MLX recently added support for CUDA, we decided to use
      scheduling gaps, while the detailed statistics at the         PyTorch as our framework of choice because it supports
      level of individual accelerator API calls enable focus-       more backends, such as Intel’s XPU, and has wide adoption
      ing on parts of the computational graph that do not           in the community.
      fully utilize hardware resources.
                                                                    3.2     Performance Analysis Agent
3.1   Program Synthesis Agent
                                                                    We introduce a specialized agent for performance analysis
In this work, we follow a similar task definition as described      rather than using a single program synthesis agent for two
in (Ouyang et al., 2025). Specifically, we treat the LLM as         reasons. (1) Profiling data is extensive but optimization
a function F : (p) 7→ k that receives a text prompt p ∈ T           signals are sparse. Previous research (Modarressi et al.,
                              KForge: Program Synthesis for Diverse AI Hardware Accelerators

2025) shows that LLM performance on relevant information         4     E XPERIMENTAL S ETUP
retrieval drops to 50% for 32K token inputs versus <1K
tokens. (2) Specialized agents enable a modular architecture     Our evaluation encompasses 8 LLMs from 3 model
with different models for each agent. Some LLMs like             providers (Table 1), examining both their ability to synthe-
deepseek-r1 or deepseek-v3 are text-only, while analyzing        size programs for hardware accelerators and their relative
profiling screenshots requires multimodal capabilities.          performance on this task.

The Performance Analysis Agent processes profiling inputs
- raw metrics from NVIDIA Nsight Systems or visual data
from Xcode Instruments—and generates optimization rec-            Provider    Checkpoint                   Chat     Reasoning
ommendations for subsequent program synthesis iterations.
                                                                  OpenAI      gpt-5-2025-08-07                         ✓
This platform-agnostic approach handles arbitrary textual or      OpenAI      o3-2025-04-16                            ✓
visual profiling data across different hardware accelerators.     OpenAI      gpt-4o-2024-11-20             ✓
                                               0      n           OpenAI      gpt-4.1-2025-04-14            ✓
Formally, the agent is defined as G : (o, k, {v , ..., v }) 7→    Anthropic   claude-opus-4-20250514                   ✓
r, where o ∈ T is the text performance optimization prompt;       Anthropic   claude-sonnet-4-20250514      ✓
k ∈ T is the synthesized program; v i ∈ RH×W ×C ∪ T , i ∈         DeepSeek    deepseek-R1-0528                         ✓
{0, ..., n} represents profiling information as screenshots       DeepSeek    deepseek-V3-0324              ✓
when v i ∈ RH×W ×C or text-based profiler output when
v i ∈ T ; and r ∈ T is the performance recommendation.                        Table 1. Models used in experiments
The agent is prompted to generate a single recommendation
for maximum performance improvement.
The recommendation rt feeds into the next synthesis iter-
ation, establishing a feedback loop: F : (p, kt−1 , rt−1 ) 7→    4.1   Dataset
kt .                                                             We base our experiments on KernelBench (Ouyang et al.,
                                                                 2025), containing 250 PyTorch modules across three diffi-
3.3   Program Verification                                       culty levels: Level 1 (single primitives like convolutions),
The proposed execution flow defines a closed feedback loop,      Level 2 (operation sequences with fusion potential), and
with valuable information that is either helpful in recovering   Level 3 (complete architectures like AlexNet (Krizhevsky
from failures or allows the model to optimize a functionally     et al., 2012) or transformer components (Radford et al.,
correct implementation to achieve speedup.                       2019)).

After every generation-evaluation iteration, we save detailed    Baseline Methodology. We measure execution time across
logs for each workload. We focus on five possible execution      100 runs with 10 warmup steps, resetting compilation con-
states:                                                          text between runs. This provides consistent reference points
                                                                 for evaluating generated kernels.

   • generation failure — typical reasons: network error,        CUDA Backend. CUDA provides comprehensive support
     model output does not contain workload’s code.              for all 250 KernelBench problems. We evaluate against both
                                                                 eager mode and torch.compile (TorchInductor back-
                                                                 end, default mode). While torch.compile occasionally
   • compilation failure — the generated result contains         degrades performance on simple operator sequences, this
     workload’s code, but fails to compile.                      effect diminishes for larger Level 3 architectures. We reset
                                                                 the compilation context after each run, while computing
   • runtime error — the workload’s code compiles but fails      baselines and evaluating generated kernels.
     at runtime, typically caused by segmentation faults or
     program abort.                                              MPS Backend. PyTorch 2.7 uses Metal Performance
                                                                 Shaders (MPS) (Apple Inc.) for GPU acceleration, but sev-
                                                                 eral operations lack native Metal implementations (Conv3D
   • numerical or shape mismatch — call to                       transpose, 3D average/max pooling). We exclude 30 prob-
     NewModel.forward returns tensors, but they                  lems containing unsupported operations (9 from Level 1,
     mismatch in tensor shapes or expected values or both.       21 from Level 2), leaving 220 problems in total. Table 2
                                                                 summarizes the problem distribution. We evaluate against
   • correct — call to NewModel.forward returns ten-             eager mode, as torch.compile for MPS remains ex-
     sors that match expected outputs both in shapes and         perimental with high failure rates (20%) and inconsistent
     numerically.                                                performance.
                               KForge: Program Synthesis for Diverse AI Hardware Accelerators

      Benchmark              Level 1    Level 2   Level 3           max output tokens unspecified,          enabling the
      KernelBench-Metal         91        79         50             model to generate as many tokens as needed to complete
      KernelBench              100       100         50             the task.
                                                                    Anthropic reasoning models are configured with a
Table 2. Problem distribution for Metal experiments. KernelBench-
                                                                    budget tokens parameter to control the model’s rea-
Metal excludes MPS-unsupported operations.
                                                                    soning effort. We follow Anthropic’s reasoning guidelines
                                                                    and set budget tokens to half of the max tokens
4.2   Metrics                                                       value. After testing multiple max tokens values on a
                                                                    subset of problems, we observed that generated outputs
As a metric, we use f astp which is defined as the fraction
                                                                    never exceeded 12,000 tokens. For all experiments, we
of tasks that are both correct and have a speedup (computed
                                                                    set max tokens=16384, which provides sufficient head-
as the ratio of baseline implementation to generated kernel
                                                                    room without constraining the model’s expressive power.
execution time) greater than threshold p:
                                                                                                 OpenAI     Anthropic     DeepSeek
                     N
               1 X
      f astp =       1(correcti ∧ {speedupi > p})                    temperature
                                                                     reasoning effort
                                                                                                    0.0
                                                                                                  “high”
                                                                                                                 0.0
                                                                                                                  –
                                                                                                                             0.0
                                                                                                                              –
               N i=1
                                                                     max output tokens             None           –           –
                                                                     max tokens                      –         16384        20000
where N is the total number of problems in a given level.            budget tokens                   –          8192          –
Key measurements include:
                                                                          Table 3. Hyper-parameter settings for our experiments
   • Correctness rate (f ast0 ): The fraction of tasks that
                                                                    For DeepSeek models, we set max tokens=20000 and
     produce correct results regardless of performance
                                                                    observed no truncated outputs in any of our experiments.
   • On-par performance (f ast1 ): The fraction of tasks            Table 3 lists hyperparameters.
     that are both correct and achieve at least the same speed      For both CUDA and MPS backends, iterative refinement
     as the reference implementation                                experiments are conducted with num iterations=5.
   • Superior performance (f astp with p > 1.0): The
     fraction of tasks that are both correct and run faster         5     CUDA BACKEND P ROGRAM S YNTHESIS
     than the reference implementation
                                                                    5.1   Iterative Refinement
4.3   Hardware Configuration                                        This section outlines the iterative refinement experiment
For Metal experiments, we use 5 Mac Studios with Apple              for CUDA program synthesis. We benchmark performance
M4 Max chips (14-core CPU, 32-core GPU, 36GB unified                against the PyTorch eager mode baseline. Comparisons with
memory).                                                            torch.compile are addressed in the subsequent section,
                                                                    where profiling data is included.
For CUDA experiments, we use a single server with 4×
H100 SXM5 GPUs (80GB HBM3 each), with 3.35 TB/s                     Reasoning models, in particular openai-gpt-5 and openai-
memory bandwidth.                                                   o3, consistently show the best performance across all levels
                                                                    of KernelBench.
To reduce measurement noise and ensure dedicated resource
allocation for benchmarking, we evaluate one kernel at a            While chat models consistently perform worse, in particular,
time per computational unit on each platform—one kernel             the gap increases with the complexity of the problems, reach-
per GPU for CUDA and one kernel per Mac Studio node                 ing its maximum for Level 3 problems. This indicates that
for Metal.                                                          the model’s capability to perform intermediate reasoning
                                                                    is crucial for solving the problems of increased complexity.
                                                                    However, we conjecture that for easy problems in Level 1
4.4   Hyperparameters
                                                                    it might be more cost-effective to perform initial synthesis
In our experiments, we use all models via API calls, al-            with a chat model and run iterative refinements using SOTA
though DeepSeek-R1 (DeepSeek-AI et al., 2025a) and                  reasoning LLMs.
DeepSeek-V3 (DeepSeek-AI et al., 2025b) are both open-
                                                                    Performance at f ast1 for all models decreases signifi-
source and can be self-hosted.
                                                                    cantly, and only a fraction of models achieves speedups
For     OpenAI reasoning models,                  we      config-   against the baseline. It is worth noting that many problems
ure     reasoning effort="high"                   and      leave    in the KernelBench dataset use input tensors with small
                             KForge: Program Synthesis for Diverse AI Hardware Accelerators

batch size. Benchmarking such problems may result in           erate actionable recommendations, analogous to the MPS
measuring kernel launch overhead To rather than time spent     backend workflow where visual profiling data guides opti-
on memory access Tm or computation Tc (where To , Tm ,         mization decisions.
and Tc represent overhead, memory, and computation time,
                                                               Figure 3 presents results for the three top-performing rea-
respectively). This occurs when To ≫ Tm or To ≫ Tc . We
                                                               soning models. Notably, for Level 1 and Level 2 prob-
perform a case study on several Level 3 problems across a
                                                               lems, torch.compile yields inferior performance com-
grid of batch size values. We describe it in detail in the
                                                               pared to Eager Mode, while showing improved baseline
Case Study section of this work.
                                                               performance on Level 3 problems. Incorporating profiling
openai-gpt-5 achieves f ast1.5 = 0.2 on Level 3 prob-          information does not seem to be consistently helpful ex-
lems. By manually inspecting generated programs, we            cept for openai-gpt-5, where the additional information
observed optimizations like kernel fusion and application      allows it to achieve the strongest performance overall, with
of torch.compile. Also, we found examples of CUDA              11% of Level 3 problems running at least 1.5× faster than
Graphs incorporation that allow consolidating several kernel   torch.compile.
launches into one graph launch.
Comparison with alternative methods. To our knowl-             6     MPS BACKEND P ROGRAM S YNTHESIS
edge, (Ouyang et al., 2025) is the only work that performs
                                                               6.1    One-shot and Iterative Refinement Kernel
a comprehensive evaluation across all problems from Ker-
                                                                      Synthesis
nelBench. One stark difference we observe is that the per-
formance of frontier LLMs has significantly improved since     The starting point of our experiments is a single-shot kernel
the introduction of KernelBench.                               synthesis, with the number of iterative refinement itera-
                                                               tions constrained to 1, effectively giving the model only
In our experiments, openai-gpt-5 is capable of achieving
                                                               one chance for generation of a numerically correct kernel.
a correctness rate that is consistently higher than 90% for
                                                               Table 4 lists correctness rates for the Baseline and CUDA
problems from all levels, while openai-o1 that was used in
                                                               reference configurations.
(Ouyang et al., 2025) experiments achieves a correctness
rate of 60% on average across all problem levels. deepseek-    Reasoning models show the best performance and achieve
r1 and deepseek-v3 are the only two models that are used       remarkable correctness rates. Even in the baseline configu-
both in ours and their experiments. If we compare f ast1       ration, openai-o3 achieves 72% accuracy on Level 2 prob-
our results appear to be less performant, except for Level 1   lems. Solid lines in Figure 4 correspond to f astp values for
problems for deepdeek-v3 where we show 18% versus 9%           iterative refinement experiments.
reported in (Ouyang et al., 2025)
                                                                                          Baseline          CUDA Reference
The f astp metric for 8 LLMs is summarized in Figure 2. In         Model            L1      L2     L3       L1   L2    L3
the subsequent sections, we will focus solely on openai-gpt-
5, openai-o3 and claude-opus-4 reasoning models since              claude-opus-4   0.66    0.62    0.22    0.86    0.83    0.42
                                                                   openai-o3       0.59    0.72    0.44    0.53    0.44    0.28
they yield the best overall performance.                           openai-gpt-5    0.78    0.65    0.44    0.69    0.72    0.48

5.2   Profiling Information Incorporation                      Table 4. Single-shot correctness rate. Baseline vs. CUDA ref-
                                                               erence configuration. These numbers demonstrate the model’s
NVIDIA offers a comprehensive profiling ecosystem with         ability to solve the task with no additional information and without
tools such as Nsight Compute and Nsight Systems that pro-      opportunities for error correction or kernel optimization.
vide both command-line interfaces and programmatic access
to detailed performance metrics. For the experiments in this   In general, reasoning models surpass chat models in perfor-
section, we use NVIDIA Nsight Systems to capture detailed      mance, attaining high accuracy rates. Both openai-gpt-5
performance metrics. Profiling is performed using targeted     and openai-o3 exceed a 90% accuracy rate across all prob-
capture with cudaProfilerApi range markers, tracing            lem levels. Meanwhile, claude-opus-4 performs similarly
CUDA API calls, GPU kernels, NVTX ranges, OS runtime           on Level 1 and Level 2 but only solves 50% of Level 3
events, and cuDNN/cuBLAS operations. For each gener-           problems.
ated kernel, we extract quantitative performance data using
nsys stats, which generates CSV reports containing             The number of correctly generated kernels that run as fast as
CUDA API summaries, GPU kernel execution statistics,           the baseline decreases significantly for all model providers
memory transfer metrics, and NVTX region timings. These        over all levels. openai-gpt-5 with iterative refinement and
structured CSV files, together with the kernel source code,    CUDA reference configuration is the only model that gen-
are fed to the performance optimization module to gen-         erates 20% of the kernels for level 1 and level 2 that run at
                                                               least 1.5× faster than the baseline.
                                 KForge: Program Synthesis for Diverse AI Hardware Accelerators




                         Figure 2. CUDA Program Synthesis. Iterative refinement against PyTorch Eager Mode




Figure 3. CUDA Program synthesis. Iterative refinement vs. Iterative refinement + Profiling Information against torch.compile


6.2    CUDA Reference Implementation                                through translation of thread indexing and synchronization
                                                                    constructs. The core parallel computational logic remains
Despite fundamental differences in memory architecture,
                                                                    largely invariant, making CUDA kernels valuable reference
CUDA and Metal exhibit significant structural similarities
                                                                    implementations for Metal kernel generation. In Listing 2
that facilitate cross-platform kernel adaptation. Both plat-
                                                                    and Listing 3 we include equivalent implementations for
forms employ analogous parallel execution hierarchies, with
                                                                    vector addition written in CUDA and Metal, respectively, to
CUDA thread blocks corresponding to Metal threadgroups
                                                                    illustrate their similarities.
and similar 32-thread execution units; warp and SIMD-
groups in CUDA and Metal terminology correspondingly.
                                                                        kernel void vector_add_kernel(
                                                                            device float* input_a [[buffer(0)]],
                                                                            device float* input_b [[buffer(1)]],
      __global__ void elementwise_add_kernel(                               device float* output [[buffer(2)]],
          const float *a, const float *b, float *out, int size) {           uint index [[thread_position_in_grid]]) {
        int idx = blockIdx.x * blockDim.x + threadIdx.x;                    output[index] = input_a[index] + input_b[index];
        if (idx < size) {                                               }
          out[idx] = a[idx] + b[idx];
        }
      }

                                                                    Listing 3: Metal kernel for element-wise vector additions
Listing 2: CUDA kernel for element-wise vector additions
                                                                    We use CUDA reference implementations from the
The kernel program syntax demonstrates substantial overlap,         KernelBench-samples dataset. We retain only correct pro-
enabling CUDA reference implementations to serve as effec-          grams, resulting in 12,600 programs spanning 245 tasks.
tive reference implementations for Metal program synthesis          For reproducibility purposes, we select the first correct im-
                              KForge: Program Synthesis for Diverse AI Hardware Accelerators




         Figure 4. MPS program synthesis. Iterative refinement vs. Iterative refinement + CUDA reference implementation

                                               CUDA Reference            CUDA Reference + Prof Info
                         Model            Level 1 Level 2  Level 3       Level 1 Level 2   Level 3
                                                             f ast1.0
                         claude-opus-4     0.121     0.423      0.100     0.132     0.500      0.160
                         openai-o3         0.462     0.321      0.220     0.418     0.474      0.280
                         openai-gpt-5      0.571     0.718      0.340     0.538     0.756      0.440
                                                             f ast1.5
                         claude-opus-4     0.044     0.115      0.020     0.066     0.154      0.020
                         openai-o3         0.066     0.115      0.060     0.088     0.115      0.040
                         openai-gpt-5      0.176     0.243      0.060     0.165     0.256      0.040

                                 Table 5. MPS Program Synthesis. Impact of profiling information


plementation for each task and use it for all runs across all      for all problems that are correct and hereafter can be opti-
model providers. The generation process is now augmented           mized. We use PyTorch MPS Profiler and capture trace files
with the CUDA reference implementation.                            by setting MTL CAPTURE ENABLED=True.
Table 4 shows correctness rates for the CUDA reference             To address the issue of profiling information collection on
configuration. All models except for openai-o3 achieve             MacOS, we automate gputrace analysis through an Apple
higher correctness rates compared to the baseline.                 Script that uses cliclick (Bluem) for interaction with
                                                                   Xcode’s GUI and captures screenshots of summary, memory,
Dashed lines in Figure 4 correspond to CUDA reference
                                                                   and timeline views for each collected gputrace.
configuration and show the effectiveness of the proposed
method in boosting model performance on a majority of the          We focus on f ast1.0 and f ast1.5 threshold since intuitively,
f astp thresholds.                                                 incorporation of profiling information is expected to in-
                                                                   crease program performance. Two configurations are con-
These results suggest that some implementation patterns are
                                                                   sidered: CUDA Reference and CUDA Reference + Perfor-
language-agnostic and, to some extent, hardware-agnostic,
                                                                   mance Recommendation. The results are reported in Table 5.
enabling easier transfer across paradigms and smoother tran-
sitions between accelerators.                                      Incorporation of optimization recommendations generated
                                                                   by the performance analysis agent G shows to be helpful for
6.3   Profiling Information Incorporation                          all models in problems from Level 2 and Level 3 at f ast1.0 .
                                                                   Specifically, openai-gpt-5 is capable of increasing f ast1.0
Profiling Metal programs’ performance on macOS presents            for Level 3 problems by 30%, when openai-o3 improves its
a challenge due to the absence of programmatic APIs for            results for Level 2 problems by 47%.
accessing GPU profiling data. Apple offers limited profiling
capabilities, primarily through Xcode.                             Interestingly, for f ast1.5 , we do not observe consistent
                                                                   trends. Moreover, the previously mentioned small input
At the program verification stage, we collect gputrace files       tensor shapes used in KernelBench incur irreducible noise
                              KForge: Program Synthesis for Diverse AI Hardware Accelerators

in measurement. The results also suggest that profiling             Method Workload                        Batch Size
information itself is still not sufficient for performance im-                                        8     16    32    64 128
provement, and sometimes can even lead to performance
degradation. We plan to elucidate the observed behavior in          PyTorch SqueezeNetFire        1.04 1.280 3.90 7.74 15.4
                                                                            MobileNetV2           2.79 2.92 5.2 9.86 19.2
greater detail in future work.                                       Eager
                                                                            MinGPT                1.38 2.59 4.94 9.68 19.4
                                                                            SqueezeNetFire 0.565 0.686 2.41 3.59 7.11
                                                                     Torch
7     C ASE S TUDIES                                                Compile MobileNetV2     2.78 2.65 4.2 7.37 13.8
                                                                            MinGPT          1.12    2.1 3.97 7.65 15.7
7.1   Evaluation Across Different Batch Sizes                                  SqueezeNetFire 0.474 0.539 1.58 3.09 6.10
                                                                    KForge
To evaluate whether synthesized programs generalize be-                        MobileNetV2       1.8 5.41 10.2 19.9 41.6
                                                                    (ours)
                                                                               MinGPT          0.87 1.81 5.35 10.3 22.8
yond their training shapes, we systematically test CUDA
programs synthesized by openai-gpt-5 across batch sizes          Table 6. Execution time in milliseconds across batch sizes for three
8, 16, 32, 64, 128 on H100 PCIe Gen5 GPUs, comparing             end-to-end architectures from Level 3
against PyTorch Eager Mode and torch.compile. All
other module hyperparameters remain constant.
A synthesized implementation of SqueezeNetFire
consistently shows superior performance over tested
batch size shapes against both PyTorch Eager Mode
and torch.compile, illustrating that our method can              nential computation within the sigmoid function employs
provide a speedup for end-to-end building blocks. The            Metal’s fast::exp intrinsic to achieve further speedup
results are summarized in Table 6.                               with a reasonable trade-off in numerical precision.
At large batch sizes (64, 128), torch.compile’s graph-           The implementation employs thread-local caching of
level optimizations deliver superior throughput. Conversely,     Metal objects, including the device handle, pipeline
at small batch sizes (8, 16, 32), KForge outperforms both        state, and command queue, to eliminate redundant
baselines on end-to-end architectures (MobileNetV2 and           initialization across kernel invocations. The thread-
MinGPT, corresponding to problems 20 and 43 from Level           group configuration is dynamically tuned based on
3), suggesting kernel-level optimizations that reduce launch     maxTotalThreadsPerThreadgroup to maintain
overhead and improve cache utilization in low-latency            high occupancy across a range of input sizes. Additionally,
regimes.                                                         the kernel performs a single bounds check per thread, min-
All synthesized programs maintain numerical correctness          imizing control flow divergence and improving execution
across the batch size range, confirming that iterative refine-   efficiency. These optimizations lead to improved through-
ment produces programs robust to shape variation rather          put and memory access coherence, while maintaining cor-
than overfitted to generation configurations.                    rectness for tensors with dimensions not divisible by eight.
                                                                 Overall, the synthesized program achieves a 5× speedup
Notably, torch.compile could be applied atop synthe-             over the PyTorch eager baseline.
sized programs to perform higher-level graph optimiza-
tions (operator fusion, memory planning, kernel scheduling)      7.3   Invariance Exploitation
while preserving the low-level optimizations introduced dur-
ing generation. This composition could yield the benefits of     We observe patterns where models leverage the fact that cer-
both kernel-level tuning and graph-level transformations, an     tain programs produce constant output values, specifically
avenue we leave for future exploration.                          synthesized programs in Appendix C.2 and Appendix C.3
                                                                 which amount to 1% of problems from Level 1 and Level 2
7.2   High Performance Programs                                  KernelBench dataset. Speedups are achieved by recognizing
                                                                 that the computation result will be a constant value. This
In Section C.1, the program synthesized by claude-sonnet         recognition allows reducing the computation graph from
applies loop-based vectorization to optimize the Swish (Ra-      multiple layers to a single operation that outputs a tensor of
machandran et al., 2017) activation function defined as          all zeros with the required shape. In this work, we do not
                                          x                      attempt to address this issue and attribute it as a data-specific
             Swish(x) = x · σ(x) =                               problem. The so-called “cheating” problem can effectively
                                       1 + e−x
                                                                 be treated as a smart fusion optimization, where the compu-
on Metal-enabled hardware. Each thread sequentially pro-         tation graph is reduced to a single node. Future work could
cesses 8 elements, reducing launch overhead while increas-       build more comprehensive benchmarks with diverse input
ing arithmetic intensity and register utilization. The expo-     shapes and randomized values.
                               KForge: Program Synthesis for Diverse AI Hardware Accelerators

7.4   Computational Graph Reduction                                9    F UTURE W ORK
We observed a clever optimization discovered by one of             Future work will explore program synthesis for both forward
OpenAI’s models that enabled the discovery of a shorter            and backward passes of neural network models, enabling
but functionally equivalent computational graph. Interest-         acceleration of not only inference but also training across
ingly, LLMs described the suggested optimization in the            diverse hardware accelerators.
doc string and added the implementation that corresponds
                                                                   We plan to investigate conditioning on intermediate repre-
to the suggested idea. Principally, that suggestion allowed
                                                                   sentations (IRs) used by compilers. This could enable the
the simplification of the problem from Matrix-Matrix mul-
                                                                   model to learn from existing compiler optimizations for the
tiplication to Matrix-Vector multiplication. The reader is
                                                                   synthesis of more performant programs.
welcome to inspect both the original problem and generated
optimization provided in Appendix C.4 and Appendix C.5.            Building on our profiling-based approach, we aim to de-
                                                                   velop a more granular feedback architecture that incorpo-
While it is not clear if this problem formulation is intentional
                                                                   rates memory bandwidth utilization and roofline model anal-
in the KernelBench dataset, but we believe that capabilities
                                                                   ysis to guide optimization decisions. Such detailed profiling
such as this one serve the illustrative purpose of how LLMs
                                                                   could help the model identify performance bottlenecks more
can facilitate invariance in optimizing computational graphs
                                                                   precisely and generate more targeted optimizations.
that can translate to a plethora of practical applications such
as chip design, route planning, and generic optimization on        Finally, we believe that integrating formal verification meth-
graphs.                                                            ods could make program synthesis more robust, ensuring
                                                                   correctness across various data types and tensor shapes
8     D ISCUSSION                                                  while maintaining the performance benefits of synthesized
                                                                   kernels.
Experimental results confirm that frontier reasoning LLMs,
when augmented with iterative feedback loops, are well-
                                                                   ACKNOWLEDGMENTS
positioned for program synthesis tasks and can accelerate
program development for diverse hardware accelerators.             The authors would like to thank Omid Azizi, Vihang Mehta,
Furthermore, by providing reference implementations, we            and Jeff Liu for insightful discussions, feedback on early
are able to improve both the correctness rate and perfor-          versions of this text, and assistance with the hardware setup
mance of the programs.                                             for the experiments.
Although we observe a remarkable success rate for single-
shot generation, it is followed by incremental changes in          R EFERENCES
subsequent iterations. We hypothesize that this occurs be-
                                                                   Ansel, J., Yang, E., He, H., Gimelshein, N., Jain, A., Voz-
cause conditioning on previous generations does not neces-
                                                                     nesensky, M., Bao, B., Bell, P., Berard, D., Burovski, E.,
sarily lead to globally optimal solutions. Instead, the model
                                                                     Chauhan, G., Chourdia, A., Constable, W., Desmaison,
may become trapped in local optima, where each iterative
                                                                    A., DeVito, Z., Ellison, E., Feng, W., Gong, J., Gschwind,
refinement produces marginal improvements while missing
                                                                     M., Hirsh, B., Huang, S., Kalambarkar, K., Kirsch, L.,
opportunities for more fundamental algorithmic restructur-
                                                                     Lazos, M., Lezcano, M., Liang, Y., Liang, J., Lu, Y.,
ing that could yield superior performance.
                                                                     Luk, C. K., Maher, B., Pan, Y., Puhrsch, C., Reso, M.,
Regardless of the accelerator in question, it remains chal-          Saroufim, M., Siraichi, M. Y., Suk, H., Zhang, S., Suo, M.,
lenging to determine which profiling information is useful          Tillet, P., Zhao, X., Wang, E., Zhou, K., Zou, R., Wang,
for making optimization decisions. Raw profiling data often         X., Mathews, A., Wen, W., Chanan, G., Wu, P., and
contain hundreds of metrics, ranging from memory band-               Chintala, S. Pytorch 2: Faster machine learning through
width utilization and cache hit rates to warp occupancy and          dynamic python bytecode transformation and graph com-
instruction throughput, creating an overwhelming amount              pilation. In Proceedings of the 29th ACM International
of information that requires expert knowledge to interpret          Conference on Architectural Support for Programming
effectively.                                                        Languages and Operating Systems, Volume 2, ASPLOS
                                                                    ’24, pp. 929–947, New York, NY, USA, 2024. Associa-
The f astp metric may obscure modest speedups below the
                                                                     tion for Computing Machinery. ISBN 9798400703850.
threshold, despite small per-kernel gains (e.g., 2-5%) com-
                                                                     doi: 10.1145/3620665.3640366. URL https://doi.
pounding to significant improvements at scale. A continuous
                                                                     org/10.1145/3620665.3640366.
speedup distribution would provide a finer-grained analysis,
revealing exact performance gains.
                                                                   Apple Inc. Metal Performance Shaders (MPS) backend
                                                                     for PyTorch. https://developer.apple.com/
                              KForge: Program Synthesis for Diverse AI Hardware Accelerators

  metal/pytorch/. Accessed: 2025-01-01.                             W. L., An, W., Liu, X., Wang, X., Chen, X., Nie, X.,
                                                                    Cheng, X., Liu, X., Xie, X., Liu, X., Yang, X., Li, X., Su,
Apple Inc. Metal, 2014. URL https://developer.                      X., Lin, X., Li, X. Q., Jin, X., Shen, X., Chen, X., Sun,
  apple.com/metal/. Graphics and compute API.                       X., Wang, X., Song, X., Zhou, X., Wang, X., Shan, X.,
Bluem, C. cliclick: A command-line tool for execut-                 Li, Y. K., Wang, Y. Q., Wei, Y. X., Zhang, Y., Xu, Y., Li,
  ing mouse- and keyboard-related actions. https://                 Y., Zhao, Y., Sun, Y., Wang, Y., Yu, Y., Zhang, Y., Shi,
  github.com/BlueM/cliclick.                                        Y., Xiong, Y., He, Y., Piao, Y., Wang, Y., Tan, Y., Ma,
                                                                    Y., Liu, Y., Guo, Y., Ou, Y., Wang, Y., Gong, Y., Zou,
Chen, M., Tworek, J., Jun, H., Yuan, Q., de Oliveira Pinto,         Y., He, Y., Xiong, Y., Luo, Y., You, Y., Liu, Y., Zhou, Y.,
  H. P., Kaplan, J., Edwards, H., Burda, Y., Joseph, N.,            Zhu, Y. X., Xu, Y., Huang, Y., Li, Y., Zheng, Y., Zhu, Y.,
  Brockman, G., Ray, A., Puri, R., Krueger, G., Petrov,             Ma, Y., Tang, Y., Zha, Y., Yan, Y., Ren, Z. Z., Ren, Z.,
  M., Khlaaf, H., Sastry, G., Mishkin, P., Chan, B., Gray,          Sha, Z., Fu, Z., Xu, Z., Xie, Z., Zhang, Z., Hao, Z., Ma,
  S., Ryder, N., Pavlov, M., Power, A., Kaiser, L., Bavar-          Z., Yan, Z., Wu, Z., Gu, Z., Zhu, Z., Liu, Z., Li, Z., Xie,
  ian, M., Winter, C., Tillet, P., Such, F. P., Cummings,           Z., Song, Z., Pan, Z., Huang, Z., Xu, Z., Zhang, Z., and
  D., Plappert, M., Chantzis, F., Barnes, E., Herbert-              Zhang, Z. Deepseek-r1: Incentivizing reasoning capa-
  Voss, A., Guss, W. H., Nichol, A., Paino, A., Tezak,              bility in llms via reinforcement learning, 2025a. URL
  N., Tang, J., Babuschkin, I., Balaji, S., Jain, S., Saun-         https://arxiv.org/abs/2501.12948.
  ders, W., Hesse, C., Carr, A. N., Leike, J., Achiam,
  J., Misra, V., Morikawa, E., Radford, A., Knight, M.,           DeepSeek-AI, Liu, A., Feng, B., Xue, B., Wang, B., Wu, B.,
  Brundage, M., Murati, M., Mayer, K., Welinder, P., Mc-            Lu, C., Zhao, C., Deng, C., Zhang, C., Ruan, C., Dai, D.,
  Grew, B., Amodei, D., McCandlish, S., Sutskever, I., and          Guo, D., Yang, D., Chen, D., Ji, D., Li, E., Lin, F., Dai,
  Zaremba, W. Evaluating large language models trained              F., Luo, F., Hao, G., Chen, G., Li, G., Zhang, H., Bao,
  on code, 2021. URL https://arxiv.org/abs/                         H., Xu, H., Wang, H., Zhang, H., Ding, H., Xin, H., Gao,
  2107.03374.                                                       H., Li, H., Qu, H., Cai, J. L., Liang, J., Guo, J., Ni, J., Li,
                                                                    J., Wang, J., Chen, J., Chen, J., Yuan, J., Qiu, J., Li, J.,
Chen, W., Zhu, J., Fan, Q., Ma, Y., and Zou, A. Cuda-               Song, J., Dong, K., Hu, K., Gao, K., Guan, K., Huang,
  llm: Llms can write efficient cuda kernels, 2025. URL             K., Yu, K., Wang, L., Zhang, L., Xu, L., Xia, L., Zhao,
  https://arxiv.org/abs/2506.09092.                                 L., Wang, L., Zhang, L., Li, M., Wang, M., Zhang, M.,
                                                                    Zhang, M., Tang, M., Li, M., Tian, N., Huang, P., Wang,
Dao, T. Flashattention-2: Faster attention with bet-
                                                                    P., Zhang, P., Wang, Q., Zhu, Q., Chen, Q., Du, Q., Chen,
  ter parallelism and work partitioning. arXiv preprint
                                                                    R. J., Jin, R. L., Ge, R., Zhang, R., Pan, R., Wang, R.,
  arXiv:2307.08691, 2023.
                                                                    Xu, R., Zhang, R., Chen, R., Li, S. S., Lu, S., Zhou, S.,
Dao, T., Fu, D. Y., Ermon, S., Rudra, A., and Ré, C. Flashat-      Chen, S., Wu, S., Ye, S., Ye, S., Ma, S., Wang, S., Zhou,
  tention: Fast and memory-efficient exact attention with           S., Yu, S., Zhou, S., Pan, S., Wang, T., Yun, T., Pei, T.,
  io-awareness. arXiv preprint arXiv:2205.14135, 2022.              Sun, T., Xiao, W. L., Zeng, W., Zhao, W., An, W., Liu,
                                                                    W., Liang, W., Gao, W., Yu, W., Zhang, W., Li, X. Q.,
DeepSeek-AI, Guo, D., Yang, D., Zhang, H., Song, J.,                Jin, X., Wang, X., Bi, X., Liu, X., Wang, X., Shen, X.,
  Zhang, R., Xu, R., Zhu, Q., Ma, S., Wang, P., Bi, X.,             Chen, X., Zhang, X., Chen, X., Nie, X., Sun, X., Wang,
  Zhang, X., Yu, X., Wu, Y., Wu, Z. F., Gou, Z., Shao, Z.,          X., Cheng, X., Liu, X., Xie, X., Liu, X., Yu, X., Song,
  Li, Z., Gao, Z., Liu, A., Xue, B., Wang, B., Wu, B., Feng,        X., Shan, X., Zhou, X., Yang, X., Li, X., Su, X., Lin, X.,
  B., Lu, C., Zhao, C., Deng, C., Zhang, C., Ruan, C., Dai,         Li, Y. K., Wang, Y. Q., Wei, Y. X., Zhu, Y. X., Zhang,
  D., Chen, D., Ji, D., Li, E., Lin, F., Dai, F., Luo, F., Hao,     Y., Xu, Y., Xu, Y., Huang, Y., Li, Y., Zhao, Y., Sun, Y.,
  G., Chen, G., Li, G., Zhang, H., Bao, H., Xu, H., Wang,           Li, Y., Wang, Y., Yu, Y., Zheng, Y., Zhang, Y., Shi, Y.,
  H., Ding, H., Xin, H., Gao, H., Qu, H., Li, H., Guo, J.,          Xiong, Y., He, Y., Tang, Y., Piao, Y., Wang, Y., Tan, Y.,
  Li, J., Wang, J., Chen, J., Yuan, J., Qiu, J., Li, J., Cai,       Ma, Y., Liu, Y., Guo, Y., Wu, Y., Ou, Y., Zhu, Y., Wang,
  J. L., Ni, J., Liang, J., Chen, J., Dong, K., Hu, K., Gao,        Y., Gong, Y., Zou, Y., He, Y., Zha, Y., Xiong, Y., Ma, Y.,
  K., Guan, K., Huang, K., Yu, K., Wang, L., Zhang, L.,             Yan, Y., Luo, Y., You, Y., Liu, Y., Zhou, Y., Wu, Z. F.,
  Zhao, L., Wang, L., Zhang, L., Xu, L., Xia, L., Zhang,            Ren, Z. Z., Ren, Z., Sha, Z., Fu, Z., Xu, Z., Huang, Z.,
  M., Zhang, M., Tang, M., Li, M., Wang, M., Li, M., Tian,          Zhang, Z., Xie, Z., Zhang, Z., Hao, Z., Gou, Z., Ma, Z.,
  N., Huang, P., Zhang, P., Wang, Q., Chen, Q., Du, Q., Ge,         Yan, Z., Shao, Z., Xu, Z., Wu, Z., Zhang, Z., Li, Z., Gu,
  R., Zhang, R., Pan, R., Wang, R., Chen, R. J., Jin, R. L.,        Z., Zhu, Z., Liu, Z., Li, Z., Xie, Z., Song, Z., Gao, Z.,
  Chen, R., Lu, S., Zhou, S., Chen, S., Ye, S., Wang, S., Yu,       and Pan, Z. Deepseek-v3 technical report, 2025b. URL
  S., Zhou, S., Pan, S., Li, S. S., Zhou, S., Wu, S., Ye, S.,       https://arxiv.org/abs/2412.19437.
 Yun, T., Pei, T., Sun, T., Wang, T., Zeng, W., Zhao, W.,
  Liu, W., Liang, W., Gao, W., Yu, W., Zhang, W., Xiao,           Fisches, Z. V., Paliskara, S., Guo, S., Zhang, A., Spisak,
                             KForge: Program Synthesis for Diverse AI Hardware Accelerators

  J., Cummins, C., Leather, H., Synnaeve, G., Isaac-            Ouyang, A., Guo, S., Arora, S., Zhang, A. L., Hu, W., Ré,
  son, J., Markosyan, A., and Saroufim, M. Ker-                   C., and Mirhoseini, A. Kernelbench: Can llms write
  nelllm: Making kernel development more accessi-                 efficient gpu kernels?, 2025. URL https://arxiv.
  ble, 6 2025. URL https://huggingface.co/                        org/abs/2502.10517.
  facebook/KernelLLM.        Corresponding authors:
  Aram Markosyan, Mark Saroufim.                                Paszke, A., Gross, S., Massa, F., Lerer, A., Bradbury, J.,
                                                                  Chanan, G., Killeen, T., Lin, Z., Gimelshein, N., Antiga,
Hannun, A., Digani, J., Katharopoulos, A., and Collobert,         L., Desmaison, A., Köpf, A., Yang, E., DeVito, Z., Rai-
  R. MLX: Efficient and flexible machine learning on              son, M., Tejani, A., Chilamkurthy, S., Steiner, B., Fang,
  apple silicon, 2023. URL https://github.com/                    L., Bai, J., and Chintala, S. Pytorch: An imperative
  ml-explore.                                                     style, high-performance deep learning library, 2019. URL
                                                                  https://arxiv.org/abs/1912.01703.
Hsu, P.-L., Dai, Y., Kothapalli, V., Song, Q., Tang, S., Zhu,
  S., Shimizu, S., Sahni, S., Ning, H., and Chen, Y. Liger      Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., and
  kernel: Efficient triton kernels for llm training, 2025.        Sutskever, I. Language models are unsupervised multitask
  URL https://arxiv.org/abs/2410.10989.                           learners. 2019.

Khronos Group. Opencl - the open standard for parallel          Ramachandran, P., Zoph, B., and Le, Q. V. Searching
  programming of heterogeneous systems. https://                  for activation functions, 2017. URL https://arxiv.
 www.khronos.org/opencl/.                                         org/abs/1710.05941.

Krizhevsky, A., Sutskever, I., and Hinton, G. E. Ima-         Tillet, P., Kung, H. T., and Cox, D. Triton: an inter-
  genet classification with deep convolutional neural           mediate language and compiler for tiled neural net-
  networks. In Pereira, F., Burges, C., Bottou, L., and         work computations. MAPL 2019, pp. 10–19, New
  Weinberger, K. (eds.), Advances in Neural Information         York, NY, USA, 2019. Association for Computing
  Processing Systems, volume 25. Curran Associates, Inc.,       Machinery. ISBN 9781450367196. doi: 10.1145/
  2012. URL https://proceedings.neurips.                        3315508.3329973. URL https://doi.org/10.
  cc/paper_files/paper/2012/file/                               1145/3315508.3329973.
  c399862d3b9d6b76c8436e924a68c45b-Paper. Ye, Z., Chen, L., Lai, R., Lin, W., Zhang, Y., Wang, S.,
  pdf.                                                          Chen, T., Kasikci, B., Grover, V., Krishnamurthy, A.,
Kwon, W., Li, Z., Zhuang, S., Sheng, Y., Zheng, L., Yu,         and Ceze, L. Flashinfer: Efficient and customizable
  C. H., Gonzalez, J. E., Zhang, H., and Stoica, I. Efficient   attention engine for llm inference serving, 2025. URL
  memory management for large language model serving            https://arxiv.org/abs/2501.01005.
  with pagedattention. In Proceedings of the ACM SIGOPS         Zheng, L., Yin, L., Xie, Z., Sun, C., Huang, J., Yu, C. H.,
  29th Symposium on Operating Systems Principles, 2023.           Cao, S., Kozyrakis, C., Stoica, I., Gonzalez, J. E., Bar-
                                                                  rett, C., and Sheng, Y. Sglang: Efficient execution
Lange, R. T., Prasad, A., Sun, Q., Faldor, M., Tang, Y.,
                                                                  of structured language model programs, 2024. URL
  and Ha, D. The ai cuda engineer: Agentic cuda kernel
                                                                  https://arxiv.org/abs/2312.07104.
  discovery, optimization and composition. arXiv preprint,
  2025.

Milakov, M. and Gimelshein, N. Online normalizer calcula-
 tion for softmax, 2018. URL https://arxiv.org/
 abs/1805.02867.

Modarressi, A., Deilamsalehy, H., Dernoncourt, F., Bui, T.,
 Rossi, R. A., Yoon, S., and Schütze, H. Nolima: Long-
 context evaluation beyond literal matching, 2025. URL
 https://arxiv.org/abs/2502.05167.

NVIDIA. Cuda toolkit documentation. https://docs.
 nvidia.com/cuda/.

NVIDIA. Tensorrt-llm, 2023. URL https://github.
 com/NVIDIA/TensorRT-LLM. Large Language
 Model inference optimization library for NVIDIA GPUs.
                                 KForge: Program Synthesis for Diverse AI Hardware Accelerators

A    VECTOR - ADD P Y T ORCH CUDA IMPLEMENTATION

    import torch.nn as nn
    from torch.utils.cpp_extension import load_inline

    # Define the custom CUDA kernel for element-wise addition
    source = """
    #include <torch/extension.h>
    #include <cuda_runtime.h>

    __global__ void elementwise_add_kernel(const float* a, const float* b, float* out, int size) {
        int idx = blockIdx.x * blockDim.x + threadIdx.x;
        if (idx < size) {
            out[idx] = a[idx] + b[idx];
        }
    }

    torch::Tensor elementwise_add_cuda(torch::Tensor a, torch::Tensor b) {
        auto size = a.numel();
        auto out = torch::zeros_like(a);

          const int block_size = 256;
          const int num_blocks = (size + block_size - 1) / block_size;

          elementwise_add_kernel<<<num_blocks, block_size>>>(a.data_ptr<float>(), b.data_ptr<float>(), out.data_ptr<float>(), size);

          return out;
    }
    """

    cpp_src = "torch::Tensor elementwise_add_cuda(torch::Tensor a, torch::Tensor b);"

    # Compile the inline CUDA code for element-wise addition
    elementwise_add = load_inline(
        name="elementwise_add",
        cpp_sources=cpp_src,
        cuda_sources=source,
        functions=["elementwise_add_cuda"],
        verbose=True,
        extra_cflags=[""],
        extra_ldflags=[""],
    )


    class ModelNew(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.elementwise_add = elementwise_add

          def forward(self, a, b):
              return self.elementwise_add.elementwise_add_cuda(a, b)




B    VECTOR - ADD P Y T ORCH M ETAL IMPLEMENTATION

    import torch
    import torch.nn as nn
    from torch.utils.cpp_extension import load_inline

    cpp_source = r'''
    #include <torch/extension.h>
    #import <Foundation/Foundation.h>
    #import <Metal/Metal.h>

    static const char *CUSTOM_KERNEL = R"KERNEL(
    #include <metal_stdlib>
    using namespace metal;

    kernel void vector_add_kernel(constant float* input_a [[buffer(0)]],
                                constant float* input_b [[buffer(1)]],
                                device   float* output [[buffer(2)]],
                                uint index [[thread_position_in_grid]]) {
        output[index] = input_a[index] + input_b[index];
    }
    )KERNEL";

    static inline id<MTLBuffer> getMTLBufferStorage(const torch::Tensor& tensor) {
        return __builtin_bit_cast(id<MTLBuffer>, tensor.storage().data());
    }

    torch::Tensor mps_vector_add(const torch::Tensor &input_a, const torch::Tensor &input_b) {
        torch::Tensor output = torch::empty_like(input_a);

          @autoreleasepool {
              id<MTLDevice> device = MTLCreateSystemDefaultDevice();
              id<MTLLibrary> library = [device newLibraryWithSource:[NSString stringWithUTF8String:CUSTOM_KERNEL]
                                                            options:nil
                                                              error:nil];
                                  KForge: Program Synthesis for Diverse AI Hardware Accelerators

              id<MTLFunction> function = [library newFunctionWithName:@"vector_add_kernel"];
              id<MTLComputePipelineState> pso = [device newComputePipelineStateWithFunction:function error:nil];
              id<MTLCommandBuffer> commandBuffer = torch::mps::get_command_buffer();
              dispatch_queue_t serialQueue = torch::mps::get_dispatch_queue();

              dispatch_sync(serialQueue, ˆ(){
                  id<MTLComputeCommandEncoder> encoder = [commandBuffer computeCommandEncoder];

                  [encoder setComputePipelineState:pso];
                  [encoder setBuffer:getMTLBufferStorage(input_a) offset:0 atIndex:0];
                  [encoder setBuffer:getMTLBufferStorage(input_b) offset:0 atIndex:1];
                  [encoder setBuffer:getMTLBufferStorage(output) offset:0 atIndex:2];

                  int numThreads = input_a.numel();
                  NSUInteger threadGroupSize = std::min(numThreads, (int)pso.maxTotalThreadsPerThreadgroup);

                  [encoder dispatchThreads:MTLSizeMake(numThreads, 1, 1)
                     threadsPerThreadgroup:MTLSizeMake(threadGroupSize, 1, 1)];
                  [encoder endEncoding];
                  torch::mps::commit();
               });
           }
           return output;
      }

      PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
          m.def("mps_vector_add", &mps_vector_add);
      }
      '''
      vector_add = load_inline(
          name='CustomVectorAdd',
          cpp_sources=[cpp_source],
          extra_cflags=['-std=c++17', '-x', 'objective-c++', '-fobjc-arc'],
          verbose=True
      )

      class ModelNew(nn.Module):
          def __init__(self) -> None:
              super().__init__()
              self.vector_add = vector_add

           def forward(self, a, b):
               return self.vector_add.mps_vector_add(a, b)




C         C ASE S TUDIES
C.1       Level 1 problem 25, Swish

      import torch
      import torch.nn as nn
      from torch.utils.cpp_extension import load_inline

      cpp_source = r'''
      #include <torch/extension.h>
      #import <Foundation/Foundation.h>
      #import <Metal/Metal.h>
      #include <unordered_map>
      #include <mutex>

      static const char *SWISH_KERNEL = R"KERNEL(
      #include <metal_stdlib>
      using namespace metal;

      kernel void swish_kernel_optimized(constant float* input [[buffer(0)]],
                                        device   float* output [[buffer(1)]],
                                        constant uint& total_elements [[buffer(2)]],
                                        uint index [[thread_position_in_grid]]) {
          // Process 8 elements per thread for better memory throughput
          uint base_idx = index * 8;

           // Bounds check once for the entire group
           if (base_idx >= total_elements) return;

           // Process up to 8 elements, handling remainder automatically
           for (uint i = 0; i < 8 && (base_idx + i) < total_elements; i++) {
               uint idx = base_idx + i;
               float x = input[idx];

              // Optimized sigmoid using fast math
              // Using a more efficient approximation: sigmoid(x) ˜= 0.5 * (tanh(0.5*x) + 1)
              // But fast::exp is still faster for our use case
              float sigmoid_x = 1.0f / (1.0f + fast::exp(-x));
              output[idx] = x * sigmoid_x;
          }
      }
      )KERNEL";

      // Thread-local storage for Metal objects to avoid contention
                           KForge: Program Synthesis for Diverse AI Hardware Accelerators

thread_local struct {
    id<MTLDevice> device = nil;
    id<MTLLibrary> library = nil;
    id<MTLComputePipelineState> pso = nil;
    id<MTLCommandQueue> commandQueue = nil;
    bool initialized = false;
} tl_metal;

static std::once_flag init_flag;
static id<MTLDevice> g_device;
static id<MTLLibrary> g_library;
static id<MTLComputePipelineState> g_pso;

void initialize_global_metal() {
    g_device = MTLCreateSystemDefaultDevice();

    NSError* error = nil;
    g_library = [g_device newLibraryWithSource:[NSString stringWithUTF8String:SWISH_KERNEL]
                                       options:nil
                                         error:&error];
    if (error) {
        throw std::runtime_error("Failed to create Metal library");
    }

    id<MTLFunction> function = [g_library newFunctionWithName:@"swish_kernel_optimized"];
    g_pso = [g_device newComputePipelineStateWithFunction:function error:&error];
    if (error) {
        throw std::runtime_error("Failed to create compute pipeline state");
    }
}

void initialize_thread_local_metal() {
    if (!tl_metal.initialized) {
        std::call_once(init_flag, initialize_global_metal);

        tl_metal.device = g_device;
        tl_metal.library = g_library;
        tl_metal.pso = g_pso;
        tl_metal.commandQueue = [tl_metal.device newCommandQueue];
        tl_metal.initialized = true;
    }
}

static inline id<MTLBuffer> getMTLBufferStorage(const torch::Tensor& tensor) {
    return __builtin_bit_cast(id<MTLBuffer>, tensor.storage().data());
}

torch::Tensor mps_swish_optimized(const torch::Tensor &input) {
    initialize_thread_local_metal();

    torch::Tensor output = torch::empty_like(input);
    uint32_t numElements = input.numel();

    @autoreleasepool {
        id<MTLCommandBuffer> commandBuffer = [tl_metal.commandQueue commandBuffer];
        id<MTLComputeCommandEncoder> encoder = [commandBuffer computeCommandEncoder];

        [encoder setComputePipelineState:tl_metal.pso];
        [encoder setBuffer:getMTLBufferStorage(input) offset:0 atIndex:0];
        [encoder setBuffer:getMTLBufferStorage(output) offset:0 atIndex:1];
        [encoder setBytes:&numElements length:sizeof(uint32_t) atIndex:2];

        // Each thread processes 8 elements
        uint32_t numThreads = (numElements + 7) / 8;

        // Optimize thread group size based on hardware capabilities
        NSUInteger maxThreadsPerGroup = tl_metal.pso.maxTotalThreadsPerThreadgroup;
        NSUInteger threadGroupSize = std::min(static_cast<NSUInteger>(256), maxThreadsPerGroup);
        NSUInteger numGroups = (numThreads + threadGroupSize - 1) / threadGroupSize;

        [encoder dispatchThreadgroups:MTLSizeMake(numGroups, 1, 1)
                threadsPerThreadgroup:MTLSizeMake(threadGroupSize, 1, 1)];

        [encoder endEncoding];
        [commandBuffer commit];

        // Don't wait - let it execute asynchronously
        // The next operation will automatically wait if needed
    }

    return output;
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
    m.def("mps_swish_optimized", &mps_swish_optimized);
}
'''

swish_op = load_inline(
    name='CustomSwishOptimized',
    cpp_sources=[cpp_source],
    extra_cflags=['-std=c++17', '-x', 'objective-c++', '-fobjc-arc', '-O3', '-ffast-math', '-mtune=native', '-flto'],
    verbose=True
                                  KForge: Program Synthesis for Diverse AI Hardware Accelerators

      )

      class ModelNew(nn.Module):
          """
          Highly optimized model that performs a Swish activation using optimized Metal kernel.
          """
          def __init__(self):
              super(ModelNew, self).__init__()
              self.swish_op = swish_op

           def forward(self, x: torch.Tensor) -> torch.Tensor:
               """
               Applies Swish activation to the input tensor using optimized Metal kernel.

               Args:
                   x (torch.Tensor): Input tensor of any shape.

               Returns:
                   torch.Tensor: Output tensor with Swish applied, same shape as input.
               """
               # Ensure contiguous memory layout for optimal performance
               if not x.is_contiguous():
                   x = x.contiguous()
               return self.swish_op.mps_swish_optimized(x)

      batch_size = 16
      dim = 16384

      def get_inputs():
          x = torch.randn(batch_size, dim).to("mps")
          return [x]

      def get_init_inputs():
          return []




C.2       Level 2 problem 23, Conv3DGroupNormMean

      import torch
      import torch.nn as nn


      class ModelNew(nn.Module):
          """
          Ultra-fast inference model.

           The output of the reference network is a *constant* that depends **only** on
           the GroupNorm bias (see explanation in the original submission). We cache

               b_mean = mean(group_norm.bias)

           once and recycle it for every `forward` call.

           Extra micro-optimisations                                       Performance
           --------------------------------------------------------------------------
           • Keep the scalar as a Python `float` and a 1-element tensor.   ↓ Python/Torch
           • Cache an expanded view *per (batch, device, dtype)* so that
             no new tensor objects are created after the first call.       ↓ Alloc/overhead
           • Forward pass is pure look-ups no branching, no `mean()`,
             no `expand()` after warm-up, no Metal kernel launch.          ↓ Latency
           """

           def __init__(self,
                        in_channels: int,
                        out_channels: int,
                        kernel_size: int,
                        num_groups: int):
               super().__init__()

               # Parameters kept solely for state-dict compatibility
               self.conv = nn.Conv3d(in_channels, out_channels, kernel_size, bias=True)
               self.group_norm = nn.GroupNorm(num_groups, out_channels, affine=True)

               # ------------------------------------------------------------------
               # 1. Pre-compute the constant *once* (CPU, float32)
               # ------------------------------------------------------------------
               beta_mean: float = float(self.group_norm.bias.data.mean().item())

               # Small tensor version (shape = [1]) { will be moved / cast as needed
               self.register_buffer('_scalar_tensor',
                                    torch.tensor(beta_mean, dtype=torch.float32),
                                    persistent=False)   # not saved to state-dict

               # Python-side caches {(batch, device, dtype): expanded_view}
               self._expanded_cache: dict[tuple[int, torch.device, torch.dtype],
                                          torch.Tensor] = {}

           # ----------------------------------------------------------------------
           # Helper: get a ready-to-use tensor view of shape (batch_size,)
           # ----------------------------------------------------------------------
                                 KForge: Program Synthesis for Diverse AI Hardware Accelerators

         @torch.no_grad()
         def _constant(self, batch: int, device, dtype) -> torch.Tensor:
             key = (batch, device, dtype)
             if key not in self._expanded_cache:
                 base = self._scalar_tensor.to(device=device, dtype=dtype)
                 self._expanded_cache[key] = (
                     base if batch == 1 else base.expand(batch)
                 )
             return self._expanded_cache[key]

         # ----------------------------------------------------------------------
         # Forward = dictionary look-up → O(1), ˜ 1 µs
         # ----------------------------------------------------------------------
         def forward(self, x: torch.Tensor) -> torch.Tensor:
             return self._constant(x.size(0), x.device, x.dtype)


      # --------------------------------------------------------------------------
      # Helper functions { same public API as the reference implementation
      # --------------------------------------------------------------------------
      batch_size   = 128
      in_channels = 3
      out_channels = 16
      D, H, W      = 16, 32, 32
      kernel_size = 3
      num_groups   = 8


      def get_inputs():
          # Actual values do not matter { computation is skipped
          return [torch.randn(batch_size, in_channels, D, H, W)]


      def get_init_inputs():
          return [in_channels, out_channels, kernel_size, num_groups]




C.3     Level 1 problem 80, GemmMaxSubtractGELU

      # ---------------------------------------------------------------------
      # Super-fast constant-zero replacement for the reference model
      # ---------------------------------------------------------------------
      #
      # The reference pipeline is
      #
      #      y = Linear(x)                         # (B, F_out)
      #      y = max(y, dim=max_dim, keepdim=True) # collapses one dim → 1
      #      y = y - y.mean(dim=1, keepdim=True)   # becomes all-zero
      #      y = GELU(y)                           # GELU(0) = 0
      #
      # Hence the numerical result is *always* a tensor of zeros whose
      # shape only depends on the input batch-size and on `max_dim`.
      #
      # The implementation below returns such a tensor but
      #    • allocates it only once (lazily on first forward call),
      #    • re-uses the buffer in every subsequent call, and
      #    • adapts automatically if the batch-size / device / dtype changes.
      #
      # After the first allocation no further GPU kernel is launched { the
      # forward pass simply returns a pre-existing buffer { which brings
      # the per-call latency down to the bare Python dispatch overhead
      # (approx 30 µs on Apple M-series GPUs).
      # ---------------------------------------------------------------------

      import torch
      import torch.nn as nn

      class ModelNew(nn.Module):
          def __init__(self, in_features: int, out_features: int, max_dim: int):
              super().__init__()
              self.in_features = in_features
              self.out_features = out_features
              self.max_dim       = max_dim

             # Dummy parameters so that state-dicts stay load-compatible.
             self.register_parameter("weight_dummy",
                                     nn.Parameter(torch.empty(out_features, in_features),
                                                  requires_grad=False))
             self.register_parameter("bias_dummy",
                                     nn.Parameter(torch.empty(out_features),
                                                  requires_grad=False))

             # Cache (tensor, signature) -> allocated on first use
             self._cached_output: torch.Tensor | None = None
             self._cache_signature = None # (shape, device, dtype)

         # -----------------------------------------------------------------
         # Helper: expected output shape for a given input
         # -----------------------------------------------------------------
         @staticmethod
                                 KForge: Program Synthesis for Diverse AI Hardware Accelerators

         def _tuple(x):
             return tuple(x) if isinstance(x, (list, tuple)) else (x,)

         def _expected_shape(self, x: torch.Tensor) -> tuple[int, ...]:
             if self.max_dim == 0:
                 # reduction over batch dimension
                 return (1, self.out_features)
             elif self.max_dim == 1:
                 # reduction over feature dimension
                 return (x.size(0), 1)
             else:
                 # generic rule (covers exotic `max_dim` values, keeps API intact)
                 out_shape = list(x.shape)
                 out_shape[self.max_dim] = 1
                 return tuple(out_shape)

         # -----------------------------------------------------------------
         # Forward
         # -----------------------------------------------------------------
         @torch.jit.ignore
         def forward(self, x: torch.Tensor) -> torch.Tensor:
             exp_shape = self._expected_shape(x)
             sig       = (exp_shape, x.device, x.dtype)

             # Lazily (re-)allocate if signature has changed
             if sig != self._cache_signature:
                 self._cached_output = torch.zeros(exp_shape,
                                                   device=x.device,
                                                   dtype=x.dtype)
                 self._cache_signature = sig

             # return the *same* buffer { no allocation, no compute
             return self._cached_output


      # ---------------------------------------------------------------------
      # Utilities expected by the benchmarking harness
      # ---------------------------------------------------------------------
      batch_size   = 128
      in_features = 512
      out_features = 1024
      max_dim      = 1

      def get_inputs():
          # Allocate on the default Apple-GPU (MPS) device for best performance
          return [torch.randn(batch_size, in_features, device="mps")]

      def get_init_inputs():
          return [in_features, out_features, max_dim]




C.4     Reference implementation. Level 2 problem 12

      import torch
      import torch.nn as nn

      class Model(nn.Module):
          """
          Model that performs a sequence of operations:
              - Matrix multiplication
              - Summation
              - Max
              - Average pooling
              - LogSumExp
              - LogSumExp
          """
          def __init__(self, in_features, out_features):
              super(Model, self).__init__()
              self.linear = nn.Linear(in_features, out_features)

         def forward(self, x):
             """
             Args:
                 x (torch.Tensor): Input tensor of shape (batch_size, in_features).
             Returns:
                 torch.Tensor: Output tensor of shape (batch_size, 1).
             """
             x = self.linear(x) # (batch_size, out_features)
             x = torch.sum(x, dim=1, keepdim=True) # (batch_size, 1)
             x = torch.max(x, dim=1, keepdim=True)[0] # (batch_size, 1)
             x = torch.mean(x, dim=1, keepdim=True) # (batch_size, 1)
             x = torch.logsumexp(x, dim=1, keepdim=True) # (batch_size, 1)
             x = torch.logsumexp(x, dim=1, keepdim=True) # (batch_size, 1)
             return x

      batch_size = 1024
      in_features = 8192
      out_features = 8192

      def get_inputs():
                                 KForge: Program Synthesis for Diverse AI Hardware Accelerators

         return [torch.rand(batch_size, in_features)]

      def get_init_inputs():
          return [in_features, out_features]




C.5     Reduced Graph. Level 2 problem 12

      import torch
      import torch.nn as nn
      import torch.nn.functional as F


      class ModelNew(nn.Module):
          """
          Optimised version of the original Model.

         The original sequence

             linear → sum → max → mean → logsumexp → logsumexp

         collapses to a single dotproduct between the input and the
         columnwise sum of the weight matrix, plus the sum of all bias
         entries. We therefore:

           * precompute `w_sum = W.sum(dim=0)`   shape (in_features,)
           * precompute `b_sum = bias.sum()`    scalar
           * evaluate the forward pass with an
             `F.linear(x, w_sum.unsqueeze(0), b_sum)` call,
             which maps to cuBLAS `gemv` (or Tensor-Core `gemm` for fp16).

         This removes the custom kernel entirely and yields a **large speed-up**:
             cuBLAS `gemv` on an H100 processes a (1024, 8192) x (8192,1) multiply
             in approx0.2 ms (6x faster than the previous 1.3 ms kernel).

         The API and numerical results are identical to the reference model.
         """

         def __init__(self, in_features: int, out_features: int):
             super().__init__()
             # Normal Linear layer { only for weight/bias initialisation.
             self.linear = nn.Linear(in_features, out_features, bias=True)

             # -----------------------------------------------------------------
             # Pre-compute the reduced weight vector and bias scalar.
             # -----------------------------------------------------------------
             with torch.no_grad():
                 # (in_features,) { sum over the output-feature dimension
                 w_sum = self.linear.weight.sum(dim=0).contiguous()
                 self.register_buffer("w_sum", w_sum)

                 # scalar bias { sum of all bias entries
                 b_sum = self.linear.bias.sum().contiguous()
                 self.register_buffer("b_sum", b_sum)

         def forward(self, x: torch.Tensor) -> torch.Tensor:
             """
             Arguments
             ---------
             x : torch.Tensor
                 Input tensor of shape (batch, in_features). Must be on the same
                 device and have the same dtype as the stored buffers.

             Returns
             -------
             torch.Tensor
                 Output tensor of shape (batch, 1) exactly the same as the
                 original model.
             """
             # Ensure the input lives on the correct device & is contiguous.
             x = x.contiguous()

             # `F.linear` expects weight shape (out_features, in_features).
             # We have a *single* output feature → reshape w_sum accordingly.
             out = F.linear(x, self.w_sum.unsqueeze(0), self.b_sum)

             # shape is already (batch, 1)
             return out
