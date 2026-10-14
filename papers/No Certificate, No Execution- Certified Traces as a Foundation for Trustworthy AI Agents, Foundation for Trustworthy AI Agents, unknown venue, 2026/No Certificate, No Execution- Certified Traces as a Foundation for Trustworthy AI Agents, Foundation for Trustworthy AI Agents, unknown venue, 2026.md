                                             No Certificate, No Execution: Certified Traces as a
                                                  Foundation for Trustworthy AI Agents


                                                             Xiao-Yang Liu Yanglet1 , Xiaodong Wang1 , Agostino Capponi2
                                                              1
                                                                SecureFinAI Lab, Electrical Engineering, Columbia University
                                                          2
                                                            Industrial Engineering and Operations Research, Columbia University
                                                                   Emails: {XL2427, XW2008, AC3827}@columbia.edu
arXiv:2605.24462v1 [cs.CE] 23 May 2026




                                                                                          Abstract

                                                     We argue that trustworthy AI agents, especially in high-stakes and policy-governed
                                                     domains, should make execution conditional on certified traces rather than rely
                                                     only on stronger generative models, output-level guardrails, or post-hoc audits.
                                                     A generative agent may propose useful recommendations, tool calls, reports,
                                                     or candidate actions, but generation is not permission: an action may be com-
                                                     putable yet impermissible, and individually permissible actions may compose into
                                                     an impermissible trace. We formalize trustworthy agency through a Proposal–
                                                     Certification–Execution (PCE) architecture: a probabilistic generating machine
                                                     MG proposes candidate execution traces, a Permissibility Machine MΠ certifies
                                                     whether a proposed trace is permitted under a given policy system Π, and execu-
                                                     tion proceeds only for certified traces. The resulting executable trace language is
                                                     Lexec = LG ∩ Lcert (MΠ ). Here a trace is not merely a retrospective log: before
                                                     execution, it is a structured pre-execution record submitted for certification, specify-
                                                     ing the intended steps, supporting evidence, proposed tool calls, required approvals,
                                                     replayable computations, credentials, and execution conditions. This perspective
                                                     complements chain-of-thought monitorability: visible reasoning may help detect
                                                     misbehavior, but monitorability is not certifiability, and a reasoning trajectory is
                                                     only one component of a broader execution trace. The resulting formal principle is
                                                     simple: an agent-generated trace should be authorized for execution only when it
                                                     carries a checkable certificate witnessing permissibility under Π: no certificate, no
                                                     execution. We develop certified traces and Permissibility Machines as foundations
                                                     for trustworthy AI agents, connect trace certification to proof-carrying execution,
                                                     proof memory, privacy, and zero-knowledge certificates, and propose a research
                                                     agenda for evaluating agents by what generated traces can be safely certified for
                                                     execution, not by output accuracy alone.


                                         1    Introduction

                                         Large language model-powered systems are moving beyond chatbots toward autonomous agents that
                                         participate in real-world operational workflows. Nowadays, individuals and institutions are actively
                                         exploring agents that retrieve documents, call APIs, write code, update memory, compute quantities,
                                         interact with external environments, and submit actions for execution [1, 2, 3]. Such exploratory
                                         agents raise a severe AI safety problem: a bad recommendation is an informational failure, but a
                                         bad execution can expose data, move money, alter records, or create institutional liability. Therefore,
                                         the central question is no longer whether an output looks acceptable, but whether the proposed trace
                                         is authorized to execute. Capability is not authority. In high-stakes and policy-governed domains,
                                         agent behaviors must satisfy preset rules for access, privacy, evidence, computation, auditability,
                                         authorization, and execution.

                                         Preprint.
Recent industry deployments make this trend concrete. OpenAI and PwC are building finance agents
for CFO workflows spanning planning, forecasting, reporting, procurement, payments, treasury,
tax, and close, with explicit emphasis on governance, controls, and human oversight [4]. American
Express’s Agentic Commerce Experiences initiative introduces agentic payment credentials for
verified AI agents, while Anthropic’s financial-services agents connect to market data, research
platforms, and internal financial systems under governed access controls [5, 6]. ICBC similarly
reports large-model and agentic systems for settlement finance, credit risk, and bank-wide AI
infrastructure [7]. These deployments show that the question is moving from whether agents can
assist finance teams to whether agent-initiated actions can be authorized, constrained, and audited.

Central principle. Trustworthy AI agents should not rely only on stronger generative models,
output-level guardrails, or post-hoc audits. In high-stakes, policy-governed domains, execution should
be authorized only for traces that carry checkable certificates under an explicit policy system. In
short: no certificate, no execution.
The progression studied in this paper is
computable action → permissible action → permissible trace → certified trace → executable trace.
In this progression, “permissible trace” refers to a trace that satisfies the policy system, while “certified
trace” refers to a proposed trace whose permissibility has been witnessed by a checkable certificate.
Execution turns a certified proposed trace into a realized trace that can later be audited. A model may
generate a candidate action, yet the action may be impermissible. Even if each individual action is
permissible, the resulting sequence may form an impermissible trace. E.g., each database query may
be individually authorized, while repeated queries to a protected resource may violate a query-budget
or privacy policy. Each trade may pass a local order check, while the sequence violates a cumulative
exposure constraint. A final answer may be factually correct, while the derivation trace relies on
unauthorized retrieval, fabricated evidence, inconsistent units, or unreplayable computation. These
examples point to the same conclusion: the primary unit of execution trust should not be the final
output, but the trace by which the output, recommendation, or action was produced.
Recent work on chain-of-thought monitorability [8, 9] highlights a related opportunity: if models
expose human-readable reasoning, monitors may inspect those reasoning trajectories for signs of
misbehavior. This is an important but partial step. A chain of thoughts is one possible observation
channel inside a broader execution trace. High-stakes agents also produce retrievals, tool calls,
database queries, memory writes, data flows, logs, computations, and execution calls. Therefore, the
safety object for agents is not merely the chain of thoughts; it is the chain of executions.
We propose certified traces as the central unit of execution trust for AI agents. A trace is not only
a retrospective log of completed actions. Before execution, it is a candidate execution record: a
structured sequence of intended states, actions, tool calls, retrievals, computations, evidence, memory
updates, approvals, credentials, and execution conditions. After execution, the realized trace becomes
the audit record. A policy system Π defines which traces are permissible. A Permissibility Machine
is a certifying role: it checks whether a proposed trace carries a certificate witnessing permissibility
under Π. The resulting architecture separates three roles: a generating machine proposes candidate
traces, a Permissibility Machine certifies or rejects them, and an executor acts only on certified traces.
In enterprise settings, this reframes accountability around three operational questions: who autho-
rized this step, what evidence supported the authorization, and can the action be reconstructed
after failure? A certified trace is intended to make these questions technically checkable rather than
left implicit in a generic system log. This is where technical certification meets institutional ac-
countability: liability cannot be assigned meaningfully if authorization evidence, policy context,
and execution lineage are not recoverable.
Although finance provides our main running examples, the trace-certification problem is broader.
Scientific and healthcare agents make the same issue visible: tool-using systems in chemistry,
biomedical discovery, and healthcare may retrieve sensitive data, call expert tools, and trigger
high-stakes downstream actions [10, 11].
We do not claim to solve all problems in verification, governance, or AI safety. Rather, we propose a
minimal formal interface for thinking about agent execution. The key objects are: a policy-induced
permissible trace region, a certified trace region, an execution-authorization rule, and a certification
boundary separating generated traces that may execute from those that must be rejected or escalated.


                                                     2
Finance is used as a running domain because its policies, audit requirements, privacy constraints,
evidence obligations, and execution risks make the trace-certification problem especially visible.
However, the framework is intended more broadly for high-stakes, policy-governed AI agents:
systems that retrieve sensitive information, call external tools, modify records, make regulated
recommendations, or trigger real-world actions.
The paper makes four major contributions: it formulates the separation between generation and
permission at the trace level; introduces a Proposal–Certification–Execution (PCE) architecture;
defines certification-boundary measures for generated impermissibility, unsafe certification, missed
certification, and executable yield; and outlines a research agenda around proof memory, policy
models, privacy-preserving certification, and certified-agent evaluation.

Why now? This question has become urgent because AI systems are shifting from answer genera-
tion to delegated execution. Modern agents increasingly combine language models with retrieval,
memory, tool use, code execution, database access, and external APIs. In such systems, safety failures
may occur before the final output is produced, and they may concern source authorization, data
flow, computation replay, cumulative risk, or policy history. This shift makes output inspection
insufficient as the primary governance object. The relevant object is the proposed execution trace and
the evidence required to authorize it.
Take-home message. Monitorability asks whether available observations are sufficient to detect or
suspect safety-relevant behavior. Certifiability asks whether the trace contains enough checkable
evidence to establish that policy obligations are satisfied. Execution authorization asks whether
certification has succeeded, so that the executor is allowed to act. To summarize,

               monitorable trace ̸≡ certifiable trace ̸≡ execution-authorized trace .

Organization. Section 2 explains why output guardrails and local action checks are insufficient.
Section 3 provides minimal axioms for certifiable execution and the basic execution safety theorem.
Sections 4–5 introduce the proposal–certification–execution architecture and the executable trace
language. Sections 6–7 discuss policy models, proof memory, and certification boundary measures.
Section 8 studies privacy and zero-knowledge trace certification. Section 9 concludes with objections,
limitations, and open problems.

2   Why Output Guardrails Fall Short
The purpose of this section is to motivate trace certification by showing that, for agentic systems, the
safety-relevant predicate is often a property of the execution trace rather than a property of the final
output alone.
Output-level guardrails inspect final answers, block prohibited text, or apply local checks to individual
tool calls. These mechanisms are useful, but they are structurally limited for agentic systems. Recent
agent benchmarks and attacks show that tool-using agents fail not only through final text, but also
through retrieval, tool outputs, environment observations, memory, and multi-step actions [12, 3, 13,
14]. Recent security surveys make the same point at the systems level: agentic risks arise across
memory, tool execution, multi-agent coordination, ecosystem, and governance layers, and many
threats are temporally extended rather than single-step failures [15]. Thus the safety-relevant violation
may occur inside the trace even when the final output appears safe.
We give three illustrative examples:

• Privacy and access control are naturally trace-dependent. A single query to a protected
  database may be authorized, while repeated queries to password-related or identity-related records
  within a time window may violate a query-budget policy. Similarly, a final answer may contain no
  personally identifiable information, while the trace that produced it may have exposed sensitive
  data through prompts, retrieval, logs, memory, or tool calls.
• Payment authorization is not output classification. A payment instruction may be well-formed
  and may even match a local rule, while the full trace lacks valid authorization evidence: the
  beneficiary account may have changed, the approval may be stale, the amount may exceed a
  contextual limit, or the credential may not be scoped to this transaction. The relevant question


                                                   3
 Challenge                    Why output checking is insufficient           Permissibility-machine            re-
                                                                            sponse
 Output-centric guardrails    The final answer may look safe while the      Certify the full trace τ , not merely
                              trace contains unsafe retrieval, tool use,    the output.
                              memory access, or execution.
 Correct answer, wrong        A claim may be true but supported by          Require evidence binding and
 derivation                   fabricated citations, inconsistent periods,   computation replay.
                              or unreplayable computations.
 Source access control        A generated answer may rely on sources        Certify retrieval permissions and
                              the agent was not authorized to access.       source lineage.
 Auditability                 A later reviewer must know what was           Maintain persistent proof mem-
                              done and under which policy version.          ory: trace lineage plus policy lin-
                                                                            eage.
 Privacy-preserving compli-   The final output may omit private infor-      Use trace-level privacy certifica-
 ance                         mation while the trace leaks it through       tion and, when needed, zero-
                              prompts, tools, logs, or memory.              knowledge proofs.
                Table 1: Trace-level challenges motivating permissibility certification.


  is not whether the payment text looks valid, but whether the execution trace carries checkable
  authorization evidence.
• A generated financial claim may be correct as a sentence but impermissible as a derivation. An
  agent may correctly state that a firm’s gross margin improved while relying on fabricated citations,
  inconsistent reporting periods, wrong XBRL/iXBRL tags, incompatible units, or arithmetic that
  cannot be replayed. This issue is especially visible in XBRL-based financial report analysis, where
  LLM agents must retrieve filing facts, interpret XBRL concepts, align periods and units, and
  perform reliable calculations [16]. The issue is not only whether the final claim is true, but whether
  it was produced by a permissible and auditable derivation trace.
Table 1 summarizes the trace-level challenges illustrated by these examples. These examples illustrate
why output-level safety and local action safety do not imply trace-level permissibility:
            acceptable final output ̸⇒ τ ∈ LΠ ,       locally permitted actions ̸⇒ τ ∈ LΠ .
The failure is not that guardrails and monitors are useless; the failure is that they do not by themselves
define an execution-authorization rule. Output guardrails ask whether the final output appears
acceptable. Local action checks ask whether each step is individually allowed. Monitoring asks
whether available observations raise concern. Trace certification asks a stronger question: whether
the proposed execution trace contains enough checkable evidence to satisfy the policy system before
execution.
This gives a hierarchy of increasingly strong execution controls:
output checking → local action checks → monitoring → trace certification → certified execution.
Each step adds information, but only the last two provide an authorization condition for execution.
Our point is not to discard monitoring, but to place it inside a stronger execution-governance pipeline.
The formal obstruction is trace non-compositionality: policies may be satisfied locally at each step
while being violated by the sequence.
Proposition 1 (Trace Non-Compositionality). There exist policy systems and traces whose individual
actions are locally permissible, while the full trace is impermissible under the policy system.

Interpretation. This existence claim does not say that every policy is trace-dependent. It says that
important policy classes are: query budgets, temporal obligations, purpose limitations, cumulative
exposure limits, approval-before-execution rules, and computation-replay requirements cannot be
certified from the final output alone. They require trace-level evidence.

Proof sketch. Construct a query-budget policy. Each individual query to a protected resource may
be locally authorized and therefore pass the action-level check. The policy, however, may permit at
most five queries to that resource within a time window. A trace containing six individually authorized
queries violates the trace-level budget, although every action is permissible. A full proof is given in
Appx. B.


                                                      4
3     Minimal Axioms of Certifiable Execution
We state the minimal assumptions under which trace certification implies execution safety. Let Σ∗
denote the universe of encoded finite trace records and τ ∈ Σ∗ denote a proposed trace submitted for
certification. This trace may include intended states, actions, tool calls, retrieval events, evidence,
approvals, credentials, computations, memory updates, and execution conditions. After execution,
the realized trace records the events actually performed and should conform to the certified proposed
trace.

• Axiom 1: Policy boundary. A policy system Π induces a semantic permissible trace region
                                                 LΠ ⊆ Σ∗ .
    A trace τ is permissible under Π when τ ∈ LΠ . This axiom defines the boundary between
    permissible and impermissible traces.
• Axiom 2: Sound certification. A Permissibility Machine may be incomplete, conservative, or
  unable to certify many permissible traces, but certification must be sound: Lcert (MΠ ) ⊆ LΠ . Thus
  every certified trace is semantically permissible. This axiom distinguishes a certificate from a
  confidence score, self-approval, or post-hoc explanation.
• Axiom 3: Execution authorization. Execution is allowed only after certification succeeds:
  Execute(τ ) =⇒ τ ∈ Lcert (MΠ ). This axiom makes certification operational rather than
  advisory: the executor cannot act on an uncertified trace.
• Axiom 4: Execution conformance. Let τ prop denote the certified proposed trace and τ real denote
  the realized trace after execution. Execution conformance requires that either
                                        Conform(τ real , τ prop ) = 1,
    or the executor halts, rolls back, or escalates before irreversible action. Moreover, conformance
    must preserve permissibility:
                    τ prop ∈ LΠ ∧ Conform(τ real , τ prop ) = 1      =⇒      τ real ∈ LΠ .
    This axiom separates authorization of a proposed trace from audit of the realized trace. Certification
    authorizes what the agent is permitted to do, while conformance checks whether the agent actually
    did it.
Theorem 1 (Execution Authorization Safety). Under sound certification and execution authorization,
every certified pre-execution trace submitted to the executor is semantically permissible:
                                       Execute(τ ) =⇒ τ ∈ LΠ .

Proof. By execution authorization in Axiom 3, Execute(τ ) =⇒ τ ∈ Lcert (MΠ ). By sound
certification in Axiom 2, Lcert (MΠ ) ⊆ LΠ . Therefore τ ∈ LΠ .

Interpretation. The separation principle, generation is not permission, explains why certification
is needed. The three axioms explain why certification makes execution safe. Policy defines the
permissible region; certification verifies that a trace lies inside it; execution authorization ensures
that only certified traces are acted upon. Proof memory, privacy-preserving certification, policy drift,
and escalation are not required to state this basic theorem, but they become essential when the policy
boundary is trace-dependent, dynamic, or only partially observable.
Theorem 2 (Certified Execution with Conformance). Under sound certification, execution authoriza-
tion, and execution conformance, every realized executed trace is permissible:
                               Execute(τ prop ) = τ real =⇒ τ real ∈ LΠ .

Proof. Suppose Execute(τ prop ) = τ real . By execution authorization, execution of τ prop implies
                                          τ prop ∈ Lcert (MΠ ).
By sound certification,
                                           Lcert (MΠ ) ⊆ LΠ ,


                                                     5
so τ prop ∈ LΠ . By execution conformance, if execution proceeds rather than halting, rolling back, or
escalating, then
                                       Conform(τ real , τ prop ) = 1.
Using the conformance-preservation condition,

                     τ prop ∈ LΠ ∧ Conform(τ real , τ prop ) = 1 =⇒ τ real ∈ LΠ .

Therefore every realized executed trace is permissible.


Interpretation. The basic authorization-safety theorem proves that a trace certified before execution
is permissible. The conformance theorem adds the execution layer: the realized trace must conform
to the certified pre-execution trace, or the system must halt, roll back, or escalate before completion.
Thus “no certificate, no execution” should be paired with “no conformance, no completion.”


4     Proposal–Certification–Execution Architecture

We now define the three roles underlying certifiable execution: generation, certification, and execution
authorization. The purpose of this architecture is to prevent capability from being confused with
permission. A system may be able to propose a trace, but execution should occur only after the trace
has been certified under the given policy system Π.

• Generator. A generating machine proposes a candidate trace: MG : x 7→ τ, where x is an input,
  prompt, task, or context, and τ is a finite proposed execution trace. At this stage, τ is not yet a
  retrospective log; it is the structured record of what the agent intends to do and what evidence or
  authorization context supports that execution. The role of MG is generative: it determines which
  traces can be produced.
• Permissibility Machine. A Permissibility Machine evaluates a proposed trace under a policy
  system Π and returns a certificate, a rejection, or an escalation:

                                   MΠ : (τ, Π) 7→ {π, ⊥, Escalate},

    where π denotes a checkable certificate, ⊥ denotes rejection, and Escalate denotes transfer to a
    stronger certifier, a human reviewer, or an external review process. High-risk execution need not
    always require manual approval, but it must require checkable authorization evidence. Human
    approval may be one component of a certificate, but certification is not defined as human approval:
    the essential requirement is checkable authorization evidence. The role of MΠ is certifying: it
    determines whether the proposed trace has enough evidence to be authorized for execution.
• Executor. An executor acts only on certified traces: E : τ 7→ o, where o is the executed outcome.
  The role of E is operational: it realizes the consequences of a trace only after certification succeeds.

Principle: separation of proposal and certification. In high-stakes settings, the generator should
not certify its own execution trace using only its own generated explanation. The generator may
supply evidence, proposed justifications, tool logs, or candidate proof objects, but certification must
be performed by a logically or institutionally separate mechanism: for example, a policy engine,
verifier, human reviewer, external auditor, cryptographic proof system, or supervisory control. This
separation is essential because a fluent self-explanation is not a certificate. The agent may propose; it
may not grant itself authority.

Three operational questions.       The architecture separates three questions:

           Generator MG :     x 7→ τ                      Can this trace be produced?
           Certifier MΠ :     τ 7→ {π, ⊥, Escalate}       Can this trace be certified under Π?
           Executor E :       τ 7→ o                      Has execution been authorized?



                                                     6
Figure 1: The Proposal–Certification–Execution (PCE) architecture. A generating machine MG
proposes candidate traces, a Permissibility Machine MΠ certifies, rejects, or escalates traces under a
policy system Π, and execution is authorized only on the certificate path. The architecture enforces
the invariant: no certificate, no execution.

A concrete instantiation. A Permissibility Machine need not be a single model or a single verifier.
In a financial-agent deployment, it may be implemented as a certifying service that takes as input a
proposed trace τ , a policy system Π, proof memory H, and external policy data DΠ , and returns
                                MΠ (τ, Π, H, DΠ ) ∈ {π, ⊥, Escalate}.
The proposed trace may include a task, retrieved sources, proposed tool calls, computed quantities,
approvals, credentials, risk checks, and intended execution conditions. The policy system may include
access-control rules, client mandates, restricted lists, query budgets, exposure limits, approval-before-
execution rules, and computation-replay requirements. Proof memory stores the history needed for
certification, such as prior queries, current exposure, retrieved filings, policy versions, approvals, and
previous certificates.
For example, consider an agent that proposes to generate a client-facing financial claim or initiate a
payment instruction. The Permissibility Machine checks whether the source was authorized, whether
the data access matches the declared purpose, whether required approvals are fresh and bound to the
proposed trace, whether risk or payment limits are satisfied, whether the computation is replayable,
and whether the credential is scoped to the intended action. If all required obligations are witnessed,
the machine emits a certificate
                      π = (πaccess , πsource , πapproval , πrisk , πcompute , πlineage ).
If an obligation fails, it returns ⊥; if evidence is incomplete or the action exceeds the certifier’s
authority, it returns Escalate. Thus the Permissibility Machine is not an output classifier. It is an
authorization boundary: it decides whether the proposed trace carries enough checkable evidence to
be executed under Π.
This separation also clarifies the relation to monitoring and runtime enforcement. Runtime verification
monitors executions against specifications, while recent agent guardrails dynamically check whether
agent behavior satisfies safety requests [17, 18]. A Permissibility Machine plays a stronger role:
it produces or verifies a certificate required for execution authorization. Monitoring may provide
evidence for certification, but monitoring alone does not authorize execution.
Architecture. A generating machine proposes a candidate trace; a Permissibility Machine certifies,
rejects, or escalates the trace under the policy system; the executor acts only when certification
succeeds. The operational chain is
                          Propose −→ Certify −→ Authorize Execution .

Fig. 1 illustrates the PCE architecture. The generating machine MG receives an input x and proposes
a candidate trace τ . The trace is then evaluated by the Permissibility Machine MΠ under the policy


                                                      7
system Π. The certifier has three possible outcomes: it may return a certificate π, reject the trace with
⊥, or escalate the case to a human reviewer, stronger certifier, or external review process. Execution
is authorized only on the certificate path: the executor E acts on τ only when MΠ (τ, Π) = π. Thus
the figure encodes the central invariant of the architecture: there is no direct execution path from
generation to execution. Thus, no certificate, no execution!
Design invariant. There is no direct execution path from MG to E. Execution is authorized only
when MΠ (τ, Π) = π. This invariant is an architectural expression of no certificate, no execution!

Interpretation. The architecture does not assume that the generator is safe by construction, nor
that the certifier is complete. Its purpose is to separate proposal from authorization. The generator
explores candidate behavior; the Permissibility Machine governs admissibility under policy; the
executor acts only on traces whose certification has succeeded.

Risk-tiered certification. The principle “no certificate, no execution” does not require the same
certificate burden for every agent action. Certification should be risk-tiered. Low-risk informational
traces may require only logging or lightweight provenance, while high-risk traces involving sensitive
data, regulated advice, external execution, asset transfer, or irreversible operations require stronger
certificates. A useful tiering is:
       C0 :   no external effect; logging only;
       C1 :   low-risk informational response; lightweight provenance;
       C2 :   client-facing or research claim; evidence and source certificate;
       C3 :   sensitive data or tool access; access, purpose, and privacy certificate;
       C4 :   regulated or irreversible action; authorization, policy, risk, and audit certificate;
       C5 :   systemic or high-liability action; external, human, or regulator-grade review.
Thus certification is not a binary choice between no verification and full formal proof. The design
question is whether the certificate stack is proportionate to the execution risk of the trace.

5   Executable Trace Languages
The PCE architecture turns execution authorization into a language-theoretic object. Let Σ∗ denote
the universe of encoded finite trace records. The generator induces a generated language LG ⊆ Σ∗ ,
consisting of the traces it can propose. For a policy system Π, the Permissibility Machine induces a
certified language Lcert (MΠ ) ⊆ Σ∗ , consisting of proposed traces for which certification succeeds.
Because execution is allowed only after certification, the executable traces are precisely the generated
traces that also lie in the certified language. This gives the central object of the paper: the executable
trace language.
Generated language. Let LG := L(MG ) ⊆ Σ∗ denote the language of candidate execution traces
proposed by the generating machine. Equivalently,
                             LG = {τ ∈ Σ∗ : ∃x such that MG (x) = τ }.

Certified language. For a fixed policy system Π, let Lcert (MΠ ) = {τ ∈ Σ∗ : MΠ (τ, Π) = π}
denote the language of traces certified by the Permissibility Machine.
Executable language. A proposed trace is authorized for execution only when certification succeeds.
We therefore define the executable trace language by
                                    Lexec (A) = LG ∩ Lcert (MΠ ),
where A = (MG , MΠ , E) denotes the proposal–certification–execution architecture.
Theorem 3 (Executable Language Composition). Fix a policy system Π and architecture A =
(MG , MΠ , E). Under execution authorization, a trace is executable if and only if it is both generated
and certified. Equivalently, Lexec (A) = LG ∩ Lcert (MΠ ).

Interpretation. The identity Lexec (A) = LG ∩ Lcert (MΠ ) captures the proposal–certification–
execution logic in one line. Generation determines what can be proposed. Certification determines
which proposed traces are authorized for execution. Policy determines the semantic target: the


                                                    8
permissible trace language LΠ . Thus execution is not identified with generation, and certification is
not merely advisory; it is the authorization condition between proposal and execution.
Proof sketch. If a trace is executable, then it must have been produced by the generator, so τ ∈ LG .
Execution authorization also requires certification, so τ ∈ Lcert (MΠ ). Hence τ ∈ LG ∩ Lcert (MΠ ).
Conversely, if τ lies in this intersection, then it is a generated trace for which certification has
succeeded. Under the architecture, such traces are authorized for execution. A full proof is given in
Appx. B.
Semantic versus operational boundaries. The permissible language LΠ and the certified language
Lcert (MΠ ) are distinct objects. The former is semantic: it is defined by the policy system. The latter
is operational: it is defined by what the certifier can recognize and certify. Soundness requires
                                            Lcert (MΠ ) ⊆ LΠ ,
but completeness need not hold. The mismatch between the semantic permissible boundary and the
operational certification boundary is the source of the evaluation quantities studied next.

6   Policy Models and Proof Memory
The policy system determines what must be certified; proof memory determines what can be remem-
bered, replayed, and certified. This distinction is essential. A policy system specifies the obligations
a trace must satisfy, while proof memory specifies the proof-relevant history available to the certifier.
Policy-system interface. At the semantic level, a policy system induces a permissible trace language
                                             Π ⇝ LΠ ⊆ Σ∗ .
A trace τ is permissible under Π when τ ∈ LΠ . For proof-carrying execution, inspired by proof-
carrying code [19], the policy system may also support a derivability judgment, Π ⊢ τ : Permitted,
meaning that the permissibility of τ can be established within the policy calculus. A certificate π is a
checkable witness for such a judgment.
Canonical policy models. Different policy structures create different certification requirements. We
use four canonical models as running examples.

• Semantic trace-language policies represent a policy only by its induced language LΠ ⊆ Σ∗ . This
  model is sufficient for execution safety and certification-boundary analysis.
• Counter or resource-budget policies constrain cumulative quantities along the trace, such as
  exposure limits, query budgets, rate limits, or liquidity constraints. These policies are trace-
  dependent because the permissibility of the next action depends on accumulated history.
• Temporal or history-dependent policies impose ordering requirements, such as approval-before-
  execution, deletion after a retention window, mandatory escalation after unresolved evidence, or
  restrictions on reusing data for a new purpose.
• Information-flow policies govern access, source authorization, personally identifiable information
  (PII), purpose limitation, logging, retention, and downstream release, following the broader
  language-based information-flow tradition [20].

Proof memory. Proof memory stores the history needed to certify these policies: prior actions, query
counts, retrieved sources, evidence, computed values, approvals, policy versions, access decisions,
and audit records. A certifier cannot enforce a five-query budget unless it remembers the relevant
query count; it cannot certify evidence binding unless it remembers sources, tags, periods, units, and
computations; and it cannot support later audit unless it records the policy version under which the
trace was certified.
Worked certificate example. Consider an agent that produces a financial claim from a filing. A
certificate for the trace may contain proof objects
                    π = (πaccess , πsource , πtag , πperiod , πunit , πcompute , πclaim ).
These components certify, respectively, that the source was authorized, the filing was retrieved,
the relevant data tag was used, the period was aligned, units were normalized, the computation


                                                      9
was replayable, and the final claim was supported by the derivation trace. The certificate is not a
natural-language explanation; it is a structured witness that the trace satisfies policy obligations.
In financial reporting, XBRL/iXBRL provides a natural evidence layer for such certificates: reported
facts are associated with machine-readable concepts, reporting contexts, units, and filings [21, 22].
This connects directly to recent work on XBRL-based financial report analysis. XBRL-Agent shows
that LLM agents augmented with retrievers and calculators still face reliability challenges in XBRL
term understanding and financial calculation [16]. From the certified-trace perspective, the remedy
is not only better retrieval or calculation, but a certificate binding the generated claim to authorized
sources, XBRL concepts, reporting periods, units, replayable computations, and the final statement.

Certificate stack. In high-stakes deployments, a certificate should not be viewed as a single
monolithic proof. Rather, it is often a stack of proof objects, each witnessing a different policy
obligation. We write
            π = (πid , πauth , πsource , πpolicy , πrisk , πcompute , πprivacy , πhuman , πlineage ).
Here πid identifies the agent, user, principal, or institutional role on whose behalf the trace is proposed;
πauth certifies scoped authority or credentials; πsource certifies source access and evidence provenance;
πpolicy records the applicable policy clauses; πrisk certifies risk limits such as exposure, query budgets,
payment thresholds, or trading constraints; πcompute certifies replayable computation, including
formulas, units, periods, and code; πprivacy certifies access, retention, release, and information-flow
obligations; πhuman records human approval or escalation when required; and πlineage records the
policy version, certificate version, timestamp, and audit linkage.
Not every trace requires every component. The certificate stack is a design interface: the policy system
determines which components are mandatory for a given trace, while proof memory determines
which components can be produced, checked, or replayed.
Expressiveness and capacity. Proof memory has both qualitative and quantitative aspects. Proof-
memory expressiveness asks which trace properties or trace languages can be certified with a given
memory model. Proof-memory capacity asks how many proof-relevant histories the certifier can
distinguish under resource constraints. The basic principle is
          a certifier can only certify trace properties that its proof memory can distinguish.
Thus proof memory determines the resolution of the certification boundary.

7   Certification Boundary and Evaluation Measures
The framework above turns trustworthy agency into a measurable boundary problem. A generator
induces a distribution over proposed traces; the policy system defines which of those traces are
semantically permissible; the certifier determines which traces cross the certification boundary. This
section introduces the basic quantities needed to study that boundary.
Trace universe and generator distribution. Let µG denote the generator-induced distribution over
traces. We view µG as a distribution over Σ∗ supported on generated traces, so generated behavior is
measured relative to the agent’s own proposal distribution.
Generated permissibility risk. The generated permissibility risk is the probability that the generator
proposes an impermissible trace:
                                      GapΠ (MG ) = Pr [τ ∈
                                                         / LΠ ].
                                                         τ ∼µG

This quantity measures the semantic gap between generation and permissibility.
Certified-but-impermissible risk. The certified-but-impermissible risk is
                                                                     
                        uΠ (MG , MΠ ) = Pr τ ∈ Lcert (MΠ ) \ LΠ .
                                                 τ ∼µG

This is the unsafe-admission event: the certifier admits a trace that is in fact impermissible.
Missed-certification risk. The missed-certification risk is
                                                               
                         mΠ (MG , MΠ ) = Pr τ ∈ LΠ \ Lcert (MΠ ) .
                                                 τ ∼µG


                                                       10
Figure 2: Certification boundary. Generated traces LG are partitioned by semantic permissibility LΠ
and operational certification Lcert (MΠ ). The executable region is Lexec = LG ∩ Lcert (MΠ ); the two
boundary errors are missed certification, LG ∩ (LΠ \ Lcert (MΠ )), and certified-but-impermissible
risk, LG ∩ (Lcert (MΠ ) \ LΠ ).

This is the incompleteness event: a semantically permissible trace fails to be certified.
Executable yield. The executable yield is the probability mass of certified traces:
                                                                   
                           yΠ (MG , MΠ ) = Pr τ ∈ Lcert (MΠ ) .
                                                τ ∼µG

Because µG is generator-induced, this is precisely the fraction of generated trace mass that crosses
the certification boundary.
Theorem 4 (Certification Boundary Decomposition). For any policy system Π, generator MG , and
certifier MΠ , we have yΠ = 1 − GapΠ − mΠ + uΠ . If the certifier is sound, then uΠ = 0 and
therefore yΠ = 1 − GapΠ − mΠ .

Interpretation. The theorem is a conservation law for generated trace mass. Relative to the generator
distribution, a trace is either permissible or impermissible. Among permissible traces, some are
certified and some are missed. Among impermissible traces, some are correctly rejected and some
are wrongly certified. The executable yield is therefore the permissible generated mass, minus missed
certification, plus unsafe certification.
Boundary distance. A natural measure of the distance between the operational certification boundary
and the semantic permissible boundary is
             dµ (MΠ , Π) = µG (Lcert (MΠ )△LΠ ) = uΠ (MG , MΠ ) + mΠ (MG , MΠ ),
where △ denotes symmetric difference. This quantity makes explicit that certification quality is a
boundary-approximation problem: the certifier is good when its certified region closely matches the
true permissible region under the generator’s trace distribution.
Monitorability gap versus certification gap. Let O(τ ) denote the observable part of a trace available
to a monitor, such as outputs, actions, tool logs, activations, or chain-of-thought. A monitorability
gap arises when O(τ ) does not contain enough policy-relevant information to detect whether τ ∈ / LΠ .
A certification gap arises when the available observations and proof memory do not contain enough
checkable evidence to produce a certificate, even if the trace is semantically permissible. Thus
monitorability and certifiability are related but distinct: monitorability concerns detection from
observations, while certifiability concerns checkable permission for execution.
Fig. 2 visualizes the trace-level certification boundary induced by semantic permissibility and op-
erational certification. The outer region LG denotes generated traces. The green set LΠ denotes


                                                  11
traces that are semantically permissible under the policy system, while the purple set Lcert (MΠ )
denotes traces certified by the Permissibility Machine. Their overlap inside LG is the safe exe-
cutable region, LG ∩ LΠ ∩ Lcert (MΠ ). The left-only region LG ∩ (LΠ \ Lcert (MΠ )) corresponds
to missed certification: permissible traces that the certifier fails to certify. The right-only region
LG ∩(Lcert (MΠ )\LΠ ) corresponds to certified-but-impermissible risk: traces certified by the system
but not actually permissible. The executable region is Lexec = LG ∩ Lcert (MΠ ); if the certifier is
sound, then Lcert (MΠ ) ⊆ LΠ , and the certified-but-impermissible region disappears.

8   Privacy and Zero-Knowledge Trace Certification
Privacy is one of the clearest examples of trace-dependent permissibility, connecting certified traces
to information-flow security and privacy-preserving verification [20]. A final output may contain no
personally identifiable information (PII), while the trace that produced it may have accessed, stored,
logged, embedded, or leaked sensitive information. Thus privacy compliance cannot be certified by
output inspection alone:
                                    Clean Output ̸⇒ τ ∈ LΠpriv .

Privacy as a trace property. Let Πpriv denote a privacy policy that may constrain which user or
agent may access which data, for what purpose, through which component, and under which logging,
retention, and release conditions. These obligations concern the information-flow trace: prompts,
retrievals, tool calls, memory updates, logs, caches, vector stores, and released outputs.
Query budgets. A simple example is a query-budget policy. One query to a protected resource may
be authorized, while repeated queries within a time window may violate privacy or access-control
constraints. Let Nτ (u, R, W ) denote the number of queries by user or agent u to protected resource
R within window W along trace τ . A privacy policy may require Nτ (u, R, W ) ≤ B. Each individual
query may be permissible, while the full trace becomes impermissible once the budget is exceeded.
Privacy–observability tension. Certification requires evidence about the trace, but the trace itself
may contain sensitive data. A certifier may need to know whether a protected source was accessed,
whether PII flowed to an unauthorized component, whether a query budget was exceeded, or whether
an output used approved data. Revealing the raw trace to prove these facts may itself violate privacy.
Zero-knowledge certificates. This motivates privacy-preserving certification. A zero-knowledge
certificate can prove selected properties of an execution trace without revealing the sensitive trace
itself. For example, a certificate may establish that τ ∈ LΠpriv without exposing the underlying
prompts, private records, retrieved documents, model inputs, or intermediate computations.
Certifiable private trace properties. Privacy-relevant certificates may establish that all source
accesses were authorized, no PII was released to an unauthorized component, a query budget was not
exceeded, a computation used approved data without revealing the raw data, or an agent satisfied a
policy predicate without exposing private prompts or records.
Interpretation. Privacy creates a fundamental tension for trustworthy agents: trace certification
needs evidence, but privacy limits evidence exposure. Zero-knowledge trace certificates address
this tension by separating the property being certified from the sensitive data used to certify it. This
motivates privacy-preserving proof memory as a core component of certified AI-agent execution.

9   Limitations, Failure Modes, and Open Problems
Certified traces define a formal execution-governance framework, not a completed verification stack.
We close by addressing alternative views, limitations, and open problems for trustworthy AI agents.

Objection 1: Stronger models will solve this. Stronger generative models may reduce factual
errors, hallucinations, and tool-use mistakes, but they do not by themselves create permission.
Capability is not authority. A model may correctly infer an action or retrieve a useful source while
the trace violates access control, privacy, mandate, evidence, or execution policy.

Objection 2: Output guardrails are enough. Output guardrails are useful but incomplete. Many
violations occur inside the trace: unauthorized retrieval, leakage through prompts or logs, unreplayable


                                                  12
   Failure mode              Example                                   Certified-trace response
   Fake certificate          The agent fabricates an approval          Certificates must be checkable proof
                             sentence or cites a nonexistent pol-      objects, not natural-language self-
                             icy check.                                attestations.
   Stale policy              A trace is certified under an old man-    Certificates must bind to policy lineage:
                             date, access rule, or regulatory pol-     version, authority, timestamp, and effec-
                             icy.                                      tive date.
   Stale approval            A human approved an earlier trace,        Approvals should bind to a trace hash,
                             but the agent modifies the benefi-        scope, time window, and execution con-
                             ciary, amount, source, or action.         ditions.
   Tool deviation            A tool returns a different result or      Realized-trace conformance must be
                             executes a different call than the cer-   checked; deviations halt, roll back, or
                             tified proposed trace.                    escalate.
   Hidden policy state       The agent cannot see a restricted list,   Proof memory and policy-state inter-
                             query budget, client mandate, or ex-      faces must expose the facts needed for
                             posure limit.                             certification.
   Certificate laundering    A weak certifier approves a high-         Risk-tiered certification should specify
                             risk trace outside its authority.         which certifier class is authorized for
                                                                       each trace type.
   Privacy leakage           The raw trace needed for certifica-       Use selective disclosure, commitments,
                             tion contains sensitive client data or    access controls, or zero-knowledge trace
                             private prompts.                          certificates.
           Table 2: Failure modes for certified traces and corresponding design responses.


computation, cumulative exposure, purpose misuse, or policy-history violations. Trace certification
asks a stronger question: not only whether the output looks acceptable, but whether the process that
produced it satisfies the policy system.

Objection 3: Certification is too expensive. Full certification of every trace may be infeasible
or unnecessary. A practical path is to certify high-stakes traces first: actions that access sensitive
data, modify records, generate regulated recommendations, transfer assets, or trigger external exe-
cution. Certification can be made incremental through reusable proof memory, partial certificates,
domain-specific certifiers, and escalation when evidence is incomplete. Human review is therefore
a design option, not the definition of safety. The core requirement is that high-risk execution be
supported by checkable authorization evidence; such evidence may include policy-engine checks,
scoped credentials, cryptographic proofs, or human approvals. Risk-tiered certification is the opera-
tional response to this objection: certificate burden should scale with execution risk, irreversibility,
regulatory exposure, privacy sensitivity, and systemic impact.
Limitations. Certified traces do not solve value disagreement, policy design, institutional legitimacy,
or adversarial policy capture. A harmful, incomplete, or mis-specified policy can still certify harmful
behavior. Trace logging can also create privacy and surveillance risks if implemented naively.
Certification must therefore be paired with policy governance, privacy-preserving proof memory,
access control, and escalation. This also reinforces the need for independent evaluation and red
teaming of agentic systems, an issue emphasized by recent ICML position work on safe harbor for
AI evaluation [23].
Table 2 summarizes common failure modes for certified traces and the corresponding design re-
sponses.

Supervisory technology: Execution Certificates for Financial AI Agents. In regulated finance,
certified traces can be instantiated as a supervisory technology. A Financial AI Agent Execution
Certificate is a machine-readable record attached to a consequential agent action, recommendation,
report, payment instruction, trade proposal, or compliance decision. Such a certificate may include:
 πfin = (πagent , πprincipal , πpurpose , πsource , πpolicy , πrisk , πapproval , πcompute , πprivacy , πconform ).
Here πagent identifies the AI agent and system version; πprincipal identifies the human, desk, client,
fund, or institution on whose behalf the agent acts; πpurpose records the business purpose and
permitted scope; πsource records source access and evidence lineage; πpolicy records applicable
regulations, firm policies, client mandates, and policy versions; πrisk records risk-limit, restricted-list,


                                                        13
exposure, liquidity, or payment-threshold checks; πapproval records human approval or escalation
when required; πcompute records replayable formulas, code, units, periods, and computed values;
πprivacy records privacy, retention, and information-flow checks; and πconform records whether the
realized trace conformed to the certified proposed trace.
This certificate is not intended to replace existing regulation. It is a technical object that can make
existing supervisory obligations auditable for agentic systems. In this sense, certified traces provide
a bridge from AI-agent architecture to financial supervision: regulators and firms can ask not only
what an agent output, but what certificate authorized the action.
Research agenda. Certified traces suggest several directions for the machine learning community:

• Certifiable trace languages. Which classes of agent traces admit efficient sound certification?
• Proof-memory capacity and expressiveness. What proof-relevant history is needed to certify
  cumulative, temporal, privacy, or information-flow policies?
• Certification-boundary benchmarks. How should agents be evaluated by generated impermissi-
  bility, certified-but-impermissible risk, missed certification, and executable yield?
• Monitorability versus certification gaps. What information is visible to a monitor, what is
  retained in proof memory, and what is sufficient to authorize execution?
• Privacy-preserving trace certificates. How can systems prove policy compliance without expos-
  ing sensitive traces, prompts, records, or computations?
• Bounded certification. What tradeoffs arise among proof memory, latency, privacy, verification
  cost, and certification error?
• Policy drift and re-certification. How should certificates be maintained when laws, mandates,
  access rules, or institutional policies change?
• Compositional certification. When do certificates for tools, agents, or subtasks compose into
  certificates for multi-agent traces?

Conclusion. Trustworthy AI agents require more than generation. They require a theory of permissi-
ble execution. The central object is not the model output alone, but the certificate-bearing trace: a
generator proposes, a Permissibility Machine certifies, and an executor acts only after certification.
No certificate, no execution.

Acknowledgments
Xiao-Yang Liu Yanglet and Xiaodong Wang acknowledge the support from Columbia’s SIRS and
STAR Program, and The Tang Family Fund for Research Innovations in FinTech, Engineering,
and Business Operations. Xiao-Yang Liu Yanglet acknowledges the support from NSF IUCRC
CRAFT center research grant (CRAFT Grant 22017) for this research. The opinions expressed in this
publication do not necessarily represent the views of NSF IUCRC CRAFT.
Xiao-Yang Liu Yanglet and Xiaodong Wang acknowledge the JPMorganChase Faculty Research
Award. Any views or opinions expressed herein are solely those of the authors listed and may differ
from the views and opinions expressed by JPMorganChase or its affiliates. This material is not
a product of the Research Department of J.P. Morgan Securities LLC. This material should not
be construed as an individual recommendation for any particular client and is not intended as a
recommendation of particular securities, financial instruments, or strategies for any particular client.
This material does not constitute a solicitation or offer in any jurisdiction.

References
 [1] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan
     Cao. ReAct: Synergizing reasoning and acting in language models. In International Conference
     on Learning Representations, 2023.
 [2] Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Luke Zettle-
     moyer, Nicola Cancedda, and Thomas Scialom. Toolformer: Language models can teach
     themselves to use tools. In Advances in Neural Information Processing Systems, 2023.


                                                  14
 [3] Edoardo Debenedetti, Jie Zhang, Mislav Balunović, Luca Beurer-Kellner, Marc Fischer, and
     Florian Tramèr. AgentDojo: A dynamic environment to evaluate prompt injection attacks and
     defenses for LLM agents. In Advances in Neural Information Processing Systems, Datasets
     and Benchmarks Track, 2024.
 [4] OpenAI. OpenAI and PwC Collaborate to Reimagine the Office of the CFO. https://openai.
     com/index/openai-pwc-finance-collaboration/, 2026. Accessed: 2026-05-23.
 [5] American Express. American Express debuts Agentic Commerce Experiences (ACE) developer
     kit and announces industry-first protection for registered agent purchases. American Express
     Newsroom, 2026. Accessed May 2026.
 [6] Anthropic. Agents for financial services. Anthropic, 2026. Accessed May 2026.
 [7] Industrial and Commercial Bank of China. Q&A record for 2025 interim results announcement
     of industrial and commercial bank of China limited. ICBC Investor Relations, 2025. Accessed
     May 2026.
 [8] Tomek Korbak, Mikita Balesni, Elizabeth Barnes, Yoshua Bengio, Joe Benton, Joseph Bloom,
     Mark Chen, Alan Cooney, Allan Dafoe, Anca Dragan, et al. Chain of thought monitorability: A
     new and fragile opportunity for ai safety. arXiv preprint arXiv:2507.11473, 2025.
 [9] OpenAI. Evaluating chain-of-thought monitorability. OpenAI Research, 2025.
[10] Andres M. Bran, Sam Cox, Oliver Schilter, et al. Augmenting large language models with
     chemistry tools. Nature Machine Intelligence, 2024.
[11] X. Tang et al. Risks of AI scientists: Prioritizing safeguarding over autonomy. Nature
     Communications, 2025.
[12] Yangjun Ruan et al. Identifying the risks of LM agents with an LM-emulated sandbox. In
     International Conference on Learning Representations, 2024.
[13] Wenkai Yang, Xiaohan Bi, Yankai Lin, Sishuo Chen, Jie Zhou, and Xu Sun. Watch out for your
     agents! investigating backdoor threats to LLM-based agents. In Advances in Neural Information
     Processing Systems, 2024.
[14] Zhexin Zhang, Shiyao Cui, Yida Lu, Jingzhuo Zhou, Junxiao Yang, Hongning Wang, and
     Minlie Huang. Agent-SafetyBench: Evaluating the safety of LLM agents. arXiv preprint
     arXiv:2412.14470, 2024.
[15] Kexin Chu. A systematic survey of security threats and defenses in LLM-based AI agents: A
     layered attack surface framework. arXiv preprint arXiv:2604.23338, 2026.
[16] Shijie Han, Haoqiang Kang, Bo Jin, Xiao-Yang Liu, and Steve Y. Yang. XBRL Agent: Lever-
     aging large language models for financial report analysis. In Proceedings of the 5th ACM
     International Conference on AI in Finance, pages 856–864, 2024.
[17] Klaus Havelund and Grigore Rosu. An overview of the runtime verification tool java pathex-
     plorer. Formal Methods in System Design, 2004.
[18] Zhen Xiang, Linzhi Zheng, Yanjie Li, Junyuan Hong, Qinbin Li, Han Xie, Jiawei Zhang, Zidi
     Xiong, Chulin Xie, Carl Yang, Dawn Song, and Bo Li. GuardAgent: Safeguard llm agents by a
     guard agent via knowledge-enabled reasoning. arXiv preprint arXiv:2406.09187, 2024.
[19] George C. Necula. Proof-carrying code. In Proceedings of the ACM SIGPLAN-SIGACT
     Symposium on Principles of Programming Languages, 1997.
[20] Andrei Sabelfeld and Andrew C. Myers. Language-based information-flow security. IEEE
     Journal on Selected Areas in Communications, 2003.
[21] XBRL International. The Standard for Reporting. https://www.xbrl.org/the-standard/
     what/the-standard-for-reporting/, 2026. Accessed: 2026-05-23.


                                               15
[22] XBRL International. Inline XBRL.                https://www.xbrl.org/the-standard/what/
     ixbrl/, 2026. Accessed: 2026-05-23.
[23] Shayne Longpre, Sayash Kapoor, Kevin Klyman, Ashwin Ramaswami, Rishi Bommasani,
     Borhane Blili-Hamelin, Yangsibo Huang, et al. Position: A safe harbor for AI evaluation and
     red teaming. In International Conference on Machine Learning, 2024.
[24] Martin Leucker and Christian Schallhart. A brief account of runtime verification. The Journal
     of Logic and Algebraic Programming, 2009.
[25] Industrial and Commercial Bank of China. 2025 annual results announcement of industrial and
     commercial bank of China limited. ICBC Investor Relations, 2026. Accessed May 2026.


A    Formal Trace Model
This appendix gives the formal trace model underlying the main text. Its purpose is to make explicit
the objects, languages, and assumptions used by the proposal–certification–execution architecture.

Trace universe. Let Σ be an alphabet used to encode states, actions, tool calls, retrieval events,
evidence records, computation steps, memory updates, and execution events. A finite agent trace is
represented as a word
                                               τ ∈ Σ∗ .
When the context is clear, we write a structured state–action trace as
                                    τ = (s0 , a1 , s1 , . . . , aT , sT ),
where st ∈ S denotes the system state at time t, at ∈ C denotes a candidate action, and T < ∞ is
the trace horizon.

Proposed and realized traces. We distinguish a proposed trace from a realized trace. A proposed
trace τ prop ∈ Σ∗ is a structured pre-execution record of intended actions, tool calls, evidence,
approvals, credentials, computations, and execution conditions. This is the object submitted to the
Permissibility Machine for certification. A realized trace τ real ∈ Σ∗ records the events actually
performed after execution. Certification authorizes execution of the proposed trace, while audit-
ing checks whether the realized trace conforms to the certified proposed trace. For long-running
workflows, certification may occur repeatedly on trace prefixes before irreversible actions:
               prop                prop
              τ1:t     −→     MΠ (τ1:t  , Π)       −→        {authorize, reject, or escalate}.

Transition model.     A trace may follow a transition rule
                                  st = δ(st−1 , at ),         1 ≤ t ≤ T,
where δ : S × C → S is an abstract transition map. The deterministic notation is used only for
simplicity. Randomness, tool outputs, external observations, and environmental events can be encoded
into the state.

Action-level objects. The computable action set C denotes the candidate actions that the agent can
represent, generate, or submit. The action-level permissible set
                                                  P ⊆C
contains actions that are permitted when considered in isolation. The action-level permissibility gap
is
                                                  C \ P.
This action-level distinction is useful but insufficient: a trace may be impermissible even when all of
its individual actions lie in P .
Fig. 3 gives the action-level geometry of the separation principle. The set C is the operative universe
of computable candidate actions, while P ⊊ C is the subset of actions permitted at the action
level. The region C \ P is the permissibility gap: actions that may be generated or submitted by a
computational system, but should not be permitted for execution.


                                                     16
Figure 3: Action-level geometry of the permissibility gap. The computable action set C is the
operative universe of candidate actions available to the system. The permissible action set P ⊆ C
contains actions permitted at the action level. The region C \ P is the permissibility gap: actions that
are available to the system but not permitted. In the strict-separation setting considered here, P ⊊ C,
so the gap is nonempty.


Trace-level languages.     The generated trace language is
                                        LG := L(MG ) ⊆ Σ∗ ,
where MG is the generating machine. The policy system Π induces a semantic permissible trace
language
                                        LΠ ⊆ Σ∗ .
The certified trace language is
                             Lcert (MΠ ) = {τ ∈ Σ∗ : MΠ (τ, Π) = π},
where MΠ is the Permissibility Machine and π is a checkable certificate. The executable trace
language is
                                Lexec = LG ∩ Lcert (MΠ ).

Semantic versus operational regions. The language LΠ is semantic: it represents the traces that
are permissible under the policy system. The language Lcert (MΠ ) is operational: it represents the
traces that the certifier can certify. Sound certification requires
                                          Lcert (MΠ ) ⊆ LΠ .
Completeness is not required. In realistic settings, some permissible traces may be rejected or
escalated because the certifier lacks sufficient proof memory, evidence, time, or authority.

B     Proofs of Main Results
This appendix contains proofs omitted or abbreviated in the main text.

B.1   Proof of Proposition 1

Restatement. There exist policy systems and traces whose individual actions are locally permissible,
while the full trace is impermissible under the policy system.


                                                  17
                      Symbol     Meaning
                      S          System state space
                      C          Computable action set
                      P          Permissible action set (action level)
                      C \P       Permissibility gap
                      Σ          Alphabet of primitive trace symbols
                      τ          Finite agent trace
                      Π          Policy system (permissibility calculus)
                      π          Certificate
                      MG         Generating machine
                      MΠ         Certifying machine (Permissibility Machine)
                      E          External execution system
                               Table 3: Notations for primitive objects.



Proof. We give a concrete construction using a query-budget policy. Let R be a protected resource,
such as a password-related or identity-related database table. Let each action ai be a query to R
by an authenticated user or agent u. Define the local action-level permissible set P so that each
authenticated query is locally permissible:
                                                ai ∈ P.

Now define a trace-level privacy policy Πpriv that imposes a query budget. Let
                                            Nτ (u, R, W )
denote the number of queries by u to resource R within time window W along trace τ . The policy
requires
                                       Nτ (u, R, W ) ≤ 5.
Construct a trace τ in which the same authenticated user or agent issues six queries to R within the
same time window W . Each individual query is locally permissible, so
                                      ai ∈ P,       i = 1, . . . , 6.
However,
                                       Nτ (u, R, W ) = 6 > 5,
so the full trace violates the privacy policy. Therefore
                                             τ∈
                                              / LΠpriv ,
although every individual action in the trace is locally permissible. Hence local action-level permissi-
bility need not compose into trace-level permissibility.


B.2   Proof of Theorem 1

Restatement. Under sound certification and execution authorization, every executed trace is per-
missible:
                                 Execute(τ ) =⇒ τ ∈ LΠ .

Proof. By execution authorization,
                                  Execute(τ ) =⇒ τ ∈ Lcert (MΠ ).
By sound certification,
                                          Lcert (MΠ ) ⊆ LΠ .
Therefore τ ∈ LΠ .


                                                  18
      Notation                     Meaning
      L(·)                         Language generated/recognized by a machine
      LG := L(MG )                 Language generated by the generating machine
      LΠ                           Permissible trace language induced by policy system Π
      Lcert (MΠ )                  Certified language recognized by the certifier
      Lexec := LG ∩ Lcert (MΠ ) Executable language after certification
      Ltask                        Task language: traces that accomplish a specified task
      A = (MG , MΠ , E)            Proposal-certification architecture with execution system
        Π
      MG                           Policy-conditioned generator
      Π(MG )                       Runtime-enforced (sandboxed) generator
      Π ⊢ τ : Permitted            Derivability judgment for permissibility
      Πℓ                           Layer of a structured policy system Π
      Π≤k                          Partial policy stack through layer k
      GapΠ (MG )                   Generated permissibility risk
      uΠ (MG , MΠ )                Certified-but-impermissible risk of the certifier
      mΠ (MG , MΠ )                Missed-certification risk of the certifier
      yΠ (MG , MΠ )                Executable yield after certification
      KΠ (τ )                      Certificate complexity or proof burden of trace τ
      Dµ (t, t′ )                  Policy-lineage drift between policy systems Πt and Πt′
      Pperm , NPperm               Permissibility search–verification complexity classes
                   Table 4: Derived languages and architecture-level notations.



B.3   Proof of Theorem 3

Restatement.     For a fixed policy system Π and architecture
                                         A = (MG , MΠ , E),
a trace is executable if and only if it is both generated and certified. Equivalently,
                                    Lexec (A) = LG ∩ Lcert (MΠ ).

Proof. If a trace is executable under A, then it must have been proposed by the generating machine.
Hence τ ∈ LG . By execution authorization, the trace must also be certified before execution, so
τ ∈ Lcert (MΠ ). Therefore
                                       τ ∈ LG ∩ Lcert (MΠ ).

Conversely, suppose
                                        τ ∈ LG ∩ Lcert (MΠ ).
Then τ is a generated trace and certification succeeds. Under the architecture, generated traces are
authorized for execution only after certification succeeds. Hence τ is executable under A. Therefore
                                    Lexec (A) = LG ∩ Lcert (MΠ ).



B.4   Proof of Theorem 4

Recall the definitions
                                    GapΠ (MG ) = Pr [τ ∈
                                                       / LΠ ],
                                                       τ ∼µG

                            uΠ (MG , MΠ ) = Pr [τ ∈ Lcert (MΠ ) \ LΠ ],
                                              τ ∼µG

                           mΠ (MG , MΠ ) = Pr [τ ∈ LΠ \ Lcert (MΠ )],
                                               τ ∼µG

and
                               yΠ (MG , MΠ ) = Pr [τ ∈ Lcert (MΠ )].
                                                 τ ∼µG


                                                   19
Restatement.      For any policy system Π, generator MG , and certifier MΠ ,
                                          yΠ = 1 − GapΠ − mΠ + uΠ .
If the certifier is sound, then uΠ = 0 and
                                            yΠ = 1 − GapΠ − mΠ .

Proof. For readability, we write
                                              Lcert := Lcert (MΠ ).
The certified language decomposes into its permissible and impermissible parts:
                                   Lcert = (Lcert ∩ LΠ ) ∪ (Lcert \ LΠ ),
and the union is disjoint. Therefore
                          yΠ = Pr [τ ∈ Lcert ∩ LΠ ] + Pr [τ ∈ Lcert \ LΠ ].
                                  τ ∼µG                            τ ∼µG

The second term is uΠ . For the first term,
                   Pr [τ ∈ Lcert ∩ LΠ ] = Pr [τ ∈ LΠ ] − Pr [τ ∈ LΠ \ Lcert ].
                  τ ∼µG                            τ ∼µG                   τ ∼µG

By definition,
                                           Pr [τ ∈ LΠ ] = 1 − GapΠ ,
                                          τ ∼µG

and
                                           Pr [τ ∈ LΠ \ Lcert ] = mΠ .
                                          τ ∼µG

Combining these identities gives
                                          yΠ = 1 − GapΠ − mΠ + uΠ .
If the certifier is sound, then
                                                  Lcert (MΠ ) ⊆ LΠ ,
so
                                              Lcert (MΠ ) \ LΠ = ∅
and hence uΠ = 0. The sound-certifier identity follows.

B.5   Residual Execution Risk

Definition. Assume yΠ (MG , MΠ ) > 0. The residual execution risk is the probability that an
executed trace is impermissible:
                           ρΠ (MG , MΠ ) = Pr [τ ∈
                                                 / LΠ | τ ∈ Lcert (MΠ )].
                                                   τ ∼µG


Claim.    If yΠ (MG , MΠ ) > 0, then
                                                                uΠ (MG , MΠ )
                                      ρΠ (MG , MΠ ) =                         .
                                                                yΠ (MG , MΠ )
In particular, a sound certifier has zero residual execution risk.

Proof. By conditional probability,
                                                                  Pr[τ ∈ Lcert (MΠ ) \ LΠ ]
                     Pr[τ ∈
                          / LΠ | τ ∈ Lcert (MΠ )] =                                         .
                                                                    Pr[τ ∈ Lcert (MΠ )]
The numerator is uΠ (MG , MΠ ) and the denominator is yΠ (MG , MΠ ). If the certifier is sound, then
                                                  Lcert (MΠ ) ⊆ LΠ ,
so uΠ (MG , MΠ ) = 0 and hence ρΠ (MG , MΠ ) = 0.


                                                           20
B.6    Permissibility Recall

Definition. Assume 1 − GapΠ (MG ) > 0. The permissibility recall is the probability that a
permissible generated trace is certified:
                      RecallΠ (MG , MΠ ) = Pr [τ ∈ Lcert (MΠ ) | τ ∈ LΠ ].
                                               τ ∼µG


Claim.    If 1 − GapΠ (MG ) > 0, then
                                                           mΠ (MG , MΠ )
                             RecallΠ (MG , MΠ ) = 1 −                    .
                                                          1 − GapΠ (MG )

Proof. By conditional probability,
                                                         Pr[τ ∈ Lcert (MΠ ) ∩ LΠ ]
                    Pr[τ ∈ Lcert (MΠ ) | τ ∈ LΠ ] =                                .
                                                               Pr[τ ∈ LΠ ]
The denominator is 1 − GapΠ (MG ). The numerator is
           Pr[τ ∈ LΠ ] − Pr[τ ∈ LΠ \ Lcert (MΠ )] = 1 − GapΠ (MG ) − mΠ (MG , MΠ ).
Dividing gives the result.

B.7    Monotonicity Under Conjunctive Policy Strengthening

Claim.    Let
                                        Π′ = Π ∧ Πnew ,
where Πnew adds an obligation conjunctively and does not introduce an exception or override that
enlarges the permissible language. Then
                                              LΠ′ ⊆ LΠ .
Consequently, for a fixed generator distribution µG ,
                                     GapΠ′ (MG ) ≥ GapΠ (MG ).

Proof. A trace belongs to LΠ′ only if it satisfies both Π and Πnew . Therefore every trace permissible
under Π′ is permissible under Π, so
                                              LΠ′ ⊆ LΠ .
Taking complements in the common trace universe Σ∗ reverses the inclusion:
                                          Σ∗ \ LΠ ⊆ Σ∗ \ LΠ′ .
Equivalently,
                            {τ ∈ Σ∗ : τ ∈
                                        / LΠ } ⊆ {τ ∈ Σ∗ : τ ∈
                                                             / LΠ′ }.
Taking µG -probabilities gives
                                   Pr [τ ∈
                                         / LΠ ] ≤ Pr [τ ∈
                                                        / LΠ′ ].
                                  τ ∼µG                τ ∼µG

Thus
                                     GapΠ′ (MG ) ≥ GapΠ (MG ).


Caveat. This monotonicity statement assumes conjunctive strengthening. It need not hold if the new
policy layer introduces exceptions, overrides, or relaxations that enlarge the permissible language.

C      Canonical Policy Models
This appendix develops several mathematical models of policy systems. These models are not
intended to be exhaustive. Their purpose is to show how common policy structures induce different
trace-certification problems.


                                                  21
C.1   Semantic Trace-Language Policy

The most abstract model represents a policy system only by its induced permissible trace language:
                                              Π ≡ LΠ ⊆ Σ∗ .
A trace is permissible when
                                             τ ∈ LΠ .
This model is sufficient for the axioms of certifiable execution, executable-language composition,
and certification-boundary measures. It does not require a specific syntax for policies.

C.2   Automaton or Monitor Policy

Some policies can be represented by finite-state monitors. A monitor policy has the form
                                           Π = (Q, q0 , δΠ , F ),
where Q is a finite set of monitor states, q0 is the initial state, δΠ : Q × Σ → Q is a transition function,
and F ⊆ Q is the set of accepting states. The induced permissible language is
                                   LΠ = {τ ∈ Σ∗ : δΠ (q0 , τ ) ∈ F }.
This model captures workflow constraints, authentication states, local rule checks, and finite-state
runtime monitors.

C.3   Counter or Resource-Budget Policy

Counter policies constrain accumulated quantities along a trace. Let zt be a vector of counters
updated by
                                     zt = zt−1 + g(st−1 , at , st ),
where g records resource usage, exposure changes, query counts, or other cumulative quantities. A
counter policy requires
                                       zt ∈ Zsafe    for all t.
Examples include exposure limits, query budgets, rate limits, liquidity constraints, and daily trading
limits. These policies are trace-dependent because an action that is locally permissible may become
impermissible after accumulated usage crosses a threshold.

C.4   Temporal or History-Dependent Policy

Temporal policies impose ordering or timing obligations on traces. They may be represented by
finite-trace temporal formulas, such as formulas in LTLf or related logics. A trace is permissible
when
                                            τ |= φΠ .
Examples include approval-before-execution, deletion within a retention window, escalation after
unresolved evidence, prohibition of execution after a risk violation, and restrictions on reusing data
for a new purpose. Temporal policies make explicit that permissibility depends on event order and
history.

C.5   Information-Flow and Access-Control Policy

Information-flow policies govern which agents or components may access, transform, store, or release
which data. A trace may contain events
                                         et = (ut , ct , dt , pt , rt ),
where ut is a user or agent, ct is a component or tool, dt is a data item or data class, pt is a declared
purpose, and rt is a retrieved, released, or stored record. A policy may require
                                       AuthΠ (ut , ct , dt , pt ) = 1
and may also constrain downstream flow, logging, retention, redaction, and release. This model is
important for PII, source authorization, purpose limitation, and privacy-preserving agent traces.


                                                      22
C.6   Proof-Calculus Policy

For proof-carrying execution, a policy system may be viewed as a calculus supporting judgments
                                          Π ⊢ τ : Permitted.
A certificate π is a checkable witness for such a judgment. Soundness requires
                                   Π ⊢ τ : Permitted =⇒ τ ∈ LΠ .
This model distinguishes semantic permissibility from derivable permissibility. A trace may be
semantically permissible but not certifiable by the current proof system or proof memory.

C.7   Versioned or Dynamic Policy

In deployed systems, policies evolve. We write
                                              Πt −→ Πt′
to denote a policy update from time t to time t′ . A certificate issued under Πt may not remain valid
under Πt′ . Versioned policies motivate policy lineage: a certificate should record the policy version,
source, authority, and effective date under which a trace was certified.

Summary. The abstract semantic model defines the target permissible region. Automaton, counter,
temporal, and information-flow models expose common policy structures. Proof-calculus policies
support certificates. Versioned policies explain why certification must be tied to policy lineage.

D     Proof-Memory Models
This appendix defines proof-memory models and distinguishes expressiveness from capacity.

Proof-memory interface.       A proof-memory model is an abstract stateful structure
                                H = (S, h0 , Update, Query, Emit),
where S is the memory-state space, h0 ∈ S is the initial memory state, Update incorporates trace
events, Query retrieves proof-relevant facts, and Emit produces certificate components.
Given trace event et , the memory state evolves as
                                       ht = Update(ht−1 , et ).
The memory state ht is not merely storage. It is the proof-relevant history available to the certifier at
time t.

Proof-memory expressiveness. Proof-memory expressiveness describes which trace properties or
certified trace languages can be supported by a given memory model. For a fixed policy system Π, let
       CertLangΠ (H) = {Lcert (MΠ ) : MΠ uses proof memory H and Lcert (MΠ ) ⊆ LΠ } .
We say that H1 is no more certification-expressive than H2 , written
                                             H1 ⪯cert H2 ,
if
                                CertLangΠ (H1 ) ⊆ CertLangΠ (H2 ).
Thus expressiveness is qualitative: it concerns which trace obligations can be certified.

Proof-memory capacity. Proof-memory capacity is quantitative. For horizon T , let ST be the set
of memory states reachable after traces of length at most T . A simple capacity measure is
                                        CapH (T ) = log |ST |.
This measures how many bits of proof-relevant history the memory model can distinguish at horizon
T . A policy that requires distinguishing many history classes requires correspondingly large proof-
memory capacity.


                                                   23
Examples of proof-memory models.            Common proof-memory models include:

       • Finite-state memory: supports local checks and simple workflow constraints.
       • Counter memory: supports budgets, exposure limits, rate limits, and query counts.
       • Stack memory: supports nested obligations, scoped approvals, and recursive tasks.
       • Key-value or table memory: supports entity records, source permissions, and account-
         specific constraints.
       • DAG or provenance memory: supports evidence binding, computation replay, and deriva-
         tion traces.
       • Append-only ledger memory: supports auditability, policy lineage, and durable certification
         records.
       • Cryptographic commitment or zero-knowledge memory: supports privacy-preserving
         certification and selective disclosure.

Principle. A certifier can only certify trace properties that its proof memory can distinguish. This
principle is the memory analogue of trace non-compositionality: if a policy depends on history, then
certification requires access to the relevant history.

E    Additional Boundary Measures
This appendix collects additional measures for studying certification boundaries.

Certifier-policy distance.     The distance between the operational certified language and the semantic
permissible language is
                            dµ (MΠ , Π) = µG (Lcert (MΠ )△LΠ ) ,
where △ denotes symmetric difference. Expanding the symmetric difference gives
                             dµ (MΠ , Π) = uΠ (MG , MΠ ) + mΠ (MG , MΠ ).
Thus certification error decomposes into certified-but-impermissible risk and missed-certification
risk.

Monitorability gap and certification gap. Let O(τ ) denote the observable part of a trace available
to a monitor. This may include final outputs, actions, tool logs, activations, or chain-of-thought. A
monitorability gap arises when O(τ ) lacks enough policy-relevant information to determine whether
the trace is unsafe or impermissible. A certification gap arises when the available observations and
proof memory are insufficient to construct a checkable certificate, even when the trace is semantically
permissible. This distinction separates detection from authorization: monitorability supports suspicion
or warning, while certifiability supports execution permission.

Residual execution risk.       The residual execution risk is
                           ρΠ (MG , MΠ ) = Pr [τ ∈
                                                 / LΠ | τ ∈ Lcert (MΠ )].
                                             τ ∼µG

When yΠ (MG , MΠ ) > 0,
                                                           uΠ (MG , MΠ )
                                    ρΠ (MG , MΠ ) =                      .
                                                           yΠ (MG , MΠ )
Sound certifiers have zero residual execution risk.

Permissibility recall.     Permissibility recall is
                         RecallΠ (MG , MΠ ) = Pr [τ ∈ Lcert (MΠ ) | τ ∈ LΠ ].
                                                τ ∼µG

When 1 − GapΠ (MG ) > 0,
                                                               mΠ (MG , MΠ )
                              RecallΠ (MG , MΠ ) = 1 −                       .
                                                              1 − GapΠ (MG )

                                                      24
Certificate complexity.    For a trace τ , define its certificate complexity under policy system Π by
                             KΠ (τ ) = min{|π| : Π ⊢ τ : Permitted},
with KΠ (τ ) = ∞ if no such certificate exists. This measures the proof burden needed to move a
trace across the certification boundary.

Expected certificate burden.     For a generator distribution µG , define
                               K̄Π (MG ) = Eτ ∼µG [KΠ (τ ) | τ ∈ LΠ ],
when the conditional expectation is well-defined. This measures the average proof burden among
permissible generated traces.

Policy-lineage drift.   For two policy systems Πt and Πt′ , define a semantic policy distance
                                                                
                                  dµ (Πt , Πt′ ) = µ LΠt △LΠt′ .
A deployment-specific drift measure is
                                Dµ (t, t′ ) = µ Lcert (MΠt ) \ LΠt′ .
                                                                   

This measures the mass of traces certified under policy Πt that would no longer be permissible under
policy Πt′ .

Certification rate-distortion. Let M(B) denote a class of certifiers whose proof-memory capacity,
verification latency, or evidence budget is at most B. A generic certification distortion is
                    DΠ (B) =       inf     [αuΠ (MG , MΠ ) + βmΠ (MG , MΠ )] ,
                                MΠ ∈M(B)

where α, β ≥ 0 weight unsafe certification and missed certification. This quantity asks: under a
bounded certification resource, how well can the operational certified boundary approximate the
semantic permissible boundary?

F    Illustrative Examples and Proof Memory
The examples here explain why proof memory is a natural organizing dimension for certifiers. In
classical automata theory, memory controls what languages can be recognized. For permissibility
certification, memory controls what trace properties can be certified. Some constraints are local;
others depend on prior actions, cumulative exposure, evidence provenance, computation replay, or
audit history. Thus proof memory is what allows a certifier to move from local action checking to
trace-level certification.
The following examples serve four purposes. An action a ∈ C may represent a trade, a portfolio
decision, or an entire trading strategy, depending on abstraction level.
First, the examples witness the nonemptiness of the permissibility gap C \ P ̸= ∅. Second, they
suggest why permissibility may require external certification, rather than generation constraints alone.
Third, this motivates organizing certifiers by the richness of the proof memory they maintain:
                                     (0)      (1)        (2)     (3)
                                   MΠ ⪯ MΠ ⪯ MΠ ⪯ MΠ .
where ⪯ denotes “no more expressive than”. Richer proof memory may permit certification of richer
permissible languages. Fourth, they show that action-level permissibility may not compose into
trace-level permissibility.
The role of memory is analogous to state augmentation in sequential decision-making. In a Markovian
model, the current state must contain enough information from the past to determine future transitions
and evaluations. Similarly, in permissibility certification, proof memory records the information
from the past needed to certify future actions: prior trades, current holdings, exposures, evidence,
computations, approvals, and unresolved obligations. Thus proof memory may be viewed as a
certification-oriented state variable. Trace dependence does not contradict Markovian modeling; it
says that the state must contain the proof-relevant history.


                                                    25
F.1   Computable but Impermissible Strategy

Let a ∈ C be a computable trading strategy exploiting a market microstructure pattern. Suppose
a∈/ P because it violates exchange conduct rules. Then a ∈ C \ P.
This motivates finite-state certifiers of class
                                                        (0)
                                                    MΠ .

Concrete instantiation. Examples include spoofing-like order placement, latency-sensitive stale-quote
strategies, or microstructure exploits.
This illustrates
                                     Profitability ̸⇒ Permissibility.

F.2   Optimality Without Permissibility

Let w∗ be a portfolio allocation maximizing return subject to conventional risk constraints. Suppose
w∗ ∈/ P because it induces hidden leverage concentration forbidden by regulation. Then w∗ ∈ C \ P.
The optimization is valid, yet the resulting action is impermissible.
This motivates certifiers with arithmetic proof memory of class
                                                        (1)
                                                    MΠ .

Concrete instantiation. Examples include leveraged portfolios that satisfy optimization objectives
yet violate concentration, liquidity, or exposure constraints. Here permissibility depends not only on
feasibility, but on proving structural constraints.
This illustrates
                                    Optimality ̸⇒ Permissibility.
Thus richer certification may require more than finite-state recognition.

F.3   Permissible Actions, Impermissible Trace

Suppose each trade ai in a sequence passes local action-level checks:
                                            ai ∈ P       for all i.
In financial applications, the policy system Π should be understood schematically as combining
multiple sources of constraints:
 Π = law/regulation + fund mandate + client policy + internal risk rule + execution-control rule.
This expression is schematic rather than algebraic: it indicates that financial permissibility is usually
induced by a layered policy system. Section 3.7 develops this point further by connecting policy
layers to proof obligations and persistent proof memory.
For example, a portfolio policy may impose a concentration limit: semiconductor exposure must
remain below 20%. Each individual buy order may pass local checks: the security is tradable, the
account is authorized, and the single-order size is below a trading limit. Yet the sequence of orders
may push aggregate semiconductor exposure above 20%. The violation is not visible from the action
name alone; it is visible only from the trace and the evolving portfolio state.
Thus the sequence of trades may create an impermissible trace. The following proposition formalizes
this phenomenon by an explicit cumulative-exposure construction.
Proposition 2 (Non-Compositionality of Action-Level Permissibility). Action-level permissibility
need not compose into trace-level permissibility. There may exist a trace
                                      τ = (s0 , a1 , s1 , . . . , aT , sT )
such that
                                            ai ∈ P       for all i,
but
                                                  τ∈
                                                   / LΠ .


                                                      26
Proof. We prove the claim by construction. Consider a simplified portfolio state st = et ∈ [0, 1],
where et denotes the portfolio exposure to a given sector after time t. Let the computable actions be
buy orders
                                       a(q) ∈ C,       q ≥ 0,
where q is the additional sector exposure created by the order. The transition rule is
                                             et = et−1 + qt
when action a(qt ) is taken.
Define action-level permissibility by a single-order limit:
                                   P = {a(q) ∈ C : 0 ≤ q ≤ 0.10}.
Thus every order of size at most 10% sector exposure is permissible at the action level.
Now let the trace-level policy system Π impose a cumulative exposure constraint:
                   LΠ = {τ = (s0 , a1 , s1 , . . . , aT , sT ) : et ≤ 0.20 for every t}.
This says that the sector exposure must never exceed 20% along the trace.
Take initial exposure e0 = 0 and consider the trace generated by three buy orders
                       a1 = a(0.10),         a2 = a(0.10),         a3 = a(0.10).
Each action is individually permissible, since
                                      ai ∈ P        for i = 1, 2, 3.
However, the resulting exposure sequence is
                               e1 = 0.10,      e2 = 0.20,        e3 = 0.30.
Since e3 > 0.20, the trace violates the cumulative exposure constraint. Therefore
                                                 τ∈
                                                  / LΠ ,
although every action in the trace belongs to P . Hence action-level permissibility need not compose
into trace-level permissibility.

This illustrates
                               Permissible Actions ̸⇒ Permissible Trace.

F.4   Correct Answer, Impermissible Trace

Let τ be a reasoning trace produced by a language model. Suppose the resulting financial conclusion
is correct, but τ contains fabricated citations, unsupported claims, or unreplayable calculations. Then
τ∈ / LΠ . Correctness of answer does not imply permissibility of trace.
A financial reporting example makes this distinction concrete. Suppose an agent writes that a firm’s
gross margin improved year over year. The statement may be true as a final claim, but the trace may
still be impermissible if the agent used inconsistent periods, unsupported sources, incorrect XBRL
tags, incompatible units, or unreplayable arithmetic. A certifiable explanation must bind the claim
to a derivation trace: source filings, extracted facts, period alignment, unit normalization, formula,
computation, and claim generation.
This phenomenon appears concretely in XBRL-based financial report analysis, where LLMs must
bind claims to filing facts, taxonomy concepts, periods, units, and computations [16].
This motivates proof-carrying certifiers of class
                                                     (2)
                                                  MΠ .

Concrete instantiation. A financial agent may correctly infer leverage has declined, yet cite nonexis-
tent filings or use inconsistent accounting periods.
This illustrates

                                 Correct Answer ̸⇒ Permissible Trace.


                                                    27
F.5   Escalation as a Permissible Action

Suppose evidence is incomplete, so neither approval nor rejection can be certified. Then
                                            MΠ (τ ) = Escalate.
Proposition 3 (Escalation Under Uncertainty). There exist states in which
                                                  Escalate
is the unique permissible action.

Proof. Suppose neither approval nor rejection is derivable under Π. Then execution is unjustified,
and rejection is unsupported. Escalation is therefore the only permissible action.

In this sense, escalation is not merely a rejection alternative. It may be the required continuation of
certification under uncertainty.
This motivates escalation-aware certifiers of class
                                                        (3)
                                                    MΠ .

Concrete instantiation. In shell-company screening, uncertain ownership structures may force
escalation.
This illustrates
                                    High Confidence ̸⇒ Permission.

F.6   Proof-Carrying Execution

Suppose a trading agent proposes the trace
                                            τ = “buy asset A”.
Execution requires a certificate
                                    π = (πsuitability , πrisk , πliquidity ).
Execution proceeds only when the trace τ is accompanied by a valid certificate π. No certificate, no
execution.
This motivates certifiers for structured proof objects.
Concrete instantiation. A trade may be computationally feasible yet executable only when accompa-
nied by certifiable evidence.
This illustrates
                             Provable Permissibility ⇒ Executable Trace.
This elevates certification from filter to precondition for execution. This operationalizes the second
purpose above: permissibility may require certification rather than generation constraints alone.

F.7   Persistent Proof Memory

Some certifications require persistent proof memory. A certifier may maintain an append-only
memory state
                                       Mt+1 = Mt ∪ {πt },
where πt records a certificate produced at time t.
In regulated finance, however, persistent proof memory should record more than the certificate alone.
It should record both the lineage of the trace and the lineage of the policy system under which the
trace was certified. A financial trace is not certified against a timeless policy; it is certified against a
particular version of the policy system in force at certification time.
Thus a persistent-memory certifier may store records of the form
                            (τt , πt , Πt , sourcet , versiont , effective datet ),


                                                      28
where τt is the certified trace, πt is the certificate, Πt is the policy system used for certification, and
the remaining fields record the legal, regulatory, mandate, or internal-policy lineage of Πt .
This distinction matters because financial requirements evolve. Laws, regulations, supervisory
guidance, client mandates, fund prospectuses, and internal risk rules may change over time. A later
auditor may ask two different questions:
                                     Was τt permissible under Πt ?
and
                   Would τt remain permissible under a later policy system Πt′ ?
These are distinct questions. The first is historical verification; the second is re-certification under
policy change.
Thus persistent proof memory may be decomposed as
                    Persistent Proof Memory = Trace Lineage + Policy Lineage.
This decomposition becomes especially important when Π has internal structure: a later audit may
need to know not only which trace was certified, but also which policy layers, policy versions, access
permissions, and evidence obligations were used to certify it. Trace lineage records how the action,
report, recommendation, or trade was produced: retrieval, tool use, evidence, computation, claim
generation, and execution conditions. Policy lineage records which policy system was applied: legal
requirements, regulatory guidance, fund mandate, client policy, internal risk rule, execution-control
rule, version, source, and effective date.

Layered policy systems and proof obligations. The policy system Π should not be viewed as a
flat list of rules. In real financial and access-control environments, policy is often layered, partially
ordered, and versioned. Some components are hard constraints; some are inherited permissions; some
are temporal; some require escalation; and some depend on evidence, prior trace history, or policy
version.
Schematic examples include
             Π = Πlaw ∧ Πmandate ∧ Πclient ∧ Πrisk ∧ Πaccess ∧ Πprivacy ∧ Πexecution .
This expression is schematic rather than literal: the layers need not form a simple linear order. For
example, legal or regulatory constraints may dominate client-specific preferences; fund mandates
may specialize institutional rules; access-control policies may be inherited through roles or groups;
and execution rules may depend on the current market state, account state, or unresolved certification
obligations.
Access control is a particularly clear example. A financial agent may need to certify that a user is
authorized to access a source, that the agent is permitted to call a tool, that the retrieved data may be
used for the stated purpose, that sensitive information may not leave a protected environment, that the
final output may contain the derived information, and that the trace may be stored in logs. Some of
these obligations are local, such as whether a user has permission to read a document. Others are
trace-dependent, such as whether a source was retrieved for one purpose and later used for another.
Still others are policy-lineage dependent, because an access may have been allowed under policy
version Πt but may require re-certification under a later policy system Πt′ .
Under a layered policy system, certification naturally decomposes into layered proof obligations. If
                                                    d
                                                    ^
                                              Π=          Πℓ ,
                                                    ℓ=0

then a certificate may be represented schematically as π = (π0 , π1 , . . . , πd ), where πℓ certifies the
obligations induced by layer Πℓ . For example, an access-control component may certify authorized
retrieval, an evidence component may certify source binding, an accounting component may certify
period and unit consistency, a risk component may certify mandate or exposure constraints, and a
privacy component may certify non-disclosure or redaction obligations.
Thus policy layers and proof-memory classes play different roles. The policy system determines
what must be certified; proof memory determines what can be remembered, replayed, and certified.


                                                    29
Proof memory is the bridge between them: it records which policy-layer obligations have already
been satisfied, under which policy version, and with which supporting evidence.
This motivates persistent-memory certifiers of class
                                                    (3)
                                                 MΠ .
Examples include immutable audit trails, blockchain commitments, zero-knowledge proof certificates,
and versioned policy ledgers.
This suggests a hierarchy of proof memory classes:
                                  Finite < Structured < Persistent.
Richer proof memory may permit certification of richer permissible languages.

F.8   Self-Approval Is Not Certification

A final example clarifies why the proposal and certification roles should not be collapsed. Suppose an
autonomous trading agent proposes a trace τ and also outputs the statement

                        πself = “this trace is permissible because I certify it.”

This statement should not by itself count as a valid certificate. It is only a self-assertion by the same
system whose behavior is being judged. If such self-approval were sufficient, then the distinction
between generation and certification would collapse: a generator could make a trace executable
merely by claiming that it is executable.
A simple governance rule is therefore:


Rind :   A trace may execute only if its certificate is verified by a certifying role distinct from the proposal itself.

Here “distinct” need not mean a different physical machine. It means a logically separate certification
role: for example, an external policy engine, a proof checker, a compliance contract, a verifier with
access to policy Π, or a human escalation process. The generator may provide evidence or a proposed
proof object, but the certificate must be checkable by the certifier.
Under this rule, the trace
                                                (τ, πself )
does not execute merely because the agent approves itself. Instead, the certifier must verify that there
exists a valid certificate
                                  π such that Π ⊢ τ : Permitted.
If no such certificate can be verified, the outcome is rejection or escalation:
                                      MΠ (τ ) ∈ {⊥, Escalate}.

This example illustrates the principle
                                   Self-Approval ̸⇒ Permissibility.

The example is not meant to prove a formal paradox. Its purpose is to show why trustworthy financial
agents should separate the authority to propose a trace from the authority to certify that the trace
may execute. More generally, policies that refer to certification, delegation, or authority may create
self-referential obligations. Such obligations motivate the incompleteness questions discussed later in
Section 7.

F.9   Examples as Separation and Proof-Memory Witnesses

The examples in Appendix F have a cumulative structure. Appendices F.1–F.2 witness the action-
level permissibility gap. Appendix F.3 shows why locally permissible actions may compose into an
impermissible trace. Appendix F.4 motivates evidence binding, claim support, and computation replay.


                                                   30
Figure 4: Proof-memory classes of certifiers. The examples in Appendix F motivate a progression
of certifier classes ordered by proof-memory support, from local checks to persistent proof memory:
   (0)       (1)       (2)       (3)
MΠ ⪯ MΠ ⪯ MΠ ⪯ MΠ . Level 0 performs deterministic checks and attaches source links;
Level 1 constructs structured certificates and supports replay of evidence and computations; Level
2 supports proof-carrying execution, where a trace executes only when accompanied by a valid
certificate; and Level 3 maintains persistent proof memory, including trace lineage, policy lineage,
and durable certification records. The hierarchy is not a claim that all implementations fall into
exactly four classes; it illustrates how richer proof memory supports richer trace-level certification.


Appendix F.5 shows why escalation may itself be the permissible continuation under uncertainty.
Appendices F.6–F.7 motivate proof-carrying execution, policy lineage, and persistent proof memory.
Section 8 develops the privacy and zero-knowledge trace-certification setting.
Thus the examples are not isolated anecdotes; they are witnesses for increasingly rich certification
requirements. They point to the same paradigm:
                     language models propose; Permissibility Machines certify.
Certification mediates execution.
These examples witness recurring separation phenomena:
                                    Profitability ̸⇒ Permissibility,
                                    Optimality ̸⇒ Permissibility,
                             Permissible Actions ̸⇒ Permissible Trace,
                               Correct Answer ̸⇒ Permissible Trace,
                                   High Confidence ̸⇒ Permission,
                                   Self-Approval ̸⇒ Permissibility.
They also motivate the certifier hierarchy
                                      (0)      (1)        (2)    (3)
                                    MΠ ⪯ MΠ ⪯ MΠ ⪯ MΠ .

Fig. 4 summarizes this progression. The figure should be read as an organizational hierarchy rather
than as a claim that all certifier implementations must fall into exactly four rigid classes. Its purpose


                                                     31
is to make explicit the role of proof memory as the organizing axis of certification. At the lowest
level, a certifier performs deterministic checks and attaches source links. At richer levels, the certifier
constructs structured certificates, supports replay of evidence and computations, conditions execution
on proof objects, and eventually maintains persistent records for audit and re-certification.
The central point is that proof memory is not merely storage. It records the proof-relevant history
needed to certify a trace: prior actions, current state, retrieved evidence, computations, approvals,
policy versions, and unresolved obligations. As the policy system becomes more layered and trace-
dependent, the certifier must preserve more of this history in order to determine whether a generated
trace may execute.
Richer proof memory may permit certification of richer permissible languages. This motivates the
heuristic principle:
Heuristic Principle 1 (Memory–Expressiveness Tradeoff).
                              (i)      (j)                       (i)                  (j)
                       If MΠ ⪯ MΠ , then Lcert (MΠ ) ⊆ Lcert (MΠ ).
The examples suggest both C \ P ̸= ∅ and the need for increasingly expressive certifiers. They all
point to the same paradigm:
                    Language Models propose;          Permissibility Machines certify .
Certification mediates execution.
These examples also suggest a broader hypothesis: generation constraints may reduce violations in
C \ P, but may not eliminate the need for certification. This motivates asking whether constrained
generation can subsume certification at all.

G    Related Work and Positioning
This appendix positions the proposed framework relative to nearby areas. The contribution is not
that certification, monitoring, or proof checking are new. The contribution is to identify certified
execution traces as an organizing object for trustworthy AI agents.

Positioning. This paper sits at the intersection of chain-of-thought monitorability, LLM-agent
safety, runtime enforcement, proof-carrying code, and information-flow security. CoT monitorability
studies whether reasoning trajectories can be inspected for signs of misbehavior [8, 9]. Agent
benchmarks and attacks expose failures arising from tool use, untrusted data, environment interaction,
and multi-step behavior [12, 3, 13, 14]. Runtime enforcement intervenes during execution [17, 18];
proof-carrying code checks safety certificates for code [19]; and information-flow security studies
end-to-end confidentiality and data-flow constraints [20]. Certified traces combine these ideas around
a policy-governed execution rule: no certificate, no execution.

 Area                        Main object                               Relation to certified traces
 Output guardrails           Final answer or response                  Useful but misses trace-level violations.
 CoT monitorability          Reasoning trajectory                      One observation channel inside a broader
                                                                       execution trace.
 Agent-safety benchmarks     Tool-use failures and adversarial         Expose failures that certified traces aim to
                             tasks                                     govern.
 Runtime monitoring          Execution-time rule violations            Detects or intervenes; certification autho-
                                                                       rizes before execution.
 Proof-carrying code         Code plus safety proof                    Formal ancestor of certificate-bearing exe-
                                                                       cution.
 Information-flow security   Data-flow constraints                     Provides policy models for privacy and
                                                                       access-control traces.
              Table 5: Positioning of certified traces relative to nearby research areas.


Proof-carrying code. Proof-carrying code requires executable code to carry a checkable safety
proof before execution [19]. Our framework adapts this idea from code artifacts to AI-agent traces.
The certificate is attached not merely to a program, but to a generated sequence of retrievals, tool
calls, computations, memory updates, evidence bindings, and execution conditions.


                                                      32
Runtime monitoring and formal verification. Runtime monitors inspect system behavior against
specifications, and formal verification studies whether systems satisfy formal properties [17, 24].
Permissibility Machines inherit this verification spirit, but focus on the agent-specific boundary
between generated traces and execution-authorized traces under policy systems.

AI agents and tool-use safety. Recent AI-agent systems can call tools, retrieve information, modify
external state, and coordinate multi-step workflows. This expands the safety object from final output
to execution trace. Certified traces provide a way to ask whether the full agent workflow, not merely
the final answer, satisfies the policy system.

Tool-using and scientific agents. Toolformer and ReAct show how language models can integrate
tool calls and interleave reasoning with acting [2, 1]. Scientific-agent systems such as ChemCrow
demonstrate the same shift in high-stakes domains, where agents use expert tools for chemistry,
drug discovery, and materials design [10]. Recent discussions of AI scientists emphasize that
autonomous scientific agents require stronger safeguarding, especially around tool use, action spaces,
and downstream impact [11]. These works motivate our claim that the safety object is not merely the
final answer, but the execution trace.

Chain-of-thought monitorability and reasoning traces. Recent work frames chain-of-thought
monitorability as a new but fragile opportunity for AI safety: visible reasoning may allow monitors
to detect intent to misbehave, but the opportunity may change as models, training methods, and
reasoning formats evolve [8]. OpenAI’s monitorability evaluations define monitorability as the
ability of a monitor to predict properties of an agent’s behavior from observations such as actions,
outputs, activations, or chain-of-thought signals [9]. Our framework is complementary. We treat
chain-of-thought as one possible component of a broader execution trace, together with retrievals,
tool calls, data flows, computations, memory updates, logs, and execution conditions. Visibility alone
is not certification: a trace may be visible but unsupported, unauthorized, private, or unreplayable.
Certified traces ask for checkable witnesses of permissibility, not merely inspectable reasoning.

Agent safety and tool use. Agent-safety benchmarks increasingly study agents that combine
reasoning with external tool calls. For example, AgentDojo evaluates prompt-injection attacks and
defenses for agents executing tools over untrusted data [3]. Such benchmarks expose precisely the
kind of trace-level failures that output checking misses: unsafe retrieval, malicious tool outputs, and
policy-violating actions. Our paper is complementary: rather than proposing another benchmark, it
asks what formal object should govern whether such traces may execute.

Layered attack surfaces for agentic systems. Recent survey work proposes a Layered Attack
Surface Model for LLM-based agents, separating threats across foundation, cognitive, memory, tool-
execution, multi-agent, ecosystem, and governance layers, and adding a temporal axis for attacks that
persist across sessions or manifest slowly [15]. This taxonomy is complementary to our framework.
LASM asks where agentic threats arise; certified traces ask when a generated trace may be authorized
for execution under a policy system.

Runtime guardrails and enforcement for agents. Recent work also studies guardrails and runtime
enforcement for LLM agents. GuardAgent, for example, oversees a target LLM agent by checking
whether its behavior satisfies user-defined guard requests and by translating those requests into
executable checking code [18]. These systems are closely related to our motivation. The distinction
is that our paper makes certification a precondition for execution and studies the induced certification
boundary, rather than treating guardrails only as runtime checks or post-hoc filters.

AI governance and auditability. Governance frameworks emphasize accountability, transparency,
risk management, and auditability. Certified traces translate these goals into technical objects: trace
languages, certificates, proof memory, policy lineage, and certification boundaries.

From model materials to trace materials. Recent licensing work for machine-learning models
introduces the notion of Model Materials: the model architecture, parameters, data, documentation,
software, evaluation assets, and related artifacts distributed with a model. This is a useful analogy for
certified execution. Model-release governance asks what materials are needed to understand, reuse,


                                                   33
or audit a model distribution. Agent-execution governance asks what trace materials are needed to
authorize an action: evidence, tool calls, source access, approvals, computations, credentials, policy
versions, and execution conditions. Open model materials clarify what is being released; certified
trace materials clarify what is being executed.

Privacy and zero-knowledge proofs. Privacy-preserving verification and zero-knowledge proofs
make it possible to prove selected properties without revealing sensitive data. In this paper, they
address the privacy–observability tension: trace certification needs evidence, but raw traces may
contain private information.

Financial AI systems and benchmarks. Financial AI systems and benchmarks motivate the frame-
work because finance combines structured data, regulations, audit requirements, privacy constraints,
and execution risks. The proposed theory is broader than finance, but finance provides concrete
examples where trace-level certification is especially visible. Financial-domain agent systems provide
concrete testbeds for trace certification.

Industry movement toward financial agents. Recent industry announcements suggest that fi-
nancial AI agents are moving from pilots toward production workflows. OpenAI and PwC describe
agents for CFO workflows such as procurement, payments, treasury, tax, and close, with an emphasis
on controls and human oversight [4]. American Express’s ACE initiative points toward agentic
commerce and payment credentials for verified agents [5]. Anthropic’s financial-services agents
connect to market data, research platforms, and internal systems under governed access controls [6].
ICBC reports AI agent systems and large-model infrastructure for settlement finance, credit risk, and
risk-control workflows [7, 25]. These developments motivate our central question: when an agent
enters a real financial workflow, what certificate authorizes execution?
XBRL-Agent uses LLM agents with retrievers and calculators for XBRL report analysis, exposing
both the promise and the reliability limits of tool-augmented financial analysis [16]. Our framework
abstracts these concerns into certificate components for source access, tag selection, period alignment,
unit normalization, computation replay, and claim support.

H     Guiding Principles and Remaining Open Problems
This appendix collects guiding principles that follow from the proposal–certification–execution
framework and identifies remaining open problems.

H.1   Guiding Principles

We summarize the guiding principles as follows.

Principle 1: Computability is not permissibility. A system may be able to represent, generate, or
submit an action without that action being permitted: P ⊊ C.

Principle 2: Permissibility is trace-dependent. Permissibility is not only an action-level property.
It may depend on the trace in which actions occur: state, timing, evidence, computation, source
access, and policy history.

Principle 3: Generation and certification are distinct roles. A generating machine proposes
candidate traces, while a Permissibility Machine certifies whether a generated trace may execute
under a policy system Π.

Principle 4: No certificate, no execution. Execution is not a direct consequence of generation. A
trace becomes executable only when accompanied by a certificate witnessing permissibility under Π.

Principle 5: Proof memory supports certification. Persistent proof memory records trace lineage
and policy lineage, allowing certifiers to replay, audit, and re-certify trace-level obligations.

Principle 6: No self-certification. A high-stakes agent may propose evidence for its trace, but it
should not be the sole authority certifying that its own proposed trace is permissible.


                                                  34
H.2   Open Problems

Open Problem 1: Certifiable trace languages. Which policy-induced trace languages LΠ ⊆ Σ∗
admit efficient sound certification? The answer should depend on the policy model: finite-state
workflow rules may admit lightweight certificates, counter and temporal policies may require proof
memory, and information-flow or proof-calculus policies may require richer evidence, provenance,
or cryptographic witnesses. A theory of certifiable trace languages should characterize the tradeoff
among policy expressiveness, proof-memory requirements, verification time, and certificate size.

Open Problem 2: Proof-memory lower bounds. What proof-memory capacity is necessary to
certify a given class of trace-dependent policies? Can one prove Myhill–Nerode-style lower bounds
showing that certain policies require distinguishing a minimum number of proof-relevant history
classes?

Open Problem 3: Certification rate-distortion. What is the best achievable certification boundary
under constraints on memory, latency, privacy, or verification cost? Can one derive rate–distortion
laws relating proof-memory capacity to certified-but-impermissible risk and missed-certification risk?

Open Problem 4: Policy drift and re-certification. How should certificates be maintained,
invalidated, or updated when policy systems evolve? What is the right measure of distance between
policy versions, and how does this distance determine re-certification burden?

Open Problem 5: Privacy-preserving proof memory. How can proof memory support auditability
without exposing sensitive trace contents? What trace properties can be certified using commitments,
selective disclosure, or zero-knowledge proofs?

Open Problem 6: Compositional certification for multi-agent systems. When do certificates for
individual agents, tools, or subtasks compose into certificates for multi-agent traces? What additional
obligations arise from delegation, communication, and shared memory?

Open Problem 7: Benchmarks for certified agents. How should the community evaluate trace-
level certification rather than output accuracy alone? What datasets, tasks, metrics, and failure
cases are needed to measure generated permissibility risk, certified-but-impermissible risk, missed
certification, executable yield, and certification cost?




                                                  35
