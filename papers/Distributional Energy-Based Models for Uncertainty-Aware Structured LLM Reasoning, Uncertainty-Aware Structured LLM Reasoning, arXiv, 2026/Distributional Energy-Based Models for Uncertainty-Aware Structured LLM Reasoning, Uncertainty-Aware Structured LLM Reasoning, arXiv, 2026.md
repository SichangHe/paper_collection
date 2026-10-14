                                                   Distributional Energy-Based Models for
                                                Uncertainty-Aware Structured LLM Reasoning


                                                     Shireen Kudukkil Manchingal†            Abhey Kalia         Fernanda Gonçalves
                                                                                     Shebin Rawther
                                                                                     Oxford Dynamics
arXiv:2605.18871v1 [cs.LG] 15 May 2026




                                                                Harwell Science and Innovation Campus, United Kingdom



                                                                                        Abstract
                                                     When Large Language Models produce structured outputs such as travel plans,
                                                     code solutions, or multi-step proofs, individual reasoning steps may appear cor-
                                                     rect while the output as a whole violates budgets, fails test cases, or contradicts
                                                     earlier deductions. We propose a decomposed energy function that combines a
                                                     learned quality scorer with deterministic analytical constraint penalties for veri-
                                                     fying structured LLM outputs. The quality scorer is a heterogeneous ensemble
                                                     of low-rank adapters on a single frozen encoder (3% trainable parameters); the
                                                     ensemble mean ranks candidates while the standard deviation quantifies epistemic
                                                     uncertainty, driving a two-pass inference loop that triggers targeted regeneration
                                                     or abstention. Across five benchmarks (GSM8K, MuSR, TravelPlanner, TACO,
                                                     Knights & Knaves), our 149M-parameter verifier orchestrating a pool of 7–26B
                                                     open generators outperforms single-shot Qwen-72B on every benchmark, matches
                                                     Claude Sonnet 4.6 on MuSR (67.7% vs. 68.0%), and reduces constraint violations
                                                     by 53% relative to Opus 4.6 on TravelPlanner (oracle 0.028, random 0.231). The
                                                     two routes are complementary: structural verification wins when constraints are
                                                     checkable (the verifier captures signal frontier models cannot self-detect), while
                                                     pretraining-scale priors win where they are not (narrative inference, code seman-
                                                     tics). A cross-dataset confounding analysis confirms genuine quality discrimination
                                                     on four reasoning tasks and identifies a model-identity shortcut on code, mitigated
                                                     via last-layer retraining. Scorers trained on difficult data transfer zero-shot: a
                                                     MuSR-trained scorer achieves 93.9% on GSM8K without seeing a math problem.

                                         1    Introduction
                                         Large Language Models have advanced rapidly, achieving strong performance across translation,
                                         summarisation, code generation, and open-ended dialogue [Brown et al., 2020, OpenAI, 2023]. A
                                         central driver of this progress is reasoning: the ability to decompose a problem into intermediate steps
                                         and arrive at a justified conclusion. Chain-of-thought (CoT) prompting [Wei et al., 2022, Kojima
                                         et al., 2022] unlocked this capability by eliciting step-by-step reasoning traces, and subsequent work
                                         has extended it through self-consistency [Wang et al., 2023], least-to-most decomposition [Zhou
                                         et al., 2023], and tree-structured search [Yao et al., 2023].
                                         Yet reasoning in current models remains fundamentally limited by the autoregressive generation
                                         mechanism: each token is committed in sequence, with no global scoring function to evaluate whether
                                         the output as a whole is consistent. Local correctness at each step does not compose into global
                                         correctness for structured outputs: cross-step violations are aggregation errors that exist only at the
                                         whole-output level (a budget exceeded only when all days are summed, a return-type mismatch
                                         propagating between functions, a single arithmetic error invalidating the rest of a derivation), and
                                             † Corresponding author: shireen.manchingal@oxdynamics.com



                                         Preprint.
per-step scoring cannot detect them by construction, no matter how accurate. Each step receives a
local correctness signal yet cross-step violations remain invisible (Fig. 1, left), so the wrong plan is
delivered with no warning. GPT-4-Turbo satisfies all constraints on TravelPlanner only 4.4% of the
time [Xie et al., 2024b], and even frontier models frequently produce code that fails on edge cases in
competitive programming benchmarks [Chen et al., 2021, Li et al., 2023].
The bottleneck, however, is not generation but se-           Problem: CoT is scored per step          Proposed solution:
lection: pass@N substantially exceeds pass@1, the               3 × 📕 ($12) + 2 × 🖋️($4)               Score N candidates
                                                                        = pays $50                   Same LLM, N samples
correct candidate is usually somewhere in the pool of                3 × $12 = $36
N samples from the same LLM, yet existing scorers                                                  $12     $10       $8    $14
                                                                      2 × $4 = $8
cannot reliably identify it [Brown et al., 2024, Stien-
                                                                     $36 + $8 = $42                $12      $6      $12    $18
non et al., 2020]. Process reward models [Lightman
et al., 2023, Khalifa et al., 2025] score individual                 $50 − $42 = $12
                                                                                                     🔍 Energy     Reasoning
                                                                                                              Verifier
reasoning steps rather than complete outputs. Energy-            $50 − $42 ≠ $12 (it's $8)

based models (EBMs) offer a more natural framework                 Wrong answer: $12
                                                                                                      Verified answer: $8

for whole-output scoring, assigning low energy to           local checks: ✅, global error: ❌
                                                                                                       right answer ∈ pool
                                                                                                       selection → usable
good candidates and high energy to bad ones [LeCun
et al., 2006], and recent work applies this principle to  Figure    1:  Left:    Chain-of-thought         scores each step
rerank reasoning traces [Jiang et al., 2025, Chen et al., locally;   cross-step         violations are   invisible.     Right:
2025, Tan and Hong, 2025]. Yet existing methods Distributional energy scores N candidates glob-
share two limitations: (i) they produce point-estimate ally, verifies constraints analytically, and quantifies
                                                          confidence via ensemble agreement.
scores with no indication of reliability [Gleave and
Irving, 2022], offering no signal for when to trust, regenerate, or abstain; and (ii) they operate on flat
reasoning chains with no mechanism for verifying domain-specific constraints exactly.
In this paper, we show that this selection problem can be addressed with a small specialised verifier
rather than by scaling the generator. We propose a decomposed, distributional energy function
E = µquality + λ · Econstraint (Fig. 1, right) combining a learned quality term µquality with deterministic
analytical constraint penalties Econstraint . The same compact architecture works across five funda-
mentally different reasoning tasks (math, narrative inference, multi-constraint planning, executable
code, formal logic). The quality term µquality is realised as a heterogeneous ensemble of K low-rank
adapters (LoRA; Hu et al., 2022) on a single frozen encoder, structurally diverse so that ensemble
disagreement reflects genuine epistemic uncertainty rather than superficial variation from random
seeds [Fort et al., 2019, Lakshminarayanan et al., 2017, Gal and Ghahramani, 2016]. The ensemble
mean ranks candidates; the standard deviation σquality drives a two-pass inference loop that triggers
regeneration with structured feedback under uncertainty or constraint violations, and abstains in the
extreme case. Crucially, the verifier is architecturally independent of the candidate generators, so its
judgement does not collapse when the generators’ self-reported reasoning is wrong.
The following are the main contributions of this paper:
• A novel modular energy decomposition with zero-shot transfer. A transferable learned quality
  scorer Equality and swappable deterministic penalties Econstraint : Equality wins beyond pretraining-
  scale priors, Econstraint wins on checkable constraints. The scorer transfers zero-shot (MuSR-trained
  reaches 93.9% on GSM8K without seeing math); new tasks need only new constraint functions.
• A novel distributional energy via heterogeneous LoRA ensemble. A parameter-efficient ensem-
  ble of structurally diverse low-rank adapters produces an energy distribution rather than a point
  estimate, enabling confounding diagnostics and σ-gated abstention.
• Honest confounding analysis with causal verification. On 4/5 tasks the scorer learns content-
  based quality with no model-identity shortcut (cross-model energy spreads < 0.25, picks near-
  uniform across generators); on TACO, a causal style-swap test exposes a formatting shortcut,
  fixed by last-layer retraining [Kirichenko et al., 2023] at no accuracy cost. Multi-model candidate
  diversity substantially improves selection.
Paper outline. Sec. 2 reviews chain-of-thought reasoning, energy-based models, reward modelling,
and test-time compute. Sec. 3 presents the energy decomposition (3.1), the distributional quality
scorer with formal propositions (3.2), training (3.3), analytical constraint penalties (3.4), and two-pass
σ-triage (3.5). Sec. 4 reports the experimental setup (4.1) and results across all five benchmarks
(4.2). Sec. 5 distils lessons learned and outlines future directions. The appendix provides proofs (§A),
model and implementation details (§B, §C), dataset details and per-model candidate quality (§D, §E),
and extended results: ablations (§F.1), energy diagnostics (§F.2), per-difficulty breakdowns (§F.3),



                                                             2
selective prediction (§F.4), two-pass analysis (§F.5), per-constraint frontier comparison (§F.6), the
full transfer matrix (§F.7), confounding analysis (§F.8), and broader impact (§G).

2     Related Work
Chain-of-thought prompting [Wei et al., 2022, Kojima et al., 2022] elicits step-by-step reasoning;
self-consistency [Wang et al., 2023], least-to-most prompting [Zhou et al., 2023], and Tree of
Thoughts [Yao et al., 2023] extend it via marginalisation, decomposition, and branching search.
Process reward models give finer-grained supervision: Uesato et al. [2022] and Lightman et al. [2023]
show step-level outperforms outcome-level verification, and Khalifa et al. [2025] train models that
generate reasoning traces before scoring, with a fraction of process labels. All produce point-estimate
scores on flat reasoning chains, with no mechanism for verifying that structured multi-section outputs
satisfy global constraints jointly.
Energy-based models assign scalar energies to input-output pairs [LeCun et al., 2006] and have
been applied to text generation [Deng et al., 2020]; Blondel et al. [2025] prove autoregressive
language models are themselves EBMs, and Carbone [2024] survey the broader landscape. For
reasoning, Jiang et al. [2025] rerank CoT on GSM8K/MATH (90.7%, 55M params); Chen et al.
[2025] apply energy-based calibration to implicit CoT; Tan and Hong [2025] connect RL-tuned
language models to EBMs theoretically. Across this work, energy is a deterministic scalar with no
reliability signal; Gleave and Irving [2022] highlight this gap for reward models but use standard
ensemble variance rather than structurally heterogeneous adapters. Our pairwise-preference learning
connects to RLHF [Christiano et al., 2017, Ouyang et al., 2022] and DPO [Rafailov et al., 2023]
but targets post-hoc verification of complete outputs; we further produce a distributional energy via
a heterogeneous ensemble, decompose energy into learned and analytical components, and target
structured multi-section outputs. A complementary line studies test-time compute allocation. Snell
et al. [2025] show verifier-guided search can outperform scaling model parameters, Guo et al. [2025]
show reinforcement learning alone can incentivise advanced reasoning, and Brown et al. [2024]
identify candidate selection as the key bottleneck: pass@N exceeds pass@1 but existing methods
close the gap only partially. For structured planning, Lee et al. [2025] reach 95.6% on TravelPlanner
via evolutionary search with Gemini 1.5 Flash, Xia et al. [2025] use reward modelling for agent
generalisation, and Wang et al. [2025] combine multiple LLMs via mixture-of-agents. We address
the selection bottleneck via energy-based reranking and the verification gap via analytical constraint
penalties, using ensemble uncertainty to decide when selection is reliable.

3     Methodology
We propose a Distributional EBM (Fig. 2) with two stages: a quality scorer trained on contrastive
candidate pairs (top), and inference-time candidate ranking with σ-triaged regeneration (bottom).
3.1   Problem Formulation
Let x denote an input problem and let {y1 , . . . , yN } denote N candidate structured outputs generated
by frozen base LLMs via temperature sampling. We propose the decomposed energy function:
                            E(x, y) = µquality (x, y) + λ · Econstraint (x, y),                       (1)
and the selected candidate is the energy minimiser over the candidate pool Y = {y1 , . . . , yN },
y ∗ = arg miny∈Y E(x, y), where µquality (x, y) is the ensemble mean energy from the learned quality
scorer, Econstraint (x, y) is a sum of analytical penalty terms, and λ > 0 controls their relative weight.
The two components serve complementary roles: Equality captures general reasoning quality learned
from training data, while Econstraint encodes task-specific rules that can be verified exactly without
any learning.
3.2   Distributional Quality Scorer
We instantiate the quality scorer as an ensemble of K EBMs sharing a frozen pretrained bidi-
rectional Transformer encoder [Devlin et al., 2019, Warner et al., 2025]. We choose an encoder
over the now-standard causal-LM verifier so that a single [CLS] forward pass scores the whole
[problem]||[candidate] pair jointly with bidirectional attention, at one to three orders of mag-
nitude fewer parameters than CLM-based reward models or PRMs. To each member k we attach
a lightweight low-rank adapter [Houlsby et al., 2019, Hu et al., 2022] that modifies a subset of


                                                    3
                                                                                                                       update                                                    Training Equality
                                                                     Tokenization
                                                                                                                       weights                       E     E(y−)
                                                    [CLS]    task   [SEP] action   obs … answer
                                                                                                                    Energy Distribution
                                                     t1       t2     t3     t4      t5          tn                      E¹ E²
                                                                                          …                           E⁰     E³
                     Query                                                                                                    E⁴
      NYC→Chicago: 3 days, 2 people,          Transformer Encoder (shared frozen
                                                                                                                           μquality
      budget $2,500, prefer Chinese food                  backbone)                                                      σquality                           E(y+)                            Energy
                                                                                                                                                     ℒ = log(1 + exp(E(y+) − E(y−)))      Landscape
                                             LoRA           LoRA          LoRA           LoRA        LoRA
                                              r=8            r=8          r=16            r=4         r=8                                                                                                         Inference
                                                                                                                            Equality       Econstraint                          Abstain
                                                                                                                E(x, y) =            + λ · analytical
                                                                                                                            learned
                   N candidates
                                             E0             E1            E2             E3          E4                                              $ ⇄   ⏱♦ ☐                        extreme σquality
                                                                                                                                                                                                           candidate output y
        ✗−     ✗−     ✓
                      ✗+       ✗−       ✓
                                        ✗+   k=0            k=1           k=2            k=3         k=4
        y      y      y        y    .... y                                                                                                               high σ
                                                                                                                                                                                              confident
                                                                                                                                                                           σquality-triage                y* = arg min E(x, y)
                          ..



             y−: Flight $800,
                                                                                                                                   y1            12.4
         ✗ Hotel $400…. $3,200                                                                                                     y2           5.7
                                                             →                                                                     y3         3.1
              +
             y : Flight $350,                                                                                                           ...                                             uncertain / violations
         ✓ Hotel $180… $2,380                             parse                                                                    y5         −2.1
                                                                                                                                                         low σ             Regenerate N with
                                                                                                                                                                          uncertainty feedback



Figure 2: Method overview. Top: Training. Correct (y + ) / incorrect (y − ) candidate pairs pass through the
frozen ModernBERT backbone with one of K=5 heterogeneous LoRA adapters; each adapter’s MLP head
maps [CLS] to a scalar E k trained via Bradley-Terry. The K energies form a distribution: µquality ranks, σquality
quantifies confidence. Bottom: Inference. Four LLMs generate N =32 candidates, scored in parallel by the
ensemble and by analytical constraints (Econstraint ), ranked by E = µquality + λ · Econstraint , then σquality -triaged.

the encoder’s attention matrices, together with an independent energy head. Given a problem x
and candidate y, the input is tokenised as inputk = [CLS] x [SEP] y [SEP]. The frozen encoder,
augmented by adapter k, produces contextualised representations. The [CLS] representation hkCLS
                                                                        k
is passed through an MLP energy head producing a scalar Equality            (x, y) (architecture in §C). Each
adapter and energy head is trained independently; the frozen backbone is shared. The distributional
                                                                          1
                                                                            PK         k
output for candidate y is the ensemble mean µquality (x, y) = K                k=1 Equality (x, y) and standard
                                   1                 K
deviation σquality (x, y) = std({Equality , . . . , Equality }). The mean µquality is used for ranking (Eq. (1));
the standard deviation σquality drives the two-pass inference loop (Sec. 3.5) and provides a calibration
signal for post-hoc analysis.
Diversity comes from three sources: structural heterogeneity (the K adapters differ in rank, scaling
factor, and target attention modules; Tab. 5 in §C), so disagreement reflects genuine epistemic
uncertainty rather than seed variation [Fort et al., 2019, Lakshminarayanan et al., 2017]; independent
random initialisation per adapter; and 80% data bagging [Breiman, 1996]. Trainable parameters per
member (∼3% of backbone) consist only of the LoRA weights and the energy head.
Theoretical justification. A natural question is what the distributional energy (µquality , σquality )
provides beyond a point-estimate scorer. We present two results that together justify the combination
of decomposition and ensemble.
Proposition 3.1 (Ensemble ranking under correlated adapters). Let each adapter k correctly rank a
random (correct, incorrect) pair with probability q > 12 , and let ρ ∈ [0, 1] denote the pairwise rank
correlation between adapters. Under a Gaussian approximation for K ≥ 5, the probability that the
ensemble mean µquality correctly ranks the pair, and its K → ∞ limit (for any ρ > 0), are:
                                    √       1
                                                                                 1
                                                                                        
                                       K (q− 2 )             ∞                  q− 2
        Pensemble (K, q, ρ) = Φ √                       , P (q, ρ) = Φ √                  < 1,      (2)
                                                                          q(1−q)(1+(K−1)ρ)                                                                                             q(1−q) ρ
                                                                                                            ∞
where Φ is the standard normal CDF and P                                                                         < 1 is a finite ceiling that no ensemble size can
surpass unless ρ = 0.
Three consequences follow (proof and detailed analysis in §A). ∂P/∂ρ < 0, so structurally heteroge-
neous adapters (lower ρ) strictly outperform same-architecture ensembles; when ρ = 1, Pensemble → q
regardless of K; and for any ρ > 0 the ceiling in Eq. (2) is binding for moderate q (e.g., narrative
reasoning) and slack only when q is near unity (e.g., K&K).
Theorem 3.1 justifies the ensemble for ranking. The following result justifies the decomposition for
uncertainty: because Econstraint is deterministic, σquality reflects purely the epistemic uncertainty of the
learned quality component, uncontaminated by constraint uncertainty.
Proposition 3.2 (Partitioned variance under energy decomposition). Let E(x, y) = µquality (x, y) +
λ · Econstraint (x, y) where Econstraint is a deterministic analytical function. The predictive variance of
the total energy decomposes as:
                                                                                                   2
                   Var(E) = Var(Equality ) + Var(Econstraint ) + 2 Cov(Equality , Econstraint ) = σquality .                                                                                                                     (3)
                                             |    {z        } |            {z                }
                                                                                                =0                                                       =0


                                                                                                                4
For a monolithic scorer Emono that jointly learns both components, the predictive variance is
       mono              mono                 mono     mono                        2
Var(Equality ) + Var(Econstraint ) + 2 Cov(Equality , Econstraint ), which equals σquality only in the degener-
                 mono
ate case that Econstraint is learned exactly; otherwise the variance mixes constraint-prediction error
into the uncertainty signal and is no longer interpretable as quality uncertainty.
This makes σquality an interpretable uncertainty signal (quality only, with zero contribution from
constraint verification), and motivates the σ-triage decision rule (Sec. 3.5): accept when σquality and
Econstraint are both low, regenerate when either is high, abstain when σquality is extreme. Proof and full
implications are in §A.
3.3   Training
We train each member independently with the Bradley–Terry pairwise loss [Bradley and Terry, 1952]
on bagged 80% subsets Dk of training problems, where Yx+ and Yx− are the correct/incorrect outputs
for x. The objective for member k is:
                 1 X 1            X                                                        
        Lk = k                                          k
                                         log 1 + exp Equality (x, y + ) − Equality
                                                                           k
                                                                                   (x, y − ) , (4)
               |D |      k
                           |Px | + −
                      x∈D         (y ,y )∈Px

where Px ⊂ Yx+ × Yx− is a set of contrastive pairs sampled per problem, capped at a maximum
count to prevent easy problems from dominating the gradient. Members are optimised separately
(L1 , . . . , LK ); no parameters are shared across members beyond the frozen backbone. The loss
pushes the energy of correct outputs below incorrect ones; the logistic form saturates naturally for
well-separated pairs, avoiding the need for explicit energy regularisation.
Contrastive pairs are split at the problem level to prevent data leakage; labelling and hyperparameters
are in Sec. 4.1. The trained ensemble is applied zero-shot to out-of-domain tasks; task-specific
verification is handled entirely by Econstraint .
3.4   Analytical Constraint Penalties
We define EconstraintPas a sum of analytical penalty terms, each encoding a specific task constraint:
Econstraint (x, y) = j wj · Cj (x, y), where Cj is the penalty for constraint j and wj is its weight.
Each Cj returns 0 when the constraint is satisfied and a positive value proportional to the degree
of violation. The constraint terms are deterministic: each is a direct computation over the parsed
structured output with no learned parameters. They are also modular: adding or removing a constraint
changes Econstraint without affecting Equality or requiring retraining. The specific constraint terms for
each evaluation domain are defined in §E.
3.5   Two-Pass Inference with σ-Triage
We extend single-pass reranking with a two-pass inference loop driven by ensemble uncertainty and
constraint satisfaction, recovering when no good candidate exists or the scorer is uncertain (Algo-
rithm 1 in §F.5). Multiple frozen LLMs each generate Nm candidates via temperature sampling, which
are pooled into the first-pass set Y1 and scored. Each candidate receives µquality and σquality from the
K=5 ensemble and Econstraint from the analytical constraint checker. Let y1∗ = arg miny∈Y1 E(x, y)
denote the first-pass selection. The system then takes one of three actions, governed by thresholds
θσ < θabstain :                         
                                        accept        if σ ≤ θσ ∧ C = 0,
                          action(y1∗ ) = regenerate if σ ≤ θa ∨ C > 0,                               (5)
                                        
                                          abstain      if σ > θa ,
where σ = σquality (y1∗ ), C = Econstraint (y1∗ ), and θa = θabstain . On regenerate, constraint violations are
formatted as natural-language feedback and used to draw N2 additional candidates Y2 . The pooled
set Y = Y1 ∪ Y2 is rescored, and the final selection is y ∗ = arg miny∈Y E(x, y), subject to a final
abstention check on σquality (y ∗ ).

4     Experiments
Our experiments (Sec. 4.2) address five questions: (i) Is the bottleneck in structured LLM reasoning
selection rather than generation? (ii) Does separating learned quality from analytical constraints
improve correctness beyond either signal alone? (iii) Can ensemble disagreement reliably indicate
when to trust, regenerate, or reject an output? (iv) Does the scorer learn genuine reasoning quality


                                                      5
or exploit model-identity shortcuts? (v) Does the quality scorer transfer across reasoning domains
without retraining? Extended results are in the Appendix (§F).

4.1   Experimental Setup
Datasets. We evaluate across five benchmarks chosen for fundamentally different verification
signals: math (GSM8K; Cobbe et al., 2021), narrative inference (MuSR; Sprague et al., 2024),
multi-constraint planning (TravelPlanner; Xie et al., 2024b), executable code (TACO; Li et al.,
2023), and formal logic (K&K; Xie et al., 2024a). We evaluate across all five domains together,
where prior reranking work [Jiang et al., 2025, Lee et al., 2025] has typically focused on math or
planning alone. GSM8K is partially contaminated [Yang et al., 2023, Oren et al., 2024], so we
rely on MuSR (released 2024, post-dating all four generators’ pretraining) as the uncontaminated
headline; MuSR results are reported on the full test split (151 problems across all three subsets),
with per-subset breakdowns in §F.3. TravelPlanner contributes five analytical constraints (budget,
connectivity, completeness, preferences, diversity) defining Econstraint , verified against its sandbox
database; K&K’s statement-consistency checker is a perfect verifier; TACO uses execution-based
verification (we filter VERY_HARD with 0% solve rate). Primary metrics: pass@1 (single-sample
correctness, the deployment-relevant figure) for GSM8K, MuSR, TACO, and K&K; mean violation
score for TravelPlanner, since the strict zero-violation pass@1 compresses methods into a 0–30%
band and hides the order-of-magnitude differences captured by the continuous score. Splits, EDA,
per-model candidate quality, and examples are in §E (Tabs. 7 and 9); training data statistics in §D.
Candidate generators. We use four frozen generators chosen for open-weight access via OpenRouter
and parameter-count diversity (7–26B): Qwen-2.5-7B-Instruct [Qwen Team, 2024], LLaMA-3.1-
8B-Instruct [Grattafiori et al., 2024], Gemma-4-26B-IT [Google DeepMind, 2026], and GPT-OSS-
20B [OpenAI, 2025]. Each produces 8 candidates per problem via temperature sampling (T =0.7,
top-p=0.95 [Holtzman et al., 2020]), for N =32 candidates per problem; all generation uses the Open-
Router API. Pass 2 adds N2 =8 candidates from Qwen-2.5-7B conditioned on constraint feedback.
Baselines. We compare against three groups: (1) heuristic selection from the candidate pool (Greedy
at T =0, random selection, Self-consistency majority vote, and an Oracle upper bound); (2) state-of-
the-art frontier models (Claude Opus 4.6 and Sonnet 4.6 [Anthropic, 2026], Qwen-72B-Instruct [Qwen
Team, 2024]) which generate one deterministic answer at T =0 rather than selecting from a pool; and
(3) external learned selection methods that score the same candidate pool as our scorer: EORM [Jiang
et al., 2025] (the closest prior energy-based method), Skywork-Reward-LLaMA-3.1-8B-v0.2 [Liu
et al., 2024] (an 8B reward model), Math-Shepherd PRM [Wang et al., 2024] (a 7B step-level
Process Reward Model), and LLM-as-Judge [Zheng et al., 2023] using Claude Sonnet 4.6 (frontier
model scoring each candidate 1-10). Every learned baseline and frontier model in this comparison
is substantially larger than our 149M-parameter scorer: Skywork at 8B (54×), Math-Shepherd
PRM at 7B (47×), Qwen-72B (∼483×), and the frontier Claude models are several hundred billion
parameters, one to three orders of magnitude larger than ours.
Scorer backbone. The primary backbone is ModernBERT-base [Warner et al., 2025] (149M parame-
ters, 8,192 token context); the long context accommodates MuSR narratives (3–6K characters) and
full TravelPlanner itineraries without truncation. DeBERTa-v3-base [He et al., 2023] (86M parame-
ters, 512 token context) is evaluated as an ablation; backbone comparison, adapter configurations,
and DeBERTa-specific results are in §B and §F.1. The heterogeneous LoRA configuration follows
Tab. 5 in §C with K=5 adapters; LoRA and energy-head dropout are both 0.2.
Training. Each scorer is trained per-dataset via the Bradley–Terry loss in Eq. (4); candidates are
labelled by task-specific verification (answer matching for GSM8K and MuSR, constraint-violation
scoring for TravelPlanner, execution-based testing for TACO, and exact-match with statement-
consistency checking for K&K). Optimiser: AdamW [Loshchilov and Hutter, 2019] with cosine
annealing [Loshchilov and Hutter, 2017]; learning rates 5 × 10−5 (K&K 2 × 10−5 ); per-dataset batch
sizes and stopping criteria in Tab. 6; all training on 3 NVIDIA L40S (46 GB).
Inference. For the energy decomposition (Eq. (1)), we set λ=1.0 for GSM8K, MuSR, and TACO
(where Econstraint is not applied) and for K&K (where the exact statement-consistency checker requires
no upweighting); λ=2.0 for TravelPlanner, where mean violation is the primary metric and heavier
constraint weighting improves it. λ values were selected on a held-out validation split. The σ-triage
rule (Eq. (5)) uses thresholds θσ =0.8 and θabstain =1.5, both chosen by grid search on a held-out
validation split to maximise the pass@1 lift from regeneration while keeping the abstention rate
below 10%. All evaluations use candidate shuffling (seed 42) to eliminate ordering bias.


                                                  6
4.2      Results
Our 149M Distributional EBM is the strongest non-oracle method on TravelPlanner, within 0.3 pp
of the best non-oracle on GSM8K, 4.3 pp on MuSR, near-greedy on TACO, and within 0.1 pp
of perfect on K&K (Tab. 1), one to three orders of magnitude smaller than every other learned
baseline. We organise the analysis around the five experimental questions: (i) selection vs. generation,
(ii) decomposition, (iii) σ-triage, (iv) confounding, and (v) cross-domain transfer results are in Tab. 2.
Table 1: Selection accuracy across five benchmarks. Shaded : our 149M-parameter scorer reranking 32
candidates from a four-generator 7B-class pool; row labels list each baseline’s parameter count (∼frontier ≈
several hundred B). Frontier models are single-shot at T =0. Bold = best non-oracle, underlined = second-best.
mean viol. = mean constraint violation (lower better, primary TravelPlanner metric).
Strategy                                                            GSM8K      MuSR     TravelPlanner‡   TACO        K&K
                                                                  (pass@1 ↑) (pass@1 ↑) (mean viol. ↓) (pass@1 ↑) (pass@1 ↑)
Greedy (T =0)                                                         91.8%    61.2%        0.098        86.4%     100.0%
Random                                                                92.7%    56.3%        0.231        46.6%      58.7%
Self-consistency                                                      97.3%    64.4%        0.096        36.4%      56.4%
EORM [Jiang et al., 2025] (55M)♯                                      90.7%      –             –           –          –
Skywork-Reward (8B) [Liu et al., 2024]                                82.1%    62.3%        0.114∗       70.5%      96.4%
Math-Shepherd PRM (7B) [Wang et al., 2024]                            94.2%      –             –           –          –
LLM-as-Judge (∼frontier, 32 calls/problem) [Zheng et al., 2023]       99.2%♭   73.5%        0.084∗       73.9%      99.9%
Claude Opus 4.6 (∼frontier, single-shot)                              97.0%    72.0%        0.098       100.0%      99.7%
Claude Sonnet 4.6 (∼frontier, single-shot)                            97.0%    68.0%        0.103        95.5%      98.7%
Qwen-72B-Instruct (72B)                                               95.4%    54.9%        0.121        64.8%      39.0%
Oracle                                                                98.5%    86.1%        0.028       100.0%     100.0%
Distributional EBM (Ours, 149M)                                       97.0%    67.7%        0.046        88.6%      99.9%

Across the comparisons as shown in Tab. 1, Distributional EBM is the strongest non-oracle method on
TravelPlanner, within 0.3 pp of the best non-oracle on GSM8K, within 4.3 pp on MuSR, near-greedy
on TACO, and within 0.1 pp of perfect on K&K, while being one to three orders of magnitude smaller
than every other learned baseline. Notes: ‡ TP pass@1 (zero-violation) compresses methods to a
0–30% band: ours 28.0%, random 14.0%, self-consistency 12.0%. ∗ Skywork and LLM-as-Judge TP
violations are on a 20-problem subset matched to ground-truth scores (full pass@1: 21.1%, 55.0%).
♯
  EORM uses 256 candidates from 5 LLMs (8× our budget). ♭ LLM-as-Judge GSM8K is on a more
lenient pool, see §E. –: baseline does not apply (math-only PRM/EORM).
(i) Selection vs. generation: before vs. after the verifier. On the same 32-candidate pool (Tab. 1):
On MuSR, greedy 61.2% / oracle@32 86.1%; the Distributional EBM closes 26% of the gap to
67.7%, exceeding self-consistency (64.4%) and the 54× larger 8B Skywork-Reward [Liu et al.,
2024]. LLM-as-Judge [Zheng et al., 2023] (Sonnet 4.6) reaches 73.5% (+5.8 pp) at 32 frontier-API
calls per problem versus our single forward pass: roughly two orders of magnitude cheaper per
accuracy point. On TACO, greedy reaches 86.4% (oracle 100.0%); the EBM lifts pass@1 to 88.6%
(+2.2 pp over greedy, +42.0 pp over random, +52.2 pp over self-consistency whose majority vote
on extracted code outputs is essentially uninformative), beating Skywork-Reward by +18.1 pp. On
K&K, greedy already saturates from the strongest single generator (Gemma-4-26B at 100.0%);
the multi-pool EBM achieves 99.9% (699/700) and dominates Skywork-Reward by +32 pp on 2-
character puzzles to +47 pp on 8-character puzzles (Tab. 15). On GSM8K, contamination compresses
the gap (greedy 91.8%, oracle 98.5%); the EBM reaches 97.0%, matching self-consistency within
0.3 pp and surpassing the 7B Math-Shepherd PRM [Wang et al., 2024] (94.2% with explicit step-
level supervision) and EORM [Jiang et al., 2025] (90.7%; both restricted to math reasoning by
construction). On TravelPlanner, where mean violation is the headline metric: greedy 0.098, EBM
0.046, a 53% reduction over greedy and 80% over random. The lift exists because the multi-generator
pool has oracle headroom to convert: a Qwen-only pool collapses the ceiling on the uncontaminated
reasoning tasks (+13.3/+52.2/+59.8 pp on MuSR/TACO/K&K; Tab. 12). Heterogeneous generators
produce diverse error patterns and a higher oracle ceiling, giving the verifier more learning signal
and more correct candidates to rank. Fig. 3 shows how the Distributional EBM front-loads correct
candidates in its energy ranking; energy separation metrics are in §F.2.
(ii) Learned quality + analytical constraints. On TravelPlanner, the combined energy of Eq. (1)
reaches 0.046 mean violation (Tab. 1), an 80% reduction over random (0.231); Skywork-Reward,
lacking any structural verification, satisfies all constraints on only 21% of problems versus our
method’s 28% pass@1. Ablating the two terms of Eq. (1) reveals complementary contributions:
Equality alone achieves 0.058 mean violation, Econstraint alone achieves 0.038, and the combination


                                                                  7
                                                                                                                                             0.5                                                           0.4
                       100                                                                                                                                                 Distributional EBM selection




                                                                                                                Constraint violation score
                                                                                                                                             0.4
                       80                                                                                                                                                                                  0.3




                                                                                                                                                                                                              Violation score
          pass@N (%)
                                                                                                                                             0.3
                       60                                                                                                                                                                                  0.2
                                                                                                                                             0.2
                       40                          GSM8K               K&K                                                                                                                                 0.1
                                                   MuSR                Distributional EBM                                                    0.1
                       20                          TravelPlanner       Random ranking
                                                   TACO
                                                                                                                                             0.0                                                           0.0
                        0
                             1 2               4          8                            16                                                              4         2               0            2
                  N (top-N by energy ranking)                                                                                                                  Learned energy quality
Figure 3: Pass@N [Chen et al., 2021] curves. The                                                        Figure 4: Energy decomposition on TravelPlanner
Distributional EBM front-loads correct candidates:                                                      (n=1,487 parseable candidates; both axes: lower ↓ bet-
pass@2 reaches 97.5% on GSM8K and 71.5% on                                                              ter). Stars mark Distributional EBM selections. µquality
MuSR. TravelPlanner uses a relaxed violation thresh-                                                    discriminates horizontally; Econstraint vertically. Selec-
old (θ=0.15).                                                                                           tions cluster in the low-energy, low-violation corner.

(0.046) outperforms Equality alone while adding learned quality dimensions that the constraint checker
does not cover. Fig. 4 visualises the two-dimensional energy landscape; the two components
agree on the top candidate in only 2% of problems, and in 28% of cases the combined energy
selects a candidate that neither component would choose independently. On tasks without analytical
constraints (GSM8K, MuSR, TACO), the method reduces to distributional µquality reranking alone
and still provides substantial gains. TravelPlanner improvements over frontier models stem from the
analytical constraint checker catching hallucinated transport routes (24-28% satisfaction for frontier
models) that LLMs cannot self-detect. Independent LLM judges (Opus 4.6, Sonnet 4.6) corroborate
the violation score and rate EBM-selected plans above oracle picks; full statistics in §F.6. Where
structural verification is available, the verifier captures signal frontier models cannot self-detect;
where pretraining-scale priors dominate (narrative, code semantics), frontier models lead: the two
routes are complementary, not competing. Per-difficulty breakdowns for TACO and K&K are in §F.3.
(iii) Ensemble uncertainty as a decision signal. Two-pass σ-triage (Eq. (5)) helps when pass-1 has
headroom and feedback is structured: on TravelPlanner (Qwen-only generator pool, used to isolate
the feedback effect from candidate diversity), it improves pass@1 from 74.0% to 80.0% (+6.0 pp).
On TACO (deconfounded), two-pass is neutral (88.6%); on GSM8K, it is mildly counterproductive
(−1.7 pp) precisely because the generator has memorised the answer and feedback distracts retrieval,
a diagnostic feature: σ-triage detects which regime each task falls into rather than applying a one-
size-fits-all loop. For selective prediction [Geirhos et al., 2020a], σquality is task-dependent: on
TravelPlanner, abstaining on 40% of problems raises pass@1 from 28.0% to 36.7% (+8.7 pp); on
MuSR, σ does not signal correctness (AUROC 0.44), and the verifier is honest about where it cannot
triage rather than offering an unreliable signal. The when-it-helps regime appears to depend on
constraint-checkability and label discreteness rather than scoring task; we discuss the pattern in §F.5.
Fig. 5 visualises the (µquality , σquality ) space; full results are in §F.5 and §F.4.
                             GSM8K                                 MuSR                             TravelPlanner                                                     TACO                                 K&K
                                                   0.75
                                                                                                                                                           2
          1.0                                                                           0.75                                                                                                      2
quality




                                                   0.50
          0.5                                      0.25                                 0.50                                                               1                                      1

                             4             2                       1              0             4           2                                  0                     5.0         2.5                  10     8                  6
                                 quality                           quality                                quality                                                          quality                         quality
                                                                                      Correct       Incorrect                                      = 0.8
Figure 5: σ-triage decision surface (µquality vs. σquality per problem). On GSM8K, incorrect selections (red)
are interspersed with correct ones. On MuSR, all σquality < θσ =0.8 (dashed), so triage never triggers. On
TravelPlanner, the wider σquality spread reflects continuous violation labels.

(iv) Reasoning quality vs. model-identity shortcuts. When candidate generators have different
accuracy levels, the scorer may learn to identify which model produced each candidate rather than
evaluating reasoning quality [Geirhos et al., 2020b]. A cross-dataset confounding analysis (per-
model pick distributions and cross-model correct-energy spreads) finds no fingerprinting on four
of five tasks: GSM8K, MuSR, TravelPlanner, and K&K all show near-uniform picks and small
spreads despite large generator accuracy gaps (full numbers in §F.8). On TACO the initial scorer
fingerprinted strongly; a causal style-swap test confirms a formatting shortcut, mitigated via deep
feature reweighting (DFR; Kirichenko et al., 2023) on the energy heads only (0.4% of parameters),
restoring uniform picks at 88.6% pass@1 with +13.3 pp on HARD and +14.4 pp on UNKNOWN


                                                                                                      8
problems. The determining factor is output format, not generator accuracy gap: K&K has a more
extreme accuracy split (88 pp) than TACO (74 pp), yet no fingerprinting, because reasoning text is
stylistically similar across generators while code contains strong model-specific structural patterns.
(v) Cross-domain transfer.             To test
whether the quality scorer captures trans- Table 2: Zero-shot transfer (Distributional EBM pass@1;
ferable reasoning signals, we evaluate each shaded = in-domain; bold = best per column; underlined =
dataset’s checkpoint on every other dataset second-best). The TP column reports pass@1 (zero-violation
zero-shot (i.e., no retraining). Tab. 2 reports rate) for all rows except the K&K source row marked ⋄ , which
the key results. Three patterns emerge, all reports mean violation (lower better; random = 0.231).
explained by training-data difficulty and
signal-regime alignment. First, hard-to- Source                GSM8K MuSR            TP      TACO K&K
easy transfer succeeds: a MuSR-trained GSM8K                     97.0        64.9    0.0      39.8      92.4
scorer achieves 93.9% on GSM8K zero- MuSR                        93.9        67.7    0.0      36.4      89.0
shot (96.1% with the DeBERTa backbone TP                         93.1        60.9   28.0      56.4      33.5
variant; §F.7), within 3.4 pp of in-domain TACO                  92.5        58.9   43.3      88.6      31.1
self-consistency (97.3%) without ever see- K&K                   94.9        64.9   0.1⋄      51.1      99.9
ing a math problem. High candidate-
accuracy entropy (MuSR 57%) forces the SC                        96.1        64.4   12.0      36.4      56.4
scorer to learn genuine reasoning-quality Rand                   91.7        53.0   14.0      46.6      58.7
signals; high contamination (GSM8K 95%
candidate accuracy) leaves few informative negatives, so the GSM8K-trained scorer reaches only
64.9% on MuSR – close to self-consistency (64.4%) but not exceeding it. Second, reasoning text
and code are different signal regimes: reasoning-trained scorers (GSM8K, MuSR) do not transfer to
TACO, but TACO→TravelPlanner transfers positively because code-execution labels capture quality
signals that partially generalise to constrained planning (Tab. 2). Beyond cross-domain transfer, the
verifier also transfers across generator distributions: a Qwen-only-trained scorer evaluated on a
multi-model candidate pool reaches 69.5% pass@1 on MuSR (matching the multi-trained scorer’s
67.7%) and 90.5% on GSM8K, confirming the quality signal is not coupled to the training-pool
generator style (§F.7). Calibration also transfers more broadly than ranking: a GSM8K-trained scorer
achieves σ-AUROC of 0.79 on TravelPlanner zero-shot despite providing no ranking lift, suggesting
ensemble disagreement captures a domain-general difficulty signal. The full transfer matrix including
MATH-500 and a heatmap visualisation (Fig. 10) are in §F.7.
Limitations. (i) Generator ceiling: when no correct candidate exists, even perfect scoring cannot
succeed (14% of MuSR; 58% of TravelPlanner at strict zero-violation). (ii) Format dependence: a
GSM8K scorer achieves 65.6% on MATH-500 [Hendrycks et al., 2021], below random (68.4%),
because it learned format signals rather than reasoning quality. (iii) Calibration limits: on MuSR,
σ-AUROC is anti-correlated (0.44), making selective prediction counterproductive. (iv) Manual
constraint design: Econstraint must be authored per task; scaling directions in §G. (v) Single-round
feedback: the two-pass loop adds only one regeneration round and is therefore less powerful than
iterative refinement [Lee et al., 2025, Madaan et al., 2023]. Full ablations are in §F.1.

5    Conclusion
Across the five reasoning tasks, three lessons emerge: (i) a 149M-parameter verifier orchestrating
cheap 7–26B open generators outperforms single-shot Qwen-72B on every benchmark and matches
frontier Claude models on constraint-heavy planning, demonstrating that the bottleneck in structured
reasoning is selection, not parameter scale; (ii) the two routes are complementary: structural verifi-
cation wins when constraints are checkable, while pretraining-scale priors win where they are not
(web-scale corpora encode narrative and code-semantic priors a small scorer cannot match; analytical
checking exposes hallucinations frontier models cannot self-detect); (iii) honest confounding analysis
confirms the scorer learns content on four of five tasks, with the lone code-formatting shortcut on
TACO fixable via last-layer retraining at no accuracy cost. The transferability of quality signals (a
MuSR scorer reaching 93.9% on GSM8K zero-shot) suggests structured reasoning shares a common
quality signature when training data is difficult enough to force genuine discrimination. Three
directions follow: replacing the heterogeneous LoRA ensemble with epistemic deep learning for an
axiomatically grounded energy in a single forward pass; extending single-round feedback to iterative
energy-guided refinement; and richer structured feedback for tasks where two-pass currently fails on
opaque signals (e.g., code execution errors).


                                                     9
6   Acknowledgments
We are grateful to Adam Crow and Harrison South for their assistance with compute infrastructure
and OpenRouter access, and to Tom Godding, Anup Jadhav, Edward Jackson, and Shefali Sharma for
many valuable technical discussions and their constructive feedback on the manuscript.

References
Anthropic. The claude model family: Claude opus 4.6, claude sonnet 4.6. Technical report, Anthropic,
  2026. https://docs.anthropic.com/en/docs/about-claude/models.

Jimmy Ba, Jamie Ryan Kiros, and Geoffrey E. Hinton. Layer normalization. ArXiv, abs/1607.06450,
  2016. URL https://api.semanticscholar.org/CorpusID:8236317.

Mathieu Blondel, Michael E Sander, Germain Vivier-Ardisson, Tianlin Liu, and Vincent Roulet.
 Autoregressive language models are secretly energy-based models: Insights into the lookahead
 capabilities of next-token prediction. arxiv:2512.15605, 2025.

Ralph Allan Bradley and Milton E. Terry. Rank analysis of incomplete block designs: I. The method
  of paired comparisons. Biometrika, 39(3/4):324–345, 1952.

Leo Breiman. Bagging predictors. Machine learning, 24(2):123–140, 1996.

Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Clark, Quoc V Le, Christopher Ré, and
  Azalia Mirhoseini. Large language monkeys: Scaling inference compute with repeated sampling.
  arxiv:2407.21787, 2024.

Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal,
  Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are
  few-shot learners. Advances in neural information processing systems, 33:1877–1901, 2020.

Davide Carbone. A hitchhiker’s guide to the relation of energy-based models with other generative
  models, sampling and statistical physics. Transactions on Machine Learning Research, 2024.
  arXiv:2406.13661.

Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared
 Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large
 language models trained on code. arxiv:2107.03374, 2021.

Zhikang Chen, Sen Cui, Deheng Ye, Yu Zhang, Yatao Bian, and Tingting Zhu. Think Consistently,
  Reason Efficiently: Energy-Based Calibration for Implicit Chain-of-Thought. arxiv:2511.07124,
  2025.

Paul F Christiano, Jan Leike, Tom Brown, Miljan Martic, Shane Legg, and Dario Amodei. Deep rein-
  forcement learning from human preferences. In I. Guyon, U. Von Luxburg, S. Bengio, H. Wallach,
  R. Fergus, S. Vishwanathan, and R. Garnett, editors, Advances in Neural Information Processing
  Systems, volume 30. Curran Associates, Inc., 2017. URL https://proceedings.neurips.cc/
  paper_files/paper/2017/file/d5e2c0adad503c91f91df240d0cd4e49-Paper.pdf.

Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser,
  Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, et al. Training verifiers to solve
  math word problems, 2021. URL https://arxiv.org/abs/2110.14168, 9, 2021.

Yuntian Deng, Anton Bakhtin, Myle Ott, Arthur Szlam, and Marc’Aurelio Ranzato. Residual energy-
  based models for text generation. In International Conference on Learning Representations (ICLR),
  2020. arXiv:2004.11714.

Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. BERT: Pre-training of deep
  bidirectional transformers for language understanding. In Proceedings of the 2019 Conference of
  the North American Chapter of the Association for Computational Linguistics (NAACL), pages
  4171–4186, 2019. arXiv:1810.04805.


                                                 10
Stanislav Fort, Huiyi Hu, and Balaji Lakshminarayanan. Deep ensembles: A loss landscape perspec-
  tive. arXiv:1912.02757, 2019.

Yarin Gal and Zoubin Ghahramani. Dropout as a Bayesian approximation: Representing model
  uncertainty in deep learning. In international conference on machine learning, pages 1050–1059.
  PMLR, 2016.

Robert Geirhos, Jörn-Henrik Jacobsen, Claudio Michaelis, Richard Zemel, Wieland Brendel, Matthias
  Bethge, and Felix A Wichmann. Shortcut learning in deep neural networks. Nature Machine
  Intelligence, 2(11):665–673, 2020a.

Robert Geirhos, Jörn-Henrik Jacobsen, Claudio Michaelis, Richard Zemel, Wieland Brendel, Matthias
  Bethge, and Felix A Wichmann. Shortcut learning in deep neural networks. Nature Machine
  Intelligence, 2(11):665–673, 2020b.

Adam Gleave and Geoffrey Irving.         Uncertainty estimation for language reward models.
  arXiv:2203.07472, 2022.

Google DeepMind. Gemma 4 technical report. Technical report, Google DeepMind, 2026.

Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad
  Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al. The llama 3 herd of
  models. arxiv:2407.21783, 2024.

Chuan Guo, Geoff Pleiss, Yu Sun, and Kilian Q Weinberger. On calibration of modern neural
  networks. In International conference on machine learning, pages 1321–1330. PMLR, 2017.

Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu
  Zhang, Shirong Ma, Xiao Bi, et al. DeepSeek-R1: Incentivizing reasoning capability in LLMs via
  reinforcement learning. arxiv:2501.12948, 2025.

Pengcheng He, Jianfeng Gao, and Weizhu Chen. Debertav3: Improving DeBERTa using ELECTRA-
  Style Pre-Training with Gradient-Disentangled Embedding Sharing, 2023. URL https://arxiv.
  org/abs/2111.09543.

Dan Hendrycks and Kevin Gimpel. Gaussian error linear units (gelus). arXiv: Learning, 2016. URL
  https://api.semanticscholar.org/CorpusID:125617073.

Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song,
  and Jacob Steinhardt. Measuring Mathematical Problem Solving With the MATH Dataset, 2021.
  URL https://arxiv.org/abs/2103.03874.

Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, and Yejin Choi. The Curious Case of Neural
  Text Degeneration. In International Conference on Learning Representations (ICLR), 2020.
  arXiv:1904.09751.

Neil Houlsby, Andrei Giurgiu, Stanislaw Jastrzebski, Bruna Morrone, Quentin de Laroussilhe, Andrea
  Gesmundo, Mona Attariyan, and Sylvain Gelly. Parameter-efficient transfer learning for NLP. In
  International Conference on Machine Learning (ICML), 2019. arXiv:1902.00751.

Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang,
  and Weizhu Chen. LoRA: Low-rank adaptation of large language models. In International
  Conference on Learning Representations (ICLR), 2022. arXiv:2106.09685.

Eric Hanchen Jiang et al.      Learning to Rank Chain-of-Thought: Using a Small Model.
  arXiv:2505.14999, 2025.

Muhammad Khalifa et al. Process Reward Models That Think. arXiv:2504.16828, 2025.

Polina Kirichenko, Pavel Izmailov, and Andrew Gordon Wilson. Last Layer Re-Training is Sufficient
  for Robustness to Spurious Correlations. In International Conference on Learning Representations
  (ICLR), 2023. arXiv:2204.02937.


                                               11
Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. Large
  Language Models are Zero-Shot Reasoners. In Advances in Neural Information Processing Systems
  (NeurIPS), 2022. arXiv:2205.11916.
Balaji Lakshminarayanan, Alexander Pritzel, and Charles Blundell. Simple and Scalable Predictive
  Uncertainty Estimation Using Deep Ensembles. In Advances in Neural Information Processing
  Systems (NeurIPS), 2017. URL https://arxiv.org/abs/1612.01474.
Yann LeCun, Sumit Chopra, Raia Hadsell, Marc’Aurelio Ranzato, and Fu Jie Huang. A Tutorial on
  Energy-Based Learning. Predicting Structured Data, 2006.
Kuang-Huei Lee, Ian Fischer, Yueh-Hua Wu, Dave Marwood, Shumeet Baluja, Dale Schuurmans,
  and Xinyun Chen. Evolving deeper LLM thinking. arxiv:2501.09891, 2025.
Rongao Li, Jie Fu, Bo-Wen Zhang, Tao Huang, Zhihong Sun, Chen Lyu, Guang Liu, Zhi Jin, and
  Ge Li. TACO: Topics in algorithmic code generation dataset. arxiv:2312.14852, 2023.
Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike,
  John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. arxiv:2305.20050, 2023.
Chris Yuhao Liu, Liang Zeng, Jiacai Liu, Rui Yan, Jujie He, Chaojie Wang, Shuicheng Yan, Yang Liu,
  and Yahui Zhou. Skywork-reward: Bag of tricks for reward modeling in LLMs. arXiv preprint
  arXiv:2410.18451, 2024.
Ilya Loshchilov and Frank Hutter. SGDR: Stochastic gradient descent with warm restarts. In
   International Conference on Learning Representations (ICLR), 2017. arXiv:1608.03983.
Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. In International Confer-
   ence on Learning Representations (ICLR), 2019. arXiv:1711.05101.
Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon,
 Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bodhisattwa Prasad Majumder,
 Katherine M. Hermann, Sean Welleck, Amir Yazdanbakhsh, and Peter Clark. Self-refine: Iterative
 refinement with self-feedback. In Advances in Neural Information Processing Systems (NeurIPS),
 2023. arXiv:2303.17651.
OpenAI. GPT-4 technical report. Technical report, OpenAI, 2023. arXiv:2303.08774.
OpenAI. Introducing gpt-oss. Technical report, OpenAI, 2025. https://openai.com/index/
  introducing-gpt-oss/.
Yonatan Oren, Nicole Meister, Niladri Bhatt, Inioluwa Deborah Raji, and Ryan Cotterell. Proving
  test set contamination in black box language models. In International Conference on Learning
  Representations (ICLR), 2024. arXiv:2310.17623.
Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong
  Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to fol-
  low instructions with human feedback. In Advances in Neural Information Processing Systems
  (NeurIPS), 2022. arXiv:2203.02155.
Qwen Team. Qwen2.5 technical report. arXiv:2412.15115, 2024.
Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, and Chelsea
  Finn. Direct preference optimization: Your language model is secretly a reward model. In Advances
  in Neural Information Processing Systems (NeurIPS), 2023. arXiv:2305.18290.
Charlie Victor Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. Scaling LLM test-time compute
  optimally can be more effective than scaling parameters for reasoning. In The Thirteenth In-
  ternational Conference on Learning Representations, 2025. URL https://openreview.net/
  forum?id=4FWAwZtd2n.
Zayne Sprague, Xi Ye, Kaj Bostrom, Swarat Chaudhuri, and Greg Durrett. Musr: Testing the limits of
  chain-of-thought with multistep soft reasoning. In B. Kim, Y. Yue, S. Chaudhuri, K. Fragkiadaki,
  M. Khan, and Y. Sun, editors, International Conference on Learning Representations, volume
  2024, pages 14670–14728, 2024.


                                                12
Nisan Stiennon, Long Ouyang, Jeff Wu, Daniel M. Ziegler, Ryan Lowe, Chelsea Voss, Alec Radford,
  Dario Amodei, and Paul Christiano. Learning to summarize from human feedback. In Proceedings
  of the 34th International Conference on Neural Information Processing Systems, NIPS ’20, Red
  Hook, NY, USA, 2020. Curran Associates Inc. ISBN 9781713829546.
Zhiquan Tan and Yinrong Hong. A theoretical lens for rl-tuned language models via energy-based
  models. arxiv:2512.18730, 2025.
Jonathan Uesato, Nate Kushman, Ramana Kumar, Francis Song, Noah Siegel, L. Wang, Antonia
  Creswell, Geoffrey Irving, and Irina Higgins. Solving math word problems with process- and
  outcome-based feedback. ArXiv, abs/2211.14275, 2022. URL https://api.semanticscholar.
  org/CorpusID:254017497.
Junlin Wang, Jue WANG, Ben Athiwaratkun, Ce Zhang, and James Zou. Mixture-of-agents enhances
  large language model capabilities. In The Thirteenth International Conference on Learning
  Representations, 2025. URL https://openreview.net/forum?id=h0ZfDIrj7T.
Peiyi Wang, Lei Li, Zhihong Shao, Runxin Xu, Damai Dai, Yifei Li, Deli Chen, Yu Wu, and Zhifang
  Sui. Math-shepherd: Verify and reinforce LLMs step-by-step without human annotations. In
  Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (ACL),
  2024.
Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H. Chi, Sharan Narang, Aakanksha
  Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language
  models. In The Eleventh International Conference on Learning Representations, 2023. URL
  https://openreview.net/forum?id=1PL1NIMMrw.
Benjamin Warner, Antoine Chaffin, Benjamin Clavié, Orion Weller, Oskar Hallström, Said
  Taghadouini, Alexis Gallagher, Raja Biswas, Faisal Ladhak, Tom Aarsen, et al. Smarter, better,
  faster, longer: A modern bidirectional encoder for fast, memory efficient, and long context finetun-
  ing and inference. In Proceedings of the 63rd Annual Meeting of the Association for Computational
  Linguistics (Volume 1: Long Papers), pages 2526–2547, 2025.
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny
  Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. Advances in
  neural information processing systems, 35:24824–24837, 2022.
Yu Xia, Jingru Fan, Weize Chen, Siyu Yan, Xin Cong, Zhong Zhang, Yaxi Lu, Yankai Lin, Zhiyuan
  Liu, and Maosong Sun. AgentRM: Enhancing agent generalization with reward modeling. In
  Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar, editors,
  Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume
  1: Long Papers), pages 19277–19290, Vienna, Austria, July 2025. Association for Computational
  Linguistics. ISBN 979-8-89176-251-0. doi: 10.18653/v1/2025.acl-long.945. URL https:
  //aclanthology.org/2025.acl-long.945/.
Chulin Xie, Yangsibo Huang, Chiyuan Zhang, Da Yu, Xinyun Chen, Bill Yuchen Lin, Bo Li, Badih
  Ghazi, and Ravi Kumar. On memorization of large language models in logical reasoning. In
  IJCNLP-AACL, 2024a. URL https://api.semanticscholar.org/CorpusID:273695832.
Jian Xie, Kai Zhang, Jiangjie Chen, Tinghui Zhu, Renze Lou, Yuandong Tian, Yanghua Xiao,
   and Yu Su. Travelplanner: A benchmark for real-world planning with language agents. In
   International Conference on Machine Learning, 2024b. URL https://api.semanticscholar.
   org/CorpusID:267406800.
Shuo Yang, Wei-Lin Chiang, Lianmin Zheng, Joseph E. Gonzalez, and Ion Stoica. Rethinking
  benchmark and contamination for language models with rephrased samples. ArXiv, abs/2311.04850,
  2023. URL https://api.semanticscholar.org/CorpusID:265050721.
Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, and Karthik R
  Narasimhan. Tree of thoughts: Deliberate problem solving with large language models. In
  Thirty-seventh Conference on Neural Information Processing Systems, 2023. URL https://
  openreview.net/forum?id=5Xc1ecxO1h.


                                                 13
Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang,
  Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, and Ion Stoica.
  Judging LLM-as-a-judge with MT-bench and chatbot arena. In Advances in Neural Information
  Processing Systems (NeurIPS), 2023.
Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale Schuurmans,
  Claire Cui, Olivier Bousquet, Quoc V Le, and Ed H. Chi. Least-to-most prompting enables
  complex reasoning in large language models. In The Eleventh International Conference on
  Learning Representations, 2023. URL https://openreview.net/forum?id=WZH7099tgfM.




                                             14
A     Proofs of Theoretical Results
This section provides full proofs and the detailed consequences/implications of Theorem 3.1 and
Theorem 3.2 from Sec. 3.2.

A.1   Proof of Theorem 3.1: ensemble ranking under correlated adapters

For each adapter k, define the binary correctness indicator
                                                             (x, y − ) ∈ {0, 1},
                                 k
                                        (x, y + ) < Equality
                                                     k
                                                                      
                        Vk = 1 Equality
so that E[Vk ] = q and Var(Vk ) = q(1 − q). The exchangeable correlation assumption is
Corr(Vj , Vk ) = ρ for all j ̸= k, equivalently Cov(Vj , Vk ) = ρ q(1 − q).
         PK
Let V = k=1 Vk be the total correct-vote count. Then
                                                                                      
 E[V ] = Kq,        Var(V ) = K q(1 − q) + K(K − 1) ρ q(1 − q) = Kq(1 − q) 1 + (K − 1)ρ .
The ensemble mean µquality (x, y + ) < µquality (x, y − ) iff V > K/2, i.e., a strict majority of adapters
vote correctly. Under the Gaussian approximation (which the central limit theorem supports for
K ≥ 5 in the parameter range we consider),
                            approx
                                                                          
                        V     ∼ N Kq, Kq(1 − q) 1 + (K − 1)ρ ,
and standardising,
                                                                                               !
                                                                      Kq − K/2
              Pensemble (K, q, ρ) = P(V > K/2) = Φ p
                                                      Kq(1 − q)(1 + (K − 1)ρ)
                                                  √          !
                                            K (q − 21 )
                                 =Φ p                          ,
                                      q(1 − q)(1 + (K − 1)ρ)
which is Eq. (2).
For the limit, write the argument of Φ as
                             √
                               K (q − 21 )             (q − 12 )
                       p                        =q                   .
                         q(1 − q)(1 + (K − 1)ρ)   q(1 − q) 1 + K−1 ρ    K       K
          1
                                                                                                   p
As K → ∞, K → 0 and K−1                                                    1
                     K → 1, so for any ρ > 0 the argument converges to (q− 2 )/                     q(1 − q)ρ,
giving Eq. (2):
                                                      !
                     ∞                   q − 12
                    P (q, ρ) = Φ p                        <1   for any finite q ∈ ( 12 , 1).
                                  q(1 − q)ρ
The ceiling is strictly below√1 because the argument of Φ is finite. Only when ρ = 0 (perfectly
independent adapters) does K in the numerator dominate, sending Pensemble → 1.

Detailed consequences.      Three consequences follow.
(C1) Diversity amplification. ∂Pensemble /∂ρ < 0 for q > 12 : lower inter-adapter correlation strictly
     improves ensemble accuracy. This is non-obvious because one might expect that highly
     correlated (i.e., individually strong) adapters would produce a stronger ensemble; the proof
     shows the opposite.
(C2) Diminishing returns of K at high correlation. When ρ = 1, all adapters are perfectly
     correlated and Pensemble → q regardless of K: adding more identical adapters provides zero
     benefit. When ρ < 1, ensemble accuracy increases with K but saturates at the ceiling P ∞ (q, ρ).
(C3) Ceiling binding regime. Empirically, at K=5, the gap P ∞ − Pensemble (K=5) is small in our
     regime (less than 1 pp for typical (q, ρ) pairs we observe), so additional adapters yield strongly
     diminishing returns once K ≳ 5. The ceiling is binding for tasks where per-adapter accuracy q
     is moderate (e.g., narrative reasoning where q ≈ 0.6) and slack only for tasks where q is near
     unity (e.g., K&K with high adapter accuracy).
The implication is that ensemble diversity is necessary but not sufficient: a fundamental ceiling is
determined by the joint (q, ρ) of the adapter architecture and training distribution.


                                                      15
A.2      Proof of Theorem 3.2: partitioned variance under energy decomposition

We have E(x, y) = µquality (x, y) + λ · Econstraint (x, y) where Econstraint is a deterministic analytical
function of (x, y) with no learnable parameters and no stochastic components. Treating µquality as a
random variable (over the ensemble’s epistemic uncertainty), the variance of a sum of a random and
a deterministic quantity is:
           Var(E) = Var(µquality + λ Econstraint )
                                                                                                   2
                       = Var(µquality ) + λ2 Var(Econstraint ) +2λ Cov(µquality , Econstraint ) = σquality ,
                                             |    {z        }      |         {z              }
                                                             =0                                =0

since the variance of any deterministic function is 0 and the covariance of any random variable with a
deterministic quantity is 0. This gives Eq. (3).
For the monolithic comparison, suppose a single scorer Emono is trained jointly to predict both
                                                     mono              mono
quality and constraint satisfaction, Emono (x, y) = Equality (x, y) + Econstraint (x, y), where now both
components are random variables under the scorer’s epistemic uncertainty. Then
                                    mono             mono                  mono       mono
                 Var(Emono ) = Var(Equality ) + Var(Econstraint ) + 2 Cov(Equality , Econstraint ).
              2                                                                       mono
This equals σquality  only in the degenerate case where the monolithic scorer learns Econstraint exactly
           mono
(so Var(Econstraint ) = 0 and the covariance term vanishes); otherwise the variance mixes constraint-
prediction error into the uncertainty signal.

Detailed implications.              Three implications follow.

(I1) Interpretable uncertainty. σquality measures exactly how uncertain the ensemble is about reason-
     ing quality, with zero contribution from constraint verification. A monolithic scorer’s uncertainty
     conflates both sources and cannot distinguish “uncertain about quality” from “uncertain about
     constraints.”
(I2) Strictly lower predictive variance. The decomposition yields strictly lower predictive variance
     than a monolithic scorer whenever the analytical constraints have lower error than a learned
     approximation. This holds by construction for TravelPlanner (database-verified routes) and
     K&K (statement-consistency checker), where Econstraint is exact.
(I3) Natural decision rule. The σ-triage mechanism (Sec. 3.5) is the natural decision rule under this
     partitioned variance:
        • Accept when both σquality and Econstraint are low (quality reliable, constraints satisfied).
        • Regenerate with constraint feedback when Econstraint is high (constraints violated, regardless
          of σquality ).
        • Regenerate with quality feedback when σquality is high but Econstraint is low (constraints fine,
          quality uncertain).
        • Abstain when σquality exceeds a threshold (quality completely unknown).

B       Model Details
This section details the candidate generators (Tab. 3), scorer backbones (Tab. 4), ensemble architecture
(Tab. 5), and training configuration (Tab. 6).

B.1      Candidate Generators


Table 3: Candidate generator models. All models are frozen throughout and accessed via the OpenRouter API.
Active parameters are listed for mixture-of-experts models.
Model                                              Architecture            Parameters       Context   Role
Qwen-2.5-7B-Instruct [Qwen Team, 2024]             Dense Transformer           7B            128K     7B baseline; pass-2 generator
LLaMA-3.1-8B-Instruct [Grattafiori et al., 2024]   Dense Transformer           8B            128K     8B baseline; highest error diversity
Gemma-4-26B-IT [Google DeepMind, 2026]             Mixture-of-Experts    26B (4B active)     128K     Strongest generator across all tasks
GPT-OSS-20B [OpenAI, 2025]                         Mixture-of-Experts   20B (3.6B active)    128K     Reasoning model (extended thinking)



                                                                   16
Gemma-4-26B-IT consistently produces the highest candidate accuracy across all four benchmarks
(96.7% on GSM8K, 66.7% on MuSR, 67.9% on TravelPlanner, 84.6% on TACO; see Tab. 8).
LLaMA-3.1-8B-Instruct produces the lowest accuracy but contributes the most diverse error patterns:
on GSM8K, it provides 1,309 unique negative problems, 4-10× more than the other generators.
GPT-OSS-20B is a reasoning model that outputs extended thinking traces before the final answer; we
set max_tokens=4096 to capture both the reasoning and the response.

B.2       Frontier Models

Three frontier models are evaluated as single-shot baselines on TravelPlanner and TACO: Claude
Opus 4.6 and Claude Sonnet 4.6 [Anthropic, 2026], and Qwen-72B [Qwen Team, 2024]. All generate
a single deterministic output at T =0 with max_tokens=2048. Opus 4.6 also serves as the primary
LLM judge for the TravelPlanner quality validation (Sec. 4.2).

B.3       Scorer Backbones


                                             Table 4: Scorer backbone comparison.
    Backbone                                                    Parameters          Max context          Trainable / backbone
    ModernBERT-base [Warner et al., 2025]                            149M                8,192                      ∼3%
    DeBERTa-v3-base [He et al., 2023]                                 86M                 512                       ∼3%

ModernBERT-base is the primary backbone for all experiments. Its 8,192-token context accommo-
dates MuSR narratives (3,000-6,000 characters) and TravelPlanner itineraries without truncation.
DeBERTa-v3-base is evaluated as an ablation; its 512-token context truncates long inputs but pro-
duces better-calibrated uncertainty estimates (ECE 0.10 vs. 0.32 on GSM8K) and stronger zero-shot
transfer (96.1% on GSM8K from MuSR training vs. 93.9% for ModernBERT).

C         Implementation Details
                                                                           k
Energy head architecture. Each adapter k has an independent energy head: Equality (x, y) =
                        
MLPk LayerNorm(hkCLS ) , where MLPk consists of Linear(d→d), GELU [Hendrycks and Gimpel,
2016], Dropout(p), Linear(d→1), preceded by LayerNorm [Ba et al., 2016].

Table 5: Heterogeneous LoRA ensemble configuration. All adapters share a single frozen encoder backbone.
Structural diversity in rank, scaling, and target modules forces disagreement that reflects epistemic uncertainty.
ModernBERT targets are shown; DeBERTa uses query, key, value, and output projections analogously.
                   Adapter          Rank      Alpha       Dropout            Target Modules (ModernBERT)
                      0               8           16           0.2           Wqkv
                      1               8           16           0.2           Wqkv, Wo
                      2              16           32           0.2           Wqkv
                      3               4            8           0.2           Wqkv
                      4               8           16           0.2           Wqkv, Wi


Table 6: Training configuration per dataset. All use AdamW with weight decay 0.01, cosine annealing, 10%
warmup, gradient clipping at L2 norm 1.0, and per-adapter bagging (80% of problems).
Dataset            Train problems    Candidates   Usable problems    Pairs       Batch size           Max length         Early stop patience
GSM8K                  7,473         32 (multi)        2,464         39,424         32                   8,192                   2
MuSR                    605          32 (multi)         544           8,704   8 (MB) / 16 (DB)   4,096 (MB) / 512 (DB)           2
TravelPlanner           175          32 (multi)         175           2,800         32                   8,192                   2
TACO                    601          32 (multi)         559           7,096         32                   5,120                   2
Knights & Knaves       6,200         32 (multi)        4,426         70,816         16                   1,536                   3



Energy head architecture. Each adapter’s energy head maps the [CLS] representation to a scalar
energy: LayerNorm(d) → Linear(d, d) → GELU → Dropout(0.2) → Linear(d, 1), where d=768


                                                                     17
for both ModernBERT-base and DeBERTa-v3-base. Trainable parameters per adapter: LoRA weights
(∼0.3-1.2M depending on rank and target modules) plus energy head (∼0.6M), totalling ∼3% of
backbone parameters per member. The full K=5 ensemble adds ∼15% trainable overhead relative to
the frozen backbone.

DeBERTa adapter configuration. DeBERTa-v3-base uses disentangled attention projections in-
stead of fused QKV. The heterogeneous adapters target: adapter 0: query_proj, value_proj;
adapter 1: query_proj, value_proj, key_proj; adapter 2: query_proj, value_proj
(r=16); adapter 3: query_proj, value_proj (r=4); adapter 4: query_proj, value_proj,
output_proj.

Training dynamics. On GSM8K (ModernBERT multi-model), all five adapters converge within
3-4 epochs, with best validation losses of 0.055-0.058. On MuSR (ModernBERT multi-model),
adapters train for 3-4 epochs with best validation losses of 0.64-0.65 (well below the random
baseline of log 2 ≈ 0.693, confirming that a learnable signal is present despite the difficulty of the
task). DeBERTa adapters consistently train for more epochs (5 on MuSR, 2-5 on GSM8K) than
ModernBERT, reflecting more stable optimisation at the shorter 512-token context. All training uses
fp16 automatic mixed precision on a single NVIDIA L40S (46 GB); peak memory usage is ∼31 GB
at batch size 32. Wall-clock time per adapter is ∼20 minutes per epoch on GSM8K and ∼5 minutes
per epoch on MuSR.

D     Training Data Details
D.1   GSM8K

Multi-model candidates: 7,473 problems × 32 candidates (8 per generator). Classification by answer
matching yields an overall candidate accuracy of 95% (dominated by contamination). Of 7,473
problems, 2,464 have both correct and incorrect candidates across the four generators (usable for con-
trastive training); 5,009 have all-correct pools (excluded). LLaMA-3.1-8B contributes 1,309 unique
negative problems (91.4% accuracy), providing 4-10× more negatives than the other generators.
Contrastive pairs are capped at 16 per problem, yielding 39,424 total pairs split 80/20 at the problem
level.

D.2   MuSR

756 problems split 80/20: 605 train, 151 test. Multi-model candidates: 32 per problem (8 per
generator, except Qwen which contributes 16 on some subsets). Average candidate accuracy: 57%.
Of 605 train problems, 544 (90%) have both correct and incorrect candidates, providing 3× better
coverage than GSM8K despite being 12× smaller. This coverage advantage is the primary reason
MuSR produces stronger training signal per problem.

D.3   TravelPlanner

175 train, 50 test problems from the validation split (sole-planning mode). Multi-model candidates:
32 per problem. Classification uses a continuous violation score in [0, 1] aggregating 8 normalised
constraint dimensions. Positives are the top 25% (8 of 32) per problem; negatives are the bottom 75%
(24 of 32). All 175 train problems have both positives and negatives by construction. Gemma-4-26B
dominates with 67.9% of its candidates in the positive set; LLaMA achieves only 8.6%.

D.4   TACO

695 fully-clean problems from likaixin/TACO-verified, filtered to drop VERY_HARD (0% solve
rate). 601 train, 94 test (88 test problems usable after filtering all-correct and all-incorrect pools).
Classification by automated test execution: candidates pass if every test case returns correct output
within a 4-second timeout. Positives capped at 8 per problem; negatives capped at 24, ranked by
status severity. Overall candidate accuracy: 31.9% (train), with Gemma-4-26B at 84.6% producing
58% of all positives. A confounding analysis (§F.8) confirmed this imbalance caused a model-identity
shortcut; DFR [Kirichenko et al., 2023] retraining on group-balanced data mitigates it.


                                                  18
E     Dataset Details
E.1       Exploratory Data Analysis

We characterise the four benchmarks along three axes: scale (split sizes and candidate counts),
length (problem and candidate token counts under the ModernBERT tokenizer), and difficulty (a
dataset-specific proxy: number of reasoning steps for GSM8K, MuSR subset and number of choices,
trip duration in days for TravelPlanner, and official difficulty label for TACO).

    Table 7: Dataset overview. Candidate accuracy is the fraction of correct candidates across all generators.
Dataset            Train    Test   N    Cand. accuracy         Label type                 Econstraint           Primary metric
GSM8K              7,473   1,319   32            95%     Binary (answer match)               None               pass@1
MuSR                 605     151   32            57%     Binary (answer match)               None               pass@1
TravelPlanner        175      50   32        Top-25%     Continuous (viol. score)        5 constraints          Mean violation
TACO                 601      88   32            32%       Binary (execution)                None               pass@1
Knights & Knaves   6,200     700   32            58%      Binary (exact match)      Statement consistency       pass@1



E.2       Per-Model Candidate Quality


Table 8: Per-model candidate accuracy on the training set. Gemma-4-26B consistently dominates; LLaMA-3.1-
8B contributes the most diverse errors.
               Model                    GSM8K        MuSR        TravelPlanner         TACO             K&K
               Gemma-4-26B-IT           96.7%        66.7%            67.9%            84.6%            99.9%
               GPT-OSS-20B              96.1%        65.3%             9.8%            25.8%            99.0%
               Qwen-2.5-7B              95.1%        51.4%            13.6%            16.9%            19.7%
               LLaMA-3.1-8B             91.4%        49.7%             8.6%            10.5%            11.7%

On GSM8K, the high candidate accuracy (91-97%) across all models reflects likely contamination.
On MuSR, the gap between Gemma (67%) and Qwen/LLaMA (∼50%) is substantial, providing
the diversity of error patterns that drives contrastive learning. On TACO, Gemma produces 58%
of all positive candidates. The initial scorer selected Gemma in 98% of test problems; after DFR
deconfounding, picks are distributed uniformly (22/24/34/20%).

E.3       GSM8K

GSM8K [Cobbe et al., 2021] comprises 8,792 grade-school math word problems (7,473 train, 1,319
test). Each problem is a short narrative ending with a question; the solution is a chain-of-thought
derivation concluding with a numeric answer after the #### delimiter. On GSM8K, Econstraint does not
apply (no structured constraints beyond answer correctness), so the method reduces to distributional
µquality reranking only.
The primary metric is pass@1 after reranking. Secondary metrics include pass@N [Chen et al.,
2021] curves, energy separation (mean energy gap between correct and incorrect candidates), Kendall
τ rank correlation, σ-AUROC, and expected calibration error (ECE; Guo et al., 2017).

Contamination. GSM8K was released in 2021 and is widely included in LLM pretraining [Yang
et al., 2023]. Random candidate accuracy of 92.7% and self-consistency at 97.3% are both implausibly
high for grade-school math, suggesting that generators are reproducing memorised answers rather
than reasoning. We report GSM8K for completeness and backward comparability, but emphasise
MuSR (released 2024, post-dating all generators’ pretraining) as the clean signal.

E.4       MuSR

MuSR [Sprague et al., 2024] (Multi-step Soft Reasoning) consists of 756 narrative reasoning problems.
Three subsets test distinct reasoning capacities: murder mysteries (250 problems, 2 choices) require
identifying a perpetrator from a narrative with multiple suspects; object placements (256 problems, 3
choices) require tracking object locations across a multi-paragraph narrative; team allocation (250


                                                         19
Table 9: Qualitative examples from each benchmark. Each row shows a truncated problem, a candidate excerpt,
and the verification outcome. Correct candidates receive low energy; incorrect candidates receive high energy.
Dataset       Problem (truncated)                              Candidate excerpt                                       Verdict
GSM8K         Janet’s ducks lay 16 eggs per day. She eats      Janet has 16 eggs per day. She eats 3 and bakes 4, so   Correct
              three for breakfast every morning and bakes      she uses 3 + 4 = 7 eggs. She has 16 − 7 = 9 eggs        E=−2.95
              muffins for her friends every day with four.     left. She sells them for $2 each: 9 × 2 = 18.
              She sells every remaining duck egg at the        #### 18
              farmers’ market for $2 each. How much
              does she make every day?
MuSR          A murder mystery narrative (3,200 chars):        Let me trace the evidence step by step. Alice has an    Correct (B)
              three suspects at a dinner party. Motive, al-    alibi confirmed by two witnesses. . . Bob was seen      E=−0.31
              ibi, and physical evidence described across      near the kitchen. . . The knife found matches Bob’s
              6 paragraphs. “Who is the most likely            set. . .
              murderer?” Choices: (A) Alice, (B) Bob,          #### 2
              (C) Carol.
TravelPlanner Please provide a travel plan departing from      [{“days”: 1, “current_city”: “from                      0 violations
              Las Vegas to Denver for 3 days, March 12-        Las Vegas to Denver”, “transportation”:                 viol. score: 0.00
              14, 2022. Budget: $1,600. Solo trip.             “Flight F3877057”, “lunch”: “The Urban
                                                               Socialite, Denver”, “dinner”: “Kloof
                                                               Street House, Denver”, “accommodation”:
                                                               “Luxury Studio Suite...”}, ...]
TACO          A flower shop has n bouquets with ai flow- def solve(): n = int(input()); a =                            Wrong answer
              ers each. Make the maximum number of list(map(int, input().split())); odd =                              test 1 failed
              large bouquets (two or more initial bouquets, sum(1 for x in a if x % 2); even = n -
              odd total). Each initial bouquet used at most odd; print(min(odd, even) + max(0, (odd
              once.                                         - even) // 2) if odd > even else odd)
K&K           Oliver says “Ethan is a knight.” Ethan says      If Oliver is a knight, his statement is true ⇒ Ethan    Correct
              “Oliver is a knave or I am a knight.” (2 char-   is a knight. Then Ethan’s statement “Oliver is a        E=−4.47
              acters)                                          knave or I am a knight” = “F or T” = T. Consistent.
                                                               {“Oliver”: “knight”, “Ethan”:
                                                               “knight”}




problems, 3 choices) require matching people to roles based on described traits. Narratives span
3,000-6,000 characters and require multi-hop inference over entities and attributes.
Econstraint does not apply; the method reduces to distributional reranking. The primary metric is
pass@1.

E.5       TravelPlanner

TravelPlanner [Xie et al., 2024b] is a multi-constraint planning benchmark. Given a natural-language
query specifying a trip (origin, destinations, dates, budget, preferences), the model produces a day-by-
day JSON itinerary. All experiments use sole-planning mode: human-curated reference information
is provided directly to the LLM.
We define five analytical constraint terms following the original benchmark categories [Xie et al.,
2024b], each verified against the sandbox database:

          • Budget: Cbudget = excess/budget, normalised to [0, 1].
          • Connectivity: fraction of inter-city legs with invalid transport routes.
          • Completeness: fraction of missing required fields (accommodation, meals, attractions per
            day).
          • Preferences: fraction of unsatisfied user preferences.
          • Diversity: fraction of repeated entities across days.

Additionally, hallucination count (entities not in the sandbox), structure violations (route reasonable-
ness), and parse success are tracked. The violation score is the mean of all 8 normalised dimensions.
The primary metric is mean violation score; secondary metric is pass@1 at θ=0 (zero violations).

LLM-as-Judge candidate pool (GSM8K). LLM-as-Judge in Tab. 1 is evaluated on a slightly more
lenient GSM8K candidate pool than the rest of the comparison: random pass@1 is 92.0% (vs. 92.7%
on our pool) and oracle@32 is 99.2% (vs. 98.5%). The judge’s headline 99.2% essentially matches
its pool’s oracle, so the row reflects pool ceiling rather than a clean head-to-head with our scorer.


                                                                    20
E.6   TACO

TACO [Li et al., 2023] (Topics in Algorithmic Code generation) consists of competitive programming
problems sourced from Codeforces, AtCoder, and related platforms. We use the verified subset
(likaixin/TACO-verified), filtered to drop VERY_HARD problems (0% solve rate). Each problem
includes a description, input/output format, constraints, and test cases.
Verification is execution-based: candidate code is extracted from the chain-of-thought response,
executed against all test cases with a 4-second timeout per test, and labelled correct only if every test
passes. Econstraint does not apply; the binary execution label serves as both the training signal and the
evaluation metric. The primary metric is pass@1.

Contamination note. TACO problems are sourced from public competitive-programming sites.
Per-difficulty pass@1 (particularly HARD) is the cleanest signal for genuine reasoning; EASY problems
are likely seen during pretraining.

E.7   Knights and Knaves

Knights and Knaves (K&K) puzzles [Xie et al., 2024a] are formal deductive reasoning problems.
Each puzzle presents n characters (2-8), each either a knight (always tells the truth) or a knave
(always lies), each making exactly one statement. The task is to determine the unique assignment of
knight/knave labels satisfying all statements simultaneously.
We use the dataset of Xie et al. [2024a] from HuggingFace (K-and-K/knights-and-knaves):
6,200 train and 700 test problems (100 per tier, 2ppl-8ppl). Candidates are classified by exact
match against the ground-truth boolean assignment. A statement-consistency constraint checker
independently verifies Econstraint =0 ⇔ correct on all 34,120 candidates checked, confirming perfect
verification.
Token lengths are short (p50∼900 tokens for problem + candidate CoT); we use max_length=1536.
Per-model accuracy reveals an extreme split: Gemma-4-26B and GPT-OSS-20B achieve ∼99%
accuracy, while Qwen-2.5-7B (19.7%) and LLaMA-3.1-8B (11.7%) rarely solve puzzles beyond 3
characters. This split creates a strong model-identification confound in the multi-model setting (see
Sec. 4.2).

E.8   Qualitative Examples

Tab. 9 shows one problem-candidate pair per dataset, illustrating the input format, reasoning style, and
verification signal. The examples illustrate several properties of the benchmarks. GSM8K candidates
are short chain-of-thought derivations with a numeric answer delimiter; the verification signal is
binary answer matching. MuSR candidates involve multi-hop narrative reasoning over thousands of
characters; correct answers require tracking entities and evidence across paragraphs. TravelPlanner
candidates are structured JSON itineraries verified against 8 constraint dimensions; even “correct”
candidates (zero violations) may vary in quality, motivating the continuous scoring. TACO candidates
are executable Python code verified by automated test execution; the most common failure mode is
wrong_answer (56.6% of negatives), where syntactically valid code produces incorrect output on
edge cases.


F     Extended Results and Analysis
This section consolidates all extended results and analysis beyond the main paper. §F.1 isolates five
design choices (ensemble size, pool size, multi-model training, backbone, energy decomposition).
§F.2 reports energy separation metrics and calibration diagnostics. §F.3 breaks down per-difficulty
performance on TACO, K&K, and MuSR. §F.4 evaluates selective prediction via σ-abstention. §F.5
analyses the two-pass σ-triage mechanism across datasets and pool configurations. §F.6 decomposes
TravelPlanner violations per constraint dimension, comparing the Distributional EBM against frontier
models. §F.7 reports the full zero-shot transfer matrix including DeBERTa backbones and MATH-500.
§F.8 presents the six-phase TACO confounding analysis and DFR mitigation.


                                                   21
F.1   Ablation Studies

We isolate five design choices: ensemble size (K), candidate pool size (N ), single-model vs. multi-
model training, backbone architecture, and energy decomposition. All ablations use ModernBERT
unless noted; DeBERTa results are included where the 512-token context does not truncate candidates.

Ensemble size (Tab. 10, Fig. 6). Increasing K from 1 to 5 has negligible effect on pass@1
across all datasets: GSM8K stays at 97.0-97.2%, MuSR fluctuates between 64.9% and 66.9%, and
TACO is constant at 88.6%. The one exception is TravelPlanner, where K≥3 provides a +4 pp lift
(24.0%→28.0%), likely because the continuous violation labels create noisier gradients that benefit
from ensemble averaging. The ensemble is justified not by accuracy but by uncertainty estimation:
σ-AUROC is undefined at K=1 (single adapter has no variance) and improves to 0.87 at K=5 on
K&K. DeBERTa shows the same pattern on GSM8K (96.4-96.6% across K) and is not evaluated on
TravelPlanner, TACO, or K&K due to its 512-token context truncating candidates.

Candidate pool size (Tab. 11, Fig. 7). The Distributional EBM’s advantage over random grows
with pool size on binary-label tasks. On GSM8K, the margin increases from +4.0 pp at N =4 to
+4.3 pp at N =32. On TACO, pass@1 scales from 75.0% (N =4) to 88.6% (N =32), closing 86%
of the random-to-oracle gap. On MuSR, the advantage peaks at N =8 (+14.5 pp over random) then
diminishes at N =16 and N =32 as the pool becomes saturated with similar candidates, indicating
diminishing returns on long-context reasoning tasks.


Table 10: Ensemble size (K) sweep across all datasets and both backbones. MB = ModernBERT, DB =
DeBERTa. All multi model. TACO values are pre-DFR (the identity shortcut saturates at K=1, making the
sweep uninformative for genuine quality discrimination; after DFR deconfounding, pass@1 is 88.6%). DeBERTa
(512-token context) is not evaluated on TravelPlanner, TACO, or K&K because candidate outputs exceed its
context window.
                          K   Backbone            GSM8K       MuSR         TravelPlanner                     TACO        K&K
                          1   MB                      97.2%   66.9%                  24.0%                   92.0%      99.9%
                          3   MB                      97.0%   64.9%                  28.0%                   92.0%     100.0%
                          5   MB                      97.0%   66.9%                  28.0%                   92.0%      99.9%
                          1   DB                      96.5%   62.3%                      –                     –             –
                          3   DB                      96.4%   63.6%                      –                     –             –
                          5   DB                      96.6%   62.9%                      –                     –             –


                               (a) Accuracy vs. ensemble size                        (b) Uncertainty quality vs. ensemble size
                                                                               1.0
                    100                                                                      GSM8K
                                                                               0.9           TravelPlanner
                                                                                             TACO
                     80                                                        0.8           K&K
       pass@1 (%)




                                                                                             Chance
                                                                      -AUROC




                                                                               0.7
                     60
                                                                               0.6
                              GSM8K
                              MuSR                                             0.5
                     40       TravelPlanner
                              TACO                                             0.4
                              K&K
                     20                                                        0.3
                          1                       3              5                   1                             3             5
                                          K (ensemble size)                                              K (ensemble size)
Figure 6: Effect of ensemble size K. (a) Pass@1 is stable across K on all datasets; the ensemble does
not improve top-1 accuracy. (b) σ-AUROC improves from chance (0.5 at K=1) to 0.87 on K&K at K=5,
confirming that structurally heterogeneous adapters produce informative uncertainty. The ensemble is justified
by uncertainty estimation, not accuracy.

Single-model vs. multi-model (Tab. 12). Multi-model candidate diversity provides the largest gain
of any design choice on every dataset (Tab. 12). The effect is most dramatic on K&K (+59.8 pp) and
TACO (+52.2 pp), where the generator accuracy gap between the strongest and weakest model is
largest. On MuSR, single-model training (Qwen only, 53.6%) barely exceeds random (51.0%); multi-
model reaches 66.9% because the four generators provide both diverse error patterns for contrastive


                                                                     22
                         GSM8K            100
                                                         MuSR                             TravelPlanner                       TACO                               K&K
                                                                             40       EBM                       100                                100
                                                                                      Random
             98                           90                                          Oracle
                                                                                                                                                   90


pass@1 (%)
                                                                             30                                 80
             96                  EBM      80                        EBM                                                                   EBM                          EBM
                                 Random                             Random                                                                Random   80                  Random
                                 Oracle   70                        Oracle
                                                                             20                                 60                        Oracle                       Oracle
             94                                                                                                                                    70
                                          60                                                                    40
                                                                             10                                                                    60
             92                           50
                  4      8           16         4   8    16             32        4   8        16          32         4   8   16              32         4   8             32
                             N                                N                                     N                              N                               N
Figure 7: Candidate pool scaling. The Distributional EBM’s advantage over random grows with N on GSM8K;
on MuSR the advantage peaks at N =8 and diminishes as the pool saturates.


Table 11: Candidate pool size (N ) ablation (ModernBERT, multi-model). Bold marks the best EBM result per
dataset. TACO values are pre-DFR; after deconfounding the N =32 result is 88.6%.
                                                        GSM8K                                  MuSR                           TACO
                                 N          EBM               Random              EBM                   Random            EBM           Random
                                 4         95.8%                  91.8%           62.9%                 51.7%             75.0%          34.1%
                                 8         96.3%                  92.3%           69.5%                 55.0%             85.2%          36.4%
                                 16        96.9%                  92.4%           68.2%                 68.2%             90.9%          31.8%
                                 32        97.0%                  92.7%           65.6%                 58.9%             92.0%          47.7%


Table 12: Single-model vs. multi-model comparison (ModernBERT, K=5). Single-model uses Qwen-2.5-7B
only (N =16). Multi-model uses N =16 (4 models × 4 candidates); the main results (Tab. 1) use N =32,
explaining small differences (e.g., MuSR 66.9% here vs. 67.7%). Bold marks the better result per column.
                                                          GSM8K                   MuSR                  TravelPlanner                  TACO                  K&K
                        Single-model EBM                      93.1%               53.6%                     8.0%                       36.4%             40.1%
                        Multi-model EBM                       97.0%               66.9%                    28.0%                       88.6%             99.9%
                        ∆                                     +3.9 pp         +13.3 pp                    +20.0 pp                 +52.2 pp              +59.8 pp


learning and higher oracle coverage (98.0% vs. 86.8%). On GSM8K, the gain is smallest (+3.9 pp)
because all models are 91-97% correct (contamination), leaving little room for multi-model diversity
to help.

F.2                   Energy Separation and Calibration

Tab. 13 and Fig. 9 report diagnostic metrics for the Distributional EBM across all five benchmarks;
Fig. 8 visualises the correct and incorrect energy distributions.
K&K exhibits the largest energy gap (9.00) and highest Kendall τ (0.62), reflecting the clean binary
signal from the statement-consistency verifier and the high candidate diversity. TACO’s gap (2.49)
and τ (0.44) are reported after DFR deconfounding; the pre-DFR values (4.30, 0.78) were inflated by
the model-identity shortcut. MuSR has the smallest gap (0.19) and lowest τ (0.14), consistent with the
difficulty of discriminating correct from incorrect narrative reasoning where both candidates contain
plausible multi-hop inferences. TravelPlanner achieves the highest τ (0.49) despite a moderate gap
(2.00), because its continuous violation labels produce a smoother energy landscape than binary
correctness labels. σ-AUROC ranges from 0.44 (MuSR, anti-correlated) to 0.87 (K&K), confirming
that ensemble uncertainty is task-dependent: reliable on tasks with clear correct/incorrect boundaries,
unreliable on nuanced reasoning. ECE is moderate across all datasets (0.21-0.43), with MuSR the
best-calibrated (0.21) and GSM8K the worst (0.43).

F.3                   Per-Difficulty Analysis

This section breaks down results by task difficulty to reveal where the Distributional EBM excels and
where it struggles.

TACO (Tab. 14). The deconfounded EBM degrades gracefully with difficulty: 93.8% on EASY,
90.9% on MEDIUM, and 80.0% on HARD. It matches Sonnet 4.6 on MEDIUM and HARD problems,


                                                                                               23
                                                                                     0.8                            GSM8K correct
                                                                                                                    GSM8K incorrect
                                                                                                                    MuSR correct
                                                                                                                    MuSR incorrect
                                                                                     0.6                            TravelPlanner correct
                                                                                                                    TravelPlanner incorrect




                                                                       Density
                                                                                                                    TACO correct
                                                                                     0.4                            TACO incorrect
                                                                                                                    K&K correct
                                                                                                                    K&K incorrect
                                                                                     0.2

                                                                                     0.0
                                                                                            8                            6                             4                 2                  0                      2                      4                       6                    8
                                                                                                                                                                     Energy Equality
                                                                                                                                                                             k
  Figure 8: Energy distributions for correct (filled) and incorrect (dashed outline) candidates on GSM8K and
  MuSR (ModernBERT, multi-model). GSM8K shows clear bimodal separation; MuSR distributions overlap
  substantially, consistent with the smaller energy gap (0.19 vs. 1.76) and the difficulty of discriminating correct
  from incorrect narrative reasoning.

                                        GSM8K (ECE=0.43)                                                     MuSR (ECE=0.21)                                         TravelPlanner (ECE=0.38)                                           TACO (ECE=0.32)                                              K&K (ECE=0.32)
                      100                                                                              Mean                                                  100                                                   100                                                    Mean   100
                                                                                           80
Accuracy in bin (%)




                      80                                                                                                                                      80                                                       80                                                        80
                                                                                           60
                      60                                                                                                                                      60                                                       60                                                        60
                      40                                                                   40
                                                                                                                                                              40                                                       40                                                        40
                      20                                                                   20                                                                 20                                                       20                                                        20
                                   Mean                                                                                                                                                   Mean                                                                                                Mean
                        0                                                                   0                                                                 0                                                        0                                                          0
                             8

                                   2

                                          9

                                                4

                                                      9

                                                            5

                                                                  9

                                                                        6

                                                                              3

                                                                                    9




                                                                                                 3

                                                                                                       9

                                                                                                              2

                                                                                                                    5

                                                                                                                          9

                                                                                                                                2

                                                                                                                                      4

                                                                                                                                            7

                                                                                                                                                  2

                                                                                                                                                        2




                                                                                                                                                                    4



                                                                                                                                                                              3



                                                                                                                                                                                     9



                                                                                                                                                                                                  5



                                                                                                                                                                                                               0




                                                                                                                                                                                                                             4

                                                                                                                                                                                                                                   8

                                                                                                                                                                                                                                          8

                                                                                                                                                                                                                                                8

                                                                                                                                                                                                                                                      5

                                                                                                                                                                                                                                                            1

                                                                                                                                                                                                                                                                   8

                                                                                                                                                                                                                                                                          3




                                                                                                                                                                                                                                                                                        6

                                                                                                                                                                                                                                                                                              1

                                                                                                                                                                                                                                                                                                     9

                                                                                                                                                                                                                                                                                                           6

                                                                                                                                                                                                                                                                                                                 3

                                                                                                                                                                                                                                                                                                                       9

                                                                                                                                                                                                                                                                                                                             6

                                                                                                                                                                                                                                                                                                                                   3

                                                                                                                                                                                                                                                                                                                                         6

                                                                                                                                                                                                                                                                                                                                               3
                            0.3

                                  0.5

                                         0.5

                                               0.6

                                                     0.6

                                                           0.7

                                                                 0.7

                                                                       0.8

                                                                             0.9

                                                                                   1.0




                                                                                                0.1

                                                                                                      0.1

                                                                                                             0.2

                                                                                                                   0.2

                                                                                                                         0.2

                                                                                                                               0.3

                                                                                                                                     0.3

                                                                                                                                           0.3

                                                                                                                                                 0.4

                                                                                                                                                       0.5




                                                                                                                                                                   0.4



                                                                                                                                                                             0.5



                                                                                                                                                                                    0.5



                                                                                                                                                                                                 0.6



                                                                                                                                                                                                           0.8




                                                                                                                                                                                                                            0.7

                                                                                                                                                                                                                                  0.9

                                                                                                                                                                                                                                         1.0

                                                                                                                                                                                                                                               1.1

                                                                                                                                                                                                                                                     1.2

                                                                                                                                                                                                                                                           1.4

                                                                                                                                                                                                                                                                  1.5

                                                                                                                                                                                                                                                                         1.9




                                                                                                                                                                                                                                                                                       0.7

                                                                                                                                                                                                                                                                                             0.9

                                                                                                                                                                                                                                                                                                    0.9

                                                                                                                                                                                                                                                                                                          1.0

                                                                                                                                                                                                                                                                                                                1.1

                                                                                                                                                                                                                                                                                                                      1.1

                                                                                                                                                                                                                                                                                                                            1.2

                                                                                                                                                                                                                                                                                                                                  1.3

                                                                                                                                                                                                                                                                                                                                        1.4

                                                                                                                                                                                                                                                                                                                                              1.7
                                        quality bin (low                high)                               quality bin (low                high)                        quality bin (low              high)                       quality bin (low              high)                             quality bin (low                high)

  Figure 9: Calibration reliability diagrams. Bars show accuracy within each σquality bin. On GSM8K, accuracy
  is uniformly high across all bins (ECE = 0.43, the scorer is poorly calibrated). On MuSR, accuracy fluctuates
  non-monotonically with σquality , confirming that the uncertainty signal is not reliably informative on this task.


 Table 13: Energy separation metrics (ModernBERT, multi-model, K=5). Energy gap = Ē(incorrect) −
 Ē(correct); positive means the scorer correctly assigns lower energy to correct candidates. Bold marks the best
 value per metric (higher is better for gap, τ , AUROC; lower for ECE).
                                                                       Metric                                              GSM8K                               MuSR                       TravelPlanner                                        TACO                            K&K
                                                                       Ē(correct)                                             −1.71                           −0.32                                    −1.26                                  −2.44                           −4.47
                                                                       Ē(incorrect)                                            0.04                           −0.12                                    0.74                                   0.04                             4.52
                                                                       Energy gap                                               1.76                            0.19                                    2.00                                   2.49                            9.00
                                                                       Kendall τ                                                0.27                           0.14                                     0.49                                   0.44                             0.62
                                                                       σ-AUROC                                                  0.54                           0.44                                     0.62                                    0.51                            0.87
                                                                       ECE                                                      0.43                            0.21                                    0.28                                   0.32                            0.32


and substantially outperforms Qwen-72B at every difficulty level (by 16-60 pp). Opus 4.6 achieves
100% across all tiers, reflecting the advantage of a much larger model on competitive programming.

 Table 14: TACO pass@1 by difficulty (multi-model). The EBM matches or exceeds Sonnet 4.6 on MEDIUM
 problems. n = number of test problems.
                                                                 Difficulty                                                                  EBM                   Opus 4.6                               Sonnet 4.6                             Qwen-72B                                    n
                                                                 EASY                                                                      93.8%                     100.0%                                    100.0%                                      77.1%                             48
                                                                 MEDIUM                                                                    90.9%                     100.0%                                     90.9%                                      45.5%                             11
                                                                 MEDIUM_HARD                                                               81.8%                     100.0%                                     90.9%                                      27.3%                             11
                                                                 HARD                                                                      80.0%                     100.0%                                     80.0%                                      20.0%                              5


  Knights and Knaves (Tab. 15). The multi-model EBM achieves 100% pass@1 on all tiers except
  8-character puzzles (99.0%), demonstrating that the scorer maintains near-perfect discrimination even


                                                                                                                                                                                   24
as combinatorial complexity grows exponentially. Gains over greedy scale with difficulty: +32 pp on
2ppl to +55 pp on 7ppl. The single-model EBM (Qwen-only) shows a different pattern: gains are
largest on the hardest tiers (+23.1 pp on 8ppl, +14.5 pp on 6ppl), suggesting that the scorer adds the
most value precisely where the generator is weakest. Qwen-72B degrades steeply from 75% (2ppl) to
10% (8ppl), falling below random (58.7%) from 5ppl onward.

Table 15: K&K pass@1 by puzzle size (number of characters). Multi-model EBM achieves 100% on all tiers
except 8ppl. Bold marks the best result per tier. Single-model EBM gains are largest on the hardest tiers.
                   Multi-model (N =32)               Single-model (N =16)             Frontier
        Tier   Greedy     EBM        Lift     Greedy     EBM        Lift     Qwen-72B    Random
        2ppl   68.0%    100.0%     +32.0 pp    58.7%     58.7%    +0.0 pp     75.0%          58.7%
        3ppl   56.0%    100.0%     +44.0 pp    45.7%     48.9%    +3.2 pp     63.0%          58.7%
        4ppl   60.0%    100.0%     +40.0 pp    25.8%     38.7%    +12.9 pp    48.0%          58.7%
        5ppl   59.0%    100.0%     +41.0 pp    28.2%     29.5%    +1.3 pp     32.0%          58.7%
        6ppl   55.0%    100.0%     +45.0 pp    17.7%     32.3%    +14.5 pp    29.0%          58.7%
        7ppl   45.0%    100.0%     +55.0 pp    14.6%     19.5%    +4.9 pp     16.0%          58.7%
        8ppl   52.0%    99.0%      +47.0 pp    10.3%     33.3%    +23.1 pp    10.0%          58.7%


MuSR (Tab. 16). MuSR’s three subsets differ in structure: murder mysteries are 2-choice (50%
random baseline), while object placements and team allocation are 3-choice (33% random). Average
candidate accuracy is highest on murder mysteries (62.2%) and lowest on object placements (52.1%),
reflecting the difficulty of spatial reasoning relative to narrative deduction. The EBM’s gains are
largest on the 3-choice subsets where the random baseline is lower and there is more room for
discrimination.

Table 16: MuSR per-subset accuracy (multi-model). Murder mysteries are 2-choice (50% random); objects and
team are 3-choice (33% random).
           Subset                Avg. candidate accuracy         Random baseline    n choices
           Murder mysteries                 62.2%                     50%                2
           Object placements                52.1%                     33%                3
           Team allocation                  57.2%                     33%                3


F.4   Selective Prediction via σ-Abstention

Tab. 17 reports pass@1 on the retained set after abstaining on the X% of problems with highest σquality .
On K&K, selective prediction reaches 100% by 20% abstention, reflecting the strong σ-AUROC
(0.87): the ensemble reliably identifies the single wrong prediction. On TravelPlanner, abstaining
on 40% of problems raises pass@1 from 28.0% to 36.7% (+8.7 pp), confirming that σquality captures
meaningful quality uncertainty on continuous-label tasks. On GSM8K, selective prediction is flat
(97.0-97.4%) because the model is already near-ceiling: there are only ∼40 wrong predictions out of
1,319. On MuSR, accuracy decreases with abstention (66.9%→61.9% at 30%), consistent with the
anti-correlated σ-AUROC (0.44): the ensemble is more confident on wrong predictions than right
ones, so abstaining on high-σquality problems removes easy ones. On TACO (after DFR), selective
prediction provides only +2.3 pp at 50% abstention (88.6%→90.9%), down from +5.3 pp pre-DFR,
because the pre-DFR σ was capturing model-identity uncertainty rather than quality uncertainty.

F.5   Two-Pass σ-Triage Analysis

Algorithm 1 provides the full inference pseudocode for the two-pass σ-triage mechanism described
in Sec. 3.5.
Tab. 18 reports two-pass σ-triage results across all datasets and pool configurations. The mechanism
helps when three conditions hold: (a) pass-1 has headroom (not already near-ceiling), (b) the feedback
is structured enough to guide regeneration, and (c) the generator can act on it. TravelPlanner single-
model satisfies all three: constraint violations (budget overruns, missing meals, invalid routes)
provide concrete feedback, yielding +6.0 pp. TACO multi-model (confounded) fails catastrophically


                                                    25
Table 17: Selective prediction: pass@1 on retained problems after abstaining on the most uncertain (highest
σquality ) fraction. Bold marks where a dataset reaches 100% accuracy. TACO values are post-DFR; selective
prediction is weak (+2.3 pp at 50% abstention) because the deconfounded σ no longer captures model-identity
uncertainty. MuSR pass@1 fluctuates non-monotonically with abstention (61.9–66.9%); the anti-correlated
σ-AUROC (0.44) means high-σ problems are not preferentially incorrect, so abstention does not concentrate on
the wrong predictions.
          Abstain %      GSM8K (MB)          MuSR (MB)        TravelPlanner      TACO        K&K
          0%                 97.0%              66.9%             28.0%          88.6%       99.9%
          10%                97.4%              66.7%             28.9%          88.6%       99.8%
          20%                97.3%              65.0%             30.0%          88.6%      100.0%
          30%                97.2%              61.9%             31.4%          88.5%      100.0%
          40%                97.2%              64.4%             36.7%          90.4%      100.0%
          50%                97.1%              66.7%             36.0%          90.9%      100.0%


Algorithm 1 Inference with σ-triage
Require: Problem x, frozen LLMs {G1 , . . . , GM }, ensemble {fk }K          k=1 , constraint set {Cj }, thresh-
    olds θσ , θabstain , weight λ
Ensure: Selected candidate y ∗ or A BSTAIN
 1: Pass 1: Generate. For each LLM Gm , sample Nm candidates via temperature sampling. Pool:
    Y1 = {y1 , . . . , yN1 }.
 2: for each yi ∈ Y1 do
 3:    Parse yi . If parse fails, set Econstraint (x, yi ) = +∞.
 4:    Score with all K adapters: {E 1 (x, yi ), . . . , E K (x, yi )}.
                                        k
 5:    µquality (x, yi ) ← mean({E
                               P          }), σquality (x, yi ) ← std({E k }).
 6:    Econstraint (x, yi ) ← j wj · Cj (x, yi ).
 7:    E(x, yi ) ← µquality (x, yi ) + λ · Econstraint (x, yi ).
 8: end for
 9: y ∗ ← arg minyi E(x, yi ).
10: if Econstraint (x, y ∗ ) > 0 or σquality > θσ then
11:    Pass 2: Regenerate. Format constraint violations of y ∗ as feedback.
12:    Generate N2 candidates conditioned on feedback: Y2 .
13:    Score all yi ∈ Y2 (repeat lines 3-7). Pool: Y = Y1 ∪ Y2 .
14:    y ∗ ← arg minyi ∈Y E(x, yi ).
15: end if
16: if σquality (x, y ∗ ) > θabstain then
17:    return A BSTAIN
18: else
19:    return y ∗
20: end if



(−89.8 pp) because all 88 problems are triaged and pass-2 candidates disrupt the Gemma-centric
energy landscape. After DFR deconfounding, TACO two-pass is neutral (88.6%→88.6%) because
the deconfounded scorer evaluates each candidate on quality alone, so re-pooling low-quality pass-2
candidates does not corrupt the ranking. GSM8K two-pass reduces pass@1 by 1.7 pp because
doubt-inducing feedback causes the contaminated generator to second-guess its (memorised) correct
answers.
Two-pass helps when pass-1 has headroom, feedback is structured (e.g., specific constraint violations),
and the generator can act on it. TravelPlanner single-model satisfies all three conditions. On K&K
single-model (θσ =0.5), two-pass is near-neutral (−0.2 pp overall) but shows a tier-dependent pattern:
it helps on easy puzzles (2-4ppl: +2 to +4 pp) where constraint feedback gives actionable corrections,
but hurts on hard puzzles (7-8ppl: −10 to −13 pp) where pass-2 candidates look confident to the
ensemble but are more often wrong. On K&K multi-model, all 700 problems trigger triage (mean
σquality =0.931) due to high inter-model disagreement, but only 1 problem has a constraint violation
receiving actionable pass-2 feedback; the remaining 699 already satisfy all constraints, so two-pass
has zero effect (99.9%→99.9%). TACO multi-model fails catastrophically because: (a) all 88


                                                      26
Table 18: Two-pass σ-triage results across datasets. θσ =0.8 unless noted, N2 =8 pass-2 candidates from
Qwen-2.5-7B with constraint/error feedback. Bold marks the only configuration where two-pass improves
pass@1. “–” = not applicable (no problems triaged or no pass-2 candidates adopted).
Dataset            Pool                  Triage rate       Pass-1 Two-pass          ∆    Pass-2 adopted
GSM8K               Single (MB v1)          201/1319 (15%)      93.1%       91.4%      −1.7 pp         56/201
MuSR                Multi                      0/151 (0%)       67.7%       67.7%       0.0 pp            –
TravelPlanner       Single                    18/50 (36%)       74.0%       80.0%      +6.0 pp          9/18
TravelPlanner       Multi                     17/50 (34%)       92.0%       92.0%       0.0 pp          1/17
TACO (pre-DFR)      Multi                    88/88 (100%)       92.0%        2.3%      −89.8 pp         0/88
TACO (DFR)          Multi                    84/88 (95.5%)      88.6%       88.6%       0.0 pp            –
TACO                Single                      0/88 (0%)       36.4%       36.4%       0.0 pp            –
K&K                 Single (θσ =0.5)        396/499 (79.4%)     85.2%       85.0%      −0.2 pp         29/396
K&K                 Multi (θσ =0.5)         700/700 (100%)      99.9%       99.9%       0.0 pp         0/700


problems trigger triage (σpool > 0.8 due to high inter-model disagreement), (b) pass-2 candidates
from Qwen-7B with opaque error feedback are uniformly poor, and (c) re-pooling these low-quality
candidates disrupts the energy landscape established by the strong pass-1 pool.

When does σ-triage help? Two patterns are visible. (a) Constraint-checkability. σ-triage adds
value where regeneration receives actionable feedback: TravelPlanner’s per-constraint violation
messages (budget over by $X, missing meal on day 2) translate directly into pass-2 prompts (+6.0 pp);
TACO’s opaque wrong_answer and doubt-inducing feedback on contaminated GSM8K do not. (b)
Quality-distribution multimodality. Triage benefits tasks where candidates cluster into discrete modes
the ensemble can disagree about (K&K’s statement-consistency states); on tasks where candidates lie
on a continuous quality manifold (MuSR’s narrative inferences), σ measures presentation variation
rather than correctness. σ-triage therefore selects which regime each task falls into rather than
applying a one-size-fits-all loop.

F.6   TravelPlanner: Per-Constraint Frontier Comparison

Tab. 19 decomposes the TravelPlanner violation score by constraint dimension, revealing where the
Distributional EBM and frontier models have complementary strengths. Frontier models (Opus,
Sonnet, Qwen-72B) systematically fail on connectivity (24-28% satisfaction) because they hallucinate
transport routes not in the reference database. The analytical constraint checker verifies routes against
the database directly, giving the EBM+Econstraint system near-perfect connectivity (86% satisfaction).
Conversely, frontier models outperform on budget (Opus: 0.040 vs. EBM+Econstraint : 0.030), reflecting
stronger numerical reasoning. Preferences are the hardest dimension for all methods, including oracle
(0.180 mean violation).

Table 19: Per-violation-dimension mean scores on TravelPlanner (50 test problems). Lower is better. Bold
marks the best (lowest) value per row.
Dimension       Oracle   Econstraint only   EBM+Econstraint   EBM     Opus 4.6   Sonnet 4.6   Qwen-72B   Random
Budget          0.018        0.012              0.030         0.176     0.040       0.078      0.062      0.238
Completeness    0.009        0.011              0.031         0.003     0.086       0.048      0.110      0.260
Hallucination   0.005        0.011              0.011         0.002     0.015       0.037      0.070      0.119
Connectivity    0.000        0.003              0.058         0.062     0.418       0.393      0.375      0.232
Preferences     0.180        0.187              0.213         0.220     0.213       0.213      0.280      0.387
Diversity       0.011        0.080              0.022         0.000     0.007       0.054      0.074      0.148


Frontier models systematically fail on connectivity (24-28% satisfaction) because they hallucinate
transport routes not present in the reference database. The analytical constraint checker verifies
routes against the database directly, giving the EBM+Econstraint system a structural advantage on this
dimension. Conversely, frontier models outperform on budget (Opus 4.6: 0.040 vs. EBM+Econstraint :
0.030), reflecting their stronger numerical reasoning. Preferences are the hardest dimension for all
methods, including oracle (0.180 mean violation even for the best candidate).

Independent LLM-judge validation. To check that the violation score reflects genuine plan
quality rather than artefacts of the constraint checker, two independent LLM judges (Opus 4.6


                                                         27
Table 20: Full zero-shot transfer matrix (EBM pass@1, ModernBERT multi-model unless noted). Shaded cells
mark in-domain (diagonal) entries. Bold highlights notable transfer results. Baselines for reference: self-
consistency (SC) and random.
          Source → Target                     GSM8K           MuSR           MATH-500          TP        TACO                         K&K
          GSM8K (MB)                           97.0%          64.9%              65.6%         0.0%      39.8%                    92.4%
          GSM8K (DB)                           97.1%          63.6%              62.7%         0.0%      45.5%                    68.4%
          MuSR (MB)                            93.9%          67.7%              67.6%         0.0%      36.4%                    89.0%
          MuSR (DB)                            96.1%          62.9%              67.8%         0.0%      39.8%                    88.4%
          TP (MB)                              93.1%          60.9%              67.2%        30.0%      56.4%                    33.5%
          TACO (MB)                            92.5%          58.9%              67.4%        43.3%      88.6%                    31.1%
          K&K (MB)                             94.9%          64.9%               0.0%        0.136⋄     51.1%                    99.9%
          Self-consistency                      96.1%         64.4%              72.6%        12.0%      36.4%                     56.4%
          Random                                91.7%         53.0%              68.4%        14.0%      46.6%                     58.7%


and Sonnet 4.6 [Anthropic, 2026], T =0) score 120 candidates on a 1–5 scale using the original
TravelPlanner criteria [Xie et al., 2024b]. The judges agree strongly with each other (Spearman
ρ=0.67, p < 10−16 ) and both correlate negatively with the violation score (Opus: ρ=−0.46; Sonnet:
ρ=−0.38; both p < 10−5 ). Opus 4.6 rates EBM-selected plans higher than oracle plans on average
(3.86 vs. 3.67), suggesting the learned scorer captures holistic coherence beyond what constraints
alone measure.

F.7   Zero-Shot Transfer: Full Matrix

Tab. 20 reports the full zero-shot transfer matrix, including both ModernBERT and DeBERTa
checkpoints and the MATH-500 benchmark. Fig. 10 visualises the transfer asymmetry as lift over
random.


                                   GSM8K     97.0        64.9            0.0         39.8        92.4       20
                                            (+5.3)      (+11.9)        (-14.0)      (-6.8)     (+33.7)
                                                                                                            15      Lift over random (pp)
                                    MuSR     93.9         67.7           0.0          36.4       89.0       10
               Source checkpoint




                                            (+2.2)      (+14.7)        (-14.0)      (-10.2)    (+30.3)
                                                                                                            5
                                             93.1        60.9           30.0         56.4        33.5
                                      TP    (+1.4)      (+7.9)        (+16.0)       (+9.8)     (-25.2)      0
                                                                                                                5
                                             92.5        58.9           43.3          88.6       31.1
                                    TACO    (+0.8)      (+5.9)        (+29.3)       (+42.0)    (-27.6)          10
                                                                                                                15
                                             94.9        64.9            0.1         51.1        99.9
                                    K&K     (+3.2)      (+11.9)        (-13.9)      (+4.5)     (+41.2)          20
                                           GSM8K        MuSR            TP         TACO        K&K
                                                                  Target dataset
Figure 10: Zero-shot transfer heatmap (ModernBERT): each cell shows pass@1 and (lift over random). Colour
encodes lift: green = positive transfer, red = negative. Black borders mark in-domain entries.


Four patterns are evident. First, hard-to-easy reasoning transfer works: both GSM8K and MuSR
checkpoints achieve 89-92% on K&K, and the MuSR-trained DeBERTa achieves 96.1% on GSM8K,
matching in-domain self-consistency. Second, easy-to-hard reasoning transfer is weak: the GSM8K
checkpoint reaches only 64.9% on MuSR (vs. 67.7% in-domain), because the contaminated training
data provides too few informative negatives. Third, reasoning-to-code transfer is negative: both
GSM8K (39.8%) and MuSR (36.4%) checkpoints score below random (46.6%) on TACO, indicating
that reasoning-quality signals actively mislead on code. Fourth, no checkpoint transfers to MATH-500:
all achieve ≤68% vs. self-consistency at 72.6%, likely due to the format mismatch (\boxed{} vs.
####).


                                                                          28
Key observations: (i) MuSR→GSM8K transfer (96.1% with DeBERTa) matches in-domain self-
consistency, confirming that hard-data training produces transferable quality signals. (ii) No check-
point transfers positively to MATH-500 (all ≤ 67.8%, below SC at 72.6%), likely due to format
mismatch (\boxed{} vs. ####). (iii) Reasoning→code transfer is negative: GSM8K (39.8%) and
MuSR (36.4%) both score below TACO random (46.6%), indicating that reasoning-quality signals
actively mislead on code. (iv) TACO→TravelPlanner shows strong positive transfer (43.3% vs. 14.0%
random, +29.3 pp), and TravelPlanner→TACO also transfers positively (56.4% vs. 46.6% random,
+9.8 pp), suggesting that execution-based labels produce more generalisable quality signals than
reasoning-based labels. (v) DeBERTa backbone transfer to K&K is asymmetric: MuSR(DB)→K&K
retains 88.4% (−0.6 pp vs. ModernBERT), while GSM8K(DB)→K&K drops to 68.4% (−24.0 pp).
The MuSR-trained scorer learns quality signals robust to 512-token truncation, whereas the GSM8K
scorer, trained on contaminated data with 95% candidate accuracy, relies on shallow features that are
lost when inputs are truncated.

Cross-pool transfer (Qwen-train → multi-test). A separate transfer axis tests whether the verifier
generalises across generator distributions: we take the Qwen-only-trained scorer (the same checkpoint
used in the single-model row of Tab. 12) and evaluate it on the multi-model candidate test pool used
for the headline results. Tab. 21 reports the result. On MuSR, the cross-pool scorer reaches 69.5%
pass@1 (151 problems), matching the multi-trained scorer (67.7%) and exceeding the single-model
in-domain configuration (53.6%) by +15.9 pp; the Qwen-only training distribution still produces a
ranker that handles candidates from LLaMA, Gemma, and GPT-OSS without seeing them during
training. On GSM8K, the cross-pool scorer reaches 90.5% pass@1 (1,319 problems), below the
multi-trained 97.0% and even below pool-random (92.7%); GSM8K’s near-saturated candidate
accuracy (95%) leaves few informative negatives during Qwen-only training, so the scorer learns
shallow signals that misrank the multi-model pool. This mirrors pattern (iv): contaminated training
data produces non-transferable signals.

Table 21: Cross-pool transfer: Qwen-only-trained EBM evaluated on the multi-model candidate test pool.
Single-train, single-test repeats the entries from the corresponding row of Tab. 12 for context. All numbers are
pass@1 with N =32 candidates per problem; multi-test pool is the same as the headline evaluation.
                          Configuration                             MuSR     GSM8K
                          Single-train, single-test (Qwen-only)    53.6%      93.1%
                          Single-train, multi-test (cross-pool)    69.5%      90.5%
                          Multi-train, multi-test (in-domain)      67.7%      97.0%



F.8   Confounding Analysis

We screen all five datasets for model-identity confounding by computing two diagnostics: (i) per-
model pick distribution (does the scorer disproportionately select one generator?) and (ii) cross-model
correct energy spread (do correct candidates from different generators receive similar energies?).
Tab. 22 summarises the results.

Table 22: Confounding screening across all datasets. Pick distribution shows the fraction of test problems where
each generator’s candidate is selected. Energy spread is the standard deviation of mean correct energy across
generators (lower = less confounded).
      Dataset            Qwen-2.5-7B      LLaMA-3.1-8B     Gemma-4-26B      GPT-OSS-20B     Energy spread
      GSM8K                   26%             24%                 25%            25%             0.04
      MuSR                    36%             23%                 18%            23%             0.18
      TravelPlanner           22%             28%                 26%            24%             0.24
      K&K                     28%             28%                 27%            18%             0.11
      TACO (pre-DFR)           1%              1%                 94%             4%             6.67
      TACO (post-DFR)         22%             24%                 34%            20%             0.34


Four datasets show near-uniform pick distributions and energy spreads below 0.25, indicating no
model-identity confounding. On MuSR, the scorer picks the weaker model (Qwen, 51% accuracy)
most often (36%), the opposite of what fingerprinting would produce. On K&K, despite the most


                                                      29
extreme accuracy split in our study (Gemma/GPT-OSS at 99% vs. Qwen/LLaMA at 15%), picks
remain uniform and the energy spread is just 0.11.
TACO is the sole outlier: the initial scorer selected Gemma on 94% of test problems with an energy
spread of 6.67, indicating severe model-identity confounding. The six-phase analysis below details
how this was detected, diagnosed, and mitigated.

TACO: detailed analysis. A six-phase confounding analysis on the TACO multi-model scorer
revealed that the initial model exploited a model-identity shortcut rather than genuine reasoning-
quality discrimination.

Phase 1-2: Detection. The scorer selected a Gemma-4-26B candidate on 83/88 test problems
(94.3%). A naive “always pick random Gemma” baseline achieved 89.8% pass@1, leaving only
+1.1 pp of genuine quality signal. Correct solutions from different models received dramatically
different energies: Gemma correct at −4.47 vs. LLaMA correct at +2.20, a 6.67-point gap for
identical correctness labels.

Phase 3: Style normalisation ablation. Progressive removal of formatting features (headers,
LaTeX, IO normalisation, comments) collapsed both the cross-model energy gap (6.67 → ∼1.0) and
the within Gemma correct/incorrect gap (2.41 → 0.55), confirming that quality and identity features
are carried by the same tokens.

Phase 4: Causal style-swap test. For 40 problems with correct Gemma solutions, three other
models rewrote each solution in their own style with variable names, algorithm, and logic locked.
Execution-verified identical code received +1.95 higher energy on average when presented in another
model’s formatting (LLaMA: +2.66, GPT-OSS: +2.20, Qwen: +0.97). This is causal proof of style
bias [Geirhos et al., 2020b].

Phase 5-6: Decomposition and case studies. Code-only scoring retained most of the model-
identity gap (3.6-point spread), while explanation-only scoring collapsed to 62.5% pass@1. The
identity signal lives primarily in code patterns (IO methods, function structure), not explanation text.
All 5 non-Gemma picks by the original scorer occurred on EASY problems; on 7 problems the scorer
picked an incorrect Gemma solution despite correct alternatives being available.

Mitigation: DFR. Last-layer retraining (DFR; Kirichenko et al., 2023) on group-balanced data (4
models × 2 labels, capped at 396 per cell) retrains only the K=5 energy heads (0.4% of parameters)
while freezing the backbone and LoRA adapters. This collapses the cross-model correct energy
spread from 6.67 to 0.34 (95% reduction) while retaining 88.6% pass@1 with picks distributed
uniformly across generators (22/24/34/20%). The deconfounded scorer improves pass@1 on HARD
(+13.3 pp) and UNKNOWN (+14.4 pp) problems and is robust to two-pass re-pooling (88.6% →
88.6%, vs. pre-DFR catastrophic collapse 92.0% → 2.3%).

G     Broader Impact
This paper presents work whose goal is to advance machine learning, specifically the verification of
structured outputs from large language models. We outline expected positive and negative societal
impacts.

Positive impacts. Uncertainty-aware verification of structured LLM outputs has beneficial appli-
cations in safety-critical domains where undetected errors propagate silently: automated planning
(travel itineraries, logistics, scheduling) where a single budget or routing violation invalidates the
entire plan; code generation where edge-case failures can cause silent data corruption or service
outages; multi-step mathematical and scientific reasoning where intermediate errors compound; and
decision support in regulated settings (legal, medical, financial) where outputs must satisfy domain
rules verifiable in closed form. The decomposition E = µquality + λ · Econstraint is auditable by design:
Econstraint is a deterministic checker of explicit task constraints, and the distributional (µquality , σquality )
exposes when the verifier itself is uncertain, enabling principled abstention rather than confidently
wrong outputs. Compared to scaling generators, a small specialised verifier on a fixed candidate


                                                       30
pool is also more energy-efficient and democratises access to reliable structured reasoning without
100B+-parameter inference.

Negative impacts and risks. Overreliance on automated verification carries three risks. (i) Spurious
shortcuts. Our confounding analysis (Sec. 4.2, Sec. F.8) demonstrates that scorers can learn high-
confidence but content-irrelevant signals (the TACO formatting shortcut), producing reliable-looking
but unreliable outputs. Without the kind of cross-dataset auditing we report, such shortcuts go
undetected. (ii) Distribution shift. A scorer trained on one candidate distribution may degrade silently
when deployed against differently-styled generations or out-of-domain inputs (illustrated by the
GSM8K→MATH-500 below-random transfer; see Tab. 20). (iii) Automation bias. Plans, code, or
proofs that pass an automated checker may be accepted with less human review than warranted,
particularly when σquality is uncalibrated (e.g., MuSR σ-AUROC = 0.44; see Limitations in Sec. 4.2).

Mitigations. We recommend: (a) running confounding diagnostics (cross-model pick distributions
and energy spreads) at deployment time, with last-layer retraining (DFR; Kirichenko et al., 2023)
when shortcuts surface; (b) treating σquality as a regime-aware signal rather than a universal abstention
threshold (Sec. 4.2 shows it is task-dependent); (c) preserving human review for high-stakes deploy-
ments and using σ-triage to route uncertain cases to humans rather than auto-accepting them; (d)
documenting candidate-pool composition and constraint definitions when releasing checkpoints, since
both interact materially with verifier behaviour. The released artefact in this work is a verifier/reranker
(not a generative model), which substantially limits direct misuse risk relative to released LLMs.

Scaling Econstraint . The decomposition E = µquality + λ · Econstraint requires a domain expert to
author each constraint term, which is the principal scalability bottleneck of the framework. Three
directions seem viable. (a) LLM-generated specifications: a frontier model can be prompted to
extract executable constraints from a natural-language task specification, with the EBM then ranking
candidates against the auto-generated checker; the verifier inherits the spec-extractor’s errors, but
an exact deterministic constraint can be cheaper to author than to learn. (b) Learned constraint
heads: a small model trained on labelled violation data can approximate Econstraint for domains where
authoring is hard but labelled examples exist (CI logs for code, structured grading rubrics for student
work, regulatory checklists in compliance settings). (c) Constraint DSLs: domain-specific languages
for stating constraints, analogous to integrity constraints in relational databases, lower the authoring
burden without removing the human in the loop. We treat these as engineering frontiers rather than
methodological gaps; the propositions of Sec. 3.2 hold regardless of how Econstraint is obtained, as
long as it is deterministic at inference time.




                                                   31
