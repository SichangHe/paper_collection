                                         Preprint




                                         AUDIT-F IRST VAPO: R ISK -C ERTIFIED S ELECTIVE
                                         U PDATES UNDER I MPERFECT V ERIFICATION
                                          Miaobo Hu1,2 , Shuhao Hu2 , Xiaobo Guo2 , Xin Wang2 ,
                                          Bokun Wang2 , Rui Chen2 , Daren Zha2 , Jun Xiao1,∗
                                          1
                                            School of Artificial Intelligence, University of Chinese Academy of Sciences, Beijing, China
                                          2
                                            Institute of Information Engineering, Chinese Academy of Sciences, Beijing, China
                                          ∗
                                            Corresponding author: xiaojun@ucas.ac.cn
arXiv:2609.33662v1 [cs.AI] 27 Sep 2026




                                                                                       A BSTRACT

                                                    Imperfect verifiers can assign a harmful update direction even when clipping
                                                    and regularization bound its magnitude. We introduce Audit-First VAPO, which
                                                    separates discrete directional admission from continuous magnitude control. An
                                                    observation-only accept–appeal–abstain policy uses a finite secondary-verification
                                                    budget; its action trace is frozen before clean labels are joined. Simultaneous finite-
                                                    sample bounds then certify selected harmful risk, coverage, and verifier-call rate
                                                    over a predeclared policy family. Conditional Hoeffding–Azuma bounds account
                                                    for the dependence induced by shared budgets, and rollout or verifier changes
                                                    initiate a new certification stage. After admission, a bounded trust–clip–KL actuator
                                                    controls magnitude. We evaluate two models on two reasoning benchmarks against
                                                    static RLVR, matched-random selection, confidence thresholding, noise correction,
                                                    and verifier augmentation. On Qwen3.5-0.8B and GSM8K at target risk ρ = 0.08,
                                                    RC-VAPO achieves 74.1% accuracy, selected harmful risk 0.0697, coverage 0.4125,
                                                    and relative verifier cost 1.16×. At matched coverage and update magnitude, its
                                                    selected-risk difference from matched random is −0.0260 with paired 95% interval
                                                    [−0.0364, −0.0157]. Across asymmetric, confidence-dependent, and correlated-
                                                    verifier noise, the certificate is satisfied on 57 of 60 independent runs. These
                                                    comparisons isolate informative directional selection from proposal suppression,
                                                    update shrinkage, and additional verifier computation.



                                         1    I NTRODUCTION

                                         Verifier-conditioned policy updates contain two logically different control problems. First, the verifier
                                         determines whether the proposed update direction is aligned with the unavailable clean objective.
                                         Second, conditional on admitting a proposal, the learner determines how large that update should be.
                                         Conflating these problems is unsafe: with a nonnegative update magnitude, clipping, trust weighting,
                                         and KL regularization shrink a wrongly signed proposal, so directional control belongs to selective
                                         admission.
                                         This observation motivates a two-stage design. The first stage is a selective admission layer that
                                         chooses among accept, appeal, and abstain under an explicit harmful-risk and verifier-cost budget.
                                         The second stage is a bounded magnitude actuator applied only after the proposal has been admitted.
                                         Our primary methodological contribution is the first stage: a risk-certified policy-selection rule whose
                                         calibration decisions are frozen before clean labels are joined and whose deployed decisions use only
                                         observed verifier signals.
                                         Our evidence has three linked layers. First, a replayable mechanism audit checks the information
                                         boundary and exposes the algebraic redundancy of the historical binary-view state. Second, a
                                         canonical learner protocol compares certified admission with matched controls and direct imperfect-
                                         verifier baselines. Third, transfer, rollout-refresh, and verifier-noise studies test the certificate under
                                         declared changes in proposals, model family, and error structure. Each result is bound to its model,
                                         split, seed, checkpoint, verifier, and resource ledger.


                                                                                              1
Preprint




Stateful certification boundary. An appeal is a state-changing operation when all records share a
finite secondary-verification budget. The action sequence can therefore be dependent even when the
underlying records are sampled independently. We make the resource state explicit, freeze a finite
candidate family on an observation-only design split, and certify a disjoint sequence with conditional
Hoeffding–Azuma bounds. A new rollout or verifier regime starts a fresh certificate stage rather than
silently reusing the previous one.

Contributions.     We make five contributions.
(1) Direction–magnitude decomposition. We formalize selective verifier-conditioned updating as
two coupled but non-interchangeable decisions: whether a proposal should enter the learner and,
conditional on admission, how strongly it should be applied. We show that a nonnegative actuator
preserves the sign of an applied update, which makes selective admission or additional verifier
information necessary for controlling directional harm.
(2) Budget-aware sequential risk certification. We introduce a finite family of observation-only
accept–appeal–abstain policies and a post-freeze calibration procedure that constructs simultaneous
finite-sample certificates for a stateful action sequence. Conditional Hoeffding–Azuma bounds cover
selected harmful risk, coverage, and verifier-call rate when appeals consume a shared budget; the
controller fails closed when no candidate is certified.
(3) Audit-first construction and renewal. Candidate policies are instantiated on an observation-only
design split and frozen before the certification split is executed. A predeclared confidence spending
schedule renews the certificate when the rollout or verifier distribution changes.
(4) Budgeted secondary verification. Ambiguous proposals may invoke a source-distinct secondary
verifier only inside a declared appeal region. Disagreement, missing responses, exhausted budget,
or failed provenance checks lead to abstention. This makes verifier quality and verifier cost explicit
components of the update decision rather than hidden properties of the reward pipeline.
(5) Matched learner evaluation. We evaluate selection quality independently from proposal sup-
pression and update shrinkage using coverage-matched and magnitude-matched controls, direct
imperfect-verifier baselines, multiple verifier-noise regimes, refreshed rollouts, and held-out task
transfer. Every reported learner result is tied to an explicit model, split, seed, checkpoint, verifier, and
resource ledger.

2    R ELATED W ORK
Offline RL and reward-hacking work show that optimizing an unreliable proxy can move away from
the intended objective (Kumar et al., 2020; Kostrikov et al., 2022; Fu et al., 2021; Skalse et al., 2022).
RLVR and process-verification systems make the same distinction between an observed trace and a
correctness signal (Shao et al., 2024; Qwen Team, 2024; DeepSeek-AI, 2025; Zheng et al., 2024;
Lightman et al., 2024; Wang et al., 2023). PPO/TRPO motivate the ratio and KL notation, while
selective prediction motivates explicit abstention and coverage (Schulman et al., 2017; 2015; Geifman
& El-Yaniv, 2019). VAPO freezes the proposal and keeps clean labels out of the online path, then
adds a risk-certified admission object that is evaluated separately from the magnitude actuator.
Tool-using and self-refining agents further motivate separating an action from the external result
that follows it (Yao et al., 2023; Schick et al., 2023; Shinn et al., 2023; Madaan et al., 2023). Our
contribution is the fail-closed boundary and its replay contract. The evaluation combines a fixed-
proposal mechanism audit with a reported learner ledger; independent task verification and per-seed
artifacts define the conditions for interpreting the latter.

Imperfect-verifier RLVR. Recent work has made verifier error itself an RLVR optimization
problem (Cai et al., 2025; Xu et al., 2025). Cai et al. model binary verification as an asymmetric noisy-
reward channel and derive backward and forward corrections that modify reward or score-function
terms to recover a cleaner policy-gradient signal; their practical system also uses an appeal verifier
to estimate verifier error online. TinyV instead augments a rule-based verifier with a lightweight
language-model verifier to recover false negatives during RL training. These approaches improve
the reward signal itself. VAPO addresses a complementary decision: given imperfect and potentially
correlated verifier observations, which proposal should be allowed to enter the learner under a finite


                                                     2
Preprint




secondary-verification budget. It uses selective admission, appeal, and abstention and certifies the
resulting admitted-update risk on a disjoint calibration split. The canonical comparison therefore
includes both noise-correction and verifier-augmentation baselines.

Selective control with stateful budgets. Selective prediction, conformal risk control, verifier
cascades, and adaptive querying motivate abstention and cost-aware routing. Our setting adds a
shared appeal resource: spending a call changes the feasible actions for later records. We consequently
certify the induced accept–appeal–abstain sequence with its resource state, rather than treating it as
independent per-record threshold decisions. The design/certification split keeps policy construction
separate from the clean labels used for the certificate.

Risk-controlling prediction. Our statistical calibration layer builds on finite-sample risk-control
methods such as conformal risk control (Angelopoulos et al., 2024). The contribution here is to
instantiate risk control for verifier-conditioned policy updates, where the candidate decision is an
accept–appeal–abstain action, coverage is a constrained resource, verifier calls have an explicit budget,
and every calibration label is joined only after the corresponding action trace has been frozen.
Verifier learning on math word problems evaluates candidate correctness (Cobbe et al., 2021), while
RewardBench evaluates reward-model preferences across challenging answer pairs (Lambert et al.,
2024). Unfaithful chain-of-thought explanations motivate evaluating correctness separately from the
plausibility of a rationale (Turpin et al., 2023). FrugalGPT and RouteLLM study the relationship
between model selection, quality, and cost (Chen et al., 2023; Ong et al., 2025). These distinctions
motivate our separate task, risk–coverage, and resource measurements.

3     M ETHOD
3.1   TASK DEFINITION

Each record comprises observed verifier views and a proposal fixed before control. The decision
is whether to apply that proposal and with what nonnegative magnitude. The evaluation target is
the joint behavior of harmful-update risk, proposal coverage, and task outcome. Clean correctness
labels are available for offline evaluation after decisions freeze. This ordering defines the information
available to a controller and separates selection quality from the cost of abstention. Figure 1 shows
the fixed-proposal information boundary; Figure 3 details sequential certification and renewal.

3.2   S ELECTIVE - UPDATE CONTRACT

For each frozen proposal, the controller chooses a triage action
                                  At ∈ {accept, appeal, abstain}.
We reserve aagr
              t for cross-view agreement and never use the same symbol for the triage action. Let
ȳt ∈ {−1, 0, +1} denote the final admitted update sign, where ȳt = 0 denotes abstention, and define
                                             bt = 1[ȳt ̸= 0].
The clean sign zt is unavailable when At and ȳt are serialized. After the trace is frozen, the evaluator
joins zt and defines
                                    ht = 1[bt = 1 ∧ zt ȳt < 0].
The primary selective-risk quantity is
                                             E[ht ]
                                    Rsel =          ,       C = E[bt ],
                                             E[bt ]
for C > 0; at zero admissions the selected risk is undefined and the admitted count is reported. The
all-proposal harmful rate remains
                                        Rall = E[ht ] = CRsel .
We therefore treat Rsel as the directional-selection metric and report Rall jointly with coverage so
that risk reductions caused only by abstention are separated from improved proposal selection.


                                                        3
Preprint




The protocol-level constraints are
                              Rsel ≤ ρ,        C ≥ Cmin ,        A ≤ Bmax ,
where A is the realized secondary-verifier call rate. Thresholds and checkpoint rules are fitted from
calibration-side observations and the declared resource budget; test labels enter only after the action
trace is frozen.

3.3   D ESIGN AND CERTIFICATION SPLITS

Let Ddesign and Dcert be disjoint before training begins. The design split contains controller-visible
observations but does not provide clean labels to the policy-construction procedure. It instantiates the
finite candidate family
                                         G = {gλ : λ ∈ Λ},
including trust thresholds, appeal regions, secondary-verifier thresholds, and no-appeal special cases.
After G is frozen, Dcert is processed exactly once by every candidate. The ordered action trace stores
observations, actions, verifier fields, pre-call and post-call budget states, final admitted sign, and
source digests before any clean certification label is joined. Thus policy construction and certificate
estimation use separate information boundaries.

3.4   R ISK - CERTIFIED POLICY SELECTION

Let
                                            G = {gλ : λ ∈ Λ}
be a finite family of triage policies declared before calibration labels are opened. A policy gλ maps
only observed state and resource state to an accept–appeal–abstain action. The family may include
different trust thresholds, appeal regions, secondary-verifier confidence thresholds, and no-appeal
special cases.
For a target selected harmful-risk level ρ ∈ (0, 1), define the bounded excess-harm loss
                                        ℓρ (g; t) = ht (g) − ρbt (g).
Because                                                                 
                                   E[ℓρ (g; t)] = E[bt (g)] Rsel (g) − ρ ,
any policy with positive coverage and E[ℓρ (g; t)] ≤ 0 satisfies Rsel (g) ≤ ρ.
Calibration proceeds in two ordered phases. First, every g ∈ G is executed using only observed
calibration fields, and its ordered actions, verifier calls, outputs, budget states, and source digests are
serialized. Second, after all candidate traces are frozen, clean calibration labels are joined to compute
                 ncal
   b ρ (g) = 1                              1 X                         1 X
                 X
   L                  ℓρ (g; t),    C(g)
                                    b    =        bt (g),       A(g)
                                                                b    =        1[At (g) = appeal].
            ncal t=1                       ncal t                      ncal t

For a predeclared confidence level δ, simultaneous Hoeffding-style bounds over the finite family are
                                                   s
                                Uρ (g) = Lb ρ (g) + log(3|G|/δ) ,
                                                         2ncal
                               s                                      s
                                  log(3|G|/δ)                  b + log(3|G|/δ) .
             LC (g) = C(g)
                        b   −                  ,    UA (g) = A(g)
                                      2ncal                                2ncal
The deployed policy is
                                           gb = arg max LC (g)
                                                     g∈G

subject to Uρ (g) ≤ 0, LC (g) ≥ Cmin , and UA (g) ≤ Bmax . If the feasible set is empty, calibra-
tion returns the explicit fail-closed policy that abstains on every proposal. The certificate stores
(b
 g , ρ, Cmin , Bmax , δ, Uρ , LC , UA ) and the calibration-trace digest. Deployment reads this certificate
and current observed state only; no current-record clean label is accessible to the controller.


                                                     4
Preprint




Budget-aware sequential certificate. Shared appeals make later actions depend on the preceding
resource state. For the declared finite stage, let Ft−1 contain the history and budget before record t.
We certify the averages of E[ht − ρbt | Ft−1 ], E[bt | Ft−1 ], and E[1[At = appeal] | Ft−1 ]. Each
centered process has bounded increments with    p range length one. Hoeffding–Azuma and a union
bound over 3|G| give the same radius rn = log(3|G|/δ)/(2n) with simultaneous probability at
least 1 − δ (Hoeffding, 1963; Azuma, 1967). A feasible policy therefore satisfies the directional-risk,
coverage, and call-rate constraints for this conditional stage estimand. A future sequence has its own
stage law. Appendix C gives the complete derivation and stateful execution diagram.

3.5    C ERTIFICATE RENEWAL UNDER ROLLOUT SHIFT

A change in the rollout generator, verifier definition, observation channel, or resource protocol starts a
            P stage. For stages r = 1, . . . , R, fresh certification buffers use predeclared confidence
new certification
levels with r δr ≤ δ. Candidate families and threshold grids are frozen before each stage’s labels
are joined. A union bound gives simultaneous validity across stages, while a stage with no feasible
candidate fails closed until a new certificate is obtained.

3.6    O BSERVED FEEDBACK STATE

The observed state contains the primary sign yt ∈ {−1, +1}, confidence ct , source-distinct auxiliary
signals, frozen proposed ratio-delta ∆rt , observed KL kt , and remaining appeal budget. The scalar
score st ∈ [0, 1] is fixed on the design split. Every auxiliary signal carries a source identifier and
digest; duplicate and oracle fields are rejected before execution. Appendix C gives the historical
five-view fixture and actuator parameterization used in the mechanism audit.

                                                                        et = ȳt mt with mt ≥ 0.
Direction–magnitude separation. After triage, an admitted proposal uses u
For every admitted proposal with mt > 0,
                                       sign(zt u
                                               et ) = sign(zt ȳt ).
Thus a nonnegative magnitude actuator cannot convert a harmful admitted direction into a helpful
one. Let mt ≤ mmax and define harmful update magnitude
                                           Hmag = E[mt ht ].
Then
                                        Hmag ≤ mmax CRsel .
The selective layer controls the frequency of harmful admitted directions through C and Rsel , whereas
the bounded actuator controls their remaining magnitude. This decomposition motivates evaluating
selection and magnitude control separately.

Matched selection and verifier dependence. At fixed coverage, a non-increasing conditional
harmful rate in the observed score motivates largest-score selection; the matched study checks
this condition rather than assuming it. A source-distinct appeal can reduce error under conditional
independence, but the protocol makes no such assumption: marginal errors, joint failures, and binary-
error correlation are reported with the appeal cost (the elementary fixed-coverage and agreement
calculations are in Appendix C).

Oracle-aligned metrics and risk–return accounting. For N frozen decisions define gt = zt u
                                                                                         et ,
where zt is joined only after the action is serialized. We report
                          1 X                 1 X                 1 X
                    U=           gt , P =            (gt )+ , H =     (−gt )+ ,
                         N t                  N t                 N t

                         1 X                        1 X
                   R=        1[gt < 0],       Z=        1[gt = 0],       C = 1 − Z.
                         N t                        N t
Here U = P − H is the aligned scalar return proxy, R is harmful-update risk, and C is proposal
coverage. Helpful and harmfulP               P all-record denominator N ; the implementation’s
                              rates use the same
nonzero direction accuracy is t 1[gt > 0]/ t 1[gt ̸= 0] (set to zero for an empty denominator).


                                                    5
Preprint




Figure 1: Fixed-proposal mechanism and information boundary. Blue blocks contain observations
and frozen proposals, orange controls set the nonnegative update magnitude, and green blocks
evaluate the frozen trace. The five-view fixture uses an uncalibrated confidence input and redundant
agreement/consistency summaries. This audit motivates the source-distinct admission policy and the
stateful certification procedure in Figure 3.


The tables report U , R, Z, and C jointly: suppressing proposals reduces exposure to both helpful and
harmful updates.
For the selected subset, we additionally report
                                P
                                     1[gt < 0]
                         Rsel = Pt              ,       R = C Rsel    (C > 0).
                                   t 1[gt ̸= 0]

This decomposition separates lower risk caused by rejecting more proposals from lower risk among
the proposals that were applied.

3.7   S OURCE - DISTINCT OBSERVED STATE

The retained binary-view fixture makes agreement a deterministic function of consistency, so those
fields cannot support an independent-signal attribution. The primary state therefore keeps only
source-distinct signals, each with its own identifier and digest; equal digests, oracle fields, and legacy
duplicates are rejected. Paired error rates and joint failures are reported to assess dependence. The
full deduplicated score, matching normalization, and tie rule are specified in Appendix C.

3.8   B UDGETED APPEAL POLICY

A candidate policy gτlow ,τhigh ,τ2 uses two primary-score thresholds:
                            
                            accept, st ≥ τhigh ,
                    At = appeal, τlow ≤ st < τhigh and budget remains,
                            
                               abstain, otherwise.
Direct acceptance sets ȳt = yt . For an appealed proposal, a source-distinct secondary verifier
          (2) (2)                                               (2)             (2)
returns (yt , ct ) and the proposal is admitted only when yt = yt and ct ≥ τ2 ; otherwise
ȳt = 0. Missing responses, verifier disagreement, provenance failure, exhausted budget, or an invalid
secondary record fail closed. The appeal request is serialized before reading the paid verifier result.
Returned fields, source identifier, source digest, pre-call and post-call budget states, final action,
and failure reason are appended to the ordered trace before any clean label is joined. No-appeal
thresholding is included in G as a special case.


                                                    6
Preprint




3.9    P OST- ADMISSION BOUNDED MAGNITUDE ACTUATOR

The bounded trust–clip–KL controller is applied after the discrete admission decision and is not
credited with correcting update direction. For an admitted proposal,
               dt = min(∆rt , ϵt ),        mt = max{0, wt dt − βt kt },         u
                                                                                et = ȳt mt .
For an abstained proposal, mt = 0. The controller surfaces retain
                   wt ∈ [wmin , 1],        ϵt ∈ [ϵmin , ϵmax ],     βt ∈ [βmin , βmax ],
so their mechanical effect remains auditable. The primary comparisons separate admission quality,
verifier escalation, and continuous magnitude control.

3.10    O BSERVED - ONLY THRESHOLD ACTION

For disjoint calibration and evaluation records, quantile thresholds are fitted from observations only:
                     τs = Qqtrust (sC ),    τk = QqKL (kC ),      τr = Qqratio (∆rC ).
The eligibility action is et = 1[st ≥ τs ∧ kt ≤ τk ]; an eligible proposal is capped at τr and an
ineligible one is replaced by (0, 0). The quantile settings belong to the frozen candidate specification;
Appendix D records the fitted values for the historical replay.

3.11    AUDIT AND REPLAY PROTOCOL

Each decision stores its source digest, observed fields, controller output, and update. Clean labels
are stored separately and joined only after the action is serialized. Replay checks digests, ordering,
and policy outputs. A match verifies deterministic execution; the post-freeze label join yields
harmful-update diagnostics.

4     E XPERIMENTS
4.1    E XPERIMENTAL SETUP

The canonical learner protocol is the reference for task accuracy, selective risk, coverage, and
resource comparisons. The primary model and task are Qwen3.5-0.8B and GSM8K; training uses
seeds 13, 17, 23, 128k rollout tokens and 256 verifier calls per update. The second backbone is Llama-
3.2-3B-Instruct, and task transfer uses SVAMP. Calibration, train, held-out, and test records are
disjoint; candidate policies, thresholds, budgets, and checkpoint rules are fixed before test labels open.
Each policy–seed pair stores its trace, certificate, learner ledger, selected checkpoint, and post-freeze
evaluation trace. The five protocol roles and the renewal trigger are specified in Appendix A.
Historical fixed-proposal and connectivity audits retain separate evaluators and run identities, detailed
in Appendix A.

4.2    BASELINES AND METRIC CONVENTIONS

Static RLVR applies all proposals; matched random applies the same number of proposals with an
independent stream. Observation and risk-certified thresholds remove appeal to isolate calibration,
while cost-matched random appeal and always-on secondary verification isolate verifier allocation.
VAPO-legacy, noise-corrected RLVR, and verifier augmentation are retained as direct controls with
the same learner and resource ledger.
Whenever no proposal is admitted, Rsel is undefined rather than zero and is reported together with
the admitted count.

4.3    M AIN RESULTS

Table 1 separates all-proposal harmful risk from selected risk. Accuracy is measured on the sealed
task test set; coverage is the fraction of admitted directions; appeal and cost use the same verifier-call


                                                      7
Preprint




Table 1: Canonical learner comparison. Rall uses all proposals as its denominator, while Rsel
conditions on admitted directions. The no-appeal, cost-matched, and always-on secondary-verifier
controls isolate selection and verification cost. Accuracy is in percent; risk and coverage are fractions.
Best accuracy, risk, cost, and GPU-hours are bold; coverage and appeal are descriptive. The symbol
n/a denotes a method without an appeal mechanism.
Method                                                  Acc.    Rall    Rsel       C Appeal   Cost GPU-h
Static RLVR                                             70.5 0.0914 0.0914 1.0000    n/a 1.00×       10.50
Matched random                                          69.8 0.0396 0.0956 0.4138    n/a 1.01×       10.57
Observation threshold                                   72.7 0.0466 0.1241 0.3752      0 1.03×       10.76
Risk-certified threshold (no appeal)                    73.2 0.0238 0.0748 0.3186      0 1.04×       10.92
Noise-corrected RLVR                                    72.4 0.0828 0.0829 0.9987      0 1.08×       11.34
Verifier augmentation                                   73.0 0.0595 0.0780 0.7624 1.0000 1.17×       12.28
Cost-matched random appeal                              70.1 0.0387 0.0939 0.4121 0.1837 1.16×       12.14
Always-on secondary verifier                            73.5 0.0494 0.0671 0.7368 1.0000 1.38×       14.49
VAPO-legacy                                             73.3 0.0347 0.0831 0.4179 0.1762 1.13×       11.86
RC-VAPO                                                 74.1 0.0288 0.0697 0.4125 0.1816 1.16×       12.17



ledger. Intervals are paired 95% hierarchical-bootstrap intervals over the declared seed/question
hierarchy.
RC-VAPO achieves the highest task accuracy, 74.1%, with selected risk 0.0697 at coverage 0.4125.
The no-appeal certificate yields lower all-proposal risk 0.0238 at coverage 0.3186; always-on sec-
ondary verification attains selected risk 0.0671 at 1.38× cost. These operating points expose the
joint selection, coverage, and verification-cost trade-off. Appendix E reports matched controls, noise
conditions, and certificate repetitions. Accuracy is a percentage; Rall , Rsel , C and appeal rate are
fractions. The certificate uses admitted directions as its denominator; the actuator’s zero-magnitude
rate is reported separately.

4.4   A NALYSIS AND ABLATIONS

The analysis separates admission quality, magnitude control, verifier allocation, and certificate
renewal under the same task-level estimands.

Primary checks and evidence strata. Matched coverage and magnitude, shared-budget validity,
order sensitivity, the mechanism audits, and the twelve-seed frontier are reported in Appendix D
and Appendix E. The shared-budget condition has one violation over 60 independent stages; the
correlated-verifier condition has three violations over 60 stages. The measured risk-target and
shared-budget panels are reported in Tables 34 and 26.

Matched selection. Table 2 compares selected risk at common coverage and mean absolute
update magnitude. The paired RC-VAPO-minus-random risk difference is −0.0260, with 95%
interval [−0.0364, −0.0157]. The negative interval identifies selection information beyond proposal
suppression under the paired protocol. Table 27 retains the full matching comparison. With both


Table 2: Selection at matched coverage and magnitude. Accuracy is a percentage; Rsel and C are
fractions. Best risk and accuracy are bold.
Method                                                           C      Mean |u|     Rsel     Accuracy (%)
Matched random                                                 0.4137    0.1071     0.0957        70.1
Matched static                                                 0.4129    0.1068     0.0942        70.8
RC-VAPO, matched                                               0.4119    0.1069     0.0697        73.8


coverage and magnitude matched, RC-VAPO attains 73.8% accuracy against 70.1% for matched
random. The cost-matched random-appeal and always-on controls in Table 1 separate targeted verifier
allocation from additional verification compute.


                                                    8
Preprint




Noise robustness and component effects. Figure 2 compares five verifier-error structures. RC-
VAPO has lower selected risk and higher accuracy than noise correction in each condition. Its
selected risk ranges from 0.0654 under false-negative-heavy noise to 0.0791 under correlated errors.
Component ablations in Table 29 give 73.2% accuracy and risk 0.0846 without a certificate, versus
74.1% and 0.0697 for the full controller. Certificate-only admission has coverage 0.3194; adding
appeals increases it to 0.4057 with selected risk 0.0709. The full controller combines this admission
gain with bounded magnitude control.




Figure 2: Verifier-noise comparison on GSM8K. Blue circles denote RC-VAPO and orange squares
denote noise correction; connectors pair methods within each noise condition. The dashed risk line is
the target ρ = 0.08. Points show reported aggregates; condition-specific uncertainty intervals are not
supplied. Exact values appear in Table 28.

Model, rollout, and task changes. On Llama-3.2-3B-Instruct, RC-VAPO attains 67.1% accuracy
and selected risk 0.0768, compared with 64.0% and 0.1048 for static training. Renewal at every
rollout refresh gives 75.3% accuracy at 1.47× cost; periodic renewal gives 74.9% at 1.25× cost.
On SVAMP, target-side recalibration yields 63.2% accuracy and risk 0.0737, while a frozen source
certificate yields 61.3% and 0.1067. The transfer comparison locates the risk benefit in calibration to
the target distribution.

5    L IMITATIONS AND S COPE OF THE G UARANTEE
The certificate targets the finite-stage conditional directional-risk estimand for the declared sequence
law, verifier definitions, initial budget, and rollout regime. Nonlinear parameter trajectories, final-
model safety, cumulative drift, and long-horizon utility require separate evaluations. Rollout, verifier,
prompt, observation-channel, or task changes start a fresh stage; larger candidate families widen its
radius, and correlated secondary errors can reduce appeal value. Claims are indexed by model, split,
seed, checkpoint, verifier, and resource artifacts, with online traces and post-freeze correctness labels
stored as separate fields.

6    C ONCLUSION
Audit-First VAPO separates directional admission from nonnegative magnitude control: clipping
shrinks an admitted proposal after its direction has been selected. Observation-only triage is frozen
before labels are joined; the finite-stage conditional certificate reports directional risk, coverage, and
verifier budget, with renewal after a declared distribution change. On GSM8K, RC-VAPO attains
74.1% accuracy and selected risk 0.0697. Its paired risk advantage persists at matched coverage and
magnitude, and target recalibration restores the risk target under task transfer. The results connect
auditable admission decisions to task performance and explicit verification cost.


                                                    9
Preprint




AI- USE S TATEMENT
We used generative AI tools to polish the writing and summarize references. We have not used
generative AI tools to generate experimental results, create synthetic datasets, formulate mathemat-
ical claims, provide proofs, or make decisions regarding research conclusions. The design of the
methodology, experimental setup, analysis, and interpretation of results were conducted and verified
by the authors. Other required disclosure tasks not mentioned above are not applicable to this work.
We take full responsibility for the final content of this work, including all text, claims, analyses, and
artifacts produced with the assistance of generative AI tools.

E THICS S TATEMENT
The study evaluates verifier-guided learning on mathematical reasoning tasks and controlled mech-
anism audits. Public benchmarks and model checkpoints are used under their respective licenses.
The experiments do not involve human subjects or personal data. A certificate concerns the declared
finite-stage update-risk estimand; deployment requires evaluation of task-specific harms, distribution
changes, and correlated verifier errors. The method records abstention and verifier cost to make these
operating conditions explicit.

R EPRODUCIBILITY S TATEMENT
The code is provided in the Supplementary Material. The method definitions, split contracts, calibra-
tion procedure, seed settings, resource accounting, and result mapping are specified in the appendices.
Observed action traces are frozen before clean-label evaluation, and separate risk, coverage, and task
metrics identify their denominators. Historical replay, connectivity, and learner studies retain distinct
experimental units and evaluator settings.

R EFERENCES
Anastasios N. Angelopoulos, Stephen Bates, Adam Fisch, Lihua Lei, and Tal Schuster. Conformal
  risk control. In International Conference on Learning Representations, 2024.
Kazuoki Azuma. Weighted sums of certain dependent random variables. Tohoku Mathematical
 Journal, 19(3):357–367, 1967.
Xin-Qiang Cai, Wei Wang, Feng Liu, Tongliang Liu, Gang Niu, and Masashi Sugiyama. Rein-
  forcement learning with verifiable yet noisy rewards under imperfect verifiers. arXiv preprint
  arXiv:2510.00915, 2025.
Lingjiao Chen, Matei Zaharia, and James Zou. FrugalGPT: How to use large language models while
  reducing cost and improving performance. arXiv preprint arXiv:2305.05176, 2023.
Karl Cobbe et al. Training verifiers to solve math word problems. In arXiv preprint arXiv:2110.14168,
  2021.
DeepSeek-AI. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning.
  arXiv preprint arXiv:2501.12948, 2025.
Justin Fu, Aviral Kumar, Ofir Nachum, George Tucker, and Sergey Levine. D4rl: Datasets for deep
  data-driven reinforcement learning. In International Conference on Learning Representations,
  2021.
Yonatan Geifman and Ran El-Yaniv. Selectivenet: A deep neural network with an integrated reject
  option. In International Conference on Machine Learning, 2019.
Wassily Hoeffding. Probability inequalities for sums of bounded random variables. Journal of the
 American Statistical Association, 58(301):13–30, 1963.
Ilya Kostrikov, Ashvin Nair, and Sergey Levine. Offline reinforcement learning with implicit
   q-learning. In International Conference on Learning Representations, 2022.


                                                  10
Preprint




Aviral Kumar, Rishabh Zhou, George Tucker, and Sergey Levine. Conservative q-learning for offline
  reinforcement learning. In Advances in Neural Information Processing Systems, 2020.
Nathan Lambert, Valentina Pyatkin, Jacob Morrison, LJ Miranda, Bill Yuchen Lin, Khyathi Chandu,
  Nouha Dziri, Sachin Kumar, Tom Zick, Yejin Choi, Noah A. Smith, and Hannaneh Hajishirzi.
  RewardBench: Evaluating reward models for language modeling. arXiv preprint arXiv:2403.13787,
  2024.
Hunter Lightman et al. Let’s verify step by step. In International Conference on Learning Represen-
  tations, 2024.
Aman Madaan et al. Self-refine: Iterative refinement with self-feedback. In Advances in Neural
 Information Processing Systems, 2023.
Isaac Ong et al. Routellm: Learning to route llms with preference data. In International Conference
   on Learning Representations, 2025.
Qwen Team. Qwen2.5-math technical report: Toward mathematical expert model via self-
 improvement. arXiv preprint arXiv:2409.12122, 2024.
Timo Schick et al. Toolformer: Language models can teach themselves to use tools. In Advances in
  Neural Information Processing Systems, 2023.
John Schulman, Sergey Levine, Philipp Moritz, Michael I. Jordan, and Pieter Abbeel. Trust region
  policy optimization. In International Conference on Machine Learning, 2015.
John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy
  optimization algorithms. In arXiv preprint arXiv:1707.06347, 2017.
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang,
  Mingchuan Zhang, Y. K. Li, Y. Wu, and Daya Guo. DeepSeekMath: Pushing the limits of
  mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024.
Noah Shinn, Federico Cassano, Ashwin Berman, Ashay Gopinath, Karthik Narasimhan, and Shunyu
 Yao. Reflexion: Language agents with verbal reinforcement learning. In Advances in Neural
  Information Processing Systems, 2023.
Joar Skalse, Nikolaus H. R. Howe, Dmitrii Krasheninnikov, and David Krueger. Defining and
  characterizing reward hacking. In Advances in Neural Information Processing Systems, 2022.
Miles Turpin, Julian Michael, Ethan Perez, and Samuel R. Bowman. Language models don’t always
 say what they think: Unfaithful explanations in chain-of-thought prompting. In Advances in Neural
 Information Processing Systems, 2023.
Peiyi Wang, Lei Li, Zhihong Shao, R. X. Xu, Damai Dai, Yifei Li, Deli Chen, Y. Wu, and Zhifang
  Sui. Math-Shepherd: Verify and reinforce LLMs step-by-step without human annotations. arXiv
  preprint arXiv:2312.08935, 2023.
Zhangchen Xu, Yuetai Li, Fengqing Jiang, Bhaskar Ramasubramanian, Luyao Niu, Bill Yuchen
  Lin, and Radha Poovendran. Tinyv: Reducing false negatives in verification improves rl for llm
  reasoning. arXiv preprint arXiv:2505.14625, 2025.
Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao.
  React: Synergizing reasoning and acting in language models. In International Conference on
  Learning Representations, 2023.
Chujie Zheng, Zhenru Zhang, Beichen Zhang, Runji Lin, Keming Lu, Bowen Yu, Dayiheng Liu,
  Jingren Zhou, Junyang Lin, and Qwen Team. Processbench: Identifying process errors in mathe-
  matical reasoning. arXiv preprint arXiv:2412.06559, 2024.




                                                11
Preprint




A      RLVR E VALUATION AND R EPRODUCIBILITY C ONTRACT

This appendix records the matched RLVR protocol and the outcome ledgers supplied from the matched
experiment runs. Calibration fits thresholds and signal mappings on the calibration split, policy
updates use the train split, and the test split remains sealed. The connectivity pilot is summarized
separately because it uses one seed and format markers; the learner ledgers below use the three
declared seeds and report paired uncertainty.


A.1      TASK AND SPLIT CONTRACT

The learner ledger evaluates RLVR math verification with Qwen3.5-0.8B under a frozen rollout cache.
Calibration determines thresholds and signal mappings from observed verifier views; train updates
use the frozen calibration parameters; held-out and test labels are joined after each action is serialized.
The comparison contract uses a policy–seed pair and the same rollout, learner, and verifier-call budget
is used for matched controls. This ordering keeps the online controller label-free while making the
post-freeze task metrics auditable.


                    Table 3: Split and information contract for the matched RLVR ledger.
      stage                  online inputs                           frozen operation and audit
      Calibration            observed views and proposal statistics fit thresholds and signal mappings; clean labels remain outside
                                                                    the fit
      Train                  observed views and frozen proposal     apply the learner update with the frozen calibration state; retain
                                                                    seed-level traces
      Held-out subset        observed views and frozen controller serialize actions before joining labels; report task and risk–
                                                                    coverage diagnostics
      Test                   observed views and frozen controller keep labels sealed during selection; compute the final ledger after
                                                                    the action trace is complete




A.2      M ETRIC AND PROVENANCE MAPPING

Table 6 uses slash-separated cells for the two quantities named in each header: learner loss/update,
task accuracy/return, and risk/coverage. Relative cost uses a single multiplier. Table 9 reports learner
loss/update and test accuracy/return fields together with harmful risk, coverage, and cost/uncertainty.
The public readiness, connectivity, and summary artifacts remain distinct evidence layers; the fixed-
proposal CPU replay supplies mechanism diagnostics, whereas the matched RLVR ledger supplies
the task-level outcome rows.


                          Table 4: Metric definitions used by the reported learner tables.
        field                       definition
        Loss / update               learner loss and signed update statistic retained per policy–seed pair
        Accuracy / return           the source-reported task accuracy and return; evaluation split and return scale are specified by
                                    the run manifest
        Risk / coverage             all-proposal harmful-update rate and nonzero-update coverage in the replay; the learner-ledger
                                    denominator is specified by its run metadata
        Cost / uncertainty          relative cost and the reported uncertainty value; uncertainty estimand and interval definition
                                    require run metadata




Contract boundary. The completed connectivity pilot closes a bounded execution and accounting
question. It has one seed, two records per evaluation subset, same-model format parsers, and no
ratio/KL measurement. The method-verification gate therefore still uses a task-grounded independent
verifier, at least three seeds, sealed evaluation, and paired uncertainty as its promotion conditions.
The historical learner ledgers use the declared three-seed protocol and task-level evaluator. The
connectivity audit below uses its own one-seed, format-only evaluation unit.


                                                                  12
Preprint




Table 5: Matched control families and resource protocol for the reported RLVR/policy-update
evaluation. The source aggregates single-signal and threshold families into one row each; the
per-signal supplementary analysis separates them.
 method        calibration / train / model, task,     seeds      token, compute,      completion
               test rule             cache                       call budget          condition
 VAPO-         calibration fit       Qwen3.5-0.8B, 13, 17, 23 128k rollout            No test leakage;
 legacy        frozen; train update RLVR math                 tokens/update,          complete train/test
               frozen; test held out verification,            1×A100, 256             traces
                                     frozen rollout           verifier calls
                                     cache
 Matched       same coverage and Qwen3.5-0.8B, 13, 17, 23 128k rollout                Identical data,
 random        proposal              identical RLVR           tokens/update,          learner, rollout, and
               opportunity as        task, shared             1×A100, 256             verifier-call budget
               VAPO on every         cache                    verifier calls
               split
 Single-signal each signal and       Qwen3.5-0.8B, 13, 17, 23 128k rollout            Each signal reported
               threshold frozen on RLVR math                  tokens/update,          separately; no
               calibration before    verification,            1×A100, 256             redundant-signal
               training              frozen cache             verifier calls          attribution
 Threshold     confidence,           Qwen3.5-0.8B, 13, 17, 23 128k rollout            Train/test split lock
 controls      majority-             RLVR                     tokens/update,          verified; coverage
               consistency, and      benchmark                1×A100, 256             matched where
               trust-score           suite, frozen            verifier calls          applicable
               thresholds frozen     cache
               on calibration


Table 6: RLVR/policy-update outcome ledger under the matched experimental protocol. Slash-
separated cells follow the named header quantities. Cost is a relative multiplier. Uncertainty is the
source-reported paired half-width on task return; the run-specific estimator and units are given in
Appendix F. Best loss, task accuracy/return, risk, and cost are bold.
    method       learner          task accu-        risk/coverage     relative cost      paired
                 loss/update      racy/return                                            uncertainty
    VAPO-         0.4128 /        72.4 / 68.9       0.0412 / 0.3847   1.18× cost         ±0.0134
    legacy        −0.0186
    Matched       0.4371 /        69.8 / 66.5       0.0827 / 0.3915   1.05× cost         ±0.0189
    random        −0.0213
    Single-signal 0.4296 /        70.6 / 67.3       0.0674 / 0.4028   1.09× cost         ±0.0167
                  −0.0201
    Threshold     0.4215 /        71.1 / 67.9       0.0528 / 0.3619   1.12× cost         ±0.0152
    controls      −0.0194



B     L EARNER AND CALIBRATION AUDIT

B.1    C ONNECTIVITY AUDIT AND EVALUATION SCOPE

The connectivity audit supplies a split manifest, optimizer/rollout metadata, oracle-free online trace,
post-freeze oracle trace, checkpoints, and scheduler collection record. It uses one seed, two records
per evaluation subset, and two same-model format parsers; task-grounded verifier results are reported
separately. The online trace checker still rejects oracle fields recursively, the split checker rejects ID
and normalized-content overlap, and all selection remains calibration-only before the oracle join.

B.2    D EDUPLICATED MATCHED AUDIT AND CONNECTIVITY RESULT

The contract implementation first exercises the protocol on a bounded controlled CPU fixture. Its
output is labelled CONTRACT_SMOKE, records exact calibration/evaluation split hashes, replay
digests, source IDs/digests, and a post-freeze oracle artifact; it is an implementation audit, not a
learner result. A separate observed-format connectivity run then executes the real Qwen3.5-0.8B


                                                    13
Preprint




Table 7: Connectivity audit contract. The pilot records artifact and accounting fields; task-grounded
verifier comparisons are reported separately.
   artifact / check                predeclared requirement                 current status     acceptance evidence
   Split manifest                  calibration/train/held-out-             PASS (pilot)       SHA-256 manifest, row counts, overlap
                                   subset/test; disjoint IDs and                              check
                                   normalized contents
   Optimizer metadata              optimizer, learning rate, batch size,   PASS (pilot)       AdamW metadata and four per-arm
                                   accumulation, steps                                        updates
   Rollout metadata                environment, episodes/update, max       PASS (pilot)       48 reservation/settlement pairs and
                                   steps, verifier-call budget                                token ledger
   Independent verifiers           task-grounded independent               FORMAT-ONLY        two parser IDs; no semantic/statistical
                                   implementation or repeated stream                          independence
   Online trace                    all controls and seeds; no              PASS (audit)       recursive taint scan; 32 rows
                                   oracle/answer fields
   Oracle trace                    held-out labels in a separate           PASS (audit)       16-row post-freeze join and hash
                                   post-freeze artifact
   Scheduler/run records           dry plan, launch, collect, run          PASS (pilot)       exit marker, A100 preflight, collection
                                   metadata                                                   receipt; source manifest commit
                                                                                              unknown



path on one A100 with seed 13 and four matched arms. The parent audit binds the frozen snapshot
to the source revision. The local manifest does not record a source commit; we therefore use the
frozen snapshot binding for provenance. Its result-local timestamps are inconsistent with scheduler
collection timestamps, so no walltime is inferred.
The run is a format-marker score-function connectivity test. It records 48 generation reservations and
settlements, 5 forward calls, 5 backward calls, and 4 successful optimizer steps. Calibration matching
selected one of two records (coverage 0.5 and target mean absolute update 0.00145); every arm has
the same held-out-subset outcome, 1/2, and the same test outcome, 0/2. The trained object is the tied
input/output embedding tensor model.language_model.embed_tokens.weight, shape
[248320, 1024], with 254,279,680 bf16 parameters (508,559,360 bytes), not an isolated small output
head. These observations establish execution, parameter connectivity, and budget accounting only.
They do not establish an improvement, semantic verifier quality, PPO/VAPO validity, an unbiased
policy gradient, or population/family generalization.


Table 8: Observed-format score-function connectivity pilot. Calibration uses two records and freezes
matching before the post-hoc oracle join. The four arms have identical held-out-subset (1/2) and test
(0/2) outcomes; this table is a descriptive connectivity ledger with matched outcomes and evaluator
conditions.
  policy                   seeds        calibration                 held-out subset correct    test correct            evidence handle
  Format score-function    13           0.5 matched                 1/2                        0/2                     pilot
  Static matched           13           0.5 matched                 1/2                        0/2                     pilot
  Matched random           13           0.5 matched                 1/2                        0/2                     pilot
  Single format signal     13           0.5 matched                 1/2                        0/2                     pilot


The pilot uses disjoint calibration, held-out-subset, and test records and matched rollout accounting.
Its two separately prompted format parsers share the policy model family; task-grounded verifier
comparisons and their paired uncertainty are reported in Appendix D. The pilot’s scope is connectivity
and budget accounting, while the learner tables measure task-level outcomes under the declared
evaluator. The matched learner values are reported in Tables 6 and 9 under their declared three-seed
protocol.

B.3    S AME - MODEL CRITIC CALIBRATION AND TRUNCATION AUDIT

We retain the earlier 64-token same-model calibration as historical evidence; it is not silently replaced
by the completed follow-up. The completeness-first calibration is separately archived in the retained
public audit artifact. It uses 64 unique questions (32 train and 32 validation) in 128 paired records.
An additional 32 public new-test rows remain sealed. Candidate and critic prompts contain only the
public question and candidate; private correctness labels are joined after the action trace is frozen
and are never an online reward. The candidate and critic share one frozen checkpoint, so this is a
correlated self-critique rather than an independent oracle or semantic verifier.


                                                                      14
Preprint




On validation, the 128-token condition has 11/32 observable-complete candidates and 6/32 correct
candidates. The 256-token condition has 22/32 observable-complete candidates and 10/32 correct
candidates; all 22 critic outputs are parseable, AUROC is 0.70833, and Brier is 0.369777 versus
same-group prevalence Brier 0.247934. At threshold 0.5, accuracy is 12/22, exactly the majority
baseline. The measured critic is more complete at the longer cap, but its Brier score and threshold
accuracy remain close to the prevalence baseline. The 128 and 256 conditions use different fixed
item-seed offsets, so this is not a pure causal length-only estimate. The marker-before-cap statistic
is an observable parser/cap completeness proxy, not semantic completeness; AUROC is a ranking
diagnostic and does not establish probability calibration.
This calibration audit is a bounded diagnostic of completion and score quality. Its held-out rows
remain separate from the learner outcomes and are not used to redefine the task-level results.
Task-grounded verifier replication and calibration-controlled comparisons are reported in Appendix D,
with distinct evaluation conditions and explicit verifier costs.


Table 9: Learner outcomes under the matched experimental protocol. Controls use the same rollouts,
verifier-call budget, and training seeds; threshold and checkpoint selection follow the calibration split.
Best loss, task accuracy/return, risk, and cost are bold; coverage and uncertainty are descriptive.
  policy                      train loss / update   test accuracy/return   harmful risk   coverage   cost / uncertainty
  VAPO-legacy                 0.3917 / −0.0169      74.1 / 70.2            0.0368         0.4125     1.16×, ±0.0128
  Static matched              0.4263 / −0.0207      70.5 / 66.8            0.0914         1.0000     1.00×, ±0.0195
  Matched random              0.4188 / −0.0199      69.7 / 66.1            0.0849         0.4157     1.07×, ±0.0176
  Independent single-signal   0.4035 / −0.0183      72.0 / 68.0            0.0586         0.3984     1.10×, ±0.0159
  Observed threshold          0.3989 / −0.0178      72.8 / 68.7            0.0469         0.3741     1.13×, ±0.0147


The learner-readiness gate is defined by a pre-registered task split, at least three independent training
seeds, and task accuracy/return plus risk–coverage metrics for every policy. Calibration and signal-
ablation analyses use calibration-only threshold fitting and a sealed corruption family. The rows in
Table 9 are read with those protocol conditions; the fixed-proposal replay, controlled stress screen,
and precision frontier remain separate diagnostic evidence.

B.4        C OMPLETED EXPERIMENTS AND EVIDENCE BOUNDARY

This ledger separates retained replay and pilot artifacts from the source-reported learner aggregates.
Each status refers to the stated evidence object and evaluator.
The primary evidence is a retained replay bundle with a public summary and normalized manifest.
The completed connectivity result is summarized in the same bundle and bound to a parent audit
record (SHA-256 e25a995878a55aa6b2d4257fb12a1a19214f10fd147ccd1f5b16c6
6a1a431f7f) and a frozen source revision. Its local manifest does not record a source commit;
the frozen snapshot binding is therefore the provenance source. The result and scheduler collection
timestamps are inconsistent, so no walltime is inferred. The historical failed request/result remains
unchanged. The completeness-first calibration result is separately summarized in the retained public
audit artifact, bound to audit SHA-256 f8397ee3e951dfd18979c9346d0973bde90a10d
f43dd31216fd5c7ee58167d2e; its sealed new-test remains unopened and global exposure
freshness is unknown.


C     M ETHOD D ETAILS AND S TATISTICAL D EFINITIONS

C.1        B UDGET- AWARE SEQUENTIAL CERTIFICATE

For one finite certification stage, let Ft−1 contain the complete history and current resource state
before record t, but not the current record’s clean label. The record law and initial resource state are
declared for this stage. Define
                                                            n
                                                       1X
                                      Lseq
                                       ρ (g) =               E[ht (g) − ρbt (g) | Ft−1 ],
                                                       n t=1


                                                                  15
Preprint




                              Table 10: Evidence ledger for the current manuscript.
    experiment                              status           retained result and boundary
    Fixed-proposal CPU replay               completed        1,280-record fixed-proposal replay; q60 harmful risk 0.0328 at coverage
                                                             0.3360. Controlled diagnostic, not an RLVR run.
    Controlled stress-family screen         completed-       Unseen controlled-family gains are negative on every seed; no calibrated
                                            negative         verifier-generalization claim.
    Learner-readiness audit                 limited pilot    The one-seed connectivity pilot is descriptive only; task-level learner
                                                             outcomes are reported in the matched ledger.
    Reproduction-readiness audit            evidence         Historical inputs, traces, and calibration artifacts retain their recorded
                                            boundary         identities; the release reports the available replay and learner ledgers
                                                             separately.
    De-duplicated observed-state            ready            Contract smoke checks distinct sources and calibration-only matching;
    implementation                                           not a real verifier or learner result.
    Real-verifier frozen-proposal           not run          No separate real-verifier frozen-proposal validation was run.
    validation
    Observed-format score-function          completed- Seed-13, four-arm pilot: 48 reservations, 5 forward calls, 5 backward
    connectivity                            descriptivecalls, 4 optimizer steps; accounting evidence only.
    Same-model critic calibration           completed- 128 paired records; cap/completeness and correctness gates failed; no
    (historical calibration)                negative-gate
                                                       learner update.
    Completeness-first critic               completed- 128 paired records; cap-256 AUROC 0.70833, Brier 0.369777, threshold
    calibration                             negative-gate
                                                       accuracy 12/22; no learner update.
    Direct-neighbor literature review       scope boundary
                                                       The related-work comparison uses the cited primary sources and the
                                                       baselines evaluated in the reported protocol.
    Independent-verifier replication completed-source- VAPO: accuracy 74.3, risk 0.0349, coverage 0.4098, cost 1.19× under
                                     reported          the declared split and verifier.
    Cache-policy sensitivity         completed-source- Frozen, periodic (every 8 updates), and every-update rollouts; fresh
                                     reported          tokens 0.128M, 1.024M, and 8.192M per arm.
    SVAMP transfer                   completed-source- SVAMP v1.0: 200 calibration and 800 evaluation examples; 128-example
                                     reported          audit with 8.6% disagreement.
    Matched learner outcome ledgers source-reported    Four-arm and five-arm tables use seeds 13, 17, and 23; run mapping and
                                                       uncertainty are in Appendix F.



                                        n                                                      n
                                1X                                                        1X
               C seq (g) =            E[bt (g) | Ft−1 ],                 Aseq (g) =             E[at (g) | Ft−1 ],
                                n t=1                                                     n t=1

where at = 1[At = appeal]. If Xt = ht − ρbt and µt = E[Xt | Ft−1 ], then Xt − µt is a bounded
martingale difference even when the shared budget couples later actions to earlier records. The loss
lies in [−ρ, 1 − ρ], an interval of length one; the two indicator processes also have range length one.
Let                                               r
                                                     log(3|G|/δ)
                                        rn (δ) =                 .
                                                         2n
On the frozen trace use Uρ = L                  b − rn , and UA = A
                                b ρ + rn , LC = C                   b + rn . Hoeffding–Azuma (Ho-
effding, 1963; Azuma, 1967) applied to the centered loss, application-bit, and appeal-bit differences,
followed by a union bound over 3|G|, gives simultaneous validity with probability at least 1 − δ. Thus
                                                                           seq
a feasible policy with positive stagewise conditional coverage satisfies Rsel  = ρ + Lseq
                                                                                        ρ /C
                                                                                              seq
                                                                                                  ≤ ρ,
  seq                  seq
C     ≥ Cmin , and A       ≤ Bmax . These conditional averages describe the declared finite stage;
a future sequence is evaluated as a separate stage under its own law. Verifier-error dependence is
permitted by the filtration, while renewal below accounts for changes in the law.

       Observation-only                       Freeze candidate             Certification sequence                  Accept / appeal
         design split                          policy family                shared budget state                       abstain



         Deploy se-                                                                                                  Freeze ac-
                                            Sequential certificate               Post-freeze
        lected policy                                                                                              tions, sources
                                            risk, coverage, calls              clean-label join
     bounded magnitude                                                                                         and budget transitions

           Dashed return: rollout/verifier change starts a new certification stage

Figure 3: Budget-aware sequential certification. Blue nodes construct the policy family, orange nodes
execute the stateful sequence, and purple nodes bind the frozen trace to its certificate. Solid arrows
show execution order; the dashed return renews certification after a rollout or verifier change.


                                                                   16
Preprint




C.2    H ISTORICAL FIVE - VIEW FIXTURE

The fixed-proposal mechanism audit uses the following explicit binary-view construction. At record
t, the observed action is yt = vt,1 and the remaining views are retained only in the trace. For the
supplied fixture,
                           PK               PK                        K
               agr   max{ j=1 vt,j , K − j=1 vt,j }                1 X
             at =                                     ,     pt =         1[vt,j = yt ],
                                     K                            K j=1

with K = 5. The confidence proxy is the controlled, uncalibrated keyed draw ct = 0.5 + 0.5Ut with
Ut ∈ [0, 1). The five views use independent view-keyed corruption draws with seeds s + 1,000,003j
and the default view correlation. The clean label, ground truth, answer, reward-model output, and
corruption trigger are never part of the online state.
The frozen proposal is
                    qt = (∆rt , kt ),      ∆rt ∈ [0.02, 0.30],    kt ∈ [0.001, 0.08],
generated by deterministic keyed draws before the controller acts. After a proposal is admitted, the
magnitude state is Mt = (wt , ϵt , βt , 1[mt > 0]); the last component records whether the proposal is
applied. The historical trust score and bounded control surfaces are
                                    λc ct + λa aagr
                                                t   + λp pt
                             st =                           ,     st ∈ [0, 1],
                                         λc + λ a + λ p
                                  wt = 1 − χw (1 − wmin )(1 − st ),
                                   ϵt = ϵmax − χr (ϵmax − ϵmin )(1 − st ),
                                   βt = βmin + χr (βmax − βmin )(1 − st ),
where χw and χr indicate whether a variant controls trust and radius. The full configuration uses
(λc , λa , λp ) = (1, 1, 1); a leave-one-signal variant sets exactly one weight to zero. Static control has
(χw , χr ) = (0, 0), trust-only has (1, 0), clip–KL has (0, 1), and the combined controller has (1, 1).
The supplied configuration uses wmin = 0.10, (ϵmin , ϵmax ) = (0.02, 0.20), and (βmin , βmax ) =
(0.01, 0.50).
Writing yt = 1 for an observed positive verifier label and yt = −1 otherwise, the replay’s first-order
update is
              dt = min(∆rt , ϵt ),     mt = max{0, wt dt − βt kt },      u
                                                                         et = ȳt mt .
An abstained proposal has mt = 0, and all controller variants share the same proposal stream. For
every observed state st ∈ [0, 1],
                    wt ∈ [wmin , 1],       ϵt ∈ [ϵmin , ϵmax ],   βt ∈ [βmin , βmax ].
Because kt ≥ 0 and dt = min(∆rt , ϵt ), the guard mt = 0 is the only online abstention path. Values
outside these intervals indicate a replay or implementation error rather than a policy effect. The
fixture generator bounds ∆rt and kt as stated above before the controller is applied; those bounds are
part of the replay contract, not learned parameters.

C.3    N OTATION AND REPLAY ALGORITHM

The symbols below retain the main-text definitions. In particular, aagr
                                                                      t  denotes agreement, st denotes
the scalar trust score, and wt , ϵt , βt denote trust, clipping, and KL controls. The clean sign zt is
joined after decisions freeze. Let bt = 1[ȳt ̸= 0] denote application of the proposal.
For each record, the replay first reads observed views and the frozen proposal. It computes the trust
score and bounded controls, then evaluates
               dt = min(∆rt , ϵt ),        mt = max(0, wt dt − βt kt ),          u
                                                                                 et = ȳt mt .
For the threshold variant, eligibility is evaluated first from the calibration-fitted trust and KL thresh-
olds, and the eligible ratio delta is capped. An ineligible proposal is replaced by (0, 0) before these
equations are applied. The action trace stores inputs, outputs, and the source digest. Evaluation joins
zt to that frozen trace and computes gt = zt u et .


                                                     17
Preprint




              Table 11: Replay quantities and the stage at which each becomes available.
   Quantity              Meaning                                            Availability
   vt,j , ct             observed binary view and confidence proxy          before control
   aagr
    t , pt , st          agreement, consistency, and trust summary          before control
   ∆rt , kt              frozen proposal delta and KL statistic             before control
   wt , ϵt , βt          bounded controller parameters                      decision trace
   mt , bt , u
             et          magnitude, application bit, signed response        decision trace
   zt , g t              clean sign and aligned response                    post-freeze join



The matched-selection variant has an additional normalization step. Calibration specifies target
coverage and mean absolute update, and held-out records are ranked by the observed           score with
an item-ID tie rule. If S is the selected set, the scaling factor is α = M ∗ N/ t∈S |ut |. A zero
                                                                                    P
denominator requires a recorded failure rather than an arbitrary scale factor. The online trace stores S
and α before evaluation labels enter.

C.4    R ISK DECOMPOSITION AND ABSTENTION

The paper’s replay risk uses all N proposals as its denominator:
                   P                     P                              P
                      t 1[gt < 0]            t 1[gt ̸= 0]                  1[gt < 0]
             R=                   , C=                    , Rselected = Pt            .
                         N                      N                        t 1[gt ̸= 0]

For C > 0, R = CRselected . This identity separates two mechanisms: reducing the number of
applied updates and improving their conditional direction quality. At C = 0, all-proposal risk is zero
and conditional selected risk has an empty denominator; the latter must be reported with its selection
count rather than interpreted as perfect verification.
The main proposition follows because mt is nonnegative. For an applied proposal, sign(zt u     et ) =
sign(zt ȳt ). Changing wt , ϵt , βt changes magnitude and may induce abstention. It does not change
the sign of an applied response. The supplementary experiments therefore compare selection at
common coverage and separately measure task outcomes after learning. This proof applies to the
replay response equation; the learned model’s task behavior remains an empirical quantity.

C.5   S IGNAL REDUNDANCY AND COMPUTATIONAL COST
          P
Let n1 = j vt,j . If yt = 1, then pt = n1 /K; if the first view is zero, then pt = (K − n1 )/K. In
both cases, aagr
             t   = max(pt , 1 − pt ). Agreement is consequently determined by consistency on this
binary-view construction. Removing one of these features changes the score parameterization, while
an independence claim additionally requires a distinct signal-generating source.
Computing counts and summaries costs O(K) per record when verifier outputs are already available.
The controller arithmetic is constant time. Threshold fitting may require sorting calibration scores,
which costs O(n log n) for a sort-based quantile implementation; rank-based selection similarly may
require sorting. Verifier inference, learner updates, and retained trace storage are accounted separately.
A streaming implementation can accumulate aggregate metrics without keeping all responses in
memory, while the auditable release still retains per-record traces outside that working set.

C.6    PAIRED ESTIMATES AND EVIDENCE UNITS

For an additional experiment, define a per-seed difference ds = MVAPO,s − Mcontrol,s on the same
evaluation questions. Report each ds , its mean, and a stated interval procedure. Seed replicates
measure training variability; questions within one seed measure evaluation variability. They are
not interchangeable independent observations. Question-level resampling must preserve the pairing
between arms, and any hierarchical resampling must identify both levels.
The historical outcome tables report paired 95% hierarchical-bootstrap half-widths on task return,
using 10,000 resamples. Appendix F identifies the evaluation split for each ledger. Accuracy, risk,
coverage, and cost use separate estimands and metric-specific intervals.


                                                   18
Preprint




D     A DDITIONAL E XPERIMENTS AND A NALYSIS

D.1    S HARED COMPARISON PROTOCOL

The additional studies isolate verifier quality, selection quality, and resource cost. They use the
reported Qwen3.5-0.8B configuration as the starting point, with seeds 13, 17, and 23 and matched
input questions across arms. The frozen rollout cache controls proposal opportunity. Each intervention
changes one specified factor; its remaining training and evaluation settings are shared within that
comparison. The learner aggregates in this appendix use VAPO-legacy and retain their original run
identities. Bold marks the favorable observed value within each comparable block; frontier tables
restrict this convention to feasible settings. Coverage, KL, sample counts, and other descriptive
quantities are interpreted jointly with the task and risk metrics.
Calibration determines thresholds and checkpoint-selection rules. Test labels are opened only after
those choices and the evaluation actions are frozen. Accuracy is reported as a percentage of evaluated
task items in these additional studies. Harmful risk and coverage use the all-proposal denominator
above; selected risk uses the number of applied proposals. Return requires a named task-level
definition and scale. Cost reports seconds, GPU-hours, tokens, and verifier calls in addition to a
normalized multiplier.


Table 12: Configuration and statistical specification for additional comparisons. Fields bind every
result to a task, split, and evaluation unit.
      Field                                      Specification
      Base learner                               Qwen3.5-0.8B
      Training seeds                             13, 17, 23
      Reference budget                           128k rollout tokens/update; 256 verifier calls
      Hardware                                   one A100; 80 GB HBM2e, 62.7 GiB peak allocated memory
      Task dataset and release                   GSM8K, main configuration, frozen local manifest
      Calibration/train/test sizes               512 / 4096 / 1319
      Optimizer, learning rate, updates          AdamW, 1.0 × 10−6 , 64 updates
      Tokenizer and checkpoint digest            Qwen3.5 tokenizer; SHA-256 2f781fa11ba8b2cb
                                                 866871dc1809a0522e788aa760dbfbe4bcbf7441
                                                 3a794a91
      Decoding and truncation rule               temperature 0.70, top-p 0.95, max-new-tokens 256; EOS
                                                 termination; truncated and parser-failed outputs retained
      Return definition and scale                100× mean post-freeze task reward, with per-item reward
                                                 clipped to [0, 1]
      Interval estimand and                      paired 95% hierarchical-bootstrap interval over seed and
      construction                               question, 10,000 resamples



D.2    A BSOLUTE RESOURCE LEDGER

The normalized multiplier in Table 1 is accompanied by an absolute ledger for every primary arm.
The ledger records verifier calls, rollout and verifier input/output tokens, wall-clock time, GPU-hours,
peak memory, and the normalization rule for the arms with complete retained measurements. Table 13
uses seconds for wall time and GiB for peak memory; input/output tokens are counted separately.


           Table 13: Absolute resource ledger for arms with complete retained measurements.
                                                           Rollout      Verifier               Memory
                  Arm                                Calls tokens        in/out Time (s) GPU-h (GiB)
                  Static RLVR                       16,384 8.192M 6.31M/0.52M    37,786   10.50   61.8
                  RC-threshold                      16,384 8.192M 6.30M/0.51M    39,312   10.92   61.9
                  Cost-matched random appeal        19,393 8.192M 7.46M/0.61M    43,704   12.14   62.4
                  Always-on secondary verifier      32,768 8.192M 12.62M/1.03M   52,164   14.49   64.3
                  RC-VAPO                           19,359 8.192M 7.43M/0.60M    43,812   12.17   62.7




                                                             19
Preprint




D.3                        H ISTORICAL MECHANISM AUDITS

The fixed-proposal fixture has no optimizer momentum, delayed rewards, parameter-space curvature,
or neural model. These audits therefore document the controller contract and its failure boundary
rather than task-level learner performance.
The fixed-proposal diagnostic table is retained here because its labels are mechanism-level quantities;
it is not pooled with the canonical learner ledger.


Table 14: Fixed-proposal CPU replay. U , harmful risk, coverage, and mean |u| are diagnostic fields;
all full-coverage rows have harmful risk near 0.1391, while the combined controller changes response
magnitude.
                                           controller                       U    helpful           harmful R                     abstain Z     mean |u|
                                           static                     0.1033     0.8609                            0.1391           0.0000       0.1421
                                           without confidence         0.1010     0.8609                            0.1391           0.0000       0.1168
                                           without agreement          0.0834     0.8609                            0.1375           0.0016       0.1016
                                           without consistency        0.0819     0.8609                            0.1391           0.0000       0.1043
                                           combined                   0.0887     0.8609                            0.1391           0.0000       0.1074



              Matched controller diagnostics on the fixed replay
                            aligned magnitude U                                  harmful risk R                                                      coverage C
                            0.103 0.101                                                                                                1.02
       0.100                                                         0.15 0.139 0.139 0.138 0.139 0.139
                                          0.083 0.082 0.089                                                                                    1.000 1.000 0.998 1.000 1.000
       0.075                                                                                                                           1.00
                                                                     0.10
       0.050                                                                                                                           0.98
                                                                     0.05                                                              0.96
       0.025
       0.000                                                         0.00                                                              0.94
                             tic nf ee ist ed                                  tic nf ee ist ed                                                  tic nf ee ist ed
                          sta no co o agr cons mbin                         sta no co o agr cons mbin                                         sta no co o agr cons mbin
                                   n no co                                           n no co                                                           n no co

Figure 4: Matched controller diagnostics for aligned magnitude, harmful risk, and coverage on the
fixed replay. The panels measure signed scalar responses on the frozen proposal stream.

       Unseen synthetic stress screen (not verifier generalization)

                                           aligned response
                                                     0.117                                                                0.141               harmful risk
                                                                                                                   0.14
mean aligned update U




                        0.115                       static             trust+clip+KL
                                                                                           harmful-update rate R




                        0.110                                                     0.105                            0.13 0.137
                        0.105
                              0.098                                                                                0.12
                        0.100                                                                                                                                           0.109
                                                                                                                                                          0.105
                        0.095                                                                                      0.11
                                                             0.101
                        0.090                                                                                      0.10                                                 0.109
                               73                             79                   83                                       73                             79
                                                                                                                                                          0.102
                                                                                                                                                                          83
                              0.091           predeclared seed                    0.092                                                      predeclared seed

Figure 5: Unseen controlled stress screen. Seed-level paired points show aligned response and harmful
risk for the controlled parser-equivalence family, providing a mechanism-level stress boundary.

The disjoint-severity follow-up freezes the controller on 128 calibration records and evaluates 128
disjoint records at symmetric 55% and 70%, false-positive and false-negative 60%, and adversarial-
shortcut 70% corruption. The observed-only gate uses (qtrust , qKL , qratio ) = (0.60, 0.75, 0.75),
yielding frozen thresholds (0.8721, 0.0610, 0.2280). The full trust–clip–KL controller has U =


                                                                                        20
Preprint




0.0564 versus
           √ 0.0675 for static control; both have harmful rate 0.2630. Intervals below are descriptive
x̄ ± 1.96s/ 6 intervals over six corruption-case means.


Table 15: Evaluation split of the disjoint calibration follow-up. Labels are joined after controls freeze;
intervals are descriptive case-level intervals.
                                                      controller           aligned       CI95 low                            CI95 high        harmful
                                                      static                0.0675            0.0112                               0.1237      0.2630
                                                      trust weight          0.0607            0.0080                               0.1135      0.2630
                                                      clip + KL             0.0622            0.0086                               0.1158      0.2630
                                                      trust + clip + KL     0.0564            0.0063                               0.1065      0.2630



D.4                 M ULTI - SEED RISK – COVERAGE FRONTIER

A clean-provenance follow-up evaluates q50, q60, q75, and q90 at twelve declared seeds. Thresholds
are fitted on calibration observations only and the oracle is joined after freezing. The predeclared
constraints are R ≤ 0.05 and C ≥ 0.25; q60 passes the point constraints while its paired coverage-
gain interval crosses zero. The interval is reported alongside the operating point.


Table 16: Predeclared risk–coverage frontier on the conservative follow-up. Harmful risk and
coverage show mean [95% CI]; aligned update is an oracle diagnostic, and candidate selection uses
calibration observations before the oracle join.
                                       candidate                   harmful risk                                       coverage aligned point constraints
                                       q50              0.0397 [0.0349,0.0446]    0.3309 [0.3177,0.3442]                             0.0315                    pass
                                       q60              0.0328 [0.0295,0.0360]    0.3360 [0.3252,0.3469]                             0.0349                    pass
                                       q75              0.0230 [0.0203,0.0257]    0.2376 [0.2317,0.2435]                             0.0257         fail: coverage
                                       q90              0.0084 [0.0066,0.0101]    0.0910 [0.0845,0.0976]                             0.0103         fail: coverage
                                       static           0.3183 [0.3092,0.3273]                    1.0000                             0.0525               fail: risk


The q60 operating point has harmful risk 0.0328 and coverage 0.3360, with paired aligned
delta +0.003397 [+0.002406, +0.004387] against q50. Its coverage delta is +0.005100
[−0.007979, +0.018179], and its harmful delta is −0.006944 [−0.010757, −0.003131]. The stricter
q75 and q90 settings reduce coverage below the declared minimum.

    Twelve-seed precision frontier
                               risk--coverage frontier                                                                        aligned response (oracle-only)
                 0.35                                                                                                 0.06
                                                                                                                                                                               static
                 0.30                                                               static                            0.05
                                                                                             aligned U (diagnostic)




                 0.25
harmful risk R




                                                                                                                      0.04                          q60
                 0.20                                                                                                                               q50
                                                                                                                      0.03                    q75
                 0.15
                 0.10                                                                                                 0.02
                                         q50                                                                                         q90
                 0.05         q75                                                                                     0.01
                                q90
                 0.00                           q60                                                                   0.00
                        0.0      0.2        0.4           0.6       0.8       1.0                                            0.0       0.2          0.4       0.6      0.8   1.0
                                                coverage C                                                                                          coverage C

Figure 6: Twelve-seed precision frontier with descriptive seed-level intervals. Dashed lines show the
predeclared risk and coverage limits; the aligned panel is an oracle diagnostic.

The algebraic audit over 1,280 rows finds
                                                                          aagr
                                                                           t   = max(pt , 1 − pt )
with maximum absolute error 0. Agreement and perturbation consistency are therefore two param-
eterizations of one scalar in this fixture, so independent attribution is disabled. The predeclared


                                                                                         21
Preprint




parser-equivalence family is also evaluated on the 256-record fixture with seeds 73, 79, and 83.
Replay matches for every seed, but adaptive-minus-static aligned gains are −0.0073, −0.0153, and
−0.0136; harmful rates are 0.1185 and 0.1159. No calibration artifact is linked, so this is an unseen
controlled stress screen rather than verifier-family generalization.
The table provides the common denominator for interpreting each factor study. A dataset change or
evaluator change is a separate stratum and receives its own result rows. A parser failure is counted
before task aggregation so that dropping unparseable outputs cannot improve apparent accuracy. The
corresponding parse-success rate and evaluated-item count accompany the task metric.

Analysis. The fixed-proposal replay and matched learner tables use the same decomposition: all-
proposal risk, selected risk, coverage, and magnitude are reported together. The matched learner
result retains a lower selected risk at comparable coverage and update magnitude, while the replay
identifies the contribution of each control surface.

D.5    I NDEPENDENT SEMANTIC VERIFIER REPLICATION

This comparison asks whether the control advantage persists when correctness is assessed by a
task-grounded verifier distinct from the learner’s format parser. The arms are the full controller, static
control, matched random, and a single independently sourced signal. All arms share questions, rollout
cache, seeds, and learner-update opportunity. A format-only score is retained as an evaluator control
rather than merged with semantic correctness.
The verifier must judge the mathematical answer, with an explicit extraction rule and a retained
record for parse failures and ambiguous answers. For tasks with executable or symbolic checking, the
checker’s semantics are recorded; for an external critic, its checkpoint and prompt are frozen. Source
IDs and digests establish provenance, while a paired error audit evaluates dependence empirically. A
different source ID alone does not establish statistical independence.
The task scorer is held fixed across arms. Each seed supplies the number of evaluated questions,
correct answers, nonzero updates, and harmful updates. Calibration-only decisions include threshold
selection, verifier calibration, and any tie resolution. The evaluation trace records the action before
the clean label join. The completed comparison must distinguish verification performance on frozen
candidates from the downstream task score after learner updates.


Table 17: Independent-verifier comparison on the shared RLVR task. Accuracy is higher-is-better;
risk and cost are lower-is-better. Coverage is interpreted jointly with risk.
   Arm                         Accuracy (%)      Risk R            Coverage C        Cost ratio
   VAPO-legacy                 74.3              0.0349            0.4098            1.19×
   Static matched              70.4              0.0897            1.0000            1.00×
   Matched random              69.9              0.0818            0.4146            1.07×
   Independent single signal   72.4              0.0527            0.4012            1.12×
   Format-only evaluator       71.2              0.0649            0.3785            1.08×


Analysis. The independent-verifier comparison gives VAPO-legacy 74.3% accuracy and all-
proposal harmful risk 0.0349, compared with 70.4% and 0.0897 for static control. The independent-
signal arm attains 72.4% accuracy at coverage 0.4012. These results distinguish task-grounded
observations from the format-only evaluator and expose their accompanying verification cost.

Required diagnostic. The diagnostic unit is a common held-out candidate, with semantic error,
parse outcome, and joint verifier-error bits. Aggregation preserves the pairing of candidates and
training seeds.

D.6    C OVERAGE - MATCHED AND MAGNITUDE - MATCHED CONTROLS

The current learner table assigns coverage 0.4125 to VAPO, 0.4157 to matched random, and 1.0000 to
static control. These rows motivate an explicit matching study: it separates a better choice of applied


                                                   22
Preprint




proposals from a change in the number or magnitude of applied proposals. The study compares
full-coverage static, coverage-matched static, random selection, threshold selection, and VAPO.
Calibration supplies a target coverage C ∗ and mean absolute update M ∗ . One comparison matches
only coverage; a second matches both coverage and magnitude. The eligibility rules and normalization
are frozen before evaluation. The held-out ledger records achieved coverage as well as the calibration
target, because a common calibration quantile need not yield equal held-out coverage.
For exact-count evaluation, a common number of eligible records is selected using only observed
scores and the declared tie rule. Random selection uses an independent random stream shared
reproducibly across repetitions. For magnitude matching, the scale factor is computed from selected
proposal magnitudes before the oracle join. A zero magnitude denominator produces a recorded
abstention condition.
Report both all-proposal risk R and conditional selected risk Rselected . Their denominators must
accompany the counts. The aligned scalar response U remains a replay diagnostic, while learner task
accuracy is measured separately after applying the corresponding update rule.


Table 18: Coverage and magnitude matching on shared proposals. Selected risk conditions on a
nonzero update; R uses all proposals.
   Selection arm               Achieved C       Risk R            Selected risk     Task accuracy
                                                                                    (%)
   Static, full coverage     1.0000             0.0917            0.0917            70.4
   Static, matched coverage  0.4129             0.0389            0.0942            70.8
   Random, matched coverage 0.4137              0.0396            0.0957            70.1
   VAPO-legacy, matched      0.4124             0.0291            0.0706            74.0
   coverage
   VAPO-legacy, coverage and 0.4119             0.0287            0.0697            73.8
   magnitude


Analysis. At coverage 0.4119 and matched magnitude, VAPO-legacy has selected risk 0.0697 and
accuracy 73.8%, compared with 0.0957 and 70.1% for matched random. The risk difference therefore
persists after controlling both proposal count and update magnitude. Coverage-only matching attains
74.0% accuracy.

Reporting decision. Calibration-target matching and exact held-out count matching are separate
protocols. Interpolation along a risk–coverage curve must use predeclared coordinates, rather than a
point selected after examining test risk.

D.7    I NDEPENDENT- SIGNAL AND CONTROLLER - SURFACE ABLATIONS

This study asks which observations and control surfaces contribute independent information. The
binary-view identity aagr
                      t   = max(pt , 1 − pt ) makes the historical agreement/consistency ablation a
reweighting experiment. A separate source-attested signal is needed to study the value of additional
evidence.
The signal panel compares confidence only, the independent verifier signal only, their deduplicated
combination, and the historical confidence/agreement/ consistency score. The controller panel
compares trust only, clip–KL only, their combination, and static control. Every row uses the same
proposal records, and the selected-coverage target is fixed on calibration.
The diagnostic trace records signal distributions, pairwise error overlap, and the frequency with
which each surface changes an action. It distinguishes proposals removed by the eligibility threshold
from proposals suppressed when the KL penalty makes mt = 0. This distinguishes selection from
continuous magnitude scaling. Each row specifies the full parameter vector and active-signal rule.
Task and replay measurements have different roles. The replay panel identifies the mechanical
effect on U, R, C; the learner panel tests task accuracy at matched resources. Pairwise deltas
compare identical seed/question units, so a row with an extra verifier call also requires a call-matched
comparator.


                                                  23
Preprint




Table 19: Signal and control-surface ablations. Each comparison uses the same proposal pool and a
calibration-fixed coverage target.
   Arm                          Accuracy (%)    Risk R            Coverage C        Calls/update
   Confidence only              71.7            0.0589            0.4076            256
   Independent signal only      72.6            0.0497            0.4059            256
   Deduplicated combination     73.8            0.0392            0.4108            256
   Historical weighted score    72.9            0.0479            0.4136            256
   Trust only                   73.1            0.0438            0.4144            256
   Clip–KL only                 72.4            0.0526            0.4191            256
   Full surfaces                74.1            0.0368            0.4125            256



Analysis. The deduplicated signal combination attains 73.8% accuracy and harmful risk 0.0392,
compared with 71.7% and 0.0589 for confidence alone. Full control surfaces attain 74.1% and 0.0368.
Trust-only and clip–KL controls yield 73.1% and 72.4% accuracy, respectively, under the common
256-call budget.

Interaction check. The joint controller and each individual surface share the same signal state.
The interaction is evaluated on paired deltas, not inferred from the visual ordering of independently
normalized bars.

D.8    V ERIFIER CALIBRATION AND TRUNCATION - CONTROLLED EVALUATION

The existing completeness audit reports a ranking statistic and a failed probability-calibration gate.
This extension isolates truncation from item and seed variation, then tests whether calibration
improves on a constant prevalence predictor. The candidate-generation settings are paired across
length caps.
The cap-controlled comparison uses the same question/seed pairs at 128 and 256 tokens, with
decoding, checkpoint, and prompt fixed. Prefix compatibility and generation-path divergence are
recorded. Both the same-model critic and a task-grounded independent verifier evaluate candidates.
Completeness and correctness are distinct quantities. A completion marker before the token cap is an
observable formatting event; semantic correctness is the post-freeze task label. AUROC measures
ranking, Brier score measures probability calibration, and threshold accuracy uses a calibration-fixed
threshold. The constant-prevalence Brier baseline uses the same candidates. Missing critic outputs
contribute to parse coverage and retain a reason code.
Any probability mapping is fitted on the calibration partition only. Both raw and calibrated predictions
are evaluated on the same held-out candidates. The confidence interval groups repeated candidates by
their source question to avoid treating paired views as independent items.


Table 20: Paired cap and calibration analysis. AUROC measures ranking; lower Brier is better.
Counts retain the denominator of each condition.
   Condition                    Complete/n      Correct/n         AUROC             Brier
   128 tokens, raw critic        11/32          6/32              0.6389            0.3846
   256 tokens, raw critic        22/32          10/32             0.70833           0.369777
   256 tokens, calibrated critic 22/32          10/32             0.70833           0.2196
   256 tokens, independent       22/32          10/32             0.8467            0.1684
   verifier
   Constant prevalence           22/32          10/32             0.5000            0.247934
   baseline



Interpretation. The cap-comparison table separates observable completeness, semantic correctness,
ranking, and probability calibration. The independent-verifier row supplies the source-distinct error
and calibration reference used by the appeal policy.


                                                  24
Preprint




Cost interpretation. Candidate and critic calls, including their input and output tokens, are ac-
counted separately. A calibrated critic is compared at the same generation budget as its raw counter-
part, while the independent verifier receives its own cost line.

D.9    T HRESHOLD SELECTION AND UNCERTAINTY OF THE FRONTIER

The threshold study measures whether a risk–coverage operating point remains stable across seeds
and disjoint data. It retains q50, q60, q75, and q90 as named calibration choices and compares the
corresponding held-out operating points under the same score definition.
For each training seed, thresholds are fitted on calibration observations and frozen before held-out
evaluation. The historical absolute constraints are R ≤ 0.05 and C ≥ 0.25; these are feasibility
targets, not observed results for the new learner study. Each row reports attained risk and coverage
with separate paired intervals and records how many independent seeds satisfy both constraints.
The primary paired comparison uses a declared reference threshold. Risk, coverage, and task-
accuracy differences have separate estimands. A point estimate that lies in the feasible region may
still have a coverage-difference interval crossing zero. Reporting these quantities separately makes
the uncertainty of promotion visible.
Threshold search has its own budget. All candidate thresholds must be named before opening test
labels; the selected choice follows the calibration rule. The final test table contains every declared
threshold to expose the trade-off rather than only the best-looking point.


Table 21: Threshold frontier on the learner evaluation. Feasibility requires both risk and coverage
constraints; each interval has its own named estimand.
   Threshold                  Risk [interval]   Coverage          Accuracy (%)    Seeds feasible
                                                [interval]
   q50                        0.0489 [0.0421,   0.5018 [0.4846,   73.6            2/3
                              0.0557]           0.5191]
   q60                        0.0368 [0.0314,   0.4125 [0.3981,   74.1            3/3
                              0.0422]           0.4269]
   q75                        0.0234 [0.0194,   0.2867 [0.2742,   73.5            3/3
                              0.0277]           0.2991]
   q90                        0.0108 [0.0079,   0.1294 [0.1206,   71.6            0/3
                              0.0138]           0.1382]
   Static                     0.0914 [0.0831,   1.0000 [1.0000,   70.5            0/3
                              0.0998]           1.0000]


Analysis. The q60 and q75 settings satisfy the constraints on all three seeds. The former retains
coverage 0.4125 and accuracy 74.1%, whereas the latter reduces harmful risk to 0.0234 with coverage
0.2867. The q90 setting has risk 0.0108 but violates the coverage constraint on every seed. This
frontier quantifies the risk–coverage trade-off at the measured operating points.

Curve reporting. Risk and coverage define the operating points, and task accuracy is a separate
measured outcome. A scalar area summary is only meaningful over a stated common coverage range,
so it must not replace the operating-point table or extrapolate to unobserved coverage.

D.10     T OKEN BUDGET, VERIFIER CALLS , AND RUNTIME EFFICIENCY

This study tests whether the task and risk benefit persists at matched compute. The historical token-
budget ledger reports accuracy, harmful risk, runtime, and GPU-hours for VAPO-legacy and static
RLVR on GSM8K with Qwen3.5-0.8B. Absolute runtime and resource counts accompany the relative
cost.
The reference condition uses 128k tokens and 256 calls. The token sweep uses 64k, 128k, and 256k
tokens per update while holding the verifier-call budget fixed. A separate call-budget sweep varies
the number of calls with the token budget fixed. The two sweeps are analyzed separately so that each
changes one resource factor.


                                                  25
Preprint




Elapsed time uses synchronized run boundaries on common hardware, with warm-up, cache hits,
failed calls, retries, and checkpoint I/O included in resource accounting. Median and tail latency have
update-level denominators; A cached verifier output retains its provenance and is accounted as a cache
hit, while the original generation cost is recorded separately when comparing cache construction.
The performance comparison is made at the same budget, while an efficiency frontier compares
performance across budgets. The static, random, and full controller arms share the same stopping
rule and maximum update count within each budget condition. Failed or incomplete arms remain
visible in the resource ledger rather than being omitted from the denominator.


Table 22: Historical token-budget sensitivity on GSM8K with a fixed verifier-call allowance. Source-
reported means use seeds 13, 17, and 23; risk is the all-proposal harmful fraction. Bold marks the
favorable value within each token budget.
               Tokens/update              Accuracy (%)         Risk R                         Time (s/update)   GPU-hours
               64k, VAPO-legacy           72.8                 0.0437                         354.6             6.30
               64k, static                69.4                 0.0962                         306.1             5.44
               128k, VAPO-legacy          74.1                 0.0368                         684.8             12.17
               128k, static               70.5                 0.0914                         590.4             10.50
               256k, VAPO-legacy          74.9                 0.0329                         1329.5            23.64
               256k, static               71.1                 0.0876                         1145.8            20.37

Figure 7 plots Table 22 against GPU-hours. At each token budget, VAPO-legacy pairs higher accuracy
and lower all-proposal harmful risk with greater runtime. The connected points describe the observed
budget settings; uncertainty must be assessed from paired runs.

                                Task accuracy                                                 All-proposal harmful risk

               76                                                                  0.10
                                                        256k
                                                                                          64k
                                   128k                                                               128k
                                                                                   0.08                                 256k
                                                                 Risk (fraction)
Accuracy (%)




               74
                       64k
                                                                                   0.06
               72
                                                 256k
                               128k                                                0.04    64k
                                                                                                        128k
               70     64k                                                                                                      256k
                                             VAPO-legacy                           0.02
                                             Static
               68                                                                  0.00
                      5        10     15       20         25                              5           10     15       20         25
                               GPU-hours per run                                                      GPU-hours per run


Figure 7: Historical accuracy–cost and risk–cost curves for Qwen3.5-0.8B on GSM8K. Points
reproduce source-reported aggregate means over seeds 13, 17, and 23; labels give rollout tokens
per update. Blue circles denote VAPO-legacy and orange squares denote static RLVR. The source
supplies no intervals for these aggregates, so the curves show point estimates.


Analysis. At each token budget, VAPO-legacy has higher accuracy and lower harmful risk than
static RLVR, with greater runtime. Increasing its budget from 64k to 256k tokens raises accuracy
from 72.8% to 74.9% and lowers harmful risk from 0.0437 to 0.0329, while GPU-hours increase
from 6.30 to 23.64.

Call-budget panel. The low and high call allowances, throughput, peak memory, and tail latency
are 128/384 calls/update, 202.6/171.4 rollout tokens/s, 61.8/64.3 GiB, and 638.7/781.2 s/update
(p95), respectively. Their selection uses hardware capacity and calibration requirements before
evaluating test task scores.


                                                                26
Preprint




D.11    F ROZEN - CACHE VERSUS REFRESHED - ROLLOUT LEARNING

The reported learner protocol uses a frozen rollout cache. This study asks whether a controller benefit
survives when proposals are refreshed as the policy changes. It directly tests the distance between
fixed-proposal accounting and a learner that generates its own later training data.
The comparison includes three cache policies: frozen throughout training, refreshed at a fixed cadence,
and refreshed every update. The cadence for the middle condition is every 8 optimizer updates and is
chosen from the training budget before test evaluation. Each policy is evaluated for VAPO and static
control on the same question splits and training seeds.
Each update records the policy checkpoint that produced the rollouts, their generation probability
information when required by the learner, the verifier snapshot, and the number of newly generated
tokens. The cache age is measured in optimizer updates. The learner’s actual ratio, clipping, and KL
diagnostics are measured from its training path; the replay’s proposal statistics are not substituted for
them.
Held-out task accuracy uses a shared checkpoint schedule, with selection by the frozen calibration
rule. The final test is opened once per selected arm/seed checkpoint. Loss trajectories and task
outcomes use separate evaluation units.


Table 23: Cache-policy sensitivity with shared checkpoints and evaluation questions. KL and clip
fraction come from the learner’s measured optimizer path.
   Cache / arm                 Accuracy (%)      Measured KL       Clip fraction     Fresh tokens
   Frozen / VAPO-legacy        74.1              0.0218            0.181             0.128M
   Frozen / static             70.5              0.0316            0.268             0.128M
   Periodic / VAPO-legacy      74.9              0.0202            0.172             1.024M
   Periodic / static           71.5              0.0293            0.249             1.024M
   Every update /              75.3              0.0191            0.165             8.192M
   VAPO-legacy
   Every update / static       71.9              0.0281            0.239             8.192M


Analysis. VAPO-legacy exceeds static accuracy under frozen, periodic, and every-update rollouts.
Its measured KL decreases from 0.0218 to 0.0191 across the frozen and every-update conditions, and
its clip fraction decreases from 0.181 to 0.165. Accuracy increases with the fresh-token budget in
both methods.

Trajectory evidence. Optimizer updates and cumulative fresh tokens are complementary resource
axes; both are required to compare learning speed across cache policies.

D.12    H ELD - OUT TASK TRANSFER AND PAIRED FAILURE ANALYSIS

Transfer is evaluated on a fresh task population with an explicit task identifier, release, and split
manifest. The comparison tests the full controller, static control, and matched-random selection. It
separates a frozen threshold transfer from a new calibration fit on the target population.
The target task population is SVAMP v1.0, using 1,000 arithmetic word problems partitioned into 200
calibration examples and 800 held-out evaluation examples. Its calibration and evaluation partitions
are checked for normalized-content and identifier overlap with each other and with the source task.
The task verifier is fixed and described independently of the model under evaluation. The same target
questions and seed mapping are used for all controls.
In the frozen-transfer condition, source calibration parameters are reused. In the recalibrated condition,
target calibration observations determine the threshold without accessing target test labels. Both
conditions share the target evaluation set, enabling a paired estimate of how much of the transfer loss
is attributable to score shift rather than missing signal information.
The error audit stratifies by task difficulty, verifier parse outcome, action application, and semantic
correctness. Human adjudication, where needed, is blinded to controller identity and uses a retained


                                                   27
Preprint




rubric. The audit covers 128 examples and has an 8.6% disagreement rate. Sampling weights identify
the aggregate rates.


Table 24: Held-out task-population transfer. Frozen-threshold and recalibrated conditions share test
questions but use distinct calibration rules.
    Target condition             Accuracy (%)    Risk R            Coverage C        Cost ratio
    Static                       59.4            0.1038            1.0000            1.00×
    Matched random               58.9            0.0441            0.4056            1.06×
    VAPO-legacy, frozen          61.3            0.0367            0.3439            1.15×
    threshold
    VAPO-legacy, recalibrated    63.2            0.0296            0.4018            1.17×
    Independent signal           62.1            0.0335            0.3946            1.12×


Analysis. Target recalibration raises VAPO-legacy accuracy from 61.3% to 63.2% and coverage
from 0.3439 to 0.4018, while lowering all-proposal risk from 0.0367 to 0.0296. The recalibrated
operating point retains a task advantage over static control and matched random under the target
evaluator.

Case taxonomy. The taxonomy separates wrong-but-admitted updates, correct-but-rejected pro-
posals, parser failures, ambiguous labels, and exhausted budgets. Each case has one primary cause
and secondary tags for overlapping mechanisms. The principal comparison uses the full evaluation
denominator; the case sample explains mechanisms.

E     R ISK -C ERTIFIED L EARNER E XPERIMENTS
The following experiments use the canonical learner split, verifier-call ledger, and paired seed/question
unit. Each policy is executed from observation-only state, its action trace is frozen, and clean labels
are joined afterward. Task accuracy is reported in percent; risk, coverage, and appeal are fractions,
and relative cost uses the static learner as its reference.

E.1       F INITE - SAMPLE RISK CERTIFICATE

The certificate experiment varies the target selected-risk level while keeping the candidate policy
family, confidence level, minimum coverage, and appeal budget fixed before evaluation. Held-out
selected risk is reported separately from the upper certificate bound, together with coverage, appeal
rate, and the number of independent seed/split repetitions satisfying every constraint. In the controlled
sequence-law audit, violations use the known conditional means of the finite stage; empirical held-out
risk is a separate descriptive quantity. Violation counts use a binomial interval over independent stage
repetitions, rather than over coupled records.


Table 25: Risk-certificate validity on held-out data. The call allowance is an absolute count per
update, distinct from the call-rate bound Bmax . Lowest held-out risk is bold; coverage and satisfied
runs show the constraint trade-off.
                                        Calls/     Held-out
      ρ           δ       Cmin          update      Rsel                Coverage         Satisfied
      0.10        0.05    0.25          256        0.0838               0.5031           60/60
      0.08        0.05    0.25          256        0.0697               0.4125           58/60
      0.06        0.05    0.25          256        0.0554               0.3018           54/60



E.2       C OVERAGE - AND MAGNITUDE - MATCHED SELECTION

The matching study separates informative selection from proposal suppression. One comparison
matches the exact number of applied proposals; a second also matches the mean absolute update
magnitude. Selection rules, random streams, tie breaking, and normalization factors are frozen on
calibration records.


                                                   28
Preprint




Table 26: Shared-budget certificate validity and order-sensitivity checks. Each row is a declared finite
certification stage. Violations are the fraction of stages exceeding a predeclared conditional-risk or
resource constraint.
                                                                      Calls/
                      Setting                                     ρ   update Runs Violation Coverage
                      No shared-budget coupling               0.08     256    60      0/60     0.4193
                      Shared budget                           0.08     256    60      1/60     0.4125
                      Shared budget + permutation             0.08     256    60      2/60     0.4084
                      Correlated verifiers                    0.08     256    60      3/60     0.3897



Table 27: Matched-selection comparison. The principal quantity is selected risk at common achieved
coverage. Best accuracy and risk are bold.
           Method                             Coverage       Mean |u|         Rall           Rsel       Accuracy
           Matched random                      0.4137         0.1071         0.0396       0.0957          70.1
           Matched static                      0.4129         0.1068         0.0389       0.0942          70.8
           RC-VAPO, coverage                   0.4124         0.1029         0.0291       0.0706          74.0
           matched
           RC-VAPO,                            0.4119         0.1069         0.0287       0.0697          73.8
           coverage+magnitude
           matched


The paired comparison is
                                   RC-VAPO    matched random
                          ∆Rsel = Rsel     − Rsel            = −0.0260,
with paired 95% interval [−0.0364, −0.0157].

E.3   V ERIFIER - NOISE STRUCTURE

The noise study compares symmetric, false-positive-heavy, false-negative-heavy, confidence-
dependent, and correlated two-verifier regimes. Every arm receives the same proposals and learner-
update opportunities. Noise-correction baselines use only their calibration information, while RC-
VAPO uses the predeclared certificate without test labels.

Table 28: Robustness to verifier-noise structure. Accuracy (%) is maximized and selected risk is
minimized within each noise condition; best values are bold. Coverage is descriptive.
             Noise                        Method                              Accuracy        Rsel      Coverage
             Symmetric                    Noise correction                         72.4      0.0841      0.8736
             Symmetric                    RC-VAPO                                  74.2      0.0679      0.4146
             FP-heavy                     Noise correction                         71.8      0.1027      0.8612
             FP-heavy                     RC-VAPO                                  73.8      0.0738      0.3989
             FN-heavy                     Noise correction                         72.0      0.0789      0.8295
             FN-heavy                     RC-VAPO                                  73.9      0.0654      0.4217
             Confidence-dependent         Noise correction                         71.6      0.0968      0.8047
             Confidence-dependent         RC-VAPO                                  73.6      0.0756      0.3862
             Correlated verifiers         Noise correction                         71.3      0.1094      0.7981
             Correlated verifiers         RC-VAPO                                  72.9      0.0791      0.3728



E.4   C OMPONENT ABLATION

All ablations use identical proposal pools, calibration records, learner budgets, and evaluation
questions. The rows separate risk certification, secondary verification, and continuous magnitude
control.

E.5   C ROSS - MODEL - FAMILY AND SCALE REPLICATION

The model comparison covers Qwen3.5-0.8B and Llama-3.2-3B-Instruct. Task splits, verifier defini-
tions, and risk targets are shared within each model comparison. Table 30 reports accuracy, selected
risk, coverage, and the training-seed count for each backbone.


                                                             29
Preprint




Table 29: RC-VAPO component ablation. Best accuracy (%), selected risk, and cost are bold;
coverage and appeal are descriptive.
           Variant                        Accuracy            Rsel      Coverage   Appeal     Cost
           No certificate                      73.2          0.0846      0.4338    0.1831     1.15×
           Certificate only                    72.9          0.0751      0.3194       0       1.04×
           Certificate + appeal                73.7          0.0709      0.4057    0.1808     1.15×
           Certificate + actuator              73.4          0.0746      0.3228       0       1.06×
           Full RC-VAPO                        74.1          0.0697      0.4125    0.1816     1.16×



Table 30: Model-family and scale replication under matched rollout and verifier budgets. Accuracy is
a percentage; risk and coverage are fractions. Best accuracy and risk are bold within each backbone.
Llama uses the Instruct checkpoint.
Backbone                     Method                                                Acc. (%)    Rsel    Coverage
Qwen3.5-0.8B                 Static RLVR                                             70.5     0.0914    1.0000
Qwen3.5-0.8B                 Matched random                                          69.8     0.0956    0.4138
Qwen3.5-0.8B                 RC-VAPO                                                 74.1     0.0697    0.4125
Llama-3.2-3B                 Static                                                  64.0     0.1048    1.0000
Llama-3.2-3B                 Matched random                                          63.4     0.1082    0.4106
Llama-3.2-3B                 RC-VAPO                                                 67.1     0.0768    0.4042



On Llama-3.2-3B-Instruct, RC-VAPO achieves 67.1% accuracy and selected risk 0.0768; static
training gives 64.0% and 0.1048. The model-specific comparison exhibits the same accuracy–risk
ordering as the primary backbone.

E.6   F ROZEN AND REFRESHED ROLLOUT POLICIES

The fixed-proposal replay isolates selection, while a policy learner changes its future proposal
distribution. We compare frozen rollouts, periodic refresh, and every-update refresh under the same
risk target and evaluation schedule. For each update the ledger records the generating checkpoint,
rollout age, policy ratio, measured KL, clip fraction, fresh tokens, verifier calls, and certificate
validity.


Table 31: Certificate renewal under refreshed rollouts. Renewal is evaluated at each declared
distribution change; violations are counted over finite stages. Best accuracy, risk, violation count, and
cost are bold; fresh tokens are reported in millions.
                                                                                   Fresh      Rel.
           Protocol                   Accuracy        Rsel    Coverage Violations tokens      cost
           Frozen certificate           74.1      0.0697       0.4125        0     0.128M 1.16×
           Periodic renewal             74.9      0.0678       0.4196        1     1.024M 1.25×
           Renew at rollout refresh     75.3      0.0662       0.4241        0     8.192M 1.47×



E.7   S HARED - BUDGET ORDER SENSITIVITY

Because a shared appeal budget couples later actions to earlier calls, the sequence order is part of the
deployment contract. We repeat the same frozen candidate and budget under immutable permutations
and report risk, coverage, appeal utilization, certificate violations, and task accuracy.

E.8   D ISTRIBUTION SHIFT AND TASK TRANSFER

The transfer study distinguishes a frozen source certificate from target-side recalibration. Frozen-
certificate evaluation reuses the source policy without modification; recalibration repeats the trace-
freeze–label-join procedure on a disjoint target calibration partition before target evaluation.


                                                       30
Preprint




Table 32: Order sensitivity under a shared appeal budget. Best risk, violation count, and accuracy (%)
are bold.
                    Order condition             Rsel    Coverage Appeal Violations Accuracy
                    Canonical order            0.0697    0.4125    0.1816     0        74.1
                    Permutation 1              0.0712    0.4089    0.1789     1        73.9
                    Permutation 2              0.0688    0.4157    0.1841     0        74.2
                    Permutation 3              0.0721    0.4054    0.1764     1        73.7




Table 33: Held-out transfer of the risk certificate on SVAMP. Best accuracy (%), selected risk, and
cost are bold.
               Target condition                  Accuracy          Rsel      Coverage         Cost
               Static                              59.4           0.1038      1.0000          1.00×
               Matched random                      58.9           0.1087      0.4056          1.06×
               RC-VAPO, frozen certificate         61.3           0.1067      0.3439          1.15×
               RC-VAPO, recalibrated               63.2           0.0737      0.4018          1.17×
               certificate



E.9    M EASURED RISK AND BUDGET SENSITIVITY

The supplied sensitivity runs vary the target risk and shared-budget condition under fixed confidence
level δ = 0.05, minimum coverage Cmin = 0.25, and 256 verifier calls per update. Risk and coverage
are fractions; satisfied runs count independent finite stages.


Table 34: Measured risk-target sensitivity. Best selected risk is bold; coverage and satisfied-run
counts are reported for the same stage family.
                  Target ρ                δ     Cmin        Rsel       Coverage    Satisfied
                  0.10                  0.05    0.25      0.0838          0.5031       60/60
                  0.08                  0.05    0.25      0.0697          0.4125       58/60
                  0.06                  0.05    0.25      0.0554          0.3018       54/60


The selected-risk target traces the measured coverage trade-off: lowering ρ from 0.10 to 0.06 lowers
selected risk from 0.0838 to 0.0554 and coverage from 0.5031 to 0.3018. The overall verifier-noise
campaign satisfies 57 of 60 stages; the 58/60 entry at ρ = 0.08 is the target-specific stage count
reported in the sensitivity ledger.
Shared budgets and verifier correlation increase the observed violation count and reduce coverage.
The sequential certificate uses the resource state in its filtration, so these conditions are evaluated as
separate finite stages.

E.10    M EASURED MATCHED CONTRASTS

At matched coverage, the selected-risk contrast is
                      ∆Rsel = −0.0260,          95% CI = [−0.0364, −0.0157].
The contrast is paired by seed and question and uses the same proposal and update-magnitude
matching rule as the main result. Accuracy, all-proposal risk, coverage, appeal, and cost retain their
own denominators in the complete learner table.

E.11    T RANSFER AND VERIFIER - NOISE OUTCOMES

Under symmetric, false-positive-heavy, false-negative-heavy, confidence-dependent, and correlated
verifier errors, RC-VAPO obtains accuracies 74.2, 73.8, 73.9, 73.6, and 72.9%, respectively, with
selected risks 0.0679, 0.0738, 0.0654, 0.0756, and 0.0791. Coverage is 0.4146, 0.3989, 0.4217,
0.3862, and 0.3728. These rows are paired with the noise-correction baseline in Table 28.


                                                   31
Preprint




Table 35: Measured shared-budget and order-sensitivity checks. Violations count finite stages;
coverage is the all-proposal admission fraction.
        Setting                              ρ     Calls/update   Runs    Violations   Coverage
        No shared-budget coupling           0.08        256        60        0/60       0.4193
        Shared budget                       0.08        256        60        1/60       0.4125
        Shared budget + permutation         0.08        256        60        2/60       0.4084
        Correlated verifiers                0.08        256        60        3/60       0.3897


On SVAMP, target recalibration gives 63.2% accuracy, selected risk 0.0737, coverage 0.4018, and
relative cost 1.17×; the frozen certificate gives 61.3%, 0.1067, 0.3439, and 1.15×. The target task
uses 200 calibration and 800 evaluation examples, with an 8.6% disagreement rate in the blinded
128-example audit.

E.12    S TATISTICAL REPORTING

Every main learner comparison is paired by training seed and evaluation question. Individual seed
results precede aggregation, and task accuracy, all-proposal risk, selected risk, coverage, appeal rate,
and cost receive separate uncertainty intervals. The primary inferential summary is a paired 95%
hierarchical-bootstrap interval over seed and question with 10,000 resamples. The finite-sample
calibration certificate is reported separately from descriptive or comparative intervals. Thresholds,
candidate policies, and checkpoint-selection rules are fixed before test labels are opened.

Status of historical evidence. The fixed-proposal CPU replay, parser-equivalence stress screen,
format-marker connectivity run, and same-model critic calibration predate the risk-certified controller.
They remain mechanism and implementation audits with their original run, split, checkpoint, verifier,
and artifact digest; they are not pooled with the canonical RC-VAPO learner experiment.

F     A RTIFACT M APPING AND R EPRODUCIBILITY
F.1    R ESULT IDENTITY AND EVALUATION METADATA

The two historical learner tables retain their original values as separate ledgers. Their repeated arm
names do not establish that they measure the same run, checkpoint, or evaluation partition. The
metadata below determines whether they can be compared or linked to the retained connectivity
artifacts.
The historical replay and calibration artifacts have their own identities in the earlier evidence ledger.
The connectivity result establishes a one-seed format-marker execution path with identical held-out
and test outcomes across its four arms. It remains distinct from the supplied three-seed learner
aggregates. The split, checkpoint, and evaluator distinguish the tables even when they share a model
name.

F.2    T RACE SCHEMA AND REPRODUCTION ORDER

A trace links the immutable item identifier, split, seed, source digest, observed verifier fields, frozen
calibration state, action, and resource counters. The clean-label join is retained separately with
its input trace digest. A reproduction first verifies the manifest and split overlap, then rebuilds
the observed state and action, and finally joins labels to compute task, risk, and coverage metrics.
Per-seed rows precede the aggregate table.
The Supplementary Material contains the source files, frozen configuration, retained outputs, and
evaluation code needed to regenerate the tables. Public task data and model checkpoints retain their
original licenses and version identifiers. An anonymous review package uses neutral artifact handles
in place of personal paths or machine names. Runtime logs belong with the artifact package, while
the paper records measured units, sample counts, and uncertainty definitions. The supporting PDF is
built from the manuscript source and bibliography and checked after all figures, tables, and references
settle.


                                                   32
Preprint




Table 36: Run metadata for the two reported historical learner ledgers. Each field identifies its
associated result and evaluation protocol.
 Field                            Four-arm ledger                        Five-arm learner ledger
 Run and checkpoint identity      ledger A, update-56                    ledger B, update-64
 Evaluation partition and item    held-out test-A, n = 768               GSM8K official test, n = 1319
 count
 Accuracy unit and return         exact-match percentage; 100×           exact-match percentage; 100×
 definition                       mean clipped task reward               mean clipped task reward
 Uncertainty estimand and         95% paired hierarchical-bootstrap      95% paired hierarchical-bootstrap
 interval type                    half-width on task return, 10,000      half-width on task return, 10,000
                                  resamples                              resamples
 Per-seed result artifact         per-seed rows retained in ledger A     per-seed rows retained in ledger B
 Risk denominator and label       all proposals N ; post-freeze frozen   all proposals N ; post-freeze
 source                           task-correctness verifier              semantic exact-match oracle
 Cost baseline and                static matched = 1.00; normalized      static matched = 1.00; normalized
 measurement unit                 GPU-seconds plus verifier              GPU-seconds plus verifier
                                  inference time                         inference time
 Raw output and verifier digest   a378f8283a84bfd6362908395b8317         0f2aa4603bcdac049cc0c9658330d7
                                  445a03f7ae816d2b1fb06efff75be6         5f9df257c7c963030ec955fedbb42b
                                  4b7d0ad77db3ba285838a859e2477e         1767c8a42d9da14bd32d6a5b6cfcaf
                                  43794cd44f6fc702efbe2c6c910786         e840647792b6d5b3e9a19aaefeb13e
                                  21b6846b                               4e6a349




                                                    33
