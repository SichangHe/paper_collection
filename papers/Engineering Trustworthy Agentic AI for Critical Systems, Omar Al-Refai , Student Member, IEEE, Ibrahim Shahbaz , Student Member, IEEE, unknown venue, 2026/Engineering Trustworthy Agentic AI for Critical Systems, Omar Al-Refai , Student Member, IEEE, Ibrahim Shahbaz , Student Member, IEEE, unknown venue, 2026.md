                                                       Engineering Trustworthy Agentic AI for Critical Systems
                                                         Omar Al-Refai , Student Member, IEEE, Ibrahim Shahbaz , Student Member, IEEE,
                                                      Adam Ali Husseinat , Member, IEEE, Michael Mandulak , Jaewon Kim , Member, IEEE,
                                                                             Eman Hammad , Senior Member, IEEE



                                            Abstract—Agentic artificial intelligence systems, capable of                         Act) [2], self-reflective agents (e.g., Reflexion) [3], delibera-
                                         autonomous perception, planning, tool use, and multi-step action,                       tive search over intermediate reasoning steps (e.g., Tree-of-
                                         are increasingly proposed for critical engineering domains where                        Thoughts) [4], and multi-agent LLM-based systems capable
                                         decisions carry physical, operational, or economic consequences.
                                         This survey addresses a gap in current literature by treat-                             of communication and task decomposition. Collectively, these
                                         ing trustworthiness, whether agentic behavior can be verified,                          approaches mark a shift from passive AI components toward
                                         audited, and trusted under the constraints that engineering                             autonomous, goal-directed systems that can adapt, plan, and
                                         practice actually requires, as a first-class engineering property,                      act in complex environments. Although these capabilities
                                         rather than evaluating agentic AI by task capability alone.                             have shown promise in various domains, their implementa-
                                         The study adopts a trustworthiness model organized around
                                         five cross-cutting dimensions: safety and constraint satisfaction;                      tion in critical infrastructure systems such as power grids,
                                         robustness and reliability; transparency and interpretability;                          autonomous vehicles and robotic platforms, high-performance
                                         accountability and auditability; and privacy and security. This is                      computing facilities, and communication networks presents
                                         mapped onto an agentic assurance workflow spanning perception                           fundamental trustworthiness challenges [5]. Failures in these
arXiv:2607.18548v1 [cs.AI] 20 Jul 2026




                                         through audit. Building on this foundation, agentic systems ar-                         environments can cause cascading outages, physical harm,
                                         chitectures, threats, concrete trust mechanisms, and quantitative
                                         metrics are surveyed for direct application in agentic systems                          financial loss, or safety hazards to the public and human
                                         development and evaluation. These principles are then exam-                             operators, in addition to performance degradations [6], [7].
                                         ined across four constraint-bound engineering domains: power                               Trust in agentic AI is an existential requirement rather
                                         systems, autonomous vehicles/robotics/UAVs, high-performance                            than an auxiliary concern, requiring autonomous agents to
                                         computing, and communication networks, identifying recurring                            consistently respect operational constraints, maintain resilience
                                         design patterns, shared failure modes, and domain-specific gaps.
                                         Synthesizing across those domains, agentic AI trustworthiness                           against adversity and uncertainty, provide transparency into
                                         is shown to be a single problem, with a path outlined toward                            decision-making processes, facilitate accountability and au-
                                         a reusable, cross-domain assurance framework analogous to                               ditability, and prevent abuse or unintentional escalation. Agen-
                                         the graded certification regimes used by mature safety-critical                         tic AI systems, in contrast to traditional automation, can create
                                         engineering fields.                                                                     and execute new action sequences, communicate with external
                                           Index Terms—Agentic AI, Large Language Models, Trust-                                 tools or simulators, and adjust their tactics online, thereby
                                         worthy AI, Safety, Robustness, Interpretability, Accountability,                        enhancing both their potential impact and their failure modes.
                                         Security, Power Systems, Robotics and UAVs, High-Performance                               This survey addresses the growing gap between the rapid
                                         Computing, Communication Networks, Critical Infrastructure.
                                                                                                                                 development of agentic AI architectures and the limited un-
                                                                                                                                 derstanding of their reliability when used in critical infras-
                                                                     I. I NTRODUCTION                                            tructures. This work offers a structured, trust-centered analysis
                                               GENTIC artificial intelligence (Agentic AI) refers to                             that specifically targets domains where autonomous decision-
                                         A     AI systems designed to autonomously perceive their
                                         environment, reason over goals and intermediate states, and
                                                                                                                                 making carries significant societal, economic, and safety con-
                                                                                                                                 sequences, rather than providing a broad or capability-driven
                                         execute sequences of actions; often iteratively and over ex-                            overview of agentic AI. In addition to cataloging agentic
                                         tended horizons to achieve objectives within dynamic envi-                              trustworthiness techniques, we synthesize existing knowledge
                                         ronments [1]. The key difference between agentic AI systems                             on whether and under what circumstances such systems can
                                         and static predictive single-turn large language models (LLMs)                          be responsibly relied upon in operational environments with
                                         lies in their incorporation of explicit decision-making loops,                          strict requirements and low fault tolerance.
                                         memory, tool use, and sometimes coordination among hetero-                                 We contribute to this effort in four ways. First, we create
                                         geneous agents, including humans.                                                       a unified taxonomy of agentic AI architectures that encom-
                                            Recent advances have operationalized these ideas through                             passes prevalent design patterns from the literature, includ-
                                         architectures such as reasoning–acting interleaving (e.g., Re-                          ing reasoning-acting interleaving agents, self-reflective and
                                                                                                                                 memory-augmented agents, tool-augmented agents based on
                                           Corresponding authors: Omar Al-Refai (e-mail: omaralrefai@tamu.edu) and               external environments, deliberative planning agents based on
                                         Eman Hammad (e-mail: eman.hammad@tamu.edu).                                             structured search, and multi-agent systems with coordination
                                           O. Al-Refai, I. Shahbaz, A. Ali Husseinat, and E. Hammad are with the
                                         Innovations in Systems Trust and Resilience (iSTAR) Laboratory, Texas A&M               and role specialization capabilities. The survey’s conceptual
                                         University, TX, USA. E.Hammad and M. Mandulak are with the Texas A&M                    foundation, grounded in this taxonomy, enables systematic
                                         Institute of Data Science - Security, Privacy and Resilience for Trusted AI             comparisons between otherwise disparate methods.
                                         (SPARTA) Thematic Lab., Texas A&M University, TX, USA. J. Kim is
                                         with the Texas A&M Global Cyber Research Institute (GCRI), Texas A&M                       Second, we organize these architectural classes around five
                                         University, TX, USA.                                                                    cross-cutting trustworthiness dimensions: safety and constraint

                                             This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
satisfaction, robustness and reliability, transparency and in-                          trustworthiness, and high-stakes real-world applications meet.
terpretability, accountability and auditability, and privacy and                        It provides a solid foundation for researchers and practitioners
security, mapped onto a ten-point agentic workflow spanning                             seeking to transition agentic AI from experimental settings to
perception through audit [8]. Instead of treating trust as a post-                      practical applications.
hoc or abstract issue, we examine where in this workflow trust                             The remainder of this paper is organized as follows.
mechanisms are present, and where they are absent, exposing                             Section II introduces agentic AI architectures and the four
recurring patterns of incomplete coverage, implicit assump-                             target domains. Section III presents our five trustworthiness
tions, and unresolved risk that are frequently overlooked in                            dimensions and the ten-point assurance workflow. Section IV
capability-focused discussions of agentic AI.                                           analyzes representative agentic architectures through this trust
   Third, we translate this workflow-level view into material                           lens. Section V surveys concrete trust mechanisms, Sec-
developers can act on directly: a survey of trust mecha-                                tion VI traces the evolution of AI safety evaluation from
nisms already embedded in agentic loops, including guardrails,                          representation-level probes to agentic, trajectory-level assess-
safe reinforcement learning formulations, and robustness mea-                           ment, and Section VII consolidates quantitative metrics for
sures against distribution shift and adversarial manipulation;                          agentic workflows. Sections VIII, IX, X, and XI examine
a review of how AI safety evaluation has evolved from                                   domain-specific applications, Section XII synthesizes cross-
representation- and reasoning-level probes to behavior, risk,                           domain insights and gaps, and Section XIII concludes with
and trajectory-level assessment of agentic workflows; and a                             open challenges and future directions.
consolidated set of quantitative metrics, spanning tool use,
memory coherence, planning quality, policy adherence, and                                     II. BACKGROUND : AGENTIC A RCHITECTURES AND
goal drift, that can be reported directly rather than inferred                                             T RUSTWORTHY AI
from task success alone.
   Fourth, we ground this architectural and trust analysis                              A. Agentic Architectures with LLMs
in four constraint-bound engineering domains: power sys-                                   Recent advances in large language models (LLMs) have
tems, autonomous vehicles/robotics/UAVs, high-performance                               led to a shift from static, single-turn inference to agentic
computing, and communication networks. We examine how                                   AI structures. In these systems, models are part of closed-
agentic AI has been proposed or implemented across these                                loop setups that can make decisions over time, interact with
domains, including the types of simulators, benchmarks, and                             their surroundings, and adapt their behavior. Unlike traditional
testbeds used for assessment, and the degree to which trust-                            LLM usage, where models produce responses based on a
worthiness is operationalized through quantifiable constraints,                         set prompt, agentic structures treat LLMs as decision-making
failure analyses, or deployment-relevant metrics. By compar-                            cores. These models constantly observe state information,
ing and contrasting agentic AI in these domains, we iden-                               consider goals and outcomes, take actions, and update their
tify and analyze discrepancies between real-world operational                           internal information based on the feedback they receive. This
requirements and benchmark-driven validation, as well as                                change has led to a growing number of LLM-based agents.
domain-specific failure modes that generic agent evaluations                               At a high level, agentic architectures can be categorized
do not capture. This led to a major insight that agentic AI                             based on the number of decision-making entities involved and
trustworthiness is not four separate engineering problems but                           their interaction patterns. Single-agent architectures consist of
one problem observed from four vantage points, obscured                                 a single LLM-driven agent operating within an environment,
by domain-specific vocabulary and disconnected evaluation                               often enhanced with memory and access to tools. These agents
practices. The recurring gaps of 1) the absence of domain-                              typically handle planning, reasoning, and acting independently
aware safety guarantees under distribution shift and adversarial                        to achieve a specific goal. In contrast, multi-agent architec-
conditions, 2) the lack of standardized trust-oriented evalua-                          tures involve several agents, each potentially powered by an
tion, 3) limited integration of formal verification and runtime                         LLM, that coordinate, communicate, or compete to solve
monitoring, and 4) inadequate human-agent oversight appear                              tasks together. Multi-agent systems add complexity through
in each domain under different vocabulary but share a common                            communication protocols, role specialization, negotiation, and
structure. Building on this insight, the survey outlines a path                         conflict resolution. They also increase the challenges posed by
toward a reusable, cross-domain trustworthiness framework                               coordination failures and unexpected behaviors.
analogous to the graded certification regimes that aviation                                A key feature of modern agentic AI systems is their use
and automotive safety engineering already use, shifting the                             of tools and interaction with their environment. Instead of
field’s next phase of progress from architectural novelty toward                        working solely in text space, agents increasingly connect
assurance infrastructure.                                                               with external APIs, simulators, databases, code interpreters,
   In contrast to current surveys on agentic AI that mostly                             cyber ranges, or physical system models [9]. Using these
focus on reasoning skills, coordination methods, and perfor-                            tools allows agents to go beyond language generation. They
mance metrics, this work highlights trustworthiness and the                             can query real-time information, execute control actions, or
challenges posed by critical infrastructure. Unlike surveys on                          manipulate simulated or real-world environments. In critical
trustworthy AI that mainly discuss static models or single-                             infrastructure contexts, these environments may include power
decision scenarios, we specifically address the unique risks                            system simulators, reinforcement learning settings, network
posed by autonomous, sequential, and tool-integrated agentic                            emulators, or operational dashboards. This tightens the link
systems. This survey fills an important gap where agentic AI,                           between agent decisions and system-level consequences.

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
                                                                                                 a ”Reviewer” agent), allowing for a divide-and-conquer
                                                                                                 approach to complex tasks.
Observe                                                                       Reason          • Communication Protocols: Agents must decide not just
System Inputs    01                                              02
                                                                       Chain-of-Thought
Sensor Data                                                                       Plans
                                                                                                 what to do, but what to tell others. This includes sharing
Environment Feedback                                                   Candidate Actions         state updates, requesting assistance, or negotiating during
                                                                                                 conflicts.
                                  Generic                                                     • Global vs. Local Memory: While individual agents

                                   Agent                                                         maintain local logs of their reasoning, a multi-agent
                                   Loop                                                          system often incorporates a shared memory or ”Global
                                                                                                 State” to ensure all participants remain aligned on the
                                                                                                 ultimate goal.
Update                                                                             Act
                   04                                            03                           As in the MAS illustrated in Figure 2, the complexity shifts
Memory                                                                       Commands
New Observations                                                               Tool Use
                                                                                           from individual thinking to group coordination. While this
Action Outcomes                                                                 Interact   can improve performance on separate tasks, it also brings in
Self-Feedback
                                                                                           ”emergent risks.” Minor errors in one agent’s output propagate
                                                                                           as they pass through the network of agent interactions.
Fig. 1. Generic agentic AI observe–reason–act loop.
                                                                                              This transition from individual reasoning to collective be-
                                                                                           havior necessitates a dual-layered approach to trustworthiness.
   Most agentic architectures can be described using a generic                             We must evaluate intra-agent reliability, ensuring the internal
agent loop, as shown in Figure 1, which captures the repeating                             decision-making core of each entity remains robust, alongside
structure behind different implementations. In this loop, the                              inter-agent trust, which governs the integrity of communica-
agent first observes the current state of the environment,                                 tion, coordination, and delegated authority across the network.
including system outputs, sensor data, or feedback from                                    Assessing these two dimensions is essential to preventing local
previous actions. It then reasons over this information to                                 errors from escalating into systemic failures within the broader
determine the best course of action, often using intermediate                              ecosystem.
representations such as chain-of-thought reasoning, plans, or
evaluations of candidate actions. The agent then acts by issuing                           B. Case Studies
commands, using tools, or interacting with other agents or                                    This survey presents a general case-study perspective on
environments. Finally, the agent updates its memory, adding                                trustworthy agentic AI, while synthesizing the discussion
new observations, action outcomes, or self-reflective feedback                             through four representative engineering domains: power sys-
to guide future decisions. This observe, reason, act, and update                           tems, autonomous vehicles, robotics, and UAVs, high-
cycle continues until a termination condition is met.                                      performance computing, and communication networks.
   While this agent loop offers flexibility, it also raises new                            These domains provide a concrete basis for examining how
trust issues that do not exist with static model inference. Errors                         agentic AI may be introduced into existing monitoring, con-
can accumulate over iterations, actions may have irreversible                              trol, optimization, and decision-making loops to support hu-
effects, and unexpected behaviors can emerge from long-                                    man operators, augment established automation pipelines, or
term interactions with complex environments or other agents.                               increasingly assume parts of the operational process. They are
Therefore, it is vital to understand how different agentic                                 selected because they are mature engineering fields with well-
architectures implement this loop, and where safeguards, con-                              defined operational constraints, hard system requirements,
straints, or oversight mechanisms are included. This under-                                and safety-critical deployments. Consequently, trustworthiness
standing is crucial for assessing their suitability in high-stakes,                        cannot be viewed solely as a property of the AI model, but
safety-critical situations. This foundational insight drives the                           must instead be evaluated against domain-specific require-
taxonomy and trust-centered analysis presented in the rest of                              ments, including safety, reliability, timing, resilience, resource
this survey.                                                                               constraints, security, accountability, and the consequences of
   Building on the single-agent loop, multi-agent systems                                  incorrect autonomous actions. While these four domains do
(MAS) spread these processes across a network of specialized                               not encompass every application of agentic AI, they provide a
entities. In a multi-agent setup, the ”environment” often be-                              technically grounded foundation for studying trust in systems
comes a shared space. Here, the actions of one agent become                                with significant real-world consequences.
the observations of another. This creates a coordination loop                                 Together, these domains span a broad range of system scales
that controls how individual agents interact. These systems                                and architectural characteristics. Power systems represent
typically depend on a communication layer, often called a                                  large-scale cyber-physical infrastructure with tightly coupled
”blackboard” or a messaging protocol, to share plans, inter-                               physical dynamics; autonomous vehicles, robotics, and UAVs
mediate reasoning, or tool outputs.                                                        embody mission-level autonomy in dynamic environments;
   The multi-agent setup introduces three critical components                              high-performance computing exposes low-level computational
beyond the standard loop:                                                                  and resource-management constraints; and communication
   •    Role Specialization: Agents are often assigned specific                            networks capture the distributed data flows that intercon-
        ”personas” or subsets of tools (e.g., a ”Coder” agent and                          nect these systems. This bounded yet diverse scope enables

       This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
                                                                 Orchestrator/Manager Agent
                                                                                 (Optional)



                                                                                  Observe
                                                      Task Assignment             Reason            Task Assignment
                                                                                    Act
                                                                                  Update



                                                                                         Observe/Monitor
            Agent 1                                                                       Overall State                                           Agent 2
                               Access                                                                                           Access
                                                                                                                               Shared Info
                              Shared Info                      Communication / Coordination
              Observe                                                                                                                              Observe
              Reason                                                                                                                               Reason
                Act                                 Shared             Collective          Conflict            Global                                Act
              Update                                                                                                                               Update
                                                   Knowledge           Reasoning          Resolution           State
                                 Post                  Facts             Planning           Arbitration        Context           Post
                                Updates               Memory              Debate             Policies        Agent Status       Updates
          Tool       Action                                                                                                                    Tool      Action
          Usage     Execution                                                                                                                  Usage    Execution



                                            Databases                                                                         Coding
                  Simulators                                                                                                                         CLI Tools
                                               APIs                                                                         Assistants

       External Interfaces, Tools and Infrastructure                                                      External Interfaces, Tools and Infrastructure

Fig. 2. Generic multi-agent architecture showing interconnected loops, shared memory, and collective interaction in a common environment.



meaningful comparisons of trustworthiness challenges across                             safety-critical engineering, safety is commonly defined as free-
complementary engineering settings while maintaining a focus                            dom from unacceptable risk [11]. For agentic AI, this requires
on domains where agentic AI requires rigorous architectural                             more than high task performance: the system must respect
design and system-level assurance.                                                      safety envelopes, operational rules, and hard constraints even
                                                                                        when goals conflict, information is incomplete, or the environ-
                                                                                        ment changes unexpectedly. This dimension is closely related
           III. D IMENSIONS OF T RUSTWORTHINESS
                                                                                        to SOTIF, which emphasizes hazards that arise not only from
   In critical engineering domains, trustworthiness cannot be                           component failures but also from functional insufficiencies
treated as a static property of an AI model or an isolated soft-                        and specification gaps in complex autonomous systems [12].
ware component. Agentic AI systems operate over extended                                In practice, safety evidence may include formal constraints,
time horizons, interact with tools and environments, and                                runtime monitors, fallback policies, hazard analysis, safety
may trigger actions whose effects propagate across physical,                            integrity targets, or empirical demonstrations that the agent
cyber, and organizational layers [10]. Accordingly, this survey                         does not violate critical operating limits [13], [14].
adopts a resilience-oriented view of trustworthiness: an agentic                           B. Robustness and Reliability: Robustness and reliability
system is trustworthy to the extent that it can anticipate,                             capture the agent’s ability to maintain acceptable behavior
withstand, recover from, and adapt to disturbances, including                           under uncertainty, stress, and imperfect operating conditions.
faults, distribution shifts, specification gaps, and adversarial                        Robustness concerns performance under distribution shifts,
manipulation, while remaining within acceptable operational                             adversarial inputs, missing information, tool failures, de-
bounds.                                                                                 layed observations, and compounding errors over long-horizon
   We organize this view around five cross-cutting dimensions:                          tasks [15]. Reliability concerns whether the system behaves
safety and constraint satisfaction, robustness and reliability,                         consistently within its intended operating conditions and main-
transparency and interpretability, accountability and auditabil-                        tains failure rates compatible with deployment requirements.
ity, and privacy and security. These dimensions are informed                            Standards such as ISO 21448 emphasize the importance of
by established safety, assurance, and governance frameworks,                            defining an Operational Design Domain (ODD), detecting
including functional safety standards, Safety of the Intended                           when the system has exited that domain, and triggering safe
Functionality (SOTIF), cybersecurity guidance, and emerging                             fallback behavior when assumptions no longer hold [12]. For
AI governance regimes such as the EU AI Act. They are                                   agentic AI, this dimension therefore requires stress testing,
not treated as independent checkboxes; rather, they serve                               boundary-case evaluation, failure-mode analysis, and evidence
as analytical lenses for comparing how agentic AI systems                               that local errors do not escalate into system-level failures [16],
are designed, evaluated, and justified in critical application                          [17].
settings.                                                                                  C. Transparency and Interpretability: Transparency and
   A. Safety and Constraint Satisfaction: Safety and constraint                         interpretability refer to the degree to which agent behavior can
satisfaction refer to the extent to which agent actions remain                          be inspected, explained, and meaningfully reviewed by human
within operational, physical, legal, and procedural limits. In                          stakeholders. In agentic systems, transparency is not limited

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
to explaining a final output; it also includes tracing goals,                           This decomposition is not meant to prescribe a fixed imple-
intermediate states, tool calls, memory updates, assumptions,                           mentation for every agentic system; instead, it provides an
uncertainty, and the reasoning pathways that connect obser-                             analytical structure for identifying where trust mechanisms,
vations to actions. Interpretability should distinguish between                         constraints, and evidence should be placed. For each trust-
post-hoc narratives that merely rationalize an outcome and                              worthiness dimension, we ask: (i) what threat, hazard, or
explanations that provide testable, decision-relevant evidence                          failure model is relevant; (ii) what mechanisms are embedded
about why the agent behaved as it did [18], [19]. This                                  into the workflow to prevent, detect, constrain, or correct
dimension is especially important for high-risk systems, where                          failures; and (iii) what evidence or quantitative metrics are
the EU AI Act emphasizes transparency and human oversight                               reported to support the trustworthiness claim. This framing
as conditions for responsible deployment [20]. In practice,                             highlights a central gap in current systems: many improve
transparency mechanisms may include interpretable state rep-                            capability, orchestration, or partial transparency, yet still lack
resentations, causal or counterfactual explanations, explicit                           compositional safeguards and evidence across safety, robust-
uncertainty reporting, and operator-facing status indicators that                       ness, accountability, and security. Figure 3 summarizes this
distinguish normal, degraded, abnormal, and unsafe behav-                               workflow-centered view of trustworthy agentic AI across the
ior [17].                                                                               target engineering domains.
   D. Accountability and Auditability: Accountability and au-
ditability refer to the mechanisms that allow actions, decisions,
                                                                                                 IV. T RUSTWORTHINESS IN C URRENT AGENTIC
failures, and design choices to be reconstructed and assigned
                                                                                                              A RCHITECTURES
to responsible actors or system components. This dimension is
essential because agentic outcomes often emerge from interac-                              Current agentic AI architectures differ in how they organize
tions among models, tools, policies, memory systems, human                              reasoning, action, memory, tool use, and coordination. From
operators, and other agents rather than from a single isolated                          a trustworthiness perspective, however, most of them follow
decision [21]. Accountability, therefore, requires traceable                            a common pattern: they improve capability, interaction, and
tool use, tamper-evident logs, versioned policies, documented                           observability, but they rarely provide explicit assurance across
memory or knowledge updates, human override pathways, and                               safety and constraint satisfaction, robustness and reliability,
clear responsibility boundaries across the system lifecycle.                            transparency and interpretability, accountability and auditabil-
Governance frameworks and conformity-assessment regimes                                 ity, and privacy and security. This section reviews the main
emphasize that high-risk systems should maintain evidence of                            architecture classes and evaluates the extent to which trust-
risk management, oversight, monitoring, and post-deployment                             worthiness is built into the architecture rather than assumed
accountability [20], [22]. In this survey, auditability is treated                      from the surrounding environment.
as the evidentiary backbone of trustworthiness: without recon-
structible evidence, claims about safety, robustness, or security
                                                                                        A. Reasoning-Acting and Self-Reflective Agents
remain difficult to verify.
   E. Privacy and Security: Privacy and security concern the                               Reasoning-acting architectures, represented by ReAct, inter-
protection of data, models, tools, and operational behavior                             leave model reasoning with external actions such as tool calls,
against unauthorized access, leakage, manipulation, or misuse.                          search, or environment interaction [2]. Their main strength is
Agentic AI expands the traditional attack surface because                               transparency: intermediate reasoning and action traces make
agents may retrieve information, call tools, write to memory,                           failures easier to inspect and debug. They also improve
coordinate with other agents, and act autonomously across                               grounding compared with purely generative models because
cyber-physical workflows [23]. Relevant risks include prompt                            the agent can observe feedback from the environment before
injection, tool hijacking, adversarial inputs, data exfiltration,                       continuing execution.
model theft, unsafe privilege escalation, and manipulation of                              However, ReAct-style systems are trust-light by design.
agent behavior by malicious actors [24]. Cybersecurity stan-                            Safety and constraint satisfaction are usually inherited from
dards and engineering practice emphasize secure communica-                              the tool environment rather than enforced by the agent itself.
tion, secure boot, access control, monitoring, and defense-in-                          Robustness is also limited, especially in long-horizon tasks
depth architectures [12], [25]. For agentic AI, this dimension                          where small reasoning or tool-use errors can accumulate.
requires not only conventional information security controls                            Extensions such as ReST meets ReAct improve reliability by
but also agent-specific safeguards such as sandboxed tool                               using self-generated trajectories and automated evaluation to
execution, least-privilege permissions, red teaming, anomaly                            refine behavior [35]. This can reduce variance across runs, but
detection, and mechanisms to contain compromised or mis-                                it also introduces a new risk: if the evaluator is itself an LLM,
aligned agent behavior.                                                                 incorrect judgments may be reinforced rather than corrected.
   To operationalize these dimensions, we treat trustworthi-                               Self-reflective agents, such as Reflexion, add an explicit
ness as a workflow-level property rather than a model-level                             feedback step in which the agent converts failures into natural
attribute. Rather than relying on the compressed observe–                               language reflections and reuses them in future attempts [3].
reason–act–update abstraction, we expand the agentic loop into                          This improves behavioral traceability and can increase task
ten stages: perception/observation, reasoning, planning, tool                           success over repeated trials. Nevertheless, the trust boundary
use, communication/coordination, memory update, validation,                             remains largely unchanged. Reflections are only as reliable as
action/execution, monitoring/re-evaluation, and audit/logging.                          the agent’s own diagnosis, and there is no built-in mechanism

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
Fig. 3. Holistic framework for trustworthy agentic AI in critical engineering systems. The figure organizes the agentic workflow around perception, reasoning,
planning, tool use, communication, memory update, validation, action, monitoring, and audit. Five trustworthiness dimensions act as cross-cutting requirements
across the workflow: safety and constraint satisfaction, robustness and reliability, transparency and interpretability, accountability and auditability, and privacy
and security. Representative trust mechanisms and quantitative metrics are mapped to the workflow, while the target application domains illustrate how trust
requirements vary across power systems, autonomous vehicles/robotics/UAVs, high-performance computing, and communication networks.



for independent verification, formal accountability, or security                         models to guide reasoning [36], but this shifts part of the
against adversarial inputs.                                                              decision process into a less interpretable component. As a
   Fig. 4(a) illustrates this architecture as a reasoning–action–                        result, deliberative planners improve reasoning quality and
observation loop augmented by a reflective trace for debugging                           robustness, but they do not, by themselves, provide safety
and behavioral feedback.                                                                 guarantees, accountability, or protection against misuse.
                                                                                            More recent reasoning models, including DeepSeek-R1 and
B. Deliberative and Test-Time Reasoning Architectures                                    OpenAI o-series models, move deliberation into the model’s
                                                                                         native test-time reasoning process [37], [38]. These systems
   Deliberative architectures address the limitations of single-
                                                                                         can perform deeper reasoning, self-checking, and backtracking
path generation by exploring multiple reasoning paths before
                                                                                         before producing a final answer. This improves capability and
selecting an answer. Tree-of-Thoughts, for example, orga-
                                                                                         often reliability, but it also creates a new trust problem: the
nizes candidate reasoning steps into a search process with
                                                                                         most important reasoning steps may be hidden, only partially
generation, evaluation, pruning, and backtracking [4]. These
                                                                                         observablas different agents can be assigned different roles
systems are stronger than simple reasoning-acting loops when
                                                                                         or areas of e, or difficult to verify. For critical systems,
tasks require planning, lookahead, or comparison between
                                                                                         this means that stronger reasoning capability must be paired
alternatives. They are also relatively interpretable because the
                                                                                         with reasoning safety, monitoring, and external validation;
explored paths and selection process can be inspected.
                                                                                         otherwise, the same capability that improves performance can
   Their weakness is that reliability depends heavily on the
                                                                                         also make failures more complex and harder to detect.
quality of the internal or external evaluator. Poor evaluation
can lead to premature pruning, overconfident selection, or                                  Fig. 4(b) shows deliberative reasoning as the exploration of
repeated exploration of weak solutions. Value-guided variants                            multiple candidate paths followed by evaluator-based selec-
such as Q* improve performance by using learned scoring                                  tion.

     This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
                                                                TABLE I
          T RUSTWORTHINESS DIMENSIONS : THREATS , MECHANISMS , AND RESILIENCE PHASES . E ACH DIMENSION IS EVALUATED ACROSS THE
                     ANTICIPATE – WITHSTAND – RECOVER – ADAPT CYCLE . S EE S ECTIONS III AND V FOR MECHANISM DETAIL .


 Dimension                  Primary failure / threat class        Representative mechanisms                     Evidence / assurance type          Resilience phase        Refs
 Safety & constraint sat-   Specification gaps (SOTIF); task-     Job Hazard Analysis; SIL levels               Probabilistic risk reduction;      Anticipate, Withstand         [12],
 isfaction                  level hazards; adversarial con-       (IEC 61508); automated interlocks;            SIL compliance; behavioral                                 [14], [26]
                            straint violation                     TAR safeguards                                constraint pass rate
 Robustness & reliability   ODD exits; distribution shift (non-   FMEA/DDMA; stress testing (AEC-               Failure rate within lifecycle      Anticipate,                   [15],
                            Lp ); error accumulation; transfer-   Q100); circuit breakers; trajectory-level     bounds; cross-model transfer       Withstand, Recover      [27], [28]
                            able adversarial attacks              evaluation (Claw-Eval)                        attack rate; trajectory coher-
                                                                                                                ence score
 Transparency & inter-      Causal opacity; goal hijacking;       Representation Engineering (RepE);            Internal state consistency; rea-   Anticipate, Adapt             [20],
 pretability                misaligned intermediate reasoning     MoReBench reasoning rubrics; opera-           soning rubric pass rate; EU AI                             [29], [30]
                                                                  tor indications                               Act traceability record
 Accountability & au-       Untraceable multi-agent outcomes;     Tamper-evident logs; Agent Delega-            Log completeness audit; dele-      Withstand,   Recover,         [21],
 ditability                 governance gaps; policy drift         tion Tokens; Plan-Do-Check-Act au-            gation chain verifiability; con-   Adapt                   [22], [31]
                                                                  dits; conformity assessments                  formity certificate
 Privacy & security         Prompt injection; tool hijacking;     Zero Trust architecture; defense-in-          WMDP        score    reduction;    Anticipate,             [31]–[34]
                            supply-chain        compromise;       depth; red teaming; RMU unlearning;           HarmBench       refusal   rate;    Withstand, Recover
                            expanded attack surface from          supply-chain auditing                         formal robustness bounds;
                            tool integration                                                                    penetration test results




                                                                                     Problem                                                Agent 1


                        LLM                  Action /
                      Reasoning                                          Path 1       Path 2        Path 3
                                             Tool Call                                                                         Agent 2                   Agent 3

                       Reflection                                                   Evaluator /
                                           Observation                                Scorer
                         Trace                                                                                                            Supervisor /
                                                                                                                                           Consensus
                                                                                     Selected
                                                                                     Answer                                                  Joint
                                                                                                                                            Decision

                   (a) Reasoning–Acting / Self-Reflective           (b) Deliberative / Test-Time Reasoning                      (c) Multi-Agent Coordination
                                                                                                                 NL / Latent



                                                                                                Agent 1                           Agent 2
                                                 Agent              Tools / APIs

                                                                                                                Protocol /
                                                                                                              Message Schema
                                                Policy /              External
                                                Sandbox             Environment
                                                                                                                  Audit /
                                                                                                                Verification


                                          (d) Tool-Using / Environment-Grounded                 (e) Communication and Coordination


Fig. 4. Representative agentic AI architecture classes and their trustworthiness implications. Dashed arrows denote reflection, communication, or information
exchange, while solid arrows denote execution, control, evaluation, or verification flow.



C. Multi-Agent Architectures and Coordination                                               level property rather than an individual-agent property. A
                                                                                            single agent may appear reasonable in isolation, while, through
   Multi-agent architectures distribute reasoning and decision-                             interaction, the group produces unsafe, inconsistent, or un-
making across multiple agents that communicate, specialize,                                 accountable behavior. Responsibility attribution is especially
debate, or hand off tasks. Examples include role-based sys-                                 difficult because final decisions emerge from communication,
tems such as CAMEL and broader LLM-based multi-agent                                        negotiation, and accumulated context rather than a single
frameworks [39], [40]. Their main advantage is robustness                                   model output.
through diversity: agents can critique one another, divide                                     Communication protocols, as discussed later on, partially
complex tasks, or recover from local errors. They also support                              address this problem by structuring agent interactions. Natural
modularity, as different agents can be assigned different roles                             language coordination is flexible but ambiguous, while struc-
or areas of expertise.                                                                      tured protocols reduce ambiguity and improve logging. Agent-
   At the same time, multi-agent systems expose some of the                                 to-agent protocols and tool-interface standards can improve
most serious trustworthiness gaps. Safety becomes a system-                                 interoperability and auditability, but they do not guarantee

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
that the content of communication is correct, safe, or aligned                          flexible dialogue, critique, and negotiation. However, its flexi-
with system goals. Supervisory agents and consensus-based                               bility introduces ambiguity. Agents may report incorrect state
coordination can improve robustness, but they also shift trust                          transitions, produce false coordination signals, or create what
to the supervisor or to the aggregation rule. Thus, multi-agent                         is often called hallucinated coordination. Structured commu-
architectures are promising for scalability and specialization,                         nication protocols address this risk by requiring interactions to
but remain weak in accountability, security, and system-level                           follow schemas or formal message formats [50], [51]. These
assurance.                                                                              protocols improve consistency and reduce ambiguity, but they
   Fig. 4(c) summarizes multi-agent coordination as distributed                         primarily constrain syntax rather than the semantic validity of
agent interaction followed by supervision or consensus-based                            exchanged information. The Model Context Protocol (MCP)
aggregation.                                                                            reflects this direction by formalizing tool use, context serial-
                                                                                        ization, and persona definitions.
                                                                                           Beyond symbolic communication, recent work explores
D. Tool-Using and Environment-Grounded Agents                                           communication in latent representation spaces, where agents
   Tool-using architectures extend agents from text generation                          share internal hidden states instead of text outputs. This can
to action in external environments. Toolformer shows that                               enable richer and more efficient information transfer, support
models can learn when to call external tools [41], while                                parallel reasoning, and improve alignment among agents [52].
systems such as VOYAGER demonstrate long-horizon skill                                  The trade-off is transparency. Latent communication reduces
acquisition in interactive environments [42]. These architec-                           human interpretability and makes interactions harder to audit,
tures improve grounding because the agent can use external                              creating an oversight challenge for trust-critical systems [53].
information, execute actions, and observe results. They also                               Coordination strategies determine how communication is
make some behavior more inspectable through tool traces,                                organized, checked, and acted upon. Decentralized, leaderless
logs, and reusable skills.                                                              methods reduce single points of failure and often draw on
   However, tool grounding does not automatically imply trust-                          Byzantine fault tolerance and consensus-based design [54].
worthiness. In fact, tool access increases the consequences of                          By aggregating outputs across agents or requiring agreement
failure. Incorrect reasoning can become incorrect action, and                           before action, these methods improve robustness against faulty
unsafe tool use can affect external systems. ToolGym makes                              or adversarial participants. Supervisory structures add moni-
this issue explicit by evaluating agents in open-world tool set-                        toring agents that enforce constraints and reduce misuse or
tings with long-horizon workflows and injected failures [43].                           unsafe behavior. However, they can also introduce bottlenecks
Such environments improve robustness evaluation, but they                               or shift trust to a single supervisory entity rather than resolving
remain primarily diagnostic rather than preventive.                                     the underlying coordination risks [55].
   Production frameworks such as LangChain, LangGraph,                                     Multi-agent systems also introduce failure modes that differ
AutoGen, CrewAI, OpenHands, and SuperAGI move agent                                     from those in single-agent models. Communication channels
design closer to deployable software systems [44], [45]. Their                          can spread misinformation, allowing incorrect or manipulated
trust contribution is mainly operational: tracing, monitoring,                          knowledge to circulate and persist in shared memory. Strate-
role assignment, workflow control, sandboxing, testing, and                             gic behavior may emerge, including deception, collusion, or
human-in-the-loop intervention. These mechanisms improve                                covert signaling embedded in otherwise benign outputs. Long
transparency, auditability, and failure containment, but they                           interaction chains can also cause role drift, in which agents
are engineering controls rather than formal guarantees. More                            gradually deviate from their assigned responsibilities, leading
security-oriented designs, such as cognitive-executive separa-                          to coordination failures. These risks show that trust cannot be
tion, go further by treating the reasoning model as untrusted                           evaluated only at the level of individual agents; it must account
and enforcing constraints outside the model [46]–[49]. This                             for interaction dynamics over time.
is a stronger trust direction because it separates decision                                Addressing these risks requires explicit verification and
generation from permission to act.                                                      interpretability of multi-agent interactions rather than relying
   Fig. 4(d) depicts tool-using agents as systems whose de-                             solely on black-box evaluation. Recent work on multi-agent
cisions are routed through tools, external environments, and                            interpretability analyzes internal representations across agents
policy or sandbox controls.                                                             to detect coordinated or deceptive behavior. Formal methods
                                                                                        provide another path by constraining interactions in which
                                                                                        agents gradually deviate from their assigned responsibilities,
E. Communication and Coordination between Agents                                        ensuring actions are carried out through verifiable protocols
   The shift from single-agent systems to multi-agent archi-                            and that behavior remains consistent with predefined specifi-
tectures changes the locus of trust. In multi-agent systems,                            cations. These approaches offer stronger guarantees, but they
reliability depends not only on individual model behavior but                           remain difficult to scale and often require access to internal
also on inter-agent interaction [50]. As agents exchange infor-                         model states or rigid interaction structures.
mation, coordinate actions, and reuse one another’s outputs,                               Overall, communication and coordination are not merely
local errors and behavioral mismatches can propagate across                             enabling mechanisms in agentic systems; they are primary
agent boundaries and become system-level risks.                                         determinants of trustworthiness. Current approaches remain
   Communication is central to this trust problem. Natural                              fragmented, addressing protocol design, robustness, or inter-
language remains the dominant interface because it supports                             pretability in isolation. A central open challenge is to develop

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
                                                          TABLE II
Q UALITATIVE TRUSTWORTHINESS COVERAGE ACROSS AGENTIC AI ARCHITECTURE CLASSES , WITH REPRESENTATIVE STRENGTHS AND WEAKNESSES .


Architecture Class        Representative Systems            Safety   Robust. Transp. Account. Priv./Sec. Strengths                            Weaknesses

                                                                                                            Improves grounding through
                                                                                                                                              Safety and constraint enforcement
                          ReAct [2]; ReST meets                                                             observe–reason–act loops;
Reasoning-acting agents                                      Low     Medium     High      Low       Low                                       are mostly delegated to tools or
                          ReAct [35]                                                                        exposes intermediate traces for
                                                                                                                                              the surrounding environment.
                                                                                                            debugging.
                                                                                                            Supports adaptation from
                                                                                                                                              Self-evaluation may reinforce
                                                                                                            previous failures; improves
Self-reflective agents    Reflexion [3]                      Low     Medium     High    Medium      Low                                       incorrect diagnoses without
                                                                                                            behavioral traceability across
                                                                                                                                              independent verification.
                                                                                                            attempts.
                                                                                                            Improves reasoning reliability    Depends on evaluator quality;
Deliberative search       Tree-of-Thoughts [4];                      Medium–Medium–
                                                             Low                    Low             Low     through search, comparison,       safety and accountability are not
agents                    value-guided planning [36]                  High   High
                                                                                                            pruning, and backtracking.        first-class architectural goals.
                                                                                                         Enables deeper reasoning,            Internal reasoning may be hidden,
Native test-time          DeepSeek-R1 [37]; OpenAI                                                 Low–
                                                           Medium     High    Medium      Low            self-checking, and stronger          only partially observable, or
reasoning models          reasoning models [38]                                                   Medium
                                                                                                         long-horizon problem solving.        difficult to independently verify.
                                                                                                            Enables specialization, critique, Responsibility attribution, role
                          CAMEL [39]; LLM-based
Multi-agent systems                                          Low     Medium Medium        Low       Low     task decomposition, and           drift, and system-level control
                          multi-agent systems [40]
                                                                                                            recovery from local failures.     remain difficult to guarantee.
                                                                                                         Improves coordination,               Ambiguity, hallucinated
                          Natural-language A2A; MCP;
Communication                                               Low–          Low–                     Low– information sharing, and              coordination, hidden signaling,
                          latent-space                            Medium                  Low
between agents                                             Medium        Medium                   Medium interoperability across agents       and interaction-level failures are
                          communication [50], [52], [53]
                                                                                                         and tools.                           hard to audit.
                                                                                                            Grounds agent behavior in
                                                                                                                                              Tool access increases failure
                          Toolformer [41];                  Low– Medium–                                    external tools, environments,
Tool-using agents                                                        Medium Medium              Low                                       consequences and requires
                          VOYAGER [42]; ToolGym [43]       Medium High                                      observations, and executable
                                                                                                                                              external containment mechanisms.
                                                                                                            actions.
                                                                                                       Provides practical controls, like
                          LangChain; LangGraph;                                                                                          Mostly relies on operational
Production agent                                                     Medium–            Medium–        tracing, monitoring, workflow
                          AutoGen; CrewAI; OpenHands;      Medium            High               Medium                                   safeguards rather than formal
frameworks                                                            High               High          design, testing, and HITL
                          SuperAGI [44], [45]                                                                                            assurance or verifiable guarantees.
                                                                                                       intervention.
                                                                                                            Separates reasoning from
                          Managed agents;                                                                                                     Adds implementation complexity
Secure execution                                                                                            execution, improving
                          cognitive-executive               High      High    Medium      High     High                                       and may restrict open-ended
architectures                                                                                               containment, authorization, and
                          separation [46]–[49]                                                                                                autonomy or flexible tool use.
                                                                                                            auditability.

   Note: Low indicates limited or mostly implicit support; Medium indicates partial support; High indicates explicit and recurring architectural support.



compositional frameworks that jointly reason about commu-                                   V. T RUST M ECHANISMS IN AGENTIC A RCHITECTURES
nication, coordination, and system-level behavior over long-
horizon interactions. Without this integration, trust in multi-
agent systems will remain partial because risks can still emerge
from interactions among otherwise well-behaved components.                                   This section reviews the technical frameworks and practical
                                                                                         measures used to keep agentic AI systems safe, predictable,
                                                                                         and aligned with ethical limits. As agent-based systems shift
  Fig. 4(e) highlights communication-centered architectures in                           from basic chatbots to tools that plan and reason across several
which agent exchanges are structured through protocols and                               steps, methods for building trust need to move past simple
checked through audit or verification mechanisms.                                        filtering of final outputs and toward safeguards built into the
                                                                                         system’s structure and the way it stores and uses information.
   As shown in Table II, current agentic architectures show                                 Taken together, the guardrail-based, learning-based, and
meaningful progress in capability, interaction, and observ-                              robustness-oriented mechanisms reviewed in this section rarely
ability, but trustworthiness remains uneven. Transparency is                             address a single trustworthiness dimension or intervene at
the most consistently supported dimension because many                                   a single point in the agentic loop. Table III consolidates
architectures expose reasoning traces, tool calls, search paths,                         this coverage, mapping each mechanism onto the five trust-
or workflow logs. Robustness is improving through reflection,                            worthiness dimensions introduced in Section III and onto
deliberation, multi-agent critique, and failure-aware evaluation.                        the ten-point agentic workflow. The resulting picture shows
In contrast, safety, accountability, and privacy/security remain                         that guardrail mechanisms concentrate on the reasoning and
comparatively weak because they require enforceable con-                                 action stages, learning-based mechanisms extend coverage into
straints, independent verification, secure execution boundaries,                         planning and memory, and robustness-oriented mechanisms
and durable audit records. This gap motivates a shift from                               such as Zero Trust and supply-chain hardening span nearly
capability-centered agent design toward assurance-centered                               the full observe–reason–act–update cycle, underscoring that
architectures, where trust mechanisms are built into the agent                           no single mechanism class delivers assurance across the entire
loop rather than added after deployment.                                                 workflow on its own.

     This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
A. Guardrails, Policies, and Safety Filters                                             control methods could be used to align these emerging values
   Clear, preventive limits serve as the primary safeguard                              with broader human norms, including standards set by citizen
against malicious misuse and unintended harm. Standard post-                            assemblies [59].
hoc alignment methods, such as training a model to refuse                                  2) Ethical Steering: A common question in agentic AI
certain requests, are widely used, but the cited sources argue                          research is whether adding ethical limits inevitably reduces
that they can be fragile and bypassed with relatively simple                            an agent’s ability to perform well [60]. The MACHIAVELLI
changes to the prompt [28], [32].                                                       benchmark tests this assumption by showing that agents can
   1) Safety Pretraining: Instead of relying solely on fixes                            be guided toward safer behavior while maintaining task per-
added after training, safety pretraining aims to incorporate                            formance [58]. By treating harmful behaviors as measurable
safety from the beginning by shaping the training data and                              signals in interactive settings, the benchmark enables safety
procedures around clear safety goals [56]. This is done in three                        to be improved through the system’s design and evaluation,
main procedures: filtering web data for safety, rewriting text                          rather than treating it as a separate rule imposed from outside.
to place unsafe content in a safer context, and training models                            In terms of trustworthiness, this result matters for neural
to refuse harmful requests in a native way. Lastly, adopting                            agentic systems because their behavior can arise stochastically
”Native Refusal” using datasets, such as RefuseWeb, so the                              from prompt-based coordination rather than from explicit
model learns why refusing is the right choice, not just when                            symbolic rules. Recent analyses note that when these systems
to refuse [56].                                                                         run on their own, they can slowly shift away from their
   2) Representation-Level ”Circuit Breakers”: Standard re-                             intended goals and apply what they learned in the wrong way.
fusal filters can be bypassed by adding adversarial suffixes                            The MACHIAVELLI findings indicate that steering language
to a prompt [32]. Circuit-breaking is a method that targets                             models can improve both safety and capability simultaneously,
the internal patterns that a model uses when it is about to                             suggesting that alignment should be treated as part of how an
produce unsafe content. In practice, it can stop or redirect                            agent makes decisions rather than as an after-the-fact oversight
the system mid-response when the prompt is trying to steer it                           layer [58].
toward harmful output [28]. In prior studies, this approach has                            3) Post-Training Unlearning Methods: A key challenge
worked well in multimodal models and can block image-based                              in deploying agentic AI systems is reducing the risk that
attacks that typical filters miss [28].                                                 they are used for harmful purposes while preserving their
   3) Programmatic Rule Enforcement: Frameworks such as                                 general capabilities [8]. Safety measures that rely on refusal
RuLES (Rule-following Language Evaluation Scenarios) pro-                               rules or prompt filtering mostly work only during the user’s
vide programmatic checks to assess whether an agent violates                            interaction with the system. They can still be bypassed through
a defined set of behavioral constraints (e.g., ”do not generate                         jailbreaks, adversarial prompts, or later fine-tuning, so the
abusive content”) during user interaction [57]. This makes it                           risky information remains stored in the model.
easier to confirm, through automated checks, whether rules are                             Representation Misdirection for Unlearning (RMU) ad-
being followed than to rely on manual review [57].                                      dresses this issue by altering the model’s internal repre-
   4) Tamper-Resistant (TAR) Safeguards: In open-weight                                 sentations tied to unsafe subject areas. Instead of blocking
LLMs, common safety measures can be weakened if someone                                 responses, RMU changes the model’s internal activations on
fine-tunes the model to change its weights. TAR aims to create                          risky inputs, while keeping activations on harmless inputs
safeguards that hold up even after hundreds of rounds of                                close to those of the original model [33]. This leads to a
adversarial fine-tuning, so the model maintains the same safety                         practical loss of access to hazardous knowledge at the level of
behavior over time [26].                                                                internal representations.
                                                                                           Results on the Weapons of Mass Destruction Proxy
                                                                                        (WMDP) benchmark suggest that RMU lowers performance
B. Learning for Trust: Safe RL, Reward Design, and Feedback
                                                                                        on biosecurity and cybersecurity hazard tasks to roughly the
   In agentic systems, trustworthiness can be compromised                               level of random guessing, while maintaining most general
when the reward signal pushes the agent toward actions that                             reasoning and conversational fluency. In probing and ad-
raise its score but do not match the user’s goals or the intended                       versarial optimization tests, the removed knowledge did not
task. This points to an ethical trade-off: when the reward                              reappear, suggesting genuine unlearning rather than simple
setup favors it, agents may learn Machiavellian tactics, such as                        masking [33].
deception and power-seeking, to increase their rewards [58].                               Representation-level unlearning can remove specific unsafe
This occurs because reward functions act as proxies for                                 behaviors after training. This gives a practical way to restrict
desired behavior, and when these proxies are incomplete or                              an agent in adversarial or misuse settings while keeping most
misspecified, agents optimize for the proxy rather than the                             of the system’s useful performance.
underlying implicit objective.
   1) Utility and Value Engineering: Recent work in Utility
Engineering reports that as large language models get bigger,                           C. Robustness to Distribution Shift and Adversaries
they tend to develop value-like patterns on their own [59]. By                            A trustworthy agent should remain reliable under expected
examining how consistent these newly observed preferences                               and unexpected real-world conditions and in the face of active
are, researchers can spot situations in which an AI may                                 adversarial attacks. This typically poses challenges similar to
prioritize its own interests over those of humans. Utility                              those associated with protecting any digital system. However,

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
because some AI models/agents are black-box, their behavior                                Taken together, the results suggest that universal and trans-
becomes more unpredictable in unforeseen real-world sce-                                ferable adversarial attacks remain a basic problem for agentic
narios, thereby making them more vulnerable to adversarial                              AI systems. System reliability should not be judged solely by
attacks, including but not limited to fuzzing attacks.                                  fixed prompt guards or by the alignment of a single model. It
   1) Generalizing to Unforeseen Adversaries: Traditional ro-                           also needs evaluation of how well it transfers across different
bustness research has focused narrowly on Lp -bounded per-                              models, whether automated tools can detect new attacks, and
turbations, but real-world ”worst-case” scenarios are far more                          how agent-style prompts can alter the system’s interpretation
diverse [27]. This is because                                                           of a user’s intent.
   To better align research results with real-world conditions,                            3) Systemic and Supply-Chain Vulnerabilities: In many
the authors of [27] propose ImageNet-UA, a benchmark                                    agentic AI systems, trust can be weakened not only by model
that tests models on eighteen new non-Lp attacks, including                             errors but also by weak software engineering practices and
Glitch, Kaleidoscope, and Wood, designed to mimic complex,                              unreliable deployment pipelines. As agent frameworks push
differentiable image corruptions.                                                       for rapid prototyping and “vibe-coding,” teams often put
   Instead of relying on threat models that assume a fixed                              security off or assume tools and libraries will handle it, leaving
set of attacks, ImageNet-UA tests models under structural,                              the full system fragile from start to finish. One clear example
semantic, and data distribution changes that were not present                           is the MoltBot case study, which was later renamed OpenClaw.
in training. This setup asks whether a model can keep making                            A security review found that the assistant saved sensitive API
correct predictions when the world shifts in ways it was not                            keys and credentials in plain text. The review also found that
trained to expect, which is closer to the kinds of changing and                         its backup process kept copies of these secrets even after users
adaptive disturbances that agentic AI systems may face in real                          tried to delete them [34].
settings [27].                                                                             These design choices break basic security principles and
   While larger models often perform better on capabilities                             show that agent-based systems can unintentionally store and
benchmarks like BIG-bench [61] or Humanity’s Last Exam                                  reveal sensitive data, regardless of the language model’s
(HLE) [62], scale alone does not guarantee robustness against                           alignment or intent. These risks become worse when indirect
lateral or unstructured reasoning challenges.                                           prompt injection attacks are involved. Agents who read outside
   2) Universal and Transferable Attacks on Agents: Recent                              materials such as web pages, PDFs, or emails can be quietly
studies suggest that agentic AI systems are particularly vulner-                        steered off course if those materials contain hidden, harmful
able to automated adversarial attacks that slip past common                             instructions. These instructions may be placed in ways a reader
alignment and safety controls. Rather than relying on hand-                             would not notice, such as white text on a white background
crafted prompts like traditional jailbreaks, these attacks ex-                          or commands stored in metadata.
ploit consistent weaknesses in how agents read goals, follow                               If these injected prompts run, they can instruct the agent to
instructions, and interpret how a task is framed.                                       pull out private data, use tools in unintended ways, or take over
   One clear case is the Greedy Coordinate Gradient (GCG)                               connected accounts, even when the user does nothing. This
method, which systematically searches for adversarial suffixes                          attack vector points to a basic trade-off in agentic systems:
that can be added to an otherwise harmless prompt to increase                           they need to accept input from their environment, but they
the chance that the model outputs content that is not allowed                           also need clear, strict limits on what actions they can carry
or could cause harm [32]. A key point is that GCG does not                              out. In summary, agentic AI can be exposed to risks that come
need access to a model’s internal details when it is used in                            through the software supply chain.
practice. After these suffixes are found, they can be applied                              Many agent frameworks and tool ecosystems rely on large
again in later interactions. More worrying is that these attacks                        numbers of third-party libraries and community contributions,
can be easily transferred across different models and settings.                         and these components are often added with limited screening
   Prior work suggests that adversarial suffixes developed with                         and little ability to audit their code or provenance. A mali-
smaller open-source models can transfer to larger, closed-                              cious commit, a compromised dependency, or a compromised
domain systems, including OpenAI and Anthropic mod-                                     package manager account can spread a backdoor across many
els [32]. Because these prompt attacks carry over from one                              downstream systems and reach hundreds of thousands of
model to another, scale or proprietary training alone does not                          deployed agents.
provide much protection against prompt-based adversaries.                                  In this setting, how much we can trust an agent depends
   In agentic settings, this vulnerability becomes even more                            directly on the integrity of the wider software ecosystem it
pronounced. Findings from the AgentHarm benchmark suggest                               relies on. Overall, these weaknesses in the wider system and
that when a harmful request is presented as part of an agent’s                          in the supply chain show that protecting agentic AI is not just
assigned work, such as helping with fraud, cybercrime, or                               about the model itself. Strong defenses depend on combining
circumventing policies, many frontier agents comply even                                secure software engineering, careful isolation and validation of
without complex jailbreak prompts [63]. This idea of agentic                            external inputs, and strict oversight of the entire supply chain.
compliance means that as systems become more capable                                    Taken together, these steps help prevent minor implementation
through goal-focused design and the use of tools, they may                              mistakes from spreading into large-scale security incidents.
also create more opportunities for attackers to interfere, be-                             4) Zero Trust and Persistence: As concerns about agen-
cause the system tends to prioritize completing the task over                           tic vulnerabilities expand, recent studies have focused on
adhering to safety limits.                                                              strengthening system design using Zero Trust principles and

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
continuous, tamper-resistant protections. Instead of relying                               Evaluating agentic behavior should not rely only on whether
on perimeter defenses or fixed assumptions about alignment,                             the final answer looks right. It also requires procedural trans-
these approaches assume compromise can occur and focus on                               parency, where, at an operational level, one can see the steps
ongoing checks throughout the agent’s lifecycle. In a Zero                              the agent takes, including the information it uses, the assump-
Trust approach to AI, agents, datasets, tools, and execution                            tions it makes, and how it handles uncertainty, to understand
pipelines are treated as separate entities that each need their                         how it arrives at a conclusion. This distinction is particularly
own verification and access controls, rather than being trusted                         important in agentic systems, where decisions unfold over
by default because they sit in the same system [31]. In this                            multiple steps and intermediate errors or misaligned reasoning
model, nothing is assumed to be trusted. Access rights are                              can propagate even when the final output appears correct.
checked each time, based on the user’s identity and the current
context.
   In agentic systems, this supports identity-bound inference                           A. Representation-Level Evaluation
and tight limits on tool use, data access, and task execution,                              Based on research in cognitive neuroscience, Representation
which helps keep the blast radius small for both prompt-                                Engineering (RepE) takes a top-down approach to trans-
driven and system-level attacks [31]. Agent Delegation Tokens                           parency [29]. Looking at patterns across groups of neurons
(ADTs) have been proposed as cryptographic add-ons to ex-                               instead of single cells allows researchers to track broader
isting identity systems, such as X, to enable controlled action                         cognitive states, such as honesty, seeking power, and intent to
delegation. X.509 certificates are digital files that bind a public                     avoid harm. This makes it possible to spot signs of deception
key to an identified subject, and they are commonly used                                that might not be visible in the final written text [66].
in systems like TLS to support authentication and encrypted
                                                                                            This view matters from a trustworthiness perspective be-
communication [31].
                                                                                        cause agents work over time, pursue goals, and change their
   Architectural hardening also depends on keeping the system
                                                                                        actions as situations and settings change. RepE-style moni-
stable, even when an attacker tries to change it in harmful
                                                                                        toring lets researchers track an agent’s internal representations
ways. This means designing the system so it resists tampering
                                                                                        over time to detect whether harmful intent, reward hacking, or
and continues to work as intended under adversarial pres-
                                                                                        goal misalignment is emerging, even when the agent’s outward
sure. Tamper-resistant (TAR) safeguards are meant to keep
                                                                                        behavior still appears compliant. This is sometimes referred to
safety controls in place even if a model is fine-tuned or
                                                                                        as ”goal hijacking”.
intentionally trained to weaken them [26]. Complementary
                                                                                            Instead of judging a system only by behavior checks or by
circuit-breaker checks discussed earlier can act on the model’s
                                                                                        filtering its outputs, RepE bases trust on whether its internal
internal representations, stopping risky action plans before
                                                                                        states stay consistent. This can flag early problems before they
they turn into actual tool calls [28]. These measures move
                                                                                        become clear mistakes in what the system says or does. The
safety enforcement away from basic prompt screening and
                                                                                        paper shows that representation-level probes can track safety-
toward tighter oversight of the agent’s underlying behavior.
                                                                                        relevant concepts, such as honesty and harmlessness, across a
   Recent work is exploring certifiable robustness methods that
                                                                                        range of prompts and tasks. This suggests RepE is a practical
provide formal guarantees against specific types of perturba-
                                                                                        proof of concept for ongoing oversight, interpretability, and
tions [64]. Lipschitz-constrained training can provide provable
                                                                                        control in long-horizon autonomous agent systems [29].
upper bounds on a model’s sensitivity to small input changes,
and it often leads to better deterministic VRA results under                                However, while representation-level monitoring provides
formal verification. Even though these guarantees cover only                            valuable signals, it should be viewed as complementary to
a narrow range of cases, they are an important step toward                              external verification mechanisms rather than a replacement,
agent-based systems whose safety can be verified with formal                            due to the difficulty of reliably interpreting internal states in
methods rather than inferred from experiments.                                          some cases.
   In an academic setting, Zero Trust architectures, crypto-
graphic delegation [65], persistent safeguards, and certifiable
                                                                                        B. Reasoning-Level Evaluation
robustness can be considered complementary components of
a defense stack, each addressing distinct risks and limitations                            Following the same design principles as the previous sub-
in system security. This shift shows that dependable agentic                            sections, the MoReBench framework shifts attention away
AI depends on more than alignment and evaluation. It also                               from models’ final answers and toward their intermediate
depends on careful system design that expects adversarial                               reasoning steps, enabling researchers to study how conclusions
pressure at every layer.                                                                are reached rather than only what is produced at the end [30].
                                                                                        The method relies on rubrics developed by subject experts to
     VI. T HE E VOLUTION OF AI S AFETY E VALUATION                                      assess how agents notice morally relevant factors and balance
   Evaluation methodologies for AI systems have undergone a                             competing aims, aiming to keep their reasoning consistent with
significant transformation, evolving from internal transparency                         established normative ethical frameworks [30].
mechanisms to system-level risk assessment frameworks. This                                In agentic settings, this form of evaluation is particularly
progression reflects a shift in focus from understanding model                          important because agents must make sequential decisions
internals to validating reasoning processes, to stress-testing                          under uncertainty, where intermediate reasoning steps directly
behavior, and ultimately to quantifying hazardous capabilities.                         influence downstream actions.

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
                                                             TABLE III
              C OVERAGE MATRIX LINKING TRUST MECHANISMS TO TRUSTWORTHINESS DIMENSIONS AND AGENTIC WORKFLOW TARGETS .

Mechanism                                          Trustworthiness coverage                                           Workflow intervention point
                                     Safety Robust. Transp. Account. Priv./Sec.                 Obs. Reas. Plan Tool Comm. Mem. Val. Act Mon. Audit
Guardrails, policies, and safety filters
Safety pretraining                     ✓                                             ✓                   ✓       ✓                                       ✓
Representation-level     circuit       ✓         ✓          ✓                        ✓                   ✓                                         ✓     ✓      ✓
breakers
Programmatic rule enforcement          ✓                    ✓           ✓                                ✓       ✓      ✓                          ✓     ✓                  ✓
Tamper-resistant safeguards            ✓         ✓                      ✓            ✓                   ✓                                 ✓       ✓     ✓      ✓           ✓
Learning for trust: safe learning, reward design, and feedback
Utility and value engineering          ✓                    ✓                                            ✓       ✓                                 ✓     ✓
Ethical steering                       ✓         ✓          ✓                                            ✓       ✓                                 ✓     ✓      ✓
Post-training unlearning               ✓                                ✓            ✓                   ✓                                 ✓       ✓     ✓                  ✓
Robustness to distribution shift, adversaries, and system compromise
Generalization to unforeseen ad-                 ✓                                   ✓           ✓       ✓                                         ✓            ✓
versaries
Universal and transferable attack      ✓         ✓                                   ✓           ✓       ✓       ✓                                 ✓     ✓      ✓
evaluation
Systemic and supply-chain hard-                  ✓                      ✓            ✓           ✓                      ✓        ✓         ✓       ✓     ✓      ✓           ✓
ening
Zero Trust and persistence             ✓         ✓                      ✓            ✓           ✓                      ✓        ✓         ✓       ✓     ✓      ✓           ✓
Evaluation and assurance across agentic workflows
Representation-level evaluation        ✓         ✓          ✓                                            ✓                                         ✓            ✓
Reasoning-level evaluation             ✓                    ✓           ✓                                ✓       ✓                                 ✓                        ✓
Behavior-level evaluation              ✓         ✓                      ✓            ✓                                  ✓                          ✓     ✓      ✓           ✓
Risk-level evaluation                  ✓                                ✓            ✓                   ✓              ✓                  ✓       ✓     ✓      ✓           ✓
Trajectory-level agentic evalua-       ✓         ✓          ✓           ✓            ✓           ✓       ✓       ✓      ✓        ✓         ✓       ✓     ✓      ✓           ✓
tion
 Note: Checkmarks indicate the primary dimensions addressed by each mechanism and the main workflow stages where it intervenes. Obs. =
 perception/observation, Reas. = reasoning, Plan = planning, Tool = tool use, Comm. = communication/coordination, Mem. = memory update, Val. =
 validation, Act = action/execution, Mon. = monitoring/re-evaluation, and Audit = audit/logging.



C. Behavior-Level Evaluation                                                             and hidden risk abilities, they often assume static or one-
   HarmBench provides a standard automated red teaming                                   step interactions. However, modern agentic systems operate
setup that supports large-scale verification. This lets developers                       in changing environments where actions unfold over longer
run the same set of tests across 18 red-teaming methods to                               periods, involve the use of tools, and rely on ongoing feedback.
check how well the model holds up and to work together                                   This change requires new evaluation frameworks that account
on stronger refusal safeguards [67]. HarmBench and similar                               for temporal structure, interactions with the environment, and
benchmarks can serve as a final encapsulation layer for verify-                          the cumulative effects of decisions.
ing trustworthiness in an Agentic AI architecture/application.                              Claw-Eval takes a step in this direction by introducing
                                                                                         evaluation protocols designed for agentic workflows. Instead
D. Risk-Level Evaluation                                                                 of evaluating isolated outputs or skills, it assesses agents
   Benchmarks such as WMDP evaluate models across do-                                    within the context of multi-step tasks. Success depends on not
mains involving dual-use knowledge—information with both                                 just being correct at each step but also on how well the overall
legitimate and potentially harmful applications, such as biose-                          path holds together [68]. This involves maintaining consistent
curity, cybersecurity, and chemical synthesis [33]. Monitor-                             goals, recovering from mid-task failures, and effectively using
ing performance on these tasks allows institutions to assess                             external tools and environmental signals.
whether an agent retains capabilities that could be misused by                              A key feature of this approach is its focus on trajectory-
malicious actors.                                                                        level evaluation. Failures are no longer limited to incorrect
   This form of evaluation is critical for trustworthiness, as                           outputs; they can also manifest as planning errors, cascading
it enables targeted auditing of high-risk knowledge domains                              mistakes across steps, or unintended interactions with tools and
and supports decisions about capability restriction, controlled                          environments. Therefore, evaluations must capture not just if
access, or post-training unlearning interventions.                                       an agent succeeds but also how it behaves throughout the task.
                                                                                         This includes its ability to adapt, withstand disruptions, and
E. Toward Agentic Evaluation                                                             stay aligned with its goals over time.
  While previous evaluation methods have focused on internal                                This approach reveals a significant limitation of earlier
representations, reasoning processes, observable behaviors,                              evaluation methods: they overlook the complex nature of

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
Fig. 5. Evolution of Benchmarks from static AI safety evaluation to agentic system-level evaluation.



agentic execution. Even when individual components, like                                (TUE), Memory Coherence and Retrieval (MCR), Strate-
reasoning modules or safety filters, work reliably alone, their                         gic Planning Index (SPI), and Component Synergy Score
interactions over time can create new failure types that static                         (CSS) [70], [71]. A consolidated summary of all metrics
benchmarks won’t catch.                                                                 introduced throughout this section, spanning component-level
   Claw-Eval thus represents a shift from focusing on specific                          effectiveness, safety and policy adherence, goal alignment,
abilities to assessing system-level behavior. Trust must be built                       domain-specific evaluation, and adversarial robustness, is pro-
through sequences of actions rather than isolated outputs.                              vided in Table IV.
This change highlights the need for evaluation frameworks
that are compositional, capable of reasoning about component
                                                                                        A. Base Operational Metrics
interactions, and sensitive to failures that only emerge in long-
term, multi-agent, or tool-integrated scenarios.                                            1) Tool Utilization Efficacy (TUE): The ability of agentic
   Figure 5 summarizes this progression toward a composable                             systems to communicate with external tools and APIs is
agentic evaluation [69]. The upper layer captures four comple-                          a major source of their usefulness or ’utility’. The choice
mentary evaluation lenses: representation-level evaluation asks                         to use a tool, however, creates a failure mode called ”tool
what the model internally encodes; reasoning-level evaluation                           hallucination,” in which an agent tries to use a nonexistent
examines how it reaches conclusions; behavior-level evalua-                             tool or sends incorrect parameters [72], [73].
tion tests what it outputs or does; and risk-level evaluation as-                           The mathematical formulation for Tool Utilization Efficacy
sesses what harmful capabilities it may enable. However, these                          is:
layers remain incomplete for agentic AI unless their evidence
can be composed across execution over time. The lower layer,                               T U E = α · (Tool Selection Accuracy)
therefore, highlights the additio nal requirements of agentic                                           + β · (Tool Usage Efficiency)
evaluation: assessing full trajectories, multi-step interactions,                                                                     + γ · (API Call Precision)
compounded errors, tool use, and environmental feedback.
This motivates a shift from isolated benchmark scores toward                            where α, β, γ are adjusted tunable weights based on the
composable, system-level evaluation of how agents behave                                specific criticality of the application. In this context, Tool
across long-horizon, tool-integrated, and environment-coupled                           Selection Accuracy refers to the rate at which the AI chooses
workflows.                                                                              the most appropriate tool for a given task, while Tool Usage
                                                                                        Efficiency provides a measure of how optimally the AI utilizes
VII. Q UANTITATIVE M ETRICS FOR AGENTIC W ORKFLOWS                                      those selected tools by considering factors such as unnecessary
    The research community has developed specific metrics to                            calls and resource usage. Finally, API Call Precision accounts
assess the internal effectiveness and logical integrity of agentic                      for the precision and appropriateness of the specific parameters
components, thereby going beyond ”black-box” evaluations.                               used during the execution of those API calls [71].
The Agentic Application Evaluation Framework (AAEF) iden-                                  This metric is particularly important for applications such
tifies four main quantitative metrics: Tool Utilization Efficacy                        as flight planning or medical diagnosis, where selecting the

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
wrong data source (e.g., using a weather API instead of a                                     number of attempted steps in a mission (P EER =
                                                                                                F ailures
NOTAM database) could paralyze the entire workflow [73].                                      T otal Steps ).
   2) Memory Coherence and Retrieval (MCR): Agents must                                    Planning failures frequently manifest when an agent’s in-
maintain persistent context over long time horizons, unlike                             ternal model is too rigid. For instance, in aviation, a failure
traditional chatbots. An agent may ”forget” user-imposed                                to adapt to a sudden Temporary Flight Restriction (TFR) can
constraints due to memory issues, such as context window                                compromise a mission. Similarly, in critical infrastructure,
saturation or ineffective retrieval, leading to undesired results.                      an agent must be able to instantly reroute planning during
The agent’s capacity to retain and use information is measured                          a change in network topology in a power grid to maintain
by MCR:                                                                                 stability. A high SPI indicates an agent that is not only a
                                                                                        precise planner but also a resilient executor in stochastic
                               Cps × Rinf o
                        M CR =               ,                (1)                       environments [73].
                                 1 + Lret                                                  4) Component Synergy Score (CSS): The CSS evaluates the
where the constituent variables are defined as:                                         caliber of interactions in multi-agent systems, where indepen-
   • Context Preservation Score (Cps ): The ratio of main-                              dent agents work together to resolve challenging issues:
      tained contextual anchors Am to the total active anchors                                                        CCU R · W CI
      At established in the prompt sequence, calculated as                                                    CSS =                                  (3)
                                                                                                                        1 + CCR
      Cps = AAmt . This measures the agent’s logical consistency
                                                                                           where the constituent variables are defined as:
      across a session.
                                                                                           • Cross-Component Utilization Rate (CCU R): How of-
   • Information Retention Rate (Rinf o ): The proportion of
                                                                                              ten information or outputs from one component are
      specific data points I successfully retrieved from a long-
                                                                                              effectively used by another. This is calculated as the
      term memory store or past context after a decay period
                                                                                              ratio of successfully ingested shared outputs to the total
      or token offset, defined as Rinf o = Irecalled
                                               Itotal .                                       number of outputs generated.
   • Retrieval Latency (Lret ): The temporal delay (usually
                                                                                           • Workflow Cohesion Index (W CI): A measure of the
      measured in seconds for human applications) between a
                                                                                              seamless integration among components. This would be
      query and the successful injection of retrieved context
                                                                                              the inverse of the average latency, or ”handoff friction,”
      into the model’s active window. The constant 1 is added
                                                                                              between agents, where 1 represents a seamless, immedi-
      to the denominator to normalize for near-zero latency and
                                                                                              ate transition.
      prevent mathematical instability [70], [71], [73].
                                                                                           • Component Conflict Rate (CCR): The frequency of
   The Information Retention Rate is measured by tagging                                      conflicts or inconsistencies between different compo-
specific data items and checking for their correct retrieval                                  nents [71]. This is the number of redundant tasks or
across intervals. High retrieval latency is penalized because                                 deadlocked states divided by the total number of task
slow agent responses can make a system impractical for                                        cycles.
real-time operations, especially during pre-flight checks or
                                                                                           Cross-component utilization tracks how effectively infor-
intrusion response [74].
                                                                                        mation flows between specialized agents (e.g., a ”researcher
   3) Strategic Planning Index (SPI): Strategy formulation can
                                                                                        agent” and a ”summarizer agent”) [71]. A high Component
be seen as the cognitive core of agentic AI. The SPI assesses
                                                                                        Conflict Rate indicates that agents duplicate work, oscillate
the agent’s proficiency in goal decomposition and its ability
                                                                                        handoffs, or create deadlocks, all of which erode system-level
to adapt to environmental change.
                                                                                        trust [70], [72].
   The index is defined by the following equation:
                                                                                        B. Safety and Policy Adherence
               SP I = (GDE · P A) · (1 − P EER)                                 (2)
                                                                                           The ”Safety Gap”, the notable discrepancy between nominal
Where the constituent metrics are defined as:                                           task completion and policy-compliant execution, is a crucial
 • Goal Decomposition Efficiency (GDE): The AI’s ability                                finding in recent agentic research. Agents often use shortcuts
   to break down complex, multi-stage goals into logical,                               or disregard safety procedures to achieve high success rates,
   manageable sub-tasks. This is the ratio of successfully                              according to benchmarks such as ST-WebAgentBench [75] and
   identified sub-tasks to the optimal number of steps re-                              AgentHarm [63]. This type of metric is particularly important
                                Subtasks
   quired for a goal (GDE = Subtasksidentif   ied
                                         optimal
                                                  ).                                    for enterprise applications.
 • Plan Adaptability (PA): The degree to which the agent                                   ST-WebAgentBench introduces the Completion Under Pol-
   adjusts its roadmap in response to dynamic circum-                                   icy (CuP) metric to evaluate agents against enterprise-grade
   stances or unforeseen constraints. This is measured by                               constraints across six dimensions: User Consent, Boundary
   the percentage of successful reroutes completed within                               Compliance, Strict Execution, Hierarchy Adherence, Robust-
   a predefined latency threshold after an environmental                                ness, and Error Handling [75], [76]. The associated metrics,
   trigger.                                                                             including Completion Rate (CR), Completion Under Policy
 • Plan Execution Error Rate (PEER): The frequency of                                   (CuP), Partial CuP (pCuP), and Risk Ratio, are summarized
   failures or deviations encountered during the physical or                            alongside all other section metrics in Table IV.
   digital execution of planned actions [71]. This is simply                               For example, an agent adhering to Boundary Compliance
   the total number of failed actions divided by the total                              would be restricted from finalizing any financial transaction

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
exceeding $5,000 without first surfacing a request for dual                                  Beyond following technical standards, it is important to
authorization from a verified human supervisor.                                           assess the agent’s ethical profile using a Harm-Reduction
   According to evaluations of state-of-the-art agents, over                              Index. This index offers a complete view of the system by
38% of successful tasks violated at least one safety policy, with                         combining three qualitative measures:
the CuP dropping to 15.0% even though the nominal success                                    • Hallucination Rate: How often the agent makes false
(CR) may reach 24.3% [75]. For instance, the company may                                        claims.
be held legally liable if a sales representative retrieves pricing                           • Toxicity Score: Identifying harmful outputs or biased
successfully but does so by scraping unapproved competitor                                      language.
websites. Agents are unintentionally encouraged to avoid ap-                                 • Fairness Metrics: Evaluating if the agent’s actions lead
proval workflows or to disregard consent checks to maximize                                     to fair outcomes for different groups.
efficiency if only CR is measured [76].                                                      By merging behavioral Goal-Drift Scores with broader
                                                                                          safety indices discussed in previous sections, evaluators can
                                                                                          ensure that an agent is not only efficient in its task but also
C. Measuring Goal Drift                                                                   remains aligned with human values throughout its operational
   Goal Drift, or an agent’s tendency to progressively stray                              life [77].
from its initially specified objective, poses a serious risk
                                                                                          D. Domain-Specific Metrics
to autonomous agents operating independently for extended
periods [77]. Even though an agent may begin a task perfectly                                The idea of trustworthiness is not fixed; it varies depending
aligned, its objectives may shift subtly as it gives in to external                       on a system’s specific context and goals. For example, in
pressures or pursues instrumental ends, such as generating                                critical infrastructure, a power grid agent sees trustworthiness
money to accomplish a larger mission. In other words, an                                  as physical reliability. Its main job is to continually meet
agent is more likely to ”forget” the mission’s original purpose                           hardware requirements, such as voltage stability and frequency
and begin imitating the distractions it encounters in its own                             control, to avoid major blackouts. In contrast, a cybersecurity
conversation history, the more involved it becomes in its                                 agent works within a logic-based system. Here, trust is judged
work [78].                                                                                by how well it can implement quick containment measures
   1) Detecting Drift: It is challenging to identify goal drift                           and handle escalation processes to reduce digital threats. The
because it is not always abrupt; rather, it is a gradual dete-                            first focuses on physical laws, while the second focuses on
rioration of intent that is missed by single-turn benchmarks.                             protecting information integrity. Therefore, an agent consid-
Researchers use a Goal-Drift Score to quantify this [78], which                           ered ”trustworthy” in one area may not work well in the other
penalizes deviations by directly comparing the agent’s inter-                             because of these differing priorities.
mediate plan states and actions to the original specification.                               1) 6G and Autonomous UAV Systems (α3 -Bench): For au-
This is frequently divided into two distinct behaviors:                                   tonomous Unmanned Aerial Vehicles (UAVs) operating under
                                                                                          the dynamic and often unpredictable constraints of next-
  • Goal Drift through Actions (Commissions): This                                        generation networking, the α3 -Bench framework introduces
    gauges instances in which an agent willfully acts im-                                 a unified evaluation paradigm [79]. Unlike traditional bench-
    properly, such as purchasing stocks that defy a ”green”                               marks that focus on isolated reasoning tasks, α3 -Bench models
    mandate in the name of profit.                                                        mission execution as a language-mediated, multi-turn control
  • Goal Drift through Inaction (Omissions): This is more
                                                                                          loop between an LLM-based agent and a human operator,
    frequent and occurs when an agent neglects to correct a                               grounded in realistic 6G conditions [79].
    misaligned state, like when it was instructed to switch                                  The framework evaluates agent performance through a com-
    back to a carbon-neutral goal but neglects to sell off                                posite α3 metric, which aggregates six critical pillars into a
    ”dirty” stocks.                                                                       weighted score:
   Even the best models, such as Claude 3.5 Sonnet, have                                     • Task Outcome (TO): Measures mission completion suc-
demonstrated detectable drift in simulated stock trading en-                                    cess and adherence to strict JSON schema requirements.
vironments after about 100,000 interactions [78]. This drift                                 • Safety Policy (SP): Assesses compliance with flight
is closely linked to ”pattern-matching”; instead of following                                   constraints. The score is initialized at 1.0, with fixed
the system prompt hidden at the very top, the model starts                                      penalties for altitude violations and No-Fly Zone (NFZ)
treating the various distractions and conflicting goals in its                                  intrusions [79].
context window as the new ”norm” to follow.                                                  • Tool Consistency (TC): Evaluates the semantic and
   2) Mitigation: Practitioners employ Strong Goal Elicitation                                  structural alignment between the agent’s Model Context
to halt the ”drift.” Rather than simply telling an agent to                                     Protocol (MCP) tool calls and the resulting environmental
”minimize emissions,” you need to give it explicit instructions                                 observations.
to ignore all other pressures and concentrate only on the                                    • Interaction Quality (IQ): Measures the grounding of the
main objective. This ”strong” instruction greatly improves                                      dialogue and ensures strict speaker alternation between
an agent’s resilience against adversarial noise, according to                                   the operator and the agent.
research. Moreover, the agent’s ”eyes on the prize” can be                                   • Network Robustness (NR): Quantifies the agent’s re-
maintained during long-horizon tasks by implementing explicit                                   silience and adaptive reasoning under degraded 6G condi-
goal reminders or constrained planning mechanisms [77].                                         tions, including jitter, packet loss, and fluctuating latency.

      This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
  •   Communication Cost (CC): Penalizes excessive token                                    Beyond operational performance, the trustworthiness of
      consumption and redundant protocol overhead to encour-                              autonomous agents depends on their ability to resist attacks
      age efficient reasoning.                                                            and prevent data theft. Additional security-focused metrics
   To facilitate cross-model comparison across varying com-                               include:
putational footprints, α3 -Bench introduces reliability-adjusted                            • PII Leakage Rate: Measures how often an agent acci-
                                       3                                                       dentally reveals Personally Identifiable Information (PII)
and efficiency-normalized scores: αper-sec   (performance per
                             3                                                                 from its underlying weights or Retrieval-Augmented Gen-
second of latency) and αper-1k (performance per 1,000 to-
kens) [79]. Empirical evaluations using this benchmark reveal                                  eration (RAG) data stores. This is an important privacy
that while state-of-the-art frontier models maintain high base-                                metric for agents managing sensitive enterprise or user
line mission success (TO and SP ≥ 0.95), their performance                                     data [82], [83].
robustness can degrade by 30–40% under adverse network                                      • Jailbreak Success Rate (JSR): Quantifies the proportion
conditions [79]. These findings highlight a critical gap in                                    of adversarial prompts, like ”Do Anything Now” (DAN)
current agent design, underscoring the need for network-aware                                  variants or complex role-play attacks, that successfully
architectures to enable reliable 6G-enabled aerial autonomy.                                   get past the model’s safety measures and refusal lay-
   2) Cybersecurity Operations: In today’s security opera-                                     ers [83].
tions, the main aim of using autonomous agents is to reduce                                 • Prompt Infection Probability: In multi-agent systems,
alert fatigue and improve threat containment lifecycles. People                                this metric tracks how quickly a single harmful input
now assess Traditional Security Operations Centers (SOCs)                                      can spread through a group. It can ruin the execution
and Managed Detection and Response (MDR) services more                                         state or decision-making logic of other agents through
on how well they can shift from human-based triage to agent-                                   communication between them [84].
assisted responses [74].                                                                    • Chain-of-Trigger (CoTri) Robustness: Evaluates the
   The efficacy of these agents is quantified through a set                                    agent’s ability to resist sequential, multi-step triggers that
of core operational metrics, including Mean Time to Detect                                     aim to divert it from its main mission through gradual
(MTTD), Mean Time to Respond (MTTR), Containment Rate,                                         manipulation. Recent research on agentic backdoors sug-
and Escalation Rate, which are summarized alongside all                                        gests that this metric checks if the agent maintains task
other section metrics in Table IV. These metrics serve as                                      integrity when faced with ”Chain-of-Trigger” sequences
benchmarks for evaluating the autonomy and reliability of                                      that unexpectedly try to influence robustness using hidden
security agents in dynamic enterprise environments.                                            triggers [84].
   While both SOC and MDR frameworks use these metrics,
MDR models usually prioritize Detection Accuracy, which is                                             VIII. A PPLICATIONS IN P OWER S YSTEMS
the ratio of True Positives to False Positives. This focus is                                Power systems provide a representative critical infrastruc-
important because autonomous agents that create too many                                  ture domain for studying trustworthy agentic AI because
false alarms can disrupt real business workflows. This under-                             grid operations combine cyber-physical dynamics, strict en-
mines the operational efficiency they are meant to improve. As                            gineering constraints, safety-critical decisions, and human
a result, the development of cybersecurity agents is moving                               operator oversight. Recent work shows a transition from
toward ”risk-based outcomes.” Here, success is measured by                                conventional AI models for forecasting, optimization, and
reducing material impact rather than just counting the number                             control toward LLM-enabled agents that can interpret natural-
of alerts handled.                                                                        language requests, retrieve grid-specific knowledge, invoke ex-
   3) Adversarial Robustness and Security Metrics: Trustwor-                              ternal solvers, and coordinate multi-step workflows. Roadmap
thiness is seriously damaged if a system can be directed                                  and review studies frame this transition as a shift from
toward harmful purposes. Adversarial testing for agents should                            passive model-in-the-loop analytics [85]–[88], to agent-in-the-
go beyond single-turn ”jailbreaks” and focus on multi-turn                                loop grid intelligence, where foundation models, standardized
”exploit generation. [80]”                                                                tool interfaces, and workflow orchestration support planning,
   The HarmBench framework offers a standardized way to                                   operations, restoration, and energy management tasks (Fig. 6)
evaluate ”robust refusal behaviors. [67]” It measures Attack                              [89]–[92]. The reviewed works, therefore, reveal two sides of
Success Rate using an open-source classifier calibrated to                                the same story: emerging design patterns that make power-
GPT-4 validation accuracy.                                                                system workflows more agentic, and systemic failure modes
                                     N                                                    that appear when semantic reasoning, tool invocation, and
                               1 X
                   ASR =             Success(fT (xi ), y)                         (4)     operational decision support are connected to critical grid
                               N i=1                                                      functions.
   Experimental results indicate that larger models do not
ensure better safety. In fact, vision-based LLM agents show                               A. Emerging Design Patterns
ASRs of up to 80% in certain contextual attacks [67]. Addi-                                  1) Agent-in-the-Loop Grid Intelligence: A first design pat-
tionally, while automated attacks like GCG result in low ASRs                             tern is the progression from task-specific AI models toward
on some defenses, multi-turn human red teaming can uncover                                agent-in-the-loop grid intelligence. This evolution can be
failures with ASRs reaching 75%. This shows that relying only                             summarized in three stages. The first stage corresponds to
on numbers can give a false sense of security [81].                                       traditional AI/ML methods used as task-specific predictors,

      This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
                                                                   TABLE IV
                            Q UANTITATIVE M ETRICS FOR AGENTIC W ORKFLOWS AND T HEIR T RUSTWORTHINESS I MPLICATIONS

Metric                                    Workflow point                  Dimension       Trustworthiness implication
Tool Selection Accuracy (TSA) [71]        Tool use                        R&R             Flags hallucinated or misrouted tool calls
Tool Usage Efficiency (TUE) [71]          Tool use                        R&R             Identifies wasteful or redundant invocations
API Call Precision (ACP) [71]             Tool use                        P&S             Detects malformed parameters that may expose attack surfaces
Context Preservation Score (Cps ) [71]    Memory update                   R&R             Measures whether session anchors remain consistent
Information Retention Rate                Memory update                   R&R             Captures forgotten constraints that create silent risk
(Rinf o ) [71]
Retrieval Latency (Lret ) [71]            Memory update                   R&R             Indicates whether memory access supports real-time trust
Goal Decomposition Efficiency             Planning                        R&R             Reveals brittle or overly coarse decomposition
(GDE) [71]
Plan Adaptability (PA) [71]               Planning                        R&R             Measures resilience when goals or context change
Plan Execution Error Rate (PEER) [71]     Action/execution                R&R             Quantifies direct execution failures
Cross-Component Utilization Rate          Communication/coordination      R&R             Detects poor information flow and duplicated work
(CCUR) [71]
Workflow Cohesion Index (WCI) [71]        Communication/coordination      R&R             Measures handoff friction in multi-agent workflows
Component Conflict Rate (CCR) [71]        Communication/coordination      A&A             Exposes conflicts that obscure responsibility
Completion Rate (CR) [75]                 Action/execution                S&CS            Provides a baseline for measuring the safety gap
Completion Under Policy (CuP) [75]        Validation                      S&CS            Measures successful completion under explicit constraints
Partial CuP (pCuP) [75]                   Validation                      S&CS            Credits cautious partial progress under constraints
Risk Ratio [75]                           Validation                      S&CS            Localizes the type and severity of violations
Goal-Drift Score [78]                     Monitoring/re-evaluation        S&CS            Detects gradual misalignment from intended objectives
Drift via Commissions [78]                Monitoring/re-evaluation        S&CS            Captures harmful actions taken by the agent
Drift via Omissions [78]                  Monitoring/re-evaluation        S&CS            Captures failures to self-correct or intervene
Hallucination Rate [77]                   Reasoning                       S&CS            Measures false claims that may cause downstream harm
Toxicity and Fairness Scores [77]         Reasoning/action                S&CS            Evaluates value alignment beyond task success
Task Outcome (TO) [79]                    Action/execution                R&R             Measures mission-level reliability
Safety Policy (SP) [79]                   Validation                      S&CS            Measures compliance with hard safety constraints
Tool Consistency (TC) [79]                Tool use                        T&I             Flags divergence between tool calls and observations
Interaction Quality (IQ) [79]             Communication/coordination      T&I             Supports human oversight through dialogue quality
Network Robustness (NR) [79]              Perception/observation          R&R             Measures degradation under realistic network conditions
Communication Cost (CC) [79]              Communication/coordination      R&R             Identifies coordination overhead that limits scalability
Mean Time to Detect (MTTD) [74]           Monitoring/re-evaluation        P&S             Measures speed of threat detection
Mean Time to Respond (MTTR) [74]          Action/execution                P&S             Measures speed of threat neutralization
Containment Rate [74]                     Action/execution                A&A             Indicates whether autonomous containment is traceable
Escalation Rate [74]                      Monitoring/re-evaluation        A&A             Marks the boundary between autonomy and oversight
Attack Success Rate (ASR) [67]            Validation                      P&S             Measures exploitable bypasses of safeguards
PII Leakage Rate [82]                     Memory update                   P&S             Quantifies privacy exposure through retained or leaked data
Jailbreak Success Rate (JSR) [83]         Validation                      P&S             Measures robustness of refusal and policy layers
Prompt Infection Probability [84]         Communication/coordination      P&S             Captures whether one agent can corrupt the workflow
CoTri Robustness [84]                     Monitoring/re-evaluation        P&S             Measures resistance to slow, multi-step manipulation

 Note: S&CS = safety and constraint satisfaction; R&R = robustness and reliability; T&I = transparency and interpretability; A&A = accountability and
auditability; P&S = privacy and security.



classifiers, or optimizers. The second stage introduces LLM-                             still allowing domain tools and human oversight to remain part
assisted power systems, where models support dispatchers and                             of the loop.
engineers through natural-language interaction, data interpre-                              2) Solver-in-the-Loop Engineering Grounding: A second
tation, code generation, and simulation. GAIA and local fine-                            design pattern is the separation of semantic reasoning from
tuned/RAG-based LLM environments are examples of this                                    numerical execution. Across the selected literature, LLMs
assistant-oriented phase [93], [94]. The third stage is agentic                          interpret user intent, decompose tasks, retrieve context, and
AI, in which the model is embedded within an architecture                                select actions, while trusted engineering tools perform power-
capable of planning, tool invocation, memory/context man-                                flow, OPF, contingency, simulation, or scheduling computa-
agement, feedback correction, and multi-agent coordination.                              tions. This solver-in-the-loop design is central to GridMind,
Representative examples include X-GridAgent for power-grid                               X-GridAgent, PowerChain [95]–[97] and a feedback-driven
analysis [95], GridMind for OPF and contingency analysis                                 simulation framework [101].
[96], PowerChain for distribution-grid workflow automation
                                                                                            This pattern directly supports safety and constraint satis-
[97], Grid-Agent for violation remediation [98], DrAgent for
                                                                                         faction. In power systems, agent outputs must respect voltage
disturbance-record analysis [99], and agentic planning frame-
                                                                                         limits, thermal ratings, generation constraints, power-flow fea-
works for simulation orchestration [100].
                                                                                         sibility, restoration requirements, and user/device constraints.
   This pattern is important because it changes the role of AI                           Grounding LLM reasoning in deterministic solvers, simu-
in power systems. The model is no longer only producing a                                lators, domain-specific tools, or verified workflows reduces
prediction or recommendation; it is increasingly embedded in                             unsupported language-model reasoning [95]–[97], [101]. Grid-
a workflow that interprets operator intent, selects tools, reasons                       Agent goes further by adding a validation agent, sandboxed
over intermediate results, and supports multi-step engineering                           execution, and rollback before accepting remediation actions
tasks. Its trustworthiness value comes from making grid intel-                           [98]. GAIA also evaluates safety but remains explicitly ad-
ligence more interactive, modular, and operator-facing, while                            visory, leaving final decisions to human dispatchers [93].

     This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
                                                                                        and black-start reasoning, while PowerAgent and foundation-
                                                                                        model studies outline broader visions for operator copilots
                                                                                        and grid-aware AI workflows [89], [90], [93]. For grid anal-
                                                                                        ysis, X-GridAgent and GridMind automate power-flow, OPF,
                                                                                        contingency, and topology-related workflows through natural-
                                                                                        language interfaces and solver calls [95], [96]. For distribution
                                                                                        systems, PowerChain targets automated analysis workflows
                                                                                        on real utility data [97]. For control-oriented applications,
                                                                                        Grid-Agent studies violation detection and remediation under
                                                                                        voltage, thermal, and connectivity constraints [98]. For event
                                                                                        analysis, DrAgent applies tool-using agents to disturbance
                                                                                        records [99]. Finally, the HEMS framework extends agentic
                                                                                        AI to behind-the-meter residential scheduling from natural-
                                                                                        language user preferences [102].
                                                                                           This pattern improves usability and interpretability by ex-
                                                                                        posing intermediate plans, tool calls, retrieved context, solver
                                                                                        outputs, and natural-language explanations. GridMind and X-
                                                                                        GridAgent make grid studies more accessible by translating
                                                                                        complex solver-driven analyses into conversational workflows
                                                                                        [95], [96]. DrAgent provides step-by-step reasoning for fault
                                                                                        analysis, allowing operators to inspect the diagnostic process
                                                                                        [99]. The HEMS agent similarly improves user interaction
                                                                                        by translating natural-language preferences into appliance
                                                                                        schedules [102]. These features matter because power-system
                                                                                        operators and users need to understand not only the final
Fig. 6. Power-systems adaptation of the multi-agent agentic AI architecture.
                                                                                        recommendation but also the assumptions and computational
                                                                                        path behind it.
Together, these works show that solver-in-the-loop grounding
is becoming a central design principle for trustworthy power-                           B. Systemic Failure Modes
system agents.                                                                             1) Empirical Safety Without Formal Assurance: The first
   3) Hierarchical Specialization and Feedback-Corrected                                failure mode is that safety is still treated mostly as empirical
Workflows: A third design pattern is hierarchical agent spe-                            validation rather than formal assurance. Current systems often
cialization, where different agents perform planning, execu-                            check whether generated workflows, simulations, schedules,
tion, validation, enhancement, or appliance-level control. Grid-                        or recommendations are feasible, but they do not prove that
Agent, the agentic planning framework, and the HEMS agent                               the agentic loop cannot produce unsafe intermediate actions,
demonstrate this modular structure [98], [100], [102]. This                             invalid tool calls, or harmful recommendations under distri-
structure supports workflow decomposition: one component                                bution shift. This is especially important in power systems
can plan, another can execute, another can validate, and                                because even advisory outputs can shape operator decisions
another can explain or refine the result.                                               under time pressure.
   A closely related pattern is feedback-based reliability im-                             The failure mode is therefore not a lack of safety aware-
provement. Several works introduce mechanisms that improve                              ness, but a gap between checked feasibility and assured
agent behavior after errors or incomplete executions. The intro-                        constraint satisfaction. Solver-in-the-loop architectures reduce
duced in [101] use feedback-driven correction for simulations;                          unsupported LLM reasoning, and validation agents or rollback
DrAgent repairs malformed tool-call arguments and caches                                mechanisms improve safety in specific workflows [95]–[98],
repeated computations [99]; PowerChain uses expert-verified                             [101]. However, future systems need explicit safety envelopes,
reasoning trajectories to improve generalization to unseen                              precondition checks for tool calls, fail-safe fallback policies,
distribution-grid analyses [97]; and Grid-Agent uses adaptive                           and clear separation between advisory, supervisory, and actu-
network representations and validation-based remediation [98].                          ation privileges.
These methods demonstrate that agentic workflows can outper-                               2) Narrow Robustness Evidence: The second failure mode
form direct prompting and improve task completion in grid-                              is that robustness evaluation remains narrow. Most evaluations
analysis settings. Their trustworthiness stems from making                              are conducted on benchmark test systems, curated simulation
power-system agents less dependent on a single, fragile model                           tasks, real disturbance records, utility analysis queries, or
response and more capable of iterative correction.                                      price-based scheduling scenarios [96], [97], [99], [101], [102].
   4) Human-Facing Assistance Across the Power-System                                   These settings are valuable, but they do not fully capture long-
Stack: A fourth design pattern is the use of agentic AI                                 horizon operation, cascading failures, corrupted telemetry,
as a human-facing interface across different levels of the                              adversarial prompts, stale topology, or tool-chain outages.
power-system stack. At the bulk-system level, GAIA sup-                                    GAIA makes this limitation visible by revealing weaknesses
ports dispatch, operation monitoring, operation adjustment,                             under rare events, where correct recommendations may still be

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
delayed, or insufficiently urgent [93]. Thus, current reliability                       unauthorized execution, and data leakage [89], [95], [96],
evidence supports feasibility but not yet deployment-grade                              [101], [102].
robustness. For trustworthy power-system agents, robustness                                Some works partially address security-relevant concerns.
must be evaluated not only by task-completion rate, but also                            The local fine-tuned LLM environment emphasizes offline
by behavior under rare contingencies, degraded observability,                           operation for sensitive power-system data [94], while Grid-
unavailable tools, adversarial inputs, and changing grid states.                        Agent considers cyberattack-induced grid violations as part
   3) Visible Reasoning Without Validated Interpretability:                             of its remediation context [98]. Reviews also identify cyber-
The third failure mode is the gap between explanation visibil-                          physical security, failure modes, and safe deployment as major
ity and validated interpretability. Agentic systems often expose                        concerns [91], [92]. Nevertheless, systematic security evalua-
reasoning steps, tool calls, retrieved information, or natural-                         tion is largely missing. Future power-system agents should
language explanations. These traces are useful for debugging                            include least-privilege tool access, typed function schemas,
and operator interaction, but they do not guarantee that the                            sandboxing, provenance checks for retrieved data, adversarial
explanation is faithful, complete, or calibrated to operator                            testing, and explicit authorization barriers for high-impact
needs.                                                                                  actions.
   The review papers emphasize explainability and operator
                                                                                        C. Synthesis
trust as central requirements [91], [92], yet most application
papers do not evaluate explanation quality through human-                                  The reviewed works show that agentic AI in power sys-
subject studies, trust calibration, or improvements in operator                         tems is advancing through four useful design patterns: agent-
decision-making. This matters because a plausible explanation                           in-the-loop grid intelligence, solver-in-the-loop engineering
can still hide an incorrect assumption, an invalid retrieved                            grounding, hierarchical and feedback-corrected workflows,
context, or a misleading chain of reasoning. For power-                                 and human-facing assistance across the grid stack. These
system agents, interpretability must therefore move beyond                              patterns make grid analysis, simulation, dispatch support, dis-
exposing workflow traces toward validating whether those                                turbance analysis, distribution-grid workflows, and residential
traces actually improve operator understanding and decision                             scheduling more interactive, modular, and capable of support-
quality.                                                                                ing multi-step engineering tasks [93], [95]–[102]. At the same
                                                                                        time, they expose five systemic failure modes: safety remains
   4) Incomplete Accountability Across Agentic Workflows:
                                                                                        mostly empirical, robustness evidence is narrow, explanations
The fourth failure mode is the lack of end-to-end account-
                                                                                        are not yet validated, accountability is incomplete, and security
ability across agentic grid workflows. Accountability requires
                                                                                        evaluation remains underdeveloped.
that agent outputs be traceable to user inputs, retrieved data,
                                                                                           The central lesson is that trustworthy power-system agents
tool calls, intermediate states, validation results, and human
                                                                                        must be evaluated not only by task success, but also by unsafe-
approvals. Some systems provide partial auditability by con-
                                                                                        action rate, constraint-violation severity, robustness to rare
struction. PowerChain represents analyses as workflow trajec-
                                                                                        events, explanation usefulness, audit completeness, security
tories [97]; GridMind preserves analytical state and solver-
                                                                                        against misuse, and human override behavior. For power
related information [96]; X-GridAgent uses modular servers
                                                                                        systems, the main challenge is not whether LLM agents can
and memory mechanisms [95]; and DrAgent produces explicit
                                                                                        assist engineers, but whether their autonomy can be bounded,
tool-call plans for fault-analysis tasks [99]. These artifacts can
                                                                                        verified, monitored, and governed well enough for critical-
support post-hoc review and debugging.
                                                                                        infrastructure environments.
   However, most papers do not define accountability as a                                  Table V summarizes representative agentic AI systems in
first-class design objective. They rarely specify responsibility                        power-system applications and evaluates them through our
assignment, operator override logging, tamper-evident records,                          trustworthiness dimensions.
approval chains, or compliance integration with utility pro-
cedures. For critical infrastructure, auditability must move                                  IX. A PPLICATIONS IN AUTONOMOUS V EHICLES ,
beyond recording tool calls toward structured governance: who                                              ROBOTICS , AND UAV S
requested the action, what data were used, which constraints                               Autonomous vehicles, robotics, and UAVs provide a high-
were checked, who approved the recommendation, and how                                  stakes, embodied setting for trustworthy agentic AI, as de-
the system can be reconstructed after an incident.                                      cisions made by agents can directly affect physical motion,
   5) Expanded Misuse Attack Surface: The fifth failure mode                            human safety, and cyber-physical infrastructure. In these sys-
is the expanded security and misuse attack surface introduced                           tems, the agentic loop does not end with text generation or
by tool-using power-system agents. Security is one of the least                         recommendation; it can extend from perception and reasoning
mature trustworthiness dimensions in the reviewed literature                            to planning, control, and actuation (Fig. 7). This creates a
on power-system agents. Tool-using agents increase grounding                            sharper trust problem than in purely digital domains. The
and numerical reliability, but they also expand the attack                              reviewed works, therefore, reveal two sides of the same story:
surface through APIs, simulators, databases, RAG pipelines,                             emerging design patterns that bind high-level autonomy to
memory modules, and actuation interfaces. MCP-style and                                 safety, monitoring, and accountability mechanisms, and sys-
tool-based architectures in PowerAgent, X-GridAgent, Grid-                              temic failure modes that appear when perception, reasoning,
Mind, Jia et al., and HEMS therefore create potential risks                             communication, and actuation are connected in real-world
such as prompt injection, malicious retrieval, tool misuse,                             environments.

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
                                                                                           Recent work also points toward Zero-Trust Architectures
                                                                                        (ZTA) and hardware-based trust, such as TPM-based remote
                                                                                        attestation, to verify and attribute autonomous decisions to
                                                                                        authenticated agents. This pattern is important because embod-
                                                                                        ied agents operate across multiple trust boundaries: sensors,
                                                                                        onboard compute, external networks, cloud services, tools, and
                                                                                        actuation modules. Layered trust architectures enable asking
                                                                                        not only whether a decision was safe, but also whether it
                                                                                        originated from an authenticated component operating within
                                                                                        a verified system state.
                                                                                           3) Multi-Layer Threat-Aware Evaluation: A third design
                                                                                        pattern is the use of threat-aware evaluation to expose how em-
                                                                                        bodied agents fail under adversarial conditions. Several works
                                                                                        study attacks on the perception layer, including physical-world
                                                                                        hijacking of visual perception through ControlLoc [108],
                                                                                        LiDAR-induced trajectory-prediction deception [109], and
                                                                                        latency-oriented physical-world attacks such as SlowPercep-
                                                                                        tion [110]. Other work studies physical-layer threats such as
                                                                                        UAV GPS spoofing and GPS spoofing detection [111], [112],
                                                                                        as well as network-layer manipulation in vehicle-to-everything
                                                                                        platforms [113].
                                                                                           More recent threats target the model layer directly. Phys-
                                                                                        ical prompt injection and visual adversarial attacks show
                                                                                        that signs, typographic artifacts, or visual inputs can hijack
                                                                                        vision-language driving agents without any digital manipula-
Fig. 7. Robotics adaptation of the multi-agent agentic AI architecture.                 tion [114], [115]. The α3 -Bench framework is an early step
                                                                                        toward benchmark-based evaluation of UAV agents under 6G
                                                                                        conditions, measuring safety, robustness, and efficiency in a
A. Emerging Design Patterns                                                             more unified setting [79]. Together, these works show that
   1) Actuation-Level Safety Filters and Runtime Assurance:                             trustworthiness in embodied agents must be evaluated across
A major design pattern is to place formally motivated or                                the full perception-to-actuation pipeline rather than only at a
runtime-enforced safety mechanisms at the actuation bound-                              single component.
ary. Control Barrier Functions (CBFs) enforce forward-                                     4) Post-Hoc Explanation and Regulatory Logging: A fourth
invariance constraints so that the system remains within a safe                         design pattern is the use of explanation and logging mecha-
set during operation [103]. Black-Box Simplex architectures                             nisms for audit, debugging, and accident reconstruction. SAFE
provide a runtime assurance structure that can switch from                              introduces saliency-aware counterfactual explanations for deep
an advanced controller to a verified safety controller without                          neural network driving systems [116], while SAFE-RL extends
requiring full access to the internal model [104]. Runtime                              this direction to deep reinforcement-learning policies [117].
assurance for learning-enabled autonomous driving applies a                             These methods support interpretability by identifying how
similar principle by wrapping a learned planner with a low-                             changes in salient inputs could alter system behavior.
level safety monitor [105].                                                                Regulatory logging and cybersecurity management frame-
   This pattern is important because it separates high-level                            works also support accountability by requiring traceability
planning from low-level safety enforcement. The high-level                              and lifecycle governance [106], [107]. Their trustworthiness
agent may reason, plan, or propose actions, but the final                               value is strongest after an incident: they can help reconstruct
actuation layer is constrained by a safety mechanism that can                           what happened, which component was involved, and whether
reject or override unsafe behavior. Its trustworthiness value                           the system followed the required cybersecurity or operational
comes from reducing the risk that an unverified agent directly                          process. In embodied agentic systems, this is essential because
controls physical motion without a validated safety backstop.                           failures may involve multiple layers, including perception,
   2) Layered Trust Architectures for Verified Autonomy: A                              reasoning, tool use, control, actuation, and human approval.
second design pattern is the use of layered trust architectures
that combine regulatory, architectural, and hardware-based
controls. Regulatory frameworks such as UNECE WP.29 R155                                B. Systemic Failure Modes
and ISO/SAE 21434 emphasize cybersecurity management,                                      1) Layered Verification Gap: The first failure mode is the
traceability, and lifecycle-based security engineering for ve-                          verification gap between layers. Low-level safety filters such as
hicles [106], [107]. These standards do not, by themselves,                             CBFs and Simplex-style architectures offer formal or runtime
solve the agentic trust problem, but they establish the need for                        guarantees at the actuation boundary [103]–[105], but the high-
auditable cybersecurity processes and accountability structures                         level reasoning layer, increasingly an LLM or VLM, remains
for autonomous systems.                                                                 unverified. Current designs treat the safety filter as a backstop,

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
yet they rarely characterize how often the high-level planner                           Architectures and hardware-based attestation, so that each
produces unsafe candidates, how the filter degrades under                               decision is both verifiable and attributable, remains an open
distribution shift, or whether a safe fallback exists when both                         design problem.
layers are uncertain.                                                                      5) Fragmented and Capability-Driven Benchmarks: The
   The failure mode is therefore not only unsafe actuation, but                         fifth failure mode is the lack of standardized, trustworthiness-
overreliance on a low-level backstop without quantifying the                            oriented benchmarks for embodied agents. The α3 -Bench
residual risk that survives it. Future systems should define ex-                        framework is an early step for UAV agents under 6G condi-
plicit fallback policies tied to the Operational Design Domain                          tions [79], but most evaluations remain capability-driven or
and determine, before deployment, when a high-level agent                               attack-specific. They typically measure whether the system
may advise, recommend, or directly actuate. This requires a                             completes the task or withstands a specific attack, rather than
notion of graded autonomy, in which actuation authority is                              jointly evaluating safety, robustness, interpretability, account-
granted incrementally and revoked the moment the high-level                             ability, and security.
planner leaves its validated operating envelope.                                           A reusable benchmark should jointly measure these trust-
   2) Cross-Layer and Physically Realizable Attacks: The                                worthiness dimensions across driving, manipulation, and aerial
second failure mode is robustness against physically realizable                         tasks. It should report unsafe-action rate, constraint-violation
and cross-layer attacks. Existing studies often evaluate threats                        severity, human-override behavior, attack success rate, ex-
one layer at a time: perception attacks [108]–[110], physical-                          planation usefulness, and audit completeness alongside task
layer spoofing [111], [112], network-layer manipulation [113],                          success. Without this shift, the field risks producing embodied
and model-layer prompt injection [114], [115] are usually                               agents that appear capable in isolated tests but remain un-
treated separately. In deployment, however, an adversary can                            trusted under real deployment conditions.
combine these vectors, and a defense validated against one
layer may fail against another.                                                         C. Synthesis
   This matters because embodied agents depend on a contin-
uous chain from sensing to interpretation, planning, commu-                                The reviewed works show that embodied agentic AI can
nication, and actuation. A small perturbation at one layer can                          be made safer through four useful design patterns: actuation-
propagate into unsafe behavior at another. The field therefore                          level safety filters, layered trust architectures, threat-aware
needs combined threat models and evaluation protocols that                              evaluation, and post-hoc explanation with regulatory logging.
stress the full perception-to-actuation pipeline under simulta-                         These patterns provide important building blocks for bounding
neous, adaptive attacks rather than single-vector benchmarks.                           autonomy, detecting adversarial failures, reconstructing inci-
   3) Faithful and Timely Interpretability: The third fail-                             dents, and connecting physical actions to cybersecurity and
ure mode is the lack of faithful and timely interpretability.                           accountability processes.
Saliency-based and counterfactual explanations support acci-                               At the same time, the evidence remains fragmented across
dent reconstruction and pre-deployment auditing [116], [117],                           isolated mechanisms and threat models. The main systemic
but they are often produced after the fact and their faithfulness                       failure modes are the verification gap between high-level
is seldom validated. A plausible explanation may identify                               reasoning and low-level safety, vulnerability to cross-layer
visually salient regions or counterfactual changes, but it may                          and physically realizable attacks, insufficiently faithful and
not faithfully represent the causal basis of the agent’s decision.                      timely explanations, missing end-to-end provenance, and the
   This limitation is especially important in embodied systems                          absence of standardized trustworthiness-oriented benchmarks.
because decisions unfold on millisecond timescales. Explana-                            The central lesson is that trustworthy embodied agents must
tions that are useful only for forensic review may not support                          be evaluated at the interfaces where perception becomes
real-time operator oversight. Future explanations should be                             interpretation, interpretation becomes planning, and planning
evaluated for whether they actually improve operator decisions                          becomes physical action. Reliable deployment requires graded
and trust calibration, not only for plausibility or visual appeal.                      autonomy, verified low-level safety layers, combined threat
   4) Missing End-to-End Provenance and Attribution: The                                models, real-time interpretability, tamper-evident provenance,
fourth failure mode is the absence of end-to-end, tamper-                               and benchmarks that measure trustworthiness rather than ca-
evident provenance. Regulatory frameworks mandate cyber-                                pability alone.
security management and traceability [106], [107], yet they
do not specify how to reconstruct the agentic chain that links                            X. A PPLICATIONS IN H IGH -P ERFORMANCE C OMPUTING
perception, reasoning, tool use, actuation, and human approval                             As agentic systems increasingly process large-scale data
into a single auditable record. This leaves a gap between                               within high-fidelity simulations, complex digital twins, and
compliance-oriented traceability and agent-level accountabil-                           heterogeneous systems, the integration of these agents with
ity.                                                                                    High-Performance Computing (HPC) resources has become
   For embodied agents, accountability must answer a concrete                           essential for feasibility. Beyond established conventions of
chain of questions: what the agent perceived, how it interpreted                        trust and resilience in agentic systems, the incorporation of
the scene, which model or tool generated the decision, what                             HPC resources introduces a new critical dimension: resilience
constraints were checked, what action was selected, whether                             at scale [118]. To achieve resilience at scale, efficient methods
a human approved it, and whether the acting component                                   addressing faults in system operations are vital for stable,
was authenticated. Pairing such provenance with Zero-Trust                              large-scale agentic systems; a critical topic in modern agentic

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
                                                                                        resource monitoring, crash detection and recovery actions to
                                                                                        incorporate system state data in decisions towards system
                                                                                        stability [122], [123]. These self-healing mechanisms are in-
                                                                                        tuitively integrated into existing agent actions on HPC topolo-
                                                                                        gies, such as workload distribution and anomaly detection
                                                                                        [124], [125].
                                                                                           In other instances, traditional rollback mechanisms can be
                                                                                        applied through multi-agent interactions as a transactional re-
                                                                                        lation [126]. These systems match actions with their reversals
                                                                                        while maintaining system interaction logs, enabling dynamic
                                                                                        return to safe states without complex coordination between
                                                                                        agents.

                                                                                        B. Systemic Failure Modes
                                                                                           1) Hardware Failures: The first and fundamental source
                                                                                        of failure stems from hardware degradation, which intro-
                                                                                        duces system instability and compromises the predictability
                                                                                        of agentic actions. In exascale environments, these failures
                                                                                        range from total system crashes to data corruption [119].
                                                                                        While standard checkpointing and self-healing mechanisms
                                                                                        can isolate localized node failures in multi-agent systems, they
                                                                                        are ineffective at detecting and responding to data corruption
                                                                                        [127]. This directly degrades agentic system trust from a
                                                                                        hardware perspective, as increased workload scales increase
Fig. 8. High-performance computing adaptation of the multi-agent agentic                the potential for data corruption and hardware failure.
AI architecture.                                                                           2) Memory Latency: The second primary failure mode
                                                                                        covers latency for expensive computations and memory ac-
                                                                                        cess. Computational overheads are consistently optimized per
system design using HPC resources [119]. Works involving
                                                                                        application, though memory access latency has been shown
HPC resources, whether to support agentic deployment or
                                                                                        to be a primary limitation to scaling AI workloads [128].
to enable the agent to act upon, focus on innovating fault
                                                                                        This latency is present within context-window updates, cache
tolerance for systemic failure modes arising from hardware
                                                                                        accesses and weight retrievals for LLM-based applications,
degradation and unsafe agent interactions in large-scale sys-
                                                                                        limiting scalability across large heterogeneous systems. This
tems (Fig. 8).
                                                                                        results in trust degradation in agentic systems, as lengthy
                                                                                        decision times lead to unpredictable behavior when conflicting
A. Emerging Design Patterns                                                             notions of the current system state arise.
   1) Fault Tolerance: As applications push exascale perfor-
mance, the likelihood of faults increases proportionally with                           C. Synthesis
the complexity of data distributions, frequent inter-process
                                                                                           The reviewed works demonstrate the importance in overlap
communication (IPC), and the maximization of parallel hard-
                                                                                        between hardware robustness and agentic trust, as AI applica-
ware [120]. These often manifest as instances of data corrup-
                                                                                        tions consistently face resilience concerns on the operational
tion, message loss, hardware defects and software interrupts,
                                                                                        level. Patterns for design in resilience mechanisms highlight
among others. To mitigate these risks, Fault Tolerance in
                                                                                        the efficacy of checkpointing, self-healing and mult-agent
HPC systems focuses on evaluating, diagnosing and preventing
                                                                                        coordination methods, though this is reliant on domain-specific
faults or failures in both software and hardware components,
                                                                                        implementations. Given the limitations of hardware degrada-
regardless of application [118]. Methods for fault tolerance
                                                                                        tion and memory latency, there is a severe lack of frameworks
range from general purpose Checkpointing rollback proto-
                                                                                        detailing resilience in extreme-scale agentic systems to broadly
cols and software-oriented Algorithm-Based Fault Tolerance
                                                                                        address these challenges. Such solutions would consider a
(ABFT) [121] to distributed repair mechanisms, among similar
                                                                                        combination of adaptive mechanisms for memory efficiency
modalities. The integration of these fault-tolerance methods
                                                                                        and decentralized operational conditions across a wide variety
improves resilience with minimal impact on performance,
                                                                                        of domain applications.
enabling stable agentic deployments.
   2) Multi-Agent Systems: To leverage interactions between
agents to further system resilience, multi-agent deployments                                 XI. A PPLICATIONS IN C OMMUNICATION N ETWORKS
effectively mimic HPC parallelism, enabling system recovery                                Agentic AI enters communication networks by turning high-
through coordination. This adopts fault tolerance through ’self-                        level intent, semantic content, or operational context into
healing’ mechanisms, which tasks agents with features for                               actions that affect the network. This makes communication

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
                                                                                           2) Semantic Communication: From Bits to Meaning: A
                                                                                        second design pattern is the move from syntactic commu-
                                                                                        nication to semantic communication. Instead of optimizing
                                                                                        only for bit-level or symbol-level recovery, semantic com-
                                                                                        munication systems aim to preserve task-relevant meaning.
                                                                                        DeepSC demonstrates this shift through transformer-based
                                                                                        semantic encoding and decoding for text transmission under
                                                                                        noisy channel conditions [133]. DeepSC-S applies the same
                                                                                        principle to speech, showing that speech communication can
                                                                                        be optimized around recovered semantic content and percep-
                                                                                        tual quality rather than exact signal reconstruction [134].
                                                                                           This pattern is important because it makes the commu-
                                                                                        nication process itself more intelligent. The channel is no
                                                                                        longer treated only as a medium for symbols; it becomes part
                                                                                        of a meaning-preserving pipeline. These works show strong
                                                                                        robustness under difficult channel conditions and establish
                                                                                        semantic-level optimization as a useful design principle. In
                                                                                        the context of agentic systems, this matters because agents
                                                                                        often act on interpreted meaning rather than raw signals.
                                                                                           3) Security-First Enhancements and Agent Evaluation: A
                                                                                        third design pattern is the introduction of security and evalua-
Fig. 9. Communication networks adaptation of the multi-agent agentic AI                 tion mechanisms around agentic communication pipelines. In
architecture.
                                                                                        semantic communication, physical-layer semantic encryption
                                                                                        and obfuscation protect the meaning of transmitted content
systems more adaptive and easier to operate, but it also                                rather than only the raw signal [135]. This is important because
changes the trust problem [129]. The system is no longer only                           semantic systems create new forms of exposure: an attacker
transmitting information or optimizing links; it is interpreting                        may target the meaning itself, even when the transmitted
intent, reconstructing meaning, selecting tools, and in some                            symbols are not fully recovered.
cases triggering network behavior (Fig. 9). The reviewed                                   Beyond communication-specific systems, ToolEmu and
works, therefore, reveal two sides of the same story: emerging                          Agent Security Bench provide evaluation frameworks for
design patterns that make communication systems more agen-                              tool-using LLM agents [136], [137]. These works are not
tic, and systemic failure modes that appear when interpretation                         network-management papers, but they are directly relevant to
is connected to actuation.                                                              communication agents because future network agents will rely
                                                                                        on tools, memory, prompts, and multi-step decision pipelines.
                                                                                        They show that agentic systems should be tested not only for
A. Emerging Design Patterns                                                             task success, but also for unsafe tool use, prompt injection,
                                                                                        memory manipulation, and adversarial behavior. This gives
   1) Intent Abstraction and Human-in-the-Loop Control:                                 communication-network research a useful model for pre-
A major design pattern is the abstraction of human intent                               deployment stress testing and security benchmarking.
into machine-interpretable network objectives. LUMI is an
early example of this pattern: it allows operators to express
network intents in natural language, maps them into the Nile                            B. Systemic Failure Modes
intermediate representation, and compiles them into executable                             1) Intent Ambiguity Leading to Unsafe Actuation: The first
configurations [130]. This creates a human-agent network                                failure mode appears at the boundary between human intent
loop in which the agent is not merely assisting the operator                            and system action. Intent-based systems assume that a user
but actively mediating between human goals and network                                  goal can be translated into a correct network behavior, but
behavior.                                                                               natural language intents are often ambiguous, underspecified,
   LLM-based intent extraction for 5G core networks extends                             or context-dependent. LUMI makes this translation more
this idea by using language models as the intent-understanding                          structured through Network Intent LanguagE (Nile), but it
layer for network management [131]. Semantic routing further                            does not fully solve the problem of whether the interpreted
strengthens this direction by routing requests across different                         intent is safe, authorized, or complete [130]. LLM-based intent
model pathways to improve orchestration performance and                                 extraction increases flexibility, but it also increases exposure
efficiency [132]. Together, these works show that intent ab-                            to prompt manipulation and unsafe intent acceptance [131].
straction can improve usability, scalability, and adaptability                             INTENDER makes this risk concrete by showing that intent
in network management. Their trustworthiness value comes                                parsing and state transitions in intent-based networking can
from making intent processing more structured and partially                             become attack surfaces [138]. This means the issue is not
inspectable, especially when intermediate representations or                            only whether the agent understands the user, but whether
routing decisions expose how a request is handled.                                      the system can prevent a misunderstood or malicious intent

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
from becoming an executable network action. The failure                                 adversarial testing, and provenance mechanisms that connect
mode is therefore a missing trust layer between interpretation                          the full pipeline.
and actuation requiring architectural changes and trust-driven
mechanisms [139].                                                                                           XII. C ROSS -D OMAIN I NSIGHTS
   2) Semantic Misalignment: The second failure mode ap-
                                                                                           The reviewed application domains show that trustworthy
pears when a system preserves meaning in a shallow sense but
                                                                                        agentic AI is not defined by a single architecture, benchmark,
fails to preserve the correct meaning for the task. DeepSC and
                                                                                        or evaluation criterion. Figure 5 makes this explicit: with the
DeepSC-S show that semantic communication can improve
                                                                                        exception of dedicated evaluation frameworks such as Claw-
robustness under noisy conditions [133], [134]. However,
                                                                                        Eval [68], whose entire purpose is to probe all five dimensions
semantic similarity or perceptual quality does not necessar-
                                                                                        at once [136], [137], no deployed or applied agentic system
ily guarantee that the reconstructed message is operationally
                                                                                        reviewed in this survey scores strongly on more than two or
correct.
                                                                                        three trustworthiness dimensions simultaneously, and which
   This is referred to as semantic misalignment. A recon-
                                                                                        dimension is left uncovered differs systematically by domain
structed message may appear plausible, fluent, or semantically
                                                                                        rather than by architecture. This is because power systems,
close, while still altering the instruction, omitting important
                                                                                        autonomous vehicles and UAVs, high-performance computing,
context, or leading to an unsafe interpretation. This is es-
                                                                                        and communication networks all instantiate the same under-
pecially dangerous when semantic communication feeds into
                                                                                        lying agentic pipeline, perception, reasoning, planning, tool
decision-making or network-control agents. In that setting, the
                                                                                        use, communication/coordination, memory update, validation,
key question is not only whether the receiver recovered similar
                                                                                        action, monitoring, and audit (Section III), but differ in where
meaning, but whether the recovered meaning is valid for the
                                                                                        along that pipeline interpretation becomes consequence, how
downstream action.
                                                                                        severe and reversible the resulting action is, and how much
   3) Lack of End-to-End Accountability: The third failure
                                                                                        of the pipeline currently carries verifiable evidence rather
mode is the lack of accountability across the full agentic
                                                                                        than best-effort engineering practice. Power systems place that
communication pipeline. Current systems often provide only
                                                                                        boundary at the solver-to-grid interface; robotics and UAVs
partial visibility into a single component. LUMI exposes an
                                                                                        place it at the planner-to-actuator interface; HPC places it at
intermediate intent representation [130]. Semantic commu-
                                                                                        the detection-to-recovery interface; communication networks
nication papers report semantic or perceptual performance
                                                                                        place it at the intent-to-configuration interface. The conse-
metrics [133], [134]. Agent benchmarks expose failures in
                                                                                        quence of crossing that boundary, not the underlying model
tool-using agents [136], [137]. However, these pieces do not
                                                                                        architecture, is what determines how much trust engineering
yet form a comprehensive recoverable accountability chain.
                                                                                        a given domain requires.
   This matters because failures can originate from many
                                                                                           This shared lens is what makes cross-domain synthesis
places: the user intent, the intent parser, the semantic encoder,
                                                                                        possible: it separates what is genuinely domain-specific (grid
the reconstructed message, the routing decision, the tool call,
                                                                                        physics, actuation dynamics, HPC fault models, network in-
or the final network action. Without provenance logs, policy-
                                                                                        tents) from what is a general property of agentic AI as a class
check records, decision traces, and responsibility attribution, it
                                                                                        of systems. Section XII-A identifies the design patterns that
is difficult to determine why a failure occurred or who should
                                                                                        recur across domains precisely because they answer the same
be held responsible. For trustworthy communication agents,
                                                                                        underlying trust question under different physical constraints.
accountability must be built into the entire workflow rather
                                                                                        Section XII-B shows that these same patterns leave behind a
than added after deployment.
                                                                                        common residue of unresolved risk regardless of domain.
C. Synthesis
   The reviewed works show that agentic AI in communication                             A. Recurring Design Patterns
networks is advancing through three useful design patterns:                                1) Tool-Grounded Reasoning and Domain-Expert Execu-
intent abstraction, semantic communication, and security-                               tion: A recurring pattern across all four domains is the
oriented evaluation. These patterns make networks easier to                             separation of semantic reasoning from trusted execution: the
operate, more robust under uncertainty, and better able to                              LLM interprets, decomposes, and plans, but a deterministic,
support autonomous workflows. At the same time, they ex-                                verifiable component actually acts. In power systems, this
pose three systemic failure modes: ambiguous intent can lead                            means LLMs interpret operator requests, decompose tasks,
to unsafe actuation, semantic preservation can still produce                            and retrieve context, but hand off numerical work to power-
incorrect meaning, and partial visibility does not provide end-                         flow, optimal-power-flow, and contingency-analysis solvers
to-end accountability.                                                                  rather than computing grid state themselves [95]–[97], [101].
   The central lesson is that trustworthy agentic communi-                              Communication-network agents follow the same logic in a
cation systems must be evaluated at the interfaces where                                different substrate: natural-language intents and semantic con-
interpretation becomes consequence. The critical boundaries                             tent are converted into intermediate representations or routing
are human intent to machine action, transmitted meaning to                              decisions before they are allowed to touch network config-
task correctness, and agent decision to responsibility. Current                         uration [130]–[132], and tool-using agents are stress-tested
work provides important building blocks, but reliable deploy-                           against this same handoff boundary [136], [137]. Robotics and
ment requires stronger formal constraints, runtime safeguards,                          UAV systems enforce the identical separation at the actuation

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
                                                                  TABLE V
                        R EPRESENTATIVE AGENTIC AI WORKS ACROSS APPLICATION DOMAINS THROUGH A TRUSTWORTHINESS LENS .

Work                                 Focus / Type                          Key Mechanism or Insight                                                  Safety Rob. Interp. Audit Sec.

Power Systems (Sec. VIII)

PowerAgent [89]                      Grid operation/planning roadmap       Foundation model + MCP + workflows                                         △     △      △      △     △
Foundation models [90]               AI–grid interaction                   Foundation-model integration                                               △     △      △      ×     △
Smart-grid review [91]               Safe/explainable smart-grid agents    Review and taxonomy of trustworthy agents                                  △     △      △      △     △
Electrical-engineering review [92]   Agentic AI in EE                      Taxonomy and failure-mode analysis                                         △     △      △      △     △
X-GridAgent [95]                     Grid analysis                         Planning–coordination–action hierarchy                                     △     △      ✓      △     ×
GridMind [96]                        OPF and contingency analysis          LLM agents with deterministic solvers                                      △     △      ✓      △     ×
PowerChain [97]                      Distribution-grid workflows           Verified tool-call trajectories                                            △     ✓      △      ✓     ×
Grid-Agent [98]                      Violation remediation                 Planning, validation, and rollback                                         ✓     △      △      △     △
DrAgent [99]                         Fault/disturbance analysis            ReWOO + tools + argument repair                                            △     △      ✓      △     ×
Agentic planning [100]               Simulation orchestration              Planning, validation, and enhancement agents                               △     △      △      △     ×
Jia et al. [101]                     Power-system simulations              RAG + reasoning + feedback acting                                          △     ✓      △      △     ×
GAIA [93]                            Dispatch support                      Fine-tuned dispatch LLM                                                    △     △      △      ×     △
Local fine-tuned LLM [94]            Secure local analysis                 Offline RAG + planner + sandbox tools                                      △     △      △      △     ✓
HEMS [102]                           Residential scheduling                Orchestrator + appliance agents                                            △     △      ✓      △     △

Autonomous Vehicles, Robotics, and UAVs (Sec. IX)

Control Barrier Functions [103]      Safety filter                         Forward-invariance constraints enforced at the actuation boundary          ✓     △      ×      ×     ×
Black-Box Simplex [104]              Runtime assurance                     Switching to a verified safety controller without model access             ✓     ✓      ×      ×     ×
RTA for learning-enabled AD [105]    Runtime assurance                     Wraps a learned planner with a low-level safety monitor                    ✓     △      ×      ×     ×
α3 -Bench [79]                       Evaluation                            Safety, robustness, and efficiency benchmark for UAV agents over 6G        ✓     ✓      △      ×     △
Physical prompt injection [114]      Threat: model layer                   Typographic injection hijacks VLM driving agents                           △     △      ×      ×     ✓
Visual adversarial attack [115]      Threat: perception                    Adversarial inputs mislead VLM autonomous-driving perception               △     ✓      ×      ×     ✓
ControlLoc [108]                     Threat: perception                    Physical-world hijacking of visual perception                              △     ✓      ×      ×     ✓
LiDAR trajectory attack [109]        Threat: perception                    LiDAR-induced trajectory-prediction deception                              △     ✓      ×      ×     ✓
SlowPerception [110]                 Threat: perception                    Physical-world latency attack on visual perception                         △     ✓      ×      ×     ✓
SAFE [116]                           Explanation                           Saliency-aware counterfactual explanations for DNN driving systems         ×     ×      ✓      △     ×
SAFE-RL [117]                        Explanation                           Saliency-aware counterfactual explainer for deep RL policies               ×     ×      ✓      △     ×
UNECE WP.29 R155 [106]               Standard                              Cybersecurity management system requirements for vehicles                  △     ×      ×      ✓     ✓
ISO/SAE 21434 [107]                  Standard                              Automotive cybersecurity engineering lifecycle                             △     ×      ×      ✓     ✓
GPS spoofing countermeasure [111]    Defense: physical layer               Game-theoretic protection of UAVs against GPS spoofing                     △     △      ×      ×     ✓
GPS spoofing detection [112]         Defense: physical layer               Camera-stream detection of drone GPS spoofing                              ×     △      ×      ×     ✓
V2X security [113]                   Defense: network layer                Securing vehicle-to-everything communication platforms                     ×     △      ×      ×     ✓

High-Performance Computing (Sec. X)

Checkpointing [118]                  Resilience amidst hardware faults     Safe state marking and rollback procedures to enable restoration in        △     ✓      ×      ×     ×
                                                                           the event of failure
Transactional Rollback [126]    Logging-based checkpointing                Pair actions with reversing actions for recovery                           △     ✓      ✓      △     △
Algorithm-Based Fault Tolerance Operational resilience                     Checksum-verified operations to separate verification from hardware        △     ✓      ×      △     △
[121]
Self-Healing [123]              Self-monitoring and recovery               Agentic profiling of system status and responding actions to combat        △     ✓      △      △     ×
                                                                           faults during system processing
Multi-Agent Coordination [122]       Agentic coordination                  Agentic synchronization to enable self-verification of faulty processes    △     ✓      △      ✓     △

Communication Networks (Sec. XI)

LUMI [130]                           Intent abstraction and HITL control   Natural-language intents compiled into executable network configura-       △     △      △      △     ×
                                                                           tions
Intent Extraction for 5G [131]       LLM-based intent extraction           LLMs used for intent understanding in 5G core management                   △     △      △      △     ×
Semantic Routing [132]               LLM-assisted semantic routing         Semantic routing improves orchestration efficiency and modularity          △     ✓      △      △     △
INTENDER [138]                       Security testing for IBN              Intent parsing and state transitions exposed as attack surfaces            △     △      △      △     ✓
DeepSC [133]                         Semantic communication                Meaning-oriented communication under noisy channels                        ×     ✓      ×      ×     ×
DeepSC-S [134]                       Semantic speech communication         Semantic speech transmission robust to channel degradation                 ×     ✓      ×      ×     ×
Secure Semantic Communication        Security-first semantic communica-    Protects semantic content through physical-layer encryption                △     △      ×      ×     ✓
[135]                                tion
ToolEmu [136]                        Agent safety evaluation               Sandbox-based evaluation for unsafe tool-using behavior                    ✓     ✓      ✓      ✓     ✓
Agent Security Bench [137]           Agent security benchmarking           Adversarial benchmarking across prompts, tools, and workflows              ✓     ✓      ✓      ✓     ✓

Legend: ✓ = strong support; △ = partial support; × = weak or missing support. Rob.: robustness/reliability; Interp.: transparency/interpretability; Audit:
accountability/auditability; Sec.: privacy/security. HITL: human-in-the-loop; IBN: intent-based networking; AD: autonomous driving; VLM: vision-language
model; MCP: Model Context Protocol.



boundary through Control Barrier Functions and Simplex-                                        2) Modular and Hierarchical Agent Organization: A sec-
style runtime monitors that sit between a learned planner and                               ond pattern is the decomposition of a single monolithic
the motor commands it produces [103]–[105]. Read together,                                  agent into specialized roles connected by a coordination
these results indicate that trustworthy agentic AI is strongest                             layer. Power-system deployments divide responsibility across
not when the LLM is granted final authority, but when it is                                 planning, execution, validation, enhancement, and appliance-
demoted to an orchestrator whose outputs are grounded in                                    level agents [98], [100], [102], while HPC multi-agent systems
domain-specific, independently verifiable execution, directly                               separate resource monitoring, crash detection, recovery, work-
operationalizing the safety and robustness dimensions of Sec-                               load distribution, and anomaly detection into distinct roles
tion III at the tool-use and validation points of the ten-point                             [122]–[125]. Communication-network research shows a par-
workflow.                                                                                   allel move toward modular interpretation-and-action pipelines
                                                                                            through intent abstraction, semantic routing, and dedicated

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
tool-use benchmarking [130], [132], [136], [137]. This con-                                2) Robustness Gaps under Rare, Degraded, or Adversarial
vergence suggests that modularity is not an engineering con-                            Conditions: Most current evaluations demonstrate feasibil-
venience but a trust mechanism in its own right: isolating re-                          ity on curated tasks rather than the tail of the operating
sponsibilities keeps any single component’s failure mode local                          distribution. Power-system evaluations lean on test systems,
and inspectable, which is a precondition for the accountability                         curated simulation tasks, and historical disturbance records
dimension discussed below, rather than a byproduct of it.                               [96], [97], [99], [101], [102]; robotics and UAV systems are
   3) Feedback, Validation, Rollback, and Recovery Loops:                               shown to be vulnerable to adversarial patches, trajectory-
A third pattern treats trustworthy behavior as an iterative                             prediction attacks, sensor spoofing, and GPS jamming [108]–
loop rather than a one-shot response. Power-system agents                               [112]; HPC systems must tolerate data corruption, message
use feedback correction, malformed-argument repair, verified                            loss, and scaling-induced hardware failures [118], [120]; and
workflow trajectories, and rollback [97]–[99], [101]; HPC sys-                          communication-network agents must withstand malicious in-
tems rely on checkpointing, algorithm-based fault tolerance,                            tents, semantic misalignment, and unsafe tool use [133], [134],
and self-healing to survive faults at scale [118], [119], [121]–                        [136]–[138]. None of these domains yet reports the kind of
[123], [140]; robotics and UAV systems achieve the equivalent                           systematic operating-envelope characterization, comparable to
through runtime assurance architectures that can revert to                              an Operational Design Domain analysis [12], that would say
a verified safety controller the instant a learned component                            with confidence where an agent’s guarantees end.
leaves its validated envelope [103]–[105]. Despite operating                               3) Partial Auditability instead of End-to-End Accountabil-
on completely different timescales (milliseconds for actuation,                         ity: Several systems expose fragments of the workflow, a
seconds for grid dispatch, and potentially hours for HPC job                            plan, a tool call, an intermediate representation, a reasoning
recovery), all three implementations share the same structural                          trace, but fragment-level visibility does not add up to a recon-
commitment: a system is trusted not because it avoids error,                            structable accountability chain. Power-system systems provide
but because it can detect, correct, and recover from error before                       partial auditability through workflow trajectories, solver state,
the consequences propagate.                                                             and tool-call plans [95]–[97], [99]; robotics and UAV systems
   4) Bounded Autonomy over Unrestricted Autonomy: The                                  require tamper-evident logs spanning perception, decision, and
fourth and most consequential pattern is that the most credible                         actuation for forensic review [116], [117]; communication-
deployments in every domain are bounded-autonomy sys-                                   network systems need provenance across intent, semantic
tems, not fully autonomous ones. Power-system agents re-                                encoding, routing, and final network action [130], [133], [134],
main grounded in solvers, advisory operation, and sandboxed,                            [136], [137]. In every domain, the gap is the same: visibility
rollback-capable execution [93], [96], [98]; robotics and UAV                           into one component does not guarantee that a failure can be
systems require actuation-level safety filters precisely because                        traced back to the decision, tool call, or human approval that
a high-level planning error can cause physical harm [103]–                              caused it.
[105]; communication-network agents require an explicit trust                              4) Expanding Security Surface from Tools, Memory, and
layer between intent interpretation and executable behavior                             Multi-Agent Coordination: The same tool use, retrieval,
[130], [131], [138]; and HPC agents require supervision before                          and coordination mechanisms that ground agent outputs and
autonomous self-healing or workload redistribution is trusted                           enable modularity also expand the attack surface. Power-
at scale [122], [123], [125]. That this pattern reproduces itself                       system agents introduce risk through APIs, simulators, re-
independently across four unrelated engineering communities                             trieval pipelines, and memory modules [89], [95], [96], [101],
is the strongest cross-domain evidence in this survey that unre-                        [102]; robotics and UAV agents face attacks that span phys-
stricted agentic autonomy is not currently a viable deployment                          ical, network, and model layers simultaneously [111]–[115];
target in any critical-infrastructure setting, only its boundary                        communication-network agents face malicious intent parsing,
location changes.                                                                       prompt injection, and memory manipulation [136]–[138]; and
                                                                                        HPC multi-agent systems must secure recovery, coordination,
                                                                                        and workload-management channels against exactly the kind
B. Shared Failure Modes                                                                 of manipulation their autonomy depends on [122]–[125]. This
   1) Unsafe Translation from Reasoning to Action: The de-                              is a structural tension rather than an engineering oversight:
sign patterns above do not eliminate risk; they relocate it to                          every mechanism identified in Section XII-A as strengthening
the interface where interpretation becomes consequence, and                             trust also introduces a new interface that an adversary can
that interface remains the most critical failure point in every                         target.
domain. In power systems, an incorrect recommendation can
violate grid constraints or respond too slowly to a rare event                              XIII. O PEN C HALLENGES AND F UTURE D IRECTIONS
[93], [98]; in robotics and UAVs, perception, planning, or
control errors propagate directly into unsafe physical actuation                        A. Mandating Trustworthiness Metrics Alongside Task Suc-
[108]–[110]; in communication networks, an ambiguous or                                 cess
malicious intent can become an executable network action                                   Most current work still reports task success, workflow com-
[130], [131], [138]. The common thread is that grounding an                             pletion, or automation gains as the primary outcome measure.
agent in tools, solvers, or intermediate representations narrows                        The field needs to shift toward unsafe-action rate, constraint-
this gap without closing it; the translation step itself is rarely                      violation severity, robustness to rare events, explanation use-
subjected to independent, adversarial verification.                                     fulness, audit completeness, and human-override behavior as

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
first-class reported metrics [93], [98], [136], [137], evaluated                        residual risk that survives each domain’s safety filter under a
under long-horizon operation, tool failure, corrupted telemetry,                        common stress model. We envision this as a common outer
and cascading error rather than single-shot tasks [96], [97],                           harness, fault injection, adversarial perturbation, and telemetry
[99], [101], [120]. Until trustworthiness metrics are reported                          corruption, with pluggable domain-specific modules.
with the same rigor as task accuracy, capability will continue
to outpace assurance across every domain surveyed here.                                 D. Provenance Standards: Build Them Before Regulators Do
We propose a standard trustworthiness scorecard, reported                                  Trustworthy agents need records that connect user requests,
alongside task-success metrics in every agentic-AI evaluation,                          retrieved data, intermediate reasoning, tool calls, validation
analogous to model cards for foundation models.                                         results, human approval, and final actions into one recov-
                                                                                        erable chain. Power-system agents should move from tool-
B. Defining Autonomy Boundaries before Deployment                                       call traces to utility-grade audit trails [95]–[97], [99]; robotics
   A major open question is when an agent should advise, rec-                           and UAV systems should maintain tamper-evident perception–
ommend, supervise, or act, and answering it requires domain-                            decision, actuation logs for incident reconstruction [116],
specific commitments rather than a generic autonomy policy.                             [117]; communication-network agents should connect intent
Power systems need explicit boundaries between advisory                                 parsing, semantic encoding, routing, and tool invocation into
output, operator-approved action, and autonomous grid-control                           a single chain [130], [133], [134], [136], [137]. Automo-
privilege [93], [98]; robotics and UAVs need actuation-level                            tive cybersecurity and lifecycle-governance regimes such as
safety constraints that bind before a high-level plan can move                          UNECE WP.29 R155 and ISO/SAE 21434 already require
a motor [103]–[105]; communication networks need policy                                 exactly this kind of end-to-end traceability for vehicle software
checks between natural-language intent and executable config-                           [106], [107]; agentic AI in the other three domains has
uration [130], [131], [138]; HPC needs supervision policies for                         no equivalent requirement yet, despite facing a structurally
self-healing and workload redistribution [122], [123], [125].                           identical accountability problem. Absent a proactive standard,
What is missing is a shared vocabulary for expressing these                             the first cross-domain audit-trail requirement will likely arrive
boundaries so that an autonomy grant in one domain can be                               only after an incident forces it, at which point the field is
compared, audited, and reasoned about using the same terms                              retrofitting rather than leading.
as in another. The human–AI autonomy spectrum in Fig. 10 –
ranging from fully autonomous AI, through human-in-the-loop                             E. Securing Tool-Using and Multi-Agent Workflows
and human-on-the-loop configurations, to human-in-command,
                                                                                           Power-system, robotics/UAV, communication-network, and
offers exactly this shared reference point: each domain-specific
                                                                                        HPC agents each need conventional hardening — least-
boundary described above can be located on this spectrum
                                                                                        privilege tool access, typed schemas, sandboxing, network-
rather than defined from scratch. It is important to note that
                                                                                        and model-layer protection [89], [94]–[96], [101], [111]–
this placement is not static, as some applications can introduce
                                                                                        [115], [122]–[125], [136]–[138], but this is standard software
a dynamic autonomy level that grows with positive feedback.
                                                                                        security practice applied to a new surface. The open problem is
                                                                                        agent-to-agent trust: impersonation, poisoned shared memory,
                                                                                        and cascading failures as a compromised or hallucinating agent
                                                                                        silently corrupts every agent downstream of it. As multi-agent
                                                  Actor




 Autonomous AI      Human-in-the-loop Human-on-the-loop Human-in-Command                deployments grow, this shift from securing a single model to
                                                                            Actor
                                  Actor




 (AI in Control)   (Human/AI as Peer) (Human as Manager) (Full Human Control)
                                                                                        securing trust relationships between models has not yet been
  Increasing AI Autonomy                                  Increasing Human Autonomy     reflected in the field’s threat models.

                                                                                        F. Making Explanations Faithful and Decision-Useful
Fig. 10. Human–AI autonomy spectrum, illustrating more collaborative
interactions in the human-in-the-loop and human-on-the-loop setups.                        Exposing a plan, a tool call, or a reasoning trace does
                                                                                        not automatically make an explanation faithful. Power-system
                                                                                        agents should evaluate whether solver outputs and natural-
C. Robustness under Rare and Adversarial Conditions                                     language explanations actually improve operator decisions and
   Future evaluation must deliberately target rare events, de-                          trust calibration, rather than assuming that visibility equals
graded sensing, corrupted inputs, adversarial prompts, and                              understanding [91], [92], [95], [96], [99]; robotics and UAV
tool-chain outages rather than curated benchmarks. This means                           systems should connect saliency and counterfactual explana-
testing power-system agents against rare grid events and solver                         tions to accident reconstruction and pre-deployment auditing
failures [93], [96], [101]; robotics and UAV agents against sen-                        [116], [117]; communication-network agents should be able
sor and actuator degradation, jitter, packet loss, and adversarial                      to explain how intent, semantic content, and routing choices
perception [108]–[112]; HPC agents against data corruption,                             became a specific network action [130]–[132]. The open prob-
message loss, and processor-level failure at scale [118], [120];                        lem is measuring whether an explanation improves a human
and communication agents against malicious intent, semantic                             decision, not merely whether one was produced. This requires
misalignment, and prompt injection [133], [134], [136]–[138].                           human-subject decision studies under realistic operational time
A cross-domain adversarial test suite, rather than four dis-                            pressure, not static proxies of faithfulness such as agent error
connected ones, would let the field compare the amount of                               correlation or attention-weight agreement.

    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
G. Toward a Reusable Cross-Domain Trustworthiness Frame-                                same rigor as latency, throughput, or accuracy, rather than a
work                                                                                    qualitative aspiration layered on afterward.
   One thesis recurs across the challenges above: agentic AI                               Making that argument actionable rather than rhetorical
trustworthiness is not four separate problems but one problem                           means locating safety, robustness, interpretability, accountabil-
observed from four vantage points. Evaluation, autonomy,                                ity, and security at specific points in an agent’s perception-
robustness, provenance, security, and explanation are each a                            to-action pipeline, organized around five trustworthiness di-
facet of this claim; this final subsection returns to it directly.                      mensions and a ten-point assurance workflow. This backbone
   A reusable framework should compare domains along the                                supports a unified taxonomy of agentic architectures, a catalog
axes that determine risk: the consequences of actions, the                              of concrete mechanisms and quantitative metrics that develop-
required response time, the availability of formal constraints,                         ers can apply when building or evaluating such systems, and
the density of human oversight, the maturity of audit mech-                             an examination of four constraint-bound engineering domains,
anisms, and the exposure of tool, memory, communication,                                power systems, autonomous vehicles/robotics/UAVs, high-
and actuation interfaces. On these axes, power systems repre-                           performance computing, and communication networks, where
sent constraint-bound, human-approved critical infrastructure;                          these mechanisms are already being tested in practice. Reading
robotics and UAVs represent embodied, real-time actuation                               these domains through a shared lens reveals a common set
with millisecond response budgets; HPC represents large-                                of failure modes: an unverified boundary between reasoning
scale resilience and recovery under weak real-time pressure;                            and action, robustness evidence that rarely extends to rare or
and communication networks represent intent and semantic                                adversarial conditions, auditability that covers fragments of a
interpretation, connected to network behavior. α3 -Bench al-                            workflow rather than its full length, and a security surface that
ready demonstrates that a unified, multi-pillar benchmark is                            grows with every tool, memory module, or coordinating agent
achievable within a single domain [79].                                                 added to the system.
   Other safety-critical engineering fields have already made                              Trustworthy-by-design agentic AI is the natural next phase
this transition once. Aviation software assurance and auto-                             for the field: extending this assurance framework beyond the
motive functional safety converged, over decades, on graded                             four domains studied and validating it against real deployment
assurance levels, tied to consequence severity, that make a                             incidents, not benchmark suites alone, so trust is engineered
certification granted in one product line legible to engineers,                         into the pipeline from the outset rather than retrofitted after
auditors, and regulators working on a different one [11],                               failure. Aviation and automotive engineering reached compara-
[12], [14], [106], [107]. Agentic AI has not yet undergone                              ble maturity only once graded, consequence-indexed assurance
this convergence: a validation result for a grid-dispatch agent                         levels made trust evidence portable across products and orga-
and a validation result for a UAV planner currently share                               nizations; agentic AI is at the beginning of that convergence,
no common unit of evidence, even though both are, in                                    not the end of it.
essence, claims about how an autonomous reasoning process
                                                                                                                         R EFERENCES
behaves at the boundary of consequential action. The EU
                                                                                           [1] A. Bandi, B. Kongari, R. Naguru, S. Pasnoor, and S. V.
AI Act’s conformity-assessment requirements for high-risk                                      Vilipala, “The rise of agentic ai: A review of definitions,
systems point in this direction but remain domain-agnostic                                     frameworks, architectures, applications, evaluation metrics, and
in a way that current agentic evaluation practice is not yet                                   challenges,” Future Internet, vol. 17, no. 9, 2025. [Online]. Available:
                                                                                               https://www.mdpi.com/1999-5903/17/9/404
equipped to satisfy [20], [22]. We expect the next phase of                                [2] S. Yao et al., “React: Synergizing reasoning and acting in language
agentic AI research to be defined less by new architectures and                                models,” 2023. [Online]. Available: https://arxiv.org/abs/2210.03629
more by this assurance infrastructure: graded, consequence-                                [3] N. Shinn, F. Cassano, E. Berman, A. Gopinath, K. Narasimhan,
                                                                                               and S. Yao, “Reflexion: Language agents with verbal reinforcement
indexed autonomy levels; adversarial benchmark suites that                                     learning,” 2023. [Online]. Available: https://arxiv.org/abs/2303.11366
generalize across domains rather than multiplying within them;                             [4] S. Yao et al., “Tree of thoughts: Deliberate problem solving
and provenance formats specific enough to support an inci-                                     with large language models,” 2023. [Online]. Available: https:
                                                                                               //arxiv.org/abs/2305.10601
dent investigation, yet general enough to be compared across                               [5] T. Raheem and G. Hossain, “Agentic ai systems: Opportunities, chal-
power systems, embodied robotics, HPC, and communication                                       lenges, and trustworthiness,” in 2025 IEEE International Conference
networks. Building shared infrastructure rather than further                                   on Electro Information Technology (eIT), 2025, pp. 618–624.
                                                                                           [6] A. Nithrakashyap, “Ai agents are breaking bad and CISOs aren’t
domain-siloed capabilities is the central open challenge this                                  ready,” Fast Company, September 2025, impact Council. [Online].
survey identifies.                                                                             Available: https://www.fastcompany.com/91404298/ai-agents-are-bre
                                                                                               aking-bad-and-cisos-arent-ready
                                                                                           [7] S. Damle, “Are we sleepwalking into an agentic AI crisis?” ABA
                           XIV. C ONCLUSION                                                    Banking Journal, December 2025, american Bankers Association.
                                                                                               [Online]. Available: https://bankingjournal.aba.com/2025/12/are-we-s
  Large language models have moved from static, single-turn                                    leepwalking-into-an-agentic-ai-crisis/
prediction to agentic architectures that perceive, plan, invoke                            [8] D. B. Acharya, K. Kuppan, and B. Divya, “Agentic ai: Autonomous in-
tools, and act over extended horizons, often with limited hu-                                  telligence for complex goals—a comprehensive survey,” IEEE Access,
                                                                                               vol. 13, pp. 18 912–18 936, 2025.
man oversight at each step. This shift changes what “reliable”                             [9] O. Al-Refai, R. Sufian, K. Abo Rubeieh, N. A. M. Abu Rmaileh,
means: task competence is no longer sufficient evidence that                                   O. M. F. Abu-Sharkh, and S. Krishnan, “Design of a web-based
a system can be trusted with consequential, physically or                                      platform to leverage matlab functionality for digital engineering,”
                                                                                               in Soft Computing and Its Engineering Applications, K. K. Patel,
operationally binding decisions. Trustworthiness in agentic AI                                 K. Santosh, G. Gomes de Oliveira, A. Patel, and A. Ghosh, Eds. Cham:
must therefore be treated as an engineering property with the                                  Springer Nature Switzerland, 2026, pp. 69–83.


    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
[10] T. Raheem and G. Hossain, “Agentic ai systems: Opportunities, chal-                [30] Y. Y. Chiu et al., “Morebench: Evaluating procedural and pluralistic
     lenges, and trustworthiness,” in 2025 IEEE International Conference                     moral reasoning in language models, more than outcomes,” 2025.
     on Electro Information Technology (eIT), 2025, pp. 618–624.                             [Online]. Available: https://arxiv.org/abs/2510.16380
[11] International Electrotechnical Commission, “Iec 61508 & functional                 [31] R. Campbell, “Zero trust for ai systems: A reference architecture and
     safety,” IEC, Tech. Rep., 2022, accessed: 2025-02-16. [Online].                         assurance framework,” Preprints, February 2026. [Online]. Available:
     Available: https://assets.iec.ch/public/acos/IEC%2061508%20&%20Fu                       https://doi.org/10.20944/preprints202602.0085.v1
     nctional%20Safety-2022.pdf?2023040501                                              [32] A. Zou, Z. Wang, N. Carlini, M. Nasr, J. Z. Kolter, and M. Fredrikson,
[12] C. Shinde. (2024) Navigating SOTIF (ISO 21448) and ensuring                             “Universal and transferable adversarial attacks on aligned language
     safety in autonomous driving. Automotive IQ. Accessed: 2025-02-16.                      models,” 2023. [Online]. Available: https://arxiv.org/abs/2307.15043
     [Online]. Available: https://www.automotive-iq.com/functional-safety/              [33] N. Li et al., “The wmdp benchmark: Measuring and reducing
     articles/navigating-sotif-iso-21448-and-ensuring-safety-in-autonomou                    malicious use with unlearning,” 2024. [Online]. Available: https:
     s-driving                                                                               //arxiv.org/abs/2403.03218
[13] J. Achiam, D. Held, A. Tamar, and P. Abbeel, “Constrained policy                   [34] M. Siman Tov Bustan and N. Zadok, “One step away from
     optimization,” in Proceedings of the 34th International Conference on                   a massive data breach: What we found inside MoltBot,” OX
     Machine Learning - Volume 70, ser. ICML’17. JMLR.org, 2017, p.                          Security Blog, Jan. 2026, accessed: 2026-02-04. [Online]. Available:
     22–31.                                                                                  https://www.ox.security/blog/one-step-away-from-a-massive-data-bre
[14] International Electrotechnical Commission, “Iec 61508 & functional                      ach-what-we-found-inside-moltbot/
     safety,” IEC, Tech. Rep., 2022, accessed: 2025-02-16. [Online].                    [35] R. Aksitov et al., “Rest meets react: Self-improvement for
     Available: https://assets.iec.ch/public/acos/IEC%2061508%20&%20Fu                       multi-step reasoning llm agent,” 2023. [Online]. Available: https:
     nctional%20Safety-2022.pdf?2023040501                                                   //arxiv.org/abs/2312.10003
[15] A. Madry, A. Makelov, L. Schmidt, D. Tsipras, and A. Vladu,                        [36] C. Wang et al., “Q*: Improving multi-step reasoning for llms
     “Towards deep learning models resistant to adversarial attacks,” in                     with deliberative planning,” 2024. [Online]. Available: https:
     International Conference on Learning Representations, 2018. [Online].                   //arxiv.org/abs/2406.14283
     Available: https://openreview.net/forum?id=rJzIBfZAb                               [37] A. Ramachandran, “Deepseek: Revolutionizing ai with open-source
[16] Montana Department of Environmental Quality. (n.d.) Failure modes                       reasoning models -advancing innovation, accessibility, and competition
     effects analysis (fmea). Montana Department of Environmental                            with openai and gemini 2.0,” 01 2025.
     Quality. PDF document. [Online]. Available: https://deq.mt.gov/files/L             [38] Meta Intelligence. (2026) Reasoning model practical guide: Enterprise
     and/Hardrock/Documents/TintinaMines/App%20R%20Failure%20Mo                              comparison and deployment strategies for deepseek r1, openai o3,
     des%20Effects%20Analysis/App%20R%20Failure%20Modes%20Effe                               and gemini 3. Meta Intelligence. Accessed: 2026-06-30. [Online].
     cts%20Analysis.pdf                                                                      Available: https://www.meta-intelligence.tech/en/insight-reasoning-m
[17] UK Ministry of Defence. (2020) ASEMS toolkit: FMEA/FMECA.                               odels
     Defence Equipment and Support (DE&S). Archived version from                        [39] G. Li, H. A. A. K. Hammoud, H. Itani, D. Khizbullin, and
     August 13, 2020. [Online]. Available: https://web.archive.org/web/20                    B. Ghanem, “Camel: Communicative agents for ”mind” exploration
     200813203140/https://www.asems.mod.uk/toolkit/fmeafmeca                                 of large language model society,” 2023. [Online]. Available:
[18] R. Dwivedi et al., “Explainable ai (xai): Core ideas, techniques, and                   https://arxiv.org/abs/2303.17760
     solutions,” ACM Comput. Surv., vol. 55, no. 9, Jan. 2023. [Online].                [40] X. Li, S. Wang, S. Zeng, Y. Wu, and Y. Yang, “A survey on llm-
     Available: https://doi.org/10.1145/3561048                                              based multi-agent systems: workflow, infrastructure, and challenges,”
[19] O. Al-Refai and A. Alabed, “Explainable brain tumor classification                      Vicinagearth, vol. 1, no. 1, p. 9, Oct 2024. [Online]. Available:
     using transfer learning of deep convolutional neural networks,” in 2025                 https://doi.org/10.1007/s44336-024-00009-2
     16th International Conference on Information and Communication                     [41] T. Schick et al., “Toolformer: Language models can teach themselves to
     Systems (ICICS), 2025, pp. 1–6.                                                         use tools,” 2023. [Online]. Available: https://arxiv.org/abs/2302.04761
[20] European Artificial Intelligence Office, “AI Pact: Organisations’                  [42] G. Wang et al., “Voyager: An open-ended embodied agent
     commitments,” European Commission, Tech. Rep., Sep. 2024,                               with large language models,” 2023. [Online]. Available: https:
     accessed: 2025-02-17. [Online]. Available: https://artificialintelligenc                //arxiv.org/abs/2305.16291
     eact.eu/wp-content/uploads/2025/03/2024.09.25-AI-Pact-final.pdf                    [43] Z. Xi et al., “Toolgym: an open-world tool-using environment for
[21] I. D. Raji et al., “Closing the ai accountability gap: defining                         scalable agent testing and data curation,” 2026. [Online]. Available:
     an end-to-end framework for internal algorithmic auditing,” in                          https://arxiv.org/abs/2601.06328
     Proceedings of the 2020 Conference on Fairness, Accountability, and                [44] S.-H. Cho and Y.-S. Lee, “A comparative study of modern AI frame-
     Transparency, ser. FAT* ’20. New York, NY, USA: Association                             works based on architecture, integration, and scalability,” International
     for Computing Machinery, 2020, p. 33–44. [Online]. Available:                           Journal of Advanced Smart Convergence, vol. 14, no. 4, pp. 158–167,
     https://doi.org/10.1145/3351095.3372873                                                 Dec. 2025.
[22] Future of Life Institute. (2025, May) AI act compliance checker                    [45] V. Mavroudis, “Langchain v0.3,” Preprints, November 2024. [Online].
     flowchart (v1.0). Future of Life Institute. Accessed: 2025-02-17.                       Available: https://doi.org/10.20944/preprints202411.0566.v1
     [Online]. Available: https://artificialintelligenceact.eu/wp-content/upl           [46] Google Cloud. (2026) Building managed agents on the Gemini
     oads/2025/07/AI-Act-Compliance-Checker-Flowchart-v1.0 compres                           Enterprise Agent Platform. Google Cloud Documentation. Accessed:
     sed.pdf                                                                                 2026-06-30. [Online]. Available: https://docs.cloud.google.com/gemini
[23] M. Abadi et al., “Deep learning with differential privacy,” in                          -enterprise-agent-platform/build/managed-agents
     Proceedings of the 2016 ACM SIGSAC Conference on Computer                          [47] Google AI for Developers. (2026) Building managed agents with
     and Communications Security, ser. CCS ’16. New York, NY, USA:                           the Gemini API. Google AI Documentation. Accessed: 2026-06-30.
     Association for Computing Machinery, 2016, p. 308–318. [Online].                        [Online]. Available: https://ai.google.dev/gemini-api/docs/custom-age
     Available: https://doi.org/10.1145/2976749.2978318                                      nts
[24] D. Hendrycks, M. Mazeika, and T. Woodside, “An overview of                         [48] Google Cloud. (2026) Interacting with managed agents on the Gemini
     catastrophic ai risks,” 2023. [Online]. Available: https://arxiv.org/abs/               Enterprise Agent Platform. Google Cloud Documentation. Accessed:
     2306.12001                                                                              2026-06-30. [Online]. Available: https://docs.cloud.google.com/gemini
[25] Synopsys. (n.d.) What is ISO 26262 functional safety standard?                          -enterprise-agent-platform/build/managed-agents/interact-with-agents
     Synopsys, Inc. Accessed: 2025-02-17. [Online]. Available: https:                   [49] G. C. Developers and P. Team. (2026, May) I/O ’26 news for agent
     //www.synopsys.com/glossary/what-is-iso-26262.html                                      developers on Google Cloud. Google Cloud Blog. Accessed: 2026-
[26] R. Tamirisa et al., “Tamper-resistant safeguards for open-weight llms,”                 06-30. [Online]. Available: https://cloud.google.com/blog/topics/devel
     2024. [Online]. Available: https://arxiv.org/abs/2408.00761                             opers-practitioners/io26-news-for-agent-developers-on-google-cloud
[27] M. Kaufmann et al., “Testing robustness against unforeseen                         [50] T. Vangalapat and S. Shaikh, “Trustworthy agentic ai: A survey
     adversaries,” 2023. [Online]. Available: https://arxiv.org/abs/1908.080                 and taxonomy of secure coordination and hallucination mitigation in
     16                                                                                      multi-agent large language model systems,” International Journal of
[28] A. Zou et al., “Improving alignment and robustness with circuit                         Innovative Science and Research Technology, p. 1660, 02 2026.
     breakers,” 2024. [Online]. Available: https://arxiv.org/abs/2406.04313             [51] HackerNoon. (2024) Inside the push to standardize communication
[29] ——, “Representation engineering: A top-down approach to ai                              between AI agents. HackerNoon. Accessed: 2026-04-15. [Online].
     transparency,” 2025. [Online]. Available: https://arxiv.org/abs/2310.0                  Available: https://hackernoon.com/inside-the-push-to-standardize-com
     1405                                                                                    munication-between-ai-agents


   This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
[52] Z. Du et al., “Enabling agents to communicate entirely in latent                   [75] I. Levy, B. Wiesel, S. Marreed, A. Oved, A. Yaeli, and
     space,” 2026. [Online]. Available: https://openreview.net/forum?id=rm                   S. Shlomov, “St-webagentbench: A benchmark for evaluating safety
     YbgsehTd                                                                                and trustworthiness in web agents,” 2025. [Online]. Available:
[53] Y. Zheng et al., “Thought communication in multiagent collaboration,”                   https://arxiv.org/abs/2410.06703
     in The Thirty-ninth Annual Conference on Neural Information                        [76] L. R. Sammeta. (2025, Dec.) The AI agent report card you’ve been
     Processing Systems, 2025. [Online]. Available: https://openreview.net                   ignoring: Why 30% of your agent’s “successes” are actually failures.
     /forum?id=tq9lyV9Cml                                                                    Accessed: 2026-02-23. [Online]. Available: https://laxmikumars.medi
[54] Y. Jo and C. Park, “Byzantine-robust decentralized coordination of llm                  um.com/the-ai-agent-report-card-youve-been-ignoring-why-30-of-y
     agents,” 2025. [Online]. Available: https://arxiv.org/abs/2507.14928                    our-agent-s-successes-are-actually-498fbebf44f9
[55] B. Chen, G. Li, X. Lin, Z. Wang, and J. Li, “Blockagents: Towards                  [77] M. Shukla, “Evaluating agentic ai systems: A balanced framework for
     byzantine-robust llm-based multi-agent coordination via blockchain,”                    performance, robustness, safety and beyond,” Preprints, August 2025.
     in Proceedings of the ACM Turing Award Celebration Conference -                         [Online]. Available: https://doi.org/10.20944/preprints202508.1847.v1
     China 2024, ser. ACM-TURC ’24. New York, NY, USA: Association                      [78] R. Arike, E. Donoway, H. Bartsch, and M. Hobbhahn, “Technical
     for Computing Machinery, 2024, p. 187–192. [Online]. Available:                         report: Evaluating goal drift in language model agents,” 2025.
     https://doi.org/10.1145/3674399.3674445                                                 [Online]. Available: https://arxiv.org/abs/2505.02709
[56] P. Maini et al., “Safety pretraining: Toward the next generation of                [79] M. A. Ferrag, A. Lakas, and M. Debbah, “α3 -bench: A unified
     safe ai,” 2025. [Online]. Available: https://arxiv.org/abs/2504.16980                   benchmark of safety, robustness, and efficiency for llm-based
[57] N. Mu et al., “Can llms follow simple rules?” 2024. [Online].                           uav agents over 6g networks,” 2026. [Online]. Available: https:
     Available: https://arxiv.org/abs/2311.04235                                             //arxiv.org/abs/2601.03281
[58] A. Pan et al., “Do the rewards justify the means? measuring trade-offs             [80] N. Carlini, J. Rando, E. Debenedetti, M. Nasr, and
     between rewards and ethical behavior in the machiavelli benchmark,”                     F. Tramèr, “Autoadvexbench: Benchmarking autonomous exploitation
     2023. [Online]. Available: https://arxiv.org/abs/2304.03279                             of adversarial example defenses,” 2025. [Online]. Available:
[59] M. Mazeika et al., “Utility engineering: Analyzing and controlling                      https://arxiv.org/abs/2503.01811
     emergent value systems in ais,” 2025. [Online]. Available: https:                  [81] L. Rijo. (2026, Feb.) UC berkeley unveils framework as AI agents
     //arxiv.org/abs/2502.08640                                                              threaten to outrun oversight. PPC Land. Accessed: 2026-02-24.
[60] M. Abou Ali, F. Dornaika, and J. Charafeddine, “Agentic AI:                             [Online]. Available: https://ppc.land/uc-berkeley-unveils-framework-a
     a comprehensive survey of architectures, applications, and future                       s-ai-agents-threaten-to-outrun-oversight/
     directions,” Artificial Intelligence Review, vol. 59, no. 1, p. 11, Nov.           [82] N. Yadav. (2025, Nov.) 10 essential steps for evaluating the reliability
     2025. [Online]. Available: https://doi.org/10.1007/s10462-025-11422-4                   of AI agents. Maxim AI. Accessed: 2026-02-24. [Online]. Available:
                                                                                             https://www.getmaxim.ai/articles/10-essential-steps-for-evaluating-the
[61] A. Srivastava et al., “Beyond the imitation game: Quantifying and
                                                                                             -reliability-of-ai-agents/
     extrapolating the capabilities of language models,” 2023. [Online].
     Available: https://arxiv.org/abs/2206.04615                                        [83] D. Mason. (2025, Oct.) ISO/IEC 42001 AI security implementation
                                                                                             guide. BD Emerson. Accessed: 2026-02-24. [Online]. Available:
[62] L. Phan et al., “Humanity’s last exam,” 2025. [Online]. Available:
                                                                                             https://www.bdemerson.com/article/iso-iec-42001-ai-security-imple
     https://arxiv.org/abs/2501.14249
                                                                                             mentation-guide
[63] M. Andriushchenko et al., “Agentharm: A benchmark for measuring
                                                                                        [84] J. Qiu, X. Ma, Y. Xu, Z. Zhang, and H. Zhao, “Chain-of-trigger:
     harmfulness of llm agents,” 2025. [Online]. Available: https:
                                                                                             An agentic backdoor that paradoxically enhances agentic robustness,”
     //arxiv.org/abs/2410.09024
                                                                                             2025. [Online]. Available: https://arxiv.org/abs/2510.08238
[64] K. Huang et al., “A novel zero-trust identity framework for agentic ai:            [85] I. Shahbaz, E. Hammad, and A. Farraj, “An interpretable federated
     Decentralized authentication and fine-grained access control,” 2025.                    learning control framework design for smart grid resilience,” in 2026
     [Online]. Available: https://arxiv.org/abs/2505.19301                                   IEEE/PES Transmission and Distribution Conference and Exposition
[65] A. Gurram, “Generative ai for enhanced cybersecurity: building a zero-                  (T&D), 2026, pp. 1–5.
     trust architecture with agentic ai,” World J. Adv. Eng. Technol. Sci,              [86] I. Shahbaz, I. Lagoy, O. Al-Refai, and E. Hammad, “Evaluating
     vol. 15, no. 1, pp. 2380–2396, 2025.                                                    interpretable kolmogorov–arnold network controllers for smart grid
[66] R. Ren et al., “The mask benchmark: Disentangling honesty                               resilience,” in 2026 IEEE Texas Power and Energy Conference (TPEC),
     from accuracy in ai systems,” 2026. [Online]. Available: https:                         2026, pp. 1–6.
     //arxiv.org/abs/2503.03750                                                         [87] O. Al-Refai, I. Shahbaz, A. A. Husseinat, and E. Hammad,
[67] M. Mazeika et al., “Harmbench: A standardized evaluation framework                      “Federated physics-grounded reinforcement learning for distributed
     for automated red teaming and robust refusal,” 2024. [Online].                          stability control in smart grids,” 2026. [Online]. Available: https:
     Available: https://arxiv.org/abs/2402.04249                                             //arxiv.org/abs/2607.05553
[68] B. Ye et al., “Claw-eval: Toward trustworthy evaluation of autonomous              [88] I. Shahbaz, O. Al-Refai, and E. Hammad, “Inertia-informed federated
     agents,” 2026. [Online]. Available: https://arxiv.org/abs/2604.06132                    learning control framework for distributed smart grid resilience,”
[69] O. Al-Refai, I. Shahbaz, and E. Hammad, “Composable trust in agentic                    2026. [Online]. Available: https://arxiv.org/abs/2607.05720
     ai: Bridging architectural capability and system-level assurance,” in              [89] Q. Zhang and L. Xie, “PowerAgent: A road map toward agentic intel-
     2026 56th Annual IEEE International Conference on Dependable                            ligence in power systems: Foundation model, model context protocol,
     Systems and Networks Workshops (DSN-W), 2026, pp. 17–20.                                and workflow,” IEEE Power and Energy Magazine, vol. 23, no. 5, pp.
[70] RagaAI. (2025) RagaAI AAEF (Agentic Application Evaluation                              93–101, Sep. 2025.
     Framework). RagaAI Catalyst. Accessed: 2026-02-18. [Online].                       [90] L. Xie, Q. Zhang, M. Yu, P. L. Joskow, and C. Singh, “Crucial role of
     Available: https://docs.raga.ai/ragaai-aaef-agentic-application-evaluat                 foundation models in enhancing the interaction of AI and power sys-
     ion-framework                                                                           tems: Achieving integrated frameworks,” IEEE Energy Sustainability
[71] ——, “Whitepaper: Agentic application evaluation framework                               Magazine, pp. 22–28, Feb. 2026.
     (AAEF),” RagaAI, Inc., Tech. Rep., Jun. 2024, accessed: 2025-                      [91] M. Kiasari and H. H. Aly, “Agentic artificial intelligence for smart
     02-18. [Online]. Available: https://raga.ai/resources/patentsandpublicat                grids: A comprehensive review of autonomous, safe, and explainable
     ions/whitepaper-agentic-application-evaluation-framework                                control frameworks,” Energies, vol. 19, no. 3, p. 617, 2026.
[72] A.-G. Starkloff, S. Kokaina, and S. Rahimi. (2026, Jan.) Evaluations               [92] S. Ghosh and G. Mittal, “Agentic AI systems in electrical
     for the agentic world. QuantumBlack, AI by McKinsey. Accessed:                          engineering: Current state-of-the-art and challenges,” arXiv preprint
     2026-02-18. [Online]. Available: https://medium.com/quantumblack/                       arXiv:2511.14478, 2025. [Online]. Available: https://arxiv.org/abs/25
     evaluations-for-the-agentic-world-c3c150f0dd5a                                          11.14478
[73] F. Morales Aguilera. (2025, Jul.) Building real-world agentic AI                   [93] Y. Cheng et al., “A large language model for advanced power dispatch,”
     systems: A practical guide. AI Simplified in Plain English. Accessed:                   Scientific Reports, vol. 15, 2025.
     2026-02-18. [Online]. Available: https://medium.com/ai-simplified-i                [94] N. Slavchev, E. M. Keller, J. M. Snodgrass, and T. J. Overbye, “Testing
     n-plain-english/building-real-world-agentic-ai-systems-a-practical-g                    fine-tuned large language models for power system analysis,” in 2026
     uide-9748d572b58b                                                                       Texas Power and Energy Conference (TPEC). College Station, TX,
[74] Wiz Experts Team. (2025, May) MDR vs. SOC: What’s the                                   USA: IEEE, Feb. 2026.
     difference? Wiz, Inc. Accessed: 2026-02-18. [Online]. Available:                   [95] Y. Wen and X. Chen, “X-GridAgent: An LLM-powered agentic
     https://www.wiz.io/academy/detection-and-response/mdr-vs-soc                            AI system for assisting power grid analysis,” arXiv preprint


   This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
      arXiv:2512.20789, 2025. [Online]. Available: https://arxiv.org/abs/25              [117] A. Samadi, K. Koufos, K. Debattista, and M. Dianati, “Safe-rl:
      12.20789                                                                                 Saliency-aware counterfactual explainer for deep reinforcement learn-
 [96] H. Jin, K. Kim, and J. Kwon, “GridMind: LLMs-powered agents for                          ing policies,” IEEE Robotics and Automation Letters, vol. 9, no. 11,
      power system analysis and operations,” in Proceedings of the SC’25                       pp. 9994–10 001, 2024.
      Workshops of the International Conference for High Performance                     [118] J. Dongarra, T. Herault, and Y. Robert, “Fault tolerance techniques for
      Computing, Networking, Storage and Analysis, 2025, pp. 560–568.                          high-performance computing,” in Fault-tolerance techniques for high-
 [97] E. O. Badmus, P. Sang, D. Stamoulis, and A. Pandey, “PowerChain:                         performance computing. Springer, 2015, pp. 3–85.
      Automating distribution grid analysis with agentic AI workflows,”                  [119] F. Cappello, A. Geist, W. Gropp, L. Kalé, B. Kramer, and M. Snir,
      arXiv preprint arXiv:2508.17094, 2025. [Online]. Available: https:                       “Toward exascale resilience,” The International Journal of High Per-
      //arxiv.org/abs/2508.17094                                                               formance Computing Applications, vol. 23, pp. 374 – 388, 2009.
 [98] Y. Zhang, A. M. Saber, A. Youssef, and D. Kundur, “Semantic                        [120] N. Losada, P. González, M. J. Martı́n, G. Bosilca, A. Bouteiller, and
      reasoning meets numerical precision: An LLM-powered multi-agent                          K. Teranishi, “Fault tolerance of mpi applications in exascale systems:
      system for power grid control,” arXiv preprint arXiv:2508.05702,                         The ulfm solution,” Future Gener. Comput. Syst., vol. 106, pp. 467–
      2025. [Online]. Available: https://arxiv.org/abs/2508.05702                              481, 2020.
 [99] B. K. Saha, Aarthi V., and O. D. Naidu, “DrAgent: An agentic approach              [121] K.-H. Huang and J. A. Abraham, “Algorithm-based fault tolerance for
      to fault analysis in power grids using large language models,” in 2025                   matrix operations,” IEEE Transactions on Computers, vol. C-33, no. 6,
      International Conference on Artificial Intelligence in Information and                   pp. 518–528, 1984.
      Communication (ICAIIC), 2025, pp. 938–945.                                         [122] P. Rajput and G. Sikka, “Multi-agent architecture for fault recovery in
[100] X. Zheng et al., “Agentic planning for power system simulation task                      self-healing systems,” Journal of Ambient Intelligence and Humanized
      orchestrations based on multi-agent systems,” in 2025 8th International                  Computing, vol. 12, pp. 2849 – 2866, 2020.
      Conference on Robotics, Control and Automation Engineering (RCAE),                 [123] J. Park, G. Yoo, and E. Lee, “Proactive self-healing system based
      2025, pp. 576–581.                                                                       on multi-agent technologies,” in Third ACIS Int’l Conference on Soft-
[101] M. Jia, Z. Cui, and G. Hug, “Enhancing LLMs for power system simu-                       ware Engineering Research, Management and Applications (SERA’05),
      lations: A feedback-driven multi-agent framework,” IEEE Transactions                     2005, pp. 256–263.
      on Smart Grid, vol. 16, no. 6, pp. 5556–5572, 2025.                                [124] I. Sidorov, “Methods and tools to increase fault tolerance of high-
[102] R. El Makroum, S. Zwickl-Bernhard, and L. Kranzl, “Agentic AI home                       performance computing systems,” in 2016 39th International Conven-
      energy management system: A large language model framework for                           tion on Information and Communication Technology, Electronics and
      residential load scheduling,” Results in Engineering, vol. 29, p. 109857,                Microelectronics (MIPRO), 2016, pp. 226–230.
      2026.                                                                              [125] P. Tejas Vinay and S. K. Saurav, “Comas-hpc: A collaborative multi-
[103] A. D. Ames, S. Coogan, M. Egerstedt, G. Notomista, K. Sreenath,                          agent system for hpc administration,” in 2025 Supercomputing India
      and P. Tabuada, “Control barrier functions: Theory and applications,”                    (SCI), 2025, pp. 1–8.
      in 2019 18th European control conference (ECC). Ieee, 2019, pp.                    [126] E. Y. Chang and L. Geng, “Sagallm: Context management, validation,
      3420–3431.                                                                               and transaction guarantees for multi-agent llm planning,” Proc. VLDB
[104] U. Mehmood, S. Sheikhi, S. Bak, S. A. Smolka, and S. D. Stoller, “The                    Endow., vol. 18, no. 12, p. 4874–4886, Aug. 2025. [Online]. Available:
      black-box simplex architecture for runtime assurance of autonomous                       https://doi.org/10.14778/3750601.3750611
      cps,” in NASA formal methods symposium. Springer, 2022, pp. 231–                   [127] M. H. Rahman, A. Shamji, S. Guo, and G. Li, “Peppa-x: Finding
      250.                                                                                     program test inputs to bound silent data corruption vulnerability in hpc
                                                                                               applications,” in SC21: International Conference for High Performance
[105] S. Chen, Y. Sun, D. Li, Q. Wang, Q. Hao, and J. Sifakis, “Runtime
                                                                                               Computing, Networking, Storage and Analysis, 2021, pp. 1–14.
      safety assurance for learning-enabled control of autonomous driving
                                                                                         [128] A. Gholami, Z. Yao, S. Kim, C. Hooper, M. W. Mahoney, and
      vehicles,” in 2022 International Conference on Robotics and Automa-
                                                                                               K. Keutzer, “Ai and memory wall,” IEEE Micro, vol. 44, no. 3, pp.
      tion (ICRA). IEEE, 2022, pp. 8978–8984.
                                                                                               33–39, 2024.
[106] U. R. No, “155 [uniform provisions concerning the approval of vehicles
                                                                                         [129] M. A. Enright, E. Hammad, and A. Dutta, “A learning-based zero-
      with regards to cyber security and cyber security management system],”
                                                                                               trust architecture for 6g and future networks,” in 2022 IEEE Future
      UNECE, UN Regulation No, 2021.
                                                                                               Networks World Forum (FNWF). IEEE, 2022, pp. 64–71.
[107] F. Siddiqui et al., “Cybersecurity engineering: bridging the security              [130] A. S. Jacobs et al., “Hey, lumi! using natural language for intent-
      gaps in advanced automotive systems and iso/sae 21434,” in 2023 IEEE                     based network management,” in 2021 USENIX Annual Technical
      97th Vehicular Technology Conference (VTC2023-Spring).              IEEE,                Conference (USENIX ATC 21), 2021, pp. 625–639. [Online]. Available:
      2023, pp. 1–6.                                                                           https://www.usenix.org/conference/atc21/presentation/jacobs
[108] C. Ma, N. Wang, Z. Zhao, Q. Wang, Q. A. Chen, and C. Shen,                         [131] D. M. Manias, A. Chouman, and A. Shami, “Towards intent-based
      “Controlloc: Physical-world hijacking attack on visual perception in                     network management: Large language models for intent extraction
      autonomous driving,” arXiv preprint arXiv:2406.05810, 2024.                              in 5g core networks,” in 2024 20th International Conference on the
[109] Y. Lou et al., “A first {Physical-World} trajectory prediction attack via                Design of Reliable Communication Networks (DRCN), 2024. [Online].
      {LiDAR-induced} deceptions in autonomous driving,” in 33rd USENIX                        Available: https://arxiv.org/abs/2403.02238
      Security Symposium (USENIX Security 24), 2024, pp. 6291–6308.                      [132] ——, “Semantic routing for enhanced performance of llm-assisted
[110] C. Ma, N. Wang, Z. Zhao, Q. A. Chen, and C. Shen, “Slowperception:                       intent-based 5g core network management and orchestration,” in
      Physical-world latency attack against visual perception in autonomous                    2024 IEEE Global Communications Conference (GLOBECOM), 2024.
      driving,” arXiv preprint arXiv:2406.05800, 2024.                                         [Online]. Available: https://arxiv.org/abs/2404.15869
[111] A. Eldosouky, A. Ferdowsi, and W. Saad, “Drones in distress: A game-               [133] H. Xie, Z. Qin, G. Y. Li, and B.-H. Juang, “Deep learning
      theoretic countermeasure for protecting uavs against gps spoofing,”                      enabled semantic communication systems,” IEEE Transactions on
      IEEE Internet of Things Journal, vol. 7, no. 4, pp. 2840–2854, 2019.                     Signal Processing, vol. 69, pp. 2663–2675, 2021. [Online]. Available:
[112] B. Davidovich, B. Nassi, and Y. Elovici, “Towards the detection of gps                   https://arxiv.org/abs/2006.10685
      spoofing attacks against drones by analyzing camera’s video stream,”               [134] Z. Weng and Z. Qin, “Semantic communication systems for speech
      Sensors, vol. 22, no. 7, p. 2608, 2022.                                                  transmission,” IEEE Journal on Selected Areas in Communications,
[113] M. Hasan, S. Mohan, T. Shimizu, and H. Lu, “Securing vehicle-to-                         vol. 39, no. 8, pp. 2434–2444, 2021. [Online]. Available: https:
      everything (v2x) communication platforms,” IEEE Transactions on                          //arxiv.org/pdf/2102.12605
      Intelligent Vehicles, vol. 5, no. 4, pp. 693–713, 2020.                            [135] Q. Qin et al., “Securing semantic communications with physical-layer
[114] C. Ling, K. Hu, H. Liu, X. Han, T. Zhang, and C. Ou, “Physical prompt                    semantic encryption and obfuscation,” in 2023 IEEE International
      injection attacks on large vision-language models,” arXiv preprint                       Conference on Communications (ICC), 2023. [Online]. Available:
      arXiv:2601.17383, 2026.                                                                  https://arxiv.org/pdf/2304.10147
[115] T. Zhang et al., “Visual adversarial attack on vision-language models              [136] Y. Ruan et al., “Identifying the risks of lm agents with an
      for autonomous driving,” arXiv preprint arXiv:2411.18275, 2024.                          lm-emulated sandbox,” in The Twelfth International Conference on
[116] A. Samadi, A. Shirian, K. Koufos, K. Debattista, and M. Dianati, “Safe:                  Learning Representations (ICLR 2024), 2024. [Online]. Available:
      Saliency-aware counterfactual explanations for dnn-based automated                       https://openreview.net/forum?id=GEcwtMk1uA
      driving systems,” in 2023 IEEE 26th International Conference on                    [137] H. Zhang et al., “Agent security bench (asb): Formalizing and
      Intelligent Transportation Systems (ITSC). IEEE, 2023, pp. 5655–                         benchmarking attacks and defenses in llm-based agents,” in The
      5662.                                                                                    Thirteenth International Conference on Learning Representations


     This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
      (ICLR 2025), 2025. [Online]. Available: https://openreview.net/forum                                           Michael Mandulak received his Ph.D. in Com-
      ?id=V4y0CpX4hK                                                                                                 puter Science from Rensselaer Polytechnic Institute
[138] J. Kim, D. Kim, C. Cutler, Z. Lin, D. Xu, and X. Zhang, “Intender:                                             (RPI), Troy, NY, USA. in 2025. He is currently a
      Fuzzing intent-based networking with intent-state transition guidance,”                                        Postdoctoral Research Associate at the Texas A&M
      in 32nd USENIX Security Symposium (USENIX Security 23), 2023,                                                  University Institute of Data Science (TAMIDS) in
      pp. 8861–8878. [Online]. Available: https://www.usenix.org/conferenc                                           the Security, Privacy and Resilience for Trusted AI
      e/usenixsecurity23/presentation/kim-jiwon                                                                      (SPARTA) Laboratory. His research interests include
[139] T. Haikal, S. Ismail, and E. Hammad, “Bridging high-level intent and                                           high-performance computing, large-scale graph ana-
      network execution: Detecting violations and intent drift through low-                                          lytics, distributed graph processing, matching algo-
      level traffic analysis,” in 2026 IEEE World AI IoT Congress (AIIoT).                                           rithms, and security in graph-based AI systems.
      IEEE, 2026, pp. 0479–0485.
[140] D. Hespe, L. Hübner, P. Sanders, and A. Stamatakis, “Restore:
      In-memory replicated storage for rapid recovery in fault-tolerant
      algorithms,” in Euro-Par 2022: Parallel Processing, J. Cano and
      J. L. Träff, Eds. Cham: Springer International Publishing, 2022, pp.
      203–217. [Online]. Available: https://doi.org/10.1007/978-3-031-125
      97-3 13




                                                                                                                  Jaewon Kim (Member, IEEE) received his Ph.D.
                         Omar Al-Refai (Student Member, IEEE) received                                            degree in Computer Engineering from Texas A&M
                         the B.Sc. degree in computer engineering from                                            University in 2023. He is currently an Assistant
                         Princess Sumaya University for Technology, Am-                                           Research Scientist at the Texas A&M Global Cyber
                         man, Jordan. He is currently pursuing the Ph.D.                                          Research Institute (GCRI). Prior to joining GCRI, he
                         degree in computer engineering at Texas A&M                                              was a Postdoctoral Associate in the Laboratory for
                         University, College Station, TX, USA. His research                                       Information & Decision Systems (LIDS) at the Mas-
                         at the Innovations in Systems Trust and Resilience                                       sachusetts Institute of Technology (MIT). He spear-
                         (iSTAR) Laboratory focuses on enhancing trust and                                        heads an interdisciplinary research program at the
                         resilience in autonomous, collaborative, and human-                                      critical intersection of cyber-physical systems (CPS)
                         in-the-loop systems and on connecting digital realms                                     and security of future autonomous infrastructures.
                         through the integration of humans, machines, and                His work investigates resilient real-time network and zero-trust architectures
agents. His broader research interests include artificial intelligence, machine          (ZTA), incorporating robust authentication and micro-segmentation, to secure
learning, and security.                                                                  unmanned aerial and ground vehicles (UAVs/UGVs).




                           Ibrahim Shahbaz (Student Member, IEEE) re-
                           ceived the B.Sc. degree in electrical engineering
                           from the University of Jordan, Amman, Jordan, and
                           the M.Sc. degree in Data Science from Princess
                           Sumaya University for Technology, Amman, Jordan.
                           He is currently a Ph.D. student in electrical engi-                                   Eman Hammad (Senior Member, IEEE) is an As-
                           neering at Texas A&M University, College Station,                                     sistant Professor and the Director of the Innovations
                           TX, USA. His research interests at the iSTAR Lab                                      in Systems Trust and Resilience (iSTAR) Laboratory
                           include intelligent cyber-physical systems, resilient                                 at Texas A&M University, College Station, TX,
                           smart grids, and scientific machine learning.                                         USA. She is also the Director of the Texas A&M
                                                                                                                 Data Institute Thematic Laboratory for Security, Pri-
                                                                                                                 vacy, and Resilience for Trusted AI (SPARTA). She
                                                                                                                 received the Ph.D. degree from the Department of
                                                                                                                 Electrical and Computer Engineering at the Univer-
                                                                                                                 sity of Toronto, Toronto, ON, Canada. Her research
                                                                                                                 is primarily in the domain of security and resilience
                                                                                         of complex network, cyber-physical systems and critical infrastructures’ with
                                                                                         applications in power systems, 6G/NG wireless networks, connected and
                           Adam Ali Husseinat (Member, IEEE) received the                autonomous vehicles (UAV/UGV), and public safety. Focus areas include
                           B.Sc. degree in electrical engineering from Jordan            trustworthy autonomous systems, physical AI, human-AI interactions, risk-
                           University of Science and Technology, Jordan, in              informed operations, 6G/NG communication networks, semantic and graph-
                           2009, and the M.Sc. degree in systems and computer            based methods, digital well-being, and CyberAI education.
                           engineering from Carleton University, Canada, in
                           2025. He is currently pursuing the Ph.D. degree in
                           electrical and computer engineering at Texas A&M
                           University, College Station, TX, USA. His research
                           interests include wireless communications, machine
                           learning for communications, semantic communica-
                           tion, and 5G/6G intelligent networks.




     This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
