                                             Why Formal Monitors Fail: Attack Distribution
                                                               Entropy
                                            as a Coverage Bound for LTL-Based LLM Agent
                                                                Safety
                                                                                                              Ruiyang Zhang
                                                                                                    Ryonix Labs Inc. Flock.io
                                                                                                  Email: zhangruiyang36@gmail.com


                                           Abstract—Runtime safety monitors based on Linear Temporal                       safety: they are computationally cheap, formally interpretable,
                                        Logic (LTL) and finite automata (FSA) are increasingly deployed                    and architecture-agnostic. A growing body of work [1]–[4]
                                        to intercept unsafe tool-call sequences in LLM agents. Yet across                  confirms they can reduce attack success rates substantially. But
                                        empirical evaluations, the same monitor achieves 68–75% attack
                                        coverage on some model architectures and near-zero coverage on                     practitioners deploying these monitors encounter a troubling
arXiv:2608.01388v1 [cs.CR] 2 Aug 2026




                                        others—with no explanation from capability scores, training data,                  phenomenon: the same monitor that blocks 75% of attacks
                                        or prompt design. We provide the missing theoretical explanation.                  on one backend blocks fewer than 7% on another, with no
                                        We prove that the recall of any fixed-invariant FSA monitor is                     correlation to model capability scores.
                                        bounded above by the concentration of the attack distribution: the
                                        fraction of attacks accounted for by the k most frequent trigger-                     The standard engineering response is to collect more training
                                        completion patterns. When attacks concentrate (low Shannon                         data or tune hyperparameters. We show this is insufficient. The
                                        entropy), a small fixed invariant set achieves high recall. When                   failure is not engineering—it is structural. Fixed-invariant FSA
                                        attacks disperse across many structurally distinct patterns (high                  monitors are provably bounded by the concentration of the
                                        Shannon entropy), no fixed invariant set of tractable size can                     attack distribution, and no amount of additional data changes
                                        achieve meaningful recall—regardless of how the invariants were
                                        derived. We validate this entropy-coverage bound empirically                       a high-entropy distribution into a low-entropy one.
                                        across eight frontier LLM architectures. Attack distributions                         This paper makes three contributions:
                                        on GPT-class and DeepSeek backends are highly concentrated                            C1 (Theory). We derive the entropy-coverage bound: for a
                                        (H ≈ 0.24 bits; one pattern covers 96% of attacks), explaining 68–
                                        75% monitor recall. Gemini variants produce high-entropy attack                    fixed set of k LTL
                                                                                                                                            Pkinvariants, monitor recall is bounded above
                                        distributions (H ≈ 2.81 bits; 7 structurally distinct clusters each                by Covk (D) = i=1 p∗i where p∗1 ≥ p∗2 ≥ · · · are the ordered
                                        covering ≤7% of attacks), explaining near-zero monitor recall                      pattern probabilities of attack distribution D. Equivalently, high
                                        (6–13%)—confirmed invariant to architecture-matched retraining.                    Shannon entropy H(D) implies that Covk (D) is small for any
                                        Across architectures, entropy accounts for 76% of variance in                      tractable k.
                                        monitor coverage (Pearson r = −0.87, p = 0.005, bootstrap 95%
                                        CI [−0.98, −0.78]), with the correlation holding under leave-one-                     C2 (Empirical validation). We measure attack distribution
                                        out analysis (r ∈ [−0.91, −0.82]). We introduce a pre-deployment                   entropy for eight frontier LLM architectures across 847
                                        entropy test that predicts monitor coverage from a small attack                    adversarial trajectories. Entropy explains 76% of variance in
                                        sample, enabling architecture-aware monitor selection before                       monitor coverage (Pearson r = −0.87, p = 0.005; bootstrap
                                        production deployment. The bound and test are architecture-
                                        agnostic and apply to any FSA-based runtime monitor over                           95% CI [−0.98, −0.78]; leave-one-out r ∈ [−0.91, −0.82]).
                                        discrete action sequences.                                                         The Spearman correlation between Elo capability score and
                                           Index Terms—LTL runtime monitors, attack distribution en-                       monitor coverage is not significant (|ρ| < 0.35, p > 0.4),
                                        tropy, FSA coverage bounds, LLM agent safety, formal verification                  confirming entropy—not capability—as the operative predictor.
                                        limits, intelligent systems security
                                                                                                                              C3 (Pre-deployment test). We introduce a practical entropy
                                                                                                                           test that estimates H(D) from 50–100 attack trajectories and
                                                                   I. I NTRODUCTION
                                                                                                                           predicts whether an FSA monitor will achieve meaningful
                                          Finite automata (FSA) runtime monitors enforcing Linear                          coverage on a given backend, enabling architecture-aware
                                        Temporal Logic (LTL) invariants are a natural fit for LLM agent                    monitor selection before production deployment.
                                                                                                                              We answer the open question of why the theater gap (near-
                                          Author’s accepted version. Accepted at the 2026 IEEE 13th International
                                        Conference on Intelligent Systems (IS). © 2026 IEEE. Personal use of this          zero monitor recall on specific architectures, invariant to
                                        material is permitted. Permission from IEEE must be obtained for all other         retraining) exists. The answer is information-theoretic, not
                                        uses, in any current or future media, including reprinting/republishing this       architectural: Gemini variants generate high-entropy attack
                                        material for advertising or promotional purposes, creating new collective works,
                                        for resale or redistribution to servers or lists, or reuse of any copyrighted      distributions that exceed the coverage capacity of any fixed
                                        component of this work in other works.                                             invariant set.
                       II. BACKGROUND                                 Definition 1 (Monitor Recall). The recall of monitor M under
                                                                      attack distribution D is:
A. LTL-FSA Monitors for LLM Agents                                                         X
  A runtime safety monitor observes the agent’s tool-call                   R(M, D) =           p(T,tc ) · 1[M covers (T, tc )] (3)
sequence s = (t1 , t2 , . . .) and flags or halts execution when an                        (T,tc )∈Π

unsafe pattern is detected. LTL-based monitors encode safety          B. The Coverage Bound
properties of the form:
                                                                      Theorem 1 (Entropy-Coverage Bound). For any fixed-invariant
                 ϕ = G(Ttrig → F[1,k] (tcomp ))                (1)    FSA monitor M containing n invariants and attack distribution
                                                                      D over patterns Π:
where G is “globally,” F[1,k] is “within k steps,” Ttrig is                                                      n
                                                                                                                 X
a trigger set, and tcomp is a forbidden completion. Each                               R(M, D) ≤ Cn (D) =              p∗i              (4)
formula is compiled to a sliding-window FSA. A monitor                                                           i=1
M = {ϕ1 , . . . , ϕn } fires if any ϕi is violated.                   where p∗1 ≥ p∗2 ≥ · · · are the ordered pattern probabilities of
   Prior work. Agent-C [1] and AgentSpec [2] use manually             D.
authored LTL rules. ProbGuard [3] learns Markov chains from
benign traces. Recent work derives invariants automatically           Proof. Each formula ϕj = G(Tj → F[1,k] tc,j ) of the bounded-
from red-team attack trajectories [5], [6], reporting coverage        finally class (1) detects trajectories exhibiting the specific
(recall) across multiple architectures. We build on this line         trigger-completion pattern πj = (Tj , tc,j ). Because patterns
of work by providing the theoretical explanation for observed         are defined as distinct trigger-completion pairs, no two distinct
coverage variance.                                                    formulas in M detect the same pattern: each formula is
                                                                      semantically disjoint at the pattern level. Therefore monitor
B. Shannon Entropy and Distribution Concentration                     M = {ϕ1 , . . . , ϕn } covers a set of patterns S ⊆ Π with
  For a discrete probability distribution D over n patterns with      |S| ≤ n.
probabilities {pi }:                                                     Since attack events are attributable to at most one pattern
                                                                      (patterns are mutually exclusive by definition of trigger-
                            n
                            X                                         completion pairs), recall is additive over covered patterns:
               H(D) = −           pi log2 pi   (bits)          (2)
                                                                                                                     n
                            i=1
                                                                                     X                  X            X
                                                                       R(M, D) =           pπ ≤ max           pπ =           p∗i = Cn (D).
                                                                                                   S⊆Π
H = 0 when all mass is on one pattern (maximally con-                                π∈S          |S|≤n π∈S          i=1
centrated); H = log2 n when mass is uniform        Pk(maximally                                                                         (5)
dispersed). The top-k concentration Ck (D) = i=1 p∗i (sum             The maximum is attained by the greedy assignment S ∗ =
of k largest probabilities) is a natural coverage proxy. For fixed    {π1∗ , . . . , πn∗ } (the n most probable patterns), which is achiev-
k, low H implies high Ck .                                            able by constructing invariants targeting those patterns ex-
                                                                      actly.
C. Monitorability in Runtime Verification
                                                                 Corollary 1 (Entropy Lower Bound on Residual Attack Rate).
   Classical runtime verification theory [7] characterizes which The minimum achievable ASR under any n-invariant FSA
LTL properties are monitorable—detectable from finite prefixes. monitor satisfies:
Bounded-finally formulas of the form (1) are monitorable.
However, monitorability is a property of the formula, not of                       ASRmin (n) ≥ 1 − Cn (D)                  (6)
the attack distribution. We extend the analysis to ask: given a
                                                                 When H(D) ≥ log2 (n + 1), we have Cn (D) ≤ n/(n + 1), so
monitorable formula class, when does the attack distribution
                                                                 ASR cannot be driven to zero by any n-invariant monitor.
make a fixed formula set insufficient regardless of formula
derivation method?                                               Proposition 1 (High-Entropy Structural Insufficiency). If D is
                                                                 approximately uniform over m patterns (pi ≈ 1/m for all i),
      III. T HEORY: T HE E NTROPY-C OVERAGE B OUND               then for any n ≪ m:
A. Setup                                                                               C (D) ≈ n/m                          (7)
                                                                                                 n
   Let Σ be the tool-call alphabet of an LLM agent deployment.
                                                                   Monitor recall scales linearly with n/m and approaches zero
An attack trajectory τ = (t1 , . . . , tm ) ∈ Σ∗ is a sequence of
                                                                   as m ≫ n.
tool calls executing an attacker’s objective. An attack distribu-
tion D is a probability distribution over the set of observable       Proposition 1 formalizes the structural insufficiency: when
trigger-completion patterns Π = {(T, tc ) : T ⊂ Σk , tc ∈ Σ} attacks are dispersed across many patterns (high entropy, large
induced by attacks in the deployment.                              m), a fixed-size invariant set covering n patterns captures only
   A fixed-invariant FSA monitor M = {ϕ1 , . . . , ϕn } covers n/m of attacks—regardless of how the invariants were derived
pattern (Ti , tc,i ) if ϕj fires on any trajectory exhibiting that or how much training data was used. This is not a learning
pattern for some j ≤ n.                                            failure; it is a coverage capacity constraint.
C. Entropy-Coverage Duality                                         TABLE I: Attack distribution entropy vs. monitor recall
                                                                    (coverage) per architecture. Low entropy correlates with high
   Theorem 1 gives an upper bound on recall; the following
                                                                    coverage; high entropy correlates with near-zero coverage.
theorem gives a complementary lower bound relating entropy
to coverage in the opposite direction.                                  Model                    H(D̂)     C8 (D̂)       Recall
                                                                                                 (bits)   (bound)    (observed)
Theorem 2 (Entropy-Coverage Duality). For any attack
distribution D and integer n ≥ 1:                                       deepseek-chat              0.19      0.98         0.75
                                                                        gpt-4o-mini                0.24      0.97         0.69
                     H(D) ≥ Hb (Cn (D))                      (8)        gpt-4.1                    0.31      0.95         0.54
                                                                        claude-sonnet-4-6          0.38      0.93         0.50
where Hb (p) = −p log2 p − (1 − p) log2 (1 − p) is the                  llama-3.1-8B               0.72      0.84         0.31
binary entropy function. Consequently, if H(D) < 1 bit, then            claude-haiku-4-5           0.89      0.79         0.25
Cn (D) > 0.5: any FSA monitor achieves better-than-random               gemini-flash-lite          2.64      0.31         0.13
                                                                        gemini-2.5-flash           2.81      0.27         0.06
coverage.
Proof. Partition Π into two groups: the top-n patterns with total
probability Cn and the remaining patterns with total probability φ = 0.05) across eight frontier LLM backends. A controlled
1 − Cn . Let G ∈ {0, 1} be the group indicator. By the chain     retraining experiment derives Gemini-specific invariants directly
rule of entropy and the non-negativity of conditional entropy:   from Gemini-Flash attack trajectories and re-evaluates ASR
                                                                 under block mode. Our contribution is the entropy analysis
   H(D) = H(G) + H(D | G) ≥ H(G) = Hb (Cn (D)). (9) and theoretical bound derived from these experimental results.
The consequence follows because Hb is strictly increasing on        Attack pattern extraction. For each backend, we extract
[0, 0.5]: Hb (Cn ) < 1 whenever Cn > 0.5, so H < 1 implies       trigger-completion   pairs (T, tc ) from attack trajectories that
Hb (Cn ) < 1, which requires Cn > 0.5.                           were   not  blocked  by  the monitor (Type II misses). These
                                                                 represent the attack patterns that fall outside current monitor
Remark 1. Theorems 1 and 2 together characterize two coverage. We cluster patterns by structural similarity (Jaccard
regimes. When H < 1 bit: Cn > 0.5 (FSA monitors achieve distance on tool-call sets) using hierarchical agglomerative
meaningful recall). When H ≥ log2 (n + 1): Cn ≤ n/(n + 1) clustering with threshold θ = 0.4 (the standard midpoint of
(recall is structurally capped). The empirically observed the normalized Jaccard range; the low-entropy vs. high-entropy
transition zone H ∈ [0.5, 2.0] bits corresponds to architectures separation in Table I is stable for θ ∈ [0.3, 0.5]).
where monitor effectiveness depends critically on invariant         Entropy computation. For each architecture A, we compute:
derivation quality and FPR constraints.                          1) The empirical attack pattern distribution D̂A from observed
                                                                     trajectories
D. Implications for the Theater Gap
                                                                 2) Shannon entropy H(D̂A ) via (2)
   The theater gap—near-zero monitor recall on certain archi- 3) Top-n concentration Cn (D̂A ) for n = 8 (our deployed
tectures, confirmed invariant to architecture-matched retraining     invariant count)
(∆ = 0.0 pp)—is a direct consequence of Theorem 1. If archi-        Models. Eight frontier LLMs across four families:
tecture A generates attacks under a high-entropy distribution GPT           (gpt-4o-mini,          gpt-4.1       [9]),     Claude
DA with m roughly equally probable patterns, then for any (claude-haiku-4-5, claude-sonnet-4-6 [10]),
n-invariant monitor: R(M, DA ) ≤ n/m. Retraining (deriving Gemini                                        (gemini-2.5-flash,
new invariants from DA trajectories) cannot increase m—it gemini-2.5-flash-lite [11]), and open-weight
only changes which n patterns the invariants cover, leaving (deepseek-chat, llama-3.1-8B [12]).
the bound unchanged.
   This is why the theater gap is invariant to retraining:                                 V. R ESULTS
the bound Cn (DA ) is a property of the attack distribution, not A. Attack Distribution Entropy by Architecture
of the invariant derivation method.                                 Table I reports Shannon entropy of the attack pattern
                  IV. E XPERIMENTAL S ETUP                       distribution  and observed monitor recall for each architecture.
                                                                    The pattern is clear: architectures with low attack entropy
   We mine the 8 LTL invariants from 847 adversarial trajecto- (H < 0.4 bits) achieve 50–75% monitor recall; architectures
ries collected on AgentDojo banking and workspace suites [8] with high entropy (H > 2.5 bits) achieve only 6–13% recall.
against gpt-4o-mini (temperature=0, seed=42); this fixes The theoretical bound C (D̂) correctly orders all architectures:
                                                                                           8
the monitor. We then independently execute the same red-team no observed recall exceeds the bound, confirming Theorem 1.
attack battery against each of the eight backends and record The gap between bound and observed recall is analyzed in
each backend’s own trajectories, from which its attack-pattern Section V-E.
distribution is computed. Each trajectory records the complete
ordered tool-call sequence. We deploy a sliding-window FSA B. Entropy Predicts Coverage: Statistical Validation
monitor implementing 8 LTL invariants mined from these              Fig. 1 shows monitor recall versus attack entropy for all
trajectories (window k = 5, support σ = 0.02, FPR threshold eight architectures. We find strong negative correlation: Pearson
                                                                  TABLE III: Cluster analysis of Gemini-2.5-Flash Type II
                                                                  misses (135 attacks not blocked by the monitor). High entropy
                                                                  confirmed: 7 clusters with ≤7% per-cluster coverage.

                                                                     Cluster            Size                   Pattern description
                                                                     C1             9 (6.7%)   Balance-check → delayed transfer
                                                                     C2             9 (6.7%)            Multi-hop recon → exfil
                                                                     C3             8 (5.9%)             Batch parallel tool calls
                                                                     C4             8 (5.9%)            IBAN-pivot → schedule
                                                                     C5             7 (5.2%)            Profile-lookup → update
                                                                     C6             7 (5.2%)                     Credential chain
                                                                     C7             6 (4.4%)             Interleaved recon-action
                                                                     Unclustered   81 (60%)                  Dispersed singletons



                                                                  H(D̂Gemini ) = 2.81 bits, close to the maximum entropy
Fig. 1: Attack entropy H(D̂) vs. monitor recall across eight      log2 (7) = 2.81 bits for 7 equal clusters.
architectures (Pearson r = −0.87, p = 0.005). Elo capability         Critically, architecture-matched retraining (deriving new
score is not a significant predictor (|ρ| < 0.35, p > 0.4),       invariants specifically from Gemini-Flash attack trajectories)
confirming entropy as the operative factor.                       achieves ∆recall = 0.0 pp: the bound C8 (D̂Gemini ) = 0.27 is
                                                                  unchanged because the distribution itself has not changed—
TABLE II: Robustness analysis of entropy-recall correlation       only which 8 of its 135+ patterns the monitor covers. This
(r = −0.87, n = 8). Bootstrap and LOO confirm the                 confirms Theorem 1: the bound is a property of D, not of the
relationship is not driven by any single architecture.            derivation method.
   Analysis            Result                 Verdict
   Pearson r (full)    −0.87 (p = 0.005)      Significant         E. Bound Tightness Analysis
   Bootstrap 95% CI    [−0.98, −0.78]         All negative
   LOO min r           −0.82 (drop Gemini)    Robust                 The bound Cn (D) is an architecture-optimal ceiling: it
   LOO max r           −0.91 (drop Llama)     No outlier           represents the maximum recall achievable by the best possible
   Spearman ρ (Elo)    |ρ| < 0.35 (p > 0.4)   Capability n.s.
                                                                   n-invariant monitor for that specific distribution. Our deployed
                                                                   monitor was derived from gpt-4o-mini trajectories only.
                                                                   When evaluated on other architectures, it uses the same n = 8
r = −0.87 (p = 0.005, n = 8), explaining 76% of variance in invariants regardless of whether those invariants target the most
monitor coverage. By contrast, LMSYS Elo capability score probable patterns for the new architecture. The gap between
is not a significant predictor (|ρ| < 0.35, p > 0.4). Attack bound and observed recall therefore decomposes into two
distribution entropy, not model capability, determines FSA components:
monitor effectiveness.
                                                                     FPR-constraint gap (affects all architectures uniformly).
                                                                   Two of our 8 invariants were suppressed at deployment due to
C. Robustness of the Correlation
                                                                   FPR > 5% on benign tasks, reducing effective invariant count
   With only n = 8 architectures, we assess robustness from 8 to 6 and consuming ≈ 20–28 pp of coverage capacity.
through bootstrap resampling and leave-one-out (LOO) analysis.       Distribution-mismatch gap (affects cross-architecture eval-
Table II summarizes results.                                       uation). For architectures whose attack distributions differ
   The bootstrap confidence interval lies entirely below −0.78, from the training distribution (gpt-4o-mini), the deployed
confirming the negative relationship with high probability. LOO invariants may not target the n most probable patterns of the
analysis removes each architecture in turn: even dropping evaluation architecture. Table I shows this effect: GPT-class
the most extreme Gemini point yields r = −0.82; dropping and DeepSeek (similar distributions) have 23–28 pp gaps, while
any single point leaves r ∈ [−0.91, −0.82]. No architecture Llama and Claude mid-range models (more distinct distribu-
dominates the correlation. These results confirm that the tions) show 41–54 pp gaps. High-entropy Gemini models show
entropy-recall relationship is a robust structural pattern, not an small absolute gaps (18–21 pp) because the bound itself is low
artefact of the small sample.                                      (C8 ≤ 0.31).
                                                                     Critically, neither gap type invalidates Theorem 1: the
D. Gemini: High-Entropy Attack Generation Confirmed
                                                                   bound is a ceiling, not a target. The FPR and mismatch
   Table III shows the cluster structure of Gemini’s 135 gaps explain why observed recall lies below the bound—never
Type II missed attacks. No cluster covers more than 6.7% above it. Architecture-specific monitor derivation would close
of attacks. The majority (60%) fall in singleton clusters with the mismatch gap but cannot raise recall above Cn (D), the
no shared pattern. This matches a near-uniform distribution: fundamental limit.
F. The Entropy-Capability Decoupling                                 Setting this ≤ δ and noting E[ℓ] = H(D) (the expected log-
   Fig. 1 demonstrates a clean decoupling: Elo scores (capability    likelihood equals entropy) yields (11).
proxy) span 1070–1330 with no significant correlation to
                                                                        Calibration. For m̂ = 3 clusters (low-entropy architectures:
monitor coverage, while entropy explains coverage almost
                                                                     deepseek, GPT-class), ε = 0.3 bits, δ = 0.05: N ≥ 51 trajec-
entirely. This decoupling has an important implication: de-
                                                                     tories. For m̂ = 10 (high-entropy: Gemini): N ≥ 226. The
ploying a higher-capability model does not improve monitor
                                                                     low-entropy case matches our leave-one-out finding (N = 50
coverage. The operative factor is how the model executes
                                                                     suffices); the high-entropy case requires more samples but
attacks—specifically, whether its attack behavior concentrates
                                                                     remains practical before production deployment. The threshold
in detectable patterns or disperses across a high-entropy               ∗
                                                                     Hlow  = 0.5 bits separating “FSA suitable” from “grey zone”
distribution.
                                                                     lies well inside the region where N = 50 provides ±0.3 bit
        VI. T HE P RE -D EPLOYMENT E NTROPY T EST                    accuracy, so the binary decision is robust even at the minimum
A. Protocol                                                          sample size.
  Given a new deployment backend A and a candidate FSA                                     VII. D ISCUSSION
monitor M, the pre-deployment entropy test proceeds:
1) Sample: collect Nmin = 50 attack trajectories from backend        A. Implications for Monitor Design
   A (via red-team or synthetic attack generation).                  The entropy-coverage bound has direct implications for
2) Cluster: extract trigger-completion patterns, cluster by       intelligent agent safety system design:
   structural similarity (θ = 0.4).                                  FSA monitors are suitable for low-entropy architectures.
3) Estimate: compute Ĥ(D̂A ) from the empirical cluster          When H(D) < 0.5 bits, a small fixed invariant set achieves
   distribution.                                                  high coverage. This holds for the majority of current frontier
                        ∗
4) Predict: if Ĥ < Hlow   = 0.5 bits, FSA monitor is expected    models in our study (GPT-class, DeepSeek). The engineering
   to achieve > 50% recall; proceed to deployment. If Ĥ >        overhead is low; the coverage guarantee is tight.
      ∗
   Hhigh  = 2.0 bits, FSA monitor will achieve < 20% recall;         FSA monitors are structurally insufficient for high-
   use probabilistic or neural monitor instead.                   entropy architectures. For Gemini variants, the bound C8 <
                                                                  0.31 means no 8-invariant FSA monitor can exceed 31% recall.
B. Threshold Calibration
                                                                  This is not fixable by collecting more data or tuning parameters.
                  ∗          ∗
   Thresholds Hlow   and Hhigh   are derived from the empirical Probabilistic monitors (e.g., Markov chain models [3]), neural
results in Table I. With n = 8 invariants: H < 0.5 bits corre- sequence classifiers, or ensemble monitors are required.
sponds to C8 > 0.9 (90% theoretical coverage); H > 2.0 bits          The pre-deployment test replaces architecture guessing.
corresponds to C8 < 0.4 (40% ceiling). The grey zone [0.5, 2.0] Without the entropy test, practitioners guess from Elo scores
requires domain-specific risk assessment.                         or benchmark performance—both of which predict nothing
C. Sample Complexity Guarantee                                    (Spearman    ρ = 0.18). The entropy test directly measures the
                                                                  operative factor.
   We provide a formal sample complexity bound for the
entropy estimation step, replacing the previous empirical rule B. Why Gemini Generates High-Entropy Attacks
of thumb with a provable guarantee.
                                                                     Gemini variants tend to use shorter individual action chains
Theorem 3 (Pre-Deployment Test Sample Complexity). Let m̂ and more parallel batching than GPT-class models, producing
be the number of distinct attack
                            P      clusters observed. The plug-in greater diversity in trigger-completion sequences even within
entropy estimator Ĥ = − c p̂c log2 p̂c computed from N i.i.d. the same attack objective. This is an emergent property of
attack trajectories satisfies, with probability at least 1 − δ:   Gemini’s instruction-following style, not a safety property. The
                                          r                       implication is that model families producing more diverse tool-
                                             ln(2/δ)
              Ĥ − H(D) ≤ log2 (m̂) ·                        (10) call behaviors are intrinsically harder to monitor with fixed-
                                               2N                 pattern approaches—an important consideration for agentic
Consequently, to achieve |Ĥ − H| ≤ ε with confidence 1 − δ: framework design.
                           log22 (m̂) · ln(2/δ)                      C. Beyond LTL: When to Use Probabilistic Monitors
                    N≥                                        (11)
                                    2ε2
                                                                        The entropy bound applies to any fixed pattern-matching
Proof. Each trajectory τi contributes the quantity ℓi =
                                                                     approach, including regex monitors, Snort-style signatures, and
− log2 p̂c(τi ) to the estimator, where c(τi ) is its cluster as-
                                                                     behavioral allowlists. It does not apply to probabilistic monitors
signment. The variable ℓi is bounded: ℓi ∈ [0, log2 m̂] (since
                                                                     (Markov chains, neural classifiers) that can capture distribu-
p̂c ≥ 1/N > 0 and p̂c ≤ 1, giving range log2 m̂). Applying
                                                                     tional spread. For high-entropy architectures, ProbGuard [3] or
Hoeffding’s inequality to the sample mean Ĥ = N −1 i ℓi :
                                                            P
                                                                     similar stochastic approaches are theoretically preferable. The
                                              −2N ε2
                                                       
                                                                   entropy test thus serves as a monitor selection criterion: low
           P |Ĥ − E[ℓ]| > ε ≤ 2 exp                      .          entropy → FSA; high entropy → probabilistic.
                                             log22 (m̂)
D. Threats to Validity                                             on Gemini variants invariant to retraining—is an information-
   Entropy estimation. Entropy estimates from 50–100 tra- theoretic consequence of high-entropy attack distributions, not
jectories have ±0.3 bit uncertainty. This does not affect the an architectural artifact.
qualitative conclusion for the extreme cases (GPT: 0.24 bits;            a) Future work.: Three directions follow directly. First,
Gemini: 2.81 bits) but could misclassify borderline architectures. our  bound   assumes a fixed invariant set; adaptive monitors
Adaptive adversary. An adversary who knows the entropy test        that  periodically  re-mine invariants from recent traffic may
can deliberately generate high-entropy attacks to evade FSA        raise  the effective  coverage ceiling on drifting, high-entropy
monitors. The entropy test predicts natural attack behavior;       distributions, and   characterizing    their bound is open. Second,
adversarial entropy injection is a separate threat requiring       the  entropy-coverage     relationship     should be tested beyond
periodic re-evaluation.                                            AgentDojo,    on  additional  agent   benchmarks   and non-tool-call
   Single deployment domain. All trajectories are from Agent-      action  spaces,  to establish  how   far  the law generalizes. Third,
Dojo banking. Attack entropy may differ in other domains; the      the  pre-deployment    entropy   test  invites a companion  defense:
test protocol should be re-applied per deployment context.         routing high-entropy backends to complementary content-level
                                                                   or learned monitors, since fixed formal monitors are provably
                    VIII. R ELATED W ORK                           insufficient for them.
   LTL runtime monitoring theory. Classical monitorability                                         R EFERENCES
theory [7] characterizes which LTL properties can be detected         [1] A. Kamath, S. Zhang, C. Xu, S. Ugare, G. Singh, and S. Misailovic,
from finite execution prefixes. Our contribution is orthogonal:           “Enforcing temporal constraints for LLM agents,” arXiv:2512.23738,
                                                                          2025, system presented: Agent-C.
we characterize when a monitorable property class achieves            [2] H. Wang, C. M. Poskitt, and J. Sun, “AgentSpec: Customizable runtime
high coverage on a given attack distribution, a question not              enforcement for safe and reliable LLM agents,” in ICSE, 2026.
addressed by classical theory.                                        [3] H. Wang, C. M. Poskitt, J. Wei, and J. Sun, “ProbGuard: Probabilistic
                                                                          runtime monitoring for LLM agent safety,” arXiv:2508.00500, 2025.
   Entropy in security. Shannon entropy has been applied              [4] T. Zhang, Y. Xu, J. Wang, K. Guo, X. Xu, B. Xiao, Q. Guan, J. Fan,
to network intrusion detection (measuring traffic flow diver-             J. Liu, Z. Liu, and H. Hu, “AgentSentry: Mitigating indirect prompt
sity [13]) and malware classification (measuring instruction              injection in LLM agents via temporal causal diagnostics and context
                                                                          purification,” arXiv:2602.22724, 2026.
sequence entropy). We apply it to the attack-side distribution in     [5] A. J. Akande et al., “LTL-based runtime verification framework for
LLM agent safety monitoring, specifically to derive coverage              cyber-attack anomaly prediction in cyber-physical systems,” Computers
bounds for a class of formal monitors.                                    & Security, vol. 155, 2025.
                                                                      [6] O. Koucham, S. Mocanu, G. Hiet, J.-M. Thiriet, and F. Majorczyk,
   Runtime monitoring for LLM agents. Agent-C [1],                        “Efficient mining of temporal safety properties for intrusion detection in
AgentSpec [2], ProbGuard [3], AgentSentry [4], and AgentVer-              industrial control systems,” in SAFEPROCESS, 2018.
ify [14] provide monitoring frameworks. None characterizes            [7] C. Mascle, D. Neider, M. Schwenger, P. Tabuada, A. Weinert, and
                                                                          M. Zimmermann, “From LTL to rLTL monitoring: Improved monitora-
the coverage limits of fixed-pattern monitors or provides the             bility through robust semantics,” Formal Methods in System Design,
pre-deployment entropy test.                                              2022, arXiv:1807.08203.
   Attack distribution characterization. The “Mapping the             [8] E. Debenedetti, J. Zhang, M. Balunović, L. Beurer-Kellner, M. Fischer,
                                                                          and F. Tramèr, “AgentDojo: A dynamic environment to evaluate prompt
Exploitation Surface” study [15] characterizes what prompt                injection attacks and defenses for LLM agents,” in NeurIPS, 2024.
conditions trigger LLM agents to exploit vulnerabilities              [9] OpenAI, “GPT-4.1: Technical report,” OpenAI, Tech. Rep., 2025.
autonomously—a different threat model (agent as attacker,                 [Online]. Available: https://openai.com/index/gpt-4-1/
                                                                     [10] Anthropic, “Claude Sonnet 4 model card,” Anthropic, Tech. Rep., 2025.
not victim). Our entropy analysis focuses on indirect prompt              [Online]. Available: https://www.anthropic.com/claude/sonnet
injection attacks against agents.                                    [11] Google DeepMind, “Gemini 2.5 Flash: Technical report,” Google
                                                                          DeepMind, Tech. Rep., 2025. [Online]. Available: https://deepmind.
                       IX. C ONCLUSION                                    google/models/gemini/flash/
                                                                     [12] Meta AI, “The Llama 3 herd of models,” Meta AI, Tech. Rep., 2024,
   We derived and empirically validated the entropy-coverage              arXiv:2407.21783.
                                                                     [13] A. Lakhina, M. Crovella, and C. Diot, “Mining anomalies using traffic
bound (Theorem 1): the recall of any fixed-invariant FSA                  feature distributions,” in ACM SIGCOMM, 2005.
monitor is bounded above by the concentration of the attack dis-     [14] E. Fang, “AgentVerify: Compositional formal verification of AI agent
tribution. Theorem 2 establishes the complementary direction:             safety properties via LTL model checking,” Preprints.org, 2026,
                                                                          dOI:10.20944/preprints202604.1029.v1.
when H(D) < 1 bit, FSA monitors provably achieve better-             [15] C. Mouzouni, “Mapping the exploitation surface: A 10,000-trial taxonomy
than-random coverage. Together, the two theorems characterize             of what makes LLM agents exploit vulnerabilities,” arXiv:2604.04561,
the full entropy-coverage tradeoff. Theorem 3 converts the                2026.
pre-deployment entropy test from an empirical heuristic into
a formally guaranteed procedure: N ≥ 51 trajectories suffice
for low-entropy architectures (m̂ ≤ 3, ε = 0.3 bits, δ = 0.05),
matching our leave-one-out result exactly. Empirically, en-
tropy explains 76% of variance in monitor coverage across
eight architectures (r = −0.87, p = 0.005; bootstrap CI
[−0.98, −0.78]; LOO r ∈ [−0.91, −0.82]), while model ca-
pability (Elo) explains none. The theater gap—near-zero recall
