                                                                                                                                                                                 1




                                          Task-Specified Active Metrological Inspection with
                                             Measurement-Steered VLA Manipulation and
                                                   Deterministic Evidence Gating
                                                 Zhiling Chen1 , Jingzhan Ge1 , Ruimin Chen1 , Matthew P. Castanier2 , David Gorsich2 , Farhad Imani1



                                            Abstract—High-mix low-volume (HMLV) manufacturing re-                 dimensions, and tolerances, while different work orders for the
                                         quires inspection systems to adapt to changing parts, specifi-           same part may request a full conformance report, a particular
arXiv:2609.14219v1 [cs.RO] 13 Sep 2026




                                         cations, and work orders without repeated task-specific pro-             feature, or a functional group of requirements. Each change
                                         gramming. Existing inspection automation typically assumes
                                         predefined sensing sequences, while general purpose robot agents         can therefore restart a human-intensive workflow of reading
                                         optimize task completion rather than the completeness and                the specification, planning the inspection, programming and
                                         validity of metrological evidence. We formulate task-specified           validating the tool, acquiring measurements, and preparing the
                                         active metrological inspection and propose From Requirements to          report. The recurring preparation process in Fig. 1 (2), rather
                                         Admissible Metrological Evidence (FRAME), a hierarchical dual-           than measurement time alone, becomes a central obstacle to
                                         arm framework that converts an inspection instruction and struc-
                                         tured specification into traceable conformance evidence. FRAME           scalable HMLV inspection. What is needed is a system that
                                         coordinates learned manipulation with calibrated laser profilom-         determines from the current instruction and specification what
                                         etry: a task manager grounds and schedules requirements, active          evidence is required instead of executing a fixed part-specific
                                         surface correspondence verifies physical-to-specification localiza-      inspection plan.
                                         tion, and evidence memory tracks measurement provenance,                    Existing inspection technologies automate individual sens-
                                         admissibility, and coverage. Learned components may propose
                                         inspection targets and physical access actions, but deterministic        ing and measurement operations, but not this complete
                                         datum-grounded measurement, admissibility checks, coverage               specification-to-evidence workflow. Manual gauges are flex-
                                         auditing, and conformance evaluation prevent incomplete or               ible but slow and operator-dependent; coordinate measuring
                                         unverified evidence from authorizing PASS. A series of phys-             machines provide accurate and traceable measurements but
                                         ical experiments shows that FRAME achieves higher end-to-                generally rely on a prepared setup and validated program; two-
                                         end inspection reliability, fewer false accepts, and shorter task
                                         completion time.                                                         dimensional vision is fast but does not directly provide the
                                                                                                                  required three-dimensional geometry; area three-dimensional
                                            Index Terms—Robotic inspection, dimensional metrology, ac-            sensing can recover surfaces but remains limited by occlusion
                                         tive perception, vision-language-action models, vision-language
                                         models, laser profilometry.                                              and difficult feature access; and a laser line profiler provides
                                                                                                                  precise localized geometry only when it follows a controlled
                                                                                                                  scan trajectory. Consequently, introducing a new part still
                                                                 I. I NTRODUCTION                                 requires an engineer to interpret its specification and plan the

                                         H     IGH-MIX low-volume (HMLV) manufacturing requires
                                               quality inspection to adapt to frequent changes in parts,
                                         specifications, and inspection intents. Unlike mass production,
                                                                                                                  sequence summarized in Fig. 1 (2). As Fig. 1 (3) emphasizes,
                                                                                                                  every available tool trades precision, coverage, or per-part
                                                                                                                  setup effort. Flexible inspection therefore requires more than
                                         where the cost of a fixed inspection program can be amor-                an accurate sensor: it must decide what to inspect, how to
                                         tized over many identical units, HMLV production repeat-                 make the required regions measurable, and when the acquired
                                         edly introduces small-batch variants with different geometries           evidence is sufficient.
                                         and inspection semantics, as illustrated in Fig. 1 (1). This                Robot foundation models have recently made rapid progress
                                         regime resembles variational automation, in which a robot                in turning language and vision into generalizable physical
                                         persistently handles task instances with nontrivial variations in        actions. Vision-language-action (VLA) models scale language-
                                         object geometry and pose, rather than fixed automation, which            conditioned visuomotor control across tasks and embodi-
                                         repeatedly executes the same motions [1]. In this work, we               ments [2], [3], [4], while world-action models (WAMs) jointly
                                         consider its metrological counterpart: the physical inspection           predict future visual states and actions to model physical
                                         setup remains fixed, while the inspection task, part geometry,           dynamics and improve transfer to unseen motions and envi-
                                         object category, and initial pose may vary across jobs. Product          ronments [5], [6], [7]. However, stronger foundation policies
                                         evolution can change features, datum definitions, nominal                do not by themselves yield reliable long-horizon systems:
                                            1 Zhiling Chen, Jingzhan Ge, Ruimin Chen, and Farhad Imani are with
                                                                                                                  existing VLAs remain vulnerable to skill-chaining, subtask-
                                         the University of Connecticut, Storrs, CT, USA.                          dependency, and progress-tracking errors that compound over
                                         2 David Gorsich and Matthew P. Castanier are with the U.S. Army DEVCOM   multi-step execution [8], [9], while WAMs can still pro-
                                         Ground Vehicle Systems Center (GVSC), Warren, MI, USA.                   duce inaccurate imagined futures whose predicted outcomes
                                         DISTRIBUTION STATEMENT A. Approved for public release; distribution      may diverge from the physical states realized during execu-
                                         is unlimited. OPSEC11090                                                 tion [5], [10]. A complementary lesson has emerged from
                                                                                                                                                                                                2


           HMLV Manufacturing                           Inspection Preparation                  Inspection Technologies                           Task-Specified Active Inspection
            High Mix, low Volume                            New Part, new Program                    Many tools, each limited                          Stated task, reach any feature

             Many Different Parts                                                                                                                                        Visible Feature
                                                                                         Manual                     Simple,                                              Hole A (top face)
                                                 New Part
                                                                                        (Gauges)                  but slow and                                             Reachable
                                                                                                                    manual.
                                                                                                                                                                        Partially Occluded
                                                                                                                                                                             Feature
                                                   Read
                                                                                                                   Accurate,                                             Hole I (side face)
                                                Specification
                                                                                          CMM                but slow to program.                                        Limited Access

                                                                                                                                                                         Hidden Feature

                  …                                 Plan
                                                 Inspection                             2D Vision                     Fast,
                                                                                                                                                                         Hole R (bottom)
                                                                                                                                                                         Not Reachable

       Many Different Specifications                                                    (camera)                  but no depth.        Need 1: Task-Specified            Need 2: Active
                                                                                                                                       The work order sets         The specified feature may
                                                                                                                                       which feature to verify     sit on a hidden face. no
                                                                                                                                       and it differs per order.   single pose reaches all of
                                                                                        Structured                  Areal 3D,                                      them.
                                                 Program                                   light                   but misses
                                                 the Tool                                                                                 Task A
                                                                                        (areal 3D)                deep features.       Verify Hole A                               Hole R
                                                                                                                                       (top surface)                              (hidden)
                                                                                                                                                                               Not Reachable
                                                                                           Laser                    Precise,               Task B
                                                                                          Profiler            but need controlled       Verify Hole I


                 …
                                                 Measure                                                                               (side surface)
                                                                                         (line 3D)                 scanning.                                       Reorient
                                                 & Report
                                                                                                                                            Task C
                                                                                                                                         Verify Hole R                Hole R
         High Variety: every part has its
         own geometry and specification
                                                      Repeated for every new part:
                                                      manual effort does not scale
                                                                                                Every option trades precision,
                                                                                              coverage, or per-part setup effort.               …
                                                                                                                                       (bottom surface)              Reachable



          Our System
                                            (1) Look                         (2) Scan                        (3) Reorient                      (4) Scan
           Input                                                                                                                                                               Verdict

                                                                                                                                                                        Diameter
            Instruction
 "Verify the diameter of each                                                                                                                                           Consistency
  through-bore and its top-
   to-bottom consistency.”                                                                                                                                                         Pass
                                                                                                                                                                               Sort
           Specification
                                      Face Correspondence
     Opening diameter:                                                    Face A Measurement                                        Face B Measurement
                                    Specification   Current
       Ø6.0 ± 0.3 mm
                                       Face A               Top        H1    H2         …       H5                                 …     H6    H7           …
 Top-to-bottom consistency:
 |dtop − dbottom| ≤ 0.2 mm             Face B            Bottom       ∅6.04 ∅6.03       …     ∅6.02 Evidence Memory                …    ∅6.03 ∅6.04         …

Fig. 1. Motivation and overview of task-specified active inspection for HMLV manufacturing. High part and specification variability makes conventional
inspection preparation costly, while existing inspection technologies trade off accuracy, coverage, and per-part setup effort. A stated inspection task may
require features distributed across visible, partially occluded, and hidden surfaces, motivating both task-specified measurement and active reorientation. Our
system takes a natural-language instruction and structured specification, grounds the required features to the current part pose, alternates LOOK, SCAN, and
REORIENT to acquire verified evidence, produces a deterministic conformance verdict, and invokes SORT for an authorized binary outcome.




digital agents, where harness engineering improves practical                                   acquire complete admissible evidence for that scope, and
capability by surrounding a foundation model with structured                                   return a traceable inspection report and operational verdict.
tool interfaces, persistent state, execution feedback, valida-                                 The setting is task-specified because different work orders
tion, and opportunities to revise failed decisions [11], [12].                                 over the same part may require different features or functional
Early efforts brought language-model reasoning into robot                                      relations, and it is active because the required regions may
execution through generated control programs and composable                                    be visible, partially occluded, or inaccessible from the initial
perception-and-control representations [13], [14]; more recent                                 configuration, as shown in Fig. 1 (4). The robot must con-
robotics work has begun to adopt the fuller harness principle                                  sequently choose among observation, reorientation, scanning,
by exposing learned policies as bounded skills and orchestrat-                                 recovery, and final sorting rather than execute a fixed sens-
ing them with high-level planners, analytic primitives, mem-                                   ing sequence. This problem has three safety-relevant failure
ory, verification, and retry mechanisms [15], [16], [17]. This                                 sources: the inferred scope may omit a required requirement,
shift improves composition and recovery, but metrological                                      the system may admit evidence from a physical region that
inspection imposes a stricter system-level requirement: the                                    does not correspond to the required specification region, or
harness must ensure not only that a physical action succeeds,                                  the metrological process may classify a truly nonconforming
but also that every required characteristic is supported by                                    requirement as conforming. The central challenge is therefore
complete, correctly localized, and admissible evidence before                                  not merely exposing a hidden feature, but preventing an error
a PASS verdict can be issued.                                                                  at any of these stages from silently supporting PASS.
   We therefore study task-specified active metrological in-                                      We propose From Requirements to Admissible Metrolog-
spection. Given an inspection instruction, a structured spec-                                  ical Evidence (FRAME), a hierarchical framework for task-
ification, and an initial observation of a physical part, the                                  specified active metrological inspection that coordinates se-
robot must infer the task-induced requirement scope, actively                                  mantic task management, active physical access, deterministic
                                                                                                                                     3



metrology, and evidence-gated conformance. The execution            measuring machine planners generate collision-free probing
flow is illustrated in Fig. 1 (5). A task manager grounds the       sequences, while robot-mounted laser-scanner methods opti-
instruction to identifiers in the structured specification, main-   mize trajectory overlap and measurement uncertainty [18],
tains a surface-correspondence table between physical regions       [19], [20]. These methods automate a predefined measurement
and specification regions, and selects the next action from         plan but commonly assume a product model, designated
the uncovered requirements in evidence memory. Calibrated           features, or feature-specific scan strategies. Active acquisition
LOOK actions establish or verify the current correspondence;        instead selects informative viewpoints or trajectories to im-
a VLA-based manipulation expert performs contact-rich reori-        prove geometric coverage, with recent work extending this
entation and final sorting; and a measurement expert performs       formulation toward instruction-conditioned high-precision sur-
calibrated line-profile acquisition, datum-grounded measure-        face scanning [21], [22]. A complementary line detects and
ment, and requirement-specific evidence-admissibility checks.       localizes visual defects from nominal image data and increas-
Failed correspondence, acquisition, or admissibility checks         ingly supports language interaction [23], [24], [25]. How-
trigger another observation, reorientation, or scan. Evidence       ever, reconstruction methods do not determine requirement-
memory is not a store of model-generated conclusions: it is         level conformance, while anomaly detectors do not produce
a traceable ledger of measurements, their physical origins,         datum-grounded quantitative measurements. Our framework
admissibility outcomes, and requirement coverage. Only after        instead derives the required inspection scope from the current
every requirement in the inferred scope has been supported by       instruction and specification, actively exposes the correspond-
admissible evidence does a deterministic, specification-driven      ing surfaces, and admits only localized, metrologically valid
conformance evaluator produce the final verdict. We evaluate        measurements into coverage-gated conformance.
FRAME on task-specified active metrological inspection tasks
spanning four controlled workpiece families, five inspection-       B. Robot Foundation Models
task families, and additional CNC cases. Empowered by veri-
                                                                       Robot foundation models provide increasingly generalizable
fied surface correspondence and evidence-gated conformance,
                                                                    physical manipulation across tasks, objects, and embodiments.
FRAME demonstrates higher end-to-end reliability and shorter
                                                                    Vision-language-action models and generalist robot policies
task-completion time while producing fewer false accepts than
                                                                    scale language-conditioned visuomotor control, while world-
fixed exhaustive inspection and unconstrained VLM control in
                                                                    action models complement action generation with future-state
physical experiments.
                                                                    prediction [26], [27], [28], [5]. These capabilities are well
   The main contributions of this article are as follows.
                                                                    suited to changing the physical accessibility of inspection
   1) We formulate task-specified active metrological inspec-       surfaces under task, geometry, and pose variation, but active
       tion in terms of an instruction-induced requirement          metrological inspection cannot be closed by manipulation
       scope, active surface access, admissible evidence cov-       alone. It requires a planner that coordinates learned physical
       erage, and specification-driven conformance, and derive      actions with a calibrated inspection sensor and uses structured
       an auditable decomposition of its false-accept risk.         measurement feedback to determine whether an acquisition
   2) We develop a hierarchical active-inspection framework         should be repeated, another surface should be exposed, a
       that connects a task manager, calibrated viewpoint con-      remaining requirement should be measured, or the inspec-
       trol, a VLA-based manipulation expert, a deterministic       tion can terminate. This coordination becomes particularly
       measurement expert, a surface-correspondence table, ev-      important over long horizons, where skill-chaining, subtask-
       idence memory, and a specification-driven conformance        dependency, and progress-tracking errors can accumulate [8],
       evaluator.                                                   [9]. Our framework therefore uses a foundation policy to
   3) We introduce datum-grounded measurement opera-                realize contact-rich reorientation, while the planner converts
       tors, requirement-specific evidence-admissibility pred-      measurement validity, evidence admissibility, requirement cov-
       icates, post-reorientation verification, active recovery,    erage, and recovery diagnostics into the next sensing or manip-
       and coverage-gated verdict generation so that a learned      ulation subgoal, thereby allowing precision-sensor feedback
       proposal cannot directly authorize PASS.                     to steer physical execution without asking the learned policy
   4) We construct a controlled benchmark spanning four             itself to interpret or certify metrological results.
       workpiece families and five inspection-task families,
       and evaluate FRAME on a physical dual-arm platform
                                                                    C. Agentic Robot Planning
       through end-to-end comparisons, metrological valida-
       tion, and component-level analyses of requirement-scope         Agentic robot systems extend foundation models from direct
       grounding, surface correspondence, and diagnostic re-        action generation to planning and orchestration over modular
       covery.                                                      physical skills. Language-model planners map open-ended
                                                                    instructions to admissible or affordance-grounded actions;
                     II. R ELATED W ORK                             closed-loop agents further incorporate environmental feed-
                                                                    back, interleave reasoning with tool use, and retain experience
A. Industrial Inspection and Metrology Automation                   across trials [29], [30], [31], [32], [33]. Physical-agent systems
  Industrial inspection automation spans dimensional metrol-        bring these ideas to real robots by integrating perception and
ogy, active geometric acquisition, and appearance-based defect      control modules, expressing goals as optimizable constraints,
detection. In dimensional metrology, CAD-based coordinate           orchestrating learned primitives with recovery, and placing
                                                                                                                                    4



runtime structure around foundation policies [34], [35], [36],     B. Active Inspection and Surface Correspondence
[1], [15]. These approaches show that performance depends             The specification names target regions symbolically,
not only on the underlying policy but also on how skills are       whereas the robot must locate physical regions that provide
exposed, sequenced, monitored, verified, and retried. However,     the required evidence. Under the inspection-cell presentation
their feedback loops are generally organized around action         protocol, a part arrives in a finite set Xc of support-stable
progress or task completion, whereas active metrological in-       scanning configurations for object class c. Each configuration
spection must use structured measurement outcomes to de-           encodes support contact, a discrete orientation class, and
termine what physical action is needed next. Our framework         the robot–sensor arrangement, and determines the physically
therefore orchestrates learned manipulation and calibrated         scannable regions F scan (x). Membership requires a collision-
sensing in a shared loop: measurement validity, evidence           free, kinematically feasible sensor trajectory with valid stand-
admissibility, remaining requirement coverage, and recovery        off, incidence, field of view, and measurement range, while
diagnostics determine whether the planner issues LOOK, SCAN,       providing sufficient coverage of the target region and any
REORIENT, REACQUIRE, or termination.                               datum support required by the measurement; visual exposure
                                                                   alone is insufficient. The initial configuration x0 ∈ Xc is
               III. P ROBLEM F ORMULATION                          unknown, but a generic locating surface or upstream handler
   We study task-specified active metrological inspection.         restricts continuous translation and rotation to a calibrated
Given an inspection instruction I, a structured specification      capture range. Unconstrained orientations and unstable place-
S, and an initial observation o0 of a physical part P , the        ments are outside our scope. Let F phys denote the physical
robot must acquire the required evidence and return a traceable    surface regions of the part, and let
report with either a supported conformance decision or a fail-                         µ∗ : F phys → F ∪ {⊥}                     (3)
safe unresolved outcome. Unlike a fixed inspection program,
I selects the requirements for the current episode, while S           denote the ground-truth physical-to-specification correspon-
defines their interpretation and evaluation.                       dence, with ⊥ marking regions absent from the active specifi-
                                                                   cation. The currently scannable specification regions are there-
                                                                   fore µ∗ (F scan (xt )) \ {⊥}. Before scan evidence can support
A. Task-Specified Inspection Scope
                                                                   conformance, the robot must infer the discrete association µ bt .
  We represent the structured specification as                        The robot interacts with the part through the action set
                  S = (C, F , Rall , D, A, Ψ),               (1)          at ∈ {LOOK, REORIENT, SCAN, FINISH / SORT}.            (4)
where C is a finite vocabulary of specification-declared task      L OOK identifies xt and checks (3); REORIENT changes the
concepts and their expansions to leaf requirements; F contains     support-stable configuration through a flip, roll, turn, or re-
surface-region identifiers; Rall is the universe of inspectable    grasp; and SCAN acquires data from F scan (xt ). F INISH / SORT
leaf requirements; and D, A, and Ψ define datum semantics,         is permitted only after report and decision generation. In-
evidence-admissibility predicates, and conformance logic. Re-      spection is therefore active because required evidence may
gions are general inspectable patches, with face used only for     span configurations, while an incorrect reorientation must not
naturally face-like regions. Leaf requirements may represent       silently corrupt the decision.
geometric characteristics, surface conditions, or inter-feature
and inter-region relations. The specification declares their       C. Evidence and Coverage
dependencies, nominal values, tolerances, datums, topology,           The robot accumulates an evidence memory Mt =
admissibility rules, and decision logic, but not which concepts    {e1 , . . . , et }. A feature-level evidence record is represented
a particular production decision requests. Let                     as
   C ∗ = ρ∗ (I, S) ⊆ C,     R∗ = ExpandS (C ∗ ) ⊆ Rall       (2)                                e = (br, qb, b, ℓ),               (5)
                                                                   where rb is the associated requirement, qb the measured quantity,
denote the ground-truth task concepts and induced leaf-
                                                                   b ∈ {0, 1} its admissibility, and ℓ its traceability metadata and
requirement scope. ExpandS follows only dependencies de-
                                                                   diagnostics. b is not a conformance decision: b = 1 only when
clared in S; for example, an assembly-readiness concept may
                                                                   the evidence satisfies the requirement-specific conditions in A,
expand to requirements for a locating interface, mounting pat-
                                                                   including feature coverage, boundary validity, point density,
tern, and supporting surface. Full conformance is the special
                                                                   and absence of truncation. Records with b = 0 cannot support
case R∗ = Rall . Task specification therefore changes the
                                                                   PASS. ℓ retains the scan identifier, physical and specification
required scope, not its completeness: every requirement in
                                                                   regions, acquisition time, and failed conditions.
R∗ still needs admissible evidence. At execution time, the
                                                                      Let e |= r denote that an evidence record contains the
robot estimates Cb from I and S and deterministically obtains
 b = ExpandS (C).b An omission R∗ ⊈ R                              measurements required by r and originates from the physical
R                                          b is safety relevant,
                                                                   surface region or regions correctly associated with the spec-
whereas extra requirements increase cost without directly caus-
                                                                   ification regions required by r. We define complete evidence
ing a false accept. S is a machine-interpretable representation
                                                                   coverage as
of drawing or semantic PMI inspection semantics, using the
subset of ASME Y14.5 datum and GD&T constructs supported           Cov(Mt , R) = 1 ⇐⇒ ∀r ∈ R, ∃e ∈ Mt : b(e) = 1 ∧ e |= r.
by single-sided line-profile acquisition [37].                                                                         (6)
                                                                                                                                 5



This ground-truth definition uses the latent correspondence µ∗ ;      Here, PFA is the joint false-accept probability over all
runtime coverage instead uses µbt . PASS requires complete esti-    episodes. Let πNP = Pr(y ∗ = NO-PASS). The corresponding
mated coverage of R,b even after one nonconformance is found.       conditional false-accept probability satisfies
Missing or inadmissible evidence drives further acquisition or,
after recovery is exhausted, an unresolved outcome rather than                          y = PASS | y ∗ = NO-PASS) .
                                                                           PFA = πNP Pr(b
measured part nonconformance.                                         A false accept has three sources. First, the inferred scope
                                                                    may omit a requirement:
D. Measurement-Steered Acquisition and Operational Out-                           G = {R∗ ⊈ R},
                                                                                            b           γ = Pr(G).           (13)
comes
   Evidence acquisition follows deficits in Mt rather than a        Second, let Df denote the episode-level event that at least
fixed sensing sequence. The uncovered requirements are              one wrong physical-to-specification association supporting
          n                                        o                required region f is admitted during the episode, and let
    Ut = r ∈ R  b ∄e ∈ Mt : b(e) = 1 ∧ e |=µb r ,
                                                t
                                                         (7)        δ = maxf Pr(Df ). Third, let Ar denote the episode-level
                                                                    event that, under correct scope and correspondence, a truly
where e |=µbt r denotes runtime support under the estimated         nonconforming requirement r ∈ R∗ is evaluated from admitted
correspondence. Each scan produces a candidate record and           evidence and assigned PASS through erroneous evidence ad-
diagnostic                                                          mission, numerical measurement, or conformance comparison.
            dt = Diagnose(et , S),                                  Let α = maxr Pr(Ar ). If only per-attempt error rates are
                                                                    available, all authorized attempts that can support a require-
            dt ∈ Ddiag ,
                                                              (8)   ment during the episode must be included in the corresponding
         Ddiag = {ADMITTED, REACQUIRE,                              union bound. Let               [
                  CHANGE - ACCESS, UNRESOLVED}.                                             FR =       F(r)                  (14)
                                                                                                 r∈R∗
These outcomes distinguish admitted evidence, local reacqui-
sition, a required change of access, and exhausted recovery.        be the required specification regions, where F(r) gives the
   The subsequent action is selected from the current corre-        regions on which r depends. Because PASS requires complete
spondence and evidence state,                                       evidence for R,
                                                                                  b a false accept must contain a scope omission,
                                                                    accepted correspondence error, or requirement-level metrolog-
                                     bt , Mt , Ut , dt ) .
           at+1 = πact (I, S, o0:t , µ                        (9)   ical misclassification. Hence,
                                                                                X               X
The process is measurement-steered when an evidence deficit         PFA ≤ γ +         Pr(Df ) +     Pr(Ar ) ≤ γ + |FR |δ + |R∗ |α.
or failed admissibility condition changes the next physical                    f ∈FR           r∈R∗
action. R EACQUIRE adjusts acquisition in the current con-                                                                   (15)
figuration, whereas CHANGE - ACCESS reorients the part to              Equation (15) is an auditable risk contract that does not
expose a missing feature, support, or datum and requires            require an independence assumption, rather than an uncon-
independent verification before scanning. Steering is evidence-     ditional guarantee. Its terms are separately estimable from
driven rather than value-driven: an admitted out-of-tolerance       annotated scopes, correspondence ground truth, and traceable
result is retained as nonconformance, not reacquired. The           metrology ground truth, allowing the resulting bound to be
formulation leaves πact and the access executor unspecified.        compared with the observed end-to-end false-accept rate. Mea-
   For complete evidence, the evaluator applies the datum           surement steering governs recovery and efficiency, whereas
semantics, deterministic tests, and verdict rule Ψ to produce       the scope, correspondence, admissibility, coverage, and con-
report Eb and conformance verdict                                   formance gates determine whether the available evidence can
                                                                    support PASS.
                 ybconf ∈ {PASS, NO-PASS},                   (10)
defined only under complete estimated coverage. The opera-                                  IV. M ETHOD
tional outcome is                                                   A. System Overview
         yb ∈ {PASS, NO-PASS, UNRESOLVED}.                   (11)      The framework closes semantic planning and physical in-
                                                                    teraction around deterministic evidence diagnostics. Fig. 2
PASS and NO - PASS are supported ybconf decisions; UNRE -           summarizes its task manager, two heterogeneous experts,
SOLVED  denotes exhausted recovery with incomplete evi-             shared inspection state, and deterministic evidence gates.
dence.                                                              The task manager grounds the instruction to specification-
                                                                    declared concepts, expands them into leaf requirements, and
E. Auditable False-Accept Risk                                      routes observation, measurement, and physical-access subtasks
   A false accept releases PASS when the task-induced ground-       from the current correspondence and evidence state. The
truth verdict is NO-PASS. Let y ∗ be the result of applying S       manipulation expert exposes two inspection-time atomic skills:
                                                                    LOOK executes a pre-calibrated camera-view action, while
to ground-truth evidence for R∗ :
                                                                    REORIENT uses a VLA policy to realize contact-rich changes
                  y = PASS ∧ y ∗ = NO-PASS] .
         PFA = Pr[b                                          (12)   of physical access. The same expert performs final sorting
                                                                                                                                                       6



                                                                                                              Conformance
                      Observation
                                                                                                               Evaluator
                      Instruction
                  “Verify the pedestal is
                   ready for assembly.”              Specification                Coverage
                                                     Constrained                   Audit
                     Specification                  Task Manager                                       Pass         No-Pass      Unresolved



               Measurement Expert                                                                         Manipulation Expert




               Acquire             Compute                                                                Execute              Execute
             Calibrated            geometric                                                             calibrated           reorient /
             line profiles         quantities                                                              views                 sort



                   Admissibility Gate                                                                      Correspondence Gate
                 admissible evidence only                                                               verified physical        spec region



                                                            Shared Inspection State
                                      Evidence Memory                                         Surface Correspondence
                          measurement . provenance . admissibility                       physical region        specification region


Fig. 2. Overview of our framework. The specification-constrained task manager coordinates a manipulation expert and a measurement expert through shared
Surface Correspondence and Evidence Memory. The manipulation expert exposes three atomic skills: pre-calibrated LOOK, VLA-based REORIENT, and VLA-
based SORT. Each reorientation is independently verified by LOOK and the correspondence gate before scanning. The measurement expert converts calibrated
profiles into admissible geometric evidence, while failed acquisitions trigger REACQUIRE. Complete coverage enables deterministic conformance evaluation:
a supported PASS or NO - PASS verdict triggers SORT, whereas exhausted execution or reacquisition budgets produce UNRESOLVED and manual review.



after a verdict is authorized. The measurement expert converts                triggers REACQUIRE in the current configuration. The loop
calibrated laser profiles into feature-level geometric quantities             terminates with a supported conformance verdict only when
and structured admissibility diagnostics. The components com-                 every requirement in Rb has admissible evidence; exhaustion
municate through a surface correspondence table, which asso-                  of the applicable execution or reacquisition budget produces
ciates observed physical regions with task-specified regions,                 an UNRESOLVED operational outcome and routes the part to
and an evidence memory, which stores admitted records and                     manual review.
their acquisition provenance; the diagnostic status of every
attempted acquisition is retained in the traceability log.

   Given an instruction I, a structured specification S, and
an initial observation o0 , the task manager first produces a                    This organization aligns the runtime interfaces with the
specification-constrained scope R b and establishes the initial               false-accept decomposition in Eq. (15). Scope grounding is the
surface correspondence from calibrated camera observations.                   component that can incur omission event G; accepted physical-
It then dispatches pose-grounded subtasks according to R,      b              to-specification associations can incur correspondence events
the accepted configuration, uncovered requirements, and the                   Df ; and evidence acquisition, admission, and conformance
evidence memory. Every reorientation is followed by a corre-                  evaluation can incur requirement-level events Ar . Measure-
spondence check before the new configuration can authorize a                  ment steering governs local reacquisition and coverage-driven
scan, and every scan is subjected to deterministic acquisition,               progression, while the scope, correspondence, admissibility,
datum, association, fit, and admissibility checks before its                  coverage, and conformance gates determine whether the re-
result can support conformance. An admissible result is written               sulting evidence can support PASS. Planning or manipulation
to evidence memory. If the next uncovered requirement lies on                 failures exposed by runtime verification, or reflected in failed
a different surface, the manager issues CHANGE - ACCESS as a                  evidence admission or coverage, may increase execution cost
normal progression action and converts it into a VLA reorien-                 or produce UNRESOLVED, but do not silently propagate into
tation subgoal. A locally recoverable acquisition failure instead             the conformance path.
                                                                                                                                        7



B. Specification-Constrained Task Manager                            is schema-validated semantic dispatch, not token-level con-
   The task manager converts the inspection instruction into         strained decoding: the VLM generates a structured proposal,
an explicit evidence-acquisition contract. The structured spec-      which is parsed and rejected or retried if validation fails.
ification in Eq. (1) provides a finite vocabulary of feature,           Evidence coverage is audited deterministically after R    b is
group, functional-role, surface-region, datum, requirement,          fixed. For every r ∈ R, the manager queries Mt for admissible
                                                                                          b
and verdict-rule identifiers. A VLM first grounds the instruc-       records associated with r and every task-specified region on
tion to a set of task concepts C,b after which a deterministic       which it depends. Admitted records update Ut , while rejected
specification expansion produces the leaf requirements that          acquisitions update dt ; together they determine the next admis-
must be evidenced,                                                   sible action through Eq. (18). Detecting one nonconforming re-
                                                                     quirement does not stop acquisition of the remaining evidence.
        Cb = gθ (I, S),       b = ExpandS (C)
                              R            b ⊆ Rall .        (16)    Natural-language interpretation is therefore isolated in gθ ,
                                                                     while task expansion, action typing, action legality, evidence
Here, gθ may select only identifiers explicitly declared in
                                                                     coverage, and termination remain reproducible operations over
S; schema validation rejects malformed or unknown outputs.
                                                                     S and Mt .
ExpandS then resolves a requested feature, group, or func-
tional role into its declared leaf evidence scope, surface de-
pendencies, cross-feature relations, and datum dependencies.         C. Active Surface Correspondence
Thus, a group name is a compact task instruction rather                 Surface correspondence bridges task-specified regions and
than an implicit source of new evidence: every resulting             the physical geometry from which evidence is acquired. A
requirement and dependency is traceable to an explicit entry         region may be a surface patch, an end region, an arm, a
in S. The grounding VLM neither reads nor edits nominal              tread, a riser, or a member of a multi-region relation, while
values and tolerances; downstream deterministic acquisition          the part arrives in an unknown configuration from a finite
and conformance modules consume them directly from S.                support-stable set Xc . A scan can therefore be numerically
An omitted valid task concept remains a scope error and is           accurate yet support the wrong requirement if its physical
measured by γ.                                                       source is assigned to the wrong region. Fig. 3 summarizes
   The manager maintains the inspection state                        the initial construction of this association. Each x ∈ Xc
                                                                     jointly encodes support contact, discrete orientation class,
              zt = (R,
                    b x     bt , Mt , Ut , dt , Brem
                       bt , µ                    t   ),      (17)    physically scannable regions, and a physical-to-specification
where x bt ∈ Xc ∪{⊥} is the accepted support-stable configura-       region assignment.
tion, µbt is the current surface correspondence table, Mt is the        The first stage determines which reusable LOOK skills are
evidence memory, Ut is the uncovered requirement set, dt is          required before any image is acquired. For each supported
the latest structured measurement diagnostic, and Brem     stores    geometry family c and inspection zone z, we define a finite
                                                       t                                   adm
the remaining execution and reacquisition budgets. Before the        admissible library Vc,z     = {v1 , . . . , vK }. Each vi couples an
first scan, dt = ∅; thereafter it stores the most recent outcome     inspection-zone-calibrated wrist-camera pose with a collision-
in Eq. (8). A deterministic action router converts the inspection    free robot motion and a designated physical target region that
state into a typed next-action request,                              is visually dominant in the acquired image. This library is
                                                                     calibrated once and reused across specification variants of the
           gtnext = Route(dt , Ut , x    bt , Brem
                                    bt , µ     t   , S) .    (18)    same geometry family.
                                                                        For a particular part specification S, the compiler enumer-
The request specifies an admissible action class, candidate
                                                                     ates the finite support-stable configuration set Xc . It constructs
target set, and access or acquisition constraints. It may rep-
                                                                     each specification-region appearance signature from the de-
resent normal coverage progression or diagnostic recovery. A
                                                                     clared geometry and visible features, including feature type,
VLM then reads a serialization of the state and next-action
                                                                     count, and approximate layout. The family model separately
request and proposes a semantic action, while a deterministic
                                                                     supplies view-to-region visibility, adjacency and opposite rela-
dispatcher checks and instantiates it:
                                                                     tions, handedness, and specification-declared equivalence. Let
               at = πθ serialize(zt , S, gtnext ) ,
                                                   
               e                                                     ΣV (x; S) be the joint region signature predicted when con-
                                                          (19)       figuration x is observed using LOOK subset V. The compiler
               at = Dispatch(e at ; zt , S, gtnext ).
                                                                     selects
A REORIENT proposal names the task-specified regions that
                                                                                V ∗ (S) = arg min |V|
should become scannable and the access constraints that must                                   adm
                                                                                          V⊆Vc,z                                     (20)
be satisfied; a SCAN proposal names a verified region and
                                                                                 s.t. ΣV (x; S) ̸= ΣV (x′ ; S), ∀x ̸∼S x′ .
the requirement identifiers assigned to it. For REACQUIRE,
the router deterministically restricts dispatch to a revised         where x ∼S x′ denotes configurations that are inspection-
acquisition in the current configuration. For CHANGE - ACCESS,       equivalent under S. Thus, LOOK skills are calibrated at the
it restricts dispatch to a reorientation that exposes the next       geometry-family and inspection-zone level, but the minimum
uncovered task region. The dispatcher accepts a proposal only        subset is compiled for the feature distribution of the particular
when all identifiers exist in S, the requested action type agrees    part. Different specifications from the same family may there-
with gtnext , the required surface dependencies agree with µ  bt ,   fore require different LOOK subsets. In the cube example in
and the action is legal in the runtime state machine. This           Fig. 3, Step 1, one upper LOOK is consistent with several yaw
                                                                                                                                                                           8



                Compile the minimum LOOK set                                            Acquire per-view region evidence                   Build correspondence
 Part-specific SpecIR      Geometry Family             LOOK Skill Library                  Calibrated Look execution                       Legal configurations
                                                              v4                         Look (v1)             Look (v2)
   f2                                         …                                                                                                                      …
                                                       v3              v5
  f3                f1
                                                  v2                                                                                       Configuration ranking
                                                                            v6                                                       x1
  f1    four holes                                                                                                                   x2
  f2    two holes                             …
  f3    slot+two holes                                 v1              v7
          …                                                                             Wrist RGB    SAM3 crop         Score         Confidence and consistency gate
                           x1     x2     x3                      …
                                                                                                                       f3 0.84
                                Look compiler                                     v1                                   f5 0.11        score         margin consistency

         One LOOK {L1}                             Add LOOK {L2}
                                                                                                                        …
                                                                                                                       f1 0.02
                                                                                                                                                             Accepted
           Top LOOK                       Top LOOK +             Left LOOK                                                                                 configuration
                                                                                                                       f1 0.76
                                                                       …          v2                                   f2 0.13             Correspondence Table
                            …
                                                                                                                        …
                                                                                                                       f6 0.06
                                                                                                                                      Physical region Spec region
  Ambiguous configurations             Unique configuration remains                                                                            p2              f1
                                                                                              Look (v1)   P1      f3
              Minimum LOOK set = {L1, L2}                    +                                            P2      f1                           p3              f2
                                                                                              Look (v2)
                                                                                                                                                          …

Fig. 3. Specification-driven construction of the surface-correspondence table. Step 1: Minimum LOOK-set compilation. Given the part specification and its
geometry-family LOOK library, the compiler selects the smallest subset that separates all non-equivalent stable configurations; in the cube example, one upper
LOOK is ambiguous, whereas upper and left LOOKs identify one configuration. Step 2: Per-view region evidence acquisition. The robot executes the selected
calibrated LOOKs, SAM3 [38] crops the workpiece, and the VLM scores the candidate specification regions. Step 3: Correspondence construction. The
per-view scores rank the legal configurations. If the best candidate passes the score, top-two-margin, and anchor/topology gates, its physical-to-specification
assignment is released as µ
                          bt ; otherwise, no table is produced.


                                                                                                                                                    (1)
hypotheses; adding the left LOOK separates them and leaves                                configurations. The system accepts x
                                                                                                                             bt = xt                      only if
one legal configuration.                                                                                                                  
                                                                                                                                     (1)
    As shown in Fig. 3, Step 2, for every selected LOOK skill                                                              st xt        ≥ ηs ,
vi ∈ V ∗ (S), the manipulation expert executes the correspond-                                                   
                                                                                                                   (1)
                                                                                                                             
                                                                                                                                  (2)
                                                                                                                                      
ing pre-calibrated motion and acquires wrist-camera image oi .                                                 st xt     − s t xt       ≥ ηm ,                        (23)
SAM3 grounds the workpiece and produces the image crop
                                                                                                                                     
                                                                                                                              (1)
                                                                                                                        At xt ; S = 1,
ci , after which the VLM compares ci with the specification-
derived description dS (f ) of every region f ∈ F:
                                                                                          where At is a deterministic anchor and topology-consistency
                                                                                          check. In the cube implementation, for example, it rejects a
                         ci = Crop(oi , SAM3(oi , pc )) ,                                 configuration that conflicts with a sufficiently strong upper-
                                                                                 (21)
                mi (f ) = VLMMatch(ci , dS (f )) ,                                        region anchor; the finite configuration model already enforces
                                                                                          opposite, adjacency, handedness, and exclusivity constraints.
where pc is the object-family prompt and mi (f ) ∈ [0, 1]                                 The specification-compiled LOOK set is executed once for
is a region-matching score. The VLM therefore provides                                    the correspondence decision. If any gate fails, x bt = ⊥, no
per-view semantic evidence; it neither outputs a complete                                 correspondence table is released, and the runtime abstains
correspondence table nor selects among arbitrary poses.                                   rather than acquiring an additional LOOK or guessing.
                                                                                             Every accepted configuration defines a complete physical-
   As shown in Fig. 3, Step 3, the code constructs the table
                                                                                          to-specification assignment Mx . The runtime table is therefore
by enumerating every legal x ∈ Xc . Let Fi (x) ⊆ F be the
specification region or region set predicted at observation slot i
under x. Each configuration receives the normalized weighted                                               µ
                                                                                                           bt (p) = Mxbt (p),              p ∈ F phys ,               (24)
score
                          X                                                               with observed entries marked as image-supported and un-
                               wi max mi (f )                                             observed entries marked as configuration-derived. The latter
                                              f ∈Fi (x)                                   are completed only through the accepted finite configuration
                                vi ∈Vt
                  st (x) =                X                      ,               (22)     and relations explicitly encoded by S. Globally symmetric
                                                   wi
                                         vi ∈Vt
                                                                                          configurations need only be resolved up to specification-
                                                                                          declared equivalence when all members induce the same
                                                                                          required evidence. Every admitted measurement record stores
              adm
where Vt ⊆ Vc,z     is the set of executed LOOK skills and                                the physical source region, associated specification region,
                                                     (1)
wi is a fixed reliability weight for skill vi . Let xt and                                configuration identifier, observation sources, and gate scores
 (2)
xt be the highest- and second-highest-scoring non-equivalent                              in traceability field ℓ.
                                                                                                                                                                                                         9


                                                                                                               Instruction                Spec grounding           Select Z settings   Acquire profile
                                                +Z
                                                       12.5%
                                                                                                                                                                     window size
                                                                                                              (a) cube                                                   = 1/8
                                                                                    Measurement                                                                     center position
                                                                                      Window         “Verify the position of the    Front: {FH1, FH2, FH3, FH4}          = 21%
                                                           50%                                        four-hole bolt pattern”       Face height: 50 mm            sampling frequency
                                                                                                                                    Feature depth: 6 ± 0.1mm            = 4kHz
                                                                                       Center
                                                                                      Position
                                                                                                                                                                     window size
                                                       87.5%                                                (b) bracket                                                  = 1/8
                                                -Z                                                                                                                  center position
                                                                                                      “Verify the base groove       Base-Top: {BG}                       = 77%
                                      Measurement Window Max            Sampling Frequency (fmax)   size and floor parallelism”     Face height: 3 mm             sampling frequency
                                        FULL         1/2         1/4          1/8        1/16                                       Feature depth: 1.5 ± 0.1mm          = 4kHz
 Reference
 Distance
                                                                                                                                                                     window size
                                                                                                          (c) stepped block                                              = 1/8
                                                                                                                                                                    center position
                                                                                                     “Inspect the counterbore       High-Tread: {CB}                     = 21%
             211 mm                                                                                     on the high tread”          Face height: 50 mm            sampling frequency
                                       68 mm    34 mm            17 mm       8.5 mm     4.25 mm                                     Feature depth: 6 ± 0.2mm            = 4kHz
             245 mm                  fmax
                      Measurement                                                                                                                                    window size
                                       500Hz     1kHz            2kHz         4kHz        8kHz            (d) stepped block
             279 mm      Range                                                                                                                                           = 1/2
                                      Smaller Window       Higher Max Sampling Frequency (fmax)                                                                     center position
                                                                                                     “Measure the step height”     SH: {High-Tread, Low-Tread}           = 39%
                                                                                                                                   Face height: 50 mm             sampling frequency
                                                                                                                                   Feature depth: 25mm ± 0.2mm          = 1kHz
Fig. 4. Measurement-range configuration of the Keyence LJ-X8200 laser
profiler. The measurement window can be shifted along the Z-axis by
adjusting its center position and reduced from the full 68 mm range to 34, 17,                      Fig. 5.     Examples of specification-driven vertical measurement-window
8.5, or 4.25 mm. Reducing the measurement range increases the maximum                               selection for different objects and inspection requests. The instruction is
sampling frequency fmax from 500 Hz to 8 kHz.                                                       grounded to the required surface, feature depth or height, and tolerance before
                                                                                                    the expert selects the measurement Z range and center position. The displayed
                                                                                                    sampling frequency is the maximum frequency fmax (Rf ) supported by the
                                                                                                    selected Z range, rather than the commanded scan frequency. (a) The cube bolt
D. Manipulation Expert                                                                              pattern uses a narrow range centered near the raised surface. (b) The shallow
                                                                                                    groove on the bracket uses the same range size but a shifted center because
   The manipulation expert exposes three atomic skills: LOOK,                                       its base surface is at a different height. (c) The counterbore on the high tread
                                                                                                    again uses a narrow, surface-centered range. (d) Step-height inspection must
REORIENT, and SORT . L OOK executes a pre-calibrated camera                                         contain both height levels, requiring a wider range, an intermediate center, and
action v ∈ V ∗ (S) and returns an observation for surface-                                          consequently a lower maximum sampling frequency. The acquired profiles
correspondence estimation. The other two skills are imple-                                          confirm that the task-required geometry lies within the configured window.
mented by a VLA policy. R EORIENT changes physical access
through geometry-dependent grasp, flip or roll, regrasp, and
                                                                                                       If the observed scannable region is not the requested target
placement actions. S ORT performs the final pick-and-place
                                                                                                    or the compiled LOOK set otherwise fails the correspondence
into the pass or no-pass region, but is enabled only after the
                                                                                                    gate, the candidate update is not committed and no scan is
conformance evaluator authorizes a verdict. This interface lets
                                                                                                    authorized. The manager may issue another legal REORIENT
the task manager select the semantic action and target while
                                                                                                    attempt within the execution budget; otherwise the episode be-
leaving contact-rich execution to the learned policy.
                                                                                                    comes UNRESOLVED and the part is routed to manual review.
   When an uncovered requirement lies outside the currently
                                                                                                    A timeout, dropped part, invalid placement, or unintended
scannable region set, the task manager issues CHANGE -
                                                                                                    reorientation is likewise handled as an unverified transition
ACCESS with the target specification region and its access
                                                                                                    and cannot directly produce measurement evidence.
constraints. The manipulation expert serializes this request as
                                                                                                       This interface separates correctness from action efficiency.
a language-conditioned VLA subgoal and invokes REORIENT;
                                                                                                    A poor plan, failed grasp, or unintended flip increases the
the target is determined by the uncovered evidence scope
                                                                                                    number of observations and reorientation attempts, but affects
rather than by a generic manipulation objective. We use real-
                                                                                                    false-accept risk only if an incorrect correspondence also
time chunking (RTC) for continuous VLA execution [39], with
                                                                                                    passes the mandatory post-action gate, which is counted by δ.
a calibrated per-skill time limit after which control returns to
                                                                                                    The VLA may therefore flexibly realize REORIENT, while the
the task manager [40]. These are execution details rather than
                                                                                                    calibrated LOOK skill and correspondence gate independently
success criteria: the outcome of a VLA invocation is accepted
                                                                                                    determine whether the resulting configuration may support
only through the independent checks below.
                                                                                                    measurement evidence.
   The VLA-based REORIENT skill is treated as an unverified
physical transition until its outcome is observed. After each
invocation, the task manager applies the commanded reori-                                           E. Measurement Expert
entation to the previously accepted configuration and corre-                                           The measurement expert maps a verified scannable-region
spondence, yielding a candidate post-reorientation state. The                                       request (f, Rf ) to traceable numerical evidence. Here, f is a
manipulation expert then executes the specification-compiled                                        task-specified region and Rf ⊆ R   b is the set of requirements
LOOK skills. The candidate is committed as the updated                                              assigned to it. Multi-region requirements are decomposed into
configuration x bt+1 and correspondence table µ   bt+1 only if                                      linked acquisitions whose partial evidence is retained until
these observations pass the surface-correspondence gate and                                         all referenced regions are covered. For each r ∈ Rf , a
verify that the requested region f belongs to the resulting                                         requirement-type-specific operator produces
set of scannable specification regions. Only then is a scan
                                                                                                                              qbr = htype(r) (Hf , DRFr , j ∗ (r)) ,                            (25)
of f authorized. Thus, independent verification is realized by
composing the two skills as REORIENT→LOOK, rather than                                              where Hf is the registered height data, DRFr is the datum
by trusting the VLA-predicted outcome.                                                              reference frame required by r, and j ∗ (r) is the deterministi-
                                                                                                                                                              10



  (a) Specification-driven acquisition                (b) Calibrated height map                  (c) Tilt normalization & candidate extraction


                             SAM3
                              ROI




  lead-out         scan      lead-in
    1. Feature        2. Z     3. Z
   Specification     range    window




     Expected
   depth/height
    ± tolerance

    (d) DRF construction & Feature association                    (e) Operator library                     (f) Evidence admission and recovery
                                      C02+C03       C01         diameter     depth      groove
  Datum A                           (counterbore) (groove)
                                                                                                         Measurement           Evidence         Admitted
                                                                                                            record             usable?         measurement
                                                                position coaxiality flatness
                                           C04
                                       (blind hole)                 .           .                                               Targeted
 Datum B                  Datum C                                             …                                                 recovery



Fig. 6. Measurement Expert pipeline from a verified inspection request to admissible evidence. (a) The grounded specification defines the feature region,
lateral scan path, and vertical measurement window. (b) Calibrated laser profiles are registered into a height map. (c) Host-surface tilt is normalized before
geometric candidates are extracted. (d) The datum reference frame is constructed and candidates are deterministically associated with the requested specification
features. (e) A requirement-specific operator computes the reported geometric quantity. (f) Deterministic admissibility predicates either admit the measurement
to Evidence Memory or trigger targeted reacquisition; an inadmissible record cannot support conformance.



cally associated feature or supporting surface. As summarized                       discrete ranges {Rk }, the expert selects
in Fig. 6, the expert first configures and acquires a calibrated                                       n                       o
scan, reconstructs geometry in the declared datum frame,                                     Rf = min Rk : Rk ≥ Df+ − Df− + 2mz ,
                                                                                                                                                           (26)
associates candidates without using their conformance values,                                Dfc = (Df− + Df+ )/2,
and applies a deterministic operator and admissibility pred-
icate. It returns the requirement identity, measured quantity,                      and converts Dfc to the device center command after checking
admissibility status, and traceability metadata rather than a                       the device’s center limits. Fig. 5 shows that this rule shifts
free-form interpretation or verdict.                                                the same narrow range across surfaces of different heights
                                                                                    and selects a wider range when both levels of a step must be
                                                                                    observed.
   1) Specification-Driven Acquisition: After the correspon-                           The selected range constrains the maximum profile fre-
dence gate authorizes region f , SAM3 localizes its lateral ac-                     quency fmax (Rf ). Given the commanded sweep pitch pv , the
quisition window in the inspection-camera image. The highest-                       expert chooses fs ≤ fmax (Rf ) and sets
confidence mask satisfying calibrated safe-region constraints
is selected. The mask extent, enlarged by a fixed margin,                                            vs = fs pv ,        fs ≤ fmax (Rf ),                  (27)
is mapped through a calibrated planar homography to the                             subject also to the robot-speed limit. The transverse profiler
measurement-arm plane and projected onto the profiler’s cali-                       pitch and pv define the sampling grid and are validated before
brated sweep axis. Lead-in and lead-out segments ensure that                        motion; an infeasible configuration is rejected rather than
the requested interval is traversed at constant speed, and the                      treated as a low-quality measurement afterward. Streamed
entire path must remain inside the calibrated workspace and                         profiles are stacked into a registered height map Hf ∈
inspection safe region.                                                             (R ∪ {∅})Nv ×Nu , where ∅ denotes a missing or out-of-range
                                                                                    return. Each map retains the path, profiler pose, calibration
   The lateral path is coupled with a specification-driven verti-                   identifier, acquisition windows and settings, timestamp, and
cal window. Let Ds = DT −ho be the exposed support-surface                          requested region.
distance, obtained from the calibrated scanner-to-table distance                       2) Calibrated Geometric Reconstruction: Residual support-
DT and the specified or observed object height ho . The                             surface tilt is removed before height-level decomposition and
requirement defines an allowable feature envelope [Df− , Df+ ],                     candidate extraction. A robust RANSAC plane is fitted to
enlarged by its tolerance and acquisition margin mz so that                         spatially distributed support samples and subtracted from valid
a nonconforming feature is not clipped. From the profiler’s                         cells of Hf ; missing returns remain undefined. The normalized
                                                                                                                                                11


                                                                       p
map is used to separate height populations, while the fitted                (ui − uc )2 + (vi − vc )2 − r, a circular opening is measured
plane, inlier support, and residual statistics are stored with the     by                                      X
scan. Insufficient support or excessive residual error makes                       (b
                                                                                    uc , vbc , rb) = arg min          ρ(ηi (uc , vc , r)) ,
the dependent evidence inadmissible and requests a larger                                          uc ,vc ,r
                                                                                                               i∈Cf                           (30)
verified support patch. Measurements are then expressed in the                           diam
                                                                                        qb      = 2b
                                                                                                   r.
datum reference frame (DRF) declared by each requirement
rather than aligned freely to nominal geometry. Given the              and a recessed-feature depth is the median host-to-feature
ordered datum definition ∆r , a deterministic constructor fits         separation
its primitives in precedence order and maps calibrated samples          qbdepth = Q0.50 ({πA (ui , vi ) − wi : (ui , vi , wi ) ∈ Ωf }) . (31)
pi into datum coordinates:
                                                                       A through opening reports no bottom depth. Counterbores
 DRFr = Φ∆r (Hf , S),            (ui , vi , wi )T = DRFr (pi ). (28)   apply the same two operators to nested contours and observed
                                                                       levels, yielding separate outer/inner diameters and seat/inner
A planar primary datum supplies the origin and normal, a
                                                                       depths. Grooves use quantile extents along the major and
projected secondary direction fixes the in-plane axes, and a
                                                                       minor footprint axes for length and width and Eq. (31) for
tertiary datum fixes the remaining translation; edge and axis
                                                                       depth; step height is the absolute median offset between two
datums use their fitted directions with the declared origin
                                                                       support regions in a common DRF.
and clocking constraints. The expert validates point count
                                                                          Form, orientation, and location operators reuse the same
and spread, fit residuals, constrained-degree observability, axis
                                                                       validated geometry. Projected true position is twice the DRF-
consistency, and datum availability before measuring a feature.
                                                                       plane distance between the fitted and basic centers, while
A failed datum check makes all dependent measurements
                                                                       projected counterbore coaxiality is twice the distance between
inadmissible, preventing a plausible fit in an invalid frame
                                                                       the fitted outer and inner centers. Flatness is the robust
from supporting a GD&T result.
                                                                       peak-to-valley band of host-plane residuals, and groove-floor
   3) Deterministic Association and Operator Library: Fea-
                                                                       parallelism is the corresponding height band relative to the
ture association uses task-specified geometry and topology in
                                                                       host plane. These are explicitly defined operational measures
the DRF, not the value of the characteristic being inspected.
                                                                       rather than claims to compute ISO minimum-zone quanti-
Registered scan patches are segmented into candidate sup-
                                                                       ties. Cross-feature consistency and spacing are respectively
porting surfaces, openings, annular recesses, grooves, steps,
                                                                       the absolute difference between like-for-like admitted values
and residual recessed components using height discontinuities,
                                                                       and the Euclidean distance between admitted DRF centers.
connectivity, and their relation to fitted support regions. For an
                                                                       Recessed-defect depth is the largest robust positive-residual
opening, the boundary at which the supporting surface loses
                                                                       depth after designed features, missing returns, and an edge
valid support defines the opening contour; fitting this contour
                                                                       band are excluded. All operators act on calibrated points in
avoids bias from partially observed walls or bottoms.
                                                                       a validated DRF, and relation operators run only after their
   Let ξ j denote the DRF descriptor of candidate j—for
                                                                       constituent records are admitted.
example, a point, axis, contour anchor, or surface-patch
coordinate—and let ξ 0r be the basic descriptor of the speci-          F. Evidence-Coverage Steering and Diagnostic Recovery
fication target referenced by requirement r. The specification
                                                                           A numerical value is admitted only when the acquisition and
also declares the required candidate primitive type ftype(r).
                                                                       fitted geometry support the requested characteristic. Common
The target candidate is selected by
                                                                       gates verify sufficient valid-return density, calibration and
                j ∗ (r) = arg min dr (ξ j , ξ0r )                      safe motion, absence of measurement-range clipping, valid tilt
                             j∈Jf
                                                                       compensation, valid DRF construction, a unique candidate in
                      s.t.    type(j) = ftype(r),              (29)
                                                                       Nr , and bounded primitive-fit residuals. Characteristic-specific
                             ξ j ∈ Nr ,                                gates then test the necessary observable geometry: opening
                                                                       diameter requires adequate arc coverage, radial inliers, contour
where Jf is the set of geometrically valid candidates on region
                                                                       closedness, and no image-boundary contact; depth requires
f , Nr is the association neighborhood declared by S, and dr is
                                                                       valid host and feature samples separated into stable height
a primitive-appropriate spatial distance defined independently
                                                                       populations; a counterbore requires two ordered contours and
of the characteristic under test. For a circular opening on a
                                                                       the requested observed level; groove dimensions require a
planar patch, this reduces to the nearest basic center in (u, v);
                                                                       nontruncated connected footprint and a valid floor fit; step
axis-based relations compare fitted axes. Because lookup does
                                                                       height requires both support regions; projected true position
not use measured depth, diameter, form error, or conformance
                                                                       requires a valid fitted center and every referenced datum;
status, an out-of-tolerance feature is not replaced by a different
                                                                       flatness requires sufficient interior coverage after edge and
candidate merely because the latter is numerically closer to
                                                                       feature exclusion; projected coaxiality requires valid nested-
nominal.
                                                                       circle fits; parallelism requires sufficient floor extent; and
    The operator library evaluates the associated geometry
                                                                       relation operators require every constituent measurement to
using fixed robust losses and quantile levels. Let Cf be an
                                                                       be admitted. For each requirement type, these checks form a
opening contour, Ωf its feature samples, and πA the host
                                                                       deterministic predicate Ar , and the expert sets
plane fitted after excluding designed features, boundaries,
and missing returns. With radial residual ηi (uc , vc , r) =                        br = I[Ar (Hf , DRFr , j ∗ (r), qbr , r) = 1]             (32)
                                                                                                                                     12



and never uses a record with br = 0 to support PASS. Each           without training a classifier or authoring a part-specific inspec-
predicate corresponds to an observable physical or numerical        tion program. Each admitted measurement is appended to Mt
failure that can be reproduced from the stored scan; it is not      together with its acquisition-time correspondence snapshot µ   be ,
a generic model-confidence score. A record with br = 1 pro-         scan identifier, and fit diagnostics; the evaluator then attaches
duces diagnostic ADMITTED; otherwise, the failed predicates         its deterministic requirement status. Let e |=µbe r denote that
and remaining recovery budget determine either REACQUIRE            the record contains the acquisition primitives required by r
or UNRESOLVED.                                                      and that their observed physical regions are associated by µ    be
    Panel (f) of Fig. 6 summarizes targeted acquisition recovery    with every specification region on which r depends. Runtime
at a high level. R EACQUIRE retains the accepted configuration      coverage is complete only if every requirement in R   b has such
and adjusts only the measurement process: boundary contact          an admitted record,
expands the SAM3-derived lateral patch, vertical clipping
shifts the device center command corresponding to Dfc or se-         Cov(M t , R) = 1 ⇐⇒ ∀r ∈ R, ∃e ∈ Mt :
                                                                     d         b              b
lects a larger Rf , excessive missing returns revise the exposure                              b(e) = 1 ∧ rb(e) = r ∧ e |=µbe r.
or measurement window, and a locally unstable tilt or primitive                                                                  (35)
fit requests a larger support patch or repeated acquisition. The    This runtime test uses the estimated correspondence snapshot
revised scan is processed by the same measurement operator          stored with each record and is therefore distinct from the latent
and must pass the same predicate Ar before it can enter             ground-truth coverage criterion used for evaluation. Missing
evidence memory. After evidence for the current surface is          evidence causes continued acquisition or, after recovery is
admitted, the manager recomputes Ut . If requirements remain        exhausted, an unresolved outcome; it is never interpreted as
on another surface, the action router issues CHANGE - ACCESS        evidence of conformance.
as the next planned action, and the dispatcher instantiates the        After coverage is complete, the evaluator applies the spec-
corresponding structured VLA subgoal. The resulting config-         ification rule Ψ to the feature statuses and group relations to
uration must pass the correspondence and scan-authorization         produce ybconf and a complete inspection report; the manager
gates before the next surface is measured. If local reacquisi-      then sets the supported operational outcome yb. The aggre-
tion exhausts its configured budget, the diagnostic becomes         gation is a deterministic program over requirement identifiers
UNRESOLVED . Every attempt, including rejected attempts,            and cannot alter the underlying measurements. Only then does
is appended to the traceability log, while only ADMITTED            the manager authorize the manipulation expert to sort the part.
records contribute to evidence coverage.                            Hence a released PASS must have traversed three explicit gates:
    Recovery is therefore evidence-driven rather than value-        the task requirement must be present in R, b its evidence must
driven. Because the sampling tuple is validated before motion,      pass surface-correspondence and admissibility checks, and its
insufficient nominal sampling density is not a normal post-         deterministic status must satisfy the specification.
acquisition recovery case. Likewise, an admitted measurement
outside the specification limit is retained as measured non-
conformance and does not trigger reacquisition or change the                          V. E XPERIMENTAL S ETUP
planned surface progression. Reacquisition is requested only
                                                                    A. Hardware Platform
for inadmissible evidence; after the configured recovery budget
is exhausted, the system records incomplete evidence, returns          The platform (Fig. 7) consists of two six-degree-of-freedom
UNRESOLVED , routes the part to manual review, and cannot           UFACTORY xArm 6 manipulators on a shared optical bread-
release it as PASS.                                                 board, with overlapping workspaces over a central inspection
                                                                    region. Their heterogeneous end-effectors realize the dual
G. Specification-Driven Conformance Evaluation                      heterogeneous experts design in hardware. The measurement
                                                                    arm carries a Keyence LJ-X8200 laser line profiler on a 3D-
   Conformance evaluation is deliberately separated from task       printed bracket, driven by a Keyence LJ-X8000A controller.
planning so that a VLM proposal cannot turn incomplete or           The profiler delivers 1 µm Z-axis repeatability and a 25 µm X-
ambiguous evidence into a PASS verdict. After the evidence-         axis profile interval over 3200 points per profile at a 245 mm
admissibility predicates have passed, a bilateral dimensional       standoff. This arm is hand-eye calibrated and its tooling is
requirement with nominal value qr0 and half-width tolerance         never changed, preserving the calibration throughout each
τr is evaluated by                                                  inspection cycle. The manipulation arm carries a UFACTORY
                         qr − qr0 | ≤ τr ,
                        |b                               (33)       xArm Gripper G2 parallel-jaw gripper and a wrist-mounted
and a nonnegative GD&T characteristic with upper limit τr is        Intel RealSense D435i, and performs all pick, place, flip, and
evaluated by                                                        reorientation actions. A second D435i on a fixed central mast
                       qbr ≤ τr .                      (34)         provides the global top-view observation. The manipulation
                                                                    policy observes both the wrist and top-view cameras; the
Evidence outside the task-specified limit is marked non-            planner and the object-grounding stage use the top-view image
conforming. Missing coverage or inadmissible evidence is            alone. The breadboard defines three regions for the tolerance-
processed by the action router and cannot support a PASS            conditioned sorting task: an inspection zone where the work-
decision. This direct comparison allows a new nominal value         piece is measured, and a pass zone and no-pass zone into
or tolerance to be supplied through the structured specification    which the manipulation arm sorts it by the final judgment.
                                                                                                                                                            13



                                                                                               Level 0        Level 1                   Level 2

                                          Top view camera

         3D-printed                    Xarm 6
          bracket
                                                           Xarm                 Bracket
                                                          gripper
                                        Wrist               G2
                                       camera


                                                                               Cylinder
        Inspection
           Parts

                                 Keyence LJ-X8200
                                                                                  Block
                                                Inspection Zone

         No-Pass Zone                                 Pass Zone

                                                                                Stepped
Fig. 7. Our real-world experiment setup. One XArm 6 carries a Keyence            Block
LJ-X8200 laser line profiler, while the other is equipped with a G2 gripper
and wrist camera for part manipulation and local observation. A fixed top-
view camera provides global workspace observations. Parts are measured in     Fig. 8. Designed 3D-printed benchmark objects across increasing geometric
the inspection zone and subsequently sorted into the pass or no-pass zone.    variation. Four object families, bracket, cylinder, block, and stepped block, are
                                                                              organized into three levels. Level 0 provides the nominal geometries used for
                                                                              manipulation policy training, Level 1 introduces feature-level variation while
B. Implementation Details                                                     largely preserving the overall shape, and Level 2 introduces larger morphology
                                                                              changes, with two variants per family.
   We instantiate the VLM with Qwen3-VL-8B-Instruct [41],
which is used for instruction grounding, semantic action pro-
posal, and visual interpretation in the surface-correspondence
module. The manipulation expert is instantiated with the
π0.5 [42]. A single shared π0.5 policy supports all workpiece
geometries and manipulation skills, with each skill invoked                   Table I. T1 requests a named feature, T2 a surface anomaly
using a distinct language prompt. Robot demonstrations are                    or form check, and T3 a within- or cross-surface relation
collected through a Meta Quest 3 teleoperation interface. For                 or GD&T constraint. T4 aggregates the requirements of a
each workpiece geometry, we define the reorientation skills                   declared interface or part, whereas T5 states a functional
required to transition among its supported stable configu-                    goal whose complete requirement scope must be inferred
rations. For example, the block requires backward-flip and                    from the specification. The object levels represent manufac-
rightward-flip skills, whereas the bracket requires a flip-over               turing progression rather than task difficulty. L0 contains four
skill. We collect 60 teleoperated episodes for every geometry–                feature-free bodies used only to train grasping, reorientation,
skill pair, including each geometry-specific reorientation skill              and placement. L1 adds holes, counterbores, grooves, da-
and the final pick-and-place skill. The demonstrations from                   tums, and functional groups and forms the main inspection
all geometries and skills are pooled to adapt the shared                      benchmark. L2A and L2B further modify global morphology
π0.5 policy using low-rank adaptation (LoRA) [43]. Fine-                      while retaining applicable L1 inspection roles and seman-
tuning is performed for 100,000 optimization steps on a single                tics; all level-specific feature, datum, position, and topology
NVIDIA RTX PRO 6000 Blackwell Workstation Edition GPU.                        changes are declared in the corresponding specification. Thus,
Intermediate checkpoints are evaluated in separate real-robot                 L2 evaluates transfer within a manufacturing lineage, not to
validation trials, and the best-performing checkpoint is frozen               unrelated categories. The real-object study is separate from
before benchmark evaluation.                                                  this hierarchy. Each design has one 3D-printed specimen
                                                                              whose as-built geometry is independently characterized with
C. Benchmark Design                                                           dedicated reference instruments. The resulting mref contains
   The benchmark unit is an inspection episode comprising a                   every inspectable characteristic; robot estimates are compared
workpiece design and specimen, an independently measured                      with these values rather than CAD nominals, and reference
reference vector, a structured specification, a natural-language              verdicts are obtained by applying the structured specifica-
instruction, and an initial stable pose. This unit supports paired            tion to mref . Each task family provides two instructions per
evaluation from identical initial conditions without treating                 object with different evidence scopes. All comparisons use
repeated scans of one specimen as independent manufactured                    frozen episode manifests; repeated executions are treated as
parts.                                                                        repeated measurements, and decision rates are reported over
   The benchmark uses four base geometries—cube, cylinder,                    task–specification pairs rather than independent manufactured
L-bracket, and stepped block—and the five task families in                    specimens.
                                                                                                                                                        14


                                                             TABLE I
       I NSPECTION TASK TAXONOMY AND ITS INDUSTRIAL MOTIVATION . M ANIPULATION DIFFICULTY IS EVALUATED INDEPENDENTLY THROUGH
                                                  REORIENTATION COST AND REGRET.


  Task   Category               Industrial need                                           Required evidence
  T1     Specified feature      Verify a named feature after machining or printing        Measure required characteristic of the requested feature
  T2     Anomaly detection      Protect mating, sealing, bearing, or datum surfaces       Measure damage and form error on the requested surface
  T3     Relation or GD&T       Ensure alignment, interchangeability, and compatibility   Evaluate relations among features, surfaces, and datums
  T4     Composite inspection   Inspect a declared feature group or interface             Aggregate all requirements in the declared group
  T5     Functional goal        Verify an intent-level production goal                    Infer the required scope and collect complete evidence



D. Compared Methods
   We compare FRAME with three alternatives under matched
parts, specifications, instructions, sensors, cameras, and
episode manifests. The autonomous methods additionally
share the robot action interface, frozen VLA manipulation pol-              (a)                                    (b)


icy, post-reorientation observations, laser acquisition interface,
low-level geometric operators, and execution and recovery
budgets; none receives oracle pose, surface correspondence, or
measurement values, and failure to return a valid binary verdict
is recorded as unresolved. Part and Task Specific Inspection                (c)                                    (d)

is a conventional operator-driven workflow in which a human
interprets each part–task request, positions the part, configures          Fig. 9. End-to-end reliability and task completion cost. (a) Paired end-
Keyence regions, tools, and limits, executes the scans, and                to-end success across L1, L2, and CNC parts, where a pair is counted as
                                                                           successful only when both the matched PASS-spec and FAIL-spec episodes
prepares the report; because it is not autonomous, it serves only          are completed correctly. (b) Mean task-to-completion time, measured from
as an engineered task-completion-time reference. Full Part                 task-specific preparation to final report and sorting or unresolved termination.
Exhaustive Inspection uses the shared VLA and automated                    (c) Terminal outcomes on PASS-spec episodes, reported as correct PASS,
                                                                           false reject, and unresolved. (d) Terminal outcomes conditional on FAIL-spec
metrology, admissibility tests, and deterministic comparisons,             episodes, reported as correct FAIL, conditional false accept, and unresolved.
but follows a reusable per-part routine that exposes every                 An episode is unresolved when no valid binary verdict is produced within the
registered surface and scans every registered feature before               common execution and recovery budget and is therefore transferred to manual
                                                                           review.
extracting the requested report, thereby isolating fixed exhaus-
tive acquisition from task-specified acquisition. VLM without
FRAME uses one VLM to select observation, reorientation,
scanning, and measurement actions and to determine com-                    within each part setting, and action, recovery, and timeout
pletion, report, and verdict while retaining the shared VLA,               budgets. An episode succeeds only when valid evidence covers
calibrated observations, laser interface, and geometric fitting            every required characteristic and the requirement statuses,
operators. It removes FRAME’s deterministic specification                  final verdict, report, and sorting action are correct. A pair
expansion, authoritative surface correspondence, requirement-              is successful only when both its PASS-spec and FAIL-spec
specific evidence admission, evidence memory, coverage au-                 episodes succeed. Failure to produce a binary verdict within
dit, and specification-driven conformance evaluator, thereby               the common limits is recorded as unresolved and routed to
testing whether VLM-level reasoning alone can govern the                   manual review; a released verdict based on incomplete or
calibrated inspection stack.                                               incorrectly localized evidence is instead scored as claimed and
                                                                           may become a false reject or false accept.
                       VI. E XPERIMENTS                                       Figure 9(a) shows that FRAME achieves the strongest
                                                                           paired reliability on L1, L2, and CNC parts. The L2 result is
A. Full-System Inspection Performance                                      especially informative because the autonomous methods share
   This experiment evaluates whether FRAME improves end-                   the same reorientation capability and differ primarily in ob-
to-end reliability and efficiency over fixed exhaustive inspec-            servation, recovery, and evidence management. Exhaustive in-
tion and direct VLM control when sensing and manipulation                  spection accumulates failure exposure through task-irrelevant
capabilities are held fixed. We use matched specifications                 operations, whereas direct VLM control lacks authoritative
to prevent success through a fixed verdict. Each test unit                 correspondence and deterministic evidence gates. FRAME
fixes the part, instruction, required scope, and initial config-           limits acquisition to the active scope and releases a verdict
uration, and is executed with both a reference-PASS spec-                  only after verified evidence completes that scope. Consistently,
ification, constructed from independently measured as-built                Fig. 9(c–d) shows more correct terminal outcomes and the
values, and a reference-FAIL specification that changes only a             fewest conditional false accepts among FAIL-spec episodes.
task-relevant conformance boundary. All autonomous methods                 Unresolved FRAME episodes occur when correspondence,
receive the same manifests, specifications, initial observations,          reorientation, or measurement admissibility cannot be estab-
calibrated measurement interfaces, frozen manipulation policy              lished within budget, thereby withholding an unsupported
                                                                                                                                                   15


                                                                                                             TABLE II
                                                                                     LOOK- BASED SURFACE - CORRESPONDENCE PERFORMANCE . B OTH
                                                                                    METHODS RECEIVE THE SAME FIXED LOOK OBSERVATIONS ; FRAME
                                                                                      ADDITIONALLY RESOLVES PER - VIEW VLM SCORES OVER LEGAL
                                                                                    CONFIGURATIONS AND APPLIES THE CONFIDENCE – CONSISTENCY GATE
                                                                                               BEFORE RELEASING A CORRESPONDENCE .



(a)                                                     (b)
                                                                                   Method                 Cand. acc. Wrong rel. Abstain   Rel. acc.
                                                                                                            (%) ↑ / trial (%) ↓ (%)        (%) ↑

Fig. 10.     Metrology validation across representative measurement oper-
ators. (a) Signed bias, mean absolute error (MAE), and 95th-percentile             L1
absolute error (P95) relative to reference measurements for opening di-            VLM w/o FRAME             54.8       45.2        -        -
ameter, depth/surface offset, groove footprint dimensions, projected loca-         VLM w/ FRAME              92.9       2.4        9.5      97.4
tion/coaxiality, and form/relative orientation. The dashed vertical line denotes
zero signed bias. (b) Repeatability standard deviation over repeated measure-      L2
ments for the same operator groups, quantifying scan-to-scan measurement           VLM w/o FRAME             52.4       47.6       -         -
consistency.
                                                                                   VLM w/ FRAME              82.1       3.6       19.0      95.6


verdict rather than releasing a nonconforming part.
                                                                                   feature, or between adjacent surface levels. Groove footprint
   Figure 9(b) shows that FRAME also completes the work-
                                                                                   dimensions denotes the in-plane length and width obtained
flow fastest by avoiding unnecessary surface access, scanning,
                                                                                   from the oriented extent of a segmented groove. Projected
and analysis and stopping when admissible coverage is com-
                                                                                   location/coaxiality denotes datum-referenced feature-center
plete. Exhaustive inspection processes requirements outside
                                                                                   displacement or the relative offset between fitted opening
the requested scope, manual task-specific inspection adds
                                                                                   centers. Finally, form/relative orientation denotes plane-based
interpretation and tool-configuration time, and direct VLM
                                                                                   characteristics, including flatness and parallelism, derived from
control may spend additional actions resolving planning or
                                                                                   fitted surface residuals or relations between fitted planes.
evidence uncertainty. Unresolved autonomous episodes are
                                                                                       Depth and surface-offset estimation provides the strongest
charged the common timeout so that early failure does not
                                                                                   overall metrological performance. This behavior is consistent
appear artificially efficient. Thus, within the supported parts
                                                                                   with the implementation: depth is determined primarily from
and measurement vocabulary, verified task-specific evidence
                                                                                   a robust vertical separation between the reference surface
improves paired reliability, false-accept protection, and com-
                                                                                   and the feature level after tilt compensation, making it com-
pletion time.
                                                                                   paratively insensitive to errors in the reconstructed in-plane
                                                                                   sweep coordinate. Diameter, groove footprint, and projected-
B. Metrological Validation                                                         location measurements, in contrast, depend directly on the
   The second experiment validates the measurement expert                          spatial spacing and shape of successive profiles. The current
independently of task-planning and manipulation outcomes.                          acquisition code reconstructs the sweep axis from the com-
Each physical characteristic is measured with a dedicated ref-                     manded robot speed and profiler rate rather than from a robot
erence instrument to establish its as-built value. The evaluation                  pose synchronized to every acquired profile. Residual velocity
covers every inspectable face of every benchmark object. For                       variation and jerk of the measurement arm can therefore create
each face, the workpiece is placed at three admissible in-plane                    nonuniform physical profile spacing that is represented as a
orientations relative to the profiler sweep direction, and three                   uniform grid, distorting dimensions and feature centers along
repeated scans are acquired at each orientation to quantify                        the sweep direction.
repeatability. Every acquisition is processed by the same                              A second limitation follows from the use of a single scan
deterministic pipeline used in the full-system experiments:                        direction for each reported acquisition; scan direction is varied
streamed laser profiles are assembled into a height map,                           between repeats, but multiple directions are not fused within
residual tilt is removed by robust plane fitting, height levels                    one measurement. When a feature is sufficiently deep, the
and feature candidates are extracted, and the corresponding                        laser-triangulation geometry causes one wall to occlude part of
datum-grounded operator produces the reported quantity. For                        the opposite wall or bottom in a direction-dependent manner.
each operator family, Fig. 10(a) evaluates agreement with the                      The implementation converts the resulting missing returns to
reference instrument using signed bias, mean absolute error,                       undefined height samples and fits the reference and feature
and tail absolute error, whereas Fig. 10(b) evaluates scan-to-                     planes only from the remaining valid points. A deep feature
scan repeatability using the standard deviation of repeated                        can consequently produce an asymmetric support region that
measurements. Repeated acquisitions characterize measure-                          perturbs plane estimation and the boundary derived from that
ment stability for the available physical features and are not                     plane, degrading form, relative-orientation, and lateral-size
treated as additional independently manufactured specimens.                        measurements even when the vertical level separation remains
   Each row on the vertical axis of Fig. 10 groups quantities                      stable.
that share a geometric estimator. Opening diameter denotes di-
ameters recovered by fitting circular contours to blind, through,                  C. Active Surface Correspondence
or nested openings. Depth and surface offset denotes the                             We evaluate LOOK based physical to specification corre-
vertical separation between a local host surface and a recessed                    spondence independently of scanning and measurement by
                                                                                                                                                                                      16


                                                                                                                TABLE III
                                                                                    P OST- REORIENTATION STATE ADMISSION ON MATCHED L2 EXECUTIONS
                                                                                       WITH AND WITHOUT THE CORRESPONDENCE GATE . R EJECTED AND
                                                                                             ABSTAINED STATES ARE COUNTED AS NOT ADMITTED .


                                                                                               Method                               Correct-face           Wrong-face
                                                                                                                                    acceptance ↑           admission ↓
                                                                                               w/o correspondence gate                  15/15                  25/25
    (a)                       (b)                       (c)
                                                                                               w/ correspondence gate                   14/15                   2/25
Fig. 11.      Scope risk evaluation with and without deterministic scope
expansion (DSE). Correct grounding rates are reported at three levels of the         (a) Requirement      (b) Invalid Acquisition    (c) Gate Diagnosis      (d) Recovered Acquisition
specification hierarchy: (a) required faces, (b) corresponding features, and (c)      (Target & Spec)      (What was scanned)        & Recovery Action           (Correct Evidence)
leaf requirements, across task types T1–T5.                                         1. Z range Clipping
                                                                                                                                         Gate: Lower
                                                                                                                                       Z-margin violated


                                                                                                                                        Recovery: Shift Z
comparing FRAME with Direct VLM Judgment. Both methods                                  “Inspect the
                                                                                    counterbore on the    Hole bottom clipped          center and enlarge         Full hole bottom
                                                                                                             by Z-window               measurement range             recovered
receive exactly the same fixed LOOK observations for each                              top end face”

                                                                                     2. Incomplete
geometry family. When a configuration requires one LOOK,                            Lateral Coverage
                                                                                                                                          Gate: Insufficient
the baseline receives that single image. When it requires                                                                                  lateral coverage

multiple LOOKs, all selected images are provided together,
                                                                                        “Inspect the         Required feature          Recovery: Re-center
and the VLM is asked to directly return the physical to                              through-holes on
                                                                                     the top end face”
                                                                                                           region truncated by
                                                                                                              scan boundary
                                                                                                                                      and extend scan path
                                                                                                                                                                  Complete feature
                                                                                                                                                                  region recovered
specification region assignment. The prediction is released                          3. Wrong host
without legal configuration resolution or a confidence and                           plane selection
                                                                                                                                          Gate: Host plane
                                                                                                                                         Consistency check
consistency gate. FRAME instead uses the VLM only to
produce region matching scores for each view, resolves those                           “Inspect the       Incorrect host plane         Recovery: Re-select
                                                                                    counterbore on the       selected for tilt         host surface point        Correct host plane
scores over the finite set of legal configurations, and releases                        back face”             correction                and refit plane             recovered

the resulting correspondence only if its score, top two margin,
and anchor and topology checks all pass. The fixed LOOK                            Fig. 12.      Representative metrology failures and recovery. Three cases
set is executed once in both methods. A failed FRAME gate                          illustrate Z-range clipping, incomplete lateral coverage, and incorrect host-
                                                                                   plane selection. Requirement-specific admissibility checks reject the invalid
produces abstention and never triggers an additional LOOK.                         acquisition and trigger targeted recovery before the measurement is admitted
   Table II reports four complementary metrics. Candidate ac-                      as evidence.
curacy is the fraction of trials whose candidate correspondence
is correct before the gate. For FRAME, this evaluates the
highest scoring legally resolved configuration. Per-trial wrong-                   respondence from the VLM is unreliable, particularly when
release rate is the fraction of all trials in which an incorrect                   the decision requires combining multiple LOOKs. A single
correspondence is released and can therefore enter the evi-                        dominant view often provides enough evidence for the VLM
dence path. Abstention rate is the fraction of trials for which                    to identify the visible region, but input with multiple views
FRAME releases no correspondence because at least one gate                         introduces hallucination and inconsistent binding between
condition fails. Released accuracy is the fraction of released                     images and specification regions. The error audit also reveals
FRAME correspondences that are correct, so it measures the                         failures on fine grained geometry. The VLM may miscount
reliability of released outputs rather than the accuracy of the                    repeated holes, omit a counterbore, or assign several observed
gate as a binary classifier. Direct VLM Judgment has no gate,                      physical faces to the same specification face. Such outputs
so its abstention rate and released accuracy are marked as not                     can appear semantically plausible while violating the object’s
applicable. Because every baseline prediction is released, its                     adjacency, opposite face, handedness, or exclusivity relations,
wrong release rate equals its candidate error rate.                                and the unconstrained baseline has no mechanism to reject
   We report L1 and L2 separately to expose the effect of                          them.
morphology and visual complexity. The benchmark contains                              FRAME largely prevents these failures by converting the
one L1 and two L2 workpieces from each of four families:                           VLM evidence from each view into scores over only legal
cube, stepped block, cylinder, and bracket. This gives four L1                     configurations and withholding outputs that are weak, am-
and eight L2 workpieces. For every cube and stepped block                          biguous, or structurally inconsistent. The resulting pattern is
workpiece, we test five legal configurations. For every cylinder                   higher candidate accuracy, substantially fewer wrong releases,
and bracket, we test two. Each configuration is executed three                     and high accuracy among released outputs, with increased
times with the prescribed LOOK set, and ground truth physical                      abstention on the more challenging L2 workpieces. Residual
to specification associations are annotated for every execution.                   errors mainly arise from observation quality rather than uncon-
This protocol yields 42 L1 trials and 84 L2 trials. Both                           strained correspondence generation. In particular, an oblique
methods are evaluated on paired observations from the same                         wrist camera viewpoint can cause the SAM3 crop to include
executions so that the comparison isolates correspondence                          multiple physical faces. The resulting mixed visual evidence
inference and gating rather than viewpoint or acquisition                          may lower the score or margin and trigger abstention. In
variation.                                                                         rare cases, it may support a coherent but incorrect legal
   The table shows that directly requesting a complete cor-                        configuration that passes the gate.
                                                                                                                                                                  17



            Task Input                 Ground Required Scope             First Verified Scan            Reorient, Verify and Scan        Evidence, Coverage, Sort
                                                                                Look                        Reorient, Verify
   “Confirm that the grooves                                                                                                                Evidence Memory
   on the back and left faces                                                                                                         Width
   match in size, and that                                                                                                            Length
   each groove floor is            back face          left face                                                                       Depth
   parallel to its host face.”                                                                                                        Parallelism
                                                                                                                                      Groove sizes match
                                                                                 Scan                             Scan
                                                                                                                                       Complete Coverage
             Structured Spec                                                                                                            of required scope
                                    groove            groove
                                                                                                                                       Conformance Evaluator
                                  Width            Width                                                                                   Groove size mismatch
                                  Length           Length                                                                                      No-Pass
                                  Depth            Depth               Admissible evidence               Admissible evidence                         Sort
                                  parallelism      parallelism                    Width                            Width
                                                                                  Length                           Length
                                                                                  Depth                            Depth
      Initial Observation           groove sizes must match                       parallelism                      parallelism



Fig. 13. Case study of cross-face groove inspection. Given the instruction and structured specification, FRAME expands the required scope from target faces
to groove features and leaf requirements, including width, length, depth, floor parallelism, and the cross-face size relation. The system verifies the first surface
before scanning, admits only valid measurements into Evidence Memory, then reorients the part, re-verifies the exposed surface, and performs the second
scan. After complete evidence coverage is achieved, the deterministic conformance evaluator identifies a groove-size mismatch and issues a NO-PASS verdict
before sorting.



D. Risk Decomposition                                                              behavior for Z-range clipping, incomplete lateral coverage,
   1) Scope Risk (γ): Figure 11 evaluates whether the                              and incorrect host-plane selection. The corresponding checks
grounded scope contains all ground-truth faces, features, and                      respectively adjust the Z window, extend and recenter the
atomic leaf requirements. DSE and its ablation perform sim-                        scan, or reselect support points before refitting. In each case,
ilarly at the face and feature levels but diverge substantially                    the recovered result must again pass admissibility, preventing
at the leaf level. The dominant error is therefore incomplete                      acquisition or reconstruction failures from supporting confor-
enumeration rather than failure to recognize the high-level tar-                   mance and reducing α without relying on a generic rescan.
get. By expanding specification-declared dependencies, DSE
prevents member measurements, cross-surface relations, and                         E. Case Study
supporting requirements from being omitted, particularly for
                                                                                      Fig. 13 demonstrates how FRAME resolves cross-face evi-
composite, relational, and functional-goal instructions.
                                                                                   dence requirements. For an instruction comparing grooves on
   2) Correspondence Risk (δ): This experiment isolates post-                      the back and left faces, the system grounds the required groove
reorientation verification using all eight L2 workpieces and                       dimensions, floor parallelism, and cross-face size relation,
five task types, with one execution per object–task pair. Each                     then verifies the exposed surface before scanning. Because
episode begins from a random admissible pose in which                              the first scan leaves the left-face requirements uncovered, the
the required canonical face fexp is not scannable. After the                       coverage audit triggers reorientation; a second L OOK confirms
frozen VLA attempts reorientation, a calibrated L OOK updates                      surface correspondence before the next scan is admitted. Once
the physical-to-specification correspondence; terminal states                      both sets of admissible measurements enter Evidence Memory,
are annotated independently from the calibrated view, feature                      the deterministic evaluator identifies a groove-size mismatch
registry, and video. Both variants use the same VLA execu-                         and returns N O -PASS, despite valid individual groove and
tions and differ only in whether the updated correspondence                        parallelism measurements. Thus, reorientation serves only
must verify fexp before measurement. Without the gate, every                       unresolved evidence demand, while verified evidence rather
completed action is admitted; with it, a mismatch, rejection,                      than the manipulation outcome determines the final verdict
or abstention triggers recovery or manual review. Table III                        and sorting action.
shows that the ungated variant accepts all 15 correct-face
states but also all 25 wrong-face states. The gate retains 14
of 15 correct states while reducing wrong-face admission to                                                    VII. C ONCLUSION
2 of 25. It does not improve manipulation; instead, it detects                        This paper introduced task-specified active metrological
most reorientation failures before they propagate as wrong-                        inspection and a hierarchical dual-arm framework that turns
face evidence. Only an incorrect correspondence that passes                        an inspection instruction and a structured specification into
the gate contributes to δ.                                                         complete, traceable evidence. Learned components ground the
   3) Metrology Risk (α): We isolate metrology risk α by                           requested task and provide physical access, while deterministic
fixing the scope, correspondence, operator, and specification                      measurement, admissibility, coverage, and conformance gates
while perturbing only acquisition or measurement processing.                       control which evidence may authorize a release decision.
Requirement-specific admissibility predicates reject plausible                     Physical experiments on controlled workpiece families and
but invalid measurements before they enter Mt ; the failed                         real CNC parts show improved end-to-end reliability and com-
predicate then selects a targeted recovery, after which the same                   pletion efficiency over exhaustive execution and unconstrained
operator and checks are reapplied. Figure 12 illustrates this                      VLM control, while component tests demonstrate the value of
                                                                                                                                                               18



correspondence verification and measurement-failure rejection.                      [9] Y. Liu, J. Zhu, Y. Mo, G. Li, X. Cao, J. Jin, Y. Shen, Z. Li, T. Yu,
The current system remains limited to a finite specification and                        W. Yuan, et al., “Palm: Progress-aware policy learning via affor-
                                                                                        dance reasoning for long-horizon robotic manipulation,” arXiv preprint
measurement vocabulary, support-stable configurations, and a                            arXiv:2601.07060, 2026.
single profilometry setup; moreover, motion-derived sweep                          [10] R. Wang, Y. Zhang, J. Lin, K. Luo, J. Wang, Z. Wang, and X. Qi,
reconstruction and single-direction acquisition can degrade                             “When to trust imagination: Adaptive action execution for world action
                                                                                        models,” arXiv preprint arXiv:2605.06222, 2026.
lateral and form measurements for difficult geometries. The                        [11] J. Yang, C. Jimenez, A. Wettig, K. Lieret, S. Yao, K. Narasimhan, and
false-accept decomposition is also an empirically qualified risk                        O. Press, “Swe-agent: Agent-computer interfaces enable automated soft-
contract rather than an unconditional deployment-wide guar-                             ware engineering,” Advances in Neural Information Processing Systems,
                                                                                        vol. 37, pp. 50 528–50 652, 2024.
antee. Future work will incorporate synchronized robot poses                       [12] H. Zhong and S. Zhu, “Ai harness engineering: A runtime substrate for
and multi-direction scan fusion, compile broader MBD/PMI                                foundation-model software agents,” arXiv preprint arXiv:2605.13357,
semantics into executable inspection rules, and evaluate the                            2026.
                                                                                   [13] J. Liang, W. Huang, F. Xia, P. Xu, K. Hausman, B. Ichter, P. Florence,
framework across more diverse geometries, materials, sensors,                           and A. Zeng, “Code as policies: Language model programs for embod-
and production cells.                                                                   ied control,” in 2023 IEEE International conference on robotics and
                                                                                        automation (ICRA). IEEE, 2023, pp. 9493–9500.
                                                                                   [14] W. Huang, C. Wang, R. Zhang, Y. Li, J. Wu, and L. Fei-Fei, “Voxposer:
                         ACKNOWLEDGMENTS                                                Composable 3d value maps for robotic manipulation with language
   This work was supported under Cooperative Agreement                                  models,” in Conference on Robot Learning. PMLR, 2023, pp. 540–562.
W56HZV-21-2-0001 with the U.S. Army DEVCOM Ground                                  [15] Y. Zhang, H. Zhang, F. Gao, X. Li, Z. Liu, C. Zhu, J. Qiu, Y. Yan,
                                                                                        J. Liu, W. Tang, et al., “Harness vla: Steering frozen vlas into reliable
Vehicle Systems Center (GVSC), through the Virtual Proto-                               manipulation primitives via memory-guided agents,” arXiv preprint
typing of Autonomy Enabled Ground Systems (VIPR-GS)                                     arXiv:2607.08448, 2026.
program, and by the National Science Foundation, United                            [16] S. Lee, J. Chae, and K.-J. Park, “Harness engineering for phys-
                                                                                        ical ai: Robot middleware is the harness layer,” arXiv preprint
States (Grant Nos. 2434519 and 2543603).                                                arXiv:2606.09416, 2026.
   DISTRIBUTION STATEMENT A. Approved for public                                   [17] Q. Wang, T. Wang, C. Li, S. Ban, Y. Chen, Y. Ge, J. Qin, C. Li, and
release; distribution is unlimited. OPSEC11090                                          W. Zhu, “Towards the harness of embodied agents,” 2026, technical
                                                                                        Report.
   Disclaimer: Reference herein to any specific commercial                         [18] Y.-J. Lin, R. Mahabaleshwarkar, and E. Massina, “Cad-based cmm
company, product, process, or service by trade name, trade-                             dimensional inspection path planning–a generic algorithm,” Robotica,
mark, manufacturer, or otherwise, does not necessarily con-                             vol. 19, no. 2, pp. 137–148, 2001.
                                                                                   [19] N. D. M. Phan, Y. Quinsat, S. Lavernhe, and C. Lartigue, “Path planning
stitute or imply its endorsement, recommendation, or favoring                           of a laser-scanner with the control of overlap for 3d part inspection,”
by the United States Government or the Department of the                                Procedia Cirp, vol. 67, pp. 392–397, 2018.
Army (DoA). The opinions of the authors expressed herein                           [20] M. Vlaeyen, H. Haitjema, and W. Dewulf, “Uncertainty-based au-
                                                                                        tonomous path planning for laser line scanners,” Metrology, vol. 2, no. 4,
do not necessarily state or reflect those of the United States                          pp. 479–494, 2022.
Government or the DoA and shall not be used for advertising                        [21] X. Chen, Q. Li, T. Wang, T. Xue, and J. Pang, “Gennbv: Generalizable
or product endorsement purposes.                                                        next-best-view policy for active 3d reconstruction,” in 2024 IEEE/CVF
                                                                                        Conference on Computer Vision and Pattern Recognition (CVPR).
                                                                                        IEEE, 2024, pp. 16 436–16 445.
                              R EFERENCES                                          [22] Z. Chen, Y. Zhang, F. J. Piran, Q. Zhou, J. Tang, and F. Imani, “Scanbot:
 [1] K. Chen, S. Xie, L. Fu, J. Yu, W. Pacini, S. Bajamahal, H. Kim,                    A benchmark for precision robotic surface scanning with industrial laser
     J. Drake, D. Kim, H. Xue, et al., “Gap: A graph-as-policy multi-agent              profilers,” arXiv preprint arXiv:2505.17295, 2025.
     self-learning harness for variational automation tasks,” arXiv preprint       [23] P. Bergmann, M. Fauser, D. Sattlegger, and C. Steger, “Mvtec ad—a
     arXiv:2607.05369, 2026.                                                            comprehensive real-world dataset for unsupervised anomaly detection,”
 [2] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, X. Chen, K. Choroman-               in 2019 IEEE/CVF Conference on Computer Vision and Pattern Recog-
     ski, T. Ding, D. Driess, A. Dubey, C. Finn, et al., “Rt-2: Vision-language-        nition (CVPR). IEEE, 2019, pp. 9584–9592.
     action models transfer web knowledge to robotic control,” arXiv preprint      [24] K. Roth, L. Pemula, J. Zepeda, B. Schölkopf, T. Brox, and P. Gehler,
     arXiv:2307.15818, 2023.                                                            “Towards total recall in industrial anomaly detection,” in 2022
 [3] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair,            IEEE/CVF Conference on Computer Vision and Pattern Recognition
     R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong, et al., “Openvla:              (CVPR). IEEE, 2022, pp. 14 298–14 308.
     An open-source vision-language-action model,” in Conference on Robot          [25] Z. Gu, B. Zhu, G. Zhu, Y. Chen, M. Tang, and J. Wang, “Anomalygpt:
     Learning. PMLR, 2025, pp. 2679–2713.                                               Detecting industrial anomalies using large vision-language models,” in
 [4] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai,              Proceedings of the AAAI conference on artificial intelligence, vol. 38,
     L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke,                    no. 3, 2024, pp. 1932–1940.
     S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, L. X. Shi,          [26] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn,
     J. Tanner, Q. Vuong, A. Walling, H. Wang, and U. Zhilinsky, “π0 :                  K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu, et al., “Rt-1:
     A vision-language-action flow model for general robot control,” 2026.              Robotics transformer for real-world control at scale,” arXiv preprint
     [Online]. Available: https://arxiv.org/abs/2410.24164                              arXiv:2212.06817, 2022.
 [5] S. Ye, Y. Ge, K. Zheng, S. Gao, S. Yu, G. Kurian, S. Indupuru, Y. L. Tan,     [27] K. Bousmalis, G. Vezzani, D. Rao, C. Devin, A. X. Lee, M. Bauzá,
     C. Zhu, J. Xiang, et al., “World action models are zero-shot policies,”            T. Davchev, Y. Zhou, A. Gupta, A. Raju, et al., “Robocat: A self-
     arXiv preprint arXiv:2602.15922, 2026.                                             improving generalist agent for robotic manipulation,” arXiv preprint
 [6] T. Yuan, Z. Dong, Y. Liu, and H. Zhao, “Fast-wam: Do world                         arXiv:2306.11706, 2023.
     action models need test-time future imagination?” arXiv preprint              [28] O. M. Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees,
     arXiv:2603.16666, 2026.                                                            S. Dasari, J. Hejna, T. Kreiman, C. Xu, et al., “Octo: An open-source
 [7] T. Ma, J. Zheng, Z. Wang, C. Jiang, A. Cui, J. Liang, and S. Yang,                 generalist robot policy,” arXiv preprint arXiv:2405.12213, 2024.
     “Dit4dit: Jointly modeling video dynamics and actions for generalizable       [29] W. Huang, P. Abbeel, D. Pathak, and I. Mordatch, “Language models
     robot control,” arXiv preprint arXiv:2603.10448, 2026.                             as zero-shot planners: Extracting actionable knowledge for embodied
 [8] Y. Fan, P. Ding, S. Bai, X. Tong, Y. Zhu, H. Lu, F. Dai, W. Zhao,                  agents,” in International conference on machine learning. PMLR, 2022,
     Y. Liu, S. Huang, et al., “Long-vla: Unleashing long-horizon capability            pp. 9118–9147.
     of vision language action model for robot manipulation,” arXiv preprint       [30] A. Brohan, Y. Chebotar, C. Finn, K. Hausman, A. Herzog, D. Ho,
     arXiv:2508.19958, 2025.                                                            J. Ibarz, A. Irpan, E. Jang, R. Julian, et al., “Do as i can, not as i
                                                                                     19



     say: Grounding language in robotic affordances,” in Conference on robot
     learning. Pmlr, 2023, pp. 287–318.
[31] W. Huang, F. Xia, T. Xiao, H. Chan, J. Liang, P. Florence, A. Zeng,
     J. Tompson, I. Mordatch, Y. Chebotar, et al., “Inner monologue: Embod-
     ied reasoning through planning with language models,” arXiv preprint
     arXiv:2207.05608, 2022.
[32] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao,
     “React: Synergizing reasoning and acting in language models,” arXiv
     preprint arXiv:2210.03629, 2022.
[33] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao, “Re-
     flexion: Language agents with verbal reinforcement learning,” Advances
     in neural information processing systems, vol. 36, pp. 8634–8652, 2023.
[34] P. Liu, Y. Orru, J. Vakil, C. Paxton, N. Shafiullah, and L. Pinto,
     “Demonstrating ok-robot: What really matters in integrating open-
     knowledge models for robotics,” Robotics: Science and Systems XX,
     2024.
[35] W. Huang, C. Wang, Y. Li, R. Zhang, and L. Fei-Fei, “Rekep: Spatio-
     temporal reasoning of relational keypoint constraints for robotic manip-
     ulation,” arXiv preprint arXiv:2409.01652, 2024.
[36] R. Li, Y. Zhou, Y. Zhu, K. Chen, J. Wang, S. Wang, K. Hu, M. Yu,
     B. Jiang, Z. Su, et al., “Roboclaw: An agentic framework for scalable
     long-horizon robotic tasks,” arXiv preprint arXiv:2603.11558, 2026.
[37] ASME, Dimensioning and Tolerancing, The American Society of Me-
     chanical Engineers, New York, NY, USA, 2018, aSME Y14.5-2018
     (R2024).
[38] N. Carion, L. Gustafson, Y.-T. Hu, S. Debnath, R. Hu, D. Suris Coll-
     Vinent, C. Ryali, K. V. Alwala, H. Khedr, A. Huang, et al., “Sam
     3: Segment anything with concepts,” in International Conference on
     Learning Representations, vol. 2026, 2026, pp. 138 846–138 923.
[39] K. Black, M. Galliker, and S. Levine, “Real-time execution of action
     chunking flow policies,” Advances in Neural Information Processing
     Systems, vol. 38, pp. 33 383–33 407, 2026.
[40] J. Hu, M. Shridhar, C. Lu, D. Shah, H.-T. L. Chiang, J. Tan, and A. Xie,
     “What matters in orchestrating robot policies: A systematic study of
     hierarchical vla agents,” arXiv preprint arXiv:2606.10267, 2026.
[41] S. Bai, Y. Cai, R. Chen, K. Chen, X. Chen, Z. Cheng, L. Deng, W. Ding,
     C. Gao, C. Ge, W. Ge, Z. Guo, Q. Huang, J. Huang, F. Huang, B. Hui,
     S. Jiang, Z. Li, M. Li, M. Li, K. Li, Z. Lin, J. Lin, X. Liu, J. Liu, C. Liu,
     Y. Liu, D. Liu, S. Liu, D. Lu, R. Luo, C. Lv, R. Men, L. Meng, X. Ren,
     X. Ren, S. Song, Y. Sun, J. Tang, J. Tu, J. Wan, P. Wang, P. Wang,
     Q. Wang, Y. Wang, T. Xie, Y. Xu, H. Xu, J. Xu, Z. Yang, M. Yang,
     J. Yang, A. Yang, B. Yu, F. Zhang, H. Zhang, X. Zhang, B. Zheng,
     H. Zhong, J. Zhou, F. Zhou, J. Zhou, Y. Zhu, and K. Zhu, “Qwen3-vl
     technical report,” arXiv preprint arXiv:2511.21631, 2025.
[42] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia,
     D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, M. Y. Galliker,
     D. Ghosh, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones,
     L. Ke, D. LeBlanc, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair,
     K. Pertsch, A. Z. Ren, L. X. Shi, L. Smith, J. T. Springenberg,
     K. Stachowicz, J. Tanner, Q. Vuong, H. Walke, A. Walling,
     H. Wang, L. Yu, and U. Zhilinsky, “π0.5 : a vision-language-action
     model with open-world generalization,” 2025. [Online]. Available:
     https://arxiv.org/abs/2504.16054
[43] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang,
     and W. Chen, “Lora: Low-rank adaptation of large language models,”
     2021. [Online]. Available: https://arxiv.org/abs/2106.09685
