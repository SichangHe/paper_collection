                                         Structural Verification for Reliable EDA Code Generation without
                                                            Tool-in-the-Loop Debugging
                                                     Dinithi Jayasuriya                             Aravind Saravanan                               Nilesh Ahuja
                                                 University of Illinois Chicago                 University of Illinois Chicago                     Intel Corporation
                                                    Chicago, Illinois, USA                         Chicago, Illinois, USA                                 USA
                                                      dkasth2@uic.edu                                asara27@uic.edu                            nilesh.ahuja@intel.com

                                                                                Amanda Rios                                  Amit Trivedi
                                                                              Intel Corporation                      University of Illinois Chicago
                                                                                     USA                                Chicago, Illinois, USA
arXiv:2604.18834v1 [cs.SE] 20 Apr 2026




                                                                            amanda.rios@intel.com                          amitrt@uic.edu
                                         Abstract                                                                 correctness in EDA scripting depends on satisfying implicit depen-
                                         Large language models (LLMs) have enabled natural-language-              dencies over design objects and operations. Queries and transfor-
                                         driven automation of electronic design automation (EDA) work-            mations must follow valid object acquisition paths, respect type
                                         flows, but reliable execution of generated scripts remains a funda-      constraints, and satisfy action-specific preconditions defined by
                                         mental challenge. In LLM-based EDA tasks, failures arise not from        the design hierarchy. As a result, many generated programs fail
                                         syntax errors but from violations of implicit structural dependen-       not due to syntax errors, but due to structurally invalid execution
                                         cies over design objects, including invalid acquisition paths, missing   paths, such as missing intermediate objects, invalid parent-child
                                         prerequisites, and incompatible API usage. Existing approaches ad-       transitions, or incompatible API usage.
                                         dress these failures through tool-in-the-loop debugging, repeatedly          Existing LLM-based approaches address this problem primarily
                                         executing and repairing programs using runtime feedback. While           through tool-in-the-loop debugging, where candidate programs are
                                         effective, this paradigm couples correctness to repeated tool invo-      generated, executed within the EDA tool, and iteratively repaired
                                         cation, leading to high latency and poor scalability in multi-step       using runtime feedback. While effective, this paradigm treats the
                                         settings. We propose to eliminate tool-in-the-loop debugging by          tool as a debugging oracle, leading to repeated execution, high
                                         enforcing structural correctness prior to execution. Each task is        latency, and poor scalability as task complexity increases. More
                                         represented as a structural dependency graph that serves as an           importantly, it does not explicitly model the structural constraints
                                         explicit execution contract, and a verifier-guided synthesis frame-      that govern valid execution, relying instead on post-hoc feedback
                                         work enforces this contract through graph-conditioned retrieval,         to detect failures. In multi-step query-action settings, where errors
                                         constrained generation, and staged pre-execution verification with       propagate across dependent operations, this results in inefficient
                                         diagnosis-driven repair. On single-step tasks, our method improves       trial-and-error loops and limited ability to localize root causes.
                                         pass rate from 73.0% (LLM+RAG) and 76.0% (tool-in-loop) to 82.5%,            In this work, we argue that failures in EDA code generation
                                         while requiring exactly one tool call per task and reducing total tool   are fundamentally structural rather than syntactic, and should be
                                         calls by more than 2×. On multi-step tasks, pass rate improves from      addressed prior to execution. Correct execution can be viewed as
                                         30.0% to 70.0%, and further to 84.0% with trajectory-level reflection.   satisfying an implicit dependency graph over design objects and
                                         Uncertainty-aware filtering further reduces verifier false positives     operations, which encodes valid acquisition paths, multi-branch
                                         from 20.0% to 6.7% and improves precision from 80.0% to 93.3%.           dependencies, and action-specific constraints.
                                         These results show that enforcing structural consistency prior to            Based on this insight, we propose to eliminate tool-in-the-loop
                                         execution decouples correctness from tool interaction, improving         debugging by enforcing structural consistency before invoking
                                         both reliability and efficiency in long-horizon EDA code generation.     the external tool. We introduce a framework that extracts a task-
                                                                                                                  level structural dependency graph from the natural-language spec-
                                                                                                                  ification and uses it as an explicit execution contract. This graph
                                         1   Introduction                                                         guides retrieval, constrains code generation, and enables staged pre-
                                                                                                                  execution verification. A multi-layer verifier detects violations such
                                         Recent advances in large language models (LLMs) have enabled the
                                                                                                                  as missing dependencies, invalid object transitions, and API mis-
                                         translation of natural-language intent into executable programs
                                                                                                                  matches, while a controller performs diagnosis-driven, localized re-
                                         [Jiang et al.(2026)], opening the possibility of automating complex
                                                                                                                  pair. By shifting error detection and correction to the pre-execution
                                         electronic design automation (EDA) workflows. In EDA, however,
                                                                                                                  stage, the framework requires only a single tool invocation per task
                                         tasks require interacting with hierarchical design databases, com-
                                                                                                                  and avoids repeated EDA tool calls.
                                         posing tool-specific APIs, and maintaining consistency across tightly
                                                                                                                      We evaluate the framework in OpenROAD on both single-step
                                         coupled flow stages. While natural-language-driven automation
                                                                                                                  and multi-step query-action tasks over design databases. Compared
                                         promises to reduce manual scripting effort, reliable execution of
                                                                                                                  to LLM+RAG baselines, the proposed method improves pass rate
                                         AI-generated EDA scripts remains a fundamental challenge.
                                                                                                                  from 73.0% to 82.5% on single-step tasks and from 30.0% to 70.0%
                                            The core difficulty arises from the structured and stateful nature
                                                                                                                  on multi-step tasks. Compared to tool-in-the-loop approaches, it
                                         of EDA environments. Unlike general-purpose code generation,
ICCAD ’26, November 8–12, 2026, San Jose, CA, USA                       Dinithi Jayasuriya, Aravind Saravanan, Nilesh Ahuja, Amanda Rios, and Amit Trivedi


achieves higher accuracy while reducing expensive OpenROAD
calls by more than 2×, demonstrating that pre-execution structural
verification improves both execution success and efficiency as task
complexity increases.
   Overall, the paper makes the following contributions:
• We identify structural dependency violations as a critical source
  of failure in EDA code generation and formalize execution cor-
  rectness as consistency with a task-level dependency graph.
• We propose a pre-execution verification framework that elimi-
  nates reliance on tool-in-the-loop debugging by enforcing struc-
  tural constraints before execution.
• We design a verifier with diagnosis-driven repair that localizes
  and corrects structural errors without repeated tool interaction.
• We demonstrate consistent improvements in correctness and effi-
  ciency across OpenROAD tasks, including multi-step workflows,
  multiple designs, and different PDKs.

2    Related Work
Agentic Code Generation. Recent advances in LLMs have im-
proved code generation, enabling performance on multi-step rea-
soning, tool use, and long-horizon tasks. Frameworks such as ReAct
[Yao et al.(2022)] and Reflexion [Shinn et al.(2023)] interleave rea-
soning and execution for iterative correction through execution
traces or self-reflection. Related approaches, including Toolformer
[Schick et al.(2023)], CodeAct [Wang et al.(2024)], program-aided        Figure 1: Verifier-guided structure-aware synthesis frame-
reasoning [Gao et al.(2023)], and self-debugging [Chen et al.(2023)],    work with staged verification and localized repair.
show that structured feedback and tool integration improve cor-
rectness. More recent systems extend this paradigm with mem-
ory and planning for more complex multi-step behavior. Despite
these advances, most approaches still generate candidate programs
[Park et al.(2023)], evaluate them via external signals, and itera-
tively refine them. While effective when execution is cheap, this
                                                                         Structure-Aware Verification. Program correctness in structured
paradigm relies on post-hoc feedback rather than explicit structural
                                                                         environments depends on dependency constraints between opera-
modeling. In structured environments such as EDA, where correct-
                                                                         tions, not on syntax alone. Prior work in program synthesis uses
ness depends on multi-step dependencies, this leads to inefficient
                                                                         structured representations [Osera and Zdancewic(2015)], such as
correction.
                                                                         abstract syntax trees, type systems, and syntax-guided synthesis, to
LLM-based EDA Scripting and OpenROAD. Recent work has                    constrain generation and reduce invalid outputs. Complementary
explored LLMs for EDA automation, including script generation,           approaches use generate-then-verify methods [Löding et al.(2016)],
design querying, and tool interaction. ChipNeMo [Liu et al.(2023)]       including type checking, constraint solving [Wang et al.(2018)],
and RTLCoder [Liu et al.(2024)] show that domain adaptation im-          execution-guided filtering, and [Ni et al.(2023)] verifier-based selec-
proves hardware design performance, especially for RTL generation        tion . However, these methods generally focus on validating generic
and documentation grounding. EDA Corpus [Wu et al.(2024)] pro-           properties of generated programs, or depend on post-hoc execution
vides a public OpenROAD-oriented dataset for reproducible evalu-         feedback to detect errors, rather than enforcing the domain-specific
ation. Subsequent work focuses on OpenROAD , an open-source              dependency constraints that govern correct execution before the
physical design system built on OpenDB with stateful stages such as      program is run. They do not capture task-level requirements such
placement, routing, and timing analysis [Ajayi and Blaauw(2019)].        as valid object acquisition paths, multi-branch dependencies, and
Scripting requires navigating hierarchical design objects and com-       action-specific preconditions in EDA workflows. Feedback-driven
posing tool-specific APIs across design states. OpenROAD-Assistant       methods such as Reflexion [Shinn et al.(2023)] and self-debugging
[Sharma et al.(2024)] and ORAssistant [Kaintura et al.(2024)] im-        improve correction, but still depend on global regeneration and re-
prove API grounding through retrieval-augmented generation but           peated execution rather than explicitly isolating structural failures.
remain prompt-to-code assistants. OpenROAD-Agent adds execution-            In contrast, our approach models EDA tasks as structural depen-
driven self-correction using runtime feedback, but relies on re-         dency graphs and enforces structural consistency before execution.
peated tool invocation [Wu et al.(2025)]. In multi-step query-action     Combined with graph-guided generation, staged verification, and
tasks, this causes repeated execution and overhead as errors propa-      localized repair, it avoids tool-in-the-loop debugging and improves
gate across dependent operations.                                        efficiency and robustness.
Structural Verification for Reliable EDA Code Generation without Tool-in-the-Loop Debugging                        ICCAD ’26, November 8–12, 2026, San Jose, CA, USA


3 Verifier-Guided Structure-Aware Synthesis
3.1 Methodology Overview
We address the problem of translating natural-language query-
action prompts into executable OpenROAD programs over the
OpenDB design database. Given a prompt 𝑃, the goal is to gener-
ate a program 𝜋 that executes correctly in a structured, stateful
physical design environment. Correctness is governed not only
by syntax, but by structural consistency with the design hierarchy,
including valid object acquisition paths, type compatibility, and
action-specific preconditions. We therefore reformulate EDA code
generation as enforcing structural consistency prior to execution.
   In our framework, each task is modeled as a structural dependency
graph 𝐺 = (𝑉 , 𝐸), where nodes represent typed design objects, inter-
mediate conditions, and actions, and edges encode acquisition and
dependency relations [Jayasuriya et al.(2025)]. This graph captures
required object traversal paths and their composition, and serves
as an explicit execution contract. A program is valid if it realizes the
acquisition paths and satisfies the dependency constraints specified
by 𝐺. Based on this formulation, we design a verifier-guided syn-
thesis framework that enforces this contract before tool invocation.
The framework operates in four stages: (1) graph construction from
the prompt, (2) graph-conditioned retrieval and code generation,
(3) staged pre-execution verification with diagnosis-driven repair,
and (4) extension to multi-step execution with trajectory-level re-
flection. Unlike execution-driven approaches, all correction occurs
prior to tool invocation, requiring a single OpenROAD execution
per task. This eliminates reliance on tool-in-the-loop debugging, de-
couples repair from execution cost, and enables localized correction
of structural errors rather than repeated trial-and-error interaction.


3.2     Structural Dependency Graph Construction                                        Figure 2: Structural representation of EDA query-action tasks
Direct prompt-to-code generation is insufficient because task struc-                    as dependency graphs. Top: both simple traversal queries
ture is implicit in natural-language specifications. Even simple                        and action queries can be expressed as object-acquisition
prompts require multiple dependent operations, including object                         paths over the design hierarchy, with actions requiring the
acquisition, hierarchical traversal, condition evaluation, and action                   composition of multiple dependencies. Bottom: multi-step
execution, which are not explicitly enumerated. As a result, cor-                       tasks decompose into a sequence of such graphs, where each
rect execution depends on recovering the underlying dependency                          step operates on the updated design state. This formulation
structure rather than generating code directly.                                         exposes the structural constraints underlying execution and
   To make this structure explicit, we construct a structural de-                       motivates enforcing consistency prior to tool invocation.
pendency graph 𝐺 = (𝑉 , 𝐸). Nodes represent typed design objects,
intermediate targets, conditions, and actions, while edges encode
                                                                                           Each node and edge must satisfy type and relation constraints
acquisition and dependency relations over the design hierarchy.
                                                                                        defined by the schema. Nodes are classified as valid, missing-but-
This representation captures both required objects and their com-
                                                                                        real, or hallucinated, and edges are checked for valid parent-child
position into valid execution paths.
                                                                                        transitions. Violations are converted into structured feedback and
   The graph supports both linear and multi-branch dependencies.
                                                                                        used to iteratively refine the graph until all constraints are satisfied.
Linear chains correspond to hierarchical traversal (e.g., Design →
                                                                                        This step acts as a structural grounding gate, ensuring that only API-
Block → Net), while multi-branch structures capture independent
                                                                                        consistent graphs are passed to synthesis. By enforcing validity at
object acquisition followed by convergence at an action node (e.g.,
                                                                                        the level of object dependencies rather than execution, the resulting
connect(Port, Net)), avoiding spurious sequential dependencies.
                                                                                        graph serves as a reliable execution contract for downstream stages.
   We construct 𝐺 via a hypothesis-and-validation process. An
initial graph is proposed through structured LLM extraction, pro-
ducing typed acquisition paths and an action node, which are de-                        3.3    Structure-Grounded Synthesis
terministically parsed into graph form. The extracted graph is then                     Given a validated structural dependency graph 𝐺, we perform
validated against a structured OpenROAD API schema defining                             structure-grounded synthesis, where both retrieval and generation
valid object types and permissible relations.                                           are conditioned on the explicit dependency structure rather than
ICCAD ’26, November 8–12, 2026, San Jose, CA, USA                            Dinithi Jayasuriya, Aravind Saravanan, Nilesh Ahuja, Amanda Rios, and Amit Trivedi


the raw prompt. This shifts synthesis from unconstrained sequence             Execution Efficiency. All correction occurs prior to tool invoca-
generation to structured composition aligned with execution.                  tion, requiring exactly one OpenROAD call per task. This decouples
Graph-Conditioned Retrieval. Retrieval is decomposed into lo-                 repair from execution cost and avoids repeated tool interaction.
calized queries aligned with edges and substructures in 𝐺. Each               Increasing the repair budget therefore improves solution quality
query corresponds to an object transition or action dependency,               without increasing tool usage, unlike execution-driven approaches
retrieving API usage patterns and code fragments relevant to that             where each iteration incurs an additional call.
relation. This yields evidence tied to individual dependencies, im-
proving grounding while covering implicit prerequisite operations.            3.5     Post-Verification Uncertainty Estimation
Aligning retrieval with the graph reduces irrelevant context and              The verifier enforces structural correctness but produces a binary
helps recover missing intermediate steps.                                     decision. In practice, some verifier-Pass programs still fail in Open-
Constrained Code Generation. Code generation is conditioned                   ROAD due to unsupported API usage or unstable repair trajec-
on the prompt, the dependency graph 𝐺, and the retrieved evidence.            tories. This highlights a limitation of purely structural verifica-
The graph enforces structural constraints, restricting generation to          tion: passing the verifier is necessary but not always sufficient for
valid object-acquisition paths and dependency compositions, while             reliable execution [Kumar et al.(2025)]. We therefore introduce a
retrieved evidence grounds API usage at each step. This reduces               post-verification uncertainty estimate that scores the reliability
the search space by eliminating structurally invalid programs, such           of verifier-Pass programs prior to execution [Tayebati et al.(2026)].
as those with missing prerequisites, incorrect traversal order, or            We decompose uncertainty into three sources: code-level uncertainty,
incompatible object types. In contrast to prompt-only generation,             capturing suspicious API usage in the final program; trajectory-
where structure must be inferred, the graph provides an explicit              level uncertainty, capturing instability in the repair process; and
plan that guides composition.                                                 verification-coverage uncertainty, capturing how much of the pro-
   The resulting program aligns with the structural execution con-            gram is actually validated. Let x denote the final program and T
tract defined by 𝐺, but may still contain residual inconsistencies            its repair trajectory: 𝑢 (x, T ) = 𝛼 1𝑢 code (x) + 𝛼 2𝑢 traj (x) + 𝛼 3𝑢 cov (T ),
in implementation or API usage. It is subsequently passed to the              where 𝛼 1 + 𝛼 2 + 𝛼 3 = 1.
verifier-guided control stage for validation and targeted repair.             3.5.1 Code-Level Uncertainty. Code-level uncertainty targets resid-
                                                                              ual failures where structurally valid programs reference unsup-
3.4     Verifier-Guided Control                                               ported API constructs. Let A𝑚 and A𝑡 denote valid method and
                                                                              type sets. We define three hallucination signals:
This stage closes the synthesis loop by coupling generation with
structured feedback and targeted repair, ensuring that the program
                                                                                                                     |{𝑚 ∈ 𝑀 (x) : 𝑚 ∉ A𝑚 }|
satisfies the structural execution contract defined by 𝐺.                       ℎ𝑚 (x) (method hallucination) =                              ,
                                                                                                                               |𝑀 (x)|
Four-Layer Verification. Each candidate is evaluated through a                   ℎ𝐼 (x) (invalid imports) = |{𝑖 ∈ 𝐼 (x) : 𝑖 ∉ A𝑚 ∪ A𝑡 }| ,
four-layer pipeline targeting progressively deeper error classes. We
denote the failure layer as ℓ ∈ {0, 1, 2, 3, 4}, where ℓ = 0 indicates all      ℎ𝐸 (x) (enum hallucination) = |{𝑒 ∈ 𝐸 (x) : 𝑒 ∉ Eknown }| .
layers are passed. Layer 1 (Syntax) ensures well-formed Python via                                                                                          (1)
AST parsing. Layers 2 and 3 perform causal verification against                  These are combined into a confidence score
𝐺. Layer 2 (Causal Flow) verifies correct acquisition order, valid                  𝑐 code (x) = clip[1 − 𝜆𝐼 ℎ𝐼 (x) − 𝜆𝐸 ℎ𝐸 (x) − 𝜆𝑟 ℎ𝑚 (x), 0, 1] ,        (2)
attribute access, and proper handling of nullable returns. Layer 3            and uncertainty is defined as 𝑢 code (x) = 1 − 𝑐 code (x).
(API Alignment) checks that invoked methods match retrieved APIs,
detecting hallucinated calls and incorrect object usage. Layer 4              3.5.2 Trajectory-Level Uncertainty. Trajectory-level uncertainty
(Semantic) evaluates task-level consistency using an LLM judge,               captures instability in the repair process. Let ℓ0, . . . , ℓ𝑇 denote veri-
including completeness, control flow, and output validity, and is             fier outcomes (ℓ𝑡 ∈ {0, . . . , 4}) and x0, . . . , x𝑇 the candidates.
applied only after L1–L3 pass.
                                                                                                                                            
Diagnosis-Driven Repair. The verifier produces a structured diag-                                                                  ℓ0 − ℓ𝑇
                                                                                    𝜏conv (convergence) = max 0, 1 −                           ,
nostic report specifying failure stage, issues, and localized inconsis-                                                           max(ℓ0, 1)
tencies (e.g., missing acquisition steps, invalid transitions, receiver                                            𝑇 −1
                                                                                                                1 ∑︁
mismatches, incorrect APIs). Each failure is mapped to a region of                   𝜏stag (stagnation) =              𝐽 (x𝑡 , x𝑡 +1 ),                     (3)
                                                                                                                𝑇 𝑡 =0
𝐺, enabling localized correction rather than global regeneration. A
controller selects actions based on the task, graph, retrieved APIs,                                                            |{𝑡 ∈ 𝑅 : ℓ𝑡 ≥ ℓ𝑡 −1 }|
                                                                                      𝜏eff (repair ineffectiveness) =                                   .
prior actions, feedback, and remaining budget: Regeneration (re-                                                                         |𝑅|
generate code with targeted repair hints for L1, L2, or persistent L3            We combine these as
failures), Edge re-retrieval (update retrieval for a specific graph
                                                                                               𝑢 traj (T ) = 𝑤𝑐 𝜏conv + 𝑤𝑠 𝜏stag + 𝑤𝑒 𝜏eff .                (4)
edge and regenerate for L3 failures), Graph re-extraction (revise 𝐺
and restart synthesis for repeated L2 failures), and Accept (commit           3.5.3 Verification-Coverage Uncertainty. Verification-coverage un-
when minor issues remain but the program is semantically valid).              certainty captures cases where a verifier Pass reflects incomplete
A deterministic safeguard prevents repeated ineffective actions by            checking rather than confirmed correctness. Let K (𝜏) denote the
detecting loops and escalating to alternative strategies.                     set of known methods for receiver type 𝜏, and let 𝐶 (x) be the set
Structural Verification for Reliable EDA Code Generation without Tool-in-the-Loop Debugging                       ICCAD ’26, November 8–12, 2026, San Jose, CA, USA


Table 1: Single-step query-action performance and efficiency.                           4 Results
Higher pass rate, lower latency and fewer tool calls are better.
                                                                                        4.1 Benchmark and Evaluation Protocol
Method                            Pass Rate (%) Latency (s) Calls / Task Total Calls We evaluate the proposed framework on generating executable
Static verifier only                  50.8          19.0         1.00         120       OpenROAD programs from natural-language query-action prompts
Causal verifier only                  79.2          27.5         1.00         120       over the OpenDB design database. The evaluation focuses on (i)
                                                                                        execution correctness and (ii) efficiency in terms of OpenROAD
Full pipeline                         82.5          34.8         1.00         120
                                                                                        tool usage. We consider two task settings. First, single-step query-
Tool-in-loop (GPT-4.1-mini)           76.0          53.0         1.77         248       action prompts, where each prompt specifies a compact OpenROAD
OpenROAD Agent (Qwen 7B)              16.4          70.0         3.54         496       operation. These provide a controlled setting for evaluating gener-
                                                                                        ation quality and verifier effectiveness, although correct execution
                                                                                        typically requires multiple dependent API calls over the design hier-
of method calls in program x, with receiver types inferred via light-
                                                                                        archy. Second, multi-step query-action prompts, where each prompt
weight propagation. We define two coverage signals:
                                                                                        consists of a sequence of dependent subtasks executed within a
                                               |𝐶 cov (x)|                              single OpenROAD session. This setting is more challenging, as
           𝑐 cov (x) (verified-call coverage) =             ,                           correctness depends on both step-level validity and consistency
                                                 |𝐶 (x)|
                                                                             (5)        of the evolving design state. Since no standard benchmark exists,
                                              |𝐶 unc (x)|
           𝑢 unc (x) (unchecked-call ratio) =             ,                             we construct a dataset of 100 complex prompts via adversarial
                                                |𝐶 (x)|
                                                                                        self-play [Lin et al.(2025)], covering diverse object hierarchies, API
where                                                                                   interactions, and multi-stage operations [Cheng et al.(2024)].
                                                                                           A task is considered successful if the generated code executes
  𝐶 cov (x) = {(𝜏, 𝑚) ∈ 𝐶 (x) : 𝜏 is well-covered and 𝑚 ∈ K (𝜏)},
                                                                             (6)        in the OpenROAD Python shell without raising an exception or
 𝐶 unc (x) = 𝐶 (x) \ 𝐶 cov (x).                                                         traceback. Execution is performed in a live OpenROAD process
                                                                                        via a pseudo-terminal. A task is marked as failed if a traceback
   Since these quantities are complementary, we define
                                                                                        occurs, if the code contains a syntax error, if execution exceeds 120
                                                 |𝐶 unc (x)|                            seconds, or if the process crashes. While execution success does
                   𝑢 cov (x) = 1 − 𝑐 cov (x) =               .               (7)        not guarantee semantic optimality, it is a necessary condition for
                                                   |𝐶 (x)|
                                                                                        usable EDA scripts. In OpenROAD, incorrect API usage typically
𝑢 code , 𝑢 traj , and 𝑢 cov capture complementary risks where unsup-                    manifests as runtime exceptions, making execution success a strong
ported API behavior, unverifiable API usage, and weak convergence,                      proxy for correctness. Structural pre-execution verification and
providing a more informative estimate than the verifier’s binary                        post-verification uncertainty filtering mitigate residual risks.
verdict and enabling uncertainty-aware filtering prior to execution.                       For multi-step tasks, subtasks are executed sequentially within
                                                                                        a single session, preserving verified state across steps. A task is
3.6     Extension to Multi-Step Tasks                                                   successful only if all subtasks execute successfully; any failure
We extend the framework to multi-step query-action prompts by                           terminates execution to prevent error propagation. In addition to
decomposing each input into an ordered sequence of subtasks.                            correctness, we measure efficiency via OpenROAD tool calls and
Each subtask follows the same pipeline, subtask → graph →                               end-to-end latency, enabling direct comparison with execution-
validation → retrieval → generation → verification, and is exe-                         driven approaches where each repair iteration incurs an additional
cuted only after successful verification. Accepted programs update                      tool call. We also evaluate generalization across designs, PDKs, and
the design state, which is propagated to subsequent steps.                              OpenROAD stages, e.g. floorplanning and placement.
   A key challenge is cascading failure, where errors in early steps
corrupt the design state and cause downstream failures, even when                       4.2    Key Results on Single-Step Tasks
later steps are locally correct. Thus, correctness must be enforced                     We evaluate the proposed framework on single-step query-action
both locally and across the full execution sequence. If a subtask                       prompts, a controlled setting for assessing execution correctness. Al-
fails after exhausting the repair budget, execution is terminated to                    though each prompt specifies a single operation, correct execution
prevent propagation of corrupted state.                                                 typically requires multiple dependent API calls over the OpenDB
   To address this, we introduce an episode-level reflection mecha-                     hierarchy. Table 1 summarizes the results. The full pipeline achieves
nism for cross-step failure diagnosis. After an initial pass, the frame-                a pass rate of 82.5%, outperforming LLM+RAG (73.0%) and tool-in-
work analyzes the full sequence of subtask outcomes to identify                         the-loop correction (76.0%), showing that enforcing structural cor-
root causes of failure. Reflection captures cross-step dependencies                     rectness prior to execution improves reliability [Lewis et al.(2020)].
and error propagation not observable within individual subtasks,                           To isolate component contributions, we evaluate ablated variants.
including inconsistencies between earlier object acquisition and                        The static verifier achieves 50.8% pass rate, while the causal verifier
later usage. The resulting diagnostic signal guides a second-pass                       improves performance to 79.2%, indicating that enforcing object-
synthesis with targeted corrections, enabling recovery from failures                    acquisition structure provides the dominant gain. The full pipeline
that cannot be resolved through local verification alone. This pass                     further increases performance to 82.5%, showing that semantic
corrects upstream structural errors rather than repeatedly repairing                    validation and repair provide smaller, incremental improvements.
downstream symptoms [Madaan et al.(2023)].                                              Compared to prior systems, the gains are substantial: OpenROAD
ICCAD ’26, November 8–12, 2026, San Jose, CA, USA                          Dinithi Jayasuriya, Aravind Saravanan, Nilesh Ahuja, Amanda Rios, and Amit Trivedi


        Table 2: OpenROAD script generation performance across systems. We report pass rate, tool usage, and latency.

                 Model            Method                      Generator       Verifier     RAG     Pass (%)     Calls / Task    Latency (s)
                 Qwen2.5-7B       OpenROAD-Agent              Qwen2.5-ft        —            ✓       16.4              3.54        69.5
                 Qwen2.5-7B       OpenROAD-Agent + verifier   Qwen2.5-ft   GPT-4.1-mini      ✓       31.8              1.00        33.4
                 GPT-4.1-mini     LLM only                    GPT-4.1-mini      —            ×       48.0               —           —
                 GPT-4.1-mini     LLM + RAG                   GPT-4.1-mini      —            ✓       73.0               —           —
                 GPT-4.1-mini     LLM + tool-in-loop          GPT-4.1-mini      —            ✓       76.0              1.77        37.6
                 GPT-4.1-mini     Ours (full)                 GPT-4.1-mini GPT-4.1-mini      ✓       82.5              1.00        34.8
                 GPT-4o           LLM only                    GPT-4o            —            ×       52.0               —           —
                 GPT-4o           Ours (full)                 GPT-4o          GPT-4o         ✓       83.0              1.00        36.2




                                                                            Figure 4: Effect of repair budget and tool interaction on exe-
                                                                            cution performance. (a) Cumulative pass rate improves with
                                                                            repair budget, reflecting gains from iterative refinement. (b)
Figure 3: Pass rate and tool usage comparison across single-                Pass rate versus average tool calls per task: the proposed
step and multi-step tasks. The proposed framework main-                     framework achieves higher accuracy (82.5%) with a single
tains higher accuracy while requiring a constant single tool                tool call, while tool-in-the-loop methods require multiple
call per task, whereas tool-in-the-loop methods incur signifi-              executions for smaller gains. (c) Failure mode breakdown
cantly higher tool usage and degrade in multi-step settings.                highlighting reductions in generation and execution errors.

                                                                                    Table 3: Multi-step query–action performance.
Agent achieves 16.4% pass rate, and only 31.8% even with a verifier,
highlighting the importance of integrating structural verification
                                                                                    Method                  Verifier    RAG    Pass (%)   Latency (s)
during generation rather than applying it post hoc. Table 2 shows
consistent trends across models. For GPT-4.1-mini, retrieval im-                    LLM + RAG                 —           ✓     30.0           12.2
proves pass rate from 48.0% to 73.0%, and tool-in-the-loop correc-                  Ours                      ✓           ✓     70.0           53.9
tion to 76.0%, while our method reaches 82.5%. Similar gains hold                   Ours + Reflection         ✓           ✓     84.0          ~94.9
for GPT-4o (52% to 83%), demonstrating robustness across models.
These results indicate that retrieval alone is insufficient, as it does     higher tool usage (up to 6.8 calls per task). This shows that execu-
not enforce structural consistency required for correct execution.          tion cost scales with task complexity for tool-in-the-loop methods
                                                                            but remains fixed under pre-execution verification. Fig. 4 further
4.3     Efficiency and Tool Call Reduction                                  shows that increasing the repair budget improves pass rate without
Table 1 shows that the proposed framework requires exactly one              increasing tool usage. In contrast, tool-in-the-loop methods incur
OpenROAD call per task, compared to 1.77 for tool-in-the-loop               additional tool calls with each repair iteration.
correction and 3.54 for OpenROAD Agent. Across the evaluation
set, this corresponds to 120 total calls versus 248 and 496, yielding       4.4     Multi-Step Execution Performance
more than a 2× reduction in tool usage. Latency follows a sim-              We evaluate the proposed framework on multi-step query-action
ilar trend. By performing all correction prior to invocation, the           prompts, where each task consists of dependent subtasks executed
framework executes each task only once. Although the full pipeline          within a single OpenROAD session. This setting is substantially
introduces modest overhead from verification and repair (34.8s vs           more challenging than single-step tasks, as correctness depends on
27.5s for causal-only), it remains significantly faster than tool-in-       both step-level validity and consistency of the evolving design state.
the-loop correction (53.0s) and OpenROAD Agent (70s).                       Since no standard benchmark exists for this regime, we construct
   Fig. 3 compares pass rate and tool usage across single-step and          a multi-step dataset through round-based adversarial evolution,
multi-step settings. The proposed method maintains higher accu-             where a creator model increases prompt complexity and a solver
racy with a constant single tool call per task, while tool-in-the-loop      model improves solvability across rounds. Figure 6 summarizes this
approaches degrade in multi-step settings and incur substantially           process. Compared to base EDA-Corpus tasks, the evolved prompts
Structural Verification for Reliable EDA Code Generation without Tool-in-the-Loop Debugging                        ICCAD ’26, November 8–12, 2026, San Jose, CA, USA




Figure 5: Causal-graph extraction accuracy. (a) Edge-level F1 and precision as a function of chain length. (b) Node-level F1 and
precision as a function of chain length. (c) Ground-truth chain length across prompt complexity buckets.




Figure 6: Round-based adversarial evolution for multi-step benchmark construction. (a) Compared to base EDA-Corpus
tasks, evolved prompts exhibit greater structural complexity, including multi-step composition, aggregation, and cross-object
interactions. (b) Failure types observed across evolution rounds, including API mismatches, missing prerequisites, type
inconsistencies, and semantic errors. (c) Newly discovered and cumulative failure modes across rounds, showing that later
rounds introduce more diverse and challenging tasks rather than repeating a fixed error distribution.


exhibit greater structural complexity and expose a broader range of                           Table 4: Causal-chain accuracy by prompt complexity
failure types, including API mismatches, missing prerequisites, type                          Complexity Level                                       Exact
                                                                                                                   Node F1 (%)     Edge F1 (%)
inconsistencies, and semantic failures. Fig. 6(c) further shows that                            (<word count)                                       Match (%)
new failure modes continue to emerge across rounds, indicating                                Simple (<8 )              100             100           100
increasing task diversity rather than overfitting to a fixed error                            Moderate (<15)             99              93            96
                                                                                              Complex (<25)              96              88            76
distribution.
                                                                                              Very Complex (26+)         87              69            31
   Table 3 summarizes multi-step execution results on this bench-
mark. LLM+RAG achieves a pass rate of 30.0%, reflecting failures
due to missing dependencies and inconsistent state propagation. En-                     4.5      Ablation Studies on Structural Components
forcing structural correctness at each step improves performance to
                                                                                        We analyze the contribution of structural graph extraction and
70.0%, indicating that most local errors can be resolved through per-
                                                                                        staged verification to explain the observed performance gains.
step verification even as task complexity increases.Incorporating
trajectory-level reflection further improves pass rate from 70.0%                       4.5.1 Structural Graph Extraction Accuracy. We evaluate the qual-
to 84.0%. This shows that many of the remaining failures arise                          ity of extracted structural dependency graphs by comparing them
not from local step errors, but from inconsistencies that propagate                     against ground-truth acquisition graphs recovered from passing
across steps. By reasoning over the full trajectory, reflection helps                   programs via static AST analysis. Node and edge correspondences
identify and correct these upstream errors.                                             are resolved using an OpenDB API return-type table.
                                                                                           As shown in Fig. 5, the extracted graphs achieve strong node-
                                                                                        level accuracy (F1 = 0.869), reliably recovering required object types.
                                                                                        Recall (0.911) exceeds precision (0.861), indicating a tendency to add
ICCAD ’26, November 8–12, 2026, San Jose, CA, USA                                   Dinithi Jayasuriya, Aravind Saravanan, Nilesh Ahuja, Amanda Rios, and Amit Trivedi


       Table 5: Verifier quality on single-task prompts.
           Verifier Stage             Precision     Recall    F1
           Static Verifier               0.508      1.000    0.674
           Causal Verifier               0.807      0.968    0.880
           LLM Semantic Verifier         0.849      1.000    0.918
           Full Staged Verifier          0.849      0.909    0.878



Table 6: Effect of uncertainty-aware filtering on pass rate and
verifier precision.


 Metric                           Baseline       + Uncertainty         Δ
                                                                                     Figure 7: Stage-wise performance across OpenROAD flow
 Step 1 pass rate                   80.0%            92.0%           +12.0%          stages, showing consistent pass rates across diverse opera-
 Step 2 pass rate                   78.0%            90.0%           +12.0%          tions and API patterns.
 Overall pass rate                  72.0%            84.0%           +12.0%
 Verifier false positive rate       20.0%             6.7%           −13.3%
 Verifier precision                 80.0%            93.3%           +13.3%
                                                                                     4.6     Uncertainty and Reliability Analysis
                                                                                     While staged verification substantially improves execution cor-
Table 7: Cross-design and cross-PDK (Process Design Kit)
                                                                                     rectness (Section 4.2), residual failures arise when verification is
generalization of the proposed framework. Inst: standard-
                                                                                     incomplete or repair does not converge. We therefore introduce
cell instances; Nets: signal nets; IO: input/output pins; Lat
                                                                                     uncertainty measures to estimate reliability prior to execution and
(s): average task latency; LLM: average large language model
                                                                                     enable selective filtering of low-confidence programs. Table 6 sum-
calls per task; Cost: estimated cost per task using GPT-4.1-
                                                                                     marizes the impact of uncertainty-aware filtering. Without filtering,
mini pricing ($0.40/M input tokens, $1.60/M output tokens).
                                                                                     the verifier exhibits a false positive rate of 20.0% and precision of
                                                                                     80.0%, indicating that a non-trivial fraction of programs marked as
Design PDK            Node        Inst   Nets IO Pass Lat (s) LLM Cost ($)           valid still fail at execution. Incorporating uncertainty reduces the
GCD Nangate45 45nm        624    581 54 81.5%                28.0 3.0      0.0028    false positive rate to 6.7% and improves precision to 93.3%, showing
GCD sky130hd 130nm 1,143         306 54 88.9%                20.0 2.2      0.0021    that uncertainty signals effectively identify unreliable candidates.
GCD sky130hs 130nm        366    402 54 94.4%                24.1 2.4      0.0019       As explained in the section 3.5 we consider three complementary
AES    Nangate45 45nm 156,172 17,388 388 88.9%               51.5 2.1      0.0020    sources of uncertainty [Wang et al.(2022)]. These signals provide
RISC-V ASAP7      7nm 12,161 9,585 135 90.7%                 22.5 1.26     0.0017    complementary views of failure: code-level uncertainty targets local
AES    ASAP7      7nm 22,107 21,542 388 94.4%                21.6 1.04     0.0013    inconsistencies, trajectory-level uncertainty reflects weak conver-
                                                                                     gence, and coverage uncertainty captures blind spots in verification
                                                                                     . Combining them yields a more informative reliability estimate
                                                                                     than the verifier’s binary decision [Geifman and El-Yaniv(2017)].
extra nodes rather than miss necessary ones. Edge-level accuracy
is lower but still substantial (F1 = 0.680), and exact graph match is
achieved in 25% of cases [Sokolova and Lapalme(2009)] .
                                                                                     4.7     Generalization Across Designs and PDKs
    Table 4 summarizes accuracy across prompt complexity. While                      We evaluate the proposed framework across different designs, pro-
performance remains near-perfect for simple tasks, exact match                       cess design kits (PDKs), and OpenROAD flow stages. Unlike prompt-
[Stengel-Eskin and Van Durme(2023)] drops to 31% for very com-                       level approaches that may overfit to specific API patterns, structural
plex prompts, confirming that precise structural recovery becomes                    verification operates on dependency constraints, enabling transfer
increasingly difficult with complexity. Despite this, execution is not               across diverse configurations.
significantly impacted, as extra nodes improve retrieval coverage                       Table 7 summarizes performance across designs and PDKs. The
and missing dependencies are corrected during verification. Thus,                    framework maintains high pass rates, indicating that structural
approximate structural extraction provides a sufficient prior for                    consistency generalizes beyond prompt-construction distributions.
correct execution .                                                                  Performance remains stable across variations in object hierarchies,
                                                                                     API usage patterns, and flow stages. Fig. 7 shows stage-wise re-
4.5.2 Verifier Contribution and Staged Enforcement. Staged veri-                     sults across OpenROAD tasks, including floorplanning, placement,
fication improves execution reliability mainly through structural                    CTS, routing, and timing. The method achieves consistent accuracy
constraint enforcement. Causal verification raises precision from                    across stages, demonstrating robustness to diverse operations and
0.508 to 0.807 and F1 from 0.674 to 0.880 over static checking. Se-                  API compositions. In contrast, baseline approaches show higher
mantic checking then refines borderline cases, and the full staged                   variability. Retrieval-based methods are sensitive to shifts in API
verifier achieves the best overall precision-recall balance.                         usage, while tool-in-the-loop approaches incur higher cost from
Structural Verification for Reliable EDA Code Generation without Tool-in-the-Loop Debugging                               ICCAD ’26, November 8–12, 2026, San Jose, CA, USA


repeated execution, especially when errors propagate across stage-                             our open-source dataset and lightweight solution. In 2024 IEEE LLM Aided Design
specific dependencies. These results suggest that structural depen-                            Workshop (LAD). IEEE, 1–5.
                                                                                          [Löding et al.(2016)] Christof Löding, P Madhusudan, and Daniel Neider. 2016. Ab-
dency modeling captures invariant properties of EDA workflows,                                 stract learning frameworks for synthesis. In International Conference on Tools and
improving robustness while maintaining low tool usage.                                         Algorithms for the Construction and Analysis of Systems. Springer, 167–185.
                                                                                          [Madaan et al.(2023)] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan,
                                                                                               Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming
5    Conclusion                                                                                Yang, et al. 2023. Self-refine: Iterative refinement with self-feedback. Advances in
                                                                                               neural information processing systems 36 (2023), 46534–46594.
We presented a framework that eliminates tool-in-the-loop de-                             [Ni et al.(2023)] Ansong Ni, Srini Iyer, Dragomir Radev, Veselin Stoyanov, Wen-tau
bugging in LLM-based EDA code generation by enforcing struc-                                   Yih, Sida Wang, and Xi Victoria Lin. 2023. Lever: Learning to verify language-to-
                                                                                               code generation with execution. In International Conference on Machine Learning.
tural correctness before execution. By modeling tasks as struc-                                PMLR, 26106–26128.
tural dependency graphs used as execution contracts, the approach                         [Osera and Zdancewic(2015)] Peter-Michael Osera and Steve Zdancewic. 2015. Type-
                                                                                               and-example-directed program synthesis. ACM SIGPLAN Notices 50, 6 (2015),
shifts correctness from post-hoc feedback to pre-execution verifi-
                                                                                               619–630.
cation, enabling graph-conditioned synthesis, staged verification,                        [Park et al.(2023)] Joon Sung Park, Joseph O’Brien, Carrie Jun Cai, Meredith Ringel
and diagnosis-driven repair with a single tool call per task. Experi-                          Morris, Percy Liang, and Michael S Bernstein. 2023. Generative agents: Interactive
                                                                                               simulacra of human behavior. In Proceedings of the 36th annual acm symposium
ments in OpenROAD show improved reliability and efficiency. The                                on user interface software and technology. 1–22.
method reaches 82.5% single-step pass rate while reducing tool calls                      [Schick et al.(2023)] Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu,
by more than 2×, and scales to multi-step tasks, achieving up to                               Maria Lomeli, Eric Hambro, Luke Zettlemoyer, Nicola Cancedda, and Thomas
                                                                                               Scialom. 2023. Toolformer: Language models can teach themselves to use tools.
84.0% with trajectory-level reflection. Uncertainty-aware filtering                            Advances in neural information processing systems 36 (2023), 68539–68551.
further improves reliability, and results across designs, PDKs, and                       [Sharma et al.(2024)] Utsav Sharma, Bing-Yue Wu, Sai Rahul Dhanvi Kankipati,
                                                                                               Vidya A Chhabria, and Austin Rovinski. 2024. Openroad-assistant: An open-
flow stages show strong generalization. Overall, the results suggest                           source large language model for physical design tasks. In Proceedings of the 2024
that failures in EDA code generation are fundamentally structural,                             ACM/IEEE International Symposium on Machine Learning for CAD. 1–7.
and that enforcing dependency consistency before execution offers                         [Shinn et al.(2023)] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik
                                                                                               Narasimhan, and Shunyu Yao. 2023. Reflexion: Language agents with verbal
a scalable alternative to execution-driven correction.                                         reinforcement learning. Advances in neural information processing systems 36
                                                                                               (2023), 8634–8652.
                                                                                          [Sokolova and Lapalme(2009)] Marina Sokolova and Guy Lapalme. 2009. A systematic
References                                                                                     analysis of performance measures for classification tasks. Information processing
[Ajayi and Blaauw(2019)] Tutu Ajayi and David Blaauw. 2019. Openroad: Toward a                 & management 45, 4 (2009), 427–437.
     self-driving, open-source digital layout implementation tool chain. In Proceedings   [Stengel-Eskin and Van Durme(2023)] Elias Stengel-Eskin and Benjamin Van Durme.
     of Government Microcircuit Applications and Critical Technology Conference.               2023. Calibrated interpretation: Confidence estimation in semantic parsing. Trans-
[Chen et al.(2023)] Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny                     actions of the Association for Computational Linguistics 11 (2023), 1213–1231.
     Zhou. 2023. Teaching large language models to self-debug. arXiv preprint             [Tayebati et al.(2026)] Sina Tayebati, Divake Kumar, Nastaran Darabi, Davide Et-
     arXiv:2304.05128 (2023).                                                                  tori, Ranganath Krishnan, and Amit Ranjan Trivedi. 2026. TRACER: Trajectory
[Cheng et al.(2024)] Pengyu Cheng, Yong Dai, Tianhao Hu, Han Xu, Zhisong Zhang,                Risk Aggregation for Critical Episodes in Agentic Reasoning. arXiv preprint
     Lei Han, Nan Du, and Xiaolong Li. 2024. Self-playing adversarial language game            arXiv:2602.11409 (2026).
     enhances llm reasoning. Advances in Neural Information Processing Systems 37         [Wang et al.(2018)] Chenglong Wang, Kedar Tatwawadi, Marc Brockschmidt, Po-Sen
     (2024), 126515–126543.                                                                    Huang, Yi Mao, Oleksandr Polozov, and Rishabh Singh. 2018. Robust text-to-
[Gao et al.(2023)] Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon, Pengfei Liu, Yim-             sql generation with execution-guided decoding. arXiv preprint arXiv:1807.03100
     ing Yang, Jamie Callan, and Graham Neubig. 2023. Pal: Program-aided language              (2018).
     models. In International conference on machine learning. PMLR, 10764–10799.          [Wang et al.(2024)] Xingyao Wang, Yangyi Chen, Lifan Yuan, Yizhe Zhang, Yunzhu
[Geifman and El-Yaniv(2017)] Yonatan Geifman and Ran El-Yaniv. 2017. Selective clas-           Li, Hao Peng, and Heng Ji. 2024. Executable code actions elicit better llm agents,
     sification for deep neural networks. Advances in neural information processing            2024. URL https://arxiv. org/abs/2402.01030 6, 1 (2024), 6–2.
     systems 30 (2017).                                                                   [Wang et al.(2022)] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi,
[Jayasuriya et al.(2025)] Dinithi Jayasuriya, Divake Kumar, Sureshkumar Senthilku-             Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. 2022. Self-consistency
     mar, Devashri Naik, Nastaran Darabi, and Amit Ranjan Trivedi. 2025. Causal-               improves chain of thought reasoning in language models. arXiv preprint
     Guided Dimension Reduction for Efficient Pareto Optimization. arXiv preprint              arXiv:2203.11171 (2022).
     arXiv:2510.09941 (2025).                                                             [Wu et al.(2024)] Bing-Yue Wu, Utsav Sharma, Sai Rahul Dhanvi Kankipati, Ajay Ya-
[Jiang et al.(2026)] Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim, and Sunghun Kim.          dav, Bintu Kappil George, Sai Ritish Guntupalli, Austin Rovinski, and Vidya A
     2026. A survey on large language models for code generation. ACM Transactions             Chhabria. 2024. Eda corpus: A large language model dataset for enhanced in-
     on Software Engineering and Methodology 35, 2 (2026), 1–72.                               teraction with openroad. In 2024 IEEE LLM Aided Design Workshop (LAD). IEEE,
[Kaintura et al.(2024)] Aviral Kaintura, Shui Song Luar, Indira Iyer Almeida, et al.           1–5.
     2024. ORAssistant: A custom RAG-based conversational assistant for OpenROAD.         [Wu et al.(2025)] Bing-Yue Wu, Utsav Sharma, Austin Rovinski, and Vidya A Chhabria.
     arXiv preprint arXiv:2410.03845 (2024).                                                   2025. OpenROAD Agent: An Intelligent Self-Correcting Script Generator for
[Kumar et al.(2025)] Divake Kumar, Patrick Poggi, Sina Tayebati, Devashri Naik,                OpenROAD. In 2025 IEEE International Conference on LLM-Aided Design (ICLAD).
     Nilesh Ahuja, and Amit Ranjan Trivedi. 2025. Calibrated Decomposition of                  IEEE, 16–22.
     Aleatoric and Epistemic Uncertainty in Deep Features for Inference-Time Adap-        [Yao et al.(2022)] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R
     tation. arXiv preprint arXiv:2511.12389 (2025).                                           Narasimhan, and Yuan Cao. 2022. React: Synergizing reasoning and acting in lan-
[Lewis et al.(2020)] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni,             guage models. In The eleventh international conference on learning representations.
     Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih,
     Tim Rocktäschel, et al. 2020. Retrieval-augmented generation for knowledge-
     intensive nlp tasks. Advances in neural information processing systems 33 (2020),
     9459–9474.
[Lin et al.(2025)] Zi Lin, Sheng Shen, Ilia Kulikov, Jingbo Shang, Jason Weston, and
     Yixin Nie. 2025. Learning to solve and verify: A self-play framework for code and
     test generation. arXiv preprint arXiv:2502.14948 (2025).
[Liu et al.(2023)] Mingjie Liu, Teodor-Dumitru Ene, Robert Kirby, Chris Cheng,
     Nathaniel Pinckney, Rongjian Liang, Jonah Alben, Himyanshu Anand, Sanmitra
     Banerjee, Ismet Bayraktaroglu, et al. 2023. Chipnemo: Domain-adapted llms for
     chip design. arXiv preprint arXiv:2311.00176 (2023).
[Liu et al.(2024)] Shang Liu, Wenji Fang, Yao Lu, Qijun Zhang, Hongce Zhang, and
     Zhiyao Xie. 2024. Rtlcoder: Outperforming gpt-3.5 in design rtl generation with
