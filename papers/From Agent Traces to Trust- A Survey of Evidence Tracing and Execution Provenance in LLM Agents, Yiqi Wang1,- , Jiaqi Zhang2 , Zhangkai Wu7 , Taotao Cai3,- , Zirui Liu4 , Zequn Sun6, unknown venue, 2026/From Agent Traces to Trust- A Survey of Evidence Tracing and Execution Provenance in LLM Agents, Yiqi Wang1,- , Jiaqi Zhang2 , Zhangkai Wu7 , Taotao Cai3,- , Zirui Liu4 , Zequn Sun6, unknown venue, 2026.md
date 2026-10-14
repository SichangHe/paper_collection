                                             F ROM AGENT T RACES TO T RUST: A S URVEY OF E VIDENCE
                                             T RACING AND E XECUTION P ROVENANCE IN LLM AGENTS

                                                        Yiqi Wang1,* , Jiaqi Zhang2 , Zhangkai Wu7 , Taotao Cai3,* , Zirui Liu4 , Zequn Sun6 ,
                                                          Manqing Dong7 , Mingkai Zheng8 , Yiqun Duan5 , Xuefei Yin1 , Yanming Zhu1
                                                        1
                                                            Griffith University 2 Jiangsu University 3 University of Southern Queensland
                                                                      4
                                                                        Peking University 5 Norve Labs Inc 6 Nanjing University
                                                             7
                                                               The University of Sydney 8 Southern University of Science and Technology
arXiv:2606.04990v5 [cs.CR] 10 Sep 2026




                                                                                  *
                                                                                      yiqi.wang.jennie@gmail.com




                                                                                            A BSTRACT
                                                 Large language model (LLM)-based agents are rapidly evolving from passive text generators into
                                                 autonomous systems capable of planning, tool use, retrieval, memory access, environmental inter-
                                                 action, and multi-agent collaboration. While these capabilities expand agent autonomy, they also
                                                 make agent behavior increasingly difficult to verify, debug, and audit. The difficulty is that agents
                                                 are evaluated almost entirely by their final answers, even though a correct answer reveals nothing
                                                 about how an output was produced, what evidence supported each claim, whether tool calls were
                                                 justified, how memory shaped later decisions, or where execution failures originated. To answer
                                                 such questions, we look beyond outputs to the execution process itself, and structure it through
                                                 evidence tracing and execution provenance. Provenance offers a process-level accountability layer
                                                 for trustworthy LLM agents by modeling the connections among retrieved evidence, tool outputs,
                                                 memory items, observations, intermediate claims, actions, and final answers. In this survey, we
                                                 treat execution provenance as the full typed graph of an agent execution and evidence tracing as its
                                                 projection onto evidence-support relations, giving a single framework that spans retrieval grounding
                                                 through audit and recovery. We introduce a taxonomy that characterizes agent systems along six
                                                 dimensions: trace sources, evidence and execution units, provenance relations, tracing granularity and
                                                 timing, representation forms, and trust functions. We then review existing methods, categorized into
                                                 seven main research threads: provenance representation, evidence attribution, tool-use provenance,
                                                 runtime guardrails, provenance-bearing memory, observability, and failure diagnosis. Finally, we
                                                 connect existing benchmarks, datasets, and metrics to provenance-related capabilities, discuss how
                                                 evaluation can move beyond final-answer correctness toward process-level accountability, and outline
                                                 open challenges for unified trace schemas, semantic provenance, provenance-aware safety, realistic
                                                 execution-trace benchmarks, recovery-oriented evaluation, and privacy-aware audit infrastructure.
                                                 Related resources are collected and continuously updated in the accompanying GitHub repository.

                                         Keywords LLM Agents, Agent Traces, Evidence Tracing, Execution Provenance, Provenance Graphs, Tool-Use Safety,
                                         Memory Provenance, Agent Observability, Runtime Guardrails, Trustworthy AI


                                         1   Introduction

                                         Large language model (LLM)-based agents are emerging as a powerful paradigm for complex task execution, moving
                                         beyond standalone text generation toward interactive execution pipelines that support reasoning, tool use, retrieval,
                                         memory access, environment interaction, and multi-agent collaboration Schick et al. [2023], Yao et al. [2023], Shinn
                                         et al. [2023]. As these capabilities expand, recent systems and benchmarks show that LLM agents increasingly operate
                                         across tools, external knowledge sources, code execution, web or GUI environments, and multi-agent workflows,
                                         creating complex execution contexts in which many intermediate sources, actions, and observations may jointly shape
                                         the final output Qin et al. [2024], Liu et al. [2024], Zhou et al. [2024], Yao et al. [2025].
                                              From Agent Traces to Trust




Figure 1: Overview of the proposed provenance framework. A user task initiates a heterogeneous agent execution
involving reasoning, retrieval, tool use, memory, environment interaction, and multi-agent communication. The
provenance layer records evidence units, execution units, and typed relations produced during this process, connecting
agent execution to downstream trust functions such as verification, attribution, debugging, safety, audit, and recovery.



This creates a process-level accountability gap in LLM agent systems. Final-answer accuracy evaluates only the
endpoint of an execution; it does not explain how an output was produced, which evidence supported each claim,
whether tool calls were justified, whether memory items were relevant and trustworthy, or which execution step caused a
failure. Recent studies make this limitation concrete: tool-safety benchmarks show that risks can arise from intermediate
tool-use decisions, adversarial tool interactions, realistic tool environments, and MCP-based workflows Ruan et al.
[2024], Debenedetti et al. [2024], Vijayvargiya et al. [2026], Zong et al. [2026], while trace-oriented and multi-agent
failure studies show that errors often require localizing responsible steps, components, agents, or error modes within
long executions Deshpande et al. [2025], Cemri et al. [2026], Zhang et al. [2026], Kong et al. [2025]. These findings
suggest that trustworthy agent systems require mechanisms that can record, connect, and reason over the evidence and
execution steps underlying agent behavior.
In this survey, we examine this need through the lens of evidence tracing and execution provenance. 1
This perspective starts from agent traces: the recorded artifacts generated or consumed during an agent run, including
instructions, retrieval queries, retrieved documents, tool calls, tool outputs, memory operations, observations, interme-
diate claims, inter-agent messages, actions, and final responses. Traceability makes these artifacts inspectable, while
provenance goes further by modeling the typed relations among them .


   1
    This perspective is informed by provenance and trace modeling in software and distributed systems, including W3C PROV-
DM for representing entities, activities, agents, and provenance relations World Wide Web Consortium [2013], OpenTelemetry
for distributed execution traces OpenTelemetry [2026], and recent agent observability systems such as AgentOps and Agent-
Trace Dong et al. [2024], AlSayyad et al. [2026].


                                                            2
                                              From Agent Traces to Trust



   Execution provenance denotes the complete typed representation of an agent run, including evidence units,
   execution units such as retrieved documents, tool calls, parameters, observations, memory accesses, intermediate
   claims, actions, inter-agent messages, and final outputs, and their causal, procedural, dependency, update,
   contradiction, and invalidation relations.


   Evidence tracing denotes the projection of this provenance structure onto evidence-support and influence
   relations between evidence units and agent claims, decisions, or actions. It is therefore a sub-problem of execution
   provenance: every evidence-support link belongs to the provenance structure, while execution provenance
   additionally records how tools, memory, observations, actions, and inter-agent messages shape the end-to-end
   execution.

Together, the two terms define the organizing contrast of this survey: execution provenance is the process view of an
agent run, while evidence tracing is the support view that explains which evidence backs which claims, decisions, and
actions.
The need for provenance appears across several parts of current LLM-agent research. Evidence grounding asks whether
generated claims are supported by retrieved sources; tool-use safety asks whether actions and arguments are justified;
memory research asks how stored information is created, updated, and reused; graph-based methods provide ways to
represent dependencies; and observability systems record executions for inspection and debugging. Viewed separately,
these topics address different trust problems. Viewed together, they point to a common process-level question: how do
evidence, tools, memory, observations, claims, actions, and agents jointly shape an execution outcome? This survey
uses evidence tracing and execution provenance to organize these questions under a single framework, summarized in
Figure 1 and developed into a six-dimensional taxonomy in Section 2. The taxonomy then guides the review along
three provenance-critical threads: representation and evidence attribution, tool-using execution, and provenance-bearing
memory, before Section 6 connects benchmarks, datasets, and metrics to process-level evaluation.
Survey scope. This survey focuses on works that make LLM-agent behavior traceable beyond final outputs. We include
methods, systems, benchmarks, and evaluation protocols when they record, represent, attribute, inspect, constrain,
or diagnose the information and execution steps that shape agent behavior. We discuss RAG, memory, graph-based
retrieval, tool-use safety, and observability not as standalone research areas, but as settings in which evidence tracing
and execution provenance become necessary. The organizing principle is provenance-centered: what should be traced,
how trace units are connected, when tracing occurs, how traces are represented, and which trust functions they support.
Literature selection. We selected papers from LLM agents, RAG attribution, tool-use safety, memory-augmented
agents, observability, and trace-based debugging when they explicitly record, represent, constrain, evaluate, or diagnose
intermediate evidence or execution artifacts. We prioritize work that introduces trace structures, provenance relations,
tool or memory lineage, runtime enforcement, failure localization, or provenance-relevant benchmarks. Rather than
exhaustively surveying all RAG, memory, agent, or safety literature, we focus on work that directly contributes to
evidence tracing or execution provenance.
In summary, this survey makes the following contributions:

       • We formulate evidence tracing and execution provenance as a unified process-level accountability framework
         for trustworthy LLM agents, distinguishing the full execution-provenance graph from its evidence-support
         projection.
       • We introduce a six-dimensional taxonomy covering trace sources, evidence and execution units, provenance
         relations, tracing granularity and timing, representation forms, and trust functions.
       • We review existing methods across seven research threads: provenance representation, evidence attribution,
         tool-use provenance, runtime guardrails, provenance-bearing memory, observability, and failure diagnosis.
       • We map benchmarks, datasets, and metrics to provenance-related capabilities, showing how evaluation can
         move beyond final-answer correctness toward trace availability, evidence support, tool-use safety, memory
         lineage, observability, and recovery.
       • We identify open challenges for provenance-aware LLM agents, including unified trace schemas, semantic
         provenance, provenance-aware safety, realistic execution-trace benchmarks, recovery-oriented evaluation, and
         privacy-aware audit infrastructure.

Structure of the Survey. The survey follows a single through-line: turning raw agent traces into accountable provenance.
Section 2 first develops a taxonomy of trace sources, evidence and execution units, provenance relations, tracing


                                                            3
                                              From Agent Traces to Trust




Figure 2: Taxonomy overview of agent provenance in this survey. The figure visualizes the main trace-generating
components, recordable units, relations, recording policy, and trust functions; Table 1 gives the complete six-dimensional
taxonomy, including representation forms.


granularity and timing, representation forms, and trust functions. We then proceed through four steps: Section 3 reviews
provenance representations, ranging from structured logs to execution graphs, evidence graphs, claim-support graphs,
and runtime provenance structures; Sections 4 and 5 examine two settings where provenance failures are especially
consequential, namely tool use and memory; Section 6 maps benchmarks and metrics to provenance-related capabilities;
and Section 7 discusses open challenges and future directions before Section 8 concludes the survey.


2   Taxonomy of Evidence Tracing and Execution Provenance

Having defined agent traces, evidence tracing, and execution provenance, this section introduces the taxonomy used
throughout the survey. The goal is not to review every system in detail, but to provide a compact vocabulary for
comparing provenance-aware agent work. We organize the space along six dimensions: trace sources, evidence and
execution units, provenance relations, tracing granularity and timing, representation forms, and trust functions. Figure 2
provides a visual overview, while Table 1 gives the full summary used as the backbone for the rest of the paper.
The taxonomy draws on two existing traditions. Provenance models such as W3C PROV-DM describe how entities,
activities, and agents participate in the production of artifacts through relations such as usage, generation, derivation,
revision, and invalidation World Wide Web Consortium [2013]. Distributed observability frameworks such as Open-
Telemetry model executions as traces and spans, which is useful for describing multi-step agent runs OpenTelemetry
[2026]. LLM agents, however, add semantic and procedural objects that these traditions do not fully capture: retrieved
passages, generated claims, tool-call rationales, memory items, natural-language observations, external state changes,
and inter-agent messages. Agent-oriented observability systems such as AgentOps and AgentTrace further motivate
structured records of both execution artifacts and context Dong et al. [2024], AlSayyad et al. [2026]. We therefore treat
classical provenance and observability as foundations, and specialize them to the execution structure of LLM agents.


                                                            4
                                                 From Agent Traces to Trust


Table 1: Taxonomy of evidence tracing and execution provenance in LLM agents. The table is the primary summary of
Section 2; the surrounding text clarifies the role of each dimension without repeating all entries.

Dimension        Categories                              Description                             Representative Work

Trace sources    Reasoning, retrieval, tool use, MCP     Components and execution                ReAct, Reflexion, ToolLLM, WebArena,
                 server/host boundaries, memory,         boundaries that generate                AutoGen, AgentTrace,
                                                                                                 MCP-SafetyBench Yao et al. [2023], Shinn
                 environment, multi-agent                provenance-relevant artifacts during    et al. [2023], Qin et al. [2024], Zhou et al.
                 communication                           agent execution.                        [2024], Wu et al. [2024], AlSayyad et al.
                                                                                                 [2026], Zong et al. [2026]
Evidence units   Documents, passages, observations,      Semantic objects that support,          ALCE, FActScore, FEVER,
                 tool outputs, memory items, claims,     contradict, invalidate, or              RAGChecker Gao et al. [2023], Min et al.
                                                                                                 [2023], Thorne et al. [2018], Ru et al.
                 policies, final answers                 contextualize agent claims, actions,    [2024]
                                                         and outputs.
Execution units Reasoning steps, retrieval calls, tool   Procedural objects that record what     AgentOps, AgentTrace, TRAIL,
                invocations, parameters, tool            the agent did, in what order, under     AgenTracer, Aegis Dong et al. [2024],
                                                                                                 AlSayyad et al. [2026], Deshpande et al.
                manifests, permission scopes,            which context, and across which         [2025], Zhang et al. [2026], Kong et al.
                memory operations, actions,              execution boundary.                     [2025]
                inter-agent messages
Provenance      Support, derive, depend-on,              Typed links that connect evidence       W3C PROV-DM, Agent-Sentry World
relations       contradict, invalidate, trigger, update, and execution units into provenance     Wide Web Consortium [2013], Sequeira
                                                                                                 et al. [2026]
                use, generate                            structures.
Tracing         Run-level, step-level, tool-call-level, Determines how fine-grained the          FActScore, SourceCheckup,
granularity     parameter-level, claim-level,            recorded provenance structure is.       Agent-Sentry Min et al. [2023], Wu et al.
                                                                                                 [2025], Sequeira et al. [2026]
                token/span-level
Tracing timing Pre-execution, runtime, post-hoc,         Determines when trace collection,       AgentSpec, Agent-Sentry, TRAIL Wang
                continuous                               verification, enforcement, or           et al. [2026], Sequeira et al. [2026],
                                                                                                 Deshpande et al. [2025]
                                                         diagnosis occurs.
Representation Structured logs, execution graphs,        Determines how traces and typed         W3C PROV-DM, AgentOps, AgentTrace,
forms           evidence graphs, claim-support           relations are encoded for inspection,   PaperTrail World Wide Web Consortium
                                                                                                 [2013], Dong et al. [2024], AlSayyad et al.
                graphs, provenance graphs, runtime comparison, enforcement, or                   [2026], Martin-Boyle et al. [2026]
                state                                    evaluation.
Trust functions Verification, attribution, debugging, Downstream purposes served by              RAGAS, AgentOps, AgentTrace,
                safety enforcement, audit, failure       evidence tracing and execution          LADYBUG, AgenTracer,
                                                                                                 OpenAgentSafety Es et al. [2024], Dong
                attribution, recovery                    provenance.                             et al. [2024], AlSayyad et al. [2026],
                                                                                                 Rorseth et al. [2025], Zhang et al. [2026],
                                                                                                 Vijayvargiya et al. [2026]



2.1   Taxonomy Dimensions

Trace sources. Trace sources are the components that generate provenance-relevant artifacts. In LLM agents, these
sources extend beyond model outputs to include reasoning, retrieval, tool use, memory, environment interaction, and
multi-agent communication. Reasoning traces can explain plans or action choices; retrieval traces provide evidence
candidates; tool traces record calls, arguments, outputs, permissions, and errors; memory traces expose cross-session
influence; environment traces record observations and state-changing actions; and multi-agent traces capture delegation,
critique, and responsibility propagation Yao et al. [2023], Shinn et al. [2023], Qin et al. [2024], Zhou et al. [2024], Yao
et al. [2025], Wu et al. [2024], Li et al. [2023]. Later sections examine tool and memory sources in depth, so here we
use them only to define the taxonomy boundary.

Evidence and execution units. Trace sources produce two broad kinds of units. Evidence units are semantic objects
that can support, contradict, invalidate, or contextualize claims and actions, such as documents, passages, observations,
tool outputs, memory items, policies, and intermediate claims. Execution units are procedural objects that describe
what the agent did, including reasoning steps, retrieval calls, tool invocations, generated parameters, memory reads or
writes, environment actions, inter-agent messages, and final outputs. The distinction is useful but not absolute: a tool
output is both the result of an execution step and possible evidence for a later claim. Provenance-aware agents therefore
need to connect semantic support with procedural execution rather than recording only one side of the trace Gao et al.
[2023], Min et al. [2023], Thorne et al. [2018], Ru et al. [2024], Dong et al. [2024], AlSayyad et al. [2026].

Provenance relations. Relations turn raw trace units into provenance. We retain PROV-compatible base relations such
as U SE, G ENERATE, and D ERIVE, and add agent-specific relations needed for LLM execution: S UPPORT, D EPEND - ON,
C ONTRADICT, I NVALIDATE, T RIGGER, and U PDATE. These relations separate semantic grounding from procedural


                                                                5
                                              From Agent Traces to Trust


dependency. For example, a passage may S UPPORT a claim, a tool call may D EPEND - ON generated parameters, a
new observation may I NVALIDATE a plan, and a failed action may T RIGGER recovery. This compact relation set is
intentionally minimal; Section 3 discusses how logs, graphs, and runtime structures encode such dependencies in
practice.

Relation to classical provenance. The proposed relation set is compatible with classical provenance modeling but
extends it for agent-specific semantics. W3C PROV-DM provides a reusable vocabulary for entities, activities, agents,
and relations such as use, generation, derivation, revision, and invalidation World Wide Web Consortium [2013]. These
constructs naturally correspond to agent artifacts, execution steps, model or tool actors, generated outputs, and memory
or state updates. However, LLM-agent provenance also requires semantic relations that classical provenance does not
directly encode. For example, S UPPORT and C ONTRADICT depend on the content-level relationship between evidence
and claims, while D EPEND - ON, T RIGGER, and I NVALIDATE capture procedural influence, recovery, and epistemic
failure during agent execution. Thus, our taxonomy reuses classical provenance as a foundation but specializes it for
evidence attribution, tool-use safety, memory lineage, and process-level accountability in LLM agents. Appendix A
provides the detailed mapping.

Tracing granularity and timing. Granularity specifies how fine-grained the trace is. Run-level traces support
coarse audit; step-level traces support debugging; tool-call and parameter-level traces support safety enforcement;
claim-level traces support factual attribution; and token- or span-level traces provide the finest but most expensive
view. Timing specifies when traces are collected or used: pre-execution checks can block unauthorized actions, runtime
tracing supports policy enforcement and information-flow control, post-hoc tracing supports audit and diagnosis, and
continuous tracing supports persistent memory and long-horizon workflows Min et al. [2023], Wu et al. [2025], Costa
et al. [2025], Cai et al. [2026], Wang et al. [2026], Sequeira et al. [2026], Deshpande et al. [2025]. The appropriate
choice depends on the risk and persistence of the workflow: low-risk RAG may require claim-level post-hoc attribution,
whereas high-impact tool use may require runtime parameter-level provenance.

Representation forms. Representation forms determine how traces are encoded. Structured logs preserve chrono-
logical events and metadata, but often leave support, contradiction, and influence implicit. Execution graphs make
procedural dependencies explicit; evidence and claim-support graphs emphasize semantic grounding; provenance
graphs combine evidence and execution units through typed edges; and runtime state representations support online
checking and enforcement. We keep this dimension concise here because Section 3 reviews representation choices in
detail.

Trust functions. The purpose of tracing is not to store more logs, but to support trust functions. Verification asks
whether claims or actions are supported by evidence; attribution identifies which evidence, tool output, memory item, or
message contributed to a claim or action; debugging localizes failures within an execution; safety enforcement prevents
untrusted or unauthorized influence from reaching sensitive actions; audit reconstructs executions for review and
accountability; and recovery uses provenance to retry, compensate, roll back, or repair affected states Gao et al. [2023],
Es et al. [2024], Deshpande et al. [2025], Rorseth et al. [2025], Debenedetti et al. [2026], Costa et al. [2025], Sequeira
et al. [2026]. These functions explain why the taxonomy includes both evidence-support links and execution-dependency
links.

2.2   Design Tensions

The taxonomy exposes four design tensions that guide the rest of the survey. First, chronological logging and semantic
provenance are not the same: a log can record what happened, but it may not show whether evidence supported a
claim or whether memory influenced a tool call. Second, component-level tracing does not guarantee end-to-end
accountability, because failures may propagate across retrieval, tools, memory, environment states, and other agents.
Third, static schemas help standardize trace objects and relations, but runtime safety requires online source tracking,
policy checking, and dependency-aware enforcement. Fourth, trace completeness must be balanced against deployability,
since fine-grained provenance improves verification, debugging, audit, and recovery but also increases storage cost,
privacy exposure, annotation burden, and system complexity.
The taxonomy is used throughout the paper as a compact comparison vocabulary. Sections 3–6 return to these tensions
when reviewing representation methods, tool-use provenance, memory provenance, and evaluation. Before turning to
these topics, Table 2 positions representative systems within the taxonomy to expose coverage gaps across trace sources,
granularity, timing, representation, and trust functions. Appendix A provides an explicit mapping to W3C PROV-DM.


                                                            6
                                                          From Agent Traces to Trust


Table 2: Representative systems mapped to the proposed taxonomy. Rows are grouped by primary trust function to
show how existing work covers trace sources, granularity, timing, and representation forms. The mapping highlights a
coverage gap: current systems often support tracing, attribution, safety enforcement, debugging, or audit separately, but
rarely integrate fine-grained provenance representation with multiple trust functions.
Primary trust                                 System                                 Trace source(s)        Granularity Timing           Representation
                                      ReAct Yao et al. [2023]                        Reasoning, tool, env   Step           Runtime       Reasoning–
                                                                                                                                         action log
                                Generative Agents Park et al. [2023]                 Memory, env            Step           Continuous    Memory stream
Substrate                         Toolformer Schick et al. [2023]                    Tool                   Tool-call      Pre-exec.     —
                                    ToolLLM Qin et al. [2024]                        Tool                   Tool-call,     Runtime       API-call path
                                                                                                            param.
                                    AutoGen Wu et al. [2024]                         Multi-agent, tool      Step           Runtime       Message log
                                   MemGPT Packer et al. [2023]                       Memory                 Step           Continuous    Tiered memory
                                    A-MEM Xu et al. [2026]                           Memory                 Step           Continuous    Linked memory
                                      ALCE Gao et al. [2023]                         Retrieval              Claim        Post-hoc        Citation links
Attribution /                       FActScore Min et al. [2023]                      Retrieval              Atomic claim Post-hoc        Claim–evidence
Verification                      SourceCheckup Wu et al. [2025]                     Retrieval              Claim        Post-hoc        Source–support
                                   RAGChecker Ru et al. [2024]                       Retrieval              Claim        Post-hoc        Claim–evidence
                                 CaMeL Debenedetti et al. [2026]                     Tool                   Parameter      Runtime       Control/data flow
                                    FIDES Costa et al. [2025]                        Tool, memory           Parameter      Runtime       IFC labels
                                   NeuroTaint Cai et al. [2026]                      Tool, memory           Param./token   Runtime       Taint labels
Safety
                                  AgentSpec Wang et al. [2026]                       Tool, env              Tool-call      Pre/Runtime   Policy rules
                                 AgentBound Bühler et al. [2026]                     Tool                   Tool-call      Pre/Runtime   Permissions
                                Agent-Sentry Sequeira et al. [2026]                  Tool                   Parameter      Runtime       Provenance graph
                                   ToolEmu Ruan et al. [2024]                        Tool                   Tool-call      Runtime       Action log
                                  InjecAgent Zhan et al. [2024]                      Tool, env              Tool-call      Runtime       —
Safety (eval)
                                AgentDojo Debenedetti et al. [2024]                  Tool, env              Tool-call      Runtime       —
                                    τ -bench Yao et al. [2025]                       Tool, env              Tool-call      Post-hoc      State log
Recovery                            Reflexion Shinn et al. [2023]                    Reasoning, memory      Step           Continuous    Episodic memory
                                 TRAIL Deshpande et al. [2025]                       All sources            Step           Post-hoc      Annotated trace
Debugging /                        MAST Cemri et al. [2026]                          Multi-agent            Step           Post-hoc      Failure taxonomy
Audit                             WebArena Zhou et al. [2024]                        Env, tool              Step           Post-hoc      Action/state log
                  AgentOps / AgentTrace Dong et al. [2024], AlSayyad et al. [2026]   All sources            Step           Post-         Structured log
                                                                                                                           hoc/Cont.




2.3      Positioning Existing Systems in the Taxonomy

Table 2 positions representative agent, attribution, safety, memory, and observability systems within the taxonomy. The
table is not intended as an exhaustive benchmark, but as a diagnostic map of where current work concentrates and
where coverage remains incomplete. Three patterns emerge. First, trace-generating systems such as ReAct, AutoGen,
MemGPT, and Generative Agents produce rich execution artifacts, but usually do not implement trust functions such as
verification, attribution, enforcement, audit, or recovery on their own. They provide substrates on which provenance
mechanisms can be built. Second, attribution and verification systems such as ALCE, FActScore, SourceCheckup,
and RAGChecker provide claim-level support analysis, but mostly operate over retrieval evidence and final answers
rather than tools, memory, environment actions, or multi-agent communication. Third, safety and enforcement systems
such as CaMeL, FIDES, NeuroTaint, and Agent-Sentry operate at runtime over tool calls, parameters, permissions, or
information-flow labels, but often lack semantic claim-evidence attribution.
This mapping shows why evidence tracing and execution provenance should be treated as a unified layer rather than as
separate literatures. Existing systems usually cover one or two dimensions well: they may record traces, verify claims,
enforce tool-use policies, audit executions, or diagnose failures. However, no existing line of work simultaneously
spans diverse trace sources, fine-grained units, runtime timing, explicit provenance representation, and multiple trust
functions. This gap motivates the rest of the survey, which reviews representation, attribution, tool-use provenance,
memory provenance, observability, safety, and evaluation as connected parts of the same provenance problem.


3     Provenance Representation and Evidence Attribution

The previous section identifies what should be traced; this section asks how traces should be represented. We organize
provenance representation into three layers. Structured logs record typed execution events. Execution graphs connect
instructions, retrievals, tool calls, memory operations, observations, claims, and actions through dependency relations.
Evidence and claim-support graphs further specify whether evidence units support, contradict, or fail to support
generated claims. This layered view is central to the rest of the survey: logs make executions reconstructable, graphs


                                                                           7
                                              From Agent Traces to Trust




Figure 3: Running example of a provenance graph for an LLM-agent execution. The graph connects user queries,
retrieved passages, intermediate claims, tool calls, tool outputs, memory items, new evidence, and final actions through
typed relations such as S UPPORT, D ERIVE, D EPEND - ON, C ONTRADICT, I NVALIDATE, and U PDATE.




make dependencies inspectable, and claim-support links make grounding and accountability measurable. Figure 3
provides a running example. It shows how evidence acquisition, claim construction, tool execution, memory update,
and recovery can be represented as a typed provenance graph rather than a flat chronological transcript.
Figure 3 provides a running example for this section. It instantiates the taxonomy by showing how evidence acquisition,
claim construction, tool execution, and conflict-driven update or recovery can be represented as a typed provenance
graph rather than as a flat chronological log.



3.1   From Logs to Execution Graphs

A natural starting point is the structured execution log. Instead of storing free-form transcripts alone, logs record typed
events such as user requests, model outputs, retrieval calls, tool invocations, tool outputs, memory reads and writes,
environment observations, inter-agent messages, and final responses. W3C PROV-DM provides a general vocabulary
of entities, activities, agents, and derivation relations [World Wide Web Consortium, 2013]. PROV-AGENT adapts
this vocabulary to agentic workflows by modeling prompts, responses, decisions, tool interactions, and workflow
context [Souza et al., 2025]. AgentOps emphasizes relationships among artifacts across the agent lifecycle [Dong et al.,
2024], while AgentTrace organizes execution records into operational, cognitive, and contextual logs [AlSayyad et al.,
2026].
Logs provide chronological observability, but dependency analysis requires graph structure. A log can show that a
retrieval, tool call, and memory write occurred; it may not show which retrieved passage supported a claim, which tool
output changed the plan, or which memory item influenced an action. Execution graphs address this gap by representing
execution artifacts as nodes and their influence relations as typed edges. TRAIL demonstrates how annotated trajectories
can localize failures to particular steps, components, or interactions [Deshpande et al., 2025]. AgenTracer further
uses counterfactual replay and fault injection to attribute failures to responsible agents and steps [Zhang et al., 2026],
whereas Aegis uses positive–negative trajectory pairs to identify faulty agents and error modes [Kong et al., 2025].
Thus, logs answer what happened; execution graphs answer what depended on what.


                                                            8
                                               From Agent Traces to Trust


                           Table 3: Main provenance representation forms for LLM agents.

Form              What it captures                                       Main role
Structured logs  Typed execution events such as requests, retrieval calls, Execution observability and reconstruction.
                 tool calls, memory operations, observations, and out-
                 puts.
Execution graphs Dependencies among instructions, evidence, tool calls, Influence analysis for debugging, audit, and recovery.
                 memory items, claims, and actions.
Evidence graphs Links among evidence units, citations, atomic claims, Separation of citation presence, relevance, support,
                 and generated answers.                                    contradiction, and omission.
Static schemas   Object types, relation types, trust labels, and required A reusable vocabulary for trace representation and
                 provenance fields.                                        comparison.
Runtime prove- Concrete source-to-sink, tool, memory, and action de- Runtime monitoring, enforcement, recovery, and
nance            pendencies during execution.                              information-flow analysis.



3.2   Evidence and Claim-Support Attribution

Evidence attribution adds a semantic layer on top of execution dependencies. The key issue is whether a generated
claim is actually supported by the evidence it cites or depends on. Existing work motivates this distinction at different
granularities: citation-based evaluation links generated answers to sources [Gao et al., 2023]; atomic-fact evaluation
checks fine-grained factual support [Min et al., 2023]; source-checking work shows that a cited source may be relevant
without supporting the specific claim [Wu et al., 2025]; and claim–evidence mapping explicitly distinguishes supported
claims, unsupported claims, and omitted evidence [Martin-Boyle et al., 2026].
For provenance representation, these correspond to distinct edge types rather than a single citation relation. A source
may be C ITED but not S UPPORT a claim; a relevant passage may be available but O MITTED from the answer; a tool
output may C ONTRADICT a memory item; and new evidence may I NVALIDATE an earlier belief. Evidence graphs
therefore distinguish evidence availability from evidence use. In LLM agents, evidence-bearing units include not only
retrieved documents, but also tool outputs, memory items, environment observations, policies, and inter-agent messages.

3.3   Representation Trade-offs

Static schemas and runtime provenance form two complementary layers of provenance representation. A static schema
defines object types, relation types, trust labels, and required fields, including evidence units, tool calls, memory
items, claims, actions, and relations such as S UPPORT, D EPEND - ON, C ONTRADICT, U PDATE, and I NVALIDATE.
Runtime provenance instantiates this schema during a concrete execution, recording the actual dependencies among
sources, tool calls, memory operations, claims, and actions. Observability systems emphasize runtime trace capture and
inspection [Dong et al., 2024, AlSayyad et al., 2026]. Safety-oriented systems additionally use runtime provenance
for enforcement [Sequeira et al., 2026], information-flow control [Costa et al., 2025], and source-to-sink influence
analysis [Cai et al., 2026].
The central trade-off concerns granularity. Fine-grained provenance enables claim verification, failure localization,
rollback, audit, and policy enforcement, but increases storage cost, logging complexity, privacy exposure, and annotation
burden. Coarse-grained provenance is easier to collect, but may miss the evidence that supported a claim, the memory
item that caused an error, or the tool argument that crossed a trust boundary. The appropriate granularity therefore
depends on the trust function: claim-level links may suffice for low-risk RAG, tool-using agents require parameter-level
provenance, and long-term personalized agents require memory lineage, invalidation, and recovery support. Table 3
summarizes the main representation forms discussed in this section.


4     Execution Provenance in Tool-Using Agents

Tool use is the outward axis of agent provenance: it is where an LLM agent moves from generating text to interacting
with APIs, databases, code interpreters, browsers, filesystems, enterprise systems, and other external environments. A
tool call may retrieve private data, modify external state, send messages, execute code, or trigger irreversible actions.
Trustworthy tool use therefore requires tracing why a tool was selected, where its arguments came from, whether its
output was reliable, and how the result shaped later decisions. This section reviews five provenance-critical questions:
what to trace in tool execution, how external content contaminates tool use, how unsafe influence can be constrained,
how action boundaries are enforced, and how traces support verification and recovery.


                                                              9
                                              From Agent Traces to Trust


4.1   Tool-Call, Argument, and Output Provenance

Tool-call provenance records the path from tool selection to downstream influence: which tool was selected, which argu-
ments were passed, what output was returned, and how that output affected later reasoning or actions. Toolformer Schick
et al. [2023] and ToolLLM Qin et al. [2024] show that external tools can expand LLM capabilities through API calls,
calculation, search, and other operations. Beyond execution success, provenance asks whether the call is justified,
whether its arguments are derived from trusted or authorized sources, and whether its output is used appropriately.
A tool call contains several provenance-critical objects: the selected tool, schema, argument values, execution result, and
downstream consumers. Argument provenance is especially important because legitimate tools can become unsafe when
their parameters are derived from untrusted or incorrectly generated values. Agent-Sentry tracks the sources of values
flowing into sensitive tool arguments, demonstrating why parameter-level lineage is needed beyond tool-level permission
checks Sequeira et al. [2026]. Tool outputs are also provenance-bearing units: they may support claims, update memory,
trigger additional tools, modify external state, or conflict with other evidence. WebArena highlights the importance
of correctly interpreting observations and executing state-changing actions in realistic web environments Zhou et al.
[2024], while τ -bench evaluates tool-agent-user interactions under domain-specific policies Yao et al. [2025]. Tool-use
provenance should therefore connect sources, arguments, outputs, and downstream consumers into a single dependency
chain.

4.2   Indirect Prompt Injection and Tool-Use Contamination

Tool-using agents are vulnerable to indirect prompt injection because they consume external content that may contain
adversarial instructions. Unlike direct prompt injection, where the malicious instruction is placed in the user prompt,
indirect injection embeds the instruction in webpages, documents, emails, database entries, tool outputs, or third-party
API responses. The attack exploits a boundary failure: untrusted data may be interpreted as executable guidance rather
than passive evidence Greshake et al. [2023], Liu et al. [2023].
InjecAgent benchmarks indirect prompt injection in tool-integrated agent scenarios Zhan et al. [2024], while AgentDojo
evaluates attacks and defenses in realistic task environments Debenedetti et al. [2024]. Related benchmarks broaden the
tool-risk surface. ToolEmu evaluates risky tool execution in an emulated sandbox Ruan et al. [2024]; OpenAgentSafety
covers real tools such as browsers, code execution, filesystems, shells, and messaging platforms Vijayvargiya et al.
[2026]; and MCP-SafetyBench targets real MCP servers and multi-server workflows Zong et al. [2026]. Together, these
benchmarks show that contaminated tool contexts can cause unauthorized tool use, privacy leakage, ignored user intent,
and unintended state changes.
From a provenance perspective, indirect prompt injection is an information-flow and influence-tracking problem. The
key question is whether malicious content influenced a later tool call, argument value, memory update, or external
action. A flat log may show that a webpage was retrieved and an email tool was later called, but not whether the
recipient, subject, or body came from the webpage, the user instruction, or the model’s reasoning. Relations such
as D ERIVE, D EPEND - ON, T RIGGER, and U SE make this influence explicit. Tool-use provenance should therefore
distinguish trusted intent from untrusted content and support enforcement against unsafe flows into privileged execution
channels.

4.3   Information Flow, Taint Tracking, and Provenance Enforcement

Recent defenses increasingly treat tool-use safety as an information-flow problem. Instead of relying only on prompting
or output filtering, they track where information originates, how it propagates, and whether it is allowed to influence
sensitive actions. This view extends classical information-flow control, where security policies regulate flows among
subjects, objects, and security classes Denning [1976], Sabelfeld and Myers [2003]. For LLM agents, the analogous
goal is to prevent low-integrity or untrusted data from exerting unauthorized influence over privileged tool calls, memory
updates, or state-changing actions.
Defenses instantiate this principle at different layers. Instruction Hierarchy establishes precedence among instruction
sources Wallace et al. [2024], whereas StruQ separates instructions from untrusted data through structured channels Chen
et al. [2025]. CaMeL makes this separation explicit at execution time by isolating control flow from data flow and
restricting how external data can influence agent behavior Debenedetti et al. [2026]. FIDES formalizes agent-level
information-flow control through confidentiality and integrity labels enforced during execution Costa et al. [2025].
At finer granularity, NeuroTaint propagates taint across neural and symbolic components Cai et al. [2026], while
Agent-Sentry tracks whether sensitive tool arguments are influenced by untrusted sources Sequeira et al. [2026].
The key lesson is that unsafe behavior can arise from influence, not content alone. A webpage may be safe to
summarize but unsafe if an embedded instruction determines an email recipient, database parameter, or authorization


                                                           10
                                              From Agent Traces to Trust


signal. Runtime provenance makes this distinction explicit by connecting sources, transformations, and sinks, allowing
enforcement policies to account for a origin of value and use as well as its content.

4.4   Access Control and Execution Boundaries

Information-flow tracking must be paired with access control and execution boundaries. Even if an agent can reason
about many tools, it should not be allowed to invoke every tool in every context. Classical principles such as least
privilege and complete mediation require sensitive actions to be explicitly authorized and access decisions to be checked
at the point of use Saltzer and Schroeder [1975]. In tool-using agents, these principles translate into tool permissions,
argument constraints, user confirmations, sandboxing, and policy-mediated execution.
Recent systems operationalize these principles at different layers. AgentSpec enforces user-defined runtime constraints
over agent actions and tool use Wang et al. [2026]. AgentBound provides capability-constrained access control for
MCP servers, limiting the resources available to each server Bühler et al. [2026]. Agent-Sentry instead uses execution
provenance, including per-argument data flow, to bound tool calls according to learned behavior and user intent Sequeira
et al. [2026]. Together, these systems show that tool-use safety requires controlling which tools and resources can be
accessed, under what context, with which arguments, and with what external effects.
Provenance makes these controls context-sensitive. Agent-Sentry, for example, uses per-argument data flow and
user-intent alignment to assess proposed tool calls Sequeira et al. [2026]. A read-only search tool may be permitted to
consume untrusted web content, whereas an email, database-update, or code-execution tool may require arguments
derived from authorized user intent, verified tool outputs, or explicit approval. Access control and provenance are
therefore complementary: capability policies delimit the tools and resources available to an agent Bühler et al. [2026],
while provenance and runtime rules determine whether a particular action should proceed, be restricted, require
confirmation, or be blocked Wang et al. [2026], Sequeira et al. [2026].

4.5   Runtime Guardrails and Pre-/Post-Execution Verification

Runtime guardrails check agent behavior before, during, or after execution. Pre-execution guardrails decide whether a
proposed tool call should proceed; runtime monitors track information flow and state changes; post-execution verification
inspects traces, outputs, and side effects for debugging, audit, and recovery. General guardrail systems illustrate how
safety mechanisms can be placed around LLM applications: NeMo Guardrails provides programmable conversational
guardrails Rebedea et al. [2023], while Llama Guard provides model-based input/output safety classification Inan et al.
[2023]. Tool-using agents, however, require checks over execution state, tool arguments, and downstream effects, not
only input–output text.
For high-impact tools, pre-execution verification is critical. A provenance-aware guardrail can check whether the
tool is authorized, whether user intent is present, whether arguments are well formed, whether sensitive fields come
from trusted sources, and whether the action violates policy. AgentSpec formalizes runtime constraints over agent
actions Wang et al. [2026]. Agent-Sentry uses execution provenance to verify whether sensitive tool arguments are
influenced by untrusted sources Sequeira et al. [2026]. ToolEmu complements these defenses by evaluating risky tool
executions in an emulated sandbox Ruan et al. [2024].
Post-execution verification supports failure localization and repair. When an agent gives a wrong answer or performs
an unsafe action, traces can help identify whether the failure arose from evidence, tool use, memory, or downstream
reasoning. AgentOps records agent artifacts and their lifecycle relationships Dong et al. [2024], while AgentTrace
structures execution records into operational, cognitive, and contextual traces AlSayyad et al. [2026]. TRAIL localizes
failures using annotated trajectories Deshpande et al. [2025], and LADYBUG uses trace-based debugging to support
failure localization and repair Rorseth et al. [2025].
Effective guardrails therefore require both semantic and procedural provenance: semantic provenance links claims
to supporting or contradicting evidence, while procedural provenance links actions to authorized paths and trusted
inputs. Together, they help detect unsupported claims, contaminated arguments, unauthorized tool calls, and invalid
state updates.
Table 4 summarizes representative systems according to their main focus, provenance object, enforcement timing, and
role in tool-use provenance.

4.6   Summary

Tool-using agents make execution provenance necessary because tool calls can consume untrusted information, expose
private data, modify external state, and trigger downstream consequences. The core questions are where tool arguments


                                                          11
                                                              From Agent Traces to Trust


Table 4: Representative work on tool-use execution provenance. The table groups systems by the objects they track, the
mechanisms they use, and the provenance role they support.
Line of Work        Representative Systems                      Tracked Objects             Core mechanism (how)                            Provenance Role
Tool-use learning   Toolformer Schick et al. [2023];          Tool calls, API arguments, Learn when and how to call tools from                 Tool-call trace
                    ToolLLM Qin et al. [2024]                 tool outputs                  (self-)supervised tool-use trajectories            construction
Prompt-injection    InjecAgent Zhan et al. [2024];            External content, injected Embed adversarial instructions in external            Contamination and risk
benchmarks          AgentDojo Debenedetti et al. [2024];      instructions, private data content and measure unsafe actions in                 evaluation
                    ToolEmu Ruan et al. [2024]                                              (emulated) tool execution
Instruction–data    Instruction Hierarchy Wallace et al.      Privileged instructions,      Mark privileged instructions vs. untrusted data Data–instruction
separation          [2024]; StruQ Chen et al. [2025];         untrusted data,               and separate control flow from data flow via       boundary control
                    CaMeL Debenedetti et al. [2026]           control/data flow             training or structured channels
Information-flow    FIDES Costa et al. [2025]; NeuroTaint Cai Security labels, tainted      Attach confidentiality/integrity (or taint) labels Source-to-sink
tracking            et al. [2026]                             values, influence paths       and propagate them source-to-sink, including enforcement
                                                                                            through semantic transformations
Argument            Agent-Sentry Sequeira et al. [2026]       Tool arguments, sources, Build an execution-provenance graph and                 Sensitive-argument
provenance                                                    trust labels                  check whether sensitive tool arguments derive verification
                                                                                            from untrusted sources
Execution           AgentSpec Wang et al. [2026];             Agent actions,                Specify, enforce, or evaluate constraints over Runtime action
boundaries          AgentBound Bühler et al. [2026];          permissions, policy           agent actions and tool access                      constraints and
                    MCP-SafetyBench Zong et al. [2026]        constraints, and tool                                                            boundary-aware
                                                              interfaces                                                                       provenance
Guardrails          NeMo Guardrails Rebedea et al. [2023]; Inputs, outputs, dialogue External rule/classifier layer that filters inputs, Application-level safety
                    Llama Guard Inan et al. [2023]            states, safety policies       outputs, and dialogue states against safety        filtering
                                                                                            policies
Trace-based         AgentOps Dong et al. [2024];              Structured traces, artifacts, Record structured execution traces and localize Audit, localization, and
debugging           AgentTrace AlSayyad et al. [2026];        failure locations             failures post hoc for audit and repair             recovery
                    TRAIL Deshpande et al. [2025];
                    LADYBUG Rorseth et al. [2025]




come from, whether tool outputs are trustworthy, how external content influences actions, and whether execution remains
within authorized boundaries. Recent work on prompt-injection benchmarks, information-flow control, taint tracking,
execution bounding, runtime guardrails, observability, and trace-based debugging marks a shift from output-only safety
toward provenance-aware execution control.
Synthesis: from tool logging to influence control. Tool-use provenance is moving from recording events to governing
influence. Tool-level traces show which API was called, but not whether the call was necessary, justified, or consistent
with the user’s goal. Parameter lineage can detect untrusted values in sensitive arguments, but may miss invalid
interpretation of tool outputs. Information-flow and taint-based methods constrain unsafe influence, but remain difficult
under summarization, paraphrasing, memory consolidation, and multi-step reasoning. The next step is to unify tool-call
lineage, semantic evidence support, source trust, state changes, policy compliance, and recovery dependencies across
the full agent workflow.



5    Memory as Provenance-Bearing Evidence

Memory is the inward counterpart of tool use. Instead of producing immediate external actions, evidence is retained,
transformed, retrieved, and reused across turns, tasks, sessions, and environments. This makes memory a persistent
part of the provenance chain: a memory item may later support a claim, shape a plan, fill a tool argument, update
another memory, or justify a final answer. Memory therefore sharpens the trace-completeness tension: agents benefit
from compact, persistent, and adaptive memory, but accountability requires source lineage, retrieval context, temporal
validity, conflict status, and downstream influence.
This section does not survey memory architectures in general. Existing work has already reviewed memory mechanisms
and evaluation protocols for LLM agents [Zhang et al., 2025, Du, 2026], as well as graph-based memory systems [Yang
et al., 2026]. We instead treat memory items as evidence-bearing objects. Under this view, a memory is not only
something stored and retrieved; it is an artifact with an origin, transformations, revisions, validity conditions, and later
effects. Without these links, long-term memory becomes an opaque evidence source rather than an auditable component
of agent execution.
Figure 4 summarizes this lifecycle. Unlike storage-centric views of memory, it treats memory items as provenance-
bearing evidence objects whose origins, updates, retrievals, validity, and downstream influence should remain in-
spectable.


                                                                                12
                                                                        From Agent Traces to Trust



                                                        Memory Provenance Lifecycyle
                                      Source Evidence                                                                                                        Update and Append
       1
                        ......     PDF
                                                                                                                                                                           ... PDF

                                                                         Environment                                                                                                                        Update /
            User                 Retrieved Doc   Tool Output                                                                                                               New Evidence
                                                                         Observation                                                                                                                         Refine
            Input
                                    Write into Memory                                                                                              Versioning and Consolidation
                  PDF                                                                                                                                                                                             3
            ...                                     2                                                               v3
                                                                                                                     v2
                                                                                                                       v1
                                                          scr: doc   t = 10:15        tool: calc
                                                                                                                                                                                                    v1     v2   v3
                                                                     id: a7f3...
                                                                                                                                                                   Merge / Summarize                     Versioned
                                                                                                                        Memory Versions
      Write / Encode / Attach Provenance                       Memory Item                                                                                           / Consolidate                        Memory

                                   Memory Ingestion                                                                                 Versioned Memory Maintenance
                                                                                                         Retrieve


                                 Retrieve Relevant Memory                                                           5               Influence on Claim / Tool Call / Action


      Current Query
                                                                     scr: doc       t=
                                                                                  10:15
                                                                                id: a7f3...
                                                                                            tool: calc

                                                                                                                         scr: doc       t=
                                                                                                                                      10:15
                                                                                                                                                tool: calc
                                                                                                                                                                      ...
          / Task                         Retrieve               Relevant Memory                                                     id: a7f3...
                                                                                                                                                                      Claim             Tool Call        Action
                                                                                                                    Retrieved Memory
                                 Current Agent Execution
       4                                                                                                                                                     Audit / Invalidation
                                                                                                                    6


                                                                                                                          Conflict                           Staleness               Poisoning      Invalidation
           Planning               Reasoning         Tool Use               Grounded                                     Contradictory                        Outdated          Malicious or Proven or Policy-
                                                                            Context                                      Information                         Relative to     Manipulated Data    Based
                                                                                                                                                              Context                           Removal
                   Memory Use in Agent Sessions                                                                                                       Provenance Outcomes

       1-2. Soure & Ingest                       3. Maintain & Version                                       4. Retrieve & Execute                                          5-6. Influence & Audit


Figure 4: Memory as provenance-bearing evidence across agent sessions. Memory items are written from source
evidence, maintained through updates and consolidation, retrieved into later agent executions, used to influence claims
and actions, and audited for conflicts, staleness, poisoning, and invalidation.



5.1   Memory Writes, Source Attribution, and Lineage

Memory provenance begins when a memory item is written. A memory write may originate from user input, retrieved
documents, environment observations, tool outputs, feedback, reflections, or messages from other agents. Existing
memory systems illustrate different write paths: Generative Agents store observations for later reflection and plan-
ning [Park et al., 2023]; Reflexion writes verbal feedback into episodic memory after failures [Shinn et al., 2023];
MemoryBank updates long-term user memories through interaction [Zhong et al., 2024]; MemGPT manages movement
across memory tiers through explicit read and write operations [Packer et al., 2023]; and A-MEM links new memories
into an evolving memory structure [Xu et al., 2026].
From a provenance perspective, the important unit is not the memory record alone, but the relation between the record
and the evidence that produced it. Each memory write should carry source and lineage metadata, including source
type, timestamp, authoring agent, supporting evidence, transformation operation, confidence, and update history. This
follows the broader provenance principle that generated artifacts should be linked to the entities, activities, and agents
that produced them [World Wide Web Consortium, 2013, Souza et al., 2025], and aligns with tracing frameworks that
record execution artifacts and operational context [AlSayyad et al., 2026, Sequeira et al., 2026]. Such lineage is crucial
because memory writes often transform information: documents are summarized, observations are merged, preferences
are inferred, and failures are abstracted into reflections. A provenance-bearing memory should therefore distinguish raw
observations, extracted facts, inferred memories, and revised memories.


                                                                                                           13
                                                From Agent Traces to Trust


Synthesis. Memory accountability starts at write time. If a memory is stored without source and transformation
metadata, later verification can inspect only its surface content, not its evidential basis.

5.2   Memory Retrieval, Temporal Validity, and Downstream Influence

Retrieval determines which stored information re-enters the current execution. Retrieved memories may affect task
decomposition, answer generation, tool choice, argument construction, user modeling, and future memory updates.
Existing memory systems motivate this retrieval-centered view: MemoryBank and Mem0 emphasize personalization
and multi-session continuity [Zhong et al., 2024, Chhikara et al., 2025]; MemGPT and LongMem manage information
beyond the current context window [Packer et al., 2023, Wang et al., 2023]; and A-MEM improves retrieval through
dynamic memory linking [Xu et al., 2026].
The provenance risk is that retrieved memory may be only partially relevant, outdated, over-generalized, derived from
hallucinated content, poisoned by adversarial interaction, or invalid under the current context. Memory poisoning and
injection attacks show that persistent memory can steer later responses and actions across sessions [Chen et al., 2024,
Dong et al., 2025, Tian et al., 2026, Pulipaka et al., 2026]. Temporal validity is therefore central: a memory item should
record when it was created or updated, what evidence supported it, whether that evidence remains valid, and whether
later observations superseded it.
A provenance-aware retrieval trace should record the triggering query or context, retrieved memory items, original
sources, relevance signals, validity status, and downstream links to claims, tool calls, actions, final answers, or later
memory updates. This would allow systems to identify whether a final output was influenced by a particular memory
and whether that influence was justified. It also enables selective invalidation: when a memory is stale, unsupported,
private, or contaminated, affected claims, actions, and derived memories can be located instead of treating the execution
history as opaque [Wang et al., 2025, Wei et al., 2025, Sequeira et al., 2026].
Synthesis. Retrieval is not only a relevance problem. It is an influence problem: once memory enters context,
provenance must track what it shaped and whether that influence remains defensible.

5.3   Conflicting, Contradictory, and Poisoned Memory

Persistent memory can accumulate incompatible, invalidated, or contaminated information. A stored memory may
conflict with newer evidence, encode an adversarial instruction, or preserve a weak inference as if it were a stable fact.
Recent attacks make this risk concrete. AgentPoison shows that poisoned long-term memory or RAG knowledge bases
can act as backdoor substrates for agents [Chen et al., 2024]. Memory-injection attacks show that malicious records can
be introduced through ordinary interactions [Dong et al., 2025]. Environment-injected and sleeper memory poisoning
studies further show that untrusted webpages, documents, or repositories can enter memory, persist silently, and later
steer behavior [Zou et al., 2026, Pulipaka et al., 2026].
This connects memory provenance to tool safety and information-flow control. FIDES tracks confidentiality and
integrity labels to restrict unsafe information flows [Costa et al., 2025], while NeuroTaint emphasizes that unsafe
influence can survive semantic transformation and memory reuse rather than appearing as exact text reuse [Cai et al.,
2026]. Indirect prompt-injection benchmarks such as InjecAgent and AgentDojo show how untrusted external content
can manipulate tool-using agents [Zhan et al., 2024, Debenedetti et al., 2024]. When such content is written into
memory, a single-run attack becomes a long-horizon provenance failure.
Synthesis. Memory quality cannot be measured only by recall, personalization, or coherence. It also depends on source
trust, write-path legitimacy, conflict status, contamination risk, and whether a memory is later activated in consequential
decisions.

5.4   Memory-Grounded Verification and Long-Term Audit

Memory-grounded verification extends evidence tracing from retrieved documents and current tool outputs to persistent
memory. When a claim or tool action relies on memory, the system should link that memory item to the observation,
document, tool call, user statement, or reflection that created it, as well as to later revisions, conflicts, invalidations, and
downstream uses. Claim–evidence interfaces such as PaperTrail motivate this granularity by decomposing answers
and sources into discrete claims and evidence units [Martin-Boyle et al., 2026]. AgentOps and AgentTrace provide
foundations for structured execution logs and inspection [Dong et al., 2024, AlSayyad et al., 2026], while Agent-Sentry
shows how provenance graphs can support source-aware enforcement over tool-call arguments [Sequeira et al., 2026].
Long-term memory requires an analogous structure across sessions.


                                                              14
                                                              From Agent Traces to Trust


Table 5: Agent memory through a provenance lens. Existing memory systems support long-term recall, updates, and
adaptive behavior, but provenance-specific capabilities such as source attribution, conflict handling, staleness detection,
contamination tracking, and evidence-aware verification remain limited.
Symbols: ✓ = Yes; ▲ = Partial; ❍ = Limited; ✗ = No; ★ = Attack-focused.
Paper / System                       Memory Type                                    Update / Evolution    Write   Retr.   Conf.   Stale   Verify
Generative Agents [Park et al.,      Memory stream / reflection                     Reflection-based       ▲       ▲       ✗       ✗        ✗
2023]
Reflexion [Shinn et al., 2023]       Episodic memory / feedback                     Feedback-driven        ▲       ▲       ✗       ✗       ▲
MemoryBank [Zhong et al., 2024]      Long-term interaction memory                   Continuous update      ▲       ✓       ❍       ❍       ✗
MemGPT [Packer et al., 2023]         Hierarchical virtual memory                    Memory-tier            ✓       ✓       ❍       ❍       ✗
                                                                                    management
LongMem [Wang et al., 2023]          Long-term memory for LMs                       Cache and update       ▲       ✓       ✗       ▲       ✗
Mem0 [Chhikara et al., 2025]         Production long-term memory                    Extraction and         ✓       ✓       ❍       ▲       ▲
                                                                                    consolidation
A-MEM [Xu et al., 2026]              Agentic interconnected memory                  Dynamic linking and    ✓       ✓       ❍       ▲        ✗
                                                                                    evolution
AgentPoison / Memory                 Poisoned or injected memory                    Cross-session          ★       ★       ✗       ✗        ✗
Injection [Chen et al., 2024, Dong                                                  persistence
et al., 2025]
FIDES / NeuroTaint [Costa et al.,    Information-flow and taint tracking            Tracks influence       ✓       ✓       ✓       ▲        ✓
2025, Cai et al., 2026]
AgentOps / AgentTrace [Dong et al., Execution logs and traces                       Trace-level history    ▲       ▲       ✗       ✗       ▲
2024, AlSayyad et al., 2026]
Agent-Sentry [Sequeira et al., 2026] Execution provenance graph                     Runtime provenance     ✓       ✓       ▲       ▲        ✓




Despite progress in systems such as MemGPT, A-MEM, and Mem0 [Packer et al., 2023, Xu et al., 2026, Chhikara et al.,
2025], most memory systems still optimize for recall, personalization, efficiency, or coherence, with limited support for
tracing origins, temporal validity, conflicts, contamination, privacy exposure, and downstream influence. This gap is
critical because memory itself can become an attack surface: poisoned, injected, stale, or private memories may later
shape claims and actions without appearing as external evidence [Chen et al., 2024, Tian et al., 2026, Pulipaka et al.,
2026, Wang et al., 2025]. Defense work such as A-MemGuard suggests that memory should support checking and
correction, not only input-time filtering [Wei et al., 2025].
Table 5 summarizes this gap. Across representative memory systems and security frameworks, write and retrieval
support are common, but conflict handling, staleness detection, contamination tracking, and evidence-aware verification
remain much less developed.
Synthesis: memory usefulness versus memory accountability. Compression, consolidation, and persistence make
memory useful; lineage, validity, conflict tracking, and influence links make it governable. A provenance-bearing
memory system must support both.

6     Benchmarks, Datasets, and Metrics
Evaluation is central to evidence tracing and execution provenance. Beyond final-answer correctness, provenance-aware
agent evaluation must assess evidence support, tool-call justification, unsafe influence, trace completeness, failure
localization, and recovery. Existing benchmarks provide partial views across RAG attribution, citation evaluation, agent
execution, tool-use safety, memory, and multi-agent analysis, but few evaluate complete provenance across evidence,
tools, memory, traces, safety, and recovery. This section summarizes representative benchmark families, metrics, and
limitations.
To provide a high-level view of these gaps, Figure 5 summarizes the coverage of major benchmark families across
provenance-related evaluation capabilities.
The heatmap shows that existing benchmark families tend to specialize in one or two dimensions, such as evidence
grounding, tool use, memory, multi-agent interaction, or safety attacks. This motivates the more detailed discussion of
benchmark families below.

6.1    Benchmark Families for Evidence Tracing

RAG and attribution benchmarks provide the closest foundation for evidence tracing because they evaluate whether
generated outputs are grounded in retrieved or cited evidence [Gao et al., 2023, Es et al., 2024, Saad-Falcon et al.,
2024, Min et al., 2023, Niu et al., 2024, Ru et al., 2024, Wu et al., 2025]. These benchmarks generally focus on the
relationship between a final answer and its supporting sources, rather than the full execution trajectory of an agent.


                                                                           15
                                                   From Agent Traces to Trust



        Benchmark                Evidence         Tool         Memory          Multi-        Safety       Provenance      Recovery
          Family                  Labels          Calls                        agent         Attacks       Relations

 RAG benchmarks                      S              L              L             L              P              P              L
 Tool-use benchmarks                 L              S              L             P              P              P              L
 Memory benchmarks                   P              L              S             L              P              P              P
 Multi-agent benchmarks              L              P              L              S             P              P              L
 Trace-debugging
                                     P              P              P             P              L              P              P
 benchmarks
 Provenance/security
                                     P              S              P             P              S              S              P
 benchmarks

  Legend: S Strong coverage         P Partial coverage     L Limited or absent coverage. Rating criteria: a capability is rated S
  when it is a primary evaluation target with dedicated labels or metrics, P when it is supported only indirectly or for a subset of
  cases, and L when it is largely absent.
   Key gap. Existing benchmarks cover important but isolated aspects of agent provenance. No benchmark family provides
   strong end-to-end coverage across evidence labels, tool calls, memory, multi-agent communication, safety attacks,
   provenance relations, and recovery.

Figure 5: Benchmark coverage heatmap across provenance-related evaluation capabilities. The heatmap summarizes
benchmark families at a high level rather than listing individual datasets. It highlights that existing benchmarks provide
partial coverage of isolated components, while full-stack evaluation of evidence tracing and execution provenance
remains underdeveloped.


Nevertheless, they provide important metrics and datasets for evaluating evidence recall, citation quality, faithfulness,
and claim-level support.
At the answer level, ALCE treats citations as explicit links between answer spans and external sources and checks
whether those citations support the generated content, while RAGAS and ARES score reference-free faithfulness,
context relevance, and answer relevance using lightweight model judges [Gao et al., 2023, Es et al., 2024, Saad-Falcon
et al., 2024]. These frameworks share one assumption—that an answer should be supported by retrieved evidence—but
evaluate it only at the answer or context level, not per claim.
Finer-grained benchmarks move toward claim-level provenance, differing mainly in the unit they score: retrieval-
versus-generation error separation (RAGChecker), word-level hallucination annotation (RAGTruth), atomic-fact support
(FActScore), source-supportiveness of cited references (SourceCheckup), and supported/refuted/unverifiable claim
classification (FEVER) [Ru et al., 2024, Niu et al., 2024, Min et al., 2023, Wu et al., 2025, Thorne et al., 2018]. The
trend is a shift from answer-level to claim-level grounding; SourceCheckup sharpens the point by showing that citation
presence does not imply evidence support.
These benchmarks are important for evidence tracing, but they remain limited from an agent-provenance perspective.
Their primary evaluation targets are answer-source grounding, citation support, faithfulness, hallucination annotation,
or claim-level factual support [Gao et al., 2023, Es et al., 2024, Saad-Falcon et al., 2024, Min et al., 2023, Niu et al.,
2024, Ru et al., 2024, Wu et al., 2025]. As a result, they provide only partial coverage of agent provenance: they help
evaluate whether claims are supported by evidence, but they do not directly evaluate how tool calls, memory operations,
environment observations, intermediate decisions, or multi-agent communication shape the final answer or action.
Thus, they should be viewed as foundations for evidence attribution rather than complete benchmarks for execution
provenance.

6.2   Benchmarks for Agent Execution Traces and Tool-Use Safety

Agent benchmarks extend evaluation from static answer generation to interactive, multi-step execution, exposing
trajectories, tool calls, environment states, and intermediate decisions. They differ mainly in setting and in what
they score: multi-environment capability (AgentBench), long-horizon web interaction (WebArena), API selection and
execution paths (ToolBench/ToolLLM), and tool-agent-user workflows that grade policy following and final database
state rather than only the final response (τ -bench) [Liu et al., 2024, Zhou et al., 2024, Qin et al., 2024, Yao et al., 2025].
The common trend is a move from scoring the answer toward scoring the process and its end state.


                                                                 16
                                              From Agent Traces to Trust


Trace-oriented benchmarks connect execution provenance to failure diagnosis. AgentTrace provides structured oper-
ational, cognitive, and contextual logs for agent observability and downstream audit [AlSayyad et al., 2026], while
TRAIL uses human-annotated traces to evaluate whether systems can localize failures to specific steps, components, or
interactions [Deshpande et al., 2025]. Recent multi-agent work moves further from trace inspection to explicit failure
attribution: AgenTracer constructs TracerTraj through counterfactual replay and fault injection to identify responsible
agents and steps [Zhang et al., 2026], and Aegis generates positive–negative trajectory pairs with faulty-agent and
error-mode labels [Kong et al., 2025]. Together, these works show that provenance can be evaluated not only by trace
completeness, but also by its ability to support failure localization and attribution.
Tool-use safety benchmarks examine whether agents remain safe when tools introduce external risks. ToolEmu
evaluates high-risk tool use in an LM-emulated sandbox [Ruan et al., 2024]; InjecAgent and AgentDojo study indirect
prompt injection and adversarial tool interactions in tool-integrated settings [Zhan et al., 2024, Debenedetti et al.,
2024]; and OpenAgentSafety extends evaluation to real tools and multi-turn, multi-user tasks across multiple risk
categories [Vijayvargiya et al., 2026]. MCP-SafetyBench further studies safety risks in real MCP servers and multi-
server workflows [Zong et al., 2026]. These benchmarks matter for provenance because unsafe behavior often depends
on hidden flows from untrusted sources into tool arguments, execution boundaries, or state-changing actions.
Recent work evaluates more explicit execution-provenance and information-flow mechanisms. Agent-Sentry introduces
execution provenance graphs to bound LLM-agent behavior and detect out-of-bounds tool calls [Sequeira et al., 2026].
NeuroTaint and TaintBench evaluate semantic taint and source-to-sink influence in LLM agents, emphasizing that
unsafe influence may be transformed through summarization, inference, or memory rather than copied verbatim [Cai
et al., 2026]. Fides applies information-flow control to secure AI agents by tracking confidentiality and integrity
labels [Costa et al., 2025]. AgentSpec evaluates runtime policy enforcement through customizable constraints [Wang
et al., 2026]. AgentBound extends this line of work to execution boundaries and access control in MCP-style agent-tool
ecosystems [Bühler et al., 2026]. Together, these benchmarks and systems shift evaluation from “can the agent use
tools?” to “can the agent use tools safely, with traceable and enforceable provenance?”

6.3   Memory and Multi-Agent Provenance Evaluation

Memory and multi-agent settings introduce additional provenance challenges because information may persist across
sessions, be updated over time, or propagate across agents. Existing memory benchmarks and systems mainly evaluate
recall, personalization, long-term consistency, memory updating, retrieval, or multi-session task performance [Zhong
et al., 2024, Packer et al., 2023, Xu et al., 2026, Chhikara et al., 2025, Maharana et al., 2024, He et al., 2026].
MemoryBank evaluates long-term memory recall, continuous updating, and personalization [Zhong et al., 2024];
MemGPT makes memory read and write operations explicit through hierarchical memory management [Packer et al.,
2023]; A-MEM organizes agent memory through dynamically evolving interconnected memory structures [Xu et al.,
2026]; Mem0 evaluates memory extraction, consolidation, and retrieval in multi-session dialogue settings [Chhikara
et al., 2025]; LOCOMO evaluates long-term conversational memory [Maharana et al., 2024]; and MemoryArena
evaluates memory use in interdependent multi-session agentic tasks [He et al., 2026]. Existing memory and graph-
memory surveys further summarize progress in memory mechanisms, evaluation protocols, and graph-based memory
systems [Zhang et al., 2025, Du, 2026, Yang et al., 2026].
From a provenance perspective, these benchmarks provide useful but incomplete proxies for memory provenance. They
often test whether an agent remembers useful information, but rarely evaluate whether a memory item is traceable
to its source, temporally valid, consistent with newer evidence, protected from contamination, or responsible for a
downstream action. Dedicated memory-provenance evaluation should therefore assess memory source attribution,
update history, conflict resolution, stale-memory invalidation, contamination detection, and downstream influence,
which remain underdeveloped in current memory evaluation protocols [Maharana et al., 2024, He et al., 2026, Zhang
et al., 2025, Du, 2026].
Multi-agent systems introduce another layer of provenance complexity because evidence, assumptions, messages, and
errors can propagate across agent boundaries. AutoGen and CAMEL provide representative frameworks for multi-agent
communication, role assignment, and collaborative task solving [Wu et al., 2024, Li et al., 2023]. Evaluating provenance
in such settings requires more than measuring final task success: it requires identifying which agent contributed which
evidence, which communication step introduced an error, and how responsibility is distributed across agents. MAST
analyzes failures from specification errors, inter-agent misalignment, and weak task verification [Cemri et al., 2026],
while TRAIL evaluates issue localization from agent traces [Deshpande et al., 2025]. AgenTracer and Aegis further
construct labeled multi-agent trajectories for identifying faulty agents, responsible steps, and error modes [Zhang et al.,
2026, Kong et al., 2025]. Together, these works suggest that multi-agent provenance benchmarks should evaluate
evidence propagation, communication-level error introduction, cross-agent dependency, and responsibility attribution,
rather than only final coordination success.


                                                           17
                                              From Agent Traces to Trust


Table 6: Representative metric dimensions for evaluating evidence tracing and execution provenance in LLM agents.
The Status column flags maturity: Established metrics are operationalized in existing RAG, attribution, tool-use, or
safety benchmarks; Partly established metrics exist for some sub-tasks (e.g., failure localization in TRAIL/MAST)
but not for recovery; Proposed metrics (trace completeness, provenance accuracy, dependency coverage, temporal
consistency) are desiderata that are not yet operationalized with agreed definitions, and we mark them as such to avoid
conflating them with mature measures.

Evaluation As- Core Question                   Representative Metrics              Status           Related Basis
pect
Evidence attribu- Are the agent’s claims sup- Evidence recall, citation precision, Established      RAG and attribution
tion              ported by reliable evidence? source supportiveness, faithfulness,                 evaluation [Gao et al.,
                                               claim support accuracy.                              2023, Min et al.,
                                                                                                    2023, Niu et al., 2024,
                                                                                                    Ru et al., 2024, Wu
                                                                                                    et al., 2025].
Execution prove- Is the agent’s execution pro- Trace completeness, provenance ac- Proposed          Provenance standards
nance            cess completely and cor- curacy, dependency coverage, tem-                         and agent observabil-
                 rectly traceable?             poral consistency.                                   ity [World Wide Web
                                                                                                    Consortium, 2013,
                                                                                                    Dong et al., 2024,
                                                                                                    AlSayyad et al., 2026,
                                                                                                    Souza et al., 2025].
Safety and robust- Can the system detect un- Unsafe influence detection, attack Established         Tool-use        safety,
ness               safe or untrusted influence success rate, policy violation rate,                 prompt       injection,
                   during execution?           intervention precision.                              and information-flow
                                                                                                    control [Ruan et al.,
                                                                                                    2024, Zhan et al.,
                                                                                                    2024, Debenedetti
                                                                                                    et al., 2024, 2026,
                                                                                                    Costa et al., 2025,
                                                                                                    Zong et al., 2026].
Debugging and Can traces help identify and Failure localization accuracy, diag- Partly       estab- Trace-based debug-
recovery      repair failures?             nosis correctness, auditability, re- lished              ging,     multi-agent
                                           covery success.                                          failure analysis, and
                                                                                                    failure-attribution
                                                                                                    datasets [Deshpande
                                                                                                    et al., 2025, Cemri
                                                                                                    et al., 2026, Al-
                                                                                                    Sayyad et al., 2026,
                                                                                                    Zhang et al., 2026,
                                                                                                    Kong et al., 2025].



6.4   Metrics for Evidence Tracing and Execution Provenance

Existing benchmarks use diverse metrics for retrieval grounding, citation quality, tool use, safety, memory, and agent
execution [Gao et al., 2023, Min et al., 2023, Ru et al., 2024, Wu et al., 2025, Ruan et al., 2024, Debenedetti et al.,
2024, Maharana et al., 2024, Deshpande et al., 2025, Cemri et al., 2026]. From the perspective of evidence tracing and
execution provenance, these metrics can be reorganized into four evaluation aspects: evidence attribution, execution
provenance, safety and robustness, and debugging and recovery. Table 6 summarizes representative metric dimensions
and their related foundations. Some metrics are already used in RAG, attribution, tool-use, and agent benchmarks,
while others are natural extensions for provenance-aware evaluation.
The table highlights that provenance-aware evaluation should go beyond final-answer correctness and component-level
task success. Building on prior work in attribution evaluation, provenance modeling, agent observability, tool-use safety,
and trace-based debugging [Gao et al., 2023, Min et al., 2023, Ru et al., 2024, World Wide Web Consortium, 2013,
Dong et al., 2024, AlSayyad et al., 2026, Souza et al., 2025, Ruan et al., 2024, Debenedetti et al., 2024, Deshpande
et al., 2025, Cemri et al., 2026], we organize these metrics by their evaluation function. Evidence attribution metrics
assess claim grounding; execution-provenance metrics assess traceability; safety and robustness metrics assess unsafe


                                                           18
                                              From Agent Traces to Trust


influence and policy violations; and debugging and recovery metrics assess whether traces support failure localization,
audit, and repair. Together, these dimensions provide a broader evaluation view for agents whose outputs depend on
retrieval, tools, memory, communication, and external state changes.

6.5   Limitations of Current Evaluation Protocols

Existing benchmarks provide useful foundations for evaluating retrieval grounding, tool use, memory, web interaction,
safety, and multi-agent behavior, but they remain insufficient for full evidence tracing and execution provenance. RAG
and attribution benchmarks mainly focus on answer-source grounding or citation quality [Gao et al., 2023, Ru et al.,
2024, Wu et al., 2025]. Tool-use and agent benchmarks emphasize task success, unsafe tool behavior, prompt injection,
environment interaction, real-world tool safety, or MCP-specific attacks [Liu et al., 2024, Zhou et al., 2024, Ruan et al.,
2024, Debenedetti et al., 2024, Yao et al., 2025, Vijayvargiya et al., 2026, Zong et al., 2026]. Memory and multi-agent
benchmarks evaluate recall, personalization, coordination, failure modes, or error attribution [Maharana et al., 2024,
He et al., 2026, Deshpande et al., 2025, Cemri et al., 2026, Zhang et al., 2026, Kong et al., 2025]. Although recent
work has improved realistic tool-safety evaluation and multi-agent failure attribution, existing benchmarks still rarely
evaluate the complete provenance chain from evidence and tool outputs to memory updates, intermediate claims, final
answers, external state changes, and recovery actions.
A key limitation is the lack of unified execution traces and provenance-relation annotations. Trace-oriented benchmarks
and observability frameworks have made useful progress, but they still differ in what artifacts they record and how
provenance is represented [Dong et al., 2024, AlSayyad et al., 2026, Souza et al., 2025, Deshpande et al., 2025, Cemri
et al., 2026]. Few benchmarks jointly capture user requests, retrieved evidence, tool calls and outputs, memory reads and
writes, inter-agent messages, intermediate claims, final responses, and state changes. Even fewer annotate relations such
as S UPPORT, C ONTRADICT, D EPEND - ON, U PDATE, and I NVALIDATE, despite the availability of general provenance
concepts in standards such as W3C PROV-DM [World Wide Web Consortium, 2013]. As a result, current evaluation
often measures correctness, faithfulness, or attack success indirectly, rather than directly assessing trace completeness,
provenance accuracy, claim support, memory validity, or cross-agent responsibility.
Recovery and governance are also under-evaluated. Existing benchmarks commonly test whether an agent succeeds,
fails, hallucinates, or takes an unsafe action, but rarely evaluate whether provenance can help the system repair
execution, such as by invalidating stale memory, quarantining contaminated evidence, retrying a tool call, requesting
human approval, or rolling back an unsafe state change [Ruan et al., 2024, Debenedetti et al., 2024, Deshpande et al.,
2025, Cemri et al., 2026]. Realistic evaluation is further complicated by long-horizon and enterprise traces involving
private tools, changing data, user-specific memory, organizational policies, credentials, and confidential intermediate
states [Maharana et al., 2024, He et al., 2026, Dong et al., 2024, AlSayyad et al., 2026]. Future provenance benchmarks
should therefore evaluate not only whether agents succeed, but also whether their behavior is traceable, auditable, safe,
privacy-aware, and recoverable [Costa et al., 2025].
Table 7 summarizes representative benchmarks and datasets according to their task type, trace availability, evidence
labels, tool calls, memory, multi-agent setting, safety attacks, and main metrics.


7     Open Problems and Future Directions

Despite progress in RAG attribution, agent observability, tool-use safety, memory systems, graph-based representation,
debugging, and multi-agent evaluation, evidence tracing and execution provenance for LLM agents remain fragmented.
Many existing systems record execution artifacts, but they rarely explain how evidence, tools, memory, observations,
messages, and actions jointly shape an agent’s final answer or external behavior. This section outlines open problems
toward provenance-aware agents that support verification, audit, attribution, runtime safety, recovery, and governance.

7.1   Toward Unified and Interoperable Trace Schemas

A central open problem is the lack of unified trace schemas for LLM agents. Existing frameworks and benchmarks
record different artifacts, including prompts, model responses, tool calls, retrieved documents, memory operations,
environment observations, execution metadata, and error events [Dong et al., 2024, AlSayyad et al., 2026, Souza et al.,
2025, Deshpande et al., 2025, Cemri et al., 2026]. However, few schemas jointly represent reasoning steps, retrieval,
tool calls and outputs, memory reads and writes, inter-agent messages, intermediate claims, final responses, and external
state changes.
Existing standards provide useful building blocks but do not fully solve the agent-provenance problem. W3C PROV-DM
offers a general vocabulary for entities, activities, agents, and derivation relations [World Wide Web Consortium, 2013];


                                                           19
                                                                 From Agent Traces to Trust


Table 7: Benchmarks for evidence tracing and execution provenance. Existing benchmarks cover different parts of
the provenance problem, including citation quality, RAG faithfulness, agent execution traces, tool-use safety, memory
evaluation, and multi-agent failure analysis. However, few benchmarks jointly provide evidence labels, tool calls,
memory operations, multi-agent communication, safety perturbations, and provenance-relation annotations.
Benchmark                  Task Type                  Trace Avail- Evidence   La- Tool Calls?   Memory?       Multi-Agent? Safety    At- Main Metrics
                                                      able?        bels?                                                   tacks?
ALCE [Gao et al., 2023]    Citation generation        Partial     Yes             No            No            No           No           Citation quality, correctness, flu-
                                                                                                                                        ency
RAGAS [Es et al., 2024]    RAG evaluation             No          Partial         No            No            No           No           Faithfulness, context relevance, an-
                                                                                                                                        swer relevance
ARES [Saad-Falcon et al., RAG evaluation                No        Partial         No            No            No           No           Context relevance, answer faithful-
2024]                                                                                                                                   ness, answer relevance
RAGChecker [Ru et al., Fine-grained RAG diagnosis Partial         Partial         No            No            No           No           Retrieval and generation diagnosis
2024]
RAGTruth [Niu et al., 2024] RAG hallucination annota- Partial     Yes             No            No            No           No           Word-level hallucination labels
                            tion
FActScore [Min et al., Atomic factuality                No        Yes             No            No            No           No           Atomic fact support
2023]
SourceCheckup [Wu et al., Source supportiveness         No        Yes             No            No            No           No           Source relevance and supportive-
2025]                                                                                                                                   ness
AgentBench [Liu et al., Agent capability evaluation Partial       No              Partial       Task-         No           No           Task success, environment-specific
2024]                                                                                           dependent                               scores
WebArena [Zhou et al., Web-agent execution              Yes       No              Yes           No            No           No           Task success, web interaction out-
2024]                                                                                                                                   come
ToolBench / ToolLLM [Qin API tool use                   Yes       No              Yes           No            No           No           Tool selection, argument correct-
et al., 2024]                                                                                                                           ness, execution success
τ -bench [Yao et al., 2025] Tool-agent-user interaction Yes       No              Yes           State-based   No           Partial      Task success, policy following, fi-
                                                                                                                                        nal state
TRAIL [Deshpande et al., Trace debugging               Yes        Partial         Partial       Partial       Partial      No           Issue localization, error type diag-
2025]                                                                                                                                   nosis
MAST [Cemri et al., 2026] Multi-agent failure analysis Yes        No              Task-         Task-         Yes          No           Failure taxonomy, error attribution
                                                                                  dependent     dependent
ToolEmu [Ruan et al., 2024] Tool-use risk evaluation Yes          No              Yes           No            No           Yes          Risk detection, unsafe action rate
InjecAgent [Zhan et al., Indirect prompt injection   Yes          No              Yes           No            No           Yes          Attack success rate, defense perfor-
2024]                                                                                                                                   mance
AgentDojo [Debenedetti Prompt injection attacks and Yes           No              Yes           No            No           Yes          Attack success, utility, defense ro-
et al., 2024]                defenses                                                                                                   bustness
Agent-Sentry Bench [Se- Out-of-bounds tool execu- Yes             Partial         Yes           No            No           Yes          Out-of-bounds detection, false pos-
queira et al., 2026]         tion                                                                                                       itives
NeuroTaint        /   Taint- Semantic taint tracking Yes          Partial         Yes           Yes           Partial      Yes          Unsafe influence detection, taint
Bench [Cai et al., 2026]                                                                                                                propagation
AgentBound [Bühler et al., MCP execution boundary    Yes          No              Yes           No            No           Yes          Access-control violations, policy
2026]                                                                                                                                   enforcement
LOCOMO [Maharana et al., Long-term conversational Partial         Partial         No            Yes           No           No           Long-range QA, event summariza-
2024]                        memory                                                                                                     tion, memory recall
MemoryArena [He et al., Multi-session agent memory Yes            Partial         Task-         Yes           No           No           Multi-session task success, mem-
2026]                                                                             dependent                                             ory use




OpenTelemetry and OpenLineage provide abstractions for distributed traces and data workflow lineage [OpenTelemetry,
2026, OpenLineage Contributors, 2026]; and PROV-AGENT adapts provenance modeling to agentic workflows [Souza
et al., 2025]. Future schemas should connect these operational trace structures with semantic evidence relations. They
should represent claims, evidence units, tool observations, memory items, environment states, and agent messages,
together with relations such as S UPPORT, C ONTRADICT, D EPEND - ON, U PDATE, and I NVALIDATE. Such schemas
would make agent traces easier to compare, replay, annotate, audit, and exchange across frameworks.


7.2    Claim-Level and Semantic Provenance

Current attribution methods often operate at coarse granularity, such as answer-level citation, context-level faithfulness,
or step-level logging [Gao et al., 2023, Ru et al., 2024, Wu et al., 2025, Schreieder et al., 2026]. However, agent
outputs frequently contain multiple claims, intermediate assumptions, and action-relevant inferences. A final response
may be partially correct: one claim may be supported by retrieved evidence, another may be inferred beyond the
source, and another may be contradicted by a tool output or memory item. This motivates claim-level provenance,
building on fine-grained factuality and attribution work such as ALCE, FActScore, RAGTruth, RAGChecker, and
SourceCheckup [Gao et al., 2023, Min et al., 2023, Niu et al., 2024, Ru et al., 2024, Wu et al., 2025].
For agents, the harder problem is semantic provenance across transformations. Evidence may be paraphrased, summa-
rized, aggregated, compressed into memory, passed through tools, or reused by another agent before influencing a claim
or action. String-level matching and citation presence are therefore insufficient. Future work should trace semantic
dependencies across retrieval, tool outputs, memory updates, reflection, and inter-agent communication, including cases
where evidence is indirectly used or transformed across multiple steps. Work on semantic taint and causal influence
points toward this direction, but robust claim-level provenance for long agent executions remains open [Cai et al., 2026].


                                                                                   20
                                              From Agent Traces to Trust


7.3   Memory and Multi-Agent Provenance

Memory provenance remains underdeveloped. Long-term memory systems allow agents to store, retrieve, update,
and reuse information across sessions, but they often provide limited support for tracing where memory items came
from, whether they remain valid, whether they conflict with newer evidence, and how they influence later claims or
actions. Existing memory and graph-memory surveys cover architectures, evaluation methods, and relational memory
structures [Zhang et al., 2025, Du, 2026, Yang et al., 2026], but memory as provenance-bearing evidence remains a
distinct open problem.
Future memory systems should attach provenance metadata to memory items, including source attribution, write time,
update history, retrieval context, downstream usage, conflict status, and invalidation events. Memory should not be
treated as an unqualified context reservoir: a memory item derived from user input, retrieved evidence, a tool output,
an environment observation, a reflection, or another agent message should carry different trust implications. This is
especially important when memory affects tool calls, personalization, or long-term decisions. Memory poisoning and
memory-injection attacks further show that compromised memory can influence future behavior without modifying
model weights [Chen et al., 2024, Dong et al., 2025].
Multi-agent provenance introduces additional complexity because agents may communicate, delegate tasks, verify one
another’s outputs, and jointly produce final decisions. Frameworks such as AutoGen and CAMEL demonstrate these
distributed workflows [Wu et al., 2024, Li et al., 2023], while MAST shows that failures can arise from specification
errors, inter-agent misalignment, weak verification, and coordination breakdowns [Cemri et al., 2026]. AgenTracer
and Aegis further show that responsible-agent and responsible-step attribution can be operationalized through labeled,
counterfactual, or contrastive multi-agent trajectories [Zhang et al., 2026, Kong et al., 2025]. Future provenance models
should therefore track how claims, evidence, messages, and errors propagate across agents: which agent introduced a
claim, which agent verified or reused it, which message carried it, which step induced failure, and where responsibility
lies. The remaining challenge is to integrate responsibility attribution with claim-level evidence provenance, memory
lineage, and recovery actions, rather than treating failure attribution as a separate diagnostic task.

7.4   Runtime Safety, Enforcement, and Recovery

Runtime safety for LLM agents requires more than output filtering. In tool-using agents, dangerous behavior may
arise when untrusted content influences tool arguments, when private information flows into public outputs, when
stale memory affects a privileged action, or when an agent invokes a tool outside its intended boundary. Guardrails
that inspect only the final answer or the current tool call may miss these source-to-sink dependencies. Provenance-
aware guardrails should reason over the evidence, memory items, tool outputs, observations, and external content that
influenced a proposed action [Zhan et al., 2024, Debenedetti et al., 2024, 2026, Costa et al., 2025, Sequeira et al., 2026,
Bühler et al., 2026].
Recent work points toward provenance-aware enforcement through prompt-injection benchmarks, control/data-flow
separation, information-flow control, semantic taint tracking, runtime constraints, execution provenance graphs, and
access boundaries [Ruan et al., 2024, Zhan et al., 2024, Debenedetti et al., 2024, 2026, Costa et al., 2025, Cai et al.,
2026, Wang et al., 2026, Sequeira et al., 2026, Bühler et al., 2026]. The remaining challenge is recovery. Most systems
focus on detecting or blocking unsafe behavior, but trustworthy agents also need to repair unsupported or unsafe
executions. Future systems should use provenance to invalidate stale memory, quarantine contaminated evidence, retry
tool calls with corrected parameters, request human approval, roll back unsafe state changes, or replay execution from
safe checkpoints. This requires provenance representations that support intervention and recovery, not only explanation.

7.5   Realistic Benchmarks, Privacy, and Governance

Current benchmarks still lack realistic full execution traces. RAG benchmarks provide evidence labels but usually omit
tools and memory; tool-use safety benchmarks provide attacks and tool calls but often lack claim-level evidence labels;
memory benchmarks evaluate recall or personalization but rarely evaluate lineage, conflict handling, or downstream
influence; and multi-agent benchmarks analyze failures but often lack complete provenance annotations. Benchmarks
such as AgentBench, WebArena, τ -bench, TRAIL, MAST, LOCOMO, and MemoryArena provide important founda-
tions for agent evaluation, trace analysis, multi-agent failure diagnosis, and long-term memory assessment [Liu et al.,
2024, Zhou et al., 2024, Yao et al., 2025, Deshpande et al., 2025, Cemri et al., 2026, Maharana et al., 2024, He et al.,
2026]. However, no benchmark family fully evaluates evidence tracing and execution provenance across retrieval, tool
use, memory, multi-agent communication, safety attacks, and recovery.
Future benchmarks should move from isolated answer-, task-, or attack-level evaluation toward trace-level evaluation.
Provenance standards such as W3C PROV-DM provide a useful vocabulary for representing entities, activities, agents,


                                                           21
                                              From Agent Traces to Trust


and derivation relations [World Wide Web Consortium, 2013]. Agent observability frameworks such as AgentOps and
AgentTrace show how agent executions can be collected and inspected as structured traces [Dong et al., 2024, AlSayyad
et al., 2026]. PROV-AGENT further adapts provenance modeling to agentic workflows [Souza et al., 2025]. Building
on these foundations, future benchmarks should capture complete execution traces across agent workflows and annotate
the provenance relations needed to evaluate evidence support, unsafe influence, responsibility attribution, and recovery.
Existing work highlights different parts of this agenda. TRAIL shows how execution traces can support failure analysis
in agent workflows [Deshpande et al., 2025]. MAST focuses on diagnosing failure modes in multi-agent systems [Cemri
et al., 2026]. AgenTracer studies responsible-agent attribution from multi-agent trajectories [Zhang et al., 2026].
Aegis further examines responsible-step attribution through contrastive or counterfactual multi-agent traces [Kong
et al., 2025]. OpenAgentSafety emphasizes realistic tool-use safety risks in open agent settings [Vijayvargiya et al.,
2026]. MCPSafetyBench extends safety evaluation to protocol-level agent-tool environments [Zong et al., 2026]. The
remaining challenge is to integrate these dimensions into benchmarks that jointly test claim-level evidence support,
memory validity, unsafe influence detection, auditability, and recovery.
Privacy and governance introduce a separate but equally important challenge. Provenance traces may contain sensitive
user data, confidential documents, credentials, tool outputs, API arguments, internal reasoning artifacts, and long-term
memory items. Observability frameworks such as AgentOps and AgentTrace provide useful foundations for collecting
and inspecting traces [Dong et al., 2024, AlSayyad et al., 2026], while security mechanisms such as Fides highlight
the need to track confidentiality and integrity constraints in agent workflows [Costa et al., 2025]. Future provenance
infrastructure should therefore support trace minimization, access control, anonymization, retention policies, encryption,
and selective disclosure. Without privacy-aware governance, provenance infrastructure itself may become a source of
compliance and security risk.
Overall, provenance-aware agents require more than richer logs. They require interoperable schemas, semantic claim-
level attribution, memory and multi-agent lineage, runtime enforcement with recovery, and benchmarks that evaluate
traceability, auditability, safety, privacy, and recoverability as first-class capabilities.

8   Conclusion
LLM agents are moving beyond isolated text generation toward systems that retrieve evidence, plan intermediate
steps, invoke tools, update memory, interact with environments, and coordinate with other agents. This shift makes
final-answer correctness insufficient for trustworthiness: reliable agent systems must also expose where answers come
from, which evidence supports them, how tools and intermediate actions contribute to them, and where failures or
unsafe influences enter the execution process. This survey positions evidence tracing and execution provenance as a
unified perspective for studying these questions across the agent lifecycle. We reviewed key provenance representations,
including structured logs, execution graphs, evidence graphs, tool dependency graphs, memory provenance, and
multi-agent communication traces, and discussed their roles in attribution, debugging, verification, safety enforcement,
evaluation, and recovery.
Our review shows that the field has made important progress, but remains fragmented. Existing systems often record
sources or tool calls, yet they rarely provide fine-grained claim-level support, semantic influence tracking, memory
lineage, cross-agent provenance propagation, or robust tracing under adversarial conditions. Looking forward, evidence
tracing and execution provenance should become a first-class infrastructure layer for reliable agent systems. We hope
this survey helps consolidate this emerging research space and motivates the development of traceable, auditable, and
recoverable LLM agents.

References
Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Eric Hambro, Luke Zettlemoyer,
  Nicola Cancedda, and Thomas Scialom. Toolformer: Language models can teach themselves to use tools. Advances
  in neural information processing systems, 36:68539–68551, 2023.
Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. ReAct: Synergizing
  reasoning and acting in language models. In International Conference on Learning Representations, 2023. URL
  https://openreview.net/forum?id=WE_vluYUL-X.
Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion:
  Language agents with verbal reinforcement learning. In Advances in Neural Information Processing Systems, 2023.
  URL https://openreview.net/forum?id=vAElhFcKW6.
Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang, Bill
  Qian, Sihan Zhao, Lauren Hong, Runchu Tian, Ruobing Xie, Jie Zhou, Mark Gerstein, Dahai Li, Zhiyuan Liu, and


                                                           22
                                            From Agent Traces to Trust


  Maosong Sun. ToolLLM: Facilitating large language models to master 16000+ real-world APIs. In International
  Conference on Learning Representations, 2024. URL https://openreview.net/forum?id=dHng2O0Jjr.
Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen Men, Kejuan
  Yang, Shudan Zhang, Xiang Deng, Aohan Zeng, Zhengxiao Du, Chenhui Zhang, Sheng Shen, Tianjun Zhang, Yu Su,
  Huan Sun, Minlie Huang, Yuxiao Dong, and Jie Tang. Agentbench: Evaluating llms as agents. In International
  Conference on Learning Representations, 2024. URL https://openreview.net/forum?id=zAdUB0aCTQ.
Shuyan Zhou, Frank F. Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue Ou, Yonatan
  Bisk, Daniel Fried, Uri Alon, and Graham Neubig. Webarena: A realistic web environment for building autonomous
  agents. In International Conference on Learning Representations, 2024. URL https://openreview.net/forum?
  id=oKn9c6ytLx.
Shunyu Yao, Noah Shinn, Parth Razavi, and Karthik Narasimhan. τ -bench: A benchmark for tool-agent-user interaction
  in real-world domains. In International Conference on Learning Representations, 2025. URL https://openreview.
  net/forum?id=roNSXZpUDN.
Yangjun Ruan, Honghua Dong, Andrew Wang, Silviu Pitis, Yongchao Zhou, Jimmy Ba, Yann Dubois, Chris J. Maddison,
  and Tatsunori Hashimoto. Identifying the risks of lm agents with an lm-emulated sandbox. In International Conference
  on Learning Representations, 2024. URL https://openreview.net/forum?id=GEcwtMk1uA.
Edoardo Debenedetti, Jie Zhang, Mislav Balunovic, Luca Beurer-Kellner, Marc Fischer, and Florian Tramèr. Agentdojo:
  A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents. In Advances in Neural
  Information Processing Systems, 2024. URL https://openreview.net/forum?id=m1YYAQjO3w.
Sanidhya Vijayvargiya, Aditya Bharat Soni, Xuhui Zhou, Zora Zhiruo Wang, Nouha Dziri, Graham Neubig, and Maarten
  Sap. OpenAgentSafety: A comprehensive framework for evaluating real-world AI agent safety. In International
  Conference on Learning Representations, 2026.
Xuanjun Zong, Zhiqi Shen, Lei Wang, Yunshi Lan, and Chao Yang. MCP-SafetyBench: A benchmark for safety
  evaluation of large language models with real-world MCP servers. In International Conference on Learning
 Representations (ICLR), 2026. arXiv:2512.15163.
Darshan Deshpande, Varun Gangal, Hersh Mehta, Jitin Krishnan, Anand Kannappan, and Rebecca Qian. TRAIL: Trace
  reasoning and agentic issue localization. arXiv preprint arXiv:2505.08638, 2025. URL https://arxiv.org/abs/
  2505.08638.
Mert Cemri, Melissa Z Pan, Shuyi Yang, Lakshya A Agrawal, Bhavya Chopra, Rishabh Tiwari, Kurt Keutzer, Aditya
 Parameswaran, Dan Klein, Kannan Ramchandran, et al. Why do multi-agent llm systems fail? Advances in Neural
 Information Processing Systems, 38, 2026.
Guibin Zhang, Junhao Wang, Junjie Chen, Wangchunshu Zhou, Kun Wang, and Shuicheng Yan. AgenTracer: Who is
  inducing failure in the LLM agentic systems? In International Conference on Learning Representations (ICLR),
  2026. arXiv:2509.03312.
Fanqi Kong, Ruijie Zhang, Huaxiao Yin, Guibin Zhang, Xiaofei Zhang, Ziang Chen, Zhaowei Zhang, Xiaoyuan Zhang,
  Song-Chun Zhu, and Xue Feng. Aegis: Automated error generation and attribution for multi-agent systems. arXiv
  preprint arXiv:2509.14295, 2025.
World Wide Web Consortium. PROV-DM: The PROV data model. W3C Recommendation, 2013. URL https:
 //www.w3.org/TR/prov-dm/.
OpenTelemetry. Opentelemetry specification: Traces. Online documentation, 2026. URL https://opentelemetry.
  io/docs/specs/otel/.
Liming Dong, Qinghua Lu, and Liming Zhu. AgentOps: Enabling observability of LLM agents. arXiv preprint
  arXiv:2411.05285, 2024. URL https://arxiv.org/abs/2411.05285.
Adam AlSayyad, Kelvin Yuxiang Huang, and Richik Pal. Agenttrace: A structured logging framework for agent system
  observability. arXiv preprint arXiv:2602.10133, 2026. URL https://arxiv.org/abs/2602.10133. Poster,
  AAAI 2026 TrustAgent Workshop (non-archival).
Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang,
  Jiale Liu, et al. AutoGen: Enabling next-gen LLM applications via multi-agent conversations. In First conference on
  language modeling, 2024.
Tianyu Gao, Howard Yen, Jiatong Yu, and Danqi Chen. Enabling large language models to generate text with citations.
  In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pages 6465–6488,
  Singapore, 2023. Association for Computational Linguistics. doi:10.18653/v1/2023.emnlp-main.398.


                                                         23
                                            From Agent Traces to Trust


Sewon Min, Kalpesh Krishna, Xinxi Lyu, Mike Lewis, Wen-tau Yih, Pang Wei Koh, Mohit Iyyer, Luke Zettlemoyer, and
  Hannaneh Hajishirzi. FActScore: Fine-grained atomic evaluation of factual precision in long form text generation. In
  Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pages 12076–12100.
  Association for Computational Linguistics, 2023. URL https://aclanthology.org/2023.emnlp-main.741/.
James Thorne, Andreas Vlachos, Christos Christodoulopoulos, and Arpit Mittal. FEVER: A large-scale dataset for fact
  extraction and verification. In Proceedings of the 2018 Conference of the North American Chapter of the Association
  for Computational Linguistics: Human Language Technologies, pages 809–819. Association for Computational
  Linguistics, 2018. doi:10.18653/v1/N18-1074.
Dongyu Ru, Lin Qiu, Xiangkun Hu, Tianhang Zhang, Peng Shi, Shuaichen Chang, Cheng Jiayang, Cunxiang Wang,
  Shichao Sun, Huanyu Li, Zizhao Zhang, Binjie Wang, Jiarong Jiang, Tong He, Zhiguo Wang, Pengfei Liu, Yue
  Zhang, and Zheng Zhang. Ragchecker: A fine-grained framework for diagnosing retrieval-augmented generation. In
 Advances in Neural Information Processing Systems, 2024.
Rohan Sequeira, Stavros Damianakis, Umar Iqbal, and Konstantinos Psounis. Agent-sentry: Bounding llm agents via
  execution provenance. arXiv preprint arXiv:2603.22868, 2026. URL https://arxiv.org/abs/2603.22868.
Kevin Wu, Eric Wu, Ally Cassasola, Angela Zhang, Kevin Wei, Teresa Nguyen, Sith Riantawan, Patricia Shi Riantawan,
  Daniel E. Ho, and James Zou. An automated framework for assessing how well LLMs cite relevant medical references.
  Nature Communications, 16:3615, 2025. URL https://www.nature.com/articles/s41467-025-58551-6.
  Earlier version: arXiv:2402.02008.
Haoyu Wang, Christopher M. Poskitt, and Jun Sun. AgentSpec: Customizable runtime enforcement for safe and reliable
  LLM agents. In Proceedings of the IEEE/ACM 48th International Conference on Software Engineering (ICSE), 2026.
  URL https://arxiv.org/abs/2503.18666. arXiv:2503.18666.
Anna Martin-Boyle, Cara Leckey, Martha Brown, and Harmanpreet Kaur. PaperTrail: A claim-evidence interface for
  grounding provenance in llm-based scholarly q&a. In Proceedings of the 2026 CHI Conference on Human Factors in
 Computing Systems, pages 1–25, 2026.
Shahul Es, Jithin James, Luis Espinosa Anke, and Steven Schockaert. RAGAS: Automated evaluation of retrieval
  augmented generation. In Proceedings of the 18th Conference of the European Chapter of the Association for
  Computational Linguistics: System Demonstrations, pages 150–158, St. Julians, Malta, 2024. Association for
  Computational Linguistics. URL https://aclanthology.org/2024.eacl-demo.16/.
Joel Rorseth, Parke Godfrey, Lukasz Golab, Divesh Srivastava, and Jarek Szlichta. LADYBUG: An LLM agent
  DeBUGger for data-driven applications. In Proceedings of the 28th International Conference on Extending Database
  Technology, pages 1082–1085, 2025. URL https://openproceedings.org/2025/conf/edbt/paper-313.
  pdf.
Guohao Li, Hasan Hammoud, Hani Itani, Dmitrii Khizbullin, and Bernard Ghanem. CAMEL: Communicative agents
  for “mind” exploration of large language model society. Advances in neural information processing systems, 36:
  51991–52008, 2023.
Manuel Costa, Boris Köpf, Aashish Kolluri, Andrew Paverd, Mark Russinovich, Ahmed Salem, Shruti Tople, Lukas
 Wutschitz, and Santiago Zanella-Béguelin. Securing ai agents with information-flow control. arXiv preprint
 arXiv:2505.23643, 2025. URL https://arxiv.org/abs/2505.23643.
Yuandao Cai, Wensheng Tang, Cheng Wen, and Shengchao Qin. Ghost in the agent: Redefining information flow
  tracking for llm agents. arXiv preprint arXiv:2604.23374, 2026. URL https://arxiv.org/abs/2604.23374.
Edoardo Debenedetti, Ilia Shumailov, Tianqi Fan, Jamie Hayes, Nicholas Carlini, Daniel Fabian, Christoph Kern,
  Chongyang Shi, Andreas Terzis, and Florian Tramèr. Defeating prompt injections by design. In IEEE Conference
  on Secure and Trustworthy Machine Learning (SaTML), 2026. URL https://arxiv.org/abs/2503.18813.
  arXiv:2503.18813.
Joon Sung Park, Joseph C. O’Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, and Michael S. Bernstein. Gen-
  erative agents: Interactive simulacra of human behavior. In Proceedings of the 36th Annual ACM Symposium on User
  Interface Software and Technology. Association for Computing Machinery, 2023. doi:10.1145/3586183.3606763.
Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, and Joseph E. Gonzalez. Memgpt:
  Towards llms as operating systems. arXiv preprint arXiv:2310.08560, 2023. URL https://arxiv.org/abs/
  2310.08560.
Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, and Yongfeng Zhang. A-MEM: Agentic memory for LLM
 agents. Advances in Neural Information Processing Systems, 38:17577–17604, 2026.


                                                         24
                                            From Agent Traces to Trust


Christoph Bühler, Matteo Biagiola, Luca Di Grazia, and Guido Salvaneschi. AgentBound: Securing execution
  boundaries of ai agents. In Proceedings of the ACM on Software Engineering (FSE), 2026. URL https://doi.
  org/10.1145/3808103. arXiv:2510.21236.
Qiusi Zhan, Zhixiang Liang, Zifan Ying, and Daniel Kang. InjecAgent: Benchmarking indirect prompt injections in
  tool-integrated large language model agents. In Findings of the Association for Computational Linguistics: ACL
  2024, pages 10471–10506. Association for Computational Linguistics, 2024. URL https://doi.org/10.18653/
  v1/2024.findings-acl.624.
Renan Souza, Amal Gueroudji, Stephen DeWitt, Daniel Rosendo, Tirthankar Ghosal, Robert Ross, Prasanna Bal-
  aprakash, and Rafael Ferreira Da Silva. Prov-agent: Unified provenance for tracking ai agent interactions in agentic
  workflows. In 2025 IEEE International Conference on eScience (eScience), pages 467–473. IEEE, 2025.
Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Thorsten Holz, and Mario Fritz. Not what you’ve
  signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection. In Proceedings
  of the 16th ACM Workshop on Artificial Intelligence and Security, pages 79–90. Association for Computing Machinery,
  2023. doi:10.1145/3605764.3623985. URL https://doi.org/10.1145/3605764.3623985.
Yi Liu, Gelei Deng, Yuekang Li, Kailong Wang, Zihao Wang, Xiaofeng Wang, Tianwei Zhang, Yepang Liu, Haoyu
  Wang, Yan Zheng, Leo Yu Zhang, and Yang Liu. Prompt injection attack against LLM-integrated applications. arXiv
  preprint arXiv:2306.05499, 2023. URL https://arxiv.org/abs/2306.05499.
Dorothy E. Denning. A lattice model of secure information flow. Communications of the ACM, 19(5):236–243, 1976.
  doi:10.1145/360051.360056. URL https://doi.org/10.1145/360051.360056.
Andrei Sabelfeld and Andrew C. Myers. Language-based information-flow security. IEEE Journal on Selected Areas in
  Communications, 21(1):5–19, 2003. doi:10.1109/JSAC.2002.806121.
Eric Wallace, Kai Xiao, Reimar Leike, Lilian Weng, Johannes Heidecke, and Alex Beutel. The instruction hierarchy:
  Training LLMs to prioritize privileged instructions. arXiv preprint arXiv:2404.13208, 2024. URL https://arxiv.
  org/abs/2404.13208.
Sizhe Chen, Julien Piet, Chawin Sitawarin, and David Wagner. StruQ: Defending against prompt injection with
  structured queries. In 34th USENIX Security Symposium (USENIX Security 25), pages 2383–2400, 2025.
Jerome H. Saltzer and Michael D. Schroeder. The protection of information in computer systems. Proceedings of the
  IEEE, 63(9):1278–1308, 1975. doi:10.1109/PROC.1975.9939.
Traian Rebedea, Razvan Dinu, Makesh Narsimhan Sreedhar, Christopher Parisien, and Jonathan Cohen. NeMo
  guardrails: A toolkit for controllable and safe LLM applications with programmable rails. In Proceedings of the
  2023 Conference on Empirical Methods in Natural Language Processing: System Demonstrations, pages 431–445,
  Singapore, December 2023. Association for Computational Linguistics. doi:10.18653/v1/2023.emnlp-demo.40. URL
  https://aclanthology.org/2023.emnlp-demo.40/.
Hakan Inan, Kartikeya Upasani, Jianfeng Chi, Rashi Rungta, Krithika Iyer, Yuning Mao, Michael Tontchev, Qing
  Hu, Brian Fuller, Davide Testuggine, and Madian Khabsa. Llama Guard: LLM-based input-output safeguard for
  human-AI conversations. arXiv preprint arXiv:2312.06674, 2023. URL https://arxiv.org/abs/2312.06674.
Zeyu Zhang, Xiaohe Bo, Chen Ma, Rui Li, Xu Chen, Quanyu Dai, Jieming Zhu, Zhenhua Dong, and Ji-Rong Wen. A
  survey on the memory mechanism of large language model based agents. ACM Transactions on Information Systems,
  2025. doi:10.1145/3748302.
Pengfei Du. Memory for autonomous llm agents: Mechanisms, evaluation, and emerging frontiers. arXiv preprint
  arXiv:2603.07670, 2026. URL https://arxiv.org/abs/2603.07670.
Chang Yang, Chuang Zhou, Yilin Xiao, Su Dong, Luyao Zhuang, Yujing Zhang, Zhu Wang, Zijin Hong, Zheng
  Yuan, Zhishang Xiang, Shengyuan Chen, Huachi Zhou, Qinggang Zhang, Ninghao Liu, Jinsong Su, Xinrun Wang,
  Yi Chang, and Xiao Huang. Graph-based agent memory: Taxonomy, techniques, and applications. arXiv preprint
  arXiv:2602.05665, 2026. URL https://arxiv.org/abs/2602.05665.
Wanjun Zhong, Lianghong Guo, Qiqi Gao, He Ye, and Yanlin Wang. MemoryBank: Enhancing large language
  models with long-term memory. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, pages
  19724–19731, 2024. doi:10.1609/aaai.v38i17.29946.
Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, and Deshraj Yadav. Mem0: Building production-
  ready ai agents with scalable long-term memory. In European Conference on Artificial Intelligence (ECAI), 2025.
  arXiv:2504.19413.
Weizhi Wang, Li Dong, Hao Cheng, Xiaodong Liu, Xifeng Yan, Jianfeng Gao, and Furu Wei. Augmenting language
  models with long-term memory. In Advances in Neural Information Processing Systems, volume 36, pages 74530–
  74543, 2023.


                                                         25
                                            From Agent Traces to Trust


Zhaorun Chen, Zhen Xiang, Chaowei Xiao, Dawn Song, and Bo Li. AgentPoison: Red-teaming LLM
  agents via poisoning memory or knowledge bases. In Advances in Neural Information Processing Sys-
  tems, volume 37, 2024.    URL https://proceedings.neurips.cc/paper_files/paper/2024/hash/
  eb113910e9c3f6242541c1652e30dfd6-Abstract-Conference.html.
Shen Dong, Shaochen Xu, Pengfei He, Yige Li, Jiliang Tang, Tianming Liu, Hui Liu, and Zhen Xiang. Memory
  injection attacks on LLM agents via query-only interaction. In Advances in Neural Information Processing Systems,
  2025. URL https://openreview.net/forum?id=QINnsnppv8.
Hanling Tian, Zeyang Sha, Jingying Wang, Yuhang Liu, Zhehao Huang, and Xiaolin Huang. InjecMEM: Memory
  injection attack on LLM agent memory systems. OpenReview preprint, 2026. URL https://openreview.net/
  forum?id=QVX6hcJ2um. Submitted to ICLR 2026.
Sidharth Pulipaka, Stanislau Hlebik, Leonidas Raghav, Sahar Abdelnabi, Vyas Raina, Ivaxi Sheth, and Mario Fritz.
  Hidden in memory: Sleeper memory poisoning in LLM agents, 2026. URL https://arxiv.org/abs/2605.
  15338.
Bo Wang, Weiyi He, Shenglai Zeng, Zhen Xiang, Yue Xing, Jiliang Tang, and Pengfei He. Unveiling privacy risks in
  LLM agent memory. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics
  (Volume 1: Long Papers), pages 25241–25260, Vienna, Austria, July 2025. Association for Computational Linguistics.
  doi:10.18653/v1/2025.acl-long.1227. URL https://aclanthology.org/2025.acl-long.1227/.
Qianshan Wei, Tengchao Yang, Yaochen Wang, Xinfeng Li, Lijun Li, Zhenfei Yin, Yi Zhan, Thorsten Holz, Zhiqiang
  Lin, and XiaoFeng Wang. A-MemGuard: A proactive defense framework for LLM-based agent memory, 2025. URL
  https://arxiv.org/abs/2510.02373.
Wei Zou, Mingwen Dong, Miguel Romero Calvo, Shuaichen Chang, Jiang Guo, Dongkyu Lee, Xing Niu, Xiaofei Ma,
 Yanjun Qi, and Jiarong Jiang. Poison once, exploit forever: Environment-injected memory poisoning attacks on web
 agents. arXiv preprint arXiv:2604.02623, 2026. doi:10.48550/arXiv.2604.02623.
Jon Saad-Falcon, Omar Khattab, Christopher Potts, and Matei Zaharia. ARES: An automated evaluation framework for
  retrieval-augmented generation systems. In Proceedings of the 2024 Conference of the North American Chapter of the
  Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), pages 338–354,
  Mexico City, Mexico, June 2024. Association for Computational Linguistics. doi:10.18653/v1/2024.naacl-long.20.
  URL https://aclanthology.org/2024.naacl-long.20/.
Cheng Niu, Yuanhao Wu, Juno Zhu, Siliang Xu, Kashun Shum, Randy Zhong, Juntong Song, and Tong Zhang. Ragtruth:
  A hallucination corpus for developing trustworthy retrieval-augmented language models. In Proceedings of the 62nd
  Annual Meeting of the Association for Computational Linguistics, pages 10862–10878. Association for Computational
  Linguistics, 2024. doi:10.18653/v1/2024.acl-long.585. URL http://papers.nips.cc/paper_files/paper/
  2024/hash/27245589131d17368cccdfa990cbf16e-Abstract-Datasets_and_Benchmarks_Track.html.
Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, Mohit Bansal, Francesco Barbieri, and Yuwei Fang. Evaluating
  very long-term conversational memory of llm agents. In Proceedings of the 62nd Annual Meeting of the Association
  for Computational Linguistics, pages 13851–13870, 2024.
Zexue He, Yu Wang, Churan Zhi, Yuanzhe Hu, Tzu-Ping Chen, Lang Yin, Ze Chen, Tong Arthur Wu, Siru Ouyang,
  Zihan Wang, Jiaxin Pei, Julian McAuley, Yejin Choi, and Alex Pentland. MemoryArena: Benchmarking agent
  memory in interdependent multi-session agentic tasks. arXiv preprint arXiv:2602.16313, 2026.
OpenLineage Contributors. OpenLineage Specification. https://github.com/OpenLineage/OpenLineage/
  blob/main/spec/OpenLineage.md, 2026. Accessed: 2026-05-25.
Tobias Schreieder, Tim Schopf, and Michael Färber. Attribution, citation, and quotation: A survey of evidence-based
  text generation with large language models. In Proceedings of the 64th Annual Meeting of the Association for
  Computational Linguistics (Volume 1: Long Papers), pages 30956–31000, 2026. URL https://aclanthology.
  org/2026.acl-long.1430/. arXiv:2508.15396.
Victor Ojewale, Harini Suresh, and Suresh Venkatasubramanian. Audit trails for accountability in large language
  models. arXiv preprint arXiv:2601.20727, 2026.
Yi Nian, Aojie Yuan, Haiyue Zhang, Jiate Li, Li Li, Xiyang Hu, Hua Wei, Xiongye Xiao, Chaowei Xiao, and Yue Zhao.
  Auditable agents. arXiv preprint arXiv:2604.05485, 2026.
Yusheng Zheng, Yiwei Yang, Wei Zhang, and Andi Quinn. ACRFence: Preventing semantic rollback attacks in agent
  checkpoint-restore. arXiv preprint arXiv:2603.20625, 2026.


                                                        26
                                                From Agent Traces to Trust


A     Additional Taxonomy Mappings

This appendix provides supplementary material for the taxonomy in Section 2. The main text keeps the taxonomy
compact by using Figure 2 and Table 1 as the backbone, while the mapping below makes explicit how the proposed
agent-provenance vocabulary relates to standard provenance modeling. The concrete provenance-graph example is
discussed in Section 3, where it serves as a running example for provenance representation rather than as appendix-only
material.

A.1   Mapping to W3C PROV-DM

Table 8 makes the relationship to the W3C PROV data model explicit. Node types align with PROV entities, activities,
and agents, so much of agent execution can reuse a standard provenance vocabulary. The relations are then grouped into
three tiers. U SE, G ENERATE and D ERIVE are inherited: their PROV semantics are retained unchanged. D EPEND - ON,
T RIGGER, I NVALIDATE and U PDATE are specialized: PROV expresses each in a weaker form, and agent execution
requires the stronger reading given in the table. Only the third tier is novel, and it is what PROV does not directly express:
agent execution introduces semantic relations such as S UPPORT and C ONTRADICT, which depend on comparing the
content of evidence and claims rather than only on bookkeeping about how artifacts were produced. In this sense, agent
provenance extends, rather than merely instantiates, classical provenance models.


B     Operational Semantics of Provenance Relations

This appendix is new in this revision. Because it is new in its entirety, it is not marked sentence by sentence.
Section 2 introduces nine provenance relations. This appendix makes them operational, so that two independent
annotators reading the same execution trace should produce the same typed graph. For each relation we give (i) a
signature constraining which node types it may connect, (ii) its direction, (iii) whether it carries a temporal requirement,
(iv) the necessary and sufficient condition under which it holds, and (v) a positive example, a negative or boundary
example, and the relation it is most often confused with together with the test that separates them. Section B.3 then
works through the two boundary cases on which annotators most often disagree. Section C then states formally what it
means for evidence tracing to be a projection of execution provenance.

B.1   Node Types and Unit Roles

The distinction between evidence units and execution units in Section 2.1 becomes sharp once artifacts are separated
from occurrences, following the entity/activity split of W3C PROV-DM [World Wide Web Consortium, 2013]. An
evidence unit is an artifact: it carries a content field ρ(v) that can be compared with the content of another node. An
execution unit is an occurrence: it carries an actor and a time interval, and its identity is that it happened, not what it
says. Table 9 assigns every node type in the taxonomy to exactly one role.
Two consequences follow, and they answer the question of when an object is an evidence unit, an execution unit, or
both.

      1. At graph level the roles are disjoint. A tool output is an evidence unit; the tool call that produced it is an
         execution unit; the two are distinct nodes joined by a G ENERATE edge. The intuition that a tool output is
         “both” reflects the granularity of a flat log, in which a single record carries the call, its arguments, and its result.
         Converting a log to a provenance graph therefore always involves splitting such records.
      2. Roles are stable, but the part of the node an edge reads is not. A semantic edge incident on a node reads
         its content ρ(v); a procedural edge reads its occurrence. This is why an intermediate claim can be the target
         of S UPPORT (a statement about its content) and, in the same graph, the source of T RIGGER to a tool call (a
         statement about its occurrence) without any ambiguity of role.

B.2   Relation Signatures, Directionality, and Temporal Semantics

We write E for the set of evidence units, X for execution units, and C ⊂ E for the assertive evidence units, namely
intermediate claims and final answers. A relation is semantic if whether it holds is determined by the contents of its
endpoints, and procedural if whether it holds is determined by the execution, independently of whether the contents are
true. Table 10 records the signature of each relation; Table 11 records the condition under which it holds together with
worked examples.


                                                              27
                                                From Agent Traces to Trust


Table 8: Explicit correspondence between the W3C PROV data model [World Wide Web Consortium, 2013] and
the agent-provenance model used in this survey. Relations are grouped into three tiers: inherited relations whose
PROV semantics are retained, specialized relations that refine a weaker PROV notion for agent execution, and novel
content-level relations, together with the semantic unit types, for which PROV has no counterpart. The contribution
of the vocabulary is the third tier plus the operational refinement in the second, not a claim that every non-inherited
relation is new.
W3C PROV construct Agent-provenance                 Notes and agent-specific extension
                   counterpart
Node types (PROV-aligned)
Entity                 Evidence / execution         Documents, passages, tool outputs, memory items, generated claims,
                       artifact                     messages.
Activity               Execution unit               Reasoning steps, retrieval and tool calls, memory operations, environment
                                                    actions.
Agent                    Agent                      LLM, tool/API, user, or sub-agent; multi-agent roles and delegation become
                                                    first-class.
Tier 1 — Inherited relations (PROV semantics retained)
used                      U SE                     A step consumed an artifact. Declarative and instrumentable, exactly as in
                                                   PROV; agent provenance adds trust and taint labels on the consumed value.
wasGeneratedBy            G ENERATE                A tool output is generated by a tool call; a claim by a reasoning step.
wasDerivedFrom            D ERIVE                  Memory derived from a document, or a claim from a table; captures
                                                   summarization and transformation, not only copying.
Tier 2 — Specialized relations (PROV-compatible notions refined for agent execution)
used (strengthened)       D EPEND - ON            PROV used records consumption; agent D EPEND - ON additionally asserts
                                                  counterfactual dependence, established by replay or ablation. The two are
                                                  deliberately distinct relations here, since a step may consume ten artifacts
                                                  and depend on one. Step-on-step dependence is outside used altogether,
                                                  since used relates an activity to an entity; the nearest PROV construct is
                                                  wasInformedBy, which records that one activity was informed by another
                                                  without asserting counterfactual dependence.
wasInformedBy             T RIGGER                An observation triggers a tool call; an error triggers replanning.
wasInvalidatedBy          I NVALIDATE             PROV invalidation ends an entity’s existence; agent I NVALIDATE marks a
                                                  claim, plan, or memory item as epistemically invalid while the record
                                                  persists.
wasRevisionOf             U PDATE                 Memory, external-state, or delivered-output updates across turns or sessions;
                                                  agent U PDATE identifies the superseded version by location rather than by
                                                  content similarity.
Tier 3 — Novel relations and units (no PROV counterpart)
—                         S UPPORT                Evidence supports a claim, decision, or action; central to attribution, but
                                                  PROV has no support/justification semantics.
—                         C ONTRADICT             A tool output contradicts a memory item or retrieved passage; requires
                                                  semantic comparison, not provenance bookkeeping.
—                         Semantic units          Generated claims, tool-call rationales, natural-language observations,
                                                  inter-agent messages, and trust labels, which PROV treats as opaque entities.


One further label appears in provenance graphs but is not one of the nine: S UPPORT- CANDIDATE, generated by the
projection of Appendix C. Its signature is E → C, it is asymmetric, its temporal constraint is t(s) < t(t) inherited from
the edges of its witness path, and its origin is always D ERIVED, the value reserved for edges computed rather than
observed. It asserts availability of content, never support, and no instrumented or annotated graph contains one.




                                                              28
                                                 From Agent Traces to Trust


Table 9: Node types and their unit role. A node type is an evidence unit if it carries a comparable content field, and an
execution unit if it carries an actor and a time interval. Under the entity/activity split the two roles are disjoint; apparent
dual membership arises only when a flat log collapses an activity and the artifact it produced into one record.

 Role              Node types                                    Content       Actor +         Eligible as
                                                                   ρ           interval
 Evidence unit     User query or instruction, retrieved               ✓               ✗        Endpoint of every semantic and
                   document or passage, environment                                            derivational relation, and of U PDATE;
                   observation, tool output, memory item,                                      source of T RIGGER; target of U SE,
                   generated tool parameter, policy, tool                                      G ENERATE, D EPEND - ON. Which end
                   manifest, inter-agent message, intermediate                                 is permitted in each case is fixed by the
                   claim, final answer                                                         signatures in Table 10: only assertive
                                                                                               units may be the target of S UPPORT.
 Execution unit    Reasoning step, retrieval call, tool call,         ✗               ✓        Source of U SE, G ENERATE,
                   memory read or write, environment action,                                   D EPEND - ON; source and target of
                   delegation step                                                             T RIGGER; target of D EPEND - ON; target
                                                                                               of S UPPORT and I NVALIDATE via its
                                                                                               precondition (Section B.2).
 Actor             LLM, tool or API, user, sub-agent                  ✗               ✗        Attribution of responsibility only; never
                                                                                               an endpoint of a semantic relation.

Table 10: Signature, directionality, and temporal semantics of the nine provenance relations. The “Temporal” column
states the ordering the relation requires between its endpoints. Write t(v) for the timestamp of an evidence unit and,
for an execution unit, for the start of its interval; an artifact produced by an activity is timestamped at that activity’s
completion, which is why G ENERATE admits equality. I NVALIDATE is stated against test (t), the time at which the target
was established (created for an artifact, scheduled for a step), because a step may be invalidated before it ever starts,
and U SE likewise admits equality, since a step may begin at the instant its input was produced. Note that the required
order is not always source-before-target: for I NVALIDATE, D EPEND - ON, U PDATE and U SE the source is the later node,
because the invalidator, the dependent step, the new version and the consuming activity all come after what they act on.
Semantic relations constrain content; procedural relations constrain execution. Note that no relation encodes temporal
succession on its own: ordering is carried by node timestamps, not by an edge.

 Relation         Signature (source → target)      Direction              Temporal Family and algebra
 S UPPORT         E →C∪X                           Supporter →             None           Semantic support. Asymmetric; not
                                                   supported                              transitive.
 C ONTRADICT E ↔ E                                 Symmetric               None           Semantic support. Symmetric; not transitive.
                                                   (unordered pair)
 I NVALIDATE      E → C ∪ {memory item} ∪ X        Invalidator →           t(s) >         Semantic support (epistemic status).
                                                   invalidated             test (t)       Asymmetric.
 D ERIVE          E →E                             Origin → derived        t(s) <         Content transformation. Asymmetric;
                                                                             t(t)         transitive.
 D EPEND - ON     X →E ∪X                          Dependent step →        t(s) >         Causal (counterfactual: parameterization).
                                                   dependency                t(t)         Asymmetric; transitive.
 T RIGGER         E ∪X →X                          Cause → activated       t(s) <         Causal (counterfactual: occurrence).
                                                   step                      t(t)         Asymmetric; not transitive.
 U PDATE          E → E (same identified           New version →           t(s) >         Procedural, state succession (instrumented).
                  location)                        superseded                t(t)         Asymmetric.
                                                   version
 U SE             X →E                             Activity →              t(s) ≥         Procedural, declarative (instrumented; PROV
                                                   consumed artifact         t(t)         used).
 G ENERATE        X →E                             Activity →              t(s) ≤         Procedural, declarative (instrumented; PROV
                                                   produced artifact         t(t)         wasGeneratedBy). Functional: each artifact
                                                                                          has at most one generator within a run.



                                                                                                                     continued on next page




                                                                 29
                                                                From Agent Traces to Trust


Table 11 (continued)
Relation        Holds if and only if                                                Positive / negative example                    Confusable with, and the test

                              Table 11: Necessary and sufficient conditions, worked examples, and boundary cases. The final column
                              names the relation each is most often confused with, together with the test that separates them. s denotes
                              the source node and t the target; ρ(·) denotes node content.

Relation        Holds if and only if                                                Positive / negative example                    Confusable with, and the test

S UPPORT        Taking ρ(s) as given raises the warrant for ρ(t), or for the         + Passage “Q3 revenue was $2.1B”              D EPEND - ON. Ablate s: if the claim
                precondition of step t, above a threshold θ fixed in advance by supports the claim “Q3 revenue exceeded            would still be warranted, S UPPORT is a
                the annotation protocol. The relation is a property of the two       $2B”.                                         property of content and survives; if the
                contents, not of the execution; given θ it is adjudicable by a       – A passage on the same topic that does       step would have been parameterized
                third party who reads only ρ(s) and ρ(t). Because θ is               not entail the claim: relevant and            differently, that is D EPEND - ON. Both
                task-specific and not derivable from the graph, a protocol that possibly cited, but not supporting [Wu             may hold; they are not alternatives.
                leaves it unstated will not reproduce, which is why                  et al., 2025].
                inter-annotator agreement bounds any metric built on this
                relation (Section 6.4). Not necessary: that the agent read s. Not
                sufficient: that the agent cited s, that s was in context, or that s
                changed the output.
C ONTRADICT     ρ(s) and ρ(t) cannot both hold under the task’s interpretation, + Tool output “balance = 0” contradicts            I NVALIDATE. C ONTRADICT is a
                at the same time index.                                              memory item “account is funded”.              symmetric statement about content and
                                                                                     – Two figures at different granularity or     asserts nothing about which endpoint
                                                                                     different time indices that are jointly       survives.
                                                                                     satisfiable: not a contradiction but
                                                                                     staleness.
I NVALIDATE     (i) s contradicts t or establishes that a precondition of t no       + A 404 response invalidates the planned      C ONTRADICT (see above) and U PDATE.
                longer holds; (ii) s is at least as authoritative as the basis of t, tool call to that endpoint, whose             I NVALIDATE marks the old item
                and t(s) > test (t); (iii) after s, t may no longer be used as a precondition no longer holds.                     unusable; U PDATE installs the new one.
                warrant. The record of t persists.                                   – A conflicting but less authoritative        They commonly co-occur as two distinct
                                                                                     source: record C ONTRADICT only, and          edges.
                                                                                     leave adjudication to a later step.
D ERIVE         ρ(t) was produced by a transformation of ρ(s) that preserves + A memory item derived from a                        S UPPORT. D ERIVE says where content
                or reduces information: copying, extraction, summarization,          conversation turn; a claim derived from a     came from; S UPPORT says whether
                translation, or aggregation. Not sufficient: topical similarity, or table row.                                     content warrants. A claim
                co-presence in the context window.                                   – A claim produced from parametric            mis-summarized from a passage is
                                                                                     knowledge while a document happened           D ERIVE without S UPPORT, which is
                                                                                     to be in context: no D ERIVE edge.            precisely the attributable-hallucination
                                                                                                                                   case [Min et al., 2023, Ru et al., 2024].
D EPEND - ON    Had t been absent or different, step s would have been issued       + A tool call whose argument string was        U SE. On dependencies whose target is
                with different arguments or would otherwise have behaved            extracted from a retrieved page.               an artifact, U SE is the observable
                differently. Whether the step occurred at all is T RIGGER, not      – A document present in the context            over-approximation that the harness
                D EPEND - ON. Established by replay, ablation, or fault             window that provably does not change           emits and D EPEND - ON is the
                injection [Zhang et al., 2026], not by reading content.             the arguments under replay: U SE but not       counterfactual subset inside it.
                                                                                    D EPEND - ON.                                  Dependencies on another step have no
                                                                                                                                   U SE counterpart at all, and can be
                                                                                                                                   established only by replay.
T RIGGER        The occurrence of s is what caused step t to be scheduled at all. + A tool error triggers replanning; a new        D EPEND - ON. The test is whether versus
                                                                                  observation triggers a diagnostic call.          how: T RIGGER governs whether the step
                                                                                  – An input that only changed the                 happened, D EPEND - ON governs how it
                                                                                  arguments of an already-scheduled step.          was parameterized. Boundary case: a
                                                                                                                                   step that would have occurred regardless
                                                                                                                                   but was brought forward or delayed by s
                                                                                                                                   is not triggered by it, since scheduling
                                                                                                                                   time is an attribute rather than an
                                                                                                                                   occurrence; record the re-timing in the
                                                                                                                                   timestamps and leave the edge out.
U PDATE         s and t occupy the same identified location (a store slot,           + A user-preference memory revised in a       D ERIVE. U PDATE requires identity
                memory key, external state variable, or an externally identified later session.                                    continuity of the slot; D ERIVE does not.
                output slot such as the response delivered for a given user turn), – A second, independent memory item             A summary written to a new key is
                and s supersedes t from its timestamp onward. Two artifacts          about the same topic that does not            D ERIVE; overwriting the old key is both.
                occupy the same location iff they are addressed by the same          overwrite the first: two items, no
                identifier within the same scope, so a revised answer to one turn U PDATE.
                updates that turn’s response while an answer to a later turn is a
                different location. Identity of location, not similarity of content,
                is what the relation asserts.
U SE            The harness supplied artifact t to activity s. A recorded fact       + A reasoning step uses all ten passages      D EPEND - ON (see above). Reporting
                about the execution; asserts no influence and no support.            returned by a retrieval call.                 U SE as if it were S UPPORT is the single
                                                                                     – A passage retrieved but filtered out        most common over-claim in
                                                                                     before the step: not used.                    citation-style evaluation.
G ENERATE       Activity s produced artifact t, whose timestamp equals the           + A tool call generates a tool output; a      D ERIVE. G ENERATE connects an
                completion of s.                                                     reasoning step generates a claim.             activity to an artifact; D ERIVE connects
                                                                                     – A corpus document that pre-existed the      two artifacts. Both are typically present:
                                                                                     run: it enters the graph with an              a reasoning step G ENERATEs a claim
                                                                                     external-origin attribute and no generator.   that D ERIVEs from a passage.




                                                                                   30
                                              From Agent Traces to Trust


B.3   Separating Semantic Support from Procedural Influence

The four notions that Table 10 keeps apart are frequently conflated in trace-based evaluation, so we state the discrimi-
nating tests directly.

       • Semantic support (S UPPORT, C ONTRADICT, and the first clause of I NVALIDATE) is decided by reading the
         contents of the two endpoints. It is agent-independent: a passage supports a claim whether or not any agent
         ever retrieved it. When the target of S UPPORT is an execution unit, which carries no content of its own, the
         content read is the step’s precondition: the proposition that must hold for the step to be justified, which the
         annotation protocol is required to make explicit before the edge can be adjudicated.
       • Content derivation (D ERIVE) is decided by asking whether the target’s content is a transformation of the
         source’s. It is agent-dependent and content-level at once, which is why it can hold while S UPPORT fails.
       • Causal dependence (T RIGGER, D EPEND - ON) is decided counterfactually, by removing or perturbing the
         source and re-running. It says nothing about whether the content is true.
       • Procedural dependence (U SE, G ENERATE, U PDATE) is decided declaratively, by reading what the harness
         emitted. It is the observable layer beneath causal dependence.
       • Temporal succession is deliberately not a relation. Adjacency in a log is an artifact of ordering, not a
         dependency, so ordering is carried by node timestamps and never by an edge. Two steps that follow one
         another with no T RIGGER, D EPEND - ON, or U SE edge between them are, by construction, independent in the
         provenance graph.

Two boundary cases deserve explicit treatment because they are the ones on which annotators most often disagree.

Case 1: a tool output changes the final decision without justifying the final claim. Record U SE(step, output)
because the harness passed it; record D EPEND - ON(action, output) if ablating the output changes the action;
record D ERIVE only if the answer’s content is a transformation of the output’s content; record S UPPORT only
if a third party reading the two contents judges that the output warrants the claim. The correct annotation is
frequently {U SE, D EPEND - ON} with neither D ERIVE nor S UPPORT, and the resulting graph says exactly the
right thing: the decision was influenced by something that did not justify it.
Case 2: an incorrect memory item causally triggers an action. Record T RIGGER(memory item, action),
because the relation is procedural and holds regardless of the item’s truth. Do not record S UPPORT, because
S UPPORT is content-conditional and a false premise cannot warrant a claim. When the error is discovered, add
C ONTRADICT(new evidence, memory item) and I NVALIDATE(new evidence, dependent claim). The graph
then simultaneously records that the item drove the execution and that it was never valid evidence, which is the
distinction the taxonomy exists to preserve.

B.4   Which Relations Are Observable, and Which Must Be Inferred

Provenance relations differ not only in meaning but in how they can be obtained. We therefore annotate every edge
with an origin attribute. Three values apply to edges of a recorded execution: I NSTRUMENTED (emitted by the agent
harness or runtime), I NFERRED (assigned post hoc by a model or a human annotator), and D ECLARED (asserted by
the agent itself, for example a self-reported citation). A fourth, D ERIVED, is reserved for edges computed from a
graph by a defined procedure rather than obtained from the execution at all; the only label carrying it is S UPPORT-
CANDIDATE , produced by the projection of Appendix C. Table 12 states which relations admit which origins. The
practical consequence is that a provenance graph is heterogeneous in reliability: its procedural skeleton can be logged,
but its semantic layer is a judgement, and evaluation must treat the two differently.
Orthogonally to origin, an edge may carry an assurance attribute recording whether the trace it came from is merely
logged, or additionally protected against post-hoc modification. Among the systems surveyed in Table 2, none reports
tamper-evidence, signing, or attestation for its traces, so provenance is trustworthy only to the extent that the party
holding the log is [Ojewale et al., 2026, Nian et al., 2026, Zheng et al., 2026]. Section 7 treats this as an open problem
rather than a solved dimension.

B.5   Derived Predicates: C ITED and O MITTED

Section 3.2 refers to C ITED and O MITTED. These are not additional taxonomy relations; they are predicates derived
from the nine above, and defining them requires the origin attribute of Section B.4, because a citation is an agent’s
assertion that support holds, which is a different thing from support holding.


                                                           31
                                                From Agent Traces to Trust


Table 12: Origin of each of the nine provenance relations; the derived S UPPORT- CANDIDATE label is not shown, since
its origin is always D ERIVED. I NSTRUMENTED edges are emitted by the runtime and are reproducible; I NFERRED
edges require model or human judgement and therefore carry annotation error; D ECLARED edges are agent self-reports
and are the least reliable, since a declared citation need not support the claim it annotates [Wu et al., 2025].

 Relation         Available origins How it is obtained in practice
 U SE,              Instrumented     Emitted directly by the agent loop, tool router, or memory store; reproducible from logs
 G ENERATE                           alone [Dong et al., 2024, AlSayyad et al., 2026, Souza et al., 2025].
 U PDATE            Instrumented,    Instrumented when the store versions its keys; otherwise inferred by matching successive
                       Inferred      items to the same slot.
 T RIGGER           Instrumented,    Instrumented when the harness dispatches on an event, such as retry-on-error; inferred
                       Inferred      when the model itself chose to act on an observation.
 D EPEND - ON          Inferred      Not directly observable. Obtained by replay, ablation, fault injection, or information-flow
                                     tracking; U SE over-approximates it only for dependencies on artifacts [Zhang et al., 2026,
                                     Costa et al., 2025, Cai et al., 2026].
 S UPPORT,        Inferred, Declared Never directly observable. Require semantic judgement by a human annotator or model
 C ONTRADICT,                        judge, and therefore require an annotation protocol and reported inter-annotator
 I NVALIDATE                         agreement [Gao et al., 2023, Min et al., 2023, Thorne et al., 2018, Ru et al., 2024].
 D ERIVE          Inferred, Declared Inferred by content comparison, or declared by an agent that reports its own sources for a
                                     summary or memory write.



Write avail(d) for “artifact d was available to the run”, that is, d was generated within the run or supplied to some step:
avail(d) ≡ ∃x. G ENERATE(x, d) ∨ U SE(x, d) ∨ external(d), where external(d) marks an artifact that pre-existed the
run and entered the graph without a generator, such as a corpus document. Distinguish two kinds of S UPPORT edge by
origin:
                    C ITED(d, c) ≡ ∃ e. λ(e) = S UPPORT, e : d → c, origin(e) = D ECLARED,

                  S UPPORTED(d, c) ≡ ∃ e. λ(e) = S UPPORT, e : d → c, origin(e) = I NFERRED.
C ITED records that the agent asserted the link; S UPPORTED records that an annotator or judge adjudicated it. The two
are independent, and their disagreement is exactly what citation-quality evaluation measures:
  citation error ≡ C ITED(d, c) ∧ ¬S UPPORTED(d, c),               attribution gap ≡ S UPPORTED(d, c) ∧ ¬C ITED(d, c),

                         O MITTED(d, a) ≡ avail(d) ∧ ¬∃ c ∈ claims(a). S UPPORTED(d, c),
where claims(a) denotes the decomposition of answer a into assertive units, which any claim-level protocol must fix. A
source that is cited but does not support is therefore a citation error and not a contradiction in terms [Gao et al., 2023,
Wu et al., 2025, Martin-Boyle et al., 2026]; O MITTED covers a retrieved-but-unused passage as well as a used one,
which is the case Section 3.2 describes. Note that this is the one place where the origin attribute is load-bearing rather
than descriptive: without it, an agent’s self-report and an adjudicated judgement are the same edge, and citation quality
cannot be expressed at all.

B.6   Derivation and Adequacy of the Relation Set

The nine relations are not postulated. Each is admitted only if it passes two tests, and the tests are stated so that the set
can be contested by exhibiting a relation that fails them or a query that none of them answers.

       • Necessity. Some trust-function query of Section 2.1 (verification, attribution, debugging, safety enforcement,
         audit, or recovery) becomes unanswerable if the relation is removed or merged into another.
       • Distinctness. The relation carries a decision test that no other relation’s test subsumes. Because the four
         families of Section B.3 are decided by different kinds of evidence (content comparison, content transformation,
         counterfactual ablation, and harness declaration), two relations in different families can never be merged
         without discarding one of those tests.

Table 13 applies both tests relation by relation. The third column is the operative one: it names what a reader would no
longer be able to express, and the fourth names surveyed work that already draws the distinction operationally, so that
necessity rests on existing practice rather than on our judgement.


                                                              32
                                                 From Agent Traces to Trust


Table 13: Derivation of the relation set. Each relation is admitted because removing or merging it makes a trust-function
query unanswerable, and because at least one surveyed system or benchmark already acts on the distinction it draws.

Relation        Query it answers                  What is lost if dropped or merged                     Already operational in
 S UPPORT       Is this claim warranted by the    Claim-level verification collapses into retrieval    ALCE, FActScore,
                evidence available?               logging. No PROV relation compares content, so       SourceCheckup,
                (verification)                    this cannot be recovered from the base model.        RAGChecker [Gao et al.,
                                                                                                       2023, Min et al., 2023,
                                                                                                       Wu et al., 2025, Ru et al.,
                                                                                                       2024]
 C ONTRADICT Which two artifacts cannot both Treated as negative S UPPORT, conflict between two FEVER, RAGTruth,
              be relied on? (verification,     non-assertive artifacts, such as two memory items or memory-conflict
              safety)                          two retrieved passages, becomes unrepresentable,        work [Thorne et al.,
                                               since S UPPORT requires an assertive target.            2018, Niu et al., 2024,
                                                                                                       Zhong et al., 2024]
 I NVALIDATE Which recorded item ceased to A stale or poisoned item can be deleted but not             A-MemGuard,
              be usable, and from when?        marked: recovery loses its audit trail. Distinguished memory-poisoning
              (recovery, memory)               from C ONTRADICT by carrying a time and by              defences [Wei et al.,
                                               leaving the target in the graph.                        2025, Chen et al., 2024]
 D ERIVE      Is this content a transformation Merged into S UPPORT, the attributable hallucination, ALCE, RAGTruth,
              of that content? (attribution)   a claim mis-summarized from a real passage and          NeuroTaint [Gao et al.,
                                               hence derived but unsupported, becomes                  2023, Niu et al., 2024,
                                               inexpressible, and it is precisely the case attribution Cai et al., 2026]
                                               benchmarks target.
 D EPEND - ON Would this step have been        Merged into U SE, availability is mistaken for          NeuroTaint, FIDES,
              parameterized differently        dependence: every artifact the harness supplied         AgenTracer [Cai et al.,
              without that artifact?           counts as a cause, and ablation-verified influence      2026, Costa et al., 2025,
              (debugging, safety)              becomes indistinguishable from mere presence.           Zhang et al., 2026]
 T RIGGER     Would this step have occurred at Merged into D EPEND - ON, whether a step happened AgentSpec,
              all? (debugging, safety)         collapses into how it was parameterized, but a          Agent-Sentry,
                                               guardrail that blocks a call acts on the former and a CaMeL [Wang et al.,
                                               taint check on the latter.                              2026, Sequeira et al.,
                                                                                                       2026, Debenedetti et al.,
                                                                                                       2026]
 U SE         What did the harness supply to The loggable skeleton of the graph disappears, and OpenTelemetry,
              this step? (audit)               every procedural edge becomes inferred rather than AgentOps, AgentTrace,
                                               instrumented, which is the distinction Section B.4      PROV-AGENT [Open-
                                               rests on.                                               Telemetry, 2026, Dong
                                                                                                       et al., 2024, AlSayyad
                                                                                                       et al., 2026, Souza et al.,
                                                                                                       2025]
 G ENERATE    Which step produced this         Artifacts lose their origin, so no chain runs from a    W3C PROV-DM,
              artifact? (audit, attribution)   tool call to a downstream claim, and evidence cannot AgentOps,
                                               be traced back past the point at which it entered the PROV-AGENT [World
                                               run.                                                    Wide Web Consortium,
                                                                                                       2013, Dong et al., 2024,
                                                                                                       Souza et al., 2025]
 U PDATE      Which version of this location Merged into D ERIVE, the same-location constraint is MemGPT, A-MEM,
              superseded which? (memory,       dropped, so memory lineage cannot be separated          Mem0 [Packer et al.,
              recovery)                        from ordinary content copying and versioned stores 2023, Xu et al., 2026,
                                               lose their history.                                     Chhikara et al., 2025]


Alternative decompositions we considered and rejected. Four alternatives are natural, and each fails on a specific
loss rather than on taste.

      1. W3C PROV-DM unextended. Its five relations record how artifacts were produced and never compare
         content, so S UPPORT and C ONTRADICT have no counterpart at all (Section 2.1). Claim–evidence grounding,
         the concern of an entire literature reviewed in Section 3, would be outside the model.
      2. A single attributed I NFLUENCE edge, with kind recorded as an attribute. This is the most tempting alternative
         and the most damaging: it makes “does this justify the claim” and “did this cause the step” two values of one
         field, so the projection π of Section C can no longer be defined by edge label, and P3 (that procedural influence


                                                               33
                                               From Agent Traces to Trust


         has no image under π) becomes unstatable. The separation of evidence tracing from execution provenance
         depends on the distinction being carried by the edge type.
      3. A finer decomposition, splitting S UPPORT into entailment, paraphrase, and partial support, or U SE into
         reading and parameterizing. Each split is a refinement of a single decision test rather than a new one, and the
         resulting distinctions are already carried by edge attributes and by the threshold θ of Table 11. Splitting them
         raises annotation burden and lowers inter-annotator agreement without letting the graph answer a query it
         could not answer before.
      4. Merging T RIGGER into D EPEND - ON, on the view that both are counterfactual. They are, but over different
         questions (occurrence versus parameterization), and runtime enforcement acts on the first while information-
         flow tracking acts on the second, so the merge would erase the boundary between the two guardrail families
         surveyed in Section 4.

Candidate relations considered and excluded. Six further candidates were considered while constructing the set and
excluded, each on one of the two tests rather than by oversight. F OLLOWS, a temporal-succession edge, fails distinctness:
order is already carried by node timestamps, and adjacency establishes no semantic, causal, or procedural dependence
(Section B.3). C ITED and O MITTED fail necessity: both are predicates derived from the nine, and Section B.5 defines
them in those terms rather than as edges of their own. R ETRIEVED - FROM fails distinctness: a retrieval is an execution
unit, so the edge it would add is already U SE on the query and G ENERATE on the returned passage. R ESPONSIBLE - FOR
and AUTHORIZED - BY fail necessity only under the current corpus, in which delegation and policy are expressed
indirectly; they are the two candidates we regard as open, and the next paragraph states the test they would have to pass.

What we do not claim. The set is not proved minimal in any formal sense, and minimality is not a property a relation
vocabulary can have absolutely. It is minimal relative to two things we state: the six trust functions of Section 2.1, and
the corpus of Section ??. A different set of trust functions would admit a different set: provenance for cost accounting
or for licensing compliance would need relations we do not have. Accordingly, we give the admission test rather than
close the vocabulary: a tenth relation is warranted when it answers a trust-function query that no combination of the
nine answers, and its decision test is not a refinement of one already listed in Table 11. Two candidates we regard as
open are an explicit authorization relation linking an action to the policy that permitted it, and a responsibility relation
for multi-agent delegation; both are currently expressed indirectly, and Section 7 treats them as such.

C     The Evidence-Tracing Projection
This appendix is new in this revision. Because it is new in its entirety, it is not marked sentence by sentence.
Section 1 describes evidence tracing as the projection of execution provenance onto its evidence-support relations,
together with the content-derivation links that connect them. This section states what that means precisely, so that the
claim is checkable rather than metaphorical. One consequence is worth flagging at the outset: π(G) is not a subgraph of
G. It retains a subset of G’s edges, but it also adds a layer of explicitly labelled S UPPORT- CANDIDATE edges recording
content flow that no semantic edge has yet adjudicated. Evidence tracing is a sub-problem of execution provenance in
the sense that it answers a strictly weaker question, not in the sense that its graph is contained in the larger one.

C.1   Definition

An execution provenance graph of a single agent run is a typed attributed directed multigraph
                                                 G = (V, E, τ, λ, α),
where V is the set of nodes; τ : V → T assigns each node a type from the vocabulary of Table 9, inducing the
partition V = E ⊎ X ⊎ A into evidence units, execution units, and actors; E is an abstract set of edges with endpoint
maps src, tgt : E → V , so that one ordered pair of nodes may carry several edges (a passage can both D ERIVE
and S UPPORT the same claim, a tool call can both U SE and D EPEND - ON the same parameter, and, crucially, two
edges may share a label and differ only in origin, which is how a citation the agent D ECLARED and an annotator
subsequently I NFERRED is recorded as two S UPPORT edges rather than one); λ : E → R+ labels each edge, where
R+ = R ∪ {S UPPORT- CANDIDATE} extends the nine relations with the derived label introduced below, subject to the
signature constraints of Table 10. An execution provenance graph produced by instrumentation or annotation carries no
S UPPORT- CANDIDATE edge; the label exists so that π’s output lies in the same class as its input, and it has signature
E → C, is asymmetric, and carries a temporal requirement inherited from the D ERIVE, U SE and G ENERATE edges of
its witness path; and α assigns attributes to nodes and edges, including timestamps, actor identity, content or content
hash, trust and taint labels, and the origin and assurance values of Section B.4.


                                                            34
                                               From Agent Traces to Trust


Partition the relation vocabulary into
                     Rsem = {S UPPORT, C ONTRADICT, I NVALIDATE},                Rder = {D ERIVE},
                    Rproc = {U SE, G ENERATE, D EPEND - ON, T RIGGER, U PDATE}.

Here Rproc groups the causal and procedural families of Appendix B.3 together, because the projection treats them
alike; the two remain distinct relation families everywhere else in the paper.
The evidence-tracing projection is the map π sending G to the evidence view π(G) = (V ′ , E ′ , τ ′ , λ′ , α′ ). All five
clauses below are evaluated against the input graph G; in particular clause 3 reads procedural edges of G before clause 2
removes them, so no clause depends on the output of another.

      1. Edges retained verbatim. Ekeep = { e ∈ E : λ(e) ∈ Rsem ∪ Rder ∪ {S UPPORT- CANDIDATE} }. The last
         disjunct is vacuous on an instrumented graph; together with clause 3’s crossing requirement it is what makes π
         idempotent.
      2. Edges discarded. No edge with λ(e) ∈ Rproc appears in E ′ .
      3. Contracted candidate paths. Call a path of G a content-flow path when every one of its edges is a D ERIVE
         edge traversed forwards, a G ENERATE edge traversed forwards from an activity to the artifact it produced, or a
         U SE edge traversed backwards from a consumed artifact to the activity that consumed it, and at least one of its
         edges is a U SE or G ENERATE edge, so that the path passes through the execution layer. For d ∈ E and c ∈ C,
         set Ecand , a set of fresh edge identities disjoint from E, to contain a derived edge S UPPORT- CANDIDATE(d, c)
         whenever G contains a content-flow path from d to c and no edge of Rsem already runs from d to c (a
         symmetric C ONTRADICT between them does not block, since contradicting is not adjudicating support). A
         candidate exists to flag content flow that has not yet been adjudicated, so an adjudicated pair needs none. Such
         an edge records that d could have contributed content to c; it is an availability statement, and it is deliberately
         not a S UPPORT edge. Requiring a content-flow path to cross the execution layer is the second half of what
         makes π idempotent: a chain of D ERIVE edges alone is already in the evidence view and must generate no
         candidate.
      4. Nodes retained. V ′ = E ∩ endpoints of Ekeep ∪ Ecand , together with any execution unit that is the target
                                                                       
         of a retained S UPPORT or I NVALIDATE edge, since justifying an action, and recording that its precondition no
         longer holds, are both evidence-tracing questions. No retained edge is therefore left dangling.
      5. Attributes retained. Content, content hash, timestamps, trust labels, origin, assurance, and, on S UPPORT-
         CANDIDATE edges, a witness identifier are kept. Scoping the witness by label rather than by which clause
         admitted the edge is what keeps π idempotent on attributes as well as on structure: on a second application
         such an edge arrives through clause 1, not clause 3, and must not lose its witness. Execution-specific attributes
         are dropped: actor identity, latency, permission scopes, retry counts, and tool manifests. The witness identifier
         names one content-flow path of G that licenses the edge; when several paths license the same edge the
         witness names one of them, so recovery of G from π(G) is partial by design. A contracted edge takes
         origin = D ERIVED, the fourth origin value of Section B.4, since it is computed from G rather than logged,
         judged, or asserted.

The components of the output are then E ′ = Ekeep ∪ Ecand , with τ ′ , λ′ and α′ the restrictions of τ , λ and α to V ′ and
E ′ , extended on Ecand by λ′ (e) = S UPPORT- CANDIDATE and the attributes just listed.

C.2   Properties
P1 (Information loss; π is not injective). Many distinct execution graphs have the same evidence view. Two runs that
        reach the same claims from the same evidence through different tool calls, different orderings, or different
        agents are indistinguishable under π. Consequently evidence tracing cannot recover execution provenance:
        the support view is strictly weaker than the process view, which is why a survey of one is incomplete without
        the other.
P2 (Groundedness). Every edge of π(G) is licensed by G: each retained edge is an edge of G, and each contracted
        edge is witnessed by at least one content-flow path of G. In particular π asserts no S UPPORT edge that is
        not already asserted in G; the edges it adds carry the distinct label S UPPORT- CANDIDATE precisely so that
        availability is never read as support.
P3 (Not all influence is evidence). No edge labelled in Rproc survives π. The consequential case is the two influence
        relations, D EPEND - ON and T RIGGER: this is the formal content of the distinction between supporting a
        conclusion and merely influencing it, since influence without semantic support is present in G and absent from


                                                            35
                                               From Agent Traces to Trust


        π(G) by construction. U SE, G ENERATE, and U PDATE are also discarded, but they are bookkeeping rather than
        influence claims, and U SE and G ENERATE survive indirectly as witnesses of contracted edges. The exclusion
        is a design choice, not an omission: the evidence view answers what justifies this, the process view answers
        what caused this. A system that reports only π(G) cannot answer safety questions, and a system that reports
        only Rproc cannot answer grounding questions.
P4 (Idempotence). π(π(G)) = π(G). Clause 1 retains Rsem , Rder and S UPPORT- CANDIDATE edges, which is every
        label present in an evidence view, so nothing is lost; clause 2 removes nothing, since no Rproc edge survives
        the first application; and clause 3 adds nothing, since a content-flow path requires a U SE or G ENERATE edge
        and the evidence view contains none. This last point is why clause 3 requires the path to cross the execution
        layer: without that requirement a bare chain of D ERIVE edges would generate a fresh candidate on every
        application and π would not converge.

We use projection in this structural sense: π is a total, idempotent, information-losing map from typed provenance
graphs to typed evidence graphs that preserves the semantic sub-structure. We do not claim it is a projection in a
categorical sense, and no result in this survey depends on stronger properties.

C.3   Worked Example

Table 14 applies the definition to the running example of Figure 3. We list the twenty edges on which the projection
acts. The generator of the recovery-phase artifact a′ , and the memory item that the write w produces, are elided; note
that this is a simplification of the example rather than of the definition, since supplying a′ with a generator and an input
would add further candidate edges into a′ . Of those twenty the evidence view retains seven, discards thirteen, and adds
four contracted candidates.
The example makes the division of labour concrete. The evidence view alone shows an auditor that the final answer
rested on a claim supported partly by a memory item that was later contradicted and whose warrant was invalidated, an
attribution failure. It does not show that the call was triggered by that claim, or that its parameterization depended on
the argument derived from it, which is the fact a safety analyst needs. Neither view subsumes the other, and this is
exactly why the survey treats execution provenance as the full graph and evidence tracing as its projection.

D     Benchmark Catalogue and Coverage Details
This appendix is new in this revision. Because it is new in its entirety, it is not marked sentence by sentence.
This appendix derives every cell of the coverage heatmap from the benchmark catalogue of Table 7, and states the
annotation protocol under which that catalogue was coded. The main text uses Figure 5 to emphasize coverage gaps;
Table 15 shows the computation itself, so that a reader can reproduce or contest any rating without relying on our
judgement. The per-benchmark entries are not repeated here: the catalogue is Table 7 in Section 6, and this appendix
adds only what the main text does not carry: the derivation and the protocol.

D.1   Derivation of the Coverage Heatmap

Figure 5 is derived from Table 7 rather than assigned by judgement. For the five capabilities that appear as columns
in the catalogue (evidence labels, tool calls, memory, multi-agent structure, and safety attacks), a family’s rating is
the maximum over its member benchmarks under the mapping Yes → S, Partial / Task-dependent / State-based → P,
No → L.
The maximum is the right aggregator because each cell states an existential claim (does any benchmark in this family
evaluate this capability?), and it has two consequences a reader should keep in view. First, the heatmap is an optimistic
upper bound: a family rated S typically contains members rated L for the same capability. Second, families differ in
size, from two members to nine, so a maximum is easier to attain in a large family; each cell of Table 15 therefore also
reports how many members attain the rating. The L cells are the size-robust signal and the ones the survey’s argument
rests on: an L means no member covers the capability, which cannot be an artifact of family size.
The catalogue’s remaining column, trace availability, has no heatmap counterpart. It is a precondition for evaluating any
of the seven capabilities rather than a capability in its own right, so we report it per benchmark in Table 7 and do not
aggregate it.
Two capabilities have no catalogue column and are coded directly from the released artifacts by a countable criterion.
Provenance relations is rated by how many of the nine relations of Section B.2 a benchmark releases as ground-truth
labels: S for three or more, P for one or two, L for none. Citation benchmarks label S UPPORT and nothing else; taint


                                                            36
                                              From Agent Traces to Trust


Table 14: The projection applied to the running example of Figure 3. Nodes: q user query, r retrieval call, p retrieved
passage, m memory item, z1 claim-forming reasoning step, c intermediate claim, g generated tool parameter, k tool
call, o tool output, z2 answer-forming reasoning step, a final answer, n new external evidence, w memory write, a′
revised answer.
Edge in G                               In π(G)?        Why
 T RIGGER(q, r)                          Dropped        Procedural: governs whether retrieval happened.
 G ENERATE(r, p)                         Dropped        Activity-to-artifact bookkeeping. It carries no edge into π(G), but
                                                        may appear inside the witness path of a contracted edge.
 U SE(z1 , p), U SE(z1 , m)              Dropped        Availability, not support.
 G ENERATE(z1 , c)                       Dropped        Activity-to-artifact.
 D ERIVE(p, c)                            Kept          Content of the claim is a transformation of the passage.
 S UPPORT(p, c)                           Kept          Passage content warrants the claim.
 S UPPORT(m, c)                           Kept          Memory content warrants the claim; later invalidated, see below.
 D ERIVE(c, g)                            Kept          Tool argument derived from the claim’s content.
 T RIGGER(c, k)                          Dropped        Governs whether the tool was called.
 U SE(k, g)                              Dropped        The call consumed the parameter; recorded, not judged.
 D EPEND - ON(k, g)                      Dropped        Governs how the call was parameterized. This edge is essential for
                                                        the tool-use safety question and invisible in the evidence view.
 G ENERATE(k, o)                         Dropped        Activity-to-artifact.
 U SE(z2 , o), G ENERATE(z2 , a)         Dropped        Answer construction: procedural bookkeeping.
 S UPPORT(o, a)                           Kept          Tool output warrants the final answer.
 C ONTRADICT(n, m)                        Kept          New evidence conflicts with the memory item.
 I NVALIDATE(n, c)                        Kept          New evidence removes the claim’s warrant.
 T RIGGER(n, w), U PDATE(a′ , a)         Dropped        Procedural recovery and state succession.
 S UPPORT- CANDIDATE(p, a)               Added          Witness:
                                                           D ERIVE   D ERIVE   U SE    G ENERATE    U SE    G ENERATE
                                                        p −−−−→ c −−−−→ g ←−− k −−−−−→ o ←−− z2 −−−−−→ a. The
                                                        passage is a possible content contributor to the answer; whether it
                                                        supports the answer is a separate judgement.
 S UPPORT- CANDIDATE(m, a)               Added          Same shape, witnessed through m → z1 → c → · · · → a. Read
                                                        together with I NVALIDATE(n, c), this is the edge that tells an auditor
                                                        a discredited memory item may have reached the answer.
 S UPPORT- CANDIDATE(c, a),              Added          The claim and the tool parameter derived from it are also content
 S UPPORT- CANDIDATE(g, a)                              contributors to the answer.
 S UPPORT- CANDIDATE(p, c),             Not added       Blocked by clause 3: S UPPORT(p, c), S UPPORT(m, c) and
 S UPPORT- CANDIDATE(m, c),                             S UPPORT(o, a) already adjudicate these pairs.
 S UPPORT- CANDIDATE(o, a)




benchmarks label source-to-sink influence, which is evidence for D EPEND - ON and nothing else; trace-debugging
benchmarks label the responsible step, which is evidence for T RIGGER and nothing else. Relations recoverable from
a call log but never labelled (U SE and G ENERATE) do not count, because an unlabelled relation supplies no ground
truth. Recovery is rated S only when a benchmark scores repair outcomes; it is P when the benchmark scores something
adjacent to repair, namely superseding stale memory, localizing the failure that a repair would target, or blocking an
unsafe action before it executes, and L otherwise. Under these criteria no family reaches S in either column, which are
therefore the sharpest gaps the heatmap records.
Table 15 gives the resulting derivation. The determining member is the benchmark that attains the family maximum;
where several members tie we name them, up to four, and otherwise indicate the count.
Three observations follow from the derivation that are not visible in the heatmap itself. First, five of the six families
reach S on exactly one capability and are P or L everywhere else. For four of the five that capability is the one the
family was built for; the exception is the trace-debugging family, whose only S is in the multi-agent column and is
inherited from MAST, which belongs to both families. Second, the exception is the provenance/security family, which
reaches S on three capabilities and is the only family with no L cell; but it is also the largest at nine members, two of
its three S ratings are unanimous while the third rests on a single member, and it never reaches S on evidence labels
or recovery. Third, and most consequentially, no family reaches S on provenance relations or on recovery. Every
rating above L in those two columns is carried by a benchmark labelling exactly one relation (S UPPORT in citation
benchmarks, D EPEND - ON in taint benchmarks, T RIGGER in trace-debugging benchmarks), or by an artifact adjacent to


                                                           37
                                                                        From Agent Traces to Trust


Table 15: Cell-by-cell derivation of Figure 5 from Table 7. Each entry gives the rating, the number of family members
attaining it out of the family size, and the determining member. Entries marked “—” have no member above L. Ratings
attained by a single member of a large family, such as memory coverage in the provenance/security family at 1/9, should
be read accordingly.
Family                  Evidence labels           Tool calls             Memory                  Multi-agent             Safety attacks         Prov. relations         Recovery

RAG (7)                 S     4/7  (FActScore, L 0/7 (—)              L 0/7 (—)                  L 0/7 (—)               L 0/7 (—)              P (S UPPORT only)       L (—)
                        ALCE, SourceCheckup,
                        RAGTruth)
Tool-use (4)            L 0/4 (—)              S 3/4 (WebArena, Tool- P 2/4 (AgentBench L 0/4 (—)                        P 1/4 (τ -bench policy L (none labelled)       L (—)
                                               Bench, τ -bench)       task-dep.; τ -bench state-                         checks)
                                                                      based)
Memory (2)              P 2/2 (LoCoMo, Memor- P 1/2 (MemoryArena S 2/2 (LoCoMo, Memor- L 0/2 (—)                         L 0/2 (—)              P (session-level S UP - P       (superseding
                        yArena)                task-dep.)             yArena)                                                                   PORT references)         stale items; repair
                                                                                                                                                                         unscored)
Multi-agent (2)         P 1/2 (AgenTracer/Aegis) P 2/2 (MAST, Agen- P 2/2 (MAST, Agen- S 2/2 (MAST, Agen- L 0/2 (—)                             P (responsible step, ev- L (—)
                                                 Tracer task-dep.)   Tracer task-dep.)   Tracer/Aegis)                                          idencing T RIGGER)
Trace-debugging (2)     P 1/2 (TRAIL)            P 2/2 (TRAIL, MAST) P 2/2 (TRAIL, MAST) S 1/2 (MAST)     L 0/2 (—)                             P (error location on P          (localization
                                                                                                                                                trace steps)             only; repair un-
                                                                                                                                                                         scored)
Provenance / security (9) P 3/9 (OpenAgentSafety, S 9/9 (all members)    S 1/9 (NeuroTaint/Taint- P      4/9    (OpenA- S 9/9 (all members)     P       (source-to-sink P (blocking, not re-
                          Agent-Sentry,   Neuro-                         Bench)                   gentSafety,     MCP-                          influence, evidencing pair)
                          Taint)                                                                  SafetyBench, Neuro-                           D EPEND - ON)
                                                                                                  Taint, AgentSpec)




repair rather than repair itself. No benchmark in the catalogue releases the typed relation vocabulary as ground truth,
and none scores recovery. This is the concrete form of the gap that Section 7 argues future benchmarks should close.

D.2       Annotation Protocol for the Coverage Ratings

Three rating schemes appear in this survey: the S/P/L coverage ratings of Figure 5, the memory-capability symbols
of Table 5, and the benchmark-capability symbols of Table 7. They share one annotation protocol, stated here so that
a reader can re-derive a cell or contest it against the artifact rather than against our judgement. The heatmap is not
annotated at all: it is computed from the catalogue by the rule of Section D.1, so the protocol below governs only the
per-artifact tables from which it is computed, and correcting a catalogue cell propagates to the heatmap automatically.

Unit of coding and evidence admitted. The unit is a single (artifact, capability) pair: one benchmark or system, one
column. Evidence is admitted in a fixed order of precedence, and the first level that decides the cell ends the search: (i)
the released dataset, repository, or evaluation harness; (ii) the artifact’s own paper, including its appendices; (iii) its
documentation. The ordering is what makes the ratings checkable, and it has one consequence worth stating plainly: a
capability claimed in prose but with no released label or trace never yields the top rating. We code what an artifact
makes available to a third party, not what it reports about itself. Where an artifact was not publicly released at the time
of coding, it is coded from its paper alone and can attain at most the middle rating.

Decision procedure. Each cell is decided by the following four steps in order, which is what allows two coders to
converge:

          1. Ground truth? Does the artifact release per-instance labels for the capability and report a metric computed
             over them? If yes, the cell takes the top rating (✓ / ✓ / S) and coding stops.
          2. Present but unlabelled? Does the capability appear in the released traces or the system’s behaviour without
             ground-truth labels, or is it labelled for only a subset of instances, only at run level, or only for some memory
             types? If yes, the cell takes the middle rating (• / ▲ / P).
          3. Structural qualifier? Two values are not degrees of coverage but statements about how the capability is
             realized, and are applied before the negative rating: T when coverage varies across the artifact’s own task suite
             rather than across instances, and S when the capability exists as external environment state rather than as an
             agent-side artifact. ★ is the corresponding value for a work that studies a capability adversarially rather than
             providing it, and ❍ for a system that exposes the information from which the capability could be built but
             does not implement it.
          4. Otherwise the cell takes the negative rating (✗ / ❍ or ✗ / L).

Where the middle and negative ratings divide. The step that decides most contested cells is the boundary between
the middle rating (• / ▲ / P) and the negative one (✗ / ❍ or ✗ / L), and it is worth stating on its own because the two
labels are easy to read as degrees of the same thing. They are not. The middle rating is a claim that the capability
is present in what the artifact releases but is not ground truth: the traces contain it unlabelled, or it is labelled for


                                                                                         38
                                               From Agent Traces to Trust


only some instances, or realized in a form the column does not name. The negative rating is a claim that it is not
there to be found: for a benchmark, neither labels nor recoverable traces are released; for a system, the capability is
not implemented. The operational test is therefore not “how much coverage is there” but “could a third party extract
this from the release at all”. One consequence is that L is the falsifiable direction: a single released file showing the
capability overturns an L, whereas overturning a P requires showing that a metric is computed over labels, which is the
step 1 test. This is why Section D.1 treats the L cells as the size-robust signal on which the survey’s argument rests, and
why ❍ in Table 5 is worded as “exposes the information but does not implement it” rather than as weak support.

Two worked cells. Applying the procedure to two cells that could plausibly have been coded either way shows where
the steps bite.
ALCE, evidence labels → ✓. Step 1 asks for per-instance ground truth and a metric over it. ALCE releases per-claim
citation annotations and reports citation precision and recall computed from them [Gao et al., 2023], so both halves hold
and coding stops at step 1. Had it released the annotations without scoring them, step 1 would fail and step 2 would
give •, since the distinction is the metric, not the labels.
τ -bench, memory → S. The benchmark carries information across turns, so a coder might record ✓ or •. Step 1 fails:
nothing about memory is labelled per instance. Step 2 is the tempting one, but what persists is the environment database
the tools read and write, not an agent-side memory item [Yao et al., 2025]; the capability exists, yet not as the artifact
the column is about. Step 3 therefore applies and the qualifier S records both facts at once: present, but realized as
external state. It maps to P in the heatmap, so the family rating is unaffected; what the qualifier preserves is why, which
a bare P would discard.

Scope and known limits of the protocol. The protocol codes the presence of a capability, never its quality: a
benchmark with weak evidence labels and one with strong labels are both ✓, and the survey makes no claim about
which is better. Three limits follow. First, coding was performed by the authors jointly, with disagreements resolved by
discussion against the released artifact; there was no independent second coder and we therefore report no inter-coder
agreement, which is the same limitation recorded for the corpus in Section ??. Second, the ratings are a snapshot: they
reflect the artifact versions available at the time of writing, and a subsequent release can change a cell. Third, step 1
turns on whether a metric is computed over the labels, which is the step at which we expect residual disagreement, and
it is the step a reader should check first when contesting a cell.
What the protocol does achieve is a change in what a disagreement is about. Under a family-level rating assigned by
judgement there is no rule to violate, and a reader who doubts a cell has nothing to check; under this protocol every
rating is a claim about a specific released artifact, and a single counterexample, such as a labelled file or a metric in a
results table, overturns it.


E     Additional Details for Open Problems

This appendix expands the open problems discussed in Section 7. It is deliberately not a restatement: the main text
makes the argument for each open problem and cites the work that motivates it, while this appendix carries in table
form only the artifact the argument implies: a requirements checklist an implementer or benchmark designer can work
from. Where a requirement here restates a sentence of Section 7, the table row is the operational version of it, and a
reader following the argument alone can skip this appendix without loss. The main text presents the research agenda;
this appendix provides more detailed design requirements, representative foundations, and evaluation dimensions.

E.1   Trace Schema Requirements

A unified LLM-agent provenance schema should combine operational execution records with semantic evidence
relations. Table 16 summarizes the main schema requirements.
Existing standards and frameworks provide partial foundations. W3C PROV-DM defines general provenance concepts
such as entities, activities, agents, generation, usage, derivation, and invalidation [World Wide Web Consortium, 2013].
OpenTelemetry provides distributed tracing abstractions, while OpenLineage provides data workflow lineage [Open-
Telemetry, 2026, OpenLineage Contributors, 2026]. AgentOps and AgentTrace move closer to LLM-agent observability
by recording structured agent artifacts and execution context [Dong et al., 2024, AlSayyad et al., 2026]. PROV-AGENT
adapts provenance modeling to agentic workflows [Souza et al., 2025]. However, LLM-agent provenance requires addi-
tional semantic units and relations, especially generated claims, evidence support, contradiction, memory invalidation,
tool-argument influence, and inter-agent responsibility.


                                                            39
                                               From Agent Traces to Trust


                     Table 16: Design requirements for unified LLM-agent provenance schemas.

Requirement           What should be represented                          Why it matters
Trace sources       User instructions, model outputs, retrieval calls, tool Enables end-to-end reconstruction of agent execu-
                    calls, memory operations, environment observations, tion.
                    inter-agent messages, and final responses.
Evidence units      User queries and instructions, documents, passages, Supports claim-level verification and attribution.
                    observations, tool outputs, memory items, generated
                    tool parameters, policies, tool manifests, inter-agent
                    messages, intermediate claims, and final answers.
Execution units     Reasoning steps, retrieval calls, tool invocations, Supports debugging, safety enforcement, and audit.
                    memory reads and writes, environment actions, and
                    delegation steps.
Typed relations     S UPPORT, C ONTRADICT, D EPEND - ON, D ERIVE, Turns raw logs into provenance graphs that expose
                    T RIGGER, U PDATE, I NVALIDATE, U SE, and G EN - influence and responsibility.
                    ERATE .
Trust metadata      Source trust, permission scope, confidentiality/in- Enables runtime enforcement, privacy-aware audit,
                    tegrity labels, timestamps, actor identity, and policy and governance.
                    constraints.
Replay and recovery Checkpoints, rollback targets, invalidation events, Supports intervention and recovery, not only post-
fields              repair steps, human approvals, and state-change hoc explanation.
                    records.



E.2   Detailed Agenda for Semantic and Claim-Level Provenance

Claim-level provenance should distinguish at least five conditions that are often conflated in current systems: citation
presence, source relevance, claim support, contradiction, and evidence omission. Only support and contradiction are
taxonomy relations; citation presence and omission are the derived predicates of Appendix B.5, and source relevance is
weaker than any of them. ALCE, FActScore, RAGTruth, RAGChecker, SourceCheckup, and related attribution surveys
provide foundations for this direction [Gao et al., 2023, Min et al., 2023, Niu et al., 2024, Ru et al., 2024, Wu et al.,
2025, Schreieder et al., 2026]. However, agentic settings introduce additional challenges because evidence may be
transformed by reasoning, retrieval, tools, memory, reflection, or inter-agent communication before it influences the
final answer or action.
Future work should therefore evaluate not only whether a final claim is supported, but also how the supporting
information traveled through the execution. Important cases include: a claim derived from multiple retrieved passages;
a tool output that contradicts a memory item; a memory item summarized from a previous conversation; a policy
constraint that justifies or blocks an action; and an inter-agent message that propagates an unsupported assumption.
Semantic taint and causal influence methods such as NeuroTaint suggest one path toward tracing transformed influence,
but robust semantic provenance remains open [Cai et al., 2026].

E.3   Memory and Multi-Agent Provenance Checklist

Table 17 lists provenance fields that future memory and multi-agent systems should expose.
Memory systems should not treat long-term memory as a generic context store. Memory items should carry lineage,
validity, trust, and downstream-use metadata, especially when they affect tool calls, personalization, or long-horizon
decisions. Memory poisoning and memory-injection attacks highlight the need to trace how compromised memory
influences later executions [Chen et al., 2024, Dong et al., 2025]. Multi-agent systems require a parallel form of
message-level provenance. In workflows built from delegation, critique, verification, and role specialization, provenance
should identify not only which final answer was wrong, but which agent introduced the unsupported claim, which agent
failed to verify it, and which message propagated it [Wu et al., 2024, Li et al., 2023, Cemri et al., 2026, Zhang et al.,
2026, Kong et al., 2025].

E.4   Runtime Safety and Recovery Requirements

Runtime provenance should support both enforcement and repair. Table 18 summarizes the distinction.
Most current systems focus on detection, blocking, or policy enforcement. A stronger provenance-aware runtime should
support intervention. For example, if a tool argument is derived from untrusted web content, the system should not


                                                            40
                                                 From Agent Traces to Trust


                              Table 17: Checklist for memory and multi-agent provenance.

Setting                 Provenance fields                                    Open question
Memory write           Source, timestamp, writer, evidence basis, confi- Was the memory created from trusted evidence or
                       dence, and policy context.                           from unsupported/injected content?
Memory update          Previous version, update source, update reason, con- Does the update revise, contradict, or invalidate ear-
                       flict status, and invalidation marker.               lier memory?
Memory retrieval       Retrieval query, retrieved memory items, ranking Why was this memory reused, and how did it affect
                       score, context of reuse, and downstream consumer. the current execution?
Memory deletion or in- Deletion trigger, invalidating evidence, affected Can stale or poisoned memory be removed without
validation             downstream claims/actions, and recovery steps.       breaking auditability?
Inter-agent communi- Sender, receiver, role, message content, cited evi- Which agent introduced, verified, reused, or ampli-
cation                 dence, delegated task, and verification status.      fied a claim?
Multi-agent failure    Responsible agent, responsible step, error mode, Where did the failure originate, and how did it prop-
                       propagated message, and counterfactual trajectory. agate across agents?

                  Table 18: Runtime safety and recovery requirements for provenance-aware agents.

Capability             Provenance requirement                                Representative foundations
Prompt-injection de- Identify whether untrusted external content influ- InjecAgent, AgentDojo, ToolEmu [Zhan et al., 2024,
tection               ences privileged instructions, tool calls, or memory Debenedetti et al., 2024, Ruan et al., 2024]
                      updates.
Information-flow con- Track confidentiality and integrity labels across in- CaMeL, FIDES [Debenedetti et al., 2026, Costa et al.,
trol                  puts, tools, memory, and outputs.                       2025]
Semantic taint track- Trace influence through summarization, paraphras- NeuroTaint [Cai et al., 2026]
ing                   ing, reasoning, and memory consolidation.
Argument verifica- Check whether sensitive tool arguments derive from Agent-Sentry [Sequeira et al., 2026]
tion                  trusted sources or explicit user intent.
Execution bounding Enforce tool permissions, access boundaries, and AgentSpec, AgentBound [Wang et al., 2026, Bühler
                      policy constraints at runtime.                          et al., 2026]
Recovery              Invalidate stale memory, quarantine contaminated Open problem building on provenance enforcement
                      evidence, retry tool calls, request approval, roll back and trace debugging.
                      state changes, or replay from safe checkpoints.



only block the action but also identify the contaminated source, remove the derived parameter, request confirmation,
and prevent the same contamination from being written into memory. If a memory item is later contradicted by new
evidence, the system should invalidate the memory and identify downstream claims or actions that depended on it.
These recovery operations require provenance graphs that preserve dependencies across evidence, tools, memory, state
changes, and actions.

E.5   Benchmark and Governance Requirements

Future benchmarks should evaluate provenance as a first-class object rather than as an implicit by-product of task
success. Table 19 summarizes the main benchmark and governance requirements.
Existing benchmark families provide partial foundations. RAG and attribution benchmarks support evidence grounding;
tool-use and safety benchmarks expose tool calls, unsafe actions, and prompt-injection risks; memory benchmarks
evaluate recall and personalization; multi-agent benchmarks evaluate coordination and failure modes; and trace-
debugging benchmarks support failure localization [Gao et al., 2023, Ru et al., 2024, Wu et al., 2025, Liu et al., 2024,
Zhou et al., 2024, Ruan et al., 2024, Debenedetti et al., 2024, Yao et al., 2025, Vijayvargiya et al., 2026, Zong et al.,
2026, Maharana et al., 2024, He et al., 2026, Deshpande et al., 2025, Cemri et al., 2026, Zhang et al., 2026, Kong et al.,
2025]. The remaining gap is end-to-end evaluation of provenance chains that connect evidence and tool outputs to
memory updates, intermediate claims, final answers, external state changes, and recovery actions.
Privacy and governance should be evaluated together with provenance quality. Provenance traces can contain sensitive
user information, confidential documents, credentials, API arguments, internal reasoning artifacts, and long-term
memory items. Observability systems such as AgentOps and AgentTrace provide foundations for trace collection [Dong
et al., 2024, AlSayyad et al., 2026], while FIDES highlights confidentiality and integrity constraints [Costa et al.,
2025]. Future systems should additionally support trace minimization, access control, anonymization, retention policies,


                                                               41
                                                From Agent Traces to Trust


                        Table 19: Requirements for realistic provenance benchmarks and governance.

Requirement                Current limitation                                Future benchmark target
Full execution traces  Existing benchmarks often capture only answers, Capture retrieval, tools, memory, environment
                       tool calls, attacks, memory retrieval, or failure la- states, inter-agent messages, claims, actions, and
                       bels.                                                 state changes.
Relation annotations   Provenance relations are rarely labeled directly.     Annotate the nine typed relations, and separately
                                                                             flag unsafe influence and recovery intervention,
                                                                             which are properties of an execution rather than
                                                                             relations.
Cross-component cover- RAG, tool-use, memory, and multi-agent bench- Evaluate how evidence, tools, memory, messages,
age                    marks usually evaluate isolated capabilities.         and state changes jointly affect final outputs and
                                                                             actions.
Recovery evaluation    Benchmarks usually test success, failure, hallucina- Test whether agents can repair traces by invalidat-
                       tion, or unsafe action.                               ing memory, quarantining evidence, retrying tools,
                                                                             requesting approval, or rolling back unsafe actions.
Privacy-aware tracing Traces may expose confidential documents, creden- Require minimization, anonymization, access con-
                       tials, API arguments, memory items, and internal trol, encryption, retention policies, and selective
                       reasoning artifacts.                                  disclosure.
Audit and governance Trace collection alone does not guarantee account- Evaluate whether traces are inspectable, policy-
                       ability.                                              compliant, comparable, and usable for audit.


encryption, and selective disclosure so that provenance infrastructure does not itself become a privacy or compliance
risk.




                                                              42
