                                                AMDKernelVault: Large-Scale Datasets and Agentic Training for
                                                            AMD GPU Kernel Optimization
                                                   Ji Liu∗,†  Saptarshi Majumder∗,† Yiqing Huang∗,† Wenwen Ouyang∗,†
                                                              Umang Pandey Zeping Li Chushi Chen Zihao An
                                                               Puyuan Yang Zekai Li Sina Rafati Ziqiong Liu
                                                               Pratik Prabhanjan Brahma Dong Li Zicheng Liu
                                                                          Sharon Zhou Emad Barsoum
                                                                          Advanced Micro Devices, Inc.
                                         *
                                           Equal contribution. Correspondence: {liuji,sapmajum,Cody.Huang,viouyang}@amd.com.
                                                                †



                                                                Abstract                              et al., 2025). However, the data and tooling be-
                                                                                                      hind these systems remain largely CUDA/NVIDIA-
arXiv:2609.12471v1 [cs.CL] 11 Sep 2026




                                              We introduce AMDKernelVault, an open HIP                centric. In contrast, AMD’s HIP/ROCm (Advanced
                                              and Triton kernel corpus and training frame-            Micro Devices, Inc., 2025c,a) ecosystem lacks
                                              work for recent AMD CDNA GPUs. Ex-
                                                                                                      large-scale, execution-verified kernel data for train-
                                              isting LLM-based kernel agents are largely
                                              CUDA/NVIDIA-centric and often depend on                 ing and evaluating kernel LLMs, especially across
                                              repeated frontier-LLM calls for generation, re-         both native HIP and Triton backends.
                                              flection, and optimization. To address this                This data gap is not a matter of syntax conver-
                                              gap, we develop HIPKernelGen and TritonKer-             sion alone. Although CUDA and HIP expose sim-
                                              nelGen, agent-driven pipelines that transform           ilar programming abstractions, performant AMD
                                              PyTorch references into HIP or Triton ker-              kernels depend on ROCm compilation behavior,
                                              nels, compile and validate candidates under
                                                                                                      wavefront execution, LDS usage, memory coa-
                                              ROCm, and latency-profile them on AMD hard-
                                              ware. The corpus contains 62,153 execution-
                                                                                                      lescing, matrix-core support, and Triton (Tillet
                                              verified HIP kernel samples, 2,377 production-          et al., 2019) backend constraints. Direct transla-
                                              grounded ROCm Libraries QA entries, and                 tion through hipify (Advanced Micro Devices,
                                              39,893 Triton kernels. We further train Qwen3-          Inc., 2025b) may preserve API structure while re-
                                              8B with supervised fine-tuning and execution-           taining NVIDIA-shaped tiling constants, warp-size
                                              aware reinforcement learning as a demonstra-            assumptions, input-specialized indexing, or mem-
                                              tion of the corpus’s utility. Under fixed evalua-       ory layouts that fail to compile or underperform
                                              tion budgets, it achieves the highest correctness
                                                                                                      on AMD GPUs. Reliable AMD kernel data there-
                                              among the compared models on PyTorch-to-
                                              HIP (34.0% Pass@1), TritonBench-G (33.2%                fore requires native compilation, execution-based
                                              Corr@3), and ROCmBench (41.94% Corr@3),                 correctness validation, and latency measurement
                                              but does not uniformly lead compilation or              under ROCm.
                                              speed metrics. The corpus and documenta-                   We present AMDKernelVault, an open,
                                              tion are available at https://huggingface.              execution-verified HIP and Triton (Tillet et al.,
                                              co/datasets/amd/AIG-Datasets, and the as-               2019) kernel corpus together with scalable agent-
                                              sociated training and kernel-generation code is
                                                                                                      based pipelines for AMD GPU kernel data produc-
                                              available at https://github.com/AMD-AGI/
                                              hip_kernel_llm_lab.
                                                                                                      tion. Our pipelines, HIPKernelGen and TritonKer-
                                                                                                      nelGen, start from PyTorch references and use a
                                          1   Introduction                                            generate–evaluate–reflect loop to synthesize candi-
                                                                                                      date kernels, compile them under ROCm, validate
                                          Recent advances in GPU kernel optimization                  numerical correctness across test inputs, and profile
                                          have been driven by LLM-based (Chen et al.,                 latency on AMD hardware. This process produces
                                          2025; Baronio et al., 2026) and agent-based ap-             64K+ validated HIP/ROCm data and ∼40K Tri-
                                          proaches (Wang et al., 2025a; Dai et al., 2026),            ton kernels for recent AMD CDNA GPUs, includ-
                                          together with standardized benchmarks such as Ker-          ing benchmark-derived tasks, synthesized operator
                                          nelBench (Ouyang et al., 2025; Lange et al., 2025b;         workloads, and production-grounded supervision
                                          Heakl et al., 2026). These agent-based systems              from rocBLAS and rocSOLVER.
                                          leverage compiler feedback, runtime correctness                Beyond releasing data, we evaluate whether this
                                          checks, and performance profiling to iteratively re-        corpus can train compact AMD kernel LLMs that
                                          fine generated kernels (Wang et al., 2025a; Chen            reduce reliance on frontier LLMs in agentic opti-

                                                                                                  1
mization systems. Existing kernel-agent workflows            2   Related Work
often call frontier models repeatedly for generation,
reflection, and optimization, which increases cost           GPU Kernel Optimization. GPU kernel op-
and limits deployment in private AMD environ-                timization is a longstanding problem in high-
ments. Using AMDKernelVault, we train Qwen3-                 performance ML systems (Ragan-Kelley et al.,
8B (Yang et al., 2025) with supervised fine-tuning           2013; Chen et al., 2018; Vasilache et al., 2018).
and execution-aware reinforcement learning, then             Significant efforts have focused on operator fusion,
insert the trained model into a GEAK-style (Wang             tiling, memory hierarchy optimization, and cus-
et al., 2025a) agent loop where one local policy             tom kernel design. Representative systems such as
serves as generator, reflector, and optimizer. The           FlashAttention (Dao et al., 2022; Shah et al., 2024)
training recipe is intended as an effectiveness test         show that carefully designed kernels can provide
for the corpus and pipeline rather than a new RL             substantial speedups for modern ML workloads.
algorithm.                                                   More recently, automated frameworks have used
                                                             program analysis, search, and learning-based tech-
   Under the same evaluation budget, the trained
                                                             niques (Zheng et al., 2020) to reduce the manual
8B model achieves the highest correctness among
                                                             effort required for kernel tuning. However, most of
the compared models on PyTorch-to-HIP (34.0%
                                                             these methods are developed and evaluated primar-
Pass@1) and TritonBench-G (33.2% Corr@3),
                                                             ily on Nvidia GPUs and CUDA backends, leaving
while running locally on AMD hardware. These
                                                             AMD-focused kernel optimization comparatively
results show that execution-verified AMD kernel
                                                             underexplored.
data can support locally deployable kernel LLMs
for ROCm environments. Our primary contribution              HIP, Triton, and ROCm. AMD’s HIP pro-
is the resource and its AMD-native generation and            vides a CUDA-like programming model within the
validation infrastructure; the SFT+RL recipe is an           ROCm software stack (Advanced Micro Devices,
effectiveness demonstration rather than a new learn-         Inc., 2025c,a), while Triton offers a Python-based
ing algorithm. Comparisons with frontier mod-                DSL for writing custom GPU kernels with explicit
els are specific to the reported correctness metrics,        control over memory and parallelism (Tillet et al.,
benchmarks, and agent budgets.                               2019). Although these abstractions improve porta-
                                                             bility, AMD execution differs in ROCm compiler
Our contributions:                                           behavior, wavefront-level execution, LDS usage,
                                                             memory coalescing, and backend scheduling con-
                                                             straints. Source-to-source tools such as hipify can
• AMD-native kernel corpus. We release 64K+                  preserve syntax but provide limited guarantees of
  HIP/ROCm and ∼40K Triton data validated                    correctness or performance portability (Advanced
  through ROCm compilation, execution-based                  Micro Devices, Inc., 2025b). This motivates native
  correctness tests, latency profiling, or production-       HIP/ROCm validation rather than treating AMD
  grounded HIP code supervision on recent AMD                support as a post-hoc translation step.
  CDNA GPUs.
                                                             GPU Kernel Datasets and Benchmarks. High-
• Scalable data production pipelines. HIPKer-                quality datasets are essential for advancing kernel
  nelGen and TritonKernelGen provide reusable                optimization research. KernelBench (Ouyang et al.,
  agent-based generate–evaluate–reflect workflows            2025) provides standardized environments for gen-
  for producing verified HIP and Triton kernel data          erating and evaluating optimized kernels, while
  from PyTorch references, including benchmark-              other benchmarks cover specific operator fami-
  derived, synthesized, and production-grounded              lies (Che et al., 2009). However, existing resources
  sources.                                                   remain largely CUDA-centric. CASS (Heakl et al.,
                                                             2026) facilitates CUDA-to-HIP translation, but
• Compact AMD kernel LLMs. As a corpus-                      does not provide large-scale PyTorch-to-HIP, HIP-
  utility demonstration, we train a local Qwen3-8B           to-HIP, or AMD Triton data. Existing Triton bench-
  model to serve the generator, reflector, and op-           marks also primarily target NVIDIA assumptions
  timizer roles in a GEAK-style loop, improving              that may not generalize to ROCm. AMDKernel-
  specific AMD HIP/Triton correctness metrics un-            Vault addresses this gap by constructing a unified
  der the same evaluation budget.                            HIP/Triton corpus validated through compilation,

                                                         2
Figure 1: Unified kernel generation framework. Stage 1 standardizes PyTorch modules into function-style
references. Stage 2 synthesizes HIP and Triton kernels using a GEAK-based agentic loop with compilation,
correctness validation, and latency-guided optimization.


execution-based correctness checks, and latency            Within this unified design, we instantiate two con-
profiling on AMD GPUs.                                     crete pipelines—HIPKernelGen and TritonKer-
                                                           nelGen—which specialize the same agent-driven
LLM-Based Kernel Agents. Recent work ex-
                                                           workflow to the HIP and Triton ecosystems respec-
plores LLM-based agents for kernel synthesis
                                                           tively.
and optimization (Chen et al., 2025; Baronio
et al., 2026; Li et al., 2025b; Wang et al., 2025a).       Stage 1: PyTorch Reference Standardization.
Kevin (Baronio et al., 2026) demonstrates multi-           For each target operator or module kernel, we con-
turn RL for CUDA kernels, AutoTriton (Li et al.,           struct a function-style PyTorch reference derived
2025b) and TritonRL (Woo et al., 2025) study               from the PyTorch module input. This represen-
execution-aware training for Triton generation, and        tation ensures reliable invocation, consistent in-
GEAK (Wang et al., 2025a) provides an agentic              terface semantics, and execution-based validation
framework for Triton optimization. AVO (Chen               across both HIP and Triton backends. When avail-
et al., 2026) further explores long-horizon au-            able, compiler-generated kernels (e.g., Torch In-
tonomous kernel evolution on NVIDIA GPUs.                  ductor Triton code) are used for cross-checking but
AMDKernelVault is complementary: it focuses on             do not replace reference-based correctness.
execution-verified AMD HIP/ROCm/Triton data
and compact local policies for generate–evaluate–          Stage 2: Backend-Specific Kernel Synthe-
reflect loops. Additional discussion is provided in        sis. Given the standardized PyTorch reference,
Appendix B.                                                backend-specific agents generate candidate GPU
                                                           kernels. Each candidate is subjected to compila-
3     Agent-Based Dataset Generation                       tion, execution-based correctness checks against
                                                           the PyTorch reference, and latency profiling. The
We present a unified framework for generating              default HIP checker uses torch.allclose with
execution-verified GPU kernels across both HIP             rtol=1e-4, atol=1e-4, and equal_nan=True.
and Triton, using a shared generate–evaluate–              For Triton, task-specific tolerances may be
reflect paradigm (Figure 1).                               configured from the reference task; otherwise,
3.1    Unified Pipeline Architecture                       the fallback is rtol=1e-4, atol=1e-3, and
                                                           equal_nan=False. We use no fixed dtype- or
We propose a unified, agent-driven framework for           operator-specific rule. Failures trigger reflector-
large-scale GPU kernel data construction. The              guided regeneration until correctness criteria are
framework follows a shared generate–evaluate–              met or the attempt limit is reached.
reflect paradigm, enabling systematic synthe-
sis, validation, and refinement of GPU kernels             Test-case construction and validation. For
grounded in standardized PyTorch references.               PyTorch→HIP and PyTorch→Triton, test

                                                       3
inputs are inherited from CUDA-Agent-Ops-                execution-based filtering. We use it as a source for
6K (Dai et al., 2026), GPUMode (Paliskara                HIP generation, but the original dataset remains
and Saroufim, 2025) and AI-CUDA-Engineer-                CUDA-centric and does not directly support HIP
Archive (Lange et al., 2025a) when available and         or ROCm.
augmented with verified LLM-generated cases
to cover additional shapes, strides, dtypes, and         3.2.2   GPUMODE-KernelBook Dataset
boundary conditions. HIP kernels, including              The GPUMODE-KernelBook (Paliskara and
HIP→HIP optimization targets, are bound through          Saroufim, 2025) dataset contains approximately
torch.utils.cpp_extension so that generated              18,000 PyTorch modules paired with Torch Induc-
kernels can be executed under the same PyTorch           tor Triton implementations from GitHub-derived
reference tests. For Triton→Triton, we extend            workloads. It provides broad operator coverage
TritonBench-style tests with ROCm-compatible             across primitives, fused kernels, and larger model
cases and discard candidates that only pass              components, but remains CUDA/Triton-centric and
input-specialized or shape-specialized checks.           does not directly provide AMD-validated HIP ker-
Thus, LLM-generated tests are not accepted               nels.
as supervision by themselves; they are used
as additional probes inside an execution-based           3.2.3   AI-CUDA-Engineer-Archive Dataset
validation loop.
                                                         The AI-CUDA-Engineer-Archive (Lange et al.,
HIPKernelGen. HIPKernelGen instantiates the              2025a) dataset is built with the AI CUDA Engineer
unified framework for HIP kernels targeting AMD          framework from over 250 KernelBench PyTorch
GPUs. Much of the HIP corpus was generated               benchmarks. It provides PyTorch references, gen-
from August to December 2025 using GPT-5, a              erated CUDA kernels, diagnostics, and profiling
strong available kernel-generation model during          results, but remains CUDA-centric and does not
collection. Each candidate is compiled via hipcc,        directly support HIP.
validated against PyTorch references, and profiled
for latency and speedup. Retention depends on            3.2.4   Stack-v2-dedup-Triton Dataset
ROCm execution rather than generator identity.
                                                         We incorporate the curated Stack-v2-dedup-
TritonKernelGen. TritonKernelGen mirrors the             Triton (Lozhkov et al., 2024) dataset, constructed
HIP pipeline for Triton kernels. We use GPT-oss-         by filtering approximately 13,000 candidate sam-
120B (Agarwal et al., 2025), DeepSeek-R1 (Guo            ples to obtain 2,269 high-quality Triton–PyTorch
et al., 2025), and Qwen2.5-32B (Qwen et al., 2025)       pairs. This source provides medium-difficulty Tri-
to diversify implementations and reasoning traces.       ton examples emphasizing correctness and moder-
Each kernel is compiled and executed via Triton          ate complexity.
3.3.0 and tested on approximately ten correctness
and three performance configurations spanning            3.2.5   TritonBench-8k Dataset
shapes, strides, FP32/FP16/BF16 where applica-
                                                         The TritonBench-8k (Li et al., 2025a) dataset con-
ble, and boundary cases.
                                                         sists of samples derived from web crawl data
3.2     Source Data                                      and synthetic code generated via the Ninetoothed
                                                         DSL (Huang et al., 2025). We apply targeted cu-
Our kernel datasets are built upon six complemen-        ration to remove DSL-specific artifacts and ensure
tary sources spanning synthesized CUDA-agent             correctness across diverse shapes, strides, and pre-
tasks, GitHub-derived PyTorch programs, curated          cision types.
Triton corpora, benchmark-style kernels, and pro-
duction ROCm libraries.                                  3.2.6   ROCm Libraries Dataset Source
3.2.1    CUDA-Agent-Ops-6K Dataset                       As a production-oriented source, we leverage
The CUDA-Agent-Ops-6K dataset (Dai et al., 2026)         AMD’s ROCm Libraries monorepo, focusing on
contains 6,000 synthesized operator-level PyTorch        rocBLAS and rocSOLVER. Unlike benchmark-style
tasks for CUDA kernel generation and optimiza-           datasets, these libraries capture engineering-tested
tion. It is built from torch/transformers seed op-       HIP kernels, launch-side logic, and idiomatic pro-
erators, LLM-composed multi-operator tasks, and          duction patterns.

                                                     4
      Dataset                              Samples           samples.
      HIP/ROCm Datasets                                         HIP-GPUMode: Generated from GPUMODE-
      HIP-CudaAgent                          5,388           KernelBook using HIPKernelGen. We first convert
      HIP-GPUMode                           22,397
      HIP2HIP (Optimization)                34,368
                                                             PyTorch modules to function-style references, then
      ROCm Libraries QA                      2,377           generate HIP kernels using frontier LLMs. Each
      Total HIP/ROCm                        64,530           candidate undergoes compilation, execution-based
      Triton Datasets
                                                             validation, and latency profiling. The generate–
      Triton-Stack                           2,269           evaluate–reflect loop iterates until correctness is
      Triton-Bench (from TritonBench-8k)     7,713           achieved or a maximum attempt limit is reached.
      Triton-GPUMode                        18,000
      Triton-AICE                           11,911
                                                             This produces 5,910 unique PyTorch entries with
                                                             22,397 HIP kernel variants (avg 3.8 variants/entry).
      Total Triton                          39,893
                                                                HIP2HIP: We extend HIPKernelGen to kernel-
Table 1: Summary of the corpus used in this paper. HIP       to-kernel optimization by operating directly on ex-
and Triton kernel samples are execution-validated on         isting HIP kernel functions or operators. Using
AMD GPUs; ROCm Libraries QA provides production-             HIP-GPUMode as a base, we generate 34,368 vali-
grounded supervision.                                        dated HIP kernel optimization pairs.
                                                             ROCm Libraries QA. The ROCm Libraries
3.3    Generated Kernel Corpus                               QA subset contains production-grounded interface-
Table 1 summarizes our released corpus. HIP and              level supervision rather than generated kernel-
Triton kernel entries are processed through HIP-             pair data. For each interface in rocBLAS and
KernelGen/TritonKernelGen with execution-based               rocSOLVER, we identify kernel-relevant code re-
validation on AMD GPUs. The ROCm Libraries                   gions and generate QA pairs targeting computation
QA subset provides complementary production-                 semantics, index-to-tensor mappings, memory ac-
grounded supervision rather than generated kernel-           cess patterns, synchronization strategies, and edge
pair data.                                                   cases. This yields 1,858 entries from rocBLAS and
                                                             519 from rocSOLVER (2,377 total), capturing pro-
Counting and audit. The 64,530 HIP/ROCm to-                  duction HIP development patterns.
tal comprises 62,153 execution-verified HIP kernel
                                                             Triton Datasets. TritonKernelGen processes all
samples and 2,377 ROCm Libraries QA entries. It
                                                             Triton sources through a unified validation pipeline,
excludes a separately released 14,282-entry HIP-
                                                             validating numerical correctness across diverse ten-
AICUDA subset that was not used in this paper.
                                                             sor shapes, strides, and dtypes (FP32/FP16/BF16)
HIP-CudaAgent retains 5,388 of 6,000 upstream
                                                             on AMD GPUs.
tasks after excluding 612 incomplete records; HIP-
                                                                Triton-Stack: Curated from Stack-v2-dedup, fil-
GPUMode contains 5,910 unique tasks and 22,397
                                                             tering ∼13K candidates to 2,269 medium-difficulty
kernel variants; and HIP2HIP contains 31,155
                                                             Triton–PyTorch pairs with verified AMD compati-
single-turn and 3,213 multi-turn records. Triton
                                                             bility, then generated and execution-verified with
counts use 39,893 unique source-level samples;
                                                             TritonKernelGen.
packaged reasoning variants may yield a different
                                                                Triton-Bench: Derived from TritonBench-8k,
row count. Since rejection logs were not aggre-
                                                             removing DSL-specific artifacts and validating
gated uniformly across source pipelines, we re-
                                                             7,713 samples, generated and execution-verified
port retained counts and subset-specific validation
                                                             with TritonKernelGen.
rather than a single corpus-wide failure rate.
                                                                Triton-GPUMode: Sourced from GPUMODE-
HIP Datasets. HIP-CudaAgent: Built from                      KernelBook (∼18K entries), with Triton imple-
CUDA-Agent-Ops-6K using HIPKernelGen. We                     mentations ported from torch-compile kernels to
adapt the synthesized PyTorch operator tasks into            generic kernels able to handle all shapes and
function-style references and use the generate–              params, generated and execution-verified with Tri-
evaluate–reflect pipeline to produce HIP implemen-           tonKernelGen.
tations. Each candidate is compiled with the ROCm               Triton-AICE: From AI-CUDA-Engineer-
toolchain, checked against the PyTorch reference,            Archive (11,911 samples), converting CUDA-
and filtered by execution-based correctness valida-          centric Triton to AMD-validated implementations
tion. This yields 5,388 validated PyTorch-to-HIP             with TritonKernelGen.

                                                         5
  Together, this yields 62,153 validated HIP ker-            tionable kernel logic.
nel samples and 39,893 validated Triton–PyTorch                 Applying this pipeline yields 519 interface-
samples for AMD GPUs, plus 2,377 production-                 level entries from rocSOLVER, comprising 226
grounded ROCm Libraries QA entries. Additional               kernel-implementation-focused samples and 293
details on dataset construction, source-specific pro-        kernel-centric QA explanations. From rocBLAS,
cessing, metadata, and difficulty distributions are          we extract 1,858 entries, including 1,169 kernel-
provided in Appendix C and Appendix D.                       implementation samples and 689 QA-style explana-
                                                             tions. Together, these 2,377 production-grounded
3.4   Production-Grounded ROCm QA                            entries complement benchmark-derived HIP and
      Supervision                                            Triton datasets with real-world host–device orches-
To extend GPU kernel data construction beyond                tration and production HIP development patterns.
benchmark-style kernels, we extract HIP-kernel-
focused supervision from production-grade ROCm               3.5    Difficulty Distribution
libraries at the interface level. This subset is             We classify samples into three difficulty levels for
not treated as direct execution-verified kernel-pair         curriculum training: Level 1 covers standalone
data; instead, it provides production-grounded QA            single-function kernels, Level 2 covers fused opera-
supervision anchored to retrieved rocBLAS and                tors or single-file implementations, and Level 3 cov-
rocSOLVER code.                                              ers multi-file kernels with cross-module dependen-
                                                             cies. The full Triton corpus comprises 11,824 L1
Interface decomposition. For each target
                                                             (29.6%), 24,765 L2 (62.1%), and 3,304 L3 (8.3%)
project, we start from a user-facing interface and
                                                             samples; the curriculum-eligible subset used per
decompose it into a compact kernel-relevant scope.
                                                             Triton RL phase is reported in Appendix G. The
We traverse the call graph from the interface en-
                                                             ROCm Libraries QA data follows a similar distri-
trypoint to identify code regions directly involved
                                                             bution: rocSOLVER (190 L1, 198 L2, 131 L3) and
in GPU execution, including device-side kernels,
                                                             rocBLAS (971 L1, 506 L2, 381 L3).
host-side launch logic, parameter preparation, and
tightly coupled helper utilities. This interface-level       4     Training Compact AMD Kernel LLMs
view preserves the connection between public
APIs and the underlying HIP kernels, which is                AMDKernelVault is designed not only as a kernel
often lost when treating files or repositories as            corpus, but also as a training resource for compact
unstructured text.                                           AMD kernel LLMs. We use it to train Qwen3-
                                                             8B with a two-stage recipe: supervised fine-tuning
Scope control. Production libraries contain sub-
                                                             (SFT) for cold-start kernel generation, followed by
stantial infrastructure code unrelated to kernel be-
                                                             execution-aware reinforcement learning (RL) that
havior. To avoid recursion blow-up and irrelevant
                                                             uses compilation, correctness, and latency feed-
context, we use project-specific allowlists and dis-
                                                             back.
allowlists. The disallowlist filters logging, debug-
ging, testing, and auxiliary utilities, while the al-        4.1    Kernel Tasks and Metrics
lowlist constrains traversal to kernel-relevant sub-
                                                             Our datasets support four kernel-centric tasks:
systems. Because rocBLAS and rocSOLVER differ
                                                             PyTorch→HIP translates PyTorch modules into
in organization and dispatch structure, each project
                                                             semantically equivalent HIP implementations;
uses tailored traversal rules.
                                                             HIP→HIP optimizes existing HIP kernels;
Kernel-centric QA generation. Given the re-                  Text→Triton generates Triton kernels from natural-
trieved interface context, an agent constructs HIP-          language specifications; and Triton→Triton
kernel-focused QA pairs. The questions target con-           improves Triton kernels through tiling, memory-
crete implementation aspects, including computa-             access, and boundary-handling changes.
tion semantics, index-to-tensor mappings, mem-                  We evaluate kernels with three execution-based
ory access patterns, synchronization and reduction           metrics: compilation pass, successful build under
strategies, launch configuration, and correctness            the target toolchain; correctness pass, numerical
constraints. Answers are grounded in the retrieved           equivalence against the PyTorch reference; and
code context rather than generic library descrip-            speed, kernel-level speedup over the input kernel
tions, so the resulting supervision emphasizes ac-           or PyTorch baseline. Comp@k and Corr@k report

                                                         6
compilation and correctness after k agent iterations,        4.4    Agentic Integration
while Pass@k measures the probability of obtain-             A key goal is to test whether the corpus can train
ing at least one correct result from k samples. For          a compact local model for an agentic kernel opti-
PyTorch-to-Triton, speedup is measured against               mization loop. We train one Qwen3-8B policy to
the original PyTorch implementation; for Triton-             serve the generator, reflector, and optimizer roles.
to-Triton, it is measured against the input kernel.          During multi-turn Triton RL, the same model pro-
Speed@10 averages the speedups of the best ten               duces a candidate, interprets execution feedback,
correct samples.                                             and emits the next revision.
                                                                This training recipe is not presented as a new RL
4.2   Supervised Fine-Tuning                                 algorithm. Rather, it evaluates whether execution-
                                                             verified AMDKernelVault data can specialize a
Direct RL from a pretrained model is difficult in            compact policy for AMD kernel agents. Section 5
this domain because early rollouts often fail to com-        therefore reports controlled, metric-specific com-
pile or violate kernel interfaces, producing sparse          parisons under identical agent budgets.
feedback. We therefore first apply SFT to teach ker-
nel syntax, binding conventions, memory-access               4.5    Training Configuration
idioms, and common implementation patterns.                  We train Qwen3-8B with SFT followed by RL on
   For HIP, we use instruction–response pairs from           AMD MI-series GPUs. HIP training uses SFT fol-
the HIP portions of AMDKernelVault, where the                lowed by single-turn GRPO, while Triton training
input is a PyTorch task or source HIP kernel and the         uses SFT followed by multi-turn on-policy reflec-
output is a validated HIP implementation. For Tri-           tion RL with curriculum scheduling. We keep the
ton, we use reasoning-augmented examples when                main text focused on the training recipe used to
available, so that the model learns to plan tiling,          evaluate AMDKernelVault as a corpus for compact
masking, boundary checks, and memory layouts                 AMD kernel LLMs. Appendix E provides task
before emitting code. This stage provides the cold-          serialization, SFT and GRPO objectives, reward
start capability needed for subsequent execution-            implementation, curriculum schedule, hyperparam-
aware RL.                                                    eters, and additional analysis of reward sensitivity.

                                                             5     Experiments
4.3   Execution-Aware Reinforcement Learning
                                                             We evaluate whether AMDKernelVault can train
After SFT, we optimize the model using execution             compact AMD kernel LLMs that improve HIP and
feedback. HIP training uses single-turn GRPO,                Triton kernel generation under execution-based val-
where each candidate is compiled, tested, and                idation. We compare Qwen3-8B trained on our cor-
scored after one generation attempt. Triton training         pus against frontier LLMs (GPT-5, Gemini 2.5 Pro,
uses a multi-turn variant aligned with the GEAK-             Claude Sonnet 4). For HIP, we evaluate PyTorch-
style generate–evaluate–reflect loop: the model              to-HIP translation on 200 KernelBench Level-1/2
proposes a kernel, observes compiler or runtime              tasks (Ouyang et al., 2025) and HIP-to-HIP op-
feedback, reflects on the failure or performance             timization on 100 held-out samples. For Triton,
bottleneck, and generates an improved candidate.             we use TritonBench-G (184 kernels) and ROCm-
                                                             Bench (31 AMD-specific kernels) with the same
   The reward combines three signals: compila-
                                                             3-iteration OptimAgent-v2 protocol (Wang et al.,
tion, correctness, and speedup. Compilation credit
                                                             2025b). Each model serves as generator, reflector,
provides partial feedback for syntactically and
                                                             and optimizer under identical agent settings, and all
interface-compatible kernels, correctness rewards
                                                             reported Triton inference runs use MI355X GPUs.
functional equivalence, and a bounded speedup
term encourages performance improvements with-               Train/test separation and overlap controls.
out allowing timing outliers to dominate learning.           Evaluation cases are excluded from training by
This reward is designed for the low-success regime           source and task identifier. HIP evaluation uses
of AMD kernel generation, where binary correct-              200 held-out KernelBench-derived translation tasks
ness rewards alone provide too little gradient signal.       and 100 held-out HIP-to-HIP optimization tasks;
Full reward definitions and GRPO details are pro-            Triton evaluation uses the curated 184-kernel
vided in Appendix E.                                         TritonBench-G and 31-kernel ROCmBench sets.

                                                         7
These controls prevent exact task-identifier reuse.            Model                   Comp Acc       Corr Acc
However, because generated kernels can implement
                                                               Gemini 2.5 Pro             70.5%        18.5%
semantically similar operator patterns using dif-              Claude Sonnet 4            85.0%        22.0%
ferent code, exact-match filtering cannot exclude              GPT-5                      75.5%        24.0%
every functional near-duplicate. We did not con-
                                                               Q3-8B (base)               50.0%        14.5%
duct an exhaustive corpus-wide semantic-overlap                Q3-8B + SFT                78.0%        31.5%
search and therefore interpret the reported results            Q3-8B + SFT + RL           83.5%        34.0%
as benchmark-specific rather than as evidence of
overlap-free generalization.                                 Table 2: Pass@1 results of PyTorch-to-HIP translation
                                                             (200 tasks from KernelBench Levels 1 and 2). Q3-8B
Evaluation protocol and metrics. All Triton                  denotes Qwen3-8B.
model comparisons use the same OptimAgent-
v2      configuration:          num_offsprings=1,             Model              Comp Acc Corr Acc Speed@10
max_iteration=3,          identical      generator/re-        Gemini 2.5 Pro        81%        69%       1.15×
flector/optimizer role assignment, and no profiler            Claude Sonnet 4       93%        67%       1.11×
feedback. Thus, each row changes the model                    GPT-5                 89%        87%       1.32×
checkpoint while holding the external agent                   Q3-8B (base)          26%        18%       1.02×
                                                              Q3-8B + SFT           86%        70%       1.06×
scaffold and execution budget fixed. Comp@k                   Q3-8B + SFT + RL      90%        84%       1.14×
and Corr@k report the fractions of tasks that
compile and pass numerical validation by iteration           Table 3: Pass@1 results of HIP-to-HIP kernel optimiza-
k, respectively; Pass@k reports the probability of           tion (100 held-out modules). Q3-8B denotes Qwen3-8B
obtaining at least one correct result from k indepen-        and speed@10 denotes average speedup achieved over
dently sampled candidates. For PyTorch-to-kernel             baseline of best 10 correct samples.
generation, speedup is measured against the Py-
Torch reference; for kernel-to-kernel optimization,          and measurement use 25 ms and 100 ms time bud-
it is measured against the input kernel. Speed               gets, respectively, with per-kernel iteration counts
comparisons include only correctness-passing                 derived from a short timing estimate. We report
candidates.                                                  median GPU-event timing, flush L2 before each
Benchmark coverage. The evaluation covers                    measured call, synchronize after the measured loop,
attention and softmax variants, layer and RMS                and discard no timing observations.
normalization, GEMM-family operations, elemen-               5.1   HIP Kernel Results
twise transformations, reductions, fused blocks,
MoE-style routing, and online-softmax-style fused            Table 2 evaluates PyTorch-to-HIP translation. Fron-
reductions. KernelBench Level-1/2 tests emphasize            tier LLMs compile many candidates but achieve
operator implementation and composition, while               limited correctness; GPT-5 reaches 75.5% com-
TritonBench-G spans difficulty levels from stan-             pilation but only 24.0% correctness. Training on
dalone operators to harder fused kernels; ROCm-              AMDKernelVault substantially improves Qwen3-
Bench adds AMD-specific cases. This breadth tests            8B: SFT raises correctness to 31.5%, and RL fur-
multiple common deep-learning kernel patterns,               ther improves it to 34.0%, outperforming all fron-
but it is not a per-family performance study: the            tier baselines in correctness.
benchmark sizes are limited, and we do not report               Table 3 evaluates HIP-to-HIP optimization. The
operator-family-specific pass rates.                         trained model reaches 84% correctness, close to
                                                             GPT-5 (87%) and substantially above the base
Triton reproducibility setup. Triton workflows               model (18%), while maintaining positive speedup.
use Triton 3.3.0. Corpus validation and profiling            These results indicate that the HIP portion of AMD-
use MI325 and MI350 GPUs; Triton SFT and                     KernelVault supports both translation and optimiza-
RL use 32 MI325X GPUs; and reported Triton                   tion tasks.
inference uses MI355X GPUs. The corpus tar-
gets gfx942 for MI325X stages and gfx950 for                 5.2   Triton Kernel Results
MI350/MI355X stages. ROCm, PyTorch, and                      Table 4 reports TritonBench-G results under the
Python versions vary across data-production snap-            fixed 3-iteration GEAK OptimAgent-v2 evaluator.
shots and are not pinned to one release. Warm-up             The base Qwen3-8B model reaches 4.9% Corr@3,

                                                         8
while SFT improves to 10.3% and SFT+RL reaches                 Model             Corr@1 Corr@3 Comp@3 Speed
33.2%, compared with GPT-5 at 15.2% and Claude                 Gemini 2.5 Pro     12.90%   25.81%   41.94%   1.47×
Sonnet 4 at 29.8%. Since all rows use the same                 Claude Sonnet 4    19.35%   35.48%   67.74%   1.82×
                                                               GPT-5              16.13%   29.03%   35.48%   1.31×
scaffold and budget, this controlled comparison                Q3-8B (base)        3.22%    6.45%   19.35%   0.74×
demonstrates the corpus’s utility for specializing a           Q3-8B + SFT + RL 22.58% 41.94%       58.06%   1.61×
compact local model.
                                                              Table 5: ROCmBench (AMD) results under the fixed 3-
 Model              Corr@1 Corr@3 Comp@3 Speed                iteration GEAK OptimAgent-v2 evaluator. All rows use
 Gemini 2.5 Pro      8.7%    23.4%     32.6%   1.31×          the same agent budget, and Q3-8B denotes Qwen3-8B.
 Claude Sonnet 4     7.6%    29.8%     46.7%   1.34×
 GPT-5               3.8%    15.2%     28.8%   1.05×
 Q3-8B (base)        0.0%     4.9%     14.7%   0.97×          6   Conclusion
 Q3-8B + SFT         4.3%    10.3%     27.7%   1.19×
 Q3-8B + SFT + RL   12.0%    33.2%     67.9%   1.46×
                                                              AMDKernelVault is an open HIP and Triton ker-
Table 4: TritonBench-G results under the fixed 3-
                                                              nel resource for recent AMD CDNA GPUs, sup-
iteration GEAK OptimAgent-v2 evaluator. All models            ported by AMD-native generation and validation
use the same agent budget and role assignment; only the       infrastructure. As a utility demonstration, we spe-
LLM checkpoint changes. Corr/Comp denote correct-             cialize Qwen3-8B for a GEAK-style loop; under
ness/compile accuracy, and Q3-8B denotes Qwen3-8B.            fixed budgets, it achieves the highest correctness on
                                                              selected benchmarks but does not uniformly lead
   Table 5 shows results on ROCmBench. The                    compilation or speed. We release the corpus, docu-
trained Qwen3-8B model obtains the highest                    mentation, and code to support future AMD kernel
Corr@3 (41.94%), compared with Claude Sonnet                  research.
4 (35.48%) and GPT-5 (29.03%). Claude Sonnet
4 remains stronger on Comp@3 (67.74% versus                   Limitations
58.06%) and speed (1.82× versus 1.61×), so the
advantage is specific to correctness.                         Our evaluation is limited to AMD GPU environ-
                                                              ments and kernel-generation benchmarks available
Difficulty Analysis. Our model leads the com-                 to us. Expert-level kernels remain difficult across
pared frontier baselines on D1–D3 of TritonBench-             all tested models, and the reported performance de-
G, but Claude Sonnet 4 solves more D4 kernels                 pends on the specific ROCm, Triton, and hardware
(18/84 versus 13/84), and D5 remains unsolved                 configurations used during validation. Although
by all models. Full results are provided in Ap-               we include production-derived ROCm library su-
pendix K.                                                     pervision, some generated kernels may still inherit
Limitations and Failure Analysis. Despite                     suboptimal structures from upstream CUDA/Triton
strong results on D1–D3 tasks, expert-level ker-              sources or from LLM-generated candidates.
nels remain challenging. Common failure modes                    Several gaps remain for future work: broader
include incorrect tile/block size choices for unusual         corpus-level profiling of latency, memory footprint,
tensor shapes, synchronization errors in multi-stage          register pressure, and occupancy; per-operator-
reductions, and memory-coalescing failures under              family pass-rate analysis beyond the current dif-
AMD’s wavefront execution model. These failures               ficulty breakdown; larger held-out HIP evaluation
suggest that future work should incorporate richer            sets; and evaluation beyond deep-learning work-
profiler-guided feedback and broader expert-kernel            loads, including HPC, sparse/graph, and database
supervision.                                                  kernels. Future work should also incorporate richer
                                                              profiler-guided feedback and broader expert-kernel
5.3   Ablation Studies                                        supervision.
We conduct ablations to assess the importance of                 We do not report a corpus-wide semantic near-
data scale, SFT cold start, and multi-turn RL. Per-           duplicate audit or uniformly aggregated candidate-
formance improves with more training data, SFT                rejection rates because source pipelines use differ-
provides a critical initialization before RL, and             ent logging formats. Software environments also
multi-turn RL contributes +13.1% on Triton. De-               vary across data-production snapshots, although
tailed ablation tables and reward-sensitivity results         Triton is fixed to version 3.3.0 for the reported Tri-
are provided in Appendix J.                                   ton workflow.

                                                          9
Ethical Considerations and Impact                               heterogeneous computing. In IEEE International
Statement                                                       Symposium on Workload Characterization (IISWC),
                                                                pages 44–54.
This work focuses on GPU kernel generation and
                                                              Terry Chen, Zhifan Ye, Bing Xu, Zihao Ye, Timmy Liu,
optimization for AMD hardware. The released ar-                 Ali Hassani, Tianqi Chen, Andrew Kerr, Haicheng
tifacts consist of program code, generated kernels,             Wu, Yang Xu, Yu-Jung Chen, Hanfeng Chen, Aditya
execution metadata, and QA supervision grounded                 Kane, Ronny Krashinsky, Ming-Yu Liu, Vinod
in public ROCm library code. Provenance, us-                    Grover, Luis Ceze, Roger Bringmann, John Tran,
                                                                and 4 others. 2026. AVO: Agentic variation opera-
age conditions, and per-source license notes are
                                                                tors for autonomous evolutionary search. Preprint,
included with the public artifact.                              arXiv:2603.24517.
   The expected positive impact is improved effi-
ciency for AI workloads. Faster generated kernels             Tianqi Chen, Thierry Moreau, Ziheng Jiang, Lianmin
                                                                Zheng, Eddie Yan, Haichen Shen, Meghan Cowan,
can reduce training and inference runtime, while a              Leyuan Wang, Yuwei Hu, Luis Ceze, Carlos Guestrin,
compact local model can reduce repeated frontier-               and Arvind Krishnamurthy. 2018. TVM: An auto-
LLM calls during kernel search. These improve-                  mated end-to-end optimizing compiler for deep learn-
ments may lower computational cost and energy                   ing. In 13th USENIX Symposium on Operating Sys-
                                                                tems Design and Implementation (OSDI 18), pages
use for AMD GPU deployments.                                    578–594.
   As with other code-generation systems, gener-
ated code may be incorrect, inefficient, or unsafe            Wentao Chen, Jiace Zhu, Qi Fan, Yehan Ma, and
if deployed without validation. We mitigate this               An Zou. 2025. Cuda-llm: Llms can write efficient
                                                               cuda kernels. arXiv preprint arXiv:2506.09092.
risk by emphasizing execution-based compilation,
correctness testing, and latency profiling through-           Weinan Dai, Hanlin Wu, Qiying Yu, Huan-ang Gao,
out data construction and evaluation. The work is              Jiahao Li, Chengquan Jiang, Weiqiang Lou, Yufan
narrowly focused on performance engineering for                Song, Hongli Yu, Jiaze Chen, et al. 2026. Cuda agent:
                                                               Large-scale agentic rl for high-performance cuda ker-
GPU kernels, and generated kernels should be vali-             nel generation. arXiv preprint arXiv:2602.24286.
dated in the target environment before production
use.                                                          Tri Dao, Dan Fu, Stefano Ermon, Atri Rudra, and
                                                                 Christopher Ré. 2022. Flashattention: Fast and
                                                                 memory-efficient exact attention with io-awareness.
                                                                Advances in neural information processing systems,
References                                                       35:16344–16359.
Advanced Micro Devices, Inc. 2025a. HIP documen-
  tation (programming guide). https://rocm.docs.              Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song,
  amd.com/projects/HIP/en/latest/. Accessed                     Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu Zhang,
  2025-12-15.                                                   Shirong Ma, Xiao Bi, et al. 2025. Deepseek-r1: In-
                                                                centivizing reasoning capability in llms via reinforce-
Advanced Micro Devices, Inc. 2025b.  HIPIFY                     ment learning. arXiv preprint arXiv:2501.12948.
  documentation.  https://rocm.docs.amd.com/
  projects/HIPIFY/en/latest/. Accessed 2025-                  Ahmed Heakl, Gustavo Bertolo Stahl, Sarim Hashmi,
  12-15.                                                        Seung Hun Eddie Han, Mukul Ranjan, Arina Khar-
                                                                lamova, Salman Khan, and Abdulrahman Mahmoud.
Advanced Micro Devices, Inc. 2025c. ROCm documen-               2026. Cass: Nvidia to amd transpilation with data,
  tation. https://rocm.docs.amd.com/. Accessed                  models, and benchmark. In Proceedings of the 64th
  2025-12-15.                                                   Annual Meeting of the Association for Computational
                                                                Linguistics (Volume 1: Long Papers), pages 34489–
Sandhini Agarwal, Lama Ahmad, Jason Ai, Sam Alt-                34508.
  man, Andy Applebaum, Edwin Arbus, Rahul K
  Arora, Yu Bai, Bowen Baker, Haiming Bao, et al.             Jiacheng Huang, Zimin Li, Yinghui Li, and Haojie
  2025. gpt-oss-120b & gpt-oss-20b model card. arXiv             Wang. 2025. Ninetoothed: A triton-based high-
  preprint arXiv:2508.10925.                                     level domain-specific language for machine learning.
                                                                 Preprint, arXiv:2507.11978.
Carlo Baronio, Pietro Marsella, Ben Pan, Simon Guo,
  and Silas Alberti. 2026. Kevin: Multi-turn rl for           Robert Tjarko Lange, Aaditya Prasad, Qi Sun, Maxence
  generating cuda kernels. In International Conference          Faldor, Yujin Tang, and David Ha. 2025a. The AI
  on Learning Representations.                                  CUDA Engineer Archive: Agentic CUDA kernel dis-
                                                                covery, optimization and composition. Hugging Face
Shuai Che, Michael Boyer, Jiayuan Meng, David Tar-              dataset,    https://huggingface.co/datasets/
  jan, Jeremy W. Sheaffer, Sang-Ha Lee, and Kevin               SakanaAI/AI-CUDA-Engineer-Archive.             Ac-
  Skadron. 2009. Rodinia: A benchmark suite for                 cessed: 2026-08-30.


                                                         10
Robert Tjarko Lange, Qi Sun, Aaditya Prasad, Maxence             Philippe Tillet, H. T. Kung, and David Cox. 2019. Tri-
  Faldor, Yujin Tang, and David Ha. 2025b. Towards                  ton: An intermediate language and compiler for tiled
  robust agentic cuda kernel benchmarking, verifica-                neural network computations. In Proceedings of the
  tion, and optimization. Preprint, arXiv:2509.14279.               3rd ACM SIGPLAN International Workshop on Ma-
                                                                    chine Learning and Programming Languages (MAPL
Jianling Li, Shangzhan Li, Zhenye Gao, Qi Shi, Yuxuan              ’19), pages 10–19.
   Li, Zefan Wang, Jiacheng Huang, Haojie Wang, Jian-
   rong Wang, Xu Han, Zhiyuan Liu, and Maosong Sun.              Nicolas Vasilache, Oleksandr Zinenko, Theodoros
   2025a. Tritonbench: Benchmarking large language                 Theodoridis, Priya Goyal, Zachary DeVito,
   model capabilities for generating triton operators. In          William S. Moses, Sven Verdoolaege, Andrew
   Findings of the Association for Computational Lin-              Adams, and Albert Cohen. 2018. Tensor compre-
   guistics: ACL 2025, pages 23053–23066, Vienna,                  hensions: Framework-agnostic high-performance
   Austria. Association for Computational Linguistics.             machine learning abstractions. CoRR.

Shangzhan Li, Zefan Wang, Ye He, Yuxuan Li, Qi Shi,              Jianghui Wang, Vinay Joshi, Saptarshi Majumder,
  Jianling Li, Yonggang Hu, Wanxiang Che, Xu Han,                   Xu Chao, Bin Ding, Ziqiong Liu, Pratik Prabhan-
  Zhiyuan Liu, and Maosong Sun. 2025b. Autotriton:                  jan Brahma, Dong Li, Zicheng Liu, and Emad Bar-
  Automatic triton programming with reinforcement                   soum. 2025a. Geak: Introducing triton kernel ai
  learning in llms. arXiv preprint arXiv:2507.05687.                agent & evaluation benchmarks. arXiv preprint
                                                                    arXiv:2507.23194.
Anton Lozhkov, Raymond Li, Loubna Ben Allal, Fed-
  erico Cassano, Joel Lamy-Poirier, Nouamane Tazi,               Jianghui Wang, Saptarshi Majumder, Umang Pandey,
  Ao Tang, Dmytro Pykhtar, Jiawei Liu, Yuxiang Wei,                 Chao Xu, Bin Ding, Manoj Rao, Ziqiong Liu,
  et al. 2024. Starcoder 2 and the stack v2: The next               Pratik Prabhanjan Brahma, Dong Li, Zicheng Liu,
  generation. arXiv preprint arXiv:2402.19173.                      and Emad Barsoum. 2025b. GEAK-Triton v2 Family
                                                                    of AI Agents: Kernel Optimization for AMD Instinct
Anne Ouyang, Simon Guo, Simran Arora, Alex L                        GPUs. AMD ROCm Blogs. Accessed: 2026-01-27.
  Zhang, William Hu, Christopher Re, and Azalia
  Mirhoseini. 2025. KernelBench: Can LLMs write                  Jiin Woo, Shaowei Zhu, Allen Nie, Zhen Jia, Yida Wang,
  efficient GPU kernels? In Proceedings of the 42nd                 and Youngsuk Park. 2025. TritonRL: Training LLMs
  International Conference on Machine Learning, vol-                to think and code triton without cheating. Preprint,
  ume 267 of Proceedings of Machine Learning Re-                    arXiv:2510.17891.
  search, pages 47356–47415. PMLR.
                                                                 An Yang, Anfeng Li, Baosong Yang, Beichen Zhang,
Sahan Paliskara and Mark Saroufim. 2025. Kernelbook.               Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao,
                                                                   Chengen Huang, Chenxu Lv, et al. 2025. Qwen3
Qwen, An Yang, Baosong Yang, Beichen Zhang,                        technical report. arXiv preprint arXiv:2505.09388.
 Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan
                                                                 Lianmin Zheng et al. 2020. Ansor: Generating high-
 Li, Dayiheng Liu, Fei Huang, Haoran Wei, Huan
                                                                   performance tensor programs for deep learning. In
 Lin, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin
                                                                   14th USENIX Symposium on Operating Systems De-
 Yang, Jiaxi Yang, Jingren Zhou, Junyang Lin, and
                                                                   sign and Implementation (OSDI 20).
 24 others. 2025. Qwen2.5 technical report. Preprint,
 arXiv:2412.15115.

Jonathan Ragan-Kelley, Connelly Barnes, Andrew
  Adams, Sylvain Paris, Frédo Durand, and Saman
  Amarasinghe. 2013. Halide: A language and com-
  piler for optimizing parallelism, locality, and recom-
  putation in image processing pipelines. In Proceed-
  ings of the 34th ACM SIGPLAN Conference on Pro-
  gramming Language Design and Implementation
  (PLDI), pages 519–530.

Jay Shah, Ganesh Bikshandi, Ying Zhang, Vijay
  Thakkar, Pradeep Ramani, and Tri Dao. 2024.
  Flashattention-3: Fast and accurate attention with
  asynchrony and low-precision. Advances in Neural
  Information Processing Systems, 37:68658–68685.

Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,
  Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan
  Zhang, Y. K. Li, Y. Wu, and Daya Guo. 2024.
  Deepseekmath: Pushing the limits of mathemati-
  cal reasoning in open language models. Preprint,
  arXiv:2402.03300.


                                                            11
A    Artifact, License, and AI-Assistance                       B   More Related Work
     Statement
                                                                Production Library Code as Supervision.
Artifacts and licenses. The data and documenta-                 Benchmark-derived datasets provide diversity but
tion are available at https://huggingface.                      are typically limited to standalone kernels. In con-
co/datasets/amd/AIG-Datasets.                 The               trast, production library code from projects such as
associated training, RL, and HIP kernel-                        rocBLAS and rocSOLVER captures interface-level
generation code is available at https:                          implementations spanning multiple files and reflect-
//github.com/AMD-AGI/hip_kernel_llm_lab.                        ing production-grade engineering practices. These
The release includes corpus-audit, validation-                  libraries encode years of architecture-specific op-
protocol, and license/provenance documentation.                 timization and correctness engineering. AMD-
Upstream resources remain subject to their                      KernelVault incorporates this signal through an
source-specific terms: CUDA-Agent-Ops-6K and                    interface-aware extraction pipeline that produces
AI-CUDA-Engineer-Archive are released under                     kernel-centric supervision grounded in real HIP
CC-BY-4.0; the current GPUMODE/KernelBook                       code.
release uses the June 9 Researcher Reciprocity Li-              Positioning Relative to Multi-Turn RL Ker-
cense; TritonBench-8k uses Apache-2.0; and Stack                nel Agents. Prior multi-turn systems, including
v2 retains the BigCode and original-repository                  Kevin (Baronio et al., 2026), demonstrate that iter-
terms. ROCm Libraries are licensed per compo-                   ative execution feedback can improve kernel gen-
nent; the source components used here include                   eration. We do not claim that multi-turn feedback
rocBLAS under the MIT License and rocSOLVER                     alone is new. Our setting differs in two ways. First,
under the BSD-2-Clause License. The ROCm                        AMD HIP/Triton generation starts from a lower-
Libraries QA subset contains interface-level                    success regime, where early compilation and cor-
supervision and provenance references rather                    rectness rewards are sparse. Second, our goal is
than a redistribution of the complete source trees.             to train a model that can be deployed inside an
Exact source revisions and applicable terms are                 agent-training framework, rather than only evalu-
documented in the released provenance metadata.                 ate an external LLM called by an agent wrapper.
                                                                In GEAK-style workflows, repeated LLM calls
Data content and filtering. The released data                   normally handle generation, reflection, and opti-
consists of program code, kernel implementations,               mization. We instead train one compact policy on
task metadata, execution logs, and interface-level              execution-feedback trajectories so that the same
QA supervision grounded in public ROCm library                  model can serve these roles locally under ROCm.
code. It is not intended to contain personally iden-
tifying information or offensive content, and the               On Comparing to Kevin and Devin-Class
data construction pipeline filters generated artifacts          Agents. Kevin is trained to emit raw CUDA
for executability, determinism, and task validity.              via torch.utils.cpp_extension.load_inline
Generated kernels are filtered through compilation,             on NVIDIA hardware, using CUDA-specific
execution-based correctness checks, and ROCm                    primitives such as __shfl_xor_sync and
validation; QA entries are grounded in retrieved                __shared__ memory. Our evaluation targets
public code contexts rather than user data.                     AMD GPUs through HIP/ROCm and TritonBench-
                                                                G/ROCmBench under ROCm. A same-protocol
AI assistance. We used AI assistants during this                comparison would require Kevin to emit AMD-
project for two purposes. First, frontier LLMs                  compatible Triton or HIP kernels, which it was not
such as GPT-5 were used inside HIPKernelGen/Tri-                trained for. We therefore treat Kevin as evidence
tonKernelGen to generate candidate GPU kernels                  that RL on execution feedback is effective in
and reflection feedback, which were then com-                   CUDA settings, while focusing our empirical
piled, tested, profiled, and filtered by the authors’           comparison on models evaluated under the same
execution-based pipeline. Second, general AI writ-              GEAK OptimAgent-v2 protocol. Devin is a hosted
ing assistants were used to help polish wording                 coding agent without a benchmark-accessible
and organize the manuscript. All experimental de-               interface exposing the fixed generator/reflector/op-
sign, dataset filtering, validation, analysis, and final        timizer role assignment used here, so we do not
claims were checked and approved by the authors.                include it as a direct baseline.

                                                           12
                                                             Multi-turn        Performance            Role
System             Target              Training
                                                             feedback          signal                 internalization
Kevin              CUDA /              Multi-turn RL         Yes             Correctness + speedup Kernel refinement, not
                   KernelBench                                                                     AMD/GEAK roles
AutoTriton         Triton              SFT +                 No explicit     Rule + execution      No generator/reflec-
                                       GRPO/RLVR             multi-role loop rewards               tor/optimizer loop
GEAK               AMD Triton          No model training     Inference-time Correctness + latency Separate frontier-LLM
                                                             only                                  calls
AMDKernelVault AMD HIP/Triton SFT +                          Yes             Compile +             One 8B policy for all
                              execution-aware                                correctness + speedup LLM roles
                              RL
References: Kevin (Baronio et al., 2026); AutoTriton (Li et al., 2025b); GEAK (Wang et al., 2025a).

                      Table 6: Positioning relative to closely related kernel-generation systems.


C     Dataset Details                                                    execution-based correctness validation, and
                                                                         latency measurements.
C.1     HIP Kernel Datasets
C.1.1     HIP-CudaAgent Dataset                                     3. Iterative Refinement. Failed kernels trig-
                                                                       ger reflector-guided feedback for iterative re-
The HIP-CudaAgent Dataset is derived from
                                                                       generation until valid or maximum attempts
CUDA-Agent-Ops-6K using the HIPKernelGen
                                                                       reached.
pipeline:
   1. PyTorch Task Normalization. The synthe-                      Final: 5,910 unique PyTorch modules with
sized operator-level PyTorch tasks are converted                 22,397 HIP kernel optimization variants (avg 3.8
into function-style references with input construc-              variants/entry).
tion and correctness-checking logic.
   2. HIP Kernel Generation. An LLM-based                          C.1.3    HIP-to-HIP Optimization Pairs
generator produces HIP implementations for each                  We extend HIPKernelGen to support kernel-level
normalized PyTorch task. Each candidate is com-                  HIP-to-HIP optimization by operating directly
piled with the ROCm toolchain and validated                      on existing HIP kernel functions annotated with
against the PyTorch reference through execution-                 __global__ or __device__. The input is a base-
based tests.                                                     line HIP kernel and the output is an optimized
   3. Iterative Refinement. Compilation errors,                  kernel with equivalent semantics. Final: 34,368
runtime failures, and numerical mismatches trigger               validated HIP kernel optimization pairs.
reflector-guided regeneration until correctness is
achieved or the maximum attempt limit is reached.                  C.2     Triton Kernel Dataset
   Final: 5,388 validated PyTorch-to-HIP samples.                We construct a large-scale Triton kernel dataset us-
                                                                 ing TritonKernelGen, aggregating multiple comple-
C.1.2     HIP-GPUMode Dataset                                    mentary sources under a unified validation pipeline.
The HIP-GPUMode Dataset is generated from the
GPUMODE-KernelBook dataset using the HIPKer-                       C.2.1    Stack-v2-dedup (curated)
nelGen pipeline:                                                 We filter and extract PyTorch code containing
                                                                 torch operators and/or Torch Inductor constructs,
    1. PyTorch Module to Function Conver-                        wrap entries into function-style references, and
       sion. The first-stage agent converts PyTorch              validate against a high-coverage test suite. From
       module-level code into function-style PyTorch             ∼13,000 candidates, we obtain 2,269 medium-
       code with correctness-checking logic to filter            difficulty, functionally correct Triton–PyTorch
       functionally equivalent pairs.                            pairs.

    2. HIP Kernel Generation.         The second-                  C.2.2    TritonBench-train (modified)
       stage agent translates each PyTorch module                We curate 7,713 samples from the original
       into HIP code using an LLM-based genera-                  TritonBench-8k. Synthetic kernels generated via
       tor. Each candidate undergoes compilation,                the ninetoothed DSL are refined or discarded to

                                                            13
remove DSL-specific artifacts and input-specific             D     Dataset Analysis
patterns. We expand test coverage to ensure gen-
eralization across shapes, strides, and precision            This section analyzes the resulting datasets in
types.                                                       terms of scale, operator coverage, diversity, and
                                                             architecture-relevant properties.
C.2.3 GPUMODE-KernelBook
We incorporate ∼18,000 PyTorch entries with Tri-
ton code extracted via Torch Inductor, using them            D.1    Dataset Summary
as a primary source for operator coverage and struc-
                                                             Table 1 summarizes the scale and composition
tural guidance.
                                                             of AMDKernelVault. The corpus contains 64K+
C.2.4 AI-CUDA-Engineer-Archive                               HIP/ROCm supervision entries and approximately
We leverage 11,911 usable PyTorch + CUDA pairs.              40K Triton kernels, spanning PyTorch-to-kernel
Where Triton code is absent, the agent synthesizes           generation, kernel-to-kernel optimization, and
Triton implementations against the shared PyTorch            production-grounded code understanding. The
reference and expanded test suite.                           HIP/ROCm portion combines HIP-CudaAgent and
                                                             HIP-GPUMode for PyTorch-to-HIP generation,
Summary. Across sources, TritonKernelGen ag-                 HIP2HIP for optimizing existing HIP kernels, and
gregates 39,893 validated samples. Available meta-           ROCm Libraries QA for interface-grounded super-
data varies by source subset and packaged represen-          vision from rocBLAS and rocSOLVER.
tation; where present, it records construction-time             The Triton portion aggregates four comple-
validation outcomes, latency, and precision/shape            mentary sources into the Triton-Curated corpus:
coverage.                                                    curated web/code examples from Triton-Stack,
C.3   ROCm Libraries QA Dataset                              benchmark-derived kernels from Triton-Bench,
                                                             Torch-Inductor-derived programs from Triton-
Interface-level extraction from AMD ROCm Li-
                                                             GPUMode, and AI-CUDA-Engineer-derived tasks
braries using depth-first call graph traversal:
                                                             from Triton-AICE. Together, these subsets provide
• rocSOLVER: 519 entries (226 kernel implemen-               broad AMD-validated coverage across generated
  tations, 293 QA explanations). Difficulty: 190             operator workloads, benchmark-style kernels, and
  L1, 198 L2, 131 L3.                                        production-grounded HIP/Triton programming pat-
                                                             terns.
• rocBLAS: 1,858 entries (1,169 implementations,
  689 QA explanations). Difficulty: 971 L1, 506
                                                             D.2    Operator and Workload Coverage
  L2, 381 L3.
                                                             Across both HIP and Triton datasets, kernels span
  Total: 2,377 production-grounded supervision
                                                             common deep learning operator families, including
entries capturing production HIP development
                                                             elementwise transforms, reductions, normalization
patterns, interface-driven kernel logic, and host–
                                                             layers (e.g., layer normalization), matrix and ten-
device orchestration.
                                                             sor transformations, and composite fusion patterns
C.4   Difficulty Distribution                                produced by Torch Inductor.
Table 7 shows the full difficulty statistics used to            Because workloads are derived from real Py-
support the curriculum discussion in Section 3.              Torch programs and benchmark suites, kernels re-
Level 1 contains standalone kernels with relatively          flect practical memory access patterns, shape vari-
direct data flow, Level 2 covers fused or single-file        ability, and fusion structures encountered in train-
implementations requiring coordinated memory ac-             ing and inference workloads, rather than synthetic
cess, and Level 3 includes multi-file or interface-          microkernels.
level code with cross-module dependencies. The                  The ROCm Libraries QA dataset extends cover-
Triton corpus is dominated by Level 2 examples,              age to production-grade linear algebra primitives
while the ROCm Libraries QA subset contains a                from rocBLAS (e.g., GEMM, TRSM, SYMM)
larger fraction of Level 3 entries because produc-           and rocSOLVER (e.g., QR factorization, eigen-
tion interfaces often involve host-side orchestration        solvers), providing supervision grounded in multi-
and multi-file kernel dispatch.                              file, interface-driven kernel implementations.

                                                        14
                      Level                                Triton    rocBLAS     rocSOLVER
                      Level 1 (Standalone)          11,824 (29.6%)        971            190
                      Level 2 (Fused/single-file)   24,765 (62.1%)        506            198
                      Level 3 (Multi-file)            3,304 (8.3%)        381            131

                                  Table 7: Difficulty distribution across datasets.


D.3   Kernel Diversity and Optimization                       rocBLAS and rocSOLVER, anchoring the dataset
      Variants                                                in production AMD code. Fourth, Triton sam-
                                                              ples are refactored and tested for shape generality,
The datasets exhibit substantial diversity in valid
                                                              stride awareness, and AMD-compatible schedul-
kernel implementations for the same functional
                                                              ing assumptions. These checks reduce reliance on
operators. In HIP-GPUMode, multiple HIP kernels
                                                              NVIDIA-specific warp-size, tensor-core, and tiling
are provided per PyTorch entry, differing in block
                                                              assumptions while still preserving useful algorith-
sizes, thread mapping strategies, tiling schemes,
                                                              mic structure from upstream corpora.
memory access orderings, and reduction structures.
   Similarly, Triton-Curated contains multiple ker-           D.5    Portability and Correctness Outcomes
nel realizations for overlapping operators, captur-
ing variation in program structure, scheduling deci-          All released HIP kernels compile and pass
sions, and memory layouts at the DSL level. This              execution-based correctness checks on AMD
diversity exposes non-trivial performance trade-              ROCm after filtering. Triton-Curated kernels like-
offs and supports studies in kernel ranking, selec-           wise compile and pass correctness validation on
tion, and agent-driven optimization.                          AMD GPUs under expanded test suites covering
   Such multiplicity of correct implementations is            diverse shapes, strides, and precision modes.
essential for learning-based systems that aim to                 Because upstream corpora differ substantially
reason over optimization spaces rather than merely            in portability, Portability filtering removes kernels
reproducing reference kernels.                                that rely on non-general indexing, device-specific
                                                              assumptions, or input-specialized schedules. As a
D.4   Data Quality and Bias Mitigation                        result, the released datasets represent AMD-valid
                                                              kernel implementations rather than raw collections
Because a large fraction of the corpus is produced
                                                              from heterogeneous sources.
by automated agents, we explicitly filter for execu-
tion quality rather than trusting raw model outputs.          D.6    Validation Metadata
Candidates must compile, pass reference-based
tests, and satisfy ROCm execution constraints be-             Validation metadata is subset-dependent. Where
fore entering the released set. For performance-              available, packaged records include source iden-
oriented subsets, multiple candidates are generated           tifiers, task or reference information, dtype/shape
and the retained variants are selected after latency          coverage, compiler or runtime status, latency, and
measurement on AMD hardware. Public expert-                   speedup relative to the relevant baseline. Some
level HIP kernels are scarce, so the corpus com-              packaged verification fields are empty even
bines production kernels from ROCm Libraries                  when construction-time validation was performed,
with rigorously filtered generated variants. This de-         and rejected-candidate logs were not retained uni-
sign removes obviously poor kernels while preserv-            formly across pipelines. For ROCm Libraries QA,
ing multiple correct implementations when they                available provenance can include source paths and
expose different optimization strategies.                     interface-level context. We therefore do not claim
   We also mitigate NVIDIA-centric bias in four               that every released record contains all fields needed
ways. First, CUDA-derived samples are treated as              to reconstruct the complete validation trajectory.
seeds, not final AMD supervision: they are trans-
                                                              D.7 Architecture-Relevant Properties (Triton)
lated, compiled, and filtered under ROCm. Sec-
ond, generated HIP variants are re-optimized and              To assess whether Triton-Curated reduces common
measured on AMD hardware rather than accepted                 vendor-shaped artifacts present in upstream cor-
solely for syntactic portability. Third, ROCm Li-             pora, we analyze kernel parameterization and code-
braries provide expert-written HIP examples from              shape properties that often encode device-specific

                                                         15
assumptions, such as distributions of num_warps,            E.1     Task Serialization and SFT Objective
num_stages, and block-size choices.                         Each training instance is serialized as an
   Compared to raw crawled or DSL-generated                 instruction–response pair. The instruction contains
Triton code, Triton-Curated exhibits greater di-            the task specification, such as PyTorch reference
versity in scheduling parameters and fewer hard-            code, a natural-language Triton prompt, or an in-
coded constants tied to specific hardware config-           put HIP/Triton kernel. The response contains the
urations. This reflects both execution-based filter-        target kernel implementation, optionally preceded
ing on AMD and agent-driven refactoring toward              by reasoning annotations for Triton examples.
stride-aware and shape-general indexing, which are             SFT optimizes the standard next-token likeli-
required for correctness across ROCm backends.              hood:
During generation and validation, prompts and
feedback expose AMD-specific constraints such                       LSFT (θ) = −E(x,y∗ ) [log πθ (y ∗ | x)] ,   (1)
as wavefront behavior, LDS capacity, compute-
unit occupancy, and target architectures including          where x is the task specification and y ∗ is the target
gfx942 and gfx950.                                          implementation.
                                                               For HIP, training examples use direct instruction–
D.8    Comparison with Existing GPU Kernel
                                                            response formatting without additional reasoning
       Datasets
                                                            augmentation. For Triton, when available, we in-
Existing kernel datasets and benchmarks primar-             clude Chain-of-Thought-style planning before the
ily target CUDA or Nvidia-backed Triton execu-              final kernel:
tion, limiting their applicability to ROCm-based
platforms. In contrast, HIP-CudaAgent and HIP-                            y ∗ = [reasoning, kernel].
GPUMode provide native HIP kernels that exe-
cute on AMD GPUs, while Triton-Curated supplies             This helps the model learn tiling choices, mask-
an AMD-validated Triton corpus aligned with the             ing logic, memory-access patterns, and boundary
same PyTorch references.                                    handling. All SFT runs use full-parameter fine-
   This enables systematic research on AMD-                 tuning rather than PEFT/LoRA; in preliminary ex-
focused kernel optimization, cross-platform tran-           periments, parameter-efficient adapters underper-
spilation, and heterogeneous GPU performance                formed for this setting because the model has to
modeling that is difficult to conduct using Nvidia-         learn both low-level kernel syntax and agentic self-
centric benchmarks alone.                                   reflection behavior, and the coupled generation
                                                            and debugging skills required broader updates than
D.9    Implications for Learning-Based Kernel               adapter-only training provided.
       Research
By combining real-world workload coverage, ver-             E.2     Reward Design
ified executability on AMD GPUs, and diverse                Execution-aware RL uses a hierarchical reward:
optimization variants across both HIP and Triton
representations, the released datasets support su-                      r = rcompile + rcorrect + rperf ,       (2)
pervised fine-tuning, reinforcement learning, and
agent-based kernel synthesis under realistic hard-          where
ware constraints.
   These properties enable research on                        rcompile = 0.4,     rcorrect = 1.0,    rperf ≤ 1.5.
performance-aware kernel generation, auto-
                                                            The compilation reward is assigned when the can-
matic optimization strategies, and cross-abstraction
                                                            didate builds successfully under the target back-
learning, substantially lowering the barrier to
                                                            end. The correctness reward is assigned when the
data-driven GPU systems research on AMD
                                                            candidate passes numerical validation against the
platforms.
                                                            PyTorch reference. The performance reward is de-
E     More Details of Compact LLM                           fined as
      Training
                                                                    rperf = min 0.375 · (log2 s)2 , 1.5 ,
                                                                                                       
                                                                                                                (3)
This appendix provides implementation details for
the training recipe summarized in Section 4.                for speedup s ≥ 1.

                                                       16
   This design gives partial credit to near-valid ker-        E.5    Curriculum and Hyperparameters
nels that compile but fail correctness, which is im-          HIP training uses SFT followed by single-turn
portant in the low-success regime of kernel RL.               GRPO. Triton training uses SFT followed by multi-
The bounded performance term rewards meaning-                 turn GRPO with on-policy reflection and curricu-
ful speedups while reducing sensitivity to noisy              lum scheduling. The Triton curriculum gradually
latency measurements, JIT effects, or autotuning              shifts from easier kernels to harder samples, reduc-
outliers. Typical fast-converging speedups during             ing the fraction of Level-1 examples while increas-
RL sit well below the 1.5 cap, so this cap func-              ing Level-2 and Level-3 tasks.
tions as a conservative stability guard rather than a            We train Qwen3-8B-Instruct with the following
tuned hyperparameter; the reward-sensitivity analy-           configuration:
sis (Appendix J, Table 13) confirms low sensitivity
to the exact cap value.                                       • HIP SFT: 8×MI250, 4 epochs.
                                                              • HIP RL: 8×MI325X, 2 epochs, batch size 12, 6
E.3   GRPO Optimization                                         rollouts.
We use Group Relative Policy Optimization                     • Triton SFT: 32×MI325X, 2 epochs.
(GRPO) for execution-aware RL (Shao et al., 2024).
Standard GRPO normalizes advantages by reward                 • Triton RL: multi-turn GRPO, 2.7 epochs, 3 turns.
variance:                                                     E.6    Reward Sensitivity and Design Rationale
                       ri − r̄
                 Âi =         .                     Binary correctness rewards are insufficient in early
                       σr + ϵ
                                                     AMD kernel RL because most candidates fail to
In our setting, many early groups contain uniformly  compile or fail numerical validation. Under such
failed samples or samples with very similar partial  sparse feedback, many GRPO groups produce zero
rewards. We therefore disable variance normaliza- or near-zero useful advantage. The compile reward
tion and use:                                        increases the fraction of samples with usable sig-
                   Âi = ri − r̄.                (4) nal, while disabled variance normalization prevents
                                                     small reward differences from being amplified or
   The policy update follows PPO-style clipping:     collapsed by unstable group statistics.
                                                        Ablations in Appendix J and Table 13 evalu-
              h                            i       ate these choices. Removing multi-turn reflection,
L(θ) = −E min ρt Ât , clip(ρt , 1 ± ϵ)Ât +βDKL .removing SFT cold start, or weakening the hier-
                                                 (5) archical reward reduces performance, confirming
                                                     that execution-aware training is important for turn-
E.4 Multi-Turn On-Policy Reflection                  ing AMDKernelVault into an effective training re-
For Triton, each rollout follows a multi-turn        source for compact AMD kernel LLMs.
generate–evaluate–reflect process. At turn t, the
                                                              F     Evaluation Details
policy observes the task prompt, previous candi-
date code, compiler output, correctness failures,             Benchmark scope. Our execution-intensive eval-
and optional latency feedback. It then emits both             uation uses 200 PyTorch-to-HIP tasks, 100 HIP-
a reflection and a revised kernel. The multi-turn             to-HIP optimization tasks, 184 TritonBench-G ker-
return is:                                                    nels, and 31 ROCmBench kernels. These sets re-
                        XT                                    quire compilation and on-device validation and are
               G(τ ) =      γ t−1 rt ,         (6)            suitable for controlled comparisons, but they do not
                         t=1                                  establish performance over every AMD operator or
                                                              workload family.
with γ = 0.6 and T = 3.
   Because the same policy produces both reflec-              Agent-budget sensitivity. Our main results use
tion and code, the model learns feedback interpre-            a fixed 3-iteration budget. On TritonBench-G, Q3-
tations that are actionable for its own generation            8B+SFT+RL improves from 12.0% Corr@1 to
behavior. This aligns training with deployment in             33.2% Corr@3, compared with 7.6% to 29.8% for
GEAK-style agent loops, where the trained model               Claude Sonnet 4 and 3.8% to 15.2% for GPT-5. On
serves as generator, reflector, and optimizer.                ROCmBench, it improves from 22.58% to 41.94%,

                                                         17
compared with Claude Sonnet 4 from 19.35% to                num_offsprings=1, max_iteration=3, and no
35.48%.                                                     profiler feedback.

G     Training Details                                      G.3     Curriculum Learning Phases (Triton)
                                                            For Triton RL training, we employ difficulty fading
G.1     Hyperparameters                                     across three phases:

 Parameter                  HIP           Triton                     Phase   Composition                Samples
 Model                                                                 1     L1 only (Easy)                5.3K
 Base model                  Qwen3-8B-Instruct                         2     L1subset + L2 + L3med        16.5K
 Sequence length            8K              16K                        3     L2subset + L3 + variants        4K
 SFT
 Hardware             8×MI250          32×MI325X                Table 9: Curriculum phases for Triton RL training.
 Learning rate        2 × 10−5          1 × 10−5
 Batch size            8/GPU             8/GPU                 Unlike cumulative curricula that add harder sam-
 Epochs                   4                 2
 Framework          LLaMA-Factory     LLaMA-Factory         ples while keeping all easy samples, difficulty fad-
 RL: GRPO / Multi-Turn GRPO
                                                            ing progressively reduces easy samples to focus
 Hardware            8×MI325X           32×MI325X           training on harder cases. This approach prevents
 Learning rate        1 × 10−6            1 × 10−6          the model from overfitting to easy examples while
 Batch size              12              64 prompts
 Group size G             6                    8
                                                            ensuring sufficient exposure to challenging multi-
 Clip ϵ                  0.2              0.2 / 0.28        file and fused kernel implementations.
 KL coefficient β       0.01                 0.01
 Framework              VeRL               SLIME            H      Training Dynamics
 Epochs                   2                  2.7
 Multi-Turn (Triton only)                                   Figure 2 presents the training dynamics for our
 Turns T                     –               3              multi-turn on-policy reflection RL on Triton ker-
 Discount γ                  –              0.6
                                                            nel generation. The reward trajectory (a) shows
 Reward
 Compile partial             –              0.4
                                                            steady improvement from the SFT baseline (∼0.19)
 Correct                     –              1.0             to peak values above 1.0, demonstrating effective
 Performance cap             –              1.5             learning from execution feedback. The benchmark
                                                            evaluation (b) tracks performance on TritonBench-
    Table 8: Complete hyperparameter configuration.         G (compilation and correctness accuracy) and
                                                            ROCmBench throughout training, showing con-
                                                            sistent gains across both benchmarks.
G.2     Implementation Components
Our implementation separates training, execu-               I     Additional Experimental Analysis
tion feedback, and benchmark scoring into mod-              Cost and deployability. A practical advantage of
ular components. The multi-turn RL trainer fol-             training one compact policy is that the GEAK-style
lows a SLIME-style rollout loop: prompts are                loop can run locally on AMD GPUs. Frontier-
sampled from the kernel task dataset, the pol-              LLM-based pipelines require repeated external
icy generates candidate code and reflections for            calls for generation, reflection, and optimization,
up to T = 3 turns, and GRPO updates the                     introducing API cost, latency variance, and deploy-
same policy using the hierarchical rewards de-              ment constraints. In contrast, our trained Qwen3-
scribed in Section 4. Reward-standard-deviation             8B model runs within the local AMD environment
normalization is disabled to preserve stable ad-            and serves all three roles in the agent loop.
vantages in the sparse-reward regime. A sepa-
rate execution server compiles candidates, runs             Cross-hardware transfer. To test whether
correctness tests, and measures latency, return-            learned optimizations overfit to one AMD target,
ing compiler/runtime traces and performance feed-           we evaluate HIP kernels optimized on MI325 GPUs
back to the rollout loop. Final benchmark scor-             on MI250 GPUs. The optimized kernels retain sub-
ing uses TritonBench-G and ROCmBench, while                 stantial gains, reaching Speed@10 of 1.68× on
the headline Triton results use the fixed agent-            MI250. Triton evaluations on MI325 and MI350
training evaluator (GEAK OptimAgent-v2) with                show similar qualitative trends, suggesting that the

                                                       18
                                    (a) Training Reward                                      45
                                                                                                             (b) Evaluation During Training
                                                                                                      TritonBench-G Call (n=120)
                    1.2                                                                      40       TritonBench-G Exec (n=120)
                                                                                                      TritonBench-G Pass@2

                                                                                             35       ROCmBench(AMD) (n=20)
                    1.0
                                                                                             30




                                                                              Accuracy (%)
                    0.8
                                                                                             25
           Reward


                    0.6                                                                      20
                                                                                             15
                    0.4
                                                                                             10
                    0.2
                                                          Training Reward                     5
                                                          SFT Baseline
                    0.00   100    200    300      400    500    600     700                   00      100       200       300      400     500   600   700
                                         Training Step                                                                     Training Step

Figure 2: RL training results for Triton kernel generation. (a) Reward trajectory showing improvement from SFT
baseline (∼0.19) to peak values above 1.0. (b) Benchmark evaluation during training.


model learns transferable optimization principles                                     (50.0%/14.5%). Performance scales consistently,
such as locality, tiling, and parallel reduction pat-                                 confirming our dataset provides high-quality, di-
terns while still benefiting from ROCm-specific                                       verse supervision.
validation.
                                                                                      J.2            Triton RL Components
Additional failure modes. Beyond D5 expert-                                           Table 11 presents ablations on the Triton training
level failures, we observe three common categories                                    framework, evaluated using the agent-training eval-
of errors: shape-specialized indexing that fails                                      uator (GEAK OptimAgent-v2) with 3 iterations on
on broader test cases, numerically unstable reduc-                                    TritonBench-G (184 kernels).
tions, and inefficient memory layouts inherited
from CUDA/NVIDIA-centric assumptions. These                                                              Configuration                     Corr Acc          ∆
findings motivate future extensions with profiler-                                                       Full system                         33.2%           –
guided training feedback and additional production
                                                                                                         Single-turn (T = 1)                 20.1%      -13.1
AMD kernels.                                                                                             No SFT cold start                    8.5%      -24.7

J     Ablation Studies                                                                             Table 11: Ablation studies on Triton generation.
We conduct comprehensive ablation studies to vali-
date our design choices across both HIP and Triton                                                Key findings:
training pipelines.                                                                   • Multi-turn is essential (+13.1%): Single-turn
                                                                                        generation cannot recover from initial failures,
J.1    Data Scale (HIP)
                                                                                        while 3-turn reflection enables progressive refine-
Table 10 evaluates the impact of training data scale                                    ment. The model learns to identify errors from
on PyTorch-to-HIP translation (200 tasks from Ker-                                      execution feedback and generate targeted fixes.
nelBench Levels 1 and 2).
                                                                                      • SFT cold start is critical (+24.7%): Without
          Data Rate          Comp Acc          Corr Acc                                 SFT initialization, the base model’s low initial
          0% (base)              50.0%           14.5%
                                                                                        success rate (∼15%) produces extremely sparse
            10%                  62.5%           17.5%                                  RL gradients. SFT raises this to ∼51%, enabling
            30%                  64.5%           18.0%                                  effective RL optimization.
            50%                  69.5%           23.0%
           100%                  83.5%           34.0%
                                                                                      J.3            Fixed Agent Scaffold Ablation
Table 10: Impact of training data scale on PyTorch-to-                                Table 12 isolates the effect of the model train-
HIP translation.                                                                      ing stage under a fixed agent-training evaluator.
                                                                                      All rows use the same GEAK OptimAgent-v2
  With only 10% of training data, the model                                           loop on TritonBench-G with num_offsprings=1,
achieves 62.5% compilation and 17.5% cor-                                             max_iteration=3, no profiler feedback, and iden-
rectness—already surpassing the base model                                            tical generator/reflector/optimizer role assignment;

                                                                            19
only the model checkpoint changes. The large                    each training stage:
gain from base Q3-8B to Q3-8B+SFT+Agentic
                                                                • Base → SFT: +5.4% (2.1×) — learns kernel
RL shows that the external agent scaffold alone is
                                                                  syntax and patterns
insufficient: the policy must be trained on agent
feedback trajectories to use compiler, correctness,             • SFT → RL: +22.9% (3.2×) — learns from exe-
and performance feedback effectively.                             cution feedback

                                                                L     Theoretical Analysis
Model inside agent     Training signal          Corr@3
evaluator                                                       L.1     Zero-Advantage Collapse in GRPO
Q3-8B (base)           None / role-agnostic      4.9%           Standard GRPO uses binary rewards (correct/in-
                       base model
Q3-8B + SFT            Supervised kernel data   10.3%           correct) with group-normalized advantages. We
Q3-8B + SFT +          Multi-turn               33.2%           first prove why this leads to frequent zero-gradient
Agentic RL             compiler/test/perf                       updates, then explain how our design avoids this
                       feedback
                                                                failure mode.
Table 12: Effect of agentic training under a fixed agent        L.1.1 Binary Reward Collapse (Motivation)
scaffold. All rows use the same GEAK OptimAgent-v2
                                                                Theorem 1 (Binary Reward Collapse). In stan-
loop; only the model checkpoint changes.
                                                                dard GRPO with group size G and binary rewards
                                                                r ∈ {0, 1}, let pe denote the probability that a
J.4   Reward Sensitivity                                        single sample succeeds (receives reward 1). The
                                                                probability that all samples in a group receive iden-
We further analyze the components of the hierar-
                                                                tical rewards, yielding zero advantages, is:
chical reward used during Triton RL. The domi-
nant sensitivity is not the absolute reward scale but                     P (Âi = 0, ∀i) = pG
                                                                                             e + (1 − pe )
                                                                                                          G
                                                                                                                     (7)
whether the reward creates usable gradient signal
in the low-success regime.                                      Proof. In standard GRPO, the advantage for sam-
   These observations motivate the chosen re-                   ple i is:
                                                                                           ri − r̄
ward in Eq. 2: partial compilation credit pro-                                       Âi =                       (8)
                                                                                           σr + ϵ
vides early learning signal, disabled normalization
                                                                where r̄ = G1 G
                                                                              P
prevents variance collapse or explosion, and the                                 j=1 rj is the group mean and σr is
bounded log-squared performance term rewards                    the group standard deviation.
real speedups without letting measurement jitter                   For binary rewards ri ∈ {0, 1}, the advantage
dominate correctness.                                           Âi = 0 for all i if and only if all samples receive
                                                                the same reward:
K     Extended Results
                                                                     • If all ri = 0: then r̄ = 0, so ri − r̄ = 0 for all
K.1    Pass@K Analysis (Parallel Scaling)                              i
Table 14 presents pass@k results on ROCmBench                        • If all ri = 1: then r̄ = 1, so ri − r̄ = 0 for all
(31 Triton kernels), measuring the probability of                      i
generating at least one correct kernel within k sam-
ples. Our model achieves the highest pass@k                         Since samples are drawn independently:
across all values, with pass@5 reaching 41.94%                                 P (all fail) = (1 − pe )G             (9)
compared to 38.71% for Claude Sonnet 4.
                                                                              P (all pass) = pG
                                                                                              e                     (10)
K.2    Full Difficulty Breakdown                                      P (zero advantage) = pG
                                                                                            e + (1 − pe )
                                                                                                         G
                                                                                                                    (11)
Table 15 provides the complete difficulty-wise
breakdown including all model variants, showing
the progression from base model through SFT to                  Corollary 1 (Collapse Rate with Binary Rewards).
RL.                                                             For typical kernel generation with ∼6% initial suc-
                                                                cess rate (pe = 0.06) and group size G = 8:
K.3    Training Progression
                                                                    P (zero advantage) = (0.06)8 + (0.94)8          (12)
The progression from Base (4.9%) to SFT (10.3%)
to RL (33.2%) demonstrates the effectiveness of                                          ≈ 0 + 0.606 = 60.6% (13)


                                                           20
Factor                       Sensitivity      Observed effect
Compile partial credit       High             Raises usable gradient mass from near-zero to ∼44%
Disable σ-normalization      Critical         Avoids advantage collapse (Adv. ≈ 0.5 vs. ∼ 10−8 )
Credit value 0.2 vs. 0.4     Low–medium       Both learn; 0.4 gives denser early compile signal
Performance cap              Low              Stabilizes late training against noisy >15× speedups

                   Table 13: Qualitative sensitivity of reward design choices in sparse Triton RL.

                            Model              pass@1      pass@2        pass@3   pass@4    pass@5
                            Ours               27.10%      35.16%        38.71%   40.65%    41.94%
                            Claude Sonnet 4    25.81%      33.87%        36.77%   38.06%    38.71%
                            GPT-5              20.65%      28.39%        31.29%   32.26%    32.26%
                            Gemini 2.5 Pro     17.42%      24.84%        29.03%   32.26%    35.48%

              Table 14: Pass@K results on ROCmBench (31 kernels, 5 samples each with temp=1.0)


Over 60% of training batches produce zero gradi-                     Curriculum-Induced Clustering. During cur-
ents—the model cannot learn.                                         riculum training, batches contain samples of sim-
                                                                     ilar difficulty (e.g., all L1-Easy). Even success-
L.1.2    Our Solution: Hierarchical Rewards +                        ful samples receive similar rewards (≈1.4), caus-
         Disabled Normalization                                      ing σr ≈ 0. Disabled normalization handles this
To avoid binary-reward collapse, we combine two                      gracefully—any differential progress (one sample
mechanisms:                                                          achieving performance bonus while others don’t)
                                                                     produces non-zero gradients.
1. Hierarchical Rewards. Instead of binary r ∈                       L.2   On-Policy Reflection
{0, 1}, we use:
                                                                     At each turn, the policy conditions on the prompt,
                                                                     prior code and reflections, and the compiler or exe-
    r = r|compile    correct
                             rperf ∈ [0, 2.9]
            {z } + |r {z } + |{z}                        (14)
                                                                     cution feedback returned by the environment. The
            0.4            1.0      ≤1.5
                                                                     same parameters generate subsequent revisions and
                                                                     are updated from the resulting trajectory return. We
   This creates intermediate reward levels: a sam-
                                                                     use this standard on-policy construction as an im-
ple that compiles but fails correctness receives
                                                                     plementation choice; we do not claim a new policy-
r = 0.4, distinguishing it from complete failures
                                                                     gradient result.
(r = 0). This makes identical rewards across a
group less likely.                                                   L.3   Multi-Turn Credit Assignment
                                                                     Lemma 1 (Temporal Credit with γ < 1). For dis-
2. Disabled σ-Normalization. Even with hi-
                                                                     count factor γ = 0.6 and T = 3 turns, the effective
erarchical rewards, early training can exhibit re-
                                                                     contribution weights are:
ward clustering (e.g., most samples get r = 0 or
r = 0.4). When σr is small but non-zero, the stan-                                  w1 = 1.0         (Turn 1)       (16)
dard normalization Âi = (ri − r̄)/σr amplifies                                     w2 = 0.6         (Turn 2)       (17)
small differences into large, unstable gradients.
                                                                                    w3 = 0.36         (Turn 3)      (18)
   During training, we observed training collapse
due to these unstable gradients when using standard                  After normalization, this assigns approximately
normalization. Disabling normalization entirely                      51.0% of the weight to Turn 1, encouraging the
resolved this:                                                       model to succeed early while still rewarding im-
                      Âi = ri − r̄                      (15)        provement through reflection.

                                                                     M     Multi-Turn Self-Correction Examples
  The combination ensures: (1) hierarchical re-
wards create variance by distinguishing partial suc-                 We present abridged pseudocode examples illus-
cesses, and (2) disabled normalization keeps gradi-                  trating self-correction on medium-to-hard diffi-
ents stable when that variance is small.                             culty kernels. Ellipses and shortened fragments

                                                                21
                                                   Pass@K on ROCmBench (n=31 kernels)
                                            Qwen3-8B + RL (Ours)                                       41.9%
                                            Claude Sonnet 4
                               40           GPT-5
                                            Gemini 2.5 Pro

                  Pass@k (%)   30


                               20


                               10


                               0        1                 2                   3                    4                 5
                                                                k (number of samples)
Figure 3: Pass@K comparison on ROCmBench (31 kernels). Our model achieves the highest pass rate at all k
values, demonstrating superior sample efficiency for kernel generation.

                                    Difficulty          Claude     GPT-5      Gemini        Base       SFT     Ours
                                    D1 (Easy, 3)         1/3        0/3             2/3      2/3         3/3    3/3
                                    D2 (Med, 27)        12/27      7/27            9/27     7/27       10/27   17/27
                                    D3 (Hard, 65)       24/65      16/65          21/65     0/65        6/65   28/65
                                    D4 (V.Hard, 84)     18/84      5/84           11/84     0/84        0/84   13/84
                                    D5 (Expert, 5)       0/5        0/5             0/5      0/5         0/5    0/5
                                    Total                 55        28             43        9          19      61

Table 15: Complete difficulty-wise results (exec-correct kernels at final iteration). Base = Qwen3-8B, SFT =
Cold-Start SFT, Ours = SFT → Multi-Turn RL.


omit boilerplate and therefore are not standalone                             Turn 2 (Compile=✓, Exec=✓, Reward=1.87,
executable listings.                                                          Speedup=2.17×): Correct numerically stable soft-
                                                                              max:
                                                                              @triton.jit
M.1     Example 1: Cross-Attention                                            def softmax_kernel(input_ptr, output_ptr, n_rows, n_cols,
        (Medium-Hard)                                                                            input_row_stride, BLOCK_SIZE: tl.constexpr):

                                                                                   row_idx = tl.program_id(0)
Task: Implement cross-attention softmax kernel                                     row_start = input_ptr + row_idx * input_row_stride
                                                                                   col_offsets = tl.arange(0, BLOCK_SIZE)
for RGB-Depth fusion.                                                              mask = col_offsets < n_cols
                                                                                   vals = tl.load(row_start + col_offsets, mask=mask, other=-
   Concepts: Multi-head attention, softmax fusion,                                   inf)
                                                                                   # FIXED: Numerical stability
batched matrix operations, numerical stability.                                    row_max = tl.max(vals, axis=0)
                                                                                   vals_shifted = vals - row_max
                                                                                   numerator = tl.exp(vals_shifted)
Turn 1 (Compile=✓, Exec=✗, Reward=0.4):                                            output = numerator / tl.sum(numerator, axis=0)
                                                                                   tl.store(output_ptr + row_idx * n_cols + col_offsets,
Missing numerical stability (max subtraction):                                       output, mask=mask)
@triton.jit
def softmax_kernel(input_ptr, output_ptr, n_rows, n_cols,                       Recovery: Immediate (1 turn). Final speedup:
                   BLOCK_SIZE: tl.constexpr):
    row_idx = tl.program_id(0)
                                                                              2.17×.
    col_offsets = tl.arange(0, BLOCK_SIZE)
    vals = tl.load(input_ptr + row_idx * n_cols + col_offsets)
    # BUG: No numerical stability - causes overflow!                          M.2         Example 2: PreNorm Transformer
    output = tl.exp(vals) / tl.sum(tl.exp(vals))
    tl.store(output_ptr + row_idx * n_cols + col_offsets,
                                                                                          Decoder (Hard)
      output)
                                                                              Task: Implement Triton-optimized Pre-Norm
  Feedback: “NaN values in output. Softmax                                    Transformer Decoder Layer.
requires numerical stability: subtract max before                               Concepts: Fused layer normalization, multi-
exp() to prevent overflow.”                                                   head attention, cross-attention, FFN, residual con-

                                                                         22
nections.                                                              Kernel                 Diff.         T1 T2 T3 Speedup

Turn 1 (Compile=✗, Exec=✗, Reward=0.0): In-                            Cross-Attn. Softmax    Med.-Hard      ✗    ✓    ✓        2.17×
                                                                       PreNorm Trans.         Hard           ✗    ✗    ✓        9.13×
correct kernel structure for layer norm:                               Bound Softmax          Medium         ✗    ✓    ✓        5.18×
@triton.jit                                                            Fused Upsample         Hard           ✗    ✗    ✓        6.79×
def layer_norm_kernel(x_ptr, weight_ptr, output_ptr, M, N):
    # BUG: Missing eps, wrong reduction, no bias
                                                                       Weight Proc.           Hard           ✗    ✗    ✓        4.22×
    row = tl.program_id(0)
    mean = tl.sum(tl.load(x_ptr + row * N)) / N # Wrong load!
    var = tl.sum((x - mean) ** 2) / N                                 Table 16: Multi-turn recovery on medium-to-hard ker-
    output = (x - mean) / tl.sqrt(var) # Missing eps!                 nels with final speedups. ✓ = compile and execution
                                                                      pass; ✗ = fail.
  Feedback: “Compilation failed: undefined ’x’.
Also: missing eps causes division by zero, missing
bias parameter.”                                                          vals = tl.load(input_ptr + row_idx * n_cols + cols)
                                                                          max_val = tl.max(vals) # Only partial max!
                                                                          exp_vals = tl.exp(vals - max_val)
Turn 2 (Compile=✓, Exec=✗, Reward=0.4):                                   output = exp_vals / tl.sum(exp_vals)
Fixed syntax but wrong reduction for large N:
@triton.jit                                                              Feedback: “Incorrect softmax for n_cols=2048
def layer_norm_kernel(x_ptr, weight_ptr, bias_ptr, output_ptr,        > BLOCK_SIZE=1024. Partial max causes incor-
                      M, N, eps: tl.constexpr, BLOCK_SIZE: tl.
      constexpr):                                                     rect normalization.”
    row = tl.program_id(0)
    cols = tl.arange(0, BLOCK_SIZE)
    # BUG: Only handles N <= BLOCK_SIZE                               Turn 2 (Compile=✓, Exec=✓, Reward=2.9,
    x = tl.load(x_ptr + row * N + cols, mask=cols < N)
    mean = tl.sum(x) / N                                              Speedup=5.18×): Correct 3-pass algorithm:
    var = tl.sum((x - mean) ** 2) / N                                 @triton.jit
    ...                                                               def bound_softmax_kernel(input_ptr, output_ptr, n_rows, n_cols,

   Feedback:       “Incorrect output for N >                                                   BLOCK_SIZE: tl.constexpr):
                                                                          row_idx = tl.program_id(0)
BLOCK_SIZE. Use multi-pass reduction                                      row_start = input_ptr + row_idx * n_cols
                                                                          # PASS 1: Find global maximum
for large feature dimensions.”                                            max_val = float('-inf')
                                                                          for col_off in range(0, n_cols, BLOCK_SIZE):
Turn 3 (Compile=✓, Exec=✓, Reward=2.9,                                        cols = col_off + tl.arange(0, BLOCK_SIZE)
                                                                              mask = cols < n_cols
Speedup=9.13×): Correct multi-pass layer norm:                                vals = tl.load(row_start + cols, mask=mask, other=
                                                                            float('-inf'))
@triton.jit
                                                                              max_val = tl.maximum(max_val, tl.max(vals, axis=0))
def layer_norm_kernel(x_ptr, weight_ptr, bias_ptr, output_ptr,
                                                                          # PASS 2: Compute exp(x-max) and sum
                      M, N, eps: tl.constexpr, BLOCK_SIZE: tl.
                                                                          sum_val = 0.0
      constexpr):
                                                                          for col_off in range(0, n_cols, BLOCK_SIZE):
    row = tl.program_id(0)
                                                                              ... # Store intermediate, accumulate sum
    # FIXED: Multi-pass for arbitrary N
                                                                          # PASS 3: Normalize by sum
    mean = 0.0
                                                                          for col_off in range(0, n_cols, BLOCK_SIZE):
    for off in range(0, N, BLOCK_SIZE):
                                                                              ... # Divide by sum_val
        cols = off + tl.arange(0, BLOCK_SIZE)
        mask = cols < N
        x = tl.load(x_ptr + row * N + cols, mask=mask, other            Recovery: Immediate (1 turn). Final speedup:
      =0.0)
        mean += tl.sum(x, axis=0)                                     5.18×.
    mean = mean / N
    # Similar multi-pass for variance...
                                                                      M.4     Summary: Recovery Statistics
  Recovery: Progressive (2 turns). Final speedup:                     These examples demonstrate that RL training en-
9.13×.                                                                ables emergent debugging capabilities on com-
M.3     Example 3: Bound Softmax Multi-Pass                           plex GPU kernels: the model learns to handle multi-
        (Medium)                                                      pass reductions, numerical stability, arbitrary tensor
                                                                      dimensions, and fused operations—patterns that re-
Task: Implement numerically stable softmax for                        quire deep understanding of GPU programming
sequences longer than block size.                                     paradigms.
  Concepts: 3-pass algorithm (max, exp+sum,
normalize), arbitrary sequence length handling.                       M.5     Kernel Quality Analysis
Turn 1 (Compile=✓, Exec=✗, Reward=0.4):                               Across the five medium-to-hard case studies sum-
Single-pass fails for long sequences:                                 marized above, the agent-trained model produces
@triton.jit                                                           correct kernels with speedups of 2.17×, 9.13×,
def softmax_kernel(input_ptr, output_ptr, n_rows, n_cols,
                   BLOCK_SIZE: tl.constexpr):                         5.18×, 6.79×, and 4.22× over the PyTorch refer-
    row_idx = tl.program_id(0)                                        ence (geometric mean ≈ 4.94×, median 5.18×).
    # BUG: Assumes n_cols <= BLOCK_SIZE
    cols = tl.arange(0, BLOCK_SIZE)                                   Two qualitative observations emerge from inspect-

                                                                 23
ing the generated code. First, the optimizations are
not generic templates: the model selects different
strategies per workload (multi-pass safe softmax
for long sequences, fused layer-norm with running
statistics for the Pre-Norm decoder, masked tile
loads with ‘tl.exp‘ numerical stabilization for cross-
attention). Second, when a turn fails, the next-turn
revision typically targets the exact error class in the
feedback (e.g., adding numerical stabilization after
a NaN report, switching from single-pass to multi-
pass reduction after an out-of-bounds error). This
pattern is consistent with the multi-turn agent train-
ing objective: the same policy must produce both
the failure analysis and the corresponding code edit,
so reflections are tied to actionable revisions rather
than generic suggestions.
   We also note what these examples do not show.
They are not microbenchmarks tuned for a sin-
gle shape; each case is validated across mul-
tiple shape/stride/dtype combinations under the
same test harness used during training, so the re-
ported speedups reflect the realistic correctness-
and-performance trade-off our pipeline filters for.
A larger-scale latency distribution and memory-
consumption study across the full corpus is left for
future work and is explicitly listed in our limita-
tions.




                                                          24
