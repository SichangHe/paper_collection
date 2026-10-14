                                         Agentic Stage-One Stellarator Optimization: Autonomous Multi-Objective
                                                            Search for Finite-Beta Equilibria
                                                                               Tingjia Zhang, Zhuoran Meng, Runlai Xu
                                                                                                August 1, 2026

                                                                                                     Abstract
                                                   Stage-one stellarator design searches a high-dimensional family of three-dimensional plasma boundaries and
                                               fixed-boundary MHD equilibria for configurations that jointly meet requirements on confinement, field-line topology,
                                               force balance, stability proxies, and geometry. These specifications do not provide a general constructive map
                                               to a validated finite-beta equilibrium. High-quality targets are commonly developed through iterative numerical
                                               optimization whose outcome depends on the initial configuration, active Fourier resolution, objective priorities,
                                               and local solver budget. Coordinating this process is computationally costly and expert-intensive, limiting both
                                               design throughput and the production of consistently evaluated data. We present a proof of concept for agentic
                                               stage-one optimization. A bounded language-model agent diagnoses the current equilibrium and selects the next
arXiv:2608.01344v2 [cs.AI] 10 Aug 2026




                                               local optimization experiment, while deterministic DESC execution owns prescribed profiles and flux, symmetry,
                                               metric evaluation, solver validity, and acceptance. On a common-budget subset from an expanding finite-beta
                                               campaign, the number of gate-valid configurations increases from five inputs to nineteen outputs; median Boozer
                                               QS RMS decreases from 2.39 × 10−4 to 1.07 × 10−4 , and median maximum principal curvature decreases from
                                               62.56 to 33.00 m−1 . A complementary long route achieves a 9.10× QS reduction while repairing magnetic-well and
                                               curvature defects. The system also records every attempted local action as transition evidence, yielding 734 structured
                                               parent–action–outcome records in the reported experiments. These results show that agentic outer-loop control can
                                               sustain finite-beta, multi-objective search and turn repeated optimization into a scalable source of improved equilibria
                                               and reusable decision data.

                                         1    Introduction                                                    ary coefficients for a declared parent, Fourier subspace,
                                                                                                              objective specification, and numerical budget. After ob-
                                         Stage-one stellarator design is a constrained inverse prob-          serving the physical and numerical response, an outer
                                         lem over a chosen family of three-dimensional plasma                 policy must decide whether to continue, repair a degraded
                                         boundaries. In the conventional two-stage workflow, each             metric, expand the mode space, return to an earlier parent,
                                         trial boundary defines a fixed-boundary ideal-MHD solve              or explore another basin. The appropriate action changes
                                         under a specified field period, symmetry, profiles, and              along the route, so a fixed scalarization or continuation
                                         flux; an outer optimizer updates the boundary, and a later           schedule does not resolve this decision problem. Managing
                                         stage designs coils that reproduce the target field [1]. A           the route therefore remains an expert-intensive bottleneck
                                         useful target must jointly address confinement or symme-             on search throughput.
                                         try proxies, rotational-transform topology, force balance,                The same bottleneck shapes the available design data.
                                         stability-related metrics, aspect ratio, and boundary reg-           Existing resources broaden geometric coverage under spe-
                                         ularity. The resulting tradeoffs make stellarator design             cific contracts: QUASR assembles vacuum-field coil config-
                                         intrinsically multi-objective [2].                                   urations spanning QA and QH designs, whereas ConStel-
                                             The target metrics do not furnish a constructive in-             laration targets QI equilibria and boundaries [4, 7]. Using
                                         verse map to a validated finite-beta equilibrium. Near-              such configurations for a finite-beta, multi-objective task
                                         axis constructions and learned generators provide use-               requires equilibrium reconstruction, reevaluation, and re-
                                         ful candidate priors in restricted regimes [3, 4]; practical         finement. These computations reveal which interventions
                                         finite-aspect-ratio targets are commonly refined through             improve, damage, or invalidate a candidate, information
                                         repeated equilibrium solves and numerical optimization.              that endpoint collections do not retain.
                                         The search is expensive and nonconvex, and its outcome                    To address this coupled optimization-and-data prob-
                                         depends strongly on initialization, objective scalarization,         lem, we introduce a bounded agentic controller around de-
                                         optimizer, and spectral resolution [5]. Fourier continua-            terministic DESC execution. At each epoch, the controller
                                         tion improves robustness by activating boundary modes                selects a parent, Fourier-mode schedule, objective specifi-
                                         progressively, while introducing further choices about how           cation, and local budget from the current route state. The
                                         the search space should be expanded [6].                             harness enforces the finite-beta physics contract, executes
                                             These dependencies leave a sequential control problem            optimization, recomputes metrics, and applies acceptance
                                         outside the local optimizer. Each solve updates bound-               gates. Every attempted local solve is stored as transition


                                                                                                          1
evidence: its parent, declared action, optimizer response,              For a stellarator-symmetric boundary, the design vari-
physical outcome, validity, and continuation decision. The           ables are Fourier coefficients in
resulting record supports route-level credit assignment                                   X
while accumulating reusable state–action–outcome data.                         R(θ, ζ) =      Rmn cos(mθ − nNFP ζ),
Figure 1 summarizes the route-scale optimization and                                       m,n
                                                                                           X                                    (2)
asynchronous multi-start system.                                               Z(θ, ζ) =         Zmn sin(mθ − nNFP ζ).
    This paper makes three contributions:                                                  m,n

    • A sequential hyperparameter-control formu-                     Low-order modes control global elongation, triangularity,
      lation. We cast stage-one route control as a typed             axis displacement, and other basin-scale geometry. Higher
      hyperparameter-optimization problem over parent                modes provide shorter-length-scale corrections, while their
      selection, Fourier-mode access, objective specifica-           derivatives can rapidly increase curvature and coordinate
      tion, and local budget under an invariant finite-beta          distortion. Mode access therefore changes both the reach-
      physics contract.                                              able geometry and the conditioning of a local solve.
                                                                         Deterministic postprocessing maps an equilibrium x to
    • A physics-grounded agentic optimization sys-
      tem. We combine a bounded language-model con-                        m(x) = (ϵQS , W (ρ), ι(ρ), rF , A, κmax , maux ) ,   (3)
      troller, deterministic DESC workers, metric-wise ac-
      ceptance, persistent lineage, and cross-route memory           where ϵQS measures symmetry-breaking Boozer harmon-
      to execute multi-start optimization routes automati-           ics, W (ρ) is the dense magnetic-well profile, ι(ρ) is rota-
      cally.                                                         tional transform, rF is the normalized force residual, A is
                                                                     aspect ratio, and κmax is maximum principal curvature.
    • Optimization-driven data infrastructure. We
                                                                     Quasisymmetry suppresses symmetry-breaking guiding-
      demonstrate repeated finite-beta, multi-objective
                                                                     center drifts; magnetic well provides a local ideal-MHD
      improvement from heterogeneous source geometries
                                                                     stability proxy; transform controls field-line winding and
      and retain successful, rejected, and failed actions in a
                                                                     resonance topology; force residual checks consistency with
      common transition schema. Each route contributes
                                                                     the prescribed MHD state; and aspect ratio and curvature
      an improved design candidate and reusable evidence
                                                                     guard geometric realizability. These quantities are cou-
      about the optimization process.
                                                                     pled through Eq. (1), so improvement in one metric can
    Together, these results establish a proof of concept             consume margin in another. Boozer QS and magnetic-well
at two connected levels: an agent can execute physically             diagnostics follow established definitions [3, 10, 11].
meaningful stage-one routes, and the resulting automation                The final design criterion is a conjunction of metric-
can scale those routes into a continuously expanding sci-            wise gates gj (m(x)) ≤ 0. This representation preserves
entific data resource. Comparative policy efficiency and             the physical meaning of each requirement. A scalar score
learned transition models remain separate questions.                 is useful for ranking otherwise comparable states, while
                                                                     acceptance remains determined by the complete gate vec-
                                                                     tor.
2     Background and problem formu-
      lation                                                         2.2    Sequential hyperparameter control
                                                                     DESC optimizes the physical boundary coefficients. We
2.1    Fixed-boundary stage-one physics                              use hyperparameter optimization (HPO) for the agent’s
A stage-one calculation seeks a plasma boundary for which            outer selection of mode access, objective specification, and
the magnetic field is simultaneously close to a target sym-          numerical budget, represented by
metry, an accurate MHD equilibrium, and compatible with
geometric and stability requirements. For a prescribed                                     h = (K, w, η, b),                    (4)
pressure profile p(ρ), current profile, and toroidal flux,
                                                                     where K specifies the Fourier-mode schedule, w contains
DESC represents the ideal-MHD equilibrium through
                                                                     objective weights, η contains typed objective parameters,
      ∇×B = µ0 J,         J×B = ∇p,          ∇·B = 0,      (1)       and b is the numerical budget. Starting from parent p, the
                                                                     solve has the schematic form
and solves these equations in a global spectral basis [8, 9].                                    X
The field-period number, stellarator symmetry, helicity                          ξ ⋆ ≈ arg min       wr ℓr (ξ; ηr , C),      (5)
                                                                                           ξ∈ΘK (p)
                                                                                                      r
convention, transform branch, profiles, and flux define a
route-specific physics contract C. They remain invariant             subject to equilibrium solution and numerical-validity
while the boundary is optimized.                                     checks. Here ΘK (p) is the mode-restricted neighborhood
                                                                     of the parent. The outer action is therefore

                                                                                     a = (p, h) = (p, K, w, η, b).              (6)


                                                                 2
Parent and mode schedule are categorical decisions, cutoffs                         3. Evaluate. Recompute all metrics on a common grid
and budgets are discrete, and weights and overrides are                                and retain endpoint, optimizer, validity, and failure
bounded numerical variables. The agent configures this                                 observations.
local experiment; the numerical optimizer determines the
Fourier update.                                                                     4. Update. Interpret the candidate set, select an ex-
    This HPO problem is state dependent. Applying the                                  ecutable next parent, and update compact route
same h to two parents can reach different basins, trig-                                memory and persistent transition storage.
ger different solver behavior, or reverse a metric tradeoff.                     The cycle continues until the route budget is exhausted.
The response surface is expensive, partially observed, and                       An outer asynchronous scheduler runs multiple routes
discontinuous at failed solves and branch changes. Its ob-                       while candidate workers parallelize the physics stage within
jective also changes with route state: a violated terminal                       each route.
gate calls for repair, whereas a gate-valid state can priori-
tize lower QS while preserving well, topology, geometry,                         3.2    Grounded route state
and force margins. Temporary violations can expose a use-
ful basin when the damaged quantity remains repairable.                          At epoch t, the planner receives a rendered state
Consequently, the outer policy must reason over both the
                                                                                          st = {C, pt , m(pt ), g(pt ), Rt , Mt , Ht , Bt },   (8)
endpoint and the route by which it was produced.
                                                                                 where g(pt ) contains signed gate margins, Rt is a com-
2.3      Transition evidence                                                     pact route digest, Mt is editable working memory, Ht is
                                                                                 retrieved cross-route transition evidence, and Bt is the
We represent one local experiment as                                             explicit remaining budget. The route digest is regenerated
                                                                                 from stored artifacts and contains the active lineage, recent
    ei = (idp , m(p), ai , idc , m(x′i ), ∆mi , si,opt , vi , di ) ,   (7)
                                                                                 epochs, and a curated parent menu. The menu includes
where x′i is the child when execution succeeds, si,opt records                   the active parent, recent successful children, earlier lineage
optimizer response, vi records solver and evaluation va-                         anchors, and metric-specific anchors for QS, well, trans-
lidity, and di indicates whether the child was selected for                      form, force, and aggregate quality. Every parent the agent
continuation. Failed actions retain their parent, declared                       can name therefore resolves to an existing equilibrium
hyperparameters, available optimizer trace, and failure                          artifact.
class. The evaluated equilibria form nodes in a route                                Working memory retains the current physical hypothe-
graph; transition records form directed edges.                                   sis, the dominant defect, observed regressions, stagnation
    Transition evidence exposes local controllability: which                     status, and the selected continuation parent. Cross-route
mode space and objective emphasis produced a physical                            memory is a compact table of selected successful parent–
response from a particular parent. It also separates an in-                      action–child transitions rather than a transcript of prior
formative tradeoff from a uniformly poor endpoint. These                         reasoning. The prompt explicitly labels these transitions
records are observations generated by a changing behav-                          as behavior-policy observations. This lets the agent use
ior policy, so they are treated as confounded empirical                          repeated mechanisms as priors while requiring the current
priors rather than causal demonstrations. This distinc-                          parent metrics and gate margins to determine the action.
tion informs both the agent context and the use of the                               Budget is part of the state rather than an implicit con-
accumulated data for later learning.                                             versation count. Opening epochs permit acquisition and
                                                                                 one diagnostic probe; development epochs compare or re-
                                                                                 pair mechanisms; exploitation concentrates on productive
3      Agentic optimization method                                               routes; closure requires every candidate to be capable of
                                                                                 producing the best feasible output. Stagnation is tracked
3.1      System overview                                                         by parent, basin, and mechanism so repeated local polish
                                                                                 cannot consume the remaining route by default.
The system separates HPO decisions from physical author-
ity. The agent chooses an existing parent and bounded
values of Eq. (4). The execution harness validates the                           3.3    Bounded planning and physics execu-
action, runs DESC, recomputes diagnostics, applies gates,                               tion
and writes provenance. Thus every policy decision be-                            The planner follows a physics-first decision order. It identi-
comes a declared and replayable numerical experiment                             fies one primary failed condition using its exact value and
under the fixed contract C.                                                      signed margin, records healthy metrics as guards, assesses
    As illustrated in Fig. 1, an epoch has four stages:                          route phase and stagnation, and chooses an acquisition,
    1. Plan. Construct a grounded route state and propose                        repair, escape, polish, validation, or backtracking mecha-
       a small set of differentiated local hypotheses.                           nism. It then emits schema-constrained JSON containing
                                                                                 the parent identifier and, for each candidate, its mode
    2. Execute. Validate each action and evaluate inde-                          schedule, complete weight vector, sparse typed overrides,
       pendent DESC optimizations in parallel.                                   iteration budget, force-solve budget, and rationale.

                                                                             3
                                             Optimization Stage                                                       Execution Context
               Input                               DESC Solver                            Postprocess
                                                  Objective Functions                    Full Metrics & Quality
             Fixed Profile                   QS                   Topology                       Score
                                                          Well
                                                                                               Transport
             Objective                        Stability          Transport
             Weights                                                                          Neoclassical
                                                   Run Optimization
                                                                                                                          Route Tree
                                                   Policy Stage                                                            Phys Metrics
                                                                                        Prior Evidence
                                     Planner                                                                             Optimizer Signal
             Detailed Plan                   Diagnose & Hypothesis                          Pre-round
                                                                                            Feedback                       Parent Delta
               Weight                   “Do topology-margin repair
                                                                                             Global                      Batch Metadata
                                        with iota_shear pressure and
              Opt. Mode                                                                    Route Tree
                                         relaxed geometry pressure,
              Next Input                guarding QS near 1.1e-4…”                            History
               Parent                                                                        Lesson                          Full Record




Figure 1: Agentic stage-one data-construction loop. A bounded agent selects an executable parent, Fourier-mode
schedule, objective specification, and numerical budget. DESC performs the local optimization under a fixed physics
contract, after which deterministic postprocessing records physical metrics, optimizer response, validity, and lineage.
Every attempted action updates the configuration collection and the persistent transition corpus.



   Candidates within an epoch test distinct hypotheses.                               Selection can continue a productive child, retain a
At least one must make a material intervention when the                           material but gate-violating tradeoff for repair, return to
route is stagnant; early epochs admit at most one small                           a lineage anchor, or terminate an exhausted mechanism.
diagnostic probe, and closure epochs admit none. Exact                            The resulting memory stores the route-level lesson and
weight bounds, allowed override keys, solver caps, and                            high-level next hypothesis. Concrete schedules, weights,
parent identifiers are checked before execution. Invalid                          and budgets are carried forward only when the evidence
plans are rejected before allocating a physics worker.                            makes them decisive; the next planning call otherwise
   For valid candidate i, the deterministic layer evaluates                       reconstructs an action from the new physical state. This
                                                                                  separation prevents a local lesson such as a strict mode
                (x′i , si,opt , vi ) = D(pt , hi ; C),                  (9)       prescription from becoming an unsupported global policy.
where D denotes equilibrium optimization followed by
common-grid postprocessing. Independent candidates run                            3.5    Persistent evidence and campaign scal-
concurrently. Successful children receive the complete met-                              ing
ric vector and gate margins. The optimizer record includes
                                                                                  The implementation preserves execution at three resolu-
initial and final local cost, normalized cost change, itera-
                                                                                  tions. Per-route directories contain equilibria, plans, logs,
tions, accepted steps, termination reason, and warnings;
                                                                                  evaluations, failures, and complete lineage. A relational
exceptions and partial traces are retained for failed solves.
                                                                                  table stores every attempted transition using Eq. (7). Com-
                                                                                  pact selected transitions are retrieved for agent context.
3.4    Lesson and route update                                                    The full archive therefore remains available for analysis and
The update call has a narrower role than the planner. It                          learned policies without expanding each online prompt.
receives the declared plan, current-epoch outcomes, pre-                              A deterministic expert score
vious working memory, route budget, and the curated                                                          X
                                                                                                    Q(x) =      αj Pj (m(x))                (10)
executable parent menu. Long historical context is omit-
                                                                                                                  j
ted at this stage so that the observed epoch response
remains the direct basis for credit assignment. The agent                         provides a lower-is-better ranking anchor across QS, well,
summarizes whether the primary-defect hypothesis was                              transform, geometry, force balance, and solver health.
supported, identifies new debt, and selects the next parent                       Metric-wise gates retain authority over acceptance. This
from the menu.

                                                                              4
division supports stable parent and endpoint ranking while          temporary well or curvature violation; terminal outputs
preserving every physical constraint explicitly.                    must satisfy every required gate.
    At campaign scale, the scheduler advances independent               Each campaign input is paired with one route output.
routes asynchronously. It samples a source lineage before           Routes that reach acceptance contribute their best ac-
selecting an eligible raw or improved member, which limits          cepted equilibrium under the deterministic quality score
repeated selection of a prolific family. Accepted outputs           in Eq. (10). The remaining routes contribute the endpoint
and the best distance-to-goal result from incomplete routes         with minimum configured distance to the full gate. This
can re-enter later campaigns. Every completed route conse-          preserves a paired evaluation over the complete selected
quently contributes an optimized configuration, the closest         subset. The configuration gallery shows the eight accepted
observed endpoint, and its complete transition evidence.            pairs with the largest quality-score reductions.
This mechanism turns repeated agentic optimization into                 For the detailed route, the reported output is the lowest-
a growing configuration and state–action data resource              QS stored equilibrium satisfying the well, force, curvature,
under a shared evaluation contract.                                 iota, and geometry guards. Its deliberately ambitious
                                                                    target is QS RMS below 10−6 with well-positive fraction at
                                                                    least 0.98 and 3 ≤ A ≤ 3.6. The common-budget campaign
4     Experimental setup                                            subset contains 543 attempted transitions, and the long
                                                                    route contains 191, yielding 734 structured observations
4.1    Source configurations and execution                          across the two experiments.
The primary evaluation uses routes from an ongoing
configuration-enhancement campaign. Source boundaries
are derived from QUASR coil-vacuum records [7] and pre-
                                                                    5     Experiments
pared as finite-beta DESC equilibria with pressure, Redl            The experiments test the two levels of the central claim.
current, toroidal flux, and field normalization supplied            The multi-start campaign asks whether the agentic work-
before agent execution. This preparation deliberately               flow can repeatedly transform heterogeneous geometric pri-
exposes each geometric prior to a common class of finite-           ors into better finite-beta, multi-objective configurations
beta, multi-objective tests. Profiles and flux remain fixed         under one evaluation contract. The retained transition
within each route.                                                  corpus then measures how much reusable optimization
    We select 23 completed routes with a common eight-              evidence this processing creates. A long trajectory re-
epoch budget for paired evaluation. Every route starts              solves the route-selection and repair behavior hidden by
from a distinct source record, and optimized outputs are            the aggregate statistics.
not recycled within this subset. A separate 50-epoch
route provides the temporal resolution needed to study
acquisition, repair, and saturation. An epoch contains              5.1    Multi-start finite-beta enhancement
one parent decision, four candidate local optimizations,            Only five inputs in the selected subset satisfy every ter-
deterministic evaluation, and a next-parent update. The             minal gate. After eight epochs per source, 19 of the 23
policy uses GPT-5.6-sol with xhigh reasoning effort; calls          selected outputs are gate-valid. Table 1 reports paired me-
receive the explicit state described in Sec. 3. Independent         dians over all routes, including the closest-to-gate endpoint
routes and candidate workers execute concurrently.                  from the four incomplete cases.
    All reported configurations are stellarator-symmetric,
positive-branch, NFP = 2 finite-beta QA equilibria with             Table 1: Paired medians for a common-budget subset of
helicity (1, 0). Boundary resolution is M = N = 6 with              23 distinct source configurations.
radial resolution L = 10; evaluation grids use Lgrid =
20 and Mgrid = Ngrid = 12. The local objective li-                           Metric                         Input       Output
brary contains Boozer QS, dense magnetic-well, rotational-                   Quality score ↓                 18.95         9.48
transform, aspect-ratio, curvature, and coordinate-quality                   QS RMS ↓                   2.39×10−4    1.07×10−4
                                                                             Well floor ↑                        0            0
terms. Magnetic-axis field strength is retained as a low-                    Well-positive fraction ↑        0.980        0.980
priority scale diagnostic.                                                   Max. curvature ↓                62.56        33.00
                                                                             Force RMS ↓                4.91×10−5    4.00×10−5

4.2    Acceptance and paired evaluation                                  The deterministic multi-objective score improves in 20
Terminal acceptance requires Boozer QS RMS below 5 ×                routes. QS RMS decreases in 22 routes, with its median
10−4 , dense-well floor at least zero, well-positive fraction       falling from 2.39×10−4 to 1.07×10−4 . Maximum curvature
at least 0.9, force RMS below 10−4 , maximum principal              decreases in 20 routes and its median moves from 62.56 to
curvature below 33.2 m−1 , 0.25 ≤ |ιedge | ≤ 1.2, and 3 ≤           33.00 m−1 , close to the terminal gate. Force RMS improves
A ≤ 5. Volume beta is reported as an audit quantity                 in 16 routes. Ten routes improve both the dense-well floor
because profiles and flux are fixed while geometry and              and positive fraction; their medians remain unchanged
field strength evolve. Intermediate parents may carry a             because many source profiles already have a zero floor and
                                                                    0.98 positive fraction. Every selected output preserves the


                                                                5
prescribed iota and aspect-ratio intervals. The aggregate            curvature while retaining the newly acquired QS level.
shift therefore reflects joint finite-beta feasibility rather        These events illustrate why continuation value cannot be
than QS reduction alone.                                             inferred from instantaneous QS rank.
    Figure 2 shows that the improvements occur across                    The selected Epoch 44 equilibrium reaches QS RMS
several LCFS families. The paired profiles also expose the           4.157 × 10−5 , a 9.10× reduction from the input. Its dense-
central multi-objective behavior: QS reductions coexist              well floor is zero, well-positive fraction is 0.980, force RMS
with preservation or repair of the dense magnetic well,              is 3.12 × 10−5 , maximum curvature is 33.111 m−1 , aspect
while substantial curvature violations are removed through           ratio is 3.444, and |ιedge | = 0.340. Volume beta changes
changes that remain moderate at the scale of the LCFS.               from 2.039% to 1.832% under fixed profiles and flux. The
                                                                     remaining six epochs vary parent replay, mode support,
5.2    Transition-data production                                    and step scale without finding a lower-QS gate-valid state,
                                                                     providing an empirical local-saturation test. The final QS
The same short routes produce 543 attempted transitions.             remains above the ambitious 10−6 target.
Each row couples a parent metric state and executable                    Figures 6 and 5 connect the physical path to the
action to a child metric state or failure, parent-relative           executed actions. The policy descriptor combines log
changes, optimizer feedback, validity, and continuation de-          objective-group weights, mode-schedule semantics, mode
cision. The records include children rejected by terminal            breadth and cutoff, solver budgets, and explicit well guards.
gates, alternatives that lost the within-epoch compari-              After standardization, the retrospective physical phases
son, and solves that terminated before a valid equilibrium.                      2
                                                                     explain Rphase     = 0.31 of descriptor variance; a label-
These outcomes locate tradeoff surfaces and numerical                permutation test gives p = 2.5 × 10−4 . This descrip-
failure boundaries that are absent from the selected end-            tive result confirms that the executed action distribution
points.                                                              changes across repair, descent, acquisition, and saturation
    The compact successful subset is retrieved by later              segments. The route contributes 191 transition records
agent calls as cross-route experience; the complete corpus           that preserve these changes at candidate resolution.
remains available for offline analysis. Its fixed schema also
admits learned state–action predictors, proposal priors,
and policy evaluation as physical and action-space cover-            6     Discussion
age increases. The present experiments use retrieval rather
than a trained dynamics model. Crucially, each additional            6.1    From agentic optimization to data in-
agent route enlarges both products under the same prove-                    frastructure
nance contract: an evaluated configuration collection and
an aligned transition corpus. Agentic execution therefore            The significance of the agentic layer extends beyond replac-
converts optimization compute into a growing record of               ing manual route decisions. It makes repeated, stateful
designs, decisions, responses, and failures.                         optimization across heterogeneous source configurations
                                                                     an executable scientific process. Source collections can
                                                                     provide broad geometric coverage even when their orig-
5.3    Mechanism study along a long route                            inal field model and objective set differ from the target
The aggregate experiment establishes repeated configu-               task. The workflow supplies a consistent finite-beta equi-
ration enhancement. A 50-epoch route reveals how one                 librium, metric, and acceptance layer, then lets an agent
output is obtained when the source has competing de-                 improve each source under that layer. In the selected eval-
fects. Its input has βvol = 2.039%, QS RMS 3.782 × 10−4 ,            uation subset, this process increases gate-valid coverage
dense-well minimum −2.267 × 10−2 , maximum principal                 and shifts QS, curvature, force balance, and composite
curvature 50.997 m−1 , and force RMS 5.68 × 10−5 . The               quality together.
initial force solve is valid, while well and curvature require           This capability suggests a practical route toward
substantial repair.                                                  foundational data infrastructure for stellarator design.
    Figures 3 and 4 show three stages. Epochs 1–3 first              Continued execution can extend the configuration collec-
construct a valid working parent: QS falls to 1.78 × 10−4 ,          tion across source families, field periods, helicities, profile
the well floor rises to near zero, curvature falls below the         regimes, and acceptance contracts. Because the physics
gate, and the positive well fraction reaches 0.98. Guarded           and provenance schema remains stable, the resulting
QS descent then reaches 7.02 × 10−5 by Epoch 11.                     configurations become comparable even as the campaign
    The subsequent improvement is nonmonotone. Epoch                 and agent policy evolve.
17 accepts a temporary QS increase while reducing curva-                 Transition evidence further compounds the scientific
ture to 30.49 m−1 and increasing the well mean. A shallow            value of the same solver budget. Endpoint databases
well defect introduced at Epoch 25 is repaired at Epoch              support design retrieval and generative modeling; the tran-
26 with little QS cost. Epoch 35 makes a second displace-            sition corpus samples local responses to mode access, ob-
ment toward lower curvature and stronger well behavior.              jective emphasis, and numerical scale. These records can
From that parent, Epoch 36 acquires QS 4.284 × 10−5 with             support action-conditioned surrogates, learned proposal
curvature slightly above the gate, and Epoch 37 repairs              priors, failure prediction, and offline policy comparison


                                                                 6
                                                                                 Input                Selected output
          (a)            LCFS                 10 3
                                                       QS profile                Well profile          (b)   LCFS               QS profile         Well profile
           0.50                                                          0.050
           0.25                                                          0.025




                                     QS RMS
  Z [m]




                                                                  well
           0.00                                                          0.000
           0.25                               10 4
                                                                         0.025
           0.50                                                          0.050


          (c)
           0.50
                                              10 3                                                     (d)
                                                                         0.050
                                    QS RMS

           0.25                                                          0.025
 Z [m]




                                                                 well
           0.00                                                          0.000
           0.25                               10 4
                                                                         0.025
           0.50                                                          0.050


          (e)                                 10 3                                                     (f)
            0.4                                                          0.050
                                    QS RMS




            0.2                                                          0.025
  Z [m]




                                                                 well



            0.0                                                          0.000
            0.2                               10 4
                                                                         0.025
            0.4                                                          0.050


          (g)0.4                              10 3                                                     (h)
                                                                        0.050
            0.2
                                    QS RMS




                                                                        0.025
  Z [m]




                                                                 well




            0.0                                                         0.000
                                              10 4
            0.2                                                         0.025
            0.4                                                         0.050
                   0.50 0.75 1.00 1.25           0.0       0.5      1.0      0.0      0.5   1.0              0.5     1.0      0.0    0.5    1.0   0.0   0.5    1.0
                         R [m]                             ρ                          ρ                            R [m]             ρ                   ρ

Figure 2: Input–output comparisons for the eight accepted configurations with the largest quality-score reductions.
Each sample contains equally sized LCFS, radial Boozer-QS-RMS, and dense magnetic-well panels. Dashed curves
denote inputs and solid curves denote selected outputs. In the LCFS panels, blue, green, and orange denote ϕ = 0,
π/(2NFP ), and π/NFP , respectively.



once coverage is sufficient. Lineage and rejected alterna-                                            jointly, so the present route does not identify a causal tran-
tives are especially important because they retain the local                                          sition law or establish language-model sample efficiency.
tradeoffs that selected designs alone cannot reconstruct.                                             Its role is to show that an agentic controller can sustain a
Agentic optimization thereby offers a path from isolated                                              physically valid, multi-stage route and that the retained
expert runs to cumulative, machine-usable optimization                                                representation resolves the relevant state–action changes.
knowledge.
                                                                                                      6.3      Scope and next steps
6.2          Interpretation of the long route
                                                                                                      The reported evaluation covers finite-beta, NFP = 2 QA
The detailed trajectory supplies the route-level proof of                                             equilibria under one policy and one principal source fam-
concept for agentic control. The selected ancestry is non-                                            ily. Matched-budget static, greedy, random, and memory-
greedy in QS, temporarily spends well or curvature margin,                                            ablated controllers are required to quantify policy efficiency.
repairs the resulting debt, and changes executable actions                                            Broader campaigns should balance geometry clusters be-
as the frontier evolves. Candidate-level records make                                                 cause distinct source records can occupy nearby boundary
these events observable. They also distinguish frontier                                               families. Four short routes remain outside the terminal
acquisition from late local saturation, where additional                                              gate, and the long route does not reach its 10−6 QS target.
mode schedules and parent replays produce no better valid                                             Magnetic-axis field strength is currently a soft scale ob-
state.                                                                                                jective, so reactor-normalized comparisons require stricter
    The action analysis is observational. Parent choice,                                              scaling control. Coil realizability and engineering loads
objective weights, mode support, and budget often change                                              [12, 13], together with energetic-particle confinement, tur-


                                                                                                  7
                                                                                                                                                                  QS-well and curvature search route
                                                                            Well floor                                                                                                  Profile mean                                                                                   Maximum curvature




                                                                                                                                                                                                                                        Maximum principal curvature [m−1]
                                                                                                                              Dense magnetic-well profile mean
                                                                                                                                                                 0.020
           Dense magnetic-well minimum


                                            10−3                              successful children                                                                                                                                                                                                                                           1.0
                                                                                                                                                                                                                                                                            50




                                                                                                                                                                                                                                                                                                                                                   Dense-well positive fraction
                                                                              route stepstone
                                                                              start                                                                              0.015
                                            10−4                                                                                                                                                                                                                                                                                            0.8
                                                                              selected output                                                                                                                                                                               45
                                                     0                                                                                                           0.010                                                                                                                                                                      0.6

                                                 −4                                                                                                                                                                                                                         40
                                          −10
                                                                                                                                                                 0.005                                                                                                                                                                      0.4

                                          −10    −3                                                                                                                                                                                                                         35
                                                                                                                                                                                                                                                                                                                                            0.2
                                                                                                                                                                 0.000
                                                 −2
                                          −10                                                                                                                                                                                                                               30
                                                                                                                                                                                                                                                                                                                                            0.0

                                                         −4            −3           −2                      −1                                                               −4         −3       −2     −1                                                                       −4         −3          −2           −1
                                                         Negative QS RMS, −RMS × 104                                                                                     Negative QS RMS, −RMS × 104                                                                             Negative QS RMS, −RMS × 104


Figure 3: Executed search path in QS–well–curvature space. Gray points are successful children with QS RMS below
5 × 10−4 ; red arrows show the selected parent–child ancestry, and the star marks the selected output. The left and
middle panels show dense magnetic-well floor and profile mean. The right panel shows maximum principal curvature,
with the dotted line marking the 33.2 m−1 gate. Gray intensity encodes dense-well positive fraction.


                                                                                                                                                                                                                                       repair                               descent              basin search             frontier      validate
                                                                       Á=0            Á = ¼=(2NFP )                           Á = ¼=NFP
                                                                                                                                                                                                                                                                                                                                                                    high
                                                          Input LCFS                                                          Selected LCFS                                                            strict schedule
                                                0.5                                                                     0.5
                                                                                                                                                                                                        mode breadth
                                  Z [m]




                                                                                                            Z [m]




                                                0.0                                                                     0.0
                                                                                                                                                                                                                                kmax

                                            −0.5                                                                    −0.5
                                                                                                                                                                                                        solve budget
                                                           0.5        1.0     1.5                                                                    0.5               1.0     1.5                                                                                                                                                                                  low
                                                                                                                                                                                                                                                                                 10          20                 30          40                50
                                                                 R [m]                                                                                           R [m]

                                                 Dense magnetic well                                                        Boozer QS profile
                                         0.02                                                                                                                                                                                                                                          QS        well           iota        geometry
                                                                                            Boozer QS RMS
 magnetic well




                                                                                                                                                                                                                                0.8
                                                                                                                                                                                                             log-weight share




                                         0.00                                                                                                                    Input
                                                                                                                                                                 Selected output                                                0.6
                                                                                                            10−4
                                                           Input
                                                           Selected output
                        −0.02
                                                                                                                                                                                                                                0.4
                                            0.00         0.25    0.50       0.75    1.00                            0.00         0.25                             0.50       0.75    1.00
                                                                   ½                                                                                                ½
                                                                                                                                                                                                                                0.2                                                                                                    2
                                                                                                                                                                                                                                                                                                                                      Rphase = 0.31
                                                                 ­ ®                                                                  ­ ®
                                                Input Boozer jBj= jBj                                               Output Boozer jBj= jBj                                                                                                                                                                                            p = 0.00025
                                           6                                           1.2250                       6                                                                   1.2250                                  0.0
                                                                                                                                                                                                                                                                                  10             20              30              40                   50
                                           4                                                                        4                                                                                                                                                                                   Epoch
                                  µB




                                                                                                            µB




                                                                                       1.0086                                                                                           1.0086
                                           2                                                                        2

                                           0                                           0.7922
                                                                                                                    0                                                                   0.7922        Figure 5: Executable action variation over 50 epochs. The
                                                 0                     2                                                0                                               2
                                                                                                                                                                                                      upper panel summarizes mode schedule, mode breadth,
                                                                 ³B                                                                                               ³B
                                                                                                                                                                                                      maximum cutoff, and solve budget. The lower panel shows
                                                                                                                                                                                                      log-weight emphasis for QS, well, iota, and geometry ob-
Figure 4: Input–output physics comparison for the long                                                                                                                                                jective groups. Phase labels are retrospective partitions
route. The top row compares LCFS cuts at three toroidal                                                                                                                                               defined by physical route events.
angles, the middle row compares dense magnetic-well and
radial Boozer-QS-RMS profiles, and the bottom row shows
normalized Boozer-coordinate field strength with common                                                                                                                                               erage, while the persistent schema allows new policy ver-
contour levels.                                                                                                                                                                                       sions and learned priors to train on the same accumulated
                                                                                                                                                                                                      transitions. At sufficient scale, this creates a progression
                                                                                                                                                                                                      from retrieved examples to learned state–action models
bulence, and transport, remain downstream tests for the                                                                                                                                               and eventually data-informed proposal policies. Controlled
fixed-boundary outputs.                                                                                                                                                                               comparisons can then measure how each capability affects
    These limitations define a direct expansion path. The                                                                                                                                             success rate, route length, and final physical quality.
existing scheduler can increase physical and geometric cov-


                                                                                                                                                                                                 8
                            Epoch frontier and continued route                            [2] David Bindel, Matt Landreman, and Misha Padidar. Understanding
                                                                                              trade-offs in stellarator design with multi-objective optimization.
                                                        best successful child                 Journal of Plasma Physics, 89(5):905890503, 2023. doi: 10.1017/
                                                        cumulative QS frontier                S0022377823000788.
                                                        best gate-valid child             [3] Matt Landreman and Rogerio Jorge. Magnetic well and Mercier sta-
                                                        continued ancestry                    bility of stellarators near the magnetic axis, 2020. arXiv:2006.14881.
 Boozer QS RMS




                                                                                          [4] Santiago A. Cadena, Andrea Merlo, Emanuel Laude, Alexander
                                                                                              Bauer, Atul Agrawal, Maria Pascu, Marija Savtchouk, Enrico
                                                                                              Guiraud, Lukas Bonauer, Stuart Hudson, and Markus Kaiser. Con-
                                                                                              Stellaration: A dataset of QI-like stellarator plasma boundaries and
                 10−4                                                                         optimization benchmarks, 2025. arXiv:2506.19583.
                                                                                          [5] Dario Panici, Byoungchan Jang, Rory Conlin, Daniel Dudt,
                                                                                              Yigit Gunsur Elmacioglu, and Egemen Kolemen.                Deflation
                                                                                              Techniques for Stellarator Equilibrium and Optimization, 2026.
                                                                                              arXiv:2602.09957.
                                                                                          [6] Byoungchan Jang, Matt Landreman, and Rory Conlin. Exponential
                                                                                              spectral scaling: robust and efficient stellarator boundary optimisa-
                        0   10        20           30          40               50            tion via mode-dependent scaling. Journal of Plasma Physics, 92
                                           Epoch                                              (1):E15, 2026. doi: 10.1017/S0022377825101074.
                                                                                          [7] Andrew Giuliani, Eduardo Rodrı́guez, and Marina Spivak. A com-
                                                                                              prehensive exploration of quasisymmetric stellarators and their
Figure 6: QS frontier and selected continuation route.                                        coil sets. Journal of Plasma Physics, 91(5):E128, 2025. doi:
                                                                                              10.1017/S0022377825000509.
Gray points show the best successful child in each epoch,                                 [8] Dario Panici, Rory Conlin, Daniel W. Dudt, Kaya Unalmis, and
the dashed line is the cumulative best-QS frontier, open                                      Egemen Kolemen. The DESC Stellarator Code Suite Part I: Quick
                                                                                              and accurate equilibria computations, 2022. arXiv:2203.17173.
circles identify the best gate-valid child, and the red line                              [9] Daniel Dudt, Rory Conlin, Dario Panici, and Egemen Kolemen.
is the ancestry of the selected output.                                                       The DESC Stellarator Code Suite Part III: Quasi-symmetry opti-
                                                                                              mization, 2022. arXiv:2204.00078.
                                                                                         [10] Matt Landreman and Elizabeth Paul. Magnetic fields with precise
                                                                                              quasisymmetry for plasma confinement, 2021. arXiv:2108.03711.
7                 Conclusion                                                             [11] Patrick Kim, Rogerio Jorge, and William Dorland. The On-Axis
                                                                                              Magnetic Well and Mercier’s Criterion for Arbitrary Stellarator
                                                                                              Geometries, 2020. arXiv:2011.07416.
We presented a proof of concept for agentic multi-objective                              [12] Alan A. Kaptanoglu, Alexander Wiedman, Jacob Halpern, Siena
stage-one stellarator optimization. The language-model                                        Hurwitz, Elizabeth J. Paul, and Matt Landreman. Reactor-scale
                                                                                              stellarators with force and torque minimized dipole coils, 2024.
agent serves as a stateful scientific controller over parent                                  arXiv:2412.13937.
equilibria, Fourier-mode access, objective specifications,                               [13] Alan A. Kaptanoglu, Matt Landreman, and Michael C. Zarnstorff.
                                                                                              Optimization of passive superconductors for shaping stellarator
and local budgets. A deterministic DESC layer owns the                                        magnetic fields, 2025. arXiv:2501.12468.
physical contract, execution, evaluation, and acceptance
decision. This division of responsibility lets the agent con-
duct extended multi-stage routes and supports continuous
multi-start operation with complete lineage and optimizer
feedback.
    In a selected common-budget subset of an expand-
ing finite-beta QA campaign, gate-valid configurations
increase from five inputs to nineteen outputs, accompa-
nied by lower median QS RMS and maximum curvature.
A long-route case achieves a 9.10× QS reduction while
repairing magnetic-well and curvature violations, exposing
the nonmonotone acquisition and repair behavior behind
the endpoint. Together, the experiments produce 734
versioned transitions. The result validates the proposed
progression from agentic optimization to data infrastruc-
ture: each route accumulates two coupled assets, physically
improved equilibria and reusable state–action evidence.
    The broader proposition is that agentic systems can
serve as scientific data engines for stellarator design. By re-
peatedly applying expert-like sequential reasoning through
a physics-governed interface, the system can expand the
scale, physical alignment, and informational depth of avail-
able design data. This provides a practical foundation
for broader configuration datasets, learned optimization
priors, and increasingly capable agentic design policies.

References
 [1] R. Jorge, A. Goodman, M. Landreman, J. Rodrigues, and F. Wech-
     sung. Single-Stage Stellarator Optimization: Combining Coils with
     Fixed Boundary Equilibria, 2023. arXiv:2302.10622.




                                                                                     9
