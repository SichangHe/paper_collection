                                                    An LLM-Based Assistance System for
                                              Intuitive and Flexible Capability-Based Planning
                                                                          Luis Miguel Vieira da Silva, Nicolas König, Felix Gehlhoff
                                                                            Institute of Automation Technology, Helmut Schmidt University
                                                                                                  Hamburg, Germany
                                                                                  Email: {miguel.vieira, felix.gehlhoff}@hsu.hamburg


                                            Abstract—In modern industry, dynamic environments and the           into a desired goal state while respecting the functions and
                                         complexity of modular and reconfigurable resources require auto-       constraints of the available resources [3].
                                         mated planning of process sequences. Capability-based planning            Classical symbolic planning approaches address this prob-
arXiv:2605.28666v1 [cs.AI] 27 May 2026




                                         approaches address this by automatically generating plans from
                                         semantic knowledge models that describe resource functions in          lem by relying on explicit formal representations of resources,
                                         a machine-interpretable form. Their practical use, however, re-        functions, constraints, and goals, and using planning algo-
                                         mains limited: solver feedback, especially in the case of unsatisfi-   rithms to compute valid plans. However, their practical use
                                         ability, is difficult to interpret, and the knowledge models require   still requires substantial expert knowledge, particularly for
                                         adaptation as operational conditions change or requests become         formulating planning problems in dedicated formal languages
                                         infeasible. This paper presents a hybrid assistance system that
                                         augments an existing capability-based Satisfiability Modulo The-       and for interpreting planning failures [3]. Our previous work
                                         ories (SMT) planning approach with an Large Language Model             has reduced the formulation effort by showing how capability-
                                         (LLM)-based layer for natural-language interaction, explanation,       based knowledge models can be transformed automatically
                                         and adaptation. Formal planning correctness remains with the           into formal planning problems [4]. Yet, in realistic automation
                                         symbolic planner, while the LLM layer handles natural-language         scenarios, planning problems may become unsatisfiable or
                                         access and flexible knowledge model adaptation under explicit
                                         Human-in-the-Loop (HitL) approval. The system decomposes               require adaptation due to resource failures, modified goal
                                         into four components: Capability Grounding, Symbolic Planning,         specifications, or changing environmental conditions. In such
                                         Result Interpretation, and Planning Adaptation, realized as a          cases, diagnosing the cause of failure and deriving suitable
                                         routed agentic workflow in which a central router delegates to         modifications to the underlying planning problem remain
                                         five specialized agents. The system is evaluated on a modular          difficult, especially for non-expert users [5].
                                         production system across four scenario types. Of 23 test cases, 9
                                         of 10 knowledge queries and all 4 satisfiable planning cases were
                                                                                                                   In parallel, Large Language Models (LLMs) have demon-
                                         handled correctly, 3 of 4 unsatisfiable cases produced concrete        strated strong performance in natural-language interaction,
                                         repair proposals, and all 5 adaptive planning scenarios resolved       task explanation, and complex reasoning [6]. These properties
                                         into satisfiable plans through iterative, user-approved knowledge      make them promising for facilitating non-expert access to
                                         model modifications. The findings confirm that combining for-          formal planning systems. At the same time, purely LLM-
                                         mal planning with LLM-based assistance substantially improves
                                         accessibility and adaptability in industrial automation.
                                                                                                                based planning remains unsuitable for many industrial use
                                            Index Terms—Large Language Models, Hybrid AI, Capa-                 cases because it may hallucinate and cannot be relied upon
                                         bilities, Ontologies, Automated Planning, Satisfiability Modulo        to satisfy hard logical and physical constraints consistently
                                         Theories, Agentic Systems, Knowledge Graphs.                           [7], [8]. For safety-critical and industrial applications, a hybrid
                                                                                                                architecture is therefore a promising direction: the symbolic
                                                                I. I NTRODUCTION                                planner remains responsible for correctness and formal con-
                                            Modern industrial automation systems operate in increas-            sistency, while the LLM serves as an interaction, explanation,
                                         ingly dynamic environments. Rapidly changing customer de-              diagnosis, and adaptation layer [9].
                                         mands, shorter product life cycles, flexible batch sizes, and             This paper follows this direction by extending our existing
                                         changing operating conditions require these systems to adapt           capability-based Satisfiability Modulo Theories (SMT) plan-
                                         quickly to new tasks and constraints, which is a central               ning approach from [4] with an LLM-based assistance layer.
                                         objective of Industry 4.0 [1]. At the same time, industrial            The work addresses the following research questions:
                                         automation environments are complex and interconnected                 RQ1: How can LLMs enable natural-language interaction
                                         through the modular integration of heterogeneous resources                     with capability-based planning, covering both knowl-
                                         such as manufacturing machines and autonomous robots [2].                      edge queries and the formulation of planning problems?
                                            In such environments, process planning, i.e., the determi-          RQ2: How can planning results for both satisfiable and unsat-
                                         nation of a suitable sequence of functions, can no longer be                   isfiable planning problems be explained in a way that
                                         regarded as a static, one-time engineering task. As manual                     is understandable to users?
                                         planning becomes too labor-intensive, slow, and error-prone in         RQ3: How can LLMs derive actionable adaptation sugges-
                                         such dynamic environments, automated planning approaches                       tions from unsatisfiable solver feedback and reported
                                         are required. Such approaches transform an initial system state                environmental changes to support planning adaptation?
   The remainder of this paper is structured as follows. Sec-        to the underlying planning problem and capability model
tion II reviews related work on symbolic planning, LLM-              remains difficult, especially for non-expert users. Moreover,
based planning, and hybrid planning architectures. Section III       the approach does not provide a natural-language interface for
presents the concept and architecture of the proposed assis-         querying capability knowledge, explaining planning outcomes,
tance system, building on our previously published capability-       or assisting users in adapting the planning problem under
based planning approach. Section IV describes its prototypi-         changing conditions.
cal implementation. Section V reports the evaluation results.           These limitations motivate the consideration of approaches
Finally, Section VI concludes the paper and outlines future          that complement automated planning with more accessible
work.                                                                forms of interaction, explanation, and adaptation.
          II. BACKGROUND AND R ELATED W ORK                          C. LLMs for Planning
A. Classical Planning Approaches                                        Recent work has explored the use of LLMs for planning due
   Classical planning approaches provide the formal founda-          to their strong performance in natural-language understanding,
tion for automated process planning by representing states, ac-      reasoning, and task decomposition [7]. In contrast to classical
tions, and goals explicitly and by computing action sequences        planning approaches, LLMs can process user requests directly
that achieve a desired target state [3]. Foundational work           in natural language and generate planning-relevant outputs
such as STanford Research Institute Problem Solver (STRIPS)          without requiring users to formulate problems in dedicated
established the paradigm of modeling actions through pre-            formal languages. This makes them attractive for improving
conditions and effects, thereby enabling systematic search in        accessibility and flexibility in planning-related tasks [9].
state spaces [10]. Later, standardized modeling languages such          Wang et al. propose the Describe, Explain, and Plan System,
as Planning Domain Definition Language (PDDL) separated              in which planning is organized as an iterative loop of four com-
domain descriptions from concrete planning instances and en-         ponents [15]. A descriptor first translates observations from
abled the use of generic planning algorithms across application      the environment into structured descriptions, an LLM then
areas [11]. More recently, satisfiability-based methods have         acts as an explainer that analyzes failures and evaluates states
become increasingly relevant. In particular, SMT-based plan-         and preconditions using few-shot chain-of-thought prompting.
ning extends Boolean satisfiability by richer theories such as       Based on this information, the planner generates candidate
arithmetic and is therefore well suited for industrial planning      subgoals that are assessed by a selector with respect to their
problems with numerical constraints [12].                            expected success. However, the approach lacks formal con-
   However, defining such planning problems typically require        straint and state-transition encoding and therefore provides no
substantial expert knowledge, while their formulation often          guarantees of plan correctness, completeness, or precondition
remains manual and labor-intensive [13].                             safety. Instead, it shifts part of the effort to costly online failure
                                                                     handling during execution.
B. Capability-based SMT Planning                                        Zhou et al. propose Language Agent Tree Search, which
   A relevant approach to reducing the manual effort of for-         combines LLM-based reasoning and acting with Monte Carlo
mal planning is our previous capability-based SMT planning           Tree Search to explore multiple solution paths instead of
method, which addresses the gap between semantic knowledge           following a single sequential reasoning chain [16]. The LLM
modeling and process planning by automatically generating            is used both to guide search and to generate self-reflective
planning problems from an existing capability model [4]. In          feedback for subsequent iterations. However, the approach still
this context, capabilities describe the functions of available re-   does not provide formal guarantees that the generated plans
sources together with their inputs, outputs, and constraints in a    satisfy hard logical constraints. In addition, the considered
machine-interpretable form [14]. Based on this ontology-based        benchmarks such as WebShop and coding tasks are not di-
representation, relevant planning information is extracted from      rectly comparable to industrial automation scenarios with strict
the knowledge model, transformed into an SMT problem, and            logical, temporal, and resource-related requirements.
solved using an off-the-shelf SMT solver [4]. By deriving               Silver et al. use GPT-4 as a generalized planner that syn-
the planning problem directly from the capability model, the         thesizes executable Python programs from PDDL domains and
approach avoids the need to formulate planning instances             few-shot examples [17]. The generated programs are validated
manually in a dedicated planning language. At the same               externally with a PDDL validation tool and iteratively repaired
time, SMT provides a suitable formal basis for representing          if syntax or semantic errors occur, which improves inspectabil-
both logical and numerical constraints, which is particularly        ity and verifiability. However, the evaluation is limited to rather
relevant for industrial automation scenarios.                        simple generalized-planning domains for which generalized
   If the generated SMT problem is satisfiable, the solver           solutions could largely be provided manually. Moreover, the
returns a valid plan in terms of selected capabilities and           method depends strongly on meaningful PDDL identifiers,
corresponding parameter assignments. If the problem is un-           suggesting that performance relies not only on formal structure
satisfiable, the solver returns a set of conflicting constraints     but also on natural-language cues and possible pretraining bias.
responsible for the infeasibility. While this provides useful           Overall, these works show that LLMs can usefully support
diagnostic information, interpreting these conflicts with respect    planning-related reasoning, task interpretation, and user inter-
action. At the same time, when used as the main planning com-        tifying applicable actions, and use these findings to develop
ponent, they remain limited by hallucinations, missing formal        Similarity-based Planning (SimPlan) [22]. In this hybrid ap-
guarantees, and unreliable handling of hard constraints [7], [8].    proach, classical planning components provide state and action
This is particularly problematic in industrial automation, where     information, while the LLM is used as a heuristic for action
planning results must satisfy explicit logical and numerical         selection. However, the approach assumes that the relevant
constraints and remain consistent with the underlying system         planning knowledge is already available in a formal symbolic
model. Accordingly, recent work increasingly motivates hybrid        representation, leaving the challenge of semantic grounding
approaches in which LLMs complement rather than replace              unresolved. Moreover, although the work analyzes model fail-
formal planning back ends, for example, by supporting inter-         ures in detail, it does not provide a user-oriented explanation
action, explanation, or adaptation while correctness is ensured      or assistance layer for making such failures actionable.
by symbolic methods [9].                                                Overall, hybrid approaches demonstrate that LLMs are
                                                                     most effective in planning settings when they complement
D. Hybrid Planning Approaches                                        rather than replace formal planning methods. Existing work
   To address the limitations of purely LLM-based planning,          mainly focuses on problem translation, heuristic support, or
recent work increasingly combines LLMs with classical plan-          consistency repair, while support for natural-language access
ning methods. In these hybrid approaches, LLMs are typically         to planning knowledge, understandable explanation of unsatis-
used for natural-language understanding, translation, expla-         fiable results, and concrete guidance for adapting the planning
nation, or intermediate reasoning, while formal planners or          problem remains limited. This gap is particularly relevant for
solvers remain responsible for computing correct plans.              industrial planning, where non-expert users must interact with
   Liu et al. propose LLM+P, a framework in which an                 formal planning systems under changing requirements and
LLM translates natural-language task descriptions into for-          disturbances.
mal PDDL problem specifications that are then solved by
a classical planner [18]. This combines the accessibility of               III. M ETHOD – H YBRID P LANNING A PPROACH
natural-language interaction with the correctness of symbolic           This work proposes an LLM-based assistance system for
planning. However, the approach assumes a fixed planning             capability-based SMT planning in industrial automation. The
domain and focuses on generating problem instances rather            method augments, rather than replaces, the underlying formal
than adapting the domain description itself. As a result, it is      planner in order to improve accessibility for non-expert users.
less suitable for dynamic automation scenarios in which not          In particular, it addresses three objectives:
only goals but also the underlying planning basis may need to           (i) natural-language access to capability knowledge and
be modified under changing conditions.                                      planning functionality,
   Ye et al. present SATLM, which uses an LLM to parse                 (ii) understandable explanation of planning outcomes in-
natural-language reasoning problems into formal constraints                 cluding unsatisfiable results, and
and delegates the actual solving to a symbolic satisfiability         (iii) user-guided support for adapting the planning basis
solver [19]. Pan et al. pursue a similar direction with Logic-              under changing conditions.
LM, which structures reasoning into problem formulation,             To achieve this, the method combines a formal planning
symbolic reasoning, and result interpretation [20]. Natural-         back end for correctness and constraint satisfaction with an
language problems are translated into symbolic representa-           LLM-based assistance layer for interaction, explanation, and
tions, solved by a deterministic symbolic reasoner, and trans-       adaptation support.
lated back into natural language. A self-refinement mechanism
further uses solver feedback to iteratively improve the gener-       A. System Overview
ated formulation. Both approaches demonstrate the benefits of           The system architecture comprises four components, draw-
combining LLMs with formal reasoning back ends. However,             ing on the hybrid decomposition proposed in [20]: Capability
they are evaluated on rather small and simple tasks that are         Grounding, Symbolic Planning, Result Interpretation, and the
not directly comparable to industrial automation scenarios and       Planning Adaptation. Fig. 1 gives a schematic overview.
do not focus on adapting the planning basis under changing              Capability Grounding is the entry point for all user inter-
conditions or on handling unsatisfiable planning problems.           action. The user’s natural-language request is interpreted and
   Jha et al. combine LLMs with an SMT solver by letting the         matched against the available capability knowledge. The pro-
LLM generate an initial solution or formalization, which is          vided capabilities of available resources are already modeled
then verified and iteratively corrected using solver-generated       in the capability ontology and form the domain description.
counterexamples [21]. However, the LLM remains the core              Depending on the intent, the system either answers a knowl-
component for solution generation, while the solver mainly           edge query directly from the graph or identifies candidate
serves verification and repair. Moreover, the approach does          required capabilities – describing a specific goal for the
not support users in understanding results or deriving concrete      industrial automation system – corresponding to the user’s
adaptations of the planning basis.                                   goal, which the user then confirms, thereby establishing the
   Hirsch et al. analyze the planning weaknesses of LLMs,            planning problem. Symbolic Planning takes the confirmed
particularly their difficulties in tracking world states and iden-   required capability together with the provided capabilities
       1         Capability Grounding                      2                           Symbolic Planning [4]
                               Query                                                                                                            1: …
                                                                                                                                                         Plan
                                                                                         x_0 = 1
                                                                                         x_1 = y_0
                                                                                         x ->
                                                                                            (x_0 = 1)                                           2: …
                                                                                                                                                3: ...

          Graph
         Database                                                                                                             X
        Capability                                          Capability       Transformation                    SMT
                                          LLM                                                                                                            Unsat
        Ontology                                            Ontology            to SMT                        Solver


       3             Result Interpretation                                  4                           Planning Adaptation


        1: …
        2: …                                                                                                                  by
                                                                                                                              n Ico
        3: ...                                                                                                                 Pro nP
                                                                                                                                  jec ai
                                                                                                                                     t




        Planning                                 NL                                    Changing                                            Capability
                              LLM                                           Unsat                                 LLM
         Result                              Explanation                               Conditions                                           Update


Fig. 1. Overview of the proposed hybrid planning assistance system, comprising four components: Capability Grounding interprets user requests and grounds
them in the capability knowledge; Symbolic Planning transforms the capability model into an SMT problem and solves it; Result Interpretation translates the
outcome into natural language; and the Planning Adaptation handles unsatisfiable results and changed conditions through knowledge graph updates.



and automatically transforms them into an SMT problem and                       components differ in their required tools, reasoning styles, and
solves it by using a solver as presented in our approach                        context – which makes a decomposition into specialized LLM
from [4]. If the problem is satisfiable, a plan is returned                     agents a natural fit: each agent can be given a focused system
in terms of selected capabilities and parameter assignments.                    prompt, a targeted tool set, and only the state information
Otherwise, the solver returns a minimal unsatisfiable set of                    it actually needs, rather than being confronted with the full
constraints. Result Interpretation translates the outcome into                  complexity of the system in every call [23].
a natural-language explanation for the user, covering both
successful plans and infeasibility diagnoses. The Planning                         The key design decision within this agent-based realiza-
Adaptation is entered in two situations. First, when planning                   tion concerns the coordination strategy. Three patterns were
yields an unsatisfiable result, the unsatisfiable set of constraints            considered. A monolithic architecture uses a single LLM
is analyzed to determine the root cause of infeasibility, a                     with one large prompt that must handle all possible user
concrete adaptation to the modeled capabilities is derived and                  intents, tool calls, and reasoning tasks. In practice this leads
presented to the user for approval, and planning is re-attempted                to prompt overload: heterogeneous instructions interfere with
with the updated knowledge graph. This loop continues until                     each other, the relevant context for any given subtask is diluted
a satisfiable plan is found or the conflict is classified as                    by irrelevant information from others, reliability degrades as
unresolvable. Second, when a changed situation is reported,                     prompt complexity grows, and traceability suffers – it becomes
the affected provided capabilities must first be updated in                     difficult to understand which part of the prompt drove a given
the knowledge graph before planning can be re-attempted.                        output or where a failure originated. A fully autonomous
In both cases, the knowledge graph is updated with explicit                     multi-agent system gives each agent the freedom to decide
user validation, ensuring that the capability model reflects                    dynamically which sub-agents to invoke and in what order.
the current state of the system before a new plan is sought.                    While this maximizes flexibility, the execution path becomes
This process is distinct from the self-refinement mechanism in                  difficult to forecast: it is unclear in advance which steps
[20], which corrects errors in problem formulation; here, the                   will be performed, in what sequence, and whether required
problem formulation is correct but the capability model itself                  Human-in-the-Loop (HitL) approval points will be reached
must be adapted to match changed or infeasible conditions.                      before the capability model is modified. A routed workflow
                                                                                addresses both shortcomings. The overall control flow follows
B. Agent Workflow                                                               a defined structure that can be anticipated and traced, while
   The decomposition into four components described above                       individual agents retain full flexibility in how they use their
naturally imposes different requirements on the underlying                      tools to accomplish their specific subtask. A central Router
LLM usage. For example, Capability Grounding requires                           Agent classifies the user intent and delegates to the appropriate
querying structured graph data and interpreting diverse user                    specialist, while HitL checkpoints are placed at fixed, well-
intents, while symbolic Planning requires invoking an external                  known positions in the workflow, ensuring that no capability
solver and interpreting its output. The subtasks of the four                    model modification is applied without explicit user approval.
                                                    Knowledge
                                                    Explanation




                                                     Knowledge
                                                                                                 Planning                Plan
     User Request           Router Agent              Retrieval               HitL
                                                                                                  Agent               Explanation
                                                       Agent




                                                                                                Analyze &
                                                                        Capability
                                                                                                Adaptation               HitL            Repair Agent
                                                                       Mapper Agent
                                                                                                  Agent


Fig. 2. Agentic workflow illustrating the three interaction paths: a knowledge query is answered directly by the Knowledge Retrieval Agent; a planning request
proceeds through capability retrieval and the Planning Agent, with the unsatisfiable path triggering the Analyze and Adaptation Agent and the Repair Agent
in a replanning loop; and a runtime failure report triggers capability identification, an adaptation proposal, and a knowledge graph update before replanning.
HitL markers indicate human validation checkpoints.



   To define the agents required for this routed workflow,                        result, and translates the plan or infeasibility outcome into
the overall process flow of the system was analyzed and                           natural language for the user.
decomposed into distinct process types. Four process types                      • Analyze and Adaptation Agent: interprets the unsatisfiable
were identified: (i) intent classification, which must deter-                     set of constraints or reported runtime changes using chain-
mine what kind of request the user has issued before any                          of-thought reasoning and derives a concrete adaptation pro-
other processing can begin, (ii) knowledge retrieval, which                       posal for the capability model.
queries the capability knowledge graph to obtain structured                     • Repair Agent executes the approved modifications to the
information about available resources and their capabilities,                     capability knowledge graph. Once the user has confirmed a
(iii) planning and explanation, which invokes the formal                          proposed adaptation via a HitL checkpoint, the Repair Agent
solver and translates its output into language understandable                     applies the necessary changes and prepares the updated
to the user, and (iv) constraint analysis and adaptation, which                   model for replanning.
reasons over infeasible results and derives concrete proposals                     A shared state object persists intermediate results across
for modifying the capability model. Each of these process                       agents within a session. HitL control points are placed at three
types is sufficiently distinct in its required tools, inputs, and               stages: (1) confirmation of the target required capability before
reasoning style to warrant dedicated agents. The workflow                       planning is initiated, (2) approval of proposed capability model
therefore comprises six specialized agents:                                     adaptations in response to an unsatisfiable result, and (3) con-
• Router Agent: classifies user input into one of three intent                  firmation of capability model changes when a runtime failure
  categories – knowledge query, planning request, or runtime                    is reported. These checkpoints ensure that no modification to
  failure report – and routes control to the appropriate work-                  the capability model is applied without explicit user approval.
  flow branch.                                                                     The workflow supports three interaction paths, illustrated
• Knowledge Retrieval Agent: retrieves structured information                   in Fig. 2. For a knowledge query, the Router Agent routes
  from the capability knowledge graph, including descriptions                   the request directly to the Knowledge Retrieval Agent, which
  and parameter constraints of available provided capabilities.                 answers from the capability knowledge graph and returns a
• Capability Mapper Agent: establishes the connection be-                       natural-language response to the user. For a planning request,
  tween formal constraint or failure information and the                        the Router Agent routes to the Knowledge Retrieval Agent to
  capability descriptions stored in the knowledge graph. This                   retrieve suitable required capabilities, which the user confirms
  mapping is essential not for the planning step itself – which                 via the first HitL checkpoint, before the Planner Agent invokes
  operates directly on the formal model – but is required in                    the solver. If the result is satisfiable, the plan is returned
  two subsequent situations: First, when the solver returns                     to the user in natural language. If it is unsatisfiable, the
  an unsatisfiable result, the Analyzer needs to know which                     Analyze and Adaptation Agent analyzes the constraint set,
  capability a given constraint refers to in order to reason                    the Capability Mapper Agent then establishes the connection
  about what needs to change in the model by comparing                          to provided capabilities and required capability, derives an
  the descriptions and parameter structures of required and                     adaptation proposal, and the user approves it via the sec-
  provided capabilities. Second, when a changed condition is                    ond HitL checkpoint before the Repair Agent updates the
  reported, the system must identify which capabilities in the                  knowledge graph and replanning is attempted. For a runtime
  knowledge graph are affected before it can be updated.                        failure report, the Router Agent routes to the Analyze &
• Planning Agent: triggers the SMT planner, receives the                        Adaptation Agent, which routes to Capability Mapper Agent to
identify the affected capabilities; the Analyze and Adaptation
Agent proposes the necessary capability model update, the user
                                                                                                                 User
confirms via HitL checkpoint, the Repair Agent applies the                                                      (Actor)
change, and replanning is initiated.
C. Planning Adaptation Cycle                                                                            Interaction Layer
                                                                                                                CLI, HitL
    When the planner returns an unsatisfiable result or a
changed operational condition is reported, the system enters
the Planning Adaptation Cycle. Rather than terminating or                                             Orchestration Layer
                                                                                                 LangGraph, State Graph, Routing
returning a bare failure message, the system attempts to
identify why the current capability model cannot satisfy the
                                                                                                           Agent Layer
request and to propose a concrete, user-approved modification.                               LangChain, LLM-based Agents with Tools
    The cycle proceeds in four steps. First, the Analyze and
Adaptation Agent examines the unsatisfiable constraint set –                                           Data Access Layer
or the reported change – using chain-of-thought reasoning to                                         Client Classes, Cache & Context

determine the root cause of infeasibility. Second, it derives
a concrete adaptation proposal: a targeted modification to
                                                                                GraphDB                    SMT-Planner                   LLM-API
the capability knowledge graph that would resolve the iden-                  (Capability Ontology)         (Planning Problem)          (Language Model)
tified conflict. Third, the proposal is presented to the user
for approval (HitL), ensuring that no change is applied au-
tonomously. Fourth, once approved, the Repair Agents updates
                                                                   Fig. 3. Four-layer implementation architecture of the assistance system,
the knowledge graph and planning is re-attempted. This loop        comprising an interaction layer (CLI, HitL logic), an orchestration layer
continues until a satisfiable plan is found or the conflict is     (LangGraph state graph and routing), an agent layer (LangChain-based LLM
classified as unresolvable given the available resources.          agents with tools), and a data-access layer (client classes, caching) connecting
                                                                   to GraphDB (capability ontology), the SMT planner, and the LLM API.
    The cycle is entered from two distinct situations. In the
unsatisfiable (UNSAT) case, the constraint analysis drives
the adaptation proposal directly from the solver output. In
the changed-condition case, the user reports a runtime event
(e.g., a resource becoming unavailable), the relevant provided
capabilities are removed or updated in the knowledge graph
with user confirmation, and planning is then re-attempted with        Tool definitions are scoped per agent. The Knowledge
the updated model. In both cases, the knowledge graph is           Retrieval Agent is equipped with SPARQL Protocol and RDF
updated before re-planning, ensuring that the capability model     Query Language (SPARQL) SELECT and ASK query tools to
reflects the current state of the system.                          retrieve structured information from the capability knowledge
                    IV. I MPLEMENTATION                            graph hosted in a GraphDB triple store. The Capability
   The system is implemented in Python using LangGraph1 . as       Mapper Agent compares capability descriptions and parameter
the workflow orchestration framework. LangGraph represents         structures of required and provided capabilities to reduce the
the agentic workflow as a directed graph in which nodes            search space for the Analyze and Adaptation Agent. The
correspond to agents and conditional edges encode the routing      Planner Agent invokes our planning approach from [4] as an
logic determined by the shared state. Each agent is realized       external tool and receives either a valid plan or an unsatisfiable
as a ReAct agent [24]: it receives the current shared state and    constraint set. The Router Agent performs few-shot prompt
iteratively reasons about which of its available tools to call,    classification with no external tool calls. The Analyze and
executes them, and incorporates the results before producing       Adaptation Agent employs chain-of-thought prompting as in-
a final output that is written back to the shared state. The       troduced in [6] to reason over infeasible constraints or reported
overall control flow, however, follows the fixed graph structure   runtime changes and derive a concrete adaptation proposal.
– routing decisions are determined by the graph edges, not by      The Repair Agent is equipped with SPARQL INSERT and
the agent itself, keeping the execution path predictable and       DELETE update tools to apply approved modifications to
easily inspectable.                                                the knowledge graph. All agents use GPT-4o mini as the
   Fig. 3 shows the four-layer implementation architecture: an     underlying LLM. The Analyze and Adaptation Agent uses
interaction layer handling user I/O and HitL logic via a CLI;      GPT-4o to meet the higher reasoning demands of multi-step
an orchestration layer realizing the LangGraph state graph,        constraint analysis and adaptation derivation. The temperature
shared state, and routing; an agent layer executing the LLM-       parameter is set to zero to increase reproducibility and relia-
based ReAct agents via LangChain; and a data-access layer          bility. All LLM calls enforce structured outputs via a JSON
providing client interfaces to the three external systems.         schema defined in each agent’s system prompt, ensuring that
                                                                   intermediate results are machine-readable and can be reliably
  1 https://www.langchain.com/langgraph                            passed between agents through the shared state.
                             V. E VALUATION                                                       TABLE I
                                                                        E VALUATION RESULTS PER SCENARIO CATEGORY. Successful COUNTS
A. Experimental Setup                                                     CASES IN WHICH ALL SCENARIO - SPECIFIC CRITERIA ( DEFINED IN
                                                                         S ECTION V-A) WERE FULLY SATISFIED ACROSS ALL REPETITIONS .
  The system is evaluated using a capability model of a
modular production system available in our laboratory. The                 Scenario             Cases    Repetitions    Successful
model encodes the provided capabilities of resources as OWL                Knowledge Query        10          1             9
individuals conforming to the CSS capability reference model               SAT Planning            4          5             4
[14], including input, output, and constraint parameters. The              UNSAT Planning         4           5             3
modeled capabilities and test scenarios are publicly available2 .          Adaptive Planning       5          5             5
  Evaluation scenarios are organized into four categories that
together cover all three research questions:
• Knowledge Query (KQ): natural-language questions about                 All 4 SAT planning cases were fully satisfied across all 5
  available capabilities and resources, answered by querying          repetitions. The Planner Agent consistently translated struc-
  the knowledge graph without triggering the planner (RQ1).           tured solver output into clear natural-language explanations,
• SAT Planning: planning requests for which a valid plan ex-          including correctly sequencing multi-step plans such as trans-
  ists; the system must identify the correct required capability,     port followed by drilling, and listing the relevant parameter
  invoke the solver, and produce a correct natural-language           assignments alongside each step (RQ1, RQ2).
  explanation of the resulting plan (RQ1, RQ2).                          UNSAT diagnoses were fully satisfactory in 3 of 4 cases
• UNSAT Planning: planning requests that are infeasible under         (RQ2). As a representative example, a user request triggered
  the current capability model; the system must recognize             the system to identify two independent conflicts in a single
  infeasibility and provide an understandable explanation of          response: Conflict 1 – “the required output product depth of
  the cause (RQ2).                                                    2 mm is outside the acceptable range of 5 mm to 10 mm for
• Adaptive Planning (AP): planning requests that begin as             the drilling module”, with the proposed repair of adjusting the
  infeasible but can be resolved through iterative knowledge          depth to 5 mm; and Conflict 2 – “the required station ID is set
  graph adaptation; the system must propose, obtain user              to 15, which does not match the provided station ID of 3”,
  approval for a proposed adaptation, and apply modifications         with the proposed repair of aligning the required station ID to
  until a satisfiable plan is found (RQ3).                            3. This same case was also the only one with reproducibility
                                                                      variance: in 2 of 5 repetitions the proposal aligned the transport
   A total of 23 test cases were evaluated: ten knowledge
                                                                      target station to the start station (3) instead of the conveyor’s
queries, four SAT scenarios, four UNSAT scenarios, and
                                                                      reachable end station (7) – a repair that is formally consistent
five adaptive planning scenarios. Each test case specifies a
                                                                      but causes the planner to drop the transport step and return
natural-language user request and a reference outcome. SAT,
                                                                      a plan that misses the user’s transport intent. The remaining
UNSAT, and AP scenarios were each repeated five times
                                                                      UNSAT cases yielded near-verbatim identical responses across
to assess reproducibility. Outcomes are assessed qualitatively
                                                                      all five repetitions.
against scenario-specific criteria: KQ cases on completeness,
ontological correctness against the underlying graph, and un-            All 5 adaptive planning cases were successful: approved
derstandability; SAT cases on step completeness, parameter            modifications were applied via SPARQL and replanning
transparency, and understandability of the natural-language           yielded satisfiable results in every run. Case 4 – correspond-
plan; UNSAT cases on identification of the affected capa-             ing to the multi-conflict UNSAT scenario above – required
bilities, description of the conflicts, and concreteness of the       two sequential repair iterations, with the second UNSAT-core
repair proposal. KQ, SAT, and UNSAT use a three-level scale           surfacing only after the first repair had been applied. Case 5
(fully, partially, not satisfied). AP uses a binary scale assessing   exercised the runtime-failure path: in response to the report
whether the SPARQL repair was applied and whether replan-             “The conveyor is defective.”, the Capability Mapper Agent
ning succeeded. A case is counted as successful when all its          identified the matching provided capability and the Repair
criteria are fully satisfied across all repetitions.                  Agent removed it from the knowledge graph, after which a
                                                                      feasible plan using alternative resources was generated (RQ3).
B. Results                                                               Overall, the results indicate that the hybrid architecture
                                                                      successfully combines formal planning correctness with acces-
   Table I summarizes the results across scenario categories.         sible natural-language interaction. The HitL approval mecha-
   Knowledge queries were fully satisfied in 9 of 10 cases. One       nism ensured that no unauthorized modification to the capa-
result was only partial correct because it omitted the explicit       bility model was applied in any test case.
parameter range justifications, leaving the answer technically
correct but incomplete; no hallucinations were observed in any                  VI. C ONCLUSIONS AND F UTURE W ORK
of the 10 cases, confirming reliable grounding in the capability
ontology (RQ1).                                                          This paper presented a hybrid LLM-based assistance system
                                                                      for capability-based SMT planning in industrial automation.
    2 https://github.com/hsu-aut/MPS500-Capabilities                  The system augments an existing formal planning approach
[4] with a natural-language interaction and explanation, and                      [6] J. Wei, X. Wang et al., “Chain-of-Thought Prompting Elicits Reasoning
an adaptation layer realized as a routed agentic workflow.                            in Large Language Models,” in Advances in Neural Information Pro-
                                                                                      cessing Systems, S. Koyejo, S. Mohamed et al., Eds., vol. 35. Curran
   The combination of the Router Agent, which classifies user                         Associates, Inc, 2022.
intent, and the Knowledge Retrieval Agent, which grounds the                      [7] H. Wei, Z. Zhang et al., “PlanGenLLMs: A Modern Survey of LLM
user’s request in the structured capability ontology, shows that                      Planning Capabilities,” in Proceedings of the 63rd Annual Meeting of
                                                                                      the Association for Computational Linguistics (Volume 1: Long Papers),
users can query capability knowledge and initiate planning                            W. Che, J. Nabende et al., Eds.         Vienna, Austria: Association for
through natural language (RQ1). Both satisfiable plans and                            Computational Linguistics, 2025, pp. 19 497–19 521.
infeasible results are translated into understandable explana-                    [8] S. Hao, Y. Gu et al., “Reasoning with Language Model is Planning with
                                                                                      World Model,” in Proceedings of the 2023 Conference on Empirical
tions, with chain-of-thought reasoning over the UNSAT core                            Methods in Natural Language Processing, H. Bouamor, J. Pino, and
enabling structured diagnosis of constraint conflicts (RQ2).                          K. Bali, Eds. Stroudsburg, PA, USA: Association for Computational
Planning adaptation under changing or infeasible conditions is                        Linguistics, 2023, pp. 8154–8173.
                                                                                  [9] V. Pallagani, B. C. Muppasani et al., “On the Prospects of Incorporating
achieved as an iterative loop in which the Analyze and Adapta-                        Large Language Models (LLMs) in Automated Planning and Scheduling
tion Agent proposes targeted knowledge graph modifications,                           (APS),” Proceedings of the International Conference on Automated
the user approves them via HitL checkpoints, and planning is                          Planning and Scheduling, vol. 34, pp. 432–444, 2024.
                                                                                 [10] R. E. Fikes and N. J. Nilsson, “Strips: A new approach to the application
re-attempted with the updated model (RQ3).                                            of theorem proving to problem solving,” Artificial Intelligence, vol. 2,
   Overall, the results confirm that a hybrid architecture –                          no. 3-4, pp. 189–208, 1971.
combining the formal correctness of SMT-based planning with                      [11] M. Ghallab, C. Knoblock et al., “PDDL - The Planning Domain
                                                                                      Definition Language,” Golden, S. Penberthy, DE Smith, Y. Sun, D. Weld,
the natural-language capabilities of LLMs – can substantially                         and D. Mcdermott, The planning domain definition language, Yale CVC,
improve the accessibility and adaptability of capability-based                        Tech. Rep, 1998.
planning systems in industrial automation settings.                              [12] M. Cashmore, D. Magazzeni, and P. Zehtabi, “Planning for Hybrid
                                                                                      Systems via Satisfiability Modulo Theories,” Journal of Artificial In-
   Several directions remain for future investigation. First, the                     telligence Research, vol. 67, pp. 235–283, 2020.
current knowledge retrieval relies on handcrafted SPARQL                         [13] A. Rogalla and O. Niggemann, “Automated process planning for cyber-
tools. Replacing these with an MCP server, exposing struc-                            physical production systems,” in 2017 22nd IEEE International Confer-
                                                                                      ence on Emerging Technologies and Factory Automation. Piscataway,
tured graph access, would increase flexibility in querying the                        NJ: IEEE, 2017, pp. 1–8.
capability knowledge graph and decouple the agent layer from                     [14] A. Köcher, A. Belyaev et al., “A reference model for common un-
the specific triple store implementation, even if at the cost of                      derstanding of capabilities and skills in manufacturing,” at - Automa-
                                                                                      tisierungstechnik, vol. 71, no. 2, pp. 94–104, 2023.
potentially higher token usage. Second, runtime failure reports                  [15] Z. Wang, S. Cai et al., “Describe, explain, plan and select: interactive
are currently triggered by user-initiated natural-language ob-                        planning with large language models enables open-world multi-task
servations. Tighter integration with live sensor data streams                         agents,” in Proceedings of the 37th International Conference on Neural
                                                                                      Information Processing Systems, ser. NIPS ’23. Red Hook, NY, USA:
and automated anomaly detection would enable proactive                                Curran Associates Inc, 2023.
identification of capability model inconsistencies, with the                     [16] A. Zhou, K. Yan et al., “Language agent tree search unifies reasoning,
remaining challenge being the reliable translation of detected                        acting, and planning in language models,” in Proceedings of the 41st In-
                                                                                      ternational Conference on Machine Learning, ser. ICML’24. JMLR.org,
anomalies into targeted knowledge graph modifications. Fi-                            2024.
nally, the current evaluation is limited to a single use case. A                 [17] T. Silver, S. Dan et al., “Generalized Planning in PDDL Domains
larger-scale evaluation involving real non-expert users would                         with Pretrained Large Language Models,” Proceedings of the AAAI
                                                                                      Conference on Artificial Intelligence, vol. 38, no. 18, pp. 20 256–20 264,
provide stronger evidence for usability and generalizability.                         2024.
                                                                                 [18] B. Liu, Y. Jiang et al., “LLM+P: Empowering Large Language Models
                         ACKNOWLEDGMENT                                               with Optimal Planning Proficiency,” 2023, arXiv:2304.11477 [cs.AI].
                                                                                      [Online]. Available: https://arxiv.org/abs/2304.11477
   This research is funded by dtec.bw – Digitalization and                       [19] X. Ye, Q. Chen et al., “SatLM: Satisfiability-Aided Language Models
Technology Research Center of the Bundeswehr as part of                               Using Declarative Prompting,” in Advances in Neural Information
                                                                                      Processing Systems, A. Oh, T. Naumann et al., Eds., vol. 36. Curran
the project RIVA. dtec.bw is funded by the European Union                             Associates, Inc, 2023.
– NextGenerationEU                                                               [20] L. Pan, A. Albalak et al., “Logic-LM: Empowering Large Language
                                                                                      Models with Symbolic Solvers for Faithful Logical Reasoning,” in
                              R EFERENCES                                             Findings of the Association for Computational Linguistics: EMNLP
                                                                                      2023, H. Bouamor, J. Pino, and K. Bali, Eds. Stroudsburg, PA, USA:
 [1] H. Kagermann, W. Wahlster, and J. Helbig, “Recommendations for                   Association for Computational Linguistics, 2023, pp. 3806–3824.
     implementing the strategic initiative INDUSTRIE 4.0: Final report of        [21] S. K. Jha, S. Jha et al., “Counterexample Guided Inductive Synthesis
     the Industrie 4.0 Working Group.”                                                Using Large Language Models and Satisfiability Solving,” in MILCOM
 [2] Y. Lu, “Industry 4.0: A survey on technologies, applications and open            2023 - 2023 IEEE Military Communications Conference (MILCOM).
     research issues,” Journal of Industrial Information Integration, vol. 6,         Piscataway, NJ: IEEE, 2023, pp. 944–949.
     pp. 1–10, 2017.                                                             [22] E. Hirsch, G. Uziel, and A. Anaby-Tavor, “What’s the Plan?
 [3] M. Ghallab, D. S. Nau, and P. Traverso, Automated planning: Theory               Evaluating and Developing Planning-Aware Techniques for Language
     and practice, ser. The Morgan Kaufmann Series in Artificial Intelligence.        Models,” 2024, arXiv:2402.11489 [cs.CL]. [Online]. Available: https:
     Amsterdam: Elsevier/Morgan Kaufmann, 2004.                                       //arxiv.org/abs/2402.11489
 [4] A. Köcher, L. M. Vieira da Silva, and A. Fay, “Automated Process           [23] X. Li, S. Wang et al., “A survey on LLM-based multi-agent systems:
     Planning Based on a Semantic Capability Model and SMT,” in AAAI                  workflow, infrastructure, and challenges,” Vicinagearth, vol. 1, no. 1,
     Workshop on AI Planning for Cyber-Physical Systems (CAIPI), 2024.                2024.
 [5] M. Ghallab, D. S. Nau, and P. Traverso, Acting, planning, and learning.     [24] S. Yao, J. Zhao et al., “ReAct: Synergizing Reasoning and Acting in
     Cambridge and New York, NY and Port Melbourne and New Delhi and                  Language Models,” in International Conference on Learning Represen-
     Singapore: Cambridge University Press, 2025.                                     tations, 2023.
