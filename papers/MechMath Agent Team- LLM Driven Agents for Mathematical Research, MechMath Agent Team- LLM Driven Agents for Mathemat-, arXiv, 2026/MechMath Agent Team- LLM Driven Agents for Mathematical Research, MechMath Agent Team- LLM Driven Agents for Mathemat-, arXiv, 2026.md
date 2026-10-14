                                        Key Laboratory of Mathematics Mechanization                                                MechMath Agent Team




                                        MechMath Agent Team: LLM Driven Agents for Mathemat-
                                        ical Research

                                        Yichuan Cao12,* , Ruichen Qiu13,* , Junqi Liu12 , Jiaqi Wang12 , Dakai Guo1 , Ruyong
                                        Feng12 , Lihong Zhi12 , Xiao-Shan Gao12,+


                                                                                             Abstract
arXiv:2607.04394v1 [cs.AI] 5 Jul 2026




                                                  AI reasoning has become a central focus in contemporary artificial intelligence, largely
                                                  driven by the success of large language models. However, mathematical research, which is
                                                  characterized by non-linear derivation paths, rigorous logical requirements, and protracted
                                                  exploration cycles, poses severe challenges for existing reasoning systems. To overcome
                                                  these limitations, we present the MechMath Agent Team (MMAT), which is a large language
                                                  model driven agent designed to serve as a co-pilot throughout the full cycle of mathemat-
                                                  ical research. We design a tripartite Harness Architecture that decouples system respon-
                                                  sibilities into Control, Execution, and Augmentation planes, thereby reconciling rigorous
                                                  logical control with the agility demanded by open-ended research. Building upon this
                                                  framework, we instantiate three specialized agents: a Knowledge Base Manager, a Natural
                                                  Language Prover, and a Formal Language Prover, all operating in a closed loop to produce
                                                  formally certified mathematical proofs. We evaluate MMAT on open problems in Num-
                                                  ber Theory, Algebraic Complexity Theory, Differential Algebra, Operator Algebra, and In-
                                                  equalities. Across a two-month deployment, 11 problems have been solved, demonstrating
                                                  its capacity to act as a co-pilot throughout the entire research cycle. The contributions are
                                                  threefold: a general decoupled Harness Architecture for multi-agent mathematical reason-
                                                  ing, its concrete instantiation in the MMAT system, and empirical validation on a diverse
                                                  suite of open problems.


                                        1    Introduction
                                        AI reasoning has been a constitutive pillar of artificial intelligence since its inception at the 1956 Dartmouth
                                        Summer Research Project [31]. In recent years, it has re-emerged as a central focus, driven overwhelm-
                                        ingly by the proliferation of large language models (LLMs) [40]. Through prompting strategies such as
                                        chain-of-thought [48], LLMs exhibit emergent multi-step inference capabilities. Additionally, LLM-based
                                        agents have expanded the scope of reasoning by integrating external tools and interacting with dynamic
                                        environments, supporting more deliberate and plan-oriented problem solving [21, 47]. Together, these de-
                                        velopments have raised new questions about the nature and evaluation of reasoning, cementing it as one
                                        of the most dynamic frontiers in contemporary AI.
                                        Despite these advances, directly applying such reasoning capabilities to mathematical research remains
                                        particularly challenging, given its non-linearity derivation trajectories, strict logical requirements, and pro-
                                        tracted exploration cycles. Conventional linear multi-agent pipelines frequently struggle with these de-
                                        mands due to their rigid, hard-coded workflows and vulnerability to error propagation [3, 35]. To ad-
                                        dress these challenges, we depart from traditional frameworks and introduce the MechMath Agent Team
                                        (MMAT), a multi-agent system built upon a disciplined, structurally robust Harness Architecture. By flex-
                                        ibly mounting various sub-agents and toolchains, MMAT coordinates multiple specialized large language
                                        models (LLMs) to work collaboratively while maintaining deterministic system states and traceable exe-
                                        cution histories. In particular, it is designed to be agent-agnostic, making it easy to integrate with current
                                            1 State Key Laboratory of Mathematical Sciences, Academy of Mathematics and Systems Science, CAS
                                            2 School of Mathematical Sciences, University of Chinese Academy of Sciences
                                            ∗ Equal contribution.
                                            3 School of Advanced Interdisciplinary Sciences, University of Chinese Academy of Sciences
                                            + Corresponding author.



                                                                                                  1
Key Laboratory of Mathematics Mechanization                                                    MechMath Agent Team




          General Harness                       Specific Subagents               Specific Tools             Agents


         Control Plane                                                   ...                   ...

                                               ORCH    ING        RES
                                                                                                          KB-Manager



                                                                         ...                   ...

                                               ORCH    EXPL       SKE
                         Augmentation                                                                      NL-Prover
                         Plane



                                                                         ...                   ...
     Execution Plane
                                               ORCH    F-RE       F-GE
                                                                                                           FL-Prover

Figure 1: Architectural of the MechMath Agent Team. The underlying harness (left) establishes the core structural
and engineering scaffold divided into three essential paradigms. By modularly equipping this generic scaffold with
task-specific Specific Subagents (middle left) and heterogeneous Specific Tools (middle right), the system instantiates the
specialized architecture (right) comprising the KB-Manager, the NL-Prover, and the FL-Prover. ORCH: Orchestrator.
ING: Ingester. RES: Researcher. EXPL: Explorer. SKE: Sketcher. F-RE: Formal Reviewer. F-GE: Formal Generator.




mainstream coding and reasoning agents such as Claude Code, Codex and ZCode, thereby anchoring our
framework in practical, production-grade toolchains.
Concretely, our Harness architecture adopts a tripartite paradigm that cleanly separates system responsi-
bilities across three planes (Figure 2), striking a balance between rigorous logical control and open-ended
research agility. First, the flexible Control Plane operates a centralized Orchestrator grounded in two de-
terministic data structures: a global execution graph and a local task ledger. By bypassing the volatile
conversational contexts of LLMs, it enforces explicit, state-driven task scheduling. Second, the decoupled
Execution Plane eliminates context bloat and concurrency conflicts through dual physical and informational
boundaries. Sandboxed Isolated Workspaces contain agent operations, while artifact-centric File-Based
Handoffs replace fragile peer-to-peer dialogue. Finally, the Augmentation Plane extends beyond standalone
cognitive limits along two axes: human-AI co-reasoning introduces flexible interaction breakpoints for ex-
pert refinement and deadlock resolution, while stratified continual memory distills recurring reasoning
errors into cross-session negative constraints, keeping the system evolvable.
Building upon this foundational harness framework, we instantiate the generic architecture as the spe-
cialized multi-agent system comprising three sovereign, domain-specialized agents (Figure 1): the Knowl-
edge Base Manager (KB-Manager), the Natural Language Prover (NL-Prover), and the Formal Language Prover
(FL-Prover). They operate within a continuous, closed-loop paradigm: NL-Prover orchestrates multi-agent
pipelines and tools to decompose problems and synthesize natural language proofs. FL-Prover acts as a logi-
cal referee by utilizing the Lean 4 compiler to mechanically verify natural language derivations. KB-Manager
manages an object-oriented memory graph to organize and archive mathematical reasoning history.
We evaluate our framework’s empirical performance on several challenging mathematical domains, includ-
ing Number Theory, Algebraic Complexity Theory, Differential Algebra, Operator Algebra, and Inequality,
going beyond static benchmarks to engage with open problems. By case studies, we demonstrate the sys-
tem’s ability to carry a mathematical problem through a complete natural-to-formal proof pipeline and
coordinate agent-driven certification of its sub-results. More importantly, beyond solving individual prob-
lems, it can audit existing proofs while tracking incremental progress, engage human-in-the-loop proving
to establish new statements, and steer the broader project-level exploration toward uncharted mathemati-
cal directions. Taken together, these results confirm that MMAT can act as a co-pilot throughout the entire
research cycle.


                                                              2
Key Laboratory of Mathematics Mechanization                                                                MechMath Agent Team




                  2.1.1 Execution Graph                                                   2.1.2 Task Ledger
                                            ...
                                                                                ID          Task            Owner        Status
                                                       Type 1
                                                       Type 2                   T1    Define main goal     Subagent 1    Done
                                     ...               Type 3
                                                                                T2    Explore key ideas    Subagent 2    Done
                                                       Type 4
                                                                                T3     Generate sketch     Subagent 3    Done

                                                                                T4    Verify correctness   Subagent 4    Done

                                                                                T5    Re-generate sketch   Subagent 3    Prog.
                                           Orchestrator                               Verify correctness   Subagent 4
                                                                                T6                                       Todo
                 Subagent 1                       • Global Scheduling           T7       Synthesize        Subagent 5    Todo
                                                  • State Management            ...           ...              ...         ...
       Isolated workspace
                                                  • Dependency Tracking
                                                  • Resource Allocation


                Subagent 2
                                           Plan & Control
                                                                                 2.3 Augmentation Plane

                                                                                                                        Local
                                                          File                                                          Memory
                                                          handoff
                        Subagent 3

                                                                                                           Long-term
                                                                                                           Memory
      2.2 Execution Plane                         Subagent 4              AI-Human Co-Reasoning



Figure 2: The Harness Architecture. The whole architecture can be divided into three parts: The control plane (blue
part), the execution plane (purple) part and the augmentation plane (green part).


Over a two-month internal experience period by authors and collaborators, MMAT solved 11 mathematical
problems (Table 4 and Figure 8), covering both longstanding open questions and entries from the OEIS 1 .
Notable examples include Katz’s question on the equivalence of generalized Airy operators [27], the “Chal-
lenge” [10, 34] regarding the complexity of sparse polynomial divisibility tests [8], the “Challenge” on the
complexity [10] of output-sensitive GCD computation [36], the open problem on the quasi-linearity [39] of
sparse polynomial multiplication [20], and the multivariate counterpart [19] of the Erdös–Rényi conjecture
asserting that the sparsity of f e entails the sparsity of f [11, 41, 53]. Among these advancements, MMAT
either provides a rigorous proof of the key theorem or fully automates the derivation of the complete result.
These findings underscore the capability of MMAT in addressing frontier mathematical problems.
In summary, our contributions are threefold, and the paper follows this structure accordingly. First, we
introduce a general harness architecture with decoupled Control, Execution, and Augmentation Planes
(Section 2) Second, We instantiate the harness framework into the MMAT multi-agent system with three
specialized agents (Section 3). Finally, we evaluate its performance on open problems in Number Theory,
Algebraic Complexity Theory, Differential Algebra, and Inequality (Section 4).


2    The Harness Architecture

Mathematical research constitutes an inherently intricate and multifaceted endeavor. The non-linearity of
its derivation trajectories, the stringent requirements for logical correctness, and the protracted exploration
cycles collectively impose profound challenges for automated systems. To surmount these obstacles, we
deviate from conventional linear multi-agent workflows and propose the Harness architecture, which is
shown in Figure 2. Serving as a disciplined and structurally robust foundation, the system orchestrates
multiple specialized large language models (LLMs) through a tripartite architectural design. This design
    1 The On-Line Encyclopedia of Integer Sequences. https://oeis.org/



                                                                    3
Key Laboratory of Mathematics Mechanization                                           MechMath Agent Team




systematically segregates responsibilities into three distinct planes: (1) a Control Plane for algorithmic or-
chestration and scheduling (blue part), (2) an Execution Plane for environmental isolation and containment
(purple part), and (3) an Augmentation Plane for cognitive scaffolding and extension (green part). This
layered paradigm ensures deterministic system states and traceable execution histories while adeptly bal-
ancing rigorous logical validation, containment safety, and open-ended research agility.
Flexible Control Plane (§2.1). To break the rigidity of hard-coded workflows, the framework introduces
a dynamic decision-making mechanism driven by a centralized Orchestrator. Instead of following a static
path, the Orchestrator grounds its logic in two interlocking, deterministic data structures: a global Execution
Graph (DAG) for macro-level task scheduling and reactive routing, and a local Task Ledger for strict micro-
level status compliance and accountability. This explicit state-management process completely bypasses
the volatile and implicit conversational contexts of LLMs.
Decoupled Execution Plane (§2.2). To mitigate data concurrency conflicts and context bloat inherent in
multi-agent collaboration, the framework establishes a decoupled execution plane governed by strict phys-
ical and informational boundaries. By utilizing Isolated Workspaces, the system rigidly confines each sub-
agent’s write operations to local sandboxes, containing reasoning errors at their source. Simultaneously,
through File-Based Handoffs, the architecture abandons fragile peer-to-peer dialogues in favor of determin-
istic artifact transformations, drastically reducing context window pressure.
Augmentation Plane (§2.3). To transcend the intrinsic cognitive ceilings and attention saturation of fully
autonomous models, the framework incorporates an augmentation plane as an external scaffolding layer.
Through Human-AI Co-Reasoning, it establishes flexible interaction breakpoints that empower human math-
ematicians to qualitatively refine proofs or break logical deadlocks via structured, human-readable progress
notes. Complementing this vertical collaboration, its Stratified Continual Memory distills recurring high-level
reasoning errors into cross-session negative constraints while externalizing dense domain facts to the un-
derlying Knowledge Base. By combining targeted human intuition with lean experience retention, this
plane scales the system beyond standalone automation into an evolvable research ecosystem.

2.1     Flexible Control Plane

To break the structural rigidity of hard-coded, linear pipelines, the Harness framework introduces a flexi-
ble, orchestrator-driven control flow. As illustrated in Figure 2, the central Orchestrator acts as the primary
decision-making engine, dynamically determining the next system action instead of following a static, pre-
defined path. To manage this execution flow without relying on the implicit, volatile conversational con-
texts of large language models [29], the Orchestrator grounds its decision-making logic in two interlocking,
deterministic data structures. Globally, it maintains an Execution Graph to model macro-level task depen-
dencies and enable reactive routing (§2.1.1). Locally, it enforces a structured Task Ledger to maintain strict
micro-level status compliance and accountability (§2.1.2). Together, these dual abstractions transform the
system from a fragile, text-driven dialogue flow into an explicit, auditable state-management process.

2.1.1    Execution Graph
Instead of following a rigid, linear pipeline, execution transitions are coordinated via an explicit,
dependency-aware Directed Acyclic Graph (DAG) over the global task space. As illustrated in the Exe-
cution Graph component of Figure 2, the Orchestrator maps the macro-workflow topology directly onto this
graph structure, where nodes represent distinct subtasks and edges delineate strict data or logical depen-
dencies. Drawing on standard workflow scheduling and modern multi-agent graph paradigms [45, 52], this
framework allows the centralized control plane to monitor execution prerequisites and structural mutations
in real time, serving as the definitive baseline for global task orchestration.
Structuring the research task space as a reactive DAG yields two fundamental architectural advantages.
First, the Orchestrator can launch parallel explorations. It continuously scans the topology to isolate mutu-
ally independent subtask nodes (e.g., independent lemmas of a mathematical theorem whose prerequisite
data dependencies are satisfied) and seamlessly dispatch them to multiple concurrent agents, maximizing
computational throughput.
Second, the DAG enables dynamic routing for error recovery. Rather than treating reasoning missteps or
validation failures as terminal exceptions, the Orchestrator intercepts them as typed routing signals [37].
Depending on the failure scope, the system adaptively alters the graph topology through three tailored
strategies as follows. (1) For localized errors, it reroutes the faulty node to a freshly instantiated copy


                                                      4
Key Laboratory of Mathematics Mechanization                                            MechMath Agent Team




of the original subtask. (2) For broader architectural defects, it triggers a macro graph reset to upstream
planning nodes to resolve structural logical inconsistencies. (3) To bypass localized deadlocks, it spawns
entirely new exploratory branches under alternative constraints. Ultimately, this seamless integration of
multi-branch parallel progression and self-healing error recovery equips the execution graph with high
topological flexibility.

2.1.2    Task Ledger
To solve tracking issues inherent in multi-round multi-agent workflows, we introduce an explicit Task Ledger
as a persistent, structured scheduling baseline that thoroughly decouples the global operational state from
the implicit conversational contexts of LLMs. At a high level, this ledger serves as a single source of truth
for the system’s current state, enabling the Orchestrator to query precise status information and bypass the
“fuzzy memory” and attention drift that plague long contexts [29].
Inspired by Hong et al. [16], we design the ledger to maintain a high-fidelity record across four primitive
fields (Figure 2): task identification (ID), task description (Task), the designated responsible entity (Owner),
and real-time execution progress (Status). It is mechanically maintained by external tooling and governed
by deterministic state transition rules. To preserve state integrity and prevent unauthorized manipulation,
individual subagents are denied write permissions; only the centralized Orchestrator holds the privilege to
modify the ledger’s fields according to strict, pre-defined structural conditions.
This centralized, constraint-driven enforcement yields several concrete architectural advantages over tradi-
tional dialogue-driven multi-agent systems. First, by delegating state tracking to this rigid external struc-
ture, the Orchestrator can precisely identify the current state and the next step at any moment, eliminating
reliance on fallible conversational memory. Second, the system continuously verifies field completeness
and logical coherence through automated tooling, ensuring that every pending item maintains an assigned
owner and every blocking state remains traceable. Third, this constraint-based design prevents agents from
using ambiguous natural language to fabricate task progress [23]. Consequently, it successfully transforms
the traditionally ill-defined challenge of multi-agent accountability into an explicit, recoverable, and au-
ditable state-management engineering process.

2.2     Decoupled Execution Plane

To complement the logical constraints enforced by the centralized control flow, the Harness establishes a
decoupled execution plane governed by strict physical and informational boundaries. As mapped out in
the Execution plane region of Figure 2, this architecture shifts away from traditional multi-agent paradigms
that rely on shared environments and unstructured dialogue flows. Instead, it systematizes execution reli-
ability through a dual-pronged approach: a spatial dimension that confines runtime file operations, and an
informational dimension that structures collaborative data exchanges. By systematically separating where
agents work from how they communicate, this execution plane effectively curbs data concurrency conflicts,
context bloat, and multi-agent coordination deadlocks during long-horizon research tasks. To operational-
ize this paradigm, the system relies on two interlocking components: an Isolated Workspace to enforce local
runtime containment, and a system of File-Based Handoffs to drive artifact-centric progression.

2.2.1    Isolated Workspace
Serving as a physical countermeasure against execution interference, the Harness introduces an Isolated
Workspace mechanism that establishes strict containment for each agent’s file operations. As illustrated in
the purple part of Figure 2 (bottom-left), the system allocates a dedicated, sandboxed directory to each
instantiated subagent (e.g., Subagent 1, 2, and 3). Within this paradigm, subagents are granted strictly
managed read permissions to fetch upstream context, while all write operations are rigidly confined within
their local sandbox. Cross-zone tampering or unauthorized data modification among other subagents is
strictly prevented by the execution environment.
This stringent spatial isolation yields two significant architectural advantages. First, it guarantees file in-
tegrity across both the parallel and sequential dimensions of the workflow. From a parallel perspective,
the isolated workspace eliminates the risk of data concurrency conflicts, since restricting write permissions
exclusively to an individual sandbox ensures that concurrent subagents never interfere. From a sequential
perspective, this strict encapsulation prevents post-hoc alteration, unauthorized deletion, or tampering by
subsequent entities. A downstream agent awakened in a later phase of exploration is strictly prevented by


                                                       5
Key Laboratory of Mathematics Mechanization                                              MechMath Agent Team




the isolation mechanism from altering or destroying the persistent historical outputs generated by its pre-
decessors. This immutability is practically enforced by underlying filesystem permission controls and can
be further complemented by optional content-hashing verification at the storage interface. Together, this
multi-dimensional protection preserves a reliable, immutable audit trail where every file variant remains
permanently traceable to its specific authoring entity.
Second, this isolation physically severs the pathway for unverified, faulty, or hallucinatory content to con-
taminate the global system state. In a completely open environment, a localized reasoning misstep or buggy
code snippet is immediately exposed to the public workspace, where it is often repeatedly referenced, prop-
agated and amplified by other agents [3, 50]. By confining unverified trials within isolated directories, the
Harness effectively contains reasoning faults at their source. A localized data artifact can be delivered to
peer subagents only after passing rigorous system validation and being explicitly approved by the central-
ized Orchestrator.

2.2.2    File-Based Handoffs
To operationalize collaboration across these isolated boundaries, the Harness implements an artifact-driven
workflow based on file-based handoffs. Subagents completely abandon fragile, dialogue-driven peer-to-peer
communications and no longer pass lengthy conversational history to one another. Instead, as visualized
by the explicit handoff in Figure 2, subagents exchange task increments, data payloads, and acceptance cri-
teria exclusively via structured files. When a subagent is awakened by the Orchestrator, the system injects
only the minimal, file-based context tailored to that specific node’s local objective. For instance, a sketcher
subagent receives a single structured file containing the initial mathematical problem and background con-
text from the Orchestrator, decomposes it into a collection of lemmas, and submits the report file back to the
Orchestrator. Crucially, the Orchestrator does not itself inspect the content within the file. Instead, its respon-
sibility is to awaken the next successor (e.g., a verifier subagent) and transfer only the specific proposition
file required for its localized task.
Decoupling agent collaboration from conversational text flows provides concrete engineering advantages:
Passing only structured files eliminates the uncontrolled growth of raw chat histories. This design dras-
tically reduces the model’s context window pressure, effectively mitigating the performance degradation
and attention drift common in long-context language models [29]. More importantly, by translating vague
natural-language coordination into deterministic file exchanges, the system prevents agents from getting
stuck in infinite conversational loops or peer-to-peer argumentation [9]. Since each handoff conveys a self-
contained task snapshot rather than enabling bidirectional message passing, the resulting interaction graph
remains acyclic and deterministic by construction. The entire multi-agent collaboration is thus formalized
into a clean, reproducible, and losslessly preserved sequence of artifact transformations.

2.3     Augmentation Plane

While the centralized control plane governs runtime scheduling and the execution plane enforces spatial
isolation, fully autonomous large language models remain fundamentally bounded by intrinsic reasoning
cognitive limits and attention saturation during complex, long-horizon research tasks. To transcend these
inherent limitations, the Harness introduces the Augmentation Plane as an external cognitive scaffolding
layer. As mapped out in the orange regions of Figure 2, this plane does not interfere with the deterministic
mechanics of the active control loop. Instead, it systematically extends the system’s capabilities along two
complementary axes: an interactive dimension that integrates external human intuition to refine achieve-
ments or break logical deadlocks, and a temporal dimension that distills abstract heuristic lessons across
entirely separate sessions. By consolidating human-in-the-loop collaboration and stratified experience re-
tention, the Augmentation Plane transforms the framework into an evolvable, highly resilient research
ecosystem.

2.3.1    Human-AI Co-Reasoning
To overcome the inherent limitations of full autonomy [43], the Harness implements a human–AI co-
reasoning mechanism featuring flexible interaction checkpoints, which is a design mandated by two dis-
tinct operational realities. First, even when an agent completes a task successfully, human expert oversight
remains essential. Autonomous generation frequently requires post-processing or optimization to reach
publication-ready quality, demanding qualitative refinement, alternative reasoning pathways, or structural
enhancements. Second, when an autonomous agent encounters an insurmountable logical impasse, it lacks


                                                        6
Key Laboratory of Mathematics Mechanization                                           MechMath Agent Team




the intrinsic capacity to resolve the deadlock [17]. Thus, it necessitates the intervention of a human mathe-
matician to diagnose the underlying bottleneck and prescribe a strategic course to advance the exploration
frontier.
The co-reasoning relies on two core technical mechanisms. First, to facilitate seamless expert comprehen-
sion, the system automatically generates a highly human-readable diagnostic report. Even when a task
cannot be fully completed, it compiles a comprehensive progress note that precisely logs all intermediate
milestone achievements, explicit blocking coordinates, and auxiliary context. Second, the interface sup-
ports flexible human input modalities, permitting mathematicians to inject strategic guidance or manual
corrections either by issuing direct instructions or by precisely annotating the report itself. The centralized
Orchestrator then ingests these critical human hints, updates the underlying task structures, and seamlessly
resumes DAG exploration directly from the recovery checkpoint. By salvaging prior computation, this
interface minimizes human effort and eliminates wasteful full-scale restarts.


2.3.2   Stratified Continual Memory

To sustain cross-session learning without inducing cognitive bloat [32], the Harness introduces a strati-
fied memory architecture. This tripartite design partitions information based on its scope of validity and
cognitive density, preventing the active context from being choked by either transient noise or heavy data
payloads. Specifically, local memory manages intra-session dynamics by tracking temporary notation con-
ventions (e.g., assigning a specific semantic definition to symbol A within a localized proof) that are vital
for immediate consistency but obsolete once the session terminates. In contrast, long-term memory operates
cross-session to preserve abstract, highly distilled strategic boundaries that govern broader heuristic rea-
soning (e.g., heuristic thresholds such as differentiating between O( T ) and soft-O( T ) complexity regimes in
asymptotic analysis). Crucially, dense and large-scale domain knowledge (e.g., certifying whether a specific
concrete algorithm satisfies soft-O( T ) bounds) is completely externalized from the active memory appara-
tus and stored as persistable data artifacts within the broader Knowledge Base, ensuring that heavy factual
payloads never saturate the context window.
Focusing the system’s memorization capacity on capturing abstracted errors yields significantly greater ar-
chitectural value than passively recording successful factual trajectories. While valid mathematical deriva-
tions are highly problem-specific and rarely transferable across disparate research domains, systemic rea-
soning failures and structural pitfalls expose universal behavioral flaws. By distilling these recurring high-
level patterns, such as a persistent tendency to confound highly similar notation conventions inherited from
entirely separate problem sessions, the memory layer transforms idiosyncratic mistakes into actionable neg-
ative constraints, which are explicit behavioral boundaries that the system should avoid crossing in future
reasoning paths [44]. Prioritizing these abstract behavioral boundaries over bulky domain facts fundamen-
tally ensures that the memory apparatus remains structurally lean, maximizing proactive defensive utility
and preventing regression while minimizing context-window overhead. Consequently, by persistently ap-
plying these negative constraints, the system aims to neutralize repetitive cognitive traps without inducing
attention drift.


3   MechMath Agent Team

This section delineates the architectural design and operational mechanics of the MechMath Agent Team, a
highly modularized, self-correcting multi-agent system engineered to automate complex mathematical re-
search. We instantiate the generic Harness architecture introduced in Section 2 by specializing the template
with component-specific tools and sub-agent roles. This process yields three sovereign, domain-specialized
agents: the Natural Language Prover (NL Prover), the Formal Language Prover (FL Prover), and the Knowledge
Base Manager (KB Manager), which will be introduced in the following sections respectively.
Rather than functioning as a rigid, linear pipeline, these agents are orchestrated within a continuous, closed-
loop paradigm as depicted in Figure 3. The architecture is instantiated as a collection of strictly isolated
projects, each dedicated to a concrete research direction (e.g., sparse polynomial in Section 4.3). Within a
single project, the three coequal agents share a unified object-oriented memory graph and interact organ-
ically through a tightly coupled loop of four primitives: Inform, Formalize, Feedback, and Archive. Different
projects remain entirely disconnected to avoid data proliferation and cross-domain interference, so that each
instance of this self-reinforcing interplay remains tightly focused within its designated research direction.


                                                      7
Key Laboratory of Mathematics Mechanization                                                MechMath Agent Team




      KB-Manager                                                                           FL-Prover
      Manages an object-oriented mem-                                                      Acts as a logical ref-
      ory graph to organize and archive                                                    eree by utilizing the




                                                     ive
      mathematical reasoning history.                                                      Lean 4 compiler to




                                                                                   In
                                                  ch


                                                            orm




                                                                                   fo
                                                                         Ar
                                                                                           autonomously gen-




                                                Ar




                                                                                      rm
                                                                           ch
                                                                                           erate formal proofs




                                                           Inf




                                                                              i
                                                                              ve
                                                                                           and mechanically
      NL-Prover                                                                            verify natural lan-
      Orchestrates multi-agent pipelines                                                   guage derivations.
      and tools to decompose problems                             Formalize
      and synthesize natural language
      proofs.

                                                                  Feedback

Figure 3: System architecture and collaborative workflow of the MechMath Agent Team. Center of the diagram shows
the dynamic, closed-loop interaction topology. Colored dotted lines visually map each agent’s core responsibilities
(KB-Manager, NL-Prover, and FL-Prover) to its respective operational role.


Concretely, Inform flows from the KB Manager to both the NL Prover and the FL Prover, proactively supply-
ing them with relevant historical knowledge, proven lemmas, and accumulated heuristics from the shared
memory graph to guide ongoing reasoning. The NL Prover then navigates complex reasoning spaces, syn-
thesizes natural language proofs, and, when a derivation requires rigorous validation, transmits it to the FL
Prover via the Formalize primitive. The FL Prover formalizes the derivation into Lean 4 code, performs deter-
ministic mechanical verification, and returns the verification outcomes to the NL Prover through Feedback.
If the verification fails, the NL Prover revises the informal proof based on the feedback and may re-initiate
the Formalize process, thereby embodying the system’s self-correcting nature. Throughout this process,
both the NL Prover and the FL Prover deposit their newly generated exploratory heuristics, formalized ar-
tifacts, verification logs, and failure records into the KB Manager via the Archive primitive, continuously
enriching the shared memory graph. This mutually reinforcing circulation ensures that informal insights,
exploratory heuristics, verification outcomes (both successful and failed), and formalized Lean 4 artifacts
are systematically consolidated, enabling accumulated mathematical experience to seamlessly seed and
optimize subsequent research iterations.

3.1     Natural Language Prover

As the core agent of MMAT responsible for generating natural language proofs, the Natural Language Prover
(NL-Prover) implements a dual-layered architecture comprising the Proof Pipeline and the Command-Line
Tooling Layer to transition automated mathematical reasoning from isolated generation to a rigorous,
scalable discovery process. The Proof Pipeline establishes a hierarchical, multi-agent framework that or-
chestrates specialized subagents across four functional layers—balancing baseline problem decomposition
with advanced diagnostic path recovery and publication-grade documentation. Serving as the bedrock for
this cognitive workflow, the Command-Line Tooling Layer acts as a deterministic “exoskeleton” that bridges
the gap between stochastic language generation and formal mathematical rigor. By offloading resource-
intensive and mechanical tasks—such as literature retrieval, PDF parsing, and structural schema gating—to
reliable programmatic routines, this infrastructure layer minimizes hallucination and preserves the agents’
cognitive capacity for pure logical synthesis. Together, these two components form a robust synergy that al-
lows highly divergent mathematical explorations to advance within a controllable, verifiable, and resource-
efficient framework.

3.1.1    Proof Pipeline
Leveraging the flexible control plane of the Harness framework, the proof pipeline is structured as a hi-
erarchical, multi-agent framework characterized by high topological flexibility and dynamic fault toler-
ance. The subagents are organized into four interconnected functional layers, which are summarized in
Table 1a: (1) the Core Derivation Baseline, which operationalizes standard problem decomposition and verifi-
cation paradigms; (2) the Grounded Infrastructure Interfaces, providing empirical grounding through external
database retrieval and programmatic execution; (3) the Advanced Mathematical Reasoning cluster—our pri-


                                                            8
Key Laboratory of Mathematics Mechanization                                               MechMath Agent Team




                                         (a) Specialist Roles in NL Prover
  Role               Responsibility
  Sketcher           Converts original problem into structured proof plan with lemmas and dependencies.
  Generator          Produces detailed informal proofs with justifications for assigned statements.
  Verifier           Independently audits proofs for correctness and completeness.
  Searcher           Traces named theorems to usable, verified statements for proof use.
  Code Executor      Programmatically validates computations, finite enumerations, and exhaustive case evidence.
  Auditor            Clarifies notations and assumptions to prevent conceptual ambiguity and logic errors.
  Explorer           Proposes diverse proof strategies when standard routes fail.
  Synthesizer        Synthesizes high-potential proposals into actionable branches.
  Regulator          Classifies proof failures to identify responsible owners and next steps.
  CE-Hunter          Investigates boundary cases and potential falsities to harden the proof search.
  Refiner            Shortens or improves verified proofs while keeping original as fallback.
  Writer             Compiles refined proof components into cohesive, publication-grade mathematical drafts.

                                             (b) Command-Line Tools
  Tool              Interfaces           Description
  Retrieval         arxiv, matlas        Retrieves verified theorems and proofs to enable cumulative reasoning.
  Extraction        PDF Parser           Converts unstructured visual documents into structured text segments.
  Linting           Linters              Enforces strict morphological and schema compliance on agent outputs.
  Verification      LLM API              Dispatches reasoning snippets to heterogeneous models for blind-testing.

Table 1: Natural Language Prover. (a) shows four kinds, 12 different subagents in the Natural Language Prover. (b)
shows 4 command-line tools and their interfaces.


mary architectural innovation—engineered for non-linear path recovery, semantic auditing, and structural
diagnostics; and (4) the Documentation layer, which synthesizes internal reasoning traces into publication-
grade artifacts. Orchestrated via an adaptive, state-aware control loop, this stack balances exploratory
autonomy with rigorous computational and logical safeguards.
Core Derivation Baseline. Drawing on established mathematical agent architectures, the Core Proof
Pipeline integrates two foundational paradigms: (1) problem decomposition, where complex tasks are bro-
ken down into actionable sub-problems, and (2) a generate-verify workflow, where proof candidates are
subjected to independent scrutiny [22]. We realize these paradigms through the Sketcher, which maps prob-
lems into structured blueprints and lemma taxonomies, and the Generator-Verifier pair, which manages the
production and auditing of proof attempts.
Distinct from rigid, linear implementations of these paradigms, our architecture is governed by an Orches-
trator-driven dynamic control flow. The Orchestrator maintains global state visibility, allowing the system
to deviate from pre-planned trajectories based on real-time feedback. For instance, upon a Verifier failure,
the Orchestrator dynamically determines the optimal remediation strategy: it may instruct the Generator to
refine a specific local segment, or, in instances of fundamental logical conflicts, trigger a backtrack to the
Sketcher to adjust the underlying decomposition strategy. This recursive feedback loop ensures that the
system proactively adapts to logical inconsistencies rather than blindly propagating errors.
Grounded Infrastructure Interfaces. To anchor abstract reasoning in verified literature and computational
evidence, the system employs two primary external interfaces. The Searcher bridges the gap between the
proof process and academic databases, ensuring that all imported theorems are contextually grounded and
their preconditions formally documented.
Concurrently, the Code Executor serves as a programmatic fallback for tasks requiring objective validation,
with a primary focus on integrating the capability to invoke symbolic computation engines. It can execute
algebraic derivations, identity verifications, and polynomial simplifications directly at the level of pure
symbols and exact rationals. By executing these specialized symbolic verification scripts, the Code Executor
provides an empirical "hard-science" layer, ensuring that critical proof claims rest firmly on audited, exact
symbolic computational results rather than heuristic reasoning.
Advanced Mathematical Reasoning. Positioned above the infrastructure layer, this cluster constitutes the
core cognitive and diagnostic engine of our architecture, specifically engineered to navigate advanced math-


                                                         9
Key Laboratory of Mathematics Mechanization                                            MechMath Agent Team




ematical nuances, execute non-linear path recovery, and perform structural failure analysis. As a founda-
tional safeguard within this cognitive core, the Auditor explicitly formalizes and clarifies specialized nota-
tions, convention-based assumptions, and localized naming protocols within the workspace. This rigorous
semantic anchoring prevents the downstream pipeline from masking logical errors within shifting or am-
biguous conceptual definitions.
When the primary pipeline encounters verification deadlocks or deep heuristic ambiguity, this cluster ini-
tiates a dynamic path-recovery sequence. A swarm of Explorer agents is deployed to propose alternative
mathematical strategies from multiple directions under varied macro-constraints, maintaining high search-
space diversity. This divergent exploration is immediately distilled by the Synthesizer, which evaluates
and ranks the generated proposals. By converting only the most viable proposals into active speculative
branches, the Synthesizer prevents the system from persisting on failed trajectories and substantially reduces
the Orchestrator’s analytical overhead.
Complementing this exploration, the Regulator provides deep structural diagnostics upon verification fail-
ures [1]. Rather than synthesizing new proof segments, it evaluates the failure state to isolate the exact
root cause—whether it stems from a localized proof gap, an invalid lemma formulation, or a definition
mismatch—thereby identifying the minimal responsible party for targeted remediation. Simultaneously,
the Counterexample Hunter (CE-Hunter) aggressively hardens the reasoning process against unprovable
propositions. Through logical deduction or algorithmic script execution, the CE-Hunter actively uncov-
ers boundary-case obstructions and falsifies flawed intermediate claims, ensuring the system promptly
abandons structurally unviable paths.
Documentation. The final stage of the derivation lifecycle centers on the Documentation cluster, which dis-
tills heterogeneous reasoning assets into structured, reader-facing academic artifacts. The Refiner performs
high-level structural compression, distilling verbose derivations into concise, logically sound arguments
while utilizing a blind-verification fallback to ensure formal equivalence with the original proof. Subse-
quently, the Writer compiles these segments into polished academic drafts. By managing stylistic align-
ment, citation formatting, and logical flow, the Writer transforms disjointed intermediate markdown files into
cohesive, publication-grade mathematical prose. This cluster ensures that the system’s accumulated inter-
nal explorations are effectively translated into transmissible knowledge, ready for human peer review or
external formalization.

3.1.2   Command-Line Tooling Layer
Beyond the collaborative workflow of the agents, the system relies on a deterministic Command-Line Tool-
ing layer as its underlying infrastructure, as summarized in Table 1b. The core design philosophy is to
bridge the gap between stochastic language generation and the absolute rigor required for mathematical
proving. Rather than burdening generative models with mechanical executions, this layer acts as a "deter-
ministic exoskeleton." It offloads non-reasoning tasks to reliable software routines, ensuring that the agents’
cognitive capacity is strictly reserved for high-level logical synthesis.
Literature Retrieval. Mathematical proving cannot occur in a vacuum, nor should computational resources
be wasted on re-proving established results. To enable cumulative reasoning, we equip the system with a
dedicated retrieval pipeline that combines two complementary tools: Matlas [25], a semantic search engine
tailored for published mathematical documents, and the official arXiv API, which provides real-time ac-
cess to preprints and their metadata. Because mathematical definitions and theorem boundaries must be
absolutely precise, relying on a model’s internal parametric memory risks fatal hallucinations. Grounding
the agent’s exploration in trusted external repositories ensures that any introduced lemma is historically
verified, preventing the system from building proofs on fabricated mathematical premises.
Local Reference Extraction. Academic literature in mathematics is uniquely dense, characterized by intri-
cate notation, multi-column layouts, and heavy cross-referencing. Feeding raw, unstructured visual doc-
uments directly into an LLM causes severe token bloat and dilutes the model’s attention. This extraction
tool is critical for context window optimization. By converting local reference materials into an instantly
queryable, structured text segment database, it allows agents to perform granular, needle-in-a-haystack
lookups. This preserves the model’s limited context window for multi-step reasoning rather than docu-
ment parsing.
Structural Lint Gates. A robust math prover requires a strict separation between structural syntax and
mathematical logic. The linting tool enforces this decoupling by acting as an automated gatekeeper. Before
a proof draft is even evaluated for logical correctness, it must pass a battery of deterministic shape checkers.


                                                      10
Key Laboratory of Mathematics Mechanization                                                  MechMath Agent Team




                                           (a) Specialist Roles in FL Prover
  Role           Responsibility
  Formalizer     Translates source text into Lean statement scaffolds with bodies marked as sorry.
  F-Reviewer     Validates statement and definition fidelity against the source text to ensure semantic alignment.
  F-Generator    Executes targeted proof derivations for specific theorems or lemmas within isolated workspaces.
  Integrator     Merges verified scratch proofs and artifacts into the master repository under structural constraints.
  Golfer         Refines post-verification code for improved aesthetics and maintainability without altering logic.
  Regulator      Conducts systemic global audits to detect formalization traps and manage reasoning cycle state.

                                              (b) Command-Line Tools
  Tool           Description
  Checking       Compile and verify Lean files as the ground truth for mathematical correctness.
  Scanning       Scans source code for sorry or admit to ensure proof integrity.
  Guarding       Snapshots theorem statements to detect and prevent unauthorized AST-level tampering.
  Indexing       Extracts dependencies and structural outlines to facilitate proof reuse.
  Searching      Use Leansearch, Leanfinder, Leandex and Loogle to retrieve lemmas from extensive libraries.

Table 2: Formal Language Prover. (a) shows six different subagents in the Formal Language Prover. (b) shows five
command-line tools and their interfaces.


If an artifact violates the expected schema or communication protocol, it is rejected immediately. This
engineering discipline prevents the system from wasting expensive model calls and reasoning cycles on
syntactically malformed outputs, ensuring the entire workflow advances on a predictable track.
Cross-model Verification. While the tooling layer consists of deterministic code, it serves as a reliable
broker to orchestrate heterogeneous language models. In formal deduction, a single generative model is
highly susceptible to confirmation bias—frequently overlooking its own subtle logical gaps or false deduc-
tions. This verification framework programmatically introduces cognitive diversity. By routing proof snip-
pets through independent peer-review and blind-testing protocols, the system breaks individual reasoning
traps and exposes hidden vulnerabilities, shifting the proof process from isolated generation to rigorous
multi-model consensus.

3.2     Formal Language Prover

The Formal Language Prover is the core engine for achieving mathematical rigor [28]. Unlike natural lan-
guage systems that rely on large models for cross-verification, mathematical validity here is absolutely and
exclusively determined by the Lean 4 compiler kernel in a deterministic manner. Anchored by this robust
mechanism, the formalization prover exhibits powerful, multi-dimensional core capabilities: it can not only
precisely formalize mathematically stated problems into rigorous code statements, but also autonomously
explore and generate complete formal proofs under stringent compilation constraints. More importantly, it
acts as the ultimate logical referee to assist in verifying informal proofs. By translating the natural language
derivation drafts of large models or human experts into Lean code for mechanical verification, it completely
eradicates logical illusions and loopholes hidden by the ambiguity of natural language.

3.2.1    Formalization Architecture
The transition from natural-language mathematical proofs to machine-verifiable code (e.g., Lean 4) intro-
duces severe cognitive and engineering challenges. Unlike informal reasoning, formalization is highly
sensitive to the semantic gap, where a slight translation error fundamentally changes a theorem’s meaning.
Additionally, it is susceptible to workspace contamination, where exploratory proving corrupts the global file
environment. Furthermore, formal verification systems are susceptible to silent anti-patterns, such as vac-
uous proofs resulting from contradictory hypotheses. To systematically insulate the codebase from these
vulnerabilities, our framework decouples the formalization lifecycle into specialized agent roles, summa-
rized in Table 2a.
To bridge the gap between informal mathematics and formal types, where language models often suffer
from translation drift, the system decouples syntax generation from semantic auditing. The Formalizer
drafts initial Lean scaffolds, while the Formal Reviewer (F-Reviewer) acts as a dedicated gatekeeper. Requiring


                                                          11
Key Laboratory of Mathematics Mechanization                                          MechMath Agent Team




an explicit approval from the F-Reviewer before a statement snapshot is established ensures that formalized
theorems remain strictly aligned with the source text before any proof efforts begin.
To mitigate workspace contamination and dependency rot caused by chaotic trial-and-error exploration, the
architecture enforces a strict isolation paradigm. The Formal Generator (F-Generator) conducts speculative
proof searches exclusively within ephemeral scratchpads, shielding the baseline repository from corrup-
tion. Once a proof is validated, the Integrator serves as the sole interface permitted to merge fragments into
the target file, acting as structural glue that sanitizes namespaces without altering proof logic.
To combat code entropy and silent anti-patterns like vacuous truths, we introduce specialized optimiza-
tion and auditing layers. The Golfer performs conservative, post-hoc syntax cleanups to maximize human
readability without compromising formal correctness. Concurrently, the Regulator conducts global audits
at the end of each reasoning wave, analyzing task ledgers and repository diffs to detect systemic traps like
statement drift or duplicate definitions.

3.2.2    Command-Line Tooling Layer

In this formal environment, agents are empowered by a specialized suite of command-line tools in Table 2b.
Since correctness is deterministically adjudicated by the Lean kernel, our tooling layer acts as a series of
final-verdict gates, categorized by their primary objectives as follows.
Verification. This suite of tools maintains the rigorous boundary of the formal environment. Checking acts
as the system’s "supreme oracle," invoking the Lean compiler to provide a deterministic ground truth that
eliminates model hallucinations. Scanning safeguards the proof chain by auditing source code for unfin-
ished placeholders, ensuring that no sorry or admit keywords bypass formal validation. Complementing
this, Guarding prevents derivation drift by maintaining snapshots of theorem statements and monitoring
Abstract Syntax Tree (AST) integrity, which effectively blocks agents from surreptitiously weakening propo-
sitions to force a successful, yet invalid, compilation.
Discovery. To handle the complexity of massive libraries, these tools optimize the agents’ navigation and
integration capabilities. Indexing provides crucial workspace awareness by extracting dependency graphs
and structural outlines, allowing agents to seamlessly reuse existing lemmas. Building upon this, Searching
offers a multi-dimensional retrieval ecosystem, including leansearch [12] (mixed natural language and
code search), leanfinder [30] and leanexplore [2] (semantic matching search), and loogle (type signature-
based pattern matching) By integrating diverse strategies, it enables agents to precisely anchor relevant
premises, whether they are navigating from a target statement or a specific proof state.

3.3     Knowledge Base Manager

The Knowledge Base Manager (KB Manager) serves as the persistent memory and structural repository
of the harness, enabling the system to manage complex mathematical research beyond the constraints of
transient execution. Departing from the “LLM-as-a-Wiki” paradigm, which treats knowledge as unstruc-
tured text, the KB Manager re-architects the repository into an actionable, object-oriented memory graph.
Through a hub-and-spoke architecture, it coordinates a suite of specialist agents to transform raw inputs
into a rigorously verified, formalization-aware knowledge structure. By decoupling global orchestration
from localized execution, the KB Manager ensures that the system’s reasoning history—ranging from suc-
cessful proofs to verified obstructions—remains transparent, auditable, and unconditionally trustworthy.

3.3.1    Persistent Wiki Knowledge Base

KB Manager adopts the “LLM-as-a-Wiki” paradigm [26], which organizes a persistent knowledge base
around three canonical page types: Source pages that capture raw input materials, Concept pages that distill
generalized insights, and Analysis pages that document analytical procedures. Yet standard implementa-
tions of this paradigm store the content within these pages merely as unstructured, enriched notes, making
them ill-suited for the precise retrieval and compositional demands of mathematical reasoning. To meet
the rigorous requirements of mathematical workflows, the KB Manager re-architects the primitive memory
unit by compiling the content of these wiki pages into a suite of strongly-typed, modular card entities. This
structural refinement decouples invariant mathematical objects (such as definitions and proven theorems)
from the empirical heuristics, incremental proof fragments, and falsified constraints generated during dy-
namic proof search. As a result, the repository transforms from a passive notebook into an actionable,


                                                     12
Key Laboratory of Mathematics Mechanization                                                                                                                                                                            MechMath Agent Team




                                                      Obstruction_NonconstantPivotExactRootGap


                                                                                                                           Obstruction_SupersparseGcdIrreducibilityHardness
                                     Source_BhargavaSarafVolkovich2020DeterministicFactorization


                                                                                                               Concept_SparsePolynomialRepresentation
                                                                                  PartialProof_ConstantPivotExactRootSparsity
                 Lean_SuppliedOutputSparsity


                                                                                                                        Analysis_FactorSparsityRouteMap




                                                                                                                                                          Source_BaraskarDewanSahaSinha2024SparseEquivalenceHardness


                                    Concept_SparsePerfectPowerAlgorithmsConcept_FactorSparsityBounds




                                                                                         Source_BishtVolkovich2025SparseFactorizationProblems




Figure 4: Knowledge Base for Sparse Polynomials. We highlight all related cards to the concept of “Factor Sparsity
Bounds”, including three source, two concept, two obstruction, one Lean, one partial proof, and one analysis card.



object-oriented memory graph that enables granular knowledge retrieval, compositional reasoning, and
the systematic accumulation of exploratory experience.
Beyond optimizing the storage of natural language knowledge, the KB Manager extends its architecture to
bridge the gap between human-readable mathematics and formal verification. The gap between natural
language reasoning and machine-checkable formal representations poses a major obstacle for automated
agents operating in interactive theorem proving (ITP) environments [24]. To overcome this problem, the
system introduces Lean cards as a dedicated formalization interface. These cards ground mathematical
concepts in concrete, machine-verifiable artifacts by explicitly tracking formal declaration names, type sig-
natures, and proof statuses within the Lean environment.
Furthermore, mathematical discovery inherently relies on dynamic, non-linear proof-search trajectories. To
capture this exploratory process, the KB Manager introduces a separate cognitive memory layer comprising
PartialProof and Obstruction cards. These schemata elevate the live, trial-and-error process of proof ex-
ploration to first-class entities within the memory graph. By explicitly separating partial proof constructions
(PartialProof) from falsified logical constraints (Obstruction), this layer preserves both valid intermedi-
ate subgoals and verified dead ends as structured, retrievable knowledge. Consequently, the architecture
enables autonomous agents to navigate complex reasoning spaces and leverage accumulated exploratory
experience without repeatedly rediscovering the same logical obstructions. The explicit taxonomy and data
composition of all these cards are formalized in Table 3a.
Collectively, these cards form a heterogeneous mathematical dependency and evidence graph governed by
strict graph connection rules (detailed in Table 3a) [33]. Driven by this structural foundation, core sys-
tem workflows are modeled directly as graph operations: ingestion initializes and links nodes, query tra-
verses bounded neighborhoods for contextual retrieval, maintenance dynamically repairs broken or weak
connections, and archiving appends formal verification structures to the graph. To guarantee the strict au-
ditability required for safe mathematical reuse, the KB Manager enforces a rigorous operational discipline
that transparently tracks graph evolution while treating human modifications as the authoritative ground
truth. Ultimately, the KB Manager’s contribution lies not merely in expanding context memory, but in es-
tablishing a mathematical card schema and a graph discipline that together render knowledge reusable,
formalization-aware, and safe to compound across extended research sessions. Refer to Figure 4 for an
example of a knowledge base.


3.3.2   Orchestrated Knowledge Lifecycle

To materialize the harness architecture’s core paradigms within the knowledge repository, the KB Manager
replaces conventional linear extraction with a dynamic, state-isolated workflow. The system completely
delegates specialized operations to a suite of functional experts while enforcing strict architectural bound-
aries to preserve global state inspectability.


                                                                                                                                13
Key Laboratory of Mathematics Mechanization                                                 MechMath Agent Team




                                              (a) Knowledge Base Cards
 Card Type        Core Function and Encoded Elements                             Graph Connections
 Source           External literature, including defs, thms, and proofs.         All cards related to the source
 Concept          Cross-source math objects aggregating defs and formulas.       All cards including the concept
 Analysis         Problem-solving insights, recurring proof patterns, etc.       Concept, PartialProof, Obstruction
 Lean             Formal artifacts tracking Lean declarations, proofs, etc.      Concept, Source
 PartialProof     Incomplete proofs with partial structures and lemmas.          Concept, Source, Obstruction
 Obstruction      Dead ends, structural anomalies, and logical conflicts.        Concept, Source, PartialProof

                                         (b) Specialist Roles in KB Manager
 Role           Responsibility
 Registrar      Registers sources into hash-addressed storage and tracks metadata before routing files to specialists.
 Ingester       Compiles natural language sources into cards under a mandatory human confirmation gate.
 Researcher     Queries the wiki graph to answer questions, persisting novel semantic syntheses.
 Maintainer     Preserves graph health by repairing topological anomalies and adding necessary links.
 Archivist      Integrates formal verification by mapping Lean 4 artifacts to cards and cross-indexing with concepts.

Table 3: Knowledge Base Manager. (a) shows six kinds of Knowledge Base cards, their functions and connection roles.
(b) shows five different subagents in the Knowledge Base Manager.



Driven by our framework’s emphasis on minimizing context overflow, this execution pipeline establishes
rigid structural isolation by relying entirely on file-based handoffs rather than conversational history pass-
ing. Under this paradigm, each subagent is strictly restricted to a bounded operational scope to eliminate
mutual cognitive interference (summarized in Table 3b). Upon receiving raw materials, the Registrar is in-
voked exclusively for physical intake—registering files into hash-addressed storage and tracking system
metadata—thereby maintaining a clean separation between source indexing and downstream semantic
processing. Guided by these generated manifests, the Orchestrator dispatches control without transferring
global memory: natural language prose is routed solely to the Ingester for knowledge compilation, while
formal scripts are isolated within the Archivist for Lean 4 integration. For downstream knowledge retrieval,
the Researcher’s exploratory radius is similarly constrained, executing queries by strictly traversing the pre-
compiled global index rather than conducting open-ended web searches. This strict compartmentaliza-
tion of roles systematically prevents memory confusion among specialists throughout extended reasoning
horizons. Meanwhile, the Maintainer’s independent topological audits guaranty global state inspectability
throughout long-horizon reasoning.
Complementing these structural boundaries, the subagents’ operational routines are further restricted by
deterministic behavioral gates to eliminate the logical hallucinations and self-verification biases intrinsic
to LLMs. Even within their isolated domains, agents are denied unilateral write privileges during graph-
mutating operations. For instance, the Ingester is prohibited from silently compiling parsed wiki cards; it is
mandated to halt execution, summarize core takeaways, and await explicit human acknowledgment before
final commit. Similarly, the Maintainer and the Archivist operate under a strict "propose-verify-commit" pro-
tocol. By transforming potential single-agent hallucinations into multi-stage verification obligations, these
behavioral guardrails ensure that the continuously accumulated mathematical graph remains structurally
sound and unconditionally trustworthy.


4   Empirical Evaluation

To evaluate the practical efficacy, mathematical adaptability, and closed-loop coordination capabilities of
our framework, we deployed the system to address several long-standing open problems across Num-
ber Theory, Algebraic Complexity Theory, Differential Algebra, Operator Algebra, and Inequality, moving
beyond static or standardized benchmarks. Table 4 catalogs these solved problems by category. In address-
ing these open problems, MMAT used strategic reasoning, symbolic computation, and formal verification
across complex mathematical problems. To comprehensively demonstrate these capabilities, the remainder
of this section unfolds across three detailed case studies, each highlighting a distinct facet of our frame-
work’s performance.


                                                          14
Key Laboratory of Mathematics Mechanization                                               MechMath Agent Team




Problems solved                                                Areas                     Formal     Human      Ref.
Sparse Polynomial Divisibility Test is CoNP-hard               Algebraic Comp. Theory       ✗          ✓       [36]
Output-sensitive Sparse Polynomial GCD is NP-hard              Algebraic Comp. Theory       ◆          ✓        [8]
Quasi-linear Time Multiplication of Sparse Polynomials         Algebraic Comp. Theory       ◆          ✓       [20]
Sparse Polynomials Exact-root Finding and Factorization        Algebraic Comp. Theory       ✗          ✓       [19]
Katz’s Problem on Generalized Airy Operators                   Differential Algebra         ✗          ✓        [6]
Skew Polynomial Multiplication                                 Differential Algebra         ✗          ✓       [51]
A GCD Criterion of Certain Binomial Coefficients               Number theory                ✓          ✗       [15]
An Integer is Sum of Tri, Pent, and Hept Number                Number theory                ✓          ✗        [7]
Removing non-CM Hypothesis for Shafarevich-Tate Bound          Number theory                ✗          ✓         -
Ideal Equality for a Positive Non-Trace-Class Commutator       Operator Algebra             ✗          ✗        -
Vasc’s cyclic inequality for n = 9 over positive reals         Inequality                   ✗          ✗       [14]

Table 4: Summary of solved problems. To date, we have uploaded nine completed works to arXiv. The “Human”
column indicates whether the work involved human participation, while the “Formal” column denotes whether it has
been formally verified by FL-Prover. The symbol ◆ signifies partial formalization, where only the theorems presented
in our paper are formalized, with all referenced theorems retained as axioms.


Full-Cycle Theorem Proving Pipeline (§4.1). This subsection details a comprehensive, end-to-end expo-
sition of the entire systemic workflow using the open problem OEIS A287616 as a baseline case study. A
proof emerges from the continuous interplay of natural language mathematical discovery, computational
certificate validation, and iterative Lean 4 formalization, yielding a result that is rigorous, computationally
verified, and formally certified [7].
Orchestrated Large-Scale Certification (§4.2). Having established the system’s capacity to close the full
proof cycle on a single problem, we now examine the robustness of its architecture when confronted with
the combinatorial explosion that traditionally overwhelms automated provers. The n = 9 positive-real
case of Vasc’s cyclic inequality serves as a demanding testbed, requiring the system to navigate a vast,
highly non-uniform search space. Here, the central Orchestrator robustly manages a primary verification
scan in Python while simultaneously deploying parallel branches for speculative symbolic computation
and fault-tolerant exception handling. This design successfully validates all 40,320 distinct algebraic cones
without a single failure [14].
From a Single Problem to a Mathematical Project (§4.3). Moving beyond, we lastly examine the frame-
work’s higher-order capabilities to carry out a whole mathematical project, including proof-chain audit,
theoretical reconstruction, and automated scientific discovery. For instance, in sparse polynomial multi-
plication, the system autonomously isolates and refutes a critical probability analysis flaw in the existing
literature, with a counterexample at an astronomical scale (N = 1020 ). Through a bidirectional human–AI
co-reasoning loop, it then reconstructs a sound quasi-linear complexity framework [20]. More importantly,
it steers the broader project-level exploration toward more problems in sparse polynomials, including divi-
sion, decomposition, GCD computation, factorization, and root finding.

4.1   Full-Cycle Theorem Proving Pipeline

We use the open problem OEIS A287616 as a case study to demonstrate the complete theorem-proving
pipeline of the MMAT. The problem asks whether every nonnegative integer n can be represented in the
form
                            x ( x + 1) y(3y + 1) z(5z + 1)
                       n=             +         +          ,   x, y, z ∈ N.                       (1)
                                 2         2          2
To solve this problem, the NL-Prover constructs the whole proof by invoking 137 subagents (Figure 5).
Starting from classical quadratic-form theory, the system progressively develops the Primitive Seed, Move
Calculus, Elementary Descents, Residual Gap, and subsequent reduction lemmas with multiple special-
ized subagents, including the Searcher, Explorer, Sketcher, Generator and Verifier. Once the proof is reduced
to the Residual Cone, multiple mathematical directions—including Finite Partition, Finite Residue Graph,
Compact Projective Cone, Finite Cover, and Uniform Descent—are explored in parallel. The Code Executor
automatically converts these mathematical hypotheses into executable programs, leveraging its symbolic
component in Python constructing Cover Certificates and Exact-LP Certificates through large-scale com-


                                                          15
Key Laboratory of Mathematics Mechanization                                                                                                                                   MechMath Agent Team




   OEIS A287616
                                                                                                             Sketcher          Searcher           Code Executor               Synthesizer          CE-Hunter
                                                                                 NL-Prover
      Prove that any nonnegative integer can be written in the form:                                         Generator          Explorer          Auditor          Verifier           Regulator         Writer

              𝑥(𝑥 + 1) 𝑦(3𝑦 + 1) 𝑧(5𝑧 + 1)
                      +         +          ,       𝑥, 𝑦, 𝑧 ∈ ℕ                                                                                                          Success  137 subagents
                 2         2         2                                                                       Integrator          Formalizer          Regulator
                                                                                 FL-Prover                                                                              Partial  10+ route explored
                                                                                                             F-Generator             F-Reviewer           Golfer
                                                                                                                                                                        Failed   ~3500 lines LEAN
   Problem Understanding and Route Exploration

               Source Investigation                                        Route Exploration                                                                                            Route Exploration
                       Owner: Searcher                                       Owner: Explorer × 3                                                                                    Owner: Explorer × 4
                 Confirm problem is open                            Representation-Transfer
                                                                                                                            Proof Sketch v1                                Component Invariant
                                                                                                                            Owner: Sketcher
                 Collect existing results                           Primitive Odd Representation                                                                         Large Modulus Conductor
                                                                                                               Local Atkin–Lehner / normalizer action
                 Explore related theorems                           Coset/genus theory                                                                                   Bounded-Lag Lexicographic Descent
                 Identify reducible parts                           Analytic route                                                                                       Alternate Normalization Probe


                                                                                                                             Sketch Verify
                                                                         Synthesis & Ranking                                  Owner: Verifier                                         Synthesis & Ranking
                                                                             Owner: Synthesizer                    No purely local / adelic mechanism                                    Owner: Synthesizer
                                                                        Representation-Transfer Win                can prove good-class reachability                                 Route 1 2 failed, Route 3 active



   Proof Development and Bottleneck Identification

                    Proof Sketch v2                                        Proof Generation                                 Exploration for L2                                             Route Audit
                     Owner: Sketcher                                        Owner: Generator × 5                             Owner: Explorer × 3                                           Owner: Auditor
         L0: Primitive Initial Seed                                                                                         Finite Cover                                            Stress test proposed routes
         L1: Transport & Window Lemmas                             L0             L1             L2                         Finite Partition                                        Evaluate feasibility
         L2: Cover & Determinacy Lemmas                                                                                     Residue Graph
         L3: Descent Termination Lemma                                                                                      Compact Cone
                                                                           L3             L4
         L4: Final Assembly Lemma                                                                                           Uniform Descent


                     Sketch Verify                                          Proof Verify                                  Synthesis & Ranking                                       Counterexample Search
                      Owner: Verifier                                     Owner: Verifier                                     Owner: Synthesizer                                         Owner: CE-Hunter
                      Sketch Pass                                 4 Lemmas Pass, 1 Lemma Failed                              Ranking all proposals                            No potential counterexample founded



   Mechanism Blockage and Strategic Recovery
                                                                                                                                                                                         Exploration for L2
                                                                                                                                                                                           Owner: Explorer × 3
                                                                        Structural Collapse                             Amendment Failed                                             Diophantine approximation
                                                                            Owner: Regulator                              Owner: Code Executer
              Computation Enumerate                                                                                                                                                  Residue graph theory
                 Owner: Code Executer                             Thin-sectors are Archimedean and                    non-periodically on absolute
                                                                                                                                                                                     Projective geometry
              Enumerate 12,600 classes                           invisible at any congruence modulus                     coordinate magnitude
                  2,200 PARTIAL
                                                                                                                                                                                       Synthesis & Ranking
                                                                           Amendment to L1                           Partial Classes Analysis                                             Owner: Synthesizer
                                                                          Owner: Sketcher                                     Owner: Auditor                                    Three routes converge on a single
                                                            Amend original L1 with three lemmas L1d,               Classify the PARTIAL to 29 classes
                  Upgrade Algorithm                                                                                                                                              uniform Diophantine floor thesis
                                                             L1e, L1f about Archimedean Window
                  Owner: Code Executer
               0 / 60 complete on hard thin-                                                                                Analysis Verify                                         Objective Misalignment
                     sector smoke test                                      Sketch Verify                                    Owner: Verifier                                           Owner: Regulator
                                                                              Owner: Verifier                          Conclusion is False since flips                   Exact key-determinacy is too hard, Change
                                                                     All 3 amendment lemmas Pass                             residue in 3-adic                               to uniform constant boundedness



   Computation Certification and Proof Assemble

               Exploration for Bound                                     Cone Cover as LP                                 Update Depth to 4                                               Final Assemble
                      Owner: Explorer × 3                               Owner: Code Executer                             Owner: Code Executer                                             Owner: Generator
                  Diophantine Margin                              Residual Cone Cover (Depth-3)                      Residual Cone Cover (Depth-4)                                   Assemble L0-L4 to final proof
                  Finite Residue Graph                                 2658 cones success                                16 hard cone success
                  Compactness Route
                                                                                                                                                                                             Final Verify
                                                                      Code & Lemma Verify                              Code & Lemma Verify                                                   Owner: Verifier
                                                                            Owner: Verifier × 2                            Owner: Verifier × 2
                                                                                                                                                                                             Final proof Pass
                                                                        Both code and lemma Pass                        Both code and lemma Pass

                  Synthesis & Ranking
                    Owner: Synthesizer                                  Boundedness Lemma                               Compactness Lemma                                                 Article Writing
              Compactness as the sketch                                    Owner: Generator                                   Owner: Generator                                              Owner: Writer
          with Diophantine margin as bridge                        Boundary wall local boundedness                 Topological compactness assembly                                 Human-friendly proof article



   LEAN 4 Formalization and Verification                                                                                                                                                    Final Check
                                                                                                                                                                                      Owner: Regulator
               Statement Formalize                                         LEAN 4 Proving                                 Fix the statements                             Final check for dependency of conjecture
                     Owner: Formalizer                                   Owner: F-Generator × 10+                            Owner: Formalizer
           Formalize the statements of all                          Finish 10+ statements proof                    Re-formalize the cited result and
          lemmas and theorems in the proof                          Extract 2 helper lemmas                       computation certification as `axiom`
                                                                                                                                                                                     Integrate LEAN proofs
                                                                                                                                                                                          Owner: Integrator
                                                                    Label 1 cited result as too hard
                                                                                                                                                                                      Merge proof pieces and
                                                                    Leave computation part as sorry
                                                                                                                                                                                       tackle dependencies
                                                                                                                     Alignment Double-check
                                                                                                                            Owner: F-Reviewer
              Semantic Consistency                                                                                  Review the statement fix                                             Proof Golfing
                  Owner: F-Reviewer                                                                                 Double-check semantic consistency                                      Owner: Golfer
      Two statements too narrow, others Pass                                                                        Verify the dependency faithfulness                             Shorten long LEAN 4 proof




Figure 5: The multi-agent theorem proving pipeline example of MMAT on open problem OEIS A287616. The NL-
Prover orchestrates a series of 137 specialized subagents to execute route exploration, dynamic error recovery, large-
scale computational validation, and finally finish the proof. FL-Prover compiles the proof into over 3,500 lines of formal
Lean 4 code, providing rigorous guarantees for the natural-language proof.


                                                                                                        16
Key Laboratory of Mathematics Mechanization                                             MechMath Agent Team




putation, while the CE-Hunter continuously searches for adversarial configurations that may invalidate the
current theory.
The flexibility of the framework becomes most evident during the exploration process. Rather than follow-
ing a single proof strategy, the system repeatedly recovers from failed mathematical routes. For example,
the initial objective is to establish key determinacy, namely that a finite state key uniquely determines the
descent path. However, both mathematical analysis and computational evidence show that this objective
is false. The Regulator therefore reformulates the mathematical target as boundedness, requiring only that
every residual state descends within a uniformly bounded number of steps, without demanding a unique
finite-state description of the descent. The proof subsequently undergoes multiple recovery stages, includ-
ing quantifier-order correction, cover-certificate reconstruction, modulus refinement, proof-depth extension
(ℓW : 4 → 5), and Exact-LP certification, ultimately converging to the complete natural-language proof.
After the natural-language proof is completed, the FL-Prover automatically formalizes the proof in over
3,500 lines of Lean 4 code. Rather than serving as a one-way translation procedure, formalization itself
forms another iterative verification loop. The Formalizer first generates Lean theorem skeletons, after which
the F-Reviewer checks their consistency against the mathematical manuscript. During the first review, the
computational verification is found to be encapsulated by an overly broad axiom boundary. The task is
therefore returned to the Formalizer, who progressively refines the formalization boundary until only two
explicit external assumptions remain: the classical genus local-global theorem and the computer-certified
finite-cover statement fin_cell_residual. All remaining mathematical components—including the Prim-
itive Seed, Move Calculus, Residual Gap, Reduction, and Final Assembly—are fully formalized in Lean4.
Subsequently, the F-Generator, Integrator, Golfer, and Regulator complete theorem proving, repository inte-
gration, code refinement, and global dependency auditing. Finally, the system invokes #print axioms to
confirm that no unintended project axioms remain.
This case study demonstrates MMAT as an end-to-end pipeline spanning from natural language to formal
code. By unifying mathematical discovery, computational validation, and formal verification (FL-Prover),
the system creates a closed, self-reinforcing research loop. This synergy ensures that complex proofs suc-
cessfully converge into results that are simultaneously mathematically rigorous, computationally verified,
and formally certified.

4.2   Orchestrated Large-Scale Certification

We evaluate our framework on the n = 9 positive-real case of Vasc’s cyclic inequality:
                                                    9
                                                         x i − x i +1
                                         C9 ( x ) = ∑                  ≥ 0.                                    (2)
                                                       x
                                                   i =1 i +1
                                                              + x i +2

The main difficulty is that no single sum-of-squares or Arithmetic Mean-Geometric Mean (AM-GM) iden-
tity certifies nonnegativity over the whole positive orthant. The domain must be partitioned into finitely
many regions, each with its own certificate. Through automated theorem retrieval, MMAT first sur-
veyed existing methods and found that Successive Difference Substitution (SDS) successfully handles
n ≤ 7 [42, 49]. However, for n = 9 the 8! = 40,320 cones make a direct reproduction of the lower-order
pattern impossible without an automated, adaptive search.
To overcome this, a sketcher-generator-verifier workflow (Figure 6a) produces a trustworthy proof plan
that splits the argument into algebraic reductions and a case-by-case certification. The algebraic reduction
clears the positive denominators, yielding a homogeneous polynomial P9 . Then it uses cyclic symmetry
to place a maximal coordinate first, followed by sorting and reparametrization via cumulative gaps (SDS
substitution) to map each cone onto a nonnegative orthant. The case certification computes the polynomial
coefficients for every reduced cone: if all coefficients are strictly positive, the cone is immediately certified;
otherwise, a Polya-multiplier method is applied to obtain a nonnegativity witness. A code executor then
carries out this plan with an automated Python pipeline, verifying the 40,320 cones in batches of 64 cases.
During the main brute-force computation, some patterns emerge when 1,152 samples are verified. Thus,
the Orchestrator opens a speculative branch that searches for symbolic invariants able to simplify the verifi-
cation, as shown in the green box of Figure 6b. Within this branch, Explorers scan verified data snapshots to
propose pattern simplifications, which the Sketcher formulates into structured algebraic hypotheses. Rather
than adopting these candidate rules directly, the Orchestrator routes them to the Generator for proof attempts
and to the CE-Hunter for falsification tests. Unfortunately, a structural obstruction falsifies the generalized


                                                        17
Key Laboratory of Mathematics Mechanization                                                         MechMath Agent Team




                   Problem: ∀ xi > 0, prove              0          Branch 1: Verification Simplifying
                         9
      Sketcher                   x −x
                        ∑ xi+i 1 + ix+i+1 2 ≥ 0.      1,152
                                                                                                                Generator
                        i =1
                                                     Some
                                                   patterns             Explorer ×3           Sketcher                      Fail to
                                                                                                                            simplify!

   Generator       Verified proof plan:                                                                         CE-Hunter
                   1. Clear denominators
                                                      5,916         Branch 2: Exception Handling
                   2. SDS reduction
                                                    Fail to
                   If all coeff ≥ 0: quit           prove!          Did not find      Use AM-GM and             Check by code,
      Verifier     Else: Polya multiplier                           any counter-      sum of squares (SOS)      regenerate the
                                                                    examples.         can fix the case!         certificate. Fixed!


                   Scans all 40,320 cases
                    ✓        ✓   ✓   ✓         ?                     CE-Hunter           Generator & Verifier         Code Executor
 Code Executor                                      40,320
            (a) Main certification flow                        (b) Two branches during the main certification

Figure 6: Orchestrated flow in proving Vasc’s Cyclic Inequality for n = 9. The computational backbone relies on an au-
tomated Python pipeline to generate certificate streams. The Orchestrator launches two branches during the verification:
a speculative optimization branch for proactive symbolic invariant discovery (green), and a fault-tolerant mitigation
branch for reactive exception handling and localized proof patch synthesis (red).


hypothesis, so the Orchestrator abandons the global symbolic-expansion route. Because this branch runs in
parallel, these explorations and the eventual rollback do not interrupt the primary verification scan.
Conversely, when the certificate checker leaves a case unresolved (sample 5,916), the Orchestrator pauses
the primary scan and opens a fault-tolerant recovery branch, as illustrated in the red box of Figure 6b.
This mitigation branch first dispatches the CE-Hunter to probe the unresolved case for violations. Find-
ing no counterexamples does not establish nonnegativity, but it signals that the case warrants a dedicated
certificate, so the Orchestrator resumes the primary verification pipeline on the remaining cases. While the
primary scan continues, a Generator synthesizes a proof patch for the skipped case. This patch is then
routed through the Verifier to authenticate its mathematical soundness, and subsequently through the Code
Executor to check by code. After regenerating certificate for the case, the exception is successfully resolved.
Through this orchestrated process, the complete fixed-maximum certificate over the entire lexicographic
range [0, 40320) passed both the mechanical checker and an independent computational audit. A subse-
quent refinement pass produced a shorter proof that was re-verified and adopted, yielding a fully certified
proof of the positive-real n = 9 Vasc inequality. The final certificate classifies every terminal row into one of
three leaf types: 36,815 positive-coefficient leaves, 2,236 Polya-multiplier leaves, and 1,269 leaves certified
by AM-GM–based Sum of Squares (SOS). Refer to [14] for the complete proof.

4.3     From a Single Problem to a Mathematical Project

Having confirmed the framework’s capability in full-cycle theorem proving and robustness in large-scale
machine certification, we now shift the focus to intellectual depth, demonstrating how MMAT can drive an
entire research project. Sparse polynomial computation serves as a running case study in this section.
Sparse polynomials are the standard representation in practice and underpin computer algebra systems
such as Maple and Mathematica, which are widely used in scientific and engineering computation. Surpris-
ingly, for many basic problems in sparse polynomials, including multiplication, division, decomposition,
GCD computation, factorization, and root finding, their computational complexity and optimal algorithms
remain poorly understood [10, 34, 38].
We begin with the first open problem in [38], which asks for a quasi-linear sparse polynomial multiplica-
tion algorithm. A positive solution is given over integers in Giorgi et al. [13], but an automatic audit by
MMAT uncovered a critical logical flaw in their probabilistic analysis. Subsequently, MMAT constructed a


                                                              18
Key Laboratory of Mathematics Mechanization                                            MechMath Agent Team




counterexample, conclusively invalidating the claim. In response, a completely new proof was constructed
through iterative human–AI collaboration, and its correctness was ultimately machine-checked by Lean
4 [20]. With this project underway, we further examined more problems for sparse polynomials and re-
solved four long-standing open problems (Figure 8) [8, 19, 20, 36], among which MMAT provides a rigor-
ous proof of the key theorem. The remainder of this section follows this progression, from automated error
detection to systematic exploration of the topic.



4.3.1   Proof-chain Auditing

The discovery of the logic flaw in Lemma 4.7(ii) represents a paradigm shift: an interactive multi-agent
system can systematically audit intricate proof dependencies and aggressively navigate extreme parameter
spaces to falsify seemingly ironclad theoretical claims.
In theoretical mathematics, primary conclusions rest on a dense, hierarchical web of supporting lemmas
imported from external literature, which are frequently accepted as unverified “black boxes”. MMAT ad-
dresses this through automated proof-chain auditing. As illustrated in the sequential pipeline of Figure 7a,
the Orchestrator parallelized the team’s execution. The Searcher (SEAR) traced upstream dependencies to au-
dit prerequisite assumptions within Huang’s UIPOLY framework [18]. Simultaneously, the Auditor (AUD)
dissected micro-algebraic boundaries, including the intermediate support size Tp and the ordinary product
Fp G p . This synchronized deep-dive allowed the agents to successfully isolate a critical logical flaw and
trigger an automated HALT sequence precisely at Lemma 4.7(ii).
To initiate a concrete refutation, the Orchestrator pivoted operations toward counterexample exploration,
empowering the CE-Hunter to spearhead the search under a hypothesis testing framework formalized by
the Sketcher. Through this setup, the CE-Hunter identified that massive scales cause canceled terms in the
ordinary product Fp G p to split violently upon modulo reductions, triggering an illegal expansion of the
intermediate support set Tp . Leveraging this insight, the CE-Hunter systematically swept the parameter
space and locked onto a highly unexpected configuration at N = 1020 , as displayed in the counterexample
block in Figure 7b. Such extreme scales lie beyond the reach of conventional verification, enabling the
discovery of a structural mutation.
To ground this symbolic insight into definitive proof, the Code Executor performed a parallel Python-based
finite enumeration. As detailed in the green block in Figure 7b, the actual success probability under this
extreme scale plummets to P = 7495/30182 ≈ 0.248, directly refuting the original paper’s theoretical claim of
1 − µ1/2 = 3/4. Backed by this data, the Verifier authenticated the algebraic model, the Regulator issued the
dual-consensus verdict, and the Writer seamlessly compiled the formal refutation report.



4.3.2   Human-MMAT Interaction Proof

With the logic flaw isolated and refuted, the pipeline shifted to theoretical reconstruction, establishing a
framework for quasi-linear bit complexity over integers through interactive human–AI collaboration. This
collaboration formed a bidirectional, self-correcting loop, as the following examples illustrate.
At the finest level, the agent initially conflated the absorption rules of soft-O notation, incorrectly reducing
m log n to Oe (m) by false analogy with the valid n log n = O e (n). Once the human mathematician identified
the error, the agent immediately corrected the derivation and stored the corrected rule, preventing the same
conflation from recurring in subsequent proofs.
At a higher strategic level, the human mathematician proposed deducing the sparse multiplication theo-
rem over finite fields Fq [ x ] from the integer case Z[ x ] via reduction. The agent successfully proved the
required lemmas, verified their compatibility, and confirmed the approach was viable. The resulting val-
idated structures were then ingested by the KB-Manager as reusable building blocks. Had this direction
proved infeasible, the agent would have automatically assumed a skeptical role, constructing explicit al-
gebraic counterexamples to disprove the hypothesis. This negative result would have been relayed to
the human to realign the research direction, and the KB-Manager would have simultaneously archived the
counterexample as an experiential constraint, preventing the collective intelligence from revisiting the same
blind alley.


                                                      19
Key Laboratory of Mathematics Mechanization                                                                                  MechMath Agent Team




                                                                                                       HALT!
        SEAR       AUD                SEAR        AUD                                 SEAR      AUD    Lemma 4.7 part (ii) has a logical flaw!

         Lemma 4.1                   Corollary 4.2                     ...                Lemma 4.7                 ...                   Theorem 4.12

                                                           (a) Global Proof-Chain Auditing


        Lemma 4.7 (ii)                               A counterexample at                                     Through symbolic computation:
        Let Tp be the maximum                        extreme scale!                       CE-Hunter          #( FG ) = 5, p ∈ [401093, 802185],
        of #( Fp G p ) and #( Fp G ′p +
                                                                                                                   
                                                        F = (1 − X N )4 ,                                          5, 7,495 cases
                                                                                                                   
        Fp′ G p )). With probability                                                                         Tp = 7, 17,698 cases
                                                        G = (1 + X N )4 ,
                                                                                                                   
                        µ                                                                                            8, 4,989 cases
                                                                                                                   
        at least 1 − 21 , we have
        Tp ≤ #( FG ).                                   N = 1020 , µ1 = 0.5                Code Executor      ⇒ Probability =
                                                                                                                                   7495  3
                                                                                                                                        < = 1−
                                                                                                                                               µ1
                                                                                                                                                  .
                                                                                                                                  30182  4     2

                                                  (b) Falsification via Counterexample Exploration

Figure 7: The agent-driven verification and counterexample discovery framework. (a) Searcher (SEAR) and Auditor
(AUD) audit prerequisite dependencies in the proof chain in [13], triggering a HALT sequence upon isolating a logical
flaw in Lemma 4.7(ii). (b) CE-Hunter instantiates a highly counterintuitive configuration. The Code Executor subse-
quently runs a parallel Python-based finite enumeration, verifying the effectiveness of the counterexample.


                          Roche [38, 2018]: Is                                                                   Davenport et al [10,        Output-sensitive
 Settle the problem       sparse polynomial                                                                      2009]: Is output-           GCD over fi-
                                                      Multiplication                            GCD
 over integers [20].      multiplication quasi-                                                                  sensitive GCD               nite field is NP-
                          linear?                                                                                polynomial-time?            hard [36].


 Sparse polynomial        Plaisted [34, 1984]:                                                                   Erdös [11, 1949]:           Mulit-variate case
 divisibility test over   Complexity of                                                                          Sparsity of h( x )2         of the conjecture:
                                                        Divisibility
 finite fields CoNP-      sparse polynomial                                                                      implies that of             Sparsity of ge im-
                          divisibility test?
                                                                                            Decomposition
 hard [8].                                                                                                       h( x ). Solved by           plies that of g and
                                                                               Sparse                            Schinzel [41] and           a polynomial-time
                                                                             Polynomial                          Zannier [53].               algorithm for g [19].
 Deciding whether         Bi et al [5, 2016]:
 a sparse polyno-         Deciding whether a
 mial vanishes at a       sparse polynomial               Roots                                                  Gathen et al [4, 46]:       Sparsity of g, h from
 root of unity is NP-     has a root in finite                                               Factorization       sparsity of factors of      that of gh, with h
 hard [36].               field is NP-hard.                                                                      a sparse polynomial.        multilinear [19].


Figure 8: Project on Sparse polynomial with MMAT. Through interaction with MMAT, we resolved six major problems,
among which GCD, Divisability, and Multiplication were explicitly identified as open problems.



4.3.3     Project-level Exploration

The resolution of the sparse multiplication problem served as an epistemic catalyst for a systematic inves-
tigation across the landscape of sparse polynomial computation, with consolidated knowledge structured
by the KN Manager. Figure 4 presents an example of how knowledge about sparse polynomial computa-
tion, as organized by the KB manager MMAT, was progressively mapped over the course of this project.
Figure 8 illustrates the six interrelated problems that were solved. We briefly summarize each problem and
the corresponding contribution in the following.
• Multiplication. Roche’s Open Problem 1 on quasi-linear complexity of multiplication [38] was settled
  over the integers [20].
• Divisibility. The longstanding open problem of the complexity of sparse polynomial divisibility test-
  ing [10, 34, 38] was solved over finite fields by showing that it is coNP-hard under BPP [8].
• GCD. The longstanding problem of output-sensitive GCD computation posed by Davenport et al. [10]
  has been resolved over finite fields and demonstrated to be NP-hard under BPP reductions [36].
• Decomposition. Extending the classical conjecture of Erdös [11] and its univariate resolutions by
  Schinzel [41] and Zannier [53], the multivariate version is solved: sparsity of ge implies sparsity of g
  and a polynomial-time algorithm for g is given [19].


                                                                                20
Key Laboratory of Mathematics Mechanization                                         MechMath Agent Team




• Roots. Extending the known NP-hardness of detecting a root in a finite field [5], it was established
  that deciding whether a sparse polynomial vanishes at a root of unity is NP-hard, further tightening the
  complexity landscape [36].
• Factorization. It is proved that sparsity of gh leads to the sparsity of g and h, provided h is multilin-
  ear [19], advancing the line of inquiries by von zur Gathen and Kaltofen [46] and Bhargava et al. [4].
Thus, MMAT moves decisively beyond solving isolated problems: it acts as an intellectual architect, steer-
ing a single problem toward a comprehensive project that encompasses an entire mathematical domain.

5   Conclusion

In this paper, we introduced the MechMath Agent Team (MMAT), a multi-agent system designed to serve as
a co-pilot across the full cycle of mathematical research. Central to MMAT is the tripartite Harness Archi-
tecture, which decouples system responsibilities into Control, Execution, and Augmentation planes, thereby
reconciling rigorous logical control with the exploratory agility demanded by open-ended problems. Three
specialized agents-a Knowledge Base Manager, a Natural Language Prover, and a Formal Language Prover lever-
aging the Lean 4 compiler—operate in a closed loop to produce formally certified proofs. We evaluated
MMAT on open problems spanning number theory, algebraic complexity theory, differential algebra, and
inequalities; over a two-month deployment, it solved ten problems, including Katz’s question on general-
ized Airy operators, conjectures on sparse polynomial divisibility and multiplication, and a multivariate ex-
tension of the Erdős–Rényi conjecture. These results confirm that MMAT can audit existing proofs, incorpo-
rate human feedback, and steer exploration toward uncharted mathematical directions. This work demon-
strates that structured multi-agent collaboration, when combined with formal verification and human–AI
co-reasoning, can meaningfully accelerate mathematical discovery, opening new avenues for AI-assisted
research.

Acknowledgment

This paper is supported by the Strategic Priority Research Program of CAS Grants XDA0480502 and
XDA0480503, and NSFC Grant No. 12288201.

References
 [1] Chenyang An, Qihao Ye, Minghao Pan, and Jiayun Zhang. QED: An open-source multi-agent sys-
     tem for generating mathematical proofs on open problems. In 3rd AI for Math Workshop: Toward Self-
     Evolving Scientific Agents, 2026.
 [2] Justin Asher. Leanexplore: A search engine for lean 4 declarations, 2025. URL https://arxiv.org/
     abs/2506.11085.
 [3] Amine Barrak. Traceability and accountability in role-specialized multi-agent llm pipelines. In 2025
     40th IEEE/ACM International Conference on Automated Software Engineering Workshops (ASEW), pp. 315–
     322, 2025.
 [4] Vishwas Bhargava, Shubhangi Saraf, and Ilya Volkovich. Deterministic factorization of sparse polyno-
     mials with bounded individual degree. Journal of the ACM, 67(2):Article 8, 2020.
 [5] Jingguo Bi, Qi Cheng, and J. Maurice Rojas. Sublinear root detection and new hardness results for
     sparse polynomials over finite fields. SIAM Journal on Computing, 45(4):1433–1447, 2016.
 [6] Yichuan Cao, Ruyong Feng, Yunfei Li, and Ruichen Qiu. The equivalence problem for generalized airy
     operators, 2026. URL https://arxiv.org/abs/2607.00359.
 [7] Yichuan Cao, Dakai Guo, Ruichen Qiu, Ruyong Feng, and Xiao-Shan Gao. Every nonnegative integer
     is a sum of a triangular, a pentagonal, and a heptagonal number, 2026. URL https://arxiv.org/abs/
     2606.26035.
 [8] Yichuan Cao, Ruichen Qiu, Qiao-Long Huang, Ruyong Feng, and Xiao-Shan Gao. Sparse polynomial
     divisibility test over finite field is conp-hard, 2026.


                                                     21
Key Laboratory of Mathematics Mechanization                                          MechMath Agent Team




 [9] KuanChao Chu, Yi-Pei Chen, and Hideki Nakayama. Cohesive conversations: Enhancing authenticity
     in multi-agent simulated dialogues. In First Conference on Language Modeling, 2024.
[10] James Harold Davenport and Jacques Carette. The sparsity challenges. In Proc. 11th International
     Symposium on Symbolic and Numeric Algorithms for Scientific Computing, SYNASC’09, pp. 3–7, 2009.
[11] P. Erdös. On the number of terms of the square of a polynomial. Nieuw Arch. Wiskd., 23(2):63–65, 1949.
[12] Guoxiong Gao, Zeming Sun, Jiedong Jiang, Yutong Wang, Jingda Xu, Peihao Wu, Bryan Dai, and
     Bin Dong. Leansearch v2: Global premise retrieval for lean 4 theorem proving, 2026. URL https:
     //arxiv.org/abs/2605.13137.
[13] Pascal Giorgi, Bruno Grenet, and Armelle Perret du Cray. Essentially optimal sparse polynomial mul-
     tiplication. In Proceedings of the 45th International Symposium on Symbolic and Algebraic Computation,
     ISSAC ’20, pp. 202–209, New York, NY, USA, 2020. Association for Computing Machinery.
[14] Dakai Guo, Ruichen Qiu, Yichuan Cao, and Ruyong Feng. A finite certificate for the positive n = 9
     vasc inequality, 2026. URL https://arxiv.org/abs/2606.06136.
[15] Dakai Guo, Ruichen Qiu, Yichuan Cao, Ruyong Feng, and Xiao-Shan Gao. A greatest common divisor
     criterion of certain binomial coefficients, 2026. URL https://arxiv.org/abs/2606.22997.
[16] Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Jinlin Wang, Ceyao
     Zhang, zili wang, Steven Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu,
     and Jürgen Schmidhuber. Metagpt: Meta programming for a multi-agent collaborative framework. In
     B. Kim, Y. Yue, S. Chaudhuri, K. Fragkiadaki, M. Khan, and Y. Sun (eds.), International Conference on
     Learning Representations, volume 2024, pp. 23247–23275, 2024.
[17] Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Yu, Xinying Song, and
     Denny Zhou. Large language models cannot self-correct reasoning yet. In B. Kim, Y. Yue, S. Chaudhuri,
     K. Fragkiadaki, M. Khan, and Y. Sun (eds.), International Conference on Learning Representations, volume
     2024, pp. 32808–32824, 2024.
[18] Qiao-Long Huang. Sparse polynomial interpolation over fields with large or zero characteristic. In
     Proceedings of the 2019 International Symposium on Symbolic and Algebraic Computation, ISSAC ’19, pp.
     219–226, New York, NY, USA, 2019. Association for Computing Machinery.
[19] Qiao-Long Huang, Yichuan Cao, Ruichen Qiu, and Xiao-Shan Gao. Deterministic polynomial-time
     exact-root computation for sparse polynomials with bounded total degree, 2026. URL https://arxiv.
     org/abs/2607.02364.
[20] Qiao-Long Huang, Yichuan Cao, Ruichen Qiu, and Xiao-Shan Gao. Quasi-linear time multiplication
     of sparse polynomials with integer coefficients, 2026. URL https://arxiv.org/abs/2606.12100.
[21] Xu Huang, Weiwen Liu, Xiaolong Chen, Xingmei Wang, Hao Wang, Defu Lian, Yasheng Wang, Ruim-
     ing Tang, and Enhong Chen. Understanding the planning of llm agents: A survey, 2024. URL
     https://arxiv.org/abs/2402.02716.
[22] Yichen Huang and Lin F. Yang. Winning gold at imo 2025 with a model-agnostic verification-and-
     refinement pipeline, 2025. URL https://arxiv.org/abs/2507.15855.
[23] Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii, Ye Jin Bang, Andrea
     Madotto, and Pascale Fung. Survey of hallucination in natural language generation. ACM Comput.
     Surv., 55(12), March 2023. ISSN 0360-0300.
[24] Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou, Timothee Lacroix, Jiacheng Liu, Wenda Li, Mateja
     Jamnik, Guillaume Lample, and Yuhuai Wu. Draft, sketch, and prove: Guiding formal theorem
     provers with informal proofs. In The Eleventh International Conference on Learning Representations, 2023.
[25] Haocheng Ju, Leheng Chen, Peihao Wu, Bryan Dai, and Bin Dong. Matlas: A semantic search engine
     for mathematics, 2026. URL https://arxiv.org/abs/2604.17484.
[26] Andrej Karpathy. LLM Wiki. Technical report, 2026. URL https://gist.github.com/karpathy/
     442a6bf555914893e9891c11519de94f.


                                                     22
Key Laboratory of Mathematics Mechanization                                            MechMath Agent Team




[27] Nicholas M Katz. On the calculation of some differential galois groups. Inventiones mathematicae, 87(1):
     13–61, 1987.

[28] Junqi Liu, Zihao Zhou, Zekai Zhu, Marco Dos Santos, Weikun He, Jiawei Liu, Ran Wang, Yunzhou
     Xie, Junqiao Zhao, Qiufeng Wang, Lihong Zhi, Jia Li, and Wenda Li. Numina-lean-agent: An open
     and general agentic reasoning system for formal mathematics, 2026. URL https://arxiv.org/abs/
     2601.14027.

[29] Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and
     Percy Liang. Lost in the middle: How language models use long contexts. Transactions of the Association
     for Computational Linguistics, 12:157–173, 2024.

[30] Jialin Lu, Kye Emond, Kaiyu Yang, Swarat Chaudhuri, Weiran Sun, and Wuyang Chen. Lean finder:
     Semantic search for mathlib that understands user intents, 2026. URL https://arxiv.org/abs/2510.
     15940.

[31] John McCarthy, Marvin L Minsky, Nathaniel Rochester, and Claude E Shannon. A proposal for the
     dartmouth summer research project on artificial intelligence, august 31, 1955. AI magazine, 27(4):12–12,
     2006.

[32] Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, and Joseph E.
     Gonzalez. Memgpt: Towards llms as operating systems, 2024. URL https://arxiv.org/abs/2310.
     08560.

[33] Heiko Paulheim. Knowledge graph refinement: A survey of approaches and evaluation methods.
     Semantic web, 8(3):489–508, 2016.

[34] David Alan Plaisted. New np-hard and np-complete polynomial and integer divisibility problems.
     Theoretical Computer Science, 31(1):125–138, 1984.

[35] Shihao Qi, Jie Ma, Rui Xing, Wei Guo, Xiao Huang, Zhitao Gao, Jianhao Deng, Jun Liu, Lingling
     Zhang, Bifan Wei, Boqian Yang, Pinghui Wang, Jianwen Sun, Jing Tao, Yaqiang Wu, Hui Liu, Yu Yao,
     and Tongliang Liu. Beyond individual intelligence: Surveying collaboration, failure attribution, and
     self-evolution in llm-based multi-agent systems, 2026. URL https://arxiv.org/abs/2605.14892.

[36] Ruichen Qiu, Yichuan Cao, Qiao-Long Huang, Ruyong Feng, and Xiao-Shan Gao. Output-sensitive
     sparse polynomial gcd over finite fields is np-hard, 2026. URL https://arxiv.org/abs/2606.12144.

[37] Tal Ridnik, Dedy Kredo, and Itamar Friedman. Code generation with alphacodium: From prompt
     engineering to flow engineering, 2024. URL https://arxiv.org/abs/2401.08500.

[38] Daniel S. Roche. What can (and can’t) we do with sparse polynomials? In Proc. ISSAC, ISSAC’18, pp.
     16–19, 2018.

[39] Daniel S. Roche. What can (and can’t) we do with sparse polynomials? In Proceedings of the 2018 ACM
     International Symposium on Symbolic and Algebraic Computation, ISSAC ’18, pp. 25–30, New York, NY,
     USA, 2018. Association for Computing Machinery.

[40] Francesca Rossi, Christian Bessiere, Joydeep Biswas, R Brooks, V Conitzer, TG Dietterich, et al. Aaai
     2025 presidential panel on the future of ai research. Association for the Advancement of Artificial Intelli-
     gence, Washington, DC, 2025.

[41] A. Schinzel. On the number of terms of a power of a polynomial. Acta Arithmetica, XLIX:55–70, 1997.

[42] Sil. Answer to “prove a cyclic inequality” (xia–yang references). Mathematics Stack Exchange, 2023.
     URL https://math.stackexchange.com/a/4693459.

[43] Aarohi Srivastava, Abhinav Rastogi, Abhishek Rao, Abu Awal Md Shoeb, Abubakar Abid, Adam
     Fisch, Adam R. Brown, Adam Santoro, and et al. Beyond the imitation game: Quantifying and ex-
     trapolating the capabilities of language models. Transactions on Machine Learning Research, 2023. ISSN
     2835-8856. Featured Certification.


                                                       23
Key Laboratory of Mathematics Mechanization                                          MechMath Agent Team




[44] Xuanbo Su, Yingfang Zhang, Hao Luo, Xiaoteng Liu, and Leo Huang. Mistake notebook learning:
     Batch-clustered failures for training-free agent adaptation. In Maria Liakata, Viviane P. Moreira, Jiajun
     Zhang, and David Jurgens (eds.), Findings of the Association for Computational Linguistics: ACL 2026, pp.
     14629–14645, San Diego, California, United States, July 2026. Association for Computational Linguis-
     tics.
[45] Atharva Tekawade and Suman Banerjee. A makespan and energy-aware scheduling algorithm for
     workflows under reliability constraint on a multiprocessor platform, 2022. URL https://arxiv.org/
     abs/2212.09274.
[46] Joachim von zur Gathen and Erich Kaltofen. Factoring sparse multivariate polynomials. Journal of
     Computer and System Sciences, 31(2):265–287, 1985.
[47] Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai
     Tang, Xu Chen, Yankai Lin, Wayne Xin Zhao, Zhewei Wei, and Jirong Wen. A survey on large language
     model based autonomous agents. Frontiers of Computer Science, 18(6):186345, 2024. ISSN 2095-2236.
[48] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, brian ichter, Fei Xia, Ed Chi, Quoc V
     Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language models. In
     S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh (eds.), Advances in Neural Infor-
     mation Processing Systems, volume 35, pp. 24824–24837. Curran Associates, Inc., 2022.
[49] Bican Xia and Lu Yang. Automated Inequality Proving and Discovering. World Scientific, 2016.
[50] Yizhe Xie, Congcong Zhu, Xinyue Zhang, Tianqing Zhu, Dayong Ye, Minfeng Qi, Huajie Chen, and
     Wanlei Zhou. From spark to fire: Modeling and mitigating error cascades in llm-based multi-agent
     collaboration, 2026. URL https://arxiv.org/abs/2603.04474.
[51] Ke Ye, Yichuan Cao, and Ruichen Qiu. Complexity of low-degree skew polynomial multiplication
     over finite fields, 2026. URL https://arxiv.org/abs/2607.00476.
[52] J. Yu, Y. Ding, and H. Sato. Dyntaskmas: A dynamic task graph-driven framework for asynchronous
     and parallel llm-based multi-agent systems. Proceedings of the International Conference on Automated
     Planning and Scheduling, 35(1):288–296, 2025.
[53] Umberto Zannier. On composite lacunary polynomials and the proof of a conjecture of Schinzel. In-
     ventiones Mathematicae, 174:127–138, 2008.




                                                     24
