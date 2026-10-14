                                                                                                                                                                                   1




                                           Agentic Neuro–Symbolic Planning and
                                        Commissioning for Human-in-the-Loop Industrial
                                                 Robotics with Digital Twins
                                        Zhihao Liu, Member, IEEE, Victor Nan Fernandez-Ayala, Graduate Student Member, IEEE, Tianyu Wang,
                                                   Qiang Qin, Xi Vincent Wang, Dimos V. Dimarogonas, Fellow, IEEE, and Lihui Wang
                                           Abstract— Flexible robotic automation requires systems                   translating high-level human intent into physically executable
                                        that interpret operator intent, verify physical feasibility,                robot motions [3], [4]. Recent advances in large language
                                        and recover from execution failures across both the plan-                   models (LLMs) have demonstrated promising capabilities for
                                        ning and execution stages. This paper proposes an agen-
arXiv:2606.08214v1 [cs.RO] 6 Jun 2026




                                        tic neuro-symbolic framework for human-in-the-loop in-                      generating task plans from natural-language instructions [5]–
                                        dustrial robotics, in which LLMs are used for tasks that                    [10]. However, deploying LLM-generated plans on physical
                                        require language understanding or contextual reasoning,                     robot systems remains challenging due to the gap between lin-
                                        while all verification, sequencing, and execution remain de-                guistic reasoning and physical constraints, the lack of closed-
                                        terministic. The framework adapts the Planner-Generator-                    loop feedback from execution to planning, and the absence
                                        Evaluator (PGE) harness pattern from software engineer-
                                        ing into a Specifier-Designer-Inspector (SDI) architecture                  of human oversight mechanisms suitable for safety-critical
                                        for industrial robotics, combined with LangGraph-based                      industrial environments.
                                        dynamic routing for failure recovery. A two-tier recovery                      Existing approaches can be broadly categorized into three
                                        mechanism addresses structure-level replanning through                      groups. First, classical task and motion planning (TAMP)
                                        context-aware orchestration and execution-level geometric
                                        failures through deterministic recovery skills. A Unity3D                   methods [11] provide formal guarantees but require hand-
                                        digital twin supports human inspection, modification, and                   coded domain descriptions and cannot handle natural lan-
                                        re-verification prior to physical execution. Evaluated on                   guage input. Second, LLM-based planning systems such as
                                        natural-language commands across multiple difficulty lev-                   SayCan [12] and Code as Policies [13] use an LLM with
                                        els against ten baselines, the proposed method achieves                     predefined prompts but lack execution monitoring, failure re-
                                        the highest task success. Ablation results confirm that
                                        structured command expansion, symbolic verification, se-                    covery, and human-in-the-loop capabilities. Third, multi-agent
                                        lective LLM routing, and recovery skills are each individu-                 LLM frameworks such as AutoGen [14] and CrewAI [15]
                                        ally necessary.                                                             enable collaboration between multiple LLM agents but op-
                                          Index Terms— Multi-agent systems, large language mod-                     erate purely in the language domain without connection to
                                        els, neuro-symbolic AI, harness engineering, digital twins,                 physical robot systems or their digital twins. Furthermore,
                                        human-in-the-loop, industrial robotics.                                     graph-based orchestration frameworks such as LangGraph [16]
                                                                                                                    enable dynamic, LLM-driven routing between agents, but
                                                                                                                    production experience has revealed that delegating all control-
                                                                 I. I NTRODUCTION
                                                                                                                    flow decisions to the LLM leads to unpredictable behavior

                                        I   NDUSTRIAL robotics and automation systems increas-
                                            ingly emphasize human-centricity in the transition toward
                                        Industry 5.0 and even Industry 6.0 [1], [2]. Artificial intel-
                                                                                                                    and difficult debugging [17]. This has motivated the Planner-
                                                                                                                    Generator-Evaluator (PGE) harness in software engineering,
                                                                                                                    where deterministic scaffolding wraps LLM calls to ensure
                                        ligence and digital twins are two emerging technologies for                 reliability, as demonstrated in tools such as Claude Code [17].
                                          This work was supported by Swedish Digital Futures’ Industrial In-           These observations point to a fundamental tension between
                                        novation project: Towards Safe Smart Construction: Algorithms, Digital      neural flexibility and symbolic reliability [18]–[20]. LLMs ex-
                                        Twins and Infrastructures (VF 2020-0315).                                   cel at interpreting ambiguous natural language and generating
                                          Corresponding author: Zhihao Liu.
                                          Zhihao Liu, Tianyu Wang, Qiang Qin, Xi Vincent Wang, and Lihui            creative spatial arrangements, yet they lack formal guarantees
                                        Wang are with the Department of Production Engineering, School              on physical feasibility. An LLM may produce a structure
                                        of ITM, Royal Institute of Technology (KTH), 100 44 Stockholm,              to be assembled by robots that violates gravity constraints,
                                        Sweden (Email: zhihaoliu@ieee.org, qiangq@kth.se,
                                        tianyuwa@kth.se, wangxi@kth.se, lihuiw@kth.se).                             causes collisions, or yields unreachable grasp poses, with no
                                          Victor Nan Fernandez-Ayala, and Dimos V. Dimarogonas are with             mechanism to detect or correct such errors from within the
                                        the Department of Decision and Control Systems, School of EECS,
                                        Royal Institute of Technology (KTH), 100 44 Stockholm, Sweden (Email:
                                                                                                                    model itself. Conversely, classical symbolic methods such as
                                        vnfa@kth.se, dimos@kth.se).                                                 constraint solvers, graph-based planners, and deterministic ver-
                                          During the preparation of this work the author(s) used Anthropic Opus     ifiers can enforce physical laws with mathematical certainty,
                                        4.7 in order to help prepare the initial draft of this manuscript, design   but they cannot process free-form language or adapt to open-
                                        code for experiments, and polish writing. After using this tool/service,
                                        the author(s) reviewed and edited the content as needed and take(s) full    ended task specifications.
                                        responsibility for the content of the published article.                       This complementarity motivates a neuro-symbolic architec-
                                          This work has been submitted to the IEEE for possible publication.
                                        Copyright may be transferred without notice, after which this version may   ture that combines the two paradigms in a principled manner.
                                        no longer be accessible.                                                    In this work, LLMs are used by neural agents for lan-
2



guage understanding, structure design generation, and context-       •  Ihuman : Adjustment input space in the digital twin, where
aware failure routing, while constraint verification, assembly          humans refine object configurations through direct ma-
sequencing, geometric recovery, and execution control are               nipulation after visual inspection
handled by symbolic and reactive agents.                              The output space is:
   Results show that purely neural baselines without symbolic                  QR       dr ×Tr
                                                                      • Q =       r=1 R        : Joint trajectory space for R robot
verification fall below 90% on open-ended large-scale tasks,            manipulators, where dr is the number of joints for robot
while purely symbolic pipelines cannot consume free-form                r and Tr is its trajectory length
natural-language instructions at all. Only the combined neuro-        We distinguish between planned and executed trajectories:
symbolic configuration sustains full coverage across the bench-           plan
                                                                      • Q      ∈ Q: Planned trajectory from commissioning via
mark. None of the existing approaches address the complete
                                                                        digital twin
pipeline from natural language to physical execution with                 exec
                                                                      • Q       ∈ Q: Executed trajectory recorded from remote
human oversight and closed-loop failure recovery. The main
                                                                        monitoring via digital twin
contributions of this paper are as follows.
                                                                      This problem decomposes into the following sub-problems.
   (i) A complete human-in-the-loop planning and commis-              Sub-problem 1: Target Structure Design Generation. Given
       sioning pipeline that unifies natural-language task in-     l ∈ L, generate a structure configuration C ∈ C:
       take, digital-twin supervision, multi-agent reasoning,
       symbolic verification, and closed-loop robot execution,               C = {c1 , c2 , . . . , cn },   ci = (idi , pi , qi , si )   (2)
       bridging AI inference and human oversight at every          where idi is the ID of any object, pi ∈ R3 is position, qi ∈
       decision point of industrial robot systems.                 SO(3) is orientation, and si ∈ R3+ is the object size. This
  (ii) A Specifier-Designer-Inspector (SDI) multi-agent or-        step corresponds to mapping linguistic intent into a geometric
       chestration that adapts the Planner-Generator-Evaluator     representation in the digital twin.
       harness pattern from software engineering to industrial        Sub-problem 2: Human Adjustment. After commissioning
       robots, coordinating heterogeneous neural and symbolic      in the digital twin, the human may refine the generated layout.
       agents through deterministic scaffolding plus LLM-          Given C ∈ C and human input Ih ∈ Ihuman , a refined
       driven dynamic routing, with the Inspector replacing the    configuration is obtained as
       LLM-based critic with a symbolic verifier for formal
       feasibility guarantees.                                                                  C ′ = C ⊕ Ih ,                           (3)
 (iii) A two-tier closed-loop failure recovery mechanism           where ⊕ denotes the application of human modifications,
       not addressed in prior LLM-based planning systems:          including translating or rotating existing objects, inserting new
       context-aware orchestration drives layout replanning at     objects, and removing objects from the configuration.
       the design tier, while domain-specific geometric recov-        Sub-problem 3: Task Sequence Planning. Given the refined
       ery skills handle motion-planning failures at the execu-    configuration C ′ = {c1 , c2 , . . . , cn } as defined in (3), find an
       tion tier, both coupled to the digital twin for automatic   assembly sequence
       re-verification and human-in-the-loop correction.
                                                                                    S = (σ1 , c1 )(σ2 , c2 ) · · · (σn , cn )            (4)
                      II. F ORMULATION                             where σi denotes the procedural order index of ci , such that
                                                                   the overall solution is feasible in the sense of Section II.
   An LLM is modeled as an autoregressive mapping param-
                                                                      Sub-problem 4: Motion Planning and Commissioning
eterized by θ that, given a prompt s ∈ Σ∗ , produces a token
                                                                   through Digital Twin. Given an assembly sequence S, com-
sequence y = fθ (s) through one complete decoding pass. We
                                                                   pute collision-free joint trajectories Qplan ∈ Q for the robot
use this notation fθ (·) throughout the paper to denote a single
                                                                   manipulators. Motion planning is executed sequentially along
LLM inference call.
                                                                   S using the current robot state at each step.
   Without loss of generality, we formalize the human-in-the-         Sub-problem 5: Motion Monitoring and Validation through
loop robot task-and-motion planning problem for industrial         Digital Twin. This sub-problem ensures execution reliability
robotic automation, where natural-language instructions, inter-    and safety by quantitatively checking whether physical robot
active digital twins, symbolic task reasoning, and continuous      motion remains consistent with the planned trajectory and
motion planning are tightly integrated. Given a natural lan-       by providing a criterion for triggering feedback actions (e.g.,
guage instruction l ∈ L and optional human adjustment input        warning, pause, or replanning). Given the executed trajectory
Ih ∈ Ihuman from digital twin, find a feasible robot trajectory    Qexec recorded from robot joint encoders, we verify that
Q ∈ Q that assembles the target structure while satisfying all     execution conforms to the plan:
physical and kinematic constraints:
                                                                     Vtraj : Qplan × Qexec → {pass, fail},          Qplan , Qexec ∈ Q    (5)
                     Π : L × Ihuman → Q                      (1)
                                                                     The validation is based on the trajectory deviation metric:
    The problem involves two types of human input:                           δ(Qplan , Qexec ) = max ∥qrplan (t) − qrexec (t)∥2          (6)
              ∗                                                                                      r,t
    • L = Σ : Natural language instruction space, where
      humans specify high-level assembly goals (e.g., “build       where qr (t) denotes the joint configuration of robot r at time
      a 3-cube tower”)                                             t.
                                                                                                                                                                                                           3



                                                                           Natural                Multi-Agent                                                                               Assembled
  The trajectory is validated as follows:                                 Language               Orchestration         replan if
                                                                                                                       needed
                                                                                                                                   Commissioning              Robot Motion
                                                                                                                                                                                             Structure
                              (
                               pass if δ(Qplan , Qexec ) ≤ ϵ
     Vtraj (Qplan , Qexec ) =                                  (7)
                               fail otherwise                                                   Specifier + Designer
                                                                                                                                    Human review
                                                                                                                                        motion
                                                                                                                                                               Robot motion
                                                                                                                                                                                            Robotic task
                                                                        User command                                                                          execution in real
                                                                                                  + Inspector with                 commissioning in                                         verified and
                                                                        of robotic tasks                                                                           world
                                                                                                   Orchestration                      digital twin                                           recorded
where ϵ is the acceptable deviation threshold.
   A structure configuration C and its assembly sequence S            Fig. 1. System workflow.
are jointly feasible if they satisfy the following six constraints,
which together define the constraint set K referenced through-
out the methodology. Two objects ci and cj are in contact                                                     III. M ETHODOLOGY
when their axis-aligned bounding boxes meet along all three           A. System Workflow
axes within a tolerance ϵ:
                                                            !           The proposed human-in-the-loop task-and-motion planning
                         ^
                                   d     d
                                               sdi + sdj              and commissioning pipeline is summarized by the following
  contact(ci , cj ) ≜            |pi − pj | ≤            + ϵ , (8)
                                                   2                  operator chain and Fig. 1:
                    d∈{x,y,z}
                                                                                           fθ (·; ϕ(E))                h                   gsym               τ                   ρmotion
where pi and si are defined in (2). This predicate is used in           π : L −−−−−−−→ C −−DT → C ′ −−→ C ∗ −−→ T −−−→ Qplan .
                                                                                                             task


Constraints 1 and 4 below.                                                                                                 (15)
  Constraint 1 (Gravity): Objects must be supported from              To close the loop during deployment, the execution and
below. For objects in contact ci , cj :                               monitoring processes are defined as
            contact(ci , cj ) ∧ (pzi < pzj ) ⇒ σi < σj         (9)                                                     execute
                                                                                           πexec : Qplan −−−−→ Qexec −−→ {pass, fail},
                                                                                                                                                      Vtraj

                                                                                                                       ηDT
where superscript z indicates the Z axis, σi is the placement                                         Qplan −−→ Z,                                                                                  (16)
order index of ci .                                                                                       exec ηreal
                                                                                                      Q            −−→ Z.
  Constraint 2 (Reachability): All objects must lie within the
robot workspace. For tractability, we use a cuboid workspace       where πexec denotes the deployment-time execution and mon-
as an example, where x, y, and z indicate the size:                itoring operator, ηDT indicates the commissioning of planned
                                                                   trajectory in digital twin, ηreal monitors the executed trajectory
∀ci : pi ∈ W, W = [xmin , xmax ]×[ymin , ymax ]×[zmin , zmax ]
                                                                   in digital twin, and Z denotes the digital space in digital twin.
                                                              (10)
                                                                      Together, (15) and (16) define a closed-loop workflow from
   Constraint 3 (Collision): Objects cannot overlap:
                                                                   natural-language intent to physical execution under digital-
       ∀ci , cj : i ̸= j ⇒ AABB(ci ) ∩ AABB(cj ) = ∅          (11) twin commissioning and monitoring. The pipeline is organized
                                                                   into four functional modules, summarized below.
where AABB denotes the Axis-Aligned Bounding Box, i.e., the           Module 1: Structure design generation (III-C). The natural-
minimum box in the world frame that encloses an object.            language command is expanded into a structured specification,
   Constraint 4 (Contact): Non-ground objects must have used to generate a candidate structure, and verified against
structural contact:                                                physical constraints, with violations fed back for targeted
                ∀ci : pzi > 0 ⇒ ∃cj : contact(ci , cj )       (12) regeneration until feasibility is reached.
                                                                      Module 2: Human-in-the-loop digital twin (III-D). The
This constraint enforces static support (no suspension), verified layout is rendered in the digital twin for the operator
whereas Constraint 1 enforces the corresponding placement to accept, modify, or reject. Any edits are automatically re-
order under gravity.                                               verified before proceeding.
   Constraint 5 (Gripping): At least one feasible gripping            Module 3: Symbolic sequencing and task planning (III-E).
exists:                                                            A graph-based symbolic planner derives an assembly order
             ∀ci : ∃β ∈ {x, y} : ¬blocked(ci , β, S<σi )      (13) respecting gravity, support, and gripping feasibility, which is
                                                                   then compiled into a robot-level action sequence.
where S<σi denotes the already placed objects. This condition         Module 4: Motion planning, previewing, and execution (III-
is critical for practical execution with parallel-jaw (two-finger) F). Collision-free trajectories are computed, previewed in the
grippers, which require at least one collision-free approach digital twin, and executed on the physical system. Measured
direction to grasp an object.                                      trajectories are compared against planned ones for in-loop
   Constraint 6 (Sequence): Assembly order respects physical monitoring and recovery.
dependencies:                                                         Although presented in order for clarity, the four mod-
                                                                   ules share three cross-cutting capabilities. Symbolic constraint
                ∀ci , cj : supports(ci , cj ) ⇒ σi < σj       (14)
                                                                   reasoning appears in both Module 1 (feasibility verification
This constraint primarily captures product-level assembly of LLM-generated structures) and Module 3 (gravity, sup-
precedence defined at design time, i.e., which component port, and gripping constraints during sequencing). The digi-
should be assembled first and which should follow. In contrast, tal twin serves as a unified commissioning interface across
Constraints 1 and 4 focus on physical feasibility (gravity and Modules 2 and 4, rendering structures, task sequences, and
static support).                                                   planned/executed trajectories for human review and in-loop
4



                                                                                             Designer Agent                              calls as D ISPATCH(Ξ, n, a) = fξ (a) . Across the system, skills
        Human                                                                                         Neural
        Operator                                                                       Target structure generation                       are organized into four categories: (i) composite verification
      Digital Twin
                                                                                           𝐶𝐶 = {𝑐𝑐1 , 𝑐𝑐2 , … , 𝑐𝑐𝑛𝑛 },                 (ξverify ), which wraps the full constraint verifier V (C, K);
                                                                                           𝑐𝑐𝑖𝑖 = 𝑖𝑖𝑑𝑑𝑖𝑖 , 𝑝𝑝𝑖𝑖 , 𝑞𝑞𝑖𝑖 , 𝑠𝑠𝑖𝑖
    ℎDT : 𝒞𝒞 × ℐhuman → 𝒞𝒞 ′
                                                                                                                                replan
                                                                                                                                         (ii) granular verification (ξws , ξgrav , ξgrip , ξcol ), which isolate in-
                           𝐶𝐶′        Orchestrator Agent                                                                                 dividual constraint checks for targeted diagnosis; (iii) planning
                                              Neural                                        Inspector Agent
                                           𝜉𝜉spec : ℒ → ℒ̂                                          Symbolic
                                                                         verify 𝐶𝐶                                                       skills (ξseq , ξtask ), which invoke assembly sequencing and task
                                     LangGraph LLM routing                                Constraint verification
                                 •   spec received → call Designer       result
                                                                                                                                         generation; and (iv) orchestrating skills (ξspec , ξflatten , ξshift ),
                                                                                          𝑉𝑉: 𝒞𝒞 × 𝒦𝒦
                                 •   layout ready → call Inspector     (pass / fail)                                                     comprising the Specifier for command expansion and domain-
                          ℒ      •   verified      → call Operator
                                                                                          → { pass, ∅ , fail, 𝐸𝐸 }
    NL Command                   •   failure       → invoke Recovery
                                                                                                                                         specific recovery skills for geometric failure correction.
                                           invoke                                            Operator Agent                                 Orchestrator Agent (Neural) decomposes user commands
         Neural                         Recovery Skills                                              Reactive

                                             Invoked by                                       Task execution
                                                                                                                                         into execution phases, schedules agents, and handles failures
         Symbolic                                                bypass Designer
                                           Orchestrator on
         Reactive                           motion failure                             invoke agent’s skill 𝜉𝜉execute                    through replanning or escalation to the human operator. It
                                                                                                                                         implements the proposed SDI harness, inspired by the PGE
Fig. 2. Data flow of the multi-agent orchestration.                                                                                      pattern [17], combined with LangGraph-based dynamic rout-
                                                                                                                                         ing [16]. The SDI Specifier (ξspec ) and Inspector verification
                                                                                                                                         provide deterministic scaffolding where reliability is critical,
monitoring. Multi-agent orchestration (III-B) spans the entire                                                                           whereas LangGraph routing is reserved for failure recov-
pipeline: heterogeneous agents coordinate sequencing, task                                                                               ery where context-awareness improves outcomes. Domain-
compilation, execution, and recovery, and failures in Mod-                                                                               specific recovery skills (ξflatten , ξshift ) address geometric failures
ules 3–4 loop back to Module 1 via LLM-driven routing.                                                                                   that neither fixed rules nor LLM replanning can reliably
                                                                                                                                         resolve. Concretely, it implements a LangGraph-based state
B. Agentic System and Orchestration                                                                                                      machine over the phase space P, consisting of P LAN, D ESIGN,
   We adopt a heterogeneous agentic architecture to cover the                                                                            I NSPECT, H UMAN R EVIEW, P RE E XECUTE, E XECUTE, and
full pipeline from structure design to physical execution with                                                                           R EPLAN, where routing decisions at branch points are made
human oversight. The system consists of four computational                                                                               by LLM calls. In the P LAN phase, the Orchestrator invokes
agents and one human operator, as shown in Fig. 2.                                                                                       ξspec : L → L̂ to expand the raw command into a structured
   An agent ai is defined as a tuple ai = (typei , Ξi , πi ), where                                                                      specification ˆl. In the R EPLAN phase, it first applies recovery
typei ∈ {Neural, Symbolic, Reactive} denotes the computa-                                                                                skills and falls back to LLM-driven replanning only when
tional paradigm, Ξi is the agent’s skill set, and πi is the                                                                              needed. Outputs from recovery skills are routed directly to
decision policy. The human operator H interacts with the                                                                                 the Inspector for re-verification. All retry, replanning, and
system through the digital twin and is not modeled as an agent                                                                           escalation decisions remain with the Orchestrator.
but as an external decision-maker.                                                                                                          Designer Agent (Neural) generates and modifies layouts
   The three agent types follow the design principle that LLMs                                                                           from structured specifications, exposing ξgenerate and ξmodify as
are used only where necessary. Neural agents handle language                                                                             skills:
understanding and contextual reasoning. Symbolic agents use                                                                                             ξgenerate : L̂ → C, ξmodify : C × E → C                (18)
deterministic algorithms for verification and sequencing. Re-
active agents interface directly with the robot system for real-                                                                         where L̂ is the structured specification space produced by the
time execution.                                                                                                                          Specifier, and E denotes error feedback from the Inspector
   All agents share a unified skill abstraction. Formally, a skill                                                                       or Operator. The Designer operates within a generate–verify–
is a self-contained tool-callable module that encapsulates a                                                                             repair loop in which violations are injected back as targeted
specific verification or planning capability. It is represented                                                                          feedback for the next attempt, and a final safety gate rejects
as a tuple ξ = (name, desc, Θ, fξ ), in which name ∈ Σ∗                                                                                  any output that does not satisfy K. Section III-C details the
denotes a unique identifier, desc ∈ Σ∗ denotes a natural-                                                                                implementation of the Designer.
language description exposed to the LLM for tool selection,                                                                                 Inspector Agent (Symbolic) performs deterministic con-
Θ denotes a JSON Schema that specifies the input parameter                                                                               straint verification and assembly sequencing without using an
space, and fξ : Θ → R denotes the execution function that                                                                                LLM:
maps validated inputs to a structured result. The result space                                                                                         ξverify : C → R, ξseq : C → (C ∗ , σ ∗ )    (19)
R is defined as
                                                                                                                   ∗                     ξverify implements the verifier V (C, K) over the six feasibility
           R = {S UCCESS, FAILURE, PARTIAL} × D × 2Σ                                                                            (17)
                                                                                                                                         constraints defined in Section II, returning either pass or a
where the first component is the execution status, D is the                                                                              violation set E ⊆ K that is fed back to the Designer. ξseq
skill-specific result data (e.g., a generated layout, an assembly                                                                        derives the assembly order σ ∗ via topological sort of a support-
sequence, or a trajectory record), and the third component                                                                               induced graph with gripping-feasibility filtering. The detailed
is a set of error descriptions returned on failure or partial                                                                            implementation is shown in Section III-E.
completion. Each result r ∈ R is serialized in JSON and                                                                                     Operator Agent (Reactive) serves as the robot execution
returned to the LLM via the tool role message.                                                                                           interface between the symbolic task plan and the physical
   A skill registry Ξ = {ξ1 , . . . , ξm } manages all available                                                                         robot system, both in commissioning in digital twin and real-
skills. It generates tool schemas T OOLS(Ξ) and dispatches tool                                                                          world execution. It executes step k through ξexecute , records
                                                                                                                                    5



Algorithm 1 Multi-Agent Orchestration with SDI Harness               not satisfy K, so the module returns either a fully feasible
Require: l ∈ L, agents {aorch , ades , ainsp , aop }, human inter-   C or a FAILURE signal. Within this paradigm we instantiate
    face hDT                                                         two strategies that differ only in how the repair loop is
Ensure: Motion task completed or FAILURE                             scheduled: an adaptive constraint-guided strategy with a fixed
 1: ˆ
    l ← aorch .ξspec (l) {Specifier expands command}                 control flow and a single LLM call per retry, and an agentic
 2: C ← ades .ξgenerate (ˆ l) {Designer generates layout}            skill-based strategy in which the Designer Agent dynamically
 3: (C ∗ , σ ∗ ) ← ainsp .ξverify and seq (C) {Inspector verifies}   decides which skills (composite or granular verifiers, layout
 4: while verification failed do                                     modifications) to invoke within an episode. We present the
 5:    C ← ades .ξmodify (C, errors) {Designer replans}              two strategies in turn.
 6:    (C ∗ , σ ∗ ) ← ainsp .ξverify and seq (C) {Re-verify}            Rather than conditioning the LLM on the full constraint
 7: end while                                                        set K, we provide only the violated constraints as feedback.
 8: C ′ ← hDT .request review(C ∗ ) {Human reviews in digital        At retry t, the prompt is augmented with ϕ(E (t−1) ), yielding
    twin}                                                            C (t) = fθ (ˆl; ϕ(E (t−1) )), where the constraint selector ϕ :
 9: if human modified layout then                                    2K → 2K (|ϕ(E)| ≪ |K|) returns only the constraints
10:    (C ∗ , σ ∗ ) ← ainsp .ξverify and seq (C ′ ) {Re-verify}      relevant to the current errors E. The verifier V : C × K →
11: end if                                                           {(pass, ∅), (fail, E)} acts as a deterministic critic. We build a
12: hDT .pre execute preview(σ ∗ ) {Pre-execution digital-twin       minimal prompt sminimal = [system] + [few-shot] + [command]
                                                                                                  (t)
    simulation}                                                      for the first attempt, and sretry = sminimal + [error] + ϕ(E) for
13: for each step k in σ ∗ do                                        retries. The loop terminates when verification passes or after
14:    (Qplan       exec
            k , Qk , sk ) ← aop .ξexecute (k)                        Tmax iterations (Algorithm 2).
15:    if sk = failure then
16:        C ← aorch .ξrecover (C, ek ) {Apply recovery skill}       Algorithm 2 Adaptive Constraint-Guided Inference Loop
17:        (C ∗ , σ ∗ ) ← ainsp .ξverify and seq (C) {Re-verify}
                                                                     Require: ˆl ∈ L̂, K, Tmax
18:        if re-verification failed then
                                                                     Ensure: feasible C ∈ C or FAILURE
19:           Orchestrator chooses retry, Designer replan, or
                                                                      1: prompt ← BuildMinimalPrompt(ˆ l)
              human escalation
                                                                      2: for t = 1 to Tmax do
20:        end if
                                                                      3:   C ← fθ (prompt)
21:    end if
                                                                      4:   (status, E) ← V (C, K)
22: end for
                                                                      5:   if status = pass then
23: return Motion task completed with trajectory records
                                                                      6:      return C
                                                                      7:   end if
                                                                      8:   prompt ← BuildRetryPrompt(ˆl, E, ϕ(E), C)
Qplan
  k    and Qexec
              k , and reports a structured failure event ek =         9: end for
(stepk , cube id, error type, target pose) when execution fails.     10: return FAILURE
   Agents communicate via a message bus with typed mes-
sages m = (sender, receiver, type, payload, id). Human inter-
                                                                        The adaptive constraint-guided loop in Algorithm 2 uses
action is handled separately through direct Orchestrator calls
                                                                     a fixed control flow with one LLM call per retry. To enable
with the digital twin. When the Operator reports a failure
                                                                     more flexible behavior, the Designer Agent replaces this fixed
ek , the Orchestrator first tries recovery skills and sends the
                                                                     schedule with an LLM-driven loop that selects skills defined
corrected layout to the Inspector for re-verification. If recovery
                                                                     in Section III-B through the function-calling interface [21].
fails, it selects among retry, Designer replanning via ξmodify ,
and human escalation. The complete pipeline is summarized               To     this    end,     we      maintain       a   conversa-
in Algorithm 1.                                                      tion state M             =       (m1 , m2 , . . .) with roles
                                                                     {system, user, assistant, tool}. The system message
                                                                     contains the base planning prompt sminimal together with skill
C. Agentic Target Structure Design Generation                        instructions and tool definitions.
   This subsection addresses Sub-problem 1 (Target Structure            At each step t, the LLM receives the full conversation
Design Generation): given a structured specification ˆl ∈ L̂,        context and the tool definitions:
generate a physically feasible configuration C ∈ C that
satisfies the full constraint set K.                                                  m̂t = fθ (M<t , T OOLS(Ξ))                 (20)
   The design module follows a common generate–verify–
                                                                       The response m̂t takes one of two forms:
repair paradigm that drives constraint satisfaction. The LLM
proposes a candidate layout C ∈ C; the symbolic verifier               1) A tool call m̂t = (name, args), in which case the frame-
V (C, K) either accepts it or returns a violation set E ⊆ K;              work executes r = D ISPATCH(Ξ, name, args), appends
and the violations are injected back as targeted feedback that            the result to M, and continues.
constrains the next attempt. This generate–verify–repair cycle         2) A text response, in which case the framework extracts
repeats until either V (C, K) = pass or a step budget Tmax is             the final layout C and terminates the loop.
exhausted, and a final safety gate rejects any output that does        Regardless of the intermediate tool sequence, the framework
6



Algorithm 3 Skill-based Pipeline of Designer Agent                step reduces uncertainty before downstream task and motion
Require: ˆl ∈ L̂, skill registry Ξ, step budget Tmax              planning.
Ensure: feasible C ∈ C or FAILURE                                    Beyond human adjustment, the digital twin also supports
 1: M ← [system : sminimal + S KILL I NSTRUCTIONS]                commissioning-oriented validation. Given C ′ and a planned
 2: M ← M ⊕ [user : ˆ      l]                                     robotic trajectory Qplan , it can perform collision, reachability,
 3: for t = 1 to Tmax do                                          and rule-based safety checks. These checks provide feedback
 4:    m̂t ← fθ (M, T OOLS(Ξ)) {LLM call with tools}              to either the previous design loop or the later motion planner.
 5:    if m̂t contains tool calls then                               During deployment, execution data can be streamed back to
 6:       M ← M ⊕ [assistant : m̂t ]                              the digital twin, yielding Qexec . The same environment is then
 7:       for each tool call (nj , aj ) in m̂t do                 used to quantify deviations and trigger alarms or replanning
 8:          rj ← D ISPATCH(Ξ, nj , aj ) {Execute skill}          when thresholds are exceeded (cf. (6) and (7)). Formally, the
 9:          M ← M ⊕ [tool : S ERIALIZE(rj )]                     digital twin provides a shared visualization and monitoring
10:       end for                                                 space Z into which both planned and executed trajectories
11:    else                                                       are projected:
12:       C ← E XTRACT L AYOUT(m̂t ) {Agent done}                               ηDT : Q → Z,          ηreal : Q → Z,           (23)
13:       if C ̸= NULL then
14:          break                                                where ηDT renders planned trajectories Qplan for pre-execution
15:       end if                                                  commissioning and ηreal projects executed trajectories Qexec
16:       M ← M ⊕ [user : “Output final JSON”]                    for in-loop monitoring, closing the feedback loop described in
17:    end if                                                     (16).
18: end for                                                          In the multi-agent pipeline, the human interacts through the
19: {Safety check: always verify final output}                    digital twin at three points: (1) generated design structure
20: if C ̸= NULL and V (C, K) = pass then                         review after the Inspector verifies a layout, where the human
21:    return C                                                   may adjust object positions by direct manipulation (triggering
22: end if                                                        re-verification); (2) pre-execution commissioning and confir-
23: return FAILURE                                                mation where the planned robotic trajectory is visualized in
                                                                  the digital twin before real execution; and (3) failure report
                                                                  when the Operator reports an execution failure that automatic
always performs a final safety check:                             replanning cannot resolve. Overall, the digital twin makes the
                  (                                               pipeline more interpretable and auditable while reducing trial-
                    C            if V (C, K) = pass               and-error on physical industrial robots.
         Cfinal ←                                          (21)
                    FAILURE otherwise
                                                                  E. Symbolic Assembly Sequencing
This guarantees physical feasibility even if the agent skips         While the agentic design loop may invoke the sequencing
verification or misuses skills. The complete agent loop is        skill ξseq during target structure design generation, this module
formalized in Algorithm 3.                                        applies the same algorithm deterministically to the human-
   If the safety gate in Algorithm 3 passes, the module returns   adjusted layout C ′ to obtain the final assembly order σ ∗ . It
a layout C ∈ C that is guaranteed to satisfy every constraint     enforces the physical dependencies induced by contact and
in K, which is then passed to the remaining pipeline modules;     support relations and rejects orders that violate the constraints
otherwise the episode terminates with a FAILURE signal that is    in Section II.
handed back to the Orchestrator for recovery (Section III-B).        Writing ci ≺ cj as shorthand for the antecedent of Con-
                                                                  straint 1 (9), we build a directed acyclic graph (DAG) with one
D. Human-in-the-Loop Verification and Adjustment via              node per object and one directed edge per support relation:
Digital Twins                                                           Gd = (V, Ed ),     Ed = {(vi → vj ) : ci ≺ cj }.       (24)
   The digital twin provides a geometry-consistent interface      We therefore define the symbolic sequencer as
between planning and real-world deployment [22], [23]. In
our method, it serves as (i) a human-AI interface, (ii) a                     gsym : C ′ → C ∗ ,   σ ∗ = TopoSort(Gd ),        (25)
commissioning environment for designed structure and robotic      where any topological ordering of Gd respects gravity and
trajectories, and (iii) a monitoring layer for the physical       structural dependencies. In practice, we implement this by
system.                                                           iterative sink-node removal: each extracted sink yields a dis-
   The human adjustment step is modeled as                        assembly order, which is then reversed to obtain σ ∗ . We use
                   hDT : C × Ihuman → C ′ ,                (22)   C ∗ ≜ (C ′ , σ ∗ ) to denote the sequenced configuration.
                                                                     Among the valid sink-node orderings, we select one that
where Ihuman denotes human input through visual inspection        also satisfies gripping feasibility (13): a sink node is added
and direct manipulation in the digital twin. Typical operations   only if at least one lateral grip direction β ∈ {x, y} remains
include translating or rotating objects, inserting or removing    unblocked. If no grippable sink node exists, the planner reports
components, and resolving ambiguous spatial relations. This       failure. The full procedure is given in Algorithm 4.
                                                                                                                                                           7



Algorithm 4 Symbolic Assembly Sequencing                                                                      TABLE I
Require: C ′ (layout), K (constraints)                                                                H ARDWARE C ONFIGURATION
Ensure: σ ∗ (feasible assembly sequence) or FAILURE                          Robot / Gripper        Firmware                    Protocol     Update Rate
 1: Gd ← BuildDAG(C ′ ) {Edges from ≺}                                       ABB IRB120             ABB RobotWare 5.15          ABB PCSDK    50 Hz
 2: σdis ← []                                                                ABB IRB1600            ABB RobotWare 6.13          ABB EGM      250 Hz
                                                                             OnRobot 2FG7           –                           Modbus       2 Hz
 3: while Gd ̸= ∅ do
                                                                             OnRobot VGC10          –                           Modbus       2 Hz
 4:   F ← {v ∈ Gd : out-degree(v) = 0} {Sink nodes}
 5:   if F = ∅ then
                                                                                 ABB IRB120
 6:      return FAILURE {Circular dependency}
                                                                                                                 OnRobot 2FG7
 7:   end if
 8:   c ← first grippable node in F {cf. (13)}                                          OnRobot VGC10
 9:   if no grippable node in F then
10:      return FAILURE {No feasible grip}
11:   end if
12:   append c to σdis ; remove c from Gd
13: end while
14: return σ ∗ ← reverse(σdis )
                                                                                      Digital twin in Unity 3D                              ABB IRB1600



                                                                            Fig. 3. Experimental setup of the dual-arm robotic system.
F. Motion Planning, Commissioning, and Monitoring via
Digital Twins
  Given the sequenced configuration C ∗ , the task generation                  If Vtraj (Qplan , Qexec ) = fail, the system can (i) pause or stop
operator                                                                    execution, (ii) request human inspection via the digital twin, or
                     τtask : C ∗ → T                     (26)               (iii) replan the remaining actions from the current robot state.
                                                                            This makes commissioning auditable and reduces the risk of
produces a sequence T = (a1 , . . . , aK ) of atomic manipula-
                                                                            silently drifting away from the validated plan.
tion actions, each specifying the object, the assigned robot,
and the required end-effector poses. For each action, the robot
                                                                                                          IV. E XPERIMENTS
is assigned according to workspace reachability, and approach
and retreat waypoints are generated to avoid collisions.                    A. Experimental Setup
   The motion planning operator then maps task actions to                      The system runs on a dual-arm robotic station comprising
joint-space trajectories:                                                   an ABB IRB120 (OnRobot VGC10 vacuum gripper) and an
                                    K
                                    M                                       ABB IRB1600 (OnRobot 2FG7 parallel gripper), as shown
   ρmotion : T → Q,       Qplan =         fmp (ak , xrobot
                                                     k     , Ek ),   (27)   in Fig. 3 and detailed in Table I. The software stack runs
                                    k=1                                     on Ubuntu Linux 22.04 with ROS 2 (Humble), ros2 control
                                                                            2.43.1, MoveIt 2, and Unity3D 2021.3.22f1. All LLM calls
where xrobot
         k    is the current robot state, Ek is the collision
                                                                            use GPT-4o-mini (temperature 0.3). We use “end-to-end” to
scene, and ⊕ denotes time-ordered trajectory concatenation.
                                                                            refer to the complete system pipeline from natural language
The framework is planner-agnostic. In our implementation, we
                                                                            to physical assembly.
use MoveIt with RRTConnect, although other planners may
                                                                               We evaluate on 70 natural-language commands organized
also be used.
                                                                            into five difficulty groups: A (13 commands, 3–15 steps): well-
   To reflect the bidirectional nature of a digital twin, we
                                                                            defined structures with explicit dimensions; B (15 commands,
include a runtime commissioning and monitoring module that
                                                                            5–15 steps): under-specified or vague instructions and patterns
closes the loop between the planned and measured trajecto-
                                                                            requiring semantic grounding; C (12 commands, 7–16 steps):
ries. The digital twin is continuously synchronized with the
                                                                            enclosed and dense structures stressing physical feasibility; D
physical robot state and uses the same scene representation as
                                                                            (18 commands, 6–20 steps): 3D packing and open-ended com-
planning for online verification.
                                                                            mands combining scale with ambiguity; and E (12 commands,
   During execution, the robot controller publishes joint en-
                                                                            13–25 steps, avg. 19.2): scale stress, structural complexity, and
coder readings at 50–250 Hz. We define a synchronization
                                                                            recovery stress that exceed Group D in both step count and
operator
                                                                            constraint density.
                    ψsync : z(t) 7→ q exec (t),           (28)
                                                                               Table II groups the ten methods in three paradigms. Non-
where z(t) denotes the telemetry at time t and q exec (t) ≜                 agentic baselines (no skill registry) differ in feedback: LLM-
(q1exec (t), . . . , qR
                      exec
                           (t)) is the multi-robot joint configuration.     Direct [12], [13] (one pass), LLM-FullPrompt (full K in
                 plan
   Given Q             and Qexec , we evaluate the deviation metric         prompt), LLM-FixedLoop [24] (retry with full feedback), LLM-
δ(Qplan , Qexec ) in (6) and apply the pass/fail rule Vtraj (·, ·) in       AdaptLoop (retry with violated subset ϕ(E), Algorithm 2).
(7). Because Qplan is time-parameterized, we compare qrexec (t)             Single-agent tool-use methods wrap one LLM in a function-
and qrplan (t) after nearest-neighbor timestamp alignment for               calling loop: Single-Agent Single-Skill (SASS, one composite
each robot r.                                                               verifier) and Single-Agent Multi-Skill (SAMS, eight granular
8



    Digital twin in Unity 3D                          Human
                                                      Adjust
                                                      Panel


                                                                                                commissioning in digital twin




                                                                                                   execution in real world




                         Generated Structure Design



Fig. 4. Digital-twin, human-AI interface, robot motion commissioning and execution.



                                  TABLE II                                                             TABLE III
                       S UMMARY OF C OMPARED M ETHODS                        M AIN R ESULTS : S UCCESS R ATE (%) BY D IFFICULTY L EVEL AND
                                                                                                   G ENERATION T IME
      Method                         Paradigm         Skills Orch.
      LLM-Direct [12], [13]          Single-pass        –      –             Method           A     B     C     D Overall Gen. Orch.
      LLM-FullPrompt                 Prompt eng.        –      –                             (13) (15) (12) (18) (58)      (s)
      LLM-FixedLoop [24]             Fixed feedback     –      –             LLM-Direct     100.0 93.3 91.7 55.6 82.8 14.9        –
      LLM-AdaptLoop                  Adaptive feedback –       –             LLM-FullPrompt 100.0 73.3 75.0 55.6 74.1 25.1        –
      SASS                           Tool-use           1      –             LLM-FixedLoop 100.0 86.7 83.3 66.7 82.8 31.5         –
      SAMS [25], [26]                Tool-use           8      –             LLM-AdaptLoop 100.0 100.0 91.7 83.3 93.1 23.7        –
      MultiAgent-RuleOrch [14], [27] Multi-agent        6    Rule            SASS           100.0 100.0 100.0 72.2 91.4 58.6      –
      Ours-PGEOrch                   Multi-agent        6    PGE             SAMS           100.0 100.0 83.3 88.9 93.1 55.9       –
      Ours-LGOrch                    Multi-agent        6     LG             Ours-Hybrid    100.0 100.0 100.0 100.0 100.0 85.3 PGE+LG
      Ours-Hybrid                    Multi-agent       6+R PGE+LG



tools) [25], [26]. Multi-agent methods share four agents and              C. Ablation Study
six skills, differing in command grounding, control flow, and
recovery: MultiAgent-RuleOrch [14], [27] uses raw commands,                  Table IV ablates the multi-agent components across all 70
a hardcoded if-else state machine, and rule-based replan; Ours-           commands. Ours-PGEOrch is strong on Group D (94.4%)
PGEOrch adds the full Specifier-Designer-Inspector (inspired              where the Specifier disambiguates open-ended commands but
from PGE) harness with a fixed PGE loop; Ours-LGOrch                      drops on Group C (83.3%) where over-constrained specifica-
drops the Specifier (raw commands) and instead routes via a               tions limit layout flexibility. Ours-LGOrch is the converse, best
LangGraph state machine; Ours-Hybrid combines both axes                   on C (100%) but weaker on D (95.5%) where raw commands
(Specifier + LangGraph) and adds the geometric recovery                   lack detail. Ours-Hybrid attains 100% on all five tiers with
skills ξflatten , ξshift . Generation time averages all commands          the shortest multi-agent generation time (85.3 s), indicating
(success and failure alike). Failed runs contribute their full            Specifier grounding upfront reduces replan cycles.
elapsed time, bounded by a 300 s per-phase timeout and up to                 The last row, Ours-Hybrid-LLMCritic, isolates the In-
3 replan attempts.                                                        spector axis and directly validates the neuro-symbolic de-
                                                                          sign adopted in this work. Replacing the symbolic Inspector
B. Main Results                                                           with an equivalently-prompted LLM (52-command subset of
                                                                          Groups A–D) collapses overall success from 98.1% to 3.8%,
   Table III presents success rates across all four diffi-
                                                                          with 0% on Groups C and D and a 4× generation-time
culty levels and all compared methods. The proposed Ours-
                                                                          blowup (85.3 s→319.0 s) caused by unreliable LLM verdicts
Hybrid method is the only one achieving 100% across all
                                                                          triggering replan storms. Unlike code review, robotic applica-
four difficulty levels, outperforming both non-agentic and
                                                                          tions demand exact geometric and kinematic verification with
single-agent baselines. Among non-agentic methods, LLM-
                                                                          hard numerical thresholds. The generic harness pattern (an
AdaptLoop (93.1%) outperforms LLM-FixedLoop (82.8%),
                                                                          LLM commonly fills the Evaluator role) transfers to industrial
confirming that adaptive constraint injection is more effec-
                                                                          robotics only when its critic is replaced by a deterministic
tive than a fixed feedback schedule, while SAMS (93.1%)
                                                                          symbolic verifier. This confirms that the neuro-symbolic split
achieves comparable overall accuracy by benefiting from ex-
                                                                          adopted here, which restricts the LLM to language understand-
plicit symbolic verification at each step. Group D is the most
                                                                          ing and generation while delegating verification to a symbolic
discriminating: all baselines fall below 90% (with the weakest
                                                                          agent, is the architecture that makes the harness effective for
reaching only 55.6%), whereas agentic methods with granular
                                                                          this task class.
skills sustain 72–89%, confirming that open-ended, large-scale
assembly tasks require the structured planning and multi-agent
coordination provided by Ours-Hybrid.
                                                                                                                                                 9



                            TABLE IV                                                                TABLE VI
 C OMPONENT A BLATION : S UCCESS R ATE (%) BY D IFFICULTY L EVEL                D ETERMINISTIC FAILURE R ECOVERY (10 S CENARIOS )

Method                  A     B     C     D     E Overall Gen. Msgs       Scenario                        Error Type Rule PGE LG Hyb
                       (13) (15) (12) (18) (12) (70)       (s)            Workspace boundary (x>0.6)      IK failure     ✓    ✓    ✓     ✓
MultiAgent-RuleOrch 100.0 100.0 83.3 77.8 66.7 85.7 59.4 5.6              Height limit (z>0.15)          Self-collision ×     ×    ✓     ✓
Ours-PGEOrch          100.0 100.0 83.3 94.4 91.7 94.3 130.3 6.5           IK singularity (center)         Singularity    ×    ×    ✓     ✓
Ours-LGOrch           100.0 100.0 100.0 95.5 91.7 97.4 125.0 6.9          Env collision (y>0.4)            Collision     ✓    ×    ✓     ✓
Ours-Hybrid           100.0 100.0 100.0 100.0 100.0 100.0 85.3 6.4        Combined (boundary + height)     Multiple      ✓    ✓    ✓     ✓
Ours-Hybrid-LLMCritic 7.1    5.9   0.0   0.0    –    3.8 319.0 22.0       Narrow corridor (x∈[0.3, 0.4]) Constrained ×        ×    ✓     ×
                                                                          Low ceiling (z>0.08)           Self-collision ✓     ×    ✓     ✓
                                                                          Y-band (y ∈[0.23,
                                                                                     /      0.37])       Env collision ✓      ×    ✓     ✓
                          TABLE V                                         Diagonal obstacle (x+y>0.7) Env collision ×         ×    ✓     ✓
 D ETECTION AND C ORRECTION OF I NVALID H UMAN M ODIFICATIONS             Corner pocket (small area)       Multiple      ×    ×    ✓     ✓
 Human Modification                  Type Steps Rule PGE LG Hyb           Total                                         5/10 2/10 10/10 9/10
 Move cube to x=1.0 in tower         WS     3    ✓    ✓    ✓     ✓        Rate (%)                                      50.0 20.0 100.0 90.0
 Move row to y=0.01 in wall          WS     9    ✓    ✓    ✓     ✓
 Move pillar to x=0.85 in canopy WS 21           ×    ×    ✓     ✓
                                                                                                    TABLE VII
 Stack two cubes at same position Col       6    ✓    ✓    ✓     ✓
                                                                          M OTION P LANNING V ERIFICATION (12 C OMMANDS , G ROUPED BY
 Overlap cubes in dense block        Col 12      ×    ✓    ✓     ✓
                                                                                                   C ATEGORY )
 Remove middle cube from tower Grav 5            ✓    ✓    ✓     ✓
 Remove pillar from bridge           Grav 5      ✓    ✓    ✓     ✓       Category (Commands)    Cubes         Arms           Speedup      Pass
 Reverse staircase assembly order    Seq    8    ✓    ✓    ✓     ✓       Simple single-arm (6)   3–5         IRB120            1.0×       6/6
 Place roof before pillars in canopy Seq 21      ✓    ✓    ✓     ✓       Complex single-arm (3)  5–6         IRB120            1.0×       3/3
 Total                                          7/9 8/9 9/9 9/9          Dual-arm (3)            5–6     IRB120+IRB1600      1.0–1.7×     3/3
 Rate (%)                                       77.8 88.9 100.0 100.0    Total                   3–6            –           up to 1.7×   12/12



D. Failure Recovery                                                     preview with a semi-transparent robot model (top), real-robot
   We evaluate two recovery scenarios: human-initiated mod-             execution upon human approval (middle), and a completed
ifications in the digital twin (Table V) and deterministic              three-cube pyramid (bottom).
motion-planning failures injected during execution (Table VI).             All 12 designs yield valid inverse kinematics and collision-
   For human modifications, the operator introduces nine viola-         free trajectories, and the three dual-arm commands confirm
tions spanning four types including workspace boundary (WS),            correct allocation between the IRB120 and IRB1600, achiev-
collision (Col), gravity support (Grav), and assembly order             ing up to 1.7× speedup through parallel execution. Since
(Seq) across structures of 3–21 assembly steps. All methods             trajectory following is a mature problem in industrial robotics,
recover simple cases (≤ 9 steps). Failures concentrate on               we observed no significant deviation between planned and
complex structures where rule-based replanning collapses (the           executed trajectories; the robots reliably tracked the planned
12-step dense block, the 21-step canopy workspace violation),           paths within nominal control accuracy. The system outputs
with only Ours-LGOrch and Ours-Hybrid succeeding on all                 an executable Python script in the robot frame for each
nine.                                                                   command, deployable directly on physical hardware without
   For deterministic execution failures, ten blocked regions            modification.
force structural replanning. Ours-Hybrid combines two mech-
anisms: dedicated recovery skills (ξflatten , ξshift ) bypass the                                V. D ISCUSSION
Designer to feed corrected layouts directly to the Inspector,              Three findings emerge from the ablation study. First, the
and adaptive Specifier-relaxation reverts to the raw command            Specifier handles ambiguity grounding. Without it, perfor-
after repeated failures. MultiAgent-RuleOrch (5/10) handles             mance drops to 95.5% on Group D, confirming that ambiguous
only workspace and collision failures; Ours-PGEOrch (2/10) is           commands require structured grounding before generation.
further limited by Specifier over-constraining during recovery.         Second, LangGraph handles failure-aware workflow. Without
Notably, Ours-LGOrch (10/10) surpasses Ours-Hybrid (9/10)               it, performance drops to 83.3% on Group C, confirming
on the narrow-corridor scenario, where the 0.14 m valid band            that fixed orchestration cannot adapt to the diverse failure
is too tight for reliable LLM coordinate generation under the           modes of enclosed and dense structures. Third, adaptive rout-
expanded specification.                                                 ing handles execution-level recovery. Without it, MultiAgent-
                                                                        RuleOrch and Ours-PGEOrch recover only 5/10 and 2/10
E. Physical Deployment and Real-world Validation                        of injected failures respectively, while LangGraph routing in
  We execute 12 commands through the full motion plan-                  Ours-LGOrch and Ours-Hybrid recovers 9–10/10. Dedicated
ning and control pipeline to verify trajectory feasibility and          geometric recovery skills (ξflatten , ξshift ) provide an additional
dual-arm task allocation (Table VII). Fig. 4 illustrates the            layer for known geometric failure patterns.
complete commissioning workflow: the Unity3D digital twin                  The SDI harness and LangGraph routing address orthogo-
and human-AI interface (left) lets the operator issue typed             nal aspects of the problem. SDI defines role decomposition
commands and refine the layout by adding, removing, or                  (Specifier for language understanding, Designer for structure
mouse-dragging cubes; the right panel shows pre-execution               design generation, Inspector for constraint verification), while
10



LangGraph defines the control flow that routes between agents                    [5] H. Fan, X. Liu, J. Y. H. Fuh, W. F. Lu, and B. Li, “Embodied intelligence
on failure. Replacing the LLM-based critic of the generic                            in manufacturing: Leveraging large language models for autonomous
                                                                                     industrial robotics,” Journal of Intelligent Manufacturing, vol. 36, no. 2,
harness pattern with a deterministic symbolic Inspector pre-                         pp. 1141–1157, Feb. 2025.
serves the harness structure while providing the physical-                       [6] I. Kadri, S. A. Selouani, M. Ghribi, R. Ghali, and S. Mekhoukh, “LLM-
feasibility guarantees industrial deployment requires. The de-                       driven agent for speech-enabled control of industrial robots: A case study
                                                                                     in snow-crab quality inspection,” Results in Engineering, vol. 27, p.
terministic failure recovery experiment (Table VI) exposes a                         106660, Sep. 2025.
Specifier trade-off: the same structure that grounds ambiguous                   [7] L. Li, Z. Chen, and Z. Kan, “Environment-driven and LLM-guided
commands over-constrains the search space during recovery.                           multi-robot task inference and allocation under temporal logic speci-
                                                                                     fications,” IEEE Transactions on Automation Science and Engineering,
PGEOrch reaches only 2/10 because the Specifier locks in                             vol. 23, pp. 2925–2940, Jan. 2026.
geometric assumptions that conflict with the failure-triggering                  [8] Y. Tsushima, S. Yamamoto, A. A. Ravankar, J. V. S. Luces, and
constraints, and LGOrch (10/10) even surpasses Hybrid (9/10)                         Y. Hirata, “Task planning for a factory robot using large language
                                                                                     model,” IEEE Robotics and Automation Letters, vol. 10, no. 3, pp. 2383–
by exploiting raw commands directly. Hybrid attains 9/10 via                         2390, Mar. 2025.
an adaptive Specifier-relaxation mechanism that reverts to the                   [9] Z. Wang, X. Zhou, J. Mao, C. Zhang, C. Cui, and J. Yang, “LLM-
raw command after repeated failures. SAMS (93.1%) does not                           MTMP: A large language model-based multi-agent task and motion
consistently outperform SASS (91.4%), suggesting that tool-                          planning framework for power inspection robots,” Journal of Industrial
                                                                                     Information Integration, vol. 49, p. 101014, Jan. 2026.
set size alone is insufficient and that structured multi-agent                  [10] L. Xia, Y. Hu, J. Pang, X. Zhang, and C. Liu, “Leveraging large
orchestration is the primary driver of performance on complex                        language models to empower Bayesian networks for reliable human-
tasks.                                                                               robot collaborative disassembly sequence planning in remanufacturing,”
                                                                                     IEEE Transactions on Industrial Informatics, vol. 21, no. 4, pp. 3117–
   As for limitation, the current system assumes known supply-                       3126, Apr. 2025.
area positions, and visual perception for object localization                   [11] C. R. Garrett, R. Chitnis, R. Holladay, B. Kim, T. Silver, L. P. Kaelbling,
was not integrated because it is out of the scope of this study.                     and T. Lozano-Pérez, “Integrated task and motion planning,” Annual
                                                                                     Review of Control, Robotics, and Autonomous Systems, vol. 4, no. 1,
Hybrid averages 85.3 s per command due to multi-agent com-                           pp. 265–293, May 2021.
munication and LLM API calls, which are time-consuming                          [12] A. Brohan, Y. Chebotar, C. Finn, K. Hausman, A. Herzog, D. Ho,
and expensive; lighter models or cached Specifier outputs may                        J. Ibarz, A. Irpan, E. Jang, R. Julian et al., “Do as I can, not as I say:
                                                                                     Grounding language in robotic affordances,” in Conference on Robot
reduce this overhead in latency-sensitive deployments.                               Learning. PMLR, 2023, pp. 287–318.
                                                                                [13] J. Liang, W. Huang, F. Xia, P. Xu, K. Hausman, B. Ichter, P. Florence,
                                                                                     and A. Zeng, “Code as policies: Language model programs for embodied
                         VI. C ONCLUSIONS                                            control,” in 2023 IEEE International Conference on Robotics and
   This paper presented an agentic neuro-symbolic planning                           Automation (ICRA). IEEE, 2023, pp. 9493–9500.
                                                                                [14] Q. Wu, G. Bansal, J. Zhang, Y. Wu, B. Li, E. Zhu, L. Jiang, X. Zhang,
and commissioning framework for human-in-the-loop indus-                             S. Zhang, J. Liu et al., “Autogen: Enabling next-gen LLM applications
trial robotics. The proposed system integrates a Specifier-                          via multi-agent conversations,” in First Conference on Language Mod-
Designer-Inspector (SDI) harness framework, symbolic con-                            eling, 2024.
                                                                                [15] G. I. Rashed, A. O. Bahageel, H. A. I. Gony, A. Badjan, and H. I.
straint verification, LangGraph-based dynamic orchestration,                         Shaheen, “Ai-driven multi-agent demand response framework for resi-
domain-specific recovery skills, and a Unity3D digital twin                          dential load optimization using CrewAI,” in 2025 IEEE 20th Conference
for human review. Across 70 natural-language commands                                on Industrial Electronics and Applications (ICIEA). IEEE, 2025, pp.
                                                                                     1–10.
spanning five difficulty levels, the proposed method achieved                   [16] S. Mandulapalli, E. Hernandez, W. J. Hall, A. Chakeri, and L. Jaimes,
100% success, showing that symbolic grounding, adaptive                              “Development of agentic workflows with LangGraph for software de-
routing, and human oversight are all essential for reliable                          velopment life cycle automation,” in North American Conference on
                                                                                     Industrial Engineering and Operations Management-Computer Science
performance on open-ended tasks. Future work will extend                             Tracks. Springer, 2025, pp. 45–54.
the framework to heterogeneous parts, integrate vision-based                    [17] Anthropic, “Harness design for long-running apps,” Anthropic
localization, and investigate adaptive skill selection to reduce                     Engineering Blog, 2026. [Online]. Available: https://www.anthropic.
                                                                                     com/engineering/harness-design-long-running-apps
generation time without sacrificing success rate.                               [18] P. Hitzler, A. Eberhart, M. Ebrahimi, M. K. Sarker, and L. Zhou, “Neuro-
                                                                                     symbolic approaches in artificial intelligence,” National Science Review,
                                                                                     vol. 9, no. 6, p. nwac035, Jun. 2022.
                               R EFERENCES
                                                                                [19] M. Singh, N. Gupta, S. Tyagi, A. Rani, V. Kumar, and S. Sharma, “To-
 [1] I. Rojek, D. Mikołajewski, A. Piszcz, O. Małolepsza, and M. Kozielski,          wards neural-symbolic grammatical inference for endangered languages
     “Role of Generative AI in AI-based digital twins in Industry 5.0 and            using integrating graph neural networks and instruction-tuned language
     evolution to Industry 6.0,” Applied Sciences, vol. 15, no. 18, p. 10102,        models,” Engineering Applications of Artificial Intelligence, vol. 168, p.
     Jan. 2025.                                                                      114011, Mar. 2026.
 [2] A. Lykov, M. A. Cabrera, M. Konenkov, V. Serpiva, K. F. Gbagbe,            [20] J. Mao, J. B. Tenenbaum, and J. Wu, “Building intelligent agents with
     A. Alabbas, A. Fedoseev, L. Moreno, M. H. Khan, Z. Guo, and                     neuro-symbolic concepts,” Commun. ACM, vol. 69, no. 2, pp. 69–79,
     D. Tsetserukou, “Industry 6.0: New generation of industry driven by             Jan. 2026.
     Generative AI and swarm of heterogeneous robots,” in 2025 IEEE/RSJ         [21] M. Wang, Y. Zhang, B. Yu, B. Hao, C. Peng, Y. Chen, W. Zhou, J. Gu,
     International Conference on Intelligent Robots and Systems (IROS), Oct.         C. Zhuang, R. Guo, W. Wang, and X. Zhao, “Function calling in large
     2025, pp. 19 992–19 997.                                                        language models: Industrial practices, challenges, and future directions,”
 [3] M. Ni, T. Wang, J. Leng, C. Chen, and L. Cheng, “A large language               ACM Comput. Surv., vol. 58, no. 9, pp. 238:1–238:37, Feb. 2026.
     model-based manufacturing process planning approach under Industry         [22] Z. Liu, J. Silva, R. Zhong, Q. Qin, N. Roy, V. Nan Fernandez-Ayala,
     5.0,” International Journal of Production Research, pp. 1–20, Feb. 2025.        J. Lesko, U. Håkansson, S. Sandberg, D. V. Dimarogonas, J. Gross,
 [4] W. Dong, D. Li, Y. Ji, H. Chen, S. Liu, Z. Ma, F. Hao, Y. Ji, H. Xing,          X. Vincent Wang, and L. Wang, “ConstrucTwin: Digital twin-driven
     and P. Zheng, “Towards a next-generation LLM empowered low-code                 multirobot construction system toward Industry 5.0,” IEEE Transactions
     programming industrial robotic system for human-centric smart man-              on Systems, Man, and Cybernetics: Systems, vol. 56, no. 4, pp. 2924–
     ufacturing,” Journal of Manufacturing Systems, vol. 83, pp. 675–686,            2939, Apr. 2026.
     Dec. 2025.                                                                 [23] Z. Liu, S. Liu, T. Wang, L. Wang, and X. V. Wang, “Establishment and
                                                                               11



     synchronisation of digital twins for multi-robot systems in manufactur-
     ing,” Procedia CIRP, vol. 134, pp. 419–424, 2025.
[24] W. Huang, F. Xia, T. Xiao, H. Chan, J. Liang, P. Florence, A. Zeng,
     J. Tompson, I. Mordatch, Y. Chebotar et al., “Inner monologue: Embod-
     ied reasoning through planning with language models,” in Conference
     on Robot Learning. PMLR, 2023, pp. 1769–1782.
[25] N. Attolino, A. Capitanelli, and F. Mastrogiovanni, “Achieving scalable
     robot autonomy via neurosymbolic planning using lightweight local
     LLM,” arXiv preprint arXiv:2505.08492, 2025.
[26] A. Capitanelli and F. Mastrogiovanni, “A framework for neurosymbolic
     robot action planning using large language models,” Frontiers in Neu-
     rorobotics, vol. 18, p. 1342786, Jun. 2024.
[27] B. Wang, L. Zheng, Y. Wang, and Z. Qi, “LLM-based multi-agent
     task planning for human-robot collaborative assembly balancing operator
     experience and efficiency,” Journal of Manufacturing Systems, vol. 82,
     pp. 1020–1045, Oct. 2025.
