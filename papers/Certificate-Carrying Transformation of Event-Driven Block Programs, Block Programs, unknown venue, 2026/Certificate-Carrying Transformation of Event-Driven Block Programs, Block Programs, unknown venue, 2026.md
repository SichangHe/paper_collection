                                        Certificate-Carrying Transformation of Event-Driven
                                                           Block Programs
                                                                                             Yuan Si and Jialu Zhang∗

                                                                                   University of Waterloo, Waterloo, Canada
                                                                           yuan.si@uwaterloo.ca, jialu.zhang@uwaterloo.ca


                                           Abstract—Block-based end-user languages such as Scratch            cleaned up these programs would benefit authors who lack
                                        run tens of millions of programs whose authors are not ex-            the means to do so themselves; recurring quality problems in
                                        pected to read a correctness argument. The tools that rewrite         shared Scratch code are documented to impede its reuse and
                                        these programs establish behavior preservation through program
                                                                                                              sharing [1], [2]. The obstacle is trust: an optimizer that silently
arXiv:2607.00563v1 [cs.PL] 1 Jul 2026




                                        analysis and testing, without a checked guarantee. We turn
                                        optimization of such programs into certificate-carrying source-       changes a child’s game is worse than none, and this population
                                        to-source rewriting. An untrusted optimizer proposes a rewrite;       cannot notice or recover from the change.
                                        a trusted, fail-closed checker accepts it only after recomputing         End-user languages make this trust problem sharp. A pro-
                                        every side condition that the rewrite’s behavior preservation         fessional developer reads diffs, runs tests, and reverts a bad
                                        depends on, under an explicit observation lens. The checker is
                                        the sole authority: given a correct checker and a small, explicitly   commit; the author of a Scratch game has none of these
                                        stated set of model-to-VM assumptions, an optimizer bug cannot        defenses, and the program is itself the deployed program, so a
                                        mint an unsound acceptance. The observation lens is a parameter       source rewrite is the shipped change. A guarantee that a rewrite
                                        of the framework, and the central soundness argument is a             preserves what the player sees is the only acceptable basis for
                                        cooperative-frame refinement theorem: a write whose value is          touching these programs automatically, and producing one for
                                        overwritten before any thread observes it, within a window in
                                        which no thread yields, can be removed. We mechanize this             a concurrent, rendered, event-driven language is this paper’s
                                        theorem in Lean and show that one parametric statement covers         problem.
                                        two concrete rewrite families, instantiated to variable state and        Certified optimization addresses this kind of trust gap, and
                                        to renderer state. We build a checker for six rewrite families and    it has a mature home in verified compilers. CompCert proves
                                        evaluate it on 300 real Scratch projects sampled from the public      once and for all that its passes preserve the observable behavior
                                        repository. The checker accepts a behavior-preserving rewrite
                                        on 94.3% of projects (283 of 300), a breadth carried by editor        of sequential C [3], [4], and translation validation discharges
                                        and asset cleanup with the certified-runtime families applying on     the same guarantee per run by checking each output against its
                                        fewer; certification costs under one tenth of a second per project    input [5]–[7]. These techniques target sequential intermediate
                                        on average; and a cross-family adversarial campaign of 4,278          representations inside a compiler. The programs we care about
                                        perturbed rewrites produces zero false accepts on the hardened        are cooperatively concurrent, event-driven, and edited directly
                                        checker. An independent pre-submission audit had earlier found
                                        eight false accepts the per-family test suites missed; each is now    by their authors, and their observable behavior is what a player
                                        rejected and carries a regression test. An ablation that strips the   sees and hears rather than a sequence of I/O calls. Certified
                                        semantic side conditions, leaving the analysis-and-testing stance     rewriting for a concurrent end-user language is open territory,
                                        alone, ships rewrites that the virtual machine confirms change        and the legality of removing a write depends on the scheduler,
                                        behavior; the full checker rejects every one. The result is a         clone creation, what the renderer commits to the screen, and
                                        working account of how to give behavior-preservation guarantees
                                        for a concurrent, event-driven, end-user language.                    which editor state a tool may change. Automated refactoring
                                                                                                              for Scratch already exists and establishes behavior preservation
                                                                 I. I NTRODUCTION                             through program analysis, preconditions, and testing [8], [9].
                                           A Scratch project is a concurrent, event-driven program.           CertiBlock adds a checker that recomputes each side condition
                                        Scripts run under a cooperative scheduler, communicate                and is the sole minter of acceptances, under an explicit lens.
                                        through broadcasts and clones, and render to a stage that the            We present CertiBlock, a system that rewrites Scratch
                                        player watches frame by frame. The public Scratch repository          programs under a trusted checker that certifies each rewrite
                                        holds tens of millions of such projects, written largely by           behavior-preserving relative to an explicit observation lens.
                                        children and hobbyists, an audience not expected to inspect           The design follows one discipline: the optimizer proposes
                                        a static analysis or a correctness argument. Programs in this         and the checker disposes. The optimizer is free to be large,
                                        setting carry the same kinds of redundancy that compilers             heuristic, and wrong. It emits a certificate that names the
                                        remove from conventional code: a sprite is repositioned twice         rewrite family, the observation lens, and the concrete edit. The
                                        with no visible frame in between, a broadcast reaches no              checker re-parses the before and after programs, recomputes
                                        receiver, a costume is removed yet still listed. A tool that          from scratch every side condition the family’s soundness
                                                                                                              depends on, and mints an acceptance only when all of them
                                          Corresponding author: Jialu Zhang.                                  hold. Nothing the optimizer claims is trusted, including its own
digests. The soundness of the whole system then rests on an         and report soundness, applicability, cost, and trusted-base size;
auditable checker and two named model-to-VM conformance             a cross-family audit found eight false accepts the per-family
assumptions, while the large optimizer stays untrusted and          suites missed, with the transferable lesson that a multi-family
can evolve without enlarging the trusted base. The two core         checker needs a boundary-crossing adversary (Sections VI–
decision procedures, the structural single-allowed-delta obli-      VII).
gation and the cooperative-frame dead-store admissibility, are
                                                                                II. BACKGROUND AND M OTIVATION
realized as compiled Lean functions proved sound, a verified-
executable reference for the deployed Python checker, which         A. Scratch as an event-driven language
the adversarial campaign, the audit, and the oracle validate           A Scratch program [10], [11] is a set of sprites and a stage,
against the model.                                                  each carrying a graph of blocks. Execution begins at hat blocks
   Two design choices carry the framework. The first is that be-    such as “when green flag clicked” or “when I receive m”. The
havior preservation is stated relative to an explicit observation   runtime runs all active scripts under a cooperative scheduler. A
lens, and the lens is a parameter. A player observes rendered       script executes straight through until it reaches a yield point, at
frames, sounds, prompts, visible monitors, and termination; an      which control returns to the scheduler and the next frame may
editor additionally observes comments and layout. A rewrite         be rendered. The yield points are a fixed set: the wait and wait-
that is sound for a player is unsound for an editor, and the        until blocks, every loop iteration boundary, the glide blocks,
checker enforces the distinction by pinning each family to the      asking for input, and the broadcast-and-wait block. Ordinary
lens under which its edit is behavior-preserving. The second is     motion and looks blocks do not yield, so a run of such blocks
a cooperative-frame refinement theorem, which we mechanize          executes as one uninterrupted segment.
in Lean. The theorem isolates the property that makes dead-            A project is stored as a JSON document mapping block
write removal sound under cooperative scheduling: within a          identifiers to blocks, where each block records its opcode,
window in which no thread yields and no observation of the          inputs, fields, and the identifiers of its parent and next blocks.
written state occurs, an overwritten write is invisible. We state   Two properties of this representation shape the checker. Iden-
the theorem so that the observed resource and the boundary          tity is by identifier: a variable, list, or broadcast message
at which observation happens are both parameters, and we            carries a display name the author can change while the virtual
instantiate it to variable state observed at yield boundaries and   machine binds by identifier, so a check that compares display
to renderer state observed at frame boundaries.                     names can disagree with the machine. Some blocks appear in
   We implement six rewrite families spanning editor cleanup,       a compressed array form, and a scan that does not expand
event-graph simplification, and two dead-store families, to-        them can miss a reference, so the checker rejects a program
gether with an equality-saturation optimizer that the checker       whose blocks it cannot fully read.
gates entirely and a differential oracle that runs the real            Scripts interact through three mechanisms that the rewriting
Scratch virtual machine before and after each accepted rewrite.     families must model. A broadcast sends a message, which
We evaluate on 300 projects sampled uniformly from the              starts every receiver script for that message; the send does not
public repository. The study answers four questions: whether        preempt the sender, and a plain broadcast returns immediately
adversarial and VM-backed validation finds a false accept,          while broadcast-and-wait yields until the receivers finish. A
how often the checker accepts a behavior-preserving rewrite on      clone block copies the source sprite’s full state into a new
real programs, how much it costs, and how large the resulting       instance and schedules the clone’s start scripts, so the clone
trusted base is. A recurring finding shapes the evaluation. Per-    is born carrying the sprite’s position, costume, size, direction,
family testing is not enough. An independent audit of the           visibility, and effects at the moment of creation. The stage is
integrated checker found eight false accepts that the per-family    redrawn once per scheduler step from the current sprite state,
suites had passed, each from a missed observation channel that      and the player observes the program through that sequence of
only a cross-family adversary surfaced.                             frames together with sounds, answer prompts, and the values
   This paper makes the following contributions. We for-            of visible variable and list monitors.
mulate optimization of event-driven end-user programs as               This execution model is the source of both the opportunity
lens-parametric certificate-carrying rewriting, with a trusted      and the difficulty. The opportunity is that the cooperative
checker that recomputes side conditions and is the sole minter      scheduler creates windows of straight-line execution in which
of acceptances (Section III). We give a cooperative-frame           intermediate state never reaches the screen, so a write that is
refinement theorem, mechanized in Lean depending only               overwritten inside such a window is invisible. The difficulty
on its kernel axioms; the end-to-end claim rests separately         is that the boundaries of these windows are subtle and the
on two named model-to-VM conformance assumptions. One               observation channels are many.
parametric statement covers variable and renderer dead-store           The observation channels divide into two kinds, and a sound
elimination, and the two core decision procedures are realized      checker accounts for both. The first is the frame boundary: the
as compiled Lean functions proved sound against it, a verified-     renderer draws after every scheduler step, not only at program
executable reference for the deployed checker (Section IV).         yields, so the window in which no frame is drawn is exactly
We build a checker for six families and an untrusted optimizer      one uninterrupted segment, and any write whose overwriter
gated by it (Section V). We evaluate on 300 real projects           lies past a scheduler step is observable at the intervening draw.
                           TABLE I                                                                    optimizer cert. checker                receipt
                                                                                      program
O BSERVATION CHANNELS OF THE COOPERATIVE , RENDERED MODEL AND                                        (untrusted)      (trusted)         ACCEPT/ REJECT
          THE TREATMENT A SOUND REWRITE OWES EACH .


Channel                    Modeled as                Treatment                                                        VM oracle
                                                                                                 conformance
                                                                                                                      (untrusted)
frame draw, per sched-     observation               a visual write cannot
uler step                  boundary                  cross it
pen down, stamp            in-segment commit         visual store in the win-    Fig. 1. The optimizer proposes a rewrite with a certificate; the checker
                                                     dow is live                 recomputes every side condition and mints the only authoritative verdict; the
clone creation             state snapshot            visual store in the win-    VM oracle independently checks behavior on the real virtual machine. Shaded
                                                     dow is live                 boxes are the trusted base.
visible variable or list   player observation        the variable or list is
monitor                                              live; asset removal re-
                                                     jects
costume or backdrop        player observation        asset removal that shifts          III. L ENS -PARAMETRIC C ERTIFIED R EWRITING
index read                                           it rejects
timer, mouse, loudness     external read             store in the window is      A. The trusted boundary
sensing                                              live; oracle fixes them
                                                     with a deterministic har-      CertiBlock separates an untrusted optimizer from a trusted
                                                     ness                        checker, as Figure 1 shows. The optimizer reads a program,
broadcast with no re-      no player effect          dead-broadcast removal      proposes a rewrite, and emits a certificate. A certificate names
ceiver                                               accepts
                                                                                 the rewrite family, the observation lens, a locator for the
                                                                                 edited region, and the SHA-256 digests of the before and after
                                                                                 byte streams; the certificate is a set of hints, a locator and
The second is the in-segment commit, where an action makes
                                                                                 not a proof object. The checker re-parses both byte streams,
state observable without yielding: a pen-down motion draws a
                                                                                 recomputes the digests, pins the lens from its name through
line, a stamp copies the sprite onto the stage, a clone snapshots
                                                                                 a fixed table, looks up the family’s obligations in a registry,
the sprite, and a sensing block or a say bubble reads or renders
                                                                                 and discharges each obligation against the recomputed facts.
the sprite at the moment it runs. A yield ends a segment; an
                                                                                 The checker mints a receipt with a single authoritative verdict,
in-segment commit does not, yet a yield-only analysis misses
                                                                                 and only a receipt that records acceptance permits the rewrite
it. That distinction is the technical crux of the visual dead-
                                                                                 to ship. This is the LCF discipline applied to rewriting. The
store family. Table I lists the channels and how a rewrite must
                                                                                 checker is the only component that can declare a rewrite sound,
treat each, and the rest of the paper recomputes exactly these
                                                                                 and it does so by reconstructing the fact, never by accepting
conditions.
                                                                                 the optimizer’s word for it.
B. A motivating example                                                             The receipt the checker mints carries the verdict and the
                                                                                 obligation results, and no field of a certificate can set a
  Consider a sprite whose green-flag script places itself, sets
                                                                                 verdict. A family is dischargeable only if it is registered in the
up its costume, then places itself again before entering its main
                                                                                 checker, and its obligation list is fixed by the family author
loop.
                                                                                 and read from the registry. The optimizer cannot add, remove,
                                                                                 or reorder obligations, and an unregistered family name is
when        clicked                                                              rejected outright. Each family carries one obligation of a
                                           when       clicked                    distinguished kind, the single-allowed-delta obligation, which
go to x: 0 y: 0                                                                  proves that the only structural difference between the before
                                           switch costume to ready               and after programs is the declared edit class. Any change the
switch costume to ready                                                          optimizer introduces beyond the declared edit fails it, so the
                                           go to x: 100 y: 50                    checker need not anticipate every way an optimizer might
go to x: 100 y: 50                                                               misbehave; it only confirms that the difference it sees is the
                                                  after: W1 removed
       before: W1 then W2                                                        one the family is allowed to make. The checker also wraps
   The first placement W1 (go to x: 0 y: 0) is overwritten                       every obligation in a fail-closed guard that turns an exception
by W2 before the loop and no block between them yields, so                       into a rejection, so the trusted base degrades safely.
no frame is drawn at the origin and removing W1 preserves                           Algorithm 1 states the entire trusted procedure. It re-derives
what the player observes. The removal is sound only under                        the digests from the byte streams before reading anything else,
the channels of Table I: a pen line or a clone between W1 and                    so a certificate that misreports the program it edited is rejected
W2 would make the intermediate position visible, a sensing                       at once. It pins the lens by name and looks the family up in
read would leak it to a monitor or a bubble, and a stage-                        the registry, so an unknown lens or an unregistered family
edge clamp depending on the prior position would make the                        is rejected before any obligation runs. It then discharges the
two placements non-interchangeable. A checker that accepts                       family’s fixed obligation list and accepts only when every
the removal must recompute all of these, and a theorem must                      obligation proves. The procedure is the sole minter of an
establish they suffice. The rest of the paper builds that checker                acceptance, and every branch that is not an explicit acceptance
and that theorem.                                                                is a rejection, which is what makes the trusted base fail closed.
 Algorithm 1: Trusted check of a single rewrite                       Recomputation has a concrete payoff in this domain, because
  Input: certificate c; before and after bytes b, a                   the soundness of a rewrite depends on how the Scratch virtual
  Output: a single verdict, ACCEPT or R EJECT                         machine reads the program, and the checker must read it the
1 if sha(b) ̸= c.bd or sha(a) ̸= c.ad then return                     same way. Three examples show why a plausible check is
    R EJECT                                                           wrong and a recomputed one is right.
                        ′
2 P ← PARSE (b); P ← PARSE (a)                                           Broadcast dispatch resolves a sent message by identifier
3 L ← L ENS (c.lens); F ← R EGISTRY [c.family]                        through the project’s broadcast table and matches messages
4 if L or F undefined, or F.lens ̸= L then return                     case-insensitively. A message that the author renames in the
    R EJECT                                                           editor keeps its identifier while its visible name changes, so
5 foreach obligation o ∈ F.O BLIGATIONS (L) do                        a reachability check that compares visible names concludes
6      if D ISCHARGE(o, P, P ′ , L) ̸= proved then return             that a live send is dead. The checker resolves the send by
         R EJECT                                                      identifier through the table, the way the virtual machine does,
                                                                      and matches case-insensitively over the ASCII range where the
7   return ACCEPT
                                                                      comparison is provably the same as the machine’s. A message
                                                                      name outside that range makes the case folding uncertain, and
                                                                      the family rejects.
B. Observation lenses                                                    The sensing block that reads another sprite’s attribute takes
   Behavior preservation is meaningful only relative to what          its target sprite from an input, and a check that reads the
counts as behavior. CertiBlock fixes a single raw observation         block’s field instead misidentifies the observed sprite, so it
of an execution and defines lenses as views of it. The player         can miss a read of a variable it is about to declare dead. The
lens Lplayer observes the sequence of rendered frames, which          checker reads the target from the input the virtual machine
the runtime commits at every scheduler step, together with            consults. The third example is asset removal. Removing a
sounds, answer prompts, the values of visible variable and            costume below the current index shifts the one-based index
list monitors, and termination. Broadcasts and clones are             that another script reads through a sensing block or a visible
observable only through these channels, so a broadcast that           monitor, so the family treats any such reader as an observer
reaches no receiver, and produces no frame, sound, prompt,            of the index and rejects a removal that would shift it. Each
or monitor change, is unobservable under Lplayer . The final-         of these is a place where the checker reads exactly what the
state lens Lfinal observes selected final state under bounded         machine reads, and where it cannot, the responsible family
scenarios and ignores intermediate frames. The debug lens             rejects. This default-deny stance is the reason the trusted
Ldebug additionally observes editor and comment state. The            base can be small: the checker never approximates a machine
lenses form a tower in which Ldebug is finer than Lplayer ,           operation it cannot replicate.
which is finer than Lfinal : an observation distinguished by a           The same stance governs unsupported features. The Scratch
coarser lens is distinguished by every finer lens. Refinement         opcode space is open, so the checker classifies blocks by
of one program by another is inclusion of observable trace            an allow-list of known stock opcodes, and any extension or
sets under a lens, so a rewrite preserves behavior under a lens       unknown opcode falls outside it and forces the responsible
when the after program refines the before program at that lens.       family to reject. A cloud variable is treated as always live,
   The framework takes the lens as a parameter, which lets it         a read of timer, mouse, loudness, or current time counts
host families with different soundness conditions under one           as an observation of external state that keeps a write in
mechanism. Editor cleanup is sound under Lplayer because              its window live, and a computed broadcast name refuses
removing a comment leaves the canonical program core byte-            the broadcast-reachability families. An unsupported feature
identical, and it is unsound under Ldebug because an editor           is rejected or marked unknown, never silently assumed safe,
observes comments. The checker pins comment cleanup to                so the soundness of the checker does not depend on having
Lplayer by name, so a certificate claiming any other lens is          enumerated every feature of an evolving platform.
rejected before obligations run. A dead-store family is also                   IV. T HE C OOPERATIVE -F RAME T HEOREM
pinned to Lplayer but for a different reason. Its edit changes
runtime state that a player would observe if the store were live,     A. Statement
and the family’s obligations prove that the store is not live. Size      The technical core of CertiBlock is a refinement theorem
is a property a tool reports as a metric, and it is not a lens;       for dead-store elimination under cooperative scheduling. The
the framework measures byte savings outside the behavioral            theorem isolates the condition under which an overwritten
model. The result is a uniform treatment: each family declares        write is unobservable. Consider a thread that writes a resource,
the lens under which its edit is behavior-preserving, and the         continues without yielding, and writes the same resource
checker holds it to that declaration.                                 again. Call the span between the two writes the pending
                                                                      window, the first write the dead store, and the second the
C. Side-condition recomputation                                       overwriter. If no observation of the resource occurs in the
   The defining move of the framework is that the checker             pending window and the window contains no yield, then the
recomputes side conditions and trusts nothing in the certificate.     state the dead store establishes never reaches an observation,
and deleting the dead store refines the original program under       scheduler step, so the only window without a draw is a
Lplayer .                                                            single uninterrupted segment, and the observation boundary
   The theorem is stated with two parameters: the observed           for visual state is larger than a program yield. The in-segment
resource and the boundary at which observation happens. A            commits of Table I, a pen line, a stamp, or a clone creation,
boundary is a step that reads a set of resource cells and emits      each count as an observation in the pending window, so a dead
a trace event, and the same abstraction covers a read by the         visual write whose window contains one fails admissibility and
running thread and a frame drawn by the renderer.                    the family rejects it. The model also requires the overwriter
                                                                     to be commit-pure (it produces no in-segment commit and
Definition 1 (Pending window and admissibility). Let W1
                                                                     ignores the old value), which matters for motion: the virtual
write resource cell r and let W2 be the next write of r on
                                                                     machine clamps a placement against the stage edge, and
the same thread with no yield between them. The pending
                                                                     the clamped result can depend on the prior position, so the
window is the span of steps between W1 and W2 . The window
                                                                     family admits a motion overwrite only when its coordinates
is admissible when every observation step o in it satisfies
                                                                     are literals within the stage bounds, where the clamp is the
read(o) ∩ {r} = ∅, and W2 does not read the value of r.
                                                                     identity. We verify in Lean that a pending-window observation
Theorem 1 (Cooperative frame). If the pending window of              of the dead resource makes the removal unsound and that
W1 is admissible, then the program obtained by deleting W1           admissibility rejects exactly that case.
refines the original under Lplayer .
   Cooperative scheduling makes the no-yield window single-          C. Mechanization and trusted base
threaded, so the only writes to r within it are W1 and W2 , and
                                                                        The development is mechanized in Lean 4 (v4.30.0) [12]
a concurrently scheduled thread enters only at a yield, which
                                                                     without external libraries. The step relation, the yield points,
ends the window. The admissibility condition states that no
                                                                     the observation steps, and the traces are defined there; the
observation in the window reads the dead cell and that the
                                                                     paper states the theorem in prose and the mechanized de-
overwriter does not depend on the old value. Under it the trace
                                                                     velopment carries the formal definitions, so the result is a
produced with the dead store present equals the trace produced
                                                                     checked theorem and not a prose claim. The headline theorem
with it deleted. The proof exhibits a simulation between the
                                                                     and both family instances depend only on the propositional-
two programs in which the configurations agree on every
                                                                     extensionality and quotient-soundness axioms that the Lean
cell except the dead one, and an admissible observation,
                                                                     kernel provides, with no use of classical choice and no family-
reading no dead cell, cannot distinguish the configurations,
                                                                     specific modeling assumption. Editor-cleanup soundness is a
so the emitted traces coincide step by step until the overwriter
                                                                     theorem rather than an axiom: the model defines a canonical
restores agreement on the dead cell as well. The window need
                                                                     core as the projection the virtual machine loads, discarding
not be straight-line: an intervening conditional whose branches
                                                                     comments, layout, and metadata, and the proof tracks the
neither yield nor observe r stays within the segment, and the
                                                                     loader’s read set to show that programs with equal cores
mechanization certifies that case too.
                                                                     produce equal player observations, so a cleanup that changes
B. Two instances of one theorem                                      only material outside the core refines under the player lens,
   The two dead-store families of CertiBlock are instances           modulo the same loader-conformance assumption the dead-
of this single statement at different choices of resource and        store families rely on. Two model-to-VM conformance as-
boundary. Variable dead-store elimination instantiates the re-       sumptions remain, and we name them as an explicit trusted
source to a variable cell and the boundary to a yield, because       base, in the style of the axiomatized hardware of CompCert.
a player observes a variable only through a visible monitor          The first states that a player observation depends only on
recomputed at frame boundaries. Visual dead-store elimination        the projected runtime state, and the second states that the
instantiates the resource to a renderer cell, a sprite’s position,   pinned virtual machine loads a program in conformance with
direction, size, visibility, costume, or graphic effect, and the     the model’s loader. Both concern the fidelity of the model to
boundary to a renderer draw. The two families are the same           the real machine, and the differential oracle of Section VII
theorem applied at two boundary values: the variable corollary       is the empirical evidence for them; neither is proved. The
and the visual corollary are the parametric theorem specialized      Lean development is 5,909 lines and builds with no incomplete
to the two boundaries, checked by reflexivity.                       proofs.
   Parameterizing the boundary is what lets one proof serve             The mechanized theorem certifies an abstract model. The
both. A yield-only theorem is sound for variables and unsound        two core decision procedures are realized as compiled Lean
for renderer state, because renderer state commits at points         functions proved sound, a verified-executable reference. The
a yield-only analysis does not see. A new dead-store family          deployed checker is a separate Python implementation, con-
supplies a resource and an observation set and inherits the          nected to the model by construction and testing, and the
proof. We claim only the genericity these two instances              differential oracle tests the model’s observation boundary
exercise; a third resource would test it further.                    against the machine. A verified bridge from the reference to
   The renderer boundary forces the theorem’s generality to          the deployed checker is future work, the honest limit of the
do real work. The virtual machine draws a frame after every          guarantee treated in Section VIII.
                  V. T HE R EWRITE L IBRARY                                                     TABLE II
                                                                      T HE SIX FAMILIES : THE CONDITION THE CHECKER RECOMPUTES ,
A. Six families                                                     WHETHER THE SOUNDNESS RESTS ON A L EAN - MECHANIZED THEOREM ,
                                                                     AND THE DIFFERENTIAL ORACLE ’ S ROLE ( SANITY, SEEDED , OR VM
   CertiBlock implements six rewrite families that span editor           VALIDATION ). A LL ARE SOUND UNDER THE PLAYER LENS .
cleanup, event-graph simplification, and dead-store elimina-
tion. Comment cleanup removes comment entries and their             Family                  Recomputed condition          Mech.   Oracle
block backreferences. It is sound under Lplayer because the         Comment cleanup         canonical core unchanged       yes    sanity
canonical program core, the projection that the virtual machine     Unused-asset cleanup    no reference or index-shift    no     sanity
loads, is unchanged, and the family proves core equality                                    observer; de-dup retargets
                                                                                            references; clean splice
directly. Unused-asset cleanup removes costumes, sounds,            Dead-broadcast          message reaches no receiver    no     sanity
variables, and lists that no block references and de-duplicates     removal
byte-identical assets. Its delicate condition is the costume        Dead-code elimination   component never runs;          no     sanity
                                                                                            clean splice
index: removing an unreferenced costume below the current           Variable dead-store     overwritten in a no-yield      yes    seeded
one shifts the index that a sensing block or a visible monitor                              window
reads, so the family forces a project-wide rejection of costume     Visual dead-store       no observable commit in the    yes    VM
                                                                                            segment
and backdrop removal whenever any such reader is present.
   Dead-broadcast removal deletes a broadcast send whose
message reaches no receiver. The family resolves the message
                                                                    Algorithm 2: Visual dead-store acceptance
by identifier through the broadcast table, matches receivers
case-insensitively over the ASCII range, and rejects when            Input: program P , proposed rewrite P ′ ; candidate
a computed message name or a non-ASCII name puts the                           write W1 on renderer keys K, target t
reachable set beyond what the checker can decide. Dead-code          Output: ACCEPT if W1 is a removable dead store,
elimination removes whole unrunnable top-level components:                      else R EJECT
an empty handler hat on a fixed whitelist of stock trigger         1 if P EN P RESENT (P ) and I S M OTION (W1 ) then

opcodes, a receiver hat for a message that is never sent, or           return R EJECT
a loose stack with no triggering hat. The family computes the      2 W2 ← ⊥

component as the transitive closure of a head over its successor   3 foreach x ∈ S TRAIGHT L INE (W1 ) do

chain and its nested inputs, and it refuses to cross into an       4      if B REAKER(x) or O BSERVES(x, K) then return
independent top-level script, because the virtual machine runs              R EJECT
any top-level block as its own script regardless of an incoming    5      if F ULL OVERWRITE(x, K) then
successor edge.                                                    6           W2 ← x; break
   The two dead-store families realize the cooperative-frame       7      else if W RITES(x, K) then return R EJECT
theorem. Variable dead-store elimination removes a variable        8  if W2 = ⊥ then return R EJECT
write that an overwriter cancels inside a no-yield window          9  if I S M OTION(W2 ) and not F ENCE I D(W2 , t) then
with no intervening read, no external observation, and no               return R EJECT
cloud variable or visible monitor on the variable. Visual dead-                   ′
                                                                   10 if C ORE (P ) ̸= C ORE (R EMOVE (P, W1 )) then return
store elimination removes an overwritten renderer write under           R EJECT
the conditions Section IV requires: a single uninterrupted         11 return ACCEPT
segment, an absolute overwriter of the same key, no pen,
stamp, clone, sensing, or bubble observation in the window,
and for motion the literal-in-bounds condition under which
the stage clamp is the identity. All six are sound under the       condition. The pen guard removes the one in-segment commit
player lens. Table II states, per family, the condition the        the walk cannot localize, because a pen-down state makes
checker recomputes, whether the soundness rests on a Lean-         every motion an observable commit. The window-breaker test
mechanized theorem, and the oracle’s role. Three of the six        ends the segment at the first yield, where a frame is drawn;
carry a mechanized theorem (cooperative-frame for the two          the observer test is admissibility itself, refusing the removal
dead-store families, core-equality for comment cleanup); the       when a sensing read, stamp, clone, or bubble in the window
other three rest on a recomputed structural argument the oracle    reads the key or a coupled key. The overwriter must be a full
corroborates.                                                      absolute commit-pure write, the theorem’s requirement that
                                                                   it not read the old value, and a partial overwrite is refused.
B. The visual dead-store decision procedure                        The fence-identity test enforces the one VM-level subtlety
  The visual family turns the cooperative-frame theorem into       the theorem leaves to the checker: a motion overwrite is a
a decision procedure, stated as Algorithm 2, whose steps map       true overwrite only when the stage clamp is the identity,
one to one onto the clauses of the theorem. The procedure          which holds for literal in-bounds coordinates on a sprite that
walks the straight-line segment after the candidate write and      cannot be dragged. The clean-splice test confirms the proposed
accepts only when the segment realizes the admissibility           program P ′ is exactly P with the candidate removed.
C. Obligations and structural soundness                             recomputed intermediate, and the transitivity of the refinement
   Algorithm 2 is one instance of a decision-procedure skeleton     preorder, mechanized in Lean, lifts the per-step guarantees to
the families share, and the others differ only in the segment       the whole sequence. This composition is where the engine
they walk and the observation they forbid. Variable dead-store      earns its place over a single-pass applier: on 57 of the 300
elimination walks the same straight-line segment but forbids        projects the verified result composes two or more families, up
a read of the variable rather than a renderer observation,          to three families and seven steps in one sequence, which a
and adds the cloud-variable and visible-monitor checks that         one-rewrite-per-family pass could not express.
make the variable externally observable. Dead-broadcast and            Behavior preservation of an accepted rewrite is checked
dead-code removal walk the event graph, and their forbidden         a second way by a differential oracle that runs the real
observation is a reachable receiver or trigger. This shared         Scratch virtual machine on the before and after programs
skeleton is what lets the cooperative-frame theorem serve more      under identical deterministic conditions and compares the
than one family: each names the segment, the resource, and          player-visible traces. The oracle is a sanity check on the
the forbidden observation, and inherits the rest.                   model and is itself untrusted. Two of its properties matter
   Each family is a list of obligations the checker discharges,     for the evaluation. It observes only player-visible state, so it
and the lists share a shape. A lens check confirms that the         ignores editor bookkeeping such as an unreferenced broadcast-
claimed lens is the one the family is sound under. A well-          message variable that the editor garbage-collects on load. It
formedness pre-pass rejects compressed or malformed block           runs a determinism control on any flagged mismatch, re-
forms that the scans cannot see, because a block the scan           tracing the before program several times, because a small frac-
cannot read could hide a reference, a sender, or a triggering       tion of real projects combine randomness, waits, and clones in
hat. The single-allowed-delta obligation confines the structural    a way the headless harness cannot reproduce deterministically;
difference to the declared edit. The family-specific conditions     a project whose own behavior is not reproducible is reported as
then establish behavior preservation under the lens.                not adjudicable rather than as a mismatch. The oracle catches
   Structural removal is reconstructed rather than trusted. The     discrepancies between the model and the machine, and the
checker derives the set of removed block identifiers from the       audit of Section VII shows that this second method finds
difference between the before and after programs, recomputes        mistakes the static obligations alone do not.
the program that results from deleting exactly that set, and
                                                                            VI. I MPLEMENTATION AND T RUSTED BASE
requires its canonical core to equal the after program’s core. A
partial deletion, an orphaned successor, or a dangling reference       CertiBlock implements the checker and optimizer in Python,
changes the reconstructed core and fails the comparison, so         drives a headless build of the Scratch virtual machine for the
the checker accepts a removal only when the after program is        differential oracle, and mechanizes the proofs in Lean 4. The
exactly the before program with a clean splice of the declared      trusted base is the checker package, which the soundness claim
component. This reconstruction is the same for every removal        rests on. It is 9,921 lines and divides into three parts: a fixed
family, which is why the soundness argument for structural          kernel of 1,856 lines for the certificate and receipt types, the
edits is shared rather than re-proved per family.                   lens table, the resource model, the well-formedness pre-pass,
                                                                    and the family registry; 6,060 lines of family obligations across
D. The optimizer and the differential oracle                        the six families; and a 2,005-line intermediate-representation
   The optimizer is an equality-saturation engine [13], [14] that   compiler that only the variable dead-store family needs to
proposes rewrites and keeps only those the checker accepts.         reason about variable reads and writes across control flow. The
Saturation gates every proposed edge through the checker, so        untrusted optimizer (3,060 lines) and the differential oracle
a hostile gate that rejects everything yields the unchanged         and harness (2,292 lines) together are 5,352 lines and carry
input, and the composed result is re-checked as a sequence          no part of the guarantee. The two core decision procedures
against the actual intermediate programs. The cost model lives      are also realized as compiled Lean functions proved sound
in the optimizer and chooses among already-accepted states,         (Section IV), a verified-executable reference separate from
so it cannot make an unsound result win. The optimizer is           these 9,921 deployed Python lines.
outside the trusted base, and it plays no role in the soundness        The proportion is the point of the design. A bug anywhere
argument; the edits themselves are framed graph rewrites in         in the 5,352 untrusted lines, or in the optimizer’s heuristics
the algebraic graph-transformation tradition [15].                  and cost model, cannot cause an unsound acceptance, because
   Composing several rewrites needs care because a certificate      the checker re-derives every fact it relies on, so the optimizer
justifies one step. The optimizer emits a sequence certificate      can grow toward more aggressive rewriting without enlarging
with the digests of the intermediate programs, and the checker      what a reviewer must trust. The family obligations dominate
re-anchors on the actual intermediates and checks each step         the trusted base because each encodes the observation con-
against the recomputed program the previous step produced.          ditions of its edit class, where the domain knowledge of the
Composition stays within one lens, and the unification of the       cooperative, rendered model lives. The parser is trusted and
families on the player lens lets one saturation run compose a       fails loudly on any input it cannot represent, and the obligation
cleanup rewrite with a dead-store rewrite into a single check-      runner wraps every obligation in a fail-closed guard, so a
able sequence: each step is certified independently against the     malformed program or a defect in one family degrades to a
                          TABLE III                                       One false accept illustrates the class. Unused-asset cleanup
 FALSE ACCEPTS FOUND BY THE AUDIT, GROUPED BY THE OBSERVATION          removed an unreferenced costume below the current index
           CHANNEL THE FAMILY FAILED TO RECOMPUTE .
                                                                       and re-pointed to keep the same image, but the removal
   Family                  Missed observation channel          Count   shifted the one-based index of every costume above it, which
   Unused-asset cleanup    costume/backdrop index read          4
                                                                       a second sprite read through a sensing block and displayed:
   Dead-code elimination   closure reach; broadcast timing      2      the image was unchanged while the number changed. The per-
   Visual dead-store       relative selector; yielding sound    2      family suite tested removal and re-pointing, not a second sprite
                                                                       reading the index, the channel that appears only when two
                                                                       families’ concerns meet. The fix treats any reader of the index,
refusal rather than an unsound acceptance. When the checker            a sensing read, a monitor, or an extension, as an observer.
is unsure it rejects, and the cost of that discipline is the              The other false accepts have the same shape, each a missed
completeness reported as the prevalence numbers.                       observation channel and each now rejected with a regression
                                                                       test that keeps it closed.
                       VII. E VALUATION                                   2) The adversarial campaign: The cross-family adversarial
   We evaluate CertiBlock on 300 projects sampled from                 campaign tests the single-allowed-delta backstop that every
the public Scratch repository. We draw project identifiers             family shares. For each project and family it takes the op-
uniformly at random across the version-3 id range. Most                timizer’s proposed removal and derives variants that add a
identifiers in the range resolve to deleted, unshared, or empty        second edit beyond the declared one, by flipping a literal,
projects, which we skip; we keep the shared, loadable ones             perturbing a field, inserting a statement, or deleting an un-
until 300 are collected. This sampling avoids the popularity           related block; each variant is no longer the single allowed
bias of the front-page listing, and the 300 parse and load             delta, so the checker must reject it. Over the real 300-project
by construction. The corpus spans real projects, from single-          corpus and a supplementary set of 400 real Scratch projects
sprite animations to games with more than two hundred targets          from [16], the campaign runs 4,278 such variants across the
and over fourteen thousand blocks; the median project has 3            six families and produces zero false accepts. The variable
targets and 34 blocks, the 90th percentile 556 blocks. Across          dead-store family, inert on natural projects, is exercised by
the sample 35% use broadcasts, 19% clones, 17% custom                  seeding a genuine dead store before perturbing it, and the
blocks, and 9% pen, so it exercises the concurrency, clone,            bespoke comment and asset fuzzers accept no invalid rewrite
and rendering features the checker reasons about. We ask four          either. This campaign stresses the structural single-allowed-
questions. RQ1 asks whether the checker admits a false accept.         delta backstop every family shares; the semantic side condi-
RQ2 asks how often the checker accepts a behavior-preserving           tions of the dead-store families are exercised separately by the
rewrite on real programs. RQ3 asks what certification costs.           differential oracle, so the two methods cover complementary
RQ4 asks how the formal development bounds the trusted                 halves of each acceptance.
base.                                                                     3) VM-differential conformance: The differential oracle
                                                                       runs scratch-vm 1.6.19 on the before and after of every
A. RQ1: Does the checker admit a false accept?                         accepted rewrite, driven from the green flag with a determin-
   The Lean theorem establishes soundness for the abstract             istic empty answer to any prompt, for 240 scheduler ticks
model; RQ1 asks whether the executable checker and the                 under a fixed seed, and compares the player-visible trace of
model-to-VM boundary admit a false accept under adversarial            frames, sounds, monitor values, and termination. Table IV
and VM-backed validation. We attack the implementation five            reports the result per family. Across the corpus the oracle
ways: unit obligations per family, an independent audit of the         finds no behavioral mismatch on any accepted rewrite. Six
integrated checker, a cross-family adversarial campaign, VM-           accepted rewrites are reported as not adjudicable because their
differential conformance, and an ablation that removes the             own behavior is not reproducible under the headless harness,
semantic side conditions to confirm the checker rejects the            identified by the determinism control; their guarantee rests
unsoundness they guard.                                                on the static obligations, which hold without the oracle. The
   Each family carries a unit suite that exercises its accept path     visual family is evaluated under the full kinematic lens that
together with one adversarial negative per obligation. The six         records sprite position and costume, the variable family on
suites hold 274 tests, and all pass. Passing the per-family suites     seeded dead stores because it is inert on natural projects, and
is necessary, and the audit shows it is not sufficient.                the rest on their natural acceptances.
   1) The audit: We ran an independent adversarial audit of               4) The side conditions are load-bearing: The first four
the integrated checker. Each probe attacks one family along            methods show the checker accepts no unsound rewrite; this one
one pitfall class drawn from the observation channels, and each        shows its semantic side conditions are why. We build a frame-
finding is reproduced and confirmed against the real virtual           unaware permissive remover that applies the textbook dead-
machine before it is counted. The audit found eight false              store rule to renderer writes, dropping the cooperative-frame
accepts in families that had passed their own suites (Table III),      model: it ignores intervening frame boundaries, pen state,
all on observation channels a single-family view does not see,         clone or stamp snapshots, and stage clamping, the analysis-
which is why the audit finds what the unit suites miss.                and-testing stance of a tool without a behavioral model. We
                             TABLE IV                                                             TABLE V
VM- DIFFERENTIAL VALIDATION ON THE CHECKER - ACCEPTED REWRITES            K ERNEL - ACCEPTED REWRITES , BYTES SAVED , AND AVERAGE
 OF THE 300- PROJECT CORPUS , ALL UNDER Lplayer ( VISUAL UNDER THE      PER - PROJECT CHECKER TIME ON THE 300 PROJECTS , FOR THE FIVE
FINER KINEMATIC PROJECTION , VARIABLE ON SEEDED MUTANTS ). E VERY      FAMILIES WITH NATURAL ACCEPTANCES ( VARIABLE DEAD - STORE IS
 ACCEPTED REWRITE IS ADJUDICATED : VALIDATED PLUS FLAKY EQUALS                              INERT; SEE TABLE IV).
 ACCEPTED , AND NO ACCEPTED REWRITE IS A MISMATCH . “F LAKY ” IS A
  PROJECT WHOSE OWN BEHAVIOR IS NOT REPRODUCIBLE UNDER THE
                                                                         Family                   Accepts   Bytes saved   Time/proj.
                         HARNESS .
                                                                         Comment cleanup              25        36,626      77.0 ms
     Family                         Accepted   Validated   Flaky         Unused-asset cleanup        267       365,857       6.3 ms
                                                                         Dead-broadcast removal        6         1,389      28.0 ms
     Comment cleanup                     25          24       1          Dead-code elimination        56       246,159      51.2 ms
     Unused-asset cleanup               267         264       3          Visual dead-store            17         3,234      46.2 ms
     Dead-broadcast removal               6           6       0
     Dead-code elimination               56          55       1
     Variable dead-store (seeded)        23          23       0
     Visual dead-store                   17          16       1      accepted removal is VM-validated with no mismatch. Dead-
                                                                     code and dead-broadcast removal apply on a smaller set of
                                                                     projects whose event graphs contain unreachable handlers
run it on every project, take the real virtual machine as ground     or sends. Variable dead-store elimination is inert on natural
truth for whether each removal changes the player-visible            projects: a variable in real Scratch is almost always read
trace, and record the checker’s verdict on the unsound ones.         somewhere, so a transaction-local dead store is rare.
On the 300-project corpus it fires 79 times; the oracle confirms        The corpus makes the inertness precise: 113 projects write a
18 change behavior, and the checker rejects all 18, in each case     variable and 105 write one twice, yet none yields a removable
naming the violated side condition: a frame boundary (wait,          transaction-local dead store, the variable being read elsewhere
glide, a yielding sound), a clone snapshot, or an unbounded          first, so the variable family is a proof-of-concept second
call. The result replicates on 400 supplementary projects from       instantiation of the theorem rather than a rewrite that fires
the ScratchLens dataset of student Scratch projects [16] (177        on natural code.
removals, 33 unsound, all rejected).
   The five methods answer RQ1 together: no method finds a           C. RQ3: What does certification cost?
surviving false accept, the audit now carries the regression tests      Certification is cheap. Table V reports, per family, the
that keep its findings fixed, and the ablation shows the side        kernel-accepted rewrites on the corpus, the bytes saved on
conditions catch real unsoundness, not merely assert safety.         the accepted set, and the average checker time per project.
The cross-family audit was necessary to reach that state.            Every family mean is under one tenth of a second despite
                                                                     the checker recomputing every side condition; across accepted
B. RQ2: How often does the checker accept a rewrite?                 checks the median is 2 ms, the 95th percentile 66 ms, and the
   A guarantee is useful only if the checker accepts behavior-       slowest single check 1.3 s on the largest project. The byte
preserving rewrites on real programs. The checker accepts            savings concentrate in the cleanup families because their edits
at least one behavior-preserving rewrite on 283 of the 300           remove larger structures; the runtime families save little space
projects (94.3%, 95% CI [91.1, 96.4]); the per-family counts         because their value is behavioral. At this cost the checker can
in Tables IV and V are accepted rewrites, and a project can          run on every editor save, and as a background service across
take rewrites from several families. The untrusted optimizer’s       a repository.
equality saturation completes within the time bound on 286 of
the 300 projects; the 14 that time out are a scalability limit of    D. RQ4: How large is the trusted base?
the optimizer, not the checker, recoverable by a more scalable          The trusted base is the 9,921-line checker of Section VI
enumeration without touching the trusted base.                       together with the Lean development and two model-to-VM
   The families differ in how often they apply, and the dif-         conformance assumptions. The Lean development is 5,909
ferences reflect the structure of real Scratch. Editor cleanup       lines, builds with no incomplete proofs, and its dead-store
and unused-asset cleanup are common, applying on most                theorems depend only on the two kernel axioms that Lean
projects, because authors leave comments and unreferenced            provides, with no classical choice and no family-specific
assets behind as they iterate, and these cleanup families carry      modeling assumption. The two core decision procedures are
the acceptance count. The runtime families apply less often          also realized as compiled Lean functions proved sound under
and are where the certified-runtime contribution lies. Among         Lean’s standard propext, Quot.sound, and the decide-
them, visual dead-store elimination has the most reach: the          introduced Classical.choice, a verified-executable ref-
feasibility scan finds candidates in 27 of the 300 projects          erence the deployed Python checker is validated against. The
(9.0%, 95% CI [6.3, 12.8]), spread across the visual keys. The       two conformance assumptions are named statements about the
checker accepts a removal on 17 of them; the oracle validates        model’s fidelity to the virtual machine, with the RQ1 oracle as
16 and reports 1 as not adjudicable, with no mismatch. The           empirical evidence. This is a CompCert-style trusted base: an
result also generalizes to student code [16]: there, dead stores     auditable checker, a mechanized argument, and a short list of
to motion and graphic-effect keys are common, and every              named assumptions about the parts the proof does not reach.
Adding a family grows the trusted base by one obligation list       basic block. Credible compilation and witness-passing valida-
audited in isolation, so the trust cost grows linearly in the       tors attach checkable evidence to a transformation [26]–[30];
number of families.                                                 the certificate of CertiBlock plays this role at the source level
                                                                    and is recomputed rather than replayed. CompCertTSO verifies
      VIII. D ISCUSSION AND T HREATS TO VALIDITY                    compilation under relaxed-memory concurrency [31]; its con-
   The deployed checker is a Python implementation of the           currency is preemptive shared memory, while the cooperative
model, so a transcription error there is a soundness gap the        scheduling of Scratch is what makes the cooperative-frame
proof does not close. The four RQ1 methods and the audit            theorem sound and far less conservative than a preemptive
guard against it, and a verified bridge from the Lean reference     analysis allows. The certificate-carrying stance descends from
to the checker would close it.                                      proof-carrying code [32], and like a small verified kernel [33]
   The differential oracle is untrusted and can miss or over-       its guarantee rests on a trusted base a reviewer can audit.
report. For projects it cannot adjudicate, the guarantee rests on      Event-driven execution relates Scratch to synchronous re-
the static obligations, the correct fallback: the oracle checks     active languages, which have verified compilation to a de-
the model, not the source of soundness.                             terministic core [34]–[36]. Software-engineering work on
   The framework should carry to other event-driven run-            Scratch [10], [11] studies, analyzes, and transforms its pro-
to-completion languages, though we have not instantiated a          grams: datasets and quality studies [2], [37], [38], static
second substrate: the cooperative-frame theorem needs only a        analyzers and bug catalogs [1], [39], [40], and automated
scheduler whose observations commit at identifiable steps, not      test generation [41]. Lens-parametric behavioral equiva-
preemptive shared memory.                                           lence for Scratch was proposed in recent work [16], on
   The corpus is a uniform random sample, so RQ2’s preva-           which CertiBlock builds certificate-carrying rewriting and
lence numbers carry sampling uncertainty and, as the families       the cooperative-frame theorem. Recent Scratch-specific work
are conservative by design, lower-bound what a sound tool           has broadened this stack from static analysis and testing
could accept. The player lens approximates perceived behavior       to multimodal feedback, tutoring, benchmarking, repair, as-
by frames, sounds, prompts, monitors, and termination, not          sessment, and equivalence: ViScratch uses code and game-
exact pixels or audio. We analyze only public project JSON          play video for feedback [42], Stitch studies stepwise tutor-
and include no personal content.                                    ing [43], ScratchEval packages executable repair tasks and
                                                                    metrics [44], EcoScratch studies cost-aware multimodal re-
                    IX. R ELATED W ORK                              pair [45], Raven uses video-grounded evaluation for assess-
   CertiBlock adopts the trusted-boundary discipline of ver-        ment [46], ScratchWorld evaluates executable consequences in
ified compilation and the per-run stance of translation vali-       Scratch worlds [47], and ScratchLens makes behavioral equiv-
dation, and applies them to a concurrent end-user language.         alence lens-parametric [16]. Broader programming-education
CompCert proves a fixed compiler correct once over small-           and software-analysis work by Zhang and collaborators studies
step semantics with explicit event traces [3], [4], CakeML          feedback for competition-level code, LLM-based Python re-
extends a single top-level correctness theorem across a whole       pair, time-limit-exceeded errors, merge-conflict resolution, CI-
verified pipeline [17], and later work carries verification into    configuration correctness, and silent misconfiguration detec-
separate compilation and the surrounding program logic [18],        tion [48]–[53]. These systems motivate reliable feedback, re-
[19]. CertiBlock keeps the optimizer outside the trusted base       pair, and analysis pipelines; CertiBlock addresses the comple-
and checks each rewrite, so the optimizer evolves without           mentary trust question of accepting source-to-source Scratch
re-verification. Translation validation validates each output       transformations only when a small checker can recompute
against its input [5], [6], [20], [21], and Alive2 frames the       certificate claims.
relation as one-directional refinement for LLVM [7]. A valida-         Closest are two Scratch refactoring systems: quality-driven
tor can itself be proved correct once and then trusted on every     refactorings behind editor preconditions [8] and search-based
run [22], [23], which is the stance CertiBlock takes for its        readability transformations validated by generated tests [9].
checker. CertiBlock formalizes the optimizer-to-checker chan-       Both establish behavior preservation through analysis and
nel as a certificate whose claims the checker recomputes, and       testing; Table VI places CertiBlock against them as the only
its refinement is observational under a lens over the schedules     one to make each accepted rewrite certificate-carrying, with a
of a cooperative runtime, where the schedule envelope is part       recomputing checker and a mechanized theorem, for this end-
of the trusted semantics.                                           user setting [54]. The optimizer follows the search-based and
   The closest technical neighbors prove local conditions that      equality-saturation tradition [13], [14], [55]–[58], the edits are
imply global correctness. The Peek framework discharges             graph rewrites [15], and the frame condition adapts separation
global semantic preservation by checking local properties per       reasoning [59]–[61] to a cooperative scheduler.
assembly peephole [24], and Alive proves rewrites correct at
authoring time over sequential IR [25]. CertiBlock checks                                  X. C ONCLUSION
each applied rewrite at acceptance time over a concurrent              CertiBlock shows that optimization of a concurrent, event-
observation semantics, and its locality is a frame condition        driven, end-user language can carry a behavior-preservation
over a cooperative scheduler rather than a liveness fact over a     guarantee: an untrusted optimizer proposes, an auditable
                            TABLE VI                                             [17] R. Kumar, M. O. Myreen, M. Norrish, and S. Owens, “CakeML:
    T RUST MODEL OF S CRATCH PROGRAM TRANSFORMATION . O NLY                           A verified implementation of ML,” in Proc. ACM SIGPLAN-SIGACT
 C ERTI B LOCK MAKES EACH ACCEPTANCE CERTIFICATE - CARRYING WITH                      Symp. Principles of Programming Languages (POPL), 2014, pp. 179–
                      MECHANIZED SOUNDNESS .                                          192.
                                                                                 [18] G. Stewart, L. Beringer, S. Cuéllar, and A. W. Appel, “Compositional
   System               Analysis    Tests    Cert. checker    Mech. thm.              CompCert,” in Proc. ACM SIGPLAN-SIGACT Symp. Principles of
                                                                                      Programming Languages (POPL), 2015, pp. 275–287.
   QIS [8]                 ✓                                                     [19] A. W. Appel, “Verified software toolchain,” in Proc. European Symp.
   Search-based [9]        ✓          ✓                                               Programming (ESOP), ser. LNCS 6602, 2011, pp. 1–17.
   CertiBlock              ✓          ✓            ✓               ✓             [20] L. Zuck, A. Pnueli, Y. Fang, and B. Goldberg, “VOC: A methodology for
                                                                                      the translation validation of optimizing compilers,” Journal of Universal
                                                                                      Computer Science, vol. 9, no. 3, pp. 223–247, 2003.
checker disposes under an explicit lens, and the dead-store core                 [21] C. Barrett, Y. Fang, B. Goldberg, Y. Hu, A. Pnueli, and L. Zuck, “TVOC:
                                                                                      A translation validator for optimizing compilers,” in Computer Aided
is backed by a mechanized cooperative-frame theorem with a                            Verification (CAV), ser. LNCS 3576, 2005, pp. 291–295.
verified-executable Lean realization. On 300 real projects it                    [22] J.-B. Tristan and X. Leroy, “Formal verification of translation valida-
accepts a rewrite on 283, with no false accept, and rejects                           tors: A case study on instruction scheduling optimizations,” in Proc.
                                                                                      ACM SIGPLAN-SIGACT Symp. Principles of Programming Languages
every behavior-changing rewrite a model-free remover would                            (POPL), 2008, pp. 17–27.
ship.                                                                            [23] ——, “Verified validation of lazy code motion,” in Proc. ACM SIGPLAN
                                                                                      Conf. Programming Language Design and Implementation (PLDI),
                               R EFERENCES                                            2009, pp. 316–326.
                                                                                 [24] E. Mullen, D. Zuniga, Z. Tatlock, and D. Grossman, “Verified peephole
 [1] P. Techapalokul and E. Tilevich, “Understanding recurring quality prob-
                                                                                      optimizations for CompCert,” in Proc. ACM SIGPLAN Conf. Program-
     lems and their impact on code sharing in block-based software,” in IEEE
                                                                                      ming Language Design and Implementation (PLDI), 2016, pp. 448–461.
     Symp. Visual Languages and Human-Centric Computing (VL/HCC),
                                                                                 [25] N. P. Lopes, D. Menendez, S. Nagarakatte, and J. Regehr, “Provably
     2017, pp. 43–51.
                                                                                      correct peephole optimizations with Alive,” in Proc. ACM SIGPLAN
 [2] G. Robles, J. Moreno-León, E. Aivaloglou, and F. Hermans, “Software
                                                                                      Conf. Programming Language Design and Implementation (PLDI),
     clones in Scratch projects: On the presence of copy-and-paste in compu-
                                                                                      2015, pp. 22–32.
     tational thinking learning,” in IEEE Int. Workshop on Software Clones
                                                                                 [26] S. Lerner, T. Millstein, and C. Chambers, “Automatically proving the
     (IWSC), 2017, pp. 31–37.
                                                                                      correctness of compiler optimizations,” in Proc. ACM SIGPLAN Conf.
 [3] X. Leroy, “Formal verification of a realistic compiler,” Communications
                                                                                      Programming Language Design and Implementation (PLDI), 2003, pp.
     of the ACM, vol. 52, no. 7, pp. 107–115, 2009.
                                                                                      220–231.
 [4] ——, “A formally verified compiler back-end,” Journal of Automated
                                                                                 [27] M. Rinard, “Credible compilation,” Massachusetts Institute of Technol-
     Reasoning, vol. 43, no. 4, pp. 363–446, 2009.
                                                                                      ogy, Tech. Rep. MIT-LCS-TR-776, 1999.
 [5] A. Pnueli, M. Siegel, and E. Singerman, “Translation validation,” in
                                                                                 [28] K. S. Namjoshi and L. D. Zuck, “Witnessing program transformations,”
     Tools and Algorithms for the Construction and Analysis of Systems
                                                                                      in Static Analysis Symposium (SAS), ser. LNCS 7935, 2013, pp. 304–
     (TACAS), ser. LNCS 1384, 1998, pp. 151–166.
                                                                                      323.
 [6] G. C. Necula, “Translation validation for an optimizing compiler,”
                                                                                 [29] J. Kang, Y. Kim, Y. Song, J. Lee, S. Park, M. D. Shin, Y. Kim, S. Cho,
     in Proc. ACM SIGPLAN Conf. Programming Language Design and
                                                                                      J. Choi, C.-K. Hur, and K. Yi, “Crellvm: Verified credible compilation
     Implementation (PLDI), 2000, pp. 83–94.
                                                                                      for LLVM,” in Proc. ACM SIGPLAN Conf. Programming Language
 [7] N. P. Lopes, J. Lee, C.-K. Hur, Z. Liu, and J. Regehr, “Alive2: Bounded
                                                                                      Design and Implementation (PLDI), 2018, pp. 631–645.
     translation validation for LLVM,” in Proc. ACM SIGPLAN Conf. Pro-
                                                                                 [30] M. Stepp, R. Tate, and S. Lerner, “Equality-based translation validator
     gramming Language Design and Implementation (PLDI), 2021, pp. 65–
                                                                                      for LLVM,” in Computer Aided Verification (CAV), ser. LNCS 6806,
     79.
                                                                                      2011, pp. 737–742.
 [8] P. Techapalokul and E. Tilevich, “Code quality improvement for all:
                                                                                 [31] J. Ševčı́k, V. Vafeiadis, F. Zappa Nardelli, S. Jagannathan, and P. Sewell,
     Automated refactoring for Scratch,” in IEEE Symp. Visual Languages
                                                                                      “CompCertTSO: A verified compiler for relaxed-memory concurrency,”
     and Human-Centric Computing (VL/HCC), 2019, pp. 117–125.
                                                                                      Journal of the ACM, vol. 60, no. 3, pp. 22:1–22:50, 2013.
 [9] F. Adler, G. Fraser, E. Gründinger, N. Körber, S. Labrenz, J. Lerchen-
                                                                                 [32] G. C. Necula, “Proof-carrying code,” in Proc. ACM SIGPLAN-SIGACT
     berger, S. Lukasczyk, and S. Schweikl, “Improving readability of Scratch
                                                                                      Symp. Principles of Programming Languages (POPL), 1997, pp. 106–
     programs with search-based refactoring,” in IEEE Int. Working Conf.
                                                                                      119.
     Source Code Analysis and Manipulation (SCAM), 2021, pp. 120–130.
                                                                                 [33] G. Klein, K. Elphinstone, G. Heiser, J. Andronick, D. Cock, P. Derrin,
[10] J. Maloney, M. Resnick, N. Rusk, B. Silverman, and E. Eastmond, “The
                                                                                      D. Elkaduwe, K. Engelhardt, R. Kolanski, M. Norrish, T. Sewell,
     Scratch programming language and environment,” ACM Transactions on
                                                                                      H. Tuch, and S. Winwood, “seL4: Formal verification of an OS kernel,”
     Computing Education, vol. 10, no. 4, pp. 16:1–16:15, 2010.
                                                                                      in Proc. ACM SIGOPS Symp. Operating Systems Principles (SOSP),
[11] M. Resnick, J. Maloney, A. Monroy-Hernández, N. Rusk, E. Eastmond,
                                                                                      2009, pp. 207–220.
     K. Brennan, A. Millner, E. Rosenbaum, J. Silver, B. Silverman, and
                                                                                 [34] G. Berry and G. Gonthier, “The Esterel synchronous programming
     Y. Kafai, “Scratch: Programming for all,” Communications of the ACM,
                                                                                      language: Design, semantics, implementation,” Science of Computer
     vol. 52, no. 11, pp. 60–67, 2009.
                                                                                      Programming, vol. 19, no. 2, pp. 87–152, 1992.
[12] L. de Moura and S. Ullrich, “The Lean 4 theorem prover and program-
                                                                                 [35] N. Halbwachs, P. Caspi, P. Raymond, and D. Pilaud, “The synchronous
     ming language,” in Automated Deduction (CADE), ser. LNCS 12699,
                                                                                      data flow programming language LUSTRE,” Proceedings of the IEEE,
     2021, pp. 625–635.
                                                                                      vol. 79, no. 9, pp. 1305–1320, 1991.
[13] R. Tate, M. Stepp, Z. Tatlock, and S. Lerner, “Equality saturation: A
                                                                                 [36] T. Bourke, L. Brun, P.-É. Dagand, X. Leroy, M. Pouzet, and L. Rieg, “A
     new approach to optimization,” in Proc. ACM SIGPLAN-SIGACT Symp.
                                                                                      formally verified compiler for Lustre,” in Proc. ACM SIGPLAN Conf.
     Principles of Programming Languages (POPL), 2009, pp. 264–276.
                                                                                      Programming Language Design and Implementation (PLDI), 2017, pp.
[14] M. Willsey, C. Nandi, Y. R. Wang, O. Flatt, Z. Tatlock, and P. Panchekha,
                                                                                      586–601.
     “egg: Fast and extensible equality saturation,” in Proc. ACM SIGPLAN-
                                                                                 [37] E. Aivaloglou, F. Hermans, J. Moreno-León, and G. Robles, “A dataset
     SIGACT Symp. Principles of Programming Languages (POPL), vol. 5,
                                                                                      of Scratch programs: Scraped, shaped and scored,” in Proc. Int. Conf.
     2021, pp. 1–29.
                                                                                      Mining Software Repositories (MSR), 2017, pp. 511–514.
[15] H. Ehrig, K. Ehrig, U. Prange, and G. Taentzer, Fundamentals of
                                                                                 [38] E. Aivaloglou and F. Hermans, “How kids code and how we know:
     Algebraic Graph Transformation. Springer, 2006.
                                                                                      An exploratory study on the Scratch repository,” in Proc. ACM Conf.
[16] Y. Si and J. Zhang, “ScratchLens: Lens-parametric behavioral
                                                                                      International Computing Education Research (ICER), 2016, pp. 53–61.
     equivalence for Scratch programs,” 2026. [Online]. Available: https:
     //arxiv.org/abs/2606.15817
[39] B. Boe, C. Hill, M. Len, G. Dreschler, P. Conrad, and D. Franklin,        [51] J. Zhang, T. Mytkowicz, M. Kaufman, R. Piskac, and S. K. Lahiri,
     “Hairball: Lint-inspired static analysis of Scratch projects,” in Proc.        “Using pre-trained language models to resolve textual and semantic
     ACM Technical Symp. Computer Science Education (SIGCSE), 2013,                 merge conflicts,” in Proceedings of the 31st ACM SIGSOFT Interna-
     pp. 215–220.                                                                   tional Symposium on Software Testing and Analysis, ser. ISSTA 2022.
[40] C. Frädrich, F. Obermüller, N. Körber, U. Heuer, and G. Fraser,             ACM, 2022, pp. 77–88.
     “Common bugs in Scratch programs,” in Proc. ACM Conf. Innovation          [52] M. Santolucito, J. Zhang, E. Zhai, J. Cito, and R. Piskac, “Learning CI
     and Technology in Computer Science Education (ITiCSE), 2020, pp.               configuration correctness for early build feedback,” in Proceedings of the
     89–95.                                                                         2022 IEEE International Conference on Software Analysis, Evolution
[41] A. Stahlbauer, M. Kreis, and G. Fraser, “Testing scratch programs              and Reengineering, ser. SANER 2022. IEEE, 2022, pp. 1006–1017.
     automatically,” in Proc. ACM Joint European Software Engineering          [53] J. Zhang, R. Piskac, E. Zhai, and T. Xu, “Static detection of silent
     Conf. and Symp. Foundations of Software Engineering (ESEC/FSE),                misconfigurations with deep interaction analysis,” Proceedings of the
     2019, pp. 165–175.                                                             ACM on Programming Languages, vol. 5, no. OOPSLA, pp. 1–30, 2021.
[42] Y. Si, D. Li, H. Shi, and J. Zhang, “ViScratch: Using large language      [54] A. J. Ko, R. Abraham, L. Beckwith, A. Blackwell, M. Burnett, M. Erwig,
     models and gameplay videos for automated feedback in Scratch,”                 C. Scaffidi, J. Lawrance, H. Lieberman, B. Myers, M. B. Rosson,
     arXiv:2509.11065 [cs.SE], 2025.                                                G. Rothermel, M. Shaw, and S. Wiedenbeck, “The state of the art in
[43] Y. Si, K. Qi, D. Li, H. Shi, and J. Zhang, “Stitch: Step-by-step LLM           end-user software engineering,” ACM Computing Surveys, vol. 43, no. 3,
     guided tutoring for Scratch,” arXiv:2510.26634 [cs.SE], 2025.                  pp. 21:1–21:44, 2011.
[44] Y. Si, S. Han, D. Li, H. Shi, and J. Zhang, “ScratchEval: A multi-        [55] R. Joshi, G. Nelson, and K. Randall, “Denali: A goal-directed superop-
     modal evaluation framework for LLMs in block-based programming,”               timizer,” in Proc. ACM SIGPLAN Conf. Programming Language Design
     arXiv:2602.00757 [cs.SE], 2026.                                                and Implementation (PLDI), 2002, pp. 304–314.
[45] Y. Si, M. Wang, D. Li, H. Shi, and J. Zhang, “EcoScratch: Cost-           [56] S. Bansal and A. Aiken, “Automatic generation of peephole superop-
     effective multimodal repair for Scratch using execution feedback,”             timizers,” in Proc. Int. Conf. Architectural Support for Programming
     arXiv:2603.29624 [cs.SE], 2026.                                                Languages and Operating Systems (ASPLOS), 2006, pp. 394–403.
[46] D. Li, D. Li, H. Shi, and J. Zhang, “Raven: Rethinking auto-              [57] E. Schkufza, R. Sharma, and A. Aiken, “Stochastic superoptimization,”
     mated assessment for Scratch programs via video-grounded evaluation,”          in Proc. Int. Conf. Architectural Support for Programming Languages
     arXiv:2604.17820 [cs.SE], 2026.                                                and Operating Systems (ASPLOS), 2013, pp. 305–316.
[47] Y. Lin and J. Zhang, “ScratchWorld: Evaluating if world models compute    [58] C. Nandi, M. Willsey, A. Zhu, Y. R. Wang, B. Saiki, A. Anderson,
     executable consequences,” arXiv:2606.31689 [cs.SE], 2026.                      A. Schulz, D. Grossman, and Z. Tatlock, “Rewrite rule inference using
[48] J. Zhang, D. Li, J. C. Kolesar, H. Shi, and R. Piskac, “Automated              equality saturation,” Proc. ACM Program. Lang. (OOPSLA), vol. 5, pp.
     feedback generation for competition-level code,” in Proceedings of             1–28, 2021.
     the 37th IEEE/ACM International Conference on Automated Software          [59] J. C. Reynolds, “Separation logic: A logic for shared mutable data
     Engineering, ser. ASE 2022. ACM, 2022, pp. 13:1–13:13.                         structures,” in Proc. IEEE Symp. Logic in Computer Science (LICS),
[49] J. Zhang, J. P. Cambronero, S. Gulwani, V. Le, R. Piskac, G. Soares,           2002, pp. 55–74.
     and G. Verbruggen, “PyDex: Repairing bugs in introductory python          [60] P. W. O’Hearn, “Resources, concurrency, and local reasoning,” Theoret-
     assignments using LLMs,” Proceedings of the ACM on Programming                 ical Computer Science, vol. 375, no. 1–3, pp. 271–307, 2007.
     Languages, vol. 8, no. OOPSLA1, pp. 1100–1124, 2024.                      [61] M. Abadi and G. D. Plotkin, “A logical view of composition,” Theoret-
[50] J. Zhang, J. Gu, W. Zhang, J. P. Cambronero, J. C. Kolesar, R. Piskac,         ical Computer Science, vol. 114, no. 1, pp. 3–30, 1993.
     D. Li, and H. Shi, “A systematic study of time limit exceeded errors in
     online programming assignments,” arXiv:2510.14339 [cs.SE], 2025.
