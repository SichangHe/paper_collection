                                         MathForm



                                         MathForm: Scaling Mathematical Autoformalization with
                                         Knowledge Retrieval and Verification-Guided Refinement
                                                Lushi Pu1 , Weiming Zhang2 , Xinheng Xie1 , Zixuan Fu2 , Bingxiang He2 , Hengyu Zhao1 ,
                                                                  Hongya Lyu1 , Xin Li1 , Jie Zhou1 , Yudong Wang2†
                                                                      1
                                                                        ModelBest Inc. 2 Tsinghua University
                                                                pulushi@modelbest.cn yudongwang@tsinghua.edu.cn

                                                                        https://huggingface.co/datasets/openbmb/FormalVerse
                                                                        https://huggingface.co/openbmb/MathForm-8B
                                                                        https://github.com/openbmb/MathForm


                                                                                           Abstract
                                                  Autoformalization is commonly framed as translating natural-language mathematical
                                                  statements into machine-verifiable formal languages such as Lean 4. However, faithful
                                                  formalization requires more than translation. Models must map mathematical concepts
arXiv:2608.14221v1 [cs.AI] 14 Aug 2026




                                                  to the complex hierarchy of types and definitions in formal libraries such as Mathlib,
                                                  while ensuring that generated statements preserve the meaning of the source propositions.
                                                  Existing approaches struggle because they rely heavily on the model’s parametric memory
                                                  for library-specific knowledge, while common data construction pipelines often resort to
                                                  filtering single-pass outputs and lack mechanisms for feedback-driven revision. To address
                                                  these challenges, we introduce MathForm, an autoformalization framework for construct-
                                                  ing verified training data through Mathlib knowledge retrieval and verification-guided
                                                  iterative refinement. Before generation, a retrieval planner gathers relevant definitions
                                                  and existing formalizations from Mathlib to guide the formalization generator. Generated
                                                  statements are then revised using compiler diagnostics and semantic-consistency feedback.
                                                  Using this framework, we construct FormalVerse, a Lean 4 dataset containing approxi-
                                                  mately 367K verified examples across diverse mathematical domains and sources. We then
                                                  train MathForm-8B through supervised fine-tuning followed by reinforcement learning.
                                                  Across six benchmarks, MathForm-8B achieves average Pass@8 rates of 88.06% under
                                                  Syntax Check (SC) and 72.37% under Consistency Check (CC), outperforming multiple
                                                  specialized 32B autoformalizers. On the challenging FATE-H and FATE-X subsets, it
                                                  attains CC pass rates of 63% and 37%, exceeding the strongest specialized baselines in
                                                  both cases.


                                         1   Introduction
                                         Recent advances in large language models (LLMs) have substantially improved formal theorem proving,
                                         enabling systems such as AlphaProof (Hubert et al., 2026), DeepSeek-Prover-V2 (Ren et al., 2025), and Goedel-
                                         Prover-V2 (Lin et al., 2025) to generate sophisticated Lean 4 (Moura & Ullrich, 2021) proofs for formally stated
                                         problems. However, scaling these systems further requires large and diverse corpora of machine-checkable
                                         statements and proofs, which remain scarce. A central bottleneck is that much mathematical knowledge exists
                                         only in natural language, and encoding it manually in a formal language demands both precise mathematical
                                         interpretation and considerable expertise with the proof assistant itself. Autoformalization addresses this
                                         bottleneck by translating natural-language mathematical statements into machine-checkable representations
                                         such as Lean 4 code, providing a scalable way to unlock these informal resources.
                                         Despite notable progress in autoformalization, existing approaches face two methodological limitations.
                                         First, prevailing methods (Wang et al., 2024; Gao et al., 2025; Xuejun et al., 2026) rely primarily on the
                                         mathematical and programming knowledge stored in parametric memory. However, formalization in Lean
                                         requires not only an understanding of the underlying mathematical semantics but also familiarity with
                                         Mathlib’s (mathlib Community, 2020) definitions, type system, notational conventions, existing structures,
                                             † Corresponding authors.




                                                                                              –1–
MathForm


           MathForm-8B                                                                               72.37

             ReForm-32B                                                                          68.41

              ReForm-8B                                                                      66.21

          Goedel-V2-32B                                                                  63.74

           Goedel-V2-8B                                                              60.07

             StepFun-32B                                                   44.47

              StepFun-7B                                           39.55

        Mathesis-HPO-7B                                    34.96

              Kimina-7B                                    34.37

               Herald-7B                           27.63

                       0%                20%                  40%                  60%                       80%
                                        Pass Rate of Consistency Check (%)

Figure 1: Macro-average Pass@8 (%) across six benchmarks among specialized autoformalizers. M ATH F ORM-
8B achieves the strongest overall performance within this category despite its smaller model size.




and common formalization patterns. Such knowledge is highly specific and evolves as the library develops,
which makes it difficult to internalize fully in model parameters. Models therefore tend to misuse existing
definitions, invoke lemmas that do not exist, or produce expressions that are valid yet depart from library
conventions. Second, many existing pipelines for constructing autoformalization data (Wang et al., 2025; Wu
et al., 2025; Yu et al., 2025b) adopt a Best-of-N (BoN) strategy, in which the model samples a large pool of
candidates that a discriminator then filters post hoc. Such pipelines can improve the quality of the resulting
data, but they merely select from the model’s existing output distribution, since every candidate comes from
single-pass generation. Moreover, the discriminator only accepts or rejects a candidate as a whole, so it cannot
indicate where a semantic deviation occurs or how to repair it. The difficulty of the data is therefore capped at
the model’s current single-pass capability. Together, these two limitations leave existing datasets and models
concentrated on competition-style algebra and number theory (Zheng et al., 2022), while statements with
complex preconditions and domains that demand deeper library knowledge, such as abstract algebra (Jiang
et al., 2026), remain underrepresented.
We argue that both limitations stem from treating autoformalization as a one-shot translation to be judged after
the fact, whereas faithful formalization is better understood as a knowledge-grounded process that converges
through repeated verification. Because a single mathematical object may correspond to a complex hierarchy of
types and definitions in Mathlib, a plausible-looking statement can compile and still strengthen a condition or
drop a key assumption. Such a deviation renders the statement of little use downstream.
To this end, we propose M ATH F ORM, a framework for autoformalization data construction and model training
that organizes library knowledge retrieval, automated verification, and iterative refinement into a closed loop.
Before generation, retrieval supplies definitions and existing formalizations from Mathlib, so the model need
not recall library knowledge from parameters alone. Compiler diagnostics and semantic-consistency judgments
then locate what is wrong with a candidate rather than merely rejecting it, and iterative refinement turns that
feedback into concrete revisions. The ceiling on data difficulty is then set by the pipeline as a whole rather
than by single-pass generation, so it can formalize statements that a single pass fails to handle, extending
the training data to harder statements and more advanced mathematical domains. Training on such data
compresses the capability of the whole pipeline into the model’s single-pass generation, realizing a form of
data–model co-evolution (Wang et al., 2026b).
Using this framework, we construct F ORMALV ERSE, a Lean 4 dataset of approximately 367K verified
examples spanning diverse mathematical domains and problem sources (Appendix Figure 6), and reconstruct
a clean formalization trajectory for each example. Building on these data, we train M ATH F ORM-8B through
supervised fine-tuning (SFT) followed by reinforcement learning (RL). On FormalMATH-Lite (Yu et al.,
2025b), DeepSeek-ProverBench (Ren et al., 2025), CombiBench (Liu et al., 2026), and FATE (Jiang et al.,
2026), it outperforms existing models of comparable size under Pass@8 and matches or exceeds substantially


                                                      –2–
MathForm




                     1. Formalization Generation             Refine                        2. Verification                           3. Refinement
                                                                                                                            Syntax Error

                            α   Questions              LLM Generator
                                                                                             Format Check                   {
                                                                                                                              "severity": "error",
                                                                                            := by sorry                       "pos": {"line": 2, "column": 46},
         Error Histories                                                                                                      "data": "failed to
                                                                                                                            synthesize OfNat Lang 0"
                                                                                                                            }
                           Retrieval Planner       Syntax Definitions
                                                                                                                            Semantic Error

                                    Generate                                                 Syntax Check                    {
                                                               ƒ(x)                                                            "result": "incorrect",
                                                                                                                               "reason": "NL quantifies n over
                                                                                                                             all integers (ℤ), but Lean typed n
                                Queries                                                                                      as ℕ — excludes negatives."
                                                                                                                             }
                           Abelian Subgroup
                                                              Retrieve
                                                                                                                     Else             Formalization
                           BooleanRing
                                                                                           Consistency Check
                                                   LeanExplore                                                                   ƒ(x) theorem ...:= by sorry
                           Left Coset                                                                          All Pass ?




                 4. Trajectory Reconstruction                                        5. Training
                                                                                                  SFT          RL
                                                                Reasoning
                                                                                                                                                  MathForm-8B
                   theorem ...:= by sorry
                                               Synthesis
                                                                         Decontamination




Figure 2: Overview of the M ATH F ORM data construction and training pipeline. The system combines Mathlib
knowledge retrieval, compilation and semantic verification, and iterative refinement to generate reliable formal
data, followed by trajectory reconstruction and training of M ATH F ORM-8B.


larger specialized autoformalizers on several challenging test sets (Figure 1). Ablations further show that
knowledge retrieval, automated verification, and reinforcement learning each contribute to this result.
In summary, our main contributions are as follows:

       • We introduce M ATH F ORM, a knowledge-augmented autoformalization framework that combines
         retrieval planning with compiler- and semantics-guided iterative refinement, enabling reliable natural-
         language-to-Lean data construction beyond reliance on parametric memory.
       • We construct F ORMALV ERSE, a large-scale Lean 4 autoformalization dataset containing approxi-
         mately 367K verified examples across diverse data sources, mathematical domains, and problem
         types.
       • Using a straightforward training recipe consisting solely of SFT and RL, we train M ATH F ORM-8B,
         which achieves average pass rates of 88.06% under Syntax Check and 72.37% under Consistency
         Check across six benchmarks, outperforming multiple specialized 32B autoformalizers.


2     Related Work
2.1    Autoformalization
Autoformalization aims to translate mathematical problems expressed in natural language into machine-
verifiable formal code, and constitutes a key subtask in formal theorem proving. Whereas early rule-based
methods were limited in both accuracy and coverage, recent research has shifted toward LLM-based ap-
proaches to autoformalization. Systems such as TheoremLlama (Wang et al., 2024), Herald (Gao et al.,
2025), Kimina-Autoformalizer (Wang et al., 2025), and Mathesis (Xuejun et al., 2026) train end-to-end
natural-language-to-formal-language (NL-to-FL) autoformalization models. Subsequent systems, including
StepFun-Formalizer (Wu et al., 2025), Goedel-Formalizer-V2 (Lin et al., 2025), ATF (Guo et al., 2025b),
and ReForm (Chen et al., 2026), incorporate verifier feedback to train autoformalizers capable of explicit
reasoning and refinement. Meanwhile, RAutoformalizer (Liu et al., 2025), DRIFT (Zhang et al., 2026), and
Aria (Wang et al., 2026a) explore retrieval-augmented frameworks for autoformalization. These retrieval-
centric approaches, however, primarily target per-instance formalization at inference time and have not been
designed for large-scale, end-to-end autoformalization data construction.


                                                                                   –3–
MathForm

                                   Textbook
                                       0.2%
                         Principia-Collection
                                        4.5%
                              OpenR1-Math
                                     7.2%                                   Lean-Workbook
                                                                            32.8%
                           AceReason-Math
                                     7.8%
                                                  FormalVerse
                                                      367K
                              DeepTheorem
                                    10.1%




                                  DeepMath
                                     11.4%                                  NuminaMath
                                                                            26.0%


              Figure 3: Distribution of natural-language problem sources in F ORMALV ERSE.


2.2     Datasets for Formal Mathematical Reasoning
High-quality formal data have long remained a scarce resource for research on formal mathematical reasoning.
MiniF2F (Zheng et al., 2022) and ProofNet (Azerbayev et al., 2023) formalize Olympiad-level problems
and undergraduate mathematical theorems as Lean statements, providing important benchmarks for autofor-
malization and formal theorem proving. More recently, CombiBench (Liu et al., 2026), FATE (Jiang et al.,
2026), and MA-ProofBench (Pu et al., 2026) extend formal evaluation to combinatorics, abstract algebra, and
mathematical analysis, domains that earlier benchmarks cover only sparsely. LeanDojo (Yang et al., 2023)
subsequently introduced an interactive Lean proving environment built upon Mathlib. More recent efforts
have constructed large-scale Lean 4 datasets for model training, including Lean Workbook (Ying et al., 2024),
Lean-GitHub (Wu et al., 2024), NuminaMath-LEAN (Wang et al., 2025), and FineLeanCorpus (Peng et al.,
2026). However, their semantic quality and domain coverage remain limited. Our approach instead combines
efficient knowledge augmentation, automated verification, and iterative refinement to construct higher-quality
formal data and thereby improve model autoformalization capabilities.

3     Method
This section presents the data construction framework and model training procedure of M ATH F ORM. As
illustrated in Figure 2, Section 3.1 describes the data construction framework, covering problem collection
and normalization, knowledge retrieval and formalization generation, verification-guided iterative refinement,
and trajectory reconstruction followed by data decontamination. Section 3.2 then presents the training of
M ATH F ORM-8B.

3.1     Autoformalization Framework
3.1.1   Problem Collection and Normalization
We first collect candidate problems from a diverse set of natural-language mathematics datasets, including
DeepTheorem (Zhang et al., 2025), NuminaMath (Li et al., 2024), AceReason-Math (Chen et al., 2025),
Lean Workbook (Ying et al., 2024), Principia-Collection (Aggarwal et al., 2026), DeepMath (He et al.,
2026), and OpenR1-Math (Hugging Face, 2025), and further supplement them with theorems and exercises
drawn from classical mathematics textbooks. We then filter out non-mathematical content, purely numerical
computation exercises, and problems that cannot be naturally expressed as theorem statements. Problems
containing redundant answer-format instructions or extraneous context are rewritten, giving a normalized pool
of natural-language problems. Figure 3 shows the source composition of the final F ORMALV ERSE dataset.

3.1.2   Knowledge Retrieval and Formalization Generation
We build a knowledge-augmented autoformalization pipeline composed of a Retrieval Planner and a Formal-
ization Generator. To keep inference fast and inexpensive, we use gpt-oss-120b (OpenAI, 2025) to drive both
modules. Given a natural-language mathematical statement, the retrieval planner analyzes the mathematical
objects, relations, and type constraints it involves, and judges whether additional Mathlib knowledge is needed.
When this is the case, the planner issues a few targeted queries for the key concepts and collects relevant
definitions, theorems, notations, and existing formalizations from Mathlib through LeanExplore (Asher, 2025),


                                                     –4–
MathForm


                                                         254K               100.0%
                                                  250             89.0%               100




                      New samples per round (K)




                                                                                            Cumulative coverage (%)
                                                  200   69.2%                         80

                                                  150                                 60

                                                  100                                 40
                                                                   73K

                                                   50                        40K
                                                                                      20

                                                    0                                 0
                                                        Round 1   Round 2   Round 3




Figure 4: Numbers of natural-language-to-formal-language pairs accepted in successive refinement rounds.
Later rounds contribute an additional 31.0% of all retained pairs.


which is set to return the top-2 results per query. The formalization generator then conditions on both the
original statement and these retrieved results, identifies the corresponding Mathlib types and definitions, and
produces the Lean 4 formal statement. Separating retrieval planning from code generation allows the pipeline
to draw on library knowledge only where it is needed, which reduces its reliance on parametric memory and
improves agreement with canonical Mathlib representations.
3.1.3   Verification-Guided Iterative Refinement
Given a natural-language statement, the retrieved context, and feedback from any previous failed attempt, the
formalization generator produces a candidate Lean 4 formalization. A Format Check first discards outputs
containing proof steps, tactics, solution procedures, or other content beyond the formal statement itself. The
remaining candidates are then compiled with Lean 4. Compilation failures are recorded with the corresponding
compiler diagnostics, which identify issues such as syntax errors, undeclared identifiers, missing dependencies,
or type mismatches.
Successfully compiled candidates then undergo a semantic consistency check that assesses whether the gen-
erated Lean 4 statement faithfully captures the semantics of the original natural-language statement, with
QwQ-32B (Qwen Team, 2025) serving as the judge. This check flags errors such as omitted assumptions,
strengthened or weakened conditions, incorrect quantifier order, extraneous constraints, inappropriate math-
ematical objects, and mismatched conclusions. A sample that fails either check proceeds to the next round
together with the corresponding feedback, and Mathlib retrieval is re-triggered when additional context is
needed. Each sample undergoes at most three rounds, and generation stops as soon as a candidate passes both
checks; samples that never pass are discarded. This adaptive, failure-driven schedule concentrates additional
computation on unresolved cases. Whereas Best-of-N spends a fixed budget on independent samples, M ATH -
F ORM turns verification signals into corrective guidance rather than using them only for post-hoc selection. As
shown in Figure 4, the first round yields about 69% of all retained pairs, and the second and third rounds add
roughly 20% and 11%, respectively. Later rounds therefore recover 31% of the data that single-pass generation
alone would not have produced. A worked example is provided in Appendix C.1.
3.1.4   Trajectory Reconstruction
The preceding pipeline produces a large collection of verified natural-language-to-formal-language (NL-FL)
pairs. However, the trajectories that produced these pairs span multiple rounds and interleave retrieved context,
compiler errors, semantic feedback, and failed attempts, which makes them unsuitable as training targets. The
native reasoning traces of the model are also unnecessarily verbose: even when the prompt asks only for a
formal statement, it sometimes deliberates repeatedly over whether to produce a proof or attempts to solve the
problem outright. This behavior likely reflects the fact that reasoning models are trained predominantly to
prove or solve mathematical problems rather than to formalize them. We therefore retrospectively synthesize
a clean, structured formalization trajectory for each verified pair. Specifically, given a natural-language
mathematical statement and its Lean 4 formalization, we ask the model to reconstruct the intermediate analysis
that maps one to the other, while explicitly excluding proof strategies, tactic selection, and problem-solving


                                                                  –5–
MathForm


procedures. Each resulting training example thus consists of a natural-language statement, a formalization
trajectory, and verified Lean 4 code. The trajectory reconstruction prompt is provided in Appendix D.

3.1.5   Data Decontamination
Finally, we decontaminate the training data against all evaluation benchmarks used in Section 4, removing
any training example that shares at least one 13-gram with an evaluation example. The resulting dataset,
F ORMALV ERSE, contains approximately 367K verified NL-FL pairs.

3.2     Training M ATH F ORM-8B
3.2.1   Supervised Fine-Tuning
We perform supervised fine-tuning on Qwen3-8B (Yang et al., 2025) with F ORMALV ERSE using the LLaMA-
Factory framework (Zheng et al., 2024), training the model to identify mathematical objects, logical structures,
variable dependencies, and implicit type constraints in natural-language statements and to generate the
corresponding Lean 4 formalizations. This stage yields M ATH F ORM-8B-SFT, which already exhibits strong
formalization ability and serves as the initialization for subsequent reinforcement learning.

3.2.2   RL Data Selection
The RL data are drawn from statements that never passed validation during iterative refinement, that is,
the problems left unsolved by the construction pipeline. We sample approximately 20,000 such candidates.
We then apply offline difficulty filtering, keeping statements that are hard enough to provide informative
optimization signals yet remain within reach of M ATH F ORM-8B-SFT. Statements whose phrasing admits
multiple reasonable formalizations are also removed so that the binary reward remains well defined. This
procedure yields an RL dataset of 3,000 examples.

3.2.3   Reward Function
After supervised fine-tuning, we further optimize M ATH F ORM-8B-SFT with Decoupled Clip and Dynamic
sAmpling Policy Optimization (DAPO) (Yu et al., 2025a) using the verl framework (Sheng et al., 2025). For
each natural-language statement x, we sample G candidate formalizations {yi }G         i=1 from the previous policy
πθold and optimize the following token-level objective:
                                             |yi |
                            "             G X
                                                                                                       #
                                 1       X                                                          
           JDAPO (θ) = E PG                        min ρi,t Ai , clip(ρi,t , 1 − ϵlow , 1 + ϵhigh )Ai .         (1)
                               i=1 |yi | i=1 t=1

Here, ρi,t denotes the token-level policy ratio and Ai the group-normalized advantage. We adopt Clip-Higher
and dynamic sampling, retaining only groups that contain both successful and unsuccessful candidates.
We use a binary reward that jointly considers compilation success and semantic consistency. Let C(y) denote
Lean 4 compilation success and S(x, y) denote the semantic-consistency judgment produced by gpt-oss-20b
for a compilable formalization. A candidate receives a positive reward only when both checks succeed:
                                           
                                             1, C(y) = 1 and S(x, y) = 1,
                                r(x, y) =                                                               (2)
                                             0, otherwise.
This reward directly aligns optimization with the two core objectives of autoformalization, namely compilability
and semantic fidelity. Full training details are provided in Appendix A.

4     Experiments
4.1     Experimental Settings
4.1.1   Benchmarks
We evaluate on six benchmarks: FormalMATH-Lite (Yu et al., 2025b), DeepSeek-ProverBench (Prover-
Bench) (Ren et al., 2025), CombiBench (Liu et al., 2026), and the recently introduced and highly challenging
FATE-M, FATE-H, and FATE-X (Jiang et al., 2026). Together, these benchmarks cover competition mathemat-
ics, combinatorics, and algebraic reasoning ranging from elementary abstract algebra to advanced commutative
algebra, homological algebra, and foundations of algebraic geometry.


                                                      –6–
MathForm


                                 AVG          FormalMATH      ProverBench     CombiBench       FATE-M          FATE-H          FATE-X
Model                          SC     CC       SC     CC       SC      CC      SC     CC       SC     CC       SC     CC      SC     CC
Specialized Autoformalizers
Herald Translator-7B          64.12   27.63   95.29   47.76   78.74   37.36   77.00    5.00   70.67   54.67   42.00   15.00   21.00 6.00
Kimina-Autoformalizer-7B      73.20   34.37   99.29   76.24   96.55   56.32   95.00   16.00   77.33   44.67   43.00    8.00   28.00 5.00
Mathesis-HPO-7B               76.20   34.96   99.06   79.29   97.13   59.77   96.00   15.00   84.00   48.67   50.00    4.00   31.00 3.00
StepFun-Formalizer-7B         58.12   39.55   97.41   81.41   89.66   59.20   79.00   28.00   60.67   52.67   17.00   12.00    5.00 4.00
StepFun-Formalizer-32B        63.65   44.47   99.06   85.88   92.53   64.94   86.00   32.00   71.33   60.00   23.00   17.00   10.00 7.00
Goedel-Formalizer-V2-8B       78.24   60.08   98.82   94.12   98.28   89.66   89.00   42.00   87.33   82.67   62.00   44.00   34.00 8.00
Goedel-Formalizer-V2-32B      78.28   63.74   99.06   94.59   98.28   92.53   91.00   49.00   89.33   85.33   63.00   48.00   29.00 13.00
ReForm-8B                     81.76   66.21   99.06   94.12   98.85   90.80   86.00   47.00   94.67   91.33   67.00   53.00   45.00 21.00
ReForm-32B                    81.61   68.41   99.06   95.53   98.28   94.25   93.00   55.00   91.33   88.67   69.00   52.00   39.00 25.00
Ours
M ATH F ORM-8B-SFT            84.38 66.53 99.29       91.06   100.00 90.80 83.00 43.00 98.00 91.33 80.00 58.00 46.00 25.00
M ATH F ORM-8B                88.06 72.37 100.00      95.06   100.00 94.83 93.00 47.00 99.33 97.33 82.00 63.00 54.00 37.00

Table 1: Pass@8 pass rates (%) under Syntax Check (SC) and Consistency Check (CC) for specialized
autoformalizers on six benchmarks. AVG is the equally weighted macro-average across all six benchmarks.
For each column, the best result is shown in bold and the second best is underlined.



4.1.2    Baselines
We compare M ATH F ORM-8B with a range of models, including specialized autoformalizers and general-
purpose LLMs. The specialized autoformalizers include Herald Translator-7B (Gao et al., 2025), Kimina-
Autoformalizer-7B (Wang et al., 2025), Mathesis-HPO-7B (Xuejun et al., 2026), StepFun-Formalizer-
7B/32B (Wu et al., 2025), Goedel-Formalizer-V2-8B/32B (Lin et al., 2025), and ReForm-8B/32B (Chen et al.,
2026). The general-purpose LLMs include DeepSeek-V4-Pro (DeepSeek-AI, 2026), Qwen3.7-Plus (Qwen
Team, 2026), Qwen3-8B/32B/235B-A22B-Thinking-2507 (Yang et al., 2025), and DeepSeek-R1-0528-Qwen3-
8B (Guo et al., 2025a); their complete results are reported in Appendix Table 7. Table 1 focuses on specialized
autoformalizers to directly compare task-specific capabilities across model scales and training strategies.

4.1.3    Evaluation
We report Pass@k rates (Chen et al., 2021) under two criteria: Syntax Check (SC) and Consistency Check
(CC). For a source statement x and its k candidate formalizations {yi }ki=1 , let C(yi ) be the binary indicator of
compilation success and S(x, yi ) the binary indicator of semantic consistency. The per-instance pass indicators
under the two criteria are defined as
                                               SC@k(x) = max C(yi ),
                                                               1≤i≤k
                                                                                                                                      (3)
                                               CC@k(x) = max C(yi )S(x, yi ).
                                                               1≤i≤k

Here, S is evaluated only for candidates that compile successfully; the final SC and CC pass rates are obtained
by averaging the corresponding indicators over all test instances. At inference time, we set k = 8 and
sample candidate formalizations for each test statement with a temperature of 0.6. For compilation validation,
we use Kimina Lean Server (Santos et al., 2025) as the Lean 4 backend to support efficient, large-scale
checking of formal code. For semantic-consistency evaluation, we adopt an LLM-as-a-Judge protocol, with
gpt-oss-120b serving as the judge under the high reasoning-effort setting. The complete semantic consistency
check prompt and the per-model inference prompts are provided in Appendix D. To assess the robustness
of semantic-consistency evaluation, we further compare multiple judge models in our subsequent analysis
(Table 4).

4.2     Main Results
4.2.1    An 8B Model Surpasses 32B Specialized Autoformalizers
As shown in Table 1, M ATH F ORM-8B achieves the best average SC and CC pass rates among specialized
autoformalizers, reaching 88.06% and 72.37%, respectively. Compared with the strongest specialized baseline,
ReForm-32B (81.61/68.41), these results represent absolute gains of 6.45 and 3.96 percentage points. Part
of this margin comes from the RL stage: relative to M ATH F ORM-8B-SFT, reinforcement learning raises the
average SC pass rate from 84.38% to 88.06% and the average CC pass rate from 66.53% to 72.37%. The
larger CC gain indicates that verification-driven reinforcement learning improves semantic alignment beyond


                                                                –7–
MathForm


                                     0.60
                                                     Raw         EMA                       0.44          mean@3




                   Training reward
                                     0.50                                                  0.40




                                                                                Accuracy
                                                                                           0.36

                                     0.40                                                  0.32

                                                                                           0.28
                                     0.30
                                            0              200            400                     0             200           400
                                                     Training step                                          Training step

Figure 5: Training dynamics during reinforcement learning. The left panel shows the training reward and its
exponential moving average (EMA), while the right panel reports the Mean@3 pass rate on FATE-H over the
course of training.

                                                     AVG                 FATE-M                         FATE-H                FATE-X
            Method                              SC         CC           SC           CC                SC        CC          SC     CC
            gpt-oss-120b
            Single                          27.33          26.43       52.00      51.30               21.00     19.00        9.00    9.00
            BoN                             42.67          41.10       70.00      69.30               40.00     37.00       18.00   17.00
            Feedback                        42.57          40.77       68.70      67.30               41.00     38.00       18.00   17.00
            Retrieval                       32.23          29.00       56.70      52.00               27.00     26.00       13.00   9.00
            M ATH F ORM                     49.67          48.00       76.00      74.00               46.00     44.00       27.00   26.00
            Qwen3-235B-A22B-Thinking-2507
            Single         7.43     7.43                               13.30      13.30                5.00      5.00       4.00    4.00
            BoN           18.77    18.77                               33.30      33.30               14.00     14.00       9.00    9.00
            Feedback      28.77    28.77                               51.30      51.30               22.00     22.00       13.00   13.00
            Retrieval      9.90     8.57                               16.70      16.70                8.00      6.00       5.00    3.00
            M ATH F ORM   37.57    36.23                               60.70      58.70               32.00     31.00       20.00   19.00

Table 2: Ablation results for SC and CC pass rates (%) of the refinement pipeline with two generators on the
FATE series. Single denotes single-pass generation; BoN denotes Best-of-N ; Feedback denotes feedback-only
iteration; and Retrieval denotes retrieval-only single-pass generation. AVG is the equally weighted average
over FATE-M, FATE-H, and FATE-X.



compilability. Human evaluation on FATE-M and FATE-H confirms this ranking, where M ATH F ORM-8B
achieves the highest SC and human-assessed CC pass rates among all compared models (Appendix Table 8).

4.2.2   Gains Concentrate on High-Abstraction Statements
On the relatively mature FormalMATH-Lite and ProverBench benchmarks, specialized models perform
comparably, and M ATH F ORM-8B is on par with or slightly better than the strongest baseline. On CombiBench,
M ATH F ORM-8B matches ReForm-8B in CC. The separation emerges on the FATE series: M ATH F ORM-8B
attains CC pass rates of 97.33%, 63.00%, and 37.00% on FATE-M, FATE-H, and FATE-X, exceeding the
strongest specialized baseline on each subset by 6, 10, and 12 percentage points, with the advantage widening as
the abstraction level increases. Advanced algebra is precisely where formalization depends most on Mathlib’s
type hierarchy and existing formalizations, and this distribution of gains is consistent with the knowledge
retrieval and verification-guided iterative refinement that underlie the construction of F ORMALV ERSE. A
representative case is provided in Appendix C.2.

4.3     Further Analysis
4.3.1   Training Dynamics
During training, we track the pass rate on the challenging FATE-H benchmark using Mean@3, the fraction of
candidates passing the Consistency Check among three samples per statement, averaged over the benchmark.


                                                                               –8–
MathForm


                       AVG      FormalMATH ProverBench CombiBench              FATE-M        FATE-H    FATE-X
Training Dataset     SC    CC     SC     CC     SC     CC     SC     CC     SC     CC        SC   CC   SC   CC
NuminaMath-LEAN 66.24 41.49 99.53 85.18 96.55 72.41 87.00 25.00 69.33 49.33 35.00 16.00 10.00 1.00
FineLeanCorpus  78.25 46.53 100.00 84.47 98.85 74.71 96.00 29.00 90.67 68.00 53.00 17.00 31.00 6.00
F ORMALV ERSE   77.17 60.32 98.82 90.59 98.85 89.66 78.00 36.00 95.33 84.67 62.00 46.00 30.00 15.00

Table 3: Pass@8 SC and CC pass rates (%) of models trained on different datasets across six benchmarks. All
models are initialized from Qwen3-8B and trained on 100K examples under the same trajectory reconstruction
and training configuration. AVG is the equally weighted macro-average across all six benchmarks. The best
result in each column is shown in bold and the second best is underlined.


                       Judge Model       Accuracy      Precision      Recall            F1
                       gpt-oss-120b         0.8917         0.8755     0.9133      0.8940
                       QwQ-32B              0.8567         0.8367     0.8867      0.8609
                       gpt-oss-20b          0.8500         0.8142     0.9067      0.8579

    Table 4: Judge-model reliability on the human-annotated semantic-consistency test set (Mean@3).



As shown in Figure 5, the average reward increases steadily throughout training, indicating that the model
progressively learns to generate formalizations satisfying both compilation success and semantic consistency.
Meanwhile, Mean@3 on FATE-H improves from 0.30 to about 0.40, corresponding to an approximately 33%
relative gain. The close agreement between the reward curve and the FATE-H pass rate suggests that the
proposed verification-driven reward reliably reflects actual autoformalization performance and provides an
effective learning signal.

4.3.2   Ablation Study of the Refinement Pipeline
To quantify the contributions of knowledge retrieval and verification-guided iterative refinement, we compare
five generation configurations on FATE-M, FATE-H, and FATE-X: single-pass generation, budget-matched
Best-of-N independent sampling with N = 3, feedback-only iteration without retrieval, retrieval-only single-
pass generation, and the complete M ATH F ORM pipeline. We conduct the experiments with both gpt-oss-120b
and Qwen3-235B-A22B-Thinking-2507, the latter belonging to a different model family. The ablation results
for both generators are reported in Table 2. For both generators, the complete M ATH F ORM pipeline achieves
the best SC and CC pass rates across all FATE difficulty levels, indicating that its effectiveness is not tied
to a particular generator. Relative to single-pass generation, M ATH F ORM improves the average SC pass
rate from 27.33% to 49.67% for gpt-oss-120b (+22.34 percentage points) and from 7.43% to 37.57% for
the Qwen3-235B generator (+30.14 percentage points). More importantly, compared with the strongest
single-component configuration among retrieval, feedback iteration, and budget-matched sampling, the full
pipeline yields additional gains of 7.00/6.90 and 8.80/7.46 percentage points in SC/CC pass rates for the
two generators, respectively. These consistent cross-model gains demonstrate that knowledge retrieval and
verification-guided refinement are complementary and jointly improve the autoformalization quality of the
data construction pipeline.

4.3.3   Data Quality of FormalVerse
To isolate the effect of training-data quality, we compare F ORMALV ERSE with two recently released large-
scale Lean 4 datasets, NuminaMath-LEAN (Wang et al., 2025) and FineLeanCorpus (Peng et al., 2026).
We randomly sample 100K examples from each, apply the same trajectory-reconstruction procedure to all
three subsets, and use each resulting dataset to fine-tune Qwen3-8B under an identical training configuration.
The resulting models are evaluated on all six benchmarks using the same Pass@8 protocol. Under this
controlled setting (Table 3), F ORMALV ERSE attains the highest average CC pass rate of 60.32%, exceeding
FineLeanCorpus by 13.79 and NuminaMath-LEAN by 18.83 percentage points, and ranks first in CC on
every benchmark. Its SC pass rate (77.17%), by contrast, is comparable to that of FineLeanCorpus (78.25%),
so the difference between the two corpora lies almost entirely in semantic fidelity rather than compilability.
This is the dimension that matters for autoformalization, since a statement that compiles but misstates the
source proposition is of little use downstream, and it is precisely what the verification-guided construction of
F ORMALV ERSE targets.


                                                     –9–
MathForm


4.3.4   Reliability of Semantic Consistency Judgment
To evaluate the reliability of judge models for semantic-consistency assessment, we construct an independent,
human-annotated test set. Specifically, we collect both accepted and rejected NL-FL pairs from the data
construction stage and have human experts independently relabel them, resulting in a test set of 200 examples.
We evaluate the gpt-oss-120b judge used in our main evaluation against QwQ-32B and gpt-oss-20b on this
test set. Accuracy, precision, recall, and F1, each averaged over three independent judging runs (Mean@3),
are reported in Table 4. The gpt-oss-120b judge achieves the best results across all four metrics. QwQ-32B
attains an F1 score of 0.8609 and exhibits strong discriminative ability; because it belongs to a different model
family from the gpt-oss models used for generation and reward evaluation, we use it during data construction
to reduce the self-preference bias that can arise when the generator and the judge come from the same model
family. Although gpt-oss-20b is smaller, its precision approaches that of QwQ-32B, its recall is higher, and its
inference is faster, making it better suited for reward computation during reinforcement learning.

5   Conclusion
We introduced M ATH F ORM, an autoformalization framework that combines knowledge retrieval with iterative
refinement guided by compilation and semantic signals. Using this framework, we constructed F ORMAL -
V ERSE, a dataset of approximately 367K verified Lean 4 examples, and trained M ATH F ORM-8B through
SFT and RL. Across six benchmarks, M ATH F ORM-8B achieves average SC and CC pass rates of 88.06%
and 72.37%, respectively, outperforming multiple specialized 32B autoformalizers and obtaining strong
results on challenging FATE subsets. Overall, the results validate the effectiveness of knowledge retrieval and
verification-guided iterative refinement for autoformalization data construction, and show that high-quality
training data can support competitive autoformalization performance in a compact model. In future work,
we plan to explore larger-scale test-time scaling methods to further strengthen formalization on complex
problems.

References
Pranjal Aggarwal, Marjan Ghazvininejad, Seungone Kim, Ilia Kulikov, Jack Lanchantin, Xian Li, Tianjian Li,
  Bo Liu, Graham Neubig, Anaelia Ovalle, Swarnadeep Saha, Sainbayar Sukhbaatar, Sean Welleck, Jason
  Weston, Chenxi Whitehouse, Adina Williams, Jing Xu, Ping Yu, Weizhe Yuan, Jingyu Zhang, and Wenting
  Zhao. Reasoning over mathematical objects: on-policy reward modeling and test time aggregation, 2026.
  URL https://arxiv.org/abs/2603.18886.
Justin Asher. Leanexplore: A search engine for lean 4 declarations, 2025. URL https://arxiv.org/abs/
  2506.11085.

Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W. Ayers, Dragomir Radev, and Jeremy
  Avigad. Proofnet: Autoformalizing and formally proving undergraduate-level mathematics, 2023. URL
  https://arxiv.org/abs/2302.12433.

Guoxin Chen, Jing Wu, Xinjie Chen, Wayne Xin Zhao, Ruihua Song, Chengxi Li, Kai Fan, Dayiheng Liu,
  and Minpeng Liao. Reform: Reflective autoformalization with prospective bounded sequence optimization,
  2026. URL https://arxiv.org/abs/2510.24592.
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri
 Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael
 Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov,
 Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such,
 Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen
 Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain,
 William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan
 Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder,
 Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba. Evaluating large
 language models trained on code, 2021. URL https://arxiv.org/abs/2107.03374.
Yang Chen, Zhuolin Yang, Zihan Liu, Chankyu Lee, Peng Xu, Mohammad Shoeybi, Bryan Catanzaro, and
  Wei Ping. Acereason-nemotron: Advancing math and code reasoning through reinforcement learning.
  In The Thirty-ninth Annual Conference on Neural Information Processing Systems, 2025. URL https:
  //openreview.net/forum?id=EgArbnS0BA.


                                                    – 10 –
MathForm


DeepSeek-AI. Deepseek-v4: Towards highly efficient million-token context intelligence, 2026. URL https:
  //arxiv.org/abs/2606.19348.

Guoxiong Gao, Yutong Wang, Jiedong Jiang, Qi Gao, Zihan Qin, Tianyi Xu, and Bin Dong. Herald: A natural
  language annotated lean 4 dataset, 2025. URL https://arxiv.org/abs/2410.10878.
Daya Guo et al. Deepseek-r1 incentivizes reasoning in llms through reinforcement learning. Nature, 645
  (8081):633–638, 2025a. ISSN 1476-4687. doi: 10.1038/s41586-025-09422-z. URL http://dx.doi.org/
  10.1038/s41586-025-09422-z.

Qi Guo, Jianing Wang, Jianfei Zhang, Deyang Kong, Xiangzhou Huang, Xiangyu Xi, Wei Wang, Jingang
  Wang, Xunliang Cai, Shikun Zhang, and Wei Ye. Autoformalizer with tool feedback, 2025b. URL
  https://arxiv.org/abs/2510.06857.

Zhiwei He, Tian Liang, Jiahao Xu, Qiuzhi Liu, Xingyu Chen, Yue Wang, Linfeng Song, Dian Yu, Zhenwen
  Liang, Wenxuan Wang, Zhuosheng Zhang, Rui Wang, Zhaopeng Tu, Haitao Mi, and Dong Yu. Deepmath-
  103k: A large-scale, challenging, decontaminated, and verifiable mathematical dataset for advancing
  reasoning. In The Fourteenth International Conference on Learning Representations, 2026. URL https:
  //openreview.net/forum?id=kHB5Te5IWm.

Thomas Hubert, Rishi Mehta, Laurent Sartran, Miklós Z Horváth, Goran Žužić, Eric Wieser, Aja Huang,
  Julian Schrittwieser, Yannick Schroecker, Hussain Masoom, et al. Olympiad-level formal mathematical
  reasoning with reinforcement learning. Nature, 651(8106):607–613, 2026.
Hugging Face. Open r1: A fully open reproduction of deepseek-r1, January 2025. URL https://github.
  com/huggingface/open-r1.

Jiedong Jiang, Wanyi He, Wang Yuefeng, Guoxiong Gao, Yongle Hu, Jingting Wang, Nailin Guan, Peihao Wu,
   Bryan Dai, Liang Xiao, and Bin Dong. FATE: A formal benchmark series for frontier algebra of multiple
   difficulty levels. In The Fourteenth International Conference on Learning Representations, 2026. URL
   https://openreview.net/forum?id=3bD19r4jqh.

Jia Li, Edward Beeching, Lewis Tunstall, Ben Lipkin, Roman Soletskyi, Shengyi Huang, Kashif Rasul,
   Longhui Yu, Albert Q Jiang, Ziju Shen, et al. Numinamath: The largest public dataset in ai4maths with
   860k pairs of competition math problems and solutions. Hugging Face repository, 13(9):9, 2024.
Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu Zhao, Lai Jiang, Yihan Geng, Jiawei
  Ge, Jingruo Sun, Jiayun Wu, Jiri Gesi, Ximing Lu, David Acuna, Kaiyu Yang, Hongzhou Lin, Yejin Choi,
  Danqi Chen, Sanjeev Arora, and Chi Jin. Goedel-prover-v2: Scaling formal theorem proving with scaffolded
  data synthesis and self-correction, 2025. URL https://arxiv.org/abs/2508.03613.
Junqi Liu, Xiaohan Lin, Bolton Bailey, Jonas Bayer, Yaël Dillies, Weijie Jiang, Xiaodan Liang, Roman
  Soletskyi, Haiming Wang, Yunzhou Xie, Beibei Xiong, Zhengfeng Yang, Jujian Zhang, Lihong Zhi,
  Zekai Zhu, Jia LI, and Zhengying Liu. Combibench: Benchmarking LLM capability for combinatorial
  mathematics. In 3rd AI for Math Workshop: Toward Self-Evolving Scientific Agents, 2026. URL https:
  //openreview.net/forum?id=qeZStJVYnc.

Qi Liu, Xinhao Zheng, Xudong Lu, Qinxiang Cao, and Junchi Yan. Rethinking and improving autoformaliza-
  tion: Towards a faithful metric and a dependency retrieval-based approach. In The Thirteenth International
  Conference on Learning Representations, 2025. URL https://openreview.net/forum?id=hUb2At2DsQ.
The mathlib Community. The lean mathematical library. In Proceedings of the 9th ACM SIGPLAN Interna-
  tional Conference on Certified Programs and Proofs, POPL ’20, pp. 367–381. ACM, January 2020. doi:
  10.1145/3372885.3373824. URL http://dx.doi.org/10.1145/3372885.3373824.
Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming language. In
  International Conference on Automated Deduction, pp. 625–635. Springer, 2021.
OpenAI. gpt-oss-120b & gpt-oss-20b model card, 2025. URL https://arxiv.org/abs/2508.10925.
Zhongyuan Peng, Yifan Yao, Kaijing Ma, Shuyue Guo, Yizhe Li, Yichi Zhang, Chenchen Zhang, Yifan
  Zhang, Zhouliang Yu, Luming Li, Minghao Liu, Yihang Xia, Jiawei Shen, Yuchen Wu, Yixin Cao,
  Zhaoxiang Zhang, Wenhao Huang, Jiaheng Liu, and Ge Zhang. CriticLean: Critic-guided reinforcement


                                                  – 11 –
MathForm


  learning for mathematical formalization. In Maria Liakata, Viviane P. Moreira, Jiajun Zhang, and David
  Jurgens (eds.), Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics
  (Volume 1: Long Papers), pp. 3049–3088, San Diego, California, United States, July 2026. Association
  for Computational Linguistics. ISBN 979-8-89176-390-6. doi: 10.18653/v1/2026.acl-long.139. URL
  https://aclanthology.org/2026.acl-long.139/.

Lushi Pu, Weiming Zhang, Xinheng Xie, Zixuan Fu, Bingxiang He, Hongya Lyu, Xin Li, Jie Zhou, and
  Yudong Wang. Ma-proofbench: A two-tiered evaluation of llms for theorem proving in mathematical
  analysis, 2026. URL https://arxiv.org/abs/2606.13782.

Qwen Team. Qwq-32b: Embracing the power of reinforcement learning, March 2025. URL https://qwenlm.
 github.io/blog/qwq-32b/.

Qwen Team. Qwen3.7-Plus: Multimodal agent intelligence, May 2026. URL https://qwen.ai/blog?id=
 qwen3.7-plus.

Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe
  Fu, Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shirong Ma, Hongxuan Tang, Yuxuan Liu, Wenjun
  Gao, Daya Guo, and Chong Ruan. Deepseek-prover-v2: Advancing formal mathematical reasoning via
  reinforcement learning for subgoal decomposition, 2025. URL https://arxiv.org/abs/2504.21801.

Marco Dos Santos, Hugues de Saxcé, Haiming Wang, Ran Wang, Mantas Baksys, Mert Unsal, Junqi Liu,
 Zhengying Liu, and Jia Li. Kimina lean server: A high-performance lean server for large-scale verification,
 2025. URL https://arxiv.org/abs/2504.21230.

Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin Wu, Wang Zhang, Ru Zhang, Yanghua Peng, Haibin
  Lin, and Chuan Wu. Hybridflow: A flexible and efficient rlhf framework. In Proceedings of the Twentieth
 European Conference on Computer Systems, EuroSys ’25, pp. 1279–1297. ACM, March 2025. doi:
 10.1145/3689031.3696075. URL http://dx.doi.org/10.1145/3689031.3696075.

Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas Baksys, Junqi Liu, Marco Dos Santos, Flood Sung, Marina
  Vinyes, Zhenzhe Ying, Zekai Zhu, Jianqiao Lu, Hugues de Saxcé, Bolton Bailey, Chendong Song, Chenjun
  Xiao, Dehao Zhang, Ebony Zhang, Frederick Pu, Han Zhu, Jiawei Liu, Jonas Bayer, Julien Michel, Longhui
  Yu, Léo Dreyfus-Schmidt, Lewis Tunstall, Luigi Pagani, Moreira Machado, Pauline Bourigault, Ran Wang,
  Stanislas Polu, Thibaut Barroyer, Wen-Ding Li, Yazhe Niu, Yann Fleureau, Yangyang Hu, Zhouliang Yu,
  Zihan Wang, Zhilin Yang, Zhengying Liu, and Jia Li. Kimina-prover preview: Towards large formal
  reasoning models with reinforcement learning, 2025. URL https://arxiv.org/abs/2504.11354.

Hanyu Wang, Ruohan Xie, Yutong Wang, Guoxiong Gao, Xintao Yu, and Bin Dong. Aria: An agent for retrieval
  and iterative auto-formalization via dependency graph, 2026a. URL https://arxiv.org/abs/2510.04520.

Ruida Wang, Jipeng Zhang, Yizhen Jia, Rui Pan, Shizhe Diao, Renjie Pi, and Tong Zhang. Theoremllama:
  Transforming general-purpose llms into lean4 experts, 2024. URL https://arxiv.org/abs/2407.03203.

Yudong Wang, Zixuan Fu, Hengyu Zhao, Chen Zhao, Chuyue Zhou, Xinle Lin, Hongya Lyu, Shuaikang Xue,
  Yi Yi, Yingjiao Wang, Zhi Zheng, Yuzhou Zhang, Jie Zhou, Chaojun Xiao, Xu Han, Zhiyuan Liu, and
  Maosong Sun. Data science and technology towards agi part i: Tiered data management, 2026b. URL
  https://arxiv.org/abs/2602.09003.

Yutong Wu, Di Huang, Ruosi Wan, Yue Peng, Shijie Shang, Chenrui Cao, Lei Qi, Rui Zhang, Zidong Du,
  Jie Yan, and Xing Hu. Stepfun-formalizer: Unlocking the autoformalization potential of llms through
  knowledge-reasoning fusion, 2025. URL https://arxiv.org/abs/2508.04440.

Zijian Wu, Jiayu Wang, Dahua Lin, and Kai Chen. Lean-github: Compiling github lean repositories for a
  versatile lean prover, 2024. URL https://arxiv.org/abs/2407.17227.

Yu Xuejun, Jianyuan Zhong, Zijin Feng, Pengyi Zhai, Roozbeh Yousefzadeh, Wei Chong Ng, Haoxiong Liu,
  Ziyi Shou, Jing Xiong, Yudong Zhou, Claudia Beth Ong, Austen Jeremy Sugiarto, Yaoxi Zhang, Wai Ming
  Tai, Huan Cao, Dongcai Lu, Jiacheng Sun, Qiang Xu, SHEN XIN, and Zhenguo Li. Mathesis: Towards
  formal theorem proving from natural languages. In The Fourteenth International Conference on Learning
  Representations, 2026. URL https://openreview.net/forum?id=CJdX82odge.


                                                  – 12 –
MathForm


An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao,
  Chengen Huang, Chenxu Lv, Chujie Zheng, Dayiheng Liu, Fan Zhou, Fei Huang, Feng Hu, Hao Ge, Haoran
 Wei, Huan Lin, Jialong Tang, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jing Zhou,
 Jingren Zhou, Junyang Lin, Kai Dang, Keqin Bao, Kexin Yang, Le Yu, Lianghao Deng, Mei Li, Mingfeng
 Xue, Mingze Li, Pei Zhang, Peng Wang, Qin Zhu, Rui Men, Ruize Gao, Shixuan Liu, Shuang Luo, Tianhao
  Li, Tianyi Tang, Wenbiao Yin, Xingzhang Ren, Xinyu Wang, Xinyu Zhang, Xuancheng Ren, Yang Fan,
 Yang Su, Yichang Zhang, Yinger Zhang, Yu Wan, Yuqiong Liu, Zekun Wang, Zeyu Cui, Zhenru Zhang,
  Zhipeng Zhou, and Zihan Qiu. Qwen3 technical report, 2025. URL https://arxiv.org/abs/2505.09388.
Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J
  Prenger, and Animashree Anandkumar. Leandojo: Theorem proving with retrieval-augmented language
  models. In A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt, and S. Levine (eds.), Advances
  in Neural Information Processing Systems, volume 36, pp. 21573–21612. Curran Associates, Inc., 2023.
  doi: 10.52202/075280-0944. URL https://proceedings.neurips.cc/paper_files/paper/2023/file/
  4441469427094f8873d0fecb0c4e1cee-Paper-Datasets_and_Benchmarks.pdf.
Huaiyuan Ying, Zijian Wu, Yihan Geng, Jiayu Wang, Dahua Lin, and Kai Chen. Lean workbook:
 A large-scale lean problem set formalized from natural language math problems. In A. Globerson,
  L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang (eds.), Advances in Neu-
  ral Information Processing Systems, volume 37, pp. 105848–105863. Curran Associates, Inc., 2024.
  doi: 10.52202/079017-3357. URL https://proceedings.neurips.cc/paper_files/paper/2024/file/
  bf236666a2cc5f3ae05d2e08485efc4c-Paper-Datasets_and_Benchmarks_Track.pdf.
Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan, Xiaochen Zuo, Yu Yue, Weinan Dai, Tiantian Fan,
  Gaohong Liu, juncai liu, LingJun Liu, Xin Liu, Haibin Lin, Zhiqi Lin, Bole Ma, Guangming Sheng,
  Yuxuan Tong, Chi Zhang, Mofan Zhang, Ru Zhang, Wang Zhang, Hang Zhu, Jinhua Zhu, Jiaze Chen,
  Jiangjie Chen, Chengyi Wang, Hongli Yu, Yuxuan Song, Xiangpeng Wei, Hao Zhou, Jingjing Liu, Wei-
  Ying Ma, Ya-Qin Zhang, Lin Yan, Yonghui Wu, and Mingxuan Wang. Dapo: An open-source llm
  reinforcement learning system at scale. In D. Belgrave, C. Zhang, H. Lin, R. Pascanu, P. Koniusz,
  M. Ghassemi, and N. Chen (eds.), Advances in Neural Information Processing Systems, volume 38, pp.
  113222–113244. Curran Associates, Inc., 2025a. URL https://proceedings.neurips.cc/paper_files/
  paper/2025/file/a4277440d50f1f15d2cb4c14f7e0c0d2-Paper-Conference.pdf.
Zhouliang Yu, Ruotian Peng, Keyi Ding, Yizhe Li, Zhongyuan Peng, Minghao Liu, Yifan Zhang, Zheng Yuan,
  Huajian Xin, Wenhao Huang, Yandong Wen, Ge Zhang, and Weiyang Liu. Formalmath: Benchmarking
  formal mathematical reasoning of large language models, 2025b. URL https://arxiv.org/abs/2505.
  02735.
Meiru Zhang, Philipp Borchert, Milan Gritta, and Gerasimos Lampouras. Drift: Decompose, retrieve, illustrate,
 then formalize theorems, 2026. URL https://arxiv.org/abs/2510.10815.
Ziyin Zhang, Jiahao Xu, Zhiwei He, Tian Liang, Qiuzhi Liu, Yansi Li, Linfeng Song, Zhenwen Liang,
  Zhuosheng Zhang, Rui Wang, Zhaopeng Tu, Haitao Mi, and Dong Yu. Deeptheorem: Advancing llm
  reasoning for theorem proving through natural language and reinforcement learning, 2025. URL https:
  //arxiv.org/abs/2505.23754.
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. minif2f: a cross-system benchmark for formal
  olympiad-level mathematics. In International Conference on Learning Representations, 2022. URL
  https://openreview.net/forum?id=9ZPegFuFTFv.
Yaowei Zheng, Richong Zhang, Junhao Zhang, Yanhan Ye, Zheyan Luo, Zhangchi Feng, and Yongqiang Ma.
  Llamafactory: Unified efficient fine-tuning of 100+ language models, 2024. URL https://arxiv.org/
  abs/2403.13372.




                                                   – 13 –
MathForm


A     Implementation Details
A.1     Category Distribution of F ORMALV ERSE
Figure 6 presents the category distribution of the natural-language mathematical problems in F ORMALV ERSE.
The dataset covers ten mathematical categories, including inequalities, algebra, geometry, arithmetic, calculus,
number theory, combinatorics, probability and statistics, and linear algebra. This composition covers a wide
variety of problem types, from competition mathematics to advanced topics, providing broad domain coverage
for training autoformalizers.

                               Inequalities                                                              29.7%
                                   Algebra                                             16.6%
                                 Geometry                                    11.4%
                                Arithmetic                               10.8%
                                  Calculus                               10.6%
                           Number Theory                           8.2%
                            Combinatorics                       6.0%
                    Probability & Statistics          2.7%
                                     Others          2.4%
                            Linear Algebra          1.6%

                                               0          20K          40K       60K       80K    100K    120K

      Figure 6: Category distribution of the natural-language mathematical problems in F ORMALV ERSE.


A.2     Training Hyperparameters
The hyperparameters used for supervised fine-tuning and RL are summarized in Tables 5 and 6, respectively.
Both training stages are conducted on 16 NVIDIA H100 80GB GPUs. All Lean compilation checks throughout
this work use Lean 4.21.0.

                                                                                 Hyperparameter                         Value
        Hyperparameter                         Value                             RL algorithm                         DAPO
        Maximum sequence length             16,384                               Learning rate                   1.0 × 10−6
        Global batch size                      128                               Clipping bounds (lower/upper)     0.8 / 1.28
                                                                                 Training batch size                       32
        Learning rate                  2.0 × 10−5
                                                                                 PPO mini-batch size                       32
        Epochs                                   3
                                                                                 PPO micro-batch size per GPU               2
        LR scheduler                       Cosine
                                                                                 Rollouts per prompt                        8
        Warmup ratio                           0.1
                                                                                 Rollout temperature                      1.0
        Precision                                  bf16
                                                                                 Maximum response length               8,192
                                                                                 KL regularization                  Disabled
 Table 5: Supervised fine-tuning hyperparameters.
                                                                                         Table 6: RL hyperparameters.



B     Additional Evaluation Results
B.1     Comparison with General-Purpose LLMs
Table 7 reports the complete results of general-purpose LLMs and M ATH F ORM-8B across all six benchmarks.
DeepSeek-V4-Pro is evaluated under the high reasoning-effort setting. M ATH F ORM-8B attains an average SC
pass rate of 88.06%, exceeding all evaluated general-purpose models, including the strongest, Qwen3.7-Plus
(86.33%); however, its average CC pass rate (72.37%) remains below Qwen3.7-Plus (83.38%) and DeepSeek-
V4-Pro (76.54%). These results highlight the capability–efficiency trade-off of M ATH F ORM-8B: task-specific
training yields strong compilability in an 8B model, while frontier general-purpose models retain an advantage
in semantic fidelity.


                                                                 – 14 –
MathForm


                                  AVG       FormalMATH ProverBench CombiBench         FATE-M       FATE-H    FATE-X
Model                           SC   CC      SC     CC      SC    CC    SC    CC      SC    CC     SC   CC   SC   CC
General-Purpose LLMs
DeepSeek-V4-Pro               78.34 76.54   97.88   96.24 94.83 93.68 85.00 81.00 87.33 87.33 70.00 68.00 35.00 33.00
Qwen3.7-Plus                  86.33 83.38   99.29   98.59 100.00 97.70 92.00 87.00 94.67 92.00 78.00 77.00 54.00 48.00
Qwen3-235B-A22B-Thinking-2507 58.94 55.37   91.29   88.24 81.03 75.29 59.00 50.00 71.33 70.67 32.00 30.00 19.00 18.00
Qwen3-32B                     43.07 36.55   80.94   72.94 61.49 50.00 43.00 27.00 46.00 43.33 20.00 19.00 7.00 7.00
DeepSeek-R1-0528-Qwen3-8B     47.28 37.65   72.24   61.18 52.30 40.23 36.00 15.00 36.00 30.00 4.00 4.00 4.00 1.00
Qwen3-8B                      27.25 17.06   61.88   42.12 37.93 27.59 29.00 7.00 26.67 22.67 4.00 3.00 4.00 0.00
Ours
M ATH F ORM-8B                 88.06 72.37 100.00 95.06 100.00 94.83 93.00 47.00 99.33 97.33 82.00 63.00 54.00 37.00

Table 7: Pass@8 SC and CC pass rates (%) of general-purpose LLMs and M ATH F ORM-8B across six
benchmarks. AVG is the equally weighted macro-average across all six benchmarks. The best result in each
column is shown in bold and the second best is underlined.



B.2     Human Evaluation
For each problem in FATE-M and FATE-H, we randomly sample one candidate from the eight formalizations
generated by each model and ask two human experts to assess whether it faithfully preserves the semantics
of the source statement; disagreements are resolved through discussion between the two experts. Table 8
summarizes the results.

                                                            FATE-M              FATE-H
                       Model                               SC          CC       SC          CC
                       StepFun-Formalizer-32B            42.67     36.00      16.00        12.00
                       Goedel-Formalizer-V2-32B          75.33     68.00      38.00        27.00
                       ReForm-32B                        78.67     74.00      50.00        41.00
                       M ATH F ORM-8B                    86.67     76.67      54.00        42.00

Table 8: Human-evaluation results (%) on FATE-M and FATE-H, based on one randomly sampled candidate
per problem. The best result in each column is shown in bold.


Human evaluation preserves the relative ordering of the models observed under automated evaluation. M ATH -
F ORM-8B attains the highest SC and CC pass rates on both FATE-M and FATE-H, reaching 86.67% and 76.67%
on FATE-M and 54.00% and 42.00% on FATE-H. These results indicate that the advantage of M ATH F ORM-8B
on the formalization of challenging statements is stable and also holds under human assessment.

C     Case Studies
C.1     Case Study of the Data Construction Pipeline
We provide a detailed case study of the refinement pipeline on a group-theoretic problem, recording the
retrieval queries and results, the generated code, and the feedback of both verification steps in each round.

        • Round 1. The retrieved results cover only the centralizer. Although the generated code compiles,
          the semantic consistency check finds that it formalizes “K is normal in G” rather than the intended
          statement that “K is normal in H,” thereby introducing a stronger assumption.
        • Round 2. Guided by the semantic feedback, the system issues an additional query about subgroup
          normality. The retrieved result clarifies the scope of the corresponding Mathlib definition, enabling
          the model to revise the condition so that it correctly states normality relative to H. The revised code
          passes both checks.

This example shows that targeted retrieval in response to verification feedback can supply the library knowledge
needed to correct a semantic deviation and guide the model toward a faithful formalization.



                                                         – 15 –
MathForm


 Case Study of the Data Construction Pipeline

 Natural-language statement
  Let G be a group and let K ⊆ H be subgroups of G with K ◁ H. If H ◁ G and CH (K) = 1, prove that H
 centralizes CG (K).

 Round 1

 Retrieval

 [1] Query: subgroup.centralizer definition
     Subgroup.centralizer      Mathlib/GroupTheory/Subgroup/Centralizer.lean:22
       def centralizer (s : Set G) : Subgroup G := { Submonoid.centralizer s with carrier := Set.
 centralizer s inv_mem’ := Set.inv_mem_centralizer }
       The ‘centralizer‘ of ‘s‘ is the subgroup of ‘g : G‘ commuting with every ‘h : s‘.
     Subgroup.center           Mathlib/GroupTheory/Subgroup/Center.lean:22
       def center : Subgroup G := { Submonoid.center G with carrier := Set.center G inv_mem’ :=
 Set.inv_mem_center }
       The center of a group ‘G‘ is the set of elements that commute with everything in ‘G‘

 Generated formalization

 import Mathlib.GroupTheory.Subgroup.Centralizer
 import Mathlib.GroupTheory.Subgroup.Basic

 open Subgroup

 variable {G : Type*} [Group G]

 theorem H_centralizes_CG_K
   {K H : Subgroup G}
   (hK_le_H : K ≤ H)                      -- `K ⊆ H`
   (hK_normal : K.Normal)                -- `K ◁ H`
   (hH_normal : H.Normal)                -- `H ◁ G`
   (hC_eq_one : (Subgroup.centralizer (K : Set G) ⊓ H) = ⊥) :
     H ≤ Subgroup.centralizer (Subgroup.centralizer (K : Set G) : Set G) := by sorry


 ✓ Compilation succeeded       ✗ Semantic consistency: incorrect

 The Lean code incorrectly states K.Normal for the normality of K, which implies K is normal in G, whereas the
 NL specifies K is normal in H (K ◁ H). All other aspects (centralizer conditions, H’s normality in G, and the
 conclusion) are correctly formalized.

 Round 2

 Retrieval

 [2] Query: normal subgroup of a subgroup definition
     Subgroup.Normal           Mathlib/Algebra/Group/Subgroup/Defs.lean:591
       structure Normal : Prop where conj_mem : ∀ n, n ∈ H → ∀ g : G, g * n * g−1 ∈ H
       A subgroup is normal if whenever ‘n ∈ H‘, then ‘g * n * g−1 ∈ H‘ for every ‘g : G‘
     commutator                Mathlib/GroupTheory/Abelianization.lean:37
       def commutator : Subgroup G := [[(⊤ : Subgroup G), ⊤]]
       The commutator subgroup of a group G is the normal subgroup generated by the commutators [
 p,q]=‘p*q*p−1 *q−1 ‘.

 Generated formalization

 import Mathlib.GroupTheory.Subgroup.Centralizer
 import Mathlib.GroupTheory.Subgroup.Basic

 open Subgroup




                                                    – 16 –
MathForm


  variable {G : Type*} [Group G]

  theorem H_centralizes_CG_K
    {K H : Subgroup G}
    (hK_le_H : K ≤ H)
    (hK_normal_in_H :
      ∀ g ∈ H, ∀ k ∈ K, g * k * g−1 ∈ K)
    (hH_normal : H.Normal)
    (hC_eq_bot : (Subgroup.centralizer (K : Set G) ⊓ H) = ⊥) :
      H ≤ Subgroup.centralizer (Subgroup.centralizer (K : Set G) : Set G) := by sorry


  ✓ Compilation succeeded        ✓ Semantic consistency: correct

  The Lean 4 code accurately formalizes the NL statement. The hypotheses correctly capture K being a subgroup of
  H, normality of K in H, normality of H in G, and the triviality of CH (K). All logical dependencies and quantifiers
  align between the NL and the code. No semantic mismatches detected.


C.2    Case Study of M ATH F ORM-8B
In this commutative-algebra case, the three 32B baselines all fail to compile for the same reason: they refer
to identifiers that do not exist in Mathlib, such as Frac or QuotField for the quotient field. M ATH F ORM-8B
maps the quotient field to FractionRing and expresses the existence of an isomorphism by wrapping a ring
equivalence in Nonempty, yielding a correct formalization.

 Case Study of a Commutative-Algebra Problem

  Natural-language statement
  Show that if R is a unique factorization domain whose quotient field is isomorphic to R, then R is isomorphic to R.

  M ATH F ORM-8B

  Model output

  <think>
  **Mathematical concept understanding**

  The natural-language statement talks about a *unique factorization domain* R whose *quotient
  field* (i.e. fraction field) is isomorphic to the real numbers R. The goal is to deduce that the
   ring R itself is isomorphic to R.

  The objects that appear are:
  - A commutative ring R that is an integral domain and satisfies the unique factorisation
  property.
  - The fraction field FractionRing R, which is the field of fractions of R.
  - A field isomorphism (ring equivalence) between FractionRing R and R.
  - A ring equivalence between R and R.

  No ambiguity remains once we interpret "quotient field" as the standard fraction field
  construction and "isomorphic to R" as a field isomorphism. The implicit conventions are:
  - R is the real field, denoted ‘R‘ in Lean.
  - The isomorphism between fields is a *ring equivalence* (type ‘≃+*‘).

  **Logical structure analysis**

  The statement is a universal implication:
  ∀R (UFD R) (FractionRing R ∼
                             = R) =⇒ R ∼  = R.
  Formally we have:
  - Hypothesis ‘hK : (FractionRing R) ≃+* R‘.
  - Conclusion ‘Nonempty (R ≃+* R)‘.

  Thus the theorem is a single implication with a single hypothesis and a single conclusion.



                                                       – 17 –
MathForm



 **Formalization strategy**

 *Types for the objects*
 - ‘R‘ must be a type equipped with ‘[CommRing R]‘ and ‘[IsDomain R]‘.
 - The unique factorisation property is expressed by the typeclass ‘[UniqueFactorizationMonoid R]‘
 .
 - The fraction field is ‘FractionRing R‘.
 - A field isomorphism is a ‘RingEquiv‘, written ‘≃+*‘.
 - To express existence of an isomorphism we wrap the ‘RingEquiv‘ in ‘Nonempty‘.

 *Imports*
 The following modules provide the needed definitions and instances:
 - ‘Mathlib.RingTheory.FractionRing‘ for ‘FractionRing‘.
 - ‘Mathlib.Algebra.Algebra.Basic‘ for basic algebraic structures.
 - ‘Mathlib.Data.Real.Basic‘ for the real numbers ‘R‘.
 - ‘Mathlib.RingTheory.UniqueFactorizationDomain‘ for the ‘UniqueFactorizationMonoid‘ typeclass.
 - ‘Mathlib.RingTheory.Localization.FractionRing‘ for the localization construction.

 *Theorem shape*
 We formulate a theorem named ‘my_favorite_theorem‘. Its arguments are:
 - An implicit type ‘R‘.
 - The three typeclass arguments listed above.
 - The hypothesis ‘hK : (FractionRing R) ≃+* R‘.

 The conclusion is ‘Nonempty (R ≃+* R)‘. The proof placeholder is ‘by sorry‘.

 *Auxiliary definitions*
 No auxiliary lemmas are needed for the statement itself; the theorem is a pure existence claim.

 **Syntax translation**

 1. **Variable declaration**
    ‘‘‘lean
    {R : Type*}
    ‘‘‘
    ‘R‘ is an implicit type argument.

 2. **Typeclass arguments**
    ‘‘‘lean
    [CommRing R] [IsDomain R] [UniqueFactorizationMonoid R]
    ‘‘‘
    These are placed after ‘R‘ and before the hypothesis.

 3. **Hypothesis**
    ‘‘‘lean
    (hK : (FractionRing R) ≃+* R)
    ‘‘‘
    ‘FractionRing R‘ is the fraction field; ‘≃+*‘ is the notation for ‘RingEquiv‘.

 4. **Conclusion**
    ‘‘‘lean
    Nonempty (R ≃+* R)
    ‘‘‘
    ‘Nonempty‘ expresses that at least one ‘RingEquiv‘ exists.

 5. **Theorem header**
    ‘‘‘lean
    theorem my_favorite_theorem
    ‘‘‘
    The name follows the usual lower-snake-case convention.

 6. **Proof placeholder**




                                              – 18 –
MathForm


    ‘‘‘lean
    : Nonempty (R ≃+* R) := by sorry
    ‘‘‘
    The ‘by sorry‘ term tells Lean that the proof is omitted.

 **Complete Lean 4 code**

 ‘‘‘lean
 import Mathlib.RingTheory.FractionRing
 import Mathlib.Algebra.Algebra.Basic
 import Mathlib.Data.Real.Basic
 import Mathlib.RingTheory.UniqueFactorizationDomain
 import Mathlib.RingTheory.Localization.FractionRing

 open scoped Classical

 theorem my_favorite_theorem
   {R : Type*} [CommRing R] [IsDomain R] [UniqueFactorizationMonoid R]
   (hK : (FractionRing R) ≃+* R) :
   Nonempty (R ≃+* R) := by sorry
 ‘‘‘

 This code follows directly from the reasoning above: the imports bring in the necessary
 algebraic constructions, the typeclass assumptions capture the unique factorisation domain
 hypothesis, the hypothesis ‘hK‘ encodes the isomorphism of fraction fields with the reals, and
 the conclusion asserts the existence of a ring isomorphism between ‘R‘ and ‘R‘. No further
 modifications are required.
 </think>

 import Mathlib.RingTheory.FractionRing
 import Mathlib.Algebra.Algebra.Basic
 import Mathlib.Data.Real.Basic
 import Mathlib.RingTheory.UniqueFactorizationDomain
 import Mathlib.RingTheory.Localization.FractionRing

 open scoped Classical

 theorem my_favorite_theorem
   {R : Type*} [CommRing R] [IsDomain R] [UniqueFactorizationMonoid R]
   (hK : (FractionRing R) ≃+* R) :
   Nonempty (R ≃+* R) := by sorry

 ✓ Compilation succeeded         ✓ Semantic consistency: correct

 Goedel-Formalizer-V2-32B

 import Mathlib
 import Aesop

 set_option maxHeartbeats 0

 open BigOperators Real Nat Topology Rat

 theorem my_favorite_theorem (R : Type*) [CommRing R] [IsDomain R] [UniqueFactorizationMonoid R]
   (h_quotient : Nonempty (Frac R ≃+* R)) :
   Nonempty (R ≃+* R) := by sorry

 ✗ Compilation failed

 Frac is not applicable as a function.

 StepFun-Formalizer-32B




                                                     – 19 –
MathForm


    import Mathlib

    theorem my_favorite_theorem {R : Type*} [CommRing R] [IsUFD R]
        (h : ∃ (f : QuotField R ≃ R)) : ∃ (g : R ≃ R) := by
      sorry

    ✗ Compilation failed

    The generated theorem contains a syntax error in the hypothesis.

    ReForm-32B

    import Mathlib
    import Aesop

    set_option maxHeartbeats 0

    open BigOperators Real Nat Topology Rat

    theorem my_favorite_theorem (R : Type*) [CommRing R] [IsDomain R] [UniqueFactorizationMonoid R]
      (h : Nonempty (Frac R ≃+* R)) :
      Nonempty (R ≃+* R) := by sorry

    ✗ Compilation failed

    Frac is not applicable as a function.



D      Prompts
D.1      Data Construction Prompts
The two prompts implement the formalization generator and the retrieval planner of the pipeline described in
the Method section. During refinement rounds, both prompts additionally carry the compiler diagnostics and
semantic-consistency feedback from the previous attempt.

 Formalization Generator Prompt

 You are an expert in Lean 4 theorem proving and the Mathlib mathematical library.
 Your task is to formalize the given mathematical statement into correct Lean 4 code using Mathlib.

 FORMALIZATION REQUIREMENTS:
 1. Use proper Lean 4 syntax and Mathlib conventions
 2. Include ALL necessary headers
 3. Define appropriate variables and assumptions
 4. The theorem statement must be mathematically correct and equivalent to the original
 5. This task is only about automatic formalization. Do NOT output any proof steps, tactics, or
 reasoning.
 6. Retrieved information may be helpful; identify what is truly relevant and use it as needed.
 7. Only generate the translation. Do not try to solve or prove the problem.

 RETRIEVED MATHLIB INFORMATION:
 {retrieval_context}

 PREVIOUS COMPILATION FAILURE - FIX REQUIRED:
 Failed code:
 {last_bad_code}
 Compiler error:
 {compile_error}
 Please analyze the error and provide corrected code.




                                                         – 20 –
MathForm


 SEMANTIC CONSISTENCY ISSUE - FIX REQUIRED:
 Previous code:
 {last_bad_code}
 Semantic feedback:
 {semantic_feedback}
 Please revise the formalization to match the mathematical meaning.

 STATEMENT TO FORMALIZE:
 {statement}




 Retrieval Planner Prompt

 You are a Lean 4/Mathlib expert. I need to formalize the mathematical statement below into Lean 4
 code.
 To ensure accurate formalization, I will search the Lean mathematical library (Mathlib) for
 relevant definitions and theorems.

 First review the existing queries and retrieved results to decide whether any new search queries
 are truly necessary. Only generate new queries if they are essential to resolve ambiguity or
 missing definitions. If more info is needed, generate 1-3 new queries; otherwise output nothing.

 Each query should be:
 - Concise and specific
 - Focus on mathematical concepts, definitions, or theorems

 Do not repeat any previous queries.
 Each query must be highly necessary and directly helpful for formalization; avoid broad or
 speculative queries.
 If no additional queries are needed, output an EMPTY code block only.

 Output format: output ONLY a single triple-backtick block. One query per line, no numbering or
 bullets. No extra text, no explanations.

 Examples:
 ‘‘‘
 group definition
 ring homomorphism
 topological space compactness
 natural number induction
 vector space dimension
 ‘‘‘

 Empty output example (no additional queries needed):
 ‘‘‘
 ‘‘‘

 Previous queries:
 {previous_queries}

 Retrieved results so far:
 {retrieval_context}

 Previous verification feedback:
 - Compilation error: {compile_error}
 - Semantic feedback: {semantic_feedback}

 Statement to formalize:
 {statement}




                                               – 21 –
MathForm


D.2    Semantic Consistency Check Prompt
The semantic consistency check compares a natural-language statement with its Lean 4 formalization and
returns a binary judgment. The same prompt is used for validation during data construction, for the semantic
term of the reward, and for evaluation.

 Semantic Consistency Check Prompt

 # Lean 4 Formalization Semantic Consistency Check

 **Role:**
 Act as an expert in Lean 4 formal verification and mathematical logic. Your task is to perform a
 rigorous semantic consistency review, comparing a Natural Language (NL) mathematical statement
 against its corresponding Lean 4 formalization.

 **Objective:**
 Determine if the provided Lean 4 code is a faithful, completely accurate, and logically equivalent
  translation of the Natural Language statement. Only focus on the formalization itself, do not
 discuss any proof process.

 **Analysis Steps:**
 Before generating the output, analyze the input pairs based on the following criteria:

 1. **Deconstruction of the Natural Language Statement:**
    * Identify all key mathematical objects, definitions, and properties.
    * Map out the logical flow (antecedents, consequents, quantifiers).
    * Identify the implicit domain of discourse.

 2. **Analysis of the Lean 4 Code Structure:**
    * Verify type hierarchy compliance (classes vs. structures).
    * Check variable declarations and hypothesis scope.
    * Ensure standard library usage matches the mathematical intent.

 3. **Semantic Mapping and Gap Analysis:**
    * **Bi-directional Fidelity:** Ensure every constraint in the NL maps to the code, and the code
  adds no unintended constraints.
    * **Quantifier Precision:** Rigorously check the order and dependency of ‘for all‘ vs ‘there
 exists‘.
    * **Condition Strength:** Ensure predicates are neither strictly stronger nor strictly weaker
 than required.

 **Output Format Requirements:**
 Your output must be **exactly** two XML tags in this order, with no other text before, between, or
  after them. Do not use code fences or markdown.

 1. <comments></comments>
    * Provide your detailed evaluation and reasoning.
    * If inconsistent, describe the specific semantic mismatch.
 2. <result></result>
    * Output exactly one word: ‘correct‘ or ‘incorrect‘.

 **Strict Output Template:**
 <comments>...</comments>
 <result>...</result>

 ---

 **Input Natural Language Statement:**
 {mathematical_statement}

 **Input Lean 4 Code:**
 {autoformalization_placeholder}




                                                  – 22 –
MathForm


D.3    Trajectory Reconstruction Prompt
Trajectory reconstruction takes a verified natural-language statement together with its Lean 4 formalization
as input and synthesizes a formalization trajectory retrospectively. The prompt organizes this process into
four stages, namely concept understanding, logical structure analysis, formalization strategy, and syntactic
translation, and restricts its content to formalization strategy rather than proof strategy.

 Trajectory Reconstruction Prompt

 Please read the following natural language math problem and its Lean 4 formalization below. Then
 reconstruct the thinking process a mathematician would go through when formalizing this problem
 into Lean 4. Your response should mimic the actual reasoning flow, including:

 **Key Requirements for Authentic CoT:**

 1. **Mathematical Concept Understanding**: What mathematical concepts and entities appear in this
 problem? What are the key mathematical objects involved (numbers, functions, sets, structures, etc
 .)? Are there any ambiguities in the natural language description that need clarification? What
 implicit assumptions or conventions might be present? Consider domain constraints, well-
 definedness conditions, and mathematical context.

 2. **Logical Structure Analysis**: Analyze the logical form of the statement. Is it a conditional
 (implication), biconditional (equivalence), universal quantification, existential statement, or a
 combination? Identify the hypotheses and conclusion clearly. What is the dependency structure
 between different parts of the statement?

 3. **Formalization Strategy**:
    - Determine appropriate types for each mathematical object. Should variables be R, N, Z, Q,
 or more complex types? Provide a concise justification based on the mathematical operations and
 constraints.
    - Outline the overall formalization approach: What theorem structure is needed? What key
 imports are required? Are auxiliary definitions or lemmas necessary? Should this be formulated as
 a theorem, lemma, or definition?
    - Briefly plan how to represent complex mathematical structures (e.g., matrices, sequences,
 sets) in Lean’s type system.

 4. **Syntax Translation**: Now translate each component step by step:
    - How should each mathematical object be declared? Consider implicit vs explicit arguments,
 type annotations needed.
    - How to express each hypothesis in Lean syntax? Walk through each condition, explaining
 notation choices (e.g., how to write matrix entries, how to express distinctness, how to state
 equations).
    - How to formalize mathematical operations? Consider operator precedence, parenthesization, and
  Lean-specific syntax requirements.
    - How to structure the theorem statement? Discuss the order of hypotheses, naming conventions,
 and how the conclusion is formulated.
    - Address any subtle translation issues: type coercions, implicit arguments, namespace
 qualifications, notation systems.
    - Present the complete Lean 4 code that results from the above reasoning process.

 **Critical Stylistic Guidelines:**

 - Do NOT question or doubt the accuracy of the provided Lean 4 code, nor raise concerns about it,
 don’t make any modifications to the provided code
 - Avoid meta-statements like "the provided code" or "the given code"
 - Focus entirely on **formalization strategy**, NOT proof strategy
 - Show genuine reasoning with considerations of alternatives and justifications for choices made
 - Be specific about Lean syntax decisions rather than giving high-level descriptions
 - Please try to describe the content using plain text as much as possible, and avoid using the
 table format of markdown

 ### Natural Language Problem
 {statement}



                                                  – 23 –
MathForm



 ### Lean 4 Code
 ‘‘‘Lean4
 {lean_code}
 ‘‘‘



D.4    Evaluation Inference Prompts
Each model is evaluated with its officially recommended prompt template. For general-purpose LLMs, we
additionally include an explicit instruction not to produce a proof, which prevents instruction drift during
inference.

 M ATH F ORM-8B Inference Prompt (Ours)

 Please convert the following informal math problem to a formal one in Lean 4 with a header. Use
 the following theorem names: my_favorite_theorem.

 {informal_problem}


 General-Purpose LLM Inference Prompt

 Please convert the following informal math problem to a formal one in Lean 4 with a header. Do not
  provide the proof, end with ‘by sorry‘. Use the following theorem names: my_favorite_theorem.

 {informal_problem}


 Kimina-Autoformalizer Inference Prompt

 You are an expert in mathematics and Lean 4. Please autoformalize the following problem in Lean 4
 with a header. Use the following theorem names: my_favorite_theorem.

 {informal_problem}


 Mathesis Inference Prompt

 [Question]:
 {informal_problem}

 You are an expert in formal mathematics. Your task is to convert the above [question] to lean 4
 theorems by completing the following lean 4 code:

 ‘‘‘lean4
 import Mathlib
 import Aesop
 set-option maxHeartbeats 0
 set-option pp.numericTypes true
 set-option pp.coercions true
 set-option pp.letVarTypes true
 set-option pp.structureInstanceTypes true
 set-option pp.instanceTypes true
 set-option pp.mvars.withType true
 set-option pp.coercions true
 set-option pp.funBinderTypes true
 set-option pp.piBinderTypes true
 open BigOperators Real Nat Topology Rat




                                                  – 24 –
MathForm


 /-
 {informal_problem}
 -/
 ‘‘‘


 StepFun-Formalizer Inference Prompt

 Please autoformalize the following problem in Lean 4 with a header. Use the following theorem
 names: my_favorite_theorem.

 {informal_problem}

 Your code should start with:
 ‘‘‘Lean4
 import Mathlib
 ‘‘‘


 Goedel-Formalizer-V2 Inference Prompt

 Please autoformalize the following natural language problem statement in Lean 4. Use the following
  theorem name: my_favorite_theorem
 The natural language statement is:
 {informal_problem}Think before you provide the lean statement.


 ReForm Inference Prompt

 Think step by step to translate the mathematical problem in natural language to Lean 4, and verify
  the consistency.
 {informal_problem}




                                               – 25 –
