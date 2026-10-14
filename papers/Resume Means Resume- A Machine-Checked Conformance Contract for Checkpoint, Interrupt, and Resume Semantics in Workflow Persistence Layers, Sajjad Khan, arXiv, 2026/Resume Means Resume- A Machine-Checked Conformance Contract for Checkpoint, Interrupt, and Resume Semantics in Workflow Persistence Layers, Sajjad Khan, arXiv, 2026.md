                                                                                                                                                                                            1




                                            Resume Means Resume: A Machine-Checked
                                               Conformance Contract for Checkpoint,
                                                Interrupt, and Resume Semantics in
                                                    Workflow Persistence Layers
                                                                                                          Sajjad Khan

                                             Abstract—A framework that persists execution state so a run can be interrupted, survive a crash, and continue must decide what a
                                             resume means for effects that already happened. Five widely deployed agent workflow frameworks answer differently, none exposes a
                                             machine-checkable contract, and measured behavior violates even the fragments they state. The R ESUME C ONTRACT states six
                                             properties over the persistence API — prefix continuation, effect exactly-once, fork determinism, checkpoint validity, consume-once,
                                             recovery determinism — plus fork-intent and liveness obligations. A TLA+ model checks a reference semantics exhaustively, verdicts
                                             unchanged at scaled bounds (7.4×106 distinct states), and the reference conjunction is additionally TLAPS-proved unbounded (196
                                             obligations); a 39-cell fault matrix and two companion modules yield the separating models independence requires (five properties
                                             independent of the conjunction of the others; consume-once splits, its consumption clause independent of all six). A deterministic,
arXiv:2608.03836v3 [cs.LG] 8 Aug 2026




                                             LLM-free harness measures five frameworks at pinned releases. LangGraph 1.2.9 durably records a second resume value and never
                                             consults it, persists schema-invalid state silently, and re-executes durably recorded work after a real SIGKILL — exactly-once across
                                             interrupts, at-least-once across crashes, on one API. CrewAI 1.15.2 re-executes completed effect-bearing methods against its written
                                             claim, and pydantic-graph 1.x cannot resume after a mid-node crash; no two probed frameworks share a conformance profile.
                                             Consume-once holds sequentially and fails under concurrent delivery: k processes resuming one parked interrupt fire the gated effect k
                                             times, saturation 1.0 in 36 of 40 cells and never below 0.933 on both durable backends. The admitting window tracks the gated node’s
                                             own execution time, measured by dose–response. The failure crosses hosts, two racers on separate machines duplicating in 10/10
                                             repetitions. Live-model cells reproduce the fork violation 40/40 per model. R EMIT, a reference sequencer whose Verus-verified recovery
                                             core is line-identical to the shipped executable under a CI gate (no end-to-end refinement is claimed), repairs the fork and validity cells.
                                             The cross-process cell is repaired at the read path, and the repair ships: an opt-in gate claims consumption in the shared store, serving
                                             one racer and refusing the rest before any node executes ({1:10} on both durable backends, and with the racers on two hosts).

                                             Index Terms—Conformance testing, formal specification, checkpointing, crash recovery, exactly-once semantics, idempotence, model
                                             checking, TLA+ , interrupts, human-in-the-loop, workflow frameworks, LLM agents.

                                                                                                                 ✦

                                        1    I NTRODUCTION


                                        A        PERSISTENCE plane makes a simple promise: a run                          happens when the same interrupt is answered twice with
                                                can stop — for a human approval, for a crash, for a different values, what may be persisted, and whether the
                                        preemption — and then continue. The promise is old and its recovery decision is a function of durable state. This paper
                                        failure modes are classical; what is new is where the promise measures whether the machinery holds.
                                        is now being made. A generation of workflow frameworks                               The gap is not mere absence of specification but incoher-
                                        for LLM agents has shipped that machinery to developers ence. None of the evaluated frameworks exposes a machine-
                                        who gate payments, messages, and file writes behind it: checkable contract for these obligations, and where fragments
                                        LangGraph checkpoints graph state per superstep and ex- are stated, the frameworks contradict one another: CrewAI’s
                                        poses interrupt/Command(resume=...); LlamaIndex checkpointing documentation claims restoration “resume[s]
                                        Workflows serializes a workflow Context mid-run and without re-running completed work” [1]; LlamaIndex Work-
                                        restores it; CrewAI persists flow state and restores runs flows instructs users to place wait_for_event early and
                                        from checkpoint files. As agents are given authority over “make any preceding work safe to re-execute” [2]; LangGraph
                                        non-idempotent effects, “continue” becomes a correctness memoizes completed @task results across resume. Three
                                        question: which completed effects may fire again, what frameworks, three incompatible answers — and, as we show,
                                                                                                                          two of the three do not satisfy even the semantics they
                                        S. Khan is an independent researcher, London, UK (e-mail: sajjadan- themselves state or imply.
                                        war200@gmail.com).
                                        Artifact (conformance probes, TLA+ models and TLC configurations, and                The chain from divergence to harm is concrete: a devel-
                                        the R EMIT reference-sequencer design), with a single-command audit               oper who ports a side-effecting workflow across frameworks
                                        (reproduce.sh) that re-derives every headline number from committed               cannot locally determine which discipline is in force — no
                                        data. The artifact repository and the R EMIT package sources (Rust core, PyO3 type, no signature, no documented property to consult
                                        bindings, decision-free LangGraph shim) are private pending publication and
                                        will be released publicly on publication; access for review is available from the — and the GitHub issues this paper reproduces are that
                                        author on request.                                                                gap made real. We treat the issues as motivation, never
                                                                                                                                 2

measurement; every behavioral claim is re-established by           (LangGraph’s BaseCheckpointSaver first), delivered at
the deterministic harness of Section 5. The persistence plane      labeled maturity levels: invariants stated in Verus [3] and
lacks what network protocols and file systems have had for         machine-discharged, the shipped recovery-decision core
decades: an explicit contract, a machine-checked model, and        a verified executable function (no end-to-end refinement
a conformance suite. A single contract can span divergent          claimed); a Rust core behind PyO3 bindings, conformance-
execution models because they share a boundary — check-            checked against the TLA+ transition relation; a validity gate
points, interrupts, resume commands, a state-inspection API        that turns silent invalid persistence into loud rejection live;
— and every property below is stated over that surface alone;      and fork determinism settled by a matched pair — write-
a framework documenting a weaker discipline is recorded as         path keying fails, a read-path fork-intent filter repairs #6663
divergent (D), not defective. We make that concrete in four        on the identical protocol — re-established by the packaged
steps.                                                             decision-free shim with the stock saver as differential control.
    (1) The R ESUME C ONTRACT (Section 3). Six properties          This completes the mechanism account of Section 4.3.
over an abstract resume plane: prefix continuation (PC), effect            Positioning: Two recent systems bracket this paper
exactly-once (EO), fork determinism (FD), checkpoint validity      without occupying it: below the framework API, Crab [4]
(CV), consume-once (CO), and recovery determinism (RD).            checkpoints OS-level sandbox state; above it, DART [5] de-
PC/EO govern what may re-execute; FD/CO govern the                 cides when a mechanically possible rollback is semantically
interrupt lifecycle; CV governs what may be persisted; RD —        admissible. Neither asks whether the primitives themselves
motivated by an ordering defect we reported in LangGraph’s         keep their promises. Consent-integrity work [6] binds an
synchronous durability mode (issue #8039) — requires the           approval to the content of the action; FD/CO govern the
recovery decision to be a function of durable state. The           approval lifecycle. Concurrent framework-testing work [7]
property set predates the measurements (Section 3.4).              searches for bugs; we define the contract such bugs violate,
    (2) A machine-checked model (Section 4). A TLA+                measure conformance, and provide a reference implemen-
module with six fault switches, each modeling a violation          tation with a machine-verified model. To our knowledge
class observed in a deployed framework. TLC verifies the           no prior work combines an explicit resume contract, a
reference configuration against all six properties (87 states      machine-checked model, and cross-framework conformance
generated, 59 distinct, no error) and produces a depth             measurement.
4–6 counterexample per single-fault configuration. A per-              What is and is not claimed. Because the sections below
invariant matrix — every fault against every property, 39 runs     qualify each claim where it is made, the scope is collected
— maps each fault’s full violation footprint; the footprints       once here. Proved: the FD–CO impossibility without a dis-
are discovered, not stipulated, and the runs whose entire          criminator (Lemma 1); independence of EO, PC, FD, CV, and
state space stays clean are exactly the separating models          RD from the conjunction of the others, and CO’s structural
Section 3.4 needs.                                                 dependence on EO (Proposition 1), each witnessed by a
    (3) A deterministic conformance harness and cross-             model checked exhaustively at stated bounds; and the
framework study (Sections 5–6). Every probe is a pure-             reference conjunction itself, TLAPS-discharged unbounded
Python protocol sequence over framework persistence                over every constant assignment satisfying the module’s
APIs — no LLM calls, no timing windows; crashes are                assumptions (Sec. 9). Machine-checked: the six properties over
exception-based in the matrix and replicated under a barrier-      the reference model’s full reachable space, re-checked at
synchronized SIGKILL (probe 133) — with process-local              the scaled bounds of Table 2; the per-invariant fault matrix
effect counters, cross-checked on the durable-backend probes       at both bound sets; the independence witnesses. Measured:
by an on-disk external ledger. On the current releases (Lang-      conformance on the probed paths of five frameworks at
Graph 1.2.9, LlamaIndex Workflows 2.22.2, CrewAI 1.15.2,           pinned versions, with the effect oracle a durable cross-process
pydantic-graph 1.107.1, AutoGen AgentChat 0.7.5) the study         ledger. Verified: R EMIT’s recovery-decision core, an executable
finds: a live fork violation and a now-silent validity violation   function line-identical to the shipped one under a CI gate;
in LangGraph on all three checkpointer backends including          the EO admission and PC/CV commit cores as verified
live PostgreSQL; re-execution of completed effect-bearing          executable twins bridged to the shipped implementations
methods under checkpoint restore in CrewAI, against the            by an exhaustive differential suite (Sec. 7.3) — not the
feature’s written claim; documented at-least-once prefix           composite package, and no refinement to the compiled binary.
replay in LlamaIndex Workflows; a crash that defeats               Not claimed: minimality or completeness of the property
pydantic-graph’s own resume entry point; loud rejection of         set; prevalence rates for any violation; that the probed
tampered state in AutoGen AgentChat, alone among probed            frameworks represent the ecosystem; that any framework
frameworks; every incomplete persistence boundary licens-          fails a property it is not measured on.
ing re-execution of completed work (probe 160); consume-
once holding sequentially and failing under cross-process
                                                                   2     T HE R ESUME P LANE AND I TS F RAGMENTATION
delivery (probe 159); and no two probed frameworks sharing
a conformance profile. Two probed LangGraph behaviors              2.1   Primitives
(#7361, #6792) shipped as 1.1.x regressions and are fixed in       We use resume plane for the subsystem of an agent framework
1.2.9 — absent a stated contract, semantics drift even within      that (i) durably records execution progress (checkpoints),
one framework.                                                     (ii) parks a run pending external input (interrupts), and
    (4) A repair path with a verified model, shipped (Sec-         (iii) continues a run from durable state (resume), whether
tion 7). R EMIT is a reference resume sequencer and append-        after an interrupt, a crash, or an explicit restore. In
only effect ledger beneath existing checkpointer interfaces        LangGraph the plane is the checkpointer (InMemorySaver,
                                                                                                                                                 3

                              TABLE 1                                                DART [5]: rollback admissibility over primitives
  Documented resume discipline for completed work, per framework                   (committed downstream consumers, effect policies)
(mechanism a practitioner would use for durable human-in-the-loop or
 crash resume). “Stated” quotes or paraphrases the framework’s own
      documentation; Section 6 tests whether behavior matches.                            This paper: the R ESUME C ONTRACT
                                                                               PC / EO / FD / CV / CO / RD over the framework resume API
                                                                                      (checkpointers, interrupts, resume commands)
Framework               Stated discipline for completed work on
(mechanism)             resume
                                                                                      Crab [4]: OS-level sandbox checkpoint/restore
CrewAI 1.15.2           Exactly-once: restore “resume[s] without re-                       (filesystems, processes, microVMs)
(Checkpoint             running completed work” [1].
Config)
LlamaIndex              At-least-once for step prefixes: the runtime     Fig. 1. Layer positioning. Adjacent systems assume the framework
Workflows 2.22.2        replays the step when the event arrives; users   resume primitive is sound; this paper specifies and tests that assumption.
(wait_for_event +       must “make any preceding work safe to
Context                 re-execute” [2]; in-progress steps restart on
serialization)          restore [9].
                                                                         2.4    Layer positioning
LangGraph 1.2.9         Exactly-once for task bodies via memoiza-
(@task +                tion of completed task results across re-
                                                              Figure 1 places the contract between the two strong recent
checkpointer)           sume; graph-node semantics are checkpoint-
                        granular [8].
                                                              systems in the recovery space. Crab [4] operates below the
                                                              framework API: an eBPF-instrumented host runtime that
                                                              checkpoints OS-visible sandbox state, and whose deployment
                                                              machinery synthesizes cached LLM responses so a restored
SqliteSaver, PostgresSaver) plus interrupt() and
                                                              agent does not replay completed actions — an implicit
Command(resume=...), addressed by (thread_id,
                                                              acknowledgment, at another layer, of the property this paper
checkpoint_id);          the    persistence  documentation
                                                              names EO. DART [5] operates above the API, certifying
gives invocation with a prior checkpoint_id two
                                                              when a rollback is admissible under committed downstream
readings — branch-creating time travel (“fork the
                                                              consumers. Both take the primitive’s own semantics as given;
graph state at arbitrary checkpoints”) and replay with
                                                              the contract layer asks the prior question: is the primitive
interrupts re-triggered [8]. In LlamaIndex Workflows
                                                              sound? Mature recovery disciplines surround this layer and
the    plane     is   Context.to_dict()/from_dict()
                                                              are positioned in Section 8; none specifies or measures the
plus       the      wait_for_event          idiom       with
                                                              agent-framework resume API itself.
InputRequiredEvent/HumanResponseEvent.                     In
                                                                  Comparability and reading guide. Per framework we probe
CrewAI it is @persist flow-state persistence and, since
                                                              the officially documented mechanism for durable human-in-
the checkpointing feature, CheckpointConfig with
                                                              the-loop or crash recovery (the artifact’s selection manifest
Flow.from_checkpoint.
                                                              records adoption figures and retrieval dates), instantiating
                                                              the same abstract workflow on each plane — gate a non-
2.2 Three frameworks, three written semantics                 idempotent effect on a human decision, crash after a durable
Table 1 summarizes what each framework’s own documen- step — so divergence between matrix rows is precisely the
tation says about the central question — does completed hazard a porting developer inherits. Documented semantics
work re-execute on resume? — for the mechanism a practi- (this section) and measured behavior (Section 6) are kept
tioner would reach for, and the statements are mutually distinct by the classification rule of Table 5 note b. Longi-
incompatible: CrewAI’s checkpointing claims completed tudinal depth follows behavioral richness: LangGraph is
work is skipped; LlamaIndex Workflows documents that swept across five releases; the remaining headline cells are
step code before a durable wait replays and that in-progress release-swept in the artifact (results/sweep/, release-date
steps restart on restore [9]; LangGraph memoizes completed receipts): six CrewAI releases spanning 2026-04-08 to 2026-07-
@task results. A developer porting a side-effecting workflow 24, the CheckpointConfig divergence present at every release
between frameworks silently crosses from an exactly-once where the restore path exists — coeval with the feature;
regime into an at-least-once regime with no type error, no three LlamaIndex Workflows and three pydantic-graph 1.x
warning, and no named property to consult.                    releases, the parallel 2.x line no longer exposing the probed
                                                              module. Stable violations under rapid release churn: nothing
                                                              converges toward an implicit norm.
2.3 Version stability of the violations
The LangGraph probe executed across five releases — 1.0.5,
1.1.0, 1.1.3, 1.1.10, 1.2.9 — to separate stable violations from
                                                                         3     T HE R ESUME C ONTRACT
transient regressions. The fork violation (#6663) and the                Design principles. The property set is not a bug taxonomy
silent-persistence violation (#6491 class) reproduce at every            ordered after the fact; they answer, in order, the questions
tested version: stable properties of the resume plane across             any caller who needs deterministic resume semantics — any
a year of releases, not regressions awaiting a patch. For                caller gating non-idempotent effects on the plane — must
#7361 and #6792, which the trackers report as regressions                be able to answer when crossing an interrupt/crash/resume
in narrow windows, the sweep finds current-and-adjacent                  boundary: where does execution resume (PC)? do effects repeat
versions clean; those are relied on only as documented                   (EO)? what does a fork mean (FD)? what may be persisted
history, never as our own measurements. The evidence file                (CV)? what consumes authority (CO)? is recovery a function
results/regression/ records every cell.                                  of durable state alone (RD)? — plus, one layer down, how is a
                                                                                                                                          4

fork asked for (FI, a protocol obligation). The observed failures        decision, deterministic by construction of the gate; model or tool
of Section 6 instantiate these questions; they did not generate          nondeterminism downstream of the decision is outside f , so FD is
them.                                                                    well-defined for nondeterministic agents.
                                                                         Property 4 (CV: Checkpoint validity). Every persisted check-
3.1   Abstract model                                                     point record satisfies the state schema: a write that would persist
Definition 1 (Resume plane). A run executes tasks 1..N in                schema-invalid state is rejected with an error, not stored.
order; task t carries one non-idempotent external effect et . One task   Property 5 (CO: Consume-once). Two clauses, named here
IP is interrupt-gated: its effect fires only after a resume value        because the rest of the paper quantifies over them separately. (CO-
v ∈ V is consumed. Completing task t appends a checkpoint                c, consumption count) An interrupt is consumed by at most one
record ⟨t, valid ⟩ to a durable log and advances the durable             resume. (CO-e, effect inertness) A resume without fork intent
frontier F to max(F, t). A crash erases volatile state; a recovery       addressed to a completed run or an already-consumed interrupt —
chooses a continuation point as a function of the durable log. A         including byte-identical re-delivery of a prior resume — is inert
resume addressed to the interrupt checkpoint carries a value vk          with respect to effects.
and yields a branch outcome ok .
                                                                       The clauses are not interchangeable, and the distinction is
    The model deliberately abstracts framework detail — load-bearing twice below. CO-e is violated when a stray
graph supersteps, event queues, flow listeners — to the delivery fires something; CO-c is violated when authority is
observable interface a caller programs against: effects, check- taken twice, whether or not a second effect follows — a gate
points, interrupts, resume values, outcomes, recovery de- that serves its effect idempotently from the durable record
cisions. One gated task is the minimal nontrivial instance; can consume one human approval twice while the effect
composition across gates and parallel branches is treated count stays at one, which leaves the approval trail wrong
under Scope at the end of this section and probed in Section 6. and the effect ledger right. The cross-process failure this
Each property below is stated over that interface, so verdicts paper measures (probe 159) is a CO-c failure that happens
are decided from surface observables alone; probes that also to break CO-e; the model of Sec. 4 formalizes CO-e only,
instrument beneath it (adversarial savers, executor traces, the and Sec. 3.4 reports what each clause is independent of.
source audit) localize mechanisms, never decide cells, and
PC’s log-derivation clause is certified, on any finite probe set, Property 6 (RD: Recovery determinism). The recovery decision
through its observable consequences — state equality with (which tasks to skip versus re-execute) is a function of durable state:
the effect record intact — not by observing provenance.                two recoveries from identical durable logs make identical decisions.
                                                                       Remark 1. CO is the effect-restricted corollary of EO at the gated
3.2 Properties                                                         task, named separately because the interrupt lifecycle is where
                                                                       deployed systems concentrate human authority, approval trails
Property 1 (PC: Prefix continuation). Recovery continues
                                                                       are audit subjects, and a framework can satisfy CO while failing
from the durably recorded frontier state: execution after recovery
                                                                       EO elsewhere, as the conformance matrix shows. (The dependence
begins in the state SF recorded at frontier F , or in a state re-
                                                                       analysis is Section 3.4, which also states the set’s non-completeness
derived deterministically from the durable log alone that equals
                                                                       and names candidate seventh properties; we flag the relationship
SF . Memoized replay conforms: prefix code may re-run during
                                                                       here so no independence assumption is carried for three pages.) RD
recovery provided every prefix effect is served from the durable
                                                                       is motivated by an ordering hazard we reported in LangGraph’s
record (so EO is preserved) and the re-derived state is a pure
                                                                       synchronous durability mode (#8039): a completed task’s pending
function of the log. Re-deriving state from initial values, or
                                                                       writes and the superseding checkpoint go to a shared executor
traversing the prefix against live effects, violates PC. Equality here
                                                                       with no ordering barrier, so a crash between them can leave either
is observable-state equality, and observable state is, throughout
                                                                       of two durable states. Two obligations travel under RD’s name.
this paper, exactly what is retrievable through the framework’s
                                                                       Property 6 as stated is determinism proper — identical durable
public state-inspection API by the caller and by subsequent tasks;
                                                                       logs, identical decisions — which the model checks (Listing 1) and
internal representation is unconstrained.
                                                                       probes 118 and 128 test directly, each recovering twice from one
Property 2 (EO: Effect exactly-once). For every task t, effect et committed crashed log (sha256-verified byte-identical copies on
fires at most once on a branch across any sequence of interrupts, the durable backend), decisions identical in every pair. The #8039
crashes, and resumes (as a safety invariant EO is at-most- hazard additionally demands order-invariance: a crash inside
once; the “exactly” is supplied by pairing with the liveness the unbarriered window is compatible with more than one legal
obligation of Sec. 4). EO constrains observable external effects log, and a recovery deterministic in each yet divergent across the
only, never message delivery: an effect that commits while its two leaves post-crash behavior unreproducible. Probes 118, 128,
acknowledgment is lost counts as fired, and the retry discipline and 136 test that stronger obligation on the realized crash pair;
for lost acknowledgments is the idempotency-key composition of the Verus recovery core (Sec. 7) covers the completed window
Remark 4.                                                              only, not the crash-truncated pair — which is how LangGraph’s
                                                                       measured invariance coheres with its crash-path EO violation.
Property 3 (FD: Fork determinism). If resumes carrying fork
                                                                       RD’s inclusion predates any observed failure.
intent (Definition 2) with values v1 , . . . , vm are addressed to
the same interrupt checkpoint, then each branch outcome satisfies
ok = f (vk ) for the branch semantics f ; in particular vj ̸= v1 ⇒ 3.3 Fork intent: making FD and CO jointly satisfiable
oj ̸= o1 whenever f is injective. Here f is the decision function: FD and CO constrain behavior at the same wire point —
the framework’s routing of the supplied value into the gated branch a second resume addressed to a consumed interrupt — in
                                                                                                                                        5

opposite directions: FD demands the new value be honored                FI hold and the lemma inapplicable; the impossibility concerns
on a new branch, CO demands a stray re-delivery be inert.               protocols whose accepted traffic carries no such bit — the probed
Without a discriminator the two are jointly unsatisfiable on            LangGraph surface. And the construction presupposes both intents
identical traffic, so the contract does not leave “explicit fork”       are admissible: an environment that excludes duplicates or forbids
undefined:                                                              same-value forks escapes by emptying one side — a fact about the
                                                                        environment, not the responder; on the probed local APIs both
Definition 2 (Explicit fork). A resume carries fork intent iff
                                                                        arrive as caller invocations.
it bears a branch discriminator distinguishing it from re-delivery
of a prior resume: a distinct resume ordinal, an explicit fork flag,        Lemma 1 is deliberately not an explanation of Lang-
or an address the framework’s own documentation designates as           Graph’s defect. Its role is prior: it is FI’s necessity in
branch-creating.                                                        theorem form — demanding FD without demanding FI
                                                                        would be incoherent. LangGraph is the harder second case:
Property 7 (FI: Fork-intent expressibility). The resume API
                                                                        its documentation gives the explicit-checkpoint address two
must make the discriminator of Definition 2 expressible on the wire.
                                                                        readings — branch-creating time travel and replay (Sec. 2) —
FI is a protocol obligation on the interface rather than a behavioral
                                                                        so the address meets Definition 2 clause 3 on the first reading
property of a trace; an API that cannot express fork intent forces
                                                                        and fails to discriminate on the second; FI holds on at most
implementations to resolve retry-versus-fork by guessing, and
                                                                        one documented reading, the dual documentation is itself an
cannot satisfy FD and CO simultaneously. FI is numbered with
                                                                        instance of the gap FI names, and the loop serves the recorded
the properties because the conformance report needs a column for
                                                                        value under either reading (FD fails) — a factorization that
it, and it is deliberately not model-checked: it constrains what the
                                                                        still localizes the defect to the serving logic, exactly the
API can say, not what traces do.
                                                                        seam probe 134’s repair exploits. Sufficiency is claimed only
Definition 3 (Intent-indexed FD and CO). Let an intent                  constructively: with a discriminator present, a responder
labeling assign to each resume w an exogenous label ι(w) ∈              keying branches on it satisfies FD jointly with same-value
{FORK, RETRY} — the caller’s intent, not a field of w. FDι holds        replay idempotence — machine-checked at model level (LGF-
of a responder iff every FORK-labeled w is honored on a fresh branch    B, Table 2); LGF is an outcome-serving model with no effect
whose gated effect fires exactly once; COι holds iff every RETRY-       state, so CO’s effect half is exercised instead by R EMIT’s
labeled w is effect-inert. Where the wire carries a discriminator, ι    per-branch ledger (Sec. 7.3).
is recoverable and these coincide with FD and CO; where it does             FI is what R EMIT’s ⟨checkpointId , resumeIndex ⟩ keying
not, they are strictly stronger. The matrix of Sec. 6 reports FD and    supplies and what the probed LangGraph protocol lacks:
CO only: no probe can supply ι either.                                  neither Command(resume=v) nor the resume-map form
                                                                        carries a retry/fork bit, and the address the probe uses
Lemma 1 (FD–CO incompatibility without a discriminator).
                                                                        — a prior checkpoint_id — is the one the persistence
On a wire protocol whose resumes carry no branch discriminator —
                                                                        documentation presents as the branch-creating time-travel
none in the accepted traffic, transport metadata included; Remark 2
                                                                        primitive [8]. The ✗ verdict in Section 6 therefore stands under
delimits the scope — no responder — deterministic or randomized
                                                                        either documented reading, while FI names the protocol gap
— satisfies both FDι and COι (Definition 3) on all traffic the
                                                                        that made the ambiguity possible.
protocol admits, for any intent labeling ι under which both labels
are realized.
                                                                        3.4 Partial independence (interface-relative) and empiri-
Proof. Let interrupt c be consumed with recorded value                  cal necessity
v1 , branch outcome o1 = f (v1 ), the branch’s effect fired
                                                                        Whether six is the right number is answered by a per-
once. Construct two executions identical in durable state,
                                                                        invariant fault matrix — each ResumeContract fault model
wire trace, local schedule, and environment inputs (clocks
                                                                        checked against every property, plus the state-rebuild mod-
included) up to and including the arrival of w = resume(v1 )
                                                                        ule; 39 TLC runs, Table 3 — whose clean rows are precisely
addressed to c: in (a), w is a transport duplicate, for which CO
                                                                        the separating models a logical-independence argument
requires effect-inertness; in (b), w is a caller-requested fork
                                                                        requires, completed by a companion module supplying the
re-answering v1 , for which FD with per-branch EO requires
                                                                        three witnesses the deployed-mechanism switches entangle
a fresh branch whose gated effect fires exactly once. Every
                                                                        (21 further runs, R10_Separations.tla, every verdict,
input the responder can condition on is identical across
                                                                        state count, and counterexample depth identical across
(a) and (b); only the caller’s intent, which by hypothesis
                                                                        the two environments). The 39-cell matrix is re-derived
the wire cannot carry, differs. A deterministic responder
                                                                        at the R8 constants with the same verdict in every cell
produces one behavior for both and violates one requirement.
                                                                        (receipts in results/tla/independence_r8/), so the
A randomized responder induces one distribution for both;
                                                                        separations are not an artifact of the small configuration:
the two required behaviors are disjoint events, so its success
                                                                        counterexamples deepen as the space grows — the fork
probabilities sum to at most one and on at least one intent it
                                                                        fault from depth 5 to 8, double consumption from 6 to 13
errs with probability ≥ 1/2. Contradiction. (The construction
                                                                        (single-worker minimal depths, receipts in results/tla/
is an indistinguishability argument: the two executions are
                                                                        singleworker_20260806/; the matrix files log 16-worker
observationally equivalent to the responder, differing only in
                                                                        abort-time traces, which can run deeper) — while every clean
an exogenous label the wire cannot carry.)
                                                                        cell stays clean over a state space four orders of magnitude
Remark 2. Scope. Transport metadata is inside the construction:         larger. Three scope words govern the title: the separations
any request id, retry token, or idempotency key the accepted traffic    are interface-relative — established over the vocabulary of
exposes is a discriminator in the sense of Definition 2, making         Definition 1, the domain over which the contract itself is
                                                                                                                                              6

stated, and the relativity every independence claim has to                conservativity holds by construction — the racer disabled, the
its signature — witness-complete (each witness fully explored             counter a function of the existing trace, the action alphabet R0’s —
at both bound sets, every holding cell at R8 exhausting 1.0–              with the 87/59 identity as that construction’s executable check; with
1.4×106 distinct states against the reference run’s 59–396),              the race enabled and the gate serving its effect idempotently from
and partial, because one dependence (CO on EO) is structural.             the durable record, TLC completes over 127 generated / 95 distinct
    One distinction carries the proof-theoretic weight and is             states with TypeOK, EO, PC, FD, CV, CO-e, and RD holding and
stated once, here. A separation claim is the non-implication              CO-c violated at depth 5, and the same verdict pattern re-derives
S ⊬ P , and non-entailment is proved, in any logic, by                    at wider bounds (8,191 distinct states, counterexample depth 6).
exhibiting one model of S∧¬P : a structure over the contract’s            This matters beyond bookkeeping: CO-c is the clause the measured
interface in which the conjunction holds and the target fails.            cross-process failure breaks, and until it is carried as an invariant
A single fully checked finite witness is such a model and                 the model cannot express the paper’s own headline composition
settles the claim outright. TLC’s exhaustive breadth-first                result. The CO-e implication is one-directional, with an in-model
enumeration of a witness’s reachable space is a complete                  separating witness for the converse: the PrefixReplay model
verification of that witness — there is no “beyond the                    — recovery restarts from task 1 while the gated task’s effect is
bound” for the structure its constants define — so the non-               served from the durable record, the memoized-gate discipline of
implications of Proposition 1 are established by exhibition,              LangGraph’s measured crash path — violates EO (at a non-gated
never sampled, and the R8 re-derivation is corroboration                  task) and PC while FD, CV, CO, and RD hold over its entire
that the witnesses are not degenerate configurations, not the             reachable state space (TLC complete, 287 generated / 183 distinct
source of their validity. What is genuinely bound-relative                states); the gate-exercising crash-path trace itself is witnessed by
is the universal side: that the reference semantics satisfies             the shipped R9W configuration (consume; crash at frontier IP;
the conjunction (R0/R8) and that each fault’s discovered                  replay; gate served from the record). (v) RD, PC, and EO are
footprint is complete are claims over all behaviors, exhaustive           each independent of the conjunction of the other five, witnessed
at the stated constants and silent beyond them. TLAPS                     by a companion module (R10_Separations.tla) whose three
now discharges the first unbounded (Section 9); footprint                 switches are effect-safe or control-safe variants of mechanisms
completeness retains exactly this bound-relative status, and              this study observed, each constructed so that exactly one property
no TLAPS step is needed to make the exhibited witnesses                   fails while the other five hold over the entire reachable state space
proofs.                                                                   (TLC complete, no error, at the reference bounds): Regate — at
                                                                          equal durable state one recovery continues past the consumed
Proposition 1 (Partial independence, machine-checked).                    gate and another re-arms it, the re-consumption served from the
Over the interface of Definition 1, as formalized in Section 4:           durable record, so the recovery decision differs (RD ✗) with no
(i) FD is logically independent of the conjunction of the other five      effect fired twice and no completed task re-executed; Rebuild
properties: the ForkIgnore model satisfies EO, PC, CV, CO,                — deterministic restart with the working state taken from initial
and RD over its entire reachable state space at the reference bounds      values rather than re-derived from the log, every prefix effect served
(TLC complete, no error) while violating FD. (ii) CV is likewise          from the record (PC ✗); and Redeliver — at-least-once re-issue
independent, witnessed by InvalidPersist — a structurally                 of the durable frontier task’s effect while control resumes past it
easy separation, and deliberately so: no other invariant reads the        and the gated task is excluded (EO ✗). Within the original switch
validity bit because the contract states CV over the write, so its in-    set none of the three separates, because nondeterministic recovery’s
model independence is definitional, while the coupling that matters       footprint is {EO, PC, CO, RD} — its replay branch re-executes
in deployment — invalid state consumed downstream — is an                 the prefix — and that entanglement is itself the finding recorded
empirical question the downstream-consequence probe answers               below. In sum: independence from the conjunction of the other
(probe 150, Sec. 6). (iii) PC is implied by no single property            properties is established for EO, PC, FD, CV, RD, and CO-c; CO-e
in the set, on non-vacuous witnesses: EO does not imply PC                alone is definitionally dependent, by (iv).
— the state-rebuild model (R7) satisfies EO over its entire state
space while violating PC — and none of FD, CV, CO, or RD                      Two comments. CO is retained as a named property
implies PC — the PrefixReplay model of (iv) violates PC                   despite (iv) because it isolates a distinct production mecha-
while all four hold, non-vacuously, over its entire state space. R7’s     nism — stray duplicate delivery versus crash replay — and
remaining cells are vacuous (machinery absent); vacuous cells             the framework data exhibit the same one-way structure:
separate nothing and Table 3 labels them as such. (iv) CO splits,         LangGraph 1.2.9 fails EO on the crash path while CO holds
and only one clause is dependent. CO-e is not independent                 on the same configuration (Table 5). And the entanglement
of EO: as formalized in ResumeContract.tla the invariant                  (v) records is itself a finding: recovery indeterminism whose
is effects[IP] ≤ 1, which is EO restricted to the gated task, so          branch includes replay drags replay’s damage along —
EO ⇒ CO-e and every CO-e violation is an EO violation — the               exactly what the CrewAI restore receipt exhibits live —
matrix confirms this, and we state plainly that this implication is       which is why the witnesses are effect-safe variants: they
a fact about the two formulas rather than a discovery: it would           show logical independence, not that any framework fails one
hold whatever the transition relation did. CO-c is independent of         property at a time.
the conjunction of all six others, including CO-e. The witness                The empirical side carries its own weight. For each of EO,
is a lost-update model (R11_ConsumeCount.tla, receipts in                 FD, CV, CO, and the liveness obligation there is an observed
formal/tla/consumecount/) that carries a consumption                      framework path on which that property fails while the others
counter and admits a second racer which reads the parked                  hold on that path; every observed PC violation (CrewAI’s
interrupt’s waiting flag before the first racer’s clearing write lands.   rebuild-from-initial restore) co-occurs with an EO violation,
Its reference cell reproduces R0 exactly (87 generated / 59 distinct);    so at framework level PC’s necessity is claimed jointly, with
                                                                                                                                           7

the model-level separation in Proposition 1(iii). Three claims, guarantee, never message delivery); EO/CO restate the application-
kept distinct: (i) empirical necessity, per the observed paths level idempotency discipline Helland argues is unavoidable [11],
above; (ii) formal partial independence — Proposition 1; [12]; PC’s memoized-replay clause is deliberately the discipline
(iii) no theorem of minimality, completeness, or sufficiency is formalized for Durable Functions [13] and practiced by event-
claimed. The set is not reverse-engineered from the failure sourced actors [14], so replay-based recovery conforms to PC while
list: RD entered from the recovery question with no observed CrewAI’s rebuild-from-initial restore does not; RD is determinism
failure then or now. CO’s statement is likewise unchanged of the recovery function in the sense of rollback recovery [15]. The
from the pre-measurement set; what measurement sharpened contribution is not these notions but their assembly into a checkable
is which path evidences it: the sequential stray resume that obligation set for an API where today they are unstated, divergent,
motivated the property is refused by the probed plane, and violated.
while the same delivery from a second process is admitted
(probe 159), so the property earns its empirical necessity on
the concurrent path.                                             4 M ACHINE -C HECKED M ODEL
     Why six — and could there be a seventh? One property The object of verification throughout this section is the
per question a caller must be able to answer across the specification, not any framework: TLC exhausts the reference
boundary, with FI the protocol precondition the fork question semantics and its fault variants, while the LangGraph-
needs. Merging is blocked by the separations above; splitting derived module of Section 4.3 is a separately flagged, expert-
further is unmotivated by any observed mechanism. Candi- established abstraction. The model inherits the contract’s
date sevenths are named as scope exclusions: cross-version scope exclusions (Section 3).
checkpoint-migration validity, an effect-visibility ordering
obligation, and loud-versus-silent disposition of discarded 4.1 The TLA+ module
resumes (Section 6 flags the last as a spec-level gap).
                                                                 We formalize Definition 1 and Properties 1–6 as a TLA+
     Scope and composition. Definition 1 linearizes: the prop-
                                                                 module, ResumeContract.tla (251 lines, in the arti-
erties are stated per causal chain, and a DAG’s parallel
                                                                 fact), paired with a consumption-counting companion,
branches are each such a chain; sequential composition
                                                                 R11_ConsumeCount.tla, that carries the CO-c invariant
across gates and concurrent fan-out at one superstep are
                                                                 the base module’s atomic Consume cannot express (the
both probed (Sec. 6, probes 138, 141), while deeper nesting
                                                                 pairing is motivated where that gap is stated, below). State
and multi-checkpointer fan-in remain future work. Invisible
                                                                 comprises the program counter, per-task effect counters, the
speculative execution that never surfaces through the public
                                                                 checkpoint log, the durable frontier, the interrupt flag, the
state API is outside the contract. CV is per schema version,
                                                                 consumed value, the sequences of fork values and fork
and checkpoint migration is a named exclusion: records
                                                                 outcomes, the crash count, the recovery history (pairs of
valid under schema v are not CV subjects under v+1, so
                                                                 durable frontier and decision), and a prefix-regression flag.
evolution requires an explicit migration step before any
                                                                 Actions are ExecTask, EmitInterrupt, Consume(v),
resume — a plane that silently auto-migrates reintroduces
                                                                 ForkResume(v), CrashRecover, and ExtraResume. The
exactly the hazard CV names (R EMIT’s gate answers relative
                                                                 six properties are state invariants; the listing shows four of
to the validator supplied at load). CO’s resume identity is
                                                                 them verbatim.
the checkpoint address plus payload; transport metadata is
excluded. The properties are not claimed orthogonal — a CV1 EffectExactlyOnce ==
failure undermines the addressability CO depends on — so2           \A t \in Tasks : effects[t] <= 1
                                                               3 ForkDeterminism ==
conformance is reported per-property, never as a single bit. 4      \A k \in 1..Len(forkOuts) :
                                                                     5       forkOuts[k] = f(forkVals[k])
Remark 3 (What the conjunction buys, informally). Under6                 CheckpointValidity ==
Definition 1: EO and CO fix effect multiplicity, PC the continua-7         \A k \in 1..Len(ckpts) : ckpts[k].valid
tion state, RD the recovery choice, CV log integrity, and FD with8       RecoveryDeterminism ==
                                                                     9     \A i, j \in 1..Len(recHist) :
FI the branch outcomes — jointly, the caller-visible outcome is a10          recHist[i].dur = recHist[j].dur
function of the inputs, the durable log, and the supplied decisions.11         => recHist[i].dec = recHist[j].dec
Orientation, not a theorem; R0/R8 machine-check the conjunction
                                                                         Listing 1. Contract invariants in ResumeContract.tla (excerpt).
over the model.
Remark 4 (Fork and exactly-once). EO is per-branch by design:                Six Boolean fault switches select the reference semantics
a fork is user-requested duplication of downstream execution, so         or one observed violation class — each switch transcribes
the gated effect legitimately fires once per requested branch. The       a deployed mechanism, not a negation of a target property,
contract forbids duplication nobody asked for — re-execution             and Table 3 then measures what each mechanism actually
within a branch across crash or resume (EO), and effects fired           breaks: FaultReplay (recovery restarts from task 1 over
by resumes that requested nothing (CO). A deployment for which           restored state — the CrewAI restore discipline, and the
even requested branch effects are unacceptable composes FD with          #7361 regression class), FaultForkIgnore (a second re-
an idempotency key at the effect itself; the contract governs the        sume at the same checkpoint is answered with the first
plane, not the payment processor.                                        branch’s outcome — #6663), FaultInvalidPersist (a
                                                                         schema-invalid completion record is persisted silently —
Remark 5 (Relation to classical semantics). EO restricted to             the #6491 class), FaultNondetRecovery (skip-versus-re-
crash recovery is the workflow analogue of exactly-once processing       execute unconstrained at equal durable state — #8039),
(state-management, not delivery [10]; throughout, EO is an effect        FaultDoubleConsume (a stray resume on a completed
                                                                                                                                                            8

                                  TABLE 2                                                                         TABLE 3
 TLC verification matrix for ResumeContract.tla (TLC 2026.04.09,                 Per-invariant fault matrix: each single-fault model checked against each
 rev. 389440f; every fault row single worker, so counterexample traces                    property individually (one TLC run per cell; 36 cells on
     are BFS-minimal and deterministic across hosts (R8-F receipt:                ResumeContract.tla with the corresponding R1–R5/R9 constants,
 results/tla/singleworker_20260806/); the clean scaled row                       plus the R7 state-rebuild module row — EO, PC, and the type invariant
 R8 ran 4 workers, which cannot alter a completed exhaustive search’s              checked; the fork/validity/consume/recovery machinery is absent, so
  totals; states = generated/distinct; CE = counterexample depth). R0                those cells are structurally vacuous — 39 runs total, receipts in
  checks all six invariants; R1–R5 and R9 check the targeted invariant           formal/tla/independence/). ✗ = violated (counterexample depth
under a single fault switch (full per-fault violation footprints: Table 3); R6   in parentheses where recorded); ✓ = the invariant holds over the faulty
checks the liveness obligation under weak fairness; LGF-A/LGF-B check             model’s entire reachable state space (TLC complete, no error). Rows
   the framework-derived model of Section 4.3 with no fault switches;            whose off-target cells are all ✓ are separating models for their targeted
          R9W’s counterexample is the by-design gate witness.                       property; off-diagonal ✗ cells are each fault’s discovered footprint.


Run     Fault switch                Invariant      Result           States; CE      Fault model                EO     PC      FD     CV    CO       RD
R0      (reference)                 all six        ✓ no error      87/59; —         Replay (R1 consts)        ✗ (4)   ✗ (4)    ✓     ✓     ✗ (7)     ✓
R1      Replay                      EO             ✗ violated          7/7; 4       ForkIgnore (R2)            ✓       ✓      ✗ (5)  ✓      ✓        ✓
R2      ForkIgnore                  FD             ✗ violated       10/10; 5        InvalidPersist (R3)        ✓       ✓       ✓    ✗ (5)   ✓        ✓
R3      InvalidPersist              CV             ✗ violated          8/8; 5       NondetRecovery (R4)         ✗       ✗      ✓     ✓       ✗      ✗ (4)
R4      NondetRecovery              RD             ✗ violated       10/10; 4        DoubleConsume (R5)        ✗ (6)    ✓       ✓     ✓     ✗ (6)     ✓
R5      DoubleConsume               CO             ✗ violated       20/20; 6        PrefixReplay (R9)         ✗ (4)   ✗ (4)    ✓     ✓      ✓        ✓
R9      PrefixReplay                EO             ✗ violated          7/7; 4       StateRebuild (R7 mod.)     ✓      ✗ (3)   (vacuous: machinery absent)
R9W     PrefixReplay                gate witness   witness CE       45/35; 7
R6      (reference)                 liveness       ✓ no error      87/59; —
LGF-A   (as implemented)            FD             ✗ violated          5/5; 3
LGF-B   (fork-keyed)                FD + idem.     ✓ no error        7/7; —      PC, and CO; injected recovery nondeterminism drags replay’s
R8      (ref., scaled)              all six        ✓ no err.  14.7M/7.4M; —      damage plus RD; only the fork and validity mechanisms
R8-F    ForkIgnore (sc.)            FD             ✗ violated       68/68; 8
                                                                                 break exactly one property each. If the switches merely
                                                                                 stipulated their targets, every off-diagonal cell would be
                                                                                 clean; four rows are not. To the demand for independence, the
run re-fires the gated effect — the #2315 class [16]), and
                                                                                 clean rows deliver it: ForkIgnore and InvalidPersist
FaultPrefixReplay (recovery restarts from task 1 while
                                                                                 are full separating models (Proposition 1), the state-rebuild
the gated task’s effect is served from the durable record —
                                                                                 row separates PC from EO, PrefixReplay separates EO
memoized-gate prefix replay, the LangGraph 1.2.9 crash-path
                                                                                 from CO in the only possible direction, and the one pair that
class of probes 118/133; added after those measurements).
                                                                                 cannot come apart is reported as the structural implication
A shipped witness configuration (R9W) checks the negation
                                                                                 it is. The full matrix replicated across hosts with identical
of the gate-exercised state, with a recHist conjunct forcing
                                                                                 verdicts, depths, and state counts. The invariants read as
consumption before the crash; TLC’s depth-7 counterexample
                                                                                 one-liners by design; the proof burden lives in the six
is the memoized-gate crash path realized end to end — the
                                                                                 actions whose every interleaving must preserve them, in
interrupt is consumed (frontier reaches IP), the crash recovers
                                                                                 ResumeContract.tla.
from dur = IP, prefix replay re-executes task 1 (the EO
                                                                                      The liveness row closes a vacuity hole: a framework that
violation), and the replayed pass crosses the gate with the
                                                                                 refuses every resume satisfies all six safety invariants, so the
gated effect served from the durable record, effects[IP]
                                                                                 contract pairs them with EventuallyCompletes under
unchanged on the trace.
                                                                                 weak fairness, verified on the reference configuration (and
                                                                                 violated in spirit by a deployed framework whose crash
4.2     TLC results                                                              leaves persistence unrestorable, Section 6.4).
Table 2 reports the verification matrix (TLC 2026.04.09,                              The R1 counterexample is worth reading against the live
rev. 389440f, one worker, N =3 tasks, IP =2, |V |=2, at most                     data: execute task 1 (⟨1, 0, 0⟩, frontier 1 durable); crash and
two resumes, one crash — two for the RD run — and                                replay; execute task 1 again (⟨2, 0, 0⟩) — EO violated in four
one stray resume). The bound is a small-scope argument:                          states. Section 6 measures the same arithmetic live in CrewAI:
every property quantifies over per-task phases relative to the                   task 1 persisted, crash in task 2, resume, and the completed
interrupt point and over recorded-versus-supplied values,                        task re-fires, landing the counter on 12 where exactly-once
so three tasks with IP =2 realize every phase relationship                       predicts 11.
the transition relation admits, and two values every equality                         Modeling assumptions and what the checking means. Sched-
pattern; each violating run finds its counterexample at depth                    uler state and message plumbing are abstracted — the
≤ 7 at these bounds; and R8 re-checks the same invariants                        abstraction the properties themselves quantify over. The
at ten tasks over 7.4×106 distinct states, unchanged. Single-                    fault switches inject mechanisms observed in deployed
worker BFS makes every counterexample minimal-depth                              frameworks and Table 3 discovers what each breaks; none
and every number bit-reproducible; reproduce.sh re-                              of this shows the specification captures any framework, a
derives the rows. The reference configuration satisfies all six                  burden that falls on Section 4.3 and the measurements. The
invariants; each single-fault configuration violates its target                  configuration is a dial, not a ceiling: the reference space is
at depth 4–6 (R1–R5); the per-invariant matrix of Table 3 then                   the minimal one in which every property is falsifiable, while
reports each fault’s full violation footprint.                                   R8 (10 tasks, interrupt at 5, 4 values, 5 resumes, 4 crashes, 4
    Table 3 answers two objections at once. To the charge                        extra resumes) passes the six invariants plus TypeOK over
that the fault switches are circular — engineered to violate                     1.47×107 generated / 7.4×106 distinct states at depth 24
their properties — the matrix replies that a switch injects a                    — an exhaustive breadth-first check of the full reachable
mechanism and TLC discovers its footprint: replay breaks EO,                     space at those constants — and the fork fault still yields
                                                                                                                              9

a counterexample at depth 8 under single-worker search. 4.3 A framework-derived model: the fork violation is the
(Workers race to counterexamples on scaled fault runs, so shadow of replay idempotence
only the violated invariant is a stable receipt there; every
depth reported here is a single-worker depth.)                    The fault-switch runs demonstrate that the contract is pre-
    Three scope bounds of the model are stated rather than cise enough to check; they say nothing about frameworks.
discovered. First, the modeled crash is a recovery-decision A second module, LangGraphFork.tla, closes that gap
event: CrashRecover carries the precondition that no inter- for the fork axis. It models LangGraph’s resume path as
rupt is pending, so a crash while the run is parked awaiting an operational abstraction consistent with the persistence
the human is outside this module’s transition relation. That documentation and the reproduced behavior of #6663: a
case is covered empirically by probes 158/158b/158c on all resume value delivered to a (thread, checkpoint) is recorded
three planes that park, and formally by a companion module, as a pending write, and an invocation addressed to a
ResumeContractParked.tla: under durable parking — checkpoint already carrying a resume write replays the
the measured behavior of every plane that parks — all recorded write rather than recording a new one. No fault
six invariants and the liveness obligation hold at both switch exists in the module. TLC discovers the violation: with
bound sets and the fault matrix re-derives with verdicts two invocations supplying ⟨va , vb ⟩, the served outcomes
and depths identical to Table 3; under volatile parking the are ⟨va , va ⟩ — FD violated at depth 3 (LGF-A) — while
six safety invariants hold while EventuallyCompletes is ReplayIdempotence holds throughout. Together that is
violated — safety by deadness, pydantic-graph’s disposition the finding: the recorded-write rule is exactly what makes
(Sec. 6.4), now a model-level counterexample and not only same-value re-invocation idempotent, a designed property,
a measured cell (receipts in formal/tla/parked/, both and exactly what breaks forking — #6663 is not a slip but
environments).                                                    the shadow of a design choice. The repaired algorithm
    Second, fork branches are outcome-level: ForkResume           —  pending writes keyed by (checkpoint, resume ordinal),
records values and outcomes and fires no effects, so Re-          precisely  R EMIT’s branch keying — verifies idempotence and
mark 4’s per-branch accounting is a property of R EMIT’s          fork determinism    together (LGF-B).
ledger (Sec. 7.3), not of this module. Third, and the one that        The  modeled   rule is located in source. The dedup guard
matters, CO-c is not representable here at all: Consume(v)        in InMemorySaver.put_writes            skips only non-negative
clears waiting atomically, so a second consumption of write indices, and the write-index table maps the resume
a live parked interrupt is not a behavior this transition channel to a negative slot (__resume__ 7→ −4), exempting it;
relation admits, and the module carries no consumption the durable savers upsert those channels. The second resume
counter. That is a real gap, not an abstraction choice, because value is therefore durably recorded — under the null task id —
the cross-process failure of Sec. 6 is exactly that second and never consulted: the binding site is task preparation,
consumption; and FaultDoubleConsume is not its shadow, where the scratchpad constructor in pregel/_algo.py
being guarded by pc = NTasks + 1 — a completed run, resolves a task’s resume by precedence (task-recorded first;
the sequential mechanism the probed plane refuses. The null-task only via get_null_resume; resume-map values
companion module R11_ConsumeCount.tla closes it: a appended after the recorded list), so an invocation addressed
consumption counter, CO-c and CO-e as separate invariants, to a checkpoint whose task already carries a consumed
and one extra racer reading the waiting flag before the first resume is served the recorded value regardless of what it
racer’s clearing write lands — probe 159’s two-racer shape, supplied, in every invocation form. The probe data corrobo-
the racer served its own value (FD intact, as measured) rate each clause: the violation is identical under the bare and
and appending no checkpoint (the duplicate invisible in resume-map forms on all three backends (probes 126, 127,
framework state, as measured). Its reference cell reproduces 130); the store dumps show both values durably present with
R0 exactly (87 generated / 59 distinct), the executable check the first served twice; and the fork-keyed saver shim cannot
of a by-construction conservativity (racer disabled; counter a repair it (probe 125) — no saver-level keying can override a
function of the R0 trace). With the race enabled and the gate decision the saver never makes. The module’s recorded-write
idempotent, TLC completes over 127 / 95 states with EO, PC, rule is this precedence at specification granularity, with the
FD, CV, CO-e, RD and TypeOK holding and CO-c violated responsible lines quoted in the artifact:
at depth 5 — the separating witness of Proposition 1(iv).             The mapping is tabulated line for line in Supplement S5,
With the race also firing the effect, the discovered footprint is with the responsible LangGraph 1.2.9 source lines quoted
{EO, CO-e, CO-c} with PC, FD, CV, RD clean, matching in the artifact. The mapping is expert-established, not tool-
probe 159 cell for cell. Both patterns re-derive at wider certified (Section 9 scopes it); probe 134 (Section 7) realizes
bounds (8,191 distinct states, depth 6). The module’s 32- LGF-B’s repair operationally — and the 125/134 matched
cell matrix replicates across two separately provisioned pair is interventional evidence for the mechanism account,
environments and across a JDK major version, so the counts not a correlation: altering the serve decision at the located
are a property of the module and the checker rather than of site flips the verdict, while altering persistence below it does
a toolchain.                                                      not. It is also mechanically exercised: a trace-conformance
    Liveness uses weak fairness only — no action is re- checker (probe 143) transliterates the serve, record, filter,
peatedly disabled and re-enabled in competition, so strong and inertness rules into ∼20 lines and must reproduce the
fairness would add assumptions without theorems — and measured branch outcome of every recorded invocation —
is a progress check, not an availability claim. Division of 8/8 across the four fork/stray protocols; its first run caught
labor: TLC checks the protocol; Verus (Sec. 7) checks R EMIT’s an omitted inertness clause and forced a model correction.
invariants — never validation of the frameworks.                  Evidence for the mapping, not a refinement proof — and
                                                                                                                                           10

consistency with the cases the model was built from, not                                              TABLE 4
validation. Probe 171 supplies the missing direction: four           Provenance of each finding. Repro = deterministic reproduction of a filed
                                                                       issue; New = no third-party tracker report of the measured behavior
protocols the model has never been exercised on, each                   (#8039 is in the tracker as our own filing, Sec. 5.2); Stable = holds
prediction registered in the probe source and committed before the                      across the version sweep (Sec. 2.3).
run, only then measured — three invocations ⟨a, b, c⟩ at one
interrupt checkpoint (predicted ⟨a, a, a⟩); a fork after a post-     Finding                     Status           Note
completion stray (predicted ⟨a, ⊥, a⟩, testing that inertness
                                                                     #6663 FD                    Repro, Stable    5 versions; source mecha-
and the serve rule compose); bare and resume-map forms                                                            nism located
interleaved (predicted ⟨a, a, a⟩); and, as negative control, two     #6491 CV                    Repro, Stable    5 versions; now silent on
interrupts on distinct checkpoints (predicted ⟨a, b, a, b⟩). The                                                  1.2.9
                                                                     EO crash-path split         New              probe 118 control; inter-
control carries the weight: a degenerate model serving the                                                        rupt vs crash
first value ever seen would satisfy the first three and fail         #8039 executor order        New              probe 124; unbarriered ad-
the fourth. All four confirmed. The mapping remains expert-                                                       jacency
established rather than mechanically extracted; what changes         CrewAI restore replay       Repro            probe 115; 12-vs-11 arith-
                                                                                                                  metic
is that it now makes falsifiable predictions off the set it was      LlamaIndex prefix (D)       Repro            documented at-least-once
derived from, and has survived them.                                 pydantic-graph unrecov.     New              probe     119;  safety-by-
                                                                                                                  deadness

5     C ONFORMANCE M ETHODOLOGY
5.1   Design principles                                                 task return — so the ledger equals the effects that fired,
The harness obeys three constraints that make every verdict             by ordering, and the only hypothetical miswiring (a lost
deterministic and portable.                                             record) undercounts, making every reported duplicate a
• LLM-free. All probes drive persistence APIs with pure-                floor. Probe 163 checks the ordering mechanically: kills
  Python tasks and deterministic values; no verdict depends             before the INSERT, after it, and after the framework’s
  on sampling, provider state, or prompt behavior.                      durable write yield post-crash counts of 0/1/1, and only
• Timing-free crash injection. Every crash verdict is de-               the post-INSERT window duplicates on resume (1 → 2,
  cided without a timing window: matrix crashes are                     every repetition, both environments).
  exception-based; probe 133 kills the process with SIGKILL              RD needs more than straight-line protocols: it concerns
  synchronized by a filesystem barrier; probe 137 widens             the ordering of persistence operations, so its probe constructs
  the kill to a three-point matrix; and probe 160 exhausts the       the two legal durable states a crash between unordered
  interface — one run per persistence operation, the durable         operations would leave — exhaustive exploration via a
  prefix frozen at exactly that many completed operations            dropping checkpointer — rather than racing a kill. Two
  by a serializing wrapper, the freeze self-audited per point.       interleavings, two deterministic resumes, one comparison.
  No sleep-window races, no kill-time distributions: a crash-            Every probe writes raw and stable-view JSON into a
  conformance verdict is a protocol property, host-invariant         per-campaign evidence directory under results/ (one
  at a fixed dependency resolution and runtime, which                subdirectory per campaign) with a generated manifest;
  is what the artifact pins. The three concurrency cells             the paper’s numbers are claimed only from committed
  (probes 159, 168, 174) are the named exception, because            evidence, which the artifact’s audit re-derives. The live-keyed
  their subject is a race: their verdicts are existence claims       ecological checks gate on API keys, are skipped without them,
  decided by the external ledger and reported as observed            and their stable fields are effect counters only (Section 6.5).
  frequencies — saturated at 1.0 in the measured range —
  never as timing-free protocol facts. Confidence intervals
  appear only for the live cells, whose repetitions are              5.2 Provenance: what is reproduced versus newly ob-
  genuine samples.                                                   served
• Effect-ledger oracle. Each side-effecting task increments a        Table 4 records each finding’s provenance. Two results
  process-local counter; EO/CO read the counters, PC reads           are new observations, in no tracker we found: the path-
  execution order and state lineage, FD compares branch              split of exactly-once in LangGraph (probe 118’s control
  outcomes to supplied values, CV inspects the durable log           run) and the executor-layer submission-order evidence for
  after a schema-violating write, and RD compares recovery           #8039 (probe 124) — that issue is ours, filed during the
  decisions across constructed durable states (probes 118,           control-plane study [17] and disclosed there as such, so it
  128). On the durable-backend probes the counter is cross-          is author-reported upstream evidence, with several other
  checked by an on-disk SQLite effect ledger, independent            developers’ reproductions as the independent half. The
  of the checkpointer database and of process memory; the            remainder are deterministic reproductions of third-party
  two oracles agree on every reported cell (probe 126). Both         filed issues — itself a contribution, since issues are anecdotes
  oracles are external to framework state: as the CrewAI             until reproduced under controlled conditions with an effect
  restore receipt shows, framework-visible state can look            oracle — and reproduction is never dressed as discovery.
  correct while the ledger records a duplicate. The ledger
  needs no two-phase commit with the effect: on the durable-
  backend and kill probes the effect is the ledger append            5.3   Probe suite
  — a single autocommitted INSERT, durable before the                Forty-seven numbered probes in eleven campaigns, plus the
  task returns, every kill gated on a durable event after            key-gated multi-model, multi-host live-replication matrix
                                                                                                                               11

(probe 148, Sec. 6.5); the artifact’s manifest is the authorita-   while mid-graph writes are deferred-loud, the corrupt record
tive inventory, and the campaign-by-campaign summary is            durable before a ValidationError surfaces one superstep
reproduced in the supplementary material (Sec. S2). Every          later and the thread’s own read APIs thereafter raise (the
probe emits raw and stable-view JSON; the replications that        original #6491 symptom). A clean subsequent run escapes
count are cross-host (Section 9) and cross-backend (Section 6).    only by full input overwrite, with the corrupt history retained
                                                                   beneath it.
5.4   Environment and versions
                                                                     RD (✓ at checkpointer granularity, both durable-
Pilot environment: Python 3.12.3, Ubuntu 24.04 container; state orders, both backends; executor layer instrumented).
LangGraph 1.2.9 with langgraph-checkpoint 4.1.1 Probes 118 (in-memory) and 128 (SqliteSaver) settle
(InMemorySaver); llama-index-workflows 2.22.2; Cre- the checkpointer-API question by construction: a dropping
wAI 1.15.2 (JSON checkpoint provider, SQLite flow persis- checkpointer builds both legal durable states around the
tence); pydantic-graph 1.107.1; AutoGen AgentChat 0.7.5, contested persistence pair, and on each backend both resume
all freshly resolved on 2026-07-16 to test current releases to identical decisions and effect counts. Probe 124 records
and then pinned by the committed lockfiles. Durable- the real submission sequence at the layer #8039 names: in
backend environment (probes 126–130): a second, sepa- synchronous durability, ⟨put, put_writes, put⟩ with the
rately provisioned Ubuntu 24.04 container (Python 3.12), task-result write and superstep checkpoint adjacent and
fresh-resolved on 2026-07-17 to the identical framework unbarriered — the #8039 precondition observed directly.
versions, with langgraph-checkpoint-sqlite 3.1.0, Probe 136 removes any need to race the pool: an adversarial-
langgraph-checkpoint-postgres 3.1.0 (psycopg 3.3.4), but-legal saver defers every put_writes past the following
and a live local PostgreSQL 16 server. Because verdicts are put — the losing schedule’s durable order, deterministic
deterministic and timing-free, the environment’s only load- — an injected crash leaves genuinely divergent durable
bearing attribute is the package version set, which the artifact states, and recovery from both is identical in result and
pins.                                                            re-execution counts: RD holds on 1.2.9 against the realized
                                                                 hazard (Remark 1).
6     C ONFORMANCE R ESULTS
Table 5 is the conformance matrix. We walk the receipts.           EO splits by path (✓ interrupt / ✗ crash; classification
                                                                resolved). With every persistence operation intact — the task’s
                                                                result durably recorded via put_writes — crash-resume
6.1 LangGraph 1.2.9: fork violation and silent validity re-executes the completed task (effect count 1 at crash, 2 after
violation                                                       resume), replicated on SqliteSaver and PostgresSaver
FD (✗, issue #6663; all three backends; both invocation with the durable ledger agreeing (probes 126, 130). The
forms). A one-node graph interrupts; the probe records documentation audit settles the classification: the pending-
the interrupt checkpoint’s checkpoint_id and issues writes section states that completed nodes’ writes are stored
two resumes addressed to the same (thread_id, precisely so that on resume “you don’t re-run the successful
checkpoint_id):            Command(resume=True)           then nodes” [8]; the measured behavior re-runs the successful task
Command(resume=False) — the address the persistence whose write is durable, so the cell is ✗ against the frame-
documentation presents as the branch-creating time-travel work’s own stated semantics. Mechanistically, interrupt-
primitive [8]. Measured: the first resume returns value 1 and resume memoizes completed task results (#6792, fixed) while
the second returns value 1 — the supplied False silently crash-resume does not: exactly-once across interrupts, at-
ignored, the first branch’s outcome re-served — invariant to least-once across crashes, on one API. Probe 133 answers
backend and invocation form: identical on SqliteSaver the exception-crash objection: SIGKILL barrier-synchronized
and live PostgresSaver (probes 126, 130) and under after the durable write, resume in a fresh interpreter, the com-
the interrupt-keyed resume-map form (probes 127, 130). pleted task re-executes identically (ledger 1→2); probe 137
Per Section 4.3, the second value is durably recorded and widens to three kill points, three repetitions each, byte-
never consulted — a human answering the same approval stable. Same-process retry contrasts (probe 141): an exception
differently is given the first answer’s consequences; Section 7 preserves the completed sibling on retry while process-death
repairs the cell (probe 134).                                   resume does not.
    CV (✗, #6491 class — now silent; all three backends).
A graph over a pydantic-typed state (items: List[str])             PC/EO on the interrupt path (✓, with regression history).
runs a node appending None. As originally reported, the Resume from the interrupt checkpoint does not re-execute
invalid output persisted and a later get_state_history the pre-interrupt node (#7361 fixed relative to the 1.1.x regres-
raised, leaving the thread unreadable; on 1.2.9 nothing raises sion), and the functional-API pipeline re-executes nothing
at invoke or history read and the schema-invalid value is on resume in sync and async variants (#6792 fixed). CO
durably present, identically on all three backends (probes 126, (✓, all three backends). A stray Command(resume=...)
130) — a strict CV violation, and a worse one, since noth- after completion is swallowed: the post-interrupt effect count
ing signals the caller. The downstream-consequence probe remains 1 and the final state is unchanged, identically on all
(probe 150; two-host replicated) splits what “silent” means three savers (probes 126, 130). The swallowing is silent — the
by regime: terminal writes are fully silent — get_state contract is satisfied, but the caller receives no signal that a
returns the corrupt value, model_validate on it raises, and resume was discarded, a spec-level gap the full study will
the silence survives a fresh-process SQLite deserialization — track.
                                                                                                                                                                         12

                                                                          TABLE 5
Conformance matrix: probed releases (pilot 2026-07-16; durable-backend replication 2026-07-17). ✓ = property holds on the probed path, and only
on it; for PC, a ✓ certifies the observable consequence of Property 1 (state equality with the effect record intact), not provenance — PC violations are
decidable from surface observables, PC satisfaction is not, and this qualifies every ✓ in the column. LangGraph’s CO ✓ is the sequential path, which
probe 159 shows does not compose across processes; ✗ = live violation (deterministically reproducible); D = documented divergence (the framework
states a discipline weaker than the property; behavior matches its statement); U = undocumented divergence (measured re-execution of completed
     effect-bearing work with no citable stated discipline for the probed mechanism: behavior reported in full, label withheld); ◦ = not probed (no
crash-time durability control on the probed path, or mechanism absent). “regr.” marks properties whose violation shipped as a 1.1.x regression and is
                                                                       fixed in 1.2.9.

Framework (path)                                                PC                   EO                       FD                   CV                 CO         RD
LangGraph 1.2.9 (graph, interrupt/                                                   ✓ int. (regr. #6792)
                                                                ✓ (regr. #7361)                               ✗ #6663              ✗ #6491 class      ✓          ✓a
Command; InMemorySaver)                                                              ✗ crash (118)
LangGraph 1.2.9 (same paths; SqliteSaver /                                           ✓ int.                   ✗ both forms         ✗ silent           ✓ seq.
                                                                ✓                                                                                                ✓a (128)
live PostgresSaver)                                                                  ✗ crash (126, 130)       (126, 127, 130)      (126, 130)         ✗ 159e
LlamaIndex Workflows 2.22.2 (Context snapshot;
                                                                ✓                    ✓                        ✓                    ✓ (fail-fast)      ✓          ◦
two-step HITL)
LlamaIndex Workflows 2.22.2 (wait_for_event
                                                                D                    D                        ✓                    ✓                  ✓          ◦
durable-HITL idiom)
AutoGen AgentChat 0.7.5
                                                                ◦                    ✓ restore                 ◦                   ✓ (loud)           ✓d         ◦
(save_state/load_state, 140)
CrewAI 1.15.2 (@persist restore)                                Ub                   Ub                       ◦                    ◦                  ◦          ◦
CrewAI 1.15.2 (CheckpointConfig
                                                                ✗                    ✗                        ◦                    ◦                  ◦          ◦
+ from_checkpoint)
pydantic-graph 1.107.1
                                                                ✓                    ✓                        ◦                    ✓ (fail-fast)      ✓          ◦
(FileStatePersistence)c
a
  RD holds at checkpointer-API granularity: probes 118 (in-memory) and 128 (SqliteSaver) construct both legal durable orders of the #8039 persistence pair and both
recover identically on 1.2.9; the executor-submission layer is instrumented (probe 124) and the pool divergence is realized deterministically via an adversarial saver
(probe 136), with recovery invariant.
b
  Classification rule, total over the outcome classes this study observed and symmetric with one deliberate exception: ✗ requires either a citable stated discipline the
measured behavior contradicts or silent persistence of corrupt durable state; D requires a citable statement of the weaker discipline; absent any citable statement for
the probed mechanism, measured re-execution of completed effect-bearing work is U — reported in full, labeled neither violation nor divergence, reclassifiable in
either direction only by a citable statement, which changes the label and never the measurement. The asymmetry is deliberate: the contract is proposed, not adopted,
so ✗ charges a framework only with contradicting its own citable semantics or corrupting durable state, while divergence from the contract is what every cell, U
included, measures. CrewAI’s @persist documentation frames restoration as state restore and states no replay discipline in either direction, so those cells are U;
the CheckpointConfig cells remain ✗ against the feature’s citable exactly-once claim. Under the strictest alternative rule every U cell becomes ✗ and no pairwise
separation of observation (i) changes (Supplement S4).
c
  pydantic-graph’s ✓ cells are qualified by a recoverability failure: after a crash, iter_from_persistence raises (GraphRuntimeError, unable to restore) — effects
are not duplicated because nothing resumes, so safety holds while progress fails (Section 6.4); v2.x removes the persistence machinery entirely.
d
  AutoGen: double-restore of the same saved state added zero effects (probe 140); an interrupt-authority axis does not exist on this plane, so CO is reported as
restore-inertness. AutoGen’s plane persists nothing framework-side — save_state hands the state to the caller, who owns durability — so Property 4’s write clause
has no framework-side instance; the probed CV analog is load-time validation of caller-supplied state, and the ✓ certifies exactly that (the tampering is of the caller-held
copy, never of anything the framework persisted).
e
  CO on the durable backends splits by concurrency: sequential re-delivery is inert (probes 126, 130), while the same delivery from two concurrent OS processes fires the
gated effect twice, 10/10 on both durable backends on the developer host (probe 159; the container replication is shorter and duplicates in every repetition) — the default
packaged R EMIT shim does not repair this cell (10/10 with the shim active; its sequencer is per-process), while the shim’s opt-in cross-process gate (v0.1.2) does: {1:10}
on both durable backends, the loser refused loudly before any node (Sec. 7.2).



6.2 LlamaIndex Workflows 2.22.2: divergence, not viola-                                  6.3   CrewAI 1.15.2: replay invisible in state
tion — and a clean fork
                                                                @persist (U). Re-kicking a completed @persist flow with
                                                                its persisted id restores state and re-executes both methods:
The two-step HITL pattern (a step returning the state counter goes 11 → 22 and both effect counters read 2.
InputRequiredEvent,              a     second       consuming The label follows note b of Table 5: the feature’s documen-
HumanResponseEvent) is clean across the board: snapshot tation states no restore discipline in either direction, so the
at the interrupt, restore, and the pre-interrupt step’s counter cells are U — duplication measured and reported in full,
stays at 1 (PC/EO); two restores of the same snapshot only the label awaiting a citable statement. The crash-resume
answered YES and NO yield the respective outcomes (FD variant is the unambiguous case: method s1 completes and
— the property LangGraph fails, LlamaIndex Workflows persists (counter 1), s2 raises; re-kickoff with the same id
passes); a second response into a live run is swallowed with re-executes s1, and the run finishes at counter 12 where
the post-step firing once (CO); serializing a context holding exactly-once predicts 11 — one unit of state and one external
a non-serializable object fails fast with ValueError (CV).      effect, duplicated. The R1 counterexample’s arithmetic, live
    The wait_for_event idiom — the documented — and no artifact of exception semantics: under SIGKILL
durable-HITL pattern — behaves differently by design: the duplication reproduces in every repetition, the second
restoring a serialized context re-executes the step prefix effect fired by a process that did not exist when the first fired
(counter 1 → 2), exactly as the documentation warns (“make (probe 164, both environments).
any preceding work safe to re-execute” [2]); D, not ✗. The          CheckpointConfig (✗). The checkpointing feature’s
sharpened claim: the ecosystem’s problem is the coexistence, documentation states restore “resume[s] without re-running
under one API shape, of exactly-once claims, at-least-once completed work” [1]. Measured on 1.15.2: with checkpointing
documentation, and silent replay, with nothing to tell a caller enabled, s1 completes and its checkpoint is written (state
which regime they are in.                                       counter 1 durable), s2 raises; Flow.from_checkpoint on
                                                                                                                                  13

the latest checkpoint followed by kickoff() re-executes sessions [18]), an agent instructed to charge once via a
the completed method — the s1 effect counter reads 2. The side-effecting tool did so (counter 1), and a fresh runner
final state counter reads 11 — numerically the exactly-once restoring the same file-backed session did not re-invoke the
answer — because state was rebuilt from initial values rather tool: EO across session restore holds live (a live observation
than resumed, so the duplicate is invisible in framework state — its LLM-free harness probe is in the full-matrix plan). On
and visible only in the external-effect ledger. If s1 charges a card, LangGraph 1.2.9 with claude-haiku-4-5 driving a ReAct agent
the card is charged twice while the flow’s state looks correct under interrupt_before=["tools"], the counter reads
— the receipt that makes the harness’s oracle external. A 0 at the interrupt, 1 after the approval resume, and still 1
maintainer statement adopting a state-only semantics would after an injected stray resume — the same silent inertness
reclassify the cell to D by note b’s rule, changing the label the LLM-free probe of the same path observed. The failure
and never the measurement.                                            direction has also run live (probe 131): the effect ledger is
    A withdrawn observation. An exploratory run empty at the gate, the approval resume fires the gated tool
in    an     ad-hoc      virtual     environment         had     sug- once (ledger [10]), and a second resume carrying an edited
gested the documented Flow event configuration decision is served the first decision’s branch — the agent
(on_events=["method_execution_finished"])                             repeats the first answer verbatim and the tool fires again with
wrote no checkpoint files. In the pinned, lock-file-resolved the stale value (ledger [10, 10]). The fork violation reproduces
environment the same configuration writes checkpoints; the live, in exactly the shape the LLM-free durable-ledger probe
zero-file observation is withdrawn, with probe 115b retained recorded.
as a regression guard. One probe, two environments, two                   The replication matrix (probe 148, auditing only the
answers: a conformance verdict is meaningful only against counters) spans two models per provider and two hosts
a pinned resolution, which reproduce.sh audits against — each provider probed on its own framework cells, so cross-
committed lockfiles.                                                  model replication is within-provider per cell — at N =20
                                                                      per (probe, model, host): 240 live runs, zero harness errors,
6.4 pydantic-graph 1.x: safety by unrecoverability                    identical pins across both hosts (the session-restore cells ran
                                                                      openai-agents 0.18.3, one patch release past the 0.18.2 pilot
Inclusion is by the selection rule, not convenience: pydantic-
                                                                      above). Pooled per model (N =40): the interrupt-approve
graph documents FileStatePersistence for interrupt-
                                                                      cell’s violation fields fire in 0/40 runs on claude-haiku-4-
ing and resuming runs, so it claims membership in the
                                                                      5 and claude-sonnet-4-6 (95% Wilson upper bound 0.09);
plane — and the liveness obligation exists precisely so
                                                                      the session-restore cell shows 0/40 violations with 40/40
that “never resumes” cannot pass by vacuity. The finding, a
                                                                      completion on gpt-4o-mini and gpt-4.1-mini; and the fork
defect against the framework’s own documented resumption
                                                                      violation reproduces in 40/40 runs on each Claude model
claim: every probed safety property passes, and the point
                                                                      (95% Wilson [0.91, 1.0]) — 80/80 overall, on every model-
of the plane fails. After a crash in the second node — first
                                                                      host combination, exactly as the mechanism account predicts
node’s effect fired and snapshotted — the framework’s own
                                                                      for a read-path defect no model choice can mask (per-(model,
resume entry point refuses to restore the persistence file
                                                                      host) rows: results/live/148_matrix.json). These
it wrote (GraphRuntimeError: Unable to restore
                                                                      are existence and stability replications — at N =40 a true
snapshot from state persistence); no completed ef-
                                                                      rate of 0.09 is consistent with observing zero — certifying
fect duplicates because no execution resumes. The failure is
                                                                      existence and cross-model, cross-host stability, never rarity
specific to mid-node crash state: SIGKILL while parked be-
                                                                      or prevalence. Live PC and CV arms complete the picture
tween nodes restores and completes exactly once (probe 158c,
                                                                      (probe 152, N =40 across the two Claude models): the pre-
two hosts), while SIGKILL inside the second node repro-
                                                                      gate checkpoint lineage is prefix-stable through the approve-
duces the refusal (probe 164, both environments) — the
                                                                      resume in 40/40 runs, and a schema-corrupt checkpoint
boundary bracketed from both sides under real process death,
                                                                      submitted through the saver API is persisted silently in
and a crash in a long-running agent step will usually land
                                                                      40/40 (the corrupt write is harness-submitted; the live traffic
inside. A stray resume of a completed run is rejected loudly
                                                                      certifies the surrounding run and the detection surface) —
(a divergence contrast: LangGraph swallows the same event
                                                                      detonating only at the next get_tuple or get_state as a
silently), and a structurally corrupted snapshot fails fast.
                                                                      KeyError far from the faulting write, the deferred failure
Safety vacuous, progress dead — the liveness obligation’s
                                                                      CV names.
deployed witness, and now also its derived one: the parked-
crash companion module under volatile parking violates
EventuallyCompletes while every safety invariant holds 6.6 Reading the matrix
(Sec. 4). A sharp fragmentation datum on the version axis:
                                                                      Sequential composition across gates (probe 138). A two-gate
2.x deletes the persistence machinery outright, the pinned
                                                                      workflow composes as the contract predicts: EO holds across
release announcing it at runtime via a deprecation warning
                                                                      a session restart between the gates, CO holds per gate, the
on the same interface the verdict is read from.
                                                                      fork violation recurs at the second gate under the stock saver,
                                                                      and the read-path shim repairs that cell on the identical
6.5 Live ecological cells                                             protocol. Crash while parked at the gate (probes 158, 158b,
The abstraction caveat — pure-Python nodes are not agents 158c). The crash location the model excludes by precondition
— is answered in both directions by keyed probes with — process death while parked awaiting the human — is
real models, whose only audited fields are the tool-effect conformant on all three planes that park, replicated on two
counters. On the OpenAI Agents SDK 0.18.2 (file-backed hosts: the pending interrupt survives, the prefix effect stands
                                                                                                                                         14

at one, the gate fires once with the supplied value, the post-                                     TABLE 6
completion stray stays inert. Durable parking is the part of       Window width by dose–response (probe 168; k=4, N =10 per cell,
                                                                 developer host, both durable backends). Cells give saturation — mean
the plane that works.                                            gated fires divided by k, the fraction of racers that win. The edge (widest
    Exhaustive kill-point sweep (probe 160). The two-task jitter still at saturation 1.0) tracks the gated node’s duration D: a resume
protocol performs five persistence operations (put, three arriving while the node still runs finds the interrupt unconsumed and fires.
put_writes, put); a SIGKILL after each — one kill per             Backend columns share a jitter seed and are paired, not independent
                                                                               (Sec. 9); the values below are the SQLite arm.
run — re-executes completed effect-bearing work at all four
incomplete boundaries and recovers at every one of the
five (the fifth is a completed run, excluded from duplicate                                        arrival jitter (ms)
accounting). On this protocol every durable prefix short of                 gate D          0     100       500 1,000 3,000
completion licenses re-execution: the crash-path EO class is                0 ms          1.00 0.40 0.30            0.28      0.28
not an artifact of where we chose to kill.                                  500 ms        1.00 1.00 1.00            0.78      0.38
    Cross-process duplicate delivery (probe 159). The one cell              2,000 ms 1.00 1.00 1.00                 1.00      0.90
where a conformant verdict does not survive its own compo-
sition. Two OS processes sharing one on-disk SqliteSaver,
each issuing Command(resume=...) against the same
parked interrupt from a spin-barrier start: the gated effect out of ten, on both backends. The failure is therefore not
fires twice in 10/10 repetitions on the developer host and “two processes duplicate” but every racer that arrives within
3/3 in the container, with no error on either side and the the window consumes, with no observed ceiling below k = 16.
pre-gate effect firing exactly once throughout — the duplicate       Jitter to 25 ms does not close it: the response is flat on all
is the gated node alone, not a replayed prefix. Byte-identical ten (backend, k) pairs, so the window exceeds the entire
re-delivery, the case the sequential probe measures as inert stock interrupt protocol of probe 139. Its width is then
(probe 126), is the arm that duplicates; when the two racers measured directly rather than bounded, by instrumenting the
carry different values both values fire and each racer is served gated node with a controlled duration D and sweeping jitter
its own, so the concurrent failure is double consumption, not past it — D standing for the model call or payment request a
the serve-first-recorded fork failure of #6663. The durable deployed gate performs before its effect. The edge tracks D
state afterwards records one branch, so — as with CrewAI’s across three doses at k = 4, ten repetitions per cell on both
restore — the duplicate is invisible in framework state and backends (Table 6). The window tracks the gated node’s execution
visible only in the external-effect ledger. Distinct threads time — the deployed magnitude: a gate whose node awaits a
under the same contention are unaffected (k=4 workers, one model response holds authority unconsumed for the length
database, per-thread exactly-once), which localizes the race of that response, and every resume arriving meanwhile
to same-thread resume rather than to the backend’s write fires. It is also independent confirmation of probe 165’s
path. The in-model shadow is not FaultDoubleConsume mechanism account — the __resume__ journal write is
(guarded by run completion, the sequential case the plane executor-concurrent with gated execution, so consumption is
refuses) but R11_ConsumeCount.tla’s lost-update switch not durable until the superstep joins. Two limits are stated
(Sec. 4), whose discovered footprint {EO, CO-e, CO-c} with rather than smoothed: the backend columns of the D-sweep
PC, FD, CV, RD clean matches this cell exactly: CO holds share a jitter seed, so they are a paired comparison and not
sequentially and fails concurrently, parallel to EO’s split independent evidence of backend invariance (that claim rests
by path. Nor is it a property of one store or machine: the on the zero-jitter cells and the source audit of probe 129);
identical protocol on PostgresSaver 3.1.0 against a live and the dose–response arm ran on the developer host alone.
server duplicates in 10/10 repetitions, no errors, on both The saturation sweep is cross-environment replicated: on a
hosts as the SQLite arm does — two backends, two separately separately provisioned single-vCPU cloud instance (2 GB,
provisioned environments. Row-level locking and MVCC do one core, k capped at 8 by memory), 32 cells and 320
not close the window: the resume path’s read–decide–write protocol executions yield 1,342 gated fires where exactly-
of the interrupt consumption is guarded by no compare-and- once predicts 320, saturation 1.0 in 25 of 32 cells and never
swap on either backend — the classical lost-update shape of below 0.9, zero racer errors; at k=8 with zero jitter the
the isolation-anomaly taxonomy [19], arriving at the resume distribution is {8:10} on both backends. This is the arm that
plane because interrupt consumption is a read–modify–write could have failed and did not: if duplication needed true
nobody made atomic.                                              parallelism, a single-vCPU host would serialize the racers
    The shape of the window (probe 168). Probe 159 measures into the already-consumed path — it does not, because the
one point — two racers, zero arrival offset. Probe 168 sweeps window exceeds 25 ms while the scheduler quantum is a
the two parameters that point leaves open: racer count k ∈ few milliseconds. Across both hosts the sweep totals 72
{2, 3, 4, 8, 16} and arrival jitter ∈ {0, 1, 5, 25} ms, on both cells and 720 protocol executions, firing 3,970 effects where
durable backends, ten repetitions per cell. Forty cells, 400 the contract predicts 720. Cross-host racers (probe 174). The
protocol executions, zero racer errors. The gated effect fires remaining distribution axis is measured directly: the two
2,628 times where exactly-once predicts 400. Saturation — racers on two machines — one co-located with a networked
mean fires divided by k , the fraction of racers that win — PostgreSQL server, one a WAN link away at ∼450 ms per
is 1.0 in 36 of the 40 cells and never below 0.933; 39 of 40 query — with the coordination tables, the effect ledger, and
cells duplicate in every repetition. At k = 16 with zero jitter per-racer arrival stamps all server-side, so the receipt itself
the distribution is {16:10} on SqliteSaver and on live carries the server-clock arrival offsets that certify a race
PostgresSaver: sixteen fires from one approval, ten times occurred. At an instrumented 5 s gate, arrival offsets of 0.38–
                                                                                                                                             15

                                TABLE 7                                     liveness obligation (the six columns alone conflate pydantic-
Pairwise separation of conformance profiles (five frameworks, ten pairs),   graph with the all-✓ safety rows). A profile is per framework
each discharged by naming the separating cell of Table 5. Behavioral =
both frameworks were probed on that cell and disagree; structural = they    — its probed path-rows over jointly probed cells, plus liveness
 agree on every jointly probed cell and differ only in which paths exist.   — and the three LangGraph backends collapse to one row
     Ten of ten separate; nine do so behaviorally. LG = LangGraph,          (backend invariance, (iv)), so the claim is not configuration-
 LI = LlamaIndex Workflows, CA = CrewAI, AG = AutoGen AgentChat,            counting. Table 7 discharges it pair by pair: nine of the
                          PG = pydantic-graph.
                                                                            ten pairs separate behaviorally on cells both frameworks
                                                                            were probed on; the tenth — AutoGen against LlamaIndex
          Pair       Kind         Separating cell                           Workflows — is structural, agreeing on every jointly probed
          LG–LI behavioral FD: ✗ (#6663) vs. ✓                              cell and differing only by path-set membership. No sepa-
          LG–CA behavioral PC: ✓ vs. ✗ (rebuild-from-                       ration rests on a U cell alone. A separation witnessed on a
                           initial)                                         jointly probed cell cannot be undone by probing a further
          LG–AG behavioral CV: ✗ (silent) vs. ✓ (loud)
                                                                            one, so filling the grid refines these profiles, never reverses
          LG–PG behavioral FD/CV: ✗ vs. ✓
          LI–CA behavioral EO: D (stated at-least-once)
                                                                            them. Nor is the harness engineered to fail: RD passes
                           vs. ✗ (stated exactly-once)                      everywhere probed, CO passes sequentially on LangGraph,
          LI–PG behavioral liveness: holds vs. fails                        the live conformant cells pass 0/40 per model, and LGF-B,
          CA–AG behavioral EO under restore: ✗/U vs.                        the repair cells, and the multi-gate EO/CO cells all pass. The
                           ✓                                                disagreements sit on the interrupt-adjacent axes: LangGraph
          CA–PG behavioral EO under restore: ✗/U vs.                        fails FD where LlamaIndex Workflows passes it; LlamaIndex
                           ✓
          AG–PG behavioral liveness: holds vs. fails                        Workflows documents away EO where LangGraph mem-
                                                                            oizes; CrewAI claims the strongest discipline and delivers
          AG–LI      structural   none: agree on all jointly
                                                                            the weakest. (ii) Violations concentrate where authority does:
                                  probed cells; differ by path-
                                  set (D idiom on LI only)                  FD and CO govern what a human’s answer means, CV
                                                                            whether the durable record can be trusted, and the live
                                                                            failures sit exactly there. (iii) The regression pairs (#7361, #6792
                                                                            — broken in 1.1.x, fixed by 1.2.9) show the plane drifting
1.89 s put both racers inside the window in every round: the                under maintenance pressure with user issues as the only
stock plane fires the gated effect twice in 10/10 repetitions,              specification; a conformance suite in CI is the standing fix,
the ledger attributing one fire to each host. The shipped gate              and the release sweep (Sec. 2.3) is the drift picture’s other
on the identical protocol serves one racer and refuses the                  half — violations stable across every probed release, surfaces
other with RemitConsumeConflict in 10/10 — without                          churning to the point that pydantic-graph’s 2.x line no longer
the gated node executing: no ledger row from the loser,                     exposes the probed module. (iv) The LangGraph verdicts
whose invoke returns in 1.8–3.8 s against the winner’s 5.04 s,              are backend-invariant across the three tested backends: every
so the refusal precedes the node’s own duration. The co-                    probed cell is identical on InMemorySaver, SqliteSaver,
located racer won every gated round; the gate serializes, it                and live PostgresSaver. This is architectural localization,
does not arbitrate fairness, and the contract requires none. A              not induction over all savers: the cross-saver source audit
first campaign on the same link is retained as the differential:            (probe 129) places the violating decisions in the execution
the remote racer, paying connection setup inside the timed                  loop, above the BaseCheckpointSaver interface, so any
window, landed past the winner’s superstep join and took                    backend reached through that interface inherits them; the
the inert path in 10/10 at a 2 s gate — the dose–response edge              measured invariance is that localization’s prediction, con-
observed across hosts. One asymmetry remains by design.                     firmed.
The default packaged R EMIT shim does not repair this cell
(10/10 duplicates with the shim active): its sequencer is per-
process state, so two processes carry two sequencers. The                   6.7 An embedded durable-execution engine on the
design implication — that the consumption record belongs                    same workload
in the shared store under a compare-and-swap rather than                    The semantic half of the deferred engine head-to-head
in the interposition layer — is realized in Section 7.2 and                 (Section 8) needs no port at scale; probe 147 measures it.
now shipped as the shim’s opt-in cross-process gate (v0.1.2),               The probe runs the paper’s abstract workload — a non-
which flips the cell to {1:10} on both backends (the ungated                idempotent effect, a gate awaiting a human decision, a crash
arm retained as the permanent differential); the section also               after a durable step — on DBOS 2.27.0 as an embedded
reproduces, on a second property, the write-path/read-path                  worker (SQLite system database, no server), with the same
asymmetry the 125/134 pair established for FD.                              external-ledger oracle as every other probe. All probed cells
    Concurrent fan-out at one superstep (probe 141). Two parallel           conform. Exactly-once across process death: the worker
branches, each with its own gate and effect: both interrupts                is SIGKILLed at the gate after the first step’s result is
surface in a single pass, a resume map routes each value                    durably recorded; a fresh process recovers the pending
to its own branch with each effect firing exactly once, a                   workflow, re-executing with recorded step results — PC’s
stray resume map is inert, and the crash cell yields the retry-             memoized-replay discipline — and the ledger shows the
preservation contrast above. Deeper nesting and fan-in racing               step’s effect exactly once. Fork intent: fork_workflow(id,
multiple checkpointers remain future work.                                  start_step) at the recorded receive step is the engine’s
    Four observations. (i) No two probed frameworks share a                 explicit, documented branch-creating address — a deployed
conformance profile, over the six properties together with the              instance of the fork-intent obligation (Definition 2) — and
                                                                                                                               16

the forked branch served its own, different decision, one order making recovery a pure function of the durable log. The
gated effect per branch, prefix not re-executed. Consume- first integration target is a shim implementing LangGraph’s
once: a stray duplicate decision to the completed run left the BaseCheckpointSaver; we report the three enforcement
ledger unchanged (silent-inert, the disposition LangGraph legs in turn.
exhibits; the send API’s idempotency-key parameter is the             (i) The core invariants are machine-discharged, post-
wire-level deduplication discriminator). The latency trade is adoption, as a set of standalone Verus targets with fresh
in Supplement Table S3(b), same protocol, both environments, per-file tallies. proof/remit_verus.rs states the ef-
with a ≈0.5 s per-run engine startup that long-lived workers fect ledger and durable frontier — EO/CO (admitting a
amortize. The container’s +39% shim delta there is stated fresh effect yields count exactly one and preserves ledger-
rather than smoothed: that probe times a short single- uniqueness), PC (commit advances the frontier by ex-
operation window in which the shim’s extra get_tuple actly one, never re-entering the durable prefix), and FD’s
step is not amortized, so it does not contradict probe 139’s keying half: 10 verified, 0 errors. The behavioral
within-5% figure over the full protocol; the developer host halves of FD and RD are theorems with inductive content,
shows the same window inside noise, which is why both each paired with a machine-checked falsifying certificate:
are reported. Absolute latencies are environment-bound; in remit_verus_fd_machine.rs proves, by an inductive
both, the engine is slower than the checkpointer path it would invariant over record/serve steps, that every branch is served
replace, by 2.9–5.0× on gate-answer latency. The direction the value its own invocation recorded (5 verified, 0
matters: an engine that were faster and conformant would errors), while negative/fd_stock_certificate.rs
end this paper’s case for a repair at the checkpointer interface. — the same obligation under the stock #6663 serve-first-
This is an engine baseline, not a matrix row. The point is recorded rule — is rejected (1 error), certifying the proof
narrow: the alternative Section 8 prices — adopt the durable- has content; remit_verus_rd_interp.rs interprets the
execution model wholesale — delivers every probed cell the recovery decision in Property 6’s own words (skip a task
frameworks fail, by construction, at its stated adoption and iff it is durably recorded) and proves order-independence
latency costs.                                                    for the completed #8039 window — the put_writes/put
                                                                  pair durably present in either order (adjacent transposi-
                                                                  tion) — and across equal write-set counts (6 verified,
7 R EMIT : A R EFERENCE S EQUENCER WITH A V ER - 0 errors; one of the six is the definitional base case,
IFIED M ODEL AND C ONFORMANCE -T ESTED C ORE                      identical records to identical decisions — the content lies
The contract’s repair artifact is R EMIT, a reference resume in the swap and write-set lemmas); the crash-truncated
sequencer and append-only effect ledger, delivered at four divergent-content pair is outside these hypotheses by design
explicitly labeled maturity levels: a machine-discharged — the sequencer removes that window, and the two-order
Verus model whose decision cores are additionally verified constructions (probes 118, 128, 136) are its evidence —
as executables in the shipped crate; a Rust core mirroring with the order-sensitive rule failing the same obligation
that model behind PyO3 bindings, with executable confor- (negative/rd_ordersensitive_certificate.rs, 1
mance to the TLA+ transition relation (Section 7.3); a live error). On Verus 0.2026.05.03.8b81855 every positive tar-
CV enforcement shim; and a two-sided FD enforcement get discharges with 0 errors. Earlier, FD and RD were
result ending in a working repair (probes 125, 134), re- stated as lemmas over definitions that made them tauto-
established by the packaged, decision-free shim at the pinned logical — verifiable with empty proof bodies; those lem-
versions. The artifact is distributed on PyPI (pip install mas are deleted, their tallies retired, and the correction,
remit-contract: prebuilt manylinux wheel and source with the full discharge history and dates, is recorded in
distribution); release v0.1.2 — the release that ships the opt- crates/remit/VERIFICATION.md.
in cross-process gate of Section 7.2 — is the exact build             (ii) The CV leg is demonstrated live: a validating saver
evaluated here. The verification object throughout is R EMIT’s enforcing commit_checkpoint’s validity clause re-runs
model and its extracted executable cores, never the composite the exact silent-persistence protocol on 1.2.9 and converts the
package. Table 9 states how far the proof reaches, layer by violation to a loud rejection with nothing invalid persisted
layer, and names the one rung that is absent; the text does and history readable — baseline ✗ to ✓ on identical inputs
not relitigate it elsewhere.                                      (probe 123). The rejection fires before persistence, so the
                                                                  thread’s durable state remains its last valid checkpoint and
                                                                  the caller can repair and resume — where the stock path
7.1 Architecture                                                  leaves the corrupt record durable and, mid-graph, breaks
R EMIT interposes at the checkpointer interface — the narrow the thread’s own read APIs (probe 150). Loudness costs the
waist every probed framework already routes durability caller an exception; silence costs the thread.
through. Its state is (i) an append-only effect ledger of             (iii) The FD leg is settled by a matched pair that localizes
⟨branch, task , effectId ⟩ records written transactionally with enforcement exactly. The write path is powerless: a fork-
the completion checkpoint, and (ii) a sequencer that to- keyed saver storing each resume write under a distinct key
tally orders, per thread, the persistence operations whose does not restore FD (probe 125), because the loop never
unenforced ordering produces #8039. The six properties consults the saver about which resume to serve — the
map to local invariants: EO/CO to ledger-uniqueness; precedence decision of Section 4.3 happens above it. The
PC to frontier monotonicity; FD to branch keying by read path succeeds: a subclass overriding only get_tuple
⟨checkpointId , resumeIndex ⟩ with per-branch ledgers; CV — when the config carries an explicit checkpoint_id, the
to schema validation at the write; RD to the sequencer’s total branch-creating address of Definition 2 clause 3, it strips
                                                                                                                              17

recorded __resume__ pending writes so the invocation’s with gated execution rather than ordered before it, so a veto
own value is consulted — repairs #6663 on the identical raised there surfaces only at superstep join.
protocol (probe 134): the stock control violates; under the            Read path (repairs the cell). Rebound at the durable-state
shim the bare and resume-map fork cells produce 1 then 0 read the loop performs before gated execution — inside
with one correctly-valued effect per branch; same-value re- get_tuple, when the returned checkpoint carries a pending
fork is deterministic; a stray resume at the ordinary address interrupt — the gate takes the claim with one INSERT
stays inert. The Verus proof said ordinal keying restores under a uniqueness constraint (SQLite primary key; Postgres
FD in the abstract; probes 125/134 say where it can bind ON CONFLICT). Both racers demonstrably load the same
in LangGraph: not at persistence, but at the durable-state checkpoint there, so exactly one can win. The gated effect
view the loop loads. The demonstrator’s discriminator is the then fires once in 10/10 repetitions on SqliteSaver and
documented branch-creating address; production carries an 10/10 on live PostgresSaver, the loser rejected before
explicit fork flag — FI (Property 7) made concrete — and any node executes; the same-value and different-value race
probe 155 evaluates that flag where the address heuristic arms both give the distribution {1:10}; the sequential single-
cannot go: under a checkpointed subgraph the flag-keyed resume control passes untouched, so the gate does not
configuration (fork_on_explicit_checkpoint=False false-positive on the legitimate first consumption; the post-
with an explicit remit_fork key) leaves subgraph interrupt– completion stray stays inert; and the stock control reproduces
resume stock-identical, still repairs the #6663 cell at the parent the duplicate in the same run (5/5, both backends) as the
gate with each branch firing exactly once, and keeps a stray differential.
ordinary-address resume inert, on both InMemorySaver                   The finding this yields is not the gate but its location.
and SqliteSaver, both environments. The matched pairs Twice now, on two different properties, a repair placed at
are the ablation a reviewer would ask for: the validity the persistence write path was powerless while the same
gate alone flips CV (probe 123), the fork filter alone flips repair placed at the durable-state read path succeeded:
FD (probe 134 against probe 125). Against the alternative fork determinism (probe 125 fails, probe 134 succeeds) and
repair families: idempotency wrappers move the burden cross-process consume-once (the v1 gate fails, the v2 gate
into user task code; replay suppression breaks per-branch succeeds). The common cause is visible in both traces —
EO on legitimate forks; full event-sourced history is the the loop’s decision is taken from what get_tuple returns,
durable-execution adoption Section 8 discusses. R EMIT is the and the saver is told about that decision only afterwards,
minimal-interposition point.                                       so interposition below a decision cannot veto it. That is a
    Interposition overhead (probe 139). N =200 fresh-database statement about where a conformance repair can bind in a
iterations per configuration of the full interrupt protocol, checkpointer-shaped architecture, conditioned on the loop
on two hosts with a 3–5× gap in absolute storage latency shape both traces exhibit: any plane whose execution loop
(Supplement Table S3(a)): within 5% of stock in the container, reads durable state, decides, then reports to the saver has its
within ±1.7% on the developer host across two 200-iteration only saver-level enforcement seam at the read. A plane that
runs (committed per-cell deltas −0.34% to +0.38%). The consults its saver before deciding is outside the claim, and
verdict holds at both latency regimes: on the single-threaded the two matched pairs establish the seam for this architecture,
protocol the enforcement point adds no measurable latency, not for every possible write-path design.
the microbenchmark being the adversarial denominator                   Two former limits are now interface rather than defect.
with no model latency to hide behind. Concurrency is get_tuple carries no read-intent discriminator, so a bare
probe 157 (Section 7.3); Section 6.7 measures the engine state inspection during a park takes the claim — confirmed
comparison’s semantic cells and a first single-workload live: get_state on a parked thread consumed it in our
latency comparison.                                                own regression harness — which the shipped gate converts
                                                                   into an explicit opt-out (remit_inspect in the invocation
                                                                   config), the CO analogue, at the read path, of the FI gap
7.2 Repairing the cross-process cell, and where the at the write path. That gap is also why the gate ships
repair binds                                                       opt-in rather than default-on: get_tuple serves state in-
Probe 159 measures a cell the default shipped shim does spection and pre-execution loads through one call with
not repair. The design implication it states — put the no bit distinguishing them, so a default-on gate would
consumption record in the shared store under a compare-and- convert every bare inspection of a parked thread into a
swap, not in the interposition layer — is realized as a saver- consumption unless every caller adopted remit_inspect
level gate in probe 165, since promoted into the shipped shim first. The default is forced by the interface, not chosen by
as its opt-in cross-process gate (v0.1.2), whose development the repair; a plane that adds a read-intent discriminator
reproduced, on a second property, the structural finding the makes default-on safe. And the gate is no longer a saver-
125/134 pair established for FD.                                   level demonstrator: v0.1.2 promotes it into the shipped shim
    Write path (falsified). The first design claimed as opt-in configuration (cross_process_gate=True), tak-
⟨thread , checkpoint⟩ in a shared durable claims table ing the (thread, checkpoint) claim in the saver’s
before any __resume__ pending write was accepted. own database and refusing the loser with a typed
Measured at the pins, the race still duplicated in every RemitConsumeConflict before any node executes —
repetition with the gate active, and the loser was rejected {1:10} on both durable backends, the ungated default
loudly — after its effect had already fired. An instrumented retained and still measuring 10/10, the permanent differ-
trace gives the reason: the null-task __resume__ journal ential. What remains bounded is scope, stated plainly: the
write is submitted to a background executor and is concurrent gate serializes ordinary-address deliveries for synchronous
                                                                                                                                               18

savers over one shared store; racers distributed across two                                              TABLE 8
hosts against a networked PostgreSQL server reproduce                      R EMIT’s Verus surface, one row per file (tallies as recorded in
                                                                         VERIFICATION.md on the pinned toolchain; the remit_verus
both sides (probe 174): the stock path duplicates in 10/10           filename prefix is elided). Composed targets restate standalone content,
repetitions inside a 5 s gate, and the shipped gate refuses the       so rows overlap and no cross-file total is claimed; the two negative/
losing racer with RemitConsumeConflict in 10/10 before                certificates fail by design — the mechanized evidence that the positive
any node executes; partitions and wider topologies remain                                       obligations have content.
unmeasured.
                                                                     File                  Verified                 Role
7.3   From verified model to shipped package                         .rs                   10, 0 err.               ledger/frontier core (EO/CO,
                                                                                                                    PC, FD keying)
R EMIT ships as an installable package (remit-contract;              _cv.rs                2, 0 err.                CV gate lemmas
MIT) with a deliberate division of labor: every contract decision    _all.rs               12, 0 err.               composed legacy target
                                                                                                                    (overlaps rows above)
is computed in Rust; Python translates types and applies verdicts.   _fd_machine.rs        5, 0 err.                FD behavioral half (inductive)
Rust is the substrate Verus verifies and one abi3 wheel ships        _rd_interp.rs         6, 0 err.                RD order-independence,
the core with no toolchain on the user’s machine; the claimed                                                       completed window
                                                                     _recover_exec.rs      7, 0 err.                executable recovery core (CI
novelty is never the language, only the contract the core                                                           line-identical to shipped)
enforces.                                                            _ledger_exec.rs       11, 0 err.               executable EO admission,
                                                                                                                    PC/CV commit gate
     Three layers. (i) remit-core, a Rust crate                      negative/ (2 files)   1 err. each, by design   stock #6663 serve rule and
(#![forbid(unsafe_code)], zero-dependency test                                                                      order-sensitive #8039 rule
                                                                                                                    falsified
suite) re-implementing the verified abstract model item
for item: the append-only effect ledger with exactly-once
admission, the prefix-monotone commit gate with validity
                                                                     InMemorySaver control — and the writer lock surfaces in
ordered before any append, ⟨checkpointId , resumeIndex ⟩
                                                                     the tail (k=64 p95 of 2.7 s on SQLite against 1.3 s on Postgres
branch keying, the probe-134 view rule as a pure function,
                                                                     on the developer host, an ordering the container’s overlay-
the per-plane sequencer/journal, and recovery as a
                                                                     filesystem Postgres does not reproduce). That is why only cor-
pure, order-independent function of the durable log;
                                                                     rectness verdicts and within-environment relative overheads
VERIFICATION.md tabulates the lemma-to-function corre-
                                                                     travel (receipts: results/matrix/157_*.json). Integra-
spondence. (ii) remit-py, a PyO3 layer exposing contract
                                                                     tion at the paper’s pins replays the probe-134 protocol against
violations as typed exceptions (RemitDuplicateEffect,
                                                                     the Rust-core shim on LangGraph 1.2.9 — eight cells, all pass-
RemitPrefixViolation,                 RemitValidityError,
                                                                     ing: bare and resume-map forks served their own values with
RemitOrderViolation,            and,     from     the     v0.1.2
                                                                     the per-branch ledger [1, 0] on both backends; same-value
cross-process        gate,        RemitConsumeConflict).
                                                                     re-fork deterministic; stray resume inert within one process;
(iii) remit.langgraph_shim, a decision-free veneer
                                                                     the validator raise surfacing as RemitValidityError with
over any BaseCheckpointSaver: get_tuple describes
                                                                     nothing persisted; the core journal strictly ordered; and the
the addressing to the core and applies its strip/keep verdict;
                                                                     stock saver reproducing #6663 as the differential control —
put reports the user validator’s answer to the validity gate,
                                                                     replicated container-and-host, re-executed by CI on every
which raises before anything is delegated; put_writes
                                                                     push.
journals in the sequencer. Every conditional in the veneer
routes a core verdict or extracts a config field — an auditable
claim.                                                               7.4    Verification status and remaining obligations
     Three bodies of executable evidence sit behind Ta-              R EMIT’s Verus surface is a set of standalone
ble 9’s rungs 4–6. Model conformance (rung 5) transliter-            targets, each with a per-file tally on the pinned
ates ResumeContract.tla’s action alphabet — enabling                 toolchain (Verus 0.2026.05.03.8b81855), recorded in
conditions included — against the Rust core, shadowing               crates/remit/VERIFICATION.md and collected as
the TLA+ variables independently so that agreement is a              Table 8; targets overlap where a composed file restates
claim about two implementations, and re-checking all six             standalone ones, so no cross-file sum is claimed. Table 8
invariants after every action; a seeded randomized arm runs          gives the surface row by row. Two rows carry more weight
2×104 sequences of up to 48 actions, and the exhaustive              than their tallies suggest. The negative/ certificates are
arm removes the sampling caveat outright. Its state count            the mechanized evidence that the positive obligations have
exceeds TLC’s 87/59 by design — implementation-level state           content: they restate the same obligations under the stock
is finer, merging fewer histories; the exhaustiveness claim is       #6663 serving rule and the order-sensitive #8039 recovery
unchanged. Concurrency (rung 6) drives admission, forking,           rule, and Verus rejects both. They are excluded from every
and sequencing from up to 64 threads, checking exactly-              verify-all path and checked only through their documented
once admission, gap-free contiguous fork ordinals, a gap-free        commands, so a green build never depends on an expected
per-plane journal, and inertness of racing stray resumes;            failure.
probe 157 then measures the end-to-end question over                     Table 9 answers not what is proved but how far down
one shared saver, k ∈ {1, 4, 16, 64}, N =200 protocols per           the proof reaches. Rung 5 carries most of the weight: the
cell, four arms, both environments. Two structural findings          composite state machine — precisely the component this
ride along: throughput is flat in k under both backends in           paper declines to call verified — has its transliterated
both environments while median latency grows roughly                 transition system exhaustively enumerated against the six
linearly — the serialization ceiling is the process (GIL-            invariants at both bound sets, a complete check of a finite
bound), not the backend, corroborated by a persistence-free          structure. Rung 7 is the honest weak one, and rung 8 is
                                                                                                                                       19

                               TABLE 9                                     its accept/refuse decisions routed through the core’s pure
 How far the proof reaches. Each rung is a distinct kind of mechanized     verdict functions. The production-scale engine head-to-head
  evidence, not a restatement of the one above; tallies are Table 8’s.
Rung 5 is exhaustive over a finite structure rather than sampled, and it   is scoped out rather than owed, for the reason Section 8
covers the composite state machine. Rung 7 is audited by construction      gives.
and reading, not mechanically. Rung 8 is absent and is the paper’s one
                      unqualified verification gap.
                                                                           8   R ELATED W ORK
  Mechanized evidence                         Strength                     Recovery layers around the contract. Crab [4] provides
1 Verus proofs over the abstract model: proved (model)                     semantics-aware OS-level checkpoint/restore for agent sand-
  ledger/frontier, CV gate, FD and RD                                      boxes; its recovery machinery synthesizes cached responses
  machines (10, 2, 5, 6 verified; 0 errors)                                precisely so a restored agent does not replay completed
2 Verus-verified executable functions, not proved (executable)             actions. DART [5] certifies rollback admissibility above
  spec-level lemmas: recovery core (7), EO
  admission and PC/CV commit gate (11);                                    persistence primitives. Both are complementary by layer
  0 errors                                                                 (Fig. 1); neither specifies or measures the primitive’s own
3 recover_core line-identical to the mechanically enforced                 semantics.
  shipped function in src/lib.rs, CI-                                          Semantic rollback attacks and approval integrity. Clos-
  gated on every push
                                                                           est to the EO/CO axes, ACRFence [21] identifies Action
4 Differential bridge from the rung-2 twins exhaustive at bound
  to the shipped HashSet/HashMap im-                                       Replay and Authority Resurrection as attack classes in agent
  plementations (∼70k sequences, in CI)                                    checkpoint–restore and mitigates them by recording irre-
5 Composite core against the TLA+ transi- exhaustive at bound              versible tool effects with replay-or-fork semantics on restora-
  tion relation: BFS over 6,110 distinct states                            tion — the adversarial face of EO and CO, and the mitigation
  / 13,035 transitions at R0, and 414,675
  states / 1.07×106 transitions at scaled                                  family R EMIT instantiates. ACRFence establishes the threat
  bounds, six invariants at every state                                    with a proof of concept and an issue survey; this paper
6 64-thread admission/fork/sequencing tested under concurrency             specifies the contract as a machine-checked model, measures
  stress; probe 157’s 6,400 end-to-end proto-                              conformance deterministically across five frameworks and
  col executions, per-protocol exactly-once
  in all                                                                   three backends, and ships a repair at the checkpointer
7 Decision-freeness of the Python veneer audited, not checked              interface — FI is the protocol-level form of its replay-or-
  (every conditional routes a core verdict or                              fork discrimination. Consent-integrity mediation [6] binds an
  extracts a config field)                                                 approval to the true content of the action; FD/CO address the
8 Refinement relation, Verus model → com- absent
  piled core
                                                                           orthogonal lifecycle axis — whether an answer is consumed
                                                                           once and whether a different answer yields a different branch
                                                                           — for which #6663 and the #2315 class [16] are the observed
                                                                           failures.
absent: no mechanized refinement connects the Verus model                      Testing and verifying agent frameworks. A 998-report
to the compiled core. Anvil [20] is the closest artifact of the            empirical study locates the dominant bug mass in execution-
same shape, including in what it declines to claim end to                  semantics mechanisms [22]; LogicHunter [7] generates frame-
end.                                                                       work tests with an agentic oracle; robustness benchmarks [23]
    An earlier claim of a single fifteen-item composed                     measure task success under perturbation. These are horizon-
discharge is retired with the deleted definitional lem-                    tal; this paper is the vertical: a named contract, a checked
mas, and the full discharge log — including a with-                        model, conformance verdicts, a reference implementation.
drawn CV/RD file that carried placeholder assume(false)                    The control-plane half of the same lifecycle — whether stop
bodies — is recorded with dates in VERIFICATION.md.                        suppresses externally visible effects — is measured and
CV is additionally demonstrated live (probe 123) and                       repaired by SoundGate [17], which establishes one property
RD carries the executor-layer and adversarial-order evi-                   of one primitive from an enforcement point outside the
dence (probes 124, 136). The production sequencer behind                   runtime, where complete mediation follows from where the
BaseCheckpointSaver ships (Section 7.3), with the con-                     gate stands. R EMIT inherits the harder position: checkpoint
tract decisions in Rust and the explicit fork flag the FI                  and resume are the plane, so it interposes inside the runtime
obligation calls for available as the deployment discriminator             and must measure its mediation rather than assume it
(fork_on_explicit_checkpoint=False plus a config-                          (Sec. 7.2) — the two papers are the same question asked
urable flag key). The unverified surface is narrowed and                   on either side of that line, and the lineage is literal at
named: no mechanized refinement connects the Verus model                   one point: the ordering hazard formalized here as RD
to the compiled remit-core (the conformance harness                        (#8039, Sec. 2) surfaced as an unresolved residue of that
and concurrency suite are bridge evidence, not proof); the                 measurement and was filed upstream there. AgentConform —
PyO3 boundary and the decision-free veneer are unverified                  the conformance checker of the AgentRFC framework [24] —
Python-facing code, mitigated by construction and audit;                   tests agent communication protocols against TLA+ models: the
and every proof here remains a proof about R EMIT’s model,                 nearest methodological cousin, on a different object. Runtime-
never validation of any framework. The one item this list                  enforcement systems [25], [26] gate actions against policies;
previously deferred — promotion of Section 7.2’s read-                     the contract governs the substrate those gates rely on when
path consumption claim into the shipped shim — is done                     they checkpoint and resume. Failure-mode taxonomies [27]
(v0.1.2, opt-in), placing the gate itself on the unverified-               motivate the deployment stakes; SagaLLM [28] adds com-
Python side of the boundary like the rest of the veneer, with              pensation semantics above the plane this paper specifies.
                                                                                                                                           20

    The persistence traditions the plane did not inherit.                                          TABLE 10
Akka Persistence [14] and Orleans [29] offer event-sourced          The contract against the obligations mature durable-execution engines
                                                                     state for the analogous question. The column that matters is the last:
state with stated persistence semantics for stateful entities;       where an engine states the obligation, the contract is a restatement at
Erlang/OTP supervision [30] codifies restart-from-clean; and         another interface and no novelty is claimed; where it delegates to the
the persistent-language line — Argus’s guardians and atomic         application, or never exposes the write the obligation constrains, it does
actions [31], orthogonal persistence [32] — made durabil-               not transfer to a framework that adopted snapshots without the
                                                                                               surrounding model.
ity a language obligation with stated semantics decades
ago. Agent frameworks reimplemented the plane without
inheriting the discipline: event-sourced replay requires de-                     Durable             DBOS [35] (mea- Transfers?
                                                                                 Funcs.   [13]     / sured, probe 147)
terministic handlers, agent loops embed nondeterministic                         Temporal [34]
model calls, so the frameworks reached for snapshot-style
                                                                            PC stated: determin- stated: recorded yes
checkpointing — exactly the plane the contract governs. FD is                  istic replay with step results on
not linearizability [33], which constrains concurrent histories                memoized results re-execution
of one object, but a determinism obligation on branch                       EO delegated: activities steps transactional; no
creation from a durable point. A direct port of Orleans-style                  at-least-once;        external       effects
                                                                               exactly-once          still caller-keyed
grain persistence or Akka’s journal is a plausible alternative                 effects           are
repair to R EMIT.                                                              the          caller’s
    Why not just use Temporal or DBOS. Durable-execution                       idempotency
engines enforce determinism and exactly-once, but impose                       key
                                                                            FD branch      identity fork_workflow partly
their execution model: Temporal (and its Cadence ancestry)
                                                                               engine-defined        at a recorded step:
quarantines nondeterminism behind activities, side-effect                                            an explicit branch
APIs, and versioning [34]; DBOS ties steps to database trans-                                        address
actions [35]; hosted orchestrators externalize the workflow                 CV engine         owns same                     no
                                                                               serialization;
definition entirely [36]. Agent frameworks chose lighter,
                                                                               no caller-facing
model-native persistence precisely to avoid these constraints;                 validity obligation
the contract lets them keep that choice while stating the                   CO duplicate external send carries an partly
guarantees they must still meet. Adopting the durable-                         signals are the idempotency key
execution model wholesale is a legitimate path this paper                      caller’s problem
                                                                            RD stated: determin- stated:          transac- yes
does not oppose; the contract governs the frameworks                           ism plus version- tional steps
that opted out. Section 6.7 runs the paper’s workload                          ing
on an embedded engine and measures every probed cell
conformant, at 2.9–5.0× the checkpointer path’s gate-answer
latency: the engine measurement prices the alternative, and
R EMIT’s own baseline is the stock checkpointer it interposes       it does not come out uniformly in this paper’s favor. PC
on (Supplement Table S3).                                           and RD are restatements of obligations those engines already
    Formal semantics for durable execution. Realizing               state, and nothing is claimed for them beyond carrying them
exactly-once external effects is the closest prior obligation       to an interface where they were absent. The load-bearing
to EO: Olive achieves it for cloud storage by pairing an            rows are the other four. EO is the sharpest: Temporal’s
intent log with idempotent, resumable operations [37], and          activities are at-least-once and its exactly-once story for
the contract’s EO is that discipline stated as a caller-visible     external effects is a caller-supplied idempotency key, so the
obligation on a plane that has neither the log nor the              contract’s EO is stronger than what the canonical durable-
idempotence. Closest in method is Flux [38], which auto-            execution engine promises — “just use Temporal” does not
matically verifies idempotence consistency of stateful serverless   dissolve the question, it relocates it into user code, which
applications — CO-e’s shape one layer up. The layer is the          is Remark 4’s composition seen from the other side. CV
whole difference: Flux verifies that the application’s functions    has no counterpart at all, because an engine that owns its
tolerate the platform’s retries, while the R ESUME C ONTRACT        own serialization never exposes the write whose validity
asks whether the plane’s own primitives keep their promises         CV constrains — the agent frameworks do expose it, and
— no per-node idempotence proof could have caught #6663,            one of them corrupts it silently. FD and CO transfer only in
where the second value is discarded during task preparation         part, and DBOS is the instructive case: it satisfies both on the
before any node runs. The nearest prior act of writing resume       probed cells precisely because it ships the two discriminators
down is the published semantics for Durable Functions [13];         the FI obligation demands, a documented branch-creating
Beldi [39], Netherite [40], the shared-log successors (Boki [41],   address and an idempotency key on the delivery API —
Halfmoon [42]), and AMBROSIA [43] build logged-effect or            corroboration of FI’s necessity from a system built without
replay-based exactly-once serverless execution, and Restate         reference to this contract.
ships durable promises aimed at agent loops [44] — each                 Verified systems, crash recovery, and below-API check-
gives one engine a semantics enforced by construction, engine-      pointing. IronFleet [45], Verdi [46], and Perennial [47] define
internal for the reason Table 10 records, while this paper          the assurance bar a mechanized refinement from R EMIT’s
specifies a contract for an ecosystem of frameworks, none of        Verus model to its compiled core would meet, and FSCQ [48]
which, to our knowledge, states one; the novelty claim is           and GoJournal [49] prove crash safety with refinement
scoped to agent frameworks, not to formal resume semantics.         to running code — the bar Section 9 names as absent
Table 10 makes the comparison property by property, and             here. Beyond Verus itself [3], Anvil [20] verifies cluster-
                                                                                                                                 21

management controllers in Rust — the closest existing               tematic counterpoint. The #8039 ordering defect motivating
instance of R EMIT’s shape, and scoped in Sec. 7.4. RD’s            RD is in LangGraph’s tracker [92].
identical-logs, identical-decisions discipline is foundational          Isolation anomalies and black-box anomaly inference.
in state-machine replication (Viewstamped Replication [50],         The cross-process consume-once failure is a lost update on a
Raft [51]); no novelty is claimed for the principle, only           read–modify–write nobody made atomic, and its natural
its statement at an interface that lacks it. Below the API,         vocabulary is the isolation literature: beyond the ANSI
record-and-replay (rr [52]), process-level checkpoint/restore       critique [19], Adya et al.’s implementation-independent
(CRIU, DMTCP [53]), and multi-level HPC checkpointing               definitions [93] are the portable form of the anomaly, and
(BLCR [54], SCR [55], VeloC [56]) supply determinism and            Elle [94] is the state of the art in inferring such anomalies
state capture whose concern is I/O cost and fidelity, not API-      from client-observable histories — precisely the epistemic
level effect semantics; RD and PC restate those obligations at      position probe 159’s oracle occupies, and the discipline a
the API level for a plane that adopted snapshots without the        multi-racer characterization of that cell should adopt. We
discipline. Stating obligations over an observable interface        name these rather than claim them: this paper exhibits the
has its own lineage — design by contract [57], interface            anomaly at one concurrency shape and does not classify the
automata [58], session types [59], lightweight modeling in          plane’s isolation level.
Alloy [60] — of which the R ESUME C ONTRACT is the resume-
plane instance.
    Workflow recovery, effect discipline, and language-             9   T HREATS TO VALIDITY
level suspension. What may re-execute on resume has a               Construct: is a documented weakness a violation? The
two-decade literature agent frameworks did not inherit: the         classification rule (Table 5, note b) is total and symmetric,
ConTract model [61] (whose name this paper’s title unknow-          and it moves labels rather than measurements: under it
ingly echoes), workflow recovery [62], the workflow-pattern         LlamaIndex Workflows’s prefix replay is D, LangGraph’s
catalogs [63], exception patterns [64], and compensation            fork behavior and CrewAI’s checkpointing behavior are
from Sagas [65] onward; Petri-net workflow soundness [66]           ✗, and CrewAI’s @persist restore is U. The strongest
and BPMN semantics [67] established machine-checkable               CrewAI claim (task skipping) is stated for crews, whose
process models two decades earlier, and TCC-style atomic            probe requires live agents and is scheduled for the full matrix.
interactions [68] are the REST-era compensation discipline.             Construct: mechanism comparability and model ground-
Helland’s idempotence line [11], [12] is the canonical ar-          ing. Matrix cells compare properties, not mechanisms:
gument that exactly-once effects require application-level          LlamaIndex Workflows’s fork ✓ rests on client-side snap-
idempotency keys — Remark 4’s FD-plus-key composition is            shot copies where LangGraph’s ✗ concerns a server-side
that argument at the fork — and Ramalingam and Vaswani              thread fork, so cross-framework FD cells certify the prop-
derive idempotence by construction for interrupted workflow         erty on each framework’s own idiom. The EO crash-
programs [69], the language-level ancestor of the discipline        path classification is resolved by the documentation audit
EO/CO place on the framework. At the RPC layer the lineage          (Sec. 6); a maintainer clarification would reclassify the cell
runs from at-most-once call semantics [70] to RIFL’s durable        as documented divergence without changing the measure-
completion records consulted before re-execution [71] — the         ment. LangGraphFork.tla is an operational abstraction
exactly-once discipline whose checkpointer-plane analogue           grounded in the reproduced behavior and a source reading at
is R EMIT’s ledger. In programming-language terms the plane         the pinned versions (Sec. 4.3); it remains expert-established
is a durable delimited continuation [72], [73], operationally a     rather than mechanically extracted, which is why model
persisted effect handler [74]; the web-continuation line met        grounding and behavioral verdicts are kept separately au-
the same back-button fork and resolved it the same way —            ditable.
explicit branch identity [75]. Ray [76] rebuilds actor state from       Construct: effect oracle. The primary oracle is a process-
lineage inside the substrate several agent frameworks run           local counter, which captures non-idempotent re-execution
on; Airflow [77] and Prefect [78] push into user task code the      exactly but not production latencies or failure modes. The
idempotency discipline EO/CO here place on the framework;           durable-backend probes add an on-disk external ledger as a
Kafka’s transactional dual-write [79] solved commit-and-fire        second oracle, agreeing on every reported cell (probe 126);
one layer down; crash-only design [80] anticipates the stance       probe 142 moves the state holder out of the tested process
that recovery paths are primary.                                    entirely — an external service in a separate OS process
    Classical foundations and methodology. The properties           whose SQLite state survives the workflow’s SIGKILL and
instantiate classical notions — rollback-recovery determin-         records the duplicated re-execution (⟨s1, s1, s2⟩). A remote
ism [15], distributed snapshots [81], exactly-once state man-       third party with production failure modes remains out of
agement in stream processing (Flink [10], MillWheel [82]),          scope; its interface to the contract is Remark 4’s idempotency-
ARIES’ repeating history [83] — at an interface where               key composition. The live cells (Sec. 6.5) audit counters at
they are absent. Methodologically the harness descends              N =20 per cell (probe 148; 240 runs, zero harness errors),
from crash-consistency conformance testing (ALICE [84],             and probe 131 catches the live fork violation via the external
CrashMonkey/B3 [85]), Jepsen’s [86] stance of checking              ledger in 80/80 runs — the oracle’s live validation is neither
implementations against stated contracts, and ioco-style            pass-only, single-model, nor single-host. Probe 152 closes
model-based testing [87], over industrial TLA+ practice [88],       PC and CV live through lineage and schema observables;
[89] — transplanted to a layer where the first task is to write     live validation of RD would require semantics-stable model
the contract down; the fault switches instantiate specification     output and is out of scope by design. Replication numbers
mutation [90], with lineage-driven fault injection [91] the sys-    are reported as observed frequencies with Wilson intervals;
                                                                                                                           22

the determinism argument is the mechanism account, never replicate across container and host with zero divergent stable
the sample.                                                     fields. The harness contains no timing, no randomness, and
     Internal: probe fidelity. Each LangGraph probe is built no model calls, so verdicts can change only with package
from the minimal reproduction in the corresponding public versions, which are pinned.
issue, extended with effect counters; the version sweep             External: breadth and drift. The study covers five frame-
(Sec. 2.3) guards against single-version artifacts; raw JSON works — three in depth, plus AutoGen AgentChat’s restore
outputs ship in the artifact. Every pilot verdict replicated plane and pydantic-graph’s persistence more narrowly —
bit-identically on a second, separately provisioned developer on documented paths; AG2, the OpenAI Agents SDK, the
host — a cross-host determinism check by the same team, Claude Agent SDK, and Agno are in the full matrix under
not an independent reproduction — (conventions follow construction. Individual violations may be patched upstream
our prior measurement work [95]); one live probe (131) had — #7361 and #6792 already were, after shipping as regressions
its model-construction import corrected post-campaign to — which is why the claims rest on the contract, the model,
match the committed environment’s pins — the framework and version-pinned receipts rather than on any single bug’s
path under test is untouched, and the re-run reproduces the longevity.
committed verdict fields — a determinism check that no              Ecological: abstraction of the effect and of the crash.
hidden host dependence leaks into verdicts, not independent Neither oracle is a real payment-style API; the oracles
methodological validation. A source-level mutation study audit the framework’s invocation discipline, while end-to-end
(probe 156) tests whether verdicts are causally coupled to delivery under partition or duplication belongs to the effect
the located mechanisms: eight first-order mutants, hand- layer’s idempotency-key composition (Remark 4). The cross-
derived at the resume-serving sites the mechanism accounts process CO cell (probe 159) establishes that the sequential
name and each anchored to a unique line of the vendored inertness guarantee does not compose across processes, not
source, were applied one at a time with the probe suite byte- a rate; probe 168 widens the shape to k=16 and 25 ms
unchanged; all eight were killed on both hosts, including the jitter over 40 cells on both backends and measures the
mutant at the exact precedence line the located #6663 mecha- window by dose–response (Sec. 6). Three residual limits
nism names (a causal-coupling check; no mutation-adequacy are named: the dose–response arm ran on the developer host
score is claimed, and hand-placed mutants at watched alone; its backend columns share a jitter seed, so they are
sites cannot answer the tuned-to-known-bugs charge). The paired and carry no weight for backend invariance; and
complementary check mutates the harness (probes 169, 170, k>16 and wider jitter remain unmeasured, while cross-
172; the full operator table and per-operator analysis are in host distribution is measured at one two-host topology
the supplementary material, Sec. S1): probe 169 re-derives (probe 174), partitions excluded — what is established is
fifteen load-bearing verdicts from the committed stable-view that the window admits every racer arriving within it, with
receipts, fifteen of fifteen present and none in disagreement; no ceiling observed to sixteen, not that no ceiling exists.
four operators kill exactly their predicted cells — fork-value A transport-level client retry reduces, at this API, to the
blindness kills #6663 and nothing else, a state-only oracle duplicate-delivery cases already probed (126 sequential-inert,
and an undercounting ledger each kill the cross-process 159 concurrent-duplicating). The crash model is fail-stop at
consume-once cell, and barrier removal kills nothing, the process granularity: exception-based in the matrix, SIGKILL-
timing-free claim discharged in evidence — two operators based in probes 133/137/158/160, and in probe 164, which
required documented corrections before they said anything, extends real process death to the two remaining crash-
and crash no-op and pin drift are out of scope by construction. bearing cells — CrewAI’s checkpoint-restore duplication
Label-rule inversion has no mechanical site at all: the U/X and pydantic-graph’s mid-node unrecoverability reproduce
rule of Table 5 note b is applied when a reader assigns identically (3/3 and 3/3, both environments) — so no matrix
a verdict, not stored by any probe. Note b’s sensitivity crash verdict rests on exception semantics alone. Power
claim is therefore discharged by relabeling rather than loss, fsync reordering, and torn writes belong to the crash-
mutation; the recomputation (Supplement S4) shows the consistency literature [84], [85], below this plane. On the LLM-
strictest alternative rule touches exactly the two U cells, all free objection: the properties are stated over the persistence
ten separations of observation (i) stand, and the rule choice API and are model-independent by construction, so a model
moves labels, never the fragmentation result.                   in the loop can only add nondeterminism the properties
     Cross-environment claims carry their own mechanical already place outside f , and the live cells check in both direc-
guard, added after a near miss: a container receipt was once tions that real model traffic neither masks nor manufactures
produced by copying its developer-host twin and rewriting the deterministic verdicts (Sec. 6.5). What live traffic could
the host field — and because every cell agreed, which is still change — workload shapes reaching paths the probes
what the replication asserts, the substitution was invisible do not — is the prevalence question this paper does not
to any check reading the cells. Cell agreement is the claim, answer. Finally, the formal results divide by quantifier shape
so it cannot also be the check; the audit therefore asserts as Sec. 3.4 states: exhibited separations are settled by fully
that no two receipts bearing different host identifiers share a enumerated finite witnesses and need no upgrade, and of the
timestamp, so a copied receipt cannot pass as a replication. two universal claims, one is now discharged. TLAPS proves
The durable-backend probes (126–130) executed in a third, the reference conjunction unbounded: Reference ⇒ (Spec ⇒
separately provisioned environment (Sec. 5) and agree with □ ContractConjunction), by exactly the inductive invariant
every InMemorySaver-path verdict; every remaining probe exhibited in IndCheck.tla — TLC-checked inductive at
family, the scaled TLC configuration, the 39-cell matrix, the three constant sets (8,610 / 450,926 / 97,800 invariant-states,
packaged Rust/PyO3 suite, and the engine-baseline cells two conjuncts found by TLC rejecting weaker candidates —
                                                                                                                                            23

with its typing generalized from the model-checking bounds        a corpus-scale prevalence study. The immediate implication
to unbounded sequences, so the theorem holds at every             for practitioners is that “the framework has checkpointing”
constant assignment satisfying the module’s assumptions           licenses nothing about completed effects; the implication for
(ResumeContractProofs.tla: 196 obligations, zero omit-            framework authors is that the contract is checkable, the suite
ted, Zenon/SMT backends with Isabelle never invoked,              is a CI job, and resume can be made to mean resume.
replicated on two hosts under two tlapm builds; runner
and receipt in formal/tla/tlaps/, the receipt carrying
                                                                  R EFERENCES
the spec’s SHA-256 as proof the audited module is byte-
unchanged). Frontier monotonicity and the CO–EO con-              [1]  CrewAI, “Checkpointing,” documentation, https://docs.crewai.
                                                                       com/en/concepts/checkpointing, accessed 2026-07-16.
tainment are discharged as lemmas in the same file. Two           [2] LlamaIndex, “Workflows API reference: Context,” documen-
disclosures keep the claim honest. The proof burden sits in            tation, https://developers.llamaindex.ai/python/workflows-api-
consecution, not sufficiency: the invariant’s load-bearing             reference/context/, accessed 2026-07-16.
                                                                  [3] A. Lattuada et al., “Verus: Verifying Rust programs using linear
conjunct is that the durable frontier trails the program
                                                                       ghost types,” Proc. ACM Program. Lang., vol. 7, no. OOPSLA1, 2023.
counter by exactly one — ExecTask is the sole writer of           [4] T. Wu, C. Chang, L. Cao, W. Gao, and W. Wang, “Crab: A semantics-
the prefix-regression flag, its write guarded by a condition           aware checkpoint/restore runtime for agent sandboxes,” arXiv
that conjunct forbids — so for the properties the invariant            preprint arXiv:2604.28138, 2026.
                                                                  [5] K. Yang, P. Li, Z. Wu, K. Xu, H. Huang, and X. Huang, “DART:
carries structurally, the implication step is near-definitional        Semantic recoverability for structured tool agents,” arXiv preprint
and the theorem’s content is preservation under every                  arXiv:2605.23311, 2026.
action. And the proofs module names the specification’s           [6] X. Weng, “What you approve is what executes: Consent integrity
own unnamed ASSUME verbatim (a tlapm citation limitation               for black-box LLM agents,” arXiv preprint arXiv:2606.02668, 2026.
                                                                  [7] M. Long et al., “LogicHunter: Testing LLM agent frameworks with
across EXTENDS); the trust base is unchanged. Fault-footprint          an agentic oracle,” arXiv preprint arXiv:2607.06195, 2026.
completeness retains its bound-relative status — exhaustive       [8] LangChain, “LangGraph persistence and interrupts,” docu-
at stated constants, re-derived an order of magnitude wider,           mentation, https://docs.langchain.com/oss/python/langgraph/
                                                                       persistence, accessed 2026-07-16.
silent beyond — and liveness, the parked companion module,        [9] LlamaIndex, “Agent workflows: Human in the loop,” documenta-
and the consumption-counting matrix remain TLC-checked                 tion, https://developers.llamaindex.ai/python/examples/agent/
results; TLAPS obligations for a consistency-level lattice are         agent workflow basic/, accessed 2026-07-16.
discharged in adjacent work [96].                                 [10] P. Carbone et al., “State management in Apache Flink: Consistent
                                                                       stateful distributed stream processing,” Proc. VLDB Endowment,
                                                                       vol. 10, no. 12, 2017.
                                                                  [11] P. Helland, “Life beyond distributed transactions: An apostate’s
10    C ONCLUSION                                                      opinion,” in Proc. CIDR, 2007.
                                                                  [12] P. Helland, “Idempotence is not a medical condition,” ACM Queue,
The resume plane of LLM-agent frameworks carries human                 vol. 10, no. 4, 2012.
approvals and non-idempotent effects across interrupts,           [13] S. Burckhardt, C. Gillum, D. Justo, K. Kallas, C. McMahon, and C. S.
crashes, and restores, and it does so today without a stated           Meiklejohn, “Durable functions: Semantics for stateful serverless,”
semantics: three major frameworks document three incom-                Proc. ACM Program. Lang., vol. 5, no. OOPSLA, 2021.
                                                                  [14] Lightbend, “Akka Persistence: Event sourcing for stateful actors,”
patible disciplines, two violate even the semantics they state         documentation, https://doc.akka.io/, accessed 2026.
or imply, and the plane regresses across point releases with      [15] E. N. Elnozahy, L. Alvisi, Y.-M. Wang, and D. B. Johnson, “A survey
user issues as its only specification. The R ESUME C ONTRACT           of rollback-recovery protocols in message-passing systems,” ACM
                                                                       Computing Surveys, vol. 34, no. 3, pp. 375–408, 2002.
names the properties that make “resume” mean something;           [16] CopilotKit, “Issue #2315: LangGraph interrupt fails due to extra
a TLA+ model checks a reference semantics, exhibits each               null-state turn between trigger and resume,” https://github.com/
observed failure as a short counterexample, and maps every             CopilotKit/CopilotKit/issues/2315, 2025.
injected fault’s full violation footprint; and a determinis-      [17] S. Khan, “Stop means stop: Measuring and repairing the enforce-
                                                                       ment gap in agent-framework control primitives,” arXiv preprint
tic, LLM-free harness turns the properties into per-release            arXiv:2607.14166, 2026.
conformance verdicts. It delivers the contract with its fork-     [18] OpenAI, “Agents SDK: Sessions,” documentation, https://openai.
intent obligation; the machine-checked model with its partial-         github.io/openai-agents-python/sessions/, accessed 2026-07-16.
                                                                  [19] H. Berenson, P. Bernstein, J. Gray, J. Melton, E. O’Neil, and P. O’Neil,
independence result and its reference conjunction TLAPS-               “A critique of ANSI SQL isolation levels,” in Proc. ACM SIGMOD,
proved unbounded; a source-grounded, out-of-sample-tested              1995, pp. 1–10.
mechanism account of the fork violation; a backend-invariant,     [20] X. Sun, W. Ma, J. T. Gu, Z. Ma, T. Chajed, J. Howell, A. Lattuada,
version-stable measurement; the cross-process characteriza-            O. Padon, L. Suresh, A. Szekeres, and T. Xu, “Anvil: Verifying
                                                                       liveness of cluster management controllers,” in Proc. USENIX OSDI,
tion — every racer within the window consumes, no ceiling              2024.
observed to k=16, the window tracking the gated node’s            [21] Y. Zheng, Y. Yang, W. Zhang, and A. Quinn, “ACRFence: Preventing
own duration by dose–response; the discharged Verus proofs             semantic rollback attacks in agent checkpoint-restore,” arXiv
                                                                       preprint arXiv:2603.20625, CoDAIM Workshop, 2026.
with the recovery core verified as a shipped executable;
                                                                  [22] X. Zhu et al., “An empirical study of bugs in modern LLM agent
and R EMIT itself, repairing the fork and validity cells with          frameworks,” arXiv preprint arXiv:2602.21806, 2026.
exactly-once intact across 6,400 concurrent protocols. The        [23] X. Liu et al., “AgentBench: Evaluating LLMs as agents,” in Proc.
cross-process cell is repaired at the read path and only there,        ICLR, 2024.
                                                                  [24] S. Zheng and Q. Zhang, “AgentRFC: Security design principles
in the shipped shim behind an opt-in gate (Sec. 7.2), holding          and conformance testing for agent protocols,” arXiv preprint
with racers on two hosts (probe 174: stock {2:10}, gate                arXiv:2603.23801, 2026.
{1:10}) — two matched pairs establishing that interposition       [25] H. Wang, C. M. Poskitt, J. Sun, and J. Wei, “Pro2Guard: Proactive
below a decision cannot veto it. What it defers, and rests             runtime enforcement of LLM agent safety via probabilistic model
                                                                       checking,” arXiv preprint arXiv:2508.00500, 2025.
no claim upon: mechanized refinement from the verified            [26] L. Miculicich et al., “VeriGuard: Enhancing LLM agent safety via
model to the compiled core, deeper concurrent nesting and              verified code generation,” arXiv preprint arXiv:2510.05156, 2025.
                                                                                                                                                     24

[27] M. Cemri et al., “Why do multi-agent LLM systems fail?” arXiv           [54] P. H. Hargrove and J. C. Duell, “Berkeley Lab Checkpoint/Restart
     preprint arXiv:2503.13657, 2025.                                             (BLCR) for Linux clusters,” Journal of Physics: Conference Series,
[28] E. Y. Chang and L. Geng, “SagaLLM: Context management, vali-                 vol. 46, pp. 494–499, 2006.
     dation, and transaction guarantees for multi-agent LLM planning,”       [55] A. Moody, G. Bronevetsky, K. Mohror, and B. R. de Supinski,
     arXiv preprint arXiv:2503.11951, 2025.                                       “Design, modeling, and evaluation of a scalable multi-level check-
[29] P. Bernstein, S. Bykov, A. Geller, G. Kliot, and J. Thelin, “Orleans:        pointing system,” in Proc. ACM/IEEE SC, 2010.
     Distributed virtual actors for programmability and scalability,”        [56] B. Nicolae, A. Moody, E. Gonsiorowski, K. Mohror, and F. Cap-
     Microsoft Research Tech. Rep. MSR-TR-2014-41, 2014.                          pello, “VeloC: Towards high performance adaptive asynchronous
[30] J. Armstrong, Making Reliable Distributed Systems in the Presence            checkpointing at large scale,” in Proc. IEEE IPDPS, 2019.
     of Software Errors. PhD thesis, KTH Royal Institute of Technology,      [57] B. Meyer, “Applying ‘design by contract’,” IEEE Computer, vol. 25,
     2003.                                                                        no. 10, pp. 40–51, 1992.
[31] B. Liskov, “Distributed programming in Argus,” Communications of        [58] L. de Alfaro and T. A. Henzinger, “Interface automata,” in Proc.
     the ACM, vol. 31, no. 3, pp. 300–312, 1988.                                  ACM ESEC/FSE, 2001, pp. 109–120.
[32] M. Atkinson and R. Morrison, “Orthogonally persistent object            [59] K. Honda, N. Yoshida, and M. Carbone, “Multiparty asynchronous
     systems,” The VLDB Journal, vol. 4, no. 3, pp. 319–401, 1995.                session types,” in Proc. ACM POPL, 2008, pp. 273–284.
[33] M. Herlihy and J. M. Wing, “Linearizability: A correctness condition    [60] D. Jackson, “Alloy: A lightweight object modelling notation,” ACM
     for concurrent objects,” ACM TOPLAS, vol. 12, no. 3, pp. 463–492,            Trans. Software Engineering and Methodology, vol. 11, no. 2, pp. 256–
     1990.                                                                        290, 2002.
[34] Temporal Technologies, “Workflow determinism and versioning,”           [61] H. Wächter and A. Reuter, “The ConTract model,” in Database
     documentation, https://docs.temporal.io/workflow-definition, ac-             Transaction Models for Advanced Applications, A. K. Elmagarmid, Ed.
     cessed 2026-07-16.                                                           Morgan Kaufmann, 1992, pp. 219–263.
[35] A. Skiadopoulos et al., “DBOS: A DBMS-oriented operating system,”       [62] J. Eder and W. Liebhart, “Workflow recovery,” in Proc. IFCIS CoopIS,
     Proc. VLDB Endowment, vol. 15, no. 1, 2022.                                  1996, pp. 124–134.
[36] Amazon Web Services, “AWS Step Functions developer guide,”              [63] W. M. P. van der Aalst, A. H. M. ter Hofstede, B. Kiepuszewski, and
     https://docs.aws.amazon.com/step-functions/, accessed 2026.                  A. P. Barros, “Workflow patterns,” Distributed and Parallel Databases,
                                                                                  vol. 14, no. 1, pp. 5–51, 2003.
[37] S. Setty, C. Su, J. R. Lorch, L. Zhou, H. Chen, P. Patel, and J. Ren,
                                                                             [64] N. Russell, W. M. P. van der Aalst, and A. H. M. ter Hofstede,
     “Realizing the fault-tolerance promise of cloud storage using locks
                                                                                  “Workflow exception patterns,” in Proc. CAiSE, 2006, pp. 288–302.
     with intent,” in Proc. USENIX OSDI, 2016, pp. 501–516.
                                                                             [65] H. Garcia-Molina and K. Salem, “Sagas,” in Proc. ACM SIGMOD,
[38] H. Ding, Z. Wang, Z. Shen, R. Chen, and H. Chen, “Automated
                                                                                  1987, pp. 249–259.
     verification of idempotence for stateful serverless applications,” in
     Proc. USENIX OSDI, 2023, pp. 887–910.                                   [66] W. M. P. van der Aalst, “The application of Petri nets to workflow
                                                                                  management,” Journal of Circuits, Systems and Computers, vol. 8,
[39] H. Zhang, A. Cardoza, P. B. Chen, S. Angel, and V. Liu, “Fault-
                                                                                  no. 1, pp. 21–66, 1998.
     tolerant and transactional stateful serverless workflows,” in Proc.
                                                                             [67] R. M. Dijkman, M. Dumas, and C. Ouyang, “Semantics and analysis
     USENIX OSDI, 2020.
                                                                                  of business process models in BPMN,” Information and Software
[40] S. Burckhardt, B. Chandramouli, C. Gillum, D. Justo, K. Kallas,              Technology, vol. 50, no. 12, pp. 1281–1294, 2008.
     C. McMahon, C. S. Meiklejohn, and X. Zhu, “Netherite: Efficient
                                                                             [68] G. Pardon and C. Pautasso, “Atomic distributed transactions: A
     execution of serverless workflows,” Proc. VLDB Endowment, vol. 15,
                                                                                  RESTful design,” in Proc. WWW Companion, 2014, pp. 943–948.
     no. 8, 2022.
                                                                             [69] G. Ramalingam and K. Vaswani, “Fault tolerance via idempotence,”
[41] Z. Jia and E. Witchel, “Boki: Stateful serverless computing with             in Proc. ACM POPL, 2013.
     shared logs,” in Proc. ACM SOSP, 2021, pp. 691–707.
                                                                             [70] A. D. Birrell and B. J. Nelson, “Implementing remote procedure
[42] S. Qi, X. Liu, and X. Jin, “Halfmoon: Log-optimal fault-tolerant             calls,” ACM Trans. Computer Systems, vol. 2, no. 1, pp. 39–59, 1984.
     stateful serverless computing,” in Proc. ACM SOSP, 2023, pp. 314–       [71] C. Lee, S. J. Park, A. Kejriwal, S. Matsushita, and J. Ousterhout,
     330.                                                                         “Implementing linearizability at large scale and low latency,” in
[43] J. Goldstein et al., “A.M.B.R.O.S.I.A: Providing performant virtual          Proc. ACM SOSP, 2015.
     resiliency for distributed applications,” Proc. VLDB Endowment,         [72] M. Felleisen, “The theory and practice of first-class prompts,” in
     vol. 13, no. 5, 2020.                                                        Proc. ACM POPL, 1988, pp. 180–190.
[44] Restate, “Durable execution and durable promises,” documenta-           [73] O. Danvy and A. Filinski, “Abstracting control,” in Proc. ACM LISP
     tion, https://docs.restate.dev/, accessed 2026-07-17.                        and Functional Programming, 1990, pp. 151–160.
[45] C. Hawblitzel, J. Howell, M. Kapritsos, J. R. Lorch, B. Parno,          [74] G. Plotkin and M. Pretnar, “Handlers of algebraic effects,” in Proc.
     M. L. Roberts, S. Setty, and B. Zill, “IronFleet: Proving practical          ESOP, 2009, pp. 80–94.
     distributed systems correct,” in Proc. ACM SOSP, 2015, pp. 1–17.        [75] C. Queinnec, “The influence of browsers on evaluators or, contin-
[46] J. R. Wilcox, D. Woos, P. Panchekha, Z. Tatlock, X. Wang, M. D.              uations to program web servers,” in Proc. ACM ICFP, 2000, pp.
     Ernst, and T. Anderson, “Verdi: A framework for implementing                 23–33.
     and formally verifying distributed systems,” in Proc. ACM PLDI,         [76] P. Moritz et al., “Ray: A distributed framework for emerging AI
     2015, pp. 357–368.                                                           applications,” in Proc. USENIX OSDI, 2018, pp. 561–577.
[47] T. Chajed, J. Tassarotti, M. F. Kaashoek, and N. Zeldovich, “Verify-    [77] Apache Software Foundation, “Apache Airflow: tasks and retries,”
     ing concurrent, crash-safe systems with Perennial,” in Proc. ACM             documentation, https://airflow.apache.org/docs/, accessed 2026.
     SOSP, 2019, pp. 243–258.                                                [78] Prefect Technologies, “Prefect: task caching and retries,” documen-
[48] H. Chen, D. Ziegler, T. Chajed, A. Chlipala, M. F. Kaashoek, and             tation, https://docs.prefect.io/, accessed 2026.
     N. Zeldovich, “Using Crash Hoare Logic for certifying the FSCQ          [79] G. Wang et al., “Consistency and completeness: Rethinking dis-
     file system,” in Proc. ACM SOSP, 2015, pp. 18–37.                            tributed stream processing in Apache Kafka,” in Proc. ACM
[49] T. Chajed, J. Tassarotti, M. Theng, M. F. Kaashoek, and N. Zeldovich,        SIGMOD, 2021, pp. 2602–2613.
     “GoJournal: A verified, concurrent, crash-safe journaling system,”      [80] G. Candea and A. Fox, “Crash-only software,” in Proc. USENIX
     in Proc. USENIX OSDI, 2021, pp. 423–439.                                     HotOS, 2003.
[50] B. M. Oki and B. H. Liskov, “Viewstamped replication: A new             [81] K. M. Chandy and L. Lamport, “Distributed snapshots: Determin-
     primary copy method to support highly-available distributed                  ing global states of distributed systems,” ACM Trans. Computer
     systems,” in Proc. ACM PODC, 1988, pp. 8–17.                                 Systems, vol. 3, no. 1, pp. 63–75, 1985.
[51] D. Ongaro and J. Ousterhout, “In search of an understandable            [82] T. Akidau, A. Balikov, K. Bekiroğlu, S. Chernyak, J. Haberman,
     consensus algorithm,” in Proc. USENIX ATC, 2014, pp. 305–319.                R. Lax, S. McVeety, D. Mills, P. Nordstrom, and S. Whittle,
[52] R. O’Callahan, C. Jones, N. Froyd, K. Huey, A. Noll, and N. Partush,         “MillWheel: Fault-tolerant stream processing at internet scale,” Proc.
     “Engineering record and replay for deployability,” in Proc. USENIX           VLDB Endowment, vol. 6, no. 11, pp. 1033–1044, 2013.
     ATC, 2017, pp. 377–389.                                                 [83] C. Mohan, D. Haderle, B. Lindsay, H. Pirahesh, and P. Schwarz,
[53] J. Ansel, K. Arya, and G. Cooperman, “DMTCP: Transparent                     “ARIES: A transaction recovery method supporting fine-granularity
     checkpointing for cluster computations and the desktop,” in Proc.            locking and partial rollbacks using write-ahead logging,” ACM
     IEEE IPDPS, 2009.                                                            Trans. Database Systems, vol. 17, no. 1, pp. 94–162, 1992.
                                                                            25

[84] T. S. Pillai et al., “All file systems are not created equal: On
     the complexity of crafting crash-consistent applications,” in Proc.
     USENIX OSDI, 2014.
[85] J. Mohan, A. Martinez, S. Ponnapalli, P. Raju, and V. Chidambaram,
     “Finding crash-consistency bugs with bounded black-box crash
     testing,” in Proc. USENIX OSDI, 2018.
[86] K. Kingsbury, “Jepsen: Distributed systems safety research,” https:
     //jepsen.io, accessed 2026.
[87] J. Tretmans, “Model based testing with labelled transition systems,”
     in Formal Methods and Testing, LNCS 4949. Springer, 2008, pp. 1–38.
[88] C. Newcombe, T. Rath, F. Zhang, B. Munteanu, M. Brooker, and
     M. Deardeuff, “How Amazon Web Services uses formal methods,”
     Communications of the ACM, vol. 58, no. 4, pp. 66–73, 2015.
[89] L. Lamport, Specifying Systems: The TLA+ Language and Tools for
     Hardware and Software Engineers. Addison-Wesley, 2002.
[90] P. Ammann, P. E. Black, and W. Majurski, “Using model checking
     to generate tests from specifications,” in Proc. IEEE ICFEM, 1998,
     pp. 46–54.
[91] P. Alvaro, J. Rosen, and J. M. Hellerstein, “Lineage-driven fault
     injection,” in Proc. ACM SIGMOD, 2015, pp. 331–346.
[92] LangGraph issue #8039, “Unenforced ordering between
     put_writes and put in synchronous durability,” https://github.
     com/langchain-ai/langgraph/issues/8039, 2026.
[93] A. Adya, B. Liskov, and P. O’Neil, “Generalized isolation level
     definitions,” in Proc. IEEE ICDE, 2000, pp. 67–78.
[94] K. Kingsbury and P. Alvaro, “Elle: Inferring isolation anomalies
     from experimental observations,” Proc. VLDB Endowment, vol. 14,
     no. 3, 2020.
[95] S. Khan, “Token budgets: An empirical catalog of budget-overrun
     incidents in LLM-agent frameworks,” manuscript under review,
     Empirical Software Engineering (EMSE-D-26-00583); preprint
     arXiv:2606.04056, 2026.
[96] S. Khan, “A consistency lattice for multi-agent memory: Specifi-
     cation, mechanized proof, and runtime enforcement,” manuscript
     under review; preprint arXiv:2606.17182, 2026.
