                                         Preprint. Under review.




                                         Constrained Path Reasoning:
                                         Measuring When Committed Stages Earn Their Cost

                                             Honglin Li
                                             ShanghaiTech University
                                             lihl2025@shanghaitech.edu.cn



                                                                                  Abstract
                                                  When does a committed intermediate stage in an LLM reasoning pipeline
                                                  earn its cost? Constrained Path Reasoning (CPR) pairs a source-aware path
                                                  hypothesis with stage-level accounting. Search generates provisional states;
                                                  trusted or validated invariants can constrain hard, while other proposals
                                                  remain soft and revisable. CPR predicts that task-compatible commitments
                                                  can factor transitions, concentrate candidate mass, induce regularity, and
                                                  expose feedback when their gains exceed propagated error and execution
                                                  cost. The formalism covers discrete commitments and continuous flows and
arXiv:2607.17240v1 [cs.AI] 19 Jul 2026




                                                  measures effective branching, endpoint concentration, and cost per usable
                                                  output. Across 1,180 generated QCQPs and 40 engineered degenerate
                                                  polynomial instances (2,140 endpoints), residual triage recovers 63.0% of
                                                  repair-all’s additional feasible yield with 17.7% of its attempts. Fixed-
                                                  LLM accounting (270 unique calls shared across nested arms) finds usable
                                                  yield of 41.1% direct, 90.0% after formalization and deterministic execution,
                                                  20.0% after one-shot convexification, and 21.1% for the full path. In 120
                                                  paired-condition calls, a two-action rollback rule reaches 90% usable yield
                                                  versus 36.7% for the feedback-conditioned selector. Two endpoint probes
                                                  separate source from validation: a 72-output cross-trajectory transplant
                                                  reduces entropy and acceptable mass; a 24-output same-call self-proposal
                                                  pilot gives unchanged two-repeat collision entropy, 25.0% versus 8.3%
                                                  usable yield, and 1/8 deterministically confirmed endpoint checks. Model-
                                                  generated states supply hypotheses; trusted execution earns constraint
                                                  strength.


                                         1     Introduction
                                         Explicit intermediate reasoning improves many LLM tasks (Wei et al., 2022; Kojima et al.,
                                         2022; Wang et al., 2023; Snell et al., 2024), while excessive reasoning can waste compute or
                                         reduce accuracy (Chen et al., 2024; Sui et al., 2025). We study a complementary design ques-
                                         tion: how do committed intermediate states change the search, execution, and verification
                                         available to later steps?

                                         Constrained Path Reasoning. We view CoT as endogenous constrained path construction.
                                         At each step, the model’s heuristic search proposes a local continuation or intermediate
                                         artifact, selects one, and conditions subsequent search on it. Trusted invariants—for example,
                                         a physical law or a verified formal contract—may restrict the path hard. Model-generated
                                         subgoals, decompositions, and surrogate assumptions remain provisional until validated,
                                         retaining revision and rollback. CPR hypothesizes that task-compatible constraints can
                                         factor a long transition into shorter operators, concentrate candidate mass, induce regularity,
                                         and expose correction signals. The same account covers single-path decoding and explicit
                                         multi-branch search (Yao et al., 2023; Besta et al., 2024; Hao et al., 2023).
                                         The theoretical claims become testable at committed-stage interfaces. CPR records artifact
                                         validity, downstream utility, operational cost, induced regularity, feedback, candidate
                                         concentration, constraint provenance, and whether an unverified state remains corrigible.
                                         Reasoning efficiency includes tokens, executor time, repair effort, and discarded outputs, so


                                                                                       1
Preprint. Under review.




each stage is also priced by cost per usable solution. Section 2.2 develops the ambiguity–
error–cost hypothesis behind this accounting (Fig. 1).

A quantitative case study: automated convexification. We ground CPR in a domain
with executable stage interfaces and numerical feedback: LLM-assisted convexification of
non-convex optimization problems, as instantiated by the recent NC2C system (Peng et al.,
2026) and related LLM-for-optimization pipelines (AhmadiTeshnizi et al., 2024; Xiao et al.,
2024). The controlled path uses literal coefficient transcription, deterministic execution
from a standardized feasible initialization, and one committed SDR or OSM surrogate
transition. The convex surrogate supports numerical solving and lower-bound diagnostics
where available; its endpoint exposes the constraint residual against the original constraints.
Classical error-bound theory (Hoffman, 1952; Pang, 1997) maps this residual to a distance
bound under standard regularity. Building on NC2C’s validation and FDC repair inter-
face, we operationalize the relation as residual-guided endpoint triage. This case study
prices the adoption and execution of explicit artifacts. A same-call pilot additionally elicits
autonomous state proposals from the natural-language problem alone.

Contributions.
      1. Stage-level accounting protocol (§2): for committed executable interfaces,
         we combine shared-call nested ablations, stage-local checks, constraint prove-
         nance/corrigibility, executor-aware cost, and utility per usable endpoint to localize
         observed changes.
      2. Source-aware CPR hypothesis (§2): verified invariants can constrain hard, while
         trajectory-generated intermediate states remain defeasible; discrete stages and
         continuous flows are organized through factorization, concentration, regularity,
         feedback, and propagated error.
      3. Quantitative case study (§§3–7): a residual verifier, fixed-LLM evaluation, and
         endpoint probe expose relaxation leakage, over-contraction, initialization sensitivity,
         a feedback-policy gap, and the failure of a cross-trajectory surrogate-state trans-
         plant; a same-call self-proposal pilot separates proposal generation from executable
         validation.

2     Constrained path reasoning
2.1   Autoregressive reasoning as sequential heuristic search

Let x be the input and sk the k-th committed reasoning state: a token prefix together with
any explicit artifact it encodes, such as a subgoal, formal program, or tool result. The local
successor distribution qθ (z | sk , x ) acts as a learned heuristic over plausible continuations. A
decoder D then commits one continuation and updates the state:
                         ẑk+1 = D (qθ (· | sk , x )) ,  sk+1 = U (sk , ẑk+1 ).                 (1)
Thus each step follows propose/score → select → condition the next search. Here a commit-
ment is a state selected strongly enough to condition later search while remaining eligible
for revision. Single-path decoding performs local scoring implicitly; beam search, Tree-of-
Thoughts (Yao et al., 2023), graph variants (Besta et al., 2024), and MCTS-style planning
(Hao et al., 2023) make candidate search explicit. CPR studies the selected path produced in
either regime.

Constraint source and strength. The path constraint is generally produced during search.
We decompose it as
                                  Cbk ∼ Gθ (· | sk , x ),     Ck = Ik ∪ Cbk ,                   (2)
where Ik contains trusted exogenous invariants and Ck is an endogenous proposal—a
                                                                        b
subgoal, decomposition, formal artifact, or local hypothesis—generated from the current
trajectory. Here ak (z; Cbk ) scores proposal compatibility, and λk is its validation strength.
                                                                             n               o
                C
               qθ k (z | sk , x ) ∝ qθ (z | sk , x ) 1[z ∈ Ωk (sk ; Ik )] exp λk ak (z; Cbk ) . (3)


                                                 2
Preprint. Under review.




                                                                                                             T2 (· ; C2 )
                                                                                        T1 (· ; C 1 )   z2                  zK
                                                                            C0)   z1
                                                                  T0 (· ;
z0                                       z⋆
                                                         z0
                                                                                       feedback (residual) → local repair

            direct transition
          one long-range step;
       broad candidate interface;                                                 constrained path
           endpoint feedback                       factorization: staged transitions · hypothesis: candidate mass concentrates
                                              regularity: some zk convex/executable/verifiable · feedback: continuous error signal



Figure 1: Constrained Path Reasoning. Left: direct prediction crosses a broad candidate
interface and receives endpoint feedback. Right: trajectory-generated states or trusted
invariants factor the transition, may concentrate candidate mass, induce regularity, and
expose correction signals. Provisional states retain rollback. The fans visualize the candidate-
level hypothesis; arrows may be discrete operators or checkpointed continuous flows, and
experiments use fixed action and endpoint interfaces.


Trusted invariants, such as a known physical law, receive hard support restriction. A model-
generated proposal receives finite weight and retains revision, rollback, or escape until a
verifier certifies it; certification strength comes from a trusted derivation or executor contract.
A certified proposal can approach the hard-constraint limit. We call the deployed constraint
support-preserving when it retains positive mass on continuations extendable to a correct
answer. It is task-compatible at tolerance τ when
                                    Pr(success | sk , Ck ) ≥ Pr(success | sk ) − τ.
For a fixed discrete candidate representation, the candidate-level effective branching factor
is                                          h                  i
                                                C
                                bkeff = exp H qθ k (· | sk , x ) .                         (4)
Continuous states require a fixed quantization or a separately specified description-length
scheme. CPR predicts that useful paths reduce accumulated candidate ambiguity, or the
search work it induces, while preserving task utility.
At the operator level, let z0 encode the problem and z⋆ an acceptable endpoint. A structured
path is
                     z0 → z1 → · · · → z K = z ⋆ ,  Zk+1 ∼ Pk (· | Zk ; Ck ),               (5)
where Pk wraps an LLM call, symbolic transformation, solver, or verifier. The kernels
localize transcription, approximation, and numerical error to the stage that creates it. Where
numeric states embed in a normed space, we write zk+1 = Tk (zk ; Ck ) + ξ k ; the kernel form
also covers symbolic and heterogeneous state spaces.

Continuous constrained paths. Let Minv  t  = {z : ϕ(z, t) = 0} encode a trusted prescribed
or independently certified manifold. A continuous CPR segment satisfies
                    żt = f θ (zt , t, x ) + ut ,       ϕ(zt , t) = 0,                 Dz ϕ żt + ∂t ϕ = 0.
Here f θ may combine a trusted prior ODE f 0 with a learned tangential residual, and ut
enforces the invariant. An uncertified learned manifold enters as a finite-weight potential
or confidence tube, preserving the same corrigibility as Cbk ; certification promotes it to
Minv
   t . Discretization recovers Eq. (5); hybrid paths alternate continuous segments with
symbolic commitments. Fixed probes and probability flow give endpoint, entropy-rate, and
reachable-volume diagnostics (App. B).

2.2   Four mechanisms and an ambiguity–error–cost hypothesis

The process in §2.1 motivates four mechanisms:
      1. Transition factorization. Intermediate states replace one endpoint transition by
         staged operators. CPR hypothesizes that semantically shorter operators can reduce


                                                              3
Preprint. Under review.




         per-step function complexity and out-of-distribution span, consistent with locality
         accounts of CoT (Prystawski et al., 2023) and expressivity results for intermediate
         tokens (Merrill & Sabharwal, 2024; Li et al., 2024).
      2. State-space contraction. A useful constraint can concentrate successor mass. At a
         fixed candidate representation, its entropy change is
                                                                            C
                                       ∆Hk := H [qθ (· | sk , x )] − H [qθ k (· | sk , x )].                    (6)
         We call the step entropy-contracting when ∆Hk > 0 and treat its sign as an empirical
         property. Section 7 instantiates the diagnostic at a fixed A–D action menu using
         schema-elicited allocations; logged candidate probabilities would instantiate it at the
         model-successor level. Measuring the model-level endpoint distribution directly is a
         planned follow-up: it requires token-level probability access or a substantially larger
         repeated-call budget. The present study instead prices a cost-bounded interface
         diagnostic.
      3. Regularity induction. Committed states can supply convexity, smoothness, ex-
         ecutability, or verifiability, making the next operator well-posed and its output
         inspectable.
      4. Feedback and correction. Intermediate states can expose continuous error signals
         (a residual, a failing test) so local repair replaces end-to-end regeneration; process
         supervision exploits the same observability in training (Lightman et al., 2024; Uesato
         et al., 2022), self-refinement at inference (Madaan et al., 2023; Shinn et al., 2023).

Error propagation.          For numeric or metrically embedded stages, suppose
                                                           !
                                                                K −1                K −1        K −1
               ∥ e k +1 ∥ ≤ L k ∥ e k ∥ + η k ,     ∥ eK ∥ ≤     ∏ Li      ∥ e0 ∥ + ∑ η j ∏ L i ,               (7)
                                                                 i =0                j =0      i = j +1

where Lk is local sensitivity and ηk is error injected at stage k. The expanded bound assigns
every injected error its downstream sensitivity. Together with (6), it yields CPR’s design
prediction: a path is valuable when ambiguity reduction and regularity gains outweigh
propagated error, task-utility loss, and execution cost. Over-contraction, relaxation leakage,
and large suffix sensitivities are corresponding failure modes. For an unverified endogenous
state, finite constraint strength and an available revision or rollback action preserve the
search’s corrigibility.
Hypothesis 1 (Pathwise endpoint concentration). Fix a discrete (or fixed-quantized) end-
point candidate variable Y with representation Y , an endpoint probe, and an acceptance set
Yacc ( x ) ⊆ Y . Let Qend
                      θ (· | Sk , x ) be the model-implied distribution returned by that same
probe from committed state Sk , and define
                                             h                     i
                               Ak := Ex,Sk H Qend  θ (· | S k , x )    .                   (8)

The expectation follows the task distribution and the path policy. Its provisional states are
generated within the sampled trajectory by (2); hard state components come from trusted
or verified invariants. For task–model pairs where structured reasoning is beneficial, CPR
conjectures a strict net concentration before endpoint generation,
                           h                                  i          h                                i
 A K −1 < A 0 ,     Ex,SK−1 Qend
                              θ  (Y acc ( x ) | S K − 1 , x )   ≥ E x,S0   Q end
                                                                             θ   (Y acc ( x ) | S 0 , x )   − τ. (9)

This compares the same endpoint variable along the path. Discrete stage contributions
are ∆end
      k   := Ak − Ak+1 . On a continuous segment, write St = (zt , t), define A(t) by (8),
                                                           RT
and use the concentration rate χ(t) = −dA(t)/dt, so 0 χ(t)dt = A(0) − A( T ). Local
quantities may have either sign: exploration, rollback, or reflection can expand the endpoint
distribution temporarily. The acceptance-mass condition distinguishes useful concentration
from confidence in an unusable endpoint. Local successor entropy and fixed endpoint
probes measure the immediate candidate interface and final-task uncertainty, respectively,
for discrete or checkpointed continuous paths.


                                                           4
Preprint. Under review.




Operational path accounting. For a path design π, let Uπ indicate a usable endpoint and
     (m)
let Cπ be a fixed cost metric m—tokens, wall-clock, continuous-flow function evaluations,
or a declared price for LLM inference, solving, verification, and repair. The target is
                                                            (m)
                                     (m)        E[Cπ ]
                                   Cuse (π ) :=          ,                              (10)
                                              Pr(Uπ = 1)
estimated by total cost divided by usable outputs. A committed stage earns its cost when an
                         (m)
ablation shows lower Cuse , greater yield under a fixed budget, or higher returned-answer
precision at an acceptable coverage. Action concentration and effective action count are
reported only when their candidate interface, prompt, and state encoding are fixed; the
four-action allocation supplies the executable local measure here. The audit additionally
records whether each constraint is trusted, verified, or provisional, and whether the suffix
exposes revision or rollback.

Accounting protocol. Given nested path packages π0 , . . . , πK , local contracts, fixed ex-
ecutors, a usable-endpoint criterion, and a cost vector, the protocol reuses upstream calls,
checks each new artifact locally, executes endpoints against common ground truth, and
                                                      (m)
reports changes in yield, coverage/precision, Cuse , and localized errors. The resulting audit
is indexed by the evaluated task, model, executor, and cost vector.

Relation to existing views. That reasoning is search is classical (Newell & Simon, 1976),
and recent work makes LLM reasoning search-like explicitly (Yao et al., 2023; Hao et al.,
2023; Gandhi et al., 2024); constrained decoding imposes structural constraints at the token
level—incremental parsing (Scholak et al., 2021), predicate-logic constraints (Lu et al., 2021),
knowledge-graph faithfulness (Luo et al., 2024)—and Constraints-of-Thought (Alrashedy
et al., 2025) turns reasoning steps into executable constraints inside a planner. CPR links
these views through a common claim: task-compatible commitments can factor transitions,
concentrate successor mass, induce regularity, and expose feedback. Its accounting layer
then measures task utility, cost, provenance, corrigibility, artifact validity, and stage-localized
error at the same stage boundary. Committed states may also be non-textual (Hao et al.,
2024).

3   Case study: committed stages in a convexification pipeline
NC2C as a constrained path. NC2C (Peng et al., 2026) maps a natural-language non-
convex optimization problem through formalization, non-convexity detection, convexifica-
tion, code execution, and feasibility repair. Its heterogeneous states are z0 = description,
z1 = P , z2 = detected structure, z3 = Pc , z4 = xc , and z5 = triage or repaired point
(Fig. 2). LLM stages construct formal artifacts, a deterministic solver executes Pc , and a
verifier/repair operator checks the original constraints. The model-proposed surrogate z3 is
a provisional path state: it supplies regularity, while its endpoint supplies the continuous
residual                               n                              o
                        r ( x ) = max max gi ( x ) + , max | h j ( x )| ,                (11)
                                            i                     j
the violation of the original constraints gi ≤ 0, h j = 0 by the surrogate’s solution. Ap-
pendix C specifies the residual conventions and local equivalences used by the harness.
Repair, re-convexification, and rollback retain corrigibility after this proposal.

Geometry of the convexification step. The two main convexification families relate to F
in opposite directions. An outer relaxation (SDR (Luo et al., 2010), McCormick envelopes
(McCormick, 1976)) satisfies F ⊆ Crelax : its optimum lower-bounds the original optimal
value and may have r > 0. An inner approximation (SCA-type majorization anchored at a
feasible point with no slack, as in our harness (Lipp & Boyd, 2016)) satisfies Cinner ⊆ F : its
solutions have r = 0 by construction but can be conservative. Together with the symbolic
formalization and detection stages, these relations produce the heterogeneous path in Fig. 2.
For outer relaxations, r ( xc ) is the computable scalar that connects the surrogate endpoint to
the original constraints and turns binary validation into graded feedback.


                                                  5
Preprint. Under review.




                                                                                                        reject ⇒ re-convexify (new strategy)



                     LLM                        LLM                   LLM strategy                        convex
                                                                                                                                        r ( xc )
      NL problem   formalize     formal         detect   non-convex (SDR/SCA/. . . ) convex               solver       solver                         residual
          z0                   program P                  structure                 surrogate Pc                     solution xc                       triage

                                 committed                                          regularity induction            repair: bounded                NEAR - FEASIBLE /
                               symbolic state                                outer: F ⊆ Crelax , r > 0 possible      local correction              REPAIR / REJECT
                                                                          inner: Cinner ⊆ F , r = 0, conservative



Figure 2: Automated convexification as a constrained path with heterogeneous operators.
LLM steps commit symbolic states, the convex surrogate induces regularity, and the end-
point residual drives triage and local correction. Outer and inner approximations relate to
F in opposite directions.


4     Residual-guided endpoint verification

We now make the feedback channel quantitative. Throughout, F = { x ∈ Rn : gi ( x ) ≤
0, h j ( x ) = 0} is the original feasible set, assumed non-empty, with gi , h j ∈ C1 and
dist( x, F ) := infy∈F ∥ x − y∥2 . We assume a bounding constraint among the gi (in our
instances the smooth ball ∥ x ∥2 − R2 ≤ 0, which also enters the residual), so F and the
residual tubes below are compact.


4.1    Classical error bounds, operationalized

Definition 1 (Hölderian residual bound). The constraint system admits a residual bound
with exponent θ ∈ (0, 1] and modulus κ > 0 on the tube Uδ0 = { x ∈ Rn : r ( x ) ≤ δ0 } if

                                           dist( x, F ) ≤ κ r ( x )θ                  for all x ∈ Uδ0 .                                                           (EBθ )


Bounds of this form have a mature literature: Hoffman’s bound for linear systems (Hoffman,
1952), error bounds under constraint qualifications (Pang, 1997; Rockafellar & Wets, 1998;
Ngai & Théra, 2008), Hölderian bounds under degeneracy (Luo & Luo, 1994; Bolte et al.,
2017), quadratic growth in convex settings (Drusvyatskiy & Lewis, 2018). We use these
classical bounds as the decision layer of the convexification path: they map an endpoint
residual to an acceptance scale or a repair budget.
Proposition 1 (Residual triage; operationalization of classical bounds). Assume (EBθ ) holds
on Uδ0 . Let 0 < ε ≤ β be an acceptance accuracy and a repair radius budget (so the two thresholds
below are ordered), and let xc satisfy r ( xc ) ≤ δ0 . Then:

        (i) if r ( xc ) ≤ (ε/κ )1/θ , some x ⋆ ∈ F has ∥ xc − x ⋆ ∥ ≤ ε (NEAR - FEASIBLE: a proximity
            certificate);
       (ii) if r ( xc ) ≤ ( β/κ )1/θ , then dist( xc , F ) ≤ β, so a feasible point lies within the repair budget
            (REPAIR);
      (iii) if r ( xc ) > ( β/κ )1/θ , the bound does not certify the existence of a feasible point within
            radius β (REJECT).
At every feasible point satisfying MFCQ, a local linear residual bound holds (Robinson, 1976;
Rockafellar & Wets, 1998; Pang, 1997). If MFCQ holds throughout compact F , finitely many local
moduli give a uniform linear bound on a neighborhood of F (and on a fixed compact residual tube as
detailed in App. C). If instead r ( x ) ≥ µ dist( x, F )2 , (EBθ ) holds with θ = 21 and κ = µ−1/2 .

The tiers certify proximity and repair radius; endpoint yield additionally depends on the
repair algorithm. We therefore count numerically feasible outputs and evaluate a fixed
bounded correction directly.


                                                                          6
Preprint. Under review.




4.2   Analytical certificate vs. calibrated gate

For a verified constraint family, Proposition 1 supplies analytic (κ, θ ). For a calibrated
family, let de( xc , F ) := minℓ≤ L ∥ xc − x̃ℓ ∥2 , where each x̃ℓ ∈ F is a feasible return from a fixed
multi-start projection protocol; hence de( xc , F ) ≥ dist( xc , F ). We fit θ̂ by unconstrained
log–log regression of de( xc , F ) on r ( xc ) and set κ̂ to the 95th percentile of d/r e θ̂ . We report
fitted slopes above one as finite-range empirical power-law exponents and summarize
their decision semantics by held-out proxy coverage within the calibration residual range.
Verified regularity provides analytical certificates; the fitted gate provides the reported
empirical coverage diagnostic.

The three-tier verifier. The verifier computes r ( xc ) and returns NEAR - FEASIBLE if r ( xc ) ≤
δ1 := (ε/κ̂ )1/θ̂ ; else REPAIR—invoke a bounded local correction with radius budget β—if
r ( xc ) ≤ δ2 := ( β/κ̂ )1/θ̂ ; else REJECT (switch strategy or re-convexify). Analytical thresholds
are capped by the bound’s validity radius; calibrated thresholds operate within empirical
support. This maps a geometric repair budget to a residual cutoff and spends correction
only on endpoints predicted to lie within reach. For deployment, a NEAR - FEASIBLE point
that still exceeds the numerical tolerance also receives correction; at our operating point
these 16 points plus 37 REPAIR points produce the 53 attempts in Table 1. The analytical
budget β is Euclidean distance; the harness adopts the stricter cumulative repair-path-length
cap at the same value. All reported yields require numerical feasibility after correction.


5     Experiments I: case-study validation

We first test the quantitative core on controlled non-convex problems (details, seeds, and
per-instance raw data: App. D and the supplementary material).

Setup. We generate feasible non-convex QCQPs minx c⊤ x subject to x ⊤ Ak x + bk⊤ x + dk ≤ 0
and ∥ x ∥ ≤ R, using m ≈ 3–4n indefinite constraints. SDR is solved with CVXPY (Diamond
& Boyd, 2016). The fixed multi-start SLSQP protocol supplies de( xc , F ), the feasible projection
proxy defined in §4.2; bounded projected-subgradient descent records path length to first
feasibility. All instances are generated and executed with standard numerical solvers and
fixed seeds.

Residual–projection-distance relation. On 325 SDR-relaxed endpoints with r > 0 (Fig. 3a),
unconstrained log–log regression gives de ≈ 0.145 r1.046 (95% bootstrap CI [1.019, 1.062],
R2 = 0.977) across roughly eight decades. The fitted slope is a pooled finite-range calibration
coefficient; the Hölder exponent in Proposition 1 is system-local. An independent 80-
problem check gives slope 1.024 with 10, 50, or 100 projection starts; the densest protocol
improves 11/80 proxies and leaves their median ratio at 1.00. With κ̂ = 0.350, this stable
near-unit fit defines the empirical gate; scaling remains stable through n = 12 (App. D).
On 40 engineered systems g( x ) = p( x )2 ≤ 0, the within-instance exponent is 0.505 ± 0.017
(Fig. 3b), realizing the quadratic-growth regime.

Triage under a common repair operator. On 360 held-out instances at β = 0.25R, the
gate reaches 28.3% feasible yield with 53 repairs, versus 35.0% with 299 for repair-all
(Table 1). It recovers (28.3 − 16.9)/(35.0 − 16.9) = 63.0% of repair-all’s additional yield
using 53/299 = 17.7% of its attempts, with 77.4% repair precision. The calibrated relation
covers 342/360 = 95.0% of held-out projection proxies (Wilson CI [92.2, 96.8]%; residual–
proxy Spearman 0.932). At this budget, the gate and residual ranking select the same 53
endpoints; calibration adds a geometric budget interpretation and held-out coverage. The
cutoff sweep appears in App. D, Fig. 5. With repair price cr and unresolved-endpoint retry
price cv , the observed counts give Cgate = 53cr + 258cv and Call = 299cr + 234cv , so gating
is cheaper exactly when cr /cv > 0.098 (derivation in App. D).


                                                   7
Preprint. Under review.




multi-start projection distance d(xc, )
̃
                                                           (a) generic SDR-relaxed QCQPs                                               (b) degenerate family: θ̂ = 0.505 ± 0.017




                                                                                                         distance to {p = 0}
                                            10   1
                                                         n=3
                                                                                                                                100
                                                                                                                                            perturbed points (40 instances)
                                                         n=4
                                                                                                                                            slope 1/2 reference
                                                −2       n=5
                                           10            n=6
                                                         n=8
                                                                                                                               10−2
                                                         fit θ̂ = 1.05 (R 2 = 0.98)
                                           10−5
                                                         slope 1 reference



                                                         10−5            10−3         10−1   101                                          10−5 10−4 10−3 10−2 10−1                100
                                                     residual r(xc) (SDR on original constraints)                                                     residual r = p(x)       2




Figure 3: Residual–projection-distance scaling on generic SDR-relaxed QCQPs and engi-
neered degenerate polynomial instances. (a) Generic QCQPs: de( xc , F ) ≈ 0.145 r1.05 , where
de ≥ dist is the multi-start projection proxy, R2 = 0.98 (n = 325 instances, colored by di-
mension). (b) Engineered degenerate family (vanishing active gradients): within-instance
exponent θ̂ = 0.505 ± 0.017, the quadratic-growth regime.

                                             Endpoint policy                                 usable yield                             repair attempts         repair precision
                                             Binary accept-only (NC2C Eq. 14)                      16.9%                                    0                          –
                                             Repair-all (budget β = 0.25R)                         35.0%                                   299                       21.7%
                                             Residual-gated triage (ours)                          28.3%                                   53                        77.4%


Table 1: Endpoint verification on 360 held-out SDR-relaxed instances. “Usable yield” is
the fraction of instances ending numerically feasible; “repair attempts” are bounded local-
correction runs; precision is successful repairs per attempt.


6                                          Experiments II: path ablation with an LLM

The case-study experiments isolate the feedback mechanism. We next run a controlled LLM
ablation to price the successive stage packages against direct prediction.

Design. We generate 30 natural-language QCQPs (n ∈ {2, 3, 4}, m = 3n) whose rounded
coefficients appear verbatim, defining a controlled literal-transcription regime. Each prob-
lem receives three samples per arm from fixed gpt-5.5 settings (medium effort, schema-
enforced JSON): D returns a numeric solution directly; F commits a formal program executed
by SLSQP; FC additionally selects SDR or one-shot inner majorization (OSM); and FCV adds
residual triage and bounded repair. D–F compares formal representation plus deterministic
execution with direct generation under literal coefficient transcription and a standardized
strictly feasible initialization x = 0. OSM instantiates one committed SCA-style surrogate
transition anchored at that initialization. A result is usable when it is 10−6 -feasible and
within 0.05R of the best-known 26-start oracle. Appendix E provides prompts, schemas,
transcripts, loose tolerance results, and the full protocol. This design fixes a low-friction exe-
cution regime: literal transcription, a constructive feasible initialization, and cheap reliable
local solves. F is therefore expected to lead at this pricing point. Certificate-driven tasks,
initialization-poor problems, and regimes where local solves stall increase the value of FC
and can reverse the stage ordering. CPR treats transcription difficulty, initialization quality,
solver reliability, and certificate value as explicit regime variables.

Results. All 270 unique calls shared across nested arms parsed against their schemas with
0 tool events. Table 2 and Fig. 4 report the utility and cost of each nested stage package.
Formal transcription with deterministic solver execution is the most effective package in this regime.
It lifts usable yield from 41.1% to 90.0% (23 F wins, 3 D wins, and 4 ties; two-sided exact sign
test p = 8.8 × 10−5 after excluding ties) and lowers every reported cost per usable solution
(Table 2).



                                                                                                     8
Preprint. Under review.




                               (a) utility                                                    (b) complete LLM token cost                                       (c) end-to-end time cost




                                                          tokens / usable (thousands)
                                   F random init. (73%)                                 150




                                                                                                                                wall-clock / usable (s)
                                                                                                 input       output 135                                         610
                              90   tol. 10−6                                                                              128                             600
usable yield (%)   100             tol. 10−3


                    75                                                                  100
                                                                                                                                                          400
                                                                                                                                                                              327    310
                         41
                    50
                                     20        21                                        50     46
                                                                                                                                                          200
                    25
                                                                                                         16
                                                                                                                                                                       39
                     0                                                                    0                                                                 0
                          D    F       FC      FCV                                              D        F         FC     FCV                                   D      F      FC     FCV


Figure 4: Stage-package pricing. (a) Usable yield at two feasibility tolerances; strict-yield
error bars are problem-level bootstrap intervals, and the diamond marks F with seeded
random initialization. (b) Complete LLM input and output tokens per usable solution. (c)
LLM plus executor wall-clock per usable solution.

            Arm                              calls usable % [CI] ret./prec. % in/use (k) out/use (k) wall/use (s)
            Direct (D)                        1           41.1 [29,52]                               100.0 / 46.7           31.0                                14.6           610
            Formalize (F)                     1           90.0 [77,100]                              100.0 / 100.0          14.4                                 1.1            39
            +Convexify (FC)                   2            20.0 [9,32]                                100.0 / 62.2         127.4                                 7.8           327
            +Verify/repair (FCV)              2           21.1 [10,33]                               63.3 / 100.0          120.7                                7.4            310


Table 2: Path ablation (30 × 3 per arm), against ground truth. Calls = LLM calls/sample;
ret./prec. gives returned coverage and feasibility among returned answers; usable = 10−6 -
feasible with gap ≤ 0.05R to the best-known oracle (SDR-certified global on 12/30 problems;
per-problem bootstrap CIs; App. E). Cost columns report input tokens, output tokens, and
total LLM+executor wall-clock per usable output. The 270 unique calls comprise 90 D, 90 F
(shared by F/FC/FCV), and 90 C (shared by FC/FCV).


F exactly transcribes all 90 programs; deterministic execution totals 0.1s and has zero output
dispersion. The remaining unusable cases are feasible local solutions with large oracle gaps.
Initialization is a measured stage-design variable. Warm-start sensitivity is 90.0% usable yield
from the standardized feasible origin and 73.0% across seeded random starts, attributing
17.0 percentage points of usable yield to initialization (App. E).
Convexification exposes two stage-specific error modes. Adding the convexification commitment
changes yield to 20.0%. SDR is usable on all tight cases (18/18) and infeasible on all
measurably loose cases (0/34), exposing relaxation leakage. OSM is feasible in 38/38
cases but usable in 0/38, exposing conservative over-contraction. Detection matches the
indefinite set in 90/90 calls; strategy varies on 21/30 problems. Per-problem usable counts
give 25/0/5 F wins/FC wins/ties, quantifying the cost of the surrogate commitment in this
regime.
Verification raises returned-answer precision. FCV returns 57/90 = 63.3% of answers with
100% feasibility, versus 62.2% for FC, and changes usable yield from 20.0% to 21.1%. The
transferred gate covers 30/34 endpoints (88.2%). F retains the highest yield at 90.0%; the
ablation prices the committed convexification stage through its observed relaxation leakage,
over-contraction, and execution cost. FCV versus FC gives 1/0/29 wins/losses/ties by
problem, localizing the recovery to one problem.


7                  Experiments III: feedback-conditioned action changes

We evaluate one feedback transition on two committed states per problem. Actions
keep/repair the endpoint (A), switch SDR↔OSM (B), roll back to the formal non-convex
program (C), or abstain (D). In 120 independent pre/post calls, feedback adds execution
status, residual, objective, SDR bound, and gap.


                                                                                                         9
Preprint. Under review.




    Metric                               state only state + feedback     paired change [95% CI]
    Reported allocation entropy (nats)    1.092          0.679         0.413 decrease [0.306, 0.523]
    Reported usable allocation mass       32.5%          38.9%              +6.3 pp [0.6, 12.8]
    Reported feasible allocation mass     71.1%          80.9%              +9.8 pp [3.7, 16.1]
    Selected-action usable yield          18.3%          36.7%             +18.3 pp [8.3, 30.0]

Table 3: Paired-condition experiment (60 states, 120 independent calls). Entropy is com-
puted from schema-elicited action allocations; usability comes from deterministic offline
execution against ground truth. Paired changes and confidence intervals are computed from
unrounded values, then rounded for display.


The model selects one action for ground-truth execution and reports an A–D allocation for
the interface-concentration diagnostic. Primary outcomes are selected-action change and
executed utility; bootstrap intervals resample problems.
Feedback changes 16/60 selections: 11 improve usability, 5 are neutral, and 0 are harmful.
Selected usable yield rises 18.3%→36.7%. Always-C and a rule that keeps only a feasible
endpoint within 0.05R of the SDR bound both reach 54/60 = 90.0%, versus 36.7% for the
selector. Their estimated executor totals are 0.042 s and 0.034 s, while 60 post-feedback
controller calls use 633.5 s, exposing a decision-quality and controller-cost gap.
Reported allocation entropy decreases by 0.413 nats and usable mass rises by 6.3 points
(Table 3); nevertheless, 6 entropy-expanding pairs gain usable mass and 28 concentrating
pairs lose it. The diagnostic therefore pairs concentration with executed utility at a fixed
action interface.


8    Discussion and conclusion

Self-proposal and executable validation. A 24-output pilot elicits provisional states within
the receiving call from the natural-language problem alone (App. H). Two-repeat collision
entropy is 0.629 nats in both conditions and usable yield is 25.0% direct versus 8.3% with self-
proposal; deterministic evaluation confirms 1/8 recorded endpoint checks. This boundary
assigns proposals to the model and trust to executable feedback.

Transplanted-state concentration and utility. On six problems, receiving calls condi-
tion on another trajectory’s surrogate state. Endpoint entropy falls 1.301→0.512 (∆H =
0.789 [0.172, 1.482]), while acceptable mass falls 30.6%→2.8% despite feasibility rising
33.3%→86.1% (App. G). The transplant concentrates feasible, objective-poor endpoints,
realizing the predicted provenance-sensitive failure mode of an unverified hard commit-
ment.

Implications and takeaways. In the measured low-friction regime, F is the highest-value
package, FC exposes relaxation leakage and over-contraction, and random starts assign 17
yield points to initialization. For pipelines with committed executable interfaces, compare
shared-call nested packages with stage-local checks, and price a transformation against
the target distribution’s leakage and over-contraction rates. Reserve hard constraints for
trusted or executor-verified invariants; keep model-proposed states soft and reversible until
validation. A continuous residual maps a repair budget to a cutoff; repair and retry prices
select the policy (here cr /cv = 0.098). Certificate value, initialization, solver reliability, and
the cost vector index the audit.

Conclusion and reproducibility. CPR pairs a source-aware path hypothesis with an exe-
cutable stage audit. The case study prices formalization, surrogate commitment, verification,
and feedback; the endpoint probes show how provenance and executable validation govern
commitment strength. Fixed-seed scripts and logged outputs reproduce every analysis; the
supplement contains code, prompts, schemas, data, logs, and collection audits.


                                                  10
Preprint. Under review.




References
Ali AhmadiTeshnizi, Wenzhi Gao, and Madeleine Udell. OptiMUS: Optimization modeling
  using MIP solvers and large language models. In International Conference on Machine
  Learning, 2024.
Kamel Alrashedy, Vriksha Srihari, Zulfiqar Zaidi, Ridam Srivastava, Pradyumna Tamb-
 wekar, and Matthew Gombolay. Constraints-of-thought: A framework for constrained
  reasoning in language-model-guided search. arXiv preprint arXiv:2510.08992, 2025.
Maciej Besta, Nils Blach, Ales Kubicek, Robert Gerstenberger, Michal Podstawski, Lukas
 Gianinazzi, Joanna Gajda, Tomasz Lehmann, Hubert Niewiadomski, Piotr Nyczyk, and
 Torsten Hoefler. Graph of thoughts: Solving elaborate problems with large language
 models. In Proceedings of the AAAI Conference on Artificial Intelligence, 2024.
Jérôme Bolte, Trong Phong Nguyen, Juan Peypouquet, and Bruce W Suter. From error
   bounds to the complexity of first-order descent methods for convex functions. Mathemati-
   cal Programming, 165(2):471–507, 2017.
Xingyu Chen, Jiahao Xu, Tian Liang, Zhiwei He, Jianhui Pang, Dian Yu, Linfeng Song,
  Qiuzhi Liu, Mengfei Zhou, Zhuosheng Zhang, Rui Wang, Zhaopeng Tu, Haitao Mi, and
  Dong Yu. Do NOT think that much for 2+3=? On the overthinking of o1-like LLMs. arXiv
  preprint arXiv:2412.21187, 2024.
Steven Diamond and Stephen Boyd. CVXPY: A Python-embedded modeling language for
  convex optimization. Journal of Machine Learning Research, 17(83):1–5, 2016.
Dmitriy Drusvyatskiy and Adrian S Lewis. Error bounds, quadratic growth, and linear
 convergence of proximal methods. Mathematics of Operations Research, 43(3):919–948, 2018.
Kanishk Gandhi, Denise Lee, Gabriel Grand, Muxin Liu, Winson Cheng, Archit Sharma,
  and Noah D Goodman. Stream of search (SoS): Learning to search in language. arXiv
  preprint arXiv:2404.03683, 2024.
Shibo Hao, Yi Gu, Haodi Ma, Joshua Jiahua Hong, Zhen Wang, Daisy Zhe Wang, and Zhiting
  Hu. Reasoning with language model is planning with world model. In Proceedings of the
  2023 Conference on Empirical Methods in Natural Language Processing, 2023.
Shibo Hao, Sainbayar Sukhbaatar, DiJia Su, Xian Li, Zhiting Hu, Jason Weston, and Yuan-
  dong Tian. Training large language models to reason in a continuous latent space. arXiv
  preprint arXiv:2412.06769, 2024.
Alan J Hoffman. On approximate solutions of systems of linear inequalities. Journal of
  Research of the National Bureau of Standards, 49(4):263–265, 1952.
Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa.
  Large language models are zero-shot reasoners. In Advances in Neural Information Process-
  ing Systems, 2022.
Zhiyuan Li, Hong Liu, Denny Zhou, and Tengyu Ma. Chain of thought empowers trans-
  formers to solve inherently serial problems. arXiv preprint arXiv:2402.12875, 2024.
Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee,
 Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. In
 International Conference on Learning Representations, 2024.
Thomas Lipp and Stephen Boyd. Variations and extension of the convex–concave procedure.
  Optimization and Engineering, 17(2):263–287, 2016.
Ximing Lu, Peter West, Rowan Zellers, Ronan Le Bras, Chandra Bhagavatula, and Yejin
  Choi. NeuroLogic decoding: (un)supervised neural text generation with predicate logic
  constraints. In Proceedings of the 2021 Conference of the North American Chapter of the
  Association for Computational Linguistics, 2021.


                                            11
Preprint. Under review.




Linhao Luo, Zicheng Zhao, Gholamreza Haffari, Yuan-Fang Li, Chen Gong, and Shirui
  Pan. Graph-constrained reasoning: Faithful reasoning on knowledge graphs with large
  language models. arXiv preprint arXiv:2410.13080, 2024.
Zhi-Quan Luo and Xiao-Dong Luo. Extension of Hoffman’s error bound to polynomial
  systems. SIAM Journal on Optimization, 4(2):383–392, 1994.
Zhi-Quan Luo, Wing-Kin Ma, Anthony Man-Cho So, Yinyu Ye, and Shuzhong Zhang.
  Semidefinite relaxation of quadratic optimization problems. IEEE Signal Processing Maga-
  zine, 27(3):20–34, 2010.
Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegr-
 effe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bod-
 hisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir Yazdanbakhsh, and
 Peter Clark. Self-refine: Iterative refinement with self-feedback. In Advances in Neural
 Information Processing Systems, 2023.
Garth P McCormick. Computability of global solutions to factorable nonconvex programs:
 Part I—convex underestimating problems. Mathematical Programming, 10(1):147–175, 1976.
William Merrill and Ashish Sabharwal. The expressive power of transformers with chain of
 thought. In International Conference on Learning Representations, 2024.
Allen Newell and Herbert A Simon. Computer science as empirical inquiry: Symbols and
  search. Communications of the ACM, 19(3):113–126, 1976.
Huynh Van Ngai and Michel Théra. Error bounds in metric spaces and application to the
 perturbation stability of metric regularity. SIAM Journal on Optimization, 19(1):1–20, 2008.
Jong-Shi Pang. Error bounds in mathematical programming. Mathematical Programming, 79
  (1–3):299–332, 1997.
Xinyue Peng, Yanming Liu, Yihan Cang, Yuwei Zhang, Xinyi Wang, Songhang Deng, and
  Jiannan Cao. NC2C: Automated convexification of generic non-convex optimization
  problems. arXiv preprint arXiv:2601.04789, 2026.
Ben Prystawski, Michael Y Li, and Noah D Goodman. Why think step by step? Reasoning
  emerges from the locality of experience. In Advances in Neural Information Processing
  Systems, 2023.
Stephen M. Robinson. Stability theory for systems of inequalities, Part II: Differentiable
  nonlinear systems. SIAM Journal on Numerical Analysis, 13(4):497–513, 1976.
R Tyrrell Rockafellar and Roger J-B Wets. Variational Analysis. Springer, 1998.
Torsten Scholak, Nathan Schucher, and Dzmitry Bahdanau. PICARD: Parsing incrementally
  for constrained auto-regressive decoding from language models. In Proceedings of the 2021
  Conference on Empirical Methods in Natural Language Processing, 2021.
Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao.
 Reflexion: Language agents with verbal reinforcement learning. In Advances in Neural
 Information Processing Systems, 2023.
Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. Scaling LLM test-time com-
 pute optimally can be more effective than scaling model parameters. arXiv preprint
 arXiv:2408.03314, 2024.
Yang Sui, Yu-Neng Chuang, Guanchu Wang, Jiamu Zhang, Tianyi Zhang, Jiayi Yuan, Hongyi
  Liu, Andrew Wen, Shaochen Zhong, Na Zou, Hanjie Chen, and Xia Hu. Stop overthinking:
  A survey on efficient reasoning for large language models. arXiv preprint arXiv:2503.16419,
  2025.
Jonathan Uesato, Nate Kushman, Ramana Kumar, Francis Song, Noah Siegel, Lisa Wang,
  Antonia Creswell, Geoffrey Irving, and Irina Higgins. Solving math word problems with
  process- and outcome-based feedback. arXiv preprint arXiv:2211.14275, 2022.


                                             12
Preprint. Under review.




Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed Chi, Sharan Narang, Aakanksha
  Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in
  language models. In International Conference on Learning Representations, 2023.
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi,
  Quoc V Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large
  language models. In Advances in Neural Information Processing Systems, 2022.
Ziyang Xiao, Dongxiang Zhang, Yangjun Wu, Lilin Xu, Yuan Wang, Xiongwei Han, Xiaojin
  Fu, Tao Zhong, Jia Zeng, Mingli Song, and Gang Chen. Chain-of-experts: When LLMs
  meet complex operations research problems. In International Conference on Learning
  Representations, 2024.
Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L Griffiths, Yuan Cao, and
  Karthik Narasimhan. Tree of thoughts: Deliberate problem solving with large language
  models. In Advances in Neural Information Processing Systems, 2023.

Public reproducibility release. Code, processed experimental records, figure-generation
scripts, prompts, and schemas are available at https://github.com/RedForestLonvor/
Constrained-Path-Reasoning.

A     Stage-interface measurement map

Table 4 connects each CPR measurement dimension to its case-study operationalization and
empirical evidence.

  Measurement dimension      Case-study operationalization           Empirical evidence
  Transition factorization   NL → program → surrogate → solution     per-stage exactness and stage-package
                             stages                                  cost/yield (Tables 2, 6)
                                               C
  State-space contraction    candidate-level qθ k ; fixed A–D        paired-condition allocation change and
                             allocation as a local instantiation     executed action utility (Table 3); fixed endpoint
                                                                     entropy and acceptable mass under state
                                                                     transplantation (App. G); collision diagnostic
                                                                     under elicited self-proposal (App. H)
  Regularity induction       numerical convex-surrogate solve; SDR   solver success; SDR lower bounds (oracle
                             lower bounds and dual diagnostics       certified on 12/30)
                             where available
  Feedback                   endpoint residual r ( xc )              residual–projection-distance fit, gate coverage,
                                                                     triage yield/precision (Table 1)



Table 4: Theory-to-measurement map. Fixed action interfaces measure local concentra-
tion; endpoint interfaces probe state transplantation and elicited self-proposal. Regularity,
feedback, localized error, and cost use executor outputs.


B     Continuous constrained-path formulation

Let ϕ : Rd × [0, T ] → Rm be continuously differentiable and let Minv           t   = {z : ϕ(z, t) = 0}
encode a prescribed or independently certified physical, logical, or geometric invariant. A
pre-learned manifold enters this hard set after the same validation. Assume the Jacobian
Jt = Dz ϕ(zt , t) has full row rank along the path. Given a base drift vt = f 0 (zt , t, x ) +
gθ (zt , t, x ), combining a known prior ODE f 0 with a learned residual gθ , the least-norm
normal correction is
                       ut = − Jt⊤ ( Jt Jt⊤ )−1 ∂t ϕ(zt , t) + Jt vt ,
                                                                   
                                                                      żt = vt + ut .
         d
It gives dt ϕ(zt , t) = Jt żt + ∂t ϕ = 0; an initially admissible path therefore follows the moving
manifold while retaining the tangential component of vt . Time-varying inequality sets can
be represented by the corresponding projected differential inclusion using the normal cone
of the admissible set.


                                                      13
Preprint. Under review.




For an uncertified learned manifold M   ct = { z : ϕ
                                                   bψ (z, t) = 0}, CPR uses a finite attraction
                          2
such as −λt ∇z ∥ϕψ (z, t)∥ /2, or a confidence tube, inside the base drift. Validation controls
                b
λt and can promote the proposal to the hard invariant above. Finite attraction preserves
departures, revision, and competing hypotheses during heuristic search.
This formulation supplies two continuous analogues of the discrete CPR quantities. First,
for a fixed reference measure, an endpoint or latent-state density ρt transported by the
tangential field obeys a continuity equation; on a fixed manifold, ∂t ρt + ∇M · (ρt żt ) = 0
and its differential-entropy rate is the expected intrinsic divergence. Learned manifold
dimension, divergence, reachable volume, and fixed checkpoint probes therefore provide
                                                                     d
distinct concentration diagnostics. Second, if perturbations satisfy dt ∥et ∥ ≤ L(t)∥et ∥ + η (t),
Grönwall’s inequality gives
                                    RT                 Z T RT
                          ∥eT ∥ ≤ e 0 L(r)dr ∥e0 ∥ +        e s L(r)dr η (s)ds,
                                                        0

the continuous counterpart of Eq. (7). Discrete operator paths are compositions or numerical
discretizations of these flows; hybrid CPR alternates continuous segments with symbolic
or tool-execution commitments. The endpoint experiments use discrete interfaces. The
self-proposal pilot generates its exposed states within the receiving call; an endogenous
continuous-path experiment would sample checkpoints within each flow realization and
apply the same fixed endpoint probe.

C    Proof and discussion of Proposition 1

Throughout, F = { x ∈ Rn : gi ( x ) ≤ 0, h j ( x ) = 0} is non-empty, gi , h j ∈ C1 , and
r is (11); distances are Euclidean. A bounding constraint (in our instances the smooth
ball ∥ x ∥2 − R2 ≤ 0) is among the gi and enters r, so F and each tube Uδ0 are compact,
and every xc has a (possibly non-unique) projection x ⋆ ∈ arg minx∈F ∥ x − xc ∥ with ∥ xc −
x ⋆ ∥ = dist( xc , F ). The harness evaluates the ball contribution as (∥ x ∥ − R)+ . Outside the
ball, ∥ x ∥2 − R2 = (∥ x ∥ − R)(∥ x ∥ + R); on each bounded tube the two forms are locally
equivalent, changing the modulus but preserving the error-bound exponent.

Parts (i)–(iii). Since r ( xc ) ≤ δ0 by assumption, (EBθ ) applies at xc ; if additionally r ( xc ) ≤
(ε/κ )1/θ , then dist( xc , F ) ≤ κr ( xc )θ ≤ ε; take x ⋆ the projection. Part (ii) is identical with
β in place of ε. Part (iii) says the bound becomes non-informative at radius β: for r ( xc ) >
( β/κ )1/θ the bound (EBθ ) yields only dist ≤ κr θ , whose right-hand side exceeds β. Part (iii)
therefore marks the boundary of the radius-β certificate; §5 measures realized repair yield
on both sides of this boundary.                                                                     □

Part (a): the regular regime. The one-constraint case gives the core argument. Let a
single inequality g be active with ∇ g ̸= 0 on the boundary; by compactness and continuity
choose δ0 > 0 and γ > 0 with ∥∇ g( x )∥ ≥ γ on the tube T = {0 < g ≤ δ0 }. Fix
x ∈ T with g( x ) = ρ and follow unit-speed steepest descent u̇ = −∇ g(u)/∥∇ g(u)∥ from
                   d
x: while in T, ds    g(u(s)) = −∥∇ g(u(s))∥ ≤ −γ, so g hits zero by arclength s⋆ ≤ ρ/γ,
and dist( x, F ) ≤ ∥u(s⋆ ) − x ∥ ≤ ρ/γ = r ( x )/γ, i.e. (EBθ ) with θ = 1, κ = 1/γ. For
general systems, assume MFCQ holds at every x̄ ∈ F . At each such point it implies              
metric regularity at ( x̄, 0) of the set-valued constraint mapping M ( x ) = g( x ), h( x ) −
 Rm
             
   − × {0} (Robinson, 1976). Thus there are a neighborhood Vx̄ and modulus κ x̄ for which
dist( x, F ) ≤ κ x̄ dist(0, M ( x )) on Vx̄ . Finite-dimensional norm equivalence lets the max-
residual (11) control dist(0, M ( x )). Compactness of F provides a finite subcover V1 , . . . , VN ;
taking the largest of the corresponding moduli gives a uniform linear residual bound
on V = iN=1 Vi ⊇ F (Rockafellar & Wets, 1998; Pang, 1997). The bound extends from
           S

V to the whole tube: on the compact set Uδ0 \ V the continuous residual has a positive
minimum rmin > 0 (since r −1 (0) = F ⊂ V) while dist(·, F ) is bounded by some D < ∞,
so dist( x, F ) ≤ ( D/rmin ) r ( x ) there; taking the larger of the two moduli gives (EBθ ) with


                                                 14
Preprint. Under review.




θ = 1 on all of Uδ0 . Under LICQ the local modulus can be bounded in terms of the smallest
singular value of the active Jacobian; the exact relation between error-bound moduli and
Jacobian spectra depends on the local nonlinear geometry.                               □

Part (b): the quadratic-growth regime. Assume there are µ > 0, δ0 > 0 with r ( x ) ≥
µ dist( x, F )2 on Uδ0 (quadratic growth of the violation transverse to F ; the implication
below is elementary algebra—cf. quadratic-growth/error-bound equivalences in convex
settings (Drusvyatskiy & Lewis, 2018)). Then dist( x, F ) ≤ µ−1/2 r ( x )1/2 , i.e. (EBθ ) with
θ = 12 , κ = µ−1/2 . This exponent is attained: for g( x ) = p( x )2 ≤ 0 with p ∈ C2 , ∇ p ̸= 0 on
S = { p = 0} = F , one has r = p2 while dist( x, S) = | p( x )|/∥∇ p∥ + o (| p( x )|) near S, so
dist ≍ r1/2 and no exponent θ > 12 can hold as r → 0.                                                □
Remark 1 (Higher-order degeneracy). Higher-order degeneracy produces other exponents:
g( x ) = x4 ≤ 0 on [−1, 1] has F = {0}, r ( x ) = x4 , dist( x, F ) = | x | = r ( x )1/4 , so the sharp
(EBθ ) exponent is θ = 14 ; anisotropic degeneracies can mix exponents by direction. The
verifier therefore accepts the (κ, θ ) pair—analytical or calibrated—that describes the target
instance family.
Remark 2 (Certificate vs. gate). When (κ, θ ) come from verified constraint qualifications,
the tier decisions of Proposition 1 are guarantees. When they come from the empirical
calibration of §4.2, (κ̂, θ̂ ) define a power-law predictor whose semantics are summarized by
held-out coverage (95.0% with respect to the projection proxy de here).


D    Case-study experimental details

Instance generator. c ∼ N (0, I ) normalized; Ak = Q diag(λ) Q⊤ with Q Haar-orthogonal
and mixed-sign λ, negative eigenvalues scaled by a non-convexity factor ∼ U [1.5, 4.5] (at
least one negative eigenvalue enforced); bk ∼ N (0, I ); dk ∼ −U [0.5, 3] (so x = 0 is strictly
feasible); R ∼ U [3, 8]; n ∈ {3, 4, 5, 6, 8}, m ∈ {3, 4} · n. SDR solved with CLARABEL (SCS
fallback) via CVXPY (Diamond & Boyd, 2016).

Projection proxy and repair. For starts xc , 0, and 8 random points, let x̃ℓ ∈ F be each
feasible SLSQP projection return. We use de( xc , F ) = minℓ ∥ xc − x̃ℓ ∥2 ≥ dist( xc , F ). Repair
uses projected subgradient descent on Φ( x ) = ∑k max(0, qk ( x ))2 + max(0, ∥ x ∥ − R)2 with
fixed step 2R/160; the cumulative path length at the first numerically feasible iterate is
recorded per instance, so success at any radius budget β is evaluable post hoc without
re-running.


Fitting and calibration. Log–log least squares of de on r over instances with r > 10−6 ; 95%
                                                               e θ̂ on the calibration split.
CIs from 2,000-sample bootstrap; κ̂ is the 95th percentile of d/r
Experiment sizes: E1 380 generated / 325 with r > 0; degenerate family 40 instances × 24
perturbation magnitudes; verification 360 held-out instances; scaling 4 × 110. This gives
1,180 generated QCQPs plus 40 engineered degenerate polynomial instances, and 2,140
evaluated endpoints (counting the 24 perturbations for each degenerate problem); the full
suite takes ≈ 47 s on a laptop CPU. Seeds are fixed in run experiments.py.

Projection-density sensitivity. An independent fixed-seed bank of 80 generated QCQPs
reuses each SDR endpoint while increasing the total projection starts from 10 to 50 and
100. Among the 67 violated endpoints used in each fit, the slopes are 1.02397, 1.02375,
and 1.02375, with R2 = 0.963, 0.963, and 0.963. The 100-start protocol improves 11/80
projection proxies relative to 10 starts; the median and mean ratios de100 /de10 are 1.000 and
0.995. This stable within-bank result assigns the small superlinear offset primarily to pooled
cross-system scaling and the finite numerical range. The archive includes the script, all
per-instance proxies, and the three fitted summaries.


                                                  15
Preprint. Under review.




Calibration support (§4.2). The fit-set residuals span [rmin , rmax ] = [1.05 × 10−6 , 56.7],
containing every held-out infeasible endpoint and all 34 infeasible LLM-formalized end-
points. The 61 endpoints below rmin are already numerically feasible (r ≤ 10−6 ). Thus every
accept/repair decision on an infeasible endpoint uses the power law within calibration
support.

                                          n                                         4             6             8            12
                                          θ̂                                     1.053         1.080         1.053         1.063
                                          κ̂ls (least-squares K)                 0.152         0.151         0.137         0.127
                                          R2                                     0.977         0.987         0.992         0.995

Table 5: Scaling of the fitted residual–projection-distance relation with dimension (m = 3n,
≥ 75 violated instances per column). The fitted exponents are 1.053–1.080 and the constants
are 0.127–0.152 across dimensions.


Operating point of Table 1. ε = 0.02R, β = 0.25R; δ1 = (ε/κ̂ )1/θ̂ , δ2 = ( β/κ̂ )1/θ̂ . Tier
counts at this point: 77 NEAR - FEASIBLE (of which 61 already numerically feasible), 37 REPAIR,
246 REJECT. Repair-all and the gated policy use the identical repair operator and budget;
differences are purely which endpoints they attempt. Sweeping budget and gate together
produces a separate budget-sensitivity curve. Figure 5 instead fixes the operational cap at
β = 0.25R and varies only the selection threshold δ2 ; its marked point uses δ2 = ( β/κ̂ )1/θ̂ .

Break-even cost model. Let cr be the price of a repair attempt and cv the expected down-
stream price of retrying or re-convexifying an unresolved endpoint. Repair-all makes 299
attempts and leaves 234 endpoints unresolved; the gate makes 53 attempts and leaves 258
unresolved. Hence
                                              Call = 299cr + 234cv ,                      Cgate = 53cr + 258cv .
The gate has lower total price precisely when 246cr > 24cv , or cr /cv > 0.09756. This
boundary turns the observed cost–yield frontier into a deployment rule: repair-all covers
the low-repair-price region, and residual triage covers the high-repair-price/high-retry-
value region.

                                                selection frontier of the residual gate (fixed repair budget β = 0.25R)
                               repair-all at this budget (35.0%, 299 attempts)
       usable yield (%)




                                                                                 residual-threshold sweep (δ2), repair cap fixed
                          30
                                                    calibrated cutoff

                          20                                                            binary accept-only (16.9%)


                                              50                 100             150             200                          250   300
                                                             repair attempts (each = one local correction run)



Figure 5: Residual-ranking frontier with the operational repair-path cap fixed at β = 0.25R.
The curve sweeps only the selection cutoff δ2 ; every selected endpoint receives the same
repair cap. The marked calibrated cutoff is δ2 = ( β/κ̂ )1/θ̂ .


E   Path-ablation protocol and additional results
Problem bank. 30 problems (n ∈ {2, 3, 4}, 10 each, m = 3n), generated from the §5 family
with all coefficients rounded to three decimals; the rounded values are the ground truth
and appear verbatim in the NL text (Fig. 6). By construction x = 0 is strictly feasible.
Reference values per problem: best-known objective from a 26-start SLSQP oracle on
the true problem (unchanged under 100 starts on all 30 problems; the SDR lower bound
certifies global optimality on 12/30), and the true-SDR residual as a looseness marker (19/30


                                                                                    16
Preprint. Under review.




problems have loose SDR). On the 12 SDR-certified problems, D/F/FC/FCV usable yield
is 52.8/100.0/50.0/52.8%; on the 18 problems evaluated against best-known multi-start
values it is 33.3/83.3/0.0/0.0%. The FC/FCV failures concentrate on loose-SDR problems.
Precisely, 18/19 loose-SDR problems belong to the uncertified subset, all 18/18 uncertified
problems have loose SDR, and the remaining loose-SDR problem (ID 18) is SDR-certified.


   A planner chooses 2 decision variables x1..x2.
   They want to MINIMIZE the cost f(x) = 0.186*x1 - 0.983*x2.
   The choice must satisfy ALL of the following constraints:
   (C1) -0.967*x1ˆ2 - 6.875*x1*x2 - 3.995*x2ˆ2 + 0.846*x1 + 0.063*x2 - 1.424 <= 0
   . . . (five more quadratic constraints) . . .
   (C7) the Euclidean norm bound sqrt(x1ˆ2 + ... + x2ˆ2) <= 6.0


     Figure 6: Example natural-language problem (abridged; problem 0 of the bank).



 LLM configuration. All calls: codex exec --sandbox read-only --ephemeral -m gpt-5.5
-c model reasoning effort="medium" --json --output-schema <schema>. The prompt
prohibits tool use and demands a single JSON object; the JSONL event logs confirm zero
 command/tool events across all calls (CLI codex-cli 0.144.1; calls issued 2026-07-11 to
 07-13). The CLI uses provider-default stochastic sampling; the three samples per problem
 are repeated calls, and statistical comparisons use problems as units. Each problem × sam-
ple makes one call per LLM stage: Direct (arm D), Formalize (shared by arms F/FC/FCV),
 Convexify-given-formalization (shared by FC/FCV); 270 calls total. Raw event logs, final
 messages, parsed outputs, and per-call token/wall-clock accounting are all in the supple-
 mentary material.


Deterministic executors. Arm F: SLSQP from the origin on the formalized non-convex
program (300 iterations); the origin is a warm start (x = 0 feasible by construction), and
from seeded random starts in the ball the same executor’s usable rate is 73.0% (mean over
10 starts per problem) vs. 90.0% from the origin (local robustness.py). Arm FC: strategy
applied to the model’s formalization—SDR via the §5 lifting; “SCA” as one SCA-style inner
majorization (OSM) anchored at x0 = 0 by dropping each quadratic’s concave part; results
target the single committed surrogate. “Already convex” is valid when every Pk is positive
semidefinite, with other selections recorded as strategy errors. Arm FCV: triage with the §5
gate (κ̂ = 0.350, θ̂ = 1.046, ε = 0.02R, β = 0.25R) on the model’s own formalization; gated
infeasible endpoints get bounded repair, and the post-repair residual check returns only
feasible endpoints.


Evaluation. Ground-truth residual (11), feasibility at tight (10−6 ) and loose (10−3 ) toler-
ances, and the signed objective gap f ( x ) − f bk to the best-known oracle value; usable
= numerically feasible at 10−6 and gap ≤ 0.05R. The 5/270 sub-oracle gaps are all
<6 × 10−7 and are treated as numerical ties. Table 6 reports usable rates at gap thresholds
0.02R/0.05R/0.1R; the arm ordering is unchanged. Formalization exactness: canonicalized
coefficient match within 10−6 . Detection exactness: claimed non-convex index set equals
the indefinite set of the model’s own formalization. Dispersion: mean pairwise ℓ2 distance
between the final answers of the 3 samples, divided by R.


Per-stage measurements. Table 6 isolates each LLM stage against its own exactly-checkable
target (formalization against the embedded ground-truth coefficients; detection against the
indefinite set of the model’s own formalization), separating model error from error injected
by the committed transitions themselves. Figure 7 localizes the resulting package utility by
problem and SDR regime.


                                             17
Preprint. Under review.




     Stage measurement                                                                                                                       value
     Direct: parse rate                                                                                                            100.0%
     Formalize: parse / valid / exact-match rate                                                                        100.0% / 100.0% / 100.0%
     Formalize: harness execution rate                                                                                             100.0%
     Convexify: parse / detection-exact rate                                                                                  100.0% / 100.0%
     Convexify: harness execution rate                                                                                             100.0%
     Strategy choices (SDR / OSM / already-convex)                                                                               52 / 38 / 0
     FCV tiers (feasible / near-feas. / repair / reject / no cand.)                                                          56 / 1 / 2 / 31 / 0
     FCV repairs attempted / successful                                                                                             3/1
     FC usable/n by cell: SDR×tight, SDR×loose, OSM                                                                 18/18, 0/34 (feas. 0), 0/38 (feas. 38)
     Median gap of feasible answers (D/F/FC/FCV)                                                                        0.01 / < 0.01 / 1.48 / 1.40
     Wall-clock (LLM+solver) per usable, s (D/F/FC/FCV)                                                                     610 / 39 / 327 / 310
     Input tokens per usable, k (D/F/FC/FCV)                                                                            31.0 / 14.4 / 127.4 / 120.7
     Usable % at gap ≤ 0.02R/0.05R/0.1R: D                                                                                   34.4 / 41.1 / 42.2
       F                                                                                                                     80.0 / 90.0 / 90.0
       FC                                                                                                                    20.0 / 20.0 / 23.3
       FCV                                                                                                                   21.1 / 21.1 / 24.4
     Matched dispersion, FCV-returned pairs (FC / FCV, n=17)                                                                     0.28 / 0.28
     Calibrated-gate coverage on FC endpoints (n=34)                                                                                88.2%
     Tool-use events across all 270 calls                                                                                             0


Table 6: Stage-level measurements over all 30 × 3 samples. Parse = output matched the
JSON schema; valid = formalization is a well-formed program of the right shape; exact =
coefficient match with ground truth within 10−6 after canonicalization.

                                                            per-problem usable outputs (0--3 samples)
                                                                           loose SDR         SDR-certified oracle

                                                                                                                                                                     3
stage package




                                                                                                                                                                         usable samples
                 D    3   3   2    1    1    3    1    3    1   0    1    0    0   0    2     0   1    1   1    0     1   2    2    1   0     3   1    1   0    2
                                                                                                                                                                     2
                  F   3   3   3    3    3    3    3    3    3   3    3    3    3   3    3     3   3    0   3    3     3   3    3    3   3     0   3    3   3    0

                                                                                                                                                                     1
                 FC   2   2   3    1    0    2    1    1    3   1    2    0    0   0    0     0   0    0   0    0     0   0    0    0   0     0   0    0   0    0


                FCV   2   2   3    1    0    2    1    1    3   1    2    1    0   0    0     0   0    0   0    0     0   0    0    0   0     0   0    0   0    0    0
                              14

                                   20

                                        24

                                             27

                                                  12

                                                       15



                                                                29

                                                                     23

                                                                          18



                                                                                   17

                                                                                        11

                                                                                             10

                                                                                                  19




                                                                                                                     21

                                                                                                                          22

                                                                                                                               26



                                                                                                                                        16



                                                                                                                                                  28



                                                                                                                                                           13

                                                                                                                                                                25
                      1

                          6




                                                            7




                                                                               8




                                                                                                       0

                                                                                                           4

                                                                                                               5




                                                                                                                                    9



                                                                                                                                             3



                                                                                                                                                       2


                                                      problem ID (sorted by SDR looseness and residual)


Figure 7: Per-problem stage-package outcomes. Each cell is the number of usable outputs
among three samples. Problems are ordered with tight SDRs first, then loose SDRs, and by
true-SDR residual within each group; the dashed line marks the group boundary. Markers
identify loose SDRs and problems whose oracle value is certified by the SDR lower bound.


F                Feedback-condition protocol

Frozen items and prompts. We use sample indices 0 and 1 from each of the 30 path-
ablation problems, yielding 60 formalization and convexification commitments. Each
commitment has two independent state-only/state-plus-feedback calls. Both prompts share
the problem, committed program, detected indices, strategy, rationale, and action menu.
The post condition adds execution status, endpoint, residual, objective, the SDR lower
bound, and their gap. Oracle values and offline action labels are reserved for evaluation.

Actions and scoring. A keeps or repairs the current endpoint; B executes the other sur-
rogate with the same verifier; C runs SLSQP on the committed program from its standard
feasible origin; D abstains. The harness executes each action with repair radius 0.25R.
Usable means ground-truth feasibility at 10−6 and objective gap at most 0.05R, as in §6.
Paired intervals resample the 30 problem IDs with replacement (2,000 draws, seed 20260715),
retaining both samples and conditions within a problem.


                                                                                         18
Preprint. Under review.




Calls and parsing. Calls use the same Codex command in App. E, with an output schema
requiring one selected label and four reported allocations in [0, 1]. All 120 medium-effort
calls parsed; every reported allocation sum was 1, the selected label was always an argmax,
and the JSONL logs contain no command/tool item. The archive also contains six configu-
ration checks; every reported result uses the 120 explicit medium-effort calls. Full events,
outputs, action outcomes, and analysis tables are included in the supplement.

Offline policy baselines. Always-A/B/C/D and an offline oracle are evaluated from the
same deterministic action outcomes. The diagnostic rule selects A only when the current
endpoint is 10−6 -feasible and its objective is within 0.05R of the available SDR lower bound;
otherwise it selects C. It chooses A on 11 states and C on 49, attaining 54/60 usable and
60/60 feasible, equal in utility to always-C and the offline oracle. The measured F executor
costs 0.0630 s for 90 runs, giving estimated totals of 0.0420 s for 60 always-C actions and
0.0343 s for the rule’s 49 C actions. The 60 post-feedback controller calls take 633.5 s before
action execution. These measurements price the interface as well as its action accuracy.


G    Cross-trajectory surrogate-state transplantation stress test

This repeated-call probe uses problem IDs {0, 5, 10, 15, 20, 25} from the released bank, giving
two problems at each n ∈ {2, 3, 4}. State S0 contains the natural-language problem. State
SK −1 contains the same problem, the sample-0 exact formal program, the committed surro-
gate endpoint, and its execution record: status, residual, objective, available SDR bound,
and gap. A shared prompt requests one final numeric endpoint under the same JSON
schema and model configuration. The formal program and surrogate state were produced
by sample 0 of another trajectory and then held fixed across the independent receiving calls;
the prompt permits retaining or revising the supplied endpoint. The estimand is therefore
cross-trajectory state transplantation. An endogenous-path test instead generates a fresh
provisional state inside every sampled trajectory before measuring its continuation.
The initial manifest targeted twelve repetitions. A collection-budget amendment, made
after 63 requests and before offline scoring, capped the run at 80 requests and retained
repetitions 0–5 for every problem–state cell. The resulting Cartesian design has 6 × 2 × 6 =
72 completed calls. Six in-flight requests interrupted at the amendment were repeated,
producing 78 actual requests in total. The archive retains both versioned manifests (current
SHA-256 prefix 4432fa5b4522) and every attempt record.
For problem i, the fixed endpoint encoding divides each coordinate of x/R into bins of width
0.05 and includes separate INVALID and ABSTAIN symbols. Let Q  b ik be the resulting empirical
distribution at state Sk . We report plug-in entropy with the Miller–Madow correction,
the number of occupied endpoint bins, and acceptable mass: the fraction of calls whose
endpoint is 10−6 -feasible and within 0.05R of the best-known objective. The primary paired
estimands are
                   ∆Hi = H ( Q
                             b i0 ) − H ( Q
                                          b i,K −1 ),   ∆Mi = Mi,K −1 − Mi0 .
Problem-level paired bootstrap intervals preserve all six calls within each state. The pre-
specified directional criterion is a positive mean ∆H together with mean ∆M ≥ −0.05; raw
collision counts and per-problem estimates accompany the aggregate because six samples
make entropy resolution explicit. This stress test reuses the endpoint representation and
utility-preservation criterion of Hypothesis 1 while intervening on state provenance.
All 72 completed outputs parse under the schema and contain zero tool events. Mean
corrected entropy changes from 1.301 at S0 to 0.512 at SK −1 , giving ∆H = 0.789 [0.172, 1.482].
The per-problem entropy comparison is 3/0/3 wins/losses/ties (one-sided sign test ex-
cluding ties, p = 0.125). Acceptable mass changes from 30.6% to 2.8%, or -27.8 percentage
points [−61.1, 0.0], while feasible mass rises from 33.3% to 86.1%. The directional criterion is
therefore unmet for the transplanted state: it concentrates the endpoint distribution and
raises feasibility while placing much of its mass outside the objective-utility tolerance. The
receiving calls inherit a surrogate basin they did not select, localizing the measured failure to


                                                  19
Preprint. Under review.




hard cross-trajectory conditioning on an unverified proposal. Figure 8 places this endpoint
result beside the fixed-action diagnostic on their respective concentration–utility planes.

                                                                    ID n            H0 HK −1                ∆H                              M0         MK −1    ∆M
                                                                      0      2   1.492      0.000         1.492 .500                                    .000 −.500
                                                                      5      4   1.580      1.580         0.000 .000                                    .000   .000
                                                                     10      3   1.492      1.492         0.000 .000                                    .167   .167
                                                                     15      2   0.000      0.000         0.000 1.000                                   .000 −1.000
                                                                     20      4   2.208      0.000         2.208 .333                                    .000 −.333
                                                                     25      3   1.034      0.000         1.034 .000                                    .000   .000
                                                               Mean              1.301      0.512 0.789                                     .306        .028   −.278

Table 7: Cross-trajectory state-transplant stress test. Entropies use the Miller–Madow
correction; M is acceptable endpoint mass. Each cell contains six receiving calls.
usable allocation-mass change (pp)




                                                                                                           acceptable-mass change (pp)
                                                (a) fixed action interface (60 states)                                                          (b) transplanted endpoint state (6 problems)
                                                                                                                                                   10
                                                                                                                                                                               utility-preservation
                                                                                                                                                   5               25            tolerance: −5 pp
                                      50                                                                                                    0

                                                                                                                                                                                              20
                                      25                                                                                                                                   0
                                                                                                                                         −50
                                       0
                                                selected utility improves    28 concentrate / lose mass
                                                selected utility unchanged        6 expand / gain mass                                             15
                                     −25                                                                                                 −100
                                           −0.25 0.00 0.25 0.50 0.75 1.00 1.25                                                                  0.0    0.5      1.0     1.5     2.0
                                             reported concentration ΔH = Hpre − Hpost                                                             endpoint concentration ΔH = H0 − HK − 1



Figure 8: Concentration paired with task utility. (a) For the fixed action interface, many
reported allocation distributions concentrate while usable allocation mass decreases; marker
shape records the executed utility of the selected action. (b) The transplanted endpoint
state concentrates several problem-level endpoint distributions while acceptable mass falls
beyond the pre-specified five-point tolerance. Shading marks the joint concentration-and-
utility region for each interface.


H                                     Same-call endogenous-state pilot
We use the same six problems and endpoint encoding as App. G. Both conditions receive
only the natural-language problem. D IRECT requests an endpoint under the usual rea-
soning process. S ELF - PROPOSAL asks the model, within the same uninterrupted call, to
autonomously expose up to three useful states and then return an endpoint. Every exposed
intermediate artifact therefore originates inside the receiving call. States directly entailed by
the problem may be marked VERIFIED - HARD; active-set guesses, numerical anchors, transfor-
mations, and other model proposals remain SOFT, REVISED, or ROLLED - BACK. The exposed
path record makes proposal provenance observable. Its estimand is behavior under this
elicited interface; latent unprompted checkpoints require model-internal instrumentation.

Clean amendment. A collection interruption left two drivers writing the same 48-tag pool,
so that pool is released only as an execution audit. After identifying the write collision,
the clean amendment fixed repetitions 0–1 for all 6 × 2 problem–condition cells. It retains
five nonoverlapping original responses and seven recovery-driver responses identified
by exact logged wall times and hashes, then collects the twelve missing cells once in an
exclusive-write directory. This outcome-independent rule yields 24 valid outputs (12 new
requests), zero tool events, and manifest SHA-256 prefix b1d099e46479.
The collision comparison gives 2/2/2 concentration wins/losses/ties and equal mean
entropy; it therefore leaves endpoint concentration unresolved at this sample size. The


                                                                                                          20
Preprint. Under review.




              Metric                              Direct   Same-call self-proposal
              Miller–Madow endpoint entropy       0.629            0.629
              Usable yield (10−6 )                25.0%             8.3%
              Usable yield (10−3 )                33.3%             8.3%
              Mean wall-clock/call (s)            184.0            222.5
              Calls exposing a state              0/12             10/12

Table 8: Clean same-call self-proposal pilot. With two repeats per cell, the entropy estimate
is a collision diagnostic taking only 0 or 0.943 nats per problem–condition cell.


self-proposal condition records 16 soft states, 9 hard restatements, and 1 revision. Usable
yield is 25.0% versus 8.3%; the loose-tolerance comparison is 33.3% versus 8.3%. An indepen-
dent implementation recomputes all 21 returned endpoints with zero residual or objective
difference from the main scorer. Among 8 path records that explicitly report checking
every original constraint at the returned endpoint, 1 passes deterministic evaluation (also
at 10−3 ). The observed interface therefore separates endogenous proposal from validation:
dense-QCQP hypotheses become operational constraints after executor feedback establishes
their validity.




                                             21
