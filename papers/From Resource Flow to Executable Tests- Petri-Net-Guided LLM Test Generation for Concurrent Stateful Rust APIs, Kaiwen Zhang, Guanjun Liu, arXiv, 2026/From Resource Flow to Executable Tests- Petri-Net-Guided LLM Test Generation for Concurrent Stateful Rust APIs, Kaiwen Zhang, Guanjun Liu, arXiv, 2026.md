                                          From Resource Flow to Executable Tests: Petri-Net-Guided LLM
                                                Test Generation for Concurrent Stateful Rust APIs
                                                                                               Kaiwen Zhang, Guanjun Liu
                                                                                                        Tongji University
                                                                                                         Shanghai,China
                                                                                                     zhangkw@tongji.edu.cn

                                         Abstract                                                                   1    Introduction
                                         Concurrent stateful library APIs expose behavior through evolving          Many Rust library APIs are not isolated function interfaces. They
                                         resource ownership, lifecycle states, and competing interleavings.         expose handles, permits, closures, buffered state, and task-level
                                         Large language models can synthesize executable Rust tests, but            interaction patterns whose behavior depends on prior operations
                                         their outputs often violate API preconditions, remain shallow, or          and competing schedules. In this setting, Rust’s type system re-
                                         reduce concurrency to accidental sequential traces. Conversely,            moves broad classes of memory errors, but it does not prove that a
                                         model-based and systematic testing techniques provide semantic             library respects its higher-level protocol. The bugs that remain are
                                         control but commonly require substantial handwritten code to turn          semantic faults: a stale capability is still accepted, a close operation
                                         abstract scenarios into executable tests. This paper addresses the         invalidates the wrong behavior, a buffered value is lost, or a test
                                         gap between formal scenario design and low-cost test concretiza-           hangs only after a specific interleaving reaches a deep state.
arXiv:2607.21530v1 [cs.SE] 23 Jul 2026




                                         tion.                                                                          These APIs are difficult to test for three coupled reasons. First,
                                             We present a Petri-net-guided methodology for test generation          interesting behaviors are strongly stateful: many failure modes
                                         over concurrent stateful Rust APIs. The method represents API              appear only after a legal prefix establishes a nontrivial resource
                                         resources, lifecycle conditions, and causal dependencies as colored        configuration. Second, the prefix itself must be semantically disci-
                                         tokens and transitions; derives legal deep-state, near-legal, and          plined; otherwise later observations are meaningless because the
                                         partial-order concurrent scenarios; and uses these scenarios as a          test never exercised a valid protocol state. Third, concurrency mat-
                                         constrained intermediate representation for LLM-based code syn-            ters at the level of partial order rather than raw length. A long
                                         thesis. A local-faithfulness contract and structural repair loop pre-      sequence is not useful if it accidentally serializes the very race that
                                         serve the modeled intent during concretization, while Petri-guided         should have been exposed.
                                         schedule shaping prioritizes high-conflict concurrency skeletons               Existing approaches each cover only part of this space. Model-
                                         for systematic exploration. A layered semantic oracle then dis-            based and dependency-aware testing can describe legal states, re-
                                         tinguishes synthesis failures from violations of the target API’s          source flow, and boundary conditions, but converting those abstrac-
                                         expected behavior.                                                         tions into executable Rust tests still demands substantial handwrit-
                                             We implement a prototype for Rust concurrency libraries and de-        ten scaffolding, task orchestration, and API-specific assertions. Di-
                                         fine an evaluation protocol that examines executability, structural        rect LLM prompting reduces that coding burden, but it also pushes
                                         fidelity, deep-state reachability, boundary-failure yield, and con-        semantic responsibility back into the model. In practice, the LLM
                                         flict coverage. The central methodological principle is to separate        may invent events, violate enablement conditions, confuse reserved
                                         responsibilities: the Petri net specifies semantic intent, resource        capabilities with fresh ones, weaken assertions, or flatten concur-
                                         flow, reachability, conflict, and bug-relevant mutations, whereas the      rent behavior into a convenient sequential trace.
                                         LLM realizes library-specific syntax, task scaffolding, and assertions.        Our position in this paper is intentionally narrower. We do not
                                         This design provides a concrete basis for studying whether formal          ask the LLM to discover concurrency semantics from scratch, and
                                         resource-flow models can make LLM-generated concurrency tests              we do not claim to eliminate modeling effort. Instead, we use a
                                         more faithful, stateful, and diagnostically useful.                        Petri-net model to encode resource multiplicity, causality, conflict,
                                                                                                                    and near-legal boundary cases, then use the LLM only to realize
                                         CCS Concepts                                                               model-produced scenarios as executable Rust code. The scheduler
                                                                                                                    still explores runtime interleavings, and API-specific invariants still
                                         • Software and its engineering → Software testing and debug-
                                                                                                                    need to be authored. The point is to separate responsibilities so that
                                         ging; Formal software verification; Software reliability.
                                                                                                                    semantic intent stays outside the LLM while code realization stays
                                                                                                                    inexpensive.
                                         Keywords                                                                       This tradeoff fits concurrent stateful Rust APIs especially well. A
                                         Petri nets, large language models, Rust, concurrency testing, stateful     Petri net can represent senders, receivers, permits, capacity, buffered
                                         API testing, test generation                                               messages, and observation obligations as tokens, and it can express
                                                                                                                    the precise conflicts and causal dependencies that make a test di-
                                         ACM Reference Format:                                                      agnostically useful. Once that structure is explicit, the LLM can
                                         Kaiwen Zhang, Guanjun Liu. 2026. From Resource Flow to Executable Tests:   do what it is relatively good at: writing target-specific setup, task
                                         Petri-Net-Guided LLM Test Generation for Concurrent Stateful Rust APIs.    creation, assertions, and cleanup. The key design rule is simple: the
                                         In . ACM, New York, NY, USA, 9 pages. https://doi.org/10.1145/nnnnnnn.     model writes meaning, the LLM writes code.
                                         nnnnnnn
Conference’17, July 2017, Washington, DC, USA                                                                          Kaiwen Zhang, Guanjun Liu


   The price of this design is also clear. SyncPetri requires manually      Table 1: Example Petri-net places for a bounded mpsc.
authored resource models, adapters, and scenario invariants, and
its schedule shaping improves harness selection above tools such           Place                  Meaning
as Loom rather than replacing their internal search. We state these
                                                                           LiveSender(s)         Sender handle 𝑠 exists and may initiate send-
limitations up front because they define the appropriate contribu-                               side operations.
tion: not fully automatic concurrency verification, but a testing          LiveReceiver(r)       Receiver handle 𝑟 exists and may receive or
architecture that trades some modeling effort for stronger semantic                              close.
control over generated tests.                                              Open(c)               Channel 𝑐 accepts ordinary sends.
   Concretely, SyncPetri synthesizes legal deep-state traces, near-        Closed(c)             Channel 𝑐 has been closed from the receive
legal boundary probes, and partial-order concurrent scenarios from                               side.
a colored Petri net; concretizes them through a constrained prompt         Permit(s,c)           Sender 𝑠 holds a reserved permit on channel 𝑐.
and structural repair loop; and judges the resulting executions with       Cap(c,n)              Channel 𝑐 has 𝑛 unreserved buffer slots.
                                                                           Buf(c,n)              Abstract buffered-item count for channel 𝑐.
a layered oracle that separates concretization failure from semantic
                                                                           Obs(x)                Runtime observation token emitted by instru-
failure. The result is a testing pipeline designed for concurrent Rust
                                                                                                 mentation.
APIs whose hard bugs live in resource protocols rather than in
isolated function outputs.
   We make five contributions:
                                                                         2.1       Bug Model
     • We formalize concurrent stateful Rust API testing as Petri-       We target semantic faults that escape Rust’s type system and strict
       net-guided scenario synthesis over resource-carrying transi-      memory-safety checks. We classify these faults into four core fami-
       tions.                                                            lies:
     • We define an adapter schema and a local-faithfulness con-               • Bpre (Precondition Enforcement): An operation incor-
       tract that connects abstract Petri-net steps to concrete Rust             rectly succeeds even though its abstract prerequisite condi-
       executions.                                                               tion is violated (e.g., sending into a closed channel).
     • We define a scenario representation that unifies legal reach-           • Bstate (Post-State Inconsistency): Resource accounting, own-
       ability, near-legal boundary mutation, and partial-order con-             ership transfer, or cleanup logic diverges from the specifica-
       currency.                                                                 tion after an operation executes.
     • We present a constrained concretization loop and a multi-               • Brace (Race Sensitivity): A schedule-dependent interleaving
       layer oracle that distinguish generation failure from semantic            exposes an observation sequence or state variation that the
       failure.                                                                  high-level protocol strictly forbids.
     • We propose a Petri-guided schedule shaping method for                   • Blive (Liveness and Blocking): The implementation suffers
       Loom-compatible harnesses and instantiate the full workflow               from permanent blocking, dropped wake-ups, or a failure to
       on tokio::sync-style APIs.                                                terminate after reaching a terminal protocol state.
                                                                            For tokio::sync APIs, these categories correspond to concrete
2    Problem Setting and Running Example                                 fault shapes such as send-after-close success, stale-handle accep-
We target APIs with three fundamental properties: 1) Statefulness:       tance, lost notification after value update, inconsistent permit ac-
The outcome or validity of an operation depends heavily on the in-       counting, or non-terminating close races. This bug model serves as
ternal abstract resource state of the system. 2) Resource sensitivity:   the ground truth for our seeded mutant evaluation.
Operations directly manipulate capabilities—consuming, produc-
ing, splitting, merging, or invalidating handles, permits, buffered      2.2       Running Example and Baseline Pitfalls
data, or access tokens. 3) Concurrency exposure: Multiple distinct       We motivate the SyncPetri workflow using a capacity-one Tokio
tasks or handles interact simultaneously, meaning distinct execu-        MPSC channel. The setup involves a receiver 𝑅0 , an ordinary sender
tion schedules can yield entirely different observable outcomes.         𝑆𝑝 used to reserve capacity, and an independent sender 𝑆𝑏 acting
   This covers a useful slice of Rust libraries. In tokio::sync, for     as a boundary probe.
example, mpsc channels expose senders, receivers, permits, buffer-          The core semantic invariant of interest involves a subtle asyn-
ing, and closure; watch exposes latest-value semantics and observed      chronous contract: closing the receiver must immediately reject
states; broadcast exposes lagging receivers and replay boundaries;       new ordinary send operations, yet any pre-existing Permit or
and Semaphore exposes acquisition, release, and closure behav-           OwnedPermit successfully acquired prior to closure remains valid
ior [9–12]. These APIs are small enough to test locally but rich         and must be allowed to commit its message to the buffer [10]. The
enough to require genuine semantic orchestration. Table 1 shows a        receiver is then obligated to drain this outstanding message before
compact abstraction for a running mpsc example.                          final termination.
   The research problem is therefore: How can we synthesize seman-          This nuanced lifecycle contract creates several plausible seman-
tically meaningful concurrent test scenarios from a Petri-net model      tic faults: an implementation might erroneously drop the message
of a Rust API, concretize those scenarios into executable Rust code      backed by the outstanding permit upon closure, reject the valid per-
with an LLM, and judge whether the resulting execution preserves or      mit commit, or hang indefinitely due to internal desynchronization
violates the intended API semantics?                                     between close flags and permit counters.
From Resource Flow to Executable Tests: Petri-Net-Guided LLM Test Generation for Concurrent Stateful Rust APIs                 Conference’17, July 2017, Washington, DC, USA


   Traditional testing paradigms struggle to isolate this behavior. A                   Table 2: SyncPetri Responsibilities Division and Artifacts for
purely random concurrency fuzzer is highly unlikely to generate the                     the Motivating Example.
exact interleaved sequence required to hit this deep state (reserving
capacity, racing a close with a commit, and then validating the                           Stage         Model intent                            Realization
residual drain). Conversely, a pure prompt-only LLM routinely
                                                                                          Scenario      7 typed events, causal Immutable JSON prompt
suffers from two opposing failures: it either collapses the concurrent                                  edges ≺, conflict pair constraints.
execution into a simplified sequential trace that entirely misses                                       (𝑒 3 , 𝑒 4 )
the race, or it hallucinates a strict sequential rule (e.g., assuming
                                                                                          Code          Resource bindings, out- LLM generates tasks, scopes,
all operations fail post-close), thereby generating incorrect test
                                                                                                        come classes Φ, banned adapters, and assertions.
assertions that mismatch the API’s actual contract.                                                     edits
  Step 1: Resource Model and Deep State. Initially, the abstract initial                  Schedule      Frontier prioritized by un- Two shaped execution har-
marking 𝑀0 contains two live sender capabilities, one live receiver,                                    covered conflicts           nesses.
an open-channel token, and one capacity token. The first modeled                          Oracle        Ostr ∧ Oout ∧ Oinv ∧ Olive              Separates synthesis failures
event explicitly targets a deep state by reserving capacity:                                                                                    from API bugs.
                     𝑒 1 = reserveOwned(𝑆𝑝 ) → 𝑃0 .
The resulting marking moves the net into a distinct configuration                       rather than letting the model serialize the actions. Listing 1 illus-
containing Permit(𝑃 0, 𝑐) and Cap(𝑐, 0). This represents the deep                       trates the resulting code artifact. The LLM remains free to handle
state of interest: the channel possesses an outstanding, isolated send                  target-specific syntax and variable scoping but cannot strip the
capability (𝑃 0 ) distinct from an ordinary open sender or a simple                     structural instrumentation markers (mark).
buffered item. Crucially, the model dictates that the permit-commit
transition consumes 𝑃 0 without requiring Open(𝑐), while ordinary                       Listing 1: Schematic generated harness for the motivating
sends still depend on both Open(𝑐) and free capacity.                                   scenario.
                                                                                        let (sp, sb, mut r0) = bounded_with_clone(1);
  Step 2: Scenarios. From this marking, SyncPetri builds a partial-                     let p0 = mark(e1, || reserve_owned(sp));
                                                                                        let gate = deterministic_handshake();
order graph over 𝐸 = {𝑒 1, . . . , 𝑒 7 } with the following labels:                     let child = mark(e2, || spawn(move || {
                                                                                            gate.ready(); gate.wait_release();
      𝑒 1 : reserveOwned(𝑆𝑝 ) → 𝑃0,             𝑒 2 : spawn(𝑇1, 𝑃0 ),                       mark(e3, || p0.send(m1))
                                                                                        }));
      𝑒 3 : permitSend(𝑃0, 𝑚 1 ),               𝑒 4 : close(𝑅0 ),                       gate.wait_ready(); gate.release();
                                                                                        mark(e4, || r0.close());
      𝑒 5 : recv(𝑅0 ) → 𝑚 1,                    𝑒 6 : trySend(𝑆𝑏 , 𝑚 2 ),               join_bounded(child);
                                                                                        assert_msg(mark(e5, || recv(&mut r0)), m1);
      𝑒 7 : recvEnd(𝑅0 ).                                                               assert_closed(mark(e6, || sb.try_send(boundary_msg)));
                                                                                        assert_end(mark(e7, || recv_bounded(&mut r0)));
Rather than fixing a rigid, linear trace, only necessary causal de-
pendencies are captured in ≺:                                                              Step 4: Petri-Guided Schedule Exploration. The synthesized event
                        𝑒 1 ≺ 𝑒 2 ≺ 𝑒 3,      𝑒 1 ≺ 𝑒 4,                                graph induces two macro harnesses:
                     𝑒 3 ≺ 𝑒 5,      𝑒4 ≺ 𝑒5 ≺ 𝑒6 ≺ 𝑒7 .                                                     ℎ commit = [𝑒 1, 𝑒 2, 𝑒 3, 𝑒 4, 𝑒 5, 𝑒 6, 𝑒 7 ],
Events 𝑒 3 and 𝑒 4 are causally independent but compete for over-                                                ℎ close = [𝑒 1, 𝑒 2, 𝑒 4, 𝑒 3, 𝑒 5, 𝑒 6, 𝑒 7 ].
lapping resource fields, and are thus flagged as an explicit race                       The generated handshakes guarantee that the deep state 𝑃0 is es-
pair: (𝑒 3, 𝑒 4 ) ∈ #. This partial order safely encapsulates two valid                 tablished before the race window opens. A deterministic scheduler
interleavings: commit-before-close and close-before-commit. Event                       adapter (or Loom) then enumerates only the micro-interleavings
𝑒 6 acts as a near-legal boundary probe; following 𝑒 5 , the channel’s                  inside that window. This division of labor lets the Petri-net model
capacity is free but its state remains closed, meaning 𝑒 6 violates                     select the macro-concurrency surface while the runtime scheduler
exactly one enablement condition (Open(𝑐)). The expected obser-                         explores local execution choices.
vations are mapped as set-valued allowed classes:
                                                                                           Step 5: Oracle Decision and Report. On a compliant implemen-
               Φ𝑒3 = {SendOk},             Φ𝑒5 = {Msg(𝑚 1 )},                           tation, either linearization may occur at runtime. Regardless of
               Φ𝑒6 = {ClosedLike},         Φ𝑒7 = {End}.                                 whether 𝑒 3 or 𝑒 4 executes first, 𝑒 3 must yield SendOk, 𝑒 5 must ob-
                                                                                        serve 𝑚 1 , and the post-close boundary check 𝑒 6 must evaluate to
   Step 3: Constrained LLM Concretization. The structural graph is                      ClosedLike.
serialized into a highly constrained data prompt rather than a loose                       The layered oracle first invokes the structural checker (Ostr ) to
text description. The prompt provides explicit resource mappings,                       verify that all seven runtime markers executed in a sequence that
edge dependencies, and allowable outcome envelopes.                                     satisfies ≺. If an LLM error or compiler optimization reordered or
   To bridge the gap between abstract events and executable tasks,                      bypassed a marker, the run is flagged as a ConcretizationError
the framework derives execution scaffolding from the conflict rela-                     and pruned. If Ostr passes but the library returns an unmapped
tion. Because (𝑒 3, 𝑒 4 ) ∈ # is an active concurrency pair, the prompt                 observation class (e.g., if a mutant rejects the outstanding per-
requires explicit readiness, release, and completion handshakes                         mit during a close-first interleaving), the system registers a true
Conference’17, July 2017, Washington, DC, USA                                                                               Kaiwen Zhang, Guanjun Liu


SemanticFailure. The resulting diagnostic profile is recorded as:        denote one concrete adapter step from runtime state 𝜎 to 𝜎 ′ with
         Report = (S𝑝𝑐 , SemanticFailure, {out}, 𝜏 ★, ℎ close ).         raw observation 𝑜, and let Ω𝑡𝑜𝑘 , Ω𝑡𝑒𝑟𝑟 ⊆ Ω denote the modeled
                                                                         success and error observation classes of 𝑡. For legal steps, we require
This structured output ensures that hundreds of identical low-level                           𝑡
scheduler interleavings that expose the exact same root bug are                           − 𝑀 ′ =⇒ ∃𝜎 ′, 𝑜. Step𝑑 (𝑡, 𝜎, 𝛽 (𝑒)) { (𝜎 ′, 𝑜)
                                                                           𝜌𝑑 (𝜎) = 𝑀 ∧ 𝑀 →
seamlessly de-duplicated into a single actionable report.                                                  ∧ 𝜌𝑑 (𝜎 ′ ) = 𝑀 ′ ∧ Γ(𝑜) ∈ Ω𝑡𝑜𝑘 .
3 Formal Model                                                           For near-legal steps, we require that a single-precondition violation
                                                                         maps to an explicit error-class outcome:
3.1 API Abstraction and Colored Petri Net
                                                                                   𝜌𝑑 (𝜎) = 𝑀 ∧ |Δ𝐹 (𝑀, 𝑡)| + |Δ𝐺 (𝑀, 𝑡)| = 1
We begin with a lightweight API abstraction
                                                                                             =⇒ ∃𝜎 ′, 𝑜. Step𝑑 (𝑡, 𝜎, 𝛽 (𝑒)) { (𝜎 ′, 𝑜)
                             𝐴 = (𝑅, 𝑂, Σ, Ω),
                                                                                                  ∧ Γ(𝑜) ∈ Ω𝑡𝑒𝑟𝑟 .
where 𝑅 is a set of resource sorts, 𝑂 is a set of operation names, Σ
maps each operation to typed arguments and result classes, and Ω         This contract is intentionally lightweight. It requires the adapter
is a set of observation classes used by the runtime oracle.              to preserve the meaning of modeled steps and boundary failures
   The API abstraction is compiled into a colored Petri net              without demanding that every internal library state be exposed or
                                                                         reconstructed.
                       𝑁𝐴 = (𝑃,𝑇 , 𝐹, 𝜒, 𝜆, 𝑔, 𝑢, 𝑀0 ).
where 𝑃 is a finite set of places, 𝑇 is a finite set of transitions,     3.3    Reusable Transition Schemas
𝐹 ⊆ (𝑃 × 𝑇 ) ∪ (𝑇 × 𝑃) is the flow relation, 𝜒 maps each place to        To avoid making each Petri net a one-off artifact, we model concur-
a token color domain, 𝜆 : 𝑇 → 𝑂 labels transitions with API or           rent Rust APIs with a small library of reusable transition schemas.
harness operations, 𝑔𝑡 is a guard predicate for each transition 𝑡, 𝑢𝑡    A schema is a tuple
is a token-update function for each transition 𝑡, 𝑀0 is the initial
                                                                                             𝜃 = 𝑃𝜃𝑖𝑛 , 𝑃𝜃𝑜𝑢𝑡 , 𝑔𝜃 , 𝑢𝜃 , Ω𝜃 ,
                                                                                                                            
marking.
    Let 𝐼𝑡 (𝑝) and 𝑂𝑡 (𝑝) denote the input and output token multisets    consisting of typed input places, typed output places, a guard, a
of transition 𝑡 at place 𝑝. A transition is enabled under marking 𝑀      token-update rule, and the observation classes attached to the step.
iff                                                                      Instantiating a schema only requires binding symbolic place names
  enabled(𝑀, 𝑡) ⇐⇒ 𝑔𝑡 (𝑀) = true ∧ ∀𝑝 ∈ 𝑃, 𝐼𝑡 (𝑝) ⊆ 𝑀 (𝑝).               and resource identifiers.
                                                                            Four schemas are especially common in tokio::sync APIs:
If enabled(𝑀, 𝑡) holds, firing 𝑡 yields a new marking 𝑀 ′ defined by
                                                                          𝜃 clone :
                     𝑀 ′ = 𝑢𝑡 (𝑀 − 𝐼𝑡 ) + 𝑂𝑡 .
                                              
                                                                                 LiveHandle(𝑥 ) → LiveHandle(𝑥 ) + LiveHandle(𝑥 ′ ),
               𝑡                                       𝑡 1 ···𝑡𝑘          𝜃 reserve :
We write 𝑀 →− 𝑀 ′ for one firing step and 𝑀0 −−−−−→ 𝑀𝑘 for a finite              LiveSender(𝑠 ) + Open(𝑐 ) + Cap(𝑐, 𝑛)
firing sequence. The reachability set is                                         → LiveSender(𝑠 ) + Permit(𝑠, 𝑐 ) + Cap(𝑐, 𝑛 −1),
                                                   𝜋                      𝜃 close :
                   Reach(𝑁𝐴 ) = {𝑀 | ∃𝜋, 𝑀0 −
                                            → 𝑀 }.
                                                                                 LiveReceiver(𝑟 ) + Open(𝑐 ) → LiveReceiver(𝑟 ) + Closed(𝑐 ),
   The practical purpose of the net is not only to reject impossible      𝜃 consume :
calls. It records how resources move, which operations compete for               LiveReceiver(𝑟 ) + Buf(𝑐, 𝑛)
them, and which events are causally independent.                                 → LiveReceiver(𝑟 ) + Buf(𝑐, 𝑛 −1)
                                                                                  + Obs(RecvOk).
3.2     Adapter Schema and Local Faithfulness                             The guards on 𝜃 reserve and 𝜃 consume additionally require 𝑛 > 0.
The Petri net is abstract, but the test oracle runs over concrete Rust   Near-legal mutations then arise naturally by violating exactly one
executions. We therefore associate each target library domain 𝑑          of these guard or token conditions, such as attempting 𝜃 reserve when
with an adapter schema                                                   the channel is closed or capacity is exhausted.
      𝐴𝑑 = (Ctor, Step, Spawn, Mark, Assert, Cleanup, Γ, 𝜌𝑑 ).               These schemas transfer across the target API family. In mpsc,
                                                                         𝜃 reserve models permit acquisition; in Semaphore, the same schema
Here Ctor constructs the initial runtime objects, Step maps a mod-       models acquisition over capacity tokens; in watch, 𝜃 consume becomes
eled transition to a concrete Rust operation, Spawn packages spawn-      observation of an unseen update; and in broadcast, it becomes lag-
able event groups into tasks, Mark emits event markers, Assert           sensitive receive with a richer outcome-class mapping. The point
instantiates concrete checks, Cleanup bounds teardown, Γ maps            is methodological: the Petri model is not handwritten from scratch
concrete results to observation classes in Ω, and 𝜌𝑑 abstracts a         for every call sequence, but assembled from resource-transition
concrete runtime state to a Petri-net marking.                           idioms that recur across concurrent Rust libraries.
    We do not require a full bisimulation between implementation
and model. The methodological requirement is a local faithfulness        3.4    Scenario Semantics
contract at modeled event boundaries. For an event 𝑒 with 𝜂 (𝑒) = 𝑡,
let                                                                      An abstract scenario is a tuple
                      Step𝑑 (𝑡, 𝜎, 𝛽 (𝑒)) { (𝜎 ′, 𝑜)                                              S = (𝐸, ≺, #, 𝜂, 𝛽, Φ),
From Resource Flow to Executable Tests: Petri-Net-Guided LLM Test Generation for Concurrent Stateful Rust APIs        Conference’17, July 2017, Washington, DC, USA


where 𝐸 is a finite event set, ≺ ⊆ 𝐸 × 𝐸 is a strict partial order,                     Algorithm 1 Petri-net scenario synthesis
# ⊆ 𝐸 × 𝐸 is a symmetric conflict relation, 𝜂 : 𝐸 → 𝑇 maps events                       Require: net 𝑁𝐴 , family 𝑓 , length bound 𝐿
to Petri-net transitions, 𝛽 binds symbolic resources and payloads                       Ensure: abstract scenario S
to event parameters, Φ contains expected outcome predicates and                          1: 𝑀 ← 𝑀0 , 𝐸 ← [ ], ≺← ∅, # ← ∅
global invariants.                                                                       2: for 𝑖 = 1 to 𝐿 do
   A linearization of S is any bijective sequence over 𝐸 that respects                   3:     𝐶 en ← {𝑡 ∈ 𝑇 | enabled(𝑀, 𝑡)}
≺. We write                                                                              4:     𝐶 near ← {𝑡 ∈ 𝑇 | |Δ𝐹 (𝑀, 𝑡)| + |Δ𝐺 (𝑀, 𝑡)| = 1}
             Lin(S) = {𝜋 | 𝜋 is a linearization of (𝐸, ≺)}.                              5:     if 𝑓 = NearLegal and 𝑖 is the mutation point then
                                                                                         6:          choose 𝑡 ★ from 𝐶 near
The executable semantics of a scenario under net 𝑁𝐴 is                                   7:          append boundary event 𝑒𝑖 with 𝜂 (𝑒𝑖 ) = 𝑡 ★
                                                 𝜂 (𝜋 )                                  8:          break
      Exec(S, 𝑁𝐴 ) = {𝜋 ∈ Lin(S) | 𝑀0 −−−−→ 𝑀 for some 𝑀 },
                                                                                         9:     else
where 𝜂 (𝜋) lifts 𝜂 pointwise from events to transition sequences.                      10:          choose 𝑡 ★ from 𝐶 en maximizing Depth
A scenario is legal iff Exec(S, 𝑁𝐴 ) ≠ ∅. Equivalently, at least one                    11:          append legal event 𝑒𝑖 with 𝜂 (𝑒𝑖 ) = 𝑡 ★
                                           𝜂 (𝑒 1 ) ···𝜂 (𝑒𝑛 )
linearization 𝑒 1, . . . , 𝑒𝑛 satisfies 𝑀0 −−−−−−−−−−→ 𝑀𝑛 .                             12:          add causal edges induced by token production and con-
    To formalize boundary mutation, let Δ𝐹 (𝑀, 𝑡) = {𝑝 ∈ 𝑃 | 𝐼𝑡 (𝑝) ⊈                       sumption
𝑀 (𝑝)}, and assume the guard of 𝑡 is written as 𝑔𝑡 = 𝑞 1 ∧ 𝑞 2 ∧ · · · ∧                13:          add conflict edges induced by shared resources
𝑞𝑟 . Let Δ𝐺 (𝑀, 𝑡) = {𝑞 𝑗 | 𝑞 𝑗 (𝑀) = false, 1 ≤ 𝑗 ≤ 𝑟 }, so that                       14:          fire 𝑡 ★ and update 𝑀
missing tokens and violated atomic guards are counted separately. A                     15:     end if
disabled transition 𝑡 is near-legal at 𝑀 if |Δ𝐹 (𝑀, 𝑡)| + |Δ𝐺 (𝑀, 𝑡)| = 1.              16: end for

This definition captures the specific kind of semantic boundary case                    17: if 𝑓 = PartialOrder then

we want: a trace that is almost enabled, but violates exactly one                       18:     remove unnecessary order edges while preserving causality
precondition.                                                                           19: end if

    The conflict relation # records pairs of events that should be                      20: return S = (𝐸, ≺, #, 𝜂, 𝛽, Φ)

scheduled adversarially because they compete for a token class,
touch the same linear resource, or correspond to user-declared race
                                                                                        These begin as legal event sets, but independent steps are left un-
pairs. The partial order ≺ records only necessary causality, not a
                                                                                        ordered. The output is therefore a DAG of causality plus a conflict
fully committed thread schedule.
                                                                                        relation, not a single linear schedule.
    For concurrent scenarios, Φ is set-valued rather than schedule-
singleton. If incomparable events can race, the allowed outcome
                                                                                        4.2     Generation Algorithm
class for event 𝑒 may be
                                        Ø                                               The Algorithm 1 is intentionally model-centric. The choice of which
                             Φ𝑒 =               Φ𝑒𝜋 ,                                   event should happen next is driven by reachability and conflict
                                 𝜋 ∈Exec( S,𝑁𝐴 )                                        structure, not by code-generation convenience.
where Φ𝑒𝜋 is the modeled observation class of 𝑒 under linearization                        In practice, near-legal mutation is not inserted uniformly. After
𝜋. This lets the oracle accept multiple race-permitted outcomes                         a legal prefix reaches marking 𝑀, we score candidate boundary
while still rejecting classes that no legal linearization admits.                       events by
                                                                                            MutScore(𝑀, 𝑡) = 𝑤 1 1[|Δ𝐹 (𝑀, 𝑡)| + |Δ𝐺 (𝑀, 𝑡)| = 1]
4 Scenario Synthesis                                                                                             + 𝑤 2 Stale(𝑀, 𝑡) + 𝑤 3 ConflictCtx(𝑀, 𝑡),
4.1 Three Scenario Families                                                             where Stale rewards operations that reuse recently invalidated
SyncPetri synthesizes three classes of scenarios from the same Petri-                   resources and ConflictCtx rewards mutations placed near a high-
net model. The classes can be used independently or composed: in                        conflict frontier. This focuses budget on the kinds of boundary
Section 2.2, a partial-order legal core is followed by a near-legal                     mistakes that concurrent libraries commonly mishandle.
boundary probe.
  These are fully enabled traces selected to reach semantically                         5 LLM Concretization
uncommon markings rather than merely long traces. We assign a
                                                                                        5.1 Prompt Contract
heuristic score
                                                                                        The LLM receives a typed prompt assembled from the scenario
                Depth(𝜋) = 𝛼𝑈 (𝑀𝑘 ) + 𝛽𝐶 (𝜋) + 𝛾𝑋 (𝜋),                                  tuple and API adapter schema:
where 𝜋 is a legal trace ending at marking 𝑀𝑘 , 𝑈 (𝑀𝑘 ) is a marking-                           𝑃 (S, 𝐴𝑑 ) = (Hdr, Res, Ev, Ord, Conf, Obs, Out, Ban).
novelty term, 𝐶 (𝜋) measures structural coverage (for example,
                                                                                        The fields encode resource declarations, typed events, order edges,
distinct transition or place classes), and 𝑋 (𝜋) measures conflict
                                                                                        concurrency hints, expected observation classes, and banned be-
exposure induced by the trace.
                                                                                        haviors such as invented semantic events or weakened assertions.
   These consist of a legal prefix followed by one near-legal event.
                                                                                        A representative prompt fragment is shown in Listing 2.
They target boundary checks, stale-resource handling, and error
propagation without collapsing into meaningless invalid sequences.                      Listing 2: Constrained prompt fragment for concretization.
Conference’17, July 2017, Washington, DC, USA                                                                                       Kaiwen Zhang, Guanjun Liu


                                                                          Algorithm 2 Concretization with structural repair
scenario_id: mpsc_permit_close
target_api: tokio::sync::mpsc                                             Require: scenario S, adapter schema 𝐴𝑑 , LLM 𝐿, retry bound 𝑅
resources:
  permit_sender: Sp                                                       Ensure: faithful test artifact or failure
  boundary_sender: Sb
                                                                           1: for 𝑟 = 1 to 𝑅 do
  receiver: R0
events:                                                                    2:     build prompt 𝑃 (S, 𝐴𝑑 )
  - e1: reserve_owned Sp -> P0
  - e2: spawn T1 with P0                                                   3:     𝑌 ← 𝐿(𝑃)
  - e3: permit_send P0 m1                                                  4:     if 𝑌 .𝑐 fails to compile then
  - e4: close R0
  - e5: recv R0 -> m1                                                      5:         feed compiler diagnostics back to 𝐿
  - e6: try_send Sb boundary_msg                                           6:         continue
  - e7: recv_end R0
order:                                                                     7:     end if
  - e1 < e2 < e3
  - e1 < e4
                                                                           8:     if marker coverage is incomplete then
  - e3 < e5                                                                9:         feed structural diagnostics back to 𝐿
  - e4 < e5 < e6 < e7
concurrent:                                                               10:         continue
  - (e3, e4)                                                              11:     end if
expected:
  - class(out(e3)) in {SendOk}                                            12:     return 𝑌
  - class(out(e6)) in {ClosedLike}                                        13: end for
  - class(out(e7)) in {End}
output_contract:                                                          14: return Fail
  - emit one marker before each modeled event
  - preserve all order constraints
  - return Rust test code only
                                                                          For any ready event 𝑒, we define a conflict-first priority
   The LLM output is represented as 𝑌 = (𝑐, 𝜇, 𝑎) where 𝑐 is Rust                                        ∑︁
test code, 𝜇 maps scenario events to emitted runtime markers, and                    prio𝜌 (𝑒) = 𝛼                  1[(𝑒, 𝑒 ′ ) ∈ #]
𝑎 is a set of generated assertions.                                                                    𝑒 ′ ∈frontierS (𝜌 )\{𝑒 }
   We accept a generated artifact for execution only if                                              + 𝛽 Rare(𝑒) − 𝛾 Seen(𝜌, 𝑒),
       WellFormed(𝑌, S) ⇐⇒ Compiles(𝑐)                                    where Rare(𝑒) rewards uncommon transition classes and Seen pe-
                                       ∧ ∀𝑒 ∈ 𝐸, 𝜇 (𝑒) ↓                  nalizes already explored prefixes.
                                       ∧ NoInventedEvents(𝑌, 𝐸).            A partial-order scenario also induces a task skeleton
This is a static admission filter; the structural oracle later checks                            𝐾 S = (𝑉task, 𝐸 spawn, 𝐸 conf ),
whether the runtime trace actually respects the intended partial          where 𝑉task partitions events by task ownership, 𝐸 spawn records
order.                                                                    spawn-parent relations, and
   For evaluation, we also use a partial structural-fidelity score. Let
ℎ★ be a maximum-cardinality order-preserving partial matching                            𝐸 conf = {(𝑒𝑖 , 𝑒 𝑗 ) | 𝑒𝑖 ∥ 𝑒 𝑗 ∧ (𝑒𝑖 , 𝑒 𝑗 ) ∈ #}
from scenario events to emitted markers. We define                        collects incomparable conflict pairs. A concrete harness variant
                                    |dom(ℎ★)|                             chooses task creation order, barrier placement, and explicit yield
                       Fid(S, 𝜏) =             .
                                        |𝐸|                               points around selected pairs in 𝐸 conf .
This allows tool to measure how much of the intended structure               We do not need to modify Loom internals to use this signal.
survives concretization even when the full structural oracle fails.       Instead, we generate a small set of schedule-shaping harness variants
The crucial rule is that the LLM may choose syntax, helper names,         that prioritize different high-conflict frontier choices, then run
and local scaffolding, but it may not invent new semantic events,         each variant under Loom when a Loom-compatible harness exists.
relax order constraints, or redefine the expected outcome classes.        For APIs where direct Loom integration is unavailable, the same
                                                                          schedule-shaping variants can be executed under a deterministic
5.2     Concretization and Repair Loop                                    scheduler wrapper. The improvement is therefore above Loom
We require a generated test to compile and to expose the marker           rather than inside Loom: the Petri net chooses which concurrency
structure needed by the runtime oracle. Algorithm 2 gives the             skeletons deserve schedule budget.
loop. This loop is deliberately strict because successful compilation        Let YieldPts(ℎ) denote the conflict pairs that a harness variant
alone is insufficient to prove that the scenario has been correctly       ℎ explicitly exposes with barriers or yields, and let 𝐶 𝑗 −1 be the set
concretized.                                                              already covered by earlier variants. We can then rank candidate
                                                                          variants by uncovered conflict gain:
6     Petri-Guided Schedule Exploration
                                                                                                                ∑︁
                                                                                      ℎ 𝑗 = arg max                        𝑤 (𝑒, 𝑒 ′ ).
                                                                                                ℎ∈ H ( S)
The scenario tuple already tells us which events are causally con-                                          (𝑒,𝑒 ′ ) ∈YieldPts(ℎ)\𝐶 𝑗 −1
strained and which pairs are in semantic conflict. We use that            This gives a concrete methodological improvement over naive
information to shape schedule exploration rather than treating all        schedule enumeration: Loom still explores schedules within each
harness variants as equally important.                                    harness, but the Petri layer decides which harnesses deserve sched-
   For a prefix 𝜌 ⊆ 𝐸, define the ready frontier as                       ule budget by maximizing semantically meaningful conflict cover-
             frontier S (𝜌) = {𝑒 ∈ 𝐸 \ 𝜌 | ∀𝑒 ′ ≺ 𝑒, 𝑒 ′ ∈ 𝜌}.            age first.
From Resource Flow to Executable Tests: Petri-Net-Guided LLM Test Generation for Concurrent Stateful Rust APIs               Conference’17, July 2017, Washington, DC, USA


Algorithm 3 Petri-guided schedule shaping                                                                  Table 3: Semantic oracle layers.
Require: partial-order scenario S, variant budget 𝐾
Ensure: harness variants 𝐻                                                               Layer            Checks                    Failure signal
 1: 𝐻 ← ∅                                                                                Structural       Marker coverage           LLM omitted an event or reordered
 2: for 𝑗 = 1 to 𝐾 do                                                                                     and order preser-         a required edge
 3:     𝜌 ← ∅, ℎ 𝑗 ← [ ]                                                                                  vation
 4:     while 𝜌 ≠ 𝐸 do                                                                   Outcome          Return/error class        A close-after-send boundary event
 5:        𝐹 ← frontier S (𝜌)                                                                             membership                unexpectedly succeeds
 6:        choose 𝑒 ★ ∈ 𝐹 maximizing prio𝜌 (𝑒)                                           Invariant        Scenario-level se-        Buffered count becomes inconsis-
                                                                                                          mantic properties         tent with sends and receives
 7:        append 𝑒 ★ to ℎ 𝑗
                                                                                         Liveness         Bounded comple-           Test hangs after a race that should
 8:        insert yield/barrier hooks around conflicting incompa-                                         tion and join be-         terminate
    rable pairs                                                                                           havior
 9:        𝜌 ← 𝜌 ∪ {𝑒 ★ }
10:     end while
11:     add ℎ 𝑗 to 𝐻
12: end for                                                                                 Let Osem = Oout ∧ Oinv ∧ Olive . We classify outcomes by
13: return 𝐻
                                                                                                           ConcretizationError                 if Ostr = 0,
                                                                                            Class(S, 𝜏) = SemanticFailure                      if Ostr = 1 ∧ Osem = 0,
7    Multi-Layer Semantic Oracle                                                                          Pass                                 otherwise.
The execution harness records a trace
                                                                                       This decision rule is operationally important: only the second case
                  𝜏 = (𝑚 1, 𝑜 1 ), (𝑚 2, 𝑜 2 ), . . . , (𝑚𝑘 , 𝑜𝑘 ) ,
                                                                                        becomes a bug candidate.
where each 𝑚𝑖 is an emitted marker and each 𝑜𝑖 is the corresponding                        Table 3 summarizes the role of each layer.
local observation or return class.                                                         This separation is important. It prevents the system from con-
   We define the oracle as a conjunction of four layers:                                fusing a bad generated test with a bad library behavior.
                  O (S, 𝜏) = Ostr ∧ Oout ∧ Oinv ∧ Olive .
                                                                                           Soundness intuition. Assume that (1) the adapter 𝐴𝑑 is locally
    Structural oracle.                                                                  faithful, (2) marker 𝜇 (𝑒) is emitted immediately before the concrete
                                 Ostr (S, 𝜏) = 1                                        step for 𝑒, and (3) helper code emits no spurious modeled markers.
                                                                                        If
iff there exists an injective matching ℎ : 𝐸 → {1, . . . , 𝑘 } such that:
    (1) the marker at position ℎ(𝑒) corresponds to event 𝑒;                                                               Ostr (S, 𝜏) = 1,
    (2) if 𝑒𝑖 ≺ 𝑒 𝑗 , then ℎ(𝑒𝑖 ) < ℎ(𝑒 𝑗 ).
                                                                                        then 𝜏 contains a matched subsequence with the same order as some
If Ostr = 0, the test is treated as a concretization failure rather than                𝜋 ∈ Exec(S, 𝑁𝐴 ). In other words, the runtime trace refines a mod-
an API bug.                                                                             eled linearization of the intended scenario up to unmodeled helper
   Outcome oracle. Each event 𝑒 may carry an allowed set of obser-                      steps. Under this assumption, a semantic-oracle failure points to
vation classes Φ𝑒 . Then                                                                API behavior under the concretized scenario rather than to missing
                                                                                        events or reordered scaffolding.
                                 Oout (S, 𝜏) = 1
iff for every matched event 𝑒, the observed class at ℎ(𝑒) belongs to                        Failure report. When a run fails, the system reports
Φ𝑒 . This allows the oracle to express sets of admissible concurrent
                                                                                                                 Report = (S, Class, 𝐿 𝑓 , 𝜏 ★, ℎ 𝑗 ),
outcomes rather than brittle single-value expectations.
  Invariant oracle. Let Ψ be the set of global scenario invariants.                     where 𝐿 𝑓 ⊆ {out, inv, live} is the set of failed oracle layers, 𝜏 ★ is
Then                                                                                    the matched event subsequence, and ℎ 𝑗 is the harness variant that
                          Oinv (S, 𝜏) = 1                                               exposed the behavior. This report structure matters in practice be-
                                                                                        cause it supports triage, de-duplication, and prompt repair without
iff every invariant in Ψ holds over the observed execution summary.
                                                                                        collapsing all failures into a single undifferentiated bug bucket.
Typical examples include resource conservation, absence of ghost
messages, bounded buffer counts, or monotonic closure state.
                                                                                        8     Evaluation and Results
    Liveness oracle.                                                                    This section reports a preliminary evaluation of the reviewed MPSC
                                 Olive (S, 𝜏) = 1                                       running example. The goal is not a large benchmark, but a paper-
iff the run terminates within a bound and no task expected to                           level check that the current prototype can carry one manually
complete remains permanently blocked. This matters because many                         modeled CPN and one reviewed ScenarioBlueprint all the way
concurrency faults manifest as hangs rather than wrong return                           to executable Tokio code, and that the resulting runtime trace agrees
values.                                                                                 with the model-derived oracle.
Conference’17, July 2017, Washington, DC, USA                                                                          Kaiwen Zhang, Guanjun Liu


          Table 4: Current MPSC prototype evidence.                     words, repair fixed the contract mismatch rather than rewriting the
                                                                        test into a different one.
    Property                         Result                                This is the relevant form of repair for the current prototype:
                                                                        the generated code may change its surface syntax and evidence
    Compilation                      passed
    Legal schedules                  2                                  plumbing, but it should not silently change the modeled scenario
    Runtime executions               3                                  or weaken the oracle.
    Records per execution            14
    Evaluator findings               none                               8.5    RQ4: Is the artifact boundary strict enough
                                                                               to isolate the generic pipeline from the
                                                                               subject-specific model?
8.1     Subjects and Setup                                              The generic LLM and evaluator layers consume the portable artifact,
The evaluated subject is a bounded Tokio MPSC channel with capac-       not handwritten MPSC logic. The subject-specific semantics live in
ity one. The reviewed scenario contains seven events and exactly        the family crate: the reviewed CPN, the reviewed scenario, and the
two legal linearizations:                                               runtime observation contract. The generic pipeline then compiles
                                                                        the generated source, executes it, and checks the emitted JSONL
e3_before_e4: e1 e2 e3 e4 e5 e6 e7
e4_before_e3: e1 e2 e4 e3 e5 e6 e7                                      records against the artifact-derived oracle.
                                                                           The limitation is scope. This is still a preliminary evaluation
   The repaired generated source compiles, executes both legal          on one running example, not a large-scale mutation study or a
schedules inside one Tokio test, and emits 14 JSONL records per run.    schedule-budget benchmark. The result supports feasibility, not
We evaluate the same source three times with the generic artifact-      statistical superiority.
driven evaluator; all three runs pass and the evaluator reports no
findings.                                                               8.6    Threats to Validity
                                                                        The main threat is scale. The current evaluation covers one reviewed
8.2     RQ1: Can the artifact-constrained prompt                        MPSC subject and one repaired generated runner. It does not yet
        produce executable Tokio code?                                  include a mutant corpus, a pure prompt baseline, or a schedule-
The generated test compiles under the recorded toolchain and runs       exploration comparison. Even so, the available evidence is enough
to completion under the generic evaluator. This is the first require-   for an arXiv submission that claims a working prototype and a
ment for the pipeline: the prompt and generation contract are strong    validated artifact boundary, rather than a completed benchmark.
enough to produce a real Tokio test rather than a sketch or pseudo-
code fragment.                                                          9     Related Work
   The same source also carries the scenario labels, the expected          Model-based testing with Petri nets. Petri nets have long been
observations, and the runtime evidence points that the evaluator        used for formal modeling, reachability reasoning, and test deriva-
consumes. For this MPSC example, those ingredients were sufficient      tion in stateful systems [4, 5]. That line of work establishes why
to obtain three successful executions without any MPSC-specific         token-based models are useful: they express multiplicity, causality,
checker in the evaluation crate.                                        and conflict more naturally than flat state machines. Our setting
                                                                        adds a missing concretization problem. The output must not stop
8.3     RQ2: Does the generated runner preserve                         at an abstract trace; it must become a compilable Rust test with
        schedule-sensitive structure?                                   tasks, ownership moves, time bounds, and executable assertions.
The scenario distinguishes two legal linearizations by the relative     SyncPetri therefore uses the Petri net as a semantic intermediate
order of e3 and e4, and the runner preserves that distinction in        representation rather than as the whole testing engine.
the runtime trace. Each execution emits the same 14 records, split         Stateful API testing and deep-state exploration. REST-ler showed
evenly across the two schedules, and the evaluator confirms that        that dependency-aware generation is necessary for stateful APIs
the observed record order matches the artifact oracle.                  because naive request composition rarely reaches meaningful deep
   This matters because the example is not merely “some test that       states [1]. StateAFL and later stateful greybox work likewise argue
passes.” It is a small schedule family whose legal orders remain        that failures often emerge only after the system enters semantically
visible in the final trace. That is the concrete structural property    distinct states [2, 6]. We share that motivation, but the target and ab-
the prototype is meant to preserve.                                     straction differ. Those systems focus on network-facing or protocol-
                                                                        facing interfaces, whereas SyncPetri targets in-process Rust library
8.4     RQ3: Can feedback repair recover from a                         APIs whose hard behaviors depend on resource ownership, handle
        concrete mismatch without changing the                          invalidation, reserved capabilities, and schedule-sensitive partial
        scenario?                                                       orders. Our near-legal scenarios also aim at semantic boundaries
                                                                        defined by the model, rather than at arbitrary invalid inputs.
The repaired source used here is the result of a bounded runtime-
feedback repair. The repair adjusted the emitted operation labels         LLM-based test generation. TitanFuzz and Fuzz4All showed that
to the exact Scenario strings, while preserving the same schedules,     LLMs can generate diverse tests and programs in domains where
the same observable behavior, and the same record count. In other       manual generators are costly [3, 13]. CoverUp further showed that
From Resource Flow to Executable Tests: Petri-Net-Guided LLM Test Generation for Concurrent Stateful Rust APIs               Conference’17, July 2017, Washington, DC, USA


external feedback and structure remain important even for strong                          [8] Tokio Contributors. 2026. loom. https://docs.rs/loom/latest/loom/. Accessed
models [7]. SyncPetri adopts that lesson but changes the guidance                             2026-07-16.
                                                                                          [9] Tokio Contributors. 2026. tokio::sync::broadcast. https://docs.rs/tokio/latest/
signal. Instead of relying on open-ended prompting or coverage                                tokio/sync/broadcast/. Accessed 2026-07-16.
alone, we provide a typed event graph with resource bindings, order                      [10] Tokio Contributors. 2026. tokio::sync::mpsc. https://docs.rs/tokio/latest/tokio/
                                                                                              sync/mpsc/. Accessed 2026-07-16.
constraints, admissible outcome classes, and banned semantic edits,                      [11] Tokio Contributors. 2026. tokio::sync::Semaphore. https://docs.rs/tokio/latest/
then judge the result with a structural oracle. The contribution is                           tokio/sync/struct.Semaphore.html. Accessed 2026-07-16.
therefore not simply to use an LLM for testing, but to restrict the                      [12] Tokio Contributors. 2026. tokio::sync::watch. https://docs.rs/tokio/latest/tokio/
                                                                                              sync/watch/. Accessed 2026-07-16.
LLM to code realization while keeping semantic intent outside the                        [13] Chunqiu Steven Xia, Matteo Paltenghi, Jia Le Tian, Michael Pradel, and Ling-
model.                                                                                        ming Zhang. 2023. Fuzz4All: Universal Fuzzing with Large Language Models.
                                                                                              arXiv:2308.04748 [cs.SE] https://arxiv.org/abs/2308.04748
   Systematic concurrency exploration. Loom provides controlled
schedule exploration for Rust concurrent code [8]. Our work is
complementary rather than competitive. Loom explores micro-
interleavings inside a harness; SyncPetri tries to make that har-
ness semantically meaningful in the first place by extracting race
windows and conflict pairs from the resource model. The schedule-
shaping component therefore operates above the scheduler: it pri-
oritizes which concurrency skeletons deserve exploration budget,
but it does not modify the scheduler’s internal search algorithm.

    Positioning. Across these lines of work, the missing combination
is a model-driven route from resource-aware concurrency semantics
to executable Rust tests without delegating the semantic oracle
to the LLM. SyncPetri occupies that space by combining Petri-
net scenario synthesis, constrained concretization, schedule-aware
harness construction, and layered runtime judgment in one testing
workflow.

10     Conclusion
This paper presented SyncPetri, a Petri-net-constrained architec-
ture for LLM-based test generation over concurrent stateful Rust
APIs. The main thesis is that model structure should control se-
mantics, boundary mutation, and concurrency exposure, while the
LLM should only control executable realization. To support that the-
sis, we formalized the target domain, defined a scenario language,
specified concretization and repair loops, proposed Petri-guided
schedule shaping, and introduced a multi-layer semantic oracle.
Together, these pieces form a main-track-sized methodology: not
merely a sketch that Petri nets and LLMs can be combined, but a con-
crete design for how they should be combined in a test-generation
system.

References
 [1] Vaggelis Atlidakis, Patrice Godefroid, and Marina Polishchuk. 2018. REST-ler:
     Automatic Intelligent REST API Fuzzing. arXiv:1806.09739 [cs.SE] https://arxiv.
     org/abs/1806.09739
 [2] Jinsheng Ba, Marcel Böhme, Zahra Mirzamomen, and Abhik Roychoudhury. 2022.
     Stateful Greybox Fuzzing. arXiv:2204.02545 [cs.CR] https://arxiv.org/abs/2204.
     02545
 [3] Yinlin Deng, Chunqiu Steven Xia, Haoran Peng, Chenyuan Yang, and Lingming
     Zhang. 2022. Large Language Models are Zero-Shot Fuzzers: Fuzzing Deep-
     Learning Libraries via Large Language Models. arXiv:2212.14834 [cs.SE] https:
     //arxiv.org/abs/2212.14834
 [4] Jai Manral. 2015.       Automated Test Case Generation using Petri Nets.
     arXiv:1509.08401 [cs.SE] https://arxiv.org/abs/1509.08401
 [5] Tadao Murata. 1989. Petri Nets: Properties, Analysis and Applications. Proc. IEEE
     77, 4 (1989), 541–580. doi:10.1109/5.24143
 [6] Roberto Natella. 2021. StateAFL: Greybox Fuzzing for Stateful Network Servers.
     arXiv:2110.06253 [cs.CR] https://arxiv.org/abs/2110.06253
 [7] Juan Altmayer Pizzorno and Emery D. Berger. 2024. CoverUp: Coverage-Guided
     LLM-Based Test Generation. arXiv:2403.16218 [cs.SE] https://arxiv.org/abs/2403.
     16218
