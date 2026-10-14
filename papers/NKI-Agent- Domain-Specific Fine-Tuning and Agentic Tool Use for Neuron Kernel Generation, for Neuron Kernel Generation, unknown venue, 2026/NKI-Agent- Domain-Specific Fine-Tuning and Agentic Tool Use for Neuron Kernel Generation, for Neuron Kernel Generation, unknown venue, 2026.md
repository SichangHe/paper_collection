                                                    NKI-Agent: Domain-Specific Fine-Tuning and Agentic Tool Use
                                                                  for Neuron Kernel Generation


                                                                  Junjie Tang 1 Jun Huan 1 Hao Zhou 1 Yuhao Zhang 1 Lin Wang 1


                                                                 Abstract                                     1. Introduction
                                                                                                              The rapid scaling of deep learning models has intensified
                                             Recent agentic approaches to LLM-based ker-                      demand for hardware-specific kernel optimization. While
arXiv:2607.04395v1 [cs.LG] 5 Jul 2026




                                             nel generation have achieved impressive results                  NVIDIA GPUs have benefited from decades of CUDA
                                             on CUDA. For emerging AI accelerators such                       ecosystem development and compiler optimizations, emerg-
                                             as AWS Trainium and Inferentia, automated ker-                   ing AI accelerators such as AWS Trainium and Inferentia
                                             nel generation and optimization remain largely                   require new approaches to kernel generation. The Neuron
                                             unaddressed. Writing kernels for these chips                     Kernel Interface (NKI) (AWS Neuron Team, 2024a) pro-
                                             via the Neuron Kernel Interface (NKI) is par-                    vides a Python-based programming model for these chips,
                                             ticularly challenging: developers must navigate                  but writing high-performance NKI kernels remains chal-
                                             a multi-engine architecture, tile-based program-                 lenging due to the unique multi-engine architecture and
                                             ming, and explicit data movement across multi-                   tile-based programming model.
                                             level memory hierarchy. Moreover, no publicly-
                                                                                                              Recent work on agentic code generation has demonstrated
                                             available training data, benchmarks, or tool-
                                                                                                              that agents equipped with execution feedback can generate
                                             augmented agents exist for this domain. We
                                                                                                              competitive GPU kernels. The CUDA-Agent (Dai et al.,
                                             introduce NKI-AGENT, the first system com-
                                                                                                              2026) system uses Proximal Policy Optimization (PPO)-
                                             bining domain-specific supervised fine-tuning
                                                                                                              trained agents on a synthesized dataset of 6,000 CUDA tasks,
                                             (SFT) with a compile-verify-fix agent loop for
                                                                                                              achieving 92–100% faster rates over torch.compile on
                                             NKI kernel generation. We adapt the existing
                                                                                                              KernelBench (Ouyang et al., 2025). However, this approach
                                             CUDA-Agent framework to Neuron hardware, cu-
                                                                                                              is specific to CUDA and does not address the distinct chal-
                                             rate 6,000 NKI kernel generation tasks for train-
                                                                                                              lenges of Neuron hardware.
                                             ing, and construct NKIG EN -B ENCH, a 250-task
                                             benchmark across three difficulty levels. Evalu-                 NKI programming presents unique challenges: (1) Multi-
                                             ated on real Trn1 hardware, NKI-AGENT with                       engine architecture with four specialized compute engines
                                             Claude Opus 4.8 and a rank-aware system prompt                   (Tensor, Vector, Scalar, GpSimd); (2) Tile-based program-
                                             achieves a 77.3% pass rate on the 150-task                       ming on 2D tiles with fixed 128-element partition dimen-
                                             NKIG EN -B ENCH. We show that tools use is criti-                sion; (3) Explicit memory hierarchy requiring manual data
                                             cal: Opus 4.8 scores 6% in single-shot mode with-                movement between HBM (high-bandwidth memory), SBUF
                                             out agent tools. On a 60-task subset, we show that               (on-chip scratchpad), and PSUM (partial-sum accumulator);
                                             an SFT-trained Qwen3-Coder-30B-A3B achieves                      (4) Evolving SDK with API changes between versions.
                                             25.0% pass rate at 1/100th the cost, outperform-
                                                                                                              In this paper, we present NKI-AGENT, the first system to
                                             ing Claude Sonnet 4 (15.0%). We also report
                                                                                                              apply domain-specific fine-tuning and agentic tool use to
                                             that Group Relative Policy Optimization (GRPO)
                                                                                                              NKI kernel generation. Our contributions:
                                             with binary compilation reward fails to improve
                                             over SFT, providing guidance on reward design
                                             for RL-based kernel generation.                                  1. NKI-AGENT: A multi-turn agent with compile and ver-
                                                                                                                 ify tools and a rank-aware system prompt for NKI kernel
                                                                                                                 generation. It supports various models including a fine-
                                            1
                                              Amazon Web Services. Correspondence to: Junjie Tang <jun-
                                                                                                                 tuned Qwen3-Coder-30B-A3B model with supervised
                                        jtang@amazon.com>.                                                       fine-tuning (SFT) and Group Relative Policy Optimiza-
                                                                                                                 tion (GRPO).
                                        Proceedings of the 43 rd International Conference on Machine
                                        Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026          2. NKI-Agent-Ops-6K & NKIG EN -B ENCH: 6,000 cu-
                                        by the author(s).                                                        rated NKI tasks and a 250-task benchmark across three

                                                                                                          1
                                 NKI-Agent: Agentic Tool Use for Neuron Kernel Generation

   difficulty levels.                                                3.1. NKI programming model

3. SFT data quality analysis: Four dataset iterations show-          Neuron chips feature four specialized engines: Tensor (ma-
   ing data curation matters more than hyperparameters.              trix ops), Vector (elementwise/reduction), Scalar (control
                                                                     flow), and GpSimd (general-purpose). Programs operate
4. Negative result: GRPO with binary reward fails to im-             on 2D tiles with a fixed 128-element partition dimension.
   prove over SFT.                                                   Data must be explicitly moved between HBM (device mem-
                                                                     ory), SBUF (24 MB scratchpad), and PSUM (partial sum
                                                                     accumulator) in a load, compute, store pattern. This differs
The NKI-AGENT framework achieves 77.3% on the 150-                   fundamentally from CUDA’s thread-block model, requiring
task NKIG EN -B ENCH with a frontier model (Opus 4.8                 domain-specific knowledge for correct kernels.
with a rank-aware prompt), and our domain-specialized
SFT model captures a large fraction of this performance at           3.2. Data synthesis pipeline
1/100th the cost (25.0% vs 63.3% on the 60-task subset),
outperforming Sonnet 4 (15.0%) with identical tools.                 We synthesize a dataset NKI-Agent-Ops-6K in three stages:
                                                                     (1) Seed crawling from PyTorch torch.nn (∼180 ops),
                                                                     nki-samples (∼30 kernels), and KernelBench (∼250
2. Related work                                                      tasks), yielding ∼400 seeds. (2) Combinatorial expansion
LLM-based kernel generation. KernelBench (Ouyang                     via shape (5×), dtype (3×), and fusion synthesis (∼200 pat-
et al., 2025) benchmarks LLM-generated GPU kernels.                  terns), producing ∼15K candidates. (3) Filtering through
CUDA-Agent (Dai et al., 2026) trains PPO-based agents                compilation, execution, stability (CV<10%), and baseline
on 6,000 CUDA tasks with compile-verify-profile tools.               checks, balanced to 6,000 tasks. The 250 NKIG EN -B ENCH
Other approaches include AlphaCode-style search (Li et al.,          tasks are held out. For SFT, we curate 647 high-quality
2022), self-repair (Olausson et al., 2024), and Triton-              episodes through four iterations (Section 5.1).
Bench (Li et al., 2025). Related code-translation work
generates accelerator code by translating across languages:          3.3. Agent architecture
TransCoder (Lachaux et al., 2020), BabelTower (Wen et al.,
                                                                     NKI-AGENT operates through multi-turn interaction with
2022), and CodeRosetta (TehraniJamsaz et al., 2024). The
                                                                     two tools on real Trn1 hardware: (1) compile kernel in-
agentic-coding evaluation lineage (SWE-bench (Jimenez
                                                                     vokes neuronx-cc with 120s timeout and returns com-
et al., 2024), SWE-agent (Yang et al., 2024)) motivates our
                                                                     pilation status with error messages; (2) verify kernel runs
tool-augmented, execution-grounded setup.
                                                                     the compiled kernel with random inputs, comparing against
                                                                     the PyTorch reference via torch.allclose. The agent
RL for code generation. CodeRL (Le et al., 2022) and                 iterates up to T =10 turns: generate, compile, verify, fix.
PPOCoder (Shojaee et al., 2023) use execution rewards;               We set T =10 empirically: in our evaluation runs the vast
DeepSeek-R1 (DeepSeek-AI et al., 2025) demonstrates                  majority of eventual successes converge within the first few
GRPO (Shao et al., 2024) without a critic. CUDA-Agent                turns, and gains beyond ten turns are negligible while the
shows RL with graded reward outperforms SFT; we show                 per-turn Trn1 compile/verify cost grows linearly, so T =10
the converse for binary reward.                                      balances solution coverage against evaluation cost.

Neuron hardware and NKI. AWS Trainium/Inferentia                     Rank-aware system prompt. NKIBench inputs span 2-D,
chips (Amazon Web Services, 2024) feature four specialized           3-D, and 4-D tensors (e.g. batched attention and N,C,H,W
compute engines. NKI (AWS Neuron Team, 2024a) pro-                   convolutions), but a naive prompt assumes a 2-D (M, N )
vides tile-based programming; prior work is limited to refer-        layout. We use a rank-aware prompt that instructs the model
ence kernels (AWS Neuron Team, 2024b). AccelOpt (Zhang               to read each task’s input-shape block and provides templates
et al., 2026) (concurrent) addresses NKI kernel optimiza-            for 2-D, 3-D, and 4-D kernels, plus a reminder that every
tion, complementary to our correctness-first generation.             output element must be written by an nl.store. This is a
                                                                     prompt-only change (no retraining or extra tool calls) and
3. Method                                                            is the primary driver of model’s performance gains on hard
                                                                     examples.
Figure 1 illustrates the NKI-AGENT system. It consists of
four components: (1) a data synthesis pipeline producing
                                                                     3.4. Training pipeline
6,000 curated NKI tasks, (2) a multi-turn agent with compile
and verify tools, (3) a binary reward function, and (4) a two-       Base model. We selected Qwen3-Coder-30B-A3B (Team,
stage SFT → GRPO training pipeline.                                  2025) after evaluating models from 1.1B to 30B parameters.

                                                                 2
                                      NKI-Agent: Agentic Tool Use for Neuron Kernel Generation




Figure 1. NKI-AGENT system overview. Top: The agent generates NKI code, then iteratively compiles and verifies on Trn1 hardware
(≤10 turns). Compile errors and verification failures feed back for correction. Bottom: Data pipeline produces 6,000 tasks; SFT on
curated episodes followed by GRPO with binary reward.


Table 1. Main results on NKIG EN -B ENCH (150-task). Pass                4. Experiments
rate on balanced subset (50 per level). All results from real Trn1
hardware. Note: at N =150, differences of 1–2 tasks (∼0.7pp)             4.1. NKIG EN -B ENCH
are within noise; per-level and 60-task results (Tables 2, 3) show
clearer separation.                                                      NKIG EN -B ENCH1 contains 250 tasks across three difficulty
                                                                         levels: Level 1 (100 tasks: single operations such as matmul,
      Model                   Single-Shot     NKIAgent (10 turns)
                                                                         activations, reductions, convolutions), Level 2 (100 tasks:
      Base (Qwen3-30B-A3B)   14.0% (21/150)     20.0% (30/150)
      SFT                    19.3% (29/150)     20.7% (31/150)           fused operations like conv+relu+bias, attention blocks, MLP
      GRPO                   15.3% (23/150)     17.3% (26/150)           components), and Level 3 (50 tasks: full model components
                                                                         including Transformer layers, ResNet bottlenecks, Mamba
                                                                         blocks). Each task provides a PyTorch Model class and
                                                                         NKI-specific metadata. Of 250 tasks, ∼150 are adapted
                                                                         from KernelBench, 60 require decomposition, and 40 are
                                                                         NKI-native. We evaluate on a balanced 150-task subset (50
                                                                         per level) and a 60-task subset for ablations.

                                                                         4.2. Evaluation setup
                                                                         Models: (1) Base Qwen3-Coder-30B-A3B; (2) SFT;
                                                                         (3) GRPO (SFT + 200 RL steps); (4) Claude Sonnet 4;
                                                                         (5) Claude Opus 4.8 (frontier upper bound). All Claude
                                                                         models use identical NKI-AGENT tools.
For inference, we serve via vLLM with tensor parallelism
and native function-calling.                                             Modes: Single-shot (SS, one generation, no tools), MT-5
                                                                         (5 turns without tools; the harness compiles the output and
Stage 1: SFT. We fine-tune Qwen3-Coder-30B-A3B on                        feeds back raw error text as a user message, but the model
647 curated episodes using LoRA (Hu et al., 2021) (rank                  cannot invoke tools itself), and NKIAgent (≤10 turns with
32, alpha 64, 26.7M params / 0.09%) for 2 epochs with                    compile/verify tools).
lr=2×10−4 , batch=4, and BF16 on 8×A100 40GB.
                                                                         Metric: pass rate = compiles on neuronx-cc + numeri-
Stage 2: GRPO. From the SFT checkpoint, we apply
                                                                             1
GRPO (Shao et al., 2024). For each prompt, G=4 ker-                            Not to be confused with the concurrently developed
nels are generated, each scored with binary reward (+1.0                 NKIB ENCH of Zhang et al. (2026), a kernel optimization suite
                                                                         for Trainium; NKIG EN -B ENCH targets kernel generation and
correct, −0.5 fail), and group-relative advantages computed.             correctness.
We trained for 200 steps with lr=5×10−7 and β=0.1.

                                                                     3
                                  NKI-Agent: Agentic Tool Use for Neuron Kernel Generation

Table 2. Pass rate by difficulty level (150-task, 50 per level). NKIAgent tool use uniquely enables Level 2 and Level 3 tasks where
single-shot achieves near-zero success.

                                                     Single-Shot               NKIAgent
                                      Model        L1     L2     L3       L1      L2       L3
                                      Base        34%     8%     0%      26%     18%      16%
                                      SFT         50%     8%     0%      30%     16%      16%
                                      GRPO        44%     2%     0%      22%     18%      12%
                                      Opus 4.8    10%     8%     0%      84%     74%      74%



cally correct (atol=rtol=10−3 ) vs PyTorch reference. All on         Table 3. Ablation study comparing evaluation modes and model
                                                                     configurations. The 60-task subset enables additional comparisons.
real Trn1 hardware.                                                  “—” indicates configurations not evaluated on the larger set due to
                                                                     compute constraints (each 150-task NKIAgent run requires ∼20
4.3. Main results                                                    hours on Trn1). Bold: best trained model and best overall.

Tables 1 and 2 present the main results. On the aggregate              Configuration                60-task            150-task
150-task metric, SFT NKIAgent (20.7%) and Base NKI-                    Base SS                   10.0% (6/60)       14.0% (21/150)
Agent (20.0%) are within statistical noise (1 task apart).             SFT SS                    15.0% (9/60)       19.3% (29/150)
The clearer signal emerges from per-level breakdown and                SFT MT-5 (no tools)       15.0% (9/60)            —
60-task ablations (Table 3). Key findings:                             Base NKIAgent            16.7% (10/60)      20.0% (30/150)
                                                                       SFT NKIAgent             25.0% (15/60)      20.7% (31/150)
• SFT + NKIAgent achieves 20.7% on 150-task and 25.0%                  GRPO NKIAgent            16.7% (10/60)      17.3% (26/150)
  on 60-task. The NKI-AGENT framework scales to 77.3%                  Sonnet NKIAgent           15.0% (9/60)             —
  with Opus 4.8 (Table 3), showing the framework design                Opus 4.8 SS               0.0% (0/60)         6.0% (9/150)
  is sound and model capability is the primary bottleneck.             Opus 4.8 NKIAgent        63.3% (38/60)      77.3% (116/150)
• Tool use uniquely enables L2/L3. No model solves any
  L3 task in single-shot (0/50); NKIAgent achieves 16%
  via iterative compile-fix.
• SFT improves L1: 34%→50%, reflecting learned NKI                   without iterative compiler feedback. Opus 4.8’s L3 pass
  patterns (tile dims, nl.load/nl.store).                            rate (74% on 150-task) is particularly notable: where all
                                                                     other models achieve ≤16%, Opus 4.8 succeeds on nearly
• L1 NKIAgent < L1 SS: a counterintuitive pattern where              three-quarters of full model components.
  tool use hurts easy tasks. The agent sometimes “fixes”
  already-correct code after seeing unrelated compiler warn-
  ings, or exhausts turns exploring alternatives. Tool use is
  net-positive only for tasks that require iterative debugging       Cost-capability tradeoff. Our SFT model (3B active
  (L2/L3).                                                           params, 7.1 tok/s) captures 40% of Opus 4.8’s performance
• GRPO degrades performance vs SFT across all settings               (25.0% vs 63.3% on the 60-task subset) at ∼1/100th the per-
  (Section 5.2).                                                     token cost. The SFT model outperforms Sonnet (25.0% vs
                                                                     15.0%) despite ∼300× less NKI training data than CUDA,
                                                                     demonstrating that domain SFT on scarce data can close a
4.4. Single-shot vs. NKIAgent                                        large fraction of the gap to frontier models.
Table 3 reveals several findings. Multi-turn without tools
does not help (MT-5 = SS at 15.0%), echoing the Reflex-              5. Analysis
ion (Shinn et al., 2023) finding that verbal self-feedback
                                                                     5.1. SFT data quality progression
without grounded execution signal yields limited gains. SFT
and NKIAgent are super-additive (+5.0pp + +6.7pp sep-                Table 4 traces our data curation journey. SFT v2 with bad
arately, +15.0pp combined). Most strikingly, Opus 4.8                data hurts performance (8.3% vs base 10.0%). Each fix tar-
achieves 0% in single-shot but 63.3% with NKIAgent                   geted one issue: v1→v2 fixed message format; v2→v3 stan-
tools on the 60-task subset (6% vs 77.3% on 150-task),               dardized function names (64% were wrong); v3→v4 con-
the largest tool-use gap in our study, demonstrating that            verted 3D tensors to 2D. This shows that each data quality
even frontier models cannot generate correct NKI kernels             fix produced larger gains than any hyperparameter change.

                                                                 4
                                                            NKI-Agent: Agentic Tool Use for Neuron Kernel Generation

                                                        Single-Shot                                                                     NKIAgent (10 turns)
                100
                                                                                 Base           GRPO                                                                         Base                     GRPO
                                                                                 SFT v4                                            84                                        SFT v4                   Opus 4.8
                 80                                                                                                                                               74                                     74
Pass Rate (%)




                 60
                                 50
                                      44
                 40      34
                                                                                                                    30
                                                                                                               26
                                                                                                                              22
                 20                                                                                                                        18      16        18               16      16
                                                                                                                                                                                                12
                                                    8          8
                                                                        2
                     0
                                 L1                           L2                          L3                             L1                             L2                                 L3
                                                    Difficulty Level                                                                        Difficulty Level

Figure 2. Pass rate by difficulty level (150-task). Left: single-shot shows steep degradation from L1 to L3, with all trained models at 0%
on L3. Right: NKIAgent enables meaningful L2/L3 performance. Opus 4.8 with the rank-aware prompt (purple) dominates all levels,
particularly L3 (74% vs ≤16% for trained models).

                70
                                                                                                                                                                                           63.3%
                60                                      Single-shot / No tools                                                          NKIAgent (10 turns)


                50
Pass Rate (%)




                40

                30
                                                                                                                                                                   25.0%

                20                                                                                     16.7%             16.7%
                                                                     15.0%           15.0%                                               15.0%
                              10.0%          8.3%                                                                                                                                                    Base SS ref.
                10

                 0
                              Base         SFT v2 SS                 SFT v4       SFT v4 MT-5        Base             GRPO               Sonnet                    SFT v4              Opus 4.8
                               SS          (bad data)                  SS          (no tools)      NKIAgent          NKIAgent           NKIAgent                  NKIAgent             NKIAgent

Figure 3. Ablation study (60-task subset). Opus 4.8 NKIAgent (63.3%) establishes the framework’s upper bound. SFT NKIAgent
(25.0%) captures 40% of frontier performance. SFT v2 with bad data (8.3%) underperforms the base model (10.0%).

Turn 1: Agent generates initial kernel with nl.matmul(a tile, b tile)
  ,→ compile kernel: FAIL — nl.matmul does not exist; use nisa.nc matmul
Turn 2: Agent switches to nisa.nc matmul, incorrect tile shape (128, 512)
  ,→ compile kernel: FAIL — free dim of lhs must equal partition dim of rhs
Turn 3: Agent transposes RHS, adds tiling loop over K dimension
  ,→ compile kernel: OK. verify kernel: FAIL — allclose atol=1e-3 failed
Turn 4: Agent adds PSUM accumulation with nisa.nc matmul(..., mask=...)
  ,→ compile kernel: OK. verify kernel: PASS

Figure 4. Illustrative NKIAgent trace (condensed from evaluation logs). The agent iteratively discovers the correct API
(nisa.nc matmul), fixes tile dimension constraints, and adds proper accumulation, errors that are impossible to recover from
in single-shot mode.


 5.2. GRPO negative result                                                                               selects among incorrect outputs. CUDA-Agent’s graded
                                                                                                         reward (speedup measurements) provides richer signal.
Table 5 shows GRPO consistently underperforms SFT v4
(average reward flat at ∼10–15% compile rate across 200
                                                                                                         5.3. Error analysis and qualitative findings
steps). We hypothesize: (1) binary reward is too sparse,
with no signal between “almost compiles” and “completely                                                 Category-level patterns. SFT excels at elementwise
wrong”; (2) subtle code changes flip reward discontinuously;                                             (87.5%) and activation (90.0%) operations. Convolutions,
(3) when ∼75% of generations fail, group-relative ranking                                                attention, and all Level 3 components achieve 0% in single-


                                                                                                   5
                                    NKI-Agent: Agentic Tool Use for Neuron Kernel Generation

Table 4. SFT data quality progression. Each version fixes a systematic data issue. “–” = version discarded before full evaluation (issues
found during spot checks).

                          Version           Issue Fixed                                  SS (60)        ∆
                          v1                Wrong message format                           —            —
                          v2                64% wrong function names + overfitting        8.3%       baseline
                          v3                48% used 3D shapes (should be 2D)              —            —
                          v4                All fixed: 2D shapes, correct naming         15.0%      +81% rel.
                          Base (no SFT)     —                                            10.0%          —

Table 5. GRPO fails to improve over SFT v4. 200 steps of GRPO with binary reward degrades performance across all configurations.

                               Model      SS (60)      NKIAgent (60)       SS (150)     NKIAgent (150)
                               SFT v4      15.0%           25.0%            19.3%             20.7%
                               GRPO        13.3%           16.7%            15.3%             17.3%
                               ∆           −11%            −33%             −21%              −16%


shot for our model. However, Opus 4.8 NKIAgent achieves                Conclusion
74% on Level 3 (37/50, 150-task), demonstrating that the
NKI-AGENT tool framework is sufficient for complex tasks               We presented NKI-AGENT, an agentic system combining
when paired with stronger base models.                                 domain-specific supervised fine-tuning with agentic tool use
                                                                       for kernel generation on AWS Neuron hardware. Evaluated
                                                                       on NKIG EN -B ENCH, our framework demonstrates that it-
Common failures. Incorrect tile dimensions (parti-                     erative compile-verify-fix loops are essential where even
tion ̸= 128), unsupported operation combinations, and                  Claude Opus 4.8 scores 6% in single-shot but 77.3% with
SBUF/PSUM memory violations. Failures are systematic:                  agent tools. Our SFT-trained Qwen3-Coder-30B-A3B cap-
entire categories fail uniformly, suggesting broader data cov-         tures 40% of frontier performance at 1/100th the cost, out-
erage is more promising than RL. SFT reliably generates the            performing Claude Sonnet 4. We additionally show that data
load→compute→store pattern with 128-element partition                  quality dominates hyperparameter tuning, and that GRPO
but struggles with Tensor Engine matmul and multi-engine               with binary reward fails to improve over SFT, providing
pipelining.                                                            guidance on reward design for RL-based kernel generation.

5.4. Example agent trace
                                                                       References
Figure 4 shows an illustrative NKIAgent interaction on a
                                                                       Amazon Web Services. Aws neuron sdk. https:
matrix multiplication task, condensed from typical evalu-
                                                                        //aws.amazon.com/ai/machine-learning/
ation logs. This trace illustrates why tool use is essential:
                                                                        neuron/, 2024.
the agent must discover that nl.matmul does not exist in
NKI, learn the tile shape constraints of nisa.nc matmul,               AWS Neuron Team.  Neuron kernel interface (nki)
and fix numerical accumulation, each requiring real com-                documentation.  https://awsdocs-neuron.
piler feedback.                                                         readthedocs-hosted.com/en/latest/nki/,
                                                                        2024a.
6. Limitations and future work                                         AWS Neuron Team.      Nki samples: Reference nki
Our work has several limitations. First, we evaluate cor-               kernel implementations. https://github.com/
rectness only, not runtime performance; AccelOpt (Zhang                 aws-neuron/nki-samples, 2024b. MIT-0 Li-
et al., 2026) addresses this complementary axis. Second,                cense.
binary reward was insufficient for GRPO; graded rewards                Dai, W., Wu, H., Yu, Q., ang Gao, H., Li, J., Jiang, C., Lou,
remain future work. Third, all results are single-run without            W., Song, Y., Yu, H., Chen, J., Ma, W.-Y., Zhang, Y.-Q.,
error bars; small absolute differences may not be statisti-              Liu, J., Wang, M., Liu, X., and Zhou, H. Cuda agent:
cally significant. Fourth, our SFT model uses only 3B active             Large-scale agentic rl for high-performance cuda kernel
parameters; our Opus 4.8 results (77.3%) confirm that scal-              generation, 2026. URL https://arxiv.org/abs/
ing model capability significantly improves results within               2602.24286.
the same framework. Finally, results are specific to Neuron
SDK 2.24.                                                              DeepSeek-AI, Guo, D., Yang, D., Zhang, H., Song, J., Wang,

                                                                   6
                                 NKI-Agent: Agentic Tool Use for Neuron Kernel Generation

  P., Zhu, Q., Xu, R., Zhang, R., Ma, S., Bi, X., Zhang,               efficient gpu kernels?, 2025. URL https://arxiv.
  X., Yu, X., Wu, Y., Wu, Z. F., Gou, Z., Shao, Z., Li,                org/abs/2502.10517.
  Z., Gao, Z., et al. Deepseek-r1: Incentivizing reasoning
  capability in llms via reinforcement learning, 2025. URL           Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X.,
  https://arxiv.org/abs/2501.12948.                                    Zhang, H., Zhang, M., Li, Y. K., Wu, Y., and Guo,
                                                                       D. Deepseekmath: Pushing the limits of mathemat-
Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang,          ical reasoning in open language models, 2024. URL
  S., Wang, L., and Chen, W. Lora: Low-rank adaptation of              https://arxiv.org/abs/2402.03300.
  large language models, 2021. URL https://arxiv.
                                                                     Shinn, N., Cassano, F., Berman, E., Gopinath, A.,
  org/abs/2106.09685.
                                                                       Narasimhan, K., and Yao, S. Reflexion: Language
Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press,         agents with verbal reinforcement learning, 2023. URL
  O., and Narasimhan, K. Swe-bench: Can language                       https://arxiv.org/abs/2303.11366.
  models resolve real-world github issues?, 2024. URL
                                                                     Shojaee, P., Jain, A., Tipirneni, S., and Reddy, C. K.
  https://arxiv.org/abs/2310.06770.
                                                                       Execution-based code generation using deep reinforce-
Lachaux, M.-A., Roziere, B., Chanussot, L., and Lam-                   ment learning, 2023. URL https://arxiv.org/
  ple, G. Unsupervised translation of programming lan-                 abs/2301.13816.
  guages, 2020. URL https://arxiv.org/abs/
  2006.03511.                                                        Team, Q. Qwen3 technical report, 2025. URL https:
                                                                       //arxiv.org/abs/2505.09388.
Le, H., Wang, Y., Gotmare, A. D., Savarese, S., and Hoi,
  S. C. H. Coderl: Mastering code generation through                 TehraniJamsaz, A., Bhattacharjee, A., Chen, L., Ahmed,
  pretrained models and deep reinforcement learning, 2022.             N. K., Yazdanbakhsh, A., and Jannesari, A. Coderosetta:
  URL https://arxiv.org/abs/2207.01780.                                Pushing the boundaries of unsupervised code transla-
                                                                       tion for parallel programming, 2024. URL https:
Li, J., Li, S., Gao, Z., Shi, Q., Li, Y., Wang, Z., Huang,             //arxiv.org/abs/2410.20527.
  J., Wang, H., Wang, J., Han, X., Liu, Z., and Sun, M.
  Tritonbench: Benchmarking large language model ca-                 Wen, Y., Guo, Q., Fu, Q., Li, X., Xu, J., Tang, Y., Zhao,
  pabilities for generating triton operators, 2025. URL               Y., Hu, X., Du, Z., Li, L., Wang, C., Zhou, X., and
  https://arxiv.org/abs/2502.14752.                                   Chen, Y. Babeltower: Learning to auto-parallelized
                                                                      program translation. In International Conference on
Li, Y., Choi, D., Chung, J., Kushman, N., Schrittwieser, J.,          Machine Learning, ICML 2022, 17-23 July 2022, Bal-
  Leblond, R., Eccles, T., Keeling, J., Gimeno, F., Lago,             timore, Maryland, USA, volume 162 of Proceedings of
  A. D., Hubert, T., Choy, P., de Masson d’Autume, C.,                Machine Learning Research, pp. 23685–23700. PMLR,
  Babuschkin, I., Chen, X., Huang, P.-S., Welbl, J., Gowal,           2022. URL https://proceedings.mlr.press/
  S., Cherepanov, A., Molloy, J., Mankowitz, D. J., Rob-              v162/wen22b.html.
  son, E. S., Kohli, P., de Freitas, N., Kavukcuoglu, K.,
  and Vinyals, O. Competition-level code generation with             Yang, J., Jimenez, C. E., Wettig, A., Lieret, K., Yao,
  alphacode, 2022. URL https://arxiv.org/abs/                          S., Narasimhan, K., and Press, O. Swe-agent: Agent-
  2203.07814.                                                          computer interfaces enable automated software engineer-
                                                                       ing, 2024. URL https://arxiv.org/abs/2405.
Olausson, T. X., Inala, J. P., Wang, C., Gao, J., and Solar-           15793.
  Lezama, A. Is self-repair a silver bullet for code gen-
  eration?, 2024. URL https://arxiv.org/abs/                         Zhang, G., Zhu, S., Wei, A., Song, Z., Nie, A., Jia, Z., Vi-
  2306.09896.                                                          jaykumar, N., Wang, Y., and Olukotun, K. Accelopt: A
                                                                       self-improving llm agentic system for ai accelerator ker-
Ouyang, A., Guo, S., Arora, S., Zhang, A. L., Hu, W., Ré,             nel optimization, 2026. URL https://arxiv.org/
  C., and Mirhoseini, A. Kernelbench: Can llms write                   abs/2511.15915.




                                                                 7
