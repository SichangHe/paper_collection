                                             Conflict-Aware Fusion: Mitigating Logic Inertia in
                                             Large Language Models via Structured Cognitive
                                                                  Priors

                                                             Qiming Bao                                             Xiaoxuan Fu
                                                       Xtracta & Strong AI Lab,                                School of Humanities,
                                                        University of Auckland                                  China University of
                                                       Auckland, New Zealand                                 Political Science and Law
                                                     {bqmbill714}@gmail.com                                        Beijing, China
                                                                                                              {xfuuva}@gmail.com
                                                                                    Michael Witbrock
                                                                           Strong AI Lab, University of Auckland
                                                                                  Auckland, New Zealand
                                                                            {m.witbrock}@auckland.ac.nz
arXiv:2512.06393v8 [cs.AI] 19 Jul 2026




                                                                                         Abstract
                                                     Large language models (LLMs) achieve high accuracy on many reasoning bench-
                                                     marks but remain brittle under structural perturbations of rule-based systems. We
                                                     introduce a controlled diagnostic framework with four orthogonal stress tests—
                                                     redundant vs. essential rule deletion, contradictory-rule injection, logic-preserving
                                                     rewrites, and multi-law stacking—and use it to expose Logic Inertia: the systematic
                                                     tendency of generative LLMs (Qwen2/3, TinyLlama, GPT-4o, Gemma-3-4B-IT),
                                                     as well as the encoder-only BERT baseline, to persist along learned deductive
                                                     trajectories even when foundational premises are inconsistent. The collapse is
                                                     sharp: untreated baselines fall from accuracy 1.00 on the base task to 0.00 on
                                                     contradiction injection (instance-level exact match; see §3), and even GPT-4o
                                                     resolves only 56.0% of contradiction cases. We propose Conflict-Aware Fusion, a
                                                     four-stage training pipeline that enforces verification-before-deduction as a learned
                                                     structural prior: (i) SFT establishes the verification preamble; (ii) DPO sharpens
                                                     the halt-on-contradiction decision boundary; (iii) Logical Invariance REgularisa-
                                                     tion (LIRE) penalises divergence between logically equivalent rule formulations
                                                     via symmetric KL; and (iv) Reinforcement Learning from Verification Feedback
                                                     (RLVF) uses a symbolic forward-chaining engine as a deterministic oracle reward,
                                                     jointly optimising invariance and sensitivity. The pipeline saturates all four primary
                                                     stress tests for both 1.5B and 8B backbones. We further validate a Phase 2 exten-
                                                     sion in which the propositional oracle is replaced by a L EAN 4 kernel, attaining
                                                     99.0% kernel agreement on the 105 classically-derivable (T) questions within a
                                                     stratified 187-question Lean-translated sample (overall 71.7% across both polari-
                                                     ties; the T/F asymmetry is analysed in §5.2), providing a sound upgrade path to
                                                     formally verified RL training. The benchmark, training pipeline, and Lean verifier
                                                     are publicly released.1


                                         1    Introduction
                                         Although large language models (LLMs) perform strongly on many reasoning benchmarks, it
                                         remains unclear whether they genuinely perform logical inference or rely on pattern completion.
                                         The distinction matters in real-world deployments—legal analysis, scientific discovery, automated
                                             1 Code and data: https://github.com/14H034160212/lemo




                                         Preprint.
decisions—where reasoning agents must handle incomplete information, redundant evidence, and
explicit contradictions. Existing evaluations largely conflate linguistic competence with logical
robustness and lack controlled stress tests for these conditions.
We introduce a diagnostic framework that probes structural robustness through four perturbations: (1)
rule deletion (redundant vs. essential), (2) contradictory-rule injection, (3) logic-preserving rewrites,
and (4) multi-law stacking. Across three model families (BERT, Qwen2, TinyLlama) we uncover a
sharp asymmetry of robustness: models stay stable under semantics-preserving rewrites but collapse
to instance-level accuracy 0.0000 under explicit contradictions. We term this Logic Inertia—the
tendency to persist along a learned deductive trajectory under inconsistent premises. Concurrent work
surfaces closely related failure modes under different terminology—“cognitive inertia” [Lee et al.,
2026], premise critique [Li et al., 2025], RuleBreakers [Chan et al., 2025], Inverse IFEval [Zhang
et al., 2026], CodeCrash [Lam et al., 2025]—but does not isolate the structural cause with a controlled
propositional benchmark or close it with a learned structural prior; we do both. The same failure is
reproduced on the Humanity’s Last Exam platform2 .
To address it, we propose Conflict-Aware Fusion (Fusion-Conflict), grounded in the Cognitive
Structure Hypothesis: robust reasoning requires an explicit structural separation between premise
validation and deductive execution, operationalised via a structured generation path trained by
a four-stage pipeline (SFT → DPO → LIRE → RLVF). Our contributions are: (i) a diagnostic
benchmark and the formalisation of Logic Inertia as a structural failure mode reproduced across BERT,
Qwen2/3, TinyLlama, GPT-4o, and Gemma-3-4B; (ii) LIRE, a symmetric-KL regulariser applied
to autoregressive reasoning traces rather than the discriminative-QA setting of prior consistency
regularisers [Asai and Hajishirzi, 2020, Li et al., 2019]; (iii) RLVF, an RL reward formulation (not
a new optimiser) replacing RLHF’s learned reward with a deterministic symbolic-oracle reward in
the propositional regime—complementary to proof-assistant-grounded RL [Xin et al., 2024, Ji et al.,
2025, AlphaProof and AlphaGeometry Teams, 2024]; (iv) a sound L EAN 4 extension (RLVF-Lean)
elevating the oracle to a Lean kernel (99.0% kernel agreement on the 105 T-cases of a 187-question
stratified Lean-translated sample; Table 5); and (v) the Fusion-Conflict pipeline, which saturates the
held-out base/V2/V3 splits for both 1.5B and 8B backbones—versus untreated baselines at 0.250 on
V2 and 0.000 on V3, and GPT-4o/Gemma-3-4B-IT at 56.0%/43.9% on V3. The synthetic benchmark
is calibrated to expose Logic Inertia; the headline contrast is the collapse pattern of strong baselines,
not the absolute ceiling.

2    Related Work
Fragility of LLM reasoning. Prior work documents that LLMs fail on multi-step deduction,
abductive explanation, and compositional generalisation [Berglund et al., 2023, Bao et al., 2022,
Cheng et al., 2025, Clark et al., 2020, Bao et al., 2024a, Young et al., 2022, Bao, 2025]. The Reversal
Curse [Berglund et al., 2023] shows bidirectional inference failures, and reasoning fidelity degrades
under controlled task-structure and premise variations [Bao et al., 2024a, Bao, 2025]. Logic-driven
augmentation and neuro-symbolic hybrids partially mitigate these gaps via equivalence-based data
expansion [Wang et al., 2022, Bao et al., 2024b] or external Prolog engines [Wang et al., 2024], but
address the symptoms rather than the model’s intrinsic sensitivity to structural perturbations.

Self-correction and verification under false premises. Closer to our setting, Xiong et al. [2025]
cast reasoning as structure-aware planning with a learned world model, and Xiong et al. [2026]
scale search-augmented LLM reasoning via adaptive information control; Huang et al. [2023] probes
self-correction; Feng et al. [2026] prune invalid reasoning via neuro-symbolic verification; Shafiei
et al. [2025] expose multi-hop fragility under naturally-embedded false premises; Saad-Falcon et al.
[2024] evaluate RAG faithfulness; Li et al. [2025], Chan et al. [2025], Qin et al. [2025] probe
premise-level evaluation and retrieval-augmented halting. We complement this line by isolating the
architectural root cause—Logic Inertia, distinct from the latent-dynamics “Cognitive Inertia” of Lee
et al. [2026] and the instruction-inertia of Zhang et al. [2026]—and by closing it with a structural
prior trained into the policy rather than elicited at inference.

Verifier-grounded RL and consistency regularisation. Proof-assistant feedback is an established
RL reward source for theorem proving [Xin et al., 2024, Ji et al., 2025, AlphaProof and AlphaGeom-
    2 https://lastexam.ai/




                                                   2
etry Teams, 2024]; RLVF-Lean is the propositional-reasoning analogue, with the kernel arbitrating
premise-verification halts rather than full proofs. A related but distinct line uses a symbolic logic
verifier to construct step-wise-supervised SFT/DPO training data rather than an online RL reward [Xu
et al., 2026]. Symmetric-KL consistency regularisation has prior art in discriminative QA [Asai and
Hajishirzi, 2020, Li et al., 2019]; a related but distinct line applies counterfactual, operator-level
sensitivity regularisation to reasoning faithfulness [Akter et al., 2026]; LIRE applies the symmetric-
KL idea at the autoregressive trace level under logically equivalent rule rewrites, where the target is
invariance across surface forms of the same proposition.

3     Methodology
Conflict-Aware Fusion (Fusion-Conflict) integrates three components: (1) a structural robustness
benchmark, (2) a two-phase generation path that enforces verification-before-deduction, and (3) a
structure-aligned four-stage optimisation pipeline.

3.1   Structural Robustness Benchmark

The benchmark is both a diagnostic tool and a training corpus. Unlike conventional benchmarks
composed of heterogeneous tasks, all evaluation instances are derived from a single canonical rule-
based system with systematically controlled perturbations; each variant preserves domain semantics
and vocabulary while differing only in structural properties, isolating reasoning robustness from
domain shift.

Canonical backbone and perturbations. All instances are derived from a single canonical back-
bone (full base example in Appendix A.8) and probed along four orthogonal axes: (1) structural ne-
cessity sensitivity—redundant vs. essential rule deletion; (2) consistency verification—contradictory-
rule injection; (3) logical-form invariance—semantics-preserving rewrites (De Morgan, contraposi-
tive, double negation, . . .); and (4) compositional robustness—stacked rewrites.

Benchmark generation (Variant 2 & 3). We generate all instances from a single canonical rule-
based template (canonical backbone) and create hard structural variants by controlled perturbations
that preserve surface vocabulary and domain semantics. Given a base instance (F, R, Q) (facts,
rules, and a fixed set of yes/no queries), we construct: Variant 2 by removing a key rule on the
main deduction chain, which breaks downstream entailments; and Variant 3 by injecting an explicit
contradictory fact, which forces the model to detect inconsistency and halt/reject deduction. All
splits are serialized into a unified CSV schema containing facts, rules, questions, and answers.
Other variants are deferred to the Appendix.

Contradiction Semantics. In this work we adopt a conservative reasoning semantics for handling
inconsistent premises. When a contradiction exists in the premise set, the reasoning process is
considered logically invalid and deduction must halt. Consequently, all queries associated with that
instance are labeled False.
Formally, let Γ denote the set of premises and Q the set of queries; the symbol ⊢ refers throughout
to derivation under our forward-chaining engine on Horn-clause rules (Algorithm 1), not classical
⊢CL which would explode under contradiction. If the premises entail a contradiction (Γ ⊢ ⊥), then
for every query q ∈ Q we define Label(q) = False. This design enables contradiction detection to
be evaluated using a standard binary classification metric while maintaining a clear and consistent
reasoning semantics.

Accuracy and SRmacro . Tables 1–3 use instance-level exact match: an instance is correct iff every
query prediction matches the variant’s label. Under the conservative semantics above, every Variant 3
query has label F; an untreated model that persists with its original deductive answers disagrees on at
least one query,Pso instance accuracy collapses to 0.0000. The structural-robustness macro score is
             1
SRmacro = |V|      v∈V Accv over V = {base, V1, V2, V3, V4-multi}. The per-question labels in the
Lean-translation study (Table 5) are the classical (pre-override) polarities, which is why Variant 3
still contains 12 classically-derivable T-questions even though the conservative-semantics instance
label is F.


                                                  3
Pseudocode for variant generation is in Appendix A.2. Although all instances are derived from a
shared canonical template, the compositional variation in rule structures and query combinations
induces diverse reasoning paths, preventing trivial memorisation.

3.2   Architectural Overview: Structured Two-Phase Generation

The core design imposes a two-phase reasoning structure—verify, then deduce—inside the Chain-
of-Thought (CoT) generation path; this is a constraint on the trace, not a modification of the neural
architecture. Deductive rules cannot be applied until the model has explicitly validated premise
consistency (Figure 1); on detected contradiction or missing dependency the model halts. The
four-stage pipeline that trains this behaviour is detailed in §3.3.

                   Running Example        Facts: Socrates is a man.     Rule: All men are mortal.   New Fact: Socrates is NOT mortal.


                   Stage 1: Structural SFT        LCE                                               Stage 2: DPO Alignment          LDPO


         “Step 1: Verify facts. Check premise consistency.                 1→2
                                                                                             Preferred yw :                         Rejected yl :
          Step 2: If consistent → proceed with deduction.                                 “Conflict detected!                   “Consistent.
                        If contradiction → HALT.”                                          HALT.” → False                  Deduce Mortal.” → True



         Learns mandatory verification-before-deduction preamble                              Sharpens halt-on-contradiction decision boundary
                                                                                 2→3

                    Stage 3: LIRE      LCE + λ Linv                                                      Stage 4: RLVF       LRLVF

                                                                                                          Oracle F ORWARD C HAIN:
              Base rule:                        Contrapositive:                            {Man, Mortal, ¬Mortal} ⊢ ⊥           ⇒       a∗ = False
                               Sym. KL ≈ 0                                 3→4
       “All men are mortal”                   “All non-mortals
             πθ (·|x)                      are non-men” πθ (·|x̃)
                                                                                           Model samples as = False         ⇒ reward r = +1
                                                                                                          (correct answer reinforced)

      Symmetric KL enforces invariance across equivalent formulations                      Oracle reward jointly balances invariance and sensitivity


Figure 1: Conflict-Aware Fusion architecture and four-stage optimization pipeline, illustrated through
a running Socrates contradiction example. Stage 1 (top-left, SFT) teaches a mandatory verification-
before-deduction preamble. Stage 2 (top-right, DPO) sharpens the halt boundary by preferring the
correct “Halt” trace over naïve deduction. Stage 3 (bottom-left, LIRE) enforces output-distribution
invariance across logically equivalent rule formulations via symmetric KL divergence. Stage 4
(bottom-right, RLVF) uses a symbolic forward-chaining oracle as a deterministic reward, jointly
optimizing invariance and sensitivity.


3.3   Structure-Aligned Optimization Pipeline

The four stages progressively address distinct failure modes: (1) SFT establishes the verification-
before-deduction structure; (2) DPO sharpens the halt-on-contradiction boundary; (3) LIRE enforces
consistency across logically equivalent formulations; (4) RLVF reconciles the invariance–sensitivity
trade-off via oracle-grounded reward.

Stage 1: Structural SFT. Supervised fine-tuning on 11,200 instances spanning canonical, per-
turbed, and contradiction-containing variants. All samples enforce a mandatory “Step 1: Verify facts”
preamble, establishing premise checking as a default procedural step rather than an optional response.

Stage 2: Logical Alignment via DPO. We refine the policy with Direct Preference Optimi-
sation [Rafailov et al., 2023]: preference pairs contrast halt-on-contradiction traces yw against
opportunistic deductive continuations yl . Let πθ denote the policy and πref the frozen reference
model:                                                                        
                                                 θ (yw |x)         πθ (yl |x) 
                        LDPO = − log σ β log ππref  (yw |x) − log πref (yl |x)   .             (1)
β controls the KL strength against πref .
Preference pairs are generated automatically from benchmark instances: for contradiction cases the
preferred trace halts after detecting the inconsistency, while the rejected trace continues deductive in-


                                                                             4
ference (full templates in Appendix A.3). This construction directly penalises deductive continuation
over inconsistent premises.

Limitation of SFT+DPO. While Stages 1–2 internalize the verification-before-deduction structural
prior, they remain vulnerable to a subtler failure mode: surface-level pattern matching. A model
trained only with SFT and DPO can achieve perfect accuracy on the original rule formulations yet
drop sharply (e.g., from 1.000 to 0.327 on De Morgan variants) when logically equivalent rules are
rephrased. This motivates the two subsequent stages, which operate at the output-distribution level
rather than at the trace level.

Stage 3: Logical Invariance REgularisation (LIRE). Let x be a base premise-rule input, x̃ its log-
ically equivalent reformulation (De Morgan, double-negation, contrapositive), and y = (y1 , . . . , yT )
the gold trace from the SFT data. LIRE penalises divergence between the next-token distributions
under the two inputs, evaluated by teacher-forcing the same gold y on both branches (which aligns
the distributions token-wise and avoids variable-length rollout mismatch):
                                                      T
                                                      X
                                                    1
                                                                              
         LLIRE = LCE πθ (·|x), y + λ Linv , Linv = 2T    KLt (x∥x̃) + KLt (x̃∥x) ,                  (2)
                                                              t=1
                                                       
where KLt (x∥x̃) := KL πθ (·|x, y<t ) ∥ πθ (·|x̃, y<t ) . Symmetry avoids the mode-seeking/covering
asymmetry of unidirectional KL; the shared y keeps the KL exact rather than approximated.

Limitation of LIRE. LIRE improves invariance (Variant 4 accuracy 0.741 → 0.999) but suppresses
any distribution shift across rule reformulations, including those that should change the answer
(Variants 2/3). Empirical sensitivity drops from 1.0 to 0.47, motivating Stage 4.

Stage 4: RLVF—Reinforcement Learning from Verification Feedback. RLVF is a verifier-
grounded RL reward formulation (not a new optimiser): plain REINFORCE [Williams, 1992] drives
the gradient, but the reward is a deterministic symbolic oracle replacing RLHF’s learned reward
model, eliminating reward-model bias on the rule-based regime. The policy emits a full reasoning
trace τ ∼ πθ (·|x); a deterministic parser Π(τ ) ∈ {T, F} extracts the boolean answer from the final
Step N: Answer = ... line (regex-matched; unparseable traces get r = −1). The oracle returns
a∗ = F ORWARD C HAIN(x) and reward compares parsed answer to oracle:
LRLVF = −Eτ ∼πθ (r−bt ) log πθ (τ |x) , r = ⊮[Π(τ )=a∗ ]−⊮[Π(τ )̸=a∗ ], bt = µbt−1 +(1−µ)r̄t ,
                                         
                                                                                                 (3)
where r̄t is the mean reward on mini-batch Bt and µ = 0.99. A single reward balances both objectives
because the oracle naturally distinguishes equivalent reformulations (V4: same a∗ ⇒ invariance)
from structural alterations (V2/V3: different a∗ ⇒ sensitivity). Each batch is composed of fraction
α = 0.5 perturbation samples (uniformly from V2∪V3∪V4) and 1−α = 0.5 base samples, balancing
sensitivity, invariance, and base-task retention.

4     Experiments
4.1   Main Results

Table 1 reports the baseline failure pattern: all models stay at 1.000 on the base task and Variant 1,
drop to 0.25–0.295 under essential-rule removal (Variant 2), and collapse to 0.000 under explicit
contradictions (Variant 3)—direct evidence of Logic Inertia.
Table 2 summarises Fusion-Conflict against six baselines on Qwen2-1.5B (the most stable backbone
for generative reasoning) and Qwen3-8B. All reported numbers are the mean over three random seeds
with bootstrap CIs ±0.02 (n=1000).

4.2   Qualitative Analysis: Why Frontier Models Fail

To understand the failure mode of frontier models, we performed an error analysis on GPT-4o using
the OpenAI API on a stratified 200-row sample per split (the per-question prediction CSVs are
released alongside the benchmark). On Variant 3, where every query has ground-truth False under


                                                   5
                                                   BERT                  Qwen2             TinyLlama
        Split                                Acc           ∆         Acc         ∆       Acc          ∆
        base                               1.0000      0.0000       1.0000     0.0000   1.0000      0.0000
        variant1                           1.0000      0.0000       1.0000     0.0000   1.0000      0.0000
        variant2 (Essential Deletion)      0.2950     -0.7050       0.2500    -0.7500   0.2500      -0.7500
        variant3 (Contradiction)           0.0000     -1.0000       0.0000    -1.0000   0.0000      -1.0000
        variant4-multi (Stacked Laws)      1.0000      0.0000       0.6450    -0.3550   0.9925      -0.0075

Table 1: Baseline Performance: Accuracy and deviation (∆) across structural variants without fusion
optimization.


Table 2: Comparison of All Methods. Fusion-Conflict architectures maintain structural robustness
(SRmacro = 1) while significantly improving general logic performance over SFT/DPO baselines.
Statistical stability verified via bootstrap resampling (n = 1000), with 95% CIs consistently within
±0.02.
 Method                                          Base Acc      Var 2 (Rule Removal) Var 3 (Contradiction)     Rank
 Stage 1 (SFT Baseline)                            0.512              0.250                 0.210              7
 DPO (Direct Alignment) Rafailov et al. [2023]     0.475              0.267                 0.510              6
 CoT (Standard) Wei et al. [2022b]                 0.500              0.390                 0.865              5
 Mixed-Aug (Data Augmentation without CoT)         0.525              0.405                 0.972              4
 RA-CoT (Standard CoT + DPO)                       0.263              0.593                 0.690              3
 Fusion-LRA (Conflict-Aware SFT)                   0.988              0.753                 0.705              2
 Fusion-Conflict (1.5B)                            1.000              1.000                 1.000              1
 Fusion-Conflict (Qwen3-8B)                        1.000              1.000                 1.000              1
 GPT-4o (Closed Frontier Baseline)                 0.789              0.818                 0.560              —
 Gemma-3-4B-IT (Open Frontier Baseline)            0.580              0.360                 0.439              —




conservative reasoning semantics, GPT-4o produces the correct halt-on-contradiction answer in
only 56.0% of the 800 test questions; the remaining 44.0% continue deductive inference despite the
explicit contradiction in the premises. A representative failure: given premises {A → B, A, ¬B},
GPT-4o often surfaces the inconsistency in its verification trace and then proceeds to conclude B from
{A → B, A}, stating “Since A is true and A implies B, then B must be true,” effectively ignoring its
own prior verification of ¬B. This suggests that frontier models suffer from a compartmentalization
of verification and execution, where the “reasoning momentum” of the deductive steps overrides
contradictory evidence. To rule out a vendor-specific artefact, we replicate the analysis on Gemma-3-
4B-IT (an open-weight frontier model from a different lab, evaluated locally with identical prompts
and decoding); it scores lower on V3 (0.439) than GPT-4o, continuing past the contradiction in 56.1%
of cases, and shows the same qualitative failure pattern. Fusion-Conflict mitigates this by fusing the
verification signal directly into the hidden state representation, forcing the model to reconcile the
conflict before proceeding.


4.3   Experimental setup

The benchmark has 100 base groups (80 train / 20 test) seeded into a combinatorially large hypothesis
space via randomised entity mapping and rule variation, yielding ≈ 11,200 Stage-2 preference
pairs. Out-of-template generalisation is evaluated on LogicNLI and MNLI-Con (Table 4). Per-stage
hyperparameters: Stage 1 SFT uses AdamW + bf16 + LoRA (r=8, α=16, dropout 0.05), 3 epochs,
batch 4, LR 2×10−5 , max length 512. DPO uses β=0.1 at the same LR. LIRE uses λ=1.0, batch 4,
grad-accum 2. RLVF mixes V2/V3/V4 at α=0.5, µ=0.99, LR 1×10−5 , batch 8, grad-accum 4.
Full ablation tables are in Appendix A.5; all hyperparameters in Appendix A.4. Compute. All
training fits on a single NVIDIA A100 (40 GB) for Qwen3-8B and a ≥ 16 GB consumer GPU for the
1.5B/0.5B/1.1B/BERT backbones (LoRA + bf16); Lean kernel verification adds ∼ 0.36 s/trace on
CPU and is dispatch-amortisable via a persistent server [Yang et al., 2023].


                                                           6
4.4    Stage-wise ablation: each stage addresses a distinct failure mode

Table 3 reports the per-stage progression on the four most diagnostic splits (base, V2 essential
deletion, V3 contradiction, V4-multi compositional rewrites) for both backbones, isolating exactly
what each training stage contributes.
Table 3: Stage-wise progression. Adding LIRE on top of SFT improves compositional invariance
(V4-multi: 0.635→0.993 on Qwen2; 0.006→1.000 on Qwen3) but collapses structural sensitivity
on V2/V3, exactly the trade-off motivated in Section 3.3. RLVF then restores V2/V3 to oracle-level
agreement on the held-out split. On the 1.5B backbone V4-multi degrades from 0.993 (Stage 3) to
0.773 (Stage 4)—a real residual of the invariance/sensitivity trade-off that LIRE alone cannot resolve
at this capacity—while on 8B the Stage-4 V4-multi remains at the LIRE ceiling (1.000); we report
the gap rather than claim “no loss”. The Qwen3-8B first row is the SFT-only baseline (Stage 1), not
an untrained zero-shot run; even with Stage 1 internalised, V3 stays at 0.656, supporting the claim
that scale and SFT alone do not solve Logic Inertia, while the same split drives every baseline below
it—including GPT-4o on V3 at 0.560—well below ceiling.

                                      Qwen2-1.5B                             Qwen3-8B
    Stage                  Base      V2     V3         V4-multi   Base      V2    V3         V4-multi
    SFT+DPO (Stage 1+2)   1.000    1.000    1.000       0.635     0.333   0.460     0.656     0.006
    + LIRE (Stage 3)      0.812    0.590    0.344       0.993     0.549   0.503     0.344     1.000
    + RLVF (Stage 4)      1.000    1.000    1.000       0.773     1.000   1.000     1.000     1.000

Three observations follow. (i) LIRE alone is harmful on V2/V3 because its symmetric-KL term
suppresses any distribution shift across rule reformulations, including those required by genuine
logical change—a clean empirical instance of the invariance–sensitivity trade-off (Eq. 2). (ii) RLVF
resolves this with a single oracle reward (Eq. 3): the same gradient signal reinforces V4 invariance
and V2/V3 sensitivity. (iii) The Qwen3-8B row shows scale + Stage-1 SFT remains insufficient—
SFT-only 8B falls to 0.656 on V3—evidence that Logic Inertia is structural, not capacity-bound,
consistent with the debate over whether apparent scale-driven capability jumps are genuine emergent
abilities [Wei et al., 2022a] or measurement artefacts [Schaeffer et al., 2023]: either way, scale
alone does not resolve it here. Note that the two “Stage 1” numbers reported are not contradictory:
Fusion-LRA in Table 2 (Base 0.988) is SFT with the conflict-aware preamble; the 0.525 entry in
Appendix A.5 is the same backbone trained on a vanilla Mixed-Aug corpus without the preamble.
The preamble, not the data mix, preserves base accuracy.

5     Discussion
Why DPO matters. SFT alone (Fusion-LRA) plateaus at 0.705 on V3—it teaches the form of
contradiction check but still occasionally hallucinates success. DPO sharpens the halt boundary and
saturates V3, casting preference optimisation as a robustness hardener, not a marginal improvement.

Why RLVF, not PPO/GRPO? Modern RLHF stacks (PPO [Schulman et al., 2017], GRPO [Shao
et al., 2024]) presuppose a learned reward model trained on human preferences, which inherits
annotator noise and distribution shift, and a clipped trust-region update to stabilise training against
that noisy reward. Our setting is fundamentally different: the ground truth on V2/V3/V4 is exactly
computable by a symbolic forward-chainer, so the reward is unbiased and deterministic. This removes
the dominant motivation for PPO’s clipping and for GRPO’s group-relative advantage normalisation.
RLVF therefore uses plain REINFORCE with an EMA baseline (Eq. 3); the contribution is the
reward formulation, not the optimiser. Plain REINFORCE is sufficient because (i) variance of the
gradient is small when the reward is ±1 deterministic, (ii) the EMA baseline already captures the
running mean, and (iii) there is no reward hacking surface for the policy to exploit. Empirically,
this single-reward formulation jointly optimises invariance (V4) and sensitivity (V2/V3) without
the multi-objective balancing that learned-reward setups require, recovering most of the gains LIRE
alone sacrificed (Table 3); a residual V4-multi loss remains at the 1.5B scale, as discussed below the
table. The RLVF-L EAN extension (Section 5.2) is the propositional-reasoning analogue of proof-
assistant-grounded RL pipelines [Xin et al., 2024, Ji et al., 2025, AlphaProof and AlphaGeometry
Teams, 2024]: it generalises the oracle to step-level rewards from a Lean 4 kernel, preserving the
unbiased-oracle property at proof granularity.


                                                   7
Cognitive Structure Hypothesis. Fusion-Conflict dominates both data-balanced (Mixed-Aug,
0.972 V3 / 0.525 base) and over-conservative (RA-CoT, 0.690/0.263) baselines, indicating that
reliability follows from structural organisation—the verification preamble is a circuit breaker—not
from data exposure alone.

Train- vs. inference-time mitigation. Unlike inference-time guards [Feng et al., 2026, Xiong et al.,
2025, Qin et al., 2025] that re-invoke a verifier on every deployment query, our structural prior is
amortised into the policy weights at training time, so V2/V3 robustness incurs zero runtime overhead;
the Phase 2 Lean kernel (§5.2) is required only during training, not at inference.

5.1   Generalisation and Sensitivity

Fusion-Conflict retains base-split accuracy under Variant 1 (redundant deletion), confirming that
contradiction detection does not introduce noise fragility, and saturates the held-out base/V2/V3 splits
for both backbones (Table 2)—versus GPT-4o 56.0% on V3 and the strongest non-Fusion baseline
(Fusion-LRA) at 0.705. The headline is the gap, not the absolute. Variant 4 multi-law stacking
remains the hardest split: 2–5 stacked rewrites degrade the 1.5B backbone to 0.773 while 8B closes
the gap. The residual at 1.5B is concentrated on instances composing ≥ 3 laws (contrapositive ◦
double-negation ◦ De Morgan), where the policy holds the structural prior but loses syntactic tracking;
this is a capacity bottleneck rather than a failure of the prior, since the same policy at 8B saturates
V4-multi. RLVF-Lean (§5.2) is the natural fix for this regime: per-tactic verification grounds each
rewrite step independently of overall trace length.

Out-of-distribution transfer. To rule out memorisation we evaluate transfer to LogicNLI Tian et al.
[2021] and the contradiction subset of MNLI Williams et al. [2018]; no LogicNLI/MNLI examples
were used in training. The transfer model is a Qwen2.5-0.5B trained with the full four-stage pipeline;
Table 4 reports each named ablation along the pipeline (Standard SFT = vanilla; Mixed-Aug =
data augmentation only; Fusion-LRA = Stage 1 with the preamble; Conflict-Aware Fusion = full
pipeline). Every variant requires “Step 1: Detect Contradiction” before entailment classification.

             Method                                          LogicNLI      MNLI (Con)
             Standard SFT (Baseline)                      58.5%            34.1%
             Mixed-Aug (Data Only)                        65.2%            41.5%
             Fusion-LRA (No DPO)                          92.4%            78.3%
             Conflict-Aware Fusion (Fusion-Conflict)      98.2%            89.4%
Table 4: Out-of-domain generalisation performance on LogicNLI and MNLI (no in-domain training)
contradiction subsets. “MNLI (Con)” refers to accuracy specifically on the contradiction subset
of the Multi-Genre NLI dataset, which tests the model’s ability to reject inconsistent premises in
open-domain text.

The structural prior generalises beyond synthetic logic to natural-language NLI; the design is model-
agnostic and applicable to larger backbones.

5.2   Phase 2: Scaling the Verifier with a Formal Proof Assistant

The propositional F ORWARD C HAIN oracle (Eq. 3) cannot verify quantified reasoning, induction,
or mathematical derivations [Davis, 2024a,c,b], motivating a formal-proof-assistant verifier as the
natural successor.

Lean as a step-level reward source. The Phase 2 extension RLVF-Lean translates the policy’s
CoT into L EAN 4 [de Moura and Ullrich, 2021] tactic applications and uses kernel verdicts as
step-level rewards:          
                             +1 L EAN K ERNEL(τ≤t ) = success
                       rt = −1 tactic fails or introduces inconsistency                           (4)
                             
                               0     trace incomplete
This converts RLVF’s sparse terminal reward into a dense, step-grounded signal akin to process reward
models [Lightman et al., 2024] but with the soundness of a kernel: every L EAN K ERNEL verdict is a


                                                   8
deductive check, not a prediction—unlike learned reward models or noisy human feedback in RLHF.
Lean is complementary to F ORWARD C HAIN in expressiveness (dependent types/quantifiers/induction
vs. Horn clauses), granularity (per-tactic verdicts), and compositionality, and is feasible end-to-end
given recent neural theorem proving [Yang et al., 2023, Polu and Sutskever, 2020, AlphaProof and
AlphaGeometry Teams, 2024].

Pilot study. A hand-crafted pilot on the Socrates example (8 traces; Appendix A.6/A.7) achieves 8/8
kernel agreement at 0.36 s/trace on CPU. One non-trivial finding: Lean’s sorry exits 0, so the bridge
treats sorry/admit as −1; production deployment would amortise dispatch via a L EAN D OJO [Yang
et al., 2023] persistent server.

Benchmark-scale verification. We auto-translated a stratified 80-row (187-question) sample from
the four test splits into Lean 4 theorems via a rule-based translator (lean_demo/lemo_to_lean.py)
that instantiates each rule/fact/query as a Prop, performs ∨-elimination on disjunctive premises, and
chains have statements. Table 5 reports Lean’s agreement with the benchmark labels.

Table 5: Lean 4 verification on real LEMO benchmark rows (20 rows per split, stratified random
sample; 187 total questions). Polarity here is each query’s classical label (i.e. the truth value
derivable from premises before the conservative-semantics override of §3), not the per-instance
“everything-is-F” override applied to Variant 3 in Tables 1–3. This is why Variant 3 still contains
12 classically-derivable T-cases. We report the number of questions (#T, #F), the count accepted
by Lean, and the agreement rate, separated by ground-truth polarity. T-cases are auto-derived via
mechanical forward chaining; F-cases are attempted via classical negation. Variant 1 happens to
draw all-T queries because the underlying test_variant1.csv file is constructed by removing
redundant rules, which preserves derivability of the original T-queries; the stratified sampler observed
42 such queries and zero F-queries in the 20-row draw. The gap between T-rate (99.0%) and F-rate
(36.6%) reflects a semantic mismatch between LEMO’s closed-world reasoning and Lean’s classical
logic, discussed below.

                                             Ground truth = T           Ground truth = F
            Split                          #T    Accept       Rate   #F    Accept      Rate
            base                            29         28    96.6%    32        12   37.5%
            variant1 (redundant removal)    42         42   100.0%     0         0       —
            variant2 (essential removal)    22         22   100.0%    20         0    0.0%
            variant3 (contradiction)        12         12   100.0%    30        18   60.0%
            Overall                        105      104     99.0%     82        30   36.6%


Interpretation: closed-world vs. classical semantics. The 99.0% agreement on T-cases is strong
evidence that Lean soundly verifies the multi-step forward-chaining derivations that RLVF
rewards: for nearly every query whose answer follows from the premises, Lean kernel-checks an
automatically generated proof. The asymmetric 36.6% rate on F-cases exposes a genuine, publishable
distinction: LEMO uses a closed-world semantics in which a claim is labelled F whenever it is
not derivable from the premises (including the degenerate case of contradictory premises, where
conservative reasoning labels everything F); Lean uses classical open-world semantics where F
requires an explicit proof of ¬P . Variant 2 (essential-rule removal) makes this gap stark—0% F-
rate—because removing a rule simply makes a conclusion unreachable, not refutable. A production
RLVF-Lean system can close this gap in two ways: (i) add a closed-world axiom (CWA) schema
that converts “unreachable” to ¬ -derivable, or (ii) follow the symbolic forward-chain oracle for
F-verdicts and use Lean only for T-verdict step-level reward. Our current pipeline implements option
(ii), retaining the best of both verifiers.

6    Conclusion

We diagnosed Logic Inertia—a structural failure mode in which generative LLMs (Qwen2/3,
TinyLlama, GPT-4o, Gemma-3-4B-IT) and the encoder-only BERT baseline persist along learned
deductive trajectories under essential-rule deletion and contradictions—and closed it with two named


                                                   9
contributions: LIRE, a symmetric-KL invariance regulariser applied at the trace level via teacher-
forcing on logically equivalent rule reformulations, and RLVF, an RL reward formulation (not
a new optimiser) whose deterministic symbolic-oracle reward replaces RLHF’s learned reward
model and admits a plain REINFORCE update. Combined in the Conflict-Aware Fusion pipeline
(SFT→DPO→LIRE→RLVF), they saturate the held-out base/V2/V3 splits for both 1.5B and 8B
backbones on a benchmark where GPT-4o resolves only 56.0% of V3 contradictions and Gemma-3-
4B-IT only 43.9%. The Phase 2 RLVF-L EAN extension upgrades the oracle to a Lean 4 kernel: on a
stratified 187-question Lean-translated sample, 99.0% of the 105 classically-derivable T-cases close
under the kernel; the 36.6% rate on the 82 F-cases reflects the closed-world / classical semantics gap
analysed in §5.2.
Code, benchmark, and verifier are released; a dedicated discussion of limitations and concrete future
work is consolidated in Appendix A.1.

References
Sanjeda Akter, Ibne Farabi Shihab, and Anuj Sharma. Causal consistency regularization: Training
  verifiably sensitive reasoning in large language models. In Proceedings of the 64th Annual Meeting
  of the Association for Computational Linguistics (ACL), 2026. arXiv:2509.01544.
AlphaProof and AlphaGeometry Teams. AI achieves silver-medal standard solving International
  Mathematical Olympiad problems. Google DeepMind Blog, 2024. URL https://deepmind.
  google/discover/blog/ai-solves-imo-problems-at-silver-medal-level/.
Akari Asai and Hannaneh Hajishirzi. Logic-guided data augmentation and regularization for con-
  sistent question answering. In Annual Meeting of the Association for Computational Linguistics
 (ACL), 2020.
Qiming Bao. Developing and Assessing Language Models for Logical Reasoning over Natural
  Language. PhD thesis, University of Auckland, 2025.
Qiming Bao, Alex Yuxuan Peng, Tim Hartill, Neşet Tan, Zhenyun Deng, Michael Witbrock, and
  Jiamou Liu. Multi-step deductive reasoning over natural language: An empirical study on out-of-
  distribution generalisation. In Proceedings of the 16th International Workshop on Neural-Symbolic
  Learning and Reasoning (NeSy), 2022.
Qiming Bao, Gaël Gendron, Alex Yuxuan Peng, Wanjun Zhong, Neşet Tan, Yang Chen, Michael
  Witbrock, and Jiamou Liu. Assessing and enhancing the robustness of large language models with
  task structure variations for logical reasoning. In Proceedings of the International Conference on
  Neural Information Processing (ICONIP), 2024a. arXiv:2310.09430.
Qiming Bao, Alex Yuxuan Peng, Zhenyun Deng, Wanjun Zhong, Gaël Gendron, Timothy Pistotti,
  Neşet Tan, Nathan Young, Yang Chen, Yonghua Zhu, Paul Denny, Michael Witbrock, and Jiamou
  Liu. Abstract meaning representation-based logic-driven data augmentation for logical reasoning.
  In Findings of the Association for Computational Linguistics (ACL), 2024b.
Lukas Berglund, Meg Tong, Max Kaufmann, Mikita Balesni, Asa Cooper Stickland, Tomasz Korbak,
  and Owain Evans. The reversal curse: LLMs trained on “A is B” fail to learn “B is A”. arXiv
  preprint arXiv:2309.12288, 2023.
Jason Chan, Robert Gaizauskas, and Zhixue Zhao. RULEBREAKERS: Challenging LLMs at
  the crossroads between formal logic and human-like reasoning. In Proceedings of the 42nd
  International Conference on Machine Learning (ICML), 2025. arXiv:2410.16502.
Fengxiang Cheng, Haoxuan Li, Fenrong Liu, Robert van Rooij, Kun Zhang, and Zhouchen Lin.
  Empowering LLMs with logical reasoning: A comprehensive survey. In Proceedings of the 34th
  International Joint Conference on Artificial Intelligence (IJCAI), 2025.
Peter Clark, Oyvind Tafjord, and Kyle Richardson. Transformers as soft reasoners over language. In
  Proceedings of the 29th International Joint Conference on Artificial Intelligence (IJCAI), 2020.
Ernest Davis. Benchmarks for automated commonsense reasoning: A survey. ACM Computing
  Surveys, 56(4):Article 81, 2024a.


                                                 10
Ernest Davis. Testing GPT-4-o1-preview on math and science problems: A follow-up study. arXiv
  preprint arXiv:2410.22340, 2024b.
Ernest Davis. Mathematics, word problems, common sense, and artificial intelligence. Bulletin of the
  American Mathematical Society, 61(2):287–303, 2024c.
Leonardo de Moura and Sebastian Ullrich. The Lean 4 theorem prover and programming language.
  In Proceedings of the 28th International Conference on Automated Deduction (CADE), pages
  625–635, 2021.
Yu Feng, Nathaniel Weir, Kaj Bostrom, Sam Bayless, Darion Cassel, Sapana Chaudhary, Benjamin
  Kiesl-Reiter, and Huzefa Rangwala. VeriCoT: Neuro-symbolic chain-of-thought validation via
  logical consistency checks. In International Conference on Learning Representations (ICLR),
  2026. arXiv:2511.04662.
Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song,
   and Denny Zhou. Large language models cannot self-correct reasoning yet. arXiv preprint
   arXiv:2310.01798, 2023.
Xingguang Ji, Yahui Liu, Qi Wang, Jingyuan Zhang, Yang Yue, Rui Shi, Chenxi Sun, Fuzheng Zhang,
  Guorui Zhou, and Kun Gai. Leanabell-Prover-V2: Verifier-integrated reasoning for formal theorem
  proving via reinforcement learning. arXiv preprint arXiv:2507.08649, 2025.
Man Ho Lam, Chaozheng Wang, Jen-tse Huang, and Michael R. Lyu. CodeCrash: Exposing LLM
 fragility to misleading natural language in code reasoning. In Advances in Neural Information
 Processing Systems (NeurIPS), 2025. arXiv:2504.14119.
Seojin Lee, ByeongJeong Kim, and Hwanhee Lee. Mitigating cognitive inertia in large reasoning
  models via latent spike steering. arXiv preprint arXiv:2601.22484, 2026.
Jinzhe Li, Gengxu Li, Yi Chang, and Yuan Wu. Don’t take the premise for granted: Evaluating the
   premise critique ability of large language models. In Findings of the Association for Computational
   Linguistics (EMNLP), 2025. arXiv:2505.23715.
Tao Li, Vivek Gupta, Maitrey Mehta, and Vivek Srikumar. A logic-driven framework for consistency
  of neural models. In Conference on Empirical Methods in Natural Language Processing (EMNLP),
  2019.
Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan
  Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. In International
 Conference on Learning Representations (ICLR), 2024.
Stanislas Polu and Ilya Sutskever. Generative language modeling for automated theorem proving.
  arXiv preprint arXiv:2009.03393, 2020.
Yuehan Qin, Shawn Li, Yi Nian, Xinyan Velocity Yu, Yue Zhao, and Xuezhe Ma. Don’t let
  it hallucinate: Premise verification via retrieval-augmented logical reasoning. arXiv preprint
  arXiv:2504.06438, 2025.
Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, and Chelsea
  Finn. Direct preference optimization: Your language model is secretly a reward model. Advances
  in Neural Information Processing Systems (NeurIPS), 36, 2023.
Jon Saad-Falcon, Omar Khattab, Christopher Potts, and Matei Zaharia. ARES: An automated
  evaluation framework for retrieval-augmented generation systems. In Proceedings of the 2024
  Conference of the North American Chapter of the Association for Computational Linguistics
  (NAACL), 2024.
Rylan Schaeffer, Brando Miranda, and Sanmi Koyejo. Are emergent abilities of large language
  models a mirage? In Advances in Neural Information Processing Systems (NeurIPS), 2023.
John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy
  optimization algorithms. arXiv preprint arXiv:1707.06347, 2017.


                                                 11
Mohammadamin Shafiei, Hamidreza Saffari, and Nafise Sadat Moosavi. MultiHoax: A dataset of
 multi-hop false-premise questions. arXiv preprint arXiv:2506.00264, 2025.
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang,
  Mingchuan Zhang, Y. K. Li, Y. Wu, and Daya Guo. DeepSeekMath: Pushing the limits of
  mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024.
Jidong Tian, Yitian Li, Wenqing Chen, Liqiang Xiao, Hao He, and Yaohui Jin. Diagnosing the
   first-order logical reasoning ability through LogicNLI. In Proceedings of the 2021 Conference on
   Empirical Methods in Natural Language Processing (EMNLP), pages 3738–3747, 2021.
Siyuan Wang, Wanjun Zhong, Duyu Tang, Zhongyu Wei, Zhihao Fan, Daxin Jiang, Ming Zhou, and
  Nan Duan. Logic-driven context extension and data augmentation for logical reasoning of text. In
  Findings of the Association for Computational Linguistics (ACL), pages 1619–1629, 2022.
Zhongsheng Wang, Jiamou Liu, Qiming Bao, Hongfei Rong, and Jingfeng Zhang. ChatLogic:
  Integrating logic programming with large language models for multi-step reasoning. In Proceedings
  of the International Joint Conference on Neural Networks (IJCNN), 2024.
Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, Barret Zoph, Sebastian Borgeaud, Dani Yogatama,
  Maarten Bosma, Denny Zhou, Donald Metzler, et al. Emergent abilities of large language models.
  Transactions on Machine Learning Research, 2022a.
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc V.
  Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language models.
  Advances in Neural Information Processing Systems (NeurIPS), 35, 2022b.
Adina Williams, Nikita Nangia, and Samuel R. Bowman. A broad-coverage challenge corpus
  for sentence understanding through inference. In Proceedings of the 2018 Conference of the
 North American Chapter of the Association for Computational Linguistics: Human Language
 Technologies (NAACL-HLT), pages 1112–1122, 2018.
Ronald J. Williams. Simple statistical gradient-following algorithms for connectionist reinforcement
  learning. Machine Learning, 8(3–4):229–256, 1992.
Huajian Xin et al. DeepSeek-Prover-V1.5: Harnessing proof assistant feedback for reinforcement
  learning and Monte-Carlo tree search. arXiv preprint arXiv:2408.08152, 2024.
Siheng Xiong, Ali Payani, Yuan Yang, and Faramarz Fekri. Deliberate reasoning in language
  models as structure-aware planning with an accurate world model. In Proceedings of the 63rd
  Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages
  31900–31931, 2025.
Siheng Xiong, Oguzhan Gungordu, James C. Kerce, and Faramarz Fekri. Adaptive information
  control for search-augmented LLM reasoning. arXiv preprint arXiv:2602.01672, 2026.
Jundong Xu, Hao Fei, Huichi Zhou, Xin Quan, Qijun Huang, Shengqiong Wu, William Yang
  Wang, Mong-Li Lee, and Wynne Hsu. LogicReward: Incentivizing LLM reasoning via step-wise
  logical supervision. In International Conference on Learning Representations (ICLR), 2026.
  arXiv:2512.18196.
Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil,
  Ryan Prenger, and Anima Anandkumar. LeanDojo: Theorem proving with retrieval-augmented
  language models. In Advances in Neural Information Processing Systems (NeurIPS), 2023.
Nathan Young, Qiming Bao, Joshua Bensemann, and Michael Witbrock. AbductionRules: Training
  transformers to explain unexpected inputs. In Findings of the Association for Computational
  Linguistics (ACL), pages 218–227, 2022.
Qinyan Zhang, Xinping Lei, Ruijie Miao, Yu Fu, Haojie Fan, Le Chang, Jiafan Hou, Dingling Zhang,
  Zhongfei Hou, Ziqiang Yang, Changxin Pu, Fei Hu, Jingkai Liu, Mengyun Liu, Yang Liu, Xiang
  Gao, Jiaheng Liu, Tong Yang, Zaiyuan Wang, Ge Zhang, and Wenhao Huang. Inverse IFEval:
  Can LLMs unlearn stubborn training conventions to follow real instructions? In International
  Conference on Learning Representations (ICLR), 2026. arXiv:2509.04292.


                                                12
A     Appendix

A.1   Limitations and Future Work

The benchmark is propositional and synthetic; saturation evidences that the structural prior generalises
across backbones, not that contradictions are universally solved—V4-multi at 1.5B drops to 0.773
after Stage 4 (a capacity bottleneck rather than a structural-prior failure; §5.2), and the Lean F-rate
gap on the closed-world / classical semantics divide is genuine. The pipeline also commits to a
single conservative contradiction semantics; paraconsistent or priority-based resolution strategies
(Appendix A.8 ff.) are out of scope. Three concrete next steps follow: (i) end-to-end RLVF-Lean
training amortised through a persistent LeanDojo server, replacing the current verification-only
deployment; (ii) lifting the closed-world override via a CWA axiom schema, or via the hybrid
forward-chain/Lean policy of §5.2 that uses Lean only for T-verdicts and the symbolic forward-
chainer for F-verdicts; (iii) evaluation on math/proof benchmarks (e.g., MiniF2F, ProofNet) where
the Lean kernel is the natural verifier and where stacked-rewrite depth substantially exceeds the 2–5
laws stress-tested in V4-multi.

A.2   Structural Variant Generation


Algorithm 1 Structural Variant Generation (Variant 2 & 3)
Require: Canonical generator Base(·), key rule r⋆ , contradiction template Contr(·), instances N
Ensure: Datasets Dbase , Dv2 , Dv3
 1: for i = 1 to N do
 2:     (F, R, Q, A) ← Base(i); Dbase ← Dbase ∪ {(F, R, Q, A)}
 3:     Rv2 ← R \ {r⋆ }; Dv2 ← Dv2 ∪ {(F, Rv2 , Q, Label(F, Rv2 , Q))}
 4:     Fv3 ← F ∪ {Contr(F, R)}; Dv3 ← Dv3 ∪ {(Fv3 , R, Q, Label(Fv3 , R, Q))}
 5: end for




A.3   Preference Pair Templates (DPO Stage 2)

For contradiction cases, the preferred reasoning trace yw correctly detects the inconsistency in the
verification step and halts; the rejected trace yl proceeds with deductive inference.
Preferred (yw ): “Step 1: Detect contradiction between premises. Step 2: Halt reasoning.”          Rejected
(yl ): “Step 1: Premises are consistent. Step 2: Continue deductive inference.”

A.4   Stage 1 Hyperparameters

Epochs 3; LR 2×10−5 ; batch 4; max length 512; AdamW (mixed precision); LoRA r=8, α=16,
dropout 0.05.

A.5   Ablation Tables

Table 6: Ablation: SFT on a vanilla Mixed-Aug corpus without the conflict-aware verification
preamble. Compared to Fusion-LRA (Conflict-Aware SFT, Table 2, Base = 0.988 on Qwen2),
removing the preamble drops Qwen2’s base accuracy to 0.5250, isolating the contribution of the
structural prior from the contribution of training data alone.

                                               BERT               Qwen2             TinyLlama
        Split                            Acc          ∆       Acc         ∆        Acc        ∆
        base                            1.0000    0.0000     0.5250    -0.4750   0.5375    -0.4625
        variant2 (Essential Deletion)   0.2500    -0.7500    0.4050    -0.1200   0.5325    -0.0050
        variant3 (Contradiction)        0.0000    -1.0000    0.0000    -1.0000   0.0000    -1.0000




                                                      13
                  Table 7: Iterative Comparison: Fusion-LRA vs. earlier iterations.

                          Method           Base Acc       Var 2   Var 3   Rank
                          Mixed-Aug          0.525        0.405   0.972    3
                          RA-CoT             0.263        0.593   0.690    2
                          Fusion-LRA         0.988        0.753   0.705    1



A.6   Lean Pilot Study (8 hand-crafted traces)

Before the benchmark-scale Lean evaluation reported in Table 5, we ran a small hand-crafted
pilot on the Socrates contradiction example to verify (i) that the Python→Lean bridge faithfully
translates a halt-on-contradiction trace into a kernel-checkable theorem, (ii) that valid halt traces
receive reward +1 while opportunistic deductive continuations and malformed traces receive −1, and
(iii) that per-trace verification latency is compatible with online RL. Table 8 reports kernel agreement
on 8 representative traces.

Table 8: Lean 4 step-level reward pilot on the Socrates example. Lean kernel agrees with the expected
RLVF-Lean reward on 8/8 traces, including sorry-based admits and syntactic errors. Mean latency
0.36 s/trace on CPU.
            Trace ID                       Category          Expected r   Lean r      Time (s)
            T1-halt-minimal                correct halt              +1        +1         0.36
            T2-halt-direct                 correct halt              +1        +1         0.38
            T3-halt-contradiction-tactic   correct halt              +1        +1         0.36
            T4-naive-stops-early           naïve continue            −1        −1         0.37
            T5-naive-wrong-goal            naïve continue            −1        −1         0.35
            T6-naive-empty (sorry)         naïve continue            −1        −1         0.36
            T7-syntax-error                malformed                 −1        −1         0.36
            T8-misspelled-lemma            malformed                 −1        −1         0.36
            Agreement with oracle                                                   8/8 (100%)


A.7   Lean 4 Feasibility Demo for RLVF-Lean (Phase 2)

The following Lean 4 script encodes the Socrates contradiction example from Figure 1 as a ver-
ified theorem. It accompanies Section 5.2 (Phase 2: Scaling the Verifier with a Formal Proof
Assistant) and demonstrates that the step-level reward signal defined by Eq. (4) can be sourced
from the Lean kernel with no additional model training. The complete source is included in
lean_demo/SocratesContradiction.lean; a minimal excerpt is shown below.

axiom Person   : Type
axiom Socrates : Person
axiom Man      : Person -> Prop
axiom Mortal   : Person -> Prop
axiom men_are_mortal : forall x : Person, Man x -> Mortal x

-- The halt-on-contradiction behavior that RLVF-Lean is rewarded
-- for discovering. Lean accepts the proof iff the policy has
-- genuinely identified both sides of the contradiction.
theorem socrates_contradiction
    (h_man        : Man Socrates)
    (h_not_mortal : Not (Mortal Socrates)) : False := by
  have h_mortal : Mortal Socrates := men_are_mortal Socrates h_man
  exact absurd h_mortal h_not_mortal

A Python bridge (lean_demo/lean_verifier_bridge.py) synthesizes one such script per policy
rollout and returns the kernel’s accept/reject verdict as the step-level reward rt in Eq. (4). The same
theorem additionally refutes the naive “continue deducing” policy: under the contradictory premise


                                                     14
set, no total proof of an arbitrary query exists without first deriving False, so any rollout that claims
True receives reward −1. This preserves the conservative reasoning semantics of Section 3 at the
level of the Lean kernel itself.

A.8    Base Example: Complex Dilemma Reasoning Structure

We begin with a comprehensive example that establishes the core reasoning pattern, drawing on a
structure analogous to the Paradox of the Court3 , a classic logical dilemma where multiple possible
paths lead to the same conclusion, despite their apparent differences.

        • Facts:
              – Anne is green or blue
        • Rules:
              – Rule 1: If someone is green then they are cold. ∀x (Green(x) → Cold(x))
              – Rule 2: If someone is blue then they are cold. ∀x (Blue(x) → Cold(x))
              – Rule 3: If someone is cold then they are rough. ∀x (Cold(x) → Rough(x))
              – Rule 4: If someone is rough then they are young. ∀x (Rough(x) → Young(x))
              – Rule 5: If someone is young then they are cold. ∀x (Young(x) → Cold(x))
              – Rule 6: If someone is young then they are nice. ∀x (Young(x) → Nice(x))
        • Questions:
              – Q1: Anne is cold. True/False? [Answer: T]
              – Q2: Anne is rough. True/False? [Answer: T]
              – Q3: Anne is young. True/False? [Answer: T]
              – Q4: Anne is nice. True/False? [Answer: T]

The fact “Anne is green or blue" combined with Rules 1 and 2 creates a classic dilemma: both
possibilities lead to the same conclusion. This dilemma reasoning yields “Anne is cold." Rule 3 then
derives “Anne is rough" from cold, Rule 4 derives “Anne is young" from rough, and Rule 6 derives
“Anne is nice" from young. Rule 5 creates a circular reinforcement but doesn’t alter the conclusions.
The logical structure can be represented as:
                                  (Ga ∨ Ba ) ∧ (Ga → Ca ) ∧ (Ba → Ca ) ⊢ Ca

        • Ga : Green(Anne)
        • Ba : Blue(Anne)
        • Ca : Cold(Anne)

A.9    Variation 1: Rule Reduction with Same Conclusions

This variation demonstrates that removing redundant rules preserves the AI’s ability to reach the
same conclusions, illustrating that fewer rules can be equally effective.

        • Facts:
              – Anne is green or blue
        • Rules:
              – Rule 1: If someone is green then they are cold. ∀x (Green(x) → Cold(x))
              – Rule 2: If someone is blue then they are cold. ∀x (Blue(x) → Cold(x))
              – Rule 3: If someone is cold then they are rough. ∀x (Cold(x) → Rough(x))
              – Rule 4: If someone is rough then they are young. ∀x (Rough(x) → Young(x))
              – Rule 6: If someone is young then they are nice. ∀x (Young(x) → Nice(x))
   3 The Paradox of the Court involves a contract between the teacher Protagoras and his student Euathlus, where the student

only pays for lessons if he wins a court case. When Protagoras sues Euathlus for the fee, a paradox arises: if Euathlus wins, he
owes nothing, but if he loses, he still avoids payment, creating a logical contradiction about the outcome.


                                                              15
       • Questions:
            – Q1: Anne is cold. True/False? [Answer: T]
            – Q2: Anne is rough. True/False? [Answer: T]
            – Q3: Anne is young. True/False? [Answer: T]
            – Q4: Anne is nice. True/False? [Answer: T]

The reasoning proceeds identically to the base case: the dilemma from Rules 1-2 yields “Anne is
cold," Rule 3 yields rough, Rule 4 yields young, and Rule 6 yields nice. The removal of Rule 5 has
no impact on the conclusions, demonstrating its redundancy.
Key Insight: AI systems that recognize this redundancy can simplify their reasoning processes
without sacrificing accuracy, embodying the “less is more" principle.
The simplified logical structure becomes:
                           (Ga ∨ Ba ) ∧ (Ga → Ca ) ∧ (Ba → Ca ) ⊢ Ca


                                       Ca ∧ (Ca → Ra ) ⊢ Ra


                                       Ra ∧ (Ra → Ya ) ⊢ Ya


                                       Ya ∧ (Ya → Na ) ⊢ Na

       • Ga = Green(Anne)
       • Ba = Blue(Anne)
       • Ca = Cold(Anne)
       • Ra = Rough(Anne)
       • Ya = Young(Anne)
       • Na = Nice(Anne)

A.10   Variation 2: Rule Equivalence with Different Conclusions

This variation replaces multiple rules with logically equivalent fewer rules, but interestingly leads to
different conclusions due to the modified rule interactions.

       • Facts:
            – Anne is green or blue
       • Rules: (This variant deliberately combines two perturbations: a logical-equivalence rewrite
         of Rules 1+2 into a single Rule A, and the deletion of Rules 5 and 6. Rule 6 is essential for
         deriving “nice”; we discuss the two perturbations separately below.)
            – Rule A: If someone is green or blue then they are cold. ∀x ((Green(x) ∨ Blue(x)) →
              Cold(x)) (replaces Rules 1+2)
            – Rule 3: If someone is cold then they are rough. ∀x (Cold(x) → Rough(x))
            – Rule 4: If someone is rough then they are young. ∀x (Rough(x) → Young(x))
            – Rule 5 (Young → Cold) – removed (redundant cycle)
            – Rule 6 (Young → Nice) – removed (essential for “nice”; this is the cause of Q4=F, not
              the Rule A rewrite)
       • Questions:
            – Q1: Anne is cold. True/False? [Answer: T]
            – Q2: Anne is rough. True/False? [Answer: T]
            – Q3: Anne is young. True/False? [Answer: T]
            – Q4: Anne is nice. True/False? [Answer: F]


                                                  16
Rule A directly captures the dilemma of Rules 1 and 2, leading to “Anne is cold" with equivalent
logical force—this is the equivalence rewrite, and it preserves Q1–Q3. The change in Q4 (“nice”
becomes F) is caused entirely by the deletion of Rule 6, not by the equivalence rewrite. We made
both edits in this single illustrative variant to keep the example compact, but they are structurally
independent: Variant 4 in the main benchmark applies the rewrite alone, and Variant 2 applies the
essential-rule deletion alone.
Key Insight: Logical equivalence of a sub-rule set (here Rules 1+2 vs. Rule A) is a local property; it
does not by itself change derivability. Macro-level derivability changes are caused by which essential
rules remain, as isolated cleanly in Variant 2.
The logical equivalence can be shown as:
                  (∀x (Gx → Cx ) ∧ ∀x (Bx → Cx )) ≡ ∀x ((Gx ∨ Bx ) → Cx )
       • Gx = Green(x)
       • Bx = Blue(x)
       • Cx = Cold(x)
However, the missing Rule 6 prevents the derivation of Nice(Anne), showing that local equivalence
doesn’t preserve global derivability.

A.11   Variation 3: Rule Interference with Contradictory Conclusions

This variation adds distracting and potentially contradictory rules, testing the AI’s ability to address
conflicts and maintain coherent reasoning.
       • Facts:
           – Anne is green or blue
           – Anne is not cold or not nice
       • Rules:
           – Rule 1: If someone is green then they are cold. ∀x (Green(x) → Cold(x))
           – Rule 2: If someone is blue then they are cold. ∀x (Blue(x) → Cold(x))
           – Rule 3: If someone is cold then they are rough. ∀x (Cold(x) → Rough(x))
           – Rule 4: If someone is rough then they are young. ∀x (Rough(x) → Young(x))
           – Rule 5: If someone is young then they are cold. ∀x (Young(x) → Cold(x))
           – Rule 6: If someone is young then they are nice. ∀x (Young(x) → Nice(x))
       • Questions:
           – Q1: Anne is cold. True/False? [Answer: F]
           – Q2: Anne is rough. True/False? [Answer: F]
           – Q3: Anne is young. True/False? [Answer: F]
           – Q4: Anne is nice. True/False? [Answer: F]

A.12   Reasoning Process and Analysis

This variation introduces contradictory interference, which challenges the AI’s ability to address
conflicts within the logical structure. The fact “Anne is green or blue," combined with the original
chain of reasoning (Rules 1-6), leads to the conclusions that Anne is cold, rough, young, and nice.
However, the fact “Anne is not cold or not nice" introduces a conflict, as it implies that being nice
would mean Anne is not cold. This creates a contradiction that different AI systems might address
differently:

Contradiction Handling Strategy. In the experiments presented in this paper we adopt a conserva-
tive contradiction-handling strategy. Once a contradiction is detected in the premise set, the reasoning
process halts and no further deductions are performed. As a result, all queries associated with that
instance are labeled False.
Alternative reasoning strategies such as priority-based resolution or paraconsistent reasoning are
possible, but they are outside the scope of the current work and are left for future investigation.


                                                  17
                        Variations        Cold Rough Young Nice
                        Base Example        T        T         T         T
                        Rule Reduction      T        T         T         T
                        Rule Equivalence    T        T         T         F
                        Rule Interference   F        F         F         F
                        Table 9: Comparison of conclusions across variations

       Split                            BERT                Qwen2              TinyLlama
                                    Acc        ∆        Acc        ∆         Acc         ∆
       base                       1.0000 0.0000 1.0000 0.0000 1.0000 0.0000
       variant1                   1.0000 0.0000 1.0000 0.0000 1.0000 0.0000
       variant2                   0.2950 -0.7050 0.2500 -0.7500 0.2500 -0.7500
       variant3                   0.0000 -1.0000 0.0000 -1.0000 0.0000 -1.0000
       variant4-contrapositive    1.0000 0.0000 1.0000 0.0000 1.0000 0.0000
       variant4-double-negation 1.0000 0.0000 1.0000 0.0000 1.0000 0.0000
       variant4-implication       1.0000 0.0000 0.9525 -0.0475 1.0000 0.0000
       variant4-de-morgan         1.0000 0.0000 1.0000 0.0000 1.0000 0.0000
       variant4-identity          1.0000 0.0000 1.0000 0.0000 1.0000 0.0000
       variant4-commutativity     0.9925 -0.0075 1.0000 0.0000 1.0000 0.0000
       variant4-multi (2–5 laws) 1.0000 0.0000 0.6450 -0.3550 0.9925 -0.0075
       Table 10: Accuracy and deviation from base (∆) for all models across structural variants.


        • Conservative approach: Detect contradiction and withhold conclusions
        • Priority-based approach: Apply rule priorities or specificity heuristics
        • Paraconsistent approach: Accept some contradictions and continue reasoning

In this case, a conservative reasoning system would recognize the contradiction and potentially reject
all derived conclusions, resulting in false for all questions.
The addition of interfering rules not only tests the AI’s ability to ignore distractions but also its
capacity for contradiction detection and resolution.
The contradiction can be formally represented as:
                                   (Ca ∧ Na ) ∧ (Na → ¬Ca ) ⊢ ⊥

        • Ca = Cold(Anne)
        • Na = Nice(Anne)
        • ⊥ represents a value that is always false.

A.13     Comparative Analysis

Table 9 provides a clear comparison of how different modifications to the rule set lead to distinct
conclusion patterns, highlighting the sensitivity of reasoning systems to structural changes. These
variations demonstrate how even minor adjustments to the logical framework can significantly impact
the reasoning process and the final outcomes.
Table 10 reports accuracy (Acc) and deviation from the base condition (∆ = Accvariant − Accbase ) for
BERT, Qwen2, and TinyLlama across all structural variants. All models achieve Acc = 1.0000 on the
base split and exhibit no degradation under redundant rule removal (Variant 1; ∆ = 0). By contrast,
removing an essential rule (Variant 2) yields a substantial drop (BERT: 0.2950, ∆ = −0.7050;
Qwen2/TinyLlama: 0.2500, ∆ = −0.7500), indicating strong sensitivity to missing inferential
links. Injecting explicit contradictory facts (Variant 3) reduces accuracy to 0.0000 for all models
(∆ = −1.0000), suggesting that the models do not reliably revise conclusions in the presence of
inconsistency.




                                                  18
