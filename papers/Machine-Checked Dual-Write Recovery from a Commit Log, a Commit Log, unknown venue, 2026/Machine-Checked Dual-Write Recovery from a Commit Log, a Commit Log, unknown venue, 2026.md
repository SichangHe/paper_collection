                                                   Machine-Checked Dual-Write Recovery from
                                                                a Commit Log
                                                                                            Andreas Andreakis
                                         Abstract                                                            1   Introduction
                                         Applications often need to make related facts durable in two        Consider an order service that commits shipped to its data-
                                         independent systems without a transaction spanning both.            base. A relay sends a confirmation email for each committed
                                         If the process crashes after the second system accepts an           order and records a checkpoint after every send. The process
                                         operation but before a source-side checkpoint is written, re-       then crashes and restarts. Its checkpoint is now one order be-
                                         covery cannot tell from source state alone whether to retry.        hind the commit log, so recovery sends the last confirmation
                                         Retrying may duplicate the effect, while skipping may leave         again and the customer receives two copies. An inspection
arXiv:2608.00501v5 [cs.DB] 11 Sep 2026




                                         committed work incomplete. Transactional outboxes and               finds no error in the database as the rows are correct, the
                                         change data capture move this dual write out of an applica-         checkpoint is valid, and the store-level audit passes. This
                                         tion process, but relay delivery and checkpointing remain           paper explains how a process that checkpoints after every
                                         separate durable operations.                                        send can still fail to provide exactly-once delivery.
                                            The engineering problem is familiar, and systems address            The failure occurs because delivery and checkpointing
                                         it with retries, checkpoints, idempotency keys, and fencing,        are separate durable operations. The crash may occur after
                                         and call the result exactly-once delivery. Whether that guar-       the mail provider accepts the request but before the process
                                         antee holds depends on which event it counts, what evidence         records the checkpoint. At restart there are two possible
                                         recovery requires, and how long that evidence must survive.         states. In one state the provider accepted the request, and
                                         Formal verification has covered adjacent problems, includ-          in the other it did not. The service can read the same data-
                                         ing transaction isolation, crash safety within one store, and       base, write-ahead log, outbox, acknowledgement log, restart
                                         protocols with a shared commit. The closest formal stud-            counter, and checkpoint in both states. Sending the message
                                         ies use model checking to verify particular outbox and log-         again creates a duplicate in the first state. Skipping it leaves
                                         delivery designs, and their results hold only for the designs       committed work incomplete in the second. The local check-
                                         and instances they check. Answering the three questions             point is not incorrect. It simply does not record whether the
                                         in general rather than for one design requires statements           receiving side accepted the effect. Only a durable record at
                                         about arbitrary recovery policies, which finite enumeration         the receiving side can distinguish the two states.
                                         cannot reach. We prove them in Isabelle/HOL, and to our
                                         knowledge they have not been machine-checked before.                   Dual writes. The incident is an example of a dual write.
                                            The main result is an impossibility theorem for source-          Related facts become durable under independent authorities
                                         only recovery. We construct two reachable post-crash states         without one commit spanning both. The source may be a
                                         with the same durable source-side state and different sink          database, while the second authority may be a mail provider,
                                         acceptance records. Any recovery policy based only on the           broker, cache, search index, or another service. The model
                                         source side must duplicate an effect in one state or leave it       distinguishes a durable source commit from a durable sink
                                         undelivered in the other. The same result holds for a deter-        acceptance. Section 2 and the theorem statements give the
                                         ministic deliver-then-checkpoint protocol whose only nonde-         remaining requirements.
                                         terminism is crash timing. When the sink exposes an author-            The usual remedy is to derive the second write from the
                                         itative, complete, and current acceptance record, recovery          source’s committed log through change data capture (CDC)
                                         can compute exactly which committed operations remain               or a transactional outbox [1, 2, 3]. This approach removes
                                         undelivered, provided source coordinates distinguish opera-         the dual write from application code. Section 9 proves what
                                         tions. We extend the model to requests that remain in flight        it provides at the store tier. A derived copy is crash-safe
                                         and to concurrent recoverers, and prove an arrival fence            exactly when it matches the committed log up to the log
                                         and a claim fence for these hazards. Finally, we show how           position it advertises. The relay must still deliver each de-
                                         bounded deduplication state and truncated source history            rived event and record its own progress. These are again two
                                         limit the lifetime of the guarantee. A recovery design must         durable operations without a shared commit. The log-based
                                         therefore identify the sink’s acceptance event, prevent stale       approach therefore moves the recovery problem to the relay.
                                         actors from changing the result after it is read, and retain        The replayable source log lets the relay retry failed deliveries
                                         the required evidence for the full recovery horizon.                and catch up after an outage. Recovery still depends on the
                                                                                                             acceptance evidence and controls provided by the sink.
                                         Keywords: dual writes, exactly-once delivery, crash recov-
                                         ery, change data capture, formal verification, Isabelle/HOL


                                                                                                         1
   Why formalize now. The engineering guidance for this                    Scope. This paper presents a theoretical study of dual-
problem is established. Prior work recommends deriving                  write recovery. All theorems are machine-checked in Is-
state from a log, retrying failed deliveries, using stable iden-        abelle/HOL. The models, theorem statements, assumptions,
tities, and fencing stale workers [1, 2, 3, 4]. Systems that            and proof ideas are included in the text, so the paper can
combine these mechanisms call the result exactly-once de-               be read without the formal artifact. The negative results
livery. Yet such claims often leave unclear what counts as              are constructions over specific machines and policy classes.
delivery, how recovery can determine whether it occurred,               They show that the stated failure is reachable and that every
and how long the required evidence remains valid. This can              policy in the class fails on the construction, without claiming
make an information limit look like a checkpoint bug. It can            that every deployed system fails. The positive results hold
also make a conditional guarantee look impossible when the              under conditions stated with each theorem. We do not ver-
required sink-side evidence and controls are available.                 ify a broker, connector, mail provider, or deployed recovery
   Formal verification has addressed nearby problems such               implementation.
as transaction isolation [5], single-store crash recovery [6, 7],          The model covers one source authority, one accepting end-
and distributed protocols with a shared commit [8]. Those               point, and one delivery direction, alongside in-flight delivery
models do not decide whether an independent sink already                and concurrent recovery on separate machines. Section 10
accepted an effect. The closest formal studies use bounded              lists further boundaries. The theory aims to identify the evi-
model checking for outbox and log-delivery designs [9, 10].             dence and acceptance controls required by a recovery claim,
To our knowledge, this is the first machine-checked proof of            not to certify a product.
this recovery limit for all policies that use only the modeled
                                                                           Organization and reading paths. The paper provides
source-side state.
                                                                        two complementary reading tracks. Readers focused on for-
   Results. The results are organized around three parts of             mal foundations can follow the Theory Track (Sections 2-11),
the recovery problem.                                                   which develops the transition systems, impossibility results,
   Source-side impossibility result. Sections 3 and 4 construct         fence constructions, and retention limits. Readers focused
reachable post-crash states that agree on the durable infor-            on practical systems can take the Practitioner Track, jumping
mation available to recovery and differ in the sink’s accepted          directly to Section 12. That self-contained guide requires no
record. Every policy that reads only the source side must               proof mechanics and translates the results into operational
choose the same recovery batch in both states. That batch               guidance for direct dual writes and CDC outbox relays, com-
duplicates a delivery in one state or leaves one undelivered in         plete with sink archetypes, hazard analyses, and recovery
the other. Section 4 strengthens the result to one determinis-          tests. Section 13 concludes.
tic deliver-then-checkpoint protocol. The protocol maintains
its cursor correctly, and crash timing alone creates the two            2   The Model
indistinguishable local states.                                         All results use a common state model. This section defines the
   Stale recovery information. Section 5 proves that recov-             shared state, the first transition system, and the terminology
ery can compute the missing batch from an authoritative,                used throughout the paper. Later sections extend the state
complete, and current sink acceptance record under stated               with a checkpoint, an in-flight channel, concurrent recovery,
conditions. Sections 6 and 7 then identify two ways in which            retention, and the store tier.
that read can become stale. A request from the crashed pro-
cess may still be in flight, or another recoverer may act on               Histories, frontiers, materialization. A source event 𝑒
the same crash. We prove an arrival fence for the first hazard          on a key 𝑘 inserts or updates that key to a value, or deletes it.
and a claim fence for the second. Both mechanisms act at                A committed source history 𝐻 is a finite sequence of (coordi-
the sink’s acceptance boundary. The arrival fence also has a            nate, event) pairs whose coordinates are non-decreasing. A
proved cost because it may reject an old request that would             frontier 𝑓 is a coordinate of that history, never a wall-clock
otherwise have completed later work.                                    time, a broker offset, or a sink-local sequence number. Given
   Evidence lifetime. Section 8 proves the standard relation-           a base map 𝑏, the materialization Src(𝑏, 𝐻, 𝑓 ) gives each key
ship between at-least-once delivery and a permanently dedu-             the value of its latest event at a coordinate at most 𝑓 (a delete
plicated sink view. It then shows what changes when dedupli-            yields absence), falling back to 𝑏 where the key has no such
cation state expires or the source history is truncated. Once           event. Formally, histories are arbitrary lists of this shape and
the sink forgets an accepted identity, a valid replay may be            frontiers arbitrary coordinates. The non-decreasing well-
processed as new. Once recovery loses the content of the                formedness just described, and membership in a machine’s
source history, it may no longer be able to distinguish work            reachable executions, are imposed by stated assumptions
that requires delivery from work that was never committed.              and by the machines’ own transition rules, not by the raw
The guarantee therefore lasts only as long as the evidence              data type. The core execution state
required by the recovery procedure.                                                  𝜎 = (𝑏, 𝐻, 𝐷, 𝑄, pend, 𝐾, fin, st, Ack)


                                                                    2
carries the base, the committed history, an independently              Section 6 splits that collapsed send/receive step, because a
delivered downstream history 𝐷, an enqueued history 𝑄                  whole class of hazards arises in the gap between the two.
with the pending set pend of enqueued-but-undelivered
                                                                          Hazards and missing deliveries. Three predicates over 𝑡
events, the key scope 𝐾, the interval end fin, a run sta-
                                                                       classify how a ledger can be wrong, and one checks for miss-
tus st ∈ {Running, Crashed 𝑐, Recovered}, and a source-
                                                                       ing deliveries. The obligations at a frontier are the scoped,
side acknowledgement history Ack. Labelled steps drive
                                                                       frontier-bounded committed events
the state: commit to 𝐻 , enqueue, deliver to 𝐷, acknowl-
edge into Ack, crash (which freezes the run at a frontier),              replay(𝐻, 𝐾, 𝑓 ) = [ (𝑐, 𝑒) ← 𝐻 | 𝑐 ≤ 𝑓 ∧ key(𝑒) ∈ 𝐾 ],
and recover. A completed recovery cycle returns the run
                                                                       and the hazard vocabulary is
to Running with a new generation. A two-event instance
grounds the notation and returns throughout the paper:                   premature(𝑡) ←→ ∃𝑥 ∈ 𝐸. ¬ justified(𝐻, 𝑥),
with 𝐻 = [(𝑐 1, ins 𝑘 7), (𝑐 2, upd 𝑘 9)] and an empty base,              duplicate(𝑡) ←→ some payload repeats on 𝐸,
Src(𝑏, 𝐻, 𝑐 1 ) (𝑘) = 7, Src(𝑏, 𝐻, 𝑐 2 ) (𝑘) = 9, and the scoped             unsafe(𝑡) ←→ premature(𝑡) ∨ duplicate(𝑡),
obligations at 𝑐 2 are both events, in order.
                                                                              lost(𝑓 , 𝑡) ←→ ∃𝑝 ∈ replay(𝐻, 𝐾, 𝑓 ). 𝑝 ∉ pay(𝐸),
   Both stores are read through the one materialization op-
erator at the same source frontier: Src(𝑏, 𝐻, 𝑓 ) is what the                  alo(𝑓 , 𝑡) ←→ replay(𝐻, 𝐾, 𝑓 ) ⊆ pay(𝐸).
committed log says, Src(𝑏, 𝐷, 𝑓 ) is what the downstream               unsafe is a safety verdict over what was emitted: something
holds.                                                                 fired too early, or fired twice. It does not constrain what never
Definition 2.1 (Scoped mismatch). At frontier 𝑓 , the down-            fired. lost and alo are each other’s complements and form
stream mismatches the committed log on key 𝑘 when 𝑘 ∈                  the completeness axis. Read at a state, they say whether a
𝐾 and Src(𝑏, 𝐷, 𝑓 ) (𝑘) ≠ Src(𝑏, 𝐻, 𝑓 ) (𝑘). Write clean(𝜎, 𝑓 )        frontier still has an undelivered payload. They make no live-
when no scoped mismatch holds at 𝑓 .                                   ness claim. They classify the state where a result is judged,
                                                                       not what some later execution might still deliver. The theo-
   When a crash can freeze such a mismatch where an ob-                rems apply them at post-recovery states, where the recovery
server sees it is a question about the store tier, and it has an       being judged has finished its work. The verdicts are order-
exact answer, proved in Section 9. The subject of this paper           invariant. What was delivered matters, but its order does not.
sits above that tier, at a boundary the store never records.           Multiplicity matters to duplicate by definition, and to the
                                                                       completeness pair only under the ascending-coordinate con-
   The acceptance boundary. The effect machine extends
                                                                       dition P4 (Section 5). “Exactly-once at 𝑓 ” always means the
𝜎 with one field and one register. A state is 𝑡 = ⟨𝜎, 𝐸, 𝛾⟩: the
                                                                       conjunction (no hazard, and at-least-once at 𝑓 ), and the bare
core, an emissions ledger 𝐸, and a generation 𝛾. The ledger
                                                                       phrase is never used as a formal name in this paper: every
records received effects such as emails sent, messages pub-
                                                                       use is frontier-relative and counted as its theorem states.
lished, and webhook calls fired. It is append-only by con-
                                                                          The core’s acknowledgement history Ack records source-
struction: a received effect cannot be unreceived, so no step
                                                                       side acknowledgements, and it supports no delivery con-
of any machine in this paper removes a ledger entry. No
                                                                       clusion: equal acknowledgement histories can coexist with
store field can read the ledger. It models what happened, not
                                                                       different emission ledgers. An acknowledgement is what
what the crashed side knows. The generation 𝛾 is the restart
                                                                       the caller heard, not what the other side did. The opening
counter of Section 1. It identifies successive process runs,
                                                                       incident turned on this distinction, and the model makes it
starting at zero. Each completed resume enters the successor
                                                                       structural.
generation. Related counters in deployed systems are called
epochs or terms.                                                          What each side must provide. The model abstracts over
   An emission is a triple 𝑥 = ⟨𝑛, 𝑔, (𝑐, 𝑒)⟩: the stamp 𝑛 (the        both ends. On the source side, the analysis assumes only a
length of the committed history when it fired), the generation         durable, ordered, append-only committed history: each fact
𝑔 current when it fired, and the payload pay(𝑥) = (𝑐, 𝑒).              either is in 𝐻 , with a stable coordinate, or is not. How a fact
An emission is justified when the durable committed prefix             became durable lies outside the model: no relational store,
covered it at fire time, a check the stamp makes readable              multi-object transaction, or isolation discipline is assumed
from the state:                                                        anywhere. A write-ahead log, an event store, a replicated
   justified(𝐻, 𝑥) ←→ stamp(𝑥) ≤ |𝐻 |                                  queue, or a store limited to single-document writes each
                           ∧ pay(𝑥) ∈ take(stamp(𝑥), 𝐻 ).              yields an 𝐻 . Strictly ascending coordinates are required twice
                                                                       (condition P4, Section 5). They keep the sink-delta re-drive
For a ledger 𝐿, pay(𝐿) is the ordered pointwise projection             batch duplicate-free, and they lift the counting results from
[ pay(𝑥) | 𝑥 ← 𝐿 ]. On this first machine, delivery is in-             set level, by payload, to per instance. A source that can lose
stantaneous: an ordinary downstream delivery advances 𝐷                committed content is not left unmodeled: this section’s ma-
and appends the received effect to 𝐸 in a single transition.           chines never shrink 𝐻 , and truncation gets its own regime


                                                                   3
in Section 8. And a fact with no single committing write has         Table 1. What the model’s objects stand for. The mapping
no place in 𝐻 until one write is designated as its durability        is one-way (theorems name only the left column), and the
event. A fact spread across independent writes with no such          outbox rows are role-split on purpose.
point reproduces this paper’s problem one level down, inside
the source.                                                          Model object                      What it stands for
   On the sink side, the judged event is durable acceptance,         emission 𝑥 on the ledger 𝐸        the second write: an email, a webhook
the moment the receiving authority durably admits the op-                                              call, a cache fill, an index update
eration: a broker’s acknowledged append, a mail provider             accepted record 𝐴 (§6)            the sink’s durable record of what it has
accepting a send request, a store committing a put. Noth-                                              accepted
ing in this paper reaches past acceptance, not into internal         wire 𝑊 (§6)                       retries, socket buffers, requests still in
processing, onward delivery, or what a user interface even-                                            flight
tually shows. Sinks differ in what they let recovery read,           store state inside 𝜎              source/downstream histories, queue and
                                                                                                       pending state, run status, source
not in their kind. A sink exposing its own durable, complete
                                                                                                       acknowledgements
per-operation accepted record supplies the raw material for
                                                                     cursor (§4)                       a durable checkpoint of delivery
the positive results ahead. Their conditions are stated where                                          progress
they are proved, starting in Section 5. A sink readable only         generation 𝛾 (§2), fence 𝜑 (§6)   producer generation and the sink’s
as current contents gets strictly less, and what that read can                                         acceptance threshold
and cannot separate is itself proved (Sections 3 and 4). The         committed log 𝐻                   the source’s log, or an outbox table read
observation bounds in Sections 3-4 apply when recovery can                                             as the relay’s source
read only the modeled source-side state. Source acknowl-             accepted record 𝐴                 sink-owned acceptance state colocated
edgements do not distinguish the constructed cases. The obli-                                          with an outbox only when updated
                                                                                                       atomically with acceptance (§9)
gation runs one way, from the source’s record to the sink’s
                                                                     journal 𝐽 , floor fl (§7, §8)     the upstream log as justification
acceptance. Obligations running both ways are reached here
                                                                                                       authority, retention and compaction
only one direction at a time, and if even the source keeps no
such record, the question cannot be posed at all.
   Re-drives, policies, observations. A re-drive policy 𝑃            accepted record only if it also holds sink-owned acceptance
maps a state to a batch of payloads. The re-drive relation           state updated atomically with acceptance. Merely consulting
𝑡 ⇝𝑃 ⟨ 𝑓 ⟩ 𝑡 ′ is one atomic recovery step doing two things:         a source outbox or a relay cursor does not turn either into
it heals the store (the delivered history is reconciled to the       the sink’s record. Which theorems govern a physical table
committed image at 𝑓 , so clean(𝑡 ′, 𝑓 ) holds after every re-       depends on the role its fields actually play. The substitution is
drive, whatever the policy), and it appends 𝑃 (𝑡)’s emissions        one-way, as theorems are stated over abstract model objects
to the ledger, stamped with the current history length and           rather than concrete technologies like webhooks or caches.
generation. That the step is one atom is a deliberate model          The target-agnostic objects subsume them. We avoid “consis-
boundary. Section 10 discusses this atomicity assumption,            tent” because it conflates several properties. When this paper
and Section 5 shows that the central bound does not lean             means the stores agree at a frontier it says mismatch-free,
on it. An observation is any function obs of the state, of any       and where it means delivery went right it names the hazard
result type. A policy 𝑃 factors through obs when 𝑃 = 𝑔 ◦ obs         and the frontier.
for some 𝑔. Factoring is the paper’s only notion of what re-            Scope of the results. Negative results concern the policy
covery reads: a policy that factors through obs can use obs’s        classes and schedule families named in their statements. Pos-
output and nothing else. We consider three observations.             itive results hold under their stated conditions. The store-tier
The complete modeled store tier includes both source and             equivalence in Section 9 ranges over all implementations
downstream histories, with obs(𝑡) = core(𝑡). The second              satisfying its assumptions.
observation adds the generation, obs(𝑡) = (core(𝑡), gen(𝑡)).
The third also includes the sink’s acceptance record. Sec-           3     The Store-Side Observation Bound
tion 3 rules out policies based on the first two observations.
Section 4 then studies a fixed protocol using the durable-           After a crash, recovery must decide what to re-send. The
local view, which excludes downstream content as well as             first two theorems show that no policy computed only from
the acceptance record. Section 5 gives a correct sink-reading        the durable store and its control plane is correct on all reach-
policy under its stated conditions.                                  able states. The state available to recovery does not reveal
                                                                     whether the sink accepted the operation.
  Mapping the model to systems. Table 1 fixes the substi-
tution between practitioner vocabulary and model objects.               The designed pair. We construct two reachable post-
Two rows distinguish roles. An outbox table is the com-              crash states with the same store state and generation but
mitted log when a relay reads it as its source, and it is an         different acceptance records. The policy being tested chooses


                                                                 4
what to resend from these states. It need not have produced                                   Designed pair: reachable, hazard-free, genuinely emitting
the histories that led to them. Section 4 shows how crash                                      core(𝑡 1 ) = core(𝑡 2 ), gen(𝑡 1 ) = gen(𝑡 2 ), 𝑝 2 = (𝑐 2 , 𝑒 2 )
timing creates this ambiguity in a fixed protocol.
   Two runs of the effect machine commit the same two
facts and crash with the second delivery enqueued but un-                                            state 𝑡 1                                     state 𝑡 2
                                                                                              pay(𝐸 1 ) = [𝑝 1 , 𝑝 2 ]                        pay(𝐸 2 ) = [𝑝 1 ]
sent. Their first recoveries then diverge in one respect: the                                 𝑝 2 already emitted                          𝑝 2 still missing at 𝑐 2
machine’s recovery rule takes a reconcile index 𝑚 marking
where re-delivery starts, and the two runs use different val-
ues of it. With 𝑚 = 1, reconcile emits the missing payload,                                                 for every obs with obs (𝑡 1 ) = obs (𝑡 2 ),
and the emissions ledger records it. With 𝑚 = 2, reconcile                                                every 𝑃 = 𝑔 ◦ obs has 𝑃 (𝑡 1 ) = 𝑃 (𝑡 2 ) = 𝐵
rebuilds the store and emits nothing, an advanced-cursor
pathology one notch away from the incident’s stale-cursor                                                    yes                                no
duplicate. Both runs then resume and stand crashed again at                                                                 𝑝 2 ∈ 𝐵?

the same frontier 𝑐 2 with the store fully caught up. At that
point their formal cores are byte-equal: base, committed and
delivered histories, queue and pending state, scope, interval,                                      state 𝑡 1′                                     state 𝑡 2′
status, and source acknowledgements all agree, and so do                                       𝑝 2 appears twice                             𝑝 2 remains absent
                                                                                                 duplicate(𝑡 1′ )                              ⇒ lost(𝑐 2 , 𝑡 2′ )
their generations. The earlier 𝑚 choices were parameters of                                     ⇒ unsafe(𝑡 1′ )
actions already taken. No trace of them remains in either
state. Both states are hazard-free, and both have genuinely
emitted work (𝐸 ≠ [ ]). One member still has an undelivered                                       Either way, both repaired stores are clean at 𝑐 2 :
payload, and the other has already delivered it. They differ                                                 clean(𝑡 1′ , 𝑐 2 ) ∧ clean(𝑡 2′ , 𝑐 2 )

only in the emissions ledger:
pay(𝐸 (𝑡 1 )) = [(𝑐 1, 𝑒 1 ), (𝑐 2, 𝑒 2 )],      pay(𝐸 (𝑡 2 )) = [(𝑐 1, 𝑒 1 )].       Figure 1. The constructed pair for Theorems 1-2. The states
Theorem 1 (Observation Bound). On the effect machine                                  have equal core and generation but different emissions
there are reachable states 𝑡 1, 𝑡 2 and a frontier 𝑐 2 with                           ledgers. Any common observation yields the same batch,
                                                                                      which duplicates 𝑝 2 in 𝑡 1 or leaves it undelivered in 𝑡 2 . Both
 core(𝑡 1 ) = core(𝑡 2 ),        gen(𝑡 1 ) = gen(𝑡 2 ),    𝐸 (𝑡 1 ) ≠ 𝐸 (𝑡 2 ),       repaired stores are mismatch-free.
both hazard-free and with nonempty emission ledgers, such
that for every observation obs of any result type with obs(𝑡 1 ) =
                                                                                      Proof idea. Policies of both classes agree on the designed pair,
obs(𝑡 2 ), and every policy 𝑃 = 𝑔 ◦ obs, there are re-drives
                                                                                      because the pair is equal on core and generation. Theorem 1
                  𝑡 1 ⇝𝑃 ⟨𝑐 2 ⟩ 𝑡 1′   and 𝑡 2 ⇝𝑃 ⟨𝑐 2 ⟩ 𝑡 2′                         then applies. The mechanized proof checks the three-way
with clean(𝑡 1′ , 𝑐 2 ) and clean(𝑡 2′ , 𝑐 2 ), and                                   split directly (empty batch, batch containing a payload from
                                                                                      the committed prefix, non-empty batch entirely outside it),
                       unsafe(𝑡 1′ ) ∨ lost(𝑐 2, 𝑡 2′ ).                              and each case yields one of the stated outcomes.             □
   Any policy that observes the same state in both executions
must choose the same batch. If the batch contains the missing                            General and pair-specific outcomes. The disjunct in
payload, one execution receives a duplicate. If the batch                             Theorem 1 is unsafe ∨ lost, and since unsafe itself splits, the
omits it, the other execution remains incomplete. Adding                              general result has three outcomes: duplicate, lose, or fire
uncommitted work only creates a premature effect. Both                                prematurely. At the designed pair the checked statement
repaired stores are mismatch-free, so a store audit cannot                            sharpens to the practitioner’s two, because in the prema-
distinguish the failure. Figure 1 shows this argument.                                ture case the skip-side member still lacks its delivery: the
   The observation is otherwise unrestricted. It may be any                           verdict there is duplicate a delivery or leave it incomplete at
function of the state, with any result type, and only equality                        the judged frontier. Both forms are machine-checked. The
on the constructed pair is assumed. The result applies only                           three-outcome statements remain the general results, and
to information represented by the modeled observation.                                the two-outcome readings apply to the designed pairs used
                                                                                      in the examples. The loss outcome carries its standing disclo-
Theorem 2 (Control-Plane Bound). Every store-measured                                 sure: it is judged where the recovery under examination has
policy, computed as 𝑃 (𝑡) = 𝑔(core(𝑡)) for every 𝑡, and every                         finished, not a claim that no later recovery could still act.
store-and-generation-measured policy, computed as 𝑃 (𝑡) =
𝑔(core(𝑡), gen(𝑡)), is defeated on a reachable effect-machine                            Store and ledger health are independent. Store health
pair as in Theorem 1: both re-drives leave the store mismatch-                        and ledger health are orthogonal on this machine, in both
free at the pair’s frontier, and the outcome is a hazard on one                       directions: states with a broken store and a clean ledger
member or a loss on the other.                                                        are reachable, and so are states with a healed store and a


                                                                                  5
broken ledger. A second crash-and-re-drive cycle can raise              One deterministic protocol. The adversary only places the crash

the same payload’s count in the emissions ledger to three.                                enqueue 𝑒 1              persist           enqueue 𝑒 2           persist
An accurate delivered-count cursor persisted outside the                           commit 𝑒 1        deliver 𝑒 1          commit 𝑒 2         deliver 𝑒 2
store would separate the pair, by being a sink-side record
                                                                                                                                               the window
under another name, which is precisely the observation class
                                                                            protocol
Section 5 builds on. Distinguishing the pair alone does not
establish a recovery guarantee. The positive results below
apply to a specific policy under stated conditions.
   There is also a structural version of that boundary. A                 crash before the delivery                              crash inside the window

proved dichotomy partitions all policy functions: every re-                   durable-local view
                                                                                                                      =
                                                                                                                                       durable-local view
                                                                            WAL · outbox · acks · gen                                WAL · outbox · acks · gen
drive policy either is a function of the modeled store and                         cursor = 1                                               cursor = 1
generation (and fails on the pair in Theorem 2) or distin-                        record 𝐸      𝑝1                    ≠                 record 𝐸   𝑝1        𝑝2
guishes some two states that agree there and differ on the
ledger. The witnessing states of the second class need not be                                   every recovery measured on this view
                                                                                                  fires the same batch in both states
reachable. The split is extensional, a statement about infor-
mation rather than operations. Its value is exhaustiveness:                                          persist lands           crash
at this abstraction there is no third kind of policy.                   AFTER THE WINDOW                                                     cursor = 2

                                                                                                             the view separates: the cursor tells the truth
   Scope of the observation bound. Both slogans that cir-
culate about this problem fail against these results. “Exactly-
                                                                       Figure 2. The checkpoint window. Crashes immediately
once is impossible” is too coarse: Sections 5, 6, and 8 prove
                                                                       before the second delivery and between that delivery and
exactly-once results at their frontiers, under conditions a
                                                                       its persist produce equal durable-local views but different
system can satisfy. The true statement is the bound above
                                                                       emissions ledgers (Theorem 3). A crash after persist advances
(no policy blind to the sink’s record achieves it), together
                                                                       the cursor and separates the states.
with the conditions under which the positive results ahead
hold. “Just read the sink before re-driving” fails in the other
direction: once deliveries travel, Section 6’s straggler defeats       cursor: this machine’s recovery action carries only the fron-
every channel-blind batch selector on the constructed pair             tier, and nothing else is left for an adversary to choose at
under the unfenced re-drive relation. The positive result              recovery time.
changes acceptance instead of reading more.
                                                                          Fixed protocol and crash schedule. On this machine we
                                                                       pin one protocol: a function from states to next actions im-
4   The Checkpoint Window                                              plementing the faithful deliver-then-persist discipline over
The observation bound uses two earlier reconciliation                  the running two-event workload (commit 𝑒 1 , enqueue 𝑒 1 ,
choices. To show the same ambiguity in a fixed implemen-               deliver 𝑒 1 , and persist, then repeat these four actions for 𝑒 2
tation, we add a durable cursor and study a deterministic              and stop). The protocol itself never crashes. A run consumes
deliver-then-checkpoint protocol. A crash before delivery              a schedule over a two-letter alphabet: Go executes the proto-
and a crash after delivery but before checkpointing leave              col’s unique next action, Crash is the adversary’s only move,
recovery with the same durable-local view and different sink           the machine’s ordinary status-flip crash, at the point in the
records. The cursor is part of the common view.                        run where it lands. The endpoint of a run is a function of
                                                                       its schedule: crash placement is the only nondeterminism
  The checkpointed machine. Extend the effect machine                  anywhere in the construction, and no per-run parameter
with a single durable field: a progress cursor. Delivery and           exists that could distinguish runs.
checkpointing are separate transitions: an ordinary delivery              Two schedules matter: Go7 Crash and Go6 Crash (the
advances the downstream and the ledger as before, and a sep-           crash landing just after the second delivery, versus just be-
arate persist step advances the cursor by one, permitted only          fore it). Both runs end crashed with cursor 1: the first inside
when there is an actual delivery to acknowledge. A crash               the second deliver-to-persist window, the second right before
may land between them, and that window is the subject of               that window opens. At the first run’s endpoint, the emis-
this section. The machine’s one recovery rule is the effect            sions ledger holds both payloads. At the second it holds only
machine’s emitting reconcile with its index 𝑚 instantiated             the first, exactly the ledgers of Section 3’s pair, this time
by the machine’s own cursor: recovery re-fires the committed           produced by one fixed protocol (Figure 2).
suffix from wherever the durable cursor points. The free
parameter of Section 3 is thereby instantiated by a durable               What recovery can read. Call the durable-local view of
                                                                       a state everything a recovery procedure of the crashed pro-
                                                                       cess reads without querying the sink side: the base map, the


                                                                   6
committed source log, the enqueue (outbox) log, the acknowl-                     Relation to the equal-core pair. One distinction sepa-
edgement log, the scope, the interval end, the run status, the                rates this result from Theorem 1. That pair was equal on the
recovery generation, and the cursor. Write dview(𝜅) for that                  whole modeled core. This pair is equal on the durable-local
projection, and call a policy durable-local-measured when                     view and provably not equal-core: the delivered member’s
it factors through it. Three parts of the full state sit outside              downstream history and pending window record the deliv-
the view, each for a stated reason. The emissions ledger is                   ery, and the model exposes this difference. The two shapes
the sink-side record. Excluding it is the entire question. The                are complementary. The mechanization also proves that be-
downstream store’s delivered content is excluded because                      fore the first resume, no reachable pair of crashed states has
reading it is reading the sink: it is not local state, and the                equal cores and ledgers that differ in their delivered pay-
pair below is provably not equal on it, so that read genuinely                loads, so an equal-core, payload-divergent pair generated
separates the members. The dichotomy at this section’s end                    by one crash-timed protocol at generation zero cannot ex-
places such readers outside the defeated policy class. The                    ist. Theorem 1 is the wider information bound over every
pending delivery window is volatile by this machine’s own                     observation that agrees on its equal-core pair. Theorem 3 is
modeling assumption: it is the crashed process’s in-memory                    the protocol-specific bound over the reads a crashed imple-
buffer, which recovery in this model does not retain. For                     mentation actually has. The two theorems therefore cover
each exclusion, a companion result shows that adding the                      different recovery observations.
excluded component back changes the verdict. The crash                           On this pair, reading the downstream store’s content sep-
transition keeps every field. The model restricts which of                    arates the members because it contains the delivered copy,
those fields recovery may read after the crash.                               so a content reader distinguishes this pair. That read is not
                                                                              store-local information. It is a read of the sink, in its cheapest
Theorem 3 (Checkpoint Dilemma). On the checkpointed
                                                                              form. But it does not survive Section 3: on the equal-core pair
machine there are reachable states 𝜅 1, 𝜅 2 , the endpoints of the
                                                                              the downstream contents agree, so those reads do not distin-
two protocol schedules above, with
                                                                              guish the two states. Only the sink’s per-operation accepted
         dview(𝜅 1 ) = dview(𝜅 2 ),          𝐸 (𝜅 1 ) ≠ 𝐸 (𝜅 2 ),             record distinguishes both regimes: the acceptance history,
                                                                              not the current contents. Reading the sink is therefore two
both hazard-free and with nonempty emission ledgers, such
                                                                              different acts, reading its state and reading its acceptance
that every durable-local-measured policy 𝑃 is defeated at
                                                                              history, and the distinction returns as a theorem boundary
the finish frontier 𝑐 2 : there are re-drives 𝜅 1 ⇝𝑃 ⟨𝑐 2 ⟩ 𝜅 1′ and
                                                                              in Sections 8 and 9.
𝜅 2 ⇝𝑃 ⟨𝑐 2 ⟩ 𝜅 2′ , both leaving the store mismatch-free at 𝑐 2 , with
                                                                                 Policy classes and the cursor. As in Section 3, the split
                    unsafe(𝜅 1′ ) ∨ lost(𝑐 2, 𝜅 2′ ).
                                                                              is exhaustive: every policy on this machine either factors
At this pair the checked verdict again sharpens to two outcomes:              through the durable-local view (and the pair defeats it) or
duplicate a delivery, or leave one undelivered at the judged                  distinguishes some two states agreeing on that entire view,
frontier.                                                                     which means it reads the downstream content, the volatile
                                                                              window, or the ledger. The cursor itself is not the defect:
   The cursor is inside the view: recovery reads it, and it is
                                                                              if the crash lands after the final persist, the cursor reads 2,
equal on the two members. So are the committed log, the out-
                                                                              which by itself separates that state’s view from both pair
box, the acknowledgements, the status, and the generation.
                                                                              members. Outside the deliver-to-persist window the cursor
The pair does not arise from pathological bookkeeping. It
                                                                              is accurate. The dilemma is the window, not the cursor’s
is the deliver-then-persist window, crossed by a crash, seen
                                                                              bookkeeping. That is why no amount of care in maintaining
from the inside.
                                                                              the checkpoint, and no smarter encoding of it, closes a gap
    The deterministic protocol. The defeat quantifies over                    that sits between two durable writes.
all durable-local-measured policies, and the machine’s own
faithful recovery inhabits the class, so the theorem applies to               5    Reading the Sink
it. A checked trace also runs it concretely. Fired from the two               The pairs in the last two sections differ in the sink-side ac-
view-indistinguishable members, the same parameter-free                       cepted record. A policy that reads this record can compute
recovery transition is exactly right on the lagging member                    what is still missing. The sink delta at frontier 𝑓 is the com-
(store healed, no hazard, no delivery missing at 𝑐 2 ) and pro-               mitted obligations not yet on the record:
duces an effect-unsafe duplicate on the delivered member,
                                                                                  Δ⟨𝑓 ⟩(𝑡) = [ 𝑝 ← replay(𝐻, 𝐾, 𝑓 ) | 𝑝 ∉ pay(𝐸 (𝑡)) ].
every entry of which is individually justified. That is the fa-
miliar at-least-once window of checkpointed delivery, stated                  Here 𝐸 (𝑡) is the model’s authoritative, complete record at
and checked as a theorem. Recovery emits 𝑝 2 after either                     the frontier of the decision. That assumption is necessary.
crash, but only the crash after delivery makes that emission                  A stale replica, a paginated status endpoint, or a lagging
a duplicate.                                                                  projection of the sink’s state is a different observation, and


                                                                          7
nothing below applies to it without a separate argument. The            Every run keeping the three guards stays hazard-free. The
guarantee is exact, and it is conditional. The result requires          folklore version of this rule has two guards. A separate coun-
four conditions:                                                        terexample shows why each guard is required, and suffix
  P1. Hazard-free: ¬ unsafe(𝑡) (the record carries no dupli-            freshness is provably necessary once a re-drive can meet a
      cate and nothing premature).                                      record that already holds part of its window. These guards do
  P2. Crashed: the run’s status is Crashed 𝑐 for some 𝑐.                not guarantee completeness. An empty re-drive suffix satis-
  P3. In-interval: 𝑓 ≤ fin.                                             fies them while silently skipping work. The guards constrain
  P4. Ascending: the committed history’s coordinates are                what fires, not what fails to fire.
      strictly increasing.                                                 Interrupted and repeated recovery. Under P1-P4, the
Theorem 4 (Sink-Reading Escape). On the effect machine,                 small-step variant can deliver a prefix of the sink-delta batch
under P1-P4, the sink-delta re-drive at 𝑓 exists, and every re-         and stop. Within this recovery window, the frontier and
drive 𝑡 ⇝Δ⟨ 𝑓 ⟩ 𝑡 ′ leaves the store mismatch-free at 𝑓 , hazard-       every field except the ledger remain fixed. Recomputing the
free, and complete:                                                     delta returns the undelivered suffix. Partial rounds remain
                                                                        hazard-free. Delivering the remainder and repairing the store
      clean(𝑡 ′, 𝑓 ),    ¬ unsafe(𝑡 ′ ),    ¬ lost(𝑓 , 𝑡 ′ ).           completes recovery.
Proof idea. Existence follows from the atomic reconcile. The               A separate result covers repeated atomic sink-delta recov-
three conclusions follow from the delta’s shape. It never re-           eries and Resume steps. Ordinary execution between them
emits a payload already on the record, so no duplicate occurs.          must satisfy the model’s guards. From a hazard-free start,
It emits only committed obligations, stamped at the full his-           with ascending coordinates at each re-drive, every completed
tory, so nothing premature occurs. It includes every payload            re-drive is exactly-once at its own frontier. Neither result
still missing at 𝑓 , so no loss remains. None of the three is           ensures eventual completion. The status-only Recover step
automatic: each depends on the batch being computed from                can mark a run Recovered without repairing its store. It is
the same record the hazards are judged against.            □            distinct from the sink-delta re-drive of Theorem 4.
                                                                           The observation bound also holds in the small-step exten-
    On the checkpointed machine of Section 4, the same policy           sion, including finite adaptive sequences of per-entry choices
also separates that section’s pair. The proof confirms that             that cannot read the sink record. It therefore does not re-
the delta is not durable-local-measured. It uses information            quire atomic recovery. Crashes inside the fenced recovery
outside the defeated class instead of refining a policy inside          operation of Section 6 remain outside that model.
it.
                                                                           Detecting omissions. Exactly-once has two conjuncts,
   Why ascending coordinates are required. P4 does dou-                 and operators observe them asymmetrically. A duplicate is
ble duty. It is what makes the delta’s own batch internally             loud: the customer gets two emails, and an incident is opened.
duplicate-free, and it is what licenses the strongest read-             A frontier-relative omission is silent: a cursor advanced past
ing of the conclusion: each committed obligation delivered              an undelivered send leaves a record with no hazard at all,
per instance exactly once. Without it the count is set-level,           and a checked trace reaches a post-recovery state whose
by payload. That distinction matters. An equal-coordinate               computed hazard verdict is clean while a committed opera-
aliasing counterexample in the mechanization refutes the                tion remains undelivered at the judged frontier. The opening
per-instance strengthening without ascending coordinates                incident was the loud kind. The quiet kind passes the same
at the deduplication tier (Section 8). One further property             store-level audit, which is why completeness needs to be
comes free and one does not: the delta emits in committed               checked separately.
source order (a proved fact), while ordering across a real
transport is a different guarantee, which this paper does not           6   Stragglers and the Arrival Fence
provide. Section 6 models exactly where it is lost.                     Theorem 4 was proved on a machine where a send and its
  Normal execution. The delta chooses the right batch at                acceptance coincide. Real deliveries travel. They wait in retry
recovery. A companion result proves the running discipline              queues and socket buffers, arrive out of order, or vanish. The
that keeps a live, emitting system hazard-free between re-              channel machine models that traffic, and on it the sink-delta
coveries, as three record-local guards:                                 policy of Section 5 stops being enough: a read cannot see
                                                                        what is still in flight.
  G1. Fire-time justification: an ordinary publish fires only a
      payload the committed history holds at fire time.                    The channel machine. A channel state is 𝑢 = ⟨𝑡,𝑊 , 𝐴, 𝜑⟩:
  G2. Publish freshness: it fires only a payload not already on         an inner effect state 𝑡, the wire 𝑊 (emissions sent and not yet
      the record.                                                       resolved), the sink’s durable accepted record 𝐴, and a fence
  G3. Fresh reconcile suffix: a re-drive’s suffix is internally         𝜑 ∈ N, zero until set. An ordinary publish adds its emission
      distinct and wholly absent from the record.                       to 𝑊 and to the inner ledger 𝐸, which here records sends


                                                                    8
rather than acceptances. An arrival resolves one in-flight                           𝑊 : old send 𝑥 remains in flight      gen(𝑥 ) = 𝛾, pay(𝑥 ) = 𝑝 2

emission, in any order (the wire reorders freely), and the sink
accepts it into 𝐴 exactly when its generation clears the fence,              recoverer
𝜑 ≤ gen(𝑥), dropping it otherwise. An in-flight emission                                                         one atom: accept Δ           𝑥 old-send arrival
may instead be lost, as a first-class step. The bookkeeping is                                                                                          duplicate
conservative (every sent emission is at all times accounted                 unfenced 𝐴     𝑝1                       𝑝2       𝜑 =0                            𝑝2
for as in flight, accepted, or dropped), and a crash moves the                                                                              𝜑 = 0 ≤ 𝛾 accepted
run’s status and nothing else: the wire, the accepted record,
                                                                                                                                               𝛾 < 𝜑 =𝛾 + 1
and the fence all survive it, because a process crash does not
empty network buffers. Hazards and completeness are now                       fenced 𝐴     𝑝1                       𝑝2     𝜑 ←𝛾 +1

judged at the accepted record (unsafe𝐴 (𝑢) for a premature                                                                                       rejected
                                                                                                                                                       dropped
or duplicate accepted entry, alo𝐴 (𝑓 , 𝑢) for at-least-once read
                                                                              schedule
there), and exactness at 𝑓 is the conjunction                                    steps
                                                                                          send   crash     read          re-drive        resume arrival
         eo(𝑓 , 𝑢) ←→ ¬ unsafe𝐴 (𝑢) ∧ alo𝐴 (𝑓 , 𝑢),                                                      record 𝐴                         𝛾 + 1 acceptance

       alo𝐴 (𝑓 , 𝑢) ←→ replay(𝐻, 𝐾, 𝑓 ) ⊆ pay(𝐴(𝑢)).                                                     𝑝 2 arrives           read 𝐴
                                                                                   EARLY CONTROL
                                                                                                                            sees 𝑝 2 ,               exact at 𝑐 2
The unfenced policy re-drive studied below atomically re-                                                                                 Δ = [ ],

pairs the store and appends its batch to both 𝐸 and 𝐴. The                                one raise           prevents                       may reject
batch is accepted synchronously without changing the wire                                𝜑 ←𝛾 +1         this late duplicate              needed later work
or fence. Cursor-based recovery, using the suffix replay de-
scribed in Section 4, instead queues its re-sends on the wire.            Figure 3. An old send crosses the sink read. Without a fence,
Theorem 5 concerns the unfenced recovery rule just de-                    its later arrival duplicates the accepted record. The fenced
scribed. The later fenced rule is outside its scope because it            re-drive atomically lands the recovery delta and raises 𝜑, so
changes the fence. Deployed systems keep a cousin of the                  the arrival is rejected (Theorems 5-6). The lower rails show
generation under another name: Kafka’s idempotent pro-                    the benign early-arrival control and the rejection of later
ducer carries a broker-checked epoch [11], and this paper                 work by the fence (Corollary 6.1).
uses that word only for the cited mechanism.
   An old request can arrive after recovery. Figure 3 shows               has an empty wire. This pair defeats every channel-blind policy
an old send that remains in flight across the crash. Recovery             𝑃 under the unfenced re-drive relation: there are re-drives of
reads the accepted record, sends the missing payload, and re-             both members at 𝑐 2 whose outcomes satisfy
sumes in a new generation. The old request then arrives and                               arrive
the sink accepts it, producing a duplicate. Every entry is in-                  ∃𝑣. 𝑢 1′ −−−−−→ 𝑣 ∧ unsafe𝐴 (𝑣) ∨ ¬ alo𝐴 (𝑐 2, 𝑢 2′ ).
                                                                                                                

dividually justified. The duplicate comes from the run’s own              Either the straggler’s arrival leaves the first member’s accepted
valid send in the previous generation, not from malformed                 record unsafe, or the second member still lacks a delivery at 𝑐 2 .
traffic.
   When the old request arrives before the read, the read sees               Because the policy cannot observe the wire, it chooses the
it and the delta is empty. This control shows that the sink               same batch for both states. If the batch carries the missing
read is correct when it occurs. It becomes stale only when                payload, the in-flight member’s straggler arrives at the never-
the wire still contains work that can arrive after the read.              set fence and the record duplicates. If it omits it, the empty-
                                                                          wire state has no pending request that could deliver the
Definition 6.1 (Channel-blind policy). A policy 𝑃 on the                  missing event and remains incomplete. The sink-delta policy
channel machine is channel-blind when it factors through                  of Section 5 is in the defeated class (Δ reads the accepted
everything but the wire: for some 𝑔,                                      record and never the wire), and the late-arrival example
         𝑃 (𝑢) = 𝑔 ⟨ 𝑡, 𝐴(𝑢), 𝜑 (𝑢) ⟩ for all 𝑢,                          above demonstrates this failure. A variant of the opening
                                     
                                                                          example has the same hazard: a send left in a retry queue
where 𝑡 is the whole inner state, including the store, ledger,
                                                                          at crash time can produce a duplicate after an otherwise
and generation.
                                                                          correct sink read. The hazard is not an artifact of the model.
  Everything durable is inside the visible triple, the accepted           The mechanization separates the late-arrival example’s final
record and the fence included. The one field outside it is the            record from everything the instant-delivery machine can
wire itself.                                                              reach, so the guarantee of Section 5 was not false on its own
                                                                          machine. That machine could not express this failure.
Theorem 5 (Wire Bound). On the channel machine there is
a reachable pair 𝑢 1, 𝑢 2 that agree on the visible triple. One has         The arrival fence. The fenced re-drive at 𝑓 is one atomic
the crashed process’s own send still in flight, while the other           act: heal the store, compute Δ from the accepted record, land


                                                                      9
the batch in the sent ledger and synchronously in 𝐴 (a re-                the record at 𝑐 2 , exactly-once there with the payload counted
covery’s own re-sends never traverse the fenced wire), and                once, while the fenced run drops the same straggler: its result
set the fence to the successor of the crash-time generation,              remains incomplete at 𝑐 2 , and exactness holds at the fence’s
𝜑 := 𝛾 + 1. From then on the sink rejects arrivals from gen-              own frontier 𝑐 1 .
erations below the fence. The guarantee has four conditions
                                                                             The fence guarantees exactly-once acceptance at the cho-
corresponding to P1-P4, read at the accepted record (record
                                                                          sen frontier. It can still leave later work undelivered by re-
hazard-free, crashed, in-interval, and ascending coordinates,
                                                                          jecting the old request that would have delivered it.
called Q1-Q4) and, for the continuation results below, the
machine’s reachability invariants.                                        Corollary 6.2 (Residual-wire stability). Under Q1-Q4 and the
                                                                          machine’s reachability invariants before a fenced re-drive at 𝑓 ,
Theorem 6 (Arrival Fence). On the channel machine, under
                                                                          every wire entry left after the composite carries a generation
Q1-Q4, the fenced re-drive at 𝑓 exists, and every fenced re-drive
                                                                          below the fence, and along any subsequent trace of arrivals
𝑢 ⇝ 𝑢 ′ leaves the store mismatch-free at 𝑓 , is exactly-once
                                                                          and losses only, the accepted record is unchanged and exactness
at 𝑓 on the accepted record, and sets the fence to the successor
                                                                          at 𝑓 persists.
generation:
    clean(𝑢 ′, 𝑓 ),    eo(𝑓 , 𝑢 ′ ),   𝜑 (𝑢 ′ ) = gen(𝑢) + 1.                Stale arrivals cannot be admitted by reordering or de-
                                                                          lay, and losses cannot alter 𝐴. The corollary is scoped to
   The theorem assumes strictly ascending coordinates be-                 arrival/loss-only continuations on purpose: it says nothing
cause duplicate-freedom of the accepted record depends on                 about arbitrary later application work. Theorem 6 applies to
them. The theorem certifies this admission mechanism under                a later recovery only if its conditions hold at that crash. Be-
the machine’s crash-time stamping discipline. It does not                 tween recoveries, an in-flight entry is neither delivered nor
say a generation fence is the only possible way to neutralize             lost at a completed frontier. The model keeps that ambiguity
a wire. A sink that atomically deduplicates on stable event               first-class rather than resolving it by fiat.
identity at admission, for instance, is a different mechanism
with different assumptions, unmodeled here.                                  Validation controls. Two companion results locate the
                                                                          modeling choices. On a twin machine whose crash wipes the
   Fence placement. The composite’s shape is forced by a                  wire, the same schedule ends exactly-once with a duplicate-
discipline the machine inherits: re-drives stamp at the crash-            free record. Crash-survival of the wire is therefore a required
time generation (the reconcile is generation-constant, and                assumption and a realistic choice because crashes do not
resume bumps the counter only afterwards), so an earlier                  empty a network’s buffers or a sidecar’s retry queue. And
process run’s in-flight emission and the recovery’s own re-               the early-arrival schedule above calibrates from the other
drive carry the same generation, and no fence value separates             side: arrival before the read is benign, so nothing weaker
them on the wire. Set the fence at resume instead, and the                than arrival-after-read defeats reading. The model treats the
straggler slips in during the gap. Setting it in a separate step          fenced re-drive as one atomic transition and does not cover
before the re-drive would cause a recovery whose own sends                a crash inside it (Section 10).
traveled the wire to fence out its own work. Synchronous
acceptance plus an atomic rise is the one sound point in this             7    Concurrent Recoverers and the Claim
rule family. It is a design argument over the stamping disci-                  Fence
pline, while the two refuted reorderings that are theorems
                                                                          A second hazard family comes from orchestration. An or-
live one machine over, in Section 7. Figure 4 places the sound
                                                                          chestrator that loses a worker’s heartbeat can start a second
rise beside its failing neighbors.
                                                                          recovery while the first is still alive: two recoverers, each
   The fence’s policy is still the channel-blind Δ. Nothing
                                                                          reading honestly, each re-driving what it read. This section
reads the wire. That is the central point: more recovery-
                                                                          is about that pair, on a machine built for it.
side reading does not flip the verdict (that was Theorem 2),
while the same generation tag, consulted at acceptance, does.                The concurrency machine. The machine carries 𝑤 =
The fence works by changing what the sink admits, not by                  ⟨𝜎, 𝐽, 𝑆, 𝐴, 𝜑, Γ, hwm, fl⟩. Its fields are the store, a journal 𝐽
reading more.                                                             (the record justification is measured against, whose role
                                                                          sharpens in Section 8), sent and accepted ledgers, a fence,
   Cost of the arrival fence. The following corollary shows
                                                                          a generation table Γ tracking each spawned generation as
that fencing can reject a delayed delivery needed at a later
                                                                          producing or armed with a batch, the high-water mark hwm
frontier.
                                                                          (the newest spawned generation), and a retention floor fl.
Corollary 6.1 (Rejection of later work). There is one schedule            Delivery happens at the fire point: an armed generation 𝑔
over fenced and unfenced twins that differ by one rule. Recovery          fires its batch, which always lands in 𝑆 and lands in 𝐴 exactly
occurs at frontier 𝑐 1 with a straggler for 𝑐 2 in flight. On this        when the fence has not moved past it, 𝜑 ≤ 𝑔. The sink delta
schedule, the unfenced run’s straggler arrives and completes              lifts to this machine, computed against the accepted record


                                                                     10
    shared gate                               guarded event 𝑒                                     𝐴             accept iff 𝜑 ≤ gen(𝑒 )



    arrival fence                                                                                               channel machine · one recoverer · hazard rides the wire


                                                                                                guarded event      𝜑 = 𝛾 + 1 > gen(𝑥 )
         𝑥 in 𝑊           FENCED RE-DRIVE – ONE ATOM
       gen(𝑥 ) = 𝛾                                                                                                                    stopped
                                                                                                 ARRIVE 𝑥
                          heal            ·     Δ(𝐴) lands in 𝐴     ·     𝜑 := 𝛾 + 1                                                  not accepted into 𝐴



       RAISE BEFORE RE-DRIVE                                                                 RAISE AT RESUME
                           channeled re-drive                                                     re-drive               old 𝑥 arrives                      resume
           𝜑↑
                                 tag 𝛾                                                             lands                     𝜑 =0                             𝜑↑

                                 own batch stopped                                                                 old arrival already accepted



    claim fence                                                                        concurrency machine · several claimants · hazard is a worker no longer authorized

                                                                                              guarded event            𝜑 ≤𝑔
        CLAIM – ONE ATOM
                                                                                                  FIRE 𝑔                                             𝐴         accepted
        𝜑 := 𝑔        ·          read 𝐴          ·                arm Δ



       FENCE AT RELEASE                                                                      CLAIM WITHOUT READING
                             sibling FIRE                               release                  read / arm               claim
        arm / work                                     accepted                                                                                FIRE 𝑔0
                                 𝜑 =0                                     𝜑↑                        at 𝑔0              𝜑 := 𝑔1 > 𝑔0

                             sibling fires in the gap                                                             claimant’s own batch stopped


                                                     wire arrival SAME TEST ≠ SAME MECHANISM claimant fire



Figure 4. Arrival and claim fences use the same acceptance test for different events. The channel machine fences arrivals after
an atomic re-drive. The concurrency machine fences fires after an atomic claim. The side cards show invalid reorderings. Only
safety transfers between the two regimes.

over what retention has kept. There is no wire here by design.                                Fence-free one-shot recovery. The negative’s subject is
The hazards of this machine come from workers that remain                                   the natural discipline (each recoverer reads, arms once, fires
alive after losing recovery authority, not from messages in                                 once) run twice in parallel without a fence.
flight, and the two hazard families do not substitute for each
                                                                                            Theorem 7 (Second-Recoverer Bound). On the concurrency
other. Before anything new begins, the observation bound
                                                                                            machine there is a reachable crashed state 𝑊 with
reappears in a strengthened form. A policy reading the store,
                                                                                                 𝜑 (𝑊 ) = 0, 𝑔1 ≠ 𝑔2 both live, ¬ unsafe𝐴 (𝑊 ),
the journal’s length, the fence, the whole generation table,
the high-water mark, and the floor (everything short of the                                                       Δ⟨𝑓 ⟩(𝑊 ) = [ 𝑝 ].
ledgers) is still defeated on a designed pair of this machine.                              The state has four properties: the fence is unset, two generations
   Three authorities must stay separate on this machine, be-                                are live, the state is hazard-free, and exactly one delivery is
cause Section 8 pulls them apart. The live source history                                   missing at 𝑓 . For every fence-free pair of one-shot recoverers,
𝐻 sits inside 𝜎. The retention-relative obligation history is                               however each computes its batch with the whole state readable,
𝐻 ret = drop(fl, 𝐻 ). Delta, loss, at-least-once, and exactness                             some schedule in the constrained family ends in a hazard
are evaluated against replay from 𝐻 ret . The journal 𝐽 is the                              or with the delivery at 𝑓 still missing. In this family, both
authority that justifies emissions, while 𝐴 detects prematu-                                recoverers arm, at least one fires, at least one heals, and every
rity and duplication. Exactness on this machine is therefore                                recoverer that heals also fires.
retained-view-relative unless an additional condition identi-
                                                                                               The defeating schedule is four or five steps, and which
fies 𝐽 , 𝐻 , and 𝐻 ret , a relativity this section will state precisely
                                                                                            steps the adversary needs depends only on where the missing
rather than gloss.
                                                                                            payload sits in the two armed batches. If both batches carry

                                                                                       11
it, let one recoverer heal and both fire. The accepted record                  its prepare, repair, and send steps must run together
then holds the payload twice. If neither carries it, the same                  without intervening actions.
steps leave the delivery incomplete. If exactly one carries it,              • Snapshot effects must match the state reconstructed
let that recoverer die silently after arming (the family permits               from the journal prefix. These effects are used by the
one silent death) while the other heals and fires its payload-                 DBLog instance described in Section 10.
free batch. The store is repaired, the run reads recovered, and         The permitted executions exclude truncating crashes, inde-
the delivery is gone. Each recoverer fixed its batch before             pendent fence raises, and batch preparation outside a claim
the schedule chose the cell. The family’s constraints exclude           or the cursor-recovery sequence above. Retention, lost pub-
trivial defeating schedules. They cannot kill both recoverers           lishes, release, and sending an already prepared batch remain
and call the loss a defeat, and a recoverer that heals cannot           permitted.
then vanish (every healer fires). As everywhere in this paper,             Under these rules, the fence never exceeds the newest
the defeat is existential over schedules and says nothing               spawned generation. A worker can still attempt to send after
about disciplines outside the fence-free one-shot class. The            a later claim removes its authority. The sink therefore checks
positive result below uses such a discipline. The sink-delta            the worker’s generation when the batch is sent.
policy of Section 5 also fails on this axis. When run by two
claimless recoverers, the sink delta double-fires. Two honest           Theorem 8 (Completed-Claim Exactness). On the concur-
workers, each individually correct by Section 5’s rule, are             rency machine, under
jointly wrong: each read was true when taken and stale by                 C1. Initialized discipline: the trace starts at the initial state
the time it was used.                                                          and follows the claim discipline.
                                                                          C2. Claimed: generation 𝑔 claims at frontier 𝑓 and later fires,
  What ordering changes. Suppose each recoverer must                           with no intervening claim or fire of 𝑔.
prepare its batch, repair the store, and then send, with no step          C3. Window-fresh: no source commit at or below 𝑓 lands
skipped. The model permits only one store repair per crash,                    between the claim and the fire.
so these ordered schedules contain at most one completed                  C4. Completed at the fence: 𝜑 ≤ 𝑔 when the fire lands, so
recovery. At the constructed state, a completed sink-delta re-                 its batch is accepted.
covery is exactly-once. The duplicate in Theorem 7 therefore
                                                                        the post-fire state is exactly-once at 𝑓 , judged against the re-
requires a recoverer to send without completing its store
                                                                        tained obligation history 𝐻 ret . Per-instance exactness addition-
repair.
                                                                        ally requires ascending coordinates. Without them the count is
  Ordering does not ensure that a batch contains the missing
                                                                        set-level, by payload.
work. Fully ordered schedules exist for every pair of batch
choices. If one batch omits the missing payload, there is an               Window freshness is required. A commit at or below 𝑓
ordered schedule in which that worker completes while the               landing inside the claim window grows the set of required
other stops after preparing its batch. The delivery remains             deliveries after the batch was fixed. One modeled idealization
missing. The original schedule family also includes these               must be stated here: the fire transition executes its armed
ordered schedules.                                                      batch atomically. A recoverer crashing after a strict prefix of a
                                                                        multi-item batch is outside the modeled transition. Per-entry
  The claim fence. An atomic claim by generation 𝑔 re-
                                                                        firing is future work, and Section 10 carries the absence.
quires 𝜑 ≤ 𝑔, so claims never lower the fence. The claim
sets the fence to 𝑔 and arms the batch computed from the                   Retention-relative exactness. The theorem’s conclusion
accepted record read in that step. The later fire is accepted           is graded against what retention kept, and the difference
only if 𝜑 ≤ 𝑔, meaning it completed at the fence.                       matters. The machine’s retention step has no guard, so a dis-
Lemma 7.1 (Claim-fence safety). Every claim-disciplined                 ciplined run can raise the floor over an obligation that was
trace from the machine’s initial state is hazard-free.                  committed and never delivered, dropping it from the graded
                                                                        history without disturbing the theorem’s verdict. The mecha-
  The safety proof requires the following restrictions in               nization includes a concrete control trace that is exactly-once
addition to the machine’s usual state and history checks.               relative to retained history while, judged against the journal,
   • Ordinary delivery sends only committed events that                 a committed obligation is lost. That run’s accepted record is
      are absent from the acceptance record. It pauses while            empty. The stronger, journal-graded statement is then closed
      any prepared recovery batch remains authorized by                 under either of two conditions, and the boundary between
      the fence.                                                        them is itself a theorem. On the permanent-source fragment
   • A claim prepares a duplicate-free batch from the sink’s            (journal equal to the committed history, floor zero), the two
      acceptance record. The alternative cursor-recovery                grades provably coincide, and Theorem 8 yields journal-
      sequence must use a duplicate-free suffix containing              grade exactness outright. Off that fragment, the bridge is
      only events absent from that record. It cannot start              floor-prefix coverage: everything retention dropped below
      while another prepared batch remains authorized, and              the floor was already accepted.

                                                                   12
Corollary 7.1 (Journal-grade exactness). With the journal                  8   Evidence Lifetime
equal to the committed source history,                                     Systems often combine at-least-once delivery with dedupli-
       eo 𝐽 (𝑓 , 𝑤) ←→ eoret (𝑓 , 𝑤) ∧ coveredfl (𝑓 , 𝑤),                  cation [2, 4]. Theorem 9 gives a coverage identity for an ideal
                                                                           sink view with permanent memory. The remaining results
where eo 𝐽 and eoret grade exactness against the journal and               examine bounded memory and loss of source history.
the retained history respectively, and coveredfl (𝑓 , 𝑤) means
that every scoped source event at or below 𝑓 that retention                   Permanent deduplication. Model the idempotent con-
has excluded from replay already appears in the acceptance                 sumer as the absorbing, permanent-memory deduplicated view
record. In particular, a disciplined run whose retention steps             of the sink’s record, in which repeated payloads are absorbed,
only ever drop already-accepted obligations delivers journal-              dedup(𝑡) = remdups(pay(𝐸 (𝑡))), remembering every pay-
grade exactness through Theorem 8.                                         load it has ever seen. For a list 𝐿, #𝑝 𝐿 is the multiplicity of
                                                                           payload 𝑝.
   The equivalence is the precise form of a folklore sentence
(“replay what retention kept, and make sure retention only                 Theorem 9 (Deduplicated-View Coverage Identity). On the
expires what was delivered”), and the guard-free counterex-                effect machine with the absorbing, permanent-memory view:
ample above is why the second clause cannot be dropped.                    every payload in the set of scoped replay obligations at 𝑓 is
                                                                           represented exactly once in the deduplicated view if and only
   Two invalid orderings. The discipline depends on this or-
                                                                           if delivery is at-least-once at 𝑓 :
der. Two concrete counterexample traces refute the tempting
variants (Figure 4, lower row). Fencing at release (doing the                 ∀𝑝 ∈ replay(𝐻, 𝐾, 𝑓 ). #𝑝 dedup(𝑡) = 1 ←→ alo(𝑓 , 𝑡).
                                                                                                                     
work first and setting the fence at hand-off) admits a batch
                                                                              The view is duplicate-free by construction. The theorem
from an earlier worker before the fence is raised. Claiming
                                                                           establishes whether every required payload is present. It does
without reading (setting the fence over a batch computed be-
                                                                           not rule out premature effects on the underlying record or
fore the claim) fences out the claimant’s own re-drive. Claim
                                                                           verify a consumer’s implementation of checking for a prior
first, read under the claim, fire under it.
                                                                           effect, applying the effect, and recording its completion.
    Interface between the two fences. This paper now has                      The per-instance corollary additionally requires strictly
two fences, and no theorem merges them. The arrival fence                  increasing source coordinates. An equal-coordinate exam-
guards a wire: one recoverer, arrivals from its own past. The              ple refutes that stronger conclusion without the condition.
claim fence guards a fire point: several recoverers, including             The following results examine the assumption of permanent
workers that can still send after losing recovery authority.               memory.
They live on different machines. What is proved between
the regimes is one interface with two obligations:                            Bounded deduplication. Real deduplication memory is a
                                                                           window, and the window here is an entry-count horizon, mea-
   (T) Transport delivers a sub-multiset: what arrives is a sub-           sured in record positions, not seconds. A duration maps to
        multiset of what was sent (reorder, delay, and drop are            it only through a delivery-rate argument. A legal-run coun-
        allowed, but fabrication, duplication, and alteration              terexample shows how the guarantee fails. A windowed view
        are not).                                                          satisfies the same equivalence at a reachable state, and then
    (J) Justification is monotone: a record that justifies an emis-        one more crash and one more honest re-drive push the orig-
        sion still justifies it after any extension.                       inal delivery out of the window, so the sink processes the
The claim discipline’s safety argument is proved once against              re-driven copy as new. The windowed count reads two while
these obligations alone, then instantiated twice: by a gen-                permanent memory still reads one. For the constructed run
uine pullback from this section’s fire point, and by a sibling             the threshold is sharp between window sizes one and two,
abstract wire grammar that permits loss, reordering, and                   and the window-sufficiency condition that protects a run is
arrivals from earlier generations. That sibling is not Sec-                proved sufficient and not necessary. The operational shape
tion 6’s channel machine and does not re-derive its theo-                  of the hazard is familiar: Stripe’s idempotency keys become
rems. The asymmetry is the interface’s shape: safety crosses               eligible for removal after at least 24 hours [12], and Kafka’s
it, exactness does not, and nothing else crosses at all. Note              producer-ID expiration setting defaults to one day, although
also what obligation (T) excludes: transport that duplicates a             ongoing transactions and topic retention affect when state
staged item. A generation fence rejects requests from gener-               expires [13]. An outage that outlives the deduplication hori-
ations below its current threshold. It does not deduplicate                zon reproduces the incident in its quiet form: recovery is
a same-generation copy the transport minted on its own.                    honest, the keys are gone, and the re-drive lands as new
Deployments running over at-least-once transport need sta-                 work.
ble identity and an admission or deduplication contract in
addition to anything this section proves, and Section 8 is                   Deduplicating by key. Deployed systems often match
about how long such contracts hold.                                        events by keys such as an LSN, offset, or idempotency


                                                                      13
key [12]. The keyed policy compares source coordinates in-                everything a policy could ask for, except that the journal
stead of the full payload (𝑐, 𝑒). It computes the same missing            enters only as its length. Now take two runs that each commit
batch when source coordinates increase strictly and every                 one event, differing only in which, and let a truncating crash
accepted entry matches a committed source record.                         cut both live histories back to empty. The surviving stores
   Each condition has a separate counterexample. Coordinate               are literally equal, and so is every other slot of the view:
matching can remove entries from the batch selected by full               same fence, same generation table, same high-water mark,
payload matching, but cannot add entries. The counterexam-                same floor, same two ledgers, and journals of the same length.
ples show how this can suppress a required replay and leave               The journal contents differ, hidden from the policy, and with
committed work undelivered. Comparing only application                    them the sets of required deliveries. One state still has an
contents is also insufficient. Distinct committed operations              undelivered event at 𝑓 . The other requires no delivery at
can have identical contents, and their source coordinates                 that frontier.
distinguish them. Derive the key once, at commit time, from
                                                                          Theorem 10 (Truncation Dilemma). On the concurrency
that stable coordinate.
                                                                          machine there are reachable states 𝑊1,𝑊2 with equal retained
   Compaction that keeps presence. On the sink’s own                      views over differing journals. State 𝑊1 has an undelivered event
record the safe boundary is presence. Rewrites that preserve              at 𝑓 according to its journal, while𝑊2 requires no delivery there.
a record’s presence (compaction, tombstoning that keeps the               Every policy computed from the retained view is defeated: there
key’s entry) do not affect the windowed policy, which needs               are re-drives of both at 𝑓 under which 𝑊2 ’s outcome is a hazard
no more than window-local presence. Presence-destroying                   (a fabricated delivery where none was required) or 𝑊1 remains
retention fabricates duplicates at a reachable state. The win-            incomplete at 𝑓 (abandonment).
dowed policy never loses work, so its only failure is dupli-                 Whatever rule the policy runs, one state makes it fabricate
cation. This bounds what the policy analyzed here needs to                work or the other makes it abandon work. Two follow-ups
read. That no policy could do better with bounded memory                  make the theorem usable. Reading the live source instead of
is not claimed (Section 10).                                              the journal does not help and actively harms: the machine
                                                                          admits phantoms (deliveries whose justifying record is gone),
   Compensation instead of deduplication. Sinks with re-
                                                                          and judging against the live history makes them retroactively
versing entries permit another approach: compensate, then
                                                                          premature, which is the machine-checked reason justifica-
redo. The theory analyzes three selected compensation obser-
                                                                          tion measures against the journal in the first place. And the
vations (matched cancellation, signed net, and truncation),
                                                                          practitioner’s version of the boundary is about content versus
and the verdicts split. Under the matched-cancellation view,
                                                                          extent: retention that hides old content while an authorita-
order-aware compensate-then-redo normalizes both out-
                                                                          tive journal can still reconstruct it is recoverable. A crash
comes of the designed pair. The same batch succeeds on both
                                                                          that leaves recovery with only length-like metadata is what
members because the judged observation has changed. Un-
                                                                          the theorem describes. Keep the recovery window’s journal
der the signed-net observation, the construction again forces
                                                                          content reconstructible, not just its size.
recovery to choose the same batch for states that require
different actions. Truncated views do not distinguish the
                                                                          9    Store-Tier Characterization of
pair either. Throughout, the underlying record stays append-
only. Reversal operations never delete sent events, but in-                    Log-Derived State
stead append matching reversing emissions in sequence. The                CDC and the transactional outbox are the standard remedy
matched-cancellation result is proved for the abstract re-                for dual writes, and they are widely deployed: Debezium
drive relation. It is not an execution of this machine’s suffix-          alone ships log connectors for most major databases [14].
only reconcile. Realizing it requires a compensation-capable              Everything so far has treated “derive downstream state from
transition, or a refinement proof for an implementation that              the committed log” as sound advice whose delivery stage
has one.                                                                  still needs a theory. This section proves the advice’s own half
                                                                          exactly, and locates the boundary between the two halves.
   Source truncation and journal evidence. The second
shrinkage is upstream, and it is the harsher one. On the con-                Store-tier characterization. At the store tier, the model
currency machine, retention raises the floor over a history               is Section 2’s substrate with implementations over it. An
that still exists. A truncating crash instead cuts the live source        implementation supplies an initial state, a step relation, and
history itself, while the journal 𝐽 remains the specification             a projection to core states. Three properties name what the
of which deliveries were required. What recovery can read                 theorem asks of it:
afterwards is the retained view                                             R1. Crash-closed: every reachable running state can crash
                                                                                at every in-interval frontier.
         view(𝑤) = ⟨ 𝜎, |𝐽 |, 𝜑, Γ, hwm, fl, 𝑆, 𝐴 ⟩,                        R2. Refining: its steps project to the substrate’s.
                                                                            R3. Running-start: its initial state is Running.

                                                                     14
For a materialized map ℎ, ℎ ↾ 𝐾 is restriction to scoped keys.            for establishing complete-frontier image faithfulness at the
An observable mismatch at (𝑐, 𝑘) means the state is Crashed 𝑐             frontiers they advertise, not as global faithfulness at every
with 𝑐 ≤ fin and the committed and downstream material-                   instant. An advertised frontier is a claim. The theorem says
izations disagree on scoped key 𝑘 at 𝑐.                                   what that claim must mean.
Theorem 11 (Faithful-Image Equivalence). For a crash-                        Limit of the store tier. The designed pair of Theorem 1
closed, refining, running-start implementation 𝐼 of the store             agrees on the whole store, so store-tier faithfulness can-
model: 𝐼 has no reachable observable scoped mismatch at a                 not arbitrate a single re-delivery decision. The acceptance
crash frontier if and only if 𝐼 is running-image-faithful at every        boundary begins where this biconditional stops. The tier
reachable Running state and every in-interval frontier 𝑓 ,                scales to multiple derived targets without new theory. The
             Src(𝑏, 𝐷, 𝑓 ) ↾ 𝐾 = Src(𝑏, 𝐻, 𝑓 ) ↾ 𝐾 .                      proof shows that fan-out diverges exactly when some sin-
                                                                          gle target does, and a target in the formal log-derived class
   Unlike the recovery bounds, which are constructions, this
                                                                          (which requires image equality at every modeled frontier)
equivalence quantifies over all implementations of its tier:
                                                                          is excluded from the divergence class. That is a statement
the one result in the paper that is universal over implementa-
                                                                          about the formal class, not a blessing of every architecturally
tions, as promised in Section 2. It characterizes the equality
                                                                          log-backed but lagging deployment. The per-target reading
that “derive from the log” must establish: under R1-R3, keep-
                                                                          is the right one, and no cross-target atomicity is implied.
ing the running downstream image faithful to the commit-
ted log is store-tier crash safety, in both directions. The two              Derivation relocates the delivery boundary. A log-
directions are useful in different places. Faithfulness rules             derived pipeline still has to deliver. The relay that tails 𝐻 and
out crash-frontier mismatches by a structural step: a crash               writes the sink performs, per event, two durable effects (the
changes no history, so a mismatch frozen at a crash was                   delivery and its own progress record) with no shared commit
already present at a running predecessor, where faithfulness              between them: Section 2’s effect machine under an opera-
forbids it. That step needs R3, and R3 is necessary. An imple-            tional name. This relocation claim is an argument assembled
mentation that begins already crashed has no running states               from proved parts (Theorem 11 below the boundary, Theo-
at all, is faithful vacuously, and is unsafe anyway. That class           rems 1-7 above it), and we state it at that level rather than
provides the counterexample when R3 is omitted. The con-                  as a theorem of its own. In the incident’s terms: the relay
verse is where R1 works: if some reachable running state held             tailing committed orders was already this stage. Derivation
a scoped mismatch at an in-interval frontier, crash-closure               had removed the handler’s dual write and left the delivery
supplies a crash at that frontier, making the mismatch ob-                loop’s own, which is where the crash found it. The replayable
servable. If R1 is weakened to crashes at only some frontiers,            log lets the relay retry failed deliveries and catch up after an
the argument has no crash to take.                                        outage. The sink must still provide the acceptance evidence
    Relay example. The two-event instance shows the bi-                   and controls recovery needs. Nor is “derive from the log” a
conditional at work. A downstream derived from the log                    single design point: the store tier’s replay interface has two
in committed order has image 7 at 𝑐 1 and 9 at 𝑐 2 , matching             genuinely distinct certified inhabitants, a refresh-free outbox
the source at both frontiers. No crash of that run freezes                segment and the snapshot-replay instance of Section 10, and
a mismatch. Now let the relay acknowledge the update at                   mechanized witnesses establish their distinctness.
𝑐 2 but defer the write. Its delivered history still stops at the
insert, so at frontier 𝑐 2 the downstream image reads 7 against              Two roles for an outbox. Table 1’s role split matters here.
the committed 9: a scoped mismatch at a running frontier,                 An outbox table read by the relay as its source is the commit-
and by R1 a crash is available right there to expose it. The              ted log 𝐻 . It is not thereby an acceptance record. The same
practitioner’s version is short: at this tier the crash adds no           physical table realizes 𝐴 only if it holds sink-owned accep-
window of its own (what a crash can expose is exactly the                 tance state updated atomically with acceptance. Otherwise
gap between the committed log and the derived image at a                  𝐴 is a separate durable record on the sink’s side. Sentences
running frontier), so derive from the log, in the log’s order,            about “the outbox pattern” that do not name the role equiv-
and close that gap.                                                       ocate between the two sides of the acceptance boundary: 𝐻
    A lagging relay also shows what the theorem does not pro-             is what Theorem 11 governs, while 𝐴 is what Theorems 4
vide. Between the acknowledgement and the deferred write,                 and 6 consume.
the relay is not running-image-faithful, and no theorem here
says a lagging pipeline “catches up.” Liveness is outside this            10    The Mechanization
model. The constructive result is frontier-scoped. At every               This section explains how the recovery models relate and
occurrence-complete frontier (one whose scoped obligations                what the Isabelle proofs establish.
have all been delivered), the image is mismatch-free. CDC
and outbox designs should therefore be read as machinery


                                                                     15
  Relationship between the machines. Write 𝜄 for the                      ■ carried ◦ absent       substrate effect    wire acceptance          fire point
                                                                          ⊘ no wire
embedding of effect-machine states into the concurrency                                                𝜎     𝐸    𝛾    𝑊      𝐴      𝜑   𝐽     𝑆    Γ hwm fl
                                                                          state delta
machine and Π for the projection back.
                                                                          1 effect machine
Theorem 12 (Shared-Core Agreement). (i) 𝜄 embeds every
effect-machine trace into the concurrency machine’s solo frag-
                                                                          2 channel machine
ment. Projection Π maps every solo-fragment trace from a
solo-invariant state back while preserving the invariant, and
                                                                          3 concurrency
Π ◦ 𝜄 is the identity. (ii) Under the alignment conditions that                + truncation
everything sent is accepted, the journal equals the committed
history, and all payloads are log entries, the hazard verdicts
premature, duplicate, and unsafe agree through Π. (iii) With               shared substrate        𝜎 = (𝑏, 𝐻, 𝐷, 𝑄, pend, 𝐾, fin, st, Ack)
the ledgers equal and the retention floor at zero, the sink-delta
                                                                                                           implements 𝜎
batch and the loss and at-least-once verdicts commute with Π.
                                                                            4 store model                                  𝐼 |= R1–R3
   So the small machine of Sections 3-5 really is a fragment of
the large one of Sections 7-8: same verdicts, same deltas, un-
                                                                          shared core                                 acceptance interface
der conditions that align the larger machine with the smaller
one. The fragment excludes several behaviors. The solo gram-                                                                             T/J
mar admits ordinary lifted steps, fused recovery, and suc-                                     𝜄
                                                                             1                                3        𝑊∗                                    3
cessive generation changes, and excludes free arms, free                                       Π
fence raises, snapshots, lost publishes, truncating crashes,                               T12                              safety             exactness
and retention. Of the shared-core laws, the three-guard fire
discipline of Section 5 transports through Π. The rest were               wire results
                                                                                           2       𝑊                                                         3
re-proved on the larger machine. Two non-transfers are struc-                                              no lift                   no follow
tural rather than accidental: the effect machine’s absorbing
recovery class does not lift (release and resume break absorp-
                                                                         Figure 5. Fields and relations of the three recovery machines
tion, and the successor law is open) and the wire is omitted
                                                                         and the store tier. The checkpointed model extends the effect
from the concurrency model. The concurrency machine has
                                                                         machine with a durable cursor and is not shown separately.
none, so Section 6’s results neither follow from it nor imply
                                                                         Filled squares mark carried fields, and the slashed circle
anything on it, and the regimes touch only at Section 7’s
                                                                         marks the absent wire. The lower diagrams show the shared-
interface. Figure 5 draws the resulting family.
                                                                         core embedding, the safety-only interface, and the blocked
   Recovery cycles and the core model. Resume changes                    wire relation.
Recovered to Running and increments the generation. The
histories and emissions ledger stay unchanged. The core
model has no matching transition, so the proof divides exe-              on both of its instances. The full development rebuilds from
cutions of the cyclic machine at Resume.                                 cold in a few minutes on a laptop.
   Each resulting segment corresponds to an execution of the                Validation controls. The formalization includes four val-
core model with relay repair added. The store-level theorem              idation controls. Closed witnesses show that the negative
applies to sequences of label steps from the segment’s start-            and positive theorem classes are inhabited. Twin runs test
ing state, subject to the stated checks. It excludes relay repair        the modeling choices used by the straggler result. A small-
and further Resume steps. A checked example preserves a                  step model confirms that the observation bound does not
store mismatch across Resume and repairs it after a later                depend on atomic recovery. A counterexample found dur-
crash.                                                                   ing development required an additional condition for keyed
                                                                         deduplication. Scratch gate sessions also checked the main
   Prover and trust base. Every numbered result in this
                                                                         proof terms for unproved dependencies. A planted failure
paper is a machine-checked theorem in Isabelle/HOL [15],
                                                                         confirmed that this check detects an unfinished proof. These
checked in a mode where an unfinished proof fails the build.
                                                                         scratch sessions are not part of the released development.
The trusted base consists of stock Isabelle2025-2 and, beyond
the standard prelude, exactly two standard-library theories                Executables. Certified executables accompany the theory,
(finite multisets and subsequence orderings). There are no               chief among them an exported, theorem-correct store/hazard
global axioms and no proof oracles. Theorems state their                 decider and the core store machine’s trace validator. Both are
assumptions explicitly. The one named-assumption context                 point evaluators, and their limits must be stated: a clean haz-
(the acceptance interface) has its two obligations discharged            ard verdict is not exactly-once (completeness at the frontier


                                                                    16
is the second conjunct, and no hazard audit sees it), and the              DBLog instance. A pipeline in the style of DBLog mixes
validator certifies label structure, not history wellformedness.        an initial snapshot or backfill with live log records, and the
In the other direction, the decider strengthens the observa-            theory covers the mixture at the safety level. Justification
tion bound from below. No function of the durable core alone            is append-stable across the machine, mixed-discipline runs
computes even the hazard verdict.                                       stay hazard-free, and the log-only fragment recovers the de-
                                                                        livery hazards exactly as stated. Two boundaries are explicit.
  Model boundaries. The model has six limitations.                      The snapshot modality provides safety guarantees without
    • A crash inside the fenced re-drive. The composite of The-         exactness laws. And the watermark algorithm itself is not
      orem 6 is one atom. Nothing covers a crash between                re-proved here: the instance consumes our prior snapshot-
      its heal, its landing, and its fence rise. An implementa-         replay development by citation [16], through a proved bridge,
      tion must realize the atom transactionally or supply              and that development’s own disclosed assumptions remain
      its own recovery argument.                                        its own. One fact about process belongs here: at the time
    • Two-step publish. A send and the sink’s readable record           of writing, no independent expert has cold-read the formal-
      coincide (and a fenced recovery’s own re-sends land               ization. The machine check and the controls above are the
      synchronously). A sink that acknowledges first and                evidence on offer.
      persists later is outside the model.
    • Per-entry claim fire. The claim machine’s fire executes              Availability. The full development is publicly archived
      its armed batch all-or-nothing. A recoverer crashing              as a permanent deposit [17], with build instructions and an
      partway through a multi-item batch is outside the mod-            index mapping every numbered statement in this paper to
      eled transition.                                                  its mechanized counterpart.
    • Truncation on the wire machine. Fabricate-or-abandon
      is proved at the fire-point machine. The wire-tier lift           11    Related Work
      is open, and no wire-tier truncation result exists here.             Operational guidance. The operational rule has been
    • Bounded-memory converse. Section 8 bounds what the                public for a decade, in places peer-reviewed: Kleppmann’s
      policy analyzed here needs to read. It does not prove             dual-writes argument and its book form [1, 2], the log-centric
      that every bounded-memory policy requires the same                architecture literature [3], and Treat’s essay on exactly-once
      information.                                                      delivery [4]. This paper formalizes the recovery decision that
    • Successor recovery-class law. The effect machine’s                remains after log-based derivation. Its theorems identify the
      recovery-cycle structure stops at the embedding of                sink acceptance evidence needed to decide what to resend
      Theorem 12. Its concurrency-machine successor is                  and state the conditions for correct recovery.
      open.
                                                                           Formal studies. Closest to our subject are bounded model
   Scope of the model. The absences above concern mechan-
                                                                        checks of outbox and log-delivery designs: Masternak and
ics. One more concerns shape. Every result in this paper con-
                                                                        Pobiega model-check an exactly-once outbox in TLA+ [9],
cerns a single one-way pair: one authority holding a durable,
                                                                        and LogPlayer model-checks in-order exactly-once delivery
ordered, per-operation record that defines the required de-
                                                                        to backend shards [10]. Both predate this work. The bound-
liveries, one endpoint whose durable acceptance defines the
                                                                        ary between us is method, and it matters here: a bounded
done work, one delivery direction between them. That shape
                                                                        check certifies the states it enumerates, while the observation
covers the log-derived pipelines this paper grew out of, and it
                                                                        bound of Sections 3-4 is a higher-order claim over arbitrary
excludes real configurations by design: obligations running
                                                                        policy functions, which is the kind of statement finite enu-
both ways, several sources feeding one sink, or one source
                                                                        meration cannot reach. Our result covers arbitrary recovery
feeding several sinks bound together rather than held each
                                                                        policies restricted to the modeled source-side state. We know
to its own pair, chains judged end to end rather than hop
                                                                        of no earlier machine-checked proof with this scope.
by hop, payloads transformed in flight rather than delivered
verbatim, and pairs in which even the source keeps no com-                 Impossibility results. The classical results bound our
mitted record of what it wrote (nothing left to identify the            scope rather than supply our theorems. FLP [18], in mech-
required deliveries, so the model cannot pose the question).            anized form too [19], concerns asynchronous consensus
The shape is not an arbitrary cut: its capabilities are the same        liveness. CALM [20] characterizes coordination-freeness.
ones every result turns on. Each positive theorem states the            CAP [21] trades availability under partition. Our model con-
capability it requires, and each bound is proved against a              cerns a different question: whether recovery can determine
named class of policies that lacks it. The generalization this          what an independent sink accepted. Mechanized impossi-
boundary map points toward is a theory that treats both end-            bility work such as Pactole [22] provides a methodological
points as capability-graded nodes of one kind and recovers              precedent for proving limits on classes of protocols.
these results as the one-way, record-bearing instance.


                                                                   17
   Atomic commitment. The classical way to remove a                    12    A Practitioner’s Guide to Dual Writes
separable completion window is a shared commit [23], and                     and CDC Recovery
atomic commitment across autonomous stores has its own                 This section translates the formal results into an operational
theory and impossibility results [24, 25]. Our failure class           guide for backend software engineers, systems architects,
instead has the source committed, delivery incomplete, no
                                                                       and reliability practitioners. Statements here are direct read-
coordinator and no votes. Where a real shared commit spans
                                                                       ings of numbered theorems or engineering guidance based
both effects, the window this paper studies never opens.               on them. Throughout, the frontier is the position in the com-
Where the sink cannot join one (the usual reason the pat-              mitted source log up to which delivery is judged, and a relay’s
tern exists), these theorems apply. Nothing here bears on              generation is its restart counter, which identifies the current
commit-protocol correctness.                                           run. We address two production architectures: (1) direct dual
  Verified data systems. Mechanized systems work ad-                   writes in application request handlers, and (2) transactional
dresses several adjacent problems. VerIso [5] and mechanized           outbox and CDC pipelines with asynchronous relays.
serializability [26] treat isolation inside a database, with no
                                                                          The dual-write dilemma across one process and a
crash-fed second store. GoJournal and Perennial [6, 7] verify
                                                                       CDC relay. Dual writes arise whenever an application must
one store’s crash safety, with no independently written copy.
                                                                       record related facts across two systems that do not partici-
Disel [8] supports compositional verification of distributed
                                                                       pate in a shared transaction (like a two-phase commit). In
protocols and their clients, including a two-phase-commit
                                                                       distributed architectures, this problem manifests in two pri-
case study. These studies address isolation, crash safety, or
                                                                       mary patterns.
protocol composition. Our focus is the recovery decision at
                                                                          Pattern 1: Direct dual writes in application handlers. An
an independently accepting sink.
                                                                       application service receives a user request (like an order
   Scope of deployed guarantees. The model gives deployed              checkout) and attempts to update its primary database while
exactly-once machinery a vocabulary for where its guaran-              publishing an event to a search index, or partner API. If
tees stop. Kafka’s idempotent producer and transactions [11]           the database transaction commits first and the application
deduplicate broker-side by producer id, epoch, and sequence            crashes before invoking the external API, the database holds
(the epoch is a deployed cousin of our generation, consulted           a committed record whose external side effect was never
at acceptance). The producer-ID expiration setting defaults            triggered. If the external API call succeeds first and the data-
to one day. IDs do not expire during an associated ongoing             base transaction subsequently rolls back, an external side
transaction, and topic retention can cause earlier expiry [13].        effect was released for a transaction that never existed. Net-
These retention limits illustrate the finite evidence lifetime         work calls across boundaries are also three-valued (success,
studied in Section 8. Flink’s two-phase-commit sink [27, 28]           failure, or timeout): on timeout, the caller cannot determine
places transactional acceptance at the sink. Kafka Streams’            whether the packet was lost before arrival or only the ac-
exactly-once guarantee covers processing from source topics            knowledgment was lost, so retrying can duplicate side effects.
to output topics and state stores [29]. That is a scope bound-         Distributed transactions (XA/2PC) [23] are widely avoided
ary, not a defect, and outside it sits the boundary this paper         in distributed architectures due to blocking latency, coordi-
studies. No broker, connector, or runtime is verified here.            nator failure risks, and the lack of 2PC support across cloud
The map says where each guarantee stops, in the model’s                services and external APIs.
terms.                                                                    Pattern 2: The transactional outbox and CDC relay. To elim-
                                                                       inate direct dual writes in application code, the standard
   Prior use of fencing. Fencing by monotonic token is
                                                                       industry pattern is the transactional outbox combined with
established engineering: Kleppmann’s fencing-token argu-
                                                                       change data capture (CDC) [1, 2, 14]. The application writes
ment [30], Kafka’s producer epoch [11], and mechanized
                                                                       its application records and an outbox event into the same
lease reasoning in Grove [31]. We claim the theorems, not
                                                                       local database transaction. A separate relay process (such as
the mechanism: the defeat of every channel-blind policy on
                                                                       a Debezium connector or outbox worker) tails the commit-
a designed pair, the conditional arrival-fence result with its
                                                                       ted database log or outbox table, delivers each event to the
cost stated as a corollary, and the claim-fence guarantee, to
                                                                       external sink, and records its own progress.
our knowledge the first mechanized separation of that infor-
                                                                          The relocation of the dual write. Change Data Capture re-
mation bound from a fenced acceptance result. The corpus
                                                                       locates the dual write rather than eliminating it. Instead of
models no clocks and no leases, so it neither supports nor
                                                                       occurring in the application handler, the dual write now sits
refutes lock-service designs.
                                                                       in the relay delivery loop. For every event, the relay must
   Connection to DBLog. The worked instance uses the                   execute two distinct durable operations under independent
snapshot-replay model from our prior study of DBLog [16].              authorities: first delivering the event to the external sink,
Section 10 uses that model as a substrate. It is not prior art         and second recording a local checkpoint (such as advancing
for the recovery claims made here.                                     an offset, watermark table, or message cursor). Because no


                                                                  18
transaction spans the external sink and the relay local check-           records, not the sink’s durable acceptance. In a post-crash
point store, a crash between delivery and checkpointing                  state where delivery succeeded but the checkpoint write
reopens the dual-write dilemma. When both source and sink                failed, the source database, write-ahead log, outbox table,
are Kafka topics and consumer offsets are committed inside               and cursor look bit-for-bit identical to a state where delivery
the producer transaction via sendOffsetsToTransaction,                   never occurred. Any source-measured recovery policy must
the system achieves a shared commit where the dual-write                 choose the same action in both states, duplicating delivery
window never opens (Section 11). In heterogeneous pipelines,             in one or silently omitting it in the other (Theorems 1-2,
Theorem 11 (Section 9) shows that store-tier crash safety                Section 3).
amounts, under its assumptions, to one condition, that the                  Committing a checkpoint after every single message re-
derived copy matches the committed log at every running                  duces the replay backlog during recovery, but does not elimi-
frontier, and the delivery obligation then moves to the relay            nate the crash window. It merely cycles the window once per
(Section 9).                                                             event. Theorem 3 (Section 4) strengthens the bound to this
                                                                         exact setting: for a deterministic protocol that checkpoints
   Defining the acceptance boundary for API sinks and
                                                                         after every send, crash timing alone constructs two reachable
email. To design recoverable delivery, engineers must draw
                                                                         post-crash states that agree on the local cursor and disagree
a clear boundary around what the delivery stage controls.
                                                                         on sink acceptance.
Consider an application sending shipping confirmation
emails through an external provider API (such as Mailgun                    Classifying sinks by recovery capability. Recovery
or AWS SES), operating across two distinct regimes:                      depends on two distinct capabilities exposed by the sink,
    • Durable API acceptance. The delivery obligation is satis-          namely what the sink lets recovery read (visibility) and what
      fied when the provider durably accepts custody of the              the sink enforces at admission (control). Practical sinks fall
      payload. An HTTP 200 OK or 202 Accepted response                   into three archetypes (summarized in Table 2).
      containing a provider-assigned message ID evidences                   Archetype 1: Blind or write-only sinks. When the sink API
      acceptance only if issued after durable persistence, as            provides no query endpoint to inspect past acceptances and
      documented by the provider. If the provider does not               does not support idempotency keys or fencing, recovery can-
      document post-persistence acknowledgement, conser-                 not determine what was delivered. No recovery policy that
      vative recovery must treat the response as non-durable             consults only source-side state can achieve exactly-once de-
      and verify delivery via the provider query API. In the             livery at the recovery frontier (Theorem 1). The system must
      formal model (Section 2), this transition marks durable            explicitly select its failure preference by either resending on
      acceptance: once accepted, the obligation is completed             ambiguity (accepting duplicates) or skipping on ambiguity
      regardless of downstream transit.                                  (accepting omissions). Client-side retries and backoff do not
    • Downstream asynchronous transit. Everything follow-                remove this trade-off [4].
      ing durable API ingestion (internal queues, MTA                       Archetype 2: Queryable logs and stores. When writing to
      routing, SMTP handshakes, spam scoring, and inbox                  a sink whose accepted history can be read back (such as a
      polling) lies outside the delivery stage’s authority.              Kafka topic or secondary database table), recovery can query
      Transit delays must not be conflated with delivery                 the sink to inspect which events are present. By comput-
      acceptance.                                                        ing the difference between the committed source log and
                                                                         the sink’s accepted records, recovery resends only missing
This distinction applies equally to payment gateways (such as
                                                                         events (the Sink-Reading Escape of Theorem 4, Section 5).
Stripe charges [12]), message brokers, and webhooks. A relay
                                                                         Three operational conditions govern this approach:
crashing while awaiting an HTTP response cannot deduce
from local state whether the sink accepted the payload before                • Coordinate monotonicity (Condition P4). Source coor-
the connection dropped.                                                         dinates must be strictly increasing per event in com-
                                                                                mit order (such as a database WAL LSN or an outbox
   Why local state cannot prove delivery. When a relay                          event coordinate assigned at commit). Auto-increment
crashes and restarts, its local log and outbox records are in-                  sequence numbers generated at insert time can com-
tact, and the last durable checkpoint cursor points to event                    mit out of order under concurrent transactions, which
𝑁 . Whether the sink accepted event 𝑁 + 1 before the crash                      breaks the commit-order assumption the frontier relies
or the crash occurred before transmission cannot be deduced                     on and can leave committed events below a frontier
from local state alone. If the sink accepted event 𝑁 + 1 im-                    unrecovered.
mediately before the crash, resending creates a duplicate.                   • The credential constraint. Production services provi-
If the crash occurred before transmission, skipping drops                       sioned with write-only permissions (such as Kafka
committed work.                                                                 produce rights without consume rights) silently de-
   This ambiguity is an information limit. A local check-                       grade an Archetype 2 sink into an Archetype 1 blind
point records the relay’s progress in persisting its own progress               sink.


                                                                    19
                          Table 2. Sink capability archetypes and corresponding recovery contracts.

Sink archetype            Examples                                Read and admission capability             Recovery contract
Blind or write-only       Basic HTTP webhooks, write-only         Cannot query past accepted events, with   No source-measured policy can
                          queues, legacy email APIs               no admission deduplication or fencing     guarantee exactly-once delivery at the
                                                                  tokens.                                   recovery frontier. The system must
                                                                                                            explicitly choose between duplicate
                                                                                                            retries or omission under ambiguity.
Queryable log or store    Kafka topic (with read ACLs),           Recovery can inspect sink history to      Compute difference between committed
                          replicated datastore table, queryable   determine which source events are         source log and sink records, and resend
                          event store                             missing, but the sink does not natively   only missing events (Theorem 4).
                                                                  deduplicate.                              Requires strictly ascending coordinates
                                                                                                            (P4) and generation fencing against
                                                                                                            stragglers and concurrent recoverers.
Deduplicating or fenced   Stripe API (idempotency keys), Kafka    Sink admission gate deduplicates by       Deduplicate by stable event key, or
                          transactional producer                  client-supplied key or rejects stale      compute missing events from
                          (transactional.id + epoch), cloud       producer epochs.                          authoritative acceptance records and use
                          queues with FIFO deduplication                                                    fenced recovery. Retain deduplication
                                                                                                            state throughout the recovery horizon.


    • Acceptance history versus current state. In a key-                   which the sink accepts. Moments later, the delayed packet
      value store, reading current state (such as status                   from Relay 1 arrives at the sink. If the sink lacks arrival fenc-
      = "shipped") distinguishes some crash states, but                    ing, it accepts the delayed request, causing a duplicate. Theo-
      fails if intermediate updates were overwritten. Re-                  rem 5 (Section 6) proves that no channel-blind policy reading
      covery requires a record of per-operation acceptance.                only durable state can detect in-flight stragglers. The proved
      Compaction that preserves key presence is safe (Sec-                 remedy is the atomic fenced re-drive (Theorem 6), where the
      tion 8), but presence-destroying retention (such as                  sink atomically accepts the recovery delta and advances its
      hard-deleting records or purging tombstones) destroys                generation threshold to one above the crashed run’s gener-
      queryable evidence. Sinks read from replicas must also               ation, rejecting older requests at admission. In this model,
      enforce strong read consistency to avoid replica lag                 recovery uses the crashed generation. Fencing first blocks
      hiding recent writes.                                                its requests, while fencing afterward leaves a window for
   Archetype 3: Deduplicating and fenced sinks. Stripe dedupli-            stragglers. Recovery with a new generation falls outside this
cates requests using client-supplied idempotency keys [12].                argument (Section 6). The cost of arrival fencing. While ar-
Kafka’s stable transactional.id supports transaction re-                   rival fencing guarantees exactness at the recovery frontier,
covery and fences old producers [11]. A relay can still resend             Corollary 6.1 proves that it can reject delayed requests that
an event already committed to Kafka. It must also commit                   carried work needed at subsequent frontiers, leaving that
its progress with the output or use the sink’s authoritative               subsequent work as a separate unfulfilled obligation.
acceptance record and the fencing rules below to send only                    Hazard 2: Concurrent recoverers. In containerized environ-
missing events. With permanent deduplication memory and                    ments, a recovery worker losing its heartbeat can cause an
strictly increasing coordinates, at-least-once delivery gives              orchestrator to launch a replacement worker. If both workers
exactly-once coverage (Theorem 9, Section 8). In practice,                 run concurrently, both query the sink, observe event 𝑁 + 1
finite memory requires a retention window long enough to                   missing, and fire re-drive batches. Distributed lock leases
cover replay. Derive idempotency keys from stable source co-               do not prevent this hazard [30]. If a worker pauses and its
ordinates and keep them unchanged across retries. Payload                  lease expires, a replacement worker claims leadership, but
hashes alone can merge distinct operations with identical                  the original worker can wake and fire its prepared network
contents and suppress required delivery.                                   call. Theorem 7 (Section 7) proves this Second-Recoverer
                                                                           Bound, establishing that without an admission fence, con-
   Controlling in-flight stragglers and concurrent re-                     current recoverers can duplicate deliveries or lose work. The
coverers. Even with queryable or deduplicating sinks, two                  proved mitigation is atomic claim fencing (Lemma 7.1 and
distinct distributed systems hazards can invalidate recovery.              Theorem 8), under which a recoverer atomically sets the
   Hazard 1: In-flight network stragglers. Suppose Relay 1                 sink fence to its own generation and arms its batch from
sends an event to a queryable sink, but crashes while the                  the sink record read under that claim. The fire step suc-
packet remains buffered in a retrying network proxy or trans-              ceeds at the sink only if the fence has not been advanced
port queue. A recovery worker restarts, queries the sink, ob-              past the worker’s generation. Theorem 8 requires window
serves that event 𝑁 + 1 is missing, and resends event 𝑁 + 1,               freshness (Condition C3, requiring that no source commit


                                                                      20
occurs within the recovery range between claim and fire)                       atomically with queue acceptance. Separate sender-
and validates generation authority at the sink admission gate                  side bookkeeping leaves the crash window open.
(Condition C4).                                                              • Source history retention. To maintain journal-grade ex-
   Fencing internal versus external SaaS sinks. Kafka enforces                 actness, upstream outbox records must be retained un-
epoch fencing natively at admission via transactional pro-                     til the downstream sink has durably confirmed their
ducer epochs. Relational datastores implement the fence as                     acceptance (Corollary 7.1). Prematurely truncating
a conditional generation check inside the same transaction                     source history removes the content needed to identify
that applies the re-drive batch. External SaaS APIs lacking                    which operations require delivery, leaving only coordi-
epoch endpoints (such as Stripe) cannot enforce claim fenc-                    nate bounds or metadata. With the historical content
ing directly. Source outbox leases reduce redundant calls                      lost, recovery is forced to choose between phantom
under normal operation, but cannot stop a resumed worker                       fabrication and abandonment (Theorem 10).
from firing. For external APIs, admission deduplication via
                                                                            Architecture checklist, auditing, and recovery tests.
deterministic idempotency keys is the sole barrier absorbing
                                                                         To translate these boundaries into practice, teams can apply
stragglers. As Section 7 notes, no theorem merges arrival
                                                                         the following checklist, monitoring strategy, and recovery
and claim fencing: they address distinct failure models on
                                                                         tests.
different machines.
                                                                            Architecture checklist.
   Retention horizons across deduplication caches and                        • Monotonic event coordinates. Assign stable event IDs
source logs. Deduplication state cannot be retained indefi-                     at source commit time strictly increasing in commit
nitely in real systems.                                                         order (such as a database WAL LSN or an outbox event
                                                                                coordinate assigned at commit). Auto-increment se-
    • Stripe’s documentation specifies that idempotency
                                                                                quence numbers generated at insert can commit out of
      keys become eligible for removal after at least 24
                                                                                order under concurrent transactions. Never generate
      hours [12].
                                                                                fresh random UUIDs during retries.
    • Apache Kafka’s producer ID expiration (producer.id.
                                                                             • Documented sink contracts. Explicitly classify each sink
      expiration.ms) defaults to 1 day [13], though topic
                                                                                as Blind, Queryable, or Deduplicating. For Blind sinks,
      log retention can cause earlier expiry.
                                                                                record the failure preference (duplicates versus omis-
    • Cloud FIFO queues configure sliding deduplication
                                                                                sions).
      windows (such as a 5-minute window from message
                                                                             • Arrival fencing for in-flight stragglers. For internal
      acceptance).
                                                                                sinks, ensure recovery atomically raises the genera-
    • Upstream database outbox tables undergo WAL or bin-
                                                                                tion fence upon re-drive, preventing delayed in-flight
      log purging.
                                                                                requests from prior runs from landing.
  Replay after retention expiry. If an upstream database un-                 • Claim fencing for concurrent recoverers. Ensure replace-
dergoes a prolonged outage or network partition and recov-                      ment recovery workers claim leadership and validate
ery replays historical events after the sink’s deduplication                    generation tokens at the sink admission gate before
cache has expired, the sink treats the replayed requests as                     firing batches.
novel transactions, triggering a wave of duplicate side effects.             • Verified read permissions. Ensure relay service ac-
  Sizing and retention guidance.                                                counts possess explicit read/consume permissions
    • Sink deduplication horizon. The theoretical model in                      where queryable recovery is assumed.
      Section 8 measures deduplication memory in entry-                      • Dead-letter queue trade-off. Routing unprocessable pay-
      count horizons. In practice, converting duration to en-                   loads to a Dead-Letter Queue (DLQ) prevents head-of-
      try capacity requires bounding the maximum arrival                        line blocking, but accepts a frontier omission. The rec-
      rate. The retention horizon must exceed the longest                       onciliation monitor must record these coordinates as
      anticipated recovery window: 𝑇dedup > 𝑇max_outage +                       acknowledged omissions (avoiding persistent alerts),
      𝑇operator_delay +𝑇replay_catchup + margin. If deduplication               and the DLQ write itself represents an auxiliary dual-
      evidence expires before replay finishes, the sink ad-                     write boundary.
      mits replayed events as novel (Section 8). When fixed                  • Outbox storage safeguards. Because outbox records
      provider windows (such as a 5-minute FIFO dedupli-                        must be retained until downstream confirmation
      cation window) cannot be widened, replays exceeding                       (Corollary 7.1), extended sink outages cause outbox
      the window cannot rely on the sink for deduplication.                     tables to accumulate rows. Implement threshold alerts
      If the queue cannot report past acceptances, recovery                     on row count and WAL utilization to prevent storage
      after expiry is blind, as in Archetype 1. An auxiliary                    exhaustion.
      record helps only if it is authoritative and updated                  Monitoring and reconciliation auditing across frontiers. De-
                                                                         livery failures are asymmetrical in production. Duplicate


                                                                    21
side effects are loud (prompting complaints or billing alerts),         other. We also proved this result for a deterministic deliver-
whereas omissions are silent (a skipped event can leave dash-           then-checkpoint protocol in which crash timing is the only
boards green). To detect silent omissions on Queryable or               nondeterminism.
Deduplicating sinks, implement an independent reconcilia-                  The positive results identify the controls required for exact
tion auditor, a background job querying the source database             recovery. An authoritative, complete, and current record of
for committed event coordinates and verifying their pres-               sink acceptance allows recovery to send only the committed
ence in the sink’s acceptance log between the last verified             operations the sink has not yet accepted. This works only
position and the latest completed frontier. Alert whenever a            if nothing changes the record between the read and the
committed obligation remains unaccepted past the SLA.                   re-send. For requests still in flight from the crashed run,
   Recovery tests. Dual-write and CDC pipelines should be               recovery uses an arrival fence. For overlapping recoverers,
verified in staging against failure scenarios tailored to sink          an atomic claim ties the read to the worker that made it, and
archetypes:                                                             the sink accepts the batch only while that claim is still the
                                                                        latest. These mechanisms solve distinct hazards on different
     • The checkpoint crash (all archetypes). Terminate the
                                                                        machines, with conditions and costs that form part of the
       relay immediately after the sink ingests a request but
                                                                        guarantee.
       before the local checkpoint commits. For Archetype 1
                                                                           The guarantee also depends on evidence retention. With
       (Blind), verify the system produces the configured com-
                                                                        permanent deduplication, every required payload appears
       promise (duplicate retry or skip). For Archetypes 2
                                                                        once in the deduplicated view exactly when each has been
       and 3, verify that restart does not create duplicate ef-
                                                                        delivered at least once. A finite deduplication window can
       fects.
                                                                        admit replays as new after identity expiry, and truncating
     • The in-flight straggler (Archetype 2). Inject artificial
                                                                        source history removes the information needed to identify
       latency on a delivery request, trigger a timeout and
                                                                        undelivered operations. Practical recovery must therefore
       recovery restart, let recovery complete, and then re-
                                                                        retain sink acceptance evidence and source history for the
       lease the delayed original request. Verify that the sink
                                                                        full recovery horizon.
       rejects the straggler at its generation fence.
                                                                           Transactional outboxes and change data capture remain
     • The split-brain worker (Archetypes 2 and 3). Pause an ac-
                                                                        the right tools for deriving downstream state from a com-
       tive recovery worker, allow a failover worker to claim
                                                                        mit log. At every recovery source-log position, downstream
       leadership and complete recovery, then resume the
                                                                        state must match the state obtained by replaying the com-
       original worker. Verify that the superseded worker’s
                                                                        mitted log to that position. This agreement is necessary and
       writes are rejected by the claim fence.
                                                                        sufficient for store-level crash safety under the model’s as-
     • The expired deduplication replay (Archetype 3). Fast-
                                                                        sumptions. The relay created by that design has its own
       forward cache expiry or flush the sink’s deduplication
                                                                        delivery boundary. Reviews of that boundary should iden-
       state, then trigger a manual replay of historical events.
                                                                        tify the sink’s durable acceptance event, active requests or
       Verify that operational safeguards reject blind replays
                                                                        recoverers, and retention horizons on both sides. A source
       across expired retention windows.
                                                                        checkpoint tracks progress, but cannot replace the sink’s
     • Crash inside fenced recovery. Inject a crash during re-
                                                                        acceptance record.
       covery re-drive. Because the model abstracts fenced
       re-drive as an atomic transition (Section 10), implemen-            AI assistance. Generative AI assistants Claude Fable 5
       tations execute distinct steps (reading accepted history,        (Anthropic) and ChatGPT 5.6 Sol (OpenAI) supported draft-
       submitting re-drive, and raising the fence). Verify that         ing, revision, and Isabelle/HOL formalization. The author
       a crash before fence advancement leaves the system               directed the research, verified all proofs and text, and takes
       recoverable without duplicate side effects.                      full responsibility for this work. The assistants are tools, not
                                                                        authors.
13     Conclusion
In this paper, we developed a machine-checked theory of                 References
recovery when a process delivers an effect to one system and             [1] Martin Kleppmann. Using logs to build a solid data infrastructure
records its progress in another. We proved that the durable                  (or: Why dual writes are a bad idea). Confluent Blog, https://www.
                                                                             confluent.io/blog/using-logs-to-build-a-solid-data-infrastructure-
state of the crashed side cannot decide whether a delivery
                                                                             or-why-dual-writes-are-a-bad-idea/, 2015.
should be repeated. Two reachable states can share identi-               [2] Martin Kleppmann. Designing Data-Intensive Applications: The Big
cal source databases, logs, control states, restart counters,                Ideas Behind Reliable, Scalable, and Maintainable Systems. O’Reilly
and checkpoints while differing in what the sink accepted.                   Media, 2017.
Any policy consulting only this shared state must duplicate              [3] Martin Kleppmann, Alastair R. Beresford, and Boerge Svingen.
                                                                             Online event processing. Communications of the ACM, 62(5):43–49,
an effect in one execution or omit committed work in the
                                                                             2019. doi: 10.1145/3312527.



                                                                   22
 [4] Tyler Treat. You cannot have exactly-once delivery. Brave New Geek             [19] Benjamin Bisping, Paul-David Brodmann, Tim Jungnickel, Christina
     blog, https://bravenewgeek.com/you-cannot-have-exactly-once-                        Rickmann, Henning Seidler, Anke Stüber, Arno Wilhelm-Weidner,
     delivery/, March 2015.                                                              Kirstin Peters, and Uwe Nestmann. A constructive proof for FLP.
 [5] Shabnam Ghasemirad, Si Liu, Christoph Sprenger, Luca Multazzu,                      Archive of Formal Proofs, https://www.isa-afp.org/entries/FLP.html,
     and David Basin. VerIso: Verifiable isolation guarantees for data-                  2016. Companion: Mechanical verification of a constructive proof for
     base transactions, 2025. URL https://arxiv.org/abs/2503.06284.                      FLP, ITP 2016, LNCS 9807, pages 107–122. https://doi.org/10.1007/
     arXiv:2503.06284.                                                                   978-3-319-43144-4_7.
 [6] Tej Chajed, Joseph Tassarotti, Mark Theng, Ralf Jung, M. Frans                 [20] Joseph M. Hellerstein and Peter Alvaro. Keeping CALM: When
     Kaashoek, and Nickolai Zeldovich. GoJournal: A verified, concurrent,                distributed consistency is easy. Communications of the ACM, 63(9):
     crash-safe journaling system. In 15th USENIX Symposium on Operat-                   72–81, 2020. doi: 10.1145/3369736.
     ing Systems Design and Implementation (OSDI 2021), pages 423–439,              [21] Seth Gilbert and Nancy Lynch. Brewer’s conjecture and the feasi-
     2021. URL https://www.usenix.org/conference/osdi21/presentation/                    bility of consistent, available, partition-tolerant web services. ACM
     chajed.                                                                             SIGACT News, 33(2):51–59, 2002. doi: 10.1145/564585.564601.
 [7] Tej Chajed, Joseph Tassarotti, M. Frans Kaashoek, and Nickolai                 [22] Cédric Auger, Zohir Bouzid, Pierre Courtieu, Sébastien Tixeuil,
     Zeldovich. Verifying concurrent, crash-safe systems with Perennial.                 and Xavier Urbain. Certified impossibility results for Byzantine-
     In Proceedings of the 27th Symposium on Operating Systems Principles                tolerant mobile robots. In Symposium on Stabilization, Safety,
     (SOSP 2019), pages 243–258, 2019. doi: 10.1145/3341301.3359632.                     and Security of Distributed Systems (SSS), volume 8255 of Lecture
 [8] Ilya Sergey, James R. Wilcox, and Zachary Tatlock. Programming                      Notes in Computer Science, pages 178–190. Springer, 2013. doi:
     and proving with distributed protocols. Proceedings of the ACM on                   10.1007/978-3-319-03089-0_13.
     Programming Languages, 2(POPL):28:1–28:30, 2018. doi: 10.1145/                 [23] Jim Gray. Notes on data base operating systems. In Operating Sys-
     3158116.                                                                            tems: An Advanced Course, volume 60 of Lecture Notes in Computer
 [9] Tomasz Masternak and Szymon Pobiega. Model checking exactly-                        Science, pages 393–481. Springer, 1978. doi: 10.1007/3-540-08755-9_9.
     once. Exactly Once blog. TLA+ models: https://github.com/exactly-              [24] James G. Mullen, Ahmed K. Elmagarmid, Won Kim, and Jamshid
     once/model-checking. Post: https://exactly-once.github.io/posts/                    Sharif-Askary. On the impossibility of atomic commitment in
     model-checking-exactly-once/, July 2020.                                            multidatabase systems. In Proceedings of the Second International
[10] Mohammad Roohitavaf, Kun Ren, Gene Zhang, and Sami Ben-                             Conference on Systems Integration (ICSI), pages 625–634. IEEE, 1992.
     Romdhane. LogPlayer: Fault-tolerant exactly-once delivery using                [25] Rachid Guerraoui. Revisiting the relationship between non-blocking
     gRPC asynchronous streaming, 2019. URL https://arxiv.org/abs/1911.                  atomic commitment and consensus. In Distributed Algorithms, 9th
     11286. arXiv:1911.11286.                                                            International Workshop (WDAG ’95), volume 972 of Lecture Notes
[11] Apache Kafka community. KIP-98: Exactly once delivery and                           in Computer Science, pages 87–100. Springer, 1995. doi: 10.1007/
     transactional messaging. Apache Kafka Improvement Proposals.                        BFb0022140.
     https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-                     [26] Dmitriy Traytel. Formalization of (conflict-)serializability and strict
     +Exactly+Once+Delivery+and+Transactional+Messaging, 2017.                           two-phase locking. Archive of Formal Proofs, https://www.isa-
[12] Stripe. Idempotent requests. Stripe API reference. https://docs.stripe.             afp.org/entries/Serializable.html, 2025.
     com/api/idempotent_requests, 2026. Accessed 9 September 2026.                  [27] Apache Flink documentation. TwoPhaseCommitSinkFunction.
[13] Apache Kafka documentation. Broker configuration                                    Flink 1.20 Javadoc. Deprecated in favour of the newer Sink
     producer.id.expiration.ms. https://kafka.apache.org/43/                             API. https://nightlies.apache.org/flink/flink-docs-release-
     configuration/broker-configs/#brokerconfigs_producer.id.expiration.                 1.20/api/java/org/apache/flink/streaming/api/functions/sink/
     ms, 2026. Default 86400000 ms. KIP-854: Separate configuration for                  TwoPhaseCommitSinkFunction.html, 2026. Accessed 9 Septem-
     producer ID expiry. Accessed 9 September 2026.                                      ber 2026.
[14] The Debezium project. Debezium: Change data capture for a variety              [28] Piotr Nowojski and Mike Winters. An overview of end-to-end
     of databases. https://debezium.io, 2026. Accessed 9 September 2026.                 exactly-once processing in Apache Flink (with Apache Kafka, too!).
[15] Tobias Nipkow, Lawrence C. Paulson, and Markus Wenzel. Is-                          Apache Flink blog, February 2018. URL https://flink.apache.org/
     abelle/HOL: A Proof Assistant for Higher-Order Logic, volume                        2018/02/28/an-overview-of-end-to-end-exactly-once-processing-in-
     2283 of Lecture Notes in Computer Science. Springer, 2002. doi:                     apache-flink-with-apache-kafka-too/.
     10.1007/3-540-45949-9.                                                         [29] Apache Kafka documentation. Kafka Streams core concepts: Process-
[16] Andreas Andreakis. A theoretical study of DBLog: Certified virtual                  ing guarantees. https://kafka.apache.org/43/streams/core-concepts/,
     cuts for a snapshot-equivalent replay of live databases, 2026. URL                  2026. processing.guarantee. KIP-129: Streams Exactly-Once
     https://arxiv.org/abs/2605.31475. arXiv:2605.31475. Formal develop-                 Semantics, 2017. Accessed 9 September 2026.
     ment archived on Zenodo, concept DOI 10.5281/zenodo.20389696                   [30] Martin Kleppmann. How to do distributed locking. https://martin.
     (version 2.1 at DOI 10.5281/zenodo.21732790).                                       kleppmann.com/2016/02/08/how-to-do-distributed-locking.html,
[17] Andreas Andreakis. Isabelle/HOL formal development for “Machine-                    February 2016.
     Checked Dual-Write Recovery from a Commit Log”, 2026. URL                      [31] Upamanyu Sharma, Ralf Jung, Joseph Tassarotti, M. Frans Kaashoek,
     https://doi.org/10.5281/zenodo.22700396. Version 1.0.1. Archival                    and Nickolai Zeldovich. Grove: A separation-logic library for
     deposit, Zenodo.                                                                    verifying distributed systems. In Proceedings of the 29th Symposium
[18] Michael J. Fischer, Nancy A. Lynch, and Michael S. Paterson. Impos-                 on Operating Systems Principles (SOSP 2023), pages 113–129, 2023. doi:
     sibility of distributed consensus with one faulty process. Journal of               10.1145/3600006.3613172.
     the ACM, 32(2):374–382, 1985. doi: 10.1145/3149.214121.




                                                                               23
