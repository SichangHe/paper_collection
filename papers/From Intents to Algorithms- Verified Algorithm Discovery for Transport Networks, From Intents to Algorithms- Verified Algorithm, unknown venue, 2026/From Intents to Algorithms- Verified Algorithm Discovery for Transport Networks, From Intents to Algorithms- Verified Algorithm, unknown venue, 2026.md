                                                                                                                                                                               1




                                               From Intents to Algorithms: Verified Algorithm
                                                     Discovery for Transport Networks
                                                                                Behnam Ojaghi, Ricard Vilalta, and Raül Muñoz
                                                                                    CTTC, Castelldefels, Barcelona, Spain
                                                                                  {bojaghi,ricard.vilalta,raul.munoz}@cttc.es



                                            Abstract—Intent-based networking decouples desired outcomes      been selected. An intent can modify objective coefficients,
                                         from device-level configuration, but most systems still map intents SLA targets, priorities, traffic demands, or constraints, but the
                                         to parameters of an algorithm selected in advance. Large language
arXiv:2609.27386v1 [cs.NI] 23 Sep 2026




                                                                                                             underlying optimization model, heuristic, or learned policy
                                         models (LLMs) create an opportunity to automate algorithm
                                         design, yet unrestricted generated code is unsuitable for transport-remains structurally fixed. Recent intent-based network-slicing
                                         network control because feasibility, reproducibility, and robustnessframeworks, for example, translate service objectives into math-
                                         must be enforced independently of the model. We present VERA-       ematical resource-allocation and conflict-resolution problems
                                         TN, a verification-guided framework that compiles a network         and adapt their parameters as network conditions change [2], [3].
                                         intent into a bounded algorithm-design specification. The target    Such approaches provide effective intent-aware optimization,
                                         architecture uses an LLM as a semantic variation operator over
                                         typed request-ordering and path-ranking programs; generated         but adaptation occurs primarily within a predefined algorithm.
                                         logic remains separated from a trusted allocator that enforces path    This distinction becomes important when the appropriate
                                         validity, latency, capacity, and single-path constraints. We prove  decision logic depends on the intent itself. Consider two feasible
                                         feasibility preservation under explicit assumptions and establish   transport policies. A latency-oriented policy may repeatedly
                                         a sufficient bound for the lexicographic latency tie-break in the
                                                                                                             choose the shortest path and concentrate traffic on a scarce cut,
                                         exact reference model. The released proof-of-concept instantiates
                                         the same interface with a bounded ten-parameter numerical           whereas a resilience-oriented policy may deliberately reserve
                                         candidate and deterministic replay, rather than a completed         that cut for critical services. Similarly, a rule that maximizes the
                                         live-LLM/AST study. Across 150 certified held-out cases on a 28-    number of admitted requests can behave differently from one
                                         node TEFNET24-derived hierarchy, evolutionary search reaches a      that maximizes priority-weighted admission, and a congestion-
                                         mean priority-utility ratio of 0.958, compared with 0.952 for equal-
                                                                                                             minimizing policy may be undesirable when reconfiguration
                                         budget random search and 0.940 for priority-greedy routing. The
                                         gain over random search is small but statistically detectable (Holm-stability becomes the dominant objective. Changing the numer-
                                         adjusted p = 0.0083). The candidate does not improve congestion     ical inputs of a fixed heuristic does not necessarily produce
                                         relative to MILP-C, and the effect of failure-aware training is     the decision structure required by these different operational
                                         inconclusive at the 0.05 level (p = 0.051). Eight discovery runs    goals.
                                         on the official national topology and replay on 12 unseen metro-
                                         regional topologies show no stable intent-specific specialization.
                                                                                                                Large language models (LLMs) create a new possibility: in-
                                         These results support the trust-boundary and numerical-evolution    stead of selecting only the output of an optimization procedure,
                                         claims but do not establish a benefit from LLM generation.          they can participate in designing the procedure itself. Recent
                                            Index Terms—Large language models, automated algorithm work on LLM-assisted algorithm design has demonstrated
                                         design, intent-based networking, transport networks, traffic engi- that language models can generate and improve executable
                                         neering, evolutionary computation, program synthesis, verification, heuristics through evaluator-driven search. FunSearch evolves
                                         network digital twin.                                               a designated function inside a predefined program skeleton [4];
                                                                                                             EoH jointly evolves heuristic ideas and executable imple-
                                                                 I. I NTRODUCTION                            mentations [5]; ReEvo uses reflective language feedback to

                                         I   NTENT-BASED networking (IBN) seeks to replace device- guide heuristic evolution [6]; and LLaMEA evolves complete
                                             level configuration with declarative descriptions of the metaheuristics from evaluation feedback [7]. More recently,
                                         outcomes that a network should achieve. Instead of specifying AlphaEvolve has demonstrated the potential of evaluator-driven
                                         individual routes, resource allocations, or controller commands, code evolution across mathematical, scientific, and systems
                                         an operator can express requirements such as preserving problems [8]. These developments suggest a progression from
                                         latency for a critical service, avoiding congested transport links,
                                         prioritizing selected service classes, or minimizing disruptive       human-designed algorithm →
                                         reconfiguration. An intent-based network system then translates,                                     LLM-assisted algorithm design.
                                         resolves, activates, and assures these requirements through a                                                                        (1)
                                         closed management loop [1]. This abstraction is particularly           Directly transferring this paradigm to transport-network
                                         attractive for beyond-5G and 6G infrastructures, where transport control is, however, problematic. A candidate algorithm can
                                         resources must support heterogeneous services whose objectives achieve a high evaluation score while still containing invalid
                                         and operating conditions evolve over time.                          logic, numerical instabilities, hidden dependencies, or op-
                                            Existing intent-driven resource-management approaches, erations that should never be available to model-generated
                                         however, typically assume that the algorithm itself has already code. More importantly, network resource allocation contains
                                                                                                                                           2



hard operational constraints. A generated procedure must                   and allows the resulting algorithm to be inspected, replayed,
not reinterpret link capacities, ignore service-latency bounds,            audited, and rolled back independently of the model provider.
construct invalid paths, or bypass the controller’s enforcement               The main contributions of this work are as follows:
policy. Performance measured on a finite training set also                 • Intent-conditioned algorithm-discovery formulation: We
provides no guarantee that an algorithm will remain effective                 formulate transport resource allocation at two levels. The
when the topology, traffic matrix, telemetry accuracy, or active              first is a path-based exact reference problem for priority-
intent changes.                                                               aware admission and routing. The second treats the decision
   A second challenge is defining what should actually be                     procedure itself as the optimization object, explicitly distin-
generated. Allowing an LLM to synthesize an unrestricted end-                 guishing a network intent from individual transport service
to-end network controller unnecessarily combines algorithm                    requests.
design, feasibility enforcement, resource-state management,                • Bounded structural algorithm representation: We intro-
and actuation into one probabilistic component. Conversely,                   duce a typed intent-to-algorithm intermediate representation
restricting generation to a fixed linear score whose coefficients             and a transport-specific DSL in which an LLM can modify
are optimized provides strong containment but corresponds                     feature selection, bounded interactions, thresholds, lexico-
primarily to parameter tuning rather than algorithm discovery.                graphic rules, and conditional decision structure rather than
A useful middle ground requires a sufficiently expressive                     only numerical coefficients.
structural search space while retaining a deterministic execution          • Trusted execution and feasibility preservation: We isolate
boundary.                                                                     generated ranking logic from path construction, resource
   This paper introduces VERA-TN, a verification-guided LLM                   accounting, hard-constraint enforcement, and controller actua-
evolution framework for intent-conditioned transport-network                  tion. We establish a feasibility-preservation property showing
algorithm discovery. Rather than asking the LLM to allocate                   that any candidate executed through the trusted allocator
each transport request directly, VERA-TN compiles an operator                 satisfies the modeled path, latency, capacity, and single-path
intent into a typed algorithm-design specification and uses the               constraints under the stated assumptions.
LLM as a semantic variation operator over a bounded domain-                • Verification-guided evolution: We define a target typed-

specific language (DSL). Candidate programs define reusable                   AST procedure that combines static and runtime verification,
request-ordering and candidate-path-ranking functions through                 exact-oracle comparison, structural-diversity preservation,
controlled combinations of transport features, thresholds, inter-             and structured failure-witness feedback. The released study
actions, and conditional branches.                                            evaluates only the bounded numerical instantiation.
   Crucially, generated logic does not control feasibility or              • Reproducible proof-of-concept evaluation: We release

network state. Candidate paths are constructed by trusted                     deterministic code, seeds, candidate vectors, solver cer-
deterministic code, and every selected path is independently                  tificates, raw metrics, and figure-generation scripts. The
checked against link-capacity, latency, path-validity, and single-            numerical study uses 150 held-out cases on a TEFNET24-
path requirements before resource state can change. The                       derived [9] hierarchy and an external-validity check on
resulting separation is                                                       the official national topology and 12 unseen metro-regional
                                                                              topologies. Model-connected typed-AST experiments remain
    intent
    | {z }         → LLM-generated algorithm → |trusted {z
                                                         allocator}           future work.
                                                                              These contributions are intended to answer a question that is
                     |        {z           }
desired behavior                   ranking logic       feasibility

                   → |controller                                           different from conventional LLM-assisted network control: can
                         {z } .                                            a generative model help discover a reusable transport-network
                       actuation
                                                                     (2)   algorithm while the network retains deterministic authority
                                                                           over what constitutes an admissible action?
   VERA-TN is verification-guided rather than universally                     The remainder of this paper is organized as follows. Sec-
“verified.” The methodology separates several distinct levels of           tion II positions VERA-TN with respect to LLM-assisted
evidence. Static and runtime verification determine whether a              algorithm design, LLM-based networking, intent-driven op-
candidate program is admissible to execute. The trusted alloca-            timization, and trusted network validation. Section III defines
tor preserves the modeled transport constraints independently              the intent and transport-network system model and the reference
of the generated ranking logic. Exact optimization supplies                allocation problem. Section IV introduces the bounded intent-to-
an external quality reference on tractable instances. Finally,             algorithm representation and trusted execution model. Section V
failure-oriented scenarios examine robustness under analytical             presents the verification-guided LLM evolution procedure. Sec-
link failures and capacity degradation. Network-digital-twin               tion VI describes the topology, prototype, and reproducibility
(NDT) evaluation remains a target operational-validation stage.            framework. Section VII defines and reports the experimental
   Another important design objective is to remove the LLM                 evaluation. Section VIII discusses implications and limitations,
from the service-critical execution path. Once discovery is                and Section IX concludes the paper.
complete, the selected typed abstract syntax tree (AST) is
                                                                                              II. R ELATED W ORK
serialized, versioned, and compiled into deterministic local
code. Transport requests can then be processed without invoking            A. Automated Heuristic and Algorithm Design
the originating LLM. This separation amortizes the potentially               Automated heuristic design predates LLM-based generation.
expensive discovery process over repeated network operation                Hyper-heuristics search over heuristics rather than directly
                                                                                                                                                                                                                         3




                                                                                                        parents + witnesses
                                                                                                         (next generation)


                                                                                             LLM-generated (no network authority)




          Network intent                                                   LLM program                                                       Program archive                                  Accepted candidate
           + SLA/SLO                                                         generator                                                         + population                                       algorithm


                                                   candidate AST
                                                                                                                   repair                                         score         robustness




                                                                                                                                           Scenario evaluator                                 Robustness evaluator
          Intent compiler               Static check                         Sandbox                  Trusted allocator                                                   MILP oracle
                                                                                                                                         admission, congestion,                              analytical perturbations
            (JSON / IR)                 AST + types                      replay + timeout            capacity + latency                                                   quality gap
                                                                                                                                            reconfiguration                                         (optional)


                                                                                                  Trusted deterministic execution



         LLM-generated      Program verification          Trusted allocation / evaluation   Archive / population              External I/O




Fig. 1. VERA-TN system architecture and trust boundary. The generated algorithm (violet) is restricted to request-ordering and path-ranking logic. Every
candidate is verified, executed through the trusted allocator, scored against the exact oracle, and stress-tested by the robustness evaluator, all inside the trusted
deterministic region (green). Selected parents and structured failure witnesses are returned to the generator for the next round of candidate generation, closing
the evolutionary loop. The architectural contribution is therefore containment of generated decision logic rather than direct LLM control of network resources.



over problem solutions, while genetic programming has long                                                           reusable decision procedure can itself become the bounded
been used to evolve routing and dispatching rules, including                                                         search object while the network retains deterministic enforce-
their structure and numerical parameters. VERA-TN does                                                               ment.
not claim a new evolutionary optimizer. Its contribution is
the trusted execution and verification boundary around a                                                             C. Traffic Engineering and Trusted Validation
generated rule. Evaluator-driven algorithm design has moved                                                             The allocation model builds on path-based multicommodity
from generating isolated code fragments toward iterative search                                                      flow and K-shortest-path traffic engineering [16], [17]. Exact
over executable procedures. FunSearch evolves a designated                                                           mixed-integer optimization supplies a quality reference rather
function within a trusted program skeleton [4]; EoH co-                                                              than an online deployment requirement. The feedback loop
evolves heuristic ideas and implementations [5]; ReEvo uses                                                          is also related to counterexample-guided inductive synthesis
reflective feedback to repair heuristics [6]; and LLaMEA                                                             (CEGIS) [18], although VERA-TN’s failure witnesses are
evolves complete metaheuristics under an external evaluator                                                          empirical counterexamples from finite network scenarios, not
[7]. LLM4AD and recent surveys organize this emerging                                                                exhaustive symbolic proofs. Network digital twins provide a
design space and its evaluation challenges [10], [11], while                                                         complementary environment for perturbation and controller-
AlphaEvolve illustrates the broader potential of evaluator-                                                          aware validation [19]; TeraFlowSDN illustrates an open
guided code evolution [8]. VERA-TN adopts the external-                                                              controller integration target [20]. The resulting distinction
evaluator principle but adds a transport-specific trust boundary:                                                    among program admissibility, allocation feasibility, solution
generated logic may rank requests and prevalidated paths, but                                                        optimality, and operational validation is central to the proposed
it cannot construct paths, mutate resource state, or invoke a                                                        methodology.
controller These methods motivate VERA-TN’s typed target
interface. However, the present numerical study does not                                                                                  III. S YSTEM M ODEL
evaluate an LLM and cannot establish whether LLM generation                                                             The first design question is not which LLM should control
improves on genetic programming under the same grammar                                                               the network, but which decisions a generated algorithm should
and evaluation budget.                                                                                               be allowed to influence. Fig. 1 therefore separates algorithm
                                                                                                                     discovery from network authority. The generator may modify
B. LLMs and Intent-Based Networking                                                                                  only the request-ordering and path-ranking logic. Program
                                                                                                                     admissibility, candidate-path construction, resource accounting,
   LLMs are increasingly used to translate networking tasks,                                                         constraint enforcement, and eventual actuation remain outside
assist protocol reasoning, and optimize resource allocation.                                                         the generated program and are performed by deterministic
NetLLM develops a general adaptation framework for network-                                                          trusted components. This boundary is the principal architectural
ing tasks [12], and LLM-RAO uses language-model reasoning                                                            mechanism through which VERA-TN limits the operational
within resource-allocation optimization [13]. These methods                                                          effect of an erroneous generated candidate.
primarily produce decisions or learned policies. In parallel,
IBN research has established closed-loop intent translation,                                                         A. Intent and Transport-Network Model
conflict resolution, activation, and assurance [1], [14], [15].
                                                                                                                       We consider an intent-driven packet transport network
Recent transport and slicing frameworks map intents into
                                                                                                                     represented by an undirected graph
multi-objective optimization models and adaptation loops [2],
[3]. VERA-TN asks a complementary question: whether the                                                                                                            G = (V, E),                                          (3)
                                                                                                                                    4



where V denotes the set of transport nodes and E denotes the          procedure [17]. The latency associated with candidate path
set of physical or logical links. Each link e ∈ E is characterized    p ∈ Pk is                    X
by its usable capacity Ce , propagation and processing delay de ,                           Dk,p =     de .                  (6)
current carried load le , and, when applicable, an operational-risk                                   e∈p
attribute qe associated with failures, degradation, or shared-risk      Any path for which
conditions. The network state available at a decision epoch is
therefore represented by the topology together with the current                               Dk,p > Lmax
                                                                                                      k                           (7)
resource and telemetry state of its links.                            is eliminated before algorithm evaluation. Hence, the generated
   The network receives a set R of transport service requests.        algorithm operates only over paths satisfying the request-level
Each request k ∈ R is represented as                                  latency constraint.
                rk = (sk , tk , bk , Lmax , πk , ck ) ,        (4)       Let xk,p ∈ {0, 1} be a binary decision variable equal to
                                      k
                                                                      one when request k is assigned to candidate path p, and
where sk and tk denote the ingress and egress nodes, respec-          zero otherwise. Let ak ∈ {0, 1} indicate whether request k is
tively, bk is the requested bandwidth, Lmaxk    is the maximum        admitted. The resulting transport allocation must satisfy three
tolerable end-to-end transport latency, πk represents the ser-        fundamental feasibility conditions: each admitted request is
vice priority, and ck denotes the service class. The priority         assigned to exactly one path, the aggregate bandwidth placed on
parameter does not itself determine a routing decision. Rather,       every link does not exceed its usable capacity, and only paths
it expresses the relative importance assigned by the operator or      satisfying the corresponding latency bound may be selected.
service policy when resource contention prevents simultaneous
satisfaction of all requests.                                         B. Reference Transport Resource-Allocation Problem
   Unlike conventional traffic-engineering formulations in
which the objective function and algorithm are predefined                To quantify the quality of discovered algorithms indepen-
by the network designer, we assume that network operation is          dently of the LLM, we formulate an exact path-based reference
initiated by a declarative intent. An intent specifies the desired    optimization problem. Its primary objective is to maximize
network outcome without prescribing the algorithm that must           priority-weighted service admission, with normalized path
achieve it. We represent a network intent conceptually as             latency used only as a secondary preference:
                                                                                            X            X X Dk,p
                         I = (O, C, P) ,                       (5)               max           πk ak − ϵ               xk,p ,    (8)
                                                                              {xk,p },{ak }                      Lmax
                                                                                                                   k
                                                                                          k∈R           k∈R p∈Pk
where O denotes the ordered set of optimization objectives,
                                                                  where ϵ > 0 controls only the latency tie-break. We use integer-
C denotes mandatory operational constraints, and P contains
                                                                  valued policy priorities, as is common for service classes.
preference or policy information used to distinguish among
                                                                     Lemma 1 (Lexicographic Dominance): For a nonempty
feasible solutions.
                                                                  request set, if every candidate path is latency-feasible
                                                                                                                         P and
   For example, an operator may express the following intent:
                                                                  0 < ϵ < 1/|R|, then any one-unit increase in             k πk ak
     “Maximize the admitted service priority, preserve            dominates every possible change in the normalized latency
      critical traffic before best-effort traffic, satisfy all    term of (8).
      bandwidth and latency requirements, and, among                    Proof: For an admitted request, exactly one selected path
      solutions with equivalent service admission, minimize       contributes a term in [0, 1] because Dk,p ≤ Lmax    . Hence the
                                                                                                                   k
      peak link utilization.”                                     total normalized latency term lies in [0, |R|], and its change
   The distinction between objectives and hard constraints is between two feasible allocations has magnitude at most |R|.
important. Capacity limits, latency bounds, and path validity Therefore ϵ|∆D| < 1, whereas a change in the integer-valued
are treated as non-negotiable constraints and cannot be relaxed priority sum is at least one. The priority objective consequently
or reinterpreted by an LLM-generated algorithm. Conversely, remains lexicographically dominant.
objectives such as reducing congestion, favoring particular          The artifact uses ϵ = 0.5/(|R| + 1), which satisfies this
service classes, minimizing reconfiguration, or increasing sufficient bound.
resilience determine how alternative feasible allocations should     Each admitted request must be assigned to exactly one
be ranked.                                                        candidate path:
   Before algorithm discovery, the natural-language intent is                        X
compiled into a structured, machine-readable specification.                              xk,p = ak ,      ∀k ∈ R.              (9)
                                                                                    p∈Pk
Ambiguous, contradictory, or unsupported requirements are
rejected or returned for clarification rather than being resolved    The aggregate bandwidth allocated over each transport link
implicitly by the generated algorithm. This establishes a stable cannot exceed its usable capacity:
semantic boundary between what the operator requests and                           X X
what the algorithm-discovery process is permitted to change.                 l e +            bk xk,p ≤ Ce ,    ∀e ∈ E.       (10)
                                                                                   k∈R p∈Pk :
   For each request k, the trusted network layer computes a                             e∈p
finite set Pk of up to K loop-free candidate paths between sk
                                                                     The decision variables satisfy
and tk . Candidate paths can be obtained using Yen’s K-shortest-
path algorithm or an equivalent deterministic path-enumeration                     xk,p ∈ {0, 1},      ak ∈ {0, 1}.           (11)
                                                                                                                                      5



   Because infeasible-latency paths are removed during              by a network intent. We now define the representation exposed
candidate-path construction, the formulation does not require       to the algorithm-discovery process and, critically, the boundary
an additional latency constraint. Similarly, path continuity and    between LLM-generated decision logic and trusted determinis-
loop freedom are inherited from the trusted path-enumeration        tic network functions. The design follows the principle that the
procedure.                                                          generated algorithm may determine how feasible alternatives
   The reference formulation is not the algorithm deployed by       are prioritized, but may not redefine feasibility, modify network
the proposed framework. Instead, it serves as an optimization       state directly, or bypass operator constraints.
oracle on instances for which an exact solution can be obtained
within the prescribed computational budget. Let J ⋆ denote its      A. Intent-to-Algorithm Intermediate Representation
optimal objective value and J(A) denote the objective achieved
by candidate algorithm A. For oracle-solvable instances, the           Directly exposing an unrestricted natural-language intent
relative optimality loss of A is measured as                        to an algorithm-generation model would leave objectives,
                                                                    constraints, and available network information open to interpre-
                                 J ⋆ − J(A)                         tation. Therefore, before algorithm discovery, the conceptual
                  Gap(A) =                       .          (12)
                                max (|J ⋆ | , ϵ)                    intent I = (O, C, P) introduced in (5) is compiled into the
   This metric provides an external measure of solution quality     typed intermediate representation (IR)
that is independent of the LLM’s own evaluation or reasoning.
                                                                                    IIR = ⟨O, C, F , B, D⟩ ,               (15)
For larger instances where proving optimality becomes compu-
tationally impractical, the exact oracle can be replaced by the where O contains the ordered optimization objectives, C con-
best available solver incumbent together with its optimization tains immutable operational constraints, F defines the features
bound. Such cases should be reported separately from exact- accessible to generated algorithms, B specifies syntactic and
optimality comparisons.                                         computational bounds on candidate programs, and D defines
                                                                the trusted execution and deployment contract.
C. Intent-Conditioned Algorithm-Discovery Problem                 The objective component O specifies how feasible allo-
   The objective of this work is fundamentally different from   cations  are evaluated, rather than prescribing the algorithm
solving the reference optimization problem once. Given a        used  to  obtain them. For example, the intent considered in
network-intent specification I, a family of transport-network   Section  III-A can be compiled into the lexicographic hierarchy
states S, and a bounded space A of executable candidate                         O = [max Uadm , min Umax , min Creconf ] ,        (16)
algorithms, we seek an algorithm A⋆ whose decision logic
performs well across the relevant operating scenarios while         where Uadm denotes priority-weighted service admission, Umax
remaining inside the trusted feasibility envelope.                  denotes peak link utilization, and Creconf denotes reconfig-
   The algorithm-discovery problem is expressed as                  uration cost when reconfiguration is considered. Additional
                                                                    objectives can be activated by the intent without changing the
            A⋆ = arg max        F (A | I, S)                (13)    trusted feasibility conditions.
                       A∈A
                         s.t.   V (A, I, S) = valid,        (14)       The constraint component C contains requirements that the
                                                                    algorithm-discovery process cannot modify. For the transport-
where F (·) evaluates the algorithm according to the objectives     network problem considered here,
encoded by the network intent, and V(·) represents the
structural and operational verification mechanisms described                   C = {capacity, latency,
                                                                                                                                  (17)
in the following sections.                                                           path validity, single-path assignment}.
   The output is therefore not a single set of routing decisions.   If an incoming intent contradicts an operator-defined hard
Instead, it is a reusable intent-conditioned algorithm that can     constraint, the compiler rejects the corresponding specification
subsequently be executed on previously unseen network states        rather than implicitly relaxing the constraint during algorithm
without invoking the LLM for every individual service request.      generation.
This distinction separates the proposed problem from direct            The feature schema F exposes only normalized, read-
LLM-based resource allocation: the LLM participates in discov-      only network and request information. Candidate algorithms
ering and improving the decision procedure, whereas trusted         therefore cannot query arbitrary controller state or introduce
deterministic components execute and verify the resulting           undeclared information during execution. We partition the
procedure during network operation.                                 feature schema into request-level and path-level features:
   The next section defines how the abstract intent in (5) is
compiled into a bounded machine-readable representation and                                 F = F req ∪ F path .                  (18)
specifies the trusted execution boundary within which candidate
algorithms are permitted to operate.                                     For request k, the request-level feature vector is represented
                                                                    as
                                                                                          fkreq = π̄k , b̄k , τk , χk ,
                                                                                                                    
   IV. I NTENT- TO -A LGORITHM R EPRESENTATION AND                                                                                (19)
             T RUSTED E XECUTION M ODEL                             where π̄k is normalized service priority, b̄k is normalized
   The system model in Section III defines the transport-           requested bandwidth, τk is latency tightness, and χk is a
resource allocation problem and the desired behavior specified      numerical or categorical encoding of the service class.
                                                                                                                                                       6



  Latency tightness is defined as                                                       whereas the bounded expression space permits controlled
                                    minp∈Pk Dk,p                                        discovery of distinct decision strategies.
                            τk =                 ,                               (20)      The expression space deliberately excludes unrestricted
                                       Lmax
                                         k                                              programming constructs. Candidate programs cannot contain
where values approaching one indicate that the request has                              recursion, unbounded loops, dynamic imports, mutable global
little latency margin even on its shortest feasible path.                               state, arbitrary system calls, external network access, or con-
    The bounds component B restricts generated programs                                 troller invocations. Each generated expression has a statically
to a finite, deterministic, and resource-bounded expression                             defined input type and must return a finite scalar value within
space. The deployment component D specifies that candidate                              a bounded execution budget.
algorithms may return only request-ranking and path-ranking                                The resulting candidate can be serialized as an expression
scores. They cannot directly modify link resources, issue                               tree and replayed independently of the LLM that generated
controller commands, access the file system or external network,                        it. This allows structural comparison among algorithms and
or call undeclared tools.                                                               supports deterministic evaluation, archival, and reproducibility.
    Hence, the IR separates three responsibilities:
             IIR            −→         A
                                      |{z}          −→         T
                                                              |{z}           ,   (21)   C. Transport Features for Algorithm Discovery
             |{z}
         desired behavior          decision logic        trusted execution                The path-ranking function operates on transport-specific
where T denotes the deterministic transport-resource allocation                         quantities computed by trusted deterministic components from
layer defined in Section IV-D.                                                          the current topology and telemetry state.
                                                                                          For request k, admitting it over path p would produce the
                                                                                        projected utilization of link e ∈ p:
B. Bounded Algorithm Design Space
  For a compiled intent IIR , the discovery process searches                                                                le + bk
                                                                                                              ue (k, p) =           .               (27)
a bounded set A(IIR ) of executable candidate algorithms.                                                                      Ce
Each candidate is represented by two deterministic decision                               The projected bottleneck utilization of path p is
functions:
                    A = (hord , hpath ) ,               (22)                                                umax
                                                                                                             k,p = max ue (k, p).                   (28)
                                                                                                                      e∈p

where hord (k) determines the order in which competing trans-                             The normalized path-latency consumption is
port requests are considered and hpath (k, p) ranks candidate
                                                                                                                          Dk,p
path p for request k.                                                                                            ρk,p =        ,                    (29)
  Accordingly,                                                                                                            Lmax
                                                                                                                           k

                                                                                        where smaller values indicate greater latency headroom.
                                     hord : F req → R,                           (23)
                                                                                          The normalized residual-capacity slack after admitting
                    hpath : F req × F path → R.                                  (24)   request k is defined as
  A central requirement is that the search space allow structural
                                                                                                                                  
                                                                                                                      Ce − le − bk
variation rather than only coefficient tuning. We therefore use a                                       sk,p = min                   .          (30)
                                                                                                                e∈p       Ce
typed domain-specific expression language in which candidate
functions may contain bounded compositions of                                             To characterize how evenly residual capacity is distributed
                                                                                        across a candidate path, let
GDSL = {weighted-sum, lexicographic, min, max,
                                                                                                  Ce − le − bk
           bounded-product, threshold, conditional}.                                re (k, p) =                          (31)
                                                                                                        Ce
                                                          (25)
                                                                 denote normalized residual capacity on link e after the
   For example, a discovered path-ranking function may instan-
                                                                 prospective allocation. We define path fragmentation as
tiate the conditional structure
                                                                                         1 X                        2
                            gtight (k, p), τk ≥ δ,                            ϕk,p =            (re (k, p) − r̄k,p ) ,  (32)
            hpath (k, p) =                                (26)                           |p| e∈p
                            g (k, p), τ < δ,
                                flex         k
                                                                 where
where δ ∈ [0, 1] is an evolved threshold, gtight (·) may                                       1 X
                                                                                     r̄k,p =           re (k, p).        (33)
emphasize path latency and bottleneck utilization, and gflex (·)                              |p| e∈p
may instead emphasize residual capacity, fragmentation, or
                                                                 A larger value of ϕk,p indicates a more uneven residual-resource
operational risk.
                                                                 profile and therefore a potentially more fragmented path.
   Thus, evolution may modify not only numerical coefficients
                                                                    When operational-risk information is available, the path-risk
but also feature selection, comparison order, interaction struc-
                                                                 feature is defined as
ture, thresholds, and conditional branches. This distinction
is important because a fixed functional form with optimized                                      1 X
                                                                                          qp =          qe .                 (34)
weights would correspond primarily to parameter tuning,                                         |p| e∈p
                                                                                                                                         7



  The normalized hop count is                                         E. Feasibility-Preservation Property
                                                                         The trusted execution boundary provides a feasibility prop-
                               |p|
                          ηp = max ,                             (35) erty    that is independent of the quality of the generated
                              H                                       algorithm.
where H max is the maximum candidate-path length considered              Proposition 1 (Feasibility Preservation): Assume that:
in the current topology.                                                1) the initial network state satisfies le ≤ Ce for every e ∈ E;
   The resulting path-level feature vector is                           2) every candidate path p ∈ Pk is loop-free, connects sk to
                                                                             tk , and satisfies Dk,p ≤ Lmax
                                                                                                          k    ;
        path     max                               reconf
                                                           
      fk,p = uk,p , ρk,p , sk,p , ϕk,p , qp , ηp , ck,p      ,   (36)   3) the trusted allocator admits request k on path p only if
                                                                             (39) is satisfied; and
where creconf
         k,p    is included only  when   the   corresponding   intent   4)   resource-state updates in (41) are atomic.
considers reconfiguration cost.                                       Then every allocation returned by the trusted allocator satisfies
   All quantities in (19)–(36) are read-only from the perspective path validity, request-level latency constraints, single-path
of the generated algorithm. The candidate can use them assignment, and link-capacity constraints, independently of
to construct its ranking policy but cannot directly alter the the structure or parameters of hord and hpath .
topology, capacity values, telemetry, or feasibility criteria.           Proof. By Assumption 2, every path exposed to a generated
                                                                      algorithm is already a valid, loop-free path connecting the
                                                                      corresponding source and destination and satisfying its latency
D. Trusted Allocation Semantics                                       bound. Hence, path validity and latency feasibility cannot be
                                                                      violated by path ranking.
   The generated algorithm determines prioritization, whereas            Consider the sequence σA of requests generated by hord . The
resource allocation itself remains inside a trusted deterministic initial state is feasible by Assumption 1. Before admitting any
component.                                                            request k on path p, the trusted allocator checks (39). Therefore,
   Let                                                                if all link loads satisfy their capacity limits before the admission,
                       σA = sort↓ (R; hord )                     (37) they continue to satisfy them after the atomic update in (41). By
                                                                      induction over all admitted requests, link-capacity feasibility
denote the request sequence produced by candidate algorithm is preserved throughout the allocation sequence.
A, with larger request scores processed first. For each request          Finally, the allocator commits at most one candidate path for
k in this sequence, its prevalidated candidate paths are ordered      each    request, while rejected requests receive no path. Hence,
according to                                                          the  single-path-assignment      condition is also satisfied.
                                                                         Proposition 1 establishes feasibility preservation, not opti-
                   ΓA
                    k = sort↑ (Pk ; hpath (k, ·)) .              (38) mality or complete correctness of the generated algorithm. A
                                                                      candidate may still make poor admission choices, create un-
Smaller path scores are preferred; candidate identifiers provide necessarily high utilization, produce excessive reconfiguration,
a deterministic final tie-break.                                      disadvantage lower-priority services, or generalize poorly to
   The trusted allocator evaluates the paths in Γk sequentially. unseen network states. These properties cannot be guaranteed
                                                        A

A candidate path p can be committed only if                           by the trusted allocator alone. They are therefore evaluated
                                                                      through the verification-guided evolutionary process introduced
                    le + bk ≤ Ce ,       ∀e ∈ p.                 (39) in Section V.

  Since paths violating                                                       V. V ERIFICATION -G UIDED LLM E VOLUTION
                                                                         Section IV defines the bounded algorithm space within which
                          Dk,p ≤ Lmax
                                  k                            (40)   an LLM is permitted to modify transport-resource allocation
                                                                      logic. We now describe how candidate algorithms are generated,
have already been removed during candidate-path construction,         verified, evaluated, and iteratively improved. The key design
a path passing (39) satisfies both the link-capacity and latency      principle is that the LLM does not directly optimize a single
requirements.                                                         network instance or issue network-control actions. Instead, it
  When such a path is found, the trusted state transition is          acts as a semantic variation operator over a bounded algorithm
                                                                      representation, while deterministic verification and evaluation
                   le ← le + bk ,       ∀e ∈ p,                (41)   components determine whether the resulting candidate is
                                                                      admissible and useful.
and the request is marked as admitted. If no path in ΓAk satisfies       Fig. 2 summarizes the discovery loop. Starting from the
the feasibility conditions, request k is rejected.                    compiled intent IIR , a set of seed algorithms, and a collec-
   Therefore, hord determines which request receives earlier          tion of discovery scenarios, the LLM proposes new request-
access to scarce resources and hpath determines which feasible        ordering and path-ranking programs. Each candidate first passes
route is preferred, but neither function can directly commit an       structural and runtime verification. Valid candidates are then
infeasible allocation.                                                executed through the trusted allocator defined in Section IV-D.
                                                                                                                                                8



Their behavior is evaluated against the intent objectives, and,                   as the subset of scenarios for which the reference optimization
for tractable instances, compared with the exact optimization                     problem can be solved to certified optimality within the
                                                                                                                                    oracle
oracle in Section III-B. Instead of returning only a scalar                       prescribed solver budget. Oracle results from Strain     may be
fitness value, the evaluator extracts structured failure witnesses                used to generate discovery feedback, whereas oracle results
identifying where and why a candidate underperforms. These                        from held-out test scenarios are used only for final reporting.
witnesses are supplied to subsequent LLM calls to guide
mutation, recombination, or repair.                                               B. LLM-Based Candidate Generation
                                                                                    Let P (g) denote the population of candidate algorithms at
                   1. Compile intent                                              generation g. Each candidate
                 objective, constraints,
                    allowed features
                                                                                                                         
                                                                                                      (g)      (g)   (g)
                                                                                                    Ai = hord,i , hpath,i                 (44)

                 2. Generate candidate                                            is represented as a typed expression tree conforming to the
                 ordering + path-score                                            domain- specific language in (25).
                       functions
                                                                                     The LLM receives a constrained generation context

                   3. Verify program                                                  CLLM = (IIR , GDSL , Aparent , Mparent , Wparent ) ,   (45)
                  syntax, AST, types,
                    runtime bounds                                                where GDSL is the permitted grammar, Aparent contains one or
                                                                                  more parent algorithms, Mparent summarizes their measured
                  4. Evaluate solution                                            performance, and Wparent contains selected failure witnesses
                                                     parents + witnesses
                 exact gap, feasibility,             (next generation)            defined in Section V-F.
                       robustness
                                                                                     The LLM is instructed to return a structured abstract syntax
                                                                                  tree (AST) rather than unrestricted executable source code. A
                5. Construct feedback                                             candidate output has the conceptual structure
                  counterexample +
                performance summary                                                           A = {request_ordering : Tord ,
                                                                                                                                             (46)
                                                                                                     path_ranking : Tpath },
                 6. Select and evolve
               Pareto archive, diversity,                                         where Tord and Tpath are typed expression trees composed
               mutation / recombination                                           only of operators and features allowed by IIR .
                             budget exhausted                                        Candidate generation supports the following bounded trans-
                             / converged
                                                                                  formations:
                   Final candidate                                                  1) parameter mutation: modification of constants, coeffi-
                 (validation-selected)
                                                                                       cients, or thresholds;
                                                                                    2) feature mutation: insertion, removal, or replacement of
Fig. 2. Verification-guided discovery loop. Candidate generation (violet) is
untrusted; deterministic verification (red) and evaluation (green) determine           permitted request/path features;
promotion into the archive (orange). Elite and structurally diverse archive         3) operator mutation: replacement of an arithmetic, compar-
members are returned, together with structured failure witnesses, to generate          ison, aggregation, or conditional operator;
the next round of candidates. The loop terminates when the search budget
is exhausted or performance converges, yielding the validation-selected final       4) branch mutation: addition, removal, or modification of a
candidate.                                                                             bounded conditional branch;
                                                                                    5) subtree recombination: combination of compatible subex-
                                                                                       pressions from two parent algorithms; and
A. Discovery Scenario Partitioning                                                  6) repair: targeted modification of an algorithm in response
  To separate algorithm discovery from final performance                               to a structured failure witness.
assessment, the available scenario set is partitioned as                             This representation allows structural algorithm variation
                                                                                  while preventing the LLM from generating arbitrary network-
                       S = Strain ∪ Sval ∪ Stest ,                         (42)
                                                                                  controller code. The originating LLM is not required when a
with pairwise-disjoint subsets. A scenario s ∈ S contains a                       candidate is subsequently executed because the accepted AST
topology, link state, transport-request set, active intent, and,                  is serialized and replayed deterministically.
where applicable, failure or telemetry perturbations.
   The evolutionary loop receives performance feedback only                       C. Structural and Runtime Verification
from Strain . The validation set Sval is used to select the final
                                                                                    Every generated candidate is verified before it is exposed to
algorithm from the discovery archive, while Stest remains
                                                                                  a network scenario. We distinguish structural verification from
unseen until the final experimental evaluation. In cross-topology
                                                                                  network feasibility preservation.
experiments, complete topology families rather than only traffic
                                                                                    Let
seeds are held out, preventing the LLM from adapting its
                                                                                                        Vstat (A) ∈ {0, 1}                    (47)
algorithm to the structure of the test graph.
   We further define                                                              denote the static program verifier. A candidate is accepted by
                           S oracle ⊆ S                      (43)                 Vstat only if all of the following conditions hold:
                                                                                                                                                        9



                              TABLE I                                                      The normalized priority-weighted admission utility is
         V ERIFICATION AND E VALUATION S TAGES IN VERA-TN                                                            P           A,s
                                                                                                                        k∈Rs πk ak
  Stage                Purpose                    Typical feedback                                     Uadm (A, s) = P               .           (52)
  Static verifier      Check                      Invalid operator, undeclared fea-                                       k∈Rs πk
                       DSL/schema/type            ture, excessive depth
                       and complexity rules                                                Peak post-allocation utilization is
  Runtime verifier     Detect numerical and ex-   NaN/Inf, timeout, exception, non-
                       ecution failures           determinism                                                                  lA,s
  Trusted alloca-      Preserve network feasi-    Rejected path/request and respon-                         Umax (A, s) = max e .                    (53)
  tor                  bility                     sible resource                                                          e∈Es Ce
  Scenario evalua-     Measure intent perfor-     Admission loss, congestion, re-
  tor                  mance                      configuration, runtime                    When a scenario contains an existing allocation, reconfigu-
  Exact oracle         Assess solution quality    Optimality gap and differing ad-
                       on tractable cases         mission/path decisions
                                                                                         ration cost is represented as
  NDT check            Assess robustness          Failure sensitivity, SLA violation,                                  X h A,s           i
                                                  recovery cost                                      Creconf (A, s) =   1 pk ̸= pprevk     ,      (54)
                                                                                                                     k∈Rs

                                                                                         where the indicator is evaluated only for previously admitted
 1) the AST conforms to the declared schema and contains
                                                                                         services.
    only whitelisted DSL operators;
                                                                                            For dynamic or network-digital-twin scenarios, the realized
 2) all referenced features belong to F;
                                                                                         SLA violation ratio is
 3) expression inputs and outputs satisfy their declared types;                                                            realized        
                                                                                                                                     > Lmax
                                                                                                                P
 4) constants and thresholds lie inside predefined numerical                                                       k∈Rs 1 Dk             k
                                                                                                  VSLA (A, s) =                               .    (55)
    bounds;                                                                                                            max(1, |Radm
                                                                                                                                  s  |)
 5) the AST depth and total number of nodes do not exceed                                   The analytical model does not use VSLA as an independent
    the configured complexity limits; and                                                feasibility metric because latency-infeasible paths have already
 6) no prohibited capabilities, including external calls, file                           been removed. Instead, (55) captures model mismatch and
    access, mutable network state, recursion, or unbounded                               dynamic behavior observed in an emulated or digital-twin
    iteration, are present.                                                              environment.
  For structurally valid candidates, a trusted compiler converts                            Candidate execution time is denoted by Texec (A, s). The
the AST into an executable scoring function. The resulting                               scenario-level metric vector is therefore
program is evaluated inside a restricted runtime environment.
Define                                                             m(A, s) = [Uadm , −VSLA , −Umax , −Creconf , −Texec ] , (56)
                       Vrun (A) ∈ {0, 1}                    (48) with inactive metrics omitted when they are not specified by
                                                                 the corresponding intent.
as the runtime verifier. It evaluates the candidate on a set        Rather than imposing a universal weighted sum, VERA-TN
Smicro of adversarial micro-instances designed to expose invalid derives the candidate ordering from the objective hierarchy O
numerical or computational behavior:                             in IIR . For a scenario set S ′ , let
 Vrun (A) = 1 ⇐⇒ outputs are finite and deterministic,                                               M(A; S ′ ) = Aggregates∈S ′ m(A, s)             (57)
                    with no exception or budget violation.
                                                        (49)                             denote the corresponding aggregate metric vector. Candidate
  A candidate is executable only if                                                      algorithms are compared using the lexicographic or Pareto
                                                                                         ordering specified by O, while program validity always
                    Vprog (A) = Vstat (A)Vrun (A) = 1.                            (50)   dominates performance.

  Program verification and network feasibility serve different
                                                                                         E. Exact-Oracle Comparison
purposes. Equation (50) determines whether generated decision
logic is safe to execute, whereas Proposition 1 guarantees that a                           For scenarios in S oracle , the optimization problem in Sec-
program executed through the trusted allocator cannot directly                           tion III-B provides an external quality reference independent
violate the modeled capacity, latency, path-validity, or single-                         of the LLM.
path constraints.                                                                           For scenario s, let Js⋆ denote the certified optimal objective
                                                                                         and J(A, s) the corresponding objective obtained by candidate
                                                                                         A. The candidate’s relative optimality loss is
D. Scenario-Based Performance Evaluation
                                                                                                                         Js⋆ − J(A, s)
  For every executable candidate A and discovery scenario                                                 Gap(A, s) =                   .            (58)
                                                                                                                         max(|Js⋆ |, ϵ)
s ∈ Strain , the trusted allocator produces
                                                                                            The oracle is used for two purposes. First, it provides
                               XA,s = T (A, s),                                   (51)   an objective benchmark for evaluating whether discovered
                                                                                         algorithms approach the quality of exact optimization. Second,
where XA,s contains admission decisions, selected paths,                                 on training instances only, the difference between the candidate
resulting link states, and an execution trace recording the                              and oracle allocation can be converted into structured feedback
ordering and ranking decisions made by A.                                                identifying decisions responsible for the quality loss.
                                                                                                                                        10



   If the solver terminates without a certificate of optimality, its     Let
incumbent solution is not denoted by Js⋆ . Instead, the incumbent                                 E (g) ⊆ P (g)                       (62)
and solver bound are recorded separately, and the corresponding
                                                                       denote the elite subset. Parent algorithms are selected from both
instance is excluded from exact optimality-gap claims.
                                                                       high-performing and structurally diverse candidates. To prevent
                                                                       the population from collapsing to nearly identical expression
F. Structured Failure Witnesses                                        trees, we associate each candidate with a structural signature
  A scalar objective reveals whether a candidate performs              consisting of the set of features, operators, thresholds, and
poorly but provides little information about how its decision          branch structures appearing in its AST.
logic should change. VERA-TN therefore converts verification              For two candidate algorithms Ai and Aj , a normalized
and evaluation failures into a structured failure witness              structural diversity measure can be expressed as
                                                                                                                                       
               w = (s, ζ, Rw , E w , yobs , yref , ξ) ,        (59)                                                          |Ψi ∩ Ψj |
                                                                         dstr (Ai , Aj ) = λdtree (Ai , Aj ) + (1 − λ) 1 −                ,
                                                                                                                             |Ψi ∪ Ψj |
where s identifies the scenario, ζ is the failure type, Rw and                                                                         (63)
E w contain affected requests and links, yobs is the observed          where dtree is normalized tree-edit distance, Ψi and Ψj are the
candidate behavior, yref is a reference behavior when available,       sets of operators and features used by the two candidates, and
and ξ is a compact deterministic explanation generated by the          λ ∈ [0, 1] controls the relative contribution of tree structure
evaluator.                                                             and feature/operator overlap.
   Witnesses can originate from several sources.                          The next candidate population is generated by
   Program witness: a candidate violates the DSL, produces a                                                                
non-finite score, times out, or raises an exception.                                 P (g+1) = Select E (g) ∪ C (g) ; O, dstr ,        (64)
   Admission-regret witness: a high-priority request is rejected
                                                                       where C (g) denotes the set of newly generated children.
while an oracle or stronger reference allocation admits it. For
                                                                       Selection first enforces program validity, then ranks candidates
an oracle-solvable scenario, request-level admission regret is
                                                                       by the intent-defined objective ordering, while reserving part
                       ∆adm
                        k   = a⋆k − aA
                                     k,                        (60)    of the population for structurally distinct candidates above a
                                                                       minimum diversity threshold.
and requests with ∆adm
                   k   = 1 are traced back to the ordering and            For repair-oriented generation, the LLM receives the parent
path-ranking decisions that exhausted the required resources.          algorithm together with a bounded set of witnesses and
   Congestion witness: the candidate creates a substantially           is explicitly instructed to modify only the decision logic
larger peak utilization than a reference solution. The most            relevant to the observed deficiency. For example, if a high-
critical link is                                                       priority request is rejected because earlier low-priority requests
                                    lA
                      e† = arg max e .                   (61)          consume a bottleneck link, the feedback identifies the affected
                               e∈E Ce
                                                                       requests, the bottleneck, and the parent ranking behavior. The
The witness includes the requests routed through e† and the            LLM may respond by changing request ordering, introducing a
alternative paths that were available when those decisions were        conditional rule for tight resources, or modifying path ranking
made.                                                                  to preserve bottleneck capacity.
   Robustness witness: a failure, demand shift, or telemetry              This process is counterexample-guided in spirit, but we
perturbation causes an excessive loss in admission, SLA                do not claim equivalence to formal counterexample-guided
compliance, or recovery performance.                                   inductive synthesis (CEGIS). The feedback is obtained from
   Reconfiguration witness: the candidate achieves only a              finite network scenarios and optimization/digital-twin evalua-
marginal utility improvement while causing excessive path              tion rather than from exhaustive symbolic verification of the
churn.                                                                 complete program state space.
   The evaluator ranks witnesses according to their effect on the
current intent hierarchy and retains at most Nw representative         H. Initialization, Termination, and Final Selection
witnesses per parent. This limits prompt length and prevents
                                                                          The initial population combines human-designed seeds and
large scenario traces from being passed directly to the LLM.
                                                                       LLM-generated candidates. Human seeds include shortest-path,
   We use the term failure witness rather than claiming a
                                                                       latency-aware, bandwidth-aware, and load-balancing heuristics.
formal counterexample in the program-verification sense. These
                                                                       A restricted linear candidate of the form
witnesses guide evolution by identifying observed deficiencies
over the evaluated scenario set; they do not constitute a proof                                   h(f ) = θ T f                       (65)
that the candidate fails for every network state.
                                                                       is also included. This candidate is important as an ablation
                                                                       because it isolates coefficient optimization from structural
G. Verification-Guided Repair and Evolution                            algorithm discovery.
  At generation g, the evaluator first removes candidates                 Discovery terminates when any of the following conditions
for which Vprog (A) = 0. Remaining candidates are ranked               is reached:
according to their training performance under the intent-defined         1) the maximum generation count Gmax is reached;
ordering.                                                                2) the candidate-evaluation budget Bmax is exhausted; or
                                                                                                                                 11



Algorithm 1 Verification-Guided LLM Algorithm Evolution            LLM therefore receives neither the test scenarios nor their
Require: Intent IR IIR , training scenarios Strain , validation    performance traces during discovery.
    scenarios Sval , population size N , generation limit Gmax ,
    evaluation budget Bmax                                         I. Computational Complexity and Deployment Cost
Ensure: Selected transport-allocation algorithm A⋆                    Let R = |R| denote the number of transport requests,
 1: Initialize seed population P (0)                               K the maximum number of candidate paths per request,
 2: H ← ∅                                             ▷ archive    and H the maximum number of links in a candidate path.
 3: B ← 0                                                          For an already discovered algorithm, request sorting requires
 4: for g = 0, . . . , Gmax − 1 do                                 O(R log R) operations. Ranking at most K candidate paths
 5:     for all A ∈ P (g) do                                       for every request requires O(RK log K) score comparisons,
 6:          if Vstat (A) = 0 then                                 while feasibility checking over at most H links per candidate
 7:               Record structural witness for A                  contributes O(RKH).
 8:               continue                                            The resulting trusted online-allocation complexity is there-
 9:          end if                                                fore
10:          if Vrun (A) = 0 then                                               O (R log R + RK log K + RKH) .                (67)
11:               Record runtime witness for A
12:               continue                                            Importantly, this online execution does not require an LLM
13:          end if                                                call. LLM inference is confined to the offline or near-line
14:          Execute A using trusted allocator on Strain           discovery process.
15:          Compute M(A; Strain )                                    Let N denote population size, G the number of generations,
16:          Compare with exact oracle where available             and Str = |Strain |. Excluding exact-oracle computation,
17:          Extract bounded witness set WA                        discovery requires at most
18:          Add (A, M, WA ) to archive H                                   O (N GStr [R log R + RK log K + RKH])              (68)
19:          B ← B + |Strain |
20:          if B ≥ Bmax then                                      candidate-scenario evaluation work, in addition to the LLM-
21:               break                                            generation calls.
22:          end if                                                   Exact optimization is intentionally excluded from the online
23:     end for                                                    complexity in (67). The reference problem includes unsplittable
24:     if B ≥ Bmax then                                           path admission and can become combinatorial with network
25:          break                                                 size; it is therefore used as a discovery/evaluation oracle only
26:     end if                                                     where a certified solution can be obtained within the configured
27:     Select elite and diversity-preserving parents              solver budget.
28:     C (g) ← ∅
29:     while |C (g) | < N do                                      J. Reproducibility of the Discovery Process
30:          Select parent(s) Ap from P (g)                           For every LLM-generated candidate, VERA-TN records the
31:          Build constrained LLM context using IIR , Ap ,        model identifier and version, generation parameters, prompt-
    metrics, and witnesses                                         template version, parent candidate hashes, generation index,
32:          Generate mutation, recombination, or repair Ac        mutation type, serialized AST, structural-verification result,
33:          Deduplicate using canonical AST hash                  runtime-verification result, scenario metrics, failure witnesses,
34:          C (g) ← C (g) ∪ {Ac }                                 token usage, wall-clock generation time, and random seed
35:     end while                                                  where applicable.
36:     Form P (g+1) according to (64)                                Accepted and rejected candidates are both retained. This is
37: end for                                                        important because reporting only successful programs would
38: Evaluate non-dominated archive candidates on Sval              obscure the reliability and computational cost of LLM-based
39: Select A⋆ using the intent-defined validation ordering         discovery. The complete archive therefore enables measurement
40: return A⋆                                                      of
                                                                      Mrepro = {valid-program and runtime-success rates,
                                                                                  time to first/best algorithm,
  3) no validation-eligible improvement is observed for Gstall                                                                 (69)
                                                                                  evaluations to convergence,
      consecutive generations.
                                                                                  LLM token and compute cost}.
   The test set is not used to determine the stopping point.
After evolution, a compact set of non-dominated candidates            Because the executable representation of every accepted
from the archive H is evaluated on Sval . The final algorithm      candidate is stored independently of the originating language
is selected as                                                     model, final transport allocation experiments can be determinis-
                                                                   tically replayed without re-querying the LLM. This separation
              A⋆ = arg max F (A | I, Sval ) .              (66)    permits the stochasticity of algorithm discovery to be analyzed
                        A∈Hvalid
                                                                   independently from the runtime behavior of the discovered
  Only after A⋆ has been fixed is it evaluated on Stest . The      network algorithm.
                                                                                                                                                                                                          12



          VI. I MPLEMENTATION AND R EPRODUCIBILITY                                                                                                 TABLE II
                                                                                                                               R ELEASED P ROOF - OF -C ONCEPT C ONFIGURATION
   This section separates the reference architecture in Sec-
                                                                                                                     Item                       Configuration
tions IV–V from the released proof-of-concept. The architecture
                                                                                                                     Topology                   28 nodes, 54 bidirectional links
specifies typed AST generation, static checks, sandboxed                                                             Candidate paths            Up to K = 4, loop-free and latency-feasible
execution, and model-connected repair. The current artifact                                                          Candidate representation   Bounded ten-parameter numerical vector
                                                                                                                     Evolution                  Population 24; 14 generations
implements the trusted allocator, exact oracle, deterministic                                                        Oracle                     Path-based binary MILP; recorded certificate status
scenario generator, bounded candidate evaluator, numerical                                                           Validation                 Nominal plus analytical link/capacity perturbations
                                                                                                                     Evaluation seeds           30 per load; 30 failed-link cases; 10 for K sensitivity
evolutionary search, perturbation tests, and result archive. It                                                      Online LLM inference       None
does not execute arbitrary model-generated Python, issue live
LLM calls, or establish a multi-provider typed-AST comparison.
This distinction keeps the implementation claim aligned with                                                       B. Released Prototype
the released code while preserving the full design contract for
                                                                     The numerical candidate is a ten-parameter vector controlling
the next model-connected stage.
                                                                  request priority/order and path features including projected
                                                                  utilization, latency, residual slack, and risk. Evolution uses a
                                                                  population of 24 candidates for 14 generations. A performance-
A. Topology and Workload                                          only search is evaluated on nominal scenarios; the VERA-TN
   TEFNET24 motivates the hierarchical structure of the prototype additionally uses perturbed scenarios and an overload
representative graph [9]. The public reference describes a multi- penalty. Both execute through the same trusted allocator, so
layer packet-optical network inspired by operational Telefónica candidate logic returns scores but never commits resource state.
deployments; its data interface is available separately [21]. The    The exact reference is the path-based binary model in (8)–
present artifact instead uses the deterministic 28-node, 54-link  (11), solved with SciPy’s MILP interface. The implementation
graph in Fig. 3, which preserves access aggregation, metro        records   solver success, status, objective, message, and MIP gap.
rings, redundant interconnection, dual homing, and a connected    A  row   is called oracle-optimal only when the solver reports
national/core layer. Capacities and delays are generated once     success   and  zero recorded gap within numerical tolerance.
per seed from tier-specific ranges.
                                                                                          VII. E VALUATION
                                                                                                                   A. Scope, Questions, and Metrics
                                      A11
                                                       A12
                                                                                                                      The study asks seven questions. RQ1 measures priority
                                                                       A13
                                                                                                                   utility under increasing contention. RQ2 tests whether evo-
                     A10
                                                        M6                                                         lution improves on priority-greedy routing and equal-budget
                                                                                        A14
                            M5                                                                                     random search. RQ3 compares congestion with MILP-C, which
          A9
                                                                             M7                                    minimizes the same metric at maximum priority utility. RQ4
                                                  C3                                                      Metro
                                                                                                   A15             tests failure-aware search on held-out failed-link cases. RQ5
                                                                                                          Access
                                                                                                                   tests whether three training intents yield specialized candidates.
                M4
    A8
                                                 CORE                                                     Core     RQ6 tests whether intent behavior transfers from the official
                                 C2                               C0

                                                                                       M0
                                                                                                     A0            national topology to unseen metro-regional topologies. The
                                                                                                                   synthetic intent-transfer test uses resilience as its third intent,
     A7

                                                  C1
                                                                                                                   whereas the official-data study uses admitted volume. The
                       M3                                                                     A1                   two transfer tests are therefore interpreted separately. RQ7
               A6
                                                                   M1                                              measures K sensitivity and separates online heuristic scaling
                                            M2
                                                                                  A2
                                                                                                                   from exact-solver tractability.
                            A5
                                                                                                                      The primary metric is priority utility divided by MILP-U
                                                             A3
                                             A4                                                                    utility. Secondary metrics are peak link utilization, accepted
                                                                                                                   requests, the fraction of cases that reach exact priority utility,
                                                                                                                   rejected priority under failure, and runtime. All methods use
                                                                                                                   the same path sets and trusted allocator. Capacity and latency
Fig. 3. Representative TEFNET24-derived hierarchy used by the released
proof-of-concept with 28 nodes, 54 bidirectional links. Capacities, delays,                                        violations are therefore checked as invariants, not treated as
and workloads are deterministic experimental inputs rather than operator                                           performance metrics.
measurements.

   Each request contains ingress, egress, bandwidth, latency B. Baselines and Statistical Protocol
bound, and an integer service priority. Up to four simple paths    Shortest path uses arrival order and the first feasible path.
are generated deterministically and paths exceeding the latency Load-balanced KSP ranks paths with a fixed bottleneck-oriented
bound are removed before ranking. Evaluation loads scale score. Priority-greedy orders requests by descending priority,
nominal demands by factors {1.0, 1.4, 1.8, 2.2, 2.5}. Perturbed breaks ties by ascending bandwidth, and chooses the path
scenarios remove links and vary capacities using archived seeds. with minimum projected bottleneck utilization. Equal-budget
                                                                                                                                                                             13



random search controls for the number of sampled parameter                                                     0.658). The gain over random search is 0.00635 (p = 0.0083,
vectors. Evolutionary search uses the same candidate budget.                                                   r = 0.434). The effect is statistically detectable but small.
MILP-U and MILP-C are offline references, not deployment                                                       Evolution reaches exact priority utility in 50 of 150 cases.
baselines.                                                                                                        The heuristic does not improve congestion over MILP-C.
   Table values aggregate 150 paired test cases. Mean utility                                                  MILP-C reaches mean peak utilization 0.939; evolutionary
and utilization use 10,000-resample bootstrap 95% confidence                                                   search reaches 0.961. Moreover, the candidate is priority-
intervals. Runtime is reported as median and interquartile range                                               optimal in only one third of the cases. On those 50 cases,
(IQR). Pre-specified paired Wilcoxon tests compare evolution                                                   its mean utilization regret relative to MILP-C is 0.058. The
and random search with priority-greedy, and evolution with                                                     earlier latency-tie-break MILP is not used as a congestion
random search. Holm correction is applied across the six utility                                               reference.
and utilization tests. Paired rank-biserial correlation is the
effect size. For the official-data study, each of eight discovery                                              E. Failure Training and Intent Transfer
seeds is the inferential unit. The 16 national or 48 metro
scores are first averaged within a seed. Paired Wilcoxon tests                                                    On 30 held-out failed-link scenarios, failure-aware search
then compare each intent-matched candidate with the two off-                                                   reaches mean utility ratio 0.934 and 10th-percentile ratio
diagonal candidates. Holm correction is applied across six                                                     0.862. Search without failure scenarios reaches 0.919 and
contrasts per domain, and bootstrap intervals resample the                                                     0.844, respectively. The paired mean difference is 0.0151 with
eight seed-level means. This avoids treating repeated replay                                                   bootstrap CI [0.0031,0.0288], but the Wilcoxon test gives
scenarios as independent discovery runs.                                                                       p = 0.051. This test therefore does not establish a robustness
                                                                                                               gain. Removing the utilization feature lowers the mean to 0.914.
                                                                                                               Removing the nearly zero slack coefficient has no observed
C. Motivating Toy Example                                                                                      effect.
   Before presenting aggregate results, we use a small con-                                                       The intent-transfer test shows no intent-specific specializa-
structed example to illustrate the mechanism through which                                                     tion. Three searches use priority, congestion, and resilience
request ordering and path ranking can affect priority utility.                                                 scores, but the priority-trained vector has the best held-out
Both policies in Fig. 4 operate on the same topology and                                                       score under all three objectives. Fig. 7 reports regret from the
candidate paths and are subject to exactly the same capacity                                                   best candidate for each target objective. Different weights alone
and latency checks. The only difference is the order in which                                                  do not establish intent-conditioned specialization. The present
requests and feasible paths are considered. Under arrival-                                                     evaluation therefore does not support a claim of structural
order shortest-path allocation, early routing decisions consume                                                algorithm discovery.
resources that could otherwise support higher-value demand,
yielding total priority utility 6. The bounded VERA-TN                                                         F. Official Cross-Topology Check
prototype changes the ordering/ranking decisions and reaches
utility 8, equal to the reference MILP utility for this constructed                                               The official-data study also shows no intent-specific spe-
instance. Thus, the illustration isolates the mechanism targeted                                               cialization. Discovery on the national graph does not produce
by algorithm discovery: the gain arises from how scarce feasible                                               a stable intent-matched diagonal. Across the three national
resources are prioritized, not from relaxing network constraints.                                              targets, the largest absolute matched contrast is below 0.0006
                                                                                                               and no adjusted test is significant.
   Shortest-path baseline: utility 6                VERA-TN prototype: utility 8 (MILP-equivalent)                Fig. 8 replays all 24 selected candidates without retraining
  S1                                         T1                S1                                         T1
                                                                                                               on 48 workloads from 12 unseen metro components. The
                                      10                                                          10
         14                   Y                                       14                   Y                   congestion-trained candidates have the best mean score under
                       10                                                           10

                 X            8
                                      10
                                                                             X             8
                                                                                                  10
                                                                                                               all three metro targets. None of the 12 intent-matched contrasts
         14             8
                                      8
                                             T2                       14            8
                                                                                                   8
                                                                                                          T2   is significant; every Holm-adjusted p-value equals 1.0. Priority-
  S2                          Z                                S2                          Z
                                                                                                               greedy obtains mean priority ratios 0.9785 nationally and
                                                                                                               0.6126 on the metro cases, close to 0.9794 and 0.6134 for the
                                                                                                               priority-trained candidates. All 1,536 candidate replays satisfy
Colored routes show admitted requests; critical requests are red/purple, premium blue, and best-effort gray.
                                                                                                               the trusted capacity and latency checks.
Fig. 4. Constructed contention illustration. The example shows why request
ordering and path ranking matter; it is not part of the statistical evaluation.                                G. Sensitivity and Tractability
                                                                       Increasing K raises median replay time from 0.53 ms at
                                                                    K = 1 to 4.46 ms at K = 16. Mean utility does not improve
D. Priority Utility and Congestion                                  monotonically: it is 0.974 at K = 1, 0.947 at K = 4, and 0.934
   Table III and Fig. 5 answer RQ1–RQ3. The higher demand at K = 16 on the ten sensitivity seeds. The fixed candidate was
levels avoid the ceiling effect observed in the earlier evaluation. selected with K = 4 and does not automatically use additional
Evolutionary search reaches mean utility ratio 0.958, compared paths well.
with 0.940 for priority-greedy and 0.952 for equal-budget              Fig. 10 separates online replay from exact optimization.
random search. Its mean paired gain over priority-greedy is Across 28–504 nodes, fitted runtime exponents are 0.99 for
0.0187 (Holm-adjusted p = 1.3 × 10−6 , rank-biserial r = evolutionary replay and 1.14 for priority-greedy under this joint
                                                                                                                                                                                                                                                                                                        14



                                                                                                                 TABLE III
                                                                          H ELD -O UT R ESULTS ACROSS F IVE L OADS AND 30 S EEDS PER L OAD (n = 150 PER M ETHOD )

                                  Method                                                  Utility ratio, mean±SD [95% CI]           Peak util.                       Accepted                       Runtime ms, median [IQR]                    Priority-opt.
                                  Shortest path                                              0.805 ± 0.115 [0.787,0.823]                0.974                            16.71                              0.198 [0.190,0.207]                     5.3%
                                  Load-balanced KSP                                          0.830 ± 0.120 [0.811,0.849]                0.955                            17.27                              1.564 [1.503,1.656]                    13.3%
                                  Priority-greedy                                            0.940 ± 0.050 [0.932,0.947]                0.948                            17.51                              0.350 [0.334,0.372]                    20.0%
                                  Equal-budget random                                        0.952 ± 0.046 [0.945,0.959]                0.963                            17.79                              1.583 [1.518,1.667]                    26.7%
                                  Evolutionary search                                        0.958 ± 0.041 [0.952,0.965]                0.961                            17.95                              1.573 [1.522,1.669]                    33.3%
                                  MILP-U                                                     1.000 ± 0.000 [1.000,1.000]                0.977                            19.03                            26.358 [17.076,37.689]                   100%
                                  MILP-C                                                     1.000 ± 0.000 [1.000,1.000]                0.939                            19.03                           84.957 [34.833,176.536]                   100%


                                                                     (a) Priority-weighted solution quality                                                                                     (b) Congestion exposure
                                                               1.0                                                                                                1.00
                                   Priority utility / MILP-U




                                                                                                                                                                  0.95




                                                                                                                                          Peak link utilization
                                                               0.9

                                                                                                                                                                  0.90
                                                               0.8

                                                                                                                                                                  0.85
                                                               0.7
                                                                                                                                                                  0.80

                                                               0.6
                                                                                                                                                                  0.75


                                                                      1.0                  1.4           1.8             2.2      2.5                                           1.0                      1.4              1.8             2.2         2.5
                                                                                                 Demand scale                                                                                                  Demand scale

                                                                                            Shortest path                      Priority-greedy                                                                  Evolutionary search
                                                                                            Load-balanced KSP                  Equal-budget random search                                                       MILP-C


Fig. 5. Held-out priority utility and peak utilization. Shaded bands in (a) are bootstrap 95% confidence intervals. MILP-C is the fair congestion reference
because it preserves MILP-U priority utility.


                                                               Held-out failed-link scenarios                                                                                                                          Intent-transfer test
                           0.96
                                                                                         Mean




                                                                                                                                                                                                                                                                       Score regret (lower is better)
                                                                                                                                                                                                                                                                0.30
                           0.94                                                          10th percentile                                                                                      Priority         0.000            0.000            0.000

                                                                                                                                                                                                                                                                0.25
                           0.92
                                                                                                                                                                         Training intent
        Utility / MILP-U




                           0.90                                                                                                                                                                                                                                 0.20
                                                                                                                                                                                           Congestion          0.017            0.017            0.239
                           0.88                                                                                                                                                                                                                                 0.15


                           0.86                                                                                                                                                                                                                                 0.10

                                                                                                                                                                                           Resilience          0.029            0.028            0.347
                           0.84                                                                                                                                                                                                                                 0.05


                           0.82                                                                                                                                                                                                                                 0.00
                                                                                                                                                                                                            Priority         Congestion     Resilience
                           0.80                                                                                                                                                                                        Held-out target intent

                           0.78
                                         h                                        res              ion               k                            Fig. 7. Intent-transfer score regret on 60 held-out nominal and failed cases.
                                 l se
                                     arc                                  failu                izat             slac
                             Fu l                                    No                    util            No                                     Zero is best. The diagonal does not dominate, so the numerical representation
                                                                                        No
                                                                                                                                                  does not validate intent-specific specialization.

Fig. 6. Mean and 10th-percentile utility over 30 held-out failed-link cases.
Failure-aware search improves the observed mean and tail, but the paired
Wilcoxon result is marginal.                                                                                                                                                                                    VIII. D ISCUSSION
                                                                                                                                                     The evidence supports two claims. First, the trust boundary
                                                                                                                                                  preserves the modeled allocation constraints independently of
                                                                                                                                                  the ranking parameters. Second, under a fixed evaluation budget,
                                                                                                                                                  numerical evolution gives a small held-out utility gain over
graph/request scaling. These are empirical fits, not asymptotic                                                                                   random sampling and a larger gain over the priority-greedy
proofs. With a two-second MILP-U budget, all five cases are                                                                                       baseline. The study does not support three stronger claims: the
certified at 28 and 56 nodes, three of five at 84 nodes, one of                                                                                   evolved candidate is not congestion-optimal, failure training is
five at 112 nodes, and none at 168 or 224 nodes. Uncertified                                                                                      not significant at α = 0.05, and intent-specific candidates do
cases are excluded from Table III; the separate curve shows                                                                                       not specialize on held-out tests.
where the exact reference stops being dependable within that                                                                                         The study has several limitations. It uses batch allocation,
budget.                                                                                                                                           analytical failures, one parameterized representation, and one
                                                                                                                                                                                                                                           15



                                                                    (a) National held-out workloads                                                        (b) Unseen metro regions
                                                                                                                                                                                                  0.005




                                                                                                                                                                                                          Score regret (lower is better)
                                                         Priority     0.0000        0.0000            0.0000                                  Priority    0.0011         0.0008         0.0016
                                                                                                                                                                                                  0.004
                                   Discovery intent




                                                                                                                        Discovery intent
                                                                                                                                                                                                  0.003
                                                      Congestion      0.0003        0.0004            0.0006                               Congestion     0.0000         0.0000         0.0000

                                                                                                                                                                                                  0.002



                                                         Volume       0.0006        0.0007            0.0000                                  Volume      0.0053         0.0036         0.0006    0.001


                                                                                                                                                                                                  0.000
                                                                      Priority     Congestion        Volume                                               Priority     Congestion       Volume
                                                                             Held-out target intent                                                              Held-out target intent


Fig. 8. Official TEFNET24 intent-transfer check. Each cell is regret from the best mean score for its target objective. Discovery uses eight seeds on the
national graph; metro evaluation uses 12 unseen components and 48 workloads without retraining. The diagonal does not dominate in either domain. Inferential
tests use discovery-seed means, not individual replay rows.



                                                      Candidate-path sensitivity                                                             central safety property is architectural: a candidate may rank
                                                                                          Utility ratio
                                                                                                          4.5                                prevalidated choices, while a trusted allocator retains path
                        0.97                                                              Runtime         4.0
                                                                                                                                             construction, resource accounting, hard-constraint enforcement,
                                                                                                                                             and actuation. Proposition 1 establishes allocation feasibility
Mean utility / MILP-U




                                                                                                                Median runtime (ms)


                                                                                                          3.5
                        0.96
                                                                                                                                             under explicit assumptions, and Lemma 1 gives a sufficient
                                                                                                          3.0                                bound for the exact model’s latency tie-break.
                                                                                                          2.5                                   Across 150 certified held-out cases, numerical evolution
                        0.95
                                                                                                          2.0
                                                                                                                                             reaches mean priority utility ratio 0.958, compared with 0.952
                                                                                                                                             for equal-budget random search and 0.940 for priority-greedy
                                                                                                          1.5
                        0.94                                                                                                                 routing. The gain over random search is small but statistically
                                                                                                          1.0                                detectable. The candidate does not match the congestion oracle,
                        0.93                                                                              0.5                                and its intent-transfer test does not show specialization. Failure-
                               1                            2            4            8             16
                                                                                                                                             aware search improves the observed mean and tail, but its
                                                            Candidate-path limit K
                                                                                                                                             paired test is marginal. This larger study separates statistically
                                                                                                                                             supported gains from null results.
Fig. 9. Candidate-path sensitivity over ten seeds. Larger path sets increase                                                                    Eight repeated searches on the official national graph and
replay time but do not improve this fixed candidate monotonically.                                                                           replay on 12 unseen metro-regional graphs also show the limits
                                                                                                                                             of the ten-parameter representation: no stable intent-matched
                                                                                                                                             diagonal appears.
machine. The official-data check spans national and metro
                                                                                                                                                The present contribution is the trust boundary and its
graphs from one topology family; it does not establish transfer
                                                                                                                                             reproducible numerical evaluation. It is not evidence that an
to an independent operator or network family. Its link capacities
                                                                                                                                             LLM improves heuristic design. That question requires a typed
are assumed, and the public traffic matrix determines end-
                                                                                                                                             structural implementation, equal-budget GP and model controls,
point marginals rather than per-request bandwidth. Concurrent
                                                                                                                                             independent topology families, and operational validation.
arrivals, reconfiguration cost, digital-twin fidelity, controller
behavior, and physical-network effects are not tested. The typed-
AST and LLM extension is specified but not implemented. A                                                                                                              ACKNOWLEDGMENT
direct comparison with genetic programming on the same                                                                                         This work is partially funded by the Juan de la
grammar is required before making a structural-search claim.                                                                                 Cierva (JDC) Grant under reference (JDC2024-053571-I),
   The next empirical step should be a controlled structural                                                                                 the SHINE (PID2024-159781OB-I00) project funded by MI-
study: implement the typed grammar, compare GP and at least                                                                                  CIU/AEI/10.13039/501100011033 and by ERDF/EU.
two model generators under the same candidate budget, archive
all rejected programs, and evaluate on independent public                                                                                                                   R EFERENCES
topology families. Dynamic multi-epoch tests are also needed
                                                                                                                                               [1] A. Leivadeas and M. Falkner, “A survey on intent-based networking,”
before reporting reconfiguration or operational resilience.                                                                                        IEEE Communications Surveys & Tutorials, vol. 25, no. 1, pp. 625–655,
                                                                                                                                                   2023.
                                                                                                                                               [2] B. Ojaghi, R. Vilalta, and R. Muñoz, “IBNS: Optimizing intent-based 6G
                                                             IX. C ONCLUSION                                                                       network slicing for conflict detection and mitigation,” IEEE Transactions
  This paper introduced VERA-TN, a verification-guided ar-                                                                                         on Network and Service Management, vol. 23, pp. 2818–2831, 2026.
                                                                                                                                               [3] B. Ojaghi, R. Muñoz, and R. Vilalta, “Intent-based network slicing in
chitecture for turning declarative transport intents into bounded,                                                                                 6G: Optimization approach for conflict resolution,” IEEE Transactions
reusable request-ordering and path-ranking procedures. The                                                                                         on Mobile Computing, 2026.
                                                                                                                                                                                                      16



                                         (a) Online heuristic: median and IQR                                                    (b) MILP-U tractability
                                                                                                                   1.0

                                                                                                                                                                     2500




                                                                                                                                                                            Median solver time (ms)
                                                                                                                   0.8
                                   101




                                                                                            Certified within 2 s
                                                                                                                                                                     2000
                    Runtime (ms)                                                                                   0.6
                                                                                                                                                                     1500

                                                                                                                   0.4
                                                                                                                                                                     1000
                                   100
                                                                                                                   0.2                                               500
                                                                    Priority-greedy
                                                                    Evolutionary search
                                                                                                                   0.0                                               0

                                                                                                                            50        100        150       200
                                          28 56 84112   16
                                                          8
                                                              22
                                                                4
                                                                     33
                                                                       6
                                                                                      50
                                                                                        4
                                                                                                                                      Topology nodes
                                                         Topology nodes


Fig. 10. Runtime scaling. (a) Online replay uses 30 repetitions per point; bands show IQR. (b) MILP-U reports the certified fraction and median elapsed time
for five cases per size under a two-second limit.



 [4] B. Romera-Paredes, M. Barekatain, A. Novikov, M. Balog, M. P. Kumar,                                            [19] N. P. Kuruvatti, M. A. Habibi, S. Partani, B. Han, A. Fellan, and H. D.
     E. Dupont, F. J. R. Ruiz et al., “Mathematical discoveries from program                                              Schotten, “Empowering 6G communication systems with digital twin
     search with large language models,” Nature, vol. 625, pp. 468–475, 2024.                                             technology: A comprehensive survey,” IEEE Access, vol. 10, pp. 112 158–
 [5] F. Liu, X. Tong, M. Yuan, X. Lin, F. Luo, Z. Wang, Z. Lu, and Q. Zhang,                                              112 186, 2022.
     “Evolution of heuristics: Towards efficient automatic algorithm design                                          [20] R. Munoz, R. Vilalta, R. Casellas et al., “TeraFlow: Secured autonomic
     using large language model,” in Proc. 41st Int. Conf. Machine Learning                                               traffic management for a tera of SDN flows,” in Proc. Joint European
     (ICML), vol. 235, 2024, pp. 32 201–32 223.                                                                           Conference on Networks and Communications and 6G Summit, 2021.
 [6] H. Ye, J. Wang, Z. Cao, F. Berto, C. Hua, H. Kim, J. Park, and                                                  [21] Telefónica Research and Development and Universidad Carlos III de
     G. Song, “ReEvo: Large language models as hyper-heuristics with                                                      Madrid, “TEFNET24 dataset,” 2024.
     reflective evolution,” in Advances in Neural Information Processing
     Systems, vol. 37, 2024.
 [7] N. van Stein and T. Bäck, “LLaMEA: A large language model
     evolutionary algorithm for automatically generating metaheuristics,” IEEE
     Transactions on Evolutionary Computation, vol. 29, no. 2, pp. 331–345,
     2025.
 [8] A. Novikov, N. Vũ, M. Eisenberger, E. Dupont, P.-S. Huang, A. Z.
     Wagner, S. Shirobokov, B. Kozlovskii, F. J. R. Ruiz, A. Mehrabian et al.,
     “AlphaEvolve: A coding agent for scientific and algorithmic discovery,”
     arXiv preprint arXiv:2506.13131, 2025.
 [9] J. M. Rivas-Moscoso, F. Arpanaei, G. Otero Pérez, J. D. Martı́nez Jiménez,
     J. P. Fernández-Palacios, Ó. González de Dios, L. M. Contreras,
     A. Sánchez-Macián, J. A. Hernández, D. Larrabeiti, and J. Folgueira,
     “TEFNET24: Reference packet optical network topology for edge to core
     transport,” Journal of Optical Communications and Networking, vol. 16,
     no. 11, pp. G28–G39, 2024.
[10] F. Liu, R. Zhang, Z. Xie, R. Sun, K. Li, X. Lin, Z. Wang, Z. Lu,
     and Q. Zhang, “LLM4AD: A platform for algorithm design with large
     language models,” arXiv preprint arXiv:2412.17287, 2024.
[11] F. Liu, Y. Yao, P. Guo, Z. Yang, X. Lin, Z. Zhao, X. Tong, K. Mao,
     Z. Lu, Z. Wang, M. Yuan, and Q. Zhang, “A systematic survey on large
     language models for algorithm design,” ACM Computing Surveys, vol. 58,
     no. 8, pp. 1–32, 2026.
[12] D. Wu, X. Wang, Y. Qiao, Z. Wang, J. Jiang, S. Cui, and F. Wang,
     “NetLLM: Adapting large language models for networking,” in Proc.
     ACM SIGCOMM, 2024, pp. 661–678.
[13] H. Noh, B. Shim, and H. J. Yang, “Adaptive resource allocation opti-
     mization using large language models in dynamic wireless environments,”
     IEEE Transactions on Vehicular Technology, vol. 74, no. 10, pp. 16 630–
     16 635, 2025.
[14] B. Ojaghi, R. Vilalta, and R. Muñoz, “Intent-based network resource
     slicing in 6G,” in Proc. IEEE Network of the Future, 2024.
[15] B. Ojaghi, R. Vilalta, and R. Munoz, “Optimizing throughput and energy
     with intent-based 6G network slicing: Conflict handling,” in Proc. IEEE
     International Conference on Communications, 2025.
[16] B. Fortz and M. Thorup, “Internet traffic engineering by optimizing
     OSPF weights,” in Proc. IEEE INFOCOM, 2000, pp. 519–528.
[17] J. Y. Yen, “Finding the K shortest loopless paths in a network,”
     Management Science, vol. 17, no. 11, pp. 712–716, 1971.
[18] A. Solar-Lezama, L. Tancau, R. Bodik, S. Seshia, and V. Saraswat,
     “Combinatorial sketching for finite programs,” in Proc. 12th Int. Conf.
     Architectural Support for Programming Languages and Operating
     Systems, 2006, pp. 404–415.
