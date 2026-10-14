                                         Specifying AI-SDLC Processes: A Protocol Language for
                                         Human-Agent Boundaries
                                         YLLI PRIFTI, Birkbeck, University of London, United Kingdom
                                         PASQUALE DE MEO, University of Messina, Italy
                                         ALESSANDRO PROVETTI, Birkbeck, University of London, United Kingdom
                                         AI agents now participate as first-class members of the software development lifecycle, but the models
                                         underneath them are both a moving target and an unreliable one: they change with every release, and they
                                         hallucinate, drift from instructions, lose context—and, more recently, lose containment, with documented
                                         cases of agents breaking out of their sandboxes and gaming the very checks meant to evaluate them. Teams
                                         therefore face a problem no existing tool addresses: how to specify how work is done the modes, approval
                                         gates, and responsibility boundaries of an AI-SDLC process in a way that is flexible enough to evolve with
                                         the models yet robust to their failures. Encoding process in agent prompts is flexible but not enforceable;
                                         adjacent formalisms (workflow management, business processes) are enforceable but do not model autonomous
arXiv:2606.20615v3 [cs.AI] 16 Aug 2026




                                         agents; and point solutions address only fragments (access control, approval gates). Teams consequently adopt
                                         AI-SDLC workflows through ad-hoc tooling.
                                            We propose a domain-specific language for specifying AI-SDLC processes as protocols, with formal abstract
                                         syntax, well-formedness conditions, operational semantics, and enforcement invariants. Its organising idea is a
                                         separation of policy (declared intent) from mechanism (structural enforcement), and this separation yields two
                                         things at once. First, flexibility: processes become portable artifacts—modes, validator quorums, and the 2+N
                                         human-in-control pattern (two human-in-control roles plus N specialised agent members, formalising classical
                                         Separation of Duties)—that teams reconfigure per task without touching agent code. Second, quasi-determinism:
                                         we prove that for any well-formed protocol, validation tokens, capability boundaries, and non-overridable
                                         gates make protocol steps impossible to skip — the enforcement invariants hold on every execution trace,
                                         closed under Kleene composition of orchestration loops — eliminating process non-determinism and bounding
                                         the residual model non-determinism. A failure-rate analysis derives two consequences: structural enforcement
                                         bounds silent failure at a weighted product of agent and validator rates while converting the remainder into
                                         visible, audited stalls (a trade autonomous benchmarks structurally cannot reward), and the benefit carries a
                                         capability floor — enforcement multiplies the value of a capable agent but cannot substitute for one.
                                            We validate the design in simulation — disagreement-policy trade-offs, governance overhead near 1% of
                                         inference latency, the failure-rate model, and Byzantine robustness — and end-to-end on real software tasks.
                                         On SWE-bench Verified, an identical bug-fix methodology yields no improvement over bare prompting when
                                         delivered as prose instructions, but a significant, replicated 14–22 point gain when executed as a validated,
                                         self-correcting process (two model tiers, task samples up to 𝑛=191); an ablation attributes the gain to the
                                         executed process itself; the process compresses the model-tier gap, with a cheap model under the process
                                         outperforming a strong model without it; and the effect vanishes below the capability floor the failure-rate
                                         model predicts.
                                            We position the contribution against multi-agent frameworks (MetaGPT), workflow specification (FlowA-
                                         gent, BPMN extensions), and capability-based security (SAGA): none combines enforceable process specifica-
                                         tion, autonomous-agent modelling, and a formal enforcement guarantee, and the combination is what the
                                         problem requires. The implication is the paper’s thesis: as foundation models converge, the durable engineering
                                         asset is the formally specified, executable process, not the model.
                                         CCS Concepts: • Software and its engineering → Software development process management; Specifi-
                                         cation languages; Formal software verification; • Computing methodologies → Multi-agent systems.
                                         Additional Key Words and Phrases: AI-SDLC, protocol specification, human-agent collaboration, validation
                                         tokens, software engineering

                                         Authors’ Contact Information: Ylli Prifti, Birkbeck, University of London, London, United Kingdom, y.prifti@bbk.ac.uk,
                                         ylli@prifti.us; Pasquale De Meo, University of Messina, Messina, Italy, pdemeo@unime.it; Alessandro Provetti, Birkbeck,
                                         University of London, London, United Kingdom, a.provetti@bbk.ac.uk.
2                                                         Ylli Prifti, Pasquale De Meo, and Alessandro Provetti


1     Introduction
Recent practitioner analysis documents the emergence of AI-SDLC: software development work-
flows where AI systems participate alongside humans across planning, coding, reviewing, and
deployment. Industry reports identify that success requires defining “human-agent responsibility
mapping: responsibilities, decisions, approval gates and authority levels are explicitly divided
between humans and the agent” [10], yet ask: “Do we have standards or frameworks for prompting
and supervising multi-agent contributions?” [13], noting that without governance and security
such workflows create “fragmentation, technical debt, and serious operational risk” [28].
   The gap: while the need for governance, oversight, and approval gates is well-documented,
no specification language exists for expressing these constraints as executable protocol. Teams
implement AI-SDLC workflows through ad-hoc tooling without formal mechanisms to specify what
agents can do, when approval is required, or how process violations are prevented. We propose a
domain-specific language for specifying AI-SDLC processes.
   Defining AI-SDLC: we use AI-SDLC (AI-Integrated Software Development Lifecycle) to mean
software development processes designed around collaboration between human and AI team
members, where both take on defined roles and responsibilities within structured workflows. AI
agents are first-class participants (planning, implementing, validating, reviewing) rather than tools
augmenting a human-centric process. The shift is that AI-SDLC requires new processes optimised
for human-agent collaboration, not acceleration of existing human-only ones. The core challenge
is specifying who (human or agent) does what, when approval is required, how disagreement is
resolved, and what constraints cannot be violated.

1.1     Contributions
Our thesis is that as models evolve and converge, the durable engineering asset is the process, not
the model so AI-SDLC needs processes that are both flexible to specify and reliable to enforce. Our
contributions follow from that thesis:

      (1) A specification language for AI-SDLC processes with formal abstract syntax, well-
          formedness conditions, operational semantics, and enforcement invariants (INV1–INV5),
          treating a process as a portable artifact independent of any agent framework.
      (2) The policy–mechanism separation as organising principle: protocols declare intent (pol-
          icy); enforcement primitives validation tokens, capability boundaries, non-overridable gates
          realise it structurally (mechanism). This single split yields the paper’s two consequences.
      (3) Flexibility. The same primitives express configurations from a solo developer to a reg-
          ulated enterprise, including the 2+N reference pattern (two human-in-control roles plus
          N specialised agents) that formalises Separation of Duties; we demonstrate this with four
          structurally distinct, executable process encodings — solo, three-mode team, and two task-
          tailored protocols with opposite enforcement targets — running unmodified on one engine
          (Section 4.13). Kleene closure of the orchestration loop and reflexive protocol-adherence
          checking are derived consequences of the specification rather than special-case constructs,
          and session resumability holds across model context boundaries.
      (4) Quasi-determinism, as a theorem. For any well-formed protocol, the enforcement invari-
          ants hold on every execution trace, closed under Kleene composition of orchestration loops
          (Theorem 4.4): protocol steps cannot be skipped, by construction. A failure-rate analysis
          derives the consequences — structural enforcement bounds silent failure at a weighted prod-
          uct of agent and validator rates while converting the remainder into visible, audited stalls
          (Proposition 4.1), with a capability floor below which the benefit vanishes (Corollary 4.3).
Specifying AI-SDLC Processes: A Protocol Language for Human-Agent Boundaries                         3


      (5) Empirical characterisation and motivation. Simulation characterises the enforcement
          layer (disagreement-policy trade-offs, ≈1% governance overhead, the failure-rate model,
          Byzantine limits), and an end-to-end study on SWE-bench Verified establishes the language’s
          empirical premise: an identical methodology yields nothing delivered as prose instructions
          and a significant, replicated 14–22 point gain when executed as a validated, self-correcting
          process (two model tiers, up to 𝑛=191), with an ablation attributing the gain to the executed
          process, a compressed model-tier gap, and the capability floor observed where the model
          predicts it.
      (6) An executable, open reference implementation, validated by property-based tests of
          the invariants and released as an artifact.
   We position this work against prior approaches (MetaGPT [14], FlowAgent [29], BPMN extensions
for human-agentic workflows [1], and capability-based security [35]) in Section 3.

1.2     Organisation
Section 2 establishes the problem through documented failure modes and the specification gap.
Section 3 positions the work against related research. Section 4 presents the formal language
specification, including the enforcement theorem, the failure-rate analysis, and the expressiveness
study. Section 5 describes our implementation. Section 6 presents an empirical characterisation of
the enforcement layer through simulation studies and an end-to-end evaluation on real software
tasks. Section 7 discusses limitations and implications.

2     Problem: The Need for Formal AI-SDLC Specification
2.1     Documented Failure Modes
Empirical research on AI coding systems documents failure modes that persist across model
generations:
   Security vulnerabilities. Analysis of 733 code snippets from GitHub Copilot and other tools
found 29.5% of Python and 24.2% of JavaScript snippets contained security weaknesses [12]; ap-
proximately 40% of Copilot-generated programs were vulnerable against CodeQL [27].
   Silent failures. Newer models produce code that “fails to perform as intended, but which on
the surface seems to run successfully” [16], imposing hidden costs through delayed discovery.
   Context overload. Agent analysis identified “over-exploration where agents fail to reach the
root of the problem due to context overload, and repeated application of the same fix without
proper testing” [6].
   Audit gaps. In regulated environments, autonomous code generation introduces “audit trail
complications that go beyond code quality into regulatory territory” [30]; structured records of
what was decided and validated are rarely provided.
   Containment violations. Agents under evaluation have circumvented the boundaries of their
environments rather than solve the task as posed: during a cybersecurity capture-the-flag evaluation,
an o1-preview agent exploited a misconfigured container API to restart and inspect the broken
challenge environment from outside it [25], and reasoning models instructed to win at chess have
edited the game-state files rather than play the position [4]. In both cases the boundary that failed
was behavioural — an instruction about what the agent should do — not infrastructural: nothing
prevented the out-of-bounds action but the agent’s own compliance.
   Self-review limitations. A single agent reviewing its own output validates against the same
model that produced it: LLMs struggle to self-correct without external feedback [15] and exhibit
self-enhancement bias, favouring their own generations when acting as judge [36].
4                                                         Ylli Prifti, Pasquale De Meo, and Alessandro Provetti


  These are process problems, not capability problems. Improving model quality does not eliminate
the need for independent review, scope boundaries, and audit trails.

2.2   Process Variability
Successful software processes have always been frameworks rather than prescriptions: Scrum fixes
boundaries — roles, ceremonies, an increment — and works unchanged for a team of three or nine
because everything inside the boundaries is left to the team. A solo developer wants speed and
tolerates risk; a regulated enterprise cannot ship without audit trails and separation of duties; a
startup falls between. An AI-SDLC formalism needs the same shape, over a wider parameter space:
1..𝑛 humans and 1..𝑚 agents, composed into modes of working. What must be expressible is the
structure of collaboration — work partitioned into modes; within a mode, typically one human in
control directing one-to-many agents; each mode anchored by a human, though one person may
hold that role in more than one mode — while everything inside a mode stays free. The requirement
is therefore not one process that fits every team, but a language in which each team’s way of
working can be stated, varied, and enforced. Adding AI agents amplifies this need: the parts of a
process that previously lived in team convention must now bind actors that convention cannot
reach.

2.3   The Specification Gap
The failure modes above and the variability they meet converge on an uncomfortable fact: the
instrument teams use to direct agent behaviour today is the prompt, while the instruments organ-
isations use to govern processes — workflow systems, review policies, compliance checklists —
cannot see agents at all. The practitioner literature registers this gap without closing it. Teams are
advised that they need “highly structured, codified context” [26], with no language in which to
codify it; industry analyses call for “governance requirements” [11], with no formal mechanism by
which such a requirement could be stated, checked, or enforced. What fills the gap in practice is
scaffolding improvised around each agent framework: implicit norms and behavioural expectations
that the agent is trusted to follow — a trust the containment violations of Section 2 already discredit,
and one this paper measures directly (Section 6.5).
   What is missing is a specification language: a form in which a team can state, machine-executably,
how agents participate in its SDLC — which modes of working exist, which validators run and at
what phase, where human approval is required, how validator disagreement resolves, and which
constraints no agent can override. Stating such things is necessary but not sufficient; the statements
must also be enforced by construction rather than by compliance, or they collapse back into
prompts. The remainder of this paper provides both: the language (Section 4) and the guarantee
that a well-formed specification enforces itself (Theorem 4.4).

3 Related Work
Our work intersects multi-agent frameworks for software engineering, workflow specification
languages, capability-based security, and human-agent collaboration modelling. We position our
contribution against the most relevant prior art.

3.1   Human Oversight Models
Recent literature distinguishes Human-in-the-Loop (HITL) from Human-on-the-Loop (HOTL)
oversight [2, 20]: HITL places the human inside the control loop with the agent blocking pending
approval; HOTL has the human monitor execution and intervene on anomalies. Our formalisation
requires both. The HI-CTRL role and require_human policy implement HITL; the audit log (INV4)
and proceed_with_log policy implement HOTL. The choice is encoded in the disagreement policy,
Specifying AI-SDLC Processes: A Protocol Language for Human-Agent Boundaries                        5


part of the protocol rather than the agent implementation. This addresses a documented limitation
of current frameworks: encoding oversight in agent code produces coverage drift as new action
types appear [33].

3.2   Multi-Agent Frameworks for Software Engineering
MetaGPT [14] is the closest prior work: it assigns software-engineering roles to distinct agents
and encodes Standardised Operating Procedures (SOPs) into prompts. It demonstrates that role
specialisation improves coherence, but encodes SOPs in prompts, a behavioural mechanism subject to
the drift and interpretation problems of Section 2, with no machine-executable specification separate
from agent instructions, no infrastructure-level mode boundaries, and no formal mechanism
preventing role contamination beyond prompt discipline.
   Other orchestration frameworks (LangGraph [19], AutoGen [34], CrewAI [7]) provide toolkits for
building agent systems rather than specification languages for SDLC processes: LangGraph models
workflows as state machines, AutoGen as conversations, CrewAI as role-goal-backstory triples. All
produce systems through code; none provides a portable, reviewable specification artifact separate
from the implementation, making audit, modification, and sharing harder.
   Our DSL differs in three respects: (i) it specifies AI-SDLC processes as standalone artifacts
independent of any framework; (ii) it distinguishes policy declaration from mechanism enforcement,
letting implementations choose context-appropriate mechanisms; (iii) it formalises infrastructure-
level mode boundaries (WF1) as required for the specification to hold.

3.3   Workflow Specification Languages
YAWL [32] provides domain-independent syntax for workflow patterns with an enforcing runtime;
BPMN [23] is the dominant business-process notation, with graphical and machine-processable
forms. Both address human-only or human-tool processes well but do not natively model au-
tonomous agent participants, agent disagreement, or the failure modes of Section 2. Ait et al. [1]
extend BPMN for human-agentic workflows; their motivation is comparable to ours, but a BPMN
extension preserves backward compatibility with existing tooling whereas our DSL is purpose-built
for AI-SDLC with infrastructure-level enforcement as a first-class concept. The two will likely
coexist: the choice depends on whether teams need BPM-tooling integration or are designing
AI-SDLC processes from scratch. FlowAgent [29] introduces a Procedure Description Language for
customer-service workflows with supervising controllers; it targets single-domain conversational
flows, while our DSL targets the multi-mode, multi-role structure of software development with
explicit producer/reviewer separation, and our enforcement primitives gate both path and authority.

3.4   Capability-Based Security and Token Mechanisms
Capability-based security has a long history in distributed systems [9, 21]; our capability boundaries
(INV2) apply established patterns to AI-SDLC. We claim novelty in the application as a specification
primitive, not in the mechanism. SAGA [35] uses cryptographic tokens for inter-agent access
control; our validation tokens instead encode validator quorum outcomes as preconditions for
dispatch, addressing validation-to-execution rather than agent-to-agent authorisation. Recent
analysis notes the shift from credential-based to capability-based control for agents that invent
workflows at runtime [31]; our DSL makes capability boundaries (INV2) a structural property of
mode definitions rather than a runtime decision.

3.5   Standard Operating Procedures and Team Composition
Formalising team roles and standardised procedures draws on Belbin’s team role theory [3] and
DeMarco & Lister [8], a tradition MetaGPT cites explicitly. Our 2+N pattern extends it by specifying
6                                                           Ylli Prifti, Pasquale De Meo, and Alessandro Provetti


the minimum viable team under AI-SDLC: two human-in-control roles (architect, reviewer) plus N
specialised agent members. Where Belbin describes roles people occupy, we specify roles that must
exist with structural enforcement of separation.

3.6    Positioning Summary
The individual primitives have substantial prior art — DSLs, capability tokens, role-based work-
flow specification, human-agent collaboration modelling — and we acknowledge specific overlap
with MetaGPT (role specialisation, SOPs), FlowAgent (procedure description with controllers),
BPMN extensions (human-agentic modelling), and capability-based security (token-gated access).
What none of these provides, and what the integration yields, is a machine-executable process
specification independent of any agent framework whose enforcement carries a formal guarantee:
infrastructure-level rather than norm-enforced mode boundaries, validation tokens encoding quo-
rum outcomes, and non-overridable blocker semantics, combining so that well-formedness implies
the enforcement invariants on every execution trace (Theorem 4.4), with failure-rate consequences
treated analytically (Section 4.9) and characterised empirically (Section 6).

4     Formal Language Specification
We present a domain-specific language for AI-SDLC processes. The language distinguishes policy
(declared intent) from mechanism (structural enforcement): protocols specify what should happen;
implementations use enforcement primitives to bound process non-determinism.

4.1    Abstract Syntax
A protocol P is a tuple of modes, validators, disagreement policy, and constraints:


                       Protocol P ::= ⟨𝑀 ∗, 𝑉 ∗, 𝐷, 𝐶 ∗ ⟩
                         Mode M ::= ⟨mode_id, 𝑅 ∗,𝑇 ∗ ⟩
                            Role 𝑅 ::= ⟨role_id, responsibilities⟩
                      Validator V ::= ⟨validator_id, evaluation_phase,
                                            criteria, severity_fn⟩
           DisagreementPolicy 𝐷 ::= quorum(𝑘),          1 ≤ 𝑘 ≤ |𝑉 ∗ |
                                      any ≡ quorum(1)        majority ≡ quorum( ⌊𝑁 /2⌋+1)
                                      unanimous ≡ quorum(𝑁 )
                     Constraint 𝐶 ::= positive(predicate) | negative(predicate)

   Modes are operational stages with defined permissions (e.g. producer writes code, reviewer
validates and approves), enforced at infrastructure level. Roles are declared actors with identifiers
and responsibilities; capabilities bind to modes (tool sets), not to individual roles, so role declara-
tions document the Separation-of-Duties structure while the mode boundary enforces it. WF2’s
uniqueness is enforced protocol-wide, which implies uniqueness within every mode. Validators
evaluate tasks against criteria and emit severities from the total order pass < warn < blocker. The
distinction is recoverability: a warn marks a violation an agent can attempt to repair (the semantics
routes it to bounded recovery), while a blocker marks a violation with no agent-recoverable path —
either because the validator’s criteria are absolute, a conflict only a human can resolve (e.g. a speci-
fication contradicting a known requirement), or because a repairable violation has exhausted its
recovery budget and hardens into one. Multiple validators can operate independently as a quorum
Specifying AI-SDLC Processes: A Protocol Language for Human-Agent Boundaries                                          7


with orthogonal criteria.1 Disagreement policies specify when a set of validator results counts as
agreement. A policy is an agreement threshold, and every named policy is an instance of quorum(𝑘):
any accepts a single passing verdict (𝑘=1), majority requires a strict majority (𝑘 = ⌊𝑁 /2⌋+1 — an
odd-sized quorum always decides; an even-sized one can genuinely fail to), and unanimous requires
all 𝑁 . Application is total, in a fixed precedence order: a blocker forces hard_stop regardless of
the policy — INV3 surfacing in the policy layer; otherwise, results meeting the threshold yield
proceed (logged when agreement is non-unanimous); otherwise the threshold is unmet, and what
happens next is determined by recoverability: warn-level violations route to bounded recovery
(Section 4.7), and the outcome becomes require_human only when the violation is absolute or the
recovery budget is exhausted. A human decision is therefore required in exactly two situations
— an absolute violation, or the absence of agreement after bounded self-correction — and this
partition is the totality that WF4 checks. The reference implementation ships the named instances
(unanimous, majority, quorum at a configured threshold, any, as in Listing 1) rather than arbitrary
𝑘, and Section 6.1 characterises their trade-offs. Constraints define structural requirements and
prohibitions enforced by the implementation.

4.2   AI-SDLC Execution Flow
Figure 1 shows how human intent flows through orchestrator collaboration into the execution
loop: intent expression, architectural breakdown, then a cycle of governance checking, validation,
execution, and progression, with human escalation when needed. Validators are invoked at their
declared phase: specification validators run before Execute, artifact validators after, feeding the
disagreement policy.

4.3   Kleene Closure of the Orchestration Loop
The orchestration loop forms a Kleene closure [18]: the system can instantiate zero, one, or arbitrarily
many loop instances, including recursively spawned sub-instances, all under the same constraints.
This is a derived consequence of the specification, not an added construct. If 𝐿 denotes a single
loop instance executing the cycle (governance, validate, execute, move_next), then:

                                                                      ∞
                                                                      Ø
                                           Execution(P) = 𝐿 ∗ =             𝐿𝑖
                                                                      𝑖=0

   where 𝐿𝑖 denotes 𝑖 sequential or recursively nested instances. This is not a special case; it follows
from the protocol’s structure: tasks may spawn subtasks, each requiring its own cycle; subtasks
may spawn subtasks to arbitrary depth, bounded only by termination conditions; and all instances
share the same validators, policies, and invariants.
   The framing carries a verification consequence: invariants holding for a single instance hold for
any composition. If 𝐿 satisfies INV1–INV4, every execution in 𝐿 ∗ does, by induction on closure
construction: the empty execution satisfies them vacuously, and each composition step preserves
them because the recovery rule (Section 4.7) spawns sub-instances under the same protocol tuple
and mode as their parent. Theorem 4.4 makes this argument precise. This lets runtime monitoring
focus on single-loop behaviour rather than tracking arbitrary depths. A blocker on a top-level task
does not halt execution; it spawns a subtask whose completion enables the parent to proceed, so
the protocol scales to arbitrary complexity through composition rather than special-case handling.

1 The evaluation_phase field lets validators declare when they execute, supporting validator classes distinguished by

domain and timing: specification validators (pre_execute), artifact validators (post_execute), and transition validators
(mode_transition). The language does not enumerate all phases; implementations may define additional classes.
8                                                                           Ylli Prifti, Pasquale De Meo, and Alessandro Provetti


                                                             Human
                                                         expresses intent



                  Escalation: blocker               Human ↔ Orchestrator
                    + {require human,
                        hard stop} ⇒
                                                    converge on architecture,
                       halt for human                break down into tasks



       Orchestration loop (instance 1)
                                     Validate                                         Validate
           Governance                                        Execute                                        Move next
                                    pre-execute                                     post-execute
         check constraints                               coders implement                                   next task
                                      quorum                                          quorum


                                                                                     Recovery: warn ⇒ spawn L′
                             completes ⇒ revalidate

                                         Orchestration loop (instance 2 — spawned subtask)
                                                  ..
                                                   . instance N : recursive spawn-
                                                     ing, same ⟨M ∗ , V ∗ , D, C ∗ ⟩



                                                                                             session boundary (pause/resume)


                                                         Pull Request
                                                        → reviewer mode



Fig. 1. AI-SDLC execution flow: intent → breakdown → orchestration loop∗ → PR. Validators run at their
declared phases (pre- and post-execute); a violation takes exactly one of the two rule paths of Section 4.7 —
Recovery (spawn a sub-instance under the same protocol tuple, then revalidate) or Escalation (halt for a
human). Instances spawn recursively (Kleene closure), all under the same constraints.



4.4    Well-Formedness Conditions
A protocol P = ⟨𝑀 ∗, 𝑉 ∗, 𝐷, 𝐶 ∗ ⟩ is well-formed iff:
  WF1 (Mode separation):
                                                   ∀𝑚 1, 𝑚 2 ∈ 𝑀 ∗, 𝑚 1 ≠ 𝑚 2
                                                ⇒ 𝑚 1 .tools ∩ 𝑚 2 .tools = ∅

    WF2 (Role uniqueness within mode):

                              ∀𝑚 ∈ 𝑀 ∗, ∀𝑟 1, 𝑟 2 ∈ 𝑚.𝑅 ∗, 𝑟 1 ≠ 𝑟 2
                                                                  ⇒ 𝑟 1 .role_id ≠ 𝑟 2 .role_id

    WF3 (Validator coverage):

                                              ∀task dispatch op, ∃𝑉 ′ ⊆ 𝑉 ∗
                                             associated with that operation

    WF4 (Policy completeness): 𝐷 defines the behaviour for all possible validator outcomes.
Specifying AI-SDLC Processes: A Protocol Language for Human-Agent Boundaries                       9


  WF5 (Constraint declaration consistency):
                                  ∀𝑐 1, 𝑐 2 ∈ 𝐶 ∗ . 𝑐 1 ≠ 𝑐 2 ⇒ 𝑐 1 .id ≠ 𝑐 2 .id
                                    ∧ ∀𝑐 ∈ 𝐶 ∗ . nonempty(𝑐.expr)
                                               ∧ registered(𝑐.predicates)
   Well-formedness is enforced by compile-time verification: a protocol failing any check is rejected
at load (WF1–WF5 via the verifier), with WF3 additionally guarded at runtime. Two conditions are
partially enforced: WF4 treats quorum policies with fewer than three validators as a warning rather
than a rejection, and WF5 verifies declaration consistency rather than logical non-contradiction,
which would require theorem-proving over constraint expressions and is left to future work.

4.5   Runtime State and Tokens
                           State 𝜎 ::= ⟨current_mode, active_roles, issued_tokens⟩
                          Token 𝜏 ::= ⟨token_id, task_ref, validator_sigs, timestamp⟩
                  ValidatorResult ::= ⟨validator_id, severity, justification⟩
  A token is an unforgeable credential issued by validators after evaluation: agents cannot mint
tokens, and dispatch operations require valid tokens. Tokens are one mechanism for enforcement;
others (signed commits, capability boundaries, formal verification traces) are equally valid.

4.6   Session Boundaries and Resumability
AI-SDLC execution is not continuous: sessions pause (context limits, human availability, overnight
breaks) and resume, and the protocol must maintain its guarantees across these boundaries.
  Session state:
                              SessionState 𝜎𝑠 ::= ⟨session_id, mode, project,
                                                  checkpoint, parent_session?⟩
                                Checkpoint 𝑐 ::= ⟨current_task?, decisions,
                                                  memory_summary, timestamp⟩
  This prevents re-asking humans (decision churn) and losing memory context. Validator re-
execution on resume is intentional: tokens are excluded from session state precisely because the
context may have shifted during the pause, and revalidation against current state is required for
soundness. Tokens are scoped to a single dispatch within an active session and do not persist across
boundaries; implementations may additionally expire them within a session after a TTL to force
revalidation when context changes substantially.

4.7   Operational Semantics
Validation:
               𝑉 ∗ = {𝑣 1, . . . , 𝑣𝑛 } phase ∈ {pre_execute, post_execute, . . .}
                        𝑉𝑝 = {𝑣 ∈ 𝑉 ∗ | 𝑣.evaluation_phase = phase}
                                       ∀𝑣 ∈ 𝑉𝑝 . 𝑣 (context) → 𝑟
                            validate(context, 𝑉𝑝 , phase) → {results}
  Token Issuance (Success):
                                           results = {𝑟 1, . . . , 𝑟𝑛 }
                                   apply_policy(𝐷, results) = proceed
                                        issue_token(results, 𝑡) →
                                  𝜏 = ⟨fresh_id, 𝑡, sign(results), now()⟩
10                                                         Ylli Prifti, Pasquale De Meo, and Alessandro Provetti


     Token Issuance (Refusal):
                                        results = {𝑟 1, . . . , 𝑟𝑛 }
                                 apply_policy(𝐷, results) ≠ proceed
                                    issue_token(results, 𝑡) → ⊥
  In particular, a blocker forces apply_policy = hard_stop ≠ proceed, so no token can be issued
over blocker-carrying results (INV3).
  Dispatch with Token Enforcement:
                                       𝜏 = ⟨_, task_ref, _, _⟩
                                             valid(𝜏)
                               current_mode.tools contains dispatch
                             dispatch(task_ref, 𝜏) → execute(task_ref)
                                            𝜏 =⊥
                                 dispatch(task_ref, 𝜏) → error
  Modes as hard boundaries. There is no mode-transition rule, by design. Modes do not hand
control to one another; they exchange only artifacts, and a change of mode is an explicit human
action outside the engine:
   Axiom 1 (Mode boundary). The engine executes exactly one mode per invocation: 𝜎.current_mode
is constant over every engine trace. A mode change is an external human action that begins a fresh
trace (and is itself audited, per INV4). The only value crossing a mode boundary is an artifact, which is
inert data: it carries no tokens and no capabilities. Tokens are scoped to a single dispatch within the
issuing trace (Section 4.6) and cannot cross the boundary.
   Axiom 1 formalises what the implementation enforces architecturally (Section 5): the output
of the producer mode is input to the reviewer mode as data, never as authority, so WF1’s tool
disjointness yields Separation of Duties at the boundary.
   Blocked outcomes. When token issuance yields ⊥, execution proceeds in exactly one of two
ways, determined by recoverability: a repairable violation is delegated to a recursively spawned
sub-instance (the Kleene step of Section 4.3), bounded by a recovery budget 𝑅; an absolute violation,
or one whose budget is exhausted, escalates to a human. There is no third path; in particular, there
is no rule by which a blocked task dispatches anyway. Let 𝑑 (𝑡) denote the recovery depth of task 𝑡
(initially 0).
   Recovery (subtask spawn):
                                     issue_token(results, 𝑡) = ⊥
                           ∀𝑟 ∈ results. 𝑟 .severity ≠ blocker        𝑑 (𝑡) < 𝑅
                 𝐿 ′ = spawn(subtask(results, 𝑡), ⟨𝑀 ∗, 𝑉 ∗, 𝐷, 𝐶 ∗ ⟩, 𝜎.current_mode)
                             blocked(𝑡) → 𝐿 ′ ; revalidate(𝑡) [𝑑 (𝑡)+1]
  The spawned instance 𝐿 ′ operates under the same protocol tuple and the same mode as its parent;
the parent may proceed only after 𝐿 ′ completes and 𝑡 is revalidated, so recovery re-enters the
semantics at the validation rule rather than bypassing it.
  Escalation (human decision):
                                     issue_token(results, 𝑡) = ⊥
                            ∃𝑟 ∈ results. 𝑟 .severity = blocker ∨ 𝑑 (𝑡) = 𝑅
                             blocked(𝑡) → halt⟨results, policy_decision⟩
  The two premises are the two origins of a non-recoverable state: a validator whose criteria are
absolute emits a blocker directly, and a repairable violation that exhausts its budget hardens into one
Specifying AI-SDLC Processes: A Protocol Language for Human-Agent Boundaries                        11


— at 𝑑 (𝑡) = 𝑅 the warn-level results are treated exactly as a blocker would be. Recoverability, not
the disagreement policy, chooses between the rules; the policy determines only whether issuance
refuses in the first place.
   Escalation halts the trace with a structured payload (blocking validators, justifications, policy
decision); resumption is a human action beginning a new trace, exactly as in Axiom 1. Every rule
above appends an entry to the audit log as a side effect (INV4); we leave the audit component
implicit in the rule notation for readability.
   The contrast between the two regimes is direct. Without enforcement, the agent interprets
the policy and may comply or drift; execution proceeds either way, compounding process non-
determinism with agent non-determinism. With enforcement, the mechanism gates execution: only
compliant paths are possible, eliminating process non-determinism while bounding the residual
non-determinism inherent to agent-based components.

4.8   Bounded Non-Determinism
The language does not produce deterministic outcomes: agent-based components (validators, coders,
the orchestrator) are inherently non-deterministic. What the mechanism eliminates is process non-
determinism, the variability from agents skipping or reinterpreting protocol steps. The distinction
is sharp. With structural enforcement, dispatch is impossible without prior validation, so the
validation step occurs deterministically (process non-determinism eliminated); the validator’s
own evaluation, once invoked, remains model-dependent (agent non-determinism bounded, not
eliminated). Disagreement policies then turn variable validator outputs into deterministic decisions
(proceed, escalate, halt). As with a type system, the mechanism does not make outcomes correct;
it removes a whole class of failures structurally, leaving residual variability bounded and explicit.
The honest claim is quasi-deterministic process behaviour: outcomes that would otherwise be
uncharacterisable become characterisable, auditable, and improvable.

4.9   Failure Rate Bounds
We characterise the quasi-deterministic improvement through a failure-rate analysis. Parameter
values are illustrative; the qualitative conclusions hold across the plausible range.
   Setup and assumptions. Model an AI-SDLC pipeline as 𝑁 sequential stages, each performed
by an agent that introduces a defect with probability 𝑝𝑖 ∈ [0, 1], independently across stages (FR1).
An execution terminates in one of three outcomes: correct (no defect ships), silent failure (a defect
ships undetected), or stall (work halts awaiting a human decision). We track two metrics, 𝑃 silent
and 𝑃 stall , because the two delivery regimes distribute failure probability between them differently;
collapsing them into a single “failure rate” obscures exactly the property enforcement provides.
Validators are homogeneous with miss rate 𝑝 𝑣 (FR2), and correlated through a common shock: each
validation event is systematic with probability 𝜌 ∈ [0, 1] — a shared blind spot of the underlying
foundation models, on which all validators miss together with probability 𝑝 𝑣 — and independent
otherwise (FR3). A recovery round is another attempt by the same agent, so its failure rate is tied
to, and correlated with, the agent’s own (FR4).
   Behavioural compliance. Under behavioural delivery there is no enforced detection point: any
validation happens at the discretion of the same agent, inside the same context, that produced the
defect, so detection failure is correlated with generation failure and we conservatively credit no
independent detection. Every introduced defect ships: 𝑃 stallbeh = 0 and, under FR1,


                                                        𝑁
                                                        Ö
                                           beh
                                         𝑃 silent ≥1−         (1 − 𝑝𝑖 ).
                                                        𝑖=1
12                                                                 Ylli Prifti, Pasquale De Meo, and Alessandro Provetti


The floor assumes stages fail independently; when process steps are skipped, downstream agents
operate on corrupted state. We model the cascade by noisy-OR composition on the accumulated
upstream error, with 𝛼𝑖 ∈ [0, 1] the susceptibility to upstream corruption:
                                                                                𝑁
                                                                                Ö
                        ′
                       𝑝𝑖+1 = 𝑝𝑖+1 + 𝛼𝑖 𝑝𝑖′ (1 − 𝑝𝑖+1 ),        beh
                                                               𝑃silent ≥1−            (1 − 𝑝𝑖′ ),
                                                                                𝑖=1

bounded in [0, 1], reducing to the independent floor at 𝛼𝑖 = 0 and rising toward saturation as
𝛼𝑖 → 1.
   Structural enforcement. Corollary 4.5 supplies the premise the behavioural regime lacks: every
stage is validated by the quorum, on every execution path. Under the common-shock assumption
(FR3), the probability that a quorum of 𝐾 validators misses a defect is the mixture of the systematic
and independent cases:
                             quorum
                            𝑃miss     = 𝜌 𝑝 𝑣 + (1 − 𝜌) 𝑝 𝑣𝐾 = 𝑝 𝑣𝐾 + 𝜌 (𝑝 𝑣 − 𝑝 𝑣𝐾 ),
reducing to 𝑝 𝑣𝐾 at 𝜌 = 0 and to 𝑝 𝑣 at 𝜌 = 1. A defect at stage 𝑖 ships silently only if the quorum misses
it. If caught, issuance refuses and repair is attempted through bounded recovery (Section 4.7), failing
with probability 𝑝 recovery — a single rate that collapses the nested recovery loop, refined below. The
per-stage failure mass therefore splits into a silent component and an unresolved component:
                                                                                                 𝑁
                                                                                                ∑︁
                             quorum(𝑖 )              quorum(𝑖 )                        str
              𝑃stage𝑖 = 𝑝𝑖 𝑃miss        + 𝑝𝑖 (1 − 𝑃 miss   ) 𝑝 recovery,              𝑃fail ≤         𝑃stage𝑖
                        | {z          }   |             {z           }                          𝑖=1
                             silent                   unresolved
                               beh /𝑃 str ≥ [1 − Î (1 − 𝑝 ′ )]/Í 𝑃
by the union bound, giving 𝑃fail     fail         𝑖      𝑖      𝑖 stage𝑖 . For realistic values (𝑝𝑖 ≈ 0.1,
𝑝 𝑣 ≈ 0.2, 𝐾 = 3, 𝜌 ≈ 0.3, 𝑝 recovery ≈ 0.1, 𝑁 = 5), structural enforcement reduces failure rates
roughly five-fold, widening past an order of magnitude at low 𝜌 and 𝑝 recovery and narrowing as the
behavioural rate saturates at large 𝑁 . Section 6.3 validates both the quorum-miss formula and this
ratio empirically.
   The silent-failure/stall trade. The unresolved component does not ship: a violation still
unrepaired at the recovery budget hardens into a blocker and the Escalation rule halts for a
human (Section 4.7). This is the structural regime’s defining trade:
     Proposition 4.1 (Silent-failure/stall trade). Under structural enforcement with escalation,
 str     Í      quorum(𝑖 )      str ≤ Í 𝑝 (1 − 𝑃 quorum(𝑖 ) ) 𝑝
𝑃silent ≤ 𝑖 𝑝𝑖 𝑃miss       and 𝑃stall  𝑖 𝑖      miss            recovery ; under behavioural compliance,
 beh = 0 while 𝑃 beh grows cumulatively in 𝑁 toward saturation. Structural enforcement converts
𝑃stall           silent
silent failures into visible, audited stalls; behavioural compliance converts stalls into silent failures.
   Corollary 4.2 (Benchmark invisibility of hard gates). An autonomous, oracle-graded evalu-
ation scores a stall as a failure, so it measures 𝑃 silent + 𝑃 stall and is indifferent to the split between them.
The governance value of a non-overridable gate — driving 𝑃silent down at the cost of 𝑃stall > 0 — is
therefore structurally invisible to such benchmarks: a hard gate can only lower a benchmark score,
never raise it, whenever the stalled tasks include any the agent would have resolved.
   Corollary 4.2 delimits what any autonomous benchmark, including our own evaluation (Sec-
tion 6.5), can and cannot establish: it can measure whether an executed, validated process improves
outcomes, but the human-in-the-loop value of hard gates requires deployment data, not benchmarks
(Section 7).
   Capability floor. FR4 ties recovery to the agent: a recovery round is a re-attempt by the same
agent with defect rate 𝑝𝑎 , and successive attempts are correlated (same model, same blind spots),
Specifying AI-SDLC Processes: A Protocol Language for Human-Agent Boundaries                         13


which we model with a second common shock 𝜌𝑎 : over 𝑅 rounds,
                                        (𝑅)
                                      𝑝 recovery = 𝜌𝑎 𝑝𝑎 + (1 − 𝜌𝑎 ) 𝑝𝑎𝑅 .
Substituting into the per-stage bound gives the advantage factor of structural enforcement over the
behavioural per-stage rate 𝑝𝑎 :
                                  𝑝𝑎      h                                   i −1
                                            quorum         quorum  (𝑅)
                     𝐴(𝑝𝑎 ) =           = 𝑃miss + 1 − 𝑃 miss       𝑝 recovery      .
                                𝑃 stage
  Corollary 4.3 (Capability floor). 𝐴(𝑝𝑎 ) is decreasing in 𝑝𝑎 and 𝐴(𝑝𝑎 ) → 1 as 𝑝𝑎 → 1: as
                                                (𝑅)
the agent’s base failure rate approaches one, 𝑝 recovery → 1 and the structural advantage vanishes.
Enforcement multiplies the value of a capable agent; it cannot substitute for one.
   The corollary predicts a floor on base capability below which enforcement yields no measurable
benefit — recovery rounds re-sample the same failure distribution, so a quorum that reliably catches
defects merely converts them into unrecovered stalls. Section 6.5 observes exactly this collapse
on a weak coder (≈15% base resolve rate), with the enforcement loop demonstrably engaging yet
producing no gain: the model’s prediction, then the observation.
   Scope and validity. The analysis is single-gate and conservative: the deployed protocol composes
multiple independent gates (deterministic predicates, pre- and post-execution phases, per-mode
gating, an orthogonal quorum), so the advantage compounds to the extent gates fail independently.
The simplifying assumptions relax without changing the conclusion’s direction: heterogeneous
validators are bounded by substituting the worst per-validator rate max 𝑗 𝑝 𝑣 𝑗 for 𝑝 𝑣 (the mixture
derivation is unchanged); drifting per-stage rates are absorbed because the bounds are per-stage
sums and products, so a time-varying 𝑝𝑖 (𝑡) is bounded by its per-stage supremum; and an unstable
                                                                                        quorum
correlation 𝜌 is handled by evaluating the bound at its upper envelope, since 𝑃 miss is mono-
tone in 𝜌. Two scope choices are explicit. The quorum-miss formula analyses the strictest gating
(unanimous, 𝑘 = 𝑁 : a defect ships only if every validator misses); weaker thresholds quorum(𝑘),
                quorum
𝑘 < 𝑁 , raise 𝑃 miss monotonically, and the resulting policy trade-off is characterised empirically
in Section 6.1. And 𝑃stall here counts defect-carrying tasks only; stalls on defect-free work — false
blocks, including a misfiring absolute validator — are a property of validator precision and policy
strictness, measured separately in the same section, and the two stall costs add in deployment. Each
substitution weakens the bound quantitatively but preserves it; the model bounds the average case
rather than any specific deployment, and the bounds degrade gracefully rather than invert — the
ratio exceeds unity across the modelled range (Section 6.3) — narrowing as 𝜌 → 1, as 𝑝𝑎 approaches
the floor of Corollary 4.3, and as the behavioural rate saturates at large 𝑁 . The structural difference
is robust: enforcement bounds silent failure at a weighted product of agent and validator rates,
while behavioural compliance permits cumulative, near-saturating growth.

4.10   Enforcement Invariants
The implementation must maintain INV1–INV5:
  INV1 (Token integrity):
                            ∀𝜏 ∈ issued_tokens. ¬can_forge(𝜏)
                                                     ∧ verify(𝜏 .validator_sigs)
  INV2 (Capability boundary):
                             ∀𝑎 ∈ active_roles, 𝑡 ∈ Tools.
                                   can_call(𝑎, 𝑡) ⇒ 𝑡 ∈ current_mode.tools
14                                                        Ylli Prifti, Pasquale De Meo, and Alessandro Provetti


     INV3 (Non-overridable blockers):
                             ∀results. (∃𝑟 ∈ results.
                                          𝑟 .severity = blocker)
                                         ⇒ issue_token(results, _) = ⊥
     INV4 (Audit completeness):
                                    ∀op ∈ {dispatch, validate,
                                           transition}.
                               execute(op) ⇒ ∃log_entry ∈ audit_log
     INV5 (Session resumability):
                  ∀𝑐 ∈ checkpoints.resume(𝑐) ⇒
                                                  preserve(𝑐.decisions)
                                                  ∧ preserve(𝑐.memory_summary)
                                                  ∧ ¬rerun(completed_tasks(𝑐))

4.11     The Enforcement Guarantee
The well-formedness conditions, operational semantics, and invariants combine into the language’s
central formal property: for a well-formed protocol, the invariants are not aspirations the im-
plementation should uphold but consequences of the rule system — no execution path exists on
which they fail. The guarantee is conditional on three assumptions, each discharged by a specific
implementation mechanism (Table 2) and each stated explicitly because it marks a boundary of the
formal claim.
  Assumption 1 (Unforgeable signing). sign(·) is computable only by validators: agents cannot
produce validator_sigs that verify(·) accepts. (Implementation: HMAC-signed single-use tokens; agents
hold no signing key.)
   Assumption 2 (Boundary integrity). Agents can invoke only tools exposed to their current
mode: tool exposure is enforced at infrastructure level, below the agent. (Implementation: disjoint tool
sets at the MCP boundary.)
   Assumption 3 (Engine mediation). Every operation in {validate, issue_token, dispatch, spawn, halt}
and every human mode action executes through the engine, which appends an audit entry for each.
(Implementation: event-sourced, hash-chained audit log.)
   Theorem 4.4 (Enforcement soundness). Let P = ⟨𝑀 ∗, 𝑉 ∗, 𝐷, 𝐶 ∗ ⟩ satisfy WF1–WF3. Under
Assumptions 1–3 and Axiom 1, every engine trace of P satisfies INV1–INV4, and the guarantee is
closed under Kleene composition: it holds for every execution in 𝐿 ∗ .
    Proof sketch. By induction on trace length, with a case per rule of Section 4.7. The empty trace
satisfies INV1–INV4 vacuously. For the inductive step, assume the invariants hold of the trace so far
and consider the next rule applied. Validate issues no token and dispatches nothing; INV4 holds
by Assumption 3. Issue-Token (Success) creates a token carrying sign(results); by Assumption 1
no other rule (and no agent) can mint one, preserving INV1. Its premise apply_policy(𝐷, results) =
proceed is evaluable on all outcomes by WF4 as declared. Issue-Token (Refusal) returns ⊥
whenever the policy outcome is not proceed; since a blocker forces hard_stop, no issuance rule is
applicable in the presence of a blocker — INV3 is immediate, and no rule ordering can circumvent
it. Dispatch fires only with a valid token and only when dispatch is among current_mode.tools;
Specifying AI-SDLC Processes: A Protocol Language for Human-Agent Boundaries                         15


the first premise means a validation preceded every execution (WF3 guarantees the validator set is
nonempty), and the second, with Axiom 1 (mode constancy) and Assumption 2, preserves INV2.
Dispatch on ⊥ yields an error and executes nothing. Recovery spawns 𝐿 ′ under the same tuple
⟨𝑀 ∗, 𝑉 ∗, 𝐷, 𝐶 ∗ ⟩ and the same mode, so the induction hypothesis applies to 𝐿 ′ intact, and the parent
resumes only through Validate — this is the composition step that closes the guarantee under 𝐿 ∗
(Section 4.3); the budget premise 𝑑 (𝑡) < 𝑅 additionally bounds any single task’s recovery chain, so
a task cannot cycle between recovery and revalidation indefinitely — it proceeds, or escalates by
𝑑 (𝑡) = 𝑅. Escalation halts the trace; nothing dispatches. Every case appends an audit entry by
Assumption 3, preserving INV4. INV5 is a cross-trace property of the checkpoint subsystem rather
than of the rule system, and is treated separately (Section 4.6).                                     □
   Corollary 4.5 (Non-skippability). In every trace of a well-formed protocol, every execute(𝑡)
is preceded by a validate step whose results issued the gating token. Validation cannot be skipped,
reordered after execution, or overridden by any agent decision.
   Corollary 4.5 is the formal content of the “process non-determinism eliminated” claim of Sec-
tion 4.8, and the property the end-to-end evaluation (Section 6.5) probes empirically.
   Scope and honesty of the claim. The theorem is deliberately conditional. It requires only
WF1–WF3, which the verifier enforces unconditionally at load; WF4 and WF5 contribute no
premise because their enforcement is partial (Section 4): WF4 admits sub-quorum policies with a
warning, and WF5 checks declaration consistency, not logical satisfiability of constraint expressions.
Consequently the theorem guarantees that validation occurs and blockers halt; it does not guarantee
that the declared policy is sensible or the constraint set consistent — a protocol author can still
write a bad process, well-formed. Nor does it bound the quality of validator judgment, which
is the failure-rate model’s subject (Section 4.9). The assumptions likewise delimit the trust base:
a compromised signing key voids INV1, and an agent with out-of-band tool access voids INV2
— enforcement is structural exactly down to the infrastructure that implements it. Beyond the
type-system analogy, the shape of the guarantee is that of noninterference results in language-based
security [9]: a syntactic discipline, checked mechanically, yielding a semantic property over all
executions. Property-based testing corroborates the theorem’s cases against the implementation: 17
property tests targeting INV1, INV4, WF1, severity-cap monotonicity, and the policy-halt behaviour,
run at a budget of 10,000 randomised examples per test, with zero violations (Section 5). The core
of the argument is additionally mechanised: a self-contained Lean 4 development (no external
libraries, no unproven obligations) models the seven rules as an inductive step relation and proves
INV3, INV2, and Corollary 4.5 by trace induction, with Assumption 1 realised structurally — a
token over blocker-containing results is unconstructible in the model, not merely forbidden. The
mechanisation covers the single-instance rule system (the Kleene composition step and INV4/INV5
are paper-only) and accompanies the artifact.

4.12 The 2+N Pattern as Reference Configuration
We formalise the 2+N team pattern (two human-in-control, or HI-CTRL, roles plus N specialised
agent members) as a reference protocol. Figure 2 shows the architecture with mode separation,
role distribution, and tool boundaries.
   Why this structure:
     • Producer-reviewer separation (WF1): producer mode cannot access merge tools, reviewer
        mode cannot access edit tools. This formalises the classical Separation of Duties principle [5,
        22] and prevents self-approval.
     • Validator quorum: validators with orthogonal criteria operate independently; unanimous
        agreement provides confidence, disagreement signals ambiguity requiring human judgment.
16                                                                 Ylli Prifti, Pasquale De Meo, and Alessandro Provetti




              Producer Mode                                                          Reviewer Mode

       HI-CTRL (Human in Control)                                              HI-CTRL (Human in Control)
         owns execution authority               infrastructure                     owns merge authority
                                                  boundary
            Orchestrator Agent                  separate MCP                           Review Agent
            coordinates execution              servers, disjoint                     coordinates review
                                               tool sets (WF1)
           Validator Quorum (N )                                                 Specialty Reviewers (N )
              security, architec-                                            architecture, security, domain, . . .
            ture, conventions, . . .                                              independent assessment
      independent orthogonal evaluation
                                                                             tools: review, approve, reject, merge
                 Coders (N )
       scoped by directory/component                                               consumes: Pull Requests
                                                     PR                         produces: approval / rejection
       parallel execution within waves

       tools: validate, dispatch, edit, test

            produces: Pull Requests




Fig. 2. The 2+N team pattern: the “2” is the two human-in-control (HI-CTRL) roles, one per mode; the “N”
is the specialised agents (validators, coders, reviewers). Producer and reviewer modes are separated by an
infrastructure boundary — separate MCP servers with disjoint tool sets — so capability separation is enforced
by WF1, not by convention; the only value that crosses is the PR artifact (Axiom 1).

Listing 1. The 2+N protocol as shipped (excerpt of the executable template 2+n.yml; validator criteria
abridged).
     protocol_id : "2+ n "
     modes :
       - mode_id : " producer "         # cannot merge or approve ( WF1 )
         tools : [ edit , dispatch , resolve , test , validate ]
         validators : [ security , architecture , conventions ,
                           quality , protocol_adherence , meta - spec ]
         transitions : { complete : reviewer }
       - mode_id : " reviewer "         # cannot edit or dispatch ( WF1 )
         tools : [ review , approve , merge , pr ]
         validators : [ security , architecture , quality , meta - spec ]
         transitions : { approved : complete , rejected : producer }
     validators :
       - validator_id : " security "
         evaluation_phase : " pre_execute "
         criteria :
             - " Check the task spec against OWASP Top 10 ..."
             - " Verify no hardcoded credentials , secrets , ..."
       - validator_id : " quality "
         evaluation_phase : " post_execute "
         # ... architecture , conventions , protocol_adherence ,
         #        meta - spec elided
     disagreement_policy : " quorum "
Specifying AI-SDLC Processes: A Protocol Language for Human-Agent Boundaries                        17


       • Non-overridable blockers (INV3): any blocker stops work regardless of other validator
         opinions.
       • Human-in-control roles: the two humans are first-class members with execution authority,
         ambiguity resolution, disagreement adjudication, and veto power. The “2” follows from the
         modes, not the other way around: a two-mode producer–reviewer process needs a human
         in control on each side of the boundary. The language admits the degenerate configurations
         explicitly rather than pretending: one person may hold the HI-CTRL role in both modes —
         the boundary remains structurally enforced (tools stay disjoint; only the artifact crosses)
         but the separation of duties becomes nominal, a declared trade rather than a hidden one —
         or a solo developer encodes a 1+N protocol with no review mode at all (producer through
         merge), accepting explicitly that the separation is gone (Section 4.13).
       • Agent roles: the N agents are first-class members with defined responsibilities within their
         capability boundaries.
   Scaling beyond 2+N. The 2+N pattern is the smallest configuration in which Separation of
Duties is structurally enforced rather than absent; the language places no upper bound on modes.
Typical enterprise SDLC processes exhibit four to five distinct modes: planning, production, re-
view, deployment, and operations, each enforcing structural separation of a different concern.
Smaller teams may collapse modes (1+N for solo developers); larger organisations may decompose
further. The language treats all configurations uniformly through the same mode/role/validator
primitives, and we anticipate additional modes (specification authorship, compliance verification,
post-deployment learning) as AI-SDLC practices mature.

4.13    Expressiveness: Four Processes, One Language
A specification language earns its keep by what it can distinguish. We demonstrate expressiveness
with four structurally different working processes, all shipped as executable templates with the
reference implementation and all running unmodified on the same engine (Table 1). They are not
toys: two are the production configurations of the implementation’s own development, and two
are the protocols of the end-to-end evaluation (Section 6.5).
   Solo (1+N). A single producer mode holds the full tool set, edit through merge: Separation of
Duties is deliberately collapsed, and the governance burden shifts entirely to the validator quorum
(four orthogonal validators plus a meta-level protocol-adherence validator). This is the language’s
lower bound: a solo developer keeps structural validation and audit without a second human, and
the protocol says so explicitly rather than implicitly.
   Team (planner/producer/reviewer). Three modes with disjoint tool sets: planning (assess,
plan) gated by intent validators (clarity, scope, value-increment, agile conformance); production
(edit, dispatch, test) unable to merge; review (review, approve, merge) unable to edit. This
is the 2+N pattern of Section 4.12 extended with an upstream planning mode — the shape of a
conventional enterprise SDLC, with WF1 enforcing at infrastructure level the separations that code
review policies enforce by convention.
   Bug-fix surgeon (task-tailored minimality). The protocol of the end-to-end evaluation. Its pre-
execute validator is a deliberate pass-through — declared only to satisfy WF3, so the raw issue reaches
the coder without inducing specification authoring — and the enforcement lives post-execute: a
minimality validator (severity cap warn) rejects sprawling or out-of-scope diffs and routes viola-
tions to recovery for a tighter fix, while a blocker-level global constraint (no_secrets_in_diff)
stays non-overridable. The protocol encodes a lesson the evaluation taught: a generic elaboration-
inducing process reduced bug-fix resolution, and the fix was to invert the enforcement target — in
configuration, not in code.
18                                                            Ylli Prifti, Pasquale De Meo, and Alessandro Provetti


   Feature warden (containment over long horizons). The surgeon’s inversion, for the task
type that fails the opposite way. Features fail by under-implementation and scope drift, so the
pre-execute validator engages structure (warn until the feature is decomposed into components
with acceptance behaviour), and the post-execute containment validator checks completeness,
rejects out-of-scope edits, and treats regression of previously working behaviour as its central
rejection criterion (routed through recovery as shipped; a deterministic blocker-level regression
gate over the previously-passing test set is designed for the feature-development study of Section 7).
Minimality and completeness are opposite enforcement targets; the language expresses both as
validator criteria plus severity policy, and switching between them is a template swap.

Table 1. Four processes in one language. Each row is an executable template; “target” is what the post-execute
enforcement optimises.

                 Protocol     Modes     SoD               Pre-execute           Target
                 Solo (1+N)   1         collapsed         quorum (4+meta)       quality
                 Team         3         enforced (WF1)    intent gates          separation
                 Surgeon      1         n/a               pass-through          minimality
                 Warden       1         n/a               decomposition         completeness


   The comparison with adjacent formalisms is now concrete rather than positional. Prompts can
state all four policies — and Section 6.5 measures what that is worth: the same policy as prose
moved nothing. Workflow and business-process languages (BPMN and its human-agentic extensions)
can express the team pipeline’s sequencing and human tasks, but have no vocabulary for the parts
doing the work here: infrastructure-level capability boundaries per mode, validator quorums with
a severity algebra and pluggable disagreement policies, unforgeable evidence gating dispatch, or
a declared severity cap that turns the same validator from a hard gate into a recovery trigger.
Framework-embedded SOPs (MetaGPT-style) encode roles in agent code, so the surgeon-to-warden
inversion — which here is a YAML swap under an unchanged engine, theorem intact — would be a
code change, and their gates bind by convention rather than by construction. The four templates are
the policy/mechanism separation made concrete: one mechanism, four policies, and the guarantee
of Theorem 4.4 holds for each because well-formedness, not intent, is what the verifier checks.

5     Implementation
We have implemented this specification in a working system, demonstrating that the formal
language is executable and the invariants maintainable.
   Architecture:
     • Protocol engine parses specifications and enforces well-formedness conditions.
     • Two MCP servers (producer-side, reviewer-side) implement mode separation (WF1).
     • Token subsystem implements validation token issuance and verification (INV1).
     • Capability boundaries enforced through tool exposure at infrastructure level (INV2).
     • Event-sourced audit log maintains immutable operation records (INV4).
     • Session checkpoint subsystem maintains resumable state across context boundaries (INV5).

5.1    Architectural Properties
Several properties emerged during implementation that strengthen the specification. The engine ex-
ecutes exactly one mode per invocation, halting at mode boundaries rather than auto-transitioning;
modes communicate only through artifacts and mode changes are explicit human actions, enforcing
Specifying AI-SDLC Processes: A Protocol Language for Human-Agent Boundaries                        19


human-in-control governance — this is the architectural realisation of Axiom 1, on which Theo-
rem 4.4 rests. On any halt, the engine emits a structured, machine-parseable payload (halt type,
blocking validators, justifications, policy decision) alongside human-readable output, enabling an
external orchestrator to interpret a refusal and revise-and-retry or escalate. Validators are resolved
through an open registry: third parties implement a single evaluate(context) interface and regis-
ter a custom validator type without modifying engine code (the reference implementation includes
a worked example). This extensibility also admits meta-level validators registered like any other:
the shipped protocol-adherence validator judges whether submitted work fits the current mode’s
declared profile, and the same interface admits validators over the audit trail itself (checking that
validators are called when required, mode boundaries are respected, and dispatches token-gated)
— protocol self-auditing is expressible as an ordinary validator definition rather than a special
construct. Validator severities form a total order (pass < warn < blocker); a severity cap lets
validators-under-evaluation participate without blocking, with every cap recorded in the audit log.

                       Table 2. Structural claims and their enforcement mechanism.

                     Invariant / condition           Enforcement mechanism
                     INV1 (token unforgeability)     JWT HMAC, single-use, TTL
                     INV2 (capability boundary)      disjoint tool sets at MCP boundary
                     INV4 (audit completeness)       hash-chained audit log
                     INV5 (session resumability)     file-based checkpoint
                     WF1 (tool disjointness)         compiler verifier
                     WF3 (validator coverage)        pre-execute validator requirement

   Self-development validation: we have used the system to extend its own codebase under
the 2+N protocol, providing initial evidence the approach is viable for real software development.
Property-based validation: we verified audit-chain integrity (INV4), token unforgeability and
single-use consumption (INV1), WF1 tool disjointness, severity-cap monotonicity, and the policy
halt invariant against randomised inputs — 17 property tests at a budget of 10,000 examples each
(small discrete input spaces exhaust earlier), completing with zero violations in 17 minutes on a
commodity development machine. The implementation is validated by 2,284 tests across three
layers: unit/integration, end-to-end CLI journeys via subprocess, and property-based randomised
testing of the core invariants; measured line coverage over the full codebase — including operational
tooling well outside the enforcement core — is 68%. A controlled end-to-end comparison against
behavioural-instruction and bare baselines on real tasks is presented in Section 6.5; broader failure-
mode analysis and quantification of human intervention rates remain future work.

6     Empirical Evaluation
The following studies characterise the enforcement properties of the specification language using
the reference implementation as a test bed.

6.1    Policy Monte Carlo: Disagreement Policy Trade-offs
We characterised the four disagreement policies via Monte Carlo simulation (25,000 trials per point,
validator accuracy swept 𝑝 ∈ [0.5, 1.0], 𝑁 = 3 validators), driving the actual PolicyEvaluator
with simulated validator outputs drawn from real severity distributions.
   False-block / false-pass trade-off. Figure 3 plots the false-block rate (good tasks refused) against
the false-pass rate (bad tasks approved). At 𝑝 = 0.5, Unanimous admits only 1.6% of bad tasks while
refusing 87.6% of good ones; Any inverts this (10.5% bad admitted, 52.5% good refused); Majority
20                                                            Ylli Prifti, Pasquale De Meo, and Alessandro Provetti


is intermediate (6.1%, 64.9%). At 𝑁 = 3, Quorum (⌈0.67 · 3⌉ = 3) coincides with Unanimous,
consistent with the formal model; the two diverge for 𝑁 ≥ 5, illustrating that policy choice becomes
a meaningful lever as validator count grows. Refusal mode decomposition. Refusals of good
tasks split into validator-level halts (blocker severity) and consensus-level escalations. At 𝑝 = 0.5,
Unanimous’s 87.6% total refusal is 49.1% HALT and 38.5% ESCALATE, while Any reduces total
refusal to 52.5%, almost entirely HALT (49.7%) with negligible escalation (2.8%). Stricter policies
escalate a larger share, raising friction on well-formed work.
   Quorum–Unanimous convergence. The coincidence at 𝑁 = 3 is a predicted consequence of
the model (⌈0.67 · 3⌉ = 3 requires unanimity); the simulation reproduces it exactly, providing a
checkable prediction against which the implementation can be validated.
   Implementation defect surfaced. The simulation served as a test oracle: an absence of policy
differentiation in initial runs flagged a defect (warnings counted as approvals, collapsing all four
policies to identical behaviour). Correcting the evaluator restored the parametrised enforcement
the model specifies, demonstrating that the analytical model provides a detectable contract against
which implementations can be validated.




Fig. 3. False-block versus false-pass rate for four disagreement policies (𝑁 = 3, real severity distributions).
Unanimous and Quorum nearly eliminate false-passes at the cost of high false-block rates; Any accepts more
bad work for lower friction on good work. Policy choice is a first-class enforcement parameter.




6.2   Governance Overhead
Structural enforcement adds runtime cost beyond inference. Microbenchmarks on the reference
implementation put the CPU-bound operations (policy evaluation, protocol verification, token
issuance and verification) all under 50 µs, and the disk-bound durability operations backing INV4
and INV5 (audit append, checkpoint write) at 127 µs and 672 µs. End-to-end, a governed task path
(governance, pre- and post-execute validation, token issuance and consumption, audit, checkpoint-
ing) adds 33.3 ms over an ungoverned baseline, with every inference-class component — coder,
validators, and task classification — stubbed, since inference is the cost against which overhead
is compared, not a burden of enforcement. Against a representative 3 s inference call this is 1.1%
overhead (teams can rescale as 33.3 ms/𝑇 for their own inference latency 𝑇 ). The dominant costs
are the durability operations, which deployments not needing audit persistence or checkpointing
can omit.
Specifying AI-SDLC Processes: A Protocol Language for Human-Agent Boundaries                              21


6.3   Detection Probability and the Structural Advantage
This study grounds the failure-rate analysis of Section 4.9 empirically, validating the quorum-miss
formula and comparing structural against behavioural failure as pipeline length grows.
                                                                             quorum
   Quorum-miss formula validation. Figure 4 compares the analytical 𝑃miss = 𝑝 𝑣𝐾 + 𝜌 (𝑝 𝑣 −𝑝 𝑣𝐾 )
against Monte Carlo simulation across 𝜌 ∈ [0, 1], for 𝐾 = 3 and 𝐾 = 5 at 𝑝 𝑣 = 0.2. Simulated
points track the analytical curve throughout: at 𝜌 = 0 the quorum benefits from independence
(𝑃miss = 0.008 for 𝐾 = 3), while at 𝜌 = 1 it collapses to a single effective validator (𝑃miss = 0.2).
The agreement confirms the implementation faithfully realises the model; whether the correlation
assumption matches real cross-provider behaviour is a separate empirical question (Section 7.1).
   The independence ceiling. The naive independent form 1 − (1 − 𝑝) 𝑁 is an upper bound on
detection that correlated validators cannot reach: any 𝜌 > 0 shifts miss probability above the
independent baseline. This is why 𝜌 appears in the model: it is not a conservatism knob but a
structural consequence of validators sharing training data and architectural priors. Methodological
diversity lowers 𝜌 but cannot drive it to zero.
   Structural versus behavioural failure by pipeline length. Figure 5 compares the structurally
enforced rate (quorum plus recovery) against the behavioural cascading rate as 𝑁 grows. The gap
widens with 𝑁 : behavioural failure rises steeply (0.10 at 𝑁 = 1, 0.45 at 𝑁 = 5, 0.91 at 𝑁 = 20) as
corrupted state compounds, while structural failure grows close to linearly (0.016, 0.080, 0.318). At
𝑁 = 5 this is a 5.6× reduction, still nearly 3× at 𝑁 = 20 where the behavioural rate saturates. This
is the empirical counterpart of the ratio claim in Section 4.9.
   Ratio sensitivity. Figure 6 maps the 𝑃behavioural /𝑃structural ratio across the (𝜌, 𝑝 recovery ) plane.
The advantage is largest when validators are near-independent and recovery reliable (exceeding
100× in the corner) and degrades gracefully otherwise. The ratio exceeds unity across the entire
plane: structural enforcement never underperforms behavioural compliance within the modelled
range, though the magnitude is an empirical property of the 𝜌 and 𝑝 recovery a deployment exhibits.




Fig. 4. Validation of the quorum-miss formula (𝑝 𝑣 = 0.2). Simulated points (markers) track the analytical
curves (lines) for 𝐾 = 3 and 𝐾 = 5 across the full correlation range. At 𝜌 = 1 the quorum provides no benefit
over a single validator.



6.4   Byzantine Robustness
The final study probes the limits of validator-quorum enforcement under adversarial validators
that ignore their criteria and always emit a fixed verdict. We model two attack directions at 𝑁 = 5,
honest accuracy 𝑝 = 0.7, sweeping compromised validators 𝑓 from 0 to 5.
22                                                                    Ylli Prifti, Pasquale De Meo, and Alessandro Provetti




Fig. 5. Structural versus behavioural failure probability by pipeline length 𝑁 . Behavioural failure (cascading)
rises steeply as corrupted state compounds; structural failure (quorum plus recovery) grows close to linearly.




Fig. 6. Sensitivity of the 𝑃behavioural /𝑃 structural ratio to validator correlation 𝜌 and recovery-loop failure 𝑝 recovery .
The ratio exceeds unity across the entire plane and is largest when validators are near-independent and
recovery is reliable.


   Always-pass (collusion / bypass). When 𝑓 adversarial validators always approve, the false-
pass rate rises with 𝑓 at a policy-dependent rate (Figure 7, left). Unanimous is most robust: it
still requires every honest validator to approve, so its false-pass rate stays below 1% until 𝑓 = 3
(2.2%), remains 14.8% even with four of five validators compromised, and reaches certainty only at
𝑓 = 5. Majority and Quorum first exceed 1% at 𝑓 = 2 (2.2% and 1.2%); Any is the most fragile,
leaking already at 𝑓 = 1 (0.8%). Degradation is graceful rather than cliff-edged — no policy exceeds
a one-in-three false-pass rate until a majority of the quorum is compromised — and the ordering
mirrors the false-block trade-off of Section 6.1: the policy most permissive of good work is most
vulnerable to permissive adversaries.
   Always-block (denial of service). When adversarial validators always emit a blocker, a single
one (𝑓 = 1) drives the false-block rate to 100% for all four policies (Figure 7, right). This is INV3
operating exactly as specified: the unconditional rule that any blocker halts execution fires before
policy aggregation, so no policy can out-vote it. What is a safety guarantee against missed defects
is, under a compromised-restrictive validator, a denial-of-service vector.
   The INV3 asymmetry. The always-block direction is policy-independent (INV3 forces all policies
to halt at 𝑓 = 1); the always-pass direction is policy-dependent (Unanimous tolerates up to two
Specifying AI-SDLC Processes: A Protocol Language for Human-Agent Boundaries                             23




Fig. 7. Adversarial validator sensitivity (𝑁 = 5, 𝑝 = 0.7, 20,000 trials per cell). Left: under always-pass
adversaries, false-pass rate is policy-dependent, with Unanimous most robust (below 1% until 𝑓 = 3) and
Any most fragile (leaking from 𝑓 = 1). Right: under always-block adversaries, a single compromised validator
(𝑓 = 1) drives all policies to 100% false-block: INV3 operating as specified.



compromised validators). No single policy is robust to both directions simultaneously: the non-
overridable-blocker semantics that make the system fail safe against missed defects necessarily
make it fail closed under a restrictive adversary. This is the quantified cost of INV3 and bounds
what validator-quorum enforcement can defend against: the mechanism assumes validators faithful
to their criteria, not adversarial. Defending against compromised validators requires orthogonal
mechanisms (validator attestation, anomaly detection on verdict distributions) outside the policy
layer.
   The fail-closed direction deserves a direct answer, because it looks like a denial-of-service vector:
one hallucinating or over-conservative validator can halt all work. Three points bound the exposure.
First, the failure is visible by construction: in the terms of Proposition 4.1, a false blocker produces an
audited stall — a halt with a structured payload naming the blocking validator and its justification,
escalated to a human — whereas the symmetric failure under behavioural compliance (a false pass)
ships silently. The asymmetry is chosen: the recoverable failure mode is made cheap and loud, the
unrecoverable one is made structurally hard. Second, the cost is bounded: a stall costs one human
adjudication, and the audit log localises the offending validator immediately; a repeatedly-blocking
validator is an operational signal, not a systemic corruption. Third, the language already carries
the mitigations: severity caps allow a validator-under-evaluation to participate without blocking
(every cap audited), disagreement policies other than Any-Blocker trade fail-closed strictness for
availability, and meta-level validators can monitor verdict distributions for exactly this anomaly.
What the language does not do is let an agent override the gate — that is INV3, and softening it
would surrender the property the rest of the paper establishes.

6.5   End-to-End Validation on Real Software Tasks
The simulation studies (Sections 6.1–6.4) characterise the enforcement layer intrinsically. This
study tests, end-to-end on real software-engineering tasks scored by hidden acceptance suites, the
empirical premise that motivates the language: that a development methodology must be executed
as a process, not merely told to an agent. It is scoped by Corollary 4.2: an autonomous, oracle-graded
24                                                       Ylli Prifti, Pasquale De Meo, and Alessandro Provetti


benchmark measures 𝑃silent + 𝑃stall and therefore cannot reward the governance value of a non-
overridable gate, so the protocol arm runs in advisory configuration (violations route to recovery,
never to a hard stop), and what the study establishes is the value of the executed, validated process
— the human-in-the-loop value of hard gates requires deployment data and is explicitly future
work (Section 7). The study deliberately exercises a single primitive — a post-execute validator
with token-gated dispatch and a bounded recovery loop — not the full apparatus (multi-validator
quorums, the 2+N pattern, Byzantine tolerance), which is characterised in simulation above.
6.5.1 Design. We use SWE-bench Verified [17, 24], a benchmark of real GitHub issues paired with
the maintainers’ hidden regression tests; a task is resolved iff the generated patch makes the failing
test pass without breaking the passing suite. On each task we run arms that share an identical
coding agent and differ only in how a fixed bug-fix methodology (“the correct fix is the smallest
change that makes the reported failure pass; do not refactor, rename, or touch unrelated files”) is
delivered:
     • Arm A (bare): the agent receives the raw issue, no methodology.
     • Arm B (prose): the agent receives the methodology as prompt instructions — the method-
       ology told, the standard “encode process in the prompt” approach (Section 2).
     • Arm B′ (executed loop, ablation): the same methodology run as an executed, validated,
       self-correcting process outside the protocol engine: a validator inspects the committed
       diff for minimality and localisation and routes violations back for a tighter fix (up to four
       attempts), implemented as plain advisory scaffolding with no tokens and no engine.
     • Arm C (executed protocol): the same methodology specified as a protocol and run by the
       engine in advisory configuration: the same post-execute validator and recovery loop as B′ ,
       with dispatch token-gated (INV1) and every step audited (INV4). No methodology text is
       added to the coder prompt beyond arm B’s, so B, B′ , and C hold the policy content constant
       and vary only the delivery mechanism.
   Because the arms run on the same tasks, the correct test is paired: we report resolve rate per arm
and the exact two-sided McNemar test on discordant pairs. To isolate the effect of the coder, the
enforcement machinery (the validator and recovery classifier) is held fixed on a single model across
all runs, so differences between arms reflect the delivery mechanism, not a change of enforcer. The
protocol used is a task-tailored minimality protocol: a prior generic protocol that induced up-front
specification authoring reduced resolve rate by inflating patch size (larger diffs resolve less), which
motivated inverting the enforcement target toward minimality rather than elaboration.
   Setup and reproducibility. All arms use the same agent scaffold the opencode CLI agent driving
an open-weight coder; only the delivery of the methodology differs (A/B/C above). The enforcement
machinery (the minimality validator and the recovery classifier) is fixed to deepseek-v4-flash
across every run, so between-arm differences isolate the delivery mechanism, not the enforcer.
Coders span two tiers of the DeepSeek-V4 family deepseek-v4-flash (cheap) and deepseek-v4-pro
(strong) with gpt-oss:20b used for the capability-boundary condition. Task sets are frozen, seeded,
repo-stratified draws from SWE-bench Verified (seeds 13, 29, and 47; per-run 𝑛 in Table 3), with one
trial per cell (cells were near-deterministic, so budget went to more tasks rather than more trials).
Patches are scored by the official SWE-bench evaluation harness under Docker, and the paired
significance test is the exact two-sided McNemar on discordant pairs. The full patch text for every
cell is retained, so each run is re-scorable from saved artifacts without re-dispatching the agent.
6.5.2 Result: the executed process beats the told process. Table 3 reports four independent runs
spanning two model tiers (a cheap and a strong variant of one open-weight family) and task
samples up to 𝑛=191. The pattern is consistent, and it is two-sided. First, the null: methodology
Specifying AI-SDLC Processes: A Protocol Language for Human-Agent Boundaries                                                25


as prose does not improve outcomes — arm B never significantly beats bare in any run (all
A-vs-B comparisons non-significant). Second, the effect: the same methodology executed as a
validated, self-correcting process (C) significantly outperforms both bare and prose, yielding
a 14–22 point absolute gain in resolve rate. The identical policy content, delivered two ways,
produces a null and a large effect; the difference is entirely in whether the process is executed or
merely described.

Table 3. Resolve rate (%) on SWE-bench Verified across four paired runs: A bare, B prose instruction,
C executed protocol (advisory). 𝑝-values are exact two-sided McNemar on discordant pairs. Rows are
deepseek-v4-flash/-pro × task seed.

                              Run             𝑛       A       B       C       𝑝 A–C       𝑝 B–C
                              flash, s13     94    59.6    55.3    69.1      0.064       0.004
                              flash, s29     96    49.0    53.1    66.7     0.0002       0.015
                              pro, s13       98    50.0    52.0    72.4    <0.0001      0.0001
                              flash, s47    191    50.3    50.3    67.0    <0.0001     <0.0001


   The effect replicates across two independent task samples (seeds 13, 29), holds at higher statistical
power (𝑛=191), and appears on both model tiers. The loop genuinely engages rather than passing
work through unchanged: across runs, 40–90% of tasks required at least one recovery round, and
arm C uniquely resolved clusters of tasks that both baselines missed. We are careful about what
this establishes. A validate-and-retry loop is a known effect class (iterated generation with critique),
and we do not claim its benefit as a novel result; what the experiment isolates is that the same
policy content yields nothing when told and a large, replicated gain when executed — the empirical
motivation for a language whose subject is precisely the specification of executable process. The
guarantee the language adds over ad-hoc scaffolding is the theorem’s (Section 4.11): the loop cannot
be skipped, by construction, rather than happening to run.

6.5.3 Ablation: the executed loop carries the gain. If the engine’s contribution on this benchmark
is the executed loop, then the same loop implemented as plain advisory scaffolding — no engine,
no tokens — should reproduce the gain, and the engine in advisory configuration should add
nothing beyond it. That is exactly what the ablation shows. On the highest-power sample (seed
47, 𝑛=191, re-scored as one pass across all four arms): A 49.7%, B 49.2%, B′ 59.7%, C 60.7%.2 Paired
McNemar: B′ vs. B, 𝑝 = 0.018 — the executed loop significantly beats the same methodology as
prose; B′ vs. C, 𝑝 = 0.90 — the engine in advisory configuration is statistically indistinguishable
from the bare loop. This is the expected mechanistic identity, not a negative surprise: in advisory
configuration the engine is the validated loop plus token-gating and audit, and Corollary 4.2
says the additional properties it guarantees (non-skippability under adversarial or drifting agents,
auditability, enforceable escalation) are precisely the ones an autonomous benchmark cannot score.
The ablation thus cleanly attributes the benchmark gain to the executed process, and delimits the
engine’s further value to properties requiring deployment evidence.

2 These rates come from a single four-arm scoring pass, so that every paired comparison in the ablation shares one scoring

environment; the three-arm seed-47 row of Table 3 was scored in a separate pass. SWE-bench scoring applies patches
and executes hidden test suites in per-task containers, and absolute rates are sensitive to the scoring environment (arm C:
67.0 there vs. 60.7 here); the within-pass discordant-pair statistics are the quantities of interest and are unaffected by this
cross-pass variation.
26                                                             Ylli Prifti, Pasquale De Meo, and Alessandro Provetti


6.5.4 Model commodity: the executed process compresses the model gap. Running the strong (“pro”)
and cheap (“flash”) tiers under both bare and executed-process conditions on the same seed-13
task set yields a 2 × 2 grid (Table 4). Two effects stand out. First, a cheap model under the
executed process outperforms a strong model bare: on the 94 instances scoreable in both runs,
flash-with-process resolves 69.1% against bare-pro’s 48.9% — a paired per-instance comparison
(discordant pairs 24/5, exact McNemar 𝑝 = 0.0005) — so the process layer is worth more than
a model-tier upgrade. Second, the executed process compresses the gap between tiers: bare, the
models differ (59.6 vs. 50.0); under the process, they converge near the top (69.1 vs. 72.4). Which
model to buy matters less than what process it runs under (Section 7).
Table 4. Model-commodity 2 × 2 (resolve rate, %, SWE-bench Verified, seed 13). The executed process lifts
both tiers and compresses the gap between them; the cheap model under the process beats the strong model
bare.

                                                    Bare (A)     Executed (C)
                               Cheap tier (flash)     59.6            69.1
                               Strong tier (pro)      50.0            72.4


6.5.5 Boundary condition: the executed process requires a capable coder. The advantage is not un-
conditional. Repeating the design with a small, weaker open-weight coder (gpt-oss:20b) collapses
the effect: resolve rates fall to A 9.1%, B 19.2%, C 14.1% (𝑛=99), the executed process no longer beats
prose (𝑝 B–C =0.33, 𝑝 A–C =0.30), and only B > A reaches significance (𝑝=0.03). This is also the one
regime in which prose is not a null, and the two findings are consistent rather than in tension: the
prose null of Table 3 is a claim about coders above the capability floor, where the executed process
dominates whatever the text adds; below the floor, recovery rounds cannot convert critique into
fixes, and methodology text is the only guidance the coder can use at all. Diagnostically, the loop
still engaged — 47 of 99 tasks exhausted all four recovery rounds and arm C produced the fewest
empty patches — but on a coder operating near 15% base capability, the process converts “gave
up” into “wrong answer” more often than into “correct fix.” The executed process guarantees that
validation occurs; it cannot manufacture a correct patch from a coder incapable of producing one.
This is the collapse Corollary 4.3 predicts: recovery rounds re-sample the same failure distribution,
so as the agent’s base failure rate grows the advantage factor 𝐴(𝑝𝑎 ) falls to one regardless of how
strictly the process is enforced. The boundary condition was derived before it was observed, and
the diagnostics match the mechanism the model posits (the quorum caught defects; recovery could
not fix them).
6.5.6 Threats to validity. SWE-bench Verified predates the models’ training cut-offs and is plausibly
contaminated; the paired design controls for this (contamination benefits all three arms equally, so
it cannot explain the between-arm gap), but absolute rates should not be read as generalisation
to unseen code. The evaluation covers a single task type (bug fixing) under one protocol and a
single primitive; multi-validator quorums, the 2+N reviewer separation, and richer protocols are
validated only in simulation, and feature development and other task types remain future work
where the over-elaboration failure mode suggests the approach may have even more headroom.
The benchmark’s scope is bounded by Corollary 4.2: it can establish the value of the executed
process, and does; it cannot, by construction, measure the governance value of non-overridable
gates or human-in-the-loop escalation, which require deployment usage data rather than oracle
grading. Finally, the enforcer is held fixed on one model to isolate the coder effect; the interaction
between coder and enforcer capability is not yet mapped.
Specifying AI-SDLC Processes: A Protocol Language for Human-Agent Boundaries                       27


6.6    Summary
Five studies characterise the enforcement layer along complementary axes. The policy Monte Carlo
(Section 6.1) shows disagreement policy is a first-class trade-off between false-block and false-pass.
The overhead study (Section 6.2) shows the machinery costs roughly 1% of inference latency. The
detection study (Section 6.3) validates the failure-rate model and confirms the structural advantage
widens with pipeline length. The Byzantine study (Section 6.4) bounds what the policy layer can
defend against, exposing the INV3 asymmetry. Finally, the end-to-end study (Section 6.5) tests the
language’s empirical premise on real software tasks: on SWE-bench Verified, an identical bug-fix
methodology yields nothing when delivered as prose but a large, replicated gain when executed
as a validated, self-correcting process (two model tiers, task samples up to 𝑛=191); an ablation
attributes the gain to the executed loop itself, exactly as Corollary 4.2 predicts for an advisory
configuration under oracle grading; the process compresses the model-tier gap, with a cheap model
under the process beating a strong model bare; and a weak-coder boundary condition confirms the
advantage is contingent on adequate agent capability, as Corollary 4.3 predicts. Broader task types
beyond bug fixing, and the coder–enforcer capability interaction, remain the principal items of
future work.

7     Discussion
7.1    Limitations
Several limitations bound the claims.
   Scope of the end-to-end evaluation. Beyond simulation and a self-development feasibility
demonstration, Section 6.5 provides a controlled end-to-end comparison against behavioural-
instruction and bare baselines on SWE-bench Verified, scored by hidden acceptance suites. That
evaluation covers a single task type (bug fixing) under one enforced protocol and a single open-
weight model family; broader task types (notably feature development) and cross-family generali-
sation remain future work.
   Analysis under assumptions. The failure rate bounds (Section 4.9) assume failure-rate con-
stancy, stable correlation, and bounded recovery cost; they establish the structural difference, but
precise quantitative claims require empirical validation.
   Token integrity is implementation-dependent. INV1 requires unforgeable tokens but not
a specific mechanism: different contexts (single-process, distributed, multi-tenant) need different
primitives. We treat this as a feature: the specification is portable, the enforcement contextual.
   Validator quality bounds system quality. Enforcement guarantees that validation occurs,
not that the validator is correct; the failure-rate advantage is contingent on validators clearing
a useful detection threshold. The mitigation is compositional (deterministic predicates, pre- and
post-execution phases, per-mode gating, an orthogonal quorum), but the problem is bounded, not
solved: a sufficiently poor or correlated validator set degrades the guarantee however strictly the
protocol is enforced.
   Applicability scales with project complexity, not team size. The same primitives express
single-agent and multi-mode configurations uniformly; what determines whether structural en-
forcement pays off is project complexity and stage. A simple project can be self-orchestrated by
hand, but the manual cost of instructing, validating, and catching missed steps scales badly as
complexity grows. We do not establish where this crossover lies.

7.2    What the Language Does Not Solve
Writing effective protocols still requires deep software engineering expertise; the language lets
senior engineers encode that knowledge but does not supply it. Protocol evolution (who may
28                                                              Ylli Prifti, Pasquale De Meo, and Alessandro Provetti


change a protocol, what review a change requires) is governance the language does not prescribe,
though its machine-executable form affords version control and peer review. Verifying temporal
properties or stated goals, and synthesising optimal protocols from constraints, remain future work.

8    Conclusion
We have presented a specification language for AI-SDLC processes, addressing a documented gap:
formal mechanisms for human-agent responsibility boundaries, approval gates, and governance
constraints. The language is built on a single idea — separating policy (the declared modes of
working) from mechanism (structural enforcement via validation tokens, capability boundaries,
and non-overridable gates) — with formal abstract syntax, well-formedness conditions, oper-
ational semantics, and enforcement invariants. The separation buys two things at once. First,
flexibility: a process becomes a portable artifact, illustrated by the 2+N reference pattern with
its producer–reviewer separation, orthogonal validator quorum, and non-overridable blockers,
that teams reconfigure without touching agent code. Second, quasi-determinism, now a theorem:
for any well-formed protocol the enforcement invariants hold on every execution trace, closed
under Kleene composition (Theorem 4.4), so protocol steps cannot be skipped by construction. A
failure-rate analysis makes the consequences precise — silent failure bounded at a weighted product
of agent and validator rates, the remainder converted into visible, audited stalls, and a capability
floor below which the benefit vanishes — validated in simulation and end-to-end. On SWE-bench
Verified, an identical methodology yielded nothing delivered as prose instruction and a significant,
replicated gain when executed as a validated, self-correcting process, with the capability floor
observed where the model predicts it. That result is the thesis in miniature: because the protocol
and its invariants are unchanged as models are swapped or upgraded, the advantage transfers
across tiers, so as foundation models converge the durable engineering asset becomes the formally
specified, executable process, not the model. The effect is not unconditional — it requires a coder
above the capability floor, and we have demonstrated it for bug fixing under one protocol — so
establishing it for feature development and across model families, and measuring in deployment the
governance value of hard gates and human-in-the-loop escalation that oracle-graded benchmarks
structurally cannot reward (Corollary 4.2), is the natural next step.

Acknowledgments
Generative AI tools (including Anthropic Claude, Google Gemini, DeepSeek, Qwen, and Kimi) were
used, under the authors’ direction, as assistive instruments in the preparation of this manuscript
and its artifact — text drafting and revision, LaTeX and figure preparation, coding assistance, and
cross-checking the manuscript’s claims against the artifact’s outputs. All research content, design,
and conclusions are the authors’ own, and the authors take full responsibility for the work.

Data and Code Availability
The reference implementation (protocol engine, verifier, MCP servers, and shipped templates), the
Lean 4 mechanisation, the five simulation studies with their regenerated outputs, the property-test
suite, and the SWE-bench experiment harness with saved per-task artifacts (every run re-scorable
without re-dispatching agents) are released as open source (Apache 2.0) at https://github.com/snodo-
dev/snodo, with the submission-time state archived at https://doi.org/10.5281/zenodo.21967946.

References
 [1] Adem Ait, Javier Luis Cánovas Izquierdo, and Jordi Cabot. 2024. Towards Modeling Human-Agentic Collaborative
     Workflows: A BPMN Extension. In arXiv preprint arXiv:2412.05958. BPMN extension for human-agent collaborative
     workflows.
Specifying AI-SDLC Processes: A Protocol Language for Human-Agent Boundaries                                           29


 [2] Anthropic. 2026. Measuring AI Agent Autonomy in Practice. Anthropic Research. HITL vs HOTL terminology and
     oversight levels.
 [3] R. Meredith Belbin. 2012. Team Roles at Work (2nd ed.). Routledge.
 [4] Alexander Bondarenko, Denis Volk, Dmitrii Volkov, and Jeffrey Ladish. 2025. Demonstrating Specification Gaming in
     Reasoning Models. arXiv:2502.13295 Palisade Research.
 [5] Reinhardt A. Botha and Jan H. P. Eloff. 2001. Separation of Duties for Access Control Enforcement in Workflow
     Environments. IBM Systems Journal 40, 3 (2001), 666–682.
 [6] Issam Bouzenia and Michael Pradel. 2025. Analyzing Autonomous Software Engineering Agents. In International
     Conference on Software Engineering. Documented over-exploration and repeated fix patterns.
 [7] CrewAI. 2024. CrewAI: Framework for Orchestrating Role-Playing Autonomous AI Agents. https://www.crewai.com/.
 [8] Tom DeMarco and Timothy Lister. 2013. Peopleware: Productive Projects and Teams (3rd ed.). Addison-Wesley
     Professional.
 [9] Jack B. Dennis and Earl C. Van Horn. 1966. Programming Semantics for Multiprogrammed Computations. Commun.
     ACM 9, 3 (1966), 143–155. Foundational work on capability-based access control.
[10] EPAM Systems. 2026. Agentic Development Lifecycle (ADLC): A New Model for AI Systems Beyond SDLC. Technical
     Report. EPAM. Identified need for human-agent responsibility mapping.
[11] Forrester Research. 2025. Create Your AI-Enhanced SDLC Transformation 90-Plus-Day Roadmap. Technical Report.
     Forrester. Governance requirements for AI-SDLC.
[12] Michael Fu, Rijnard van Tonder, Sumit Gulwani, Sergey Mechtaev, and Nebojsa Tomasic. 2024. Security Implications
     of Large Language Model Code Assistants: A User Study. ACM Transactions on Software Engineering and Methodology
     33, 4 (2024). Analysis of 733 code snippets from AI tools.
[13] Grid Dynamics. 2026. AI SDLC: Redefining Developer Work. https://www.griddynamics.com. Asked about frameworks
     for multi-agent supervision.
[14] Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Ceyao Zhang, Jinlin Wang, Zili Wang,
     Steven Ka Shing Yau, Zijuan Lin, et al. 2024. MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework.
     In International Conference on Learning Representations (ICLR). Role-based multi-agent framework with SOPs encoded
     in prompts.
[15] Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, and Denny Zhou. 2024.
     Large Language Models Cannot Self-Correct Reasoning Yet. In International Conference on Learning Representations
     (ICLR). arXiv:2310.01798
[16] IEEE Spectrum. 2025. Silent Failures in AI Code Generation. IEEE Spectrum (January 2025). Analysis of newer LLM
     coding failures.
[17] Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik Narasimhan. 2024. SWE-
     bench: Can Language Models Resolve Real-World GitHub Issues?. In Proceedings of the 12th International Conference
     on Learning Representations (ICLR). arXiv:2310.06770 [cs.CL]
[18] Stephen C. Kleene. 1956. Representation of Events in Nerve Nets and Finite Automata. In Automata Studies, Claude E.
     Shannon and John McCarthy (Eds.). Princeton University Press, 3–41. Original formulation of the Kleene star operator.
[19] LangChain. 2024. LangGraph: Multi-Agent Workflows. https://www.langchain.com/langgraph.
[20] LangChain. 2026. Human-in-the-Loop Middleware. https://docs.langchain.com/. HumanInTheLoopMiddleware with
     four decision types.
[21] Adrian Shuai Li, Reihaneh Safavi-Naini, and Philip W. L. Fong. 2022. A Capability-based Distributed Authorization
     System to Enforce Context-aware Permission Sequences. arXiv preprint arXiv:2211.04980 (2022).
[22] NIST. 2020. Security and Privacy Controls for Information Systems and Organizations. Technical Report SP 800-53 Rev.
     5. National Institute of Standards and Technology. AC-5 Separation of Duties.
[23] Object Management Group. 2013. Business Process Model and Notation (BPMN), Version 2.0.2. https://www.omg.org/
     spec/BPMN/2.0.2/.
[24] OpenAI. 2024. Introducing SWE-bench Verified. Technical report. OpenAI. https://openai.com/index/introducing-swe-
     bench-verified/.
[25] OpenAI. 2024. OpenAI o1 System Card. Technical Report. OpenAI. https://openai.com/index/openai-o1-system-card/
[26] Rajat Pandit. 2025. Agentic SDLC: A Complete Guide. https://rajatpandit.com. Called for structured, codified context.
[27] Hammond Pearce, Baleegh Ahmad, Benjamin Tan, Brendan Dolan-Gavitt, and Ramesh Karri. 2022. Asleep at the
     Keyboard? Assessing the Security of GitHub Copilot’s Code Contributions. In IEEE Symposium on Security and Privacy.
     Found 40% of Copilot programs vulnerable via CodeQL.
[28] Ran The Builder. 2026. AI-Driven SDLC: Build Secure, Scalable Software with AI. https://ranthebuilder.cloud.
     Documented governance risks.
[29] Yuchen Shi, Siqi Cai, Zihan Xu, Yuei Qin, Xuhao Hu, Jiayi Xu, Yasheng Liao, Yangyang Lu, Shi Wang, Lingpeng Xiong,
     Junxian Lin, Zhipeng Liu, and Xipeng Qiu. 2025. FlowAgent: Achieving Compliance and Flexibility for Workflow
30                                                                 Ylli Prifti, Pasquale De Meo, and Alessandro Provetti


     Agents. In arXiv preprint arXiv:2502.14345. Procedure Description Language (PDL) for workflow agents.
[30] SitePoint. 2026. Audit Trail Complications in AI Code Generation. https://www.sitepoint.com. Analysis of compliance
     challenges.
[31] Token Security. 2026. The Shift From Credentials to Capabilities in AI Access Control Systems. https://www.token.
     security/blog/.
[32] Wil M. P. van der Aalst and Arthur H. M. ter Hofstede. 2005. YAWL: Yet Another Workflow Language. Information
     Systems 30, 4 (2005), 245–275.
[33] Waxell. 2026. Human-in-the-Loop vs Human-on-the-Loop for AI Agents. https://www.waxell.ai/blog/human-in-the-
     loop-vs-human-on-the-loop-ai-agents. Coverage drift in agent-encoded oversight.
[34] Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang,
     Jiale Liu, Ahmed Hassan Awadallah, Ryen W. White, Doug Burger, and Chi Wang. 2023. AutoGen: Enabling Next-Gen
     LLM Applications via Multi-Agent Conversation. In arXiv preprint arXiv:2308.08155.
[35] Yiqun Yao et al. 2025. SAGA: A Security Architecture for Governing AI Agentic Systems. In arXiv preprint
     arXiv:2504.21034. Cryptographic access control tokens for agent-to-agent communication.
[36] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li,
     Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, and Ion Stoica. 2023. Judging LLM-as-a-Judge with MT-Bench
     and Chatbot Arena. In Advances in Neural Information Processing Systems (NeurIPS), Datasets and Benchmarks Track.
     arXiv:2306.05685
