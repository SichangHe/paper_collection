                                         PREPRINT, SEPTEMBER 2026                                                                                                               1




                                                 Verification Reward Model for Reinforcement
                                                      Learning in Chip Design Verification
                                                                                                   Shashank Chaurasia



                                            Abstract—We propose a Verification Reward Model (VRM)                therefore not only what to reward but which quantities may
                                         framework for training language models to create and repair             be learned, which must remain deterministic, and how partial
                                         chip verification artifacts. The central object is a versioned          evidence should be used before a full campaign completes.
                                         verification contract that binds requirements, permissible stim-
                                         ulus, observation boundaries, reference behavior, evaluation               This position paper proposes a Verification Reward Model
                                         budgets, and acceptance criteria. Compiler, simulator, formal,          (VRM) framework built on that separation. Fig. 1 summarizes
arXiv:2609.22347v1 [cs.AR] 17 Sep 2026




                                         mutation, coverage, and expert-review evidence are converted            the architecture. A frozen verification contract and a protected
                                         into auditable records. Deterministic acceptance checks remain          evaluator produce versioned evidence. A learned outcome
                                         outside the learned model. A learned outcome model predicts             model predicts expensive future evidence from the contract,
                                         expensive future evidence from the specification, the generated
                                         artifact, and explicitly masked partial evidence; a semantic            the artifact, and explicitly masked partial evidence; a semantic
                                         critic identifies evidence-supported weaknesses; a deterministic        critic identifies evidence-supported weaknesses; a deterministic
                                         reward composer translates the resulting quality vector into task-      reward composer maps measured outcomes to training rewards;
                                         conditioned training rewards. Extensions include paired clean/fault     a cost-aware scheduler decides which evaluations to run.
                                         interventions, marginal fault-discovery rewards, uncertainty-           Learned components inform selection and diagnosis. They
                                         aware evaluation scheduling, and a quarantined cross-domain
                                         learning loop. Evaluation emphasizes independently validated            never override a measured result or an acceptance check.
                                         fault detection, false alarms, generalization across design families,      Our contributions are as follows.
                                         and total cost to reach a specified quality level. We describe a           1) A verification contract and evidence-record formalism
                                         first experiment on a small, open-tool-compatible benchmark with               that makes observation boundaries, provenance, and
                                         lightweight models, with full UVM capability admitted through
                                         feature-specific qualification. This is a position paper: we specify           evidence status explicit (Sections III and IV).
                                         the framework and the experiments that would test it, and we               2) A sound fault-detection target for hardware, with vali-
                                         report no training, EDA, or silicon results.                                   dated mutation populations, paired clean/fault controls,
                                            Index Terms—Verification reward models; reinforcement learn-                attribution rules, and explicit units for recall and false
                                         ing; mutation testing; EDA evidence; hardware verification; large              alarms (Section V).
                                         language models                                                            3) An eligibility-gated reward design with marginal fault-
                                                                                                                        discovery credit and correctly applied potential-based
                                                                I. I NTRODUCTION                                        shaping (Section VI).
                                                                                                                    4) A partial-evidence outcome model, an evidence-linked
                                            Language models can now produce syntactically plausible
                                                                                                                        critic, and an uncertainty-aware evaluation scheduler with
                                         SystemVerilog, assertions, and testbench components [1], [2],
                                                                                                                        mandatory random audits (Sections VII to IX).
                                         [3], [4]. Turning that ability into a dependable verification
                                                                                                                    5) A preregistrable experimental program with hypotheses,
                                         assistant requires a training signal that rewards what verification
                                                                                                                        family-level splits, baselines, and ablations that could
                                         engineers actually value: detection of real design faults, absence
                                                                                                                        confirm or refute the approach (Section XII).
                                         of false alarms on correct designs, requirements traceability,
                                         and bounded evaluation cost. Simple proxies do not supply                  We report no training, EDA, or silicon results. The named
                                         that signal. Code coverage can rise while checking weakens;             mechanisms are design labels rather than established techniques,
                                         an assertion with zero failures may never have been activated;          and the numerical thresholds are initial engineering targets to
                                         a testbench that prints an unconditional error “detects” every          be fixed by preregistration after a pilot.
                                         fault and every clean design alike. A policy optimized against
                                         such proxies will exploit them [5], [6].                                A. Primary objective
                                            We take the reward function for a verification-generation               For a fixed verification task distribution and evaluation
                                         policy to be a mapping (x, y, e) 7→ R, where x describes                budget, we aim to increase the number and diversity of
                                         a verification problem, y is a generated verification artifact,         independently validated DUT faults detected while controlling
                                         and e contains evidence from electronic design automation               false alarms on independently validated correct behavior.
                                         (EDA) tools. Unlike conversational preference learning [7],             Secondary goals are lower evaluation cost, faster repair,
                                         this setting has executable ground truth: compilers, simulators,        greater requirements traceability, and useful generalization to
                                         formal engines, and mutation campaigns can measure much of              unfamiliar designs.
                                         what the reward should encode. But those measurements are                  The target artifact may be a sequence, test, assertion set,
                                         expensive, partial, and easy to corrupt. The design problem is          coverage model, scoreboard, monitor, driver, reference model,
                                          S. Chaurasia is an AI Researcher with MooresLab AI (e-mail: shashank   testplan, or complete environment. Each requires its own eval-
                                         @mooreslab.ai). Preprint, September 2026.                               uation contract. A testplan cannot earn a compilation reward;
PREPRINT, SEPTEMBER 2026                                                                                                                               2



              Frozen contract                                                                                              Fixed reward
                                         Policy proposes          Protected execution        Versioned evidence
              and independent                                                                                                composer
                                        verification artifact    Clean/fault evaluation     and eligibility checks
                   oracles                                                                                               and policy update


                                                                   Learned outcome
                                                                    predictor / critic                 Evaluation scheduler
                                                                    Partial evidence;                  Cost-aware selection
                                                                   uncertainty; scope                   and random audit


Fig. 1. Proposed separation of trusted evidence, learned prediction, and budget allocation. Solid paths carry measured evidence to a deterministic reward
composer. Dashed paths support selection and critique; they do not replace the contract’s required acceptance checks.



a stimulus-only sequence cannot independently demonstrate                     checkers, and clean controls must guard against unconditional
checker correctness.                                                          failure.
                                                                                 Reward shaping and uncertainty. Potential-based shaping
B. Scope boundaries                                                           preserves optimal policies under stated assumptions [16].
                                                                              Conformal prediction supplies distribution-free intervals under
   The first campaign targets digital block-level verification.
                                                                              exchangeability [17]. We use both with their assumptions stated
Analog behavior, electrical PHY correctness, production signoff,
                                                                              explicitly, because adaptive policy optimization violates them
and complete SoC correctness remain outside the initial claim.
                                                                              in ways that matter for this application.
A selected cycle-level simulator can evaluate a particular digital
model; it cannot establish all physical behavior. Every result
                                                                                   III. C ONTRACT, E VIDENCE , AND D ECISION ROLES
states its observation boundary and modeling assumptions.
                                                                              A. Verification contract
                        II. R ELATED W ORK                                       We define a task contract
   Preference-based reward models. InstructGPT trained a
reward model from ranked responses and optimized a policy                         C = (S, D, I, O, A, G, B, V ),
against it [7]. DPO removes the separately trained reward           where S is the requirement set, D identifies DUT versions,
model from the policy-optimization loop [8], and GRPO I is the legal input space, O defines observability, A contains
provides a group-relative policy-gradient baseline suited to environment assumptions, G identifies trusted oracles and
verifiable rewards [9]. Optimizing against an imperfect reward goals, B is the evaluation budget, and V records versions
model degrades true performance as optimization pressure and provenance. Interface timing, reset semantics, supported
increases [6], and reward hacking has been characterized parameter values, allowed nondeterminism, and outstanding-
formally [5]. Reward-model ensembles mitigate but do not transaction rules belong in C.
eliminate the problem [10]. LLM-as-a-judge evaluation agrees        The policy may edit only declared artifact paths. It cannot
well with human preference on conversational tasks [11], change the DUT, reference model, grading scripts, required
but that agreement is measured on tasks without executable coverage bins, mutation population, pass criteria, or tool
ground truth. Our design responds to these results by keeping constraints unless the task explicitly concerns that object and
measured acceptance outside the learned model and by treating supplies an independent evaluator. Contract changes create new
optimization against the surrogate as an experiment to be task versions.
audited rather than a default.
   LLMs for hardware design and verification. VerilogEval B. Five distinct services
and RTLLM benchmark RTL generation with fixed functional
                                                                    Fig. 1 separates five services. We refer to the two learned
testbenches [1], [2]. AssertLLM generates SystemVerilog as-
                                                                 components, the outcome model and the semantic critic, jointly
sertions from specification documents [3], AutoSVA generates
                                                                 as the VRM.
formal properties for module interactions from annotated
                                                                    Trusted evaluator T . Executes versioned tools and produces
interfaces [12], and AutoBench generates and evaluates HDL
                                                                 evidence e = T (C, y). It owns process exit codes, time limits,
testbenches with LLMs [4]. These works measure artifact
                                                                 trace collection, and protected reference files.
quality by fixed test outcomes or by agreement with reference
                                                                    Outcome model Oθ . Predicts future measurements under a
assertions. None trains a reward model over EDA evidence,
                                                                 named evaluation protocol. At evidence stage k:
and none addresses the credit-assignment problem that arises
when the artifact under evaluation is itself the observer.
                                                                                     pθ (q>k | C, y, e≤k , mk ).
   Mutation testing. Mutation analysis is a mature technique
for measuring test-suite adequacy [13]. MCY applies it to           The mask mk identifies what has actually been observed.
hardware with formal filtering of equivalent mutants [14]. MIST- The model must never receive its target measurements through
RL uses incremental mutation-kill rewards to train unit-test logs, filenames, summaries, or metadata. Its scalar utility head,
generators for software [15]. We extend the mutation reward to written uθ , is used for ranking and scheduling.
hardware, where valid faults must be qualified under contract       Semantic critic Jϕ . Produces a structured assessment of
conditions, detection must be attributed through temporal requirements alignment, artifact architecture, and likely gaps.
PREPRINT, SEPTEMBER 2026                                                                                                              3



Each assertion is linked to a requirement, code location, or        B. Evidence stages
evidence record. Unverified diagnoses are labeled hypotheses.         Stage E0 contains only the contract and generated artifact. E1
   Reward composer U . Applies fixed validity rules and a           adds lint and compilation. E2 adds a short, fixed smoke suite.
versioned scalarization to measured outcomes. It can expose         E3 adds a larger clean regression and requirements coverage.
a separate predicted utility for scheduling. A predicted utility    E4 adds validated fault campaigns. E5 adds an independently
cannot overwrite a measured result.                                 administered audit on hidden fault families, alternate clean
   Evaluation scheduler Aψ . Chooses the next candidate, test       implementations, or a second qualified tool flow.
subset, or fidelity level to spend budget on. Its objective is        We train separate heads or stage-conditioned models for
evidence acquisition and decision quality. It has no authority      E0-to-E4, E1-to-E4, and E2-to-E4 prediction, and include
to change acceptance criteria.                                      real partial trajectories in training. Random evidence dropout
   These services may eventually share representations, but         can regularize a model, but it does not by itself replicate
their permissions, training targets, and validation sets remain     the missingness patterns of a scheduler that selectively runs
distinguishable.                                                    expensive jobs.


C. Why a learned model is useful                                    C. Repository-scale context
   A network adds little value when every input already               We use bounded retrieval around interfaces, transaction
contains all the numbers needed by a fixed reward formula.          definitions, the candidate diff, requirements, checker call sites,
Its useful jobs are predicting unrun regressions, interpreting      and relevant dependency slices, and record which files were
local code/evidence interactions, ranking candidates under          omitted. A flat concatenation of an entire RTL repository can
partial observations, estimating repairability, and deciding        hide truncation-induced failure. We begin with features and
which additional measurement is informative. The deterministic      compact code encodings, then test whether richer retrieval or
composer remains the baseline to beat.                              a graph encoder improves held-out decisions.


IV. E VIDENCE R EPRESENTATION AND T RUST B OUNDARIES                      V. FAULT D ETECTION AS A Q UALIFIED TARGET

   An evidence record stores a contract digest, candidate digest,   A. Validated fault population
toolchain digest, evaluation stage, observed timestamps, work-         Let MC be the fault population declared for contract C. A
load or seed identifier, measurement units, status, uncertainty,    mutation is eligible only after checking that it builds, is relevant
and raw artifact references. Records are append-only. Candidate-    to legal operating conditions, and changes an observable
controlled text is treated as data, including comments and logs     requirement under those conditions. Where feasible, formal
that contain instructions to a judge.                               comparison or a witness trace validates relevance. Equivalent,
   We use distinct statuses: pass, fail, unknown, not_run, and      unreachable-under-contract, invalid, and unresolved mutations
infrastructure_error. A formal timeout normally produces            are separate categories. A timeout is not proof that a mutation
unknown. A crashed worker produces an infrastructure error.         is equivalent. MCY provides an implementation starting point
A reproducible candidate-induced deadlock may be a task             for hardware mutation generation and formal filtering [14].
failure if the contract defines a completion bound. The outcome        Mutation operators should span state transitions, counter
depends on its cause and contractual meaning.                       boundaries, handshake retention, reset behavior, address de-
                                                                    coding, ordering, data corruption, arbitration, and parameter
                                                                    edge cases. Structural netlist mutations and semantic RTL
A. Structured evidence channels
                                                                    fault injections are complementary campaigns. Real historical
   Compilation captures errors, supported language features,        defects with independently reviewed fixes form an additional,
elaboration status, and top-level binding. Simulation captures      more deployment-relevant test set when authorized data exists.
completion reason, transactions driven and observed, checker
activation, mismatches, dropped responses, reset episodes, and
seed identity. Coverage includes raw numerator, denominator, B. Sound kill definition
exclusions, hierarchy, and coverage-model version. Assertion        A fault is counted as detected when a candidate verification
evidence includes attempts, nonvacuous activations where artifact produces a reproducible, contract-relevant failure on a
measurable, failures, reset-disable intervals, and pending obli- validated faulty DUT and behaves acceptably on paired clean
gations. Mutation evidence includes validation status, fault controls. A missing library or simulator crash is not a valid
family, detection mechanism, and reproducer. Runtime evidence detection. A candidate that prints an unconditional error will
separates queueing, compilation, simulation, parsing, and model also fail the clean control and loses eligibility.
inference.                                                          For a test t and fault m, we define K(t, m) = 1 only
   An assertion with zero failures can be inactive. A scoreboard after detection attribution. The reproducer stores the triggering
with zero mismatches can have compared zero transactions. stimulus, observation, expected behavior, checker identity, and
A coverage percentage can increase after its denominator is minimized evidence slice. Duplicate manifestations of the same
weakened. These conditions must be visible to the evaluator. root fault do not become multiple discoveries.
PREPRINT, SEPTEMBER 2026                                                                                                            4



C. Recall and false alarms use explicit units                        validity, and all task-required evidence. Failure on a known
  For a fixed set of independently adjudicated design/workload       faulty DUT is expected evidence of success when attribution
episodes, define a positive episode as one containing a              is valid. A global rule that penalizes every simulation failure
qualifying defect. Precision and recall then have their usual        is therefore unsuitable for verification generation.
meanings:
                                                                     C. Marginal suite utility
                     TP                    TP
            P =              ,    R=               .
                 TP + FP                TP + FN                      PFor a suite S and fixed nonnegative fault weights vm with
                                                                      m vm > 0, define
   The same episode definition must govern all four counts.
Combining a count of unique buggy designs with a count of                             P
millions of clean transactions does not yield a precision. We                             m∈MC vm 1[∃t ∈ S : K(t, m) = 1]
                                                                            F (S) =               P                          .
report mutation recall by fault family and clean false-alarm                                         m∈MC vm
rate separately. F1 may be a secondary diagnostic; its value            The incremental value of a new test is F (S ∪ {t}) − F (S).
depends on the artificial defect prevalence in the benchmark.        Repeated tests that detect the same already-covered faults
   Zero observed clean failures does not establish a zero false-     receive no additional discovery credit. All denominators are
alarm probability. Under an independent Bernoulli model,             frozen for a campaign. This principle has precedent in software
zero failures in n trials gives a one-sided 95% upper bound          mutation-based RL [15]; the hardware extension must establish
1 − 0.051/n . For n = 100, this is about 2.95%. Correlated           valid faults, temporal behavior, and checker soundness.
seeds require cluster-aware analysis and can supply much less           Runtime cost can be included as a separately bounded penalty
information than 100 independent trials.                             or a budget constraint. We report both unconstrained detection
                                                                     and cost-normalized detection so that smaller tests do not win
                      VI. R EWARD D ESIGN                            by omitting required behavior.
A. Quality vector and ranges
  The measured quality vector is                                     D. Potential-based shaping
                                                                       Intermediate feedback can use a fixed potential over observ-
        q = (qfault , qreq , qrobust , qeff ),   qj ∈ [0, 1].        able artifact states:
   Here fault quality is severity-weighted detection over a
                                                                                      rt′ = rt + γΦ(st+1 ) − Φ(st ).
fixed validated population; requirements quality measures
independently instrumented, checked obligations; robustness             Potential-based shaping has policy-invariance results under
measures predefined legal stress scenarios; and efficiency is a      the associated MDP assumptions [16]. For the finite repair
bounded transformation of runtime at an otherwise comparable         episode considered here, we freeze Φ during each collection/up-
quality level. Raw code coverage and subjective style remain         date cycle and set the terminal potential consistently, normally
diagnostics in the initial experiment.
                                 P                                   to zero. Clipping individual shaping terms, changing the poten-
   Weights satisfy wj ≥ 0 and j wj = 1. A starting scalar-           tial mid-episode, or rewarding only positive improvements can
ization for complete environments is (0.55, 0.25, 0.15, 0.05).       invalidate the intended telescoping argument. Final acceptance
These values are hypotheses, not empirically optimal settings.       uses the original terminal metric.
Scoreboard, assertion, stimulus, and testplan training each use
a different versioned contract. A weight is interpretable only       VII. M ODEL A RCHITECTURE AND L EARNING O BJECTIVES
together with the component’s normalization and denominator.
                                                                     A. Baselines first
                                                                        We implement a fixed-rule composer, a tabular outcome
B. Eligibility before utility                                        predictor, and a frozen generic LLM judge before a domain-
  We define the measured terminal reward as                          trained VRM. The tabular predictor sees only information
                                                                     genuinely available at its evaluation stage. A gradient-boosted
      
       −1,       tampering or confirmed unsoundness,                 tree or small multilayer perceptron may outperform an expen-
      
      
      
      −0.5,                                                         sive text model on a small dataset. That outcome would itself
                 attributable build/task failure,                    be informative and would argue for the simpler model.
RDV =
      
      
      NA,       required evidence unresolved,
      P
           w q
         j j j , eligible evidence complete.                         B. Structured outcome model
   The numerical range of scored records is [−1, 1]. NA means           A candidate architecture combines a compact code/spec-
the sample is masked from the applicable outcome loss or held        ification encoder, structured EDA features, evidence masks,
for another evaluation; it is not silently converted to zero. The    and task/fidelity embeddings. Late fusion feeds classification,
controller budgets unresolved work so that deliberate resource       regression, ranking, and abstention heads. The first version need
exhaustion cannot create an advantageous free pass.                  not use a graph neural network. A later requirement-to-code-to-
   Eligibility includes protected-file integrity, correct binding,   checker graph can expose whether stimulus, observation, and
minimum activity, clean-control behavior, reference-oracle           comparison paths jointly support an obligation.
PREPRINT, SEPTEMBER 2026                                                                                                             5



  We predict per-fault detection probabilities where the data        B. Requirement-fault-checker interaction record
supports them and aggregate by fault family with uncertainty.
                                                                        We store a sparse tensor indexed by requirement, fault family,
For count outcomes, successes and trials are retained instead
                                                                     stimulus family, checker, and evidence stage. Its entries contain
of collapsed into a percentage. A beta-binomial head is one
                                                                     activation and detection outcomes. The VRM is trained to
candidate for overdispersed detection counts. Its assumptions
                                                                     distinguish failure to activate a condition, failure to propagate
must be checked against simpler calibrated models.
                                                                     a fault, and failure to observe or check the resulting behavior.
                                                                     These are explanatory targets; supervision must come from
C. Multi-task training                                               instrumentation or reviewed traces.
  We use a masked objective
                                                                     C. Metamorphic soundness tests
        L = λb LBCE + λr Lreg + λp Lpair + λc Lcritic .
                                                                        We challenge the artifact with semantics-preserving renam-
   Binary heads estimate declared events, continuous heads           ing, legal timing variation, alternate clean implementations,
predict future metrics, pairwise heads rank candidates, and          harmless logging changes, and reordered independent transac-
the optional critic head learns evidence-linked feedback. Loss       tions where the contract permits it. A black-box verification task
weights are tuned on development families. Expert labels are         should not rely on private internal signal names. A white-box
recorded with reviewer disagreement, not collapsed into an           task can use declared internal observability and must identify
unexplained authoritative score.                                     that dependency.
   For a valid pair a ≻ b, the ranking term uses the utility head       These challenges also test the judge: harmless formatting
uθ of the outcome model:                                             should not materially change its correctness estimate; removing
                                                                     a real comparison should lower it. An invariance failure
                                                                     becomes training data and an evaluator defect ticket.
               Lpair = − log σ(uθ (a) − uθ (b)).

   Pairs must share contract, fidelity, budget, and scalarization.      IX. U NCERTAINTY-AWARE E VALUATION AND AUDIT
Pareto-incomparable candidates remain incomparable unless a
stakeholder weight vector is supplied. A higher-mutation/lower-      A. What uncertainty means
coverage candidate is not automatically ranked above every              We separate aleatoric variation, such as random workload
alternative. Near ties and unresolved evidence are masked or         behavior, from epistemic uncertainty caused by unfamiliar
modeled explicitly. Many pairs from the same candidates do           artifacts or sparse data. Ensembles, quantile models, and held-
not create independent data.                                         out calibration are candidate techniques. Ensemble agreement
                                                                     alone cannot establish correctness; reward-model ensembles
D. Critic reliability                                                are known to retain reward-hacking risk [10].
                                                                        Conformal intervals can be considered when calibration
   The critic emits issue category, requirement identifier,
                                                                     and deployment data satisfy the relevant exchangeability
code span, evidence identifier, confidence, and a proposed
                                                                     assumptions [17]. Adaptive policy optimization changes the
discriminating test. An unsupported explanation cannot count
                                                                     distribution. Ordinary calibration guarantees cannot be asserted
as a verified defect. We evaluate whether following a critique
                                                                     automatically for newly optimized candidates or unseen IP
improves independently measured results. A fluent explanation
                                                                     types.
with no repair benefit should not increase reward.

   VIII. C OUNTERFACTUAL AND I NTERACTION -BASED                     B. Scheduler objective
                    E XTENSIONS                                         The scheduler selects an evaluation action a using an
A. Paired clean/fault interventions                                  estimated decision-value objective such as
   Matched runs use the same legal stimulus, seed, tool version,                       E[reduction in selection regret | a]
and environment while changing only the DUT fault. This                       A(a) =                                        .
                                                                                             E[evaluation cost | a]
isolates the observed effect of that injected change within the
controlled experiment. It does not establish general real-world         A practical approximation combines expected quality im-
causal attribution beyond the model and contract.                    provement, uncertainty, and fault-family diversity. The approx-
   A second intervention changes only the checker or stimulus        imation is a scheduling heuristic. It is not a theorem that the
component. For example, compare an original sequence and             next selected candidate is optimal.
an added backpressure sequence under a weak and a repaired              We reserve an initial 20% of evaluation budget for stratified
scoreboard. A four-cell experiment reveals whether the stimulus      random audits, independent of predicted quality, and record
improvement becomes observable only after the checker is             selection probabilities. This limits blind spots and makes
repaired. This addresses a central credit-assignment problem:        selection bias measurable. Predictive screening is allowed to
a useful test can appear worthless when the observer cannot          save EDA work only after its false-rejection behavior is audited.
detect its consequence.                                              All release candidates receive the mandated full evaluation.
PREPRINT, SEPTEMBER 2026                                                                                                           6



C. Stopping and escalation                                                    XI. W ORKED V ERIFICATION S CENARIO
   Evaluation escalates to real measurement when uncertainty           Consider a parameterized synchronous FIFO whose con-
is high, evidence conflicts, a new failure family appears, or       tract fixes reset behavior, simultaneous push/pop semantics,
a candidate approaches a release threshold. Evaluation of a         ordering, and backpressure. Candidate A drives many random
candidate stops when it is conclusively invalid or cannot meet      transactions and reaches broad RTL activity, but compares only
the remaining budget. Infrastructure failures are retried under     a total transfer count. Candidate B exercises wraparound and
a bounded policy and counted in operational cost.                   compares every returned data item using an independent queue
                                                                    model.
                                                                       A validated fault duplicates one stored value at wraparound.
     X. P OLICY T RAINING AND THE DATA F LYWHEEL                    Candidate A may retain a high activity score and miss the defect.
                                                                    Candidate B produces a data mismatch on the faulty FIFO and
   We begin with supervised fine-tuning on authorized, exter-       passes paired clean runs. Its mismatch is positive verification
nally accepted artifacts and repair trajectories. DPO is a useful   evidence. A third candidate emits an error unconditionally; its
offline preference baseline that does not require a separately      clean-control failures disqualify it.
optimized reward model during policy training [8]. For online          The VRM should predict the relative detection strength from
RL, we evaluate a GRPO-style or comparable policy-gradient          the comparison logic and smoke evidence before a full fault
baseline using fixed external rewards [9]. Algorithm choice is      campaign. Its critic can identify the missing data comparison
an empirical question settled on the development families.          in A, cite the affected requirement, and propose a wraparound
   We store the exact behavior-policy checkpoint, prompt,           reproducer. The final detection credit is awarded only after the
sampling settings, actions, tool outputs, and reward version.       trusted campaign validates that behavior.
For long EDA jobs, a complete small batch is gathered under
a frozen policy and scorer before updating. A GRPO trainer
cannot treat arbitrary stale trajectories as on-policy without                    XII. E XPERIMENTAL P ROGRAM
appropriate handling. Groups with identical rewards carry no        A. Hypotheses
useful relative preference signal; the remedy is harder tasks or       H1: partial-evidence outcome prediction improves candidate
more diverse data, not invented differences.                        selection under a fixed total evaluation budget. H2: soundness-
   The initial role of the VRM is reranking and scheduling. Its     qualified mutation targets generalize to withheld fault operators
use as a policy-optimization reward is a later ablation with a      and historical defects better than raw coverage targets. H3:
small, audited influence. Measurements and predictions remain       component-intervention supervision improves repair credit
separate fields. Repeated optimization against a surrogate is       assignment. H4: learned critiques improve externally measured
specifically tested for divergence between predicted utility and    repairs beyond a generic judge. H5: the complete flywheel
hidden external outcomes, the failure mode documented by            improves a frozen-policy baseline without increasing clean
Gao et al. [6].                                                     false alarms.


A. Flywheel sequence                                                B. Splits and baselines
                                                                       We group all descendants of a design, generator template,
  1) Freeze a contract set, evaluator, split, and policy check-
                                                                    reference implementation, and mutation family before splitting,
     point.
                                                                    and maintain train, development, calibration, and sealed-test
  2) Generate multiple bounded candidates or repair actions.
                                                                    partitions. Evaluation covers both new implementations of
  3) Run integrity, build, and activity checks.
                                                                    familiar IP types and withheld IP categories. Public benchmark
  4) Allocate clean, stress, and fault evaluations using the
                                                                    scores are supplementary because exposure during model
     scheduler plus random audits.
                                                                    pretraining may be unknown.
  5) Adjudicate ambiguous failures and compute measured
                                                                       Baselines are random candidate selection, fixed heuristics,
     rewards.
                                                                    generic LLM judging, tabular prediction, text-only VRM,
  6) Train the outcome model and critic on training families
                                                                    partial-evidence VRM, and a full-evidence oracle-ranking upper
     only.
                                                                    reference. The oracle consumes the expensive measurements
  7) Train a challenger policy using the selected baseline or
                                                                    and must be charged their actual cost when used operationally.
     RL procedure.
  8) Evaluate the challenger on development families with
     frozen external metrics.                                       C. Metrics
  9) Promote only after a separate release audit; otherwise            Primary metrics are validated fault recall at a bounded false-
     retain the incumbent.                                          alarm rate and total cost to reach a target recall. We report
 10) Add genuinely new, authorized failures to the next             per-family recall, top-k selection regret, missed-promising-
     training cycle and version all changes.                        candidate rate, calibration, coverage of prediction intervals,
  The hidden final test suite is not fed back into the same         abstention rate, repair success, and valid-output rate. Cost
development cycle. Once detailed test feedback has influenced       accounting includes model inference, data labeling, retraining,
development, that suite is retired from final-test status.          tool startup, and failed jobs.
PREPRINT, SEPTEMBER 2026                                                                                                                        7



   We use paired comparisons on the same held-out contracts              XV. FAILURE M ODES AND R ESEARCH D ECISIONS
and bootstrap at the design-family level, reporting effect             The largest risks are weak oracles, mutation distribution mis-
sizes and confidence intervals. A high Pearson or Spearman          match, hidden label leakage, evaluator tampering, false failures
correlation alone does not demonstrate safe screening. The con-     from incorrect checkers, unsupported language constructs, and
sequences of the actual top-k decisions are what is evaluated.      uncalibrated surrogate optimization. Each corresponds to an
                                                                    ablation or metamorphic challenge in Sections VIII and XII. A
D. Critical ablations                                               learned model that cannot beat the tabular baseline should be
  Remove mutation validity filtering; remove clean controls;        simplified or deferred. A fault reward that improves synthetic
replace requirement coverage with raw coverage; remove              mutations while harming historical-defect performance must
evidence masks; compare family-level and random-record splits;      be reweighted or redesigned.
remove random audits; remove the critic; replace the text              The strongest initial contribution would be a reproducible
model with tabular features; optimize aggressively against          evidence protocol plus an audited cost-quality gain on un-
the surrogate. The first several ablations are intentionally        familiar design families. A general verification foundation
unsafe diagnostic experiments and cannot become deployment          model is a longer-term outcome that requires broader data and
configurations.                                                     demonstrated transfer. The immediate scientific claim should
                                                                    remain narrower and measurable.
 XIII. R ESOURCE M ODEL AND F IRST I MPLEMENTATION
                                                                                             XVI. C ONCLUSION
   The first campaign uses CPU EDA workers and a small local
model before any large-model campaign. A single consumer-              The proposed VRM framework treats verification quality
grade GPU can support an optional compact-model path; fit           as a contract-dependent, evidence-supported quantity. Learned
and throughput must be measured on the target hardware.             models predict missing outcomes, interpret artifact weaknesses,
Full-model or large-context training is not assumed. QLoRA          and allocate evaluation effort. Trusted external checks determine
provides a parameter-efficient training technique; actual fit and   eligibility and release. The recommended first experiment is
throughput still require local measurement [18].                    a small family-split FIFO, arbiter, register-block, and stream-
   For D designs, N candidates, S clean runs, M faults, and         controller campaign that tests whether partial-evidence ranking
Sm runs per fault, the simulation count is                          reduces EDA cost without losing validated fault detection. That
                                                                    experiment can establish the value of the learning layer before
                  Nsim = DN (S + M Sm ).                            committing to a larger domain-specific policy.

   An illustrative pilot with D = 24, N = 6, S = 3,
                                                                                                  R EFERENCES
M = 24, and Sm = 2 has 7,344 simulation instances. At
an assumed five seconds per simulation this is 10.2 CPU-hours        [1] M. Liu, N. Pinckney, B. Khailany, and H. Ren, “VerilogEval: Evaluating
                                                                         large language models for Verilog code generation,” in Proc. IEEE/ACM
of simulation alone. Mutant compilation, original compilation,           Int. Conf. Computer-Aided Design (ICCAD), 2023. arXiv:2309.07544.
formal filtering, scheduling, and model work are additional.             [Online]. Available: https://arxiv.org/abs/2309.07544
These are planning calculations, not measured runtimes.              [2] Y. Lu, S. Liu, Q. Zhang, and Z. Xie, “RTLLM: An open-source
                                                                         benchmark for design RTL generation with large language model,” in
   The pilot starts with synthesizable SystemVerilog, a sup-             Proc. Asia and South Pacific Design Automation Conf. (ASP-DAC), 2024.
ported assertion subset, and independent testbench infrastruc-           arXiv:2308.05345. [Online]. Available: https://arxiv.org/abs/2308.05345
ture. Verilator and SymbiYosys supply relevant open-source           [3] W. Fang, M. Li, M. Li, Z. Yan, S. Liu, H. Zhang, and Z. Xie,
                                                                         “AssertLLM: Generating and evaluating hardware verification assertions
capabilities [19], [20]. UVM support must be qualified for               from design specifications via multi-LLMs,” arXiv:2402.00386, 2024.
the exact pinned features and library version; the existence of          [Online]. Available: https://arxiv.org/abs/2402.00386
upstream UVM work in Verilator does not justify an assumption        [4] R. Qiu, G. L. Zhang, R. Drechsler, U. Schlichtmann, and B. Li,
                                                                         “AutoBench: Automatic testbench generation and evaluation using
that every existing environment will run unchanged [21].                 LLMs for HDL design,” arXiv:2407.03891, 2024. [Online]. Available:
                                                                         https://arxiv.org/abs/2407.03891
 XIV. C ROSS -D OMAIN E XTENSION AND I NDEPENDENCE                   [5] J. Skalse, N. H. R. Howe, D. Krasheninnikov, and D. Krueger, “Defining
                                                                         and characterizing reward hacking,” in Advances in Neural Informa-
   A verification model can evaluate artifacts used to test              tion Processing Systems (NeurIPS), 2022. arXiv:2209.13085. [Online].
generated RTL. The RTL generator and verification generator              Available: https://arxiv.org/abs/2209.13085
                                                                     [6] L. Gao, J. Schulman, and J. Hilton, “Scaling laws for reward model
must not jointly redefine their own oracle. Trusted functional           overoptimization,” arXiv:2210.10760, 2022. [Online]. Available: https:
behavior is frozen and reference models are independently                //arxiv.org/abs/2210.10760
developed or reviewed. Newly discovered RTL counterex-               [7] L. Ouyang et al., “Training language models to follow instructions
                                                                         with human feedback,” arXiv:2203.02155, 2022. [Online]. Available:
amples enter a quarantine set until adjudicated. Architecture            https://arxiv.org/abs/2203.02155
requirements can supply obligations to both tracks, but shared       [8] R. Rafailov et al., “Direct preference optimization: Your language model
generated specifications are not independent proof of intent.            is secretly a reward model,” arXiv:2305.18290, 2023. [Online]. Available:
                                                                         https://arxiv.org/abs/2305.18290
   Common contract and evidence schemas are shared across            [9] Z. Shao et al., “DeepSeekMath: Pushing the limits of mathematical
tracks while acceptance owners remain separate. This enables             reasoning in open language models,” arXiv:2402.03300, 2024. [Online].
shared data engineering and representation learning without              Available: https://arxiv.org/abs/2402.03300
                                                                    [10] J. Eisenstein et al., “Helping or herding? Reward model ensembles
merging correctness authority into a single self-evaluating              mitigate but do not eliminate reward hacking,” arXiv:2312.09244, 2023.
model.                                                                   [Online]. Available: https://arxiv.org/abs/2312.09244
PREPRINT, SEPTEMBER 2026                                                                                                                                      8



[11] L. Zheng et al., “Judging LLM-as-a-judge with MT-Bench and Chatbot               transformations: Theory and application to reward shaping,” in Proc.
     Arena,” arXiv:2306.05685, 2023. [Online]. Available: https://arxiv.org/ab        16th Int. Conf. Machine Learning (ICML), 1999, pp. 278–287.
     s/2306.05685                                                                [17] A. N. Angelopoulos and S. Bates, “A gentle introduction to con-
[12] M. Orenes-Vera, A. Manocha, D. Wentzlaff, and M. Martonosi, “Au-                 formal prediction and distribution-free uncertainty quantification,”
     toSVA: Democratizing formal verification of RTL module interactions,”            arXiv:2107.07511, 2021. [Online]. Available: https://arxiv.org/abs/
     in Proc. 58th ACM/IEEE Design Automation Conf. (DAC), 2021, pp.                  2107.07511
     535–540.                                                                    [18] T. Dettmers, A. Pagnoni, A. Holtzman, and L. Zettlemoyer, “QLoRA:
[13] Y. Jia and M. Harman, “An analysis and survey of the development of              Efficient finetuning of quantized LLMs,” arXiv:2305.14314, 2023.
     mutation testing,” IEEE Trans. Softw. Eng., vol. 37, no. 5, pp. 649–678,         [Online]. Available: https://arxiv.org/abs/2305.14314
     2011.                                                                       [19] Veripool, “Verilator user’s guide,” documentation, accessed Sep. 15, 2026.
[14] YosysHQ, “Mutation Cover with Yosys (MCY),” software repository,                 [Online]. Available: https://verilator.org/guide/latest/index.html
     accessed Sep. 15, 2026. [Online]. Available: https://github.com/Yosys       [20] YosysHQ, “SymbiYosys documentation,” documentation, accessed Sep.
     HQ/mcy                                                                           15, 2026. [Online]. Available: https://yosyshq.readthedocs.io/projects/sb
[15] S. Zhu, J. Wang, J. Ai, and X. Li, “MIST-RL: Mutation-based incremental          y/en/stable/
     suite testing via reinforcement learning,” arXiv:2603.01409, 2026.          [21] Veripool, “Verilator documentation: UVM support and related techni-
     [Online]. Available: https://arxiv.org/abs/2603.01409                            cal reports,” documentation index, accessed Sep. 15, 2026. [Online].
[16] A. Y. Ng, D. Harada, and S. Russell, “Policy invariance under reward             Available: https://veripool.org/verilator/documentation/
