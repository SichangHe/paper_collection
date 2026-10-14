                              A Verifier-Guided Explainable Reasoning Framework
                                  with Gold-Anchored QLoRA, Task-Aware
                                Mixture-of-Experts, and Group-Relative RLVR
                                        Thi Kim Trang Vo1,3 , Nam Tien Le2,3 , Thi Kim Nguyet Vo4,5 , Minh Khang Tran1,3 , Duy Phuong Tran1,3
                                                           1
                                                               University of Information Technology (UIT), Ho Chi Minh City, Vietnam
                                                                 2
                                                                   Ho Chi Minh City University of Technology (HCMUT), Vietnam
                                                                       3
                                                                         Vietnam National University, Ho Chi Minh City, Vietnam
                                                                    4
                                                                      University of Economics Ho Chi Minh City (UEH), Vietnam
                                                                      5
                                                                        Viet Nam – The Netherlands Programme (VNP), Vietnam
arXiv:2609.05221v1 [cs.CL] 4 Sep 2026




                                 Abstract—Large language models (LLMs) show strong reason-              intermediate reasoning.
                              ing ability, but their explanations can remain inconsistent, weakly          Prior work improves reasoning through self-consistency [3],
                              grounded, or difficult to verify. We propose a verifier-guided            process supervision [4], and scientific-logicality evaluation [5].
                              explainable reasoning framework for transparent educational ques-
                              tion answering that combines gold-anchored QLoRA, task-aware              Reinforcement learning with verifiable rewards (RLVR) further
                              symbolic routing, and group-relative RLVR. Qwen2.5-3B-Instruct            enables optimization from automatically checkable signals.
                              is first adapted with field-weighted QLoRA supervision anchored to        DeepSeekMath introduced Group Relative Policy Optimization
                              authoritative answers. A lightweight router then assigns logic problems   (GRPO) [6], while One-Shot-RLVR demonstrated reasoning
                              to a FOL/Z3 verifier and physics problems to a formula- and unit-         improvements with limited supervision [7]. Nevertheless,
                              aware symbolic solver. Verifier feedback is further used to support
                              candidate evaluation, self-revision, and reward construction during       answer-only rewards cannot distinguish an accidentally correct
                              RLVR. Candidate responses are evaluated along three complementary         prediction from a well-supported solution.
                              dimensions: P1 for answer correctness, P2 for evidence or unit               This challenge is closely aligned with the 2nd Interna-
                              consistency, and P3 for reasoning depth and explainability. At            tional XAI Challenge for Transparent Educational Question-
                              inference, gold-free self-consistency aggregates multiple candidate       Answering (EXACT 2026), organized with IJCNN 2026 [8]. Its
                              responses before an optional question-only physics verifier performs
                              conservative system-level correction. On 438 held-out examples, RLVR      heterogeneous tasks require different verification mechanisms:
                              increases P3 from 50.68% to 72.20%, while hybrid P1 remains               logic questions require premise-based entailment checking,
                              approximately stable at 55.94%. Self-consistency improves model-          whereas physics questions additionally require formula, numer-
                              only P1 from 48.86% to 50.23%, with symbolic verification providing       ical, and unit consistency.
                              the remaining hybrid gain. These results indicate that RLVR primarily        To address these requirements, we propose a Verifier-
                              strengthens explicit reasoning structure, while symbolic verification
                              complements the neural policy by improving answer reliability at the      Guided Explainable Reasoning Framework with Gold-Anchored
                              system level.                                                             QLoRA, Task-Aware Mixture-of-Experts, and Group-Relative
                                                                                                        RLVR. Qwen2.5-3B-Instruct [2] is adapted using QLoRA [9],
                                 Our code implementation is available at:                               following LoRA [10]. Training targets are anchored to author-
                              https://github.com/VoThiKimTrang06101997/Explainable-xAI/tree/
                              master/One-Shot-RLVR
                                                                                                        itative answers, while field-weighted supervision emphasizes
                                                                                                        answers, evidence, and units. Unlike conventional neural MoE
                                 Index Terms—Explainable AI, Large Language Models (LLM),               architectures [11], [12], our lightweight router dispatches tasks
                              Educational Question Answering, Reinforcement Learning with Ver-          to external symbolic experts: FOL/Z3 verification for logic
                              ifiable Rewards (RLVR), QLoRA, Task-Aware Mixture-of-Experts,             [13] and a formula- and unit-aware solver for physics.
                              Neuro-Symbolic Reasoning, First-Order Logic, FOL/Z3 Verifier,
                              Scientific Reasoning.
                                                                                                           We evaluate three complementary dimensions: P1 for final-
                                                                                                        answer correctness, P2 for evidence or unit consistency, and
                                                                                                        P3 for reasoning depth and explainability. Verifier feedback
                                                     I. INTRODUCTION                                    supports candidate evaluation, self-revision, and group-relative
                                 Large language models (LLMs) have achieved strong multi-               RLVR, while inference combines gold-free self-consistency
                              step reasoning performance through chain-of-thought (CoT)                 with optional conservative physics verification. On 438 held-out
                              prompting and instruction tuning [1], [2]. However, in scientific         examples, RLVR increases P3 from 50.68% to 72.20%, while
                              and educational question answering, a plausible explanation               hybrid P1 remains approximately stable at 55.94%, indicating
                              is not necessarily trustworthy. A correct answer may still rely           that RLVR primarily strengthens explicit reasoning structure
                              on an invalid inference, an inappropriate physical formula,               while symbolic verification contributes complementary system-
                              unsupported evidence, or inconsistent units. Thus, reliable               level reliability.
                              reasoning requires both answer correctness and inspectable                   Our contributions are mainly:
• Gold-anchored QLoRA: a field-weighted adaptation strat-
  egy that preserves authoritative answers and structured
                                                                                     p(e | x) = softmax(Wr h(x) + br ) ,             (3)
  evidence before RLVR.
• Task-aware neuro-symbolic verification: lightweight rout-               and selects
  ing to FOL/Z3 logic verification and formula- and unit-aware
  physics verification.
• Verifier-guided P1/P2/P3 RLVR: a framework that sep-
                                                                               e∗ = arg max p(e | x),       e ∈ {Logic, Physics}.    (4)
                                                                                           e
  arates answer correctness, evidence/unit consistency, and
                                                                           Thus, routing does not modify the Qwen Transformer or
  reasoning depth while distinguishing neural-policy perfor-
                                                                        activate Transformer-level experts; it only dispatches each
  mance from hybrid-system gains.
                                                                        problem to an external task-specific verifier.
                            II. METHOD                                  1) Logic Expert. For logic tasks, natural-language premises
                                                                        are converted into first-order-logic (FOL) representations and
A. Framework Overview
                                                                        checked using Z3 [13]. A candidate claim c is entailed when
  We formulate transparent educational QA as a generation–
verification–optimization problem in which both the final
answer and its reasoning are evaluated. As shown in Fig. 1,                             P |= c ⇐⇒ UNSAT(P ∧ ¬c).                     (5)
the framework consists of seven stages: (1) gold-anchored                  Contradiction is checked analogously through UNSAT(P ∧
canonicalization, (2) field-weighted QLoRA SFT and cali-                c). For multiple-choice questions, candidate options are com-
bration, (3) task-aware Mixture-of-Experts (MoE) routing, (4)           pared according to their symbolic support.
symbolic verification, (5) self-revision and candidate ranking,         2) Physics Expert. For physics tasks, the verifier extracts
(6) P1/P2/P3 group-relative RLVR, and (7) gold-free self-               variables and units, retrieves a supported relation set E, solves
consistency with optional physics verification.                         the relation, and normalizes the result:
  Our MoE is a task-level routing mechanism, not a
Transformer-internal sparse MoE architecture [11], [12]. The
                                                                                    zSOL         = Solve(E, V, U ),
LLM backbone is unchanged; the router only selects an external                                                                       (6)
Logic or Physics verification expert.                                               aSOL         = NormalizeUnit(zSOL ).

B. Gold-Anchored QLoRA Fine-Tuning                                         The physics expert checks formula applicability, numerical
                                                                        consistency, and units, while the LLM remains the primary
    For each example xi = (qi , a∗i , mi ), where qi is the question,
  ∗                                                                     reasoning model.
ai is the authoritative answer, and mi contains task metadata,
teacher-generated supervision may be repaired while the source          D. Verifier-Guided Self-Revision
answer remains locked:                                                     Verifier feedback identifies unsupported premises, incorrect
                                                                        formulas, unit inconsistencies, or answer–explanation conflicts.
                 yiT           = Repair(xi , a∗i ),                     A candidate may therefore be revised as
                                                                 (1)
                 aaligned
                  i            = a∗i .
   The aligned target contains the answer, unit, premises,                              ỹk = Revise(yk , Fverifier (yk )) ,         (7)
explanation, and a compact reasoning trace, preventing noisy              where Fverifier denotes task-specific feedback. Candidates
teacher outputs from replacing authoritative labels.                    are also compared using verifier-derived quality signals,
   We adapt Qwen2.5-3B-Instruct [2] using 4-bit NF4 QLoRA               encouraging responses whose answers and reasoning are jointly
[9], following LoRA [10], with r = 32, α = 64, and dropout              better supported.
0.05. Completion-only SFT uses
                                                                        E. P1/P2/P3 Group-Relative RLVR
                                P                                          Starting from the calibrated SFT checkpoint, we apply
                                   twt mt ℓt
                  LSFT =            P                ,           (2)    reinforcement learning with verifiable rewards (RLVR) follow-
                             max(1,      t wt mt )
                                                                        ing One-Shot-RLVR [7] and the group-relative optimization
   where mt masks prompt tokens and wt assigns larger weights           principle of GRPO [6]. For each training question, K = 3
to answer, unit, and premise fields. A subsequent answer-               responses are sampled.
focused calibration stage further strengthens these fields before          The reward used in the final experiment is
RLVR.
C. Task-Aware Mixture-of-Experts Routing and Symbolic                              Ri,k = 0.50Rexact + 0.20Rdense
                                                                                                                                      (8)
Verification                                                                              + 0.15RP2 + 0.10RP3 + 0.05Rfmt .
   Unlike neural MoE models that route tokens through train-              Here, Rexact measures exact final-answer correctness, Rdense
able expert layers, our task-aware MoE operates only at the             provides task-aware partial answer credit, RP2 measures
verification level. Given an input representation h(x), the router      premise consistency for logic or unit consistency for physics,
estimates                                                               and RP3 rewards explicit reasoning depth:
Figure 1: Overview of the proposed verifier-guided framework. Gold-anchored targets support QLoRA SFT and calibration. A task-aware MoE
router selects the Logic/FOL/Z3 or Physics/SOL verification path. Verifier signals support revision and group-relative RLVR. At inference,
one greedy and four sampled responses are grouped by answer equivalence before optional question-only physics verification.



                                                                      surrogate implemented in our training code. Let ℓ̄θ and ℓ̄old
                                       
                                 NCoT                                 denote the sequence-average log probabilities under the current
                 RP3 = min 1,             .                     (9)   and rollout policies:
                                    4
  For each response group, the relative advantage is                                                                    
                                                                                      ρi,k (θ) = exp ℓ̄θ,i,k − ℓ̄old,i,k .           (13)
                              Ri,k − µi
                       Ai,k =           ,                     (10)       The group-relative policy loss is
                               σi + ϵ
  with                                                                                    K
                                                                                      1 X    
                                                                        Lpolicy = −       min ρi,k Ai,k ,
                                  K                                                   K
                       µi =
                              1 X
                                  Ri,k .                      (11)
                                                                                         k=1                                      (14)
                              K                                                                     clip(ρi,k , 1 − ε, 1 + ε)Ai,k ,
                                 k=1
   Groups with negligible reward variance are skipped because           where ε = 0.2 in the final run. Combining this clipped
they provide no useful relative preference signal.                    objective with reference regularization gives the RLVR loss
   A frozen copy of the calibrated SFT checkpoint serves as
the reference policy. In the active implementation, reference
regularization uses the difference between sequence-average                              LRLVR = Lpolicy + βLref .                   (15)
log probabilities:                                                      Thus, Ai,k favors candidates whose verifiable reward exceeds
                                                                      the group mean, clipping limits overly large policy updates,
                                           2                         and Lref constrains drift from the calibrated SFT policy.
                      Lref = ℓ̄θ − ℓ̄ref        .             (12)
  Following the group-relative RL formulation [6] and                 F. Gold-Free Self-Consistency and Final Output
verifiable-reward training setting [7], the policy uses the clipped     At held-out inference, five responses are generated,
                                                                     B. Quantitative Results
                                                                        We report three complementary reasoning dimensions. P1 is
                 n                                     o
              Y = y (g) , y (1) , y (2) , y (3) , y (4) ,     (16)
                                                                     final answer correctness after the complete inference pipeline.
                                                                     P2 is a task-aware supporting-consistency score: for logic it is
   where y (g) is generated greedily and the remaining four
                                                                     the partial F1 between predicted and reference premise indices,
responses are sampled. They are grouped by task-aware answer
                                                                     whereas for physics it checks normalized unit consistency (with
equivalence:
                                                                     partial multi-unit credit for multi-valued answers). P3 is the
                                                                     generated reasoning-depth proxy defined in Eq. (9). Table II
                 C = ClusterEquivalent(Y).                    (17)   compares calibrated SFT and the final RLVR policy on the
                                                                     same 438 held-out examples.
   The largest cluster is selected. If clusters have equal size,        The three metrics reveal different effects of RLVR. P1
preference is given to the cluster containing the greedy             changes only from 56.62% to 55.94% (−0.68 points), so the
response; remaining ties are resolved by a gold-free structural      completed RLVR run does not produce an additional held-out
quality score [3]. No validation gold label is used during this      answer-accuracy gain. P2 decreases from 77.70% to 75.33%
selection.                                                           (−2.37 points), indicating that richer generated reasoning does
   For physics, a conservative question-only verifier may            not automatically preserve premise selection or physical-unit
override the selected answer only when                               consistency. In contrast, P3 rises from 50.68% to 72.20%, a
                                                                     gain of 21.52 points, making reasoning depth the dominant
                                                                     observed post-training change.
                          cverifier ≥ 0.98,                   (18)
                                                                        This pattern is technically consistent with the group-relative
   otherwise it abstains. The final output contains the answer       reward. Exact P1 has the largest individual coefficient, but
and, where applicable, unit, supporting premises, symbolic/FOL       candidates inside a rollout group frequently share the same
information, reasoning trace, and verification confidence.           answer reward. When this occurs, P1 contributes little relative
                                                                     ranking signal, whereas differences in P2, P3, dense answer
                     III. EXPERIMENTS                                credit, and formatting can still produce non-zero advantages.
A. Experimental Setup                                                Since P3 is explicitly rewarded, the policy can therefore learn to
                                                                     emit more complete reasoning traces even when final-answer
   We evaluate the proposed framework on the EXACT logic
                                                                     accuracy has already saturated within a group. The format
and physics data [8]. After preprocessing, 2,162 examples are
                                                                     decrease from 98.17% to 94.52% further shows that longer
divided using a group-safe 80:20 split into 1,724 training and
                                                                     structured outputs create more opportunities for malformed
438 held-out validation samples. Shared logic premise blocks,
                                                                     fields or schema violations.
duplicate normalized physics questions, and identical model
                                                                        P2 should also be interpreted jointly with the task mixture
inputs are kept within the same partition to reduce leakage.
                                                                     rather than as a single homogeneous quantity. Physics con-
Retrieval is disabled (RETRIEVAL_TOP_K=0), and validation
                                                                     tributes 274 of the 438 validation examples and retains high
labels are accessed only after generation.
                                                                     unit consistency (91.79% for SFT and 89.23% for RLVR),
   Table I summarizes the resulting data split.
                                                                     which lifts the micro-averaged P2. Logic P2 instead measures
             Table I: Experimental data composition.
                                                                     premise selection and is substantially lower. Consequently, the
               Task                    Total   Train   Val.
                                                                     overall P2 decrease reflects both a modest physics-unit decline
               Logic Multiple Choice     360     287    73           and weaker premise consistency in some logic categories, rather
               Logic Yes/No              415     331    84
               Logic Uncertain            33      26     7
                                                                     than one uniform failure mode.
               Physics                 1,354   1,080   274              Finally, P3 is a reasoning-depth proxy, not a proof of logical
               Total                   2,162   1,724   438           validity. A longer trace can make intermediate assumptions
                                                                     easier to inspect while still containing an unsupported premise
   The backbone is Qwen2.5-3B-Instruct [2] with 4-bit NF4            or numerical mistake. Reporting P1, P2, P3, and Strict together
QLoRA [9]. Maximum sequence, prompt, and generation                  therefore separates final correctness, supporting consistency,
lengths are 1,280, 1,024, and 224 tokens. Stage A performs           reasoning explicitness, and end-to-end structural validity. The
three SFT epochs at 5×10−5 , Stage B performs one calibration        small Macro-P1 change (76.82% to 76.14%) likewise indicates
epoch at 2 × 10−5 , and Stage C performs 240 RLVR rollout            that the P1 shift is not caused by collapse of a single task
steps at 2 × 10−6 .                                                  family.
   Evaluation uses five-generation gold-free self-consistency:       1) Task-Level P1/P2/P3 Analysis.
one greedy response and four sampled responses (T = 0.35,               Table III decomposes all three metrics by task family. The
top-p = 0.90). The question-only physics verifier intervenes         P2 values are computed with the same task-aware definition
only for supported rules with confidence ≥ 0.98. Experiments         used in the overall score and are therefore directly consistent
run on one NVIDIA L4 24 GB GPU in a PyTorch/Hugging                  with Table II.
Face environment using Transformers, PEFT, Accelerate,                  For P1, Logic Multiple Choice remains exactly 91.78%, Logic Uncertain remains
                                                                     100% on its seven-example subset, Logic Yes/No decreases by 2.38 points, and Physics
bitsandbytes, and repository-side FOL/Z3 and SOL modules.
                 Table II: Held-out validation results (%). Macro P1 is the unweighted mean over the four evaluated task families.
                                           Model                      P1   Macro P1    Logic P1          Physics P1           P2          P3         Format    Strict
                                           Calibrated SFT          56.62      76.82       83.54               40.51        77.70       50.68           98.17   41.44
                                           RLVR                    55.94      76.14       82.32               40.15        75.33       72.20           94.52   40.14
                                           ∆                       -0.68       -0.69      -1.22                -0.36       -2.37      +21.52           -3.65    -1.30


 Table III: Task-level P1/P2/P3 performance (%).                              Table IV: Inference-component ablation on P1 (%).                                 Table V: Physics P1 by answer
                                P1            P2          P3                           Policy Inference                     Overall Logic Physics               representation (%).
           Task              SFT RLVR SFT RLVR SFT RLVR                                SFT Greedy                            50.46 83.54 30.66
           Logic MC         91.78 91.78 57.26 53.70 40.75 72.95                        SFT +         Five-generation   self- 51.14 83.54 31.75                          Type                 N SFT RLVR
           Logic Yes/No     75.00 72.62 52.20 51.87 42.86 75.00                               consistency                                                               Plain numeric      195 49.74 49.74
           Logic Uncertain 100.00 100.00 45.31 38.16 53.57 71.43                       SFT + Physics verifier                  56.62 83.54   40.51                      Scientific numeric  48 6.25   6.25
           Physics          40.51 40.15 91.79 89.23 55.66 71.17                        RLVR Greedy                             48.86 82.32   28.83                      Binary               4 75.00 75.00
                                                                                       RLVR +        Five-generation   self-   50.23 82.32   31.02                      Categorical text     8 37.50 37.50
                                                                                              consistency                                                               Numeric assignment   3 66.67 66.67
                                                                                       RLVR + Physics verifier                 55.94 82.32   40.15                      Multiple values      6 50.00 33.33




changes only from 40.51% to 40.15%. Hence, the small global P1 decrease is distributed                   or physical units remain consistent, and P3 measures whether the generated response
across limited task-level changes rather than a broad loss of answer capability.                         exposes explicit intermediate reasoning. The comparison is therefore methodological
    For P2, Logic Multiple Choice changes from 57.26% to 53.70%, Logic Yes/No from                       rather than a direct leaderboard.
52.20% to 51.87%, Logic Uncertain from 45.31% to 38.16%, and Physics from 91.79%
to 89.23%. The largest percentage-point logic decrease occurs on the seven-example                       E. Discussion
Uncertain subset and should not be over-interpreted. The physics P2 value is much higher                     The verified results expose a clear three-way P1–P2–P3 trade-off. Relative to calibrated
because it measures unit consistency, whereas logic P2 is a partial premise-selection F1.                SFT, RLVR changes P1 by −0.68 points and P2 by −2.37 points but improves P3 by
This confirms that P2 is best used as a task-aware diagnostic rather than as a substitute                +21.52 points. The result does not support the claim that RLVR improves every metric;
for P1.                                                                                                  instead, it supports a more specific conclusion: under the present reward weighting and
    For P3, every populated task family improves: Logic Multiple Choice increases by                     optimization budget, RLVR mainly strengthens reasoning explicitness while preserving
32.19 points, Logic Yes/No by 32.14, Logic Uncertain by 17.86, and Physics by 15.51.                     answer accuracy within approximately one percentage point of the calibrated baseline.
This consistency across heterogeneous tasks strengthens the interpretation that RLVR                         P2 provides an additional diagnostic that prevents the P3 result from being overstated.
primarily reshapes reasoning explicitness. The physics result is especially informative: P3              The modest P2 decline shows that a deeper response can introduce an incorrect or
rises substantially while P1 stays near 40%, showing that producing a deeper trace is not                unnecessary premise, or lose unit consistency, even when the trace becomes more complete.
sufficient to solve numerical execution or formula-selection errors.                                     Conversely, P1 can remain correct despite a weaker supporting trace. Reporting all three
                                                                                                         metrics therefore makes the source of a gain or degradation visible and better matches the
C. Ablation Study                                                                                        objective of transparent educational QA than relying on one aggregate accuracy number.
    We isolate the contribution of greedy decoding, five-generation gold-free self-                          Five-generation self-consistency and symbolic verification address different parts of this
consistency, and deterministic physics verification. Table IV reports P1 because this                    trade-off. Self-consistency reduces single-generation variance, whereas the deterministic
ablation is designed specifically to measure final answer correction at inference; complete              physics verifier selectively corrects cases that can be solved by supported high-confidence
component-wise P2/P3 traces are not logged for every intermediate decoding mode and                      relations. The verifier’s large physics P1 gain despite sparse activation indicates that
are therefore not inferred.                                                                              some residual errors are execution failures rather than failures to produce reasoning text.
    Five-generation self-consistency increases overall P1 by 0.68 points for SFT and                     Together, these observations motivate treating the neural policy, reasoning objective, and
1.37 points for RLVR. Symbolic verification provides a substantially larger physics gain:                symbolic checker as complementary components rather than attributing all system-level
relative to self-consistency, physics P1 improves by 8.76 points for SFT and 9.12 points                 improvement to RLVR alone.
for RLVR. The verifier intervenes on only 43 of 274 physics queries (15.69%), correcting
                                                                                                         F. Visualization Results
26 SFT and 27 RLVR errors while introducing two regressions for each policy. This
sparse intervention pattern supports the intended design: the symbolic module acts as a                     The five diagnostics summarize the same measurements reported in the tables. Figure 2
selective checker for supported high-confidence relations rather than as a second model                  shows task-level P1, P2, and P3 from Table III; Fig. 3 separates inference-stage P1
that replaces the LLM on every physics query.                                                            correction from RLVR training-time dynamics.
    The ablation also clarifies where the observed system-level gain originates. For both
policies, moving from greedy decoding to five-generation self-consistency yields only a
small increase, whereas the physics verifier produces the dominant final correction. This
separation is important because it prevents the verifier gain from being misattributed to
RLVR itself: the policy changes the distribution and structure of generated reasoning,
while the deterministic checker repairs a smaller subset of supported numerical cases after
generation. The similar verifier gains for SFT and RLVR further suggest that the symbolic
module is exploiting task structure that remains useful across both neural checkpoints
rather than compensating for one particular policy.                                                      Figure 2: Task-level diagnostics from Table III. Left: P1 correctness.
1) Physics Error Analysis.
    Table V further decomposes physics answer correctness by representation. Plain                       Middle: P2 consistency. Right: P3 reasoning depth.
numeric answers reach 49.74% P1, whereas scientific-notation answers reach only 6.25%.
At the same time, physics P2 (unit consistency) remains 89.23% after RLVR. The gap                           Figure 2 makes the P1–P2–P3 trade-off directly checkable against Table III. P1
between high unit consistency and much lower answer correctness indicates that the                       is nearly unchanged: Logic MC remains 91.8%, Logic Yes/No changes 75.0→72.6%,
dominant physics failures are not primarily unit recognition; they are more consistent with              Logic Uncertain remains 100.0%, and Physics changes 40.5→40.1%. P2 decreases from
formula selection, numerical execution, exponent normalization, and answer representation                57.3→53.7%, 52.2→51.9%, 45.3→38.2%, and 91.8→89.2%, respectively. In contrast,
errors.                                                                                                  P3 rises in every task: 40.8→72.9%, 42.9→75.0%, 53.6→71.4%, and 55.7→71.2%.
    The RLVR training trajectory provides a complementary explanation. Of 240 rollout                    The visual pattern therefore supports the same conclusion as Table II: RLVR changes
groups, 57 (23.75%) have zero reward variance and are skipped, leaving 183 informative                   reasoning depth more strongly than final-answer correctness.
groups and 30 optimizer updates. The right panel of Fig. 3 summarizes 20-step
rolling means observed during RLVR training. The first versus last 20-step means
are approximately 0.86→0.90 for reward, 0.93→0.95 for P1, 0.67→0.75 for P2, and
0.53→0.74 for P3. Thus, the value near 0.94 refers to sampled P1 during RLVR training
rather than the held-out P1 values in Tables II–IV. Under Eq. (10), zero-variance groups
provide no relative ranking signal, so optimization is concentrated on groups where
candidate rewards differ; the strongest sustained change is consequently observed in P3.
D. Comparison with Prior Reasoning Frameworks
    Table VI provides a contextual comparison with representative reasoning and
verification approaches. Because datasets, models, inference budgets, and evaluation
metrics differ, the reported numbers are not directly comparable.
    Prior work emphasizes either intermediate process supervision or verifiable mathemati-
cal outcomes. Our framework instead combines heterogeneous logic and physics reasoning
                                                                                                         Figure 3: Inference and training dynamics. Left: P1 progression
with task-specific symbolic verification and reports all three core diagnostics together. P1             from Table IV. Right: 20-step rolling reward/P1/P2/P3 during RLVR
captures whether the final answer is correct, P2 measures whether its supporting premises                training.
Table VI: Contextual comparison with representative reasoning and verification approaches. Results are not directly comparable across
benchmarks.
          Method                    Benchmark / Model       Supervision                                   Reasoning / Verification                     Reported Result
          Let’s Verify Step by Step MATH subset / large LLM Process supervision                           Process Reward Model                         78.2% accuracy
          [4]
          DeepSeekMath [6]          MATH / DeepSeekMath-7B SFT + GRPO                                     Outcome-verifiable group-relative opti- 51.7%; 60.9% with 64-
                                                                                                          mization                                sample self-consistency
          One-Shot-RLVR [7]              MATH500 / Qwen2.5-Math- One-example RLVR                         Group-relative verifiable reward        36.0% → 73.6%
                                         1.5B
          Scientific Logicality [5]      PhysLogic / multiple LLMs Logicality-guided                    Process-aware scientific reasoning eval-       Improved logicality and
                                                                                                        uation                                         physics performance
          Ours                           EXACT      /   Qwen2.5-3B- Gold-anchored           QLoRA     + FOL/Z3 + Physics/SOL + five-generation         55.94% P1; 75.33% P2;
                                         Instruct                   RLVR                                gold-free self-consistency                     72.20% P3



    Figure 3 (left) reproduces Table IV: SFT progresses 50.5→51.1→56.6%, while                    Physics also remains limited by formula selection, numerical execution, and scientific-
RLVR progresses 48.9→50.2→55.9% from greedy decoding to self-consistency and then                 notation normalization. Future work will study (i) improved P1/P2/P3 reward balancing,
hybrid verification. Hence, self-consistency gives the modest model-only gain and the             (ii) stronger numerical and symbolic normalization, (iii) broader logic/physics verifier
verifier supplies the larger final correction. The right panel is not a held-out accuracy         coverage, (iv) complete reward-component and routing ablations, and (v) larger scientific
plot; it summarizes 20-step rolling statistics observed during RLVR training. Its first/last      reasoning benchmarks. We also plan to calibrate verifier confidence, use symbolic feedback
20-step means are reward 0.86/0.90, P1 0.93/0.95, P2 0.67/0.75, and P3 0.53/0.74. The             earlier in candidate revision, and test robustness under paraphrased premises, altered
value near 0.94 therefore refers to sampled training-time P1, not the held-out values             numerical scales, and unit conversions, aiming to preserve the P3 gain while improving
reported in Tables II or IV. Together, the five plots separate RLVR’s reasoning-depth             correctness, consistency, and transfer.
shift, self-consistency’s variance reduction, and the physics verifier’s selective correctness         Beyond these extensions, a stronger evaluation protocol should quantify the stability of
gain.                                                                                             the observed gains across random seeds and alternative validation splits. In particular, the
G. Inference Results                                                                              seven-example Logic Uncertain subset is too small to support strong conclusions by itself,
                                                                                                  while physics dominates the held-out distribution and therefore has a disproportionate effect
    The final inference pipeline combines five-generation gold-free self-consistency with
                                                                                                  on overall P1. Future experiments will report confidence intervals, per-task calibration,
optional symbolic verification. One greedy and four sampled responses are grouped by
                                                                                                  and repeated runs so that changes in P1, P2, and P3 can be distinguished from sampling
answer equivalence, after which the selected physics response may be conservatively
                                                                                                  variation. We will also evaluate the verifier as an explicit selective-prediction component
checked by the question-only verifier. Fig. 4 presents six representative correct cases
                                                                                                  by measuring coverage, correction rate, regression rate, and confidence calibration rather
covering three logic and three physics output formats. Each case exposes the question,
                                                                                                  than accuracy alone.
premises or physical information, model answer, reasoning response, gold answer, and
                                                                                                       A second direction concerns efficiency and transfer. The current pipeline uses multiple
verification notes. The cases are selected only after generation for qualitative visualization;
                                                                                                  generations for gold-free self-consistency and invokes symbolic verification only on
gold labels are not available to clustering or the question-only verifier.
                                                                                                  supported high-confidence cases. We plan to study whether candidate count can be
                                                                                                  reduced adaptively when answer clusters agree early, and whether verifier routing can
                                                                                                  be learned with lower inference overhead. Finally, the same separation between answer
                                                                                                  correctness, supporting consistency, and reasoning depth can be tested on broader STEM
                                                                                                  domains and multilingual educational QA. Such experiments would clarify whether the
                                                                                                  present neural–symbolic design transfers beyond the EXACT setting while preserving the
                                                                                                  interpretability advantages of structured outputs and selective verification.
                                                                                                     Finally, we will study reward-weight sensitivity, reference regularization, verifier-
                                                                                                  confidence calibration, repeated-run uncertainty, and the latency/memory overhead of
                                                                                                  multi-candidate generation and symbolic checking so that reasoning gains can be assessed
                                                                                                  jointly with correctness and deployment cost.
                                                                                                                                          References
                                                                                                   [1] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. Chi, Q. V. Le, and
                                                                                                       D. Zhou, “Chain-of-thought prompting elicits reasoning in large language models,” in
                                                                                                       Advances in Neural Information Processing Systems, vol. 35, 2022.
Figure 4: Representative correct inference cases across six logic and                              [2] Qwen Team, “Qwen2.5 technical report,” arXiv preprint arXiv:2412.15115, 2024.
                                                                                                   [3] X. Wang, J. Wei, D. Schuurmans, Q. V. Le, E. H. Chi, S. Narang, A. Chowdhery, and
physics task formats.                                                                                  D. Zhou, “Self-consistency improves chain of thought reasoning in language models,” in
                                                                                                       International Conference on Learning Representations, 2023.
                                                                                                   [4] H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman,
   The qualitative cases complement the quantitative P1/P2/P3 analysis. Logic examples                 I. Sutskever, and K. Cobbe, “Let’s verify step by step,” arXiv preprint arXiv:2305.20050,
                                                                                                       2023.
make premise use directly inspectable, whereas physics examples expose the chosen                  [5] Z. Yu, N. Xu, K. Chen, J. Zhao, L. Wang, and W. Mao, “Scientific logicality enriched
                                                                                                       methodology for llm reasoning: A practice in physics,” arXiv preprint arXiv:2605.17104,
relation, numerical substitution, units, and verifier status. They also illustrate why the             2026.
metrics should not be collapsed: P1 can be correct while premise selection is incomplete,          [6] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. K. Li, Y. Wu, and
                                                                                                       D. Guo, “Deepseekmath: Pushing the limits of mathematical reasoning in open language
P2 can remain high despite a numerical answer error, and P3 can increase simply because                models,” arXiv preprint arXiv:2402.03300, 2024.
                                                                                                   [7] Y. Wang, Q. Yang, Z. Zeng, L. Ren, L. Liu, B. Peng, H. Cheng, X. He, K. Wang, J. Gao,
more reasoning steps are made explicit. The intended system therefore uses the LLM for                 W. Chen, S. Wang, S. S. Du, and Y. Shen, “Reinforcement learning for reasoning in
                                                                                                       large language models with one training example,” in Advances in Neural Information
general reasoning and reserves symbolic intervention for supported, verifiable cases.                  Processing Systems, 2025.
                                                                                                   [8] EXACT 2026, “The 2nd international xai challenge for transparent educational question-
           IV. CONCLUSION AND FUTURE WORK                                                              answering,” 2026, iJCNN 2026 Competition.
                                                                                                   [9] T. Dettmers, A. Pagnoni, A. Holtzman, and L. Zettlemoyer, “Qlora: Efficient finetuning
    We presented a verifier-guided framework combining gold-anchored QLoRA, task-                      of quantized llms,” arXiv preprint arXiv:2305.14314, 2023.
aware symbolic routing, self-revision, and group-relative RLVR for transparent educational        [10] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, and W. Chen, “Lora:
QA. It separately evaluates P1 final-answer correctness, P2 evidence/unit consistency,                 Low-rank adaptation of large language models,” arXiv preprint arXiv:2106.09685, 2021.
and P3 reasoning depth.                                                                           [11] W. Fedus, B. Zoph, and N. Shazeer, “Switch transformers: Scaling to trillion parameter
    On 438 held-out examples, RLVR raises P3 from 50.68% to 72.20%, while hybrid P1                    models with simple and efficient sparsity,” Journal of Machine Learning Research,
remains close to calibrated SFT (55.94% vs. 56.62%) and P2 is 75.33%. Five-generation                  vol. 23, no. 120, pp. 1–39, 2022.
gold-free self-consistency gives a modest model-only gain, whereas the conservative               [12] A. Q. Jiang, A. Sablayrolles, A. Roux et al., “Mixtral of experts,” arXiv preprint
                                                                                                       arXiv:2401.04088, 2024.
physics verifier yields the largest physics-P1 gain. Thus, RLVR mainly reshapes explicit          [13] L. de Moura and N. Bjørner, “Z3: An efficient smt solver,” in Tools and Algorithms for
reasoning, while symbolic verification selectively corrects high-confidence numerical                  the Construction and Analysis of Systems, ser. Lecture Notes in Computer Science, vol.
failures.                                                                                              4963. Springer, 2008, pp. 337–340.
    The current RLVR objective improves reasoning depth more strongly than answer
accuracy, and longer outputs can introduce premise, unit, or formatting inconsistencies.
