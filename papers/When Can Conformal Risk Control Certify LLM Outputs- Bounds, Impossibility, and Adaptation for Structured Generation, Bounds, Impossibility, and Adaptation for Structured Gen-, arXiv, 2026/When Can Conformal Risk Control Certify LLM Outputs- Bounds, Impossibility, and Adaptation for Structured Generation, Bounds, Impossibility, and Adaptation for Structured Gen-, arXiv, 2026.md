                                        When Can Conformal Risk Control Certify LLM Outputs?
                                        Bounds, Impossibility, and Adaptation for Structured Gen-
                                        eration

                                        Varun Kotte
                                        Independent Researcher
                                        kottevarun@gmail.com
arXiv:2606.29054v2 [cs.LG] 7 Sep 2026




                                                                                           Abstract

                                                Large language models (LLMs) deployed for structured generation (NER, JSON extraction,
                                                QA, classification) lack formal reliability guarantees, and heuristic abstention policies violate
                                                user-specified risk targets on 7.5–12.5% of settings, with no per-deployment guarantee. We
                                                characterize when conformal risk control (CRC), which tunes an abstention threshold to
                                                certify a target risk, can certify structured LLM outputs and when it provably cannot: a
                                                synthesis of known distribution-free tools with new sharpenings and a constructive dual, not
                                                a new conformal primitive. First, a sharpened, attained feasibility frontier: when base risk
                                                µ exceeds target α, any distribution-free method must abstain on at least (µ − α)/(M − α)
                                                of inputs, M = ess sup R (on our F1 /exact-match losses M =1, matching the standard floor;
                                                strictly tighter only when an audited M < 1 holds), and achievable abstention decomposes
                                                into this floor plus a dispersion gap plus a score-ordering gap. Second, a proven certification
                                                phase diagram over 716 configurations (six open-weight models 3B–72B, eight datasets, six
                                                scores): at strict targets (α ≤ 0.20) the certified sets are nested (51/72/80 certified; Bernstein
                                                the largest upgrade over Hoeffding, +41%; e-CRC best under scarcity), while at relaxed
                                                targets the Hoeffding–Bernstein ordering reverses at a closed-form frontier α∗ (n, δ), with
                                                minimal sufficient set {Hoeffding, e-CRC}. Third, a negative shift result with a constructive
                                                dual: under cross-dataset shift (µ > α) the target is violated on 14/16 transfers by static
                                                CRC and every tested ACI step size, yet a full-feedback anytime-valid monitor certifies 0/16
                                                while remaining non-vacuous. The result is a three-step deployment recipe: check feasibility,
                                                select bound and score, then re-check under shift.


                                        1   Introduction

                                        When an LLM extracts the wrong medication from a clinical note, misses a liability clause in a contract, or
                                        pulls the wrong account number from a financial filing, the error is silent: the model reports full confidence
                                        and nothing downstream flags it. LLMs are increasingly deployed for such structured generation (extracting
                                        named entities, parsing JSON, answering factual questions, classifying inputs), where the output must match
                                        a schema and can be scored against ground truth, yet they give no guarantee on output quality.
                                        Standard uncertainty quantification (token probabilities, entropy thresholds, temperature scaling) is miscal-
                                        ibrated for structured outputs where the loss is defined at the level of entities, fields, or semantic units (Guo
                                        et al., 2017; Kadavath et al., 2022; Kuhn et al., 2023; Farquhar et al., 2024). Heuristic abstention policies
                                        violate user-specified risk targets on 7.5–12.5% of settings, with no guarantee for any individual deployment
                                        (Appendix Table H.4). Concretely: to guarantee ≤ 10% entity-level error, if the model’s base risk µ on the
                                        deployment population exceeds 10%, no post-hoc method can hit the target without heavy abstention. A
                                        heuristic never sees this floor; our impossibility result computes it in closed form.
                                        We ask a prior question, before “which bound is tightest?”: when can conformal risk control (CRC) (An-
                                        gelopoulos et al., 2024; Bates et al., 2021) certify structured LLM outputs at all, and when is it provably


                                                                                                1
impossible? The algebra behind our floor is elementary; the contribution is recognizing it as a deployment-
facing, tight feasibility frontier: when µ > α, no distribution-free method certifies without abstaining on
≥ (µ − α)/(M − α) of examples, so the first question is “is µ < α?”. We then establish a certification hierar-
chy (Hoeffding ⊆ Bernstein ⊆ e-CRC; finite-sample under a variance condition, asymptotic for the second)
with a closed-form reversal frontier and a Pareto-necessity result at relaxed targets, and evaluate ACI (Gibbs
& Candès, 2021) under cross-dataset transfer alongside a constructive anytime-valid counterpart. Concurrent
CRC-style work for LLMs asks which conformal procedure to apply (Quach et al., 2024; Mohri & Hashimoto,
2024; Abbasi-Yadkori et al., 2024; Gui et al., 2024; Anonymous, 2026); we study when any such procedure
can succeed under task-specific structured losses (see Related Work).

Contributions. Our contribution is a characterization—a synthesis of known distribution-free tools with
new sharpenings and a constructive dual, not a new conformal primitive.

     1. Sharpened two-sided feasibility frontier. We upgrade the abstention floor to the attained (µ −
        α)/(M −α), M = ess sup R (Proposition 3; strictly tighter than the M =1 floor when an audited M <
        1 holds), with an exact extremal-law reachability condition, and decompose achievable abstention
        into this floor plus a marginal dispersion gap plus a score ordering gap that a better-ranked score
        can shrink (Remark 4), tying the impossibility result to score quality. This specializes—rather than
        reinvents—known-distribution reject-option optima (Chow, 1970; El-Yaniv & Wiener, 2010; Franc
        et al., 2023).

     2. A proven certification phase diagram. We sharpen a known pairwise bound-width compar-
        ison (Maurer & Pontil, 2009) into the hierarchy Λ∗Hoeff ⊆ Λ∗Bern ⊆ Λ∗e-CRC (Proposition 2) and,
        at relaxed targets, a closed-form reversal frontier α∗ (n, δ) (exact on binary losses) with a Pareto-
        necessity result: no single bound dominates, e-CRC subsumes Bernstein, so the minimal sufficient
        set is {Hoeffding, e-CRC} (Proposition 7). Verified across 716 configurations: 51/72/80 certified at
        strict targets (Hoeffding→Bernstein +41%; e-CRC 4.2% vs. 1.9% at 10% calibration; relaxing α
        unlocks 28% NER, 13% QA, 19% CLS at α = 0.40).

     3. A negative shift result with a constructive counterpart. Under cross-dataset shift with
        µ > α, the target is violated on 14 of 16 transfers by static CRC and every tested ACI step size
        (γ ∈ [0.001, 0.1], 7 values); a full-feedback anytime-valid monitor certifies 0/16 on the same transfers
        while emitting 65–97% on feasible streams (§3.6), and an emit-only obstruction (Proposition 8)
        shows ACI’s failure is a feedback-model property, not tuning. (ACI still helps under gradual shift:
        60%→4% temporal, <12% severity-sweep.)

     4. An open benchmark, all configurations reported. Evaluation spans six models (3B–72B) from
        three families, eight datasets, four tasks, and six scores; all 716 configurations are reported with no
        post-hoc exclusion, including the negative shift result above. Calibrated score fusion is analyzed as
        a score-quality question (§3.7): on a disjoint split it yields only marginal AUROC gains and does
        not expand the certified set.

No prior line of work combines all five ingredients—applicability to structured LLM outputs, risk-based
(not merely coverage-based) control, the abstention lower bound, the bound hierarchy, and shift adaptation
(Appendix Table M.2).


2   Method

Problem setup. An LLM f : X → Y produces ŷ = f (x); a score s(x, ŷ) ∈ [0, 1] quantifies reliability,
and a selective predictor emits when s ≥ λ. We seek λ∗ with E[Rtask (Ŷ , Y ) | s(X) ≥ λ∗ ] ≤ α with
probability ≥ 1 − δ, where Rtask is a task-specific risk and α the target. The four risks RNER = 1 − F1entity ,
RJSON = 1 − F1field , RQA = 1 − I(EM), RCLS = 1 − I(correct) are bounded in [0, 1], satisfying CRC
requirements (Angelopoulos et al., 2024; 2025) (background in Appendix A).


                                                       2
CRC calibration. Given calibration {(xi , yi )}ni=1 , we compute scores si and risks ri . Thresholds come
from a fixed grid Λ of 200 evenly spaced points on [0, 1]; the emit set is Eλ = {i : si ≥ λ}, nλ = |Eλ |, and
candidates are grid points with nλ ≥ 20 (a pre-registered, score-deterministic rule).p    All three bounds scan
candidates in decreasing λ, test each at level δ (for standard CRC, UH (λ) = R̂(λ) + log(2/δ)/(2nλ ) ≤ α),
stop at the first failure, and set λ∗ to the smallest certified threshold, controlling family-wise error without
multiplicity correction (Appendix Lemma E.1). At test time we emit when s ≥ λ∗ , with the guarantee
P(E[R | s ≥ λ∗ ] > α) ≤ δ for i.i.d. calibration data.

2.1   Betting-Based CRC (e-CRC)

The Hoeffding UCB ignores variance. The empirical Bernstein bound (Maurer & Pontil, 2009) incorporates
sample variance σ̂ 2 :                    s
                                                    2σ̂ 2 log(2/δ) 7 log(2/δ)
                                  UB (λ) = R̂ +                   +           ,                                (1)
                                                           nλ       3(nλ − 1)
where σ̂ 2 is the empirical variance with the 1/n convention, matching our implementation (Appendix E).
This is tighter than Hoeffding whenever the emit-set variance satisfies an explicit finite-sample condition
σ̂ 2 ≤ c(nλ , δ) whose large-n limit is the classical σ̂ 2 < 1/4 (Proposition 2); the asymptotic condition holds
for all our datasets (Table 1). We go further using the testing-by-betting framework (Shafer, 2021; Waudby-
Smith & Ramdas, 2024; Ramdas et al., 2023; Grünwald et al., 2024; Vovk & Wang, 2021). For each candidate
λ, we construct a wealth process over the emit set Eλ : W0 = 1, Wj = Wj−1 (1 + κj (α − rj )), where κj is
a Kelly-style bet clipped to [0, 0.5] with κ1 = 0 (no bet before the first observation). The e-value is the
minimum wealth Wm over 22 pre-registered orderings of the emit set (score-descending, score-ascending,
and 20 seeded random permutations); if this minimum reaches 1/δ, the test at λ passes. Threshold selection
uses the same descending fixed-sequence scan as above (Appendix B for full pseudocode).
Theorem 1 (Betting-Based Risk Validity). For i.i.d. calibration data and any fixed threshold λ, the e-CRC
test satisfies P(E[R(λ)] > α and λ certified) ≤ δ.

Proof sketch. Under H0 : E[R] ≥ α, non-negative bets make the wealth {Wj } a non-negative supermartin-
gale. By Ville’s inequality (Howard et al., 2021), P(supj Wj ≥ 1/δ) ≤ δ. Full proof in Appendix E.

Theorem 1 is stated for a fixed λ; Appendix E (Lemma E.1) extends validity to the scan-selected λ̂ via
fixed-sequence testing with early stopping, which requires no risk-monotonicity assumption.
Proposition 2 (Bound Ordering). Fix a calibration set with bounded risks ri ∈ [0, 1], a shared candidate
threshold set, and confidence level δ; write L = log(2/δ), and let nλ ≥ 2 and σ̂λ2 denote the size and empirical
variance of the emit set Eλ . (i) Hoeffding ⊆ Bernstein (finite-sample). For an emit set of size n ≥ 2,
UB (λ) ≤ UH (λ) holds if and only if
                                                          r                !2
                                                      n      L       7L
                                   σ̂ ≤ c(n, δ) :=
                                     2
                                                                −             ,
                                                     2L     2n 3(n − 1)

valid when L/(2n) > 7L/(3(n − 1)) (which holds for all n above a small threshold depending only on δ;
             p

e.g. n ≥ 35 at δ = 0.1); when this positivity condition fails, UB > UH for every σ̂ 2 ≥ 0. Consequently,
Λ∗Hoeff ⊆ Λ∗Bern holds deterministically on any calibration set on which every emit set satisfies σ̂λ2 ≤ c(nλ , δ);
as n → ∞, c(n, δ) → 1/4, recovering the classical condition σ̂ 2 < 1/4. In our experiments this condition held
on 99.6% of the emit sets at which the Hoeffding UCB certifies (those on which the inclusion depends) and on
50 of the 51 selected emit sets of Hoeffding-certified configurations, but on only 40.7% of all candidate emit
sets; at strict targets (α ≤ 0.20) the certified sets were nested without exception, while at relaxed targets the
ordering reverses exactly where the condition fails (§3.3). (ii) Bernstein ⊆ e-CRC (asymptotic and empirical).
Under any alternative with E[R] < α, the clipped Kelly-style bet has strictly positive expected log-wealth drift,
so the wealth test is consistent: as n → ∞ it certifies every fixed threshold whose true risk is below α, hence
(asymptotically) every threshold Bernstein certifies. We make no deterministic finite-sample claim for this
inclusion. Empirically it held without exception: no configuration was certified by Bernstein but not by e-CRC
at any α (0.05–0.20 across five seeds, 3,580 paired evaluations, and α ∈ {0.25, 0.30, 0.40}).


                                                        3
Intuition: Hoeffding treats R as worst-case on [0, 1]; Bernstein tightens when σ̂ 2 ≤ c(n, δ); e-CRC adapts
sequentially via betting. The tightening is regime-dependent (Bernstein under low variance, e-CRC under
scarcity), and at relaxed targets the Hoeffding–Bernstein ordering reverses (§3.3). Proof in Appendix E.

2.2   Fundamental Limits of Certification

Proposition 3 (Sharpened two-sided abstention floor). Let µ = E[R] be the base risk and M = ess sup R ≤ 1,
with α < M . Any selective predictor whose emitted risk satisfies E[R | emit] ≤ α must abstain with probability
                                                       µ−α    µ−α
                                       P(abstain) ≥         ≥     .
                                                       M −α   1−α
The bound is attained: the two-point law R ∈ {0, M } paired with a perfectly ordering score meets it with
equality, and a general law reaches it iff P(R = M ) ≥ (µ − α)/(M − α); it is thus a tight feasibility frontier,
not merely a lower bound. For losses bounded away from 1, i.e. when an audited M < 1 holds, (µ−α)/(M −α)
strictly sharpens the M = 1 floor and is deployable by auditing M on held-out data. On our F1 /exact-match
losses a complete per-example miss gives R = 1, so the audited M = 1.00 for every NER/QA/CLS dataset
and the sharpening coincides with the standard floor there; only JSON field-F1 has M ≤ 0.33, and there
µ < α already (audited values in Appendix R). The population statement is exact; for a known  p or audited
M and µ̂ from n held-out points at level δ/2, the plug-in correction is ε/(M − α), ε = log(2/δ)/(2n)
(Appendix E). Tables in this paper report the conservative M = 1 instance (µ − α)/(1 − α), which remains
a valid floor.

Proof sketch. Decompose µ = E[Rϕ] + E[R(1 − ϕ)] for emit indicator ϕ; validity gives E[Rϕ] ≤ α E[ϕ]
and R ≤ M pointwise gives E[R(1 − ϕ)] ≤ M (1 − p), p = E[ϕ]. Hence µ ≤ αp + M (1 − p), forcing
p ≤ (M − µ)/(M − α) and abstention ≥ (µ − α)/(M − α). Attainment and the extremal-law condition are
proved in Appendix N.
Remark 4 (Floor plus dispersion and ordering gaps). The minimum abstention achievable by a score-
measurable rule decomposes as ADF = M         −α + ∆disp (R) + ∆ord (S) with ∆disp , ∆ord ≥ 0: a marginal-only
                                            µ−α

dispersion gap (= 0 iff P(R=M ) ≥ floor) and a score-only ordering gap (= 0 iff the calibrated score E[R | S]
orders risk perfectly at the operating point). Calibrated fusion (§3.7) leaves ∆disp fixed and can act only on
∆ord , tying score quality to certification in principle (Appendix N); empirically, on our grid the gain fusion
buys is on ranking, not on the certified set (§3.7).

Why this matters (beyond the algebra). The one-line lower bound is total expectation; its value is as
a tight feasibility frontier. The per-law achievability—that the optimal selective rule thresholds the calibrated
conditional risk—is classical known-distribution reject-option theory (Chow, 1970; El-Yaniv & Wiener, 2010;
Franc et al., 2023), which we specialize rather than reinvent. What is specific to the distribution-free regime is
(i) the ess sup sharpening, (ii) the degeneracy of the distribution-free minimax—under an uninformative score
the only valid rule is full abstention, so the floor is a frontier, not a saddle—and (iii) the score decomposition
(Rem. 4), which names why score quality, not the floor, sets the achievable gap. As a deployment-feasibility
test it explains in closed form why many NER/QA/CLS configurations cannot be certified at strict α and
predicts observed abstention across 3B–72B models (Appendix Table H.1).
Remark 5. When µ > α, any valid method must abstain on ≥ (µ − α)/(1 − α) examples, regardless of
bound tightness, score quality, or calibration size. For CoNLL NER at 72B (µ = 0.24, α = 0.10): abstention
≥ 15.6%; at 3B (µ = 0.42): ≥ 35.6%. Computing µ on a held-out set thus decides feasibility before running
any CRC procedure.

2.3   Score Fusion and Adaptive Inference

Calibrated score fusion. Individual scores capture complementary signal (agreement, per-token confi-
dence, output diversity) (Wang et al., 2023; Kuhn et al., 2023; Farquhar et al., 2024). We learn s̃(x) =
σ(w⊤ [s1 , . . . , sK ] + b) by logistic regression predicting I(R ≤ α) on a held-out slice of the training split
(disjoint from calibration), then run CRC using s̃, preserving validity while improving ranking.


                                                        4
Proposition 6 (Fusion Preserves CRC Guarantee). Let s̃(x) = g(s1 (x), . . . , sK (x)) where g is a fixed,
deterministic function independent of the calibration sample used by CRC (e.g., learned on disjoint data
or a held-out split). Then running CRC with s̃ preserves the finite-sample guarantee: P(E[R(λ̃∗ )] >
α and a certified threshold exists) ≤ δ.

Proof sketch. Conditioned on fixed g, the transformed scores s̃i are a deterministic function of (xi , yi ), so the
scored calibration sample retains its i.i.d. structure and CRC validity follows for the chosen UCB/betting
bound. Full proof in Appendix E.

Adaptive conformal inference (ACI). Under distribution shift, the exchangeability assumption under-
lying CRC is violated, and static thresholds can fail badly (our experiments show 60–88% violation rates).
Following ACI (Gibbs & Candès, 2021; Tibshirani et al., 2019; Barber et al., 2023), we update the threshold
online:
                             λt = λt−1 + γ(α − eff t ),    eff t = rt · I{emitt },                      (2)
where γ > 0 is the step size and eff t is the effective risk at time t: the observed risk rt if the prediction was
emitted (requiring feedback labels or a verification signal) and 0 on abstention. Effective risk below α raises
the threshold; effective risk above α lowers it. When the clamp of λt to [λmin , λmax ] (the score range) never
                                                      PT
binds, telescoping the update gives the identity T1 t=1 eff t = α − (λT − λ0 )/(γT ) (Appendix Theorem E.2):
the long-run effective risk is pinned near α, which is an algebraic property of the update, not a finite-sample
guarantee on emitted risk. We set γ = 0.01 in headline runs.

3     Experiments

Roadmap. We first use Proposition 3 as a feasibility test: when µ > α, low certification at strict targets
is the outcome the theory anticipates. Relaxing the target (§3.3) then expands certification on hard tasks
and reveals the Hoeffding–Bernstein reversal, before we compare bound tightness and shift-handling.

3.1   Setup

Models. Six open-weight models from three families: Qwen2.5-Instruct (3B, 7B, 14B, 72B-AWQ) (Team,
2024), Gemma-3 (4B) (Gemma Team, Google DeepMind, 2025), Ministral (8B) (Mistral AI, 2024), served
with vLLM (Kwon et al., 2023) on A100-80GB (greedy and K = 10 sampling, T = 0.7).

Datasets. Eight datasets across four tasks (Appendix Table M.1): CoNLL-2003 (Tjong Kim Sang
& De Meulder, 2003), Few-NERD (Ding et al., 2021), WNUT-17 (Derczynski et al., 2017) (NER);
TriviaQA (Joshi et al., 2017), NQ Open (Kwiatkowski et al., 2019) (QA); MMLU-STEM, MMLU-
Humanities (Hendrycks et al., 2021) (CLS); JSON-Extract (JSON).

Scores. Six nonconformity scores: Token Margin (TM), NLL, Self-Consistency (SC), Semantic Entropy
(SE), Entity Agreement (EA, NER-specific), Field Completeness (FC, JSON-specific). All normalized to
[0, 1]; higher = more reliable. Details in Appendix D.

Protocol. 60/40 calibration–test split (seed 42; seeds 42–46 in Appendix J); δ = 0.1; thresholds on cali-
bration only. We report 716 model-dataset-score-α configurations, none excluded post hoc: retained iff both
splits have ≥ 20 valid (score, risk) pairs, covering three bounds × six models × eight datasets × up to six
scores. The 72B model uses greedy scores only (TM, NLL).

3.2   LLMs Are Miscalibrated for Structured Tasks

Models report average confidence 74–97% but actual risk ranges from 3% (JSON) to 80% (NQ Open), with
ECE from 0.05 to 0.61. Miscalibration severity correlates with µ: where models are most wrong they are also
most overconfident, making heuristic abstention doubly unreliable (Guo et al., 2017; Kadavath et al., 2022;
Xiong et al., 2024).


                                                        5
                              Dataset    Task        µ       Var(R)     LB      n
                              CoNLL      NER     0.356        0.179   28.4%   3453
                              FNERD      NER     0.540        0.164   48.9%   2000
                              WNUT       NER     0.480        0.237   42.2%   1287
                              TQA        QA      0.441        0.241   37.9%   1000
                              NQ         QA      0.804        0.156   78.2%   3610
                              STEM       CLS     0.516        0.242   46.2%    400
                              Hum.       CLS     0.333        0.217   25.9%    400
                              JSON       JSON    0.033        0.007    0.0%    600

Table 1: Base risk µ and risk variance by dataset (averaged over the five sampling-based models; 72B is greedy-
only). All datasets satisfy Var(R) < 1/4, the large-sample form of the variance condition of Proposition 2
(the finite-sample condition holds on 99.6% of Hoeffding-certifying emit sets, 40.7% of all candidates). LB =
max{0, (µ − α)/(1 − α)} is the minimum abstention required by any valid method at α = 0.10 (Prop. 3).
The audited M = ess sup R = 1.00 on every NER/QA/CLS dataset (complete per-example misses occur),
so the sharpened floor (µ − α)/(M − α) coincides with this M =1 instance here (Appendix R).


3.3   Extended Risk Targets Unlock Hard Tasks

At α = 0.10, NER/QA/CLS certifications are near-zero because µ ≫ α, as Proposition 3 predicts: averaged
over the five sampling-based models, the floor (µ − α)/(1 − α) is 40.0% (NER, µ = 0.46), 57.8% (QA,
µ = 0.62), and 35.6% (CLS, µ = 0.42) minimum abstention, a basic limit of distribution-free abstention, not
of any method.
Relaxing the target changes this. At α = 0.30 the best bound certifies 16% of NER, 8% of QA, 11% of
CLS score-configurations; at α = 0.40, 28% NER, 13% QA, 19% CLS (JSON near 100% throughout). These
targets are realistic (70% accuracy, 60% F1) and useful for triage when the alternative is no guarantee.

The bound hierarchy reverses at relaxed targets. Which bound certifies most also changes. At
α ≤ 0.20 the certified sets are nested (Hoeffding ⊆ Bernstein ⊆ e-CRC) with zero reversals in 3,580 paired
evaluations. At α ≥ 0.25 the Hoeffding–Bernstein ordering reverses (visualized in Appendix Fig. R.1b): total
certifications at α = 0.30 are Hoeffding 42 > e-CRC 41 > Bernstein 35 (of 179 score-configurations), and at
α = 0.40 they are 57 > 55 > 48; the reversal is seed-stable across seeds 42–46 (Appendix R). Proposition 7
makes this a predictive boundary rather than an observation.
In plain terms: part (i) pins down the exact target α∗ above which the simple Hoeffding bound beats the
variance-aware Bernstein bound, a crossover driven by Bernstein’s additive penalty, not a real loss of power;
part (ii) shows no single bound is best everywhere, so a practitioner needs at least Hoeffding and e-CRC.
Proposition 7 (Reversal frontier and Pareto necessity). Fix δ; write L = log(2/δ), wH (n) = L/(2n),
                                                                                                     p

c(n, δ) as in Prop. 2, and A(n) = wH (n) − 7L/(3(n − 1)). (i) Reversal frontier. When A(n) > 0 (i.e. n ≥ 35
at δ = 0.1), a feasible emit set of size n that Hoeffding certifies but empirical Bernstein does not exists iff

                                α > α∗ (n, δ) := wH (n) + 12 1 − 1 − 4c(n, δ) .
                                                                  p             


For binary 0/1 losses (QA exact-match, CLS accuracy) the Bhatia–Davis bound σ̂ 2 ≤ R̂(1 − R̂) (the largest
variance a [0, 1] quantity of mean R̂ can have) holds with equality, so α∗ is the exact reversal boundary
on the hard tasks; α∗ has minimum 0.169 at n = 88 and rises to 12 as n → ∞. (ii) Pareto necessity. No
single bound dominates the other two: on the operating grid some configurations are certified by Hoeffding
but by neither other bound (3) and some by e-CRC but by neither other bound (10), while e-CRC statistically
subsumes empirical Bernstein (Maurer & Pontil, 2009; Waudby-Smith & Ramdas, 2024) (0 configurations
certified by Bernstein but not e-CRC). The minimal sufficient set for maximal certification is therefore
{Hoeffding, e-CRC}; empirical Bernstein is a closed-form convenience.

Proof in Appendix O (Propositions O.1–O.2). The α = 0.30 and 0.40 counts confirm part (i): reversals appear
only above the frontier, with 0 of 947 pointwise reversals below α∗ (n) in the n ≥ 35 regime (Appendix O).


                                                         6
                                                      Hoeffding    Bernstein    e-CRC (Ours)
                      Certified configs              51 (7.1%) 72 (10.1%)        80 (11.2%)
                      Violations (cert.)               0/51       0/72              0/80
                      Avg. abst. (joint-cert., n=51)   7.6%       6.9%              6.2%
                      Low-variance (σ̂ 2 < 0.1, n = 88)
                      Certified                         47 (53%) 65 (74%)         72 (82%)
                      High-variance (σ̂ 2 ≥ 0.1, n = 628)
                      Certified                          4 (0.6%)    7 (1.1%)     8 (1.3%)
                      Cal. efficiency (cert. rate at cal fraction 0.1)
                      Cert. rate                           1.1%        1.9%        4.2%

Table 2: Three-way comparison of certification bounds across 716 configurations (seed 42; calibration-
efficiency row averages seeds 42–44). All three keep near-zero violation rates, but variance-aware methods
certify more and abstain less. The “joint-cert.” abstention row averages over the 51 configurations certified by
all three methods (a subset of each method’s own certified set), not each method’s own-set average; over their
own certified sets Bernstein and e-CRC average higher abstention (10.6%, 11.5%) because they additionally
certify harder configurations.


This is the regime change Proposition 2 describes: the configurations that become certifiable are high-variance
(NER/QA/CLS), exactly where σ̂ 2 ≤ c(n, δ) fails and Bernstein’s additive 7L/(3(n−1)) term makes it looser
than Hoeffding. e-CRC never certifies fewer configurations than Bernstein at any tested α (72B certification
with scale is discussed below).


3.4   CRC Validity

Across all four α levels (per-cell results in Appendix Table H.3), CRC maintains risk control: certified
configurations show zero test violations at seed 42 (0/51, 0/72, 0/80). JSON certifies with zero abstention
(µ ≈ 0); for NQ-Open (µ = 0.80) nothing certifies even at α = 0.20, the floor at work. Pooled over five
seeds, certified-set violations are 1/261, 1/361, 1/409 (Clopper–Pearson 95% upper limits 2.1%, 1.5%, 1.4%;
Appendix J), far below δ = 0.1.
The hierarchy of Proposition 2 holds at strict targets: Hoeffding certifies 51 (7.1%), Bernstein 72 (10.1%), e-
CRC 80 (11.2%) of 716, nested in every run (Hoeffding→Bernstein the largest upgrade, +41%). The ordering
is seed-stable: across seeds 42–46 (3,580 paired evaluations) not a single reversal (McNemar p = 1.6 × 10−30 ,
7.1 × 10−15 ; Appendix J). High-variance configs certify ≤ 1.3% under every bound, in line with the floor.

Theory matches practice (Appendix Table H.1). The floor (conservative M = 1 instance) predicts
minimum abstention across datasets and scales: while µ > α for NER/QA/CLS, low strict-target certification
is expected, and µ stays above α = 0.10 even at 72B (closest: MMLU-Humanities µ = 0.17; hardest: NQ
Open µ = 0.70). A direct audit supports the floor: across the 159 (model, dataset, α) cells with µ > α,
neither the 35 certified instances nor an oracle emitter ever abstained below it (0 violations), whereas the
naive 1 − α/µ is oracle-violated in 156/159 cells.

Three-way bound comparison (Table 2). Among the 51 configurations certified by all three methods,
average test abstention drops from 7.6% (Hoeffding) to 6.9% (Bernstein) to 6.2% (e-CRC): tighter bounds
need less abstention for the same guarantee. e-CRC’s edge is largest under scarcity (10% calibration: 4.2%
vs. 1.9% Bernstein, 1.1% Hoeffding), which matters in low-resource extraction.

Model scale determines controllability. Average base risk falls with scale (Qwen2.5 3B/7B/14B:
49%/43%/36%), and reducing µ directly expands certifiable configurations, consistent with Proposition 3:
the 72B model (µ = 0.24 on CoNLL NER, greedy-only) certifies at α = 0.25 via e-CRC and reaches zero
test abstention at α = 0.30.


                                                         7
3.5   ACI Under Distribution Shift

We evaluate ACI under three shift types of increasing realism.


(i) Temporal shift models pipeline drift via index-order splitting (CoNLL by publication date, TriviaQA
by source document). In the original run, static CRC violates on 60% (15/25) of configs; ACI reduces this
to 4% (1/25).


(ii) Severity sweep models gradual quality degradation. We oversample high-risk examples 1–3×; in the
original run, static CRC rises from 8% to 56% violations while ACI stays < 12%.


(iii) Cross-dataset transfer models genuine domain shift: calibrate on one dataset, deploy on another
without recalibration (CoNLL→WNUT, CoNLL→FewNERD, TriviaQA→NQ). This is the regime the floor
warns about: every target has µ = 0.40–0.84 > α = 0.10. The emitted-risk target is violated on 14 of 16 runs
under both static CRC and every tested γ ∈ [0.001, 0.1] (7 values); the compliant pairs differ between methods
and involve near-total abstention (Appendix Table I.1, Appendix I). ACI instead controls the effective risk
(violations 11/16 at γ = 0.01), and its compliant runs abstain 75–100%, at or above the floor. Adaptation
cannot beat infeasibility.


3.6   A Constructive Counterpart Under Shift

The cross-dataset result is negative, but it has a constructive dual. On the same 16 transfers where static
CRC and ACI violate the target on 14/16 runs, a full-feedback anytime-valid monitor (SAVeR-FF) that
abstains whenever it cannot certify emitted risk at level δ achieves 0/16 violations, and is non-vacuous
on feasible streams, emitting 65–97% of inputs (JSON at α=0.10; CoNLL at α=0.40) at controlled risk.
It maintains a per-threshold test-supermartingale (Howard et al., 2021; Waudby-Smith & Ramdas, 2024)
with a predictable release rule, giving anytime emitted-risk control under arbitrary shift, with abstention
respecting the floor of Prop. 3. The construction is not new—closely related to A-RCPS (Xu et al., 2024),
Conformal Selective Acting (Khosravi & Huo, 2026), and anytime-valid CRC (Hultberg et al., 2026)—and
we claim no novelty for the machinery; the contribution is the demonstrated dual on the paper’s own failed
transfers plus the obstruction below (full details in Appendix Q).
Proposition 8 (Emit-only feedback obstruction). Under emit-only feedback (risk observed only on emitted
inputs) and arbitrary shift, any procedure that guarantees anytime emitted-risk control at level α with proba-
bility ≥ 1 − δ (δ < 1) and emits with positive probability can be forced to violate. ACI uses emit-only feedback,
so its failure is a property of the feedback model, not of the step size γ; the positive guarantee requires full
feedback (a verifier, or labels on abstained inputs).

Proof in Appendix Q (Proposition Q.3).


3.7   Score Fusion

Fusion is a score-quality question, not a certification lever. On a disjoint split (weights fit on a held-out
slice disjoint from CRC calibration; AUROC read out-of-sample, respecting Proposition 6’s independence
requirement), calibrated fusion improves AUROC on 23 of 34 configurations (68%), mean +0.004, median
+0.006, up to +0.062, with a worst-case loss of −0.154 on a small-n MMLU-Humanities configuration where
the fusion weights overfit. Crucially, fusion never certifies a configuration that no individual score already
certifies: across all three bounds there are 0 fused-only certifications (Hoeffding, Bernstein, e-CRC), and in
the two cases where a fused e-CRC certificate exists it reduces test abstention by only ≈ 1.9pp. So fusion’s
benefit here is on ranking (AUROC), not on the certified set (Appendix R). Scores are complementary
(correlations 0.31–0.58). The coefficients are fit on a held-out slice and held fixed, so s̃ is deterministic and
the CRC guarantee is preserved (Proposition 6).


                                                       8
                                     NER         QA      CLS    JSON
                        Score CoNLL FNERD WNUT TQA NQ STEM Hum. JSON
                        TM  0.539     0.517   0.521 0.616 0.583 0.491 0.531 0.818
                        NLL 0.536     0.514   0.514 0.604 0.588 0.485 0.542 0.793
                        SC  0.708     0.721   0.653 0.816 0.805 0.600 0.672 0.732
                        SE  0.496     0.529   0.501 0.524 0.547 0.516 0.477 0.677
                        EA  0.680     0.690   0.616   –     –     –     –     –
                        FC    –         –       –     –     –     –     –   0.734

Table 3: AUROC of confidence scores for risk discrimination (averaged across models). Higher values indicate
better ability to distinguish correct from incorrect outputs. Bold: best per dataset. – indicates score is not
applicable.


3.8   Analysis

Score comparison. Table 3 compares AUROC of six confidence scores. Self-Consistency is the strongest
general-purpose score (best on 7/8 datasets, up to 0.82 on QA); Entity Agreement is a strong NER-specific
score (0.69 on Few-NERD); Token Margin is best for JSON (0.82). Semantic Entropy appears weak under our
exact-match clustering proxy (AUROC ≈ 0.50, except JSON, 0.68), reflecting the coarseness of exact-match
clustering rather than semantic entropy itself (Kuhn et al., 2023; Farquhar et al., 2024).

Data efficiency. Variance-aware bounds are more data-efficient: at 10% calibration e-CRC certifies 4.2%
vs. 1.9% (Bernstein) and 1.1% (Hoeffding), and e-CRC at 25% already beats Hoeffding at 70% (full sweep,
Appendix H).

Baselines. We compare CRC against Always Answer and entropy/TM/SC thresholds tuned on calibration
(Appendix Table H.4): Always Answer violates on 7/8 datasets, and threshold baselines reach low test risk
only by abstaining 85–87% without any guarantee, whereas CRC’s guarantee holds for any i.i.d. test set at
comparable or lower abstention.
The single pooled violation over five seeds (Self-Consistency, Ministral-8B, CoNLL, α = 0.2, seed 44; Ap-
pendix J) shows no bound- or model-specific pattern; rare violations are expected under a probabilistic
guarantee, and monitoring remains advisable.

Practical decision framework. The results give a three-step recipe (spelled out in the Conclusion). Step
1 (feasibility): compute µ; if µ > α, any valid method abstains on ≥ (µ − α)/(M − α) (Prop. 3). Step 2
(bound/score): at strict targets prefer Bernstein or e-CRC (variance condition of Prop. 2, met on 99.6%
of certification-relevant emit sets), checking α∗ (Prop. 7) at relaxed targets where Hoeffding can win; use
e-CRC under scarcity and Self-Consistency as the score. Step 3 (shift): re-check feasibility on the target
domain, deploy ACI (γ = 0.01) in the feasible regime, and where full feedback is available the monitor of
§3.6 certifies before emitting.

4     Discussion

There is a tension: the tasks that most need a guarantee (high-risk NER, QA) are the hardest to certify.
The floor says why: difficulty is set by µ/α, not the bound or score. Audited across 24 model-task-scale
configurations (Appendix Table H.1), it lets practitioners read off feasibility and the payoff from scaling
before any experiment.

The reversal is an artifact of the additive Bernstein term. The Hoeffding–Bernstein reversal
(Prop. 7) stems entirely from empirical Bernstein’s additive 7L/(3(n − 1)) overhead (a robustness check,
not a fourth reported method). The inverted Learn-Then-Test p-value certificate, the Hoeffding–Bentkus
bound (Bentkus, 2004; Angelopoulos et al., 2025), dominates Hoeffding unconditionally (no variance condi-
tion, no reversal; a two-line Pinsker argument, Appendix P), but operates nearer the δ budget: on our grid it


                                                      9
incurs a small nonzero test-violation rate within δ (pooled 6/479, Clopper–Pearson 95% upper 2.46% ≪ δ)
rather than the near-zero regime of the conservative additive bounds. We keep the additive bounds as our
reported certificates—their zero-violation record (0/51, 0/72, 0/80) is the paper’s operating point—and note
Hoeffding–Bentkus as the tighter valid alternative under this validity-versus-tightness trade-off.

ACI cannot beat infeasibility. Under cross-dataset transfer every target has µ ≥ 0.40 ≫ α; the target
is violated on 14/16 under static CRC and every tested γ, and ACI only drives the long-run effective risk
toward α by raising abstention. Reweighting cannot help either: the floor binds any distribution-free method,
including non-exchangeable CRC (Farinhas et al., 2024). The constructive escape is full feedback (§3.6), not
a better step size.

5   Related Work

Conformal prediction for LLMs. Conformal prediction (Vovk et al., 2005; Angelopoulos & Bates,
2023) has been applied to LLMs along four threads: factuality and claim filtering (Mohri & Hashimoto,
2024; Cherian et al., 2024); generation and abstention (Quach et al., 2024; Abbasi-Yadkori et al., 2024);
cascades, arbitration, and judging (Fanconi & van der Schaar, 2025; Overman & Bayati, 2025; Jung et al.,
2025); and alignment and property control (Gui et al., 2024; Overman et al., 2024; Campos et al., 2024).
CRC (Angelopoulos et al., 2024; Bates et al., 2021) handles arbitrary losses; Barber et al. (2023) relax ex-
changeability and Farinhas et al. (2024) reweight calibration points. Our work is orthogonal: rather than
proposing a new procedure, we ask when any such procedure can succeed under schema-validated struc-
tured losses (NER/QA/CLS/JSON) and characterize the abstention forced when it cannot; concurrent work
addresses multi-stage pipeline coverage (Anonymous, 2026).

Selective prediction and uncertainty. Selective prediction (Geifman & El-Yaniv, 2017; El-Yaniv &
Wiener, 2010; Chow, 1970) studies coverage–risk trade-offs, with jointly-trained rejection (Geifman & El-
Yaniv, 2019). Concurrent work integrates conformal prediction with selective classification as a two-stage
certified procedure (Xu et al., 2025; Yu & Liu, 2026; Lee et al., 2024) or gives error–reject curves for a
fixed conformal predictor (Hallberg Szabadváry et al., 2025); these give per-procedure guarantees, not a
distribution-free lower bound on abstention, which is what Proposition 3 supplies. LLM confidence is miscal-
ibrated (Kadavath et al., 2022; Guo et al., 2017); self-consistency (Wang et al., 2023), semantic entropy (Kuhn
et al., 2023; Farquhar et al., 2024), and elicitation (Xiong et al., 2024) offer alternatives, which we evaluate
as nonconformity scores within CRC.

Concentration inequalities and e-values. Empirical Bernstein (Maurer & Pontil, 2009) and the
Hoeffding–Bentkus p-value (Bentkus, 2004) sharpen Hoeffding; testing-by-betting yields e-values (Shafer,
2021; Grünwald et al., 2024; Ramdas et al., 2023; Vovk & Wang, 2021; Howard et al., 2021; Waudby-Smith
& Ramdas, 2024). The pairwise UCB-width comparison behind our bound hierarchy (Proposition 2) is it-
self known (Maurer & Pontil, 2009); what is new is turning it into a certification-level map through the
Bhatia–Davis variance coupling, yielding the closed-form reversal frontier α∗ (n, δ) and the Pareto-necessity
result that {Hoeffding, e-CRC} is minimal sufficient (Proposition 7). Anytime-valid and selective risk con-
trol under shift is developed by Xu et al. (2024); Khosravi & Huo (2026); Hultberg et al. (2026), on which
our constructive monitor (§3.6) builds. Our contribution is not a new inequality but a deployment-facing
characterization of when CRC can certify structured LLM outputs and when it is provably impossible.

6   Conclusion

We characterize when CRC can certify structured LLM outputs and when it cannot, as a three-step recipe
run before deploying CRC. Step 1: compute µ; the sharpened floor (Proposition 3) turns µ > α into an exact
minimum abstention rate, so a team learns in one pass whether a target is reachable before calibrating any
bound. Step 2: in the feasible regime, the phase diagram (Proposition 7) selects the bound (Bernstein or
e-CRC at strict targets, Hoeffding past α∗ ). Step 3: under shift, re-check feasibility and, where full feedback
is available, deploy the anytime-valid monitor (§3.6), the operational counterpart to the negative ACI result.


                                                      10
Making feasibility explicit turns a failed certification attempt into a specific next action instead of a dead
end.

Limitations, reproducibility, ethics. Guarantees are probabilistic (δ=0.1), assume i.i.d. calibration,
and are voided by shift; out-of-sample fusion adds no certification beyond the best single score. Full caveats,
reproducibility (public data and open-weight models; seeds 42–46; code on publication), and ethics are in
Appendices J–L.

References
Yasin Abbasi-Yadkori, Ilja Kuzborskij, David Stutz, András György, Adam Fisch, Arnaud Doucet, Iuliya
  Beloshapka, Wei-Hung Weng, Yao-Yuan Yang, Csaba Szepesvári, Ali Taylan Cemgil, and Nenad Toma-
  sev. Mitigating LLM hallucinations via conformal abstention. In NeurIPS 2024 Workshop on Statistical
  Frontiers in LLMs and Foundation Models, 2024. arXiv:2405.01563.
Anastasios N. Angelopoulos and Stephen Bates. Conformal prediction: A gentle introduction. Foundations
 and Trends in Machine Learning, 16(4):494–591, 2023.
Anastasios N. Angelopoulos, Stephen Bates, Adam Fisch, Lihua Lei, and Tal Schuster. Conformal risk
 control. In International Conference on Learning Representations (ICLR), 2024. arXiv:2208.02814.
Anastasios N. Angelopoulos, Stephen Bates, Emmanuel J. Candès, Michael I. Jordan, and Lihua Lei. Learn
 then test: Calibrating predictive algorithms to achieve risk control. Annals of Applied Statistics, 19(2):
 1641–1662, 2025. arXiv:2110.01052.
Anonymous. PASC: Pipeline-aware split conformal prediction with joint coverage guarantees for multi-stage
 NLP and LLM pipelines. arXiv preprint, 2026.
Rina Foygel Barber, Emmanuel J. Candès, Aaditya Ramdas, and Ryan J. Tibshirani. Conformal prediction
  beyond exchangeability. Annals of Statistics, 51(2):816–845, 2023.
Stephen Bates, Anastasios Angelopoulos, Lihua Lei, Jitendra Malik, and Michael Jordan. Distribution-free,
  risk-controlling prediction sets. Journal of the ACM, 68:1–34, 2021.
Vidmantas Bentkus. On Hoeffding’s inequalities. The Annals of Probability, 32(2):1650–1673, 2004. doi:
  10.1214/009117904000000360. arXiv:math/0410159.
Margarida M. Campos, António Farinhas, Chrysoula Zerva, Mário A. T. Figueiredo, and André F. T. Martins.
 Conformal prediction for natural language processing: A survey. Transactions of the Association for
 Computational Linguistics (TACL), 2024. arXiv:2405.01976.
John J. Cherian, Isaac Gibbs, and Emmanuel J. Candès.         Large language model valid-
  ity via enhanced conformal prediction methods. In Advances in Neural Information Process-
  ing Systems 37, 2024.   URL https://proceedings.neurips.cc/paper_files/paper/2024/hash/
  d02ff1aeaa5c268dc34790dd1ad21526-Abstract-Conference.html.
C. K. Chow. On optimum recognition error and reject tradeoff. IEEE Transactions on Information Theory,
  16(1):41–46, 1970.
Leon Derczynski, Eric Nichols, Marieke van Erp, and Nut Limsopatham. Results of the WNUT2017 shared
  task on novel and emerging entity recognition. In Proceedings of the 3rd Workshop on Noisy User-generated
  Text, pp. 140–147, Copenhagen, Denmark, 2017. Association for Computational Linguistics. doi: 10.18653/
  v1/W17-4418.
Ning Ding, Guangwei Xu, Yulin Chen, Xiaobin Wang, Xu Han, Pengjun Xie, Haitao Zheng, and Zhiyuan
  Liu. Few-NERD: A few-shot named entity recognition dataset. In Proceedings of the 59th Annual Meeting
  of the Association for Computational Linguistics and the 11th International Joint Conference on Natural
  Language Processing (Volume 1: Long Papers), pp. 3198–3213, Online, 2021. Association for Compu-
  tational Linguistics. doi: 10.18653/v1/2021.acl-long.248. URL https://aclanthology.org/2021.acl-
  long.248/.


                                                      11
Ran El-Yaniv and Yair Wiener. On the foundations of noise-free selective classification. Journal of Machine
  Learning Research, 11:1605–1641, 2010.

Claudio Fanconi and Mihaela van der Schaar. Cascaded language models for cost-effective human–
  AI decision-making. In Advances in Neural Information Processing Systems 38, 2025. URL https:
  //arxiv.org/abs/2506.11887.

António Farinhas, Chrysoula Zerva, Dennis Ulmer, and André F. T. Martins. Non-exchangeable conformal
 risk control. In Proceedings of the Twelfth International Conference on Learning Representations (ICLR),
 2024. URL https://openreview.net/forum?id=j511LaqEeP.

Sebastian Farquhar, Jannik Kossen, Lorenz Kuhn, and Yarin Gal. Detecting hallucinations in large language
  models using semantic entropy. Nature, 630:625–630, 2024.

Vojtech Franc, Daniel Prusa, and Vaclav Voracek. Optimal strategies for reject option classifiers. Journal
  of Machine Learning Research, 24(11):1–49, 2023. URL https://www.jmlr.org/papers/v24/21-0048.
  html. arXiv:2101.12523.

Yonatan Geifman and Ran El-Yaniv. Selective classification for deep neural networks. In Advances in Neural
  Information Processing Systems (NeurIPS), 2017.

Yonatan Geifman and Ran El-Yaniv. SelectiveNet: A deep neural network with an integrated reject option.
  In International Conference on Machine Learning (ICML), 2019.

Gemma Team, Google DeepMind. Gemma 3 technical report. Technical report, Google DeepMind, 2025.
 arXiv:2503.19786.

Isaac Gibbs and Emmanuel Candès. Adaptive conformal inference under distribution shift. In Advances in
  Neural Information Processing Systems (NeurIPS), 2021.

Peter Grünwald, Rianne de Heide, and Wouter M. Koolen. Safe testing. Journal of the Royal Statistical
  Society: Series B, 86(5):1091–1128, 2024.

Yu Gui, Ying Jin, and Zhimei Ren. Conformal alignment: Knowing when to trust foundation models with
  guarantees. In Advances in Neural Information Processing Systems (NeurIPS), 2024. arXiv:2405.10301.

Chuan Guo, Geoff Pleiss, Yu Sun, and Kilian Q. Weinberger. On calibration of modern neural networks. In
  International Conference on Machine Learning (ICML), 2017.

Johan Hallberg Szabadváry, Tuwe Löfström, Ulf Johansson, Cecilia Sönströd, Ernst Ahlberg, and Lars
  Carlsson. Classification with reject option: Distribution-free error guarantees via conformal prediction.
  Machine Learning with Applications, 20:100664, 2025. arXiv:2506.21802.

Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and Jacob Stein-
 hardt. Measuring massive multitask language understanding. In International Conference on Learning
 Representations (ICLR), 2021. URL https://openreview.net/forum?id=d7KBjmI3GmQ.

Steven R. Howard, Aaditya Ramdas, Jon McAuliffe, and Jasjeet Sekhon. Time-uniform, nonparametric,
  nonasymptotic confidence sequences. Annals of Statistics, 49(2):1055–1080, 2021.

Bror Hultberg, Dave Zachariah, and António H. Ribeiro. Anytime-valid conformal risk control. arXiv
  preprint arXiv:2602.04364, 2026.

Mandar Joshi, Eunsol Choi, Daniel Weld, and Luke Zettlemoyer. TriviaQA: A large scale distantly su-
 pervised challenge dataset for reading comprehension. In Proceedings of the 55th Annual Meeting of the
 Association for Computational Linguistics (Volume 1: Long Papers), pp. 1601–1611, Vancouver, Canada,
 2017. Association for Computational Linguistics. doi: 10.18653/v1/P17-1147.


                                                    12
Jaehun Jung, Faeze Brahman, and Yejin Choi. Trust or escalate: LLM judges with provable guarantees
  for human agreement. In International Conference on Learning Representations, 2025. URL https:
  //proceedings.iclr.cc/paper_files/paper/2025/hash/08dabd5345b37fffcbe335bd578b15a0-
  Abstract-Conference.html.

Saurav Kadavath, Tom Conerly, Amanda Askell, Tom Henighan, Dawn Drain, Ethan Perez, Nicholas Schiefer,
  Zac Hatfield-Dodds, Nova DasSarma, Eli Tran-Johnson, et al. Language models (mostly) know what they
  know. arXiv preprint arXiv:2207.05221, 2022.

Hamed Khosravi and Xiaoming Huo. Conformal selective acting: Anytime-valid risk control for RLVR-trained
  LLMs. arXiv preprint arXiv:2605.20270, 2026.

Lorenz Kuhn, Yarin Gal, and Sebastian Farquhar. Semantic uncertainty: Linguistic invariances for uncer-
  tainty estimation in natural language generation. In International Conference on Learning Representations
  (ICLR), 2023.

Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti,
  Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, Kristina Toutanova, Llion Jones, Matthew
  Kelcey, Ming-Wei Chang, Andrew M. Dai, Jakob Uszkoreit, Quoc Le, and Slav Petrov. Natural questions: A
  benchmark for question answering research. Transactions of the Association for Computational Linguistics,
  7:452–466, 2019. doi: 10.1162/tacl_a_00276.

Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E. Gon-
 zalez, Hao Zhang, and Ion Stoica. Efficient memory management for large language model serving with
 PagedAttention. In ACM Symposium on Operating Systems Principles (SOSP), 2023.

Minjae Lee, Kyungmin Kim, Taesoo Kim, and Sangdon Park. Selective generation for controllable language
 models. In Advances in Neural Information Processing Systems (NeurIPS), 2024. arXiv:2307.09254.

Andreas Maurer and Massimiliano Pontil. Empirical Bernstein bounds and sample variance penalization. In
 Conference on Learning Theory (COLT), pp. 115–124, 2009.

Mistral AI. Un Ministral, des Ministraux. https://mistral.ai/news/ministraux/, 2024. Accessed: 2026-
 07-14.

Christopher Mohri and Tatsunori Hashimoto. Language models with conformal factuality guarantees. In
  Proceedings of the 41st International Conference on Machine Learning (ICML), volume 235, pp. 36029–
  36047. PMLR, 2024. arXiv:2402.10978.

William Overman and Mohsen Bayati. Conformal arbitrage: Risk-controlled balancing of competing ob-
 jectives in language models. In Advances in Neural Information Processing Systems 38, 2025. URL
 https://arxiv.org/abs/2506.00911.

William Overman, Jacqueline Jil Vallon, and Mohsen Bayati. Aligning model properties via confor-
 mal risk control. In Advances in Neural Information Processing Systems 37, 2024. URL https:
 //proceedings.neurips.cc/paper_files/paper/2024/hash/c79625091a4f8b5d3abe29f3b14fa43a-
 Abstract-Conference.html.

Victor Quach, Adam Fisch, Tal Schuster, Adam Yala, Jae Ho Sohn, Tommi S. Jaakkola, and Regina Barzilay.
  Conformal language modeling. In International Conference on Learning Representations (ICLR), 2024.
  arXiv:2306.10193.

Aaditya Ramdas, Peter Grünwald, Vladimir Vovk, and Glenn Shafer. Game-theoretic statistics and safe
  anytime-valid inference. Statistical Science, 38(4):576–601, 2023.

Glenn Shafer. Testing by betting: A strategy for statistical and scientific communication. Journal of the
  Royal Statistical Society: Series A, 184(2):407–431, 2021.

Qwen Team. Qwen2.5 technical report. arXiv preprint arXiv:2412.15115, 2024.


                                                    13
Ryan J. Tibshirani, Rina Foygel Barber, Emmanuel Candès, and Aaditya Ramdas. Conformal prediction
  under covariate shift. In Advances in Neural Information Processing Systems (NeurIPS), 2019.

Erik F. Tjong Kim Sang and Fien De Meulder. Introduction to the CoNLL-2003 shared task: Language-
  independent named entity recognition. In Proceedings of the Seventh Conference on Natural Language
  Learning at HLT-NAACL 2003, pp. 142–147, 2003. URL https://aclanthology.org/W03-0419/.

Vladimir Vovk and Ruodu Wang. E-values: Calibration, combination and applications. Annals of Statistics,
  49(3):1736–1754, 2021.

Vladimir Vovk, Alexander Gammerman, and Glenn Shafer. Algorithmic Learning in a Random World.
  Springer, 2005.

Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and
 Denny Zhou. Self-consistency improves chain of thought reasoning in language models. In International
 Conference on Learning Representations (ICLR), 2023.

Ian Waudby-Smith and Aaditya Ramdas. Estimating means of bounded random variables by betting. Journal
  of the Royal Statistical Society: Series B, 86(1):1–27, 2024.

Miao Xiong, Zhiyuan Hu, Xinyang Lu, Yifei Li, Jie Fu, Junxian He, and Bryan Hooi. Can LLMs express
 their uncertainty? an empirical evaluation of confidence elicitation in LLMs. In International Conference
 on Learning Representations (ICLR), 2024.

Yunpeng Xu, Wenge Guo, and Zhi Wei. Selective conformal risk control. arXiv preprint arXiv:2512.12844,
  2025.

Ziyu Xu, Nikos Karampatziakis, and Paul Mineiro. Active, anytime-valid risk controlling prediction sets. In
  Advances in Neural Information Processing Systems (NeurIPS), 2024. arXiv:2406.10490.

Xiaoli Yu and Jiamiao Liu. A joint finite-sample certificate for adaptive selective conformal risk control.
  arXiv preprint arXiv:2606.08517, 2026.



A     Background

A.1   Conformal Risk Control

Conformal risk control (Angelopoulos et al., 2024) provides distribution-free guarantees on the expected
risk of a selective predictor. Given a calibration set of exchangeable examples (Xi , Yi )ni=1 , a risk function
R(Ŷ , Y ), and a target risk level α, CRC selects a threshold λ∗ such that the conditional risk E[R | emit] ≤ α
holds with high probability. The key insight is that by calibrating on the empirical risk of a nested family of
selectors, one obtains finite-sample validity without distributional assumptions.

A.2   Learn-Then-Test Framework

The Learn-Then-Test (LTT) framework (Angelopoulos et al., 2025) extends conformal prediction to risk
control. For each candidate threshold λ, LTT tests the hypothesis H0 : R(λ) > α using upper confidence
bounds, controlling the family-wise error over the candidate set with a multiple-testing correction. A Bonfer-
roni (union-bound) correction tests each candidate at level δ/|Λ|; alternatively, a pre-registered fixed-sequence
scan with early stopping tests each candidate at full level δ and needs no correction, and this is what we use
(Lemma E.1). The fixed-sequence guarantee does not require the risk to be monotone in λ; monotonicity
matters only for interpretation and power.


                                                       14
Algorithm 1 CRC Procedure: Calibration for risk control at level α (fixed-sequence scan; used for Hoeffding
and Bernstein).
 1: Input: Calibration {(xi , yi )}n
                                   i=1 , risk R, target α, failure prob. δ; fixed grid Λ = 200 evenly spaced points
    on [0, 1].
 2: For each (xi , yi ): compute si = s(xi , ŷi ) and ri = R(yi , ŷi ).
 3: Candidates: Λc = {λ ∈ Λ : nλ ≥ 20}, where Eλ = {i : si ≥ λ}, nλ = |Eλ | (deterministic given the
    scores).
 4: for λ ∈ Λc in decreasing order do
      Compute R̂(λ) = n1λ i∈Eλ ri and the level-δ UCB U (λ) (Hoeffding or Bernstein).
                             P
 5:
 6:   If U (λ) ≤ α, mark λ certified and continue; else stop (fixed-sequence rule; Lemma E.1).
 7: end for
 8: Return λ∗ = smallest certified λ (none certified ⇒ no certification).


Algorithm 2 ACI-SG: Adaptive Conformal Inference for Structured Generation.
 1: Input: Target α, step γ > 0, initial λ0 , clamp range [λmin , λmax ].
 2: for t = 1, 2, . . . do
 3:   Receive xt ; compute ŷt , st ; emit if st ≥ λt−1 , else abstain.
 4:   Observe feedback rt = R(ŷt , yt ); set eff t = rt · I{emitted at t}.
 5:   λt = clamp λt−1 + γ(α − eff t ), λmin , λmax .
 6: end for



A.3   Selective Prediction

Selective prediction (Geifman & El-Yaniv, 2017) studies the trade-off between coverage (fraction of examples
answered) and risk (error rate among answered examples). The goal is to abstain on uncertain inputs so that
the risk of emitted predictions meets a target. Our work bridges selective prediction with conformal methods
to obtain distribution-free guarantees for structured LLM outputs.

B     Algorithm Pseudocode

Algorithm 1 gives the standard CRC calibration procedure, Algorithm 2 the ACI update for structured
generation, and Algorithm 3 the betting-based e-CRC procedure of the main text.

C     Task-Specific Risk Functions

We define risk as one minus the task metric, so lower risk corresponds to better performance:

      • NER Risk: RNER = 1 − F1entity , where F1entity is entity-level micro F1 (exact span match).
      • JSON Risk: RJSON = 1 − F1field , where F1field is field-level F1 over key-value pairs.
      • QA Risk: RQA = 1 − I(exact_match).
      • Classification Risk: RCLS = 1 − I(correct).

All risk functions are bounded in [0, 1], satisfying the requirements for conformal risk control.

D     Confidence Score Details

We evaluate six confidence scores s(x, ŷ) ∈ [0, 1] where higher values indicate greater reliability:

      1. Token Margin (TM): Average gap between top-1 and top-2 token log-probabilities, normalized
         to [0, 1] via sigmoid. Higher margin → more confident.


                                                        15
Algorithm 3 e-CRC: Betting-Based Risk Control at level α.
 1: Input: Calibration {(xi , yi )}n   i=1 , risk R, target α, failure prob. δ; fixed grid Λ = 200 evenly spaced points
    on [0, 1]; candidates Λc = {λ : nλ ≥ 20}.
 2: for λ ∈ Λc , scanned in decreasing order of λ do
 3:   for each of 22 pre-registered orderings of Eλ (score-descending, score-ascending, 20 seeded random
      permutations) do
 4:      Take risks r1 , . . . , rm in that order; set W0 = 1.
 5:      for j = 1, . . . , m do
            Running mean µ̂j = j−1     1
                                                  r (predictable); κ1 = 0.
                                          P
 6:
                                            k<j k         
                                              α−µ̂j
 7:         Kelly-style bet: κj = clip α(1−α) , 0, 0.5 for j ≥ 2.
 8:        Update: Wj = Wj−1 · (1 + κj (α − rj )).
 9:      end for
10:   end for
11:   E-value e(λ) = minimum final wealth Wm over the 22 orderings.
12:   If e(λ) ≥ 1/δ, certify λ and continue the scan; else stop (fixed-sequence rule; Lemma E.1).
13: end for
14: Return λ∗ = smallest certified λ (the last certification before the stop).



      2. Negative Log-Likelihood (NLL): exp(−NLL/T ) where T is sequence length. Higher → more
         likely output.

      3. Self-Consistency (SC): Fraction of K = 10 samples matching the greedy output. Higher agreement
         → more confident.

      4. Semantic Entropy (SE): 1 − H(clusters)/ log2 K over semantically clustered outputs. Higher →
         more concentrated.

      5. Entity-Level Agreement (EA): Minimum entity agreement across K samples. NER-specific.

      6. Field-Level Completeness (FC): Minimum field agreement across K samples. JSON-specific.


E     Proofs

E.1   Proof of Theorem 1: Betting-Based Risk Validity

Proof. Step 1: E-value validity. Fix λ and let r1 , . . . , rm be the risks in Eλ , i.i.d. under the sampling
model. The wealth process is W0 = 1, Wj = Wj−1 (1 + κj (α − rj )) with predictable bets κj ∈ [0, 0.5] and
κ1 = 0. Under H0 : E[rj | Fj−1 ] ≥ α:

                                 E[Wj | Fj−1 ] = Wj−1 (1 + κj (α − E[rj | Fj−1 ]))
                                                ≤ Wj−1 ,

where the inequality uses κj ≥ 0; because κj ≤ 0.5 and rj ∈ [0, 1], every factor is positive, so {Wj } is a
non-negative supermartingale. By Ville’s inequality (Howard et al., 2021): P(supj Wj ≥ 1/δ) ≤ δ. Taking the
minimum of the final wealth over 22 pre-registered orderings only decreases the certifying statistic, so the
test remains level δ.
Step 2: Certification. Certifying when the e-value reaches 1/δ gives false certification probability ≤ δ.
Step 3: Growth rate (heuristic). For unclipped Kelly bets, the expected log-wealth growth per observation
under an alternative with mean µ < α is of order (α − µ)2 /(2 E[(α − R)2 ]) to second order; clipping to [0, 0.5]
can only reduce this rate. We use this only as intuition for why the betting test is powerful when the risk
distribution is concentrated below α; no formal rate claim is made or used.


                                                           16
E.2   Validity of the Selected Threshold under Grid Search

Theorem 1 of the main text controls the error of the test at a fixed λ. The procedures of Algorithms 1
and 3, however, scan a candidate set and return a data-dependent λ̂. The following lemma licenses exactly
the implemented selection rule; it requires no monotonicity of the risk in λ.
Lemma E.1 (Validity of the descending fixed-sequence scan). Condition on the calibration scores s1 , . . . , sn .
The candidate set Λc = {λ ∈ Λ : nλ ≥ 20} (fixed grid ∩ size rule) and its descending scan order are then
deterministic, and conditional on the scores the risks in any emit set are i.i.d. draws from the score-conditional
risk distribution. Suppose each candidate λ is tested with a level-δ test of H0 (λ) : E[R(λ)] > α (the level-δ
UCB test for Hoeffding and Bernstein; the Ville wealth test for e-CRC), scanning Λc in decreasing order of
λ and stopping at the first failure, with every candidate passed before the stop certified. Then
                                                                         
                                   P some certified λ has E[R(λ)] > α ≤ δ.

Proof. This is a fixed-sequence testing argument in the sense of Learn-then-Test (Angelopoulos et al., 2025).
The certified set is by construction a prefix of the fixed scan order λ(1) > λ(2) > · · · > λ(m) . Let

                                       λ† = max{λ ∈ Λc : E[R(λ)] > α}

be the first true null in scan order; if no candidate is null there is nothing to prove. Because the certified
prefix is contiguous from λ(1) , it contains a true null if and only if it contains λ† (every other null appears
later in the scan than λ† ). Hence

                                      P some certified λ has E[R(λ)] > α
                                                                            

                                         ≤ P λ† certified ≤ δ,
                                                          


where the last step is the level-δ guarantee of the single test at λ† : Ville’s inequality applied to the wealth
process {Wj (λ† )} for e-CRC (Howard et al., 2021; Ramdas et al., 2023), or the level-δ UCB test for Hoeffd-
ing/Bernstein. Controlling this single boundary test controls the family-wise error over the entire scan; no
correction over |Λc | is needed (Angelopoulos et al., 2025; Grünwald et al., 2024).

Remark (monotonicity and Bonferroni). Note what the argument does and does not use. Early-stop
fixed-sequence FWER control does not require the risk λ 7→ E[R(λ)] to be monotone: rejections form a prefix
of a pre-registered order, so the first true null in scan order gates all others, and it is falsely certified with
probability at most δ. Monotonicity matters only for interpretation (with nonincreasing conditional risk the
nulls form a contiguous low-λ tail and the scan stops near the feasibility boundary) and for power (a non-
monotone empirical risk curve can stop the scan at an unlucky early candidate, forfeiting certifications further
down). An alternative requiring no ordering at all is a Bonferroni correction, testing every candidate at level
δ/|Λc |, i.e., dividing the level by the number of candidates (a multiplicative factor on δ); the fixed-sequence
scan avoids this factor and tests each candidate at full level δ.

Provenance note. An earlier version of our pipeline searched the full threshold grid without the fixed-
sequence rule (with data-dependent grid endpoints) and allowed signed bets; all results reported in this paper
use the corrected procedure described above.

E.3   Proof of Proposition 2: Bound Ordering

Proof. Part (i): Hoeffding ⊆ Bernstein (finite-sample). Write L = log(2/δ) and fix an emit set of size
n ≥ 2 with empirical mean R̂ and empirical variance σ̂ 2 . Both bounds are stated with the shared two-sided
constant L = log(2/δ), matching the Maurer–Pontil statement and making the two UCBs directly compara-
ble; using the one-sided constant log(1/δ) in both would rescale c(n, δ) but change no containment statement.
Throughout, σ̂ 2 is the empirical variance with the 1/n convention (ddof = 0), matching our implementation;
Maurer & Pontil (2009) state the bound with the unbiased (1/(n − 1)) variance, and recomputing our entire


                                                       17
grid with the unbiased convention left every certified set unchanged. The two upper confidence bounds are
                                                  r
                                                     L
                                      UH = R̂ +          ,
                                                     2n
                                                  r
                                                     2σ̂ 2 L      7L
                                      UB = R̂ +              +          .
                                                       n       3(n − 1)
Subtracting R̂ from both sides, UB ≤ UH is equivalent to
                                        r           r
                                          2σ̂ 2 L      L        7L
                                                  ≤       −          .
                                            n          2n 3(n − 1)
If the right-hand side is negative, i.e. L/(2n) ≤ 7L/(3(n − 1)), the inequality fails for every σ̂ 2 ≥ 0:
                                         p

Bernstein is looser than Hoeffding regardless of the variance. When the right-hand side is nonnegative, both
sides are nonnegative and squaring is an equivalence:
                                        r                !2
                            2σ̂ 2 L       L        7L
                                    ≤          −
                               n          2n 3(n − 1)
                                                            r               !2
                                                        n      L       7L
                                ⇐⇒ σ̂ ≤ c(n, δ) :=
                                        2
                                                                  −            ,
                                                       2L      2n 3(n − 1)

which is the claimed if-and-only-if condition. The positivity condition L/(2n) > 7L/(3(n − 1)) holds for
                                                                        p

all n above a threshold depending only on δ; at δ = 0.1 (L = log 20 ≈ 3.0) it holds for n ≥ 35 and fails for
n ≤ 34.
For the large-n limit, expand the square:
                                               r                        !
                                       n L       L     7L          49L2
                            c(n, δ) =       −2     ·         +
                                      2L 2n      2n 3(n − 1) 9(n − 1)2
                                      1  7              49 nL
                                            p
                                              nL/2
                                    =   − ·        +             .
                                      4  3 n−1        18(n − 1)2
Both correction terms are O( L/n), so c(n, δ) → 1/4 as n → ∞, recovering the classical asymptotic
                                 p

condition σ̂ 2 < 1/4. The finite-sample condition is strictly stronger: because of the additive term 7L/(3(n −
1)), Bernstein can be looser than Hoeffding at moderate n even when σ̂ 2 < 1/4 (e.g. at δ = 0.1, c(120, 0.1) ≈
0.056 and c(600, 0.1) ≈ 0.147). Whenever every emit set indexed by the candidate grid satisfies σ̂λ2 ≤ c(nλ , δ),
we have UB (λ) ≤ UH (λ) pointwise, hence {λ : UH (λ) ≤ α} ⊆ {λ : UB (λ) ≤ α}, i.e. Λ∗Hoeff ⊆ Λ∗Bern
deterministically on that calibration set. Note that the inclusion of certified configurations only requires the
condition at emit sets where the Hoeffding UCB certifies: if UH (λ) ≤ α and UB (λ) ≤ UH (λ) at that λ,
Bernstein certifies too. In our experiments the condition held on 99.6% of such Hoeffding-certifying emit
sets, and on 50 of the 51 emit sets actually selected for Hoeffding-certified configurations (over all candidate
emit sets evaluated in the calibration scan, including small and high-variance sets, the fraction is 40.7%);
at α ≤ 0.20 the certified sets were nested in every configuration and every split seed, while at α ≥ 0.25 the
ordering reverses exactly where the condition fails (Section 3.3).
Part (ii): Bernstein ⊆ e-CRC (asymptotic and empirical). This inclusion is asymptotic, not finite-
sample. Under any fixed alternative with µ = E[R] < α, the clipped Kelly-style bet eventually stabilizes at a
strictly positive value (the running mean converges to µ, so κj → clip((α − µ)/(α(1 − α)), 0, 0.5) > 0), giving
the wealth process a strictly positive expected log-drift; by the law of large numbers the wealth grows to
infinity almost surely, so the test certifies every fixed threshold with true risk below α as n → ∞, and hence
(asymptotically) every threshold the Bernstein UCB certifies. We emphasize that we make no deterministic
finite-sample claim, and no claim that the betting test’s growth rate matches the empirical-Bernstein rate.
Empirically the containment held without exception at every tested α: across all 716 configurations and
five split seeds at α ∈ {0.05, 0.10, 0.15, 0.20} (3,580 paired evaluations) and across the α-relaxation grid at
α ∈ {0.25, 0.30, 0.40} (179 score-configurations each), none was certified by Bernstein but not by e-CRC.


                                                       18
E.4   Proof of Proposition 3: Sharpened Two-Sided Abstention Floor

The lower-bound half of Proposition 3 is proved here; attainability, the extremal-law reachability condition,
the degeneracy of the distribution-free minimax, and the two-gap decomposition of Remark 4 are proved in
§N.


Proof. Population statement (exact). Let ϕ(X) = P(emit | X) ∈ [0, 1] and p = E[ϕ], and write M =
ess sup R ≤ 1. Decompose µ = E[Rϕ] + E[R(1 − ϕ)]. Validity gives E[Rϕ] ≤ α E[ϕ] = αp, and R ≤ M
pointwise gives E[R(1 − ϕ)] ≤ M (1 − p). Hence µ ≤ αp + M (1 − p), giving p ≤ (M − µ)/(M − α), hence
abstention = 1 − p ≥ (µ − α)/(M − α). The proof uses only validity and R ≤ M , so it holds for arbitrary
(even R-measurable) rules. Since M ≤ 1, (µ − α)/(M − α) ≥ (µ − α)/(1 − α), and the M = 1 instance is the
conservative floor tabulated in the main text. When µ, M are known the bound is exact.
Plug-in version (δ/2 + δ/2 split). With µ̂ (and an audited M ) estimated from n held-out points, split the
failure budget: suppose the risk guarantee holds withpprobability ≥ 1 − δ/2, and apply a one-sided Hoeffding
bound at level δ/2: P(µ < µ̂ − ε) ≤ δ/2 with ε = log(2/δ)/(2n). On the intersection event (probability
≥ 1 − δ), substituting µ ≥ µ̂ − ε gives

                                                      µ̂ − α     ε
                                      abstention ≥           −      .
                                                      M −α     M −α

The correction is ε/(M − α), not ε. Numerically, with n = 1000, δ = 0.1, M = 1: ε ≈ 0.0387, and at α = 0.1
the correction is ε/(1 − α) ≈ 0.043.

E.5   Proof of Proposition 6: Fusion Preserves CRC Guarantee

Proof. The fused score s̃ is fixed once the data used to train g is observed. Conditional on s̃, the values
s̃(xi ) on the CRC calibration set are a deterministic function of (xi , yi ), so the scored calibration sample
retains its i.i.d. structure. CRC threshold selection via any UCB then provides a valid guarantee, regardless
of how s̃ was constructed. We emphasize that the guarantee requires g to be trained on data disjoint from
the CRC calibration set; our implementation fits the fusion weights on a held-out slice of the training split,
disjoint from the CRC calibration set. Reusing the same data for both steps would break the distributional
argument (Vovk et al., 2005), and we make no validity claim in that regime.

E.6   Theorem S2: ACI Effective-Risk Identity

Theorem E.2 (ACI effective-risk identity). Under the implemented update λt = λt−1 + γ(α − eff t ) with
eff t = rt · I{emitt } ∈ [0, 1] and fixed γ > 0, if the clamp of λt to [λmin , λmax ] never binds through time T ,
then
                                          T
                                       1X                λT − λ0
                                             eff t = α −         ,       so
                                       T t=1               γT
                                              T
                                         1X                λmax − λmin
                                               eff t − α ≤             .
                                         T t=1                 γT


                                                                         PT                        PT
Proof. Summing the update over t = 1, . . . , T telescopes: λT − λ0 = γ t=1 (α − eff t ) = γT α − γ t=1 eff t .
Rearranging gives the identity; the bound follows from λT , λ0 ∈ [λmin , λmax ].


This is a conditional algebraic identity about the effective risk (abstentions counted as zero risk), not a
guarantee on the risk among emitted predictions; when the clamp binds, even the identity fails. See §I for
the empirical consequences.


                                                       19
F     Cost-Sensitive Framework

The optimal abstention policy depends on the relative cost of errors vs. abstentions. Let cerror denote the
cost of emitting an incorrect prediction and cabstain the cost of abstaining. The expected utility is:

                                    U = − cerror · P(error | emit) · P(emit)
                                          − cabstain · P(abstain).

For a risk-controlling selector with conditional risk α, the optimal target is α∗ = cabstain /cerror . When
abstention is cheap (medical NER), use stricter α; when costly (customer-facing QA), looser α is preferred.

G     Implementation Details

Inference configuration. All models are served using vLLM (Kwon et al., 2023) v0.7+ on a sin-
gle NVIDIA A100-80GB GPU with gpu_memory_utilization=0.90. Greedy decoding uses T = 0 with
max_tokens=512. Sampling uses T = 0.7 with K = 10 samples per input. The 72B model uses AWQ 4-bit
quantization.

Prompt templates. We use task-specific 3-shot prompt templates. For NER: entity schema plus three
annotated examples. For QA: context-question-answer triples. For MMLU: question, four choices, three
demonstrations. For JSON: document, target schema, three examples.

CRC hyperparameters. Fixed grid of m = 200 thresholds, evenly spaced on [0, 1] (all scores are normal-
ized to [0, 1]); candidates restricted to emit sets with nλ ≥ 20; selection by the descending fixed-sequence scan
with early stopping (Algorithms 1 and 3). Confidence level δ = 0.1. For e-CRC: Kelly-style bets clipped to
[0, 0.5] with κ1 = 0; e-value = minimum over 22 pre-registered orderings (score-descending, score-ascending,
20 permutations from a per-configuration seeded generator consumed in scan order). Split seed 42 for the
60/40 split in headline results; multi-seed robustness (split seeds 42–46) is reported in §J.

Computational cost. Greedy inference for all 8 datasets: 45–90 min per model. Sampling (K = 10):
3–5× longer. Score computation: < 5 min per model (CPU). Full pipeline: < 60 min on single CPU.

H     Additional Experimental Results

H.1    Impossibility Bound Across Model Scales

H.2    Miscalibration Analysis

H.3    CRC Validity Across Risk Levels

H.4    Cross-Task Controllability

We define controllability C(α) = 1 − abstention at α. At α = 0.10 with Qwen2.5-3B: JSON achieves
C = 0.996, CLS 0.366, QA 0.183, NER 0.141. The strong correlation with base risk confirms that CRC
cannot compensate for weak models.

H.5    Baselines Comparison

H.6    Data Efficiency

Variance-aware bounds are substantially more data-efficient. We swept calibration fractions
{10%, 25%, 40%, 55%, 70%} of each dataset over three split seeds (42–44), re-running the full 716-
configuration grid at each fraction. Mean certification rates (Hoeffding / Bernstein / e-CRC): 1.1/1.9/4.2%
at 10% (pooled counts 24/40/90 of 2,148); 4.1/5.5/8.0% at 25% (87/119/172); 6.1/8.3/10.5% at 40%
(132/179/225); 7.2/9.8/11.4% at 55% (154/211/244); 7.5/10.5/11.9% at 70% (162/225/255). e-CRC’s


                                                       20
                              Dataset     Task     Model      µ       LB    Cert?
                                                   3B       0.42   35.6%      ✗
                                                   7B       0.33   25.6%      ✗
                              CoNLL       NER
                                                   14B      0.26   17.8%      ✗
                                                   72B      0.24   15.6%      ✗
                                                   3B       0.55   50.0%      ✗
                                                   7B       0.45   38.9%      ✗
                              TQA         QA
                                                   14B      0.34   26.7%      ✗
                                                   72B      0.27   18.9%      ✗
                                                   3B       0.84   82.2%      ✗
                                                   7B       0.81   78.9%      ✗
                              NQ Open     QA
                                                   14B      0.75   72.2%      ✗
                                                   72B      0.70   66.7%      ✗
                                                   3B       0.53   47.8%      ✗
                                                   7B       0.47   41.1%      ✗
                              MMLU-S      CLS
                                                   14B      0.38   31.1%      ✗
                                                   72B      0.28   20.0%      ✗
                                                   3B       0.35   27.8%      ✗
                                                   7B       0.29   21.1%      ✗
                              MMLU-H      CLS
                                                   14B      0.22   13.3%      ✗
                                                   72B      0.17    7.8%      ✗
                                                   3B       0.06    0.0%      ✓
                                                   7B       0.11    1.1%      ✓
                              JSON        JSON
                                                   14B      0.00    0.0%      ✓
                                                   72B      0.00    0.0%      ✓

Table H.1: Minimum abstention lower bound (LB = max{0, (µ − α)/(1 − α)}) vs. certification across model
scales at α = 0.10. µ values are from the original run; Cert? = whether any (score, bound) pair certifies at
α = 0.10. The 72B model’s recomputed grid covers CoNLL, Few-NERD, WNUT, and TriviaQA only, so its
NQ/MMLU/JSON rows reflect the original run. When µ ≫ α, Proposition 3 of the main text implies any
distribution-free certificate must abstain heavily; in our experiments, these settings do not certify. As scale
increases, µ decreases across NER/QA/CLS yet remains above α even at 72B. Only JSON (µ ≈ 0) certifies
at all scales. MMLU-Hum. at 72B (µ = 0.17) nears the certification frontier.


                                Dataset   Task     ECE ↓    Confidence     Risk
                                CoNLL     NER       0.237          0.881   0.356
                                FNERD     NER       0.418          0.878   0.540
                                WNUT      NER       0.332          0.850   0.480
                                TQA       QA        0.270          0.809   0.441
                                NQ        QA        0.611          0.806   0.804
                                STEM      CLS       0.343          0.824   0.516
                                Hum.      CLS       0.139          0.737   0.333
                                JSON      JSON      0.048          0.967   0.033

Table H.2: LLM miscalibration on structured generation tasks. High ECE values show that model confidence
is a poor proxy for correctness, motivating formal risk control.


relative advantage over Bernstein is largest in the data-scarce regime (+125% at 10% calibration, where
e-CRC also certifies 3.75× Hoeffding) and narrows monotonically to +13% at 70%; e-CRC at 25% calibration
already exceeds Hoeffding at 70%. Pooling caveat: the three seeds share the evaluation pool via different
splits, so fraction-level comparisons indicate aggregate tendency rather than independent replications. The
10% row is summarized in Table 2 of the main text.


                                                      21
                                            NER                             QA                       CLS             JSON
         Model         α      CoNLL        FNERD        WNUT          TQA         NQ        STEM           Hum.      JSON
                       0.05    –/1.00      –/1.00       –/1.00     –/1.00        –/1.00   1.00/0.99† 0.00/0.97      0.00/0.00
         gemma3-4b     0.10    –/1.00      –/1.00       –/1.00     –/1.00        –/1.00   1.00/0.99† 0.33/0.96†     0.00/0.00
                       0.15    –/1.00      –/1.00       –/1.00    0.00/0.98      –/1.00   1.00/0.99† 0.33/0.96†     0.00/0.00
                       0.20    –/1.00      –/1.00       –/1.00    0.00/0.97      –/1.00   1.00/0.99† 0.33/0.96†     0.00/0.00
                       0.05   0.01/1.00    –/1.00       –/1.00    0.00/0.99      –/1.00     –/1.00         –/1.00   0.00/0.00
                       0.10   0.07/0.99    –/1.00       –/1.00    0.00/0.99      –/1.00     –/1.00         –/1.00   0.00/0.00
         qwen2.5-14b
                       0.15   0.07/0.98    –/1.00       –/1.00    0.12/0.35      –/1.00     –/1.00         –/1.00   0.00/0.00
                       0.20   0.15/0.97    –/1.00       –/1.00    0.16/0.27      –/1.00     –/1.00         –/1.00   0.00/0.00
                       0.05    –/1.00      –/1.00       –/1.00     –/1.00        –/1.00     –/1.00         –/1.00   0.05/0.28
                       0.10   0.08/0.93    –/1.00       –/1.00     –/1.00        –/1.00     –/1.00         –/1.00   0.08/0.00
         qwen2.5-3b
                       0.15    –/1.00      –/1.00       –/1.00     –/1.00        –/1.00     –/1.00         –/1.00   0.08/0.00
                       0.20   0.12/0.92    –/1.00       –/1.00    0.18/0.64      –/1.00     –/1.00         –/1.00   0.08/0.00
                       0.05    –/1.00      –/1.00       –/1.00    0.00/0.99      –/1.00     –/1.00       –/1.00     0.04/0.30
                       0.10    –/1.00      –/1.00       –/1.00    0.00/0.99      –/1.00     –/1.00       –/1.00     0.08/0.17
         qwen2.5-7b
                       0.15    –/1.00      –/1.00       –/1.00    0.00/0.99      –/1.00     –/1.00       –/1.00     0.12/0.00
                       0.20    –/1.00      –/1.00       –/1.00    0.16/0.49      –/1.00     –/1.00     0.19/0.90    0.12/0.00
                      0.05 0.09/0.82†     0.20/0.92†   0.15/0.72† 0.05/0.63    0.20/1.00† 0.09/0.93† 0.07/0.62†     0.00/0.00
                                     †
         ministral-8b 0.10 0.13/0.69†     0.20/0.92†   0.15/0.72† 0.10/0.52    0.20/1.00† 0.19/0.90† 0.19/0.40†     0.00/0.00
                      0.15 0.16/0.58      0.20/0.92†   0.19/0.60† 0.15/0.37†   0.37/0.91† 0.19/0.90† 0.21/0.34†     0.00/0.00
                      0.20 0.13/0.63      0.28/0.86†   0.22/0.51† 0.10/0.52    0.37/0.91† 0.19/0.90 0.13/0.53       0.00/0.00


Table H.3: CRC risk control across α levels (best score per dataset; original-run values). Format: test risk /
abstention rate. – indicates an empty emit set (full abstention); such degenerate settings are not counted as
“certified” in our aggregate rates. †: violation on test set. The 72B model is omitted (greedy-only scores; no
per-cell sampling grid).

                                Method                           Risk ↓     Abstain ↓     Viol. % ↓
                                Always Answer                     0.434           0.000      90.0%
                                Entropy Thr.                      0.021           0.868      12.5%
                                TM Thr. (no guar.)                0.022           0.869       7.5%
                                SC Thr. (no guar.)                0.019           0.846       7.5%
                                CRC (Ours, guaranteed)           0.009           0.075       0.0%

Table H.4: Aggregate comparison at α = 0.10 (averaged over the five sampling-based models, eight datasets;
the 72B model is greedy-only). Threshold methods tune threshold on calibration set without formal guaran-
tees. CRC (guaranteed) reports only formally certified configurations.


I     Cross-Dataset ACI Transfer

I.1   ACI Experimental Setup

For the distribution shift experiments:

       • Temporal shift: Split by index order (first 60%/last 40%). CoNLL-2003 articles are ordered by
         publication date; TriviaQA by source document; MMLU by subject cluster. Index order captures
         topic drift within corpora.

       • Domain shift: Calibrate on MMLU-STEM (400), test on MMLU-Humanities (400).

       • Severity sweep: Oversample high-risk examples (R > median(R)) by factors 1.0–3.0×.

       • Cross-dataset:    CoNLL→WNUT         (newswire→social      media),                                    CoNLL→FewNERD
         (newswire→Wikipedia), TriviaQA→NQ (trivia→Google queries).

ACI uses γ = 0.01 with initial threshold from static CRC.


                                                                 22
                          Transfer     Model µtgt Stat. R̂ ACI R̂ ACI abst. Stat. ACI
                                       3B     0.53     0.52   0.53       0.01 ✗     ✗
                                       4B     0.49     0.00   0.48       0.03 ✓∗    ✗
                          CoNLL        7B     0.50     0.46   0.49       0.04 ✗     ✗
                          →WNUT        8B     0.44     0.19   0.14       0.75 ✗     ✗
                                       14B    0.45     0.37   0.43       0.10 ✗     ✗
                                       72B    0.40     0.67   0.00       1.00 ✗     ✓∗
                                   3B         0.63     0.68   0.64       0.03 ✗     ✗
                                   4B         0.55     0.00   0.54       0.03 ✓∗    ✗
                          CoNLL    7B         0.47     0.34   0.44       0.33 ✗     ✗
                          →FewNERD 8B         0.54     0.27   0.19       0.92 ✗     ✗
                                   14B        0.51     0.54   0.51       0.05 ✗     ✗
                                   72B        0.43     1.00   0.00       1.00 ✗     ✓∗
                                       3B     0.84     0.56   0.77       0.51   ✗    ✗
                          TQA          7B     0.81     0.52   0.79       0.17   ✗    ✗
                          →NQ          8B     0.79     0.39   0.34       0.91   ✗    ✗
                                       14B    0.75     0.44   0.73       0.08   ✗    ✗

Table I.1: Cross-dataset ACI transfer at α = 0.10 (γ = 0.01; R̂ = risk among emitted outputs; values
rounded to two decimals). Every target has base risk µtgt > α. Static CRC violates on 14/16 runs and ACI
also violates on 14/16; the exceptions (∗ ) all correspond to (near-)total abstention, i.e. (almost) nothing is
emitted. Models: 3B/7B/14B/72B = Qwen2.5, 4B = Gemma-3, 8B = Ministral. Gemma-3-4B TQA→NQ
is skipped (no valid target pairs) and 72B TQA→NQ lacks target data.


Sensitivity to the ACI step size γ. We swept γ ∈ {0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1} across all
16 transfer runs. Under the emitted-risk criterion the violation count is identical at every γ: 14/16. Under
the effective-risk criterion (emitted risk mass over all streamed examples, abstentions counted as zero risk),
violations range from 9/16 (γ ≤ 0.002) to 12/16 (γ = 0.1), while mean abstention falls from 59% (γ = 0.001)
to 26% (γ = 0.1). Conclusions are therefore not sensitive to γ: no step size restores the emitted-risk target,
because every transfer lands in the infeasible regime of Proposition 3 of the main text (per-model target-
domain base risks: CoNLL→WNUT 0.40–0.53, CoNLL→FewNERD 0.43–0.63, TQA→NQ 0.75–0.84; per-
transfer static violation rates 5/6, 5/6, and 4/4). Mechanically, the telescoping identity of Theorem E.2
pins the long-run effective risk near α whenever the threshold clamp does not bind, which makes risk-
among-emitted converge to roughly α divided by the emit rate, a quantity above α whenever abstention is
nonzero; on hard transfers ACI therefore trades abstention for effective-risk control rather than restoring
the per-emission guarantee, and on runs that saturate the clamp even the effective-risk identity no longer
applies.


J   Multi-Seed Robustness and Statistical Significance

To assess whether the certification ordering is an artifact of the seed-42 split, we reran the full 716-
configuration grid under five split seeds (42–46). Certified counts are stable across seeds: Hoeffding
51/52/54/53/51, Bernstein 72/73/75/70/71, e-CRC 80/83/83/82/81. Certified-set violations per seed are
0/0/0 (seed 42), 0/0/0 (43), 1/1/1 (44), 0/0/0 (45), 0/0/0 (46) for Hoeffding/Bernstein/e-CRC respectively.

Paired significance analysis. We pooled the 5 × 716 = 3,580 paired configuration observations and
applied McNemar’s exact test to each pair of methods (Table J.1).
The headline finding is that zero configurations are certified by Hoeffding but not Bernstein, and zero by
Bernstein but not e-CRC, across all 3,580 paired observations at α ∈ {0.05, 0.10, 0.15, 0.20}: at strict targets
the hierarchy holds without a single reversal. At relaxed targets (α ≥ 0.25) the Hoeffding–Bernstein ordering
does reverse (Section 3.3); Bernstein-not-e-CRC remains zero at every tested α. Pooling caveat. Because
the five seeds share the evaluation pool via different splits, the pooled p-values indicate aggregate consistency,


                                                       23
                            Pair (A vs B)            Both A-only B-only        p-value
                            Hoeffding vs Bernstein    261       0     100 1.6 × 10−30
                            Bernstein vs e-CRC        361       0      48 7.1 × 10−15
                            Hoeffding vs e-CRC        261       0     148 5.6 × 10−45

Table J.1: McNemar exact test on pooled paired observations (5 × 716 = 3,580 per pair). Columns: both
certify / A-only / B-only / exact two-sided p.


not independent replications in the classical sense. The zero-reversal count is therefore the primary evidence;
the p-values reinforce but do not replace it.

Pooled violation rates. Across the five seeds, certified-set violation rates with Clopper–Pearson
95% confidence intervals are: Hoeffding 1/261 (0.38%, CI [0.010%, 2.12%]), Bernstein 1/361 (0.28%, CI
[0.007%, 1.53%]), and e-CRC 1/409 (0.24%, CI [0.006%, 1.35%]); all upper limits are far below the δ = 0.10
tolerance. All three pooled violations are the same configuration: Ministral-8B, CoNLL, Self-Consistency,
α = 0.2, seed 44. For the Ministral-8B model specifically, pooled certified-set violations are 1/74 (Hoeffd-
ing), 1/100 (Bernstein), and 1/111 (e-CRC), with Clopper–Pearson 95% upper limits 7.3%, 5.4%, and 4.9%;
Ministral is not an outlier beyond that single config.

K    Threats to Validity

We report all 716 configurations; none excluded post hoc. Thresholds λ∗ determined entirely on calibration
(Algorithm 1); no hyperparameters tuned on test. “Guaranteed” means R̂n+ (λ∗ ) ≤ α on calibration, where
R̂n+ (λ) denotes the upper confidence limit for the emit-set risk at λ computed from the n calibration points
(the Hoeffding or Bernstein UCB, or the betting certificate’s implied bound), implying E[R(λ∗ )] ≤ α with
probability ≥ 1 − δ for i.i.d. calibration data. We fix δ = 0.1, so CRC guarantees are probabilistic: rare
test-set violations can occur even for certified configurations. Empirically, violations are near-zero among
certified sets, suggesting the bounds are conservative in our settings. Threshold selection uses a pre-registered
descending fixed-sequence scan with early stopping, so no Bonferroni correction is needed and no risk-
monotonicity assumption is invoked (Lemma E.1) (Angelopoulos et al., 2025); cross-bound comparisons
are structural (nested sets at α ≤ 0.20), complemented by the McNemar analysis of §J. Two resampling
analyses quantify the stability of the certified counts. (i) Split-level re-randomization: recomputing the full
716-configuration grid under B = 200 fresh 60/40 calibration/test splits (seeds 1001–1200) gives mean
certified counts [95% percentile intervals] of 53.1 [51, 56] for Hoeffding, 72.4 [68, 75] for Bernstein, and 82.4
[79, 86] for e-CRC. (ii) Config-level outcome bootstrap: resampling the 716 seed-42 configuration outcomes
10,000 times gives 51 [38, 65], 72 [56, 88], and 80 [64, 96]. The two procedures answer different questions: (i)
captures split-to-split variability of the pipeline, (ii) the sampling variability of the configuration population;
the seed-42 point estimates (51/72/80) are consistent with both.

L   Limitations and Future Work

Limitations. Static guarantees are stated for i.i.d. calibration data; under shift they no longer apply, and
ACI provides only the conditional effective-risk identity of Theorem E.2, not finite-sample control. Sampling-
based scores require K forward passes. Score fusion requires a disjoint split, reducing the effective calibration
size. The MMLU classification datasets are small (n = 400 each); QA is evaluated on only two datasets, of
which NQ Open is an outlier in base risk; the 72B model is evaluated on only two greedy-decoding scores.
JSON-Extract uses template-based extraction tasks, and its near-ceiling certification rates may partly reflect
template regularity. ACI conclusions are limited to the tested step-size range γ ∈ [0.001, 0.1] (7 values).
Evaluation spans 3B–72B; larger models (175B+) or closed-source APIs would further test generalizability.

Future work. Learned scores optimized for risk–coverage; finite-sample ACI via e-processes; multi-task
CRC with shared calibration; integration with constrained decoding; evaluation on 70B+ models.


                                                        24
                                Dataset          Task         Size   Domain
                                CoNLL-2003       NER         3,453   News
                                Few-NERD         NER         2,000   Wikipedia
                                WNUT-17          NER         1,287   Social media
                                TriviaQA         QA          1,000   Trivia
                                NQ Open          QA          3,610   Wikipedia
                                MMLU-STEM        CLS           400   STEM
                                MMLU-Hum.        CLS           400   Humanities
                                JSON-Extract     JSON          600   Structured

                                Table M.1: Datasets used in our evaluation.


M    Additional Baselines and Failure Analysis

Comparability to CP-Sets and conformal factuality. CP-Sets (Quach et al., 2024) focus on set-
valued prediction (returning a set of candidate labels/answers) with coverage guarantees, whereas we certify
single schema-validated structured outputs under task losses such as entity-level F1 and exact match. Bring-
ing CP-Sets into our setting would require (i) a method to generate and score sets of structured candidates
(e.g., multiple JSON/NER outputs), and (ii) a coverage definition tied to a structured distance (e.g., edit
distance over entity sets). Conformal factuality (Mohri & Hashimoto, 2024) certifies factual claims by com-
posing retrieval and entailment-style checks; this is complementary to our focus on certifying format-valid
structured generations with task-specific losses, and could be combined with our approach as an additional
nonconformity signal.

Selective prediction baselines. Learning-based rejection (e.g., SelectiveNet (Geifman & El-Yaniv, 2019))
can yield strong empirical coverage–risk tradeoffs, but typically does not provide distribution-free guarantees
without an additional conformalization step; Lee et al. (2024) is a case in point of that added step, learning
a rejection function on top of a frozen LLM that achieves a distribution-free FDR-control guarantee via a
semi-supervised conformal procedure. Our CRC framework can wrap any score (including learned rejectors
or retrieval-based confidence signals), provided exchangeability holds; thus CRC should be viewed as a
guarantee layer rather than a competing uncertainty method.

Why ACI can still violate under shift. ACI (Gibbs & Candès, 2021) adapts thresholds online using
realized feedback. While this helps under gradual shift, it cannot bypass feasibility: when the base risk µ is
far above the target α, any distribution-free method must abstain heavily (Proposition 3 of the main text).
In our cross-dataset transfers, the remaining ACI violations tend to occur in such high-µ regimes or when
feedback is delayed/noisy, which limits adaptation. Practically, we recommend using the feasibility check (µ
vs. α) before deployment and treating ACI as a monitoring-and-adjustment tool when feedback is available.

Score brittleness. Nonconformity scores can in principle be sensitive to tokenizer/model family and
quantization artifacts (e.g., AWQ). In our recomputed runs, certified-set violations were too rare to sup-
port any pattern-level claim (a single pooled configuration across five seeds; §J), so we retain this as a
deployment consideration rather than an empirical finding: use score functions that are stable across decod-
ing/implementation variations and validate guarantees per deployment stack.

Datasets.    Table M.1 summarizes the eight evaluation datasets (Section 3.1).


N    Sharpened Abstention Floor: Attainability, Extremal Law, and Decomposition

This section supplies the attainability, extremal-law, minimax, and decomposition results supporting Propo-
sition 3 and Remark 4 of the main text; the lower bound was proved in §E. Throughout, S ∈ [0, 1] is the
observable score, R ∈ [0, 1] the risk with µ = E[R] and M = ess sup R; a selective rule is ϕ : X → [0, 1] with


                                                        25
                                                        Struct. Risk Lower Bound Shift
                        Line of work                     LLM abst. bound hier. adapt.
                        CP sets                           ✗       ✗       ✗         ✗        ✗
                        CRC / LTT risk control            ✗       ✓       ✗         ✗        ✗
                        Selective pred. / reject opt.     ✗       ✓       ✓         ✗        ✗
                        ACI                               ✗       ✗       ✗         ✗        ✓
                        Betting / e-values seq.           ✗       ✗       ✗         ✗        ✗
                        This work                         ✓       ✓       ✓        ✓         ✓

                Table M.2: Positioning relative to closely related lines of work (Section 1).


coverage c(ϕ) = E[ϕ], emitted risk er(ϕ) = E[Rϕ]/E[ϕ], abstention a(ϕ) = 1 − c(ϕ), and abstention target
ADF (P ; α) = inf{a(ϕ) : ϕ is σ(S)-measurable and α-valid}. Randomized thresholds split atoms of S.

Relation to prior work. The per-fixed-law achievability below—the optimal selective rule thresholds
the calibrated conditional risk, and the risk–coverage curve has a rearrangement lower envelope—is classi-
cal known-distribution reject-option theory: Chow (1970) (threshold on the posterior), El-Yaniv & Wiener
(2010) (risk–coverage), and especially Franc et al. (2023) (bounded-abstention and bounded-improvement
optima). We specialize these to a scalar score. Our contribution is the distribution-free framing over mean-
constrained laws: the ess sup sharpening, the extremal-law condition, the minimax degeneracy, and the gap
decomposition—not the achievability, which we do not claim as new.
Proposition N.1 (Attainability, extremal law, and minimax degeneracy). Fix µ > α and M ≤ 1. (i)
Attainability. There is a law P ⋆ of (S, R) with E[R] = µ, ess sup R = M , and a randomized score-threshold
rule ϕ⋆ (score-measurable) that is α-valid with a(ϕ⋆ ) = (µ − α)/(M − α). Hence (µ − α)/(M − α) is the
largest constant lower-bounding abstention across all mean-µ, ess sup-M laws, and the outer infimum is
attained (a minimum). (ii) Extremal condition. For a general law, the floor is attained by some α-valid rule
iff P(R = M ) ≥ (µ − α)/(M − α). (iii) Minimax degeneracy. inf P : E[R]=µ ADF (P ; α) = (µ − α)/(M − α)
while supP : E[R]=µ ADF (P ; α) = 1 (attained by any law with S ⊥ R). There is no minimax saddle over the
unrestricted mean-µ class; the floor is a tight feasibility frontier, not a saddle value.

Proof. (i) Take R ∈ {0, M } with P(R = M ) = µ/M (mean µ; µ ≤ M ) and a perfectly ordering score
S = ⊮{R = 0}. Emit every S = 1 point and each S = 0 point with probability q: ϕ⋆ = ⊮{S = 1}+q ⊮{S = 0}.
Then E[Rϕ⋆ ] = qµ and c(ϕ⋆ ) = (1 − µ/M ) + qµ/M ; choosing q = α(M − µ)/(µ(M − α)) ∈ [0, 1] makes
er(ϕ⋆ ) = α and a(ϕ⋆ ) = (µ/M )(1 − q) = (µ − α)/(M − α) (verified numerically for M ∈ {0.6, 0.8, 1}). The
rule is σ(S)-measurable; the randomization is essential since S is two-valued. The Proposition 3 lower bound
gives “≥”, so the value is exactly the floor and is attained. (ii) Sufficiency: with x = (µ − α)/(M − α), if
P(R = M ) ≥ x, abstain on a measurable subset of {R = M } of mass x and emit the rest; then emitted risk
= (µ − M x)/(1 − x) = α and a = x. Necessity: equality throughout the Proposition 3 chain forces R = M
a.s. on the abstain set, so a mass-x abstain set lies in {R = M }, whence P(R = M ) ≥ x. (iii) The infimum is
(i). For the supremum, if S ⊥ R then E[R | S ≥ λ] = µ > α for every non-empty emit set, so validity forces
c = 0, i.e. ADF = 1; and ADF ≤ 1 always.

Proposition N.2 (Two-gap decomposition (Remark 4)). For any law of (S, R) with µ > α, let g(s) =
E[R | S =R s] and let qu be the quantile function of R; by the Hardy–Littlewood rearrangement inequality,
            c
ρ† (c) = 1c 0 qu du is the pointwise-minimal risk–coverage curve. With A† (R; α) = 1 − sup{c : ρ† (c) ≤ α},

                                            µ−α  h          i 
                            ADF (P ; α) =       + A† − Mµ−α
                                                              + ADF − A† ,
                                                                        
                                            M −α |       −α
                                                      {z    }  |   {z   }
                                                          ∆disp (R) ≥ 0       ∆ord (S) ≥ 0


where ∆disp = 0 iff P(R = M ) ≥ (µ − α)/(M − α) and ∆ord = 0 iff the optimal emit set {g(S) ≤ τ } coincides
(P -a.s.) with a bottom-risk set. Among σ(S)-measurable α-valid rules, abstention is minimized by a threshold
on the calibrated score g(S).


                                                         26
Proof. By the tower property E[Rϕ] = E[g(S)ϕ] for σ(S)-measurable ϕ, so maximizing c = E[ϕ] subject
to E[(g(S) − α)ϕ] ≤ 0, 0 ≤ ϕ ≤ 1, is a fractional-knapsack (Neyman–Pearson) problem whose optimum
thresholds g(S) with the constraint binding, giving ADF = 1−E[ϕ∗ ]. The decomposition telescopes. ∆ord ≥ 0:
ADF optimizes over σ(S) ⊆ σ(X, R) and ρ† is the pointwise-minimal risk–coverage curve, so ADF ≥ A† , with
equality iff the S-optimal emit set is a bottom-R set. ∆disp ≥ 0: apply Proposition 3 to the oracle rule
(A† ≥ (µ − α)/(M − α)); the equality condition is Proposition N.1(ii). Computed checks: two-point {0, 1}
with µ = .5, α = .25 gives A† = 1/3 = floor (∆disp = 0); uniform R on [0, 1] gives A† = .5 > 1/3
(∆disp = 1/6); S ⊥ R gives ∆ord = 1 − A† .

Bridge to fusion. Calibrated fusion g = σ(w⊤ s + b) cannot change ∆disp (fixed by the risk marginal and
M ) and can only act on ∆ord by making g(S) a better monotone proxy for R; this links score quality to
certification in principle. Empirically the link is weak on our grid: a disjoint-split re-evaluation (§R) finds
fusion’s gain is on AUROC (ranking), not on certified-set size.

O    Certification Phase Diagram: Reversal Frontier and Pareto Necessity (Full Proofs)

Notation   as in Proposition 2: L = log(2/δ), wH (n) =             L/(2n), b(n) = 7L/(3(n − 1)), wB (n, σ̂ 2 ) =
                                                               p

  2σ̂ 2 L/n + b(n), A(n) = wH (n) − b(n), and c(n, δ) = 2L A(n)2 (valid when A(n) > 0; n ≥ 35 at δ = 0.1).
p                                                          n

The feasibility coupling is Bhatia–Davis: for risks in [0, 1], σ̂ 2 ≤ R̂(1 − R̂), with equality for 0/1 losses (QA
exact-match, CLS accuracy). The pairwise width comparison UB ≤ UH ⇐⇒ σ̂ 2 ≤ c(n, δ) is Proposition 2
and is known (Maurer & Pontil, 2009); the new content is the certification-level frontier and the Pareto struc-
ture. All numbers are from theory/verify_phasediagram.py (seed-42 grid, the paper’s own certification
code), output verify_phasediagram_out.json.
Proposition O.1 (Reversal frontier (Proposition 7(i))). Fix n, δ with A(n) > 0. A feasible emit set of size
n that Hoeffding certifies but empirical Bernstein does not (i.e. UH ≤ α < UB with 0p    ≤ σ̂ 2 ≤ R̂(1 − R̂))
exists iff (α − wH )(1 − α + wH ) > c(n, δ), equivalently α > α (n, δ) = wH (n) + 2 (1 − 1 − 4c(n, δ) ). For
                                                               ∗                  1

0/1 losses the Bhatia–Davis bound is an equality, so α∗ is the exact reversal boundary at R̂ = α − wH .

Proof. A reversal at mean R̂ needs (a) R̂ ≤ α − wH (Hoeffding certifies) and (b) R̂ + wB > α, i.e. σ̂ 2 >
  2
σcrit (R̂) := 2L
               n
                  (α−R̂−b)2 when α−R̂−b ≥ 0. Since wB increases in σ̂ 2 , the easiest witness sets σ̂ 2 at its feasible
maximum R̂(1 − R̂). So a reversal exists iff ∃ R̂ ∈ [0, α − wH ] with h(R̂) := R̂(1 − R̂) − 2L
                                                                                             n
                                                                                               (α − R̂ − b)2 > 0. On
[0, α − wH ] (with α − wH ≤ 2 ), h (R̂) = (1 − 2R̂) + L (α − R̂ − b) ≥ 0 (both terms ≥ 0, the second because at
                                1   ′                  n

the endpoint α − R̂ − b = A ≥ 0), so h is increasing and maximized at R̂∗ = α − wH , where α − R̂∗ − b = A
and σcrit
        2
           (R̂∗ ) = 2L
                     n
                       A2 = c. Thus h(R̂∗ ) > 0 ⇐⇒ R̂∗ (1 − R̂∗ ) > c ⇐⇒ (α − wH )(1 − α + wH ) > c; solving
R̂∗ (1 − R̂∗ ) = c on the branch R̂∗ ≤ 12 gives α > α∗ . For 0/1 losses no Bhatia–Davis slack is discarded, so
“if” becomes exact.

Two mechanisms and numerical confirmation. For n < 35 (A(n) ≤ 0 at δ = 0.1), wB ≥ wH for every
σ̂ 2 ≥ 0 (the additive b(n) alone exceeds wH ), so Bernstein is universally looser and reversals occur even
at σ̂ 2 < c; the frontier α∗ is claimed only in the A(n) > 0 regime. On the seed-42 grid (28,761 candidate
emit sets × 7 targets; 1,091 pointwise reversals): in the A > 0 regime, 0 of 947 reversals violate σ̂ 2 > c
and 0 occur below α∗ (n); the A ≤ 0 regime contributes 144 reversals, 27 of them with σ̂ 2 < c (the additive
mechanism). α∗ is smooth with minimum 0.169 at n = 88, rising to 0.20 (n=300), 0.23 (n=600), 0.32
(n=5000), → 21 as n → ∞; c(120) = 0.056, c(600) = 0.147 match Proposition 2. The Bhatia–Davis ratio
σ̂ 2 /[R̂(1− R̂)] has medians QA 1.00, CLS 1.00, NER 0.80, JSON 0.27, confirming that binary losses sit on the
frontier. Config-level reversals (Hoeffding certifies, Bernstein does not) first appear at α = 0.25 (H = 31 > B
= 30), consistent with α∗ being necessary but realized only where a real emit set attains R̂ ≈ α − wH with
near-maximal variance.
Proposition O.2 (Pareto necessity (Proposition 7(ii))). Over (n, R̂, σ̂ 2 , α) with α                      ∈
{0.05, . . . , 0.20, 0.25, 0.30, 0.40}: (i) no single bound dominates the other two; (ii) e-CRC statistically
subsumes empirical Bernstein (Maurer & Pontil, 2009; Waudby-Smith & Ramdas, 2024) (0 configurations


                                                          27
certified by Bernstein but not e-CRC); (iii) the best-of-three certified set equals ΛH ∪ Λe-CRC and strictly
dominates every single bound, so {Hoeffding, e-CRC} is minimal sufficient and Bernstein is a closed-form
convenience.

Proof (constructive, seed-42 grid). (i) H-only = 3 (e.g. Qwen2.5-3B/TriviaQA/self-consistency/α = 0.30:
selected emit set n = 222, R̂ = 0.216, binary EM so σ̂ 2 = 0.170 on the frontier, UH = 0.298 ≤ 0.30 <
UB = 0.316, and α∗ (222) = 0.188 < 0.30; betting also fails), and e-CRC-only = 10 (e.g. JSON at α = 0.05–
0.10, data-abundant and low-variance, where the one-sided log 2 threshold saving and the absent additive
term let betting certify while both UCBs miss). (ii) Verified B-not-e-CRC = 0 across the grid including
α ∈ {0.25, 0.30, 0.40}, hence ΛB ⊆ Λe-CRC and B-only = 0. (iii) Summed over the 7 targets, best-of-three
= 212 = best-of-{H, e-CRC}, while e-CRC-alone = 209 and H-alone = 181; both H and e-CRC are Pareto-
necessary.

A second-order growth-rate argument (Taylor expansion of log-wealth, not an exact boundary) explains
e-CRC’s data-scarce edge: empirically at 10% calibration, certifications are H = 7, B = 7, e-CRC = 19,
matching the regime where the log 2 saving and absent additive term dominate.

P    Hoeffding–Bentkus Domination (Analysis Remark)

This supports the Discussion remark that the additive-Bernstein reversal is an artifact and that the inverted
Learn-Then-Test p-value dominates Hoeffding unconditionally. This is an analysis remark, not a change
of method: the paper’s reported certificates remain Hoeffding, empirical Bernstein, and e-CRC,
with their zero-violation record (0/51, 0/72, 0/80 at seed 42) intact. The Hoeffding–Bentkus (HB)
certificate is not a new primitive: it is the standard LTT p-value (Angelopoulos et al., 2025), combining the
Chernoff–Hoeffding (KL) tail with the Bentkus binomial-tail bound (Bentkus, 2004); we claim no novelty
for it.
For H0 : µ ≥ α and observed mean R̂ < α, define pCH = exp(−n kl(R̂∥α)) (kl the binary relative entropy)
and pBent = e · P(Binom(n, α) ≤ ⌈nR̂⌉), and certify λ iff pHB := min(pCH , pBent ) ≤ δ. Both are nonincreasing
in R̂, so their rejection regions are nested lower intervals and the min is a valid level-δ p-value; validity of
the selected threshold follows from the same descending fixed-sequence argument as Lemma E.1.
Proposition P.1 (Unconditional     Hoeffding domination). For every n, σ̂ 2 , and α: if additive Hoeffding
certifies λ (i.e. R̂ + L/(2n) ≤ α), then HB certifies λ. There is no variance condition and no reversal.
                      p


Proof. Additive Hoeffding certifies iff α − R̂ ≥   L/(2n). Pinsker’s inequality kl(R̂∥α) ≥ 2(α − R̂)2 ≥
                                                 p

2 · L/(2n) = L/n gives pCH ≤ e−L = δ/2 < δ, so pHB ≤ pCH ≤ δ. The δ/2 slack comes from the two-sided
constant L = log(2/δ) used in the additive Hoeffding bound.

Validity versus tightness. Being valid but tighter, HB operates nearer the δ budget rather than the ad-
ditive bounds’ near-zero-violation regime. On the seed-42 strict grid it certifies 94 versus 51/72/80 with
ΛHB ⊇ ΛHoeff , ΛBern , Λe-CRC ; pooled over seeds 42–46 its certified-set violation rate is 6/479 = 1.25%
(Clopper–Pearson 95% upper 2.46% ≪ δ = 0.1), and an adversarial boundary Monte-Carlo (400,000 draws at
µ = α) gives worst-case false-certification 7.7% < δ. HB and empirical Bernstein are Pareto-incomparable in
general (a near-zero-variance corner with R̂ near α lets Bernstein certify where HB does not), but HB domi-
nates Bernstein on all binary-risk and all LLM emit sets in our grid. We report the additive/e-CRC certificates
in the main text to preserve the zero-violation narrative; HB is noted only as the unconditionally-Hoeffding-
dominating valid alternative under this validity-versus-tightness trade-off. Scripts: recompute/dirD_*.py.

Q    A Constructive Anytime-Valid Shift Monitor (Full Construction)

This section gives the construction, validity proofs, and numbers behind the constructive-counterpart sub-
section of the main text and Proposition 8. The machinery is known and we claim no novelty for it:
time-uniform confidence sequences (Howard et al., 2021), betting/e-processes (Waudby-Smith & Ramdas,


                                                      28
2024; Ramdas et al., 2023), and the closely related anytime-valid selective-risk methods A-RCPS (Xu et al.,
2024), Conformal Selective Acting (Khosravi & Huo, 2026), and anytime-valid CRC (Hultberg et al., 2026).
Our contribution is the demonstrated constructive dual of Proposition 3 on the paper’s own failed transfers,
plus the emit-only obstruction (Proposition 8).

Setup and filtration. At step t, nature reveals xt , the model produces ŷt and score st , we choose a
predictable threshold λt (Ft−1 -measurable), emit iff Et = ⊮{st ≥ λt }, and observe rt = R(ŷt , yt ) ∈ [0, 1].
With Gt = Ft−1 ∨ σ(xt , st ), the conditional emitted risk is qt = E[rt | Gt ]; we assume nothing about {qt }
(arbitrary, adversarial drift). Full feedback observes rt at every t (a verifier, or labels on abstained inputs
too); emit-only feedback observes rt only when Et = 1.
Theorem Q.1    P (Per-threshold anytime  confidence sequence). Fix λ and let It = {u ≤ t : su ≥ λ}, nt =
|It |, At = n1t u∈It ru , Mt = n1t u∈It qu . Under full feedback, with Ut = At + Bδ (nt )/nt and Bδ (n) =
                                   P

   (n/4 + ρ)(2 log(1/δ) + log((n/4 + ρ)/ρ)),
p


                                              P(∃t : Mt > Ut ) ≤ δ

for an arbitrary (non-exchangeable, adversarially drifting) risk process.


Proof. St = u∈It (ru − qu ) is a martingale with increments in [−1, 1], since ⊮{su ≥ λ} is Gu -measurable and
               P

E[ru − qu | Gu ] = 0. By Hoeffding’s lemma, Lt (η) = exp(ηSt − (η 2 /8)nt ) is a nonnegative supermartingale
with L0 = 1; mixing over η ∼ N (0, 1/ρ) and applying Ville’s inequality (Howard et al., 2021) gives P(∃t :
|St | ≥ Bδ (nt )) ≤ δ. The event Mt > Ut is −St > Bδ (nt ), whose probability is ≤ δ (lower tail of the symmetric
mixture).


The monitor SAVeR-FF maintains Ut (λ) over a predictable grid at Bonferroni level δ/G and emits at λt =
min{λ : Ut−1 (λ) ≤ α}; every emission then occurs at a threshold certified ≤ α anytime. Its abstention obeys
the floor of Proposition 3, and when a fixed λ∗ stays below α its emit rate → P(s ≥ λ∗ ): abstention tracks the
floor when the score stays informative under shift and saturates to 1 when the stream is genuinely infeasible.
Theorem Q.2 (Self-selected    supermartingale validity). Under emit-only feedback, the emitted-substream
betting process Wt = u≤t (1 + Eu κu (ru − α)) with predictable Eu and κu ∈ [0, 1/α] is, under H0 : qu ≤ α
                      Q
for every emitted u, a nonnegative Ft -supermartingale, so P(∃t : Wt ≥ 1/δ) ≤ δ.


Proof. E[Wt | Gu ] = Wt−1 (1 + Eu κu (qu − α)): on {Eu = 1}, qu − α ≤ 0 and κu ≥ 0 so the factor is ≤ 1;
on {Eu = 0} it is 1; nonnegativity from κu ≤ 1/α. The predictable multiplier Eu κu makes self-selection
harmless—abstained steps contribute factor 1 and no ru is needed there—so the feedback required coincides
with the feedback obtained.

Proposition Q.3 (Emit-only feedback obstruction (Proposition 8)). Under emit-only feedback and arbitrary
shift, any procedure guaranteeing P(∀t : At ≤ α) ≥ 1 − δ (δ < 1) that emits with positive probability can be
forced to violate.


Proof. The emit decision at t is Gt -measurable and cannot depend on rt . Let the adversary set rt = 1 on the
first step the procedure emits: then A = 1 > α, with probability equal to the procedure’s probability of ever
emitting. To keep the guarantee the procedure must emit nothing.


ACI updates on eff t = rt ⊮{emitt } (emit-only feedback), so it can learn a region’s risk only by emitting into
it; Proposition Q.3 shows this exploration cost is charged as violations under shift—a model-level reason,
complementing the feasibility-level Proposition 3, that ACI cannot restore the emitted target. The escape is
full feedback.


                                                       29
                                                                         (a) Feasibility floor                                                                        (b) Bound-ordering phase diagram


        min. required abstention (μ − α)/(1 − α)
                                                   1.0               α = 0.10                   JSON      WNUT                                                    Hoeffding




                                                                                                                       certified score-configs (of 179)
                                                                                                Hum.      STEM                                            60      emp. Bernstein
                                                                                                CoNLL     FNERD                                                   e-CRC
                                                   0.8                                          TQA       NQ
                                                                                                                                                          50




                                                                                                                                                                                            reversal α *
                                                   0.6                                                                                                    40

                                                                                                                                                          30
                                                   0.4
                                                                                                                                                          20
                                                   0.2
                                                                                                                                                          10           nested
                                                                                                                                                                      H⊆B⊆e

                                                   0.0                                                                                                     0
                                                         0.0   0.1              0.2       0.3       0.4       0.5                                              0.05   0.10   0.15    0.20   0.25           0.30   0.40
                                                                                risk target α                                                                                       risk target α



Figure R.1: The two headline results of the main text, visualized. (a) Minimum required abstention (µ −
α)/(1 − α) vs. risk target α, one curve per dataset at its measured base risk µ (main-text Table 1). A
curve reaches zero exactly at α = µ; every point to its left is provably infeasible without abstaining at least
that much (main-text Proposition 3). At the headline target α = 0.10 (dashed), seven of eight datasets
sit strictly above zero abstention, which is why strict-target certification is rare. (b) Number of certified
score-configurations (of 179) for each bound as α relaxes. Below α ≈ 0.20 (grey) the three certified sets
are strictly nested Λ∗Hoeff ⊆ Λ∗Bern ⊆ Λ∗e-CRC (main-text Proposition 2); past the reversal band (orange)
Hoeffding overtakes empirical Bernstein, the empirical signature of the closed-form frontier α∗ (n, δ) (main-
text Proposition 7).


R     Additional Analyses (Audited M , Disjoint-Split Fusion, Robustness)

This section supplies four supporting analyses recomputed from the cached per-example (score, risk) data
with the paper’s own certification library (no new model inference): the audited essential supremum M
behind Proposition 3, a disjoint-split re-evaluation of score fusion, the δ-sensitivity of the certified counts,
and per-task and multi-seed breakdowns of the phase diagram. Figure R.1 first visualizes the paper’s two
headline results.

R.1   Audited Essential Supremum

Proposition 3’s sharpened floor (µ − α)/(M − α) improves on the conservative (µ − α)/(1 − α) only when
M = ess sup R < 1. We audit M the way the proposition says it should be deployed (the empirical sample
maximum of the per-example risk, pooled over calibration and test, averaged over the five sampling-based
models). Table R.1 reports the result: on every NER/QA/CLS dataset the audited M = 1.00 exactly, because
a complete per-example miss (entity-F1 = 0, or a wrong exact-match/label) occurs in every model×dataset
cell (on 18–53% of examples). The sharpened floor therefore coincides numerically with the conservative
M =1 floor for all NER/QA/CLS rows, and moves no tabulated LB value in this paper. Only JSON field-
F1 has M < 1 (audited M̂ ≤ 0.33), but there µ < α already, so the floor is 0 under either formula. The
sharpening is a real, provable generalization (it would bind on losses whose per-example value cannot reach
1, e.g. macro-F1 , 1 − BLEU, 1 − ROUGE), but it does not tighten any number on our grid.

R.2   Disjoint-Split Score Fusion

The main-text fusion numbers (§3.7) are recomputed here under a protocol that respects Proposition 6’s
independence requirement, replacing an earlier in-sample estimate. Using a three-way disjoint split (the seed-
42 test set is byte-identical to the headline grid; the 60% calibration block is halved into a fusion-training
slice, on which the logistic-regression fusion weights are fit, and a CRC-calibration slice, on which thresholds
are selected by the paper’s own fixed-sequence scan), AUROC is read out-of-sample and individual-score
baselines are certified on the identical CRC-calibration/test split. Over 136 model×dataset×α rows (34
configurations averaged over α):


                                                                                                                  30
                             Dataset    Task        µ̄        M̂   floor gap @ α=0.1
                             CoNLL      NER     0.356      1.00               0.0 pp
                             FNERD      NER     0.540      1.00               0.0 pp
                             WNUT       NER     0.480      1.00               0.0 pp
                             TQA        QA      0.441      1.00               0.0 pp
                             NQ         QA      0.804      1.00               0.0 pp
                             STEM       CLS     0.516      1.00               0.0 pp
                             Hum.       CLS     0.333      1.00               0.0 pp
                             JSON       JSON    0.033     0.13∗              0.0 pp†

Table R.1: Audited M̂ = ess sup R per dataset (averaged over the five sampling-based models). “floor gap”
= (µ − α)/(M − α) − (µ − α)/(1 − α) at α = 0.10. ∗ JSON field-F1 audits to M̂ between 0.00 and 0.33 across
models. † For JSON µ < α, so both floors are 0. On all NER/QA/CLS datasets M̂ = 1.00, so the sharpened
and conservative floors coincide.

      • AUROC. Fusion improves on 23/34 configurations (68%; mean +0.004, median +0.006, max
        +0.062), with a worst-case loss of −0.154 (Qwen2.5-14B/MMLU-Humanities, where the small fusion-
        training slice overfits). This is roughly 7× smaller than the in-sample +0.026 previously reported.
      • Certification. Fused vs. best-individual certified counts on the same split are 0 vs. 7 (Hoeffding),
        0 vs. 8 (Bernstein), 2 vs. 13 (e-CRC). Fusion never certifies a configuration that no individual score
        already certifies (0 fused-only certifications at every bound); in the two e-CRC cases where both
        certify, fusion lowers test abstention by ≈ 1.9pp.

Caveat. The CRC-calibration slice here is half the headline calibration budget, since the released per-
example files contain no separate training pool; both arms are equally starved, so this is a conservative test,
not a proof that fusion cannot help at the full budget. It is, however, the disjointness-respecting estimate,
and it shows fusion’s benefit on this data is on ranking quality, not on certified-set size.

R.3   Sensitivity to the Confidence Level

Re-running the seed-42 grid at δ ∈ {0.05, 0.10, 0.20} gives certified counts (Hoeffding/Bernstein/e-CRC) of
48/64/74, 51/72/80 (paper), and 58/79/89. Two findings are worth stating. First, at δ = 0.20, e-CRC pro-
duces 3 violations of 89 certifications (3.4%, well within the 20% budget: Qwen2.5-3B/JSON/{token-margin,
NLL}/α=0.05 and Qwen2.5-72B/CoNLL/token-margin/α=0.20), positive evidence that the guarantee is not
vacuously conservative. Second, nesting Λ∗Hoeff ⊆ Λ∗Bern holds without exception at δ = 0.10 and 0.20, and fails
in exactly 1 of 2,148 method-pairs at δ = 0.05 (Ministral-8B/MMLU-Humanities/self-consistency/α=0.20),
consistent with Proposition 2’s δ-dependent finite-sample threshold (L = log(2/δ)). The paper’s “nested
without exception at α ≤ 0.20” claim is thus a δ = 0.10 statement.

R.4   Per-Task Certified Counts and Multi-Seed Reversal

Table R.2 breaks the seed-42 strict-target counts down by task (cells sum to the headline 51/72/80). Essen-
tially all strict-target certification comes from JSON alone (47 of 51 Hoeffding certifications); NER/QA/CLS
certify near-zero at α ≤ 0.10, exactly as the floor predicts.
The relaxed-target Hoeffding–Bernstein reversal is seed-stable across seeds 42–46. At α = 0.30, Hoeffding
> Bernstein at all five seeds (Hoeffding 42/42/42/41/43 vs. Bernstein 35/38/38/36/39); at α = 0.40, all
five (57/56/59/57/57 vs. 48/50/49/50/50); at α = 0.25, nearest the reversal onset, four of five seeds show
Hoeffding > Bernstein and one seed ties, consistent with the frontier’s n-dependence (Proposition 7). The
seed-42 relaxed counts reported in the main text (42, 57 Hoeffding) sit squarely inside these ranges.

Numerical demonstration. Code theory/saver.py, run_saver.py; results saver_results.json. On
the identical cross-dataset transfers of Table I.1 (best score, static-CRC warm start, δ = 0.1, ρ = 25), at
α = 0.10 (16 model×transfer runs): static CRC 14/16 violations, ACI (γ = 0.01) 14/16, SAVeR-FF (full


                                                         31
                              Task (n/α) α=0.05     α=0.10    α=0.15    α=0.20
                              NER (81)      0/0/0  0/0/0    0/2/2    2/2/2
                              QA (40)      0/0/0   0/0/0    0/1/1   1/1/1
                              CLS (36)      0/0/0  0/0/0    0/0/1    1/1/1
                              JSON (22)    0/9/12 9/17/19 18/19/20 20/20/21

Table R.2: Per-task certified counts at seed 42 (cells are Hoeffding/Bernstein/e-CRC). Column-summed
totals are 51/72/80.


feedback) 0/16 at mean abstention 1.00, since every transfer is infeasible (floors 0.33–0.83 by Proposition 3);
the emit-only betting monitor reproduces Proposition Q.3, paying an exploration cost and violating 14/16.
Non-vacuity on feasible streams: qwen2.5-14b/JSON at α = 0.10 emits 388/600 (65%) at risk 0.000 (0
violations); qwen2.5-14b/CoNLL at α = 0.40 emits 3338/3453 (97%) at risk 0.258; qwen2.5-72b/CoNLL
at α = 0.40 emits 3316/3453 (96%) at risk 0.242; ministral-8b/CoNLL→WNUT at α = 0.40 (floor 0.06)
emits 718 (abstention 0.44) at 0 violations. Abstention ≥ floor on all runs. A synthetic coverage check with
known drifting/adversarial qt (2000 reps, T = 1500) gives empirical miscoverage ≤ 0.011 ≪ δ (drift-up 0.003,
sinusoid 0.009, adversarial-burst 0.000, iid-mid 0.011), confirming Theorem Q.1. Limitation. The rigorous
guarantee uses the Hoeffding mixture (σ 2 = 1/4) and over-abstains on low-risk streams; a variance-adaptive
uniform boundary is a drop-in tightening we do not re-derive here to avoid an invalid guarantee.




                                                      32
