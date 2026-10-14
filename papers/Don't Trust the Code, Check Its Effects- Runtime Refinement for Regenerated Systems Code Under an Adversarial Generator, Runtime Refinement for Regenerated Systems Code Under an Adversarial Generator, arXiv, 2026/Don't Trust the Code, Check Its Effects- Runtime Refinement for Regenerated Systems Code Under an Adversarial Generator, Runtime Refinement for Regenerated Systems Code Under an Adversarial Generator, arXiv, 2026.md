                                                             Don’t Trust the Code, Check Its Effects
                                          Runtime Refinement for Regenerated Systems Code Under an Adversarial Generator
                                                           Jinhao Hu                                      Ashvin Goel                            Laurent Bindschaedler
                                              Max Planck Institute for Software                       University of Toronto                  Max Planck Institute for Software
                                                          Systems                                       Toronto, Canada                                  Systems
                                                  Saarbrücken, Germany                                                                           Saarbrücken, Germany

                                         Abstract                                                                      1   Generating Systems Components
                                         Recent work uses large language models to generate sys-                       A growing body of work uses large language models to re-
                                         tems code from specifications, treating the specification as                  generate systems code on demand, treating the specification,
arXiv:2609.00430v1 [cs.CR] 31 Aug 2026




                                         the durable artifact and the implementation as disposable.                    not the implementation, as the durable engineering arti-
                                         Regenerating the implementation specializes it to each work-                  fact [4, 5, 27, 30, 32, 42]. The pattern already spans the stack:
                                         load and device. However, that work lives in a forgiving                      file systems synthesized from specifications and checked
                                         setting: a component’s externally visible effects, its writes                 against specification-derived test suites [26], distributed pro-
                                         and device commands, are recoverable, and the generator                       tocols generated with mechanized proofs [2], and analyti-
                                         is honest, so trust is discharged by re-execution. We target                  cal database engines synthesized per workload for order-of-
                                         the unforgiving setting: systems code whose effects are ir-                   magnitude speedups [46]. A deployer curates a specification,
                                         reversible, produced by a generator that may be adversarial.                  a model emits a native implementation, and regenerates it
                                         There, re-execution cannot check an effect after the fact, and                rather than patching it when the specification changes or a
                                         a proof fails silently when its assumptions do. We take the                   defect surfaces. The specification is what humans maintain,
                                         position that the only safe way to operate here is to deny                    and the implementation is disposable.
                                         the generated code the authority to act. The generated code                      Regeneration buys specialization. Systems components
                                         only plans, while a fixed trusted mediator owns every effect                  must be tuned to hardware and workload, and a single imple-
                                         and performs one only when the specification would have                       mentation commits once to a large design space: a storage
                                         produced it. Because the guarantee lives in the mediator,                     engine’s layout, a network stack’s congestion control, a dri-
                                         not the code, it survives regeneration. We instantiate this                   ver’s queueing strategy. A model can search that space and
                                         as a reference monitor for regenerated device drivers, and                    re-search it per deployment. The deployer re-specializes by
                                         characterize the mediability envelope, six conditions on the                  regenerating, never by editing.
                                         effect vocabulary: legibility, spec-input observability, corre-                  These systems share a setting that makes them tractable:
                                         latability, completeness, outcome enumerability, and explicit                 their effects are recoverable, an analytical query can be re-
                                         durability. They decide when such mediation is possible.                      run, an engine re-benchmarked, a wrong output recomputed,
                                                                                                                       and their generators are treated as honest. Trust is there-
                                         Keywords: generated systems code, reference monitors, run-                    fore discharged by re-execution: validate the implementation
                                         time refinement, effect authority, device drivers                             against tests or a workload and regenerate on failure [26, 46].
                                                                                                                       This works precisely because every effect can be undone.
                                         ACM Reference Format:                                                            We target the unforgiving setting, where that assumption
                                         Jinhao Hu, Ashvin Goel, and Laurent Bindschaedler. 2026. Don’t                fails. Systems code produces irreversible, externally visible
                                         Trust the Code, Check Its Effects: Runtime Refinement for Regen-              effects, the operations through which it changes state outside
                                         erated Systems Code Under an Adversarial Generator. In Practical              itself, such as a device command, a packet send, or a disk
                                         Adoption Challenges of ML for Systems (PACMI ’26), September 29–              write. Once an effect reaches the host it cannot be recalled,
                                         October 2, 2026, Prague, Czech Republic. ACM, New York, NY, USA,              so re-execution cannot check it after the fact. And the gen-
                                         7 pages. https://doi.org/10.1145/3843967.3844678                              erator cannot be assumed honest: a compromised provider,
                                                                                                                       a poisoned training set, or prompt injection can emit an im-
                                                                                                                       plementation that issues an out-of-spec effect [8, 15]. Under
                                                                                                                       irreversible effects and an adversarial generator, validation
                                                                                                                       by re-execution is unavailable, and, as we argue next, so is
                                         This work is licensed under a Creative Commons Attribution 4.0 Interna-       verification alone.
                                         tional License.                                                                  A device driver is the sharpest instance, and our running
                                         PACMI ’26, Prague, Czech Republic                                             example. A model generates the native driver that turns ker-
                                         © 2026 Copyright held by the owner/author(s).                                 nel block requests into device commands, managing queues,
                                         ACM ISBN 979-8-4007-2998-0/26/09                                              DMA, and interrupts, and regenerates it per deployment.
                                         https://doi.org/10.1145/3843967.3844678
                                                                                                                   1
Drivers are a dominant share of kernel code and its faults,                 This is not a claim that verification cannot be safe; a stack
tuned across thousands of devices, and their most dangerous              verified down to a trusted machine model needs no mediator.
effect, a DMA into arbitrary host memory, is irreversible and            Under an adversarial generator, native code, and irreversible
unconfined by construction.                                              effects, though, verification’s preconditions are unmet, so the
                                                                         trusted decision must be made at the effect, not the artifact.
                                                                         Where achievable, verification raises availability by making
2    From Verification to Enforcement                                    proposals usually correct, but safety rests on enforcement.
Section 1 established the setting; we now pin the threat                    We make three contributions. We recast trust for regener-
model. We treat the generated component as Byzantine: it                 ated systems code as effect authority rather than code ver-
may compute arbitrarily, hide an out-of-spec effect behind a             ification: the code only plans, and a fixed mediator owns
branch no test exercises, and misreport anything it tells us.            and adjudicates every effect. We instantiate this as a refer-
Every value the code supplies is untrusted.                              ence monitor for regenerated drivers (Section 3), extending
   The natural response is to verify the code. Prove that the            driver-safety monitoring [47] to functional refinement. And
generated component refines its specification, admit it, and             we characterize the mediability envelope (Section 4): six con-
run it with authority over the device, as in proof-carrying              ditions on the effect vocabulary that decide when such media-
generation and admission-time regeneration [2, 3, 28, 48].               tion is possible. This is a position paper: no formal semantics,
Trust is discharged once, before running, as a property of               mechanized proof, implementation, or measurement.
the artifact.
   Verification alone does not survive this setting, because its         3   The Boundary, by Example
guarantee is conditional on assumptions the setting breaks. A            Figure 1 illustrates the boundary we call proposal-commit
proof yields safety only if the generator produces a checkable           separation: the driver proposes device commands, and the
proof for every regeneration, the host model it assumes is               mediator commits one only when it refines the specification.
complete and sound, the toolchain from proof to binary is
trusted, and the running bits are bound to the verified artifact.                                                     kernel block layer
An adversarial generator need not prove anything; a model of                                                      request              validated
                                                                                                       Dispatch                          result
real hardware is never complete; compilers and extraction are                  generated driverObserve, Propose mediator (trusted)
rarely verified; and regenerated native code is rarely bound                   untrusted, confined                   spec + abstract state
to a proof. Where any assumption breaks, the proof fails                        plans; cannot act
                                                                                                   Commit | Reject
                                                                                                                     sole effect authority
silently and the component commits an irreversible effect                                                        effect               completion
                                                                                                               primitives                (env.)
anyway. Verification establishes a property of a description;
what reaches the device is a property of the run, and under                                                         device (MMIO, DMA)
regeneration the two need not coincide.
                                                                         Figure 1. Proposal-commit boundary for a driver. The ker-
   Our position is different: trusting the code is not enough,
                                                                         nel’s request enters the mediator, which dispatches to the
so we deny the generated code the authority to act in the
                                                                         confined driver; the driver may only Observe and Propose.
first place. Safety then no longer depends on its correctness.
                                                                         The mediator alone holds the specification and effect primi-
The generated component becomes a planner that proposes
                                                                         tives (MMIO, DMA), committing only effects that refine it.
effects but performs none; a fixed, handwritten mediator
owns every effect primitive, the low-level operations through
                                                                             The specification. The mediator holds a specification of
which state leaves the machine, and performs one only after
                                                                         the driver’s interface, not of its implementation. Figure 2
checking, against the specification and its own state, that the
                                                                         gives the WRITE clause: a small, device-generic transition
effect is one the specification would produce. The guarantee
                                                                         relation over the outstanding requests and the queue state.
no longer rests on the code but on the mediator, which ob-
                                                                         It is a fraction of the driver’s queueing and DMA machinery,
serves the actual effect at the one point it can still be refused,
                                                                         so checking a command against it costs far less than produc-
from a bounded abstract state, not the device’s internals.
                                                                         ing one. Runtime values are taken from the request itself.
   This trades a verification toolchain for a mediator that
                                                                         req.lba names whatever the kernel asked for in the request
carries its own abstract state, its own account of what is
                                                                         now pending, and the mediator, which holds that request, re-
safe, and its own compiler. We do not claim that the trusted
                                                                         derives the value rather than taking the driver’s word for it.
base is smaller, and size is not the useful comparison. What
                                                                         The driver chooses only the queue slot, and the specification
separates them is the work a regeneration forces. A proof
                                                                         bounds that choice to the slots the driver observes free.
binds one binary, so every regenerated implementation must
earn its evidence again, from proof through extraction to                   The protocol. The driver never touches the device. The
binary. Our compiler checks the specification, which does                mediator Dispatches a pending request. While planning, the
not change when the implementation does, so a regenerated                driver must first Observe the abstract state the specification
driver re-runs nothing and gains no authority.                           permits it to see, the free queue slots and DMA grants of
                                                                     2
   operation WRITE(lba, len, buf) -- kernel's request                     Catching a wrong write. The kernel issues write
     observe queue.free, dma.grant[buf]                                LBA 100..107 from 𝐵; consider a driver that proposes
     permit   op = WRITE           -- fixed by request
                                                                       {op=WRITE, LBA=200, len=8, src=𝐵, slot=𝑘} instead
              lba = req.lba
              len = req.len                                            of the requested LBA 100: it overwrites the wrong block with
              dma = req.buf                                            𝐵’s contents, an effect no later regeneration can undo. Every
              slot in queue.free -- driver's choice                    other check passes: the DMA source is still the authorized
     outcome ok        -> req.done                                     buffer 𝐵, so an IOMMU, which never sees an LBA at all, has
              EIO      -> req.failed, device unchanged
                                                                       nothing to object to; 200 is a legal LBA, so a device-safety
              short(n) -> req.partial(n)
                                                                       monitor that never observes the kernel’s request, such as a
Figure 2. The WRITE clause of a driver specification. The              reference validation mechanism [47], has no requested value
mediator’s abstract state is the outstanding requests, the             to compare against; an LBA the test suite never exercised
queue’s free slots, and the DMA grants. permit separates               would pass sampled admission validation [26] just the same.
the fields the specification fixes from the pending request,           Only a check that holds the pending request and compares
which the mediator re-derives, from the one field the driver           it against the proposed command catches this: the media-
is free to choose. outcome enumerates what the primitive               tor’s Validate rejects it before the doorbell rings, because
may return and the abstract-state transition each produces.            100 ≠ 200, and nothing is written to the device. This same
                                                                       comparison covers the rest of the proposal. A wrong len, or
Figure 2; it may observe again before proposing. Observe               a DMA source other than 𝐵, fails identically, since Figure 2
returns state, never authority, together with a fresh sealed           fixes both to the request. A slot outside the observed free
token, a value the driver cannot forge, binding the request, the       set fails instead against the permitted set, and a proposal
versions of the abstract state that were read, and an expiry.          naming no pending request is rejected at the token. Every
The driver necessarily plans against a snapshot, and that              Propose carries the token from its most recent Observe,
snapshot may move before it proposes; the mediator rechecks            and Validate consumes it, so a request in flight yields at
the token during Validate, under the commit lock. A later              most one effect, however often the driver replans, and a
observation invalidates the preceding token, so a proposal             driver that proposes nothing stays silent. Absent a crash,
always describes a plan against one identified observation.            one request never yields a second effect.
   Propose is the driver’s only message that asks the medi-
ator to perform an effect. It submits an attempted effect, a              Confinement and ownership. The driver runs with no
device command, and nothing more, together with its token.             direct kernel access, no device register mapping, and no DMA
Every field of the proposal is an untrusted witness. The dri-          authority; the mediator is its only outward channel. Confine-
ver says nothing about what the effect will return, because            ment blocks any effect the driver might attempt on its own,
the specification has already said it: Figure 2 closes the out-        rather than relying on inspect-and-continue seccomp notifi-
come set at three entries for WRITE and pairs each one with            cation, which is unsafe against concurrently mutated argu-
its abstract-state transition. Once the primitive has run, the         ments [21]. The mediator owns the trusted effect primitives,
mediator therefore needs nothing further from the driver.              observation-token issuance, DMA authorization through the
   The mediator runs Validate under a commit lock, and                 IOMMU, the abstract state of Figure 2 and the commits that
rejects a replayed, expired, superseded, or stale token. It then       advance it, the append-only log in which each committed
checks that every field the specification fixes matches what it        effect is recorded together with the outcome it produced,
re-derives from the pending request, which it holds itself and         and the specification interpreter. It is the authority for the
never reads from the proposal, and that each freely chosen             declared effect vocabulary.
field falls inside the permitted set. Validate consumes the              Concurrency. Drivers may plan and compute concur-
token whether it accepts or rejects the proposal: one request          rently, but the mediator serializes the parts that matter: vali-
cannot produce a second effect by replaying a token.                   dation, primitive invocation, abstract-state update, and log
   Only then does the mediator Commit. It invokes the trusted          insertion run under a single commit lock, tokens are revali-
primitive and reads the actual outcome, which Figure 1                 dated after the lock is taken, and a stale proposal is rejected
shows returning as completion. The specification, not the              and replanned. The commit-log order is the specification’s
driver, says which transition that outcome produces, and the           serialization order. Serializing primitives does not make a
mediator records it and delivers the validated result to the           multi-primitive guest operation atomic; an operation that
kernel. A device error that the specification lists, such as the       needs cross-effect atomicity requires one atomic primitive,
EIO of Figure 2, is a committed outcome rather than a failure          substrate locking, or exclusion from the vocabulary.
of mediation. The mediator records req.failed and reports
the error upward. When Validate fails instead, it Rejects                 Guarantee. A realization should claim committed-trace
before any irreversible primitive runs, so a rejected proposal         safety: every committed sequence of externally visible ef-
is externally silent.                                                  fects is a prefix of a trace the specification allows over the
                                                                   3
declared effect vocabulary. It presupposes that the effect vo-               Correlatability. Effects must group into per-operation
cabulary lies within the mediability envelope (Section 4),                transactions with a recoverable order under concurrency.
and it is conditional on a correct specification and inter-               At the specification’s altitude a device command is self-
preter, complete mediation with no bypass, trusted effect                 delimiting, so grouping is free: one proposal, one transaction,
primitives, serialized commits, outcome enumerability, and                serialized at commit. Figure 2’s WRITE is exactly this. Block
a stated crash model. The guarantee excludes liveness and                 writes are not: concurrent operations interleave unlabeled
availability, since a Byzantine driver may propose nothing                writes over shared structures, so they cannot be grouped by
or select the worst permitted proposal, and it does not cover             address, and no serialization recovers an identity the vocab-
timing channels or defects in the specification itself.                   ulary never carried. Even where effects self-delimit, physical
                                                                          write order can diverge from commit order, and only the com-
4    The Mediability Envelope                                             mit lock recovers it. Certifying a stream that fails either half
A specification is written against an interface: it names that            means modeling the component’s own concurrency control.
interface’s operations, such as mkdir(path,mode) or write
LBA 100..107, and the objects those operations touch, such                   What the deployment must supply. Completeness. With
as paths, credentials, queue slots, and DMA buffers. We call              intent legible, the record of what changed must be kept
that interface’s level of abstraction the specification’s altitude.       sound: every externally visible state change must cross the
The architecture works only where the effect vocabulary lets              boundary, as a validated effect primitive or a mediator-owned
the mediator see and check the right thing cheaply, at that               environment transition; any third path voids the guarantee.
altitude, without becoming the code it checks. Refinement                 The standing risk is effect authority the component already
is a relation over what the mediator must observe and hold                holds: a writable shared mapping or DMA lets it change
against the specification across the life of a request: the intent        host-visible state before any proposal. Both must be excluded
(the requested operation), the delta (what actually changed),             or reified into proposals, shared memory through shadow
the result (what the caller is told), and, over time, whether             pages, DMA through IOMMU-authorized buffers. Figure 2’s
what was recorded survives a crash. Whether a vocabulary                  dma.grant[buf] is exactly this reification, checked before
supplies these, cheaply and independently, defines a medi-                any WRITE is permitted, not assumed.
ability envelope. Six conditions delimit it, and they are of                 Outcome enumerability. The record must also be trustwor-
two kinds. The first three ask what the effect vocabulary                 thy on the way out: the outcomes a primitive may produce,
supplies, and altitude settles them, so they decide whether a             as reported at the mediator’s interface, must be closed and
domain can be mediated at all. The last three ask what the                enumerable, so that whatever it returns, success, a device
deployment supplies, and engineering settles them at any                  error, or a partial completion, can be classified against the
altitude. We read each condition against two vocabularies:                specification’s allowed set the moment it returns, before any
the driver’s device commands, which satisfy it, and a file                abstract state is advanced, as Figure 2’s three-entry outcome
system’s block writes, which serve as a foil for what failure             clause does for WRITE. The mediator needs no model of why
looks like. Where a condition fails, the mediator can regain              the device produced an outcome, only an enumeration of the
it only by reconstructing what the vocabulary discarded.                  forms it can take; an unenumerable outcome space forces
                                                                          the mediator to guess at commit time what an incomplete
   What the vocabulary must supply. Legibility. A single                  device model forces a prover to guess at admission time.
effect must be legible, on its own, as an instance of one                    Explicit durability. Persistence extends the same concern
operation: from the effect alone, without replaying what                  into time: whether what the record says happened still holds
came before, the mediator must be able to tell which oper-                after a crash. Figure 2’s WRITE illustrates the gap: its ok out-
ation it belongs to. A device command names its operation:                come means the bytes reached the device, not that they
Figure 2’s WRITE is legible on its own, distinguishable from a            survive a crash. Durability must be a first-class effect the
READ by its own encoding. A block write does not: the same                component proposes, a flush or barrier, not a property that
write to a directory block and a bitmap could be a mkdir,                 emerges from write ordering, since a crash truncates the
an rmdir, a rename, or a corruption, so whether an opera-                 stream at an arbitrary point while destroying volatile state.
tion changed state, changed nothing, or did the opposite is               If it is explicit, the mediator checks that a claimed-durable
invisible. Ambiguity denies the mediator the intent.                      WRITE issued a following flush the device confirmed; if im-
   Spec-input observability. The mediator must observe ev-                plicit, the mediator must reconstruct the component’s barrier
ery input the transition reads. Figure 2’s WRITE observes                 discipline and keep its own crash-consistent store.
dma.grant[buf], the caller’s own authorized source buffer,                   One condition straddles the split. Correlatability’s group-
before permitting a slot; mkdir similarly is licensed only                ing half belongs to the vocabulary, but its ordering half is
against the caller’s credentials, but the virtual-filesystem in-          closed only by the commit lock. So the rule narrows: mediate
terface carries them while the block layer strips them, so a              at the specification’s own interface, never below it, and treat
permission-dependent transition cannot be checked there.                  confinement, serialization, outcome closure, and durability
                                                                      4
as separate engineering. Below that altitude the mediator             and atomicity invariants over block writes [11, 12], but below
must lift effects back to operations, re-implementing the read        the specification’s altitude, reading only metadata and never
path, concurrency control, and recovery, and re-attaching             the caller’s request, so they catch structural corruption, not
the intent and authority the vocabulary discarded.                    permitted-but-wrong outcomes. Concurrent work mediates
   Within the envelope, a separate question is economic: how          LLM agents at the tool boundary [8, 10, 17, 18, 31, 33, 38],
much standing state a check must consult. A driver sits at the        but assumes an honest generator and acts above regenerated
cheap end (queue descriptors, DMA grants); a file system at           native systems code. Our companion workshop papers place
the virtual-filesystem interface sits at the costly end, owning       a mediation boundary around agent explorations [19] and
the namespace and per-file digests while the component                price fleets’ residual risk [29], but target agent workloads,
owns the physical data plane; arbitrary specialization or             not regenerated systems code.
bugs then degrade availability, not silently corrupt data. At                                    Permission                 Correctness
the block layer the same system falls out of the envelope:                                       (effect is allowed)        (effect refines the spec)

legibility, spec-input observability, and correlatability fail.           At admission           static allowlists; the eBPF proof-bearing generation
                                                                          per artifact; redone   verifier                    (PCC, Verus, IDS); admission
Altitude is the line between checking and re-implementing.                on regeneration                                    validation (SYSSPEC)
                                                                          At commit              policy substrates (NaCl, runtime refinement (this
                                                                          per effect; survives   gVisor, WASI, seccomp); paper)
                                                                          regeneration           device-safety monitors
5   Related Work                                                                                 (RVM)
The approaches we reject have deep lineages. Table 1 or-              Table 1. Design space for trusting regenerated systems code.
ganizes the design space along two questions: when the                Admission-time checks are redone on regeneration; commit-
check runs, at admission or at commit, and what it checks,            time checks survive in the mediator. This paper claims the
permission or correctness. Proof certifies the artifact at            fourth cell.
admission, before it runs, from proof-carrying code [34] to
verified systems [22, 23] and provers aimed at generated
code [2, 3, 28, 48]. The proof is re-earned for every regenera-       6     What a Realization Must Answer
tion. Policy withholds effect authority and asks only whether         A realization must answer four engineering questions be-
an effect is permitted: the eBPF verifier [14] checks at admis-       yond mediability. Cost: how large is the mediator’s trusted
sion, while software fault isolation [43] and NaCl [49] check         code and abstract state against the component it guards,
at commit. Policy substrates such as [1, 44, 50] can also             what latency does serialized commit add, and how often do
interpose at that point, but typically decide whether a prim-         proposals go stale? If the mediator grows with the imple-
itive, fd, address, or DMA buffer is authorized, not whether          mentation, the envelope was drawn at the wrong altitude.
it refines the current trusted request and contract state; a          Whether drivers clear that bar is a fair doubt: the per-effect
policy that retains and checks the specification’s transition         check is cheap only because the driver’s abstract state stays
relation there is already a mediator in this paper’s sense.           small, and thin margins argue for regenerating device by
   Our mediator composes established mechanisms: con-                 device. Adapter trust: each effect primitive reaches the device
fined code that delegates to a trusted agent [13, 21], opaque         through an adapter, the trusted code that turns a validated
handles from capability systems [16, 41, 45], speculate-and-          command into the register writes and DMA descriptors the
commit from system transactions [20, 37], and behavioral-             hardware expects. Is each adapter mechanically verified,
model checking from model-carrying code [40], edit au-                audited against a contract, or excluded from the trusted
tomata [25, 39], and shield synthesis [6]. Runtime verifica-          base? Availability: a Byzantine component can propose noth-
tion compiles specifications into monitors that run alongside         ing, stall with fresh observations, or exhaust its permitted
the program [7, 24], and runtime refinement checking is two           choices, so a deployment needs a deadline, budgets, or a fall-
decades old [9], but both observe a trace rather than gating          back. Unknown unknowns: a specification defect is enforced
it. Output-buffering speculation defers an external effect            faithfully, and an unenumerated outcome breaks outcome
until it is known safe [35, 36], but it presumes a recoverable        enumerability, so a realization must fail stop on both.
substitute stands in for the effect; it cannot withdraw a                Regenerated systems code needs a trust boundary that
command the device has already run.                                   survives regeneration. Denying it effect authority and medi-
   The closest work is driver safety through a reference val-         ating each effect provides one, and the envelope says when:
idation mechanism [47]: untrusted, restartable native dri-            this paper isolates the laws a regenerable OS builds on.
vers, each interaction checked at commit by a specification-
compiled monitor that survives replacement. That monitor              Acknowledgments
enforces a device-safety automaton; ours checks functional            We thank the PACMI ’26 reviewers for their comments. We
refinement against a generator that rewrites the driver on de-        used AI tools for editorial assistance (drafting, copy-editing,
mand. Runtime checking of file-system metadata at commit              and trimming for length); all technical content, results, and
is a similar line: Recon and its successor check consistency          conclusions are our own.
                                                                  5
References                                                                              Extensions. In Proceedings of the 40th ACM SIGPLAN Conference on Pro-
 [1] Alexandru Agache, Marc Brooker, Andreea Florescu, Alexandra Ior-                   gramming Language Design and Implementation (PLDI ’19). Association
     dache, Anthony Liguori, Rolf Neugebauer, Phil Piwonka, and Diana-                  for Computing Machinery, 1069–1084. doi:10.1145/3314221.3314590
     Maria Popa. 2020. Firecracker: Lightweight Virtualization for Server-         [15] Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres,
     less Applications. In Proceedings of the 17th USENIX Symposium on                  Thorsten Holz, and Mario Fritz. 2023. Not What You’ve Signed Up For:
     Networked Systems Design and Implementation (NSDI ’20). USENIX                     Compromising Real-World LLM-Integrated Applications with Indirect
     Association, 419–434.                                                              Prompt Injection. In Proceedings of the 16th ACM Workshop on Artifi-
 [2] Shubham Agarwal, Alexander Krentsel, Shu Liu, Mert Cemri, Audrey                   cial Intelligence and Security (AISec ’23). Association for Computing
     Cheng, Rui Meng, Tomas Pfister, Chun-Liang Li, Sylvia Ratnasamy,                   Machinery, 79–90. doi:10.1145/3605764.3623985
     Aditya Parameswaran, Matei Zaharia, Ion Stoica, and Mohsen Lesani.            [16] Norman Hardy. 1985. KeyKOS Architecture. ACM SIGOPS Operating
     2026. Inductive Deductive Synthesis: Enabling AI to Generate Formally              Systems Review 19, 4 (1985), 8–25. doi:10.1145/858336.858337
     Verified Systems. CoRR abs/2605.23109 (2026). arXiv:2605.23109 [cs.AI]        [17] Jun He and Deying Yu. 2026. Protocol-Driven Development: Governing
     doi:10.48550/arXiv.2605.23109                                                      Generated Software Through Invariants and Continuous Evidence.
 [3] Pranjal Aggarwal, Bryan Parno, and Sean Welleck. 2025. AlphaVerus:                 CoRR abs/2605.12981 (2026). arXiv:2605.12981 [cs.SE] doi:10.48550/
     Bootstrapping Formally Verified Code Generation through Self-                      arXiv.2605.12981
     Improving Translation and Treefinement. In Proceedings of the 42nd            [18] Jun He and Deying Yu. 2026. Sovereign Assurance Boundary:
     International Conference on Machine Learning (ICML ’25) (Proceedings               Certificate-Bound Admission for Agentic Infrastructure. CoRR
     of Machine Learning Research, Vol. 267). PMLR, 587–615.                            abs/2606.11632 (2026). arXiv:2606.11632 [cs.CR] doi:10.48550/arXiv.
 [4] Thomas Anderson, Ratul Mahajan, Simon Peter, and Luke Zettlemoyer.                 2606.11632
     2025. Self-Defining Systems. White paper. Paul G. Allen School of             [19] Jinhao Hu, Bardia Mohammadi, Ashvin Goel, and Laurent Bind-
     Computer Science & Engineering, University of Washington. https:                   schaedler. 2026. Externalization Barriers: An OS Abstraction for Un-
     //self-defining-systems.cs.washington.edu/papers/sds.pdf                           trusted Agent Exploration. The 2nd Workshop on Operating Systems
 [5] Laurent Bindschaedler. 2026. ForkOps: Operating Fleets of Generated                Design for AI Agents (AgenticOS ’26). https://os-for-agent.github.io
     Software Variants. In Proceedings of the 2nd International Workshop on             29 September 2026, Prague, Czechia; co-located with SOSP 2026.
     Software Genomics (SWGeno ’26). Munich, Germany. Co-located with              [20] Suman Jana, Donald E. Porter, and Vitaly Shmatikov. 2011. TxBox:
     ASE 2026.                                                                          Building Secure, Efficient Sandboxes with System Transactions. In 2011
 [6] Roderick Bloem, Bettina Könighofer, Robert Könighofer, and Chao                    IEEE Symposium on Security and Privacy (S&P ’11). IEEE Computer
     Wang. 2015. Shield Synthesis: Runtime Enforcement for Reactive                     Society, 329–344. doi:10.1109/SP.2011.33
     Systems. In Proceedings of the 21st International Conference on Tools         [21] Michael Kerrisk. 2026. seccomp_unotify(2) — Linux manual page
     and Algorithms for the Construction and Analysis of Systems (TACAS                 (6.18 ed.). Linux man-pages project. https://man7.org/linux/man-
     ’15) (Lecture Notes in Computer Science, Vol. 9035). Springer, 533–548.            pages/man2/seccomp_unotify.2.html
     doi:10.1007/978-3-662-46681-0_51                                              [22] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick,
 [7] Feng Chen and Grigore Roşu. 2007. MOP: An Efficient and Generic                    David Cock, Philip Derrin, Dhammika Elkaduwe, Kai Engelhardt, Rafal
     Runtime Verification Framework. In Proceedings of the 22nd ACM SIG-                Kolanski, Michael Norrish, Thomas Sewell, Harvey Tuch, and Simon
     PLAN Conference on Object-Oriented Programming Systems, Languages,                 Winwood. 2009. seL4: Formal Verification of an OS Kernel. In Pro-
     and Applications (OOPSLA ’07). Association for Computing Machinery,                ceedings of the ACM SIGOPS 22nd Symposium on Operating Systems
     569–588. doi:10.1145/1297027.1297069                                               Principles (SOSP ’09). Association for Computing Machinery, 207–220.
 [8] Zheng Chen, Hanqing Liu, Duling Xu, Dong Dong, Jialin Li,                          doi:10.1145/1629575.1629596
     Bangzheng Pu, and Jidong Zhai. 2026. Cordon: Semantic Trans-                  [23] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha
     actions for Tool-Using LLM Agents. CoRR abs/2606.17573 (2026).                     Subasinghe, Yi Zhou, Jon Howell, Bryan Parno, and Chris Hawblitzel.
     arXiv:2606.17573 [cs.OS] doi:10.48550/arXiv.2606.17573                             2023. Verus: Verifying Rust Programs using Linear Ghost Types. Pro-
 [9] Tayfun Elmas, Serdar Tasiran, and Shaz Qadeer. 2005. VYRD: VerifY-                 ceedings of the ACM on Programming Languages 7, OOPSLA1, Article
     ing Concurrent Programs by Runtime Refinement-Violation Detection.                 85 (2023), 30 pages. doi:10.1145/3586037
     In Proceedings of the 2005 ACM SIGPLAN Conference on Programming              [24] Martin Leucker and Christian Schallhart. 2009. A Brief Account of
     Language Design and Implementation (PLDI ’05). Association for Com-                Runtime Verification. The Journal of Logic and Algebraic Programming
     puting Machinery, 27–37. doi:10.1145/1065010.1065015                               78, 5 (2009), 293–303. doi:10.1016/j.jlap.2008.08.004
[10] Marcelo Fernandez. 2026.           Agent Control Protocol: Admis-             [25] Jay Ligatti, Lujo Bauer, and David Walker. 2005. Edit Automata: En-
     sion Control for Agent Actions. CoRR abs/2603.18829 (2026).                        forcement Mechanisms for Run-Time Security Policies. International
     arXiv:2603.18829 [cs.CR] doi:10.5281/zenodo.19672575                               Journal of Information Security 4, 1–2 (2005), 2–16. doi:10.1007/s10207-
[11] Daniel Fryer, Mike Qin, Jack Sun, Kah Wai Lee, Angela Demke Brown,                 004-0046-8
     and Ashvin Goel. 2014. Checking the Integrity of Transactional Mech-          [26] Qingyuan Liu, Mo Zou, Hengbin Zhang, Dong Du, Yubin Xia, and
     anisms. ACM Transactions on Storage 10, 4, Article 17 (2014), 23 pages.            Haibo Chen. 2026. Sharpen the Spec, Cut the Code: A Case for Gen-
     doi:10.1145/2675113                                                                erative File System with SYSSPEC. In Proceedings of the 24th USENIX
[12] Daniel Fryer, Kuei Sun, Rahat Mahmood, Tinghao Cheng, Shaun Ben-                   Conference on File and Storage Technologies (FAST ’26). USENIX Associ-
     jamin, Ashvin Goel, and Angela Demke Brown. 2012. Recon: Verifying                 ation, 291–311.
     File System Consistency at Runtime. ACM Transactions on Storage 8,            [27] Shu Liu, Alexander Krentsel, Shubham Agarwal, Mert Cemri, Ziming
     4, Article 15 (2012), 29 pages. doi:10.1145/2385603.2385608                        Mao, Soujanya Ponnapalli, Alexandros G. Dimakis, Sylvia Ratnasamy,
[13] Tal Garfinkel, Ben Pfaff, and Mendel Rosenblum. 2004. Ostia: A Delegat-            Matei Zaharia, Aditya Parameswaran, and Ion Stoica. 2026. The Time
     ing Architecture for Secure System Call Interposition. In Proceedings              is Here for Just-in-Time Systems: Challenges and Opportunities. CoRR
     of the 11th Annual Network and Distributed System Security Symposium               abs/2605.24096 (2026). arXiv:2605.24096 [cs.DB] doi:10.48550/arXiv.
     (NDSS ’04). Internet Society, 187–201.                                             2605.24096
[14] Elazar Gershuni, Nadav Amit, Arie Gurfinkel, Nina Narodytska,                 [28] Yuwei Liu, Xinyi Wan, Yanhao Wang, Minghua Wang, Lin Huang,
     Jorge A. Navas, Noam Rinetzky, Leonid Ryzhyk, and Mooly Sagiv.                     and Tao Wei. 2026. KVerus: Scalable and Resilient Formal Verifica-
     2019. Simple and Precise Static Analysis of Untrusted Linux Kernel                 tion Proof Generation for Rust Code. CoRR abs/2605.03822 (2026).
                                                                                        arXiv:2605.03822 [cs.SE] doi:10.48550/arXiv.2605.03822
                                                                               6
[29] Bardia Mohammadi and Laurent Bindschaedler. 2026. The Irreversibil-             [41] Jonathan S. Shapiro, Jonathan M. Smith, and David J. Farber. 1999.
     ity Budget: Fleet-Level Risk Accounting and Admission Control for                    EROS: a fast capability system. In Proceedings of the 17th ACM Sym-
     Agent Operating Systems. The 2nd Workshop on Operating Systems                       posium on Operating Systems Principles (SOSP ’99). Association for
     Design for AI Agents (AgenticOS ’26). https://os-for-agent.github.io                 Computing Machinery, 170–185. doi:10.1145/319151.319163
     29 September 2026, Prague, Czechia; co-located with SOSP 2026.                  [42] Ion Stoica, Matei Zaharia, Joseph Gonzalez, Ken Goldberg, Koushik
[30] Bardia Mohammadi, Lars Klein, Aman Chadha, Akhil Arora, and Lau-                     Sen, Hao Zhang, Anastasios N. Angelopoulos, Shishir G. Patil, Lingjiao
     rent Bindschaedler. 2026. The Working Set of a Coding Agent: Co-                     Chen, Wei-Lin Chiang, and Jared Q. Davis. 2024. Specifications: The
     herence Debt in Repository-Scale Tasks. CoRR abs/2608.16630 (2026).                  missing link to making the development of LLM systems an engineer-
     arXiv:2608.16630 [cs.SE] doi:10.48550/arXiv.2608.16630                               ing discipline. CoRR abs/2412.05299 (2024). arXiv:2412.05299 [cs.SE]
[31] Bardia Mohammadi, Nearchos Potamitis, Lars Klein, Akhil Arora, and                   doi:10.48550/arXiv.2412.05299
     Laurent Bindschaedler. 2026. Atomix: Timely, Transactional Tool                 [43] Robert Wahbe, Steven Lucco, Thomas E. Anderson, and Susan L.
     Use for Reliable Agentic Workflows. In Agents in the Wild: Safety,                   Graham. 1993. Efficient Software-Based Fault Isolation. In Pro-
     Security, and Beyond at ICLR 2026. arXiv:2602.14849 [cs.LG] https:                   ceedings of the 14th ACM Symposium on Operating Systems Prin-
     //openreview.net/forum?id=UeRbEpSVUz                                                 ciples (SOSP ’93). Association for Computing Machinery, 203–216.
[32] Martin Monperrus. 2026. Bootstrapping Coding Agents: The Specifi-                    doi:10.1145/168619.168635
     cation Is the Program. IEEE Software 43, 4 (2026), 19–22. doi:10.1109/          [44] WASI Subgroup. 2026. WASI 0.3.0. https://github.com/WebAssembly/
     MS.2026.3687051                                                                      WASI/releases/tag/v0.3.0 Ratified standards-track release, 11 June
[33] Royce Moon and Lav R. Varshney. 2026. Containment Verification: AI                   2026.
     Safety Guarantees Independent of Alignment. In Second Workshop on               [45] Robert N. M. Watson, Jonathan Anderson, Ben Laurie, and Kris Kenn-
     Agents in the Wild: Safety, Security, and Beyond at ICML 2026. OpenRe-               away. 2010. Capsicum: Practical Capabilities for UNIX. In Proceedings
     view.net. https://openreview.net/forum?id=NGNK03iIam                                 of the 19th USENIX Security Symposium (USENIX Security ’10). USENIX
[34] George C. Necula. 1997. Proof-Carrying Code. In Proceedings of the                   Association, 29–46.
     24th ACM SIGPLAN-SIGACT Symposium on Principles of Programming                  [46] Johannes Wehrstein, Timo Eckmann, Matthias Jasny, and Carsten
     Languages (POPL ’97). Association for Computing Machinery, 106–119.                  Binnig. 2026. Bespoke OLAP: Synthesizing Workload-Specific One-
     doi:10.1145/263699.263712                                                            size-fits-one Database Engines. Proceedings of the VLDB Endowment
[35] Edmund B. Nightingale, Peter M. Chen, and Jason Flinn. 2005. Specu-                  19, 11 (2026), 3759–3771. doi:10.14778/3836663.3836723
     lative Execution in a Distributed File System. In Proceedings of the 20th       [47] Dan Williams, Patrick Reynolds, Kevin Walsh, Emin Gün Sirer, and
     ACM Symposium on Operating Systems Principles (SOSP ’05). Associa-                   Fred B. Schneider. 2008. Device Driver Safety Through a Reference
     tion for Computing Machinery, 191–205. doi:10.1145/1095810.1095829                   Validation Mechanism. In Proceedings of the 8th USENIX Symposium
[36] Edmund B. Nightingale, Kaushik Veeraraghavan, Peter M. Chen, and                     on Operating Systems Design and Implementation (OSDI ’08). USENIX
     Jason Flinn. 2006. Rethink the Sync. In Proceedings of the 7th USENIX                Association, 241–254.
     Symposium on Operating Systems Design and Implementation (OSDI                  [48] Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Jianan Yao, Wei-
     ’06). USENIX Association, 1–14.                                                      dong Cui, Yeyun Gong, Chris Hawblitzel, Shuvendu Lahiri, Jacob R.
[37] Donald E. Porter, Owen S. Hofmann, Christopher J. Rossbach, Alexan-                  Lorch, Shuai Lu, Fan Yang, Ziqiao Zhou, and Shan Lu. 2025. AutoVerus:
     der Benn, and Emmett Witchel. 2009. Operating System Transac-                        Automated Proof Generation for Rust Code. Proceedings of the ACM
     tions. In Proceedings of the ACM SIGOPS 22nd Symposium on Operating                  on Programming Languages 9, OOPSLA2, Article 396 (2025), 29 pages.
     Systems Principles (SOSP ’09). Association for Computing Machinery,                  doi:10.1145/3763174
     161–176. doi:10.1145/1629575.1629591                                            [49] Bennet Yee, David Sehr, Gregory Dardyk, J. Bradley Chen, Robert Muth,
[38] Igor Santos-Grueiro. 2026. Lingering Authority: Revocable Resource-                  Tavis Ormandy, Shiki Okasaka, Neha Narula, and Nicholas Fullagar.
     and-Effect Capabilities for Coding Agents. CoRR abs/2606.22504 (2026).               2009. Native Client: A Sandbox for Portable, Untrusted x86 Native
     arXiv:2606.22504 [cs.CR] doi:10.48550/arXiv.2606.22504                               Code. In 2009 30th IEEE Symposium on Security and Privacy (S&P ’09).
[39] Fred B. Schneider. 2000. Enforceable Security Policies. ACM Trans-                   IEEE Computer Society, 79–93. doi:10.1109/SP.2009.25
     actions on Information and System Security 3, 1 (2000), 30–50. doi:10.          [50] Ethan G. Young, Pengfei Zhu, Tyler Caraza-Harter, Andrea C. Arpaci-
     1145/353323.353382                                                                   Dusseau, and Remzi H. Arpaci-Dusseau. 2019. The True Cost of Con-
[40] R. Sekar, V. N. Venkatakrishnan, Samik Basu, Sandeep Bhatkar, and                    taining: A gVisor Case Study. In Proceedings of the 11th USENIX Work-
     Daniel C. DuVarney. 2003. Model-Carrying Code: A Practical Approach                  shop on Hot Topics in Cloud Computing (HotCloud ’19). USENIX Asso-
     for Safe Execution of Untrusted Applications. In Proceedings of the                  ciation. https://www.usenix.org/conference/hotcloud19/presentation/
     19th ACM Symposium on Operating Systems Principles (SOSP ’03). Asso-                 young
     ciation for Computing Machinery, 15–28. doi:10.1145/945445.945448




                                                                                 7
