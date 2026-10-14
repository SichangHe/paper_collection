                                                    ShannonProver: Towards Automating Formal Cryptographic Proofs

                                                                  Yiping Ma† , Yu-Lin Tsai† , Mayank Rathee† , Deevashwer Rathee† ,
                                                                    François Dupressoir‡ , Pierre-Yves Strub§ , Raluca Ada Popa†
                                                                             †                 ‡                              §
                                                                                 UC Berkeley       University of Bristol          PQ Shield


                                        Abstract—Cryptographic proofs are produced at a scale that            cryptographic proofs. If the check passes, the theorem that
                                        increasingly exceeds the community’s ability to verify them           the script proves is certified without any expert examining
arXiv:2607.02847v3 [cs.CR] 3 Oct 2026




                                        manually. Machine-checked proofs offer a path toward scalable         the argument by hand. However, the bottleneck shifts to
                                        proof verification, but they shift the bottleneck to writing          producing the proof script in the first place.
                                        the proofs themselves: even when the high-level proof plan                Writing such proof scripts is far more exacting than
                                        is known, turning it into a proof script requires spelling out        writing traditional pen-and-paper proofs: a machine-checked
                                        every detail the plan leaves implicit, which is laborious even        proof is not a line-by-line translation of a pen-and-paper
                                        for experts. This paper presents ShannonProver, an agentic            proof; rather, it expands the cryptographer’s shorthand of
                                        system for automating cryptographic proofs. Given a protocol          a cryptographic argument (e.g., “two games are indistin-
                                        and its security definitions modeled by a cryptographer, Shan-        guishable”) into explicit stateful programs and precisely
                                        nonProver decomposes the main theorem into intermediate               reasons about the program equivalence. Historically, devel-
                                        games and lemmas, and constructs EasyCrypt proof scripts              oping formal proofs for standardized schemes such as MEE-
                                        for those lemmas.                                                     CBC [19], CMAC [20], and ChaCha20-Poly1305 [21] has
                                            We evaluate ShannonProver on a new dataset of lemmas              required several person-weeks to several person-months1 ,
                                        in EasyCrypt. The benchmark spans textbook primitives, de-            and the effort for recent post-quantum NIST standards such
                                        ployed standardized protocols, as well as recent NIST pro-
                                                                                                              as ML-KEM [13,22] is even larger, involving more than 10
                                                                                                              experts for one or two years.
                                        posals, and includes expert case studies drawn from a corpus
                                                                                                                  This effort raises a natural question: can experts dele-
                                        that has not previously been available online. On case stud-
                                                                                                              gate writing these proof scripts to LLM agents? Machine-
                                        ies such as ChaChaPoly1305 and MEE-CBC, ShannonProver
                                                                                                              checked proofs make such delegation safe: the agent per-
                                        completes within hours proof developments that historically
                                                                                                              forms the proof search, which may be heuristic, while
                                        took experts weeks to months. More broadly, this work suggests
                                                                                                              EasyCrypt performs the proof checking, which is sound.
                                        a path toward accelerating cryptographic research: as agents          The agent may hallucinate or make mistakes along the way,
                                        automate the proof-engineering burden, cryptographers can             but this cannot compromise soundness: EasyCrypt rejects
                                        iterate more quickly on new constructions, obtain machine-            every invalid proof attempt, so once the agent produces a
                                        checked assurance earlier, and bring protocols from design to         script that passes the check, the theorem is certified.
                                        deployment faster.                                                        The most direct approach to this question is to ask the
                                                                                                              agent to write the entire proof through checker-in-the-loop
                                        1. Introduction                                                       interaction [23,24]: the agent receives the specification of
                                                                                                              the scheme and the statement of the main theorem, submits
                                            Cryptographers “generate more proofs than we carefully            tactics to EasyCrypt, receives the resulting goal or error, and
                                        verify”, as Halevi observed two decades ago [1]. This                 repeats until the theorem is proved. While this approach
                                        concern is even more pressing today. Modern cryptographic             suffices for simple textbook schemes (e.g., ElGamal), it
                                        protocols are increasingly complex, their proofs are longer           falls far short of our target: formal proofs at the scale and
                                        and more intricate, and their correctness has consequences            complexity of NIST standards and proposals. We observed
                                        far beyond research papers: they have become standards [2–            that even strong LLMs fail on such proofs. They sometimes
                                        5], libraries [6–9], and security infrastructure [5,10–12].           re-prove facts they have already established or drift to the
                                        Flaws discovered after publication or even standardization            wrong level of abstraction; as a result, their proofs grow far
                                        underscore the same point [13,14]: the community cannot               longer than necessary, or they eventually give up.
                                        manually scrutinize cryptographic proofs at the same scale                Experts do not develop such proofs monolithically. They
                                        at which it produces them.                                            proceed in three phases (Fig. 1): they first write the specifi-
                                            Machine-checked proofs offer a way to scale proof                 cation, which formalizes the scheme, its security definitions,
                                        verification. Here, a proof is written as a proof script, a
                                                                                                                 1. The exact historical effort for the ChaChaPoly development is no
                                        sequence of commands called tactics, and a proof assis-               longer recoverable; the person-month estimate is based on the size and
                                        tant [15–17] checks the script mechanically. This work uses           complexity of the current proof relative to comparable projects with known
                                        EasyCrypt [18], a proof assistant designed for game-based             effort.



                                                                                                          1
and the underlying assumptions (Phase I), then decompose
                                                                                       PHASE I • SPECIFICATION                                               HUMAN EXPERT
the main theorem into intermediate games and lemmas                                    module type IVScheme = {                      module CBC(P : PseudoRP) = {
(Phase II), and finally prove each lemma with a tactic-                                   proc keygen() : key                           proc enc(key,iv,p) = { ... }
                                                                                          proc enc(k,iv,p) : block list              }.
level proof script (Phase III). Phase II requires cryptographic                           proc dec(k,c) : ...
insight and high-level planning, whereas Phase III is tedious                          }.

and demands exacting, mechanical proof writing. The two
phases are not sequential: whether a decomposition works is                            PHASE II • DECOMPOSITION                                                DECOMPOSER
                                                                                       lemma cleanup &m : Pr...                      lemma Bound_by_PRP_PRF &m : ...
often known only after trying to prove its lemmas. Experts                             lemma CBC_PRP_RF &m : ...                     lemma Bound_by_Birthday &m : ...
therefore move back and forth between the two phases until                             lemma CBC_upto &m : ...




                                                                       ShannonProver
                                                                                                                                     lemma Conclusion (A) &m : ...




                                                                                                                                                                                     feedback
every lemma is proved. This process is costly: the original                                                                      lemmas

MEE-CBC proof took experts a few person-weeks, and the                                 PHASE III • LEMMA PROVING                                             LEMMA PROVER

ChaCha20-Poly1305 proof a few person-months.                                           proof.
                                                                                         byequiv=> //=. proc. call (_: ={bad,qs}(DoubleQuery,Compute)).
    In this work, we develop ShannonProver, an agentic                                   by conseq DQ_Sample_Compute_eq. by inline *; auto.
                                                                                       qed.
system that follows this workflow to automate Phases II
and III. It has two components, both built on LLM agents
(Fig. 2): a decomposer for Phase II and a lemma prover                Figure 1. The three phases of a formal proof development. A human
for Phase III. The decomposer works at the level of the               expert writes the specification (Phase I), and ShannonProver automates
whole proof: it writes the intermediate games and lemma               decomposition (Phase II) and lemma proving (Phase III).
statements, and hands individual lemmas to the lemma
prover. The lemma prover proves each lemma by interacting                        Decomposer      games G1–G3;
                                                                                                                   prove L3 itself
                                                                                                                                          split L4 into L4a, L4b;
                                                                                                                                             prove L4b itself
                                                                                                                                                                       assemble proof;
                                                                                                                                                                    final EasyCrypt check
                                                                                    (Phase II)   lemmas L1–L4
with EasyCrypt tactic by tactic. If it succeeds, it returns a
verified proof script; otherwise, it returns feedback, which          Lemma prover                                     L1 ✓                        L2 ✓
the decomposer uses to revise or split the lemma, or to                  (Phase III,
                                                                           two jobs
restructure the decomposition. Because the decomposer can                 at a time)
                                                                                                                        L4 ✗                        L4a ✓

launch the lemma prover on several independent lemmas                                                                                                                               time
at once, ShannonProver greatly reduces the time needed to
test whether a decomposition actually works. Given only               Figure 2. Interleaving of Phases II and III in ShannonProver. Solid arrows
the specification and the main theorem, ShannonProver con-            hand a lemma to the lemma prover; dashed arrows return the result, either a
structs complete proofs for MEE-CBC in 2 hours and for                proof (✓) or feedback (✗). The decomposer does not wait for results: while
                                                                      L1 and L4 are being attempted, it proves L3 itself. When the attempt on
ChaCha20-Poly1305 in about 5 hours.                                   L4 fails, the decomposer splits L4 into L4a and L4b. Two jobs run at a
    This workflow hinges on the lemma prover: a decom-                time here for illustration; the number of concurrent jobs is configurable.
position can be tested only as quickly and as reliably as its
lemmas are proved. Yet even on a single lemma in Phase III,
the checker-in-the-loop approach can fail when the lemma              only much later that it has led to a dead end. A single agent
is difficult or tedious. These failures have two sources: the         explores one path at a time, and it often fails to notice when
agent lacks the context relevant to each step of the proof, and       to turn back: it keeps trying variants of the same failing
it explores the proof along a single linear path. The lemma           move instead of returning to where its strategy went wrong.
prover addresses them with two design ideas: a proof-state            The lemma prover therefore organizes the search as a tree of
compiler and multi-agent tree search.                                 checker-accepted proof states (Fig. 6). Agents can backtrack
                                                                      within their own branches, and a deterministic orchestrator
❶ Proof-state compiler (§3). The context an agent needs               oversees all branches: when an agent stalls, it starts a fresh
changes with every tactic. Each tactic transforms the proof           agent on a different branch, prunes branches that no longer
state, and with it which proof resources apply (previously            make progress, and records dead ends so that no agent retries
proved lemmas, assumptions, and hypotheses; App. A.1) and             a failed approach at the same state. Each agent reasons about
how their arguments must be instantiated (left in Fig. 4). An         its own branch; the orchestrator decides where the search
agent can recover this context only by rereading the project          should go.
files after every tactic, which is slow; when it misses some-             We view this work as a first step toward automating
thing, it often switches to a worse strategy or gets stuck. Yet       formal proofs for cryptography. Ultimately, we hope Shan-
this context is fully determined by the current state and the         nonProver will let experts focus on the critical judgments
project: the agent need not rediscover it, because it can be          in formal verification, while automating as much of the
computed. Much as a compiler resolves names and types so              remaining work as possible.
that programmers need not, the proof-state compiler (right
in Fig. 4) analyzes each new state and shows the agent the            2. Design Overview
resources that apply, with their arguments instantiated. The
agent keeps every strategic decision; the compiler takes over
the bookkeeping.
                                                                      2.1. Observations in Agentic Proving
❷ Multi-agent tree search (§4). A proof rarely proceeds                   We observe the failures below in baseline runs, where
in a straight line: a step that looks reasonable may reveal           the agent interacts directly with EasyCrypt (left in Fig. 4).


                                                                  2
They fall into the two groups identified in §1: the agent                                                          ❷ Semantic mislocalization. An agent can choose a resource
lacks the context relevant to each step of the proof, and it                                                       that does not apply. This is not simply a lack of information:
explores the proof along a single linear path.                                                                     the proof context may contain the right clues, but the agent
Missing context. At every step, the agent must decide which                                                        can be pulled toward the wrong resource by names that
proof resources apply, which one to use, and how to apply                                                          appear in the goal or by the literal wording of an error
it. Making this decision requires assembling information                                                           message. For example, in one run, a goal mentioning IFinRO
scattered across project lemmas, imported theories, module                                                         and IndRO led the agent to treat these names as evidence for
arguments, and even the source code of the proof checker.                                                          an eager/lazy random-oracle lemma and to spend the rest of
When the agent lacks this information, we observe three                                                            the run trying to fit pr_RO_FinRO_D, which is unrelated to
recurring failure patterns, each at a different point of this                                                      the proof (App. D).
decision: the agent misses a resource that applies, chooses                                                        ❸ Agent flinch. An agent can choose the right resource and
one that does not, or cannot apply the one it has chosen.                                                          still fail to apply it. Applying a lemma means turning the
❶ Unconscious lowering. A proof often moves across sev-                                                            choice into a command that EasyCrypt accepts: looking up
eral abstraction levels (Fig. 3): from probability algebra and                                                     the lemma’s exact statement, supplying its module argu-
pRHL equivalences, to module or oracle calls, procedure                                                            ments, matching types, and finding the right tactic form.
bodies, and finally SMT side conditions. Higher levels let                                                         When this information is available only through trial and
the prover reuse facts already proved about whole games,                                                           error with the checker, the agent often abandons the plan
modules, or oracle behaviors. Human experts descend to a                                                           after a few rejected attempts and switches to a tactic that
lower level only when the proof really needs more concrete                                                         is easier to write, even if it leads to a worse proof state
program structure, guided by experience and by the intuition                                                       (App. D). The failure is not the absence of a proof idea, but
they gained from lemma decomposition (Phase II); an LLM                                                            the cost of carrying it out.
agent has to make this judgment after every tactic. The agent                                                      Exploring a single path. Even with the right context at
can mistakenly interpret a local but unhelpful goal change                                                         every step, a tactic that EasyCrypt accepts can lead the
as real proof progress. In the baseline runs, a tactic such                                                        proof into a dead end that becomes visible only many steps
as inline* is very tempting because it is easy to write                                                            later. The agent must therefore also decide when to abandon
and immediately produces a different-looking goal. What                                                            its current strategy and where to resume. Even an agent
the agent does not see is that this change may cut off                                                             that can return to an earlier state often does not notice
resources that are usable at the higher level: a lemma stated                                                      when it should: it stays at a state and keeps submitting
about a procedure call, such as an equivalence between                                                             variants of the same failing move, or keeps repairing a
two oracle implementations, applies only while that call                                                           branch whose strategy no longer works, instead of returning
is still visible in the goal; once the call is inlined, the                                                        to the point where the strategy went wrong. And when it
lemma no longer matches (App. D). The agent must then                                                              does backtrack, it pursues one strategy at a time, so several
either reprove from scratch what the lemma would have                                                              plausible strategies can only be tried one after another. These
established, or keep pursuing the original plan that relied                                                        failures do not come from a single wrong step, but from the
on the lemma but can no longer succeed from this state.                                                            lack of any view of the search as a whole.
The failure is not that the agent chose to descend; descent
is often necessary. The failure is that the interface gives no                                                     2.2. Design Ideas
state-aware information when a locally productive-looking
move is globally destructive.
                                                                                                                   Proof-state compiler. The three failure patterns point to
                                                                                                                   an interface problem: the agent must reconstruct, through
                                                       semantic / proof-structure level
                                                                                                                   ad hoc queries such as Grep and Read, proof context that
                                                                                          program structure
                                    Pr expression algebra         rewrite, congr
                                                                                                 preserved         is already determined by the current proof state and the
                          byequiv
                                                                                          program structure
                                                                                                                   project. ShannonProver instead computes this context deter-
                                pRHL program equivalence          sim, conseq
                         proc
                                                                                                 preserved         ministically with a proof-state compiler (§3, Fig. 4). At each
                                                                                            call abstraction       proof state, the compiler takes as input the checker’s output,
lowering




                          Module-level call                       call (_: Inv)
                                                                                                  preserved
              inline f                                                                                             the proof history, and the project context, including source
                      Procedure instructions                      wp, rnd, sp
                                                                                            procedure body
                                                                                                  exposed
                                                                                                                   files, imported theories, module definitions, and available
           inline *                                                                                                lemmas. Its output addresses the three failure patterns in
                                                                                            all abstractions
                  All-modules expansion                           wp, rnd, sp
                                                                                                  expanded         turn: it shows which resources still apply at the current
           skip
                                                                                               atomic goal         state, so that the agent does not lower past them; it matches
           Atomic / SMT discharge                                 smt(), auto
                                                                                               discharged          resources against the goal by structure rather than by name;
                                       syntactic / verification-condition level                                    and once the agent selects a resource, it fills in the arguments
                                                                                                                   and premises that the current state determines, so that the
Figure 3. The tactic pyramid: abstraction levels in an EasyCrypt proof,
from probability expressions down to SMT goals. Each level lists the tactics
                                                                                                                   agent can carry its plan through. These outputs are facts
used within it; each arrow between two levels is labeled with the tactic that                                      about the current proof state, not a proof strategy: the agent
moves the proof down. Lowering exposes program detail but can invalidate                                           still decides which proof operation and resource to use next.
resources that apply only at higher levels.                                                                        The compiler’s analyses follow classical compiler design,


                                                                                                               3
which builds an intermediate representation, resolves names           In particular, the compiler never replaces the agent’s choices.
and types, tracks which facts remain valid, and reports               Changing the proof strategy is also the agent’s decision;
diagnostics [25]; Fig. 5 shows its three layers.                      Section 4 describes the backtracking that supports it.
Multi-agent tree search. Neither failure of single-path               Running example. We use a simple losslessness proof
exploration can be fixed inside one agent: an agent that              throughout this section to illustrate our design (Fig. 4).
does not notice when to turn back cannot be relied on to              The goal is to prove that the procedure D2(O).distinguish,
turn back, and a single agent can pursue only one strategy            shown below in simplified form, is lossless:
at a time. ShannonProver therefore organizes the search as
                                                                      proc D2(O).distinguish() = {
a tree of checker-accepted proof states (§4, Fig. 6). Each
                                                                        D2(O).O.init();
agent can backtrack within its own branch, which handles
                                                                        b <@ Adv_MAC_to_F(A, D2(O).O).guess();
the wrong turns it recognizes. A deterministic orchestrator
                                                                        return b;
watches the progress of all branches and handles the rest:
                                                                      }
when an agent stalls, it starts a fresh agent on a different
branch, and because several branches run at once, plausible           Elsewhere in the project, the following lemma has been
strategies are tried in parallel rather than one after another.       proved:
It also prunes branches that fall behind and records the
                                                                      lemma Alossless_F (X <: PRF_Oracles) :
attempts that failed.
                                                                        islossless X.f =>
                                                                        islossless Adv_MAC_to_F(A, X).guess.
3. Proof-State Compiler
                                                                      After opening the procedure with proc, the agent correctly
                                                                      decides to use the proof operation call with the resource
     Writing an EasyCrypt proof requires two kinds of work.           Alossless_F, but submits call (Alossless_F _ _). Easy-
First, the prover makes a strategic choice: it selects a proof        Crypt rejects the command because it cannot infer the
operation and the proof resources with which to carry out             module argument. The intended step should be realized as
that operation. By a proof operation we mean a kind of proof
step rather than one specific command: for example, using a                call (Alossless_F (<: D2(O).O) _).
lemma about a procedure call (call, ecall), rewriting with
                                                                          In the agent’s attempt, the first hole is a module argu-
an equation (rewrite), or turning a probability statement
                                                                      ment, which the current state determines. The second hole
into a program equivalence (byequiv). The same operation
                                                                      is a premise of the lemma. The compiler fills it only if the
can be written with different tactics and tactic forms. A
                                                                      current proof context already has a hypothesis stating that
proof resource is something the proof can use instead of
                                                                      premise; otherwise the premise is a new proof obligation
reasoning from scratch, such as a lemma already proved in
                                                                      that requires semantic reasoning, and it is left to the agent.
the project or in a library, an axiom of the specification, or
a hypothesis in the current proof. Which resources can be             Design overview. Our compiler is organized into three
used changes as the proof proceeds (App. A.1). Second, the            layers (Fig. 5). The first layer, state projection (§3.1), de-
prover must realize that choice as an EasyCrypt command               termines which proof state the agent is working on; all
that is valid at the exact current proof state. This requires         later analysis refers to this state. The second layer, ProofIR
resolving names and modules, supplying the appropriate                (§3.2), parses the current goal into a typed representation,
arguments, and using the correct tactic form.                         together with the proof operation and resource of the agent’s
     The first kind of work is strategic: it requires proof           attempt, if there is one. The third layer, resource and binding
insight, that is, semantic reasoning about what the programs          analysis, uses these results in one of two ways, depending
and statements mean. The second is mechanical: it is often            on whether the agent has already selected a resource. If it
determined by the syntactic form of the current goal and              has not, resource exposure (§3.3) finds the resources that
of the selected resource, and therefore changes with every            apply at the current state and shows them to the agent. If
proof state. Repeatedly working on such details through               it has, binding analysis (§3.4) realizes the agent’s intended
trial and error consumes reasoning budget on work that can            step.
instead be performed deterministically. More importantly,
we observed that these low-level failures can cause an agent          3.1. State Projection: Where am I in the proof?
to abandon an otherwise correct high-level plan and fall back
to a worse proof strategy, as in the agent flinch of Section 2.           Writing a formal proof for a lemma is often highly local.
     We therefore separate strategic choices from their me-           At each step, the information needed to construct the next
chanical realization. Concretely, the agent chooses the proof         tactic sequence is often specific to the current proof state. An
operation, the proof resource, and any other arguments that           accepted tactic advances the proof to a new state, a rejected
require proof insight, such as an invariant. The proof-state          tactic reports an error while leaving the state unchanged, and
compiler then realizes the agent’s intended step: it keeps            an undo restores an earlier state. Consequently, the interac-
the proof operation and resource that the agent chose, fills          tion transcript between the agent and EasyCrypt interleaves
in what the current state determines, and uses the tactic form        goals, error messages, and analyses associated with different
that EasyCrypt expects; everything else is left to the agent.         proof states.


                                                                  4
 Without the compiler                                                                        With the proof-state compiler

                                           tactic                                                            attempt                             tactic
  LLM agent                                                                                   LLM agent                    Proof-state
                                                                             EasyCrypt                                                                      EasyCrypt
                                                                                                                            compiler
                                 goal or error                                                                   view                                goal
           agent searches and reads                                                                                                 compiler input

   project files                                                                                                            project files

 What the agent sees                                                                         What the agent sees

   Goal after proc                                                                             Goal after proc                                                  §3.1
      D2(O).O.init();                                                                           D2(O).O.init();
      b <@ Adv_MAC_to_F(A, D2(O).O).guess();                                                    b <@ Adv_MAC_to_F(A, D2(O).O).guess();

   The agent’s attempt                                                                         Applicable resources                                             §3.3
      call (Alossless_F _ _).                                                                   Alossless_F matches the call to guess
      ✗ rejected: EasyCrypt cannot infer the module argument                                      X := D2(O).O
                                                                                                  premise: islossless D2(O).O.f

   What the agent must do next                                                                 Realized tactic, after the agent selects Alossless_F             §3.4
    find the module argument, the premise, and the tactic form                                  call (Alossless_F (<: D2(O).O) _).       ✓ submitted to EasyCrypt
    by searching the project files and retrying                                                   new subgoal: islossless D2(O).O.f


Figure 4. One step of the running example without (left) and with (right) the proof-state compiler. Left: the agent’s attempt call (Alossless_F _ _).
is rejected because EasyCrypt cannot infer the module argument, and the agent must search the project files to recover it. Right: the compiler shows the
resources that apply at the current state, with their arguments instantiated (§3.3); once the agent selects Alossless_F, the compiler realizes the tactic and
submits it (§3.4). The agent chooses the resource; the compiler fills in only what the state determines and leaves the lemma’s premise to the agent as a
new subgoal.


   INPUT current EasyCrypt state and project files                                           example, should not become a general statement that a tactic
            optional agent choice: proof operation + resource + other arguments              or resource is unusable.
                                                                                                 Long-term reasoning is not the compiler’s job. The agent
          State projection
  1       Attach goals, errors, and derived facts to the current state.                      keeps its overall plan and the proof strategy it is following,
          output: a view of the current state; facts from other states are not shown         and the proof tree of Section 4 records which alternatives
                                                                                             have already failed. State projection only ensures that the
          ProofIR
  2       Parse the goal and the agent’s attempt into a typed representation.                proof facts presented by the compiler describe where the
          output: typed goal and program; the role of each missing argument                  agent is now.
          Resource and binding analysis                                                      Running example. After the agent runs proc, the goal shows
          Depends on whether the agent has selected a resource.
                                        Match available resources to the
                                                                                             the body of D2(O).distinguish. The rejected attempt call
            Resource exposure
                                        current goal or program.                             (Alossless_F _ _). does not change the proof state, so its
            no resource selected
                                        output: all matching resources,                      error is attached to the state after proc, and the compiler
                                        instantiated at the current state
  3                                              agent selects a resource
                                                                                             analyzes that same state. If the agent later undoes proc or
            Binding analysis            Fill arguments and premises fixed by                 moves to a different state, this error is no longer shown as
                                        the state; EasyCrypt elaborates.
            resource selected                                                                if it described the new state.
                                        output: one realized tactic (submitted),
                                        or an explanation or a list of completions

                                                                                             3.2. ProofIR: How to interpret the state?
Figure 5. The three compiler layers. The third layer either shows the agent
the resources that match the current state or realizes a resource that the                       Once the current state is fixed, the compiler must de-
agent has already selected.                                                                  termine what part of the agent’s proof attempt is already a
                                                                                             strategic choice and what part is an incomplete mechanical
                                                                                             detail. Raw tactic syntax does not make this distinction
    We do not ask the agent to keep the history. Instead, the                                explicit. An underscore in an EasyCrypt term, for example,
compiler maintains a state-centered view consisting of the                                   may stand for a module parameter, a value argument, or
current goal together with information derived specifically                                  an unresolved proof premise. Treating all of these simply
for that state. When the proof advances or returns to an                                     as “missing syntax” would give the compiler no principled
earlier state, the view is recomputed for that state.                                        way to decide what it may fill in.
    This design serves two purposes. First, it removes book-                                     ProofIR makes these roles explicit. For each proof at-
keeping from the agent: the agent does not need to determine                                 tempt of the agent, it records three kinds of information:
which parts of a long transcript are still relevant. Second,                                 ❶ The current goal and relevant program structure.
it prevents stale information from silently influencing later                                ❷ The proof operation and proof resource selected by the
proof decisions. An error produced before an undo, for                                       agent.


                                                                                         5
❸ The typed parameters of that resource, including which              (Adv_MAC_to_F), that the module arguments already present
arguments were supplied and which remain unresolved.                  are the same (A), and that the remaining module parameter X
    If the agent has not submitted an attempt, ProofIR                can be instantiated with the concrete module D2(O).O from
records only the first kind of information, which resource            the current state.
exposure (§3.3) uses.                                                 ❸ The compiler shows the agent each matching resource,
    ProofIR turns an informal failure such as “this command           with its statement instantiated at the current state, including
did not elaborate” into a precise state-dependent question            the premises that remain to be proved. Here, the agent is
about the proof operation and resource that the agent has             shown Alossless_F with
already selected.                                                     premise   : islossless D2(O).O.f
Running example. The ProofIR layer parses the agent’s at-             conclusion: islossless
tempt call (Alossless_F _ _). It records that the requested                         Adv_MAC_to_F(A, D2(O).O).guess
proof operation is call and the selected resource is a lemma
Alossless_F. It parses the lemma as                                   If several resources match, the compiler shows all of them,
                                                                      without ranking them, and the agent chooses. Once the agent
module param     : X                                                  selects a resource, binding analysis (§3.4) completes the
module type      : PRF_Oracles                                        tactic.
premise          : islossless X.f
conclusion       : islossless Adv_MAC_to_F(A, X).guess                3.4. Binding Analysis: How should I execute?
In this representation, the role of each missing argument
in the agent’s attempt is explicit: the first hole asks for                Binding analysis handles the case in which the agent
a module instantiation; the second asks for a proof of a              has selected a proof operation and a resource, either on
losslessness premise. This layer only parses: it does not fill        its own, as in the running example, or from those shown
either hole or assert that the lemma applies. It makes explicit       by resource exposure. It realizes the agent’s intended step.
what binding analysis (§3.4) must relate.                             This addresses agent flinch (§2): the agent has chosen the
                                                                      right resource but cannot turn the choice into a command
                                                                      that EasyCrypt accepts. We allow the compiler to fill an
3.3. Resource Exposure: What can I use?                               argument only when that argument is determined by the
                                                                      selected proof operation, the selected resource, and the
     Resource exposure handles the case in which the agent            current proof state. The analysis proceeds in three steps.
has not yet selected a resource. This addresses unconscious           ❶ It determines where the attempted proof operation ap-
lowering and semantic mislocalization (§2), in which the              plies in the current state and checks whether the selected
agent misses a resource that applies or chooses one that              resource applies there. This applicability is inherently state-
does not. For example, after a procedure body is opened,              dependent: a lemma about a procedure call, for example, can
the goal shows a procedure call, but it does not show which           be used only while the corresponding call is still visible in
existing lemmas can be used at that call.                             the goal; after the procedure is inlined or the proof moves
     The compiler therefore finds resources that are struc-           past that call, the same lemma may no longer apply (the
turally applicable. This matching is syntactic: the compiler          unconscious lowering of §2; Fig. 3).
compares the form of the current goal with the form of                ❷ When the selected resource does apply, the compiler
each resource’s statement, rather than by the similarity of           uses its typed structure to determine missing arguments.
names or text. Because the matching is syntactic, we do it            Module parameters, procedure parameters, or other bindings
deterministically instead of using an LLM. It proceeds in             can often be read off by comparing the resource with the
three steps.                                                          program object to which it is being applied. A premise of
❶ The compiler finds the objects in the current goal against          the resource is filled only if a hypothesis in the current
which resources can be matched, such as procedure calls.              proof context states exactly that premise. This is mechanical:
In the running example, after the proof operation proc                the agent has chosen the resource, and the hypothesis is
and before the agent submits any call, the goal contains              determined by the premise. Otherwise the premise is left
the two statements of the procedure body shown above.                 as a hole, because it is a new proof obligation. Finally, the
The last statement is the procedure call Adv_MAC_to_F(A,              compiler writes the instantiated resource in the form that
D2(O).O).guess, which is where a lemma about a call can               the proof operation expects (for example, marking a module
be applied with call.                                                 argument with <:).
❷ The compiler finds the resources available in the current           ❸ The compiler asks EasyCrypt to elaborate the instantiated
file and its imports (App. A.1) whose statements match that           term. If elaboration fails, the proposed binding is discarded;
call:                                                                 the compiler does not substitute a different resource. If
                                                                      this yields exactly one tactic, the compiler submits it to
resource     :      Adv_MAC_to_F(A, X       ).guess
                                                                      EasyCrypt. Otherwise, it tells the agent why no tactic was
current call :      Adv_MAC_to_F(A, D2(O).O ).guess
                                                                      produced, for example that the selected resource does not
It checks that the procedure names are the same                       apply at the current state; if several completions are possible,
(guess), that the enclosing module application is the same            it lists them and lets the agent choose.


                                                                  6
Running example. As in §3.3, comparing the call                           (a)        parallel start                     (b)      backtrack
                                                                                                        initial state
Adv_MAC_to_F(A, D2(O).O).guess with the statement of the
selected lemma determines the module argument uniquely                                                                                                      undo


as X := D2(O).O, which leaves the premise islossless
                                                                                 Agent 1                      Agent 2            Agent 1          Agent 2
D2(O).O.f. If the current proof context has a hypothesis
Ofll : islossless D2(O).O.f, for example an assumption
of the lemma being proved, the compiler uses it, and the                  (c)        stall, spawn a child               (d)      prune stalled branch

realized tactic is
                                                                                               spawn
                                                                           stuck;
    call (Alossless_F (<: D2(O).O) Ofll).                                  failure
                                                                        recorded
                                                                                                                        pruned

                                                                                          Agent 1.1

Otherwise, the premise is a new proof obligation. The                                                  Agent 2                        Agent 1.1   Agent 2

compiler leaves it as a hole, and the realized tactic is
    call (Alossless_F (<: D2(O).O) _).                                Figure 6. A proof tree evolving over a search. (a) Two agents explore
                                                                      in parallel from the initial state. (b) Agent 2 recognizes a wrong turn,
EasyCrypt then turns the hole into a new subgoal,                     backtracks to an earlier state, and takes a different edge. (c) Agent 1 stalls;
                                                                      the orchestrator records the failed attempt and spawns Agent 1.1 at the
islossless D2(O).O.f, which the agent proves.                         parent state. (d) The stalled branch is pruned (×); Agent 1.1 and Agent 2
                                                                      continue.

4. Tree-Based Proof Orchestration
                                                                      4.2. Backtracking within an Agent
    Section 2 observed that a single agent explores the proof
along one path and often does not notice when it should turn              At each node, the agent reads the output of the proof-
back. ShannonProver addresses this with a tree-based search           state compiler (Section 3), which gives it a structured view
explored at two levels. Within a single agent, the agent can          of the current proof state. Based on this view, the agent
backtrack and re-explore an earlier state when it discovers           extends its branch one tactic at a time, then reads the
that the current strategy is unproductive. Across agents, an          compiler’s output for the resulting state and continues from
orchestrator manages several branches of the proof tree: it           there.
decides when to start a new agent on a fresh branch, when                 An agent does not only move forward. During proof
to stop an unpromising one, and how failures found on one             construction, it may discover that the current strategy has
branch should guide the others. We first introduce the basic          become unproductive, or that an earlier tactic quietly led the
tree concepts (§4.1).                                                 proof into a dead end. In that case, the agent can backtrack to
                                                                      the earlier state, revise the proof from that point, and extend
                                                                      a new edge to a new child. This makes exploration less
4.1. Proof Tree                                                       brittle: the agent does not have to make a perfect sequence
                                                                      of irreversible choices, but can try a strategy, learn from
                                                                      where it breaks, and return to a better branching point.
    A node represents a proof state. Working on a proof
means moving progressively between nodes. An edge is
an accepted transition between states: the agent submits a            4.3. Scheduling across Agents
tactic, the checker accepts it, and the proof state moves from
the current node to a child node. A rejected tactic leaves the             Backtracking (§4.2) handles the wrong turns that the
state unchanged and creates no edge. A path is the sequence           agent itself recognizes. It does not address the two lim-
of nodes from the root to the current node, representing              itations observed in Section 2: an agent may stall at a
proof attempts. An agent is a prover instance that extends a          state instead of backtracking, and a single branch explores
single branch of the tree, advancing the proof one node at            alternatives one after another, even when several strategies
a time.                                                               are worth exploring together.
    The search space is a tree rather than a single line                   To address both limitations, ShannonProver uses an or-
because the same state can be continued in more than one              chestrator. The orchestrator is not an LLM agent, but instead
way. A node gains another child in two ways. First, an agent          a deterministic algorithm that manages the same proof tree
may backtrack to that node and try a different strategy; if           from above. It decides where to fork the search with a fresh
the new tactic is accepted, it leads to a different child state       agent, which branches should be stopped, and how failures
(§4.2). Second, the orchestrator may spawn another agent              on one branch should inform the others. The orchestrator
at the same shared state, so that a different strategy can be         uses three mechanisms: spawning, pruning, and negative
explored without waiting for the current branch to finish             memory (Fig. 6).
(§4.3). The resulting branches are siblings below a common            Spawning children. At each node, the orchestrator may
node. A branch ends at a leaf : either a closed proof (qed.)          spawn additional children, each exploring a different path.
or a state that is abandoned because it is a dead end or is           Without control, this would quickly become infeasible:
pruned by the orchestrator (§4.3).                                    spawning two children from the root, then two children from


                                                                  7
each child, would make the number of live agents grow                 5. Coordinating Proof Decomposition and
exponentially. ShannonProver therefore spawns new agents              Lemma Proving
only when the current search behavior suggests that another
strategy is worth trying.                                                  Sections 3 and 4 prove lemmas whose statements are
❶ Persistent local failure. If an agent at a node (state)             fixed. We now start from only the specification and the final
repeatedly submits tactics and the checker rejects them, this         theorem, whose proof is left open, and let ShannonProver
suggests that the agent may be stuck in a local neighborhood          construct the decomposition as well (Phase II in Fig. 1).
of bad moves and the current branch is unproductive. Rather           Phase II need not finish before Phase III starts: whether a
than letting the agent spend more time on the same strategy,          decomposition is good is often known only after trying to
the orchestrator creates a sibling branch. It does so by              prove its lemmas. An invariant may turn out to be too weak
spawning a child at the parent of the node where the agent            to carry through an oracle call, or a planned game hop may
is currently working, giving the search a chance to approach          violate the restrictions on which modules the adversary may
the state through a different path.                                   access. As experts do, ShannonProver moves back and forth
❷ Structural undo. Some tactics fix the shape of the rest             between the two phases (Fig. 2).
of the proof: they open a procedure or turn a probability             Decomposer. The decomposer is an LLM agent that works
statement into a program equivalence (e.g., proc, byequiv),           on an EasyCrypt file containing the specification and the
cut the program with an intermediate assertion or invariant           statement of the final theorem. Its goal is the same file with a
(seq, while, call), inline code (inline), or introduce an             complete proof: EasyCrypt must accept the whole file, with
intermediate fact (have, transitivity). We call an undo               no admit remaining. In our experiments, the final theorem
structural when it undoes such a tactic: the agent has                and the supplied definitions must remain unchanged, and
abandoned an earlier decision that shaped much of the later           new declarations may be added only in a marked region of
proof, so the state before that tactic is a valuable branching        the file, so the decomposer cannot make the theorem easier
point. If the same agent has not repaired its strategy within         by weakening it or adding assumptions. The decomposer
five minutes, the orchestrator spawns a child at that state.          chooses the intermediate games, writes the auxiliary lemmas
                                                                      together with the modules and invariants they need, and
Pruning. Spawning creates new opportunities, but it also              assembles the proof of the final theorem; it may also prove
creates the risk of an unbounded search. The orchestra-               lemmas directly. It checks its work by replaying the whole
tor therefore prunes branches and terminates unproductive             file in EasyCrypt, temporarily allowing admit placeholders,
agents. The pruning decision is based on a progress gap: if           so that it can confirm that a skeleton of the argument type-
an agent remains far behind the other agents in the tree, it          checks and connects to the final theorem before every lemma
becomes a candidate for pruning.                                      is proved.
    This decision has to be made carefully. A branch that             Handing lemmas to the lemma prover. When a lemma
looks behind is not necessarily useless: an agent may be              would benefit from step-by-step interaction with the proof
backtracking through earlier states, which temporarily re-            state, the decomposer hands it to the lemma prover as a
duces its depth but may eventually lead to a better proof             job. A job works on exactly one named lemma, using the
strategy. The orchestrator therefore distinguishes agents that        proof-state compiler and the proof tree of §3 and §4. The
are temporarily behind because they are performing mean-              decomposer never hands over the final theorem or asks the
ingful backtracking from agents that remain behind through-           lemma prover to invent the overall reduction: choosing game
out the search. In this way, pruning keeps the number of live         hops and lemma statements remains its own responsibility.
agents bounded without discarding every branch that briefly           Each job receives a snapshot of the file, the name of
moves backward.                                                       the lemma, a time limit, and usually a short note with
                                                                      the goal, any proof prefix already accepted by EasyCrypt,
Negative memory. When one agent fails to extend a path,               the intended strategy, and the attempts that have already
the other agents should not blindly repeat the same exper-            failed. A job that receives an accepted prefix first replays
iment. The orchestrator therefore records failures as state-          it, so it never starts from a state that the checker has not
indexed negative memory. For a given node, negative mem-              accepted. Based on checked progress rather than elapsed
ory records which attempted extension led to a dead end               time, the decomposer requests one of three kinds of job: an
and why. When the orchestrator later spawns a child at that           exploratory job that tests whether a game hop, an invariant,
node, it passes the corresponding negative memory to the              or a proof strategy works; a completion job once accepted
new agent, so that the new branch can avoid spending budget           tactics already fix the strategy; or a continuation of an earlier
on the same failed strategy.                                          job from its saved state. Handing off a lemma does not
    Negative memory is a search-control mechanism, not                block the decomposer: a limited number of jobs run at the
proof knowledge. It records that a particular experiment              same time (two in our experiments), while the decomposer
failed for a particular state shape; it does not claim that the       continues with independent parts of the argument, such as
underlying proof strategy is impossible. This distinction is          later games or probability bounds.
important: negative memory guides exploration, but it does            Feedback from Phase III to Phase II. A job that proves its
not rule out proof strategies as a matter of logic.                   lemma returns the proof, which is checked again against the


                                                                  8
current file before it is merged. Otherwise, the job returns               run as a give-up. This rule prevents runs from spending
the longest prefix of tactics that EasyCrypt accepted, the                 an unbounded budget in states where the agent repeatedly
remaining goals, and, when available, a saved state for a                  reports that it is stuck. In pilot runs, forcing the agent to
continuation; any notes it adds are hints, not checked facts.              continue led either to wasted tokens at the same stuck point
From such a result, the decomposer can finish the proof                    or to behavior unrelated to the proof, such as reading files
itself, request a continuation, restate or split the lemma or              outside the project.
add helper lemmas, or change the decomposition. The last                   Data sampling. To keep the API cost of the ablation study
two are where Phase III feeds back into Phase II (Fig. 2; §6.4             manageable while keeping the evaluation representative, we
describes an example from the ChaChaPoly case study).                      sample 40 lemmas from our benchmark dataset, covering
                                                                           different types and difficulty levels. Appendix C describes
6. Evaluation                                                              how we built this dataset. We group lemmas by proof
                                                                           shape: procedural (P), invariant-synthesis (I), and game-
                                                                           hop/reduction (G). This grouping is not meant to label
Implementation. ShannonProver is an open-source research
                                                                           cryptographic importance; rather, it separates qualitatively
prototype written in Python and built on EasyCrypt. The
                                                                           different proof-engineering regimes. Procedural lemmas are
core implementation contains about 89K lines of code: about
                                                                           mostly local: once the relevant procedure body is ex-
86K lines of Python and about 3K lines of OCaml that
                                                                           posed, progress is often made by a sequence of greedily
extend EasyCrypt. By component, it comprises about 33K
                                                                           discoverable symbolic-execution and simplification tactics.
lines for the multi-agent tree search (§4), including the
                                                                           Invariant-synthesis lemmas require the agent to choose a
orchestrator, the agents, and recovery from agent crashes;
                                                                           relational invariant that is strong enough to carry through
about 26K lines for the proof-state compiler (§3); about
                                                                           a call or loop boundary, but not so strong that it creates
24K lines for running EasyCrypt and parsing its output;
                                                                           unnecessary side obligations. Game-hop and reduction lem-
and about 7K lines for the decomposer (§5). App. B de-
                                                                           mas require the proof to preserve higher-level game structure
scribes the architecture in detail. Our code is available at
                                                                           long enough to apply bridge lemmas, oracle equivalences,
https://github.com/SkyShannonProver/shannon-prover.
                                                                           or probability bounds. These three shapes pose different
                                                                           difficulties for the agent, so aggregating them into a single
6.1. Evaluation Design                                                     average would obscure where the lemma prover helps.
                                                                           Metrics. LLM-based theorem provers are usually evaluated
    Our evaluation has two parts. The first is a controlled                by pass@k [26,27]: the model writes k complete proof
ablation of the lemma prover’s two design ideas. For the                   scripts, and a theorem counts as solved if any of them is
proof-state compiler, we measure how much it reduces                       accepted. We do not use this metric, for two reasons. First,
the agent’s errors and the cost of recovering from them.                   it suits short proofs that can be written in one shot, as in
For the multi-agent tree search, we measure how much it                    miniF2F [27]. Our lemmas often need dozens of tactics,
speeds up proof writing compared with a single agent. The                  so writing a complete proof in one shot that the checker
second part is a case study on ChaCha20-Poly1305 [21],                     accepts is unrealistic, and sampling many attempts (i.e., a
in which we evaluate both the lemma prover given the                       very large k ) is prohibitively expensive. Second, the binary
experts’ decomposition and the end-to-end setting with the                 outcome, whether a lemma is proved or not, does not show
decomposer. Appendix C presents additional case studies                    what our mechanisms change. For example, two runs may
on MEE-CBC [19] and CMAC [20], together with expert                        both succeed, one through a short, direct proof and the other
comments on these developments (App. C.3).                                 only after many rejected tactics. We instead use metrics that
Setup. All ablations share the following setup. We use                     target each mechanism, detailed in §6.2 and §6.3.
Opus 4.82 with high reasoning effort. The agent may read
all project files and EasyCrypt source files, and we give it               6.2. The Effects of the Proof-State Compiler
no hints about proof strategy. Each ablation compares the
lemma prover with a baseline in which the mechanism under                  Baseline. The baseline has the agent interact directly with
study is disabled (§6.2 and §6.3 describe each baseline). The              the checker: after submitting each tactic to the checker it
baseline uses the same MCP-based EasyCrypt interaction                     sees only the resulting goal or the error message. The lemma
layer as the lemma prover, so that differences in results do               prover instead shows the agent the output of the proof-state
not stem from unrelated engineering factors such as session                compiler (§3).
management and crash recovery.
    We use the same stopping rule in all configurations: the               Metrics. A cheaper proof could come from two very differ-
agent may announce that it gives up at most three times.                   ent places, and a fair ablation has to separate them. The
After each announcement, the system prompts the agent to                   compiler’s output might make the model propose fewer
try another strategy. If the agent makes three consecutive                 wrong tactics in the first place, or it might leave the first-
such announcements without proof progress, we count the                    attempt error rate unchanged while making those errors far
                                                                           less costly. We therefore have the following metrics:
  2. This was the strongest model available when we ran the ablation       ❶ Error-generation rate. The fraction of the model’s distinct
experiments.                                                               proposed tactics that the checker rejects on its first attempt.


                                                                       9
              (a) Error-generation                (b) Error friction              has a visibly higher rate. The experimental traces suggest
                      rate                          (% of spend)                  why: with the richer information provided by the compiler,
                                                                                  the agent often attempts stronger and more structured invari-
               0.10                              10.8%                            ants, because it can see more of the resources that apply, the
      0.1                                10
                             0.07
 P
     0.05
                                                                                  program statements to which they apply, and the required
                                          5
                                                               0.0%
                                                                                  bindings. Some of these ambitious invariant attempts are
       0                                  0                                       rejected on the first attempt. In the baseline, however, the
     0.15                                15
                                                                                  agent is more likely to choose a weaker invariant that passes
                             0.12                12.3%
      0.1      0.08                      10
                                                                                  immediately, even if it leaves the proof in a worse state later.
 I                                                                                    The compiler ablation therefore shows that the proof-
     0.05                                 5
                                                               0.3%               state compiler mainly reduces the cost of errors rather than
       0                                  0
                                                                                  their number: the agent still makes mistakes, but it spends
     0.15                    0.13                 9.8%
                                                                                  far less of its budget recovering from them.
               0.11                      10
 G    0.1
     0.05
                                          5
                                                               1.3%
                                                                                  6.3. The Effects of Multi-Agent Tree Search
       0                                  0
              baseline   ShannonProver          baseline   ShannonProver          Baseline. The multi-agent tree search has two layers (§4):
                                                                                  backtracking within a branch, and spawning further branches
Figure 7. Compiler ablation on lemma pairs that both cases proved, grouped
by proof shape: P = procedural, I = invariant-synthesis, G = game-
                                                                                  from shared checkpoints. Backtracking itself cannot be
hop/reduction.                                                                    meaningfully removed: an agent that cannot undo a wrong
                                                                                  step can only fail. The baseline therefore keeps backtracking
                                                                                  and removes spawning. It runs one branch at a time: the
❷ Error friction. The fraction of an agent’s total API                            agent can undo and backtrack within its branch, and if
spend on sequences of consecutive tactics rejected by the                         its agent process crashes, the branch is resumed from its
checker. This captures the fraction that the agent spends on                      committed prefix, but no sibling branch ever races it. The
debugging syntax and recovering from errors.                                      lemma prover adds the cross-agent tree policy: a second
     To collect these metrics, our measurement pipeline sepa-                     branch can race from a shared checkpoint, and dead or
rates deterministic metrics from qualitative judgement. The                       stalled nodes can be respawned with negative memory so
first stage is a Python parser: for each run it extracts the                      that the next agent does not repeat the same failed strategy.
submitted tactics, the checker responses, and the agent rea-                      In both configurations, the agent can use the proof-state
soning traces for each submitted tactic. The second stage                         compiler.
uses an LLM for cases a parser cannot classify mechani-                           Metrics. We measure how often the agent needs to back-
cally: for example, when the agent commits several steps                          track: the fraction of solved runs that backtrack at least once,
and later reverts them with no explicit checker error, so                         and the number of backtrack events per solved run. These
the parser cannot tell an unproductive dead end from a                            numbers show how far proof search departs from a straight
deliberate restructuring; there the LLM labels those tactic                       line in each lemma category. We also measure the solve rate
moves with the corresponding qualitative cause. The final                         in each category, and how it grows over the course of a run.
stage is deterministic again: a script aggregates the parsed
                                                                                  Results. Figure 8a–b first shows that the need for backtrack-
events and the labels into the reported numbers.
                                                                                  ing is highly lemma-type dependent. Procedural lemmas are
Results. Figure 7 shows that the proof-state compiler does                        almost straight-line, as expected from their local structure.
not primarily work by making the model intrinsically less                         In contrast, invariant-synthesis and game-hop lemmas are
error-prone. The error-generation rate is close between the                       much less linear. 38% of solved invariant runs and 43% of
baseline and the lemma prover across the three lemma types.                       solved game-hop runs backtrack at least once, with about
This is expected, because this metric is dominated by the                         2.0–2.3 backtrack events per solved run. These are exactly
model’s own stochastic search behavior.                                           the lemmas where an attempted tactic that is accepted by the
    The error-friction numbers show the more important                            checker can lead the agent into an unproductive strategy: an
effect. Across all lemma types, the lemma prover sharply                          invariant may be too weak or too strong, and a game-hop
reduces the fraction of spend on such rejected sequences.                         proof may descend too early and lose a bridge lemma or
This means that even when the agent still makes mistakes                          oracle-equivalence resource. For these lemmas, the ability
when it first tries a move, the agent can immediately recover                     to rewind is not a rare recovery feature; it is part of how
from it. Meanwhile, the agent in the baseline must figure out                     successful proofs are found.
the right move via trial-and-error. The ablation shows that                           Figure 8c–d shows what spawning adds on top of an
the proof-state compiler is not a proof oracle that provides                      agent that backtracks. On procedural lemmas, backtracking
the right move, but an interface that provides sufficient                         within one branch already suffices: the single agent proves
information to free the agent from mechanical debugging.                          every lemma, and a second branch only wins the race.
    The main counter-intuitive result for the error-generation                    On invariant-synthesis and game-hop lemmas, it does not:
rate is invariant-synthesis lemmas, where the lemma prover                        even with backtracking, a third of single-agent runs fail,


                                                                             10
                                              (a) Solved runs that                                                    (b) Backtrack events                     This case study demonstrates that LLM agents today can
                                                  backtracked                                                            per solved run                   fully automate lemma-level proof (Phase III in Fig. 1) at the




                                                                                          events / solved run
 % of solved runs




                                                                43%                                                                           2.29        scale and complexity of ChaChaPoly. Figure 10 shows all
                                                      38%                                                                          2.00
                            40                                                                                   2                                        the lemmas in ChaChaPoly and the API cost per lemma. The
                            20                                                                                   1
                                                                                                                                                          procedural lemmas are generally easy and they are solved at
                                              3%                                                                      0.04                                low API cost. This is already useful because large projects
                                    0                                                                            0                                        contain many such lemmas, and writing them manually still
                                                  P    I        G                                                         P         I          G
                                                                                                                                                          consumes expert time. Importantly, ShannonProver solved
                                         (c) Winning path needed                                                            (d) Solve rate                the hardest lemmas in the project, while the baseline agent
                                            backtrack / respawn                                                           (I + G lemmas)                  failed. These hard lemmas are fewer in the project, but they
 % of orch. solves




                                                                           % of runs solved
                                                                                                                                                          are also the most important: they are the points where the
                                                      80%                                               100                                90%
                            80
                                                                                                                          67%
                                                                                                                                                          lemma decomposition is tested. If these lemmas can be
                            60                                  50%
                            40                                                                                  50                                        proven, the expert gains evidence that the decomposition
                            20                3%
                                                                                                                                                          has the right structure. If LLM agents or humans fail to
                             0                                                                                   0                                        prove a lemma, the thought process in the failed attempts is
                                                  P    I        G                                                         single          orches-         still informative: it often indicates that the current lemma
                                                                                                                          agent            trator
                                                                                                                                                          is missing an invariant, that a game hop has not been
Figure 8. Tree-search ablation, grouped by proof shape (P = procedural;                                                                                   modularized at the right boundary, or that some other part
I = invariant-synthesis; G = game-hop/reduction).                                                                                                         of the decomposition needs to be revised. This feedback is
                                                                                                                                                          valuable for redoing the decomposition.
                     % of runs solved




                                        100                                                                               orchestrator
                                                                                                                                                               We also evaluate proof quality on three fronts: conci-
                                                                                                                                                          sion (C), maintainability/readability (M) and semantic proof
                                         80                                                                               single agent                    idiom (S). C measures whether the proof is compact and
                                                                                                                                                          avoids unnecessary tactic churn or duplicated reasoning. M
                                         60
                                              0            15         30                                             45              60                   measures whether the proof structure is easy for a human to
                                                                 elapsed time (minutes)                                                                   inspect, debug, and adapt when the surrounding definitions
Figure 9. Fraction of lemmas solved by elapsed time. The two configura-                                                                                   change. S measures whether the proof follows the natural
tions coincide for the first 15 minutes (dashed line) and separate afterwards.                                                                            EasyCrypt proof structure and uses existing proven facts,
                                                                                                                                                          rather than reproving low-level details. We have two experts
                                                                                                                                                          independently receive each pair of proofs in randomized
and spawning raises the solve rate from 67% to 90%. The                                                                                                   order and manually evaluate for each dimension. Figure 10
gain comes mainly from redundancy: the second branch                                                                                                      shows that the AI-generated proofs still leave room for
completed the proof after the root branch’s agent had died.                                                                                               improvement on invariant and game-hop lemmas, making
It also appears late (Fig. 9): both configurations solve 82%                                                                                              proof quality a promising direction for future work.
of all runs within 15 minutes and separate only afterwards,                                                                                                    The LLM API cost is also reasonable to make iter-
once a first branch has stalled.                                                                                                                          ative proof development practical. Across the ChaCha20-
    The tree ablation therefore supports two conclusions.                                                                                                 Poly1305 lemmas (Fig. 10), proving all lemmas of the
First, proof search is not uniformly non-linear: for local                                                                                                expert decomposition once costs $233.65 for API calls
procedural obligations, a single branch with backtracking                                                                                                 and completes within a day of wall-clock time. The cost
is enough. Second, for the proof types that matter most in                                                                                                is concentrated in the harder lemmas: the 27 procedural
cryptographic developments—invariants and game hops—                                                                                                      lemmas together cost $40.98, while the invariant-synthesis
backtracking within one branch is not enough, and spawning                                                                                                and game-hop/reduction lemmas account for $76.99 and
further branches makes the search robust to branches that                                                                                                 $115.68, respectively. This distribution is desirable from a
stall or die.                                                                                                                                             workflow perspective: the system spends little on procedural
                                                                                                                                                          lemmas, and most of the cost goes to the lemmas that
6.4. Case Studies                                                                                                                                         are most informative for testing the decomposition. Even
                                                                                                                                                          if a cryptographer revises the decomposition and reruns the
    ChaCha20-Poly1305 [21] is a representative case study                                                                                                 proof pass several times, the marginal cost remains on the
project. It is an AEAD construction that combines the                                                                                                     order of a few hundred dollars per iteration and the time is
ChaCha20 stream cipher with the Poly1305 authenticator                                                                                                    at most a day, rather than person-weeks or person-months of
and is used in IETF protocols and deployed in TLS [5].                                                                                                    expert proof engineering. This makes ShannonProver useful
Its EasyCrypt formal proof contains a mixture of low-level                                                                                                not only as a one-shot proof generator, but also as a practical
algebraic reasoning, invariant-heavy relational proofs, and                                                                                               tool for iterating on large cryptographic formalizations.
game-hop/reduction lemmas. Experts described the devel-
opment as interleaving the design of new abstractions with                                                                                                Evaluation for end-to-end proof. We further evaluate
mechanical proof engineering: abstraction choices shaped                                                                                                  ShannonProver in an end-to-end setting, where the system
the proof structure, while mechanization difficulties fed back                                                                                            is given only the specification and the statement of the
into the abstraction design.                                                                                                                              main theorem. In this workflow, the complete proof was


                                                                                                                                                     11
     ShannonProver and baseline comparable                            ShannonProver substantially better, or baseline gives up
     C/M/S: agent proof as good as or better than expert proof                           C/M/S: expert proof better       standout agent proof

                                        (a) Procedural (27 lemmas)                                                                           (b) Invariant synthesis (8 lemmas)
                                                                                                          CM S                                                                                                           CM S
                          pr_TPI_ok                                                               $4.19                      equiv_step4                                                                      $44.73
                      pr_step4_badi                                                  $3.25                                    step4_badi                          $13.94
   gen_CTR_encrypt_bytes_cons                                               $2.51                                                                      $6.70
                                                                                                                        UFCMA_genCC
         make_lbad1_size_cons2                                           $2.34
                                                                                                                                  equ_cc          $4.67
               take_xor_map2_xor                                      $2.11
                                                                                                                            CCP_OCCP             $3.47
                        chacha_enc2                                  $2.04
                                                                                                                            chacha_spec        $1.65
                 filter_test_poly_in                               $1.90
                                                                   $1.88                                                 pr_CCP_OCCP          $1.03
                          dblock_uni
                       mk_rs_ofpair                                $1.88                                                       poly_spec      $0.80
                        chacha_enc1                        $1.47                                                                         $0             $10              $20            $30         $40            $50
                          poly_mac2                       $1.41
                              nth_xor                     $1.40
                          poly_mac1                       $1.40                                                                              (c) Game hop / reduction (12 lemmas)
                                                                                                                                                                                                                         CM S
             iter_gen_ctr_round_S                        $1.35
                                                        $1.30                                                                 step4_bad2                                                                      $24.55
           iter_gen_ctr_round_nil
      iter_gen_ctr_round_nil_cat                      $1.19                                                            step4_bad1_lbad1                                                             $20.60
       gen_CTR_encrypt_bytes0                       $1.04                                                                         step2_3                                                     $18.32
                           dblock_fu                $1.01                                                                            step3                                     $12.35
                               xorK1               $0.97                                                                          step4_1                            $9.01
                           nth_map2                $0.97                                                                                                          $7.73
                                                                                                                                  step2_2
                            dblock_ll              $0.96
                                                                                                                                     step1                       $7.11
                                addK              $0.89
                                                                                                                                  step2_1                $4.62
                   pr_TPI_ok_filter               $0.86
                                                                                                                        step4_lbad1_sum                  $4.47
                             nth_zero            $0.81
                                               $0.67                                                                           conclusion              $3.35
                         dblock_funi
                          size_map2            $0.66                                                                          step4_bad1         $2.28
                           map2_zip          $0.52                                                                                   step2     $1.29
                                    $0           $1            $2               $3           $4                                          $0             $5          $10          $15          $20            $25


Figure 10. Per-lemma API cost for the ChaCha20-Poly1305 project, grouped by proof shape (P/I/G). Bar color compares ShannonProver with the baseline.
For concision (C), maintainability/readability (M), and semantic proof idiom (S), a filled green dot denotes an agent proof comparable to or better than
the expert proof, while a hollow gray circle denotes an expert advantage. Stars mark the two agent proofs described in Appendix D.


constructed in 5 hours, using a strong model (Opus 53 ) as                                                        loop, and studies the interface and search policy that make
decomposer and keep the lemma provers same as before.                                                             this possible. We build on EasyCrypt because it covers the
In this run, about 20% of the lemmas in the decomposition                                                         computational proof patterns of these developments; rather
were reworked after the decomposer first wrote them and                                                           than trade this expressiveness for push-button proving, we
received feedback from the lemma prover. The total cost is                                                        aim to supply the automation with LLM agents.
about $420 for a complete proof. In comparison, a baseline                                                        LLMs for formal proofs. LLM-based theorem prov-
that uses CLI with Opus 5 takes 8 hours to complete the                                                           ing has advanced rapidly, mostly in mathematics, through
proof end to end; and Opus 4.8 failed to complete the task.                                                       whole-proof generation [26,46–50] evaluated on compe-
                                                                                                                  tition benchmarks [27,51,52], tactic-level interaction with
7. Related Work                                                                                                   the proof assistant [23,53,54], and, more recently, agentic
                                                                                                                  provers [55,56]. Other work enriches the interface between
Machine-checked cryptography. Game-based crypto-                                                                  model and prover, by suggesting tactics in the human work-
graphic proofs are supported by mature proof assis-                                                               flow [57,58], exposing proof states to agents [59], or adding
tants [18,28–32], complemented by tools for symbolic                                                              a natural-language representation of the proof state [60].
protocol analysis [33,34], computationally sound protocol                                                         ShannonProver’s proof-state compiler instead computes, at
proofs [35], and verified implementations [9,36,37]. With                                                         every state, which resources apply and how to instantiate
them, experts have verified standardized schemes and NIST                                                         them, and its tree search coordinates several agents over the
post-quantum standards [14,19,21,22,38,39], at a cost of                                                          same proof.
person-weeks to person-years. Prior automation has focused
on the symbolic model, using reinforcement learning or                                                            8. Conclusion and Future Work
learned search heuristics [40,41] and LLMs to build or check
protocol models [42,43]. Closer to our setting, generative AI                                                         This work shows that LLM agents can take on a sub-
has helped a researcher formalize computational security                                                          stantial part of mechanized cryptographic proof when the
proofs in Lean [44], and AI provers have closed correct-                                                          system around them supplies the right context and controls
ness obligations extracted from cryptographic code [45].                                                          the search.
                                                                                                                      Two problems remain open. Decomposing a large proof
ShannonProver instead proves fixed statements from existing
                                                                                                                  obligation into provable lemmas (Phase II) still depends
expert developments in EasyCrypt without a human in the
                                                                                                                  strongly on the capability of the model; better harness
  3. We ran this experiment during the revision of this paper, after the                                          support for the decomposer may improve performance. For
other ablations; Opus 5 was the strongest model available at that time.                                           Phase I, it is interesting to explore how AI can help experts


                                                                                                             12
design the specification itself, or help the experts design the               [2]   National Institute of Standards and Technology, “FIPS 202: SHA-3
abstractions needed for certain cryptographic schemes.                              standard: Permutation-based hash and extendable-output functions,”
                                                                                    Federal Information Processing Standards Publication 202, 2015.
                                                                              [3]   National Institute of Standards and Technology, “FIPS 197: Advanced
9. Generative AI Responsibility Policy                                              encryption standard (AES),” Federal Information Processing Stan-
                                                                                    dards Publication 197, 2023.
Content and data holder rights. ShannonProver is evalu-                       [4]   National Institute of Standards and Technology, “FIPS 203: Module-
ated on a benchmark of EasyCrypt developments comprising                            lattice-based key-encapsulation mechanism standard,” Federal Infor-
ML-KEM, MEE-CBC, ChaCha20-Poly1305, and CMAC.                                       mation Processing Standards Publication 203, 2024.
We used each artifact in a manner consistent with the terms                   [5]   E. Rescorla, “The transport layer security (TLS) protocol version 1.3,”
under which its rights holders released it.                                         RFC 8446, 2018.
    The ML-KEM specification is released under the Cre-                       [6]   D. J. Bernstein, T. Lange, and P. Schwabe, “The security impact of a
ative Commons CC0 1.0 Universal public domain dedi-                                 new cryptographic library,” in Progress in Cryptology – LATINCRYPT
cation. The MEE-CBC and ChaCha20-Poly1305 develop-                                  2012, ser. Lecture Notes in Computer Science, vol. 7533. Springer,
                                                                                    2012, pp. 159–176.
ments are distributed with the EasyCrypt proof assistant,
under the MIT License.                                                        [7]   libsodium contributors, “libsodium documentation,” https://doc.
                                                                                    libsodium.org/, accessed 2026-05-09.
    The CMAC development is not publicly available. We
obtained explicit authorization from its authors to evaluate                  [8]   OpenSSL Software Foundation, “OpenSSL: Cryptography and SS-
                                                                                    L/TLS toolkit,” https://www.openssl.org/, accessed 2026-05-09.
ShannonProver on it, and our use is confined to the scope of
that authorization. We therefore report aggregate results for                 [9]   J. Protzenko, B. Parno, A. Fromherz, C. Hawblitzel, M. Polubelova,
                                                                                    K. Bhargavan, B. Beurdouche, J. Choi, A. Delignat-Lavaud, C. Four-
CMAC without releasing the underlying source files; readers                         net, N. Kulatova, T. Ramananandro, A. Rastogi, N. Swamy, C. M.
seeking access should contact the original authors directly.                        Wintersteiger, and S. Zanella-Béguelin, “EverCrypt: A fast, verified,
                                                                                    cross-platform cryptographic provider,” in 2020 IEEE Symposium on
Environmental footprint. ShannonProver substantially re-                            Security and Privacy. IEEE, 2020, pp. 983–1002.
duces token usage compared with using Codex or Claude
                                                                              [10] M. Thomson and S. Turner, “Using TLS to secure QUIC,” RFC 9001,
through a plain CLI to solve the same task. We believe                             2021.
this points to a more responsible way of using LLMs for
                                                                              [11] K. Cohn-Gordon, C. J. F. Cremers, B. Dowling, L. Garratt, and
proof automation going forward: whenever possible, work                            D. Stebila, “A formal security analysis of the Signal messaging pro-
that does not require substantial model reasoning should be                        tocol,” in 2017 IEEE European Symposium on Security and Privacy
moved to deterministic components, reserving LLM calls                             (EuroS&P). IEEE, 2017, pp. 451–466.
for tasks where their reasoning capabilities are genuinely                    [12] J. A. Donenfeld, “WireGuard: Next generation kernel network tun-
needed.                                                                            nel,” in 24th Annual Network and Distributed System Security Sym-
                                                                                   posium (NDSS 2017). Internet Society, 2017.

Acknowledgments                                                               [13] J. B. Almeida, S. A. Olmos, M. Barbosa, G. Barthe, F. Dupres-
                                                                                   soir, B. Grégoire, V. Laporte, J.-C. Léchenet, C. Low, T. Oliveira,
                                                                                   H. Pacheco, M. Quaresma, P. Schwabe, and P.-Y. Strub, “Artifact
    This work is supported by gifts from Accenture, Algo-                          for formally verifying kyber episode V: Machine-checked IND-CCA
rithmic SuperIntelligence Labs, Amazon, AMD, Anyscale,                             security and correctness of ML-KEM in EasyCrypt,” IACR Artifact
Broadcom, cmpnd, Google, IBM, Intel, Intesa Sanpaolo,                              Archive, crypto/2024/a3, 2024.
Lambda, Lightspeed, Mirendil, NVIDIA, Samsung SDS,                            [14] M. Barbosa, F. Dupressoir, A. Hülsing, M. Meijers, and P.-Y. Strub,
and VESSL.                                                                         “A tight security proof for SPHINCS+, formally verified,” in Ad-
                                                                                   vances in Cryptology – ASIACRYPT 2024, ser. Lecture Notes in
    We would like to thank Quang Dao, Shafi Goldwasser,                            Computer Science, vol. 15487. Springer, 2024, pp. 35–67.
Mohsen Lesani, Hongyi Ling, Ning Luo, Surya Mathiala-
                                                                              [15] Y. Bertot and P. Castéran, Interactive Theorem Proving and Program
gan, Yibin Yang, the students in the security group at Sky                         Development: Coq’Art: The Calculus of Inductive Constructions, ser.
Lab, and the participants and organizers in HACS 2026                              Texts in Theoretical Computer Science. Springer, 2004.
for valuable discussions. We also thank Sebastian Angel                       [16] L. de Moura and S. Ullrich, “The Lean 4 theorem prover and
and AWS Cryptography Group, especially Tal Rabin, Yuval                            programming language,” in Automated Deduction – CADE 28, ser.
Ishai, and Shai Halevi, for valuable discussion and feedback                       Lecture Notes in Computer Science, vol. 12699. Springer, 2021, pp.
on this draft and future directions.                                               625–635.
                                                                              [17] N. Swamy, C. Hriţcu, C. Keller, A. Rastogi, A. Delignat-Lavaud,
                                                                                   S. Forest, K. Bhargavan, C. Fournet, P.-Y. Strub, M. Kohlweiss, J.-
Competing Interests                                                                K. Zinzindohoué, and S. Zanella-Béguelin, “Dependent types and
                                                                                   multi-monadic effects in F*,” in Proceedings of the 43rd Annual
   Apart from the research funding listed in the acknowl-                          ACM SIGPLAN-SIGACT Symposium on Principles of Programming
edgments, the authors declare no competing financial or                            Languages (POPL). ACM, 2016, pp. 256–270.
non-financial interests.                                                      [18] G. Barthe, B. Grégoire, S. Heraud, and S. Z. Béguelin, “Computer-
                                                                                   aided security proofs for the working cryptographer,” in Advances in
                                                                                   Cryptology – CRYPTO 2011, ser. Lecture Notes in Computer Science,
References                                                                         vol. 6841. Springer, 2011, pp. 71–90.
                                                                              [19] J. B. Almeida, M. Barbosa, G. Barthe, and F. Dupressoir, “Verifiable
[1]   S. Halevi, “A plausible approach to computer-aided cryptographic             side-channel security of cryptographic implementations: Constant-
      proofs,” Cryptology ePrint Archive, Paper 2005/181, 2005.                    time MEE-CBC,” in Fast Software Encryption (FSE), 2016.



                                                                         13
[20] C. Baritel-Ruet, F. Dupressoir, P.-A. Fouque, and B. Grégoire, “For-           [39] J. B. Almeida, C. Baritel-Ruet, M. Barbosa, G. Barthe, F. Dupressoir,
     mal security proof of cmac and its variants,” in 2018 IEEE 31st                     B. Grégoire, V. Laporte, T. Oliveira, A. Stoughton, and P.-Y. Strub,
     Computer Security Foundations Symposium (CSF). IEEE, 2018,                          “Machine-checked proofs for cryptographic standards: Indifferentia-
     pp. 91–104.                                                                         bility of sponge and secure high-assurance implementations of SHA-
[21] J. B. Almeida, M. Barbosa, G. Barthe, B. Grégoire, A. Koutsos, V. La-               3,” in ACM CCS, 2019.
     porte, T. Oliveira, and P.-Y. Strub, “The last mile: High-assurance and        [40] Y. Xiong, C. Su, W. Huang, F. Miao, W. Wang, and H. Ouyang,
     high-speed cryptographic implementations,” in IEEE Symposium on                     “SmartVerif: Push the limit of automation capability of verifying
     Security and Privacy, 2020.                                                         security protocols by dynamic strategies,” in 29th USENIX Security
[22] J. B. Almeida, S. A. Olmos, M. Barbosa, G. Barthe, F. Dupres-                       Symposium (USENIX Security 20), 2020, pp. 253–270.
     soir, B. Grégoire, V. Laporte, J.-C. Léchenet, C. Low, T. Oliveira,            [41] M. Cosler, C. Cremers, B. Finkbeiner, M. Ghanem, and N. Medinger,
     H. Pacheco, M. Quaresma, P. Schwabe, and P.-Y. Strub, “Formally                     “Less effort, shorter proofs: Reinforcement learning for security pro-
     verifying kyber episode V: Machine-checked IND-CCA security and                     tocol analysis in Tamarin,” arXiv preprint arXiv:2605.23643, 2026.
     correctness of ML-KEM in EasyCrypt,” in Advances in Cryptology –
     CRYPTO 2024, ser. Lecture Notes in Computer Science, vol. 14921.               [42] C. Curaba, D. D’Ambrosi, A. Minisini, and N. P.-C. Antolín, “Crypto-
     Springer, 2024, pp. 384–421.                                                        FormalEval: Integrating LLMs and formal verification for auto-
                                                                                         mated cryptographic protocol vulnerability detection,” arXiv preprint
[23] K. Yang, A. Swope, A. Gu, R. Chalamala, P. Song, S. Yu, S. Godil,                   arXiv:2411.13627, 2024.
     R. J. Prenger, and A. Anandkumar, “Leandojo: Theorem proving with
     retrieval-augmented language models,” Advances in Neural Informa-              [43] Z. Mao, J. Wang, J. Sun, S. Qin, and J. Xiong, “LLM-aided auto-
     tion Processing Systems, vol. 36, pp. 21 573–21 612, 2023.                          matic modeling for security protocol verification,” in International
                                                                                         Conference on Software Engineering (ICSE), 2025.
[24] S. Rajaee, K. Pratik, G. Cesa, and A. Behboodi, “Local look-ahead
     guidance via verifier-in-the-loop for automated theorem proving,” in           [44] B. Spitters, “CatCrypt: From Rust to cryptographic security in Lean,”
     Findings of the Association for Computational Linguistics: ACL 2025,                Cryptology ePrint Archive, Paper 2026/604, 2026.
     2025.                                                                          [45] N. Klaus, J. Conejero, and P. Tolmach, “A Rust-to-Lean verification
[25] A. V. Aho, M. S. Lam, R. Sethi, and J. D. Ullman, Compilers:                        pipeline with AI provers: An experience report,” arXiv preprint
     Principles, Techniques, and Tools, 2nd ed. Addison-Wesley, 2006.                    arXiv:2605.30106, 2026.
[26] S. Polu and I. Sutskever, “Generative language modeling for auto-              [46] G. Lample, T. Lacroix, M.-A. Lachaux, A. Rodriguez, A. Hayat,
     mated theorem proving,” arXiv preprint arXiv:2009.03393, 2020.                      T. Lavril, G. Ebner, and X. Martinet, “Hypertree proof search for
                                                                                         neural theorem proving,” Advances in neural information processing
[27] K. Zheng, J. M. Han, and S. Polu, “MiniF2F: A cross-system bench-                   systems, vol. 35, pp. 26 337–26 349, 2022.
     mark for formal olympiad-level mathematics,” in ICLR, 2022.
                                                                                    [47] H. Xin et al., “DeepSeek-Prover-V1.5: Harnessing proof assistant
[28] G. Barthe, B. Grégoire, and S. Z. Béguelin, “Formal certification of                feedback for reinforcement learning and monte-carlo tree search,”
     code-based cryptographic proofs,” in POPL, 2009.                                    arXiv preprint arXiv:2408.08152, 2024.
[29] D. A. Basin, A. Lochbihler, and S. R. Sefidgar, “CryptHOL: Game-
                                                                                    [48] DeepSeek-AI, “DeepSeek-Prover-V2: Advancing formal mathemati-
     based proofs in higher-order logic,” Journal of Cryptology, 2020.
                                                                                         cal reasoning via reinforcement learning for subgoal decomposition,”
[30] P. G. Haselwarter, E. Rivas, A. Van Muylder, T. Winterhalter,                       arXiv preprint arXiv:2504.21801, 2025.
     C. Abate, N. Sidorenco, C. Hriţcu, K. Maillard, and B. Spitters,
                                                                                    [49] Y. Lin, S. Tang, B. Lyu, J. Wu, H. Lin, K. Yang, J. LI, M. Xia,
     “Ssprove: A foundational framework for modular cryptographic
                                                                                         D. Chen, S. Arora et al., “Goedel-prover: A frontier model for
     proofs in coq,” ACM transactions on programming languages and
                                                                                         open-source automated theorem proving,” in Second Conference on
     systems, vol. 45, no. 3, pp. 1–61, 2023.
                                                                                         Language Modeling.
[31] A. Petcher and G. Morrisett, “The foundational cryptography frame-
     work,” in Principles of Security and Trust (POST), 2015.                       [50] T. Hubert, R. Mehta, L. Sartran, M. Z. Horváth, G. Žužić, E. Wieser,
                                                                                         A. Huang, J. Schrittwieser, Y. Schroecker, H. Masoom et al.,
[32] D. Tuma, Q. Dao, J. Waters, A. Hicks, and N. Hopper, “Vcvio: Veri-                  “Olympiad-level formal mathematical reasoning with reinforcement
     fied cryptography in lean via oracle effects and handlers,” Cryptology              learning,” Nature, pp. 1–3, 2025.
     ePrint Archive, 2026.
                                                                                    [51] Z. Azerbayev, B. Piotrowski, H. Schoelkopf, E. W. Ayers, D. Radev,
[33] S. Meier, B. Schmidt, C. Cremers, and D. Basin, “The TAMARIN                        and J. Avigad, “ProofNet: Autoformalizing and formally proving
     prover for the symbolic analysis of security protocols,” in Computer                undergraduate-level mathematics,” arXiv preprint arXiv:2302.12433,
     Aided Verification, ser. Lecture Notes in Computer Science, vol. 8044.              2023.
     Springer, 2013, pp. 696–701.
                                                                                    [52] G. Tsoukalas, J. Lee, J. Jennings, J. Xin, M. Ding, M. Jennings,
[34] B. Blanchet, “Modeling and verifying security protocols with the                    A. Thakur, and S. Chaudhuri, “Putnambench: Evaluating neural
     applied pi calculus and ProVerif,” Foundations and Trends in Privacy                theorem-provers on the putnam mathematical competition,” Advances
     and Security, vol. 1, no. 1–2, pp. 1–135, 2016.                                     in Neural Information Processing Systems, vol. 37, pp. 11 545–11 569,
[35] B. Blanchet, “A computationally sound mechanized prover for se-                     2024.
     curity protocols,” IEEE Transactions on Dependable and Secure                  [53] A. Q. Jiang, W. Li, S. Tworkowski, K. Czechowski, T. Odrzygóźdź,
     Computing, 2008.                                                                    P. Miłoś, Y. Wu, and M. Jamnik, “Thor: Wielding hammers to
[36] J.-K. Zinzindohoué, K. Bhargavan, J. Protzenko, and B. Beurdouche,                  integrate language models and automated theorem provers,” Advances
     “HACL*: A verified modern cryptographic library,” in ACM CCS,                       in Neural Information Processing Systems, vol. 35, pp. 8360–8373,
     2017.                                                                               2022.
[37] J. B. Almeida, M. Barbosa, G. Barthe, A. Blot, B. Grégoire, V. La-             [54] E. First, M. N. Rabe, T. Ringer, and Y. Brun, “Baldur: Whole-proof
     porte, T. Oliveira, H. Pacheco, B. Schmidt, and P.-Y. Strub, “Jasmin:               generation and repair with large language models,” in Proceedings of
     High-assurance and high-speed cryptography,” in ACM CCS, 2017.                      the 31st ACM Joint European Software Engineering Conference and
                                                                                         Symposium on the Foundations of Software Engineering, 2023, pp.
[38] M. Barbosa, F. Dupressoir, B. Grégoire, A. Hülsing, M. Meijers, and
                                                                                         1229–1241.
     P.-Y. Strub, “Machine-checked security for XMSS as in RFC 8391
     and SPHINCS+,” in Advances in Cryptology – CRYPTO 2023, ser.                   [55] B. Breen, M. D. Tredici, J. McCarran et al., “Ax-Prover: A deep
     Lecture Notes in Computer Science, vol. 14085. Springer, 2023, pp.                  reasoning agentic framework for theorem proving in mathematics and
     421–454.                                                                            quantum physics,” arXiv preprint arXiv:2510.12787, 2025.



                                                                               14
[56] A. Sosso, A. Arora, and B. Spitters, “Agentic proving for program              TABLE 1. O BJECTS IN A PROOF STEP AND HOW S HANNON P ROVER
     verification,” arXiv preprint arXiv:2605.23772, 2026.                         TREATS THEM . E XAMPLES REFER TO THE RUNNING EXAMPLE OF §3.

[57] P. Song, K. Yang, and A. Anandkumar, “Lean Copilot: Large language
     models as copilots for theorem proving in Lean,” arXiv preprint              Object                 Example                Role in a proof      Handled by
     arXiv:2404.12534, 2024.                                                                                                    step

[58] S. Welleck and R. Saha, “LLMSTEP: LLM proofstep suggestions in               Proof resource:        Alossless_F            Used instead of      Agent chooses;
     Lean,” arXiv preprint arXiv:2310.18457, 2023.                                lemma, axiom, local                           new reasoning        compiler finds
                                                                                  hypothesis                                                         and instantiates
[59] L. Aniva, C. Sun, B. Miranda, C. Barrett, and S. Koyejo, “Pantograph:
                                                                                  Hypothesis stating a   Ofll : islossless      Fills that premise   Compiler
     A machine-to-machine interaction interface for advanced theorem              premise of the         D2(O).O.f
     proving, high level reasoning, and data extraction in Lean 4,” arXiv         chosen resource
     preprint arXiv:2410.16429, 2024.
                                                                                  Invariant,             A relational           Must be invented     Agent
[60] L. Teodorescu, G. Baudart, E. J. G. Arias, and M. Lelarge, “NLIR:            intermediate game,     invariant for a loop
     Natural language intermediate representation for mechanized theorem          new lemma
     proving,” NeurIPS MATH-AI Workshop, 2024.
                                                                                  Module, type           D2(O).O for the        Fills an argument    Compiler
[61] J. B. Almeida, M. Barbosa, G. Barthe, B. Grégoire, V. Laporte, J.-C.                                parameter X            of a resource
     Léchenet, T. Oliveira, H. Pacheco, M. Quaresma, P. Schwabe et al.,           Program structure      The call to guess in Decides whether a      Compiler tracks
     “Formally verifying kyber: Episode iv: Implementation correctness,”                                 the goal             resource applies       it
     IACR Transactions on Cryptographic Hardware and Embedded Sys-                                                            now
     tems, vol. 2023, no. 3, pp. 164–193, 2023.
                                                                                  Side condition         islossless             A goal that          Agent proves it
                                                                                                         D2(O).O.f, if no       remains to be
Appendix A.                                                                                              hypothesis states it   proved

Deferred Explanations of Concepts
                                                                                  compiler recomputes at every proof state which resources
A.1. Proof Resources                                                              apply, instead of treating the project’s lemmas as a fixed
                                                                                  library.
    A proof resource is something the proof can use instead
of reasoning from scratch. The main kinds are lemmas                              What the agent sees. When the compiler shows a resource
already proved in the project or in a library (including equiv-                   to the agent, it gives the name of the resource, its statement
alence lemmas, bridge lemmas, and probability bounds),                            instantiated at the current state, and which of its arguments
axioms and assumptions of the specification, and hypotheses                       remain open (§3.3).
in the current proof. Each of them packages reasoning that
has already been done or assumed; using it at the right point                     Appendix B.
saves the proof from redoing that reasoning.                                      System Architecture
    Two properties of resources matter for ShannonProver.
First, resources are chosen, not invented: the agent decides
which resource to use, whereas an invariant or a new lemma                             Figure 11 shows how ShannonProver is organized. The
has to be created before it can be used. Second, which                            architecture follows one rule: an LLM agent may choose
resources can be used changes as the proof proceeds. Choos-                       proof actions, but it does not own the proof state and does
ing a resource is a strategic decision left to the agent; finding                 not decide when a proof is valid. The figure has four bands,
the resources that apply at the current state and instantiating                   which also define the code categories reported in Section 6.
them is mechanical work done by the compiler (§3). Filling                        Decomposer. The decomposer is the LLM agent of Sec-
a premise of the chosen resource with a hypothesis is part                        tion 5. It writes the intermediate games and lemma state-
of this mechanical work: when a hypothesis in the current                         ments and submits individual lemmas as jobs to a scheduler,
proof states exactly that premise, the compiler uses it (§3.4).                   which runs a bounded number of jobs in parallel. Each job
    Table 1 places proof resources among the other objects                        runs the lemma prover on one lemma and returns either a
that appear in a proof step, using the running example of                         proof that has passed the final check or feedback for the
§3.                                                                               decomposer.
Program structure decides which resources apply. Pro-                             Proof search. Within a job, the orchestrator manages the
gram structure is not a resource, but it determines which                         proof tree of Section 4. Each branch is extended by one
resources can be used. In game-based proofs, many re-                             LLM agent, paired with a branch manager. The agent acts
sources apply only at particular program points: a lemma                          through six actions: commit a tactic, undo the last step, undo
about a procedure call applies only while that call is still                      to a checkpoint, amend an earlier tactic and replay, restart, or
visible in the goal, and a lemma about an oracle applies                          finish. The branch manager checks each action, dispatches
only at a call to that oracle. Each accepted tactic changes the                   it to an EasyCrypt session, and composes the agent’s next
visible program structure, so a resource may not apply yet,                       turn from the current goal, the outcome of the last action,
apply now, or no longer apply. For example, after inline*                         and the output of the proof-state compiler. The orchestrator
replaces a call with the body of the procedure, a lemma                           observes all branches: it spawns agents at branch points,
about that call no longer applies to the resulting goals;                         prunes branches that fall behind, records failed attempts,
this is the unconscious lowering of §2. For this reason, the                      and selects the winning branch.


                                                                             15
                                Job scheduler                        lemma                                 Decomposer (LLM agent)
    Decomposer             runs lemma jobs in parallel;                                         writes the intermediate games and lemma statements;
    (§5)                     merges returned proofs                                                    assembles the proof of the main theorem

                            lemma              proof or feedback
                                                                              one per branch
                                 Orchestrator
    Proof search         spawns agents at branch points            spawn,                                          action            LLM agent
    (§4)                 prunes branches that fall behind           prune             Branch manager
                              records failed attempts                          checks and dispatches each action;           commit a tactic, undo, undo to a
                            selects the winning branch                              composes the next turn                   checkpoint, amend and replay,
                                                                                                                  next turn        restart, or finish



                                                                                                     applicable resources, realized tactics, diagnostics
    Proof-state
    compiler                                                                                Resource and                                     State projection
                                                                                           binding analysis              ProofIR
    (§3)                                  winning proof                     tactic


                                                                                                                                                           new state

    EasyCrypt
    interaction                   Final check                                         EasyCrypt session                                   Event log
    (trusted)            recompiles the proof from scratch                            executes tactics; undo;                    goals, errors, and accepted
                          in EasyCrypt; rejects any admit                               checkpoint replay                          tactics, per proof state



Figure 11. ShannonProver’s architecture. The decomposer hands each lemma to the lemma prover as a job. Within a job, the orchestrator runs one LLM
agent per branch of the proof tree: the agent chooses an action, the branch manager dispatches it to an EasyCrypt session, and the proof-state compiler
turns the resulting state into the agent’s next turn. Only the bottom band is trusted: a tactic changes the proof only if EasyCrypt accepts it, and a proof
counts only after the final check recompiles it from scratch.


Proof-state compiler. After each action that changes the                                  and difficulty levels for the ablation study in the main body.
proof state, the compiler reads the new state from the event                              The public and private parts of the benchmark are described
log and runs the pipeline of Section 3: state projection,                                 below.
ProofIR, and resource and binding analysis. Its output,                                   Building the dataset. Each task in the benchmark is a
namely the applicable resources, realized tactics, and diag-                              single lemma taken from a real cryptographic development
nostics, becomes part of the agent’s next turn. The compiler                              in EasyCrypt, together with the surrounding context it needs
only reads the proof state; it never changes it.                                          (i.e., sibling definitions, cloned theories, and imported lem-
EasyCrypt interaction. The bottom band is the only part of                                mas). We remove the original proof; the task is to reconstruct
the system that interacts with EasyCrypt, and it is the trust                             a proof script for the lemma, with its statement and context
boundary. An EasyCrypt session executes tactics, supports                                 unchanged. Each lemma is labeled with the scheme from
undo and checkpoint replay, and records every goal, error,                                which it comes, the cryptographic property it concerns, the
and accepted tactic in an event log. A tactic changes the                                 proof techniques it requires, and a difficulty level.
proof only if EasyCrypt accepts it. When a branch finishes,                               The four parts and what each one measures. The bench-
the final check writes the proof into the source file, recom-                             mark is organized into four parts of increasing realism and
piles the file from scratch in EasyCrypt, and rejects the proof                           difficulty. They differ in where the proofs come from, how
if any admit remains. Errors in the agents, the orchestrator,                             hard they are, and crucially whether they could have been
or the compiler can therefore waste time, but they cannot                                 seen during a model’s pretraining.
cause an invalid proof to be accepted.                                                    ❶ Foundational primitives. Textbook and building-block
                                                                                          schemes such as ElGamal and hashed-ElGamal, Schnorr,
Appendix C.                                                                               pseudorandom generators, private information retrieval, Ped-
                                                                                          ersen commitments, and the correctness of Cramer–Shoup.
Dataset and Additional Case Studies                                                       These are short, local proofs, and they test whether the
                                                                                          basic proof-state representation is adequate: finite-set and
C.1. Dataset Construction                                                                 list algebra, simple relational coupling, losslessness, and
                                                                                          single textbook reductions. This part establishes the floor
    Our benchmark collects proof tasks from EasyCrypt de-                                 of the benchmark and isolates interface issues from genuine
velopments of cryptographic schemes. It complements math-                                 reasoning difficulty.
ematical theorem-proving resources such as LeanDojo [23]                                  ❷ Deployed real-world schemes. This part includes stan-
with tasks involving probabilistic and relational programs,                               dardized real-world schemes (e.g., ChaCha20-Poly1305,
adversaries and oracles, bad events, game hops, and security                              which we use as a case study). Unlike Part ❶, these are
reductions. We use a subset spanning different proof types                                large, multi-lemma developments, so they test whether an


                                                                                     16
LLM agent can move beyond isolated lemmas and find                    CBC, we report the three final theorem targets together with
useful proof resources across lemmas, such as long game-              the helper lemmas that the decomposer proposed for them.
hop chains, oracle invariants, bad-event probability bounds,          For CMAC, we report individual lemma and equivalence
and reasoning that depends on context established by other            statements, each counted once even if it was attempted more
lemmas in the same project.                                           than once. These counts refer to different proof tasks and
❸ Post-quantum standards. Lemmas from the machine-                    are not compared as success rates.
checked proofs of the NIST post-quantum standards: the                MEE-CBC. The agents receive the security model and
IND-CCA security of ML-KEM (FIPS-203) [22,61], the                    selected targets with their intermediate human lemmas re-
tight security proof of SLH-DSA/SPHINCS+ [14], the re-                moved. Using Opus 5 for decomposition and Opus 4.8 for
lated XMSS development [38], and the security argument                lemma proving, ShannonProver constructs auxiliary lem-
of ML-DSA/Dilithium. These are the most demanding and                 mas and their proofs in separate runs for the selected
most current proofs in the benchmark, addressing the same             tasks. It completes all three final targets: confidentiality
problems that the standardization community itself verifies:          (RCPA_security), plaintext integrity (PTXT_security), and
lattice hardness assumptions, the Fujisaki-Okamoto trans-             functional correctness (mee_correct). Across the three tar-
form, and hash-based signature arguments. Because these               gets, the decomposer proposed 33 helper lemmas, and the
developments are recent and specialized, they also test               lemma prover proved all 33 together with the three targets;
whether an LLM agent can operate on proofs that lie well              each target run took 23–41 minutes.
outside the well-trodden textbook material.                                The experiment reuses existing verified dependencies,
❹ A published case study with non-public proof scripts. This          including the CBC library and its security proof. The agent-
part consists of the CMAC/CBC-MAC family of proofs.                   generated proofs are combined with retained proofs in the
We obtained the scripts directly from their authors, who              final source files. Thus, the result establishes the three
authorized their use in this evaluation. To our knowledge,            target theorems without requiring the agents to regenerate
these scripts have not been publicly released. This reduces           every proof in the supporting libraries. The final sources are
the chance that a model has seen these particular proofs              available in the MEE-CBC proof browser.
during training, although it does not rule out exposure to
related mathematics or proof techniques.                              CMAC. For CMAC, we evaluate lemma proving only
                                                                      (Phase III): the lemma and equivalence statements come
Sources and availability. Parts ❶–❸ are built from publicly           from the original development, and we report how many of
available formal developments: the EasyCrypt example suite            them now have proofs that EasyCrypt accepts. The original
and standard libraries for the foundational and deployed              development contains 333 named statements, which we kept
schemes, and the public machine-checked artifacts for the             unchanged except for updates to EasyCrypt syntax. Of these,
post-quantum standards. For these parts, we will openly               299 have agent-generated proofs: 239 were proved directly,
release our benchmark. Part ❹ is the exception: the CMAC              and 60 reuse a proof found for a matching statement in
development is private. Its proof scripts are not available in        another file. Five keep their existing proofs, and 29 remain
any public repository, and we obtained them directly from             unfinished, including the final theorem CMAC_security. One
the development’s authors for the purpose of this bench-              file, which relates EMAC to CMAC, could not be loaded
mark. We report aggregate CMAC results without releasing              and referred to missing definitions; we reconstructed it
the underlying private scripts. Readers seeking access should         and report its 11 statements separately: nine have agent-
contact the original authors.                                         generated proofs and two remain unfinished. All proofs are
Scope and difficulty. In total the benchmark comprises                checked against the supplied dependencies, some of which
more than 1,600 lemma-level obligations across these four             remain unproved. The counts therefore show how much of
parts, with the post-quantum developments contributing the            the proof work is done, not a complete CMAC security
largest share. Within every part, obligations span three dif-         proof; since lemmas differ in difficulty, they also do not
ficulty levels: “easy” obligations test local proof mechan-           measure how much expert effort is saved.
ics, “medium” ones require selecting and following a non-
trivial proof strategy, and “hard” ones are the security-proof
                                                                      C.3. Expert Comments on MEE-CBC and CMAC
components—adversary and oracle reasoning, game hops,
and probability-bound composition. Because some of the
                                                                          We consulted experts who participated in the develop-
developments were written for older versions of the proof
                                                                      ments or had substantial knowledge of them, and received
assistant, we port them to current EasyCrypt where feasible
                                                                      their comments on how LLM agents can accelerate their
and record, per obligation, whether it is machine-checkable
                                                                      work.
today; the obligations that remain are flagged so that the
benchmark grows as more developments can be loaded and                MEE-CBC. This development started from an existing
checked.                                                              proof that CBC mode is secure with uniformly random
                                                                      IVs, which was composed with a new proof that MAC-
C.2. Final Results for MEE-CBC and CMAC                               then-Encode-then-Encrypt is INT-PTXT secure. This new
                                                                      proof was formalized by an expert EasyCrypt user with one
   Table 2 summarizes the completed proofs and the re-                person-week of effort. A further proof refining the security
maining obligations in the two case studies. For MEE-                 result to an implementation model (a C-like imperative


                                                                 17
  TABLE 2. F INAL RESULTS FOR MEE-CBC AND CMAC. F OR MEE-CBC, THE DECOMPOSER PROPOSED THE HELPER LEMMAS FOR EACH FINAL
               THEOREM ; FOR CMAC, THE LEMMA AND EQUIVALENCE STATEMENTS COME FROM THE ORIGINAL DEVELOPMENT.


 Case study and scope                                  Completed proofs                                 Unfinished proofs
 MEE-CBC: confidentiality (RCPA_security)              Final theorem and its 8 helper lemmas            None for this target
 MEE-CBC: plaintext integrity (PTXT_security)          Final theorem and its 4 helper lemmas            None for this target
 MEE-CBC: functional correctness (mee_correct)         Final theorem and its 21 helper lemmas           None for this target
 CMAC: 333 original statements, with syntax            304: 299 with AI-generated proofs and 5          29, including CMAC_security
 changes where needed                                  with existing proofs
 CMAC: 11 reconstructed EMAC-to-CMAC                   9, all with AI-generated proofs                  2: pr_PRP_PRF_ECBC and CMAC
 statements
MEE-CBC uses an existing verified CBC library. Of the 299 CMAC statements with AI-generated proofs, 239 have newly found proofs and 60 reuse an
AI-generated proof checked for another matching statement. CMAC lemma proofs are checked under the supplied dependencies, some of which remain
unproved; the complete CMAC security proof is unfinished.


model in EasyCrypt) took an additional person-week from                    trying to use pr_RO_FinRO_D and inlining eager and lazy
the same expert. The main source of expert judgment in                     loops. The useful next step was to apply byequiv and reason
this development is in choosing the right abstractions and                 about the calls to chacha_enc2 and poly_mac2. The agent
modularizing the proof; once this structure was fixed, much                followed name similarity without matching the lemma to the
of the remaining work was mechanical proof engineering.                    procedure calls in the current goal.
Experts commented that the novel part of the MEE-CBC                       ❸ Agent flinch: not applying an identified lemma. The
proof involved little human insight, and would have been                   agent repeatedly identified the right strategy: use byequiv,
automated with LLM agents.                                                 apply the bridge lemma pr_CCP_OCCP, and use the PRF
CMAC. The proof for CMAC took three person-months                          distinguishing argument. It proposed this plan four times but
by ordinary users of EasyCrypt. This effort also included                  never applied the bridge lemma. Instead, it tried local tactics
identifying and resolving small issues in the pen-and-paper                such as proc; inline * and wp; skip; smt(), or restarted
proof, as well as making nontrivial design decisions for                   the proof. The difficulty was in supplying the arguments
a part of the argument that could not be formalized as                     needed to apply the lemma. The baseline interface did not
written. (The formalized bound is looser than the pen-and-                 provide the typed argument information needed to turn the
paper bound as a result.) The experts suggested that the                   plan into a proof step.
CMAC proof could have been greatly accelerated with LLM                    Standout agent proofs. Agent proofs are sometimes better
agents, not only by reducing the amount of mechanical proof                than the human proofs. For five ChaChaPoly lemmas, the
work, but also by surfacing issues in the pen-and-paper proof              experts judged the agent proof better in concision, read-
earlier and helping inform the high-level proof decisions that             ability, and semantic idiom (Fig. 10). We describe the two
affect the theorem statement.                                              marked with stars in the figure.
                                                                                chacha_spec: stating the loop invariant with the spec-
Appendix D.                                                                ification. The lemma states that the loop implementing
                                                                           ChaCha20 encryption computes the functional specifica-
Baseline Failure Examples and Standout Agent                               tion gen_CTR_encrypt_bytes, which encrypts the message
Proofs                                                                     block by block with counters 1, 2, . . .. The difficulty is the
                                                                           loop invariant. The human proof states it in terms of the
    Baseline runs, in which the agent interacts directly with              number of blocks that remain to be encrypted, so each
EasyCrypt, show the three failure patterns of §2.                          iteration must show by integer arithmetic that this number
❶ Unconscious lowering: inlining before applying an equiv-                 decreases by exactly one, with a case split on whether
alence. The agent recognized that the oracle equivalence                   a full block remains (23 lines). The agent instead states
equ_cc should be applied at a procedure call and recovered                 the invariant with the specification itself: the ciphertext
its quantified parameters. It then used inline *. Although                 produced so far, followed by the encryption of the remaining
EasyCrypt accepted this tactic, it removed the call structure              message from the current counter, equals the encryption
needed to apply the equivalence. The agent spent 35 minutes                of the whole message. One iteration is then exactly the
on the resulting unsuccessful proof attempt. The baseline                  existing lemma that removes one block from the encryp-
interface did not warn that inlining would make the intended               tion (gen_CTR_encrypt_bytes_cons), and loop exit is the
lemma inapplicable.                                                        lemma for the empty message (gen_CTR_encrypt_bytes0).
❷ Semantic mislocalization: choosing a lemma by its name.                  The arithmetic is still needed, but it is already done inside
The agent searched around IFinRO/IndRO and chose a lemma                   these lemmas, so the proof takes 7 lines.
whose name looked relevant. It spent more than 25 minutes                       step4_badi: describing the bad event exactly. This



                                                                      18
lemma is one step of a union bound in the integrity proof.
Each call to an internal procedure samples a fresh tag and
compares it with a list of earlier tags; the game records every
compared pair in a list lbad1, and a collision in any pair
is a bad event. To bound the probability of a collision, the
proof bounds each position i of lbad1 separately. For this,
it uses a modified game that, in the call that fills position
i, records in a flag badi whether the fresh tag equals the
earlier tag at that position. The lemma states that a collision
at position i in the original game is no more likely than badi
in the modified game, and the proof relates the two games
one call at a time. The human proof (73 lines) carries an
auxiliary invariant relating the length of lbad1 to the number
of queries so far, and distinguishes four cases for each call:
no pair is added, or position i was filled earlier, is filled by
this call, or is still empty afterwards. The agent’s proof (41
lines) states the relation between the two games directly:
before position i is filled, badi is false, and after it is filled,
badi holds exactly when the pair at position i collides. Each
call then only needs to check whether it fills position i, and
the auxiliary invariant on the length of lbad1 is no longer
needed.

Appendix E.
Ethics Considerations
Research scope. This work studies automated construc-
tion of formal cryptographic proofs. It does not involve a
recruited human-subject study, collect or process sensitive
personal data, or deploy experiments on third-party systems.
It does not report new vulnerabilities in deployed systems
requiring coordinated disclosure. The permissions for the
cryptographic developments used in our evaluation, includ-
ing the non-public CMAC development, and the use of
generative AI are discussed in Section 9.
Benefits and limitations of proof automation. The in-
tended benefit of ShannonProver is to reduce the effort
needed to obtain machine-checked cryptographic proofs. A
risk is that users may overinterpret an accepted proof as an
unconditional guarantee about a deployed system. The guar-
antee is limited to the formal statement, its assumptions, and
the trusted verification infrastructure; it does not establish
that a model captures every property of an implementation.
Users must therefore review the specification and theorem
statements, and check the final proof scripts with EasyCrypt.
An unsuccessful search also does not establish that a theo-
rem is false. These boundaries are essential to using proof
automation to support, rather than replace, judgments about
cryptographic security.




                                                                      19
