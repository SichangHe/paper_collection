                                               Verified Secure Compilation for Mixed-Sensitivity
                                                             Concurrent Programs

                                                                       Robert Sison∗ † and Toby Murray∗
                                                     ∗ School of Computing and Information Systems, University of Melbourne, Australia
                                                                      † CSIRO’s Data61 and UNSW Sydney, Australia

                                                                      (e-mail: [firstname].[lastname]@unimelb.edu.au)
arXiv:2010.14032v2 [cs.PL] 28 Feb 2022




                                                                                        Abstract
                                         Proving only over source code that programs do not leak sensitive data leaves a gap between reason-
                                         ing and reality that can only be filled by accounting for the behaviour of the compiler. Furthermore,
                                         software does not always have the luxury of limiting itself to single-threaded computation with re-
                                         sources statically dedicated to each user to ensure the confidentiality of their data. This results in
                                         mixed-sensitivity concurrent programs, which might reuse memory shared between their threads to
                                         hold data of different sensitivity levels at different times; for such programs, a compiler must preserve
                                         the value-dependent coordination of such mixed-sensitivity reuse despite the impact of concurrency.
                                            Here we demonstrate, using Isabelle/HOL, that it is feasible to verify that a compiler preserves
                                         noninterference, the strictest kind of confidentiality property, for mixed-sensitivity concurrent pro-
                                         grams. First, we present notions of refinement that preserve a concurrent value-dependent notion
                                         of noninterference that we have designed to support such programs. As proving noninterference-
                                         preserving refinement can be considerably more complex than the standard refinements typically
                                         used to verify semantics-preserving compilation, our notions include a decomposition principle that
                                         separates the semantics-preservation from security-preservation concerns. Second, we demonstrate
                                         that these refinement notions are applicable to verified secure compilation, by exercising them on a
                                         single-pass compiler for mixed-sensitivity concurrent programs that synchronise using mutex locks,
                                         from a generic imperative language to a generic RISC-style assembly language. Finally, we exe-
                                         cute our compiler on a nontrivial mixed-sensitivity concurrent program modelling a real-world use
                                         case, thus preserving its source-level noninterference properties down to an assembly-level model
                                         automatically. All results are formalised and proved in the Isabelle/HOL interactive proof assistant.
                                            Our work paves the way for more fully featured compilers to offer verified secure compilation
                                         support to developers of multithreaded software that must handle data of multiple sensitivity levels.


                                         1    Introduction
                                         Here we show how to extend secure compilation support to programs that are designed to
                                         address two fundamental problems of scale: (1) the need to divide work in computer systems
                                         that handle information, and (2) the need to share scarce resources to be able to service every
                                         customer for whom that work is done. There will always be a program for which that sharing
                                         is not abstracted; that program’s responsibility is to implement that sharing in such a way
                                         that it never allows the information of one customer to flow to another. In this paper, we
                                         prove formally that a compiler does not break that program’s responsibility.
                                             © CSIRO (ABN 41 687 119 230), Robert Sison, and Toby Murray 2019-2021; accepted manuscript to
                                         appear (excl. appendices) in CUP JFP Special Issue on Secure Compilation; licensed under CC BY-NC-ND 4.0


                                                                                            1
  It is well known that program translations of the kind carried out by compilers can easily
break security properties like confidentiality (Kaufmann et al., 2016; Barthe et al., 2018).
This is especially the case for mixed-sensitivity concurrent programs, which feature both:

    • Concurrency of access to memory locations shared between different threads of ex-
      ecution. A compiler must preserve both (1) the synchronisation that coordinates
      threads’ access to shared memory, and (2) the absence of any internal timing leaks, to
      prevent them from manifesting as storage leaks (Volpano & Smith, 1998).

    • Mixed-sensitivity reuse of shared memory to hold information of different sensitivity
      levels at different times. A compiler must preserve the program functionality that co-
      ordinates this reuse; this implies support for value-dependent classification policies,
      which allow the classification of a memory location to change dynamically depending
      on values held in other memory locations (Murray, 2015). Furthermore, it must do so
      accounting for the potential impact of concurrent access by other threads.

   Although existing verified compilers for dialects of mainstream programming languages,
like CompCert (Leroy, 2009) and CakeML (Kumar et al., 2014), have been proved to pre-
serve program functionality (semantics) and some timing-sensitive forms of noninterfer-
ence (Barthe et al., 2020), none are yet verified to preserve proofs of noninterference for
mixed-sensitivity concurrent programs. Ideally such a compiler, applied to the threads of a
proved-secure mixed-sensitivity concurrent program, would yield assembly code that, run
concurrently, also composes into a secure mixed-sensitivity concurrent program.
   To this end, here we present notions of concurrent value-dependent noninterference-
preserving refinement, which are compositional across the threads of mixed-sensitivity con-
current programs. In these notions, the usual square-shaped commuting diagram commonly
used to depict (semantics-preserving) refinement (Figure 4a) has been replaced by a cube
(Figure 3). This reflects that it preserves a 2-safety hyperproperty (Terauchi & Aiken, 2005;
Clarkson & Schneider, 2010), which compares two executions rather than examining a sin-
gle one. Our earlier work (Murray et al., 2016b) was the first to make this observation
and to propose a general cube-shaped refinement property; however other work on veri-
fied secure compilation targeted towards noninterference preservation (Barthe et al., 2018,
2020) since made the same observation. As these cube-shaped properties are significantly
more complicated to prove than standard notions of semantics-preserving refinement typ-
ical in verified compilation (Leroy, 2009; Kumar et al., 2014), we present a principle of
decomposing the cube (Figure 3) into three separate obligations (Figure 4): the first of these
is akin to semantics-preserving refinement, while the rest prevent the introduction of any
termination- and timing-leaks. A simple comparison of proof effort for a refinement exam-
ple (Figure 2) shows this approach can almost halve its complexity, and that it is applicable
to proofs of refinement for programs with secret-dependent control flow—the example pads
an if h then . . . else . . . fi conditional with skips, so as not to introduce a timing leak of h.
   We then go on to demonstrate that the decomposition principle we provide makes our
notion of refinement a tractable target for verified secure compilation. Our compiler is an
executable function in Isabelle/HOL that translates mixed-sensitivity concurrent programs
that synchronise using mutex locks, from a generic imperative While language to a generic
RISC-style assembly language. In particular, it supports the class of programs that avoid all


                                                2
implicit flows, where a secret determines the choice between two control flow paths with dif-
ferent observable effects, by disallowing any secret-dependent control flow—for example,
disallowing if h then . . . else . . . fi conditionals to prevent any timing leaks from h. This is
a common approach against implicit flows, as it avoids any precise source-level reasoning
about time. To preserve confidentiality for programs that take that approach, we instanti-
ate the decomposition principle so that it enforces that our compiler does not introduce any
new secret-dependent control flow. Furthermore, as part of satisfying the demands of our
refinement notion, our compiler demonstrates a way of formalising and proving when it is
safe for a compiler to perform optimisations in the presence of concurrency. To ensure that
the contents of shared memory locations are preserved under compilation despite potential
interference from other threads, our compiler tracks which shared memory locations are free
from data races. It then makes use of this tracking to avoid redundant loads from “stable”
(i.e. race-free) shared variables safely, that would otherwise be considered unsafe to omit.
   Finally, to show that the compiler preserves noninterference for actual mixed-sensitivity
concurrent programs, we execute it on a real-world use case: a model of the software-
componentised input-handling regime for the Cross Domain Desktop Compositor (Beau-
mont et al., 2016), a device that enforces information-flow control over input classified
dynamically by a trusted user. We leave treatment on the design and application of per-
thread proof techniques establishing CVDNI for the successive versions of this model to
other works (Murray et al., 2018; Sison, 2020), and here focus on its CVDNI-preserving
compilation—expanding on Sison & Murray (2019), the conference version of this paper.
This yields the first proofs of noninterference for an assembly-level model of a nontrivial
mixed-sensitivity concurrent program, demonstrating the power of verified secure compila-
tion to preserve security properties of compiled code.
   The structure of our paper is as follows. First, we present language-independent notions
of noninterference and its refinement, designed for mixed-sensitivity concurrent programs
(Section 2). Our attention then turns to preliminaries for our compiler: the main properties
of interest of the source While language it compiles (Section 3), and of the target RISC
language it produces (Section 4). Then, after presenting the details of our compiler and its
verification (Section 5), and the case study to which we apply it (Section 6), we discuss the
most closely related work in the area (Section 7), before concluding (Section 8).
   We expand on the conference version of this paper (Sison & Murray, 2019) as follows:

    • Here we have adapted the noninterference properties to support assumptions on initial
      memory and extra security requirements; these will allow us to clarify exactly what
      our compiler is verified to preserve, and for which kinds of programs.

    • We also in Section 2 present further preliminaries that will allow us to explain in
      greater detail the different ways to establish and use proofs about a verified compiler
      to obtain whole-system noninterference at the target-language level. These include:

         1. The side conditions and theorem of compositionality for the noninterference
            properties. In Section 3, we then for the first time present the proof, whose de-
            tails were elided from Sison & Murray (2019), for a noncompositional “global”
            part of this side condition, which is necessary to obtain whole-system noninter-
            ference from per-thread noninterference both at source and target level.


                                                3
        2. A whole-system refinement theorem, adapted to support assumptions on ini-
           tial memory. This theorem was alluded to in Murray et al. (2016b) but, until
           now, has never been formally presented outside of the Isabelle/HOL theories. It
           gives us a means to prove preservation of whole-system noninterference by the
           compiler, without having to re-prove the noncompositional side condition at the
           target-language level.

    • In Section 5, we then compare alternative methods of obtaining whole-system security
      at RISC level, that a developer would choose depending on whether all, or only some
      threads are compiled with our compiler. In contrast, Sison & Murray (2019) stopped
      after presenting the application of refinement decomposition principle.

    • In Section 6, the case study to which we apply the compiler is significantly expanded,
      being a 3-component version of the CDDC input-handling program—closer to a ver-
      sion presented in Murray et al. (2018)—as opposed to the 2-component version of
      Sison & Murray (2019).

    • Furthermore, we present substantially more details of our case study in Section 6,
      which were mostly elided from Sison & Murray (2019). These include formal state-
      ments of both the source-level properties preserved and the target-level properties
      obtained, alongside explanations of all alternative methods for obtaining the latter
      from the former.

    • Finally, every lemma and theorem we prove is presented with a proof sketch or ex-
      planation, which were largely absent from Sison & Murray (2019). We also include
      here appendices with further details of our compiler (see Appendices A, B, and C).



2    Noninterference and its refinement for mixed-sensitivity con-
     current programs
To support mixed-sensitivity concurrent programs, we verify our compiler to preserve the
concurrent value-dependent noninterference (CVDNI) notions of Murray et al. (2016b). In
this section we present the definitions of CVDNI and its refinement, as we have adapted
them from that work’s Isabelle formalisation (Murray et al., 2016c,a). In particular, the ver-
sion of the theory we present here supports extra customisation of requirements beyond the
prior work; we will need this to parameterise the theory with initial conditions needed for
a compositionality property of our source language (Section 3), and our compiler’s preser-
vation of a ban on secret-dependent control flow (Section 5). Furthermore, it is simplified
to the case where the shared memory is the same for both the original abstract and the
refined concrete program—refinement adds no new shared variables. Later, we will instan-
tiate this CVDNI theory to have our compiler’s source and target languages (Sections 3, 4)
respectively play the roles of the abstract and concrete programs’ languages in the theory.
   We begin by introducing with an illustrative example the challenges of verifying value-
dependent noninterference in the presence of shared-variable concurrency (Section 2.1).
Then we present the per-thread and whole-system noninterference properties themselves


                                              4
while TRUE do
      lock(workspace lock);
      while !suspended do
            lock(source lock);
            workspace := source;
            /* . . . operations on workspace . . . */
            if domain = LOW then                        (b) The phone providing the High personality:
                                                        domain ̸= LOW, and source is classified High
                   low sink := workspace
                                                        to reflect that the user might type in secrets.
            else
                   high sink := workspace;
                   workspace := 0
            fi;
            unlock(source lock)
      od;
      unlock(workspace lock);                           (c) The phone displaying visual indicators that
      while suspended do skip od                        it is providing the Low personality: domain =
od                                                      LOW, and source is classified Low to reflect
                                                        that we trust the user not to type in secrets.
     (a) Input processing worker thread program

Figure 1: Example: Touchscreen input processing for a dual-personality smartphone.
Reproduced from Sison & Murray (2019).


(Section 2.2), followed by the notion of per-thread refinement that preserves the per-
thread property between the two languages (Section 2.3). As the cube-shapedness of
noninterference-preserving refinement diagrams in general makes them difficult to apply
directly to compiler verification, we present a decomposition principle (Section 2.4) that we
will use to prove CVDNI-preserving refinement for our compiler. We then present require-
ments and a theorem for whole-system refinement by which we have that CVDNI-preserving
refinement is compositional across the threads of the program being compiled, such that it
yields the whole-system property at the target language level (Section 2.5).

2.1     Illustrative example of a mixed-sensitivity concurrent program
Consider the task of verifying a multithreaded system that manages the user interface (UI)
for a dual-personality smartphone, a phone that provides clearly distinguished user contexts
(personalities), typically for work versus leisure. Specifically, our task is to verify that
it does not leak sensitive information intended only for one of those personalities, which
we classify High (Figure 1b), to locations belonging to the other, which we classify Low
(Figure 1c).
   Here and generally throughout this paper, our attacker model is an entity that can read
from the system’s untrusted sinks: some subset of permanently Low-classified locations not
subject to synchronisation. In our example, the untrusted sinks may include WLAN device
registers in a hostile environment.
   The smartphone’s UI system consists of a number of threads running concurrently with a
shared address space; we aim to verify that, as a whole, this system of threads satisfies the
security requirement. However, to avoid a state space explosion that is exponential in the


                                                        5
number of threads, we must do this compositionally: one thread at a time, then combining
the results of these analyses.
   We focus on a particular worker thread (Figure 1a), the one responsible for sending touch-
screen input from the source variable to its intended destination.
   The first challenge is that the destination depends on which personality the phone is cur-
rently providing, which is indicated by the value of domain. This is reflected by the classi-
fication of source being dependent on the value of domain: source is classified Low exactly
when domain = LOW (where LOW is a designated constant), and is classified High other-
wise. Due to this dependency, domain is known as a control variable of source.
   The second challenge is the worker thread runs in a shared address space that might be
accessed or modified by other threads, for various purposes. One of these threads may
be responsible for maintaining that domain = LOW exactly when the phone indicates it
is providing the Low personality (Figure 1c), so the user knows not to type in anything
sensitive. Another thread may be responsible for assigning suspended := TRUE when the
user turns the phone’s screen off, to make the worker stop processing touchscreen input. We
may then wish for workspace to be usable by some other thread—for example, processing
input from a fingerprint scanner—in such a way that it can assume that workspace no longer
contains any sensitive values.
   When we analyse one thread like this worker in terms of our compositional security prop-
erty (Section 2.2), all the other threads in the system are trusted to do two things:

   1. They follow a synchronisation discipline; in particular for this example, this is a mu-
      tual exclusion (mutex) locking discipline: If read- or write-access to a certain variable
      is governed by a lock, each thread may only access the variable in that manner if
      they hold that lock. Mutual exclusion then follows from the semantics of the locking
      primitives ensuring only one thread may hold a given lock at a time.

   2. They themselves do not leak values from High-classified locations (we refer to such
      values themselves as High) to Low-classified locations that are read-accessible to
      other threads. Note that, here, it is our objective to prove that the thread we are
      analysing can be trusted in the same way.

Even under these assumptions, the concurrency gives rise to some tricky considerations.
   First, it is important that no thread in the system (including the one under analysis) mod-
ifies any control variables carelessly. For example, writing domain := LOW immediately
after the worker reads a High value from source, will cause it to leak to low sink. To prevent
this, the worker uses source lock, granting it exclusive write-access to source and domain.
   Furthermore, as noted above, we may want to ensure that a non-attacker-observable lo-
cation is nevertheless cleared of any sensitive values before being used by another thread.
In our example, we classify workspace Low for the analysis to enforce this when the worker
is suspended, but as the worker sometimes uses it to process High values, it is important
to know workspace is accessible only to the worker during that time. To ensure this, the
worker uses workspace lock, granting it exclusive read- and write-access to workspace. It
is then responsible for clearing it of any High values by the time it releases that access.




                                              6
2.2     Concurrent value-dependent notions of noninterference
Having illustrated the challenges with an example, we now present the definitions of per-
thread and whole-system noninterference, the theorem by which the former composes into
the latter, and the compositionality side conditions demanded by that theorem.
   As proved for each thread, CVDNI is defined by Murray et al. (2016b) in terms of:

   1. A binary strong low-bisimulation (modulo modes) relation B between program con-
      figurations, which serves as witness to CVDNI. In the style of other low-bisimulation–
      based noninterference definitions (Focardi et al., 1995; Sabelfeld & Sands, 2000;
      Mantel et al., 2011) it requires the program configurations it relates to agree on their
      “low”-observable portions, and demands that lock-step execution preserves that cor-
      respondence. Furthermore, it is rely–guarantee-style concurrency aware, following
      Mantel et al. (2011), but modified to allow value-dependent classifications (Murray,
      2015) for mixed-sensitivity reuse (see next point).

   2. A classification function L that determines the “low”-observable portion of a pro-
      gram configuration, thus affecting B’s requirements. The innovation of L , as pa-
      rameterised first by Murray (2015) and then by Murray et al. (2016b) as reproduced
      here, is that L can depend on values in the program configuration itself, thus express-
      ing dynamic and not just static classifications.

   The theory is parameterised over the type of values Val, a finite set of shared variables Var,
and a deterministic evaluation step semantics ⇝ between local configurations of a thread in
a concurrent program. Each local configuration is a triple ⟨tps, mds, mem⟩:

      • tps :: ThreadPrivate is the thread-private state, which the theory will consider to be
        permanently inaccessible to the attacker and not shared with the other threads. Note
        that, due to this inaccessibility, we allow the user of the theory to parameterise the
        type ThreadPrivate, and we do not impose any particular structure on it.

      • mds :: Mode ⇒ Var set is the (assume–guarantee) mode state, which is ghost state as-
        sociating each of Mode ≜ {AsmNoW, AsmNoRW, GuarNoW, GuarNoRW} with
        a set of shared variables. Intuitively, it identifies the set of variables for which the
        thread currently Assumes it possesses (or Guarantees it respects) exclusive permis-
        sion to Write (or Read and Write), granted (or obligated) for those variables typically
        by some synchronisation scheme. This facilitates compositional, rely–guarantee-style
        reasoning about such access (Jones, 1981; Mantel et al., 2011).
        For example, when our worker thread (of Figure 1a) holds source lock, it as-
        sumes that no other threads write to source or its control variable domain
        (i.e. {source, domain} ⊆ mds AsmNoW), otherwise it guarantees it does not write
        to them (GuarNoW). Similarly, when it holds workspace lock it assumes that no
        other threads read or write to workspace (i.e. workspace ∈ mds AsmNoRW), and at
        all other times it makes the corresponding guarantee (GuarNoRW).

      • mem :: Mem is shared memory considered potentially accessible to the attacker and
        other threads. To make what is accessible amenable to analysis, we impose the struc-
        ture Mem ≜ Var ⇒ Val, a total map from shared variable names to values.

                                                7
   The theory is then further parameterised by the value-dependent classification function
L :: Mem ⇒ Var ⇒ {High, Low}, inducing a function C vars :: Var ⇒ Var set that returns
all the control variables of a given variable. In our worker thread example, L mem x gives:

    • High when x is high sink, meaning high sink is classified High at all times.

    • when x is source: Low if mem domain = LOW, and High otherwise.

    • Low for all other variables x, meaning they are classified Low at all times.

   The set C = {y | ∃x. y ∈ C vars x} is then defined to contain all control variables in the
system. Thus in our worker thread example, C vars source = {domain} and C = {domain}.
   With these parameters having been set, we can now define notions of observational equiv-
alence—underpinning noninterference properties—that are value dependent.
   The notion of observational equivalence of memories, used by the whole-system non-
interference property to quantify over initial state pairs, is as follows: Variables that are
value-dependently classified Low according to both memories are required to have the same
value in both memories. Formally, as defined originally by Murray (2015):

Definition 2.1 (Low-equivalent memories).

            mem1 =Low mem2 ≜ ∀x. L mem1 x = Low −→ mem1 x = mem2 x

Note that the asymmetry of Definition 2.1 (also Definition 2.3 to follow) referring only to
mem1 is resolved by requiring the classification function L to classify all control variables
as Low statically—that is, Low always, regardless of the memory state (cf. our restriction
Proposition 3.4 on the classification of state used to implement locks, later in Section 3.2).
   To support compositionality for concurrent programs, however, the equivalence notion
for the per-thread noninterference property is relaxed to be modulo modes in the style of
Mantel et al. (2011): Here, Low-classified non-control variables x ∈  / C are only required
to have the same value if they are assumed to be readable by other threads according to
the mode state. (Control variables x ∈ C are excluded from that relaxation, and are always
required to be equal.) Defined more formally, again as originally by Murray (2015):1

Definition 2.2 (Readability of variable x, according to mode state mds).

                             readable mds x ≜ x ∈
                                                / mds AsmNoRW

Definition 2.3 (Low-equivalence of memories, modulo the mode state mds).

     mem1 =Low
           mds mem2 ≜
           ∀x. x ∈ C ∨ L mem1 x = Low ∧ readable mds x −→ mem1 x = mem2 x

Moreover, we will use notation lc1 =Low mds lc2 from Sison & Murray (2019) to lift Defini-
tion 2.3 to local program configurations, asserting also that the local configurations lc1
and lc2 have the same assume–guarantee mode state. Additionally, we will use notation
lc1 =mds lc2 to denote (only) that lc1 and lc2 have the same assume–guarantee mode state.
  1 Logical operator precedence here is just as in Isabelle/HOL—from most tightly to least: ∧, ∨, −→.




                                                    8
   Thus, intuitively, the user of the theory should model the permanent untrusted output
sinks, of their whole concurrent program, as variables for which L always returns Low,
ungoverned by any synchronisation scheme that the attacker cannot be trusted to follow. In
our worker example program (of Figure 1a), low sink is untrusted permanently in this way,
but workspace is untrusted only when unlocked.
   We now have almost enough definitions to state the per-thread compositional secu-
rity property. This property will assert the existence of a witness bisimulation relation
B for every possible observationally equivalent pair of starting configurations. Specifi-
cally, this witness relation must be a strong low-bisimulation (modulo modes) (denoted by
strong-low-bisim-mm B), meaning that it must satisfy the following three conditions:
   1. It must maintain observational indistinguishability by requiring that all configuration
      pairs it relates (i.e. (lc1 , lc2 ) ∈ B) that have the same mode state (lc1 =mds lc2 ), are
      low-equivalent modulo modes (lc1 =Low      mds lc2 ).

   2. Furthermore, it must be a bisimulation by being symmetric (denoted by sym B) and
      progressing to itself : Any step taken by one of the configurations (lc1 ⇝ lc′1 ) must
      be matched by some step taken by the configuration related to it (lc2 ⇝ lc′2 ), so the
      destinations remain related (i.e. (lc′1 , lc′2 ) ∈ B) and modes-equal (lc′1 =mds lc′2 ).

   3. Finally, it must be closed under globally consistent changes made to memory by other
      threads (denoted by cg-consistent B)—that is, changes that preserve low-equivalence
      and are permitted by the current mode state mds. Specifically, other threads are per-
      mitted to change either of variable x’s value or its classification only when x is consid-
      ered writable by the current mode state (denoted by writable mds x, Definition 2.5).
      This is the most crucial element of the per-thread CVDNI property itself that ensures
      its compositionality for concurrent programs.
These requirements are formalised by Definition 2.4, using Definitions 2.5 and 2.6:
Definition 2.4 (Strong low bisimulation, modulo modes).

   strong-low-bisim-mm B ≜ cg-consistent B ∧ sym B ∧
         (∀lc1 lc2 . (lc1 , lc2 ) ∈ B ∧ lc1 =mds lc2 −→
              lc1 =Low
                   mds lc2 ∧
              (∀lc′1 . lc1 ⇝ lc′1 −→ (∃lc′2 . lc2 ⇝ lc′2 ∧ lc′1 =mds lc′2 ∧ (lc′1 , lc′2 ) ∈ B)))

Definition 2.5 (Writability of variable x, according to mode state mds).

               writable mds x ≜ x ∈
                                  / mds AsmNoW ∧ x ∈
                                                   / mds AsmNoRW

Definition 2.6 (Closedness under globally consistent changes).

     cg-consistent B ≜ ∀tps1 mem1 tps2 mem2 mds.
          (⟨tps1 , mds, mem1 ⟩, ⟨tps2 , mds, mem2 ⟩) ∈ B −→
          (∀mem′1 mem′2 . (∀x. (mem1 x ̸= mem′1 x ∨ mem2 x ̸= mem′2 x ∨
           L mem1 x ̸= L mem′1 x) −→ writable mds x) ∧ mem′1 =Low    ′
                                                              mds mem2 −→
          (⟨tps1 , mds, mem′1 ⟩, ⟨tps2 , mds, mem′2 ⟩) ∈ B)

                                                 9
Note that, to prevent unnecessary proof effort, strong-low-bisim-mm assumes instead of
asserting the initial modes-equality (lc1 =mds lc2 ), as the security property that will use
strong-low-bisim-mm will take responsibility for asserting it (to follow, in Definition 2.7).
   We now present definitions of the CVDNI security properties that differ from those pub-
lished in Murray et al. (2016b) and our conference paper Sison & Murray (2019), in that
they allow two additional forms of customisation as parameters to the theory, necessary for
a fuller written presentation of the formal verification of our compiler:

   1. Initialisation requirements for the system, in the form of a predicate over shared mem-
      ory called INIT.
      The per-thread and whole-system security properties are relaxed such that they only
      quantify over initial shared memories that obey this predicate.

   2. Extra requirements to be imposed on top of strong low-bisimulation modulo modes,
      in the form of a predicate over bisimulation relations called EXTRA.
      The per-thread security property is strengthened to impose these additional require-
      ments on any candidate security witness.

When dropped from each of the names of the properties “com-secure” and “sys-secure”
soon to be introduced, INIT and EXTRA default to (λ . True); in that case, the definitions
of those properties will then simplify to their original versions as presented in Murray et al.
(2016b); Sison & Murray (2019).
   The per-thread security property is then as follows:

Definition 2.7 (Per-thread compositional security, with INIT, EXTRA requirements).

                 com-secureEXTRA
                           INIT  (tps, mds) ≜ ∀mem1 mem2 .
                      mem1 =Low
                            mds mem2 ∧ INIT mem1 ∧ INIT mem2 −→
                           (∃B. strong-low-bisim-mm B ∧ EXTRA B ∧
                                (⟨tps, mds, mem1 ⟩, ⟨tps, mds, mem2 ⟩) ∈ B)

   We have proved in Isabelle/HOL that the compositionality theorem of Murray et al.
(2016b) holds regardless of the INIT, EXTRA chosen—in short, the INIT condition relaxes
the goal sufficiently to relax each of its assumptions the same way, and the EXTRA require-
ment only strengthens its assumptions. Subject to some “sound mode use” side conditions
(to be discussed soon), it gives us that the parallel composition cms :: (ThreadPrivate ×
(Mode ⇒ Var set)) list of com-secure program threads will itself be a concurrent program
that enforces “sys-secure”, a system-wide value-dependent noninterference property. Here,
the set operator returns the set of all the elements in a given list:

Theorem 2.8 (Compositionality of com-secureEXTRA
                                           INIT ).

                    ∀(tps, mds) ∈ set cms. com-secureEXTRA
                                                     INIT  (tps, mds)
                   ∀mem. INIT mem −→ sound-mode-use (cms, mem)
                                     sys-secureINIT cms



                                              10
   We first introduce the elements of this whole-system property “sys-secure”, before defin-
ing it formally (to follow, in Definition 2.9).
   From all low-equivalent pairs of initial memories that both satisfy the INIT conditions,
this whole-system property “sys-secure” asserts a form of low-equality between all global
configuration pairs that are reachable via evaluation 99Ksched to the same fixed schedule
sched, for all such finite lists sched giving an order of steps of execution from each thread:

                    gc 99K[] gc′ ≜ (gc = gc′ )
                    gc 99Kn.ns gc′ ≜ (∃gc′′ . gc ⇝n gc′′ ∧ gc′′ 99Kns gc′ )

Here [] is an empty list, . is the cons operator, and ⇝n means the nth thread in the global
configuration takes one step.
    In always comparing pairs of runs executing against the same schedule, the property
models the class of schedulers whose decisions never depend on any secrets. Consequently,
this excludes schedulers that are specialised, in the manner of Barthe et al. (2007a), to
actively monitor the sensitivity level of each thread’s control flow, so as to intervene and
avoid interleaving it with others when it has become dependent on secrets. Instead, the
CVDNI theory puts the onus on the developer of the program to prove that any branching
on secret conditionals does not lead to timing-sensitive flows of the secret as discernible via
low-classified sinks accessible to other threads in the system. Note that, as CVDNI prohibits
mode state from ever becoming secret dependent, it will implicitly prohibit any leaks into
parts of memory with which the mode state is directly associated—in Section 3, we will
need to prohibit leaks into the memory we use to implement mutex locks, for this reason.
    The special form of low-equality applied by the whole-system property is one that is mod-
ified from Definition 2.1, so that it only requires each Low-classified non-control variable
x∈ / C to be of equal value in both global configurations if the mode states of all threads con-
sider x to be readable (Definition 2.2). Furthermore, the property ensures that paired global
configurations continue to agree on the number of threads in the system, and on the mode
states for all threads, written cms′1 =all-mds cms′2 ≜ (map mds cms′1 = map mds cms′2 ),
where the syntax “map mds cms” denotes the mapped projection that extracts a list of mode
states from a list cms of ThreadPrivate × (Mode ⇒ Var set) pairs. Finally, we will use
syntax cms[i] to denote the ith element in list cms.
    This whole-system noninterference property, written formally, is then as follows:

Definition 2.9 (Whole-system value-dependent security, with INIT requirements).

  sys-secureINIT cms ≜ ∀mem1 mem2 .
  INIT mem1 ∧ INIT mem2 ∧ mem1 =Low mem2 −→
        (∀sched cms′1 mem′1 . (cms, mem1 ) 99Ksched (cms′1 , mem′1 ) −→
             (∃cms′2 mem′2 . (cms, mem2 ) 99Ksched (cms′2 , mem′2 )) ∧
             (∀cms′2 mem′2 . (cms, mem2 ) 99Ksched (cms′2 , mem′2 ) −→
                  length cms′1 = length cms′2 ∧ cms′1 =all-mds cms′2 ∧
                  (∀x. x ∈ C ∨ L mem′1 x = Low ∧
                       (∀i < length cms′1 . readable cms′1 [i] x) −→ mem′1 x = mem′2 x)))


                                              11
  Finally, we must note that the use of assume–guarantee reasoning to obtain the com-
positionality of the per-thread property in the style of Mantel et al. (2011) gives rise to
requirements justifying the soundness of that reasoning; requirements that we will prove
our compiler to preserve. For CVDNI, these are summed up by the “sound-mode-use” side
condition of Theorem 2.8, which consists of a “local” and a “global” part:
Definition 2.10 (Sound mode use side-condition).
                sound-mode-use (cms, mem) ≜
                     (∀cm ∈ set cms. local-mode-compliance (cm, mem)) ∧
                     global-modes-compatibility (cms, mem)
   First, all threads must each obey a local mode compliance requirement. This says that for
all reachable local configurations of the program, at no point will the thread violate any of its
own guarantees not to access a particular location in the shared state, which implies also not
accessing any of its control variables. We leave precise definitions for “reachable-lcs” and
“doesnt-read-(or-modify)” to this paper’s Isabelle/HOL supplement material,2 but mention
here that it is the doesnt-read-(or-modify) assertions that enforce that any guarantees not to
access some variable x will effectively apply also to all of x’s control variables:
Definition 2.11 (Local mode compliance).
  local-mode-compliance lc ≜
  ∀c mds mem. ⟨c, mds, mem⟩ ∈ reachable-lcs lc −→ respects-own-guarantees (c, mds)
  where
        respects-own-guarantees (c, mds) ≜
             (∀x. (x ∈ mds GuarNoRW −→ doesnt-read-or-modify c x) ∧
                  (x ∈ mds GuarNoW −→ doesnt-modify c x))
   Then, all threads must together obey a global modes compatibility requirement. This
requirement says that the threads’ mode states in all reachable global configurations of the
concurrent program (the “reachable-mds-lists”) are compatible—that is, if any one thread
assumes a particular location will not be accessed for writing or reading, then all other
threads must be guaranteeing not to access that location for the same purpose:
Definition 2.12 (Global modes compatibility).
global-modes-compatibility gc ≜ ∀mdss ∈ reachable-mds-lists gc. compatible-modes mdss
where
     reachable-mds-lists gc ≜
          {mdss | ∃cms′ mem′ sched. gc 99Ksched (cms′ , mem′ ) ∧ map mds cms′ = mdss}
     compatible-modes mdss ≜ ∀i x. i < length mdss −→
          (x ∈ mdss[i] AsmNoRW −→
               (∀ j < length mdss. j ̸= i −→ x ∈ mdss[ j] GuarNoRW)) ∧
          (x ∈ mdss[i] AsmNoW −→
               (∀ j < length mdss. j ̸= i −→ x ∈ mdss[ j] GuarNoW))
  2 The Isabelle/HOL theories are available at http://covern.org/jfpsc.html.



                                               12
if h ̸= 0 then
                                     reg3 := h;                       ...
       x := y
                                     if reg3 ̸= 0 then                else
else                                       skip;                             reg1 := y;
       x := y + z                          skip;                             reg2 := z;
fi                                         reg0 := y;                        reg0 := reg1 + reg2;
(a) Abstract if-conditional.               x := reg0                         x := reg0
Relation R pairs configurations of   ...                              fi
this program with configurations
                                     (b) Concrete if-conditional. Relation I pairs configurations
of the program in Figure 2b that
                                     of this program as shown by the dashed lines.
are of the same-shaded region.

Figure 2: Excerpts from a CVDNI-preserving refinement example with secret-dependent
control flow: h contains a secret, y and z contain zero, and x is an untrusted sink. Reproduced
from Sison & Murray (2019)—the example is originally from Murray et al. (2016b).


   Note that this global modes compatibility requirement is not compositional; consequently,
instead of obliging the program developer to prove it for the source programs to be fed to
our compiler, we will prove it as an invariant maintained by the execution semantics of our
source language—particularly, by its synchronisation primitives (see Section 3).
   For more details and precise presentations of all the definitions we have adapted from
Murray et al. (2016b,c) to enable the compiler verification work described in this paper,
please refer to the Isabelle/HOL formalisation in our supplement material.

2.3      Cube-shaped refinement for preserving noninterference
Proof of CVDNI-preserving refinement (also security-preserving or secure refinement), for
a single-threaded program that will be run as a thread of a concurrent program, requires the
user of the theory to nominate two binary relations (both illustrated by Figure 2):

     1. A refinement relation R relating local configurations of the abstract program to local
        configurations of the concrete program: Abstract must simulate concrete, in a sense
        typical of much other work on program refinement, including compiler verification.

     2. A concrete coupling invariant I that allows us to use B and R to build a new strong
        low-bisimulation (modulo modes) for the concrete program, by discarding pairs of lo-
        cal configurations after the refinement that should not be reached in the same number
        of evaluation steps. It thereby witnesses that any changes a refinement (or compiler)
        might make to the execution time do not introduce any timing channels.

   The essence of the proof technique is to require that a number of conditions—analogous
to those for strong-low-bisim-mm (Definition 2.4)—be imposed on the nominated R and
I , in relation to a given witness relation B establishing com-secure (Definition 2.7) for the
abstract program. The definitions to follow are adapted from Murray et al. (2016b) Section
V, as we presented in Sison & Murray (2019)—for better readability, a simplified version
in which no new shared variables are added by the refinement. Consequently, we use the
notation =mem
            mds to denote that two local configurations have equal mode state and memory,
regardless of whether relating configurations of the same or differing languages.


                                                   13
coupling-inv-pres B R I ≜
                                                                           2 a                 a′2
∀a1 c1 . (a1 , c1 ) ∈ R −→                                      abstract             n
                                                                         B                B
  (∀c′1 . c1 ⇝C c′1 −→                                        execution a1               a′1
                                                                                 n
     (∃n a′1 . a1 ⇝nA a′1 ∧ (a′1 , c′1 ) ∈ R ∧
                                                                             R                 R
       (∀a2 c2 a′2 . (a1 , a2 ) ∈ B ∧ a1 =mds a2 ∧
          (a2 , c2 ) ∈ R ∧ (c1 , c2 ) ∈ I ∧ c1 =mds c2 ∧                 R               R
          a2 ⇝nA a′2 ∧ a′1 =mds a′2 −→                                     c2                  c′2
                                                                concrete             1
            (∃c′2 . c2 ⇝C c′2 ∧ c′1 =mds c′2 ∧                           I                I
                                                              execution c1               c′1
              (a′2 , c′2 ) ∈ R ∧ (c′1 , c′2 ) ∈ I ))))                           1

Figure 3: Definition and graphical depiction of refinement preservation obligation for
secure-refinement (Definition 2.15). Reproduced from Sison & Murray (2019)—the def-
inition is a simplified restatement of its original formalisation in Murray et al. (2016b).

   Regarding the maintenance of modes equivalence and observational equivalence across
the relation, the restrictions on refinement are tighter than those that were applied to
strong-low-bisim-mm, in that R is required to preserve the shared memory in its entirety:
Definition 2.13 (Preservation of modes and memory).
            preserves-modes-mem R ≜ ∀lcA lcC . (lcA , lcC ) ∈ R −→ lcA =mem
                                                                        mds lcC

   Regarding the closedness under changes by other threads that ensures composition-
ality for concurrency, on I we again impose cg-consistent (Definition 2.6) from Sec-
tion 2.2. However, in the case of R, we instead impose “closed-others”, a simplification
of cg-consistent that considers only environmental actions that affect the memories on both
sides of the relation identically. Furthermore, closed-others ensures equality of all shared
variables, not just those judged observable. Defined formally:
Definition 2.14 (Closedness of refinements under changes by others).
     closed-others R ≜ ∀tpsA tpsC mds mem mem′ .
            (⟨tpsA , mds, mem⟩A , ⟨tpsC , mds, mem⟩C ) ∈ R) ∧
            (∀x. (mem x ̸= mem′ x ∨ L mem x ̸= L mem′ x) −→ writable mds x) −→
            (⟨tpsA , mds, mem′ ⟩A , ⟨tpsC , mds, mem′ ⟩C ) ∈ R)
   The final major—and hardest—requirement for confidentiality preservation is to prove
R and I closed simultaneously under the pairwise executions of the concrete and abstract
programs, using a cube-shaped “refinement and coupling invariant preservation” diagram
(coupling-inv-pres, depicted in Figure 3), whose edges are configuration pairs in B, R, and
I . (Reducing its difficulty is the focus of the decomposition principle in Section 2.4.)
   All that then remains is for the nominated concrete coupling invariant I to be symmetric
(sym I ), and the predicate secure-refinement puts together all the requirements:
Definition 2.15 (Requirements for confidentiality-preserving secure refinement).
 secure-refinement B R I ≜ preserves-modes-mem R ∧ closed-others R ∧
                                            cg-consistent I ∧ sym I ∧ coupling-inv-pres B R I

                                                         14
   The soundness theorem for confidentiality-preserving refinement by Murray et al.
(2016b) then gives us that, under these conditions, the concrete relation “B C of B R I ”,
derived from a witness strong-low-bisim-mm relation B, refinement relation R, and cou-
pling invariant I , is itself a witness strong-low-bisim-mm for the concrete program. For
readability, from here onwards we will use a1 , c1 , . . . instead of lc1A , lc1C , . . . for local con-
figuration variables when comparing abstract and concrete executions simultaneously:

Definition 2.16 (Concrete bisimulation relation derived from B, R and I ).

          B C of B R I ≜ {(c1 , c2 ) | ∃a1 a2 . (a1 , c1 ) ∈ R ∧ (a2 , c2 ) ∈ R ∧
                                           (a1 , a2 ) ∈ B ∧ c1 =Low
                                                                mds c2 ∧ (c1 , c2 ) ∈ I }

Theorem 2.17 (Preservation of strong-low-bisim-mm by secure-refinement).

                   strong-low-bisim-mm B               secure-refinement B R I
                             strong-low-bisim-mm (B C of B R I )

2.4     Decomposition principle and its impact on refinement proofs
We now present, as we first did in Sison & Murray (2019), an alternative way to prove
secure-refinement (Definition 2.15) that obviates the need to use the cube-shaped, two-sided
refinement obligation (depicted by Figure 3), by decomposing its concerns into:

   1. Proving R closed using a square-shaped simulation diagram (depicted by Figure 4a)
      akin to the backward simulations commonly used to prove semantics-preserving re-
      finement by compilers (e.g. for CompCert (Leroy, 2009)), and

   2. Security-focused proof obligations (depicted by Figures 4b, 4c), separable from the
      square-shaped simulation, that prevent the introduction of timing leaks, termination
      leaks, and secret-dependent differences in assume–guarantee mode state.

   The decomposition requires the verifier to nominate a new parameter, called abs-steps or
the pacing function. Its role is to dictate the pace of the square-shaped simulation by speci-
fying the number of abstract steps that ought to be taken for one concrete step, as depicted
by Figure 4a. Deferring the security-focused side conditions (“decomp-refinement-safe”)
to afterwards, the decomposition principle is then defined formally as follows:

Definition 2.18 (Decomposition principle for secure-refinement).

      secure-refinement-decomp B R I abs-steps ≜
          preserves-modes-mem R ∧ closed-others R ∧ cg-consistent I ∧ sym I ∧
          decomp-refinement-safe B R I abs-steps ∧ (∀a c. (a, c) ∈ R −→
                                                (abs-steps a c)
               (∀c′ . c ⇝C c′ −→ (∃a′ . a ⇝A                      a′ ∧ (a′ , c′ ) ∈ R)))

  The aforementioned side conditions on all refinement parameters, depicted by Figures
4b, 4c, are then defined formally under the predicate decomp-refinement-safe as follows:



                                                  15
                                                                            a2
                                          a2     abs-steps a2 c2
                                      B               =                 B
 a                      a′                                             a1
       abs-steps a c                 a1        abs-steps a1 c1

                                          R                                 R
R                       R                                              R
                                     R
                                          c2
                                                                            c2                     c′2
                                                  stops c2                            1
                                      I            =                    I                    I
 c                      c′                                             c1                    c′1
            1                        c1        stops c1                           1

(a) Refinement preservation         (b) Consistency of pacing and     (c) Closedness of the cou-
for relation R under program        stopping behaviour, to prevent    pling invariant relation I un-
execution paced by abs-steps.       timing and termination leaks.     der lockstep program execu-
(Part of Definition 2.18.)          (Part of Definition 2.19.)        tion. (Part of Definition 2.19.)

Figure 4: Graphical depictions of decomposed refinement preservation obligations.
Reproduced from Sison & Murray (2019).


Definition 2.19 (Security-focused side conditions for decomposition principle).

        decomp-refinement-safe B R I abs-steps ≜ ∀a1 a2 c1 c2 . (a1 , a2 ) ∈ B ∧
        a1 =mds a2 ∧ (a1 , c1 ) ∈ R ∧ (a2 , c2 ) ∈ R ∧ (c1 , c2 ) ∈ I ∧ c1 =mds c2
         −→ stops c1 = stops c2 ∧ abs-steps a1 c1 = abs-steps a2 c2 ∧
                (∀c′1 c′2 . c1 ⇝C c′1 ∧ c2 ⇝C c′2 −→ (c′1 , c′2 ) ∈ I ∧ c′1 =mds c′2 )

The intuitive meanings of the side conditions in Definition 2.19 are:
     • stops c1 = stops c2 ensures that the refinement has not introduced any termination
       leaks, by asserting consistent stopping behaviour for I -related concrete program
       configurations, which we know to be observationally indistinguishable.
     • abs-steps a1 c1 = abs-steps a2 c2 ensures that the refinement has not introduced any
       timing leaks, by asserting consistency of the pace of the refinement for R-related pro-
       gram configurations, which we again know to be observationally indistinguishable.
     • The final ∀-quantified clause asserts I ’s suitability as a coupling invariant, in that it
       must remain closed under lockstep evaluation of the concrete program configurations
       it relates. Furthermore it must maintain mode state equality with each lockstep evalu-
       ation, which ensures that the refinement has not introduced any inconsistencies in the
       memory access assumptions and guarantees needed for the concurrent composition-
       ality of the property.
Note that the B- and R-edges in Figure 4c may capture useful facts about a particular pro-
gram verification technique and compiler (respectively), so their availability as assumptions
is intended to reduce greatly the effort needed to specify a coupling invariant I and prove
it satisfies the condition.
    Assuming the fulfilment of all the decomposed requirements, we obtain that they are a
sound method for establishing secure refinement of the per-thread confidentiality property,
as desired:

                                                     16
Theorem 2.20 (Soundness of the decomposition principle).

     secure-refinement-decomp B R I abs-steps =⇒ secure-refinement B R I

Proof. The only obligation for secure-refinement (Definition 2.15) not obtained
immediately from secure-refinement-decomp (Definition 2.18) is the cube-shaped
coupling-inv-pres (Figure 3). We discharge this as follows:
   The front face of the cube is just ordinary square-shaped refinement preservation (de-
picted in Figure 4a), given to us by secure-refinement-decomp: that a single concrete step
from c1 is simulated by n abstract steps from a1 , where n is given by abs-steps.
   We are then obliged to prove a simulation in the other direction (the back face of the
cube), that n abstract steps from all configurations a2 related by B to a1 are simulated by
some concrete step from c2 related by R to a2 and by I to c1 .
   Here, we lean on the determinism of the abstract program’s evaluation semantics (re-
quired by the theory) to flip the direction of simulation, knowing that n abstract steps from
a2 , simulating a single concrete step from c2 , could only be the very same n abstract steps
from a2 that we were required to consider. This allows us to obtain that simulation by
using, once again, the square-shaped refinement preservation (Figure 4a) given to us by
secure-refinement-decomp.
   Consistency of refinement pacing and stopping behaviour (depicted in Figure 4b) given
by decomp-refinement-safe (Definition 2.19) then respectively ensure that n (via abs-steps)
is the correct number of abstract steps to consider, and that there will indeed be a concrete
step from c2 to drive the matching simulation step.
   Finally, the remainder of decomp-refinement-safe (depicted in Figure 4c) discharges the
requirement of closedness and modes-equality maintenance of I under lockstep execution,
demanded by the bottom face of the cube.

   To demonstrate how the decomposition principle reduces proof complexity and effort,
we returned to the example program refinement discussed in Section V-E of Murray et al.
(2016b) and proved in its Isabelle formalisation (Murray et al., 2016a), an excerpt of which
is shown in Figure 2. The abstract program (9 imperative commands) branches on a sensitive
value, and executes a single atomic expression assignment in each branch. Its refinement (to
16 commands) models expansion of the expressions into multiple steps, resolving a timing
disparity between the two branches by padding with skip.
   We use proof size as a proxy for proof effort, since the former is known to be strongly
linearly correlated with the latter (Staples et al., 2014). Formalised in Isabelle/HOL as
EgHighBranchRevC.thy (Murray et al., 2016a), the proof line count for that theory stood
at about 4.6K lines of definitions and proof, of which approx. 3.6K line were proofs. Adapt-
ing the proof instead to use the decomposition principle (secure-refinement-decomp, Defi-
nition 2.18), the proof line count drops from 3.6K to approx. 2K, a 44% reduction. Regard-
ing definition changes, the new proof makes less than 10 lines of adaptations to a coupling
invariant and pacing function used by the old proof, and adds about 30 lines worth of new
helper definitions, for use with the decomposition principle. The rest of the theory and its
external dependencies remain in common between the two versions.
   As would be expected, the bulk of the deletions are from the full cube-shaped refinement
diagram proof (Figure 3) of secure-refinement (Definition 2.15) for the refinement relation.
The surviving parts of that proof just become the square-shaped refinement diagram proof

                                             17
(Figure 4a) of the decomposition principle (Definition 2.18), without much modification.
The deletions are replaced by newly added proofs of the decomposition principle’s more
security-focused side conditions (Definition 2.19, depicted by Figures 4b, 4c).

2.5   Compositional whole-system secure refinement
We now present the whole-system refinement theorem from Murray et al. (2016b,a), which
we adapt here to support the specification of INIT requirements (as in com-secureEXTRA    INIT ,
Definition 2.7), and simplify to the case of refinements that add no shared variables.
   The main usefulness of this theorem is that, beyond demanding secure-refinement (Def-
inition 2.15), which dealt with the preservation of per-thread security as witnessed by a
strong-low-bisim-mm (Definition 2.4), it deals additionally with the preservation of the
sound-mode-use side conditions (Definition 2.10) that will be demanded by the compo-
sitionality theorem for CVDNI (Theorem 2.8) at the target language level.
   Notably, although it imposes the requirement for the refinement to preserve the “local”
part of sound-mode-use (Definition 2.11), it automatically preserves the non-compositional
“global” part of this side condition (Definition 2.12) as a consequence of the requirements
imposed by the per-thread secure refinements. Thus, our source-level proof of the global
condition (see Section 3) will be sufficient, and there will be no need for us to prove anything
extra about our compiler for it to preserve that to the target-language level.
   We now present the requirements and theorem for whole-system refinement formally.
   First, in addition to the per-thread refinement notion secure-refinement (Definition 2.15)
that we addressed in Sections 2.3 and 2.4, our whole-system refinement theorem will require
that the refinement relation R established by the compiler additionally preserves the compo-
sitional local mode compliance property for each thread. Here, “respects-own-guarantees”
is from Definition 2.11:

Definition 2.21 (Refinement R preserves local mode compliance).

          preserves-local-compliance R ≜ ∀tpsA mdsA memA tpsC mdsC memC .
                respects-own-guarantees (tpsA , mdsA ) ∧
                (⟨tpsA , mdsA , memA ⟩A , ⟨tpsC , mdsC , memC ⟩C ) ∈ R −→
                     respects-own-guarantees (tpsC , mdsC ))

   We define a new “compositional refinement” predicate to capture all per-thread require-
ments that will be demanded by our compositional whole-system refinement theorem. This
bundles together preserves-local-compliance and secure-refinement so as to preserve the
strong-low-bisim-mm relations (Definition 2.4) that witness noninterference for each thread
of the abstract program. Alongside all these requirements just described, it also requires the
concrete coupling invariant I to cover all possible initial memory pairs that are low-equal
modulo modes (Definition 2.3) and satisfy the INIT C conditions that will parameterise the
target language-level CVDNI property:




                                              18
Definition 2.22 (Requirements for compositional whole-system refinement).

  compositional-refinement B R I ≜
        secure-refinement B R I ∧ strong-low-bisim-mm B ∧
        preserves-local-compliance R ∧
        (∀tpsC mds mem1 mem2 . mem1 =Low
                                     mds mem2 ∧ INIT C mem1 ∧ INIT C mem2 −→
             (⟨tpsC , mds, mem1 ⟩C , ⟨tpsC , mds, mem2 ⟩C ) ∈ I )

   With these requirements, we prove using Isabelle/HOL that a whole-system refinement
theorem, proved originally by Murray et al. (2016b,a), can be adapted to support the spec-
ification of INIT requirements on initial memory at both abstract- and concrete-level. (As
with Theorem 2.8, the relaxation of the goal by INIT C is enough to permit the relaxations
of its assumptions by INIT C , INIT A .) First we will state the theorem, then we will explain it,
line-by-line. This theorem proves that abstract-level sound-mode-use (including its global
part) by a system of secure mixed-sensitivity concurrent program threads (i.e. list cmsA ,
as witnessed by bisimulations Bs for each thread) is sufficient for a set of per-thread se-
cure refinements (in terms of the lists Bs, Rs, I s of bisimulation, refinement, and concrete
coupling invariant relations for each thread, respectively) to yield a concrete-level secure
concurrent program (i.e. list cmsC that satisfies sys-secure, Definition 2.9):
Theorem 2.23 (Whole-system compositionality of per-thread secure refinement).

      (∀mem. INIT C mem −→ INIT A mem) ∧
      (∀mem. INIT A mem −→ sound-mode-use (cmsA , mem)) ∧
      length cmsA = length Bs = length Rs = length I s = length cmsC ∧
      (∀i < length cmsC .
           compositional-refinement Bs[i] Rs[i] I s[i] ∧
           (∀mem. INIT C mem −→ ((cmsA [i], mem), (cmsC [i], mem)) ∈ Rs[i]) ∧
           (∀mem1 mem2 . INIT A mem1 ∧ INIT A mem2 ∧ mem1 =Low
                                                           (snd cmsC [i]) mem2 −→
                 ((cmsA [i], mem1 ), (cmsA [i], mem2 )) ∈ Bs[i]))

                                     sys-secureINITC cmsC

  The premises of this theorem can be understood as follows:
    • (∀mem. INIT C mem −→ INIT A mem):
      The concrete-level “INIT C ” initial condition must be no weaker than the abstract-level
      “INIT A ” one.

    • (∀mem. INIT A mem −→ sound-mode-use (cmsA , mem)):
      For the abstract program, sound-mode-use (Definition 2.10) must hold for all possible
      initial memories.

    • The lists of initial thread-private and mode states at abstract and concrete level
      (resp. cmsA , cmsC ), and lists of bisimulation, refinement, and concrete coupling in-
      variant relations (resp. Bs, Rs, I s) must all be for the same number of threads.

                                               19
    • Then, for all threads i in the system:

         – The relations B, R, I for thread i must meet the requirements for “composi-
           tional whole-system refinement” (Definition 2.22).
         – The refinement relation R for thread i must hold initially, i.e. cover its initial
           thread-private and mode states at concrete and abstract level (resp. cmsC , cmsA ),
           for all initial memories that satisfy the concrete INIT C requirement.
         – The abstract bisimulation relation B for thread i must hold initially, i.e. must
           relate its initial thread-private and mode state to itself, for all pairs of memories
           that are low-equal modulo that mode state, and that both satisfy the abstract
           INIT A requirement.

   Given all these assumptions, Theorem 2.23 yields a whole-system noninterference prop-
erty sys-secureINITC for the resulting concurrent program (with the list of initial thread-
private and mode states cmsC ) that assumes that the initial memory satisfies INIT C .


3    Source language: While with mutex locks
In this section, we give a focused presentation of our compiler’s source language, centered
on its properties that enable the composition of per-thread proofs of CVDNI-preserving
refinement to the compiler’s target RISC language. Our Isabelle/HOL supplement provides
full formalisations of its semantics, and of instances of all per-thread proof techniques for
proving CVDNI itself (developed for While by Sison (2020); Murray et al. (2016b,c)).
   While with mutex locks (hereafter While) is a generic imperative language with support
for conditional looping, consisting of the commands cmd over arithmetic expressions exp:

                   exp ::= n | v | exp ⊕ exp
                  cmd ::= skip | cmd ; cmd | if exp then cmd else cmd fi |
                           while exp do cmd od | v := exp | stop |
                           lock(k) | unlock(k)

   The language is parameterised over shared program-variable identifiers v :: Var, shared
lock-variable identifiers k :: Lock, constant values n :: Val, and binary arithmetic operators
⊕ :: Val ⇒ Val ⇒ Val that each have a big-step evaluation semantics; these induce a big-
step evaluation semantics for exp as a whole. The commands cmd then have a small-step
operational semantics, wherein skip and variable assignment v := exp execute in one step to
stop (which itself does not step to anything); conditional branch if steps to the appropriate
cmd depending on whether its expression evaluates to zero; and conditional loop while steps
to an if-conditional between either (1) the loop body sequenced with a repetition of the
while command, or (2) stop. Finally the sequential command c1 ; c2 executes to c2 when c1
executes to stop, and to c′1 ;c2 (c′1 being c1 ’s destination) otherwise. Of these aforementioned
commands, only variable assignments can modify the shared memory (program-variables
only), and none can directly modify the mode state or lock-variables.
   We will give special focus to the addition to the While language of the mutex synchro-
nisation primitives lock(k) and unlock(k), which are the sole means of modifying lock
variables and mode state. These replace both the ad-hoc mode annotations and the await(v)

                                               20
synchronisation primitive that were previously offered for While by Murray et al. (2016b).
After briefly noting here how While instantiates the underlying theory from Section 2, we
will present these new primitives’ operational semantics, which depends on the program
developer supplying details of the locking discipline as a parameter (Section 3.1) subject to
some restrictions (Section 3.2). We will then prove that global-modes-compatibility (Defi-
nition 2.12) is invariant for systems of While programs running concurrently (Section 3.3),
subject to some initial conditions (Section 3.4). Discharging this once-off noncomposi-
tional proof obligation is crucial in enabling both composition of per-thread noninterference
properties (using Theorem 2.8), and compositional whole-system secure refinement of non-
interference down to RISC by our compiler (using Theorem 2.23).
   While instantiates the concurrent value-dependent noninterference theory described in
Section 2.2. This instantiation assumes that the underlying concurrent execution model
(e.g. operating system, scheduler) for the While language prevents threads from seeing
each others’ current program location. Thus the While program command c :: cmd being
executed (understood as the current program location) is modelled as the thread-private
state of the local configuration triple: ⟨c, mds, mem⟩w . (The subscript w distinguishes While
program triples from RISC ones, which are subscripted r .)
   To ease formalisation of lock(k) and unlock(k), we instantiate the shared mem :: Mem
type as a total mapping from a sum type to values Val. This sum type, with constructors
Lock, Var, distinguishes lock-variable identifiers k :: Lock (which can only be read or written
by the lock primitives) from program-variable identifiers v :: Var (which can be read or
written by the rest of the commands). In Isabelle/HOL’s datatype notation, this is:

                           Mem ≜ (Lock Lock | Var Var) ⇒ Val

For readability, we will elide this distinction between Lock and Var—or applications of their
constructors Lock and Var—from the presentation whenever clear from the context.

3.1   Locking discipline and its semantics
The program developer provides the details of the program’s locking discipline in the form
of a lock interpretation parameter lock-interp :: Lock ⇒ (Var set × Var set), which gives
for each lock the two non-overlapping sets of program-variables over which acquiring
the lock grants exclusive permission to write, (resp.) read and write. For readability, this
presentation will elide lock-interp from the arguments of definitions, and use the notation
varsNoW, varsNoRW :: Lock ⇒ Var set to refer to its fst and snd projection.
   Alongside encoding the mutex primitives’ usual effect on control flow—most crucially,
lock(k) should refuse to proceed meaningfully if the lock k is already held—we will now
specify for them an evaluation semantics that furthermore encodes the permissions implied
by the locking discipline, as assumptions and guarantees expressed in the mode state. This
semantics assumes that, initially, no locks are held, and all threads are making guarantees
not to access the variables they govern (conditions we will define formally in Section 3.4).
   The following two helpers specify how acquiring (resp. releasing) a lock affects the mode
state under a given lock interpretation lock-interp. When a thread acquires a lock it gains
more assumptions, and makes fewer guarantees about the region of memory concerned:



                                              21
Definition 3.1 (Impact on mode state mds of acquiring lock k).

         mds ⊕ k ≜ λ m. case m of GuarNoW ⇒ mds GuarNoW − varsNoW k
                                           | AsmNoW ⇒ mds AsmNoW ∪ varsNoW k
                                           | GuarNoRW ⇒ mds GuarNoRW − varsNoRW k
                                           | AsmNoRW ⇒ mds AsmNoRW ∪ varsNoRW k

  The converse occurs when releasing a lock: the thread drops the assumptions it was
making about that region of memory, and once again makes guarantees not to access it.
Definition 3.2 (Impact on mode state mds of releasing lock k).

        mds ⊖ k ≜ λ m. case m of GuarNoW ⇒ mds GuarNoW ∪ varsNoW k
                                           | AsmNoW ⇒ mds AsmNoW − varsNoW k
                                           | GuarNoRW ⇒ mds GuarNoRW ∪ varsNoRW k
                                           | AsmNoRW ⇒ mds AsmNoRW − varsNoRW k

   The operational semantics for lock(k) is then given by two rules: L OCK ACQ when lock
k is available, and L OCK S PIN when it is already held. For these, we use predicate evLock ::
Val ⇒ bool with designated constants TrueLock , FalseLock :: Val to indicate that the lock is,
resp. is not held—i.e. evLock (TrueLock ) = True, and evLock (FalseLock ) = False.3
   Apart from impacting the mode state as already specified (by Definition 3.1), attempting
to acquire an available lock will succeed in the usual manner, setting the lock-variable to the
designated constant (TrueLock ) to prevent subsequent lock acquisition attempts:

           ¬evLock (mem (Lock k))              mem′ = mem[Lock k 7→ TrueLock ]
                                             mds′ = mds ⊕ k
                                                                                              L OCK ACQ
                     ⟨lock(k), mds, mem⟩w ⇝w ⟨stop, mds′ , mem′ ⟩w

   Attempting to acquire an already-held lock results in a stuttering evaluation step:

                                     evLock (mem (Lock k))
                                                                                     L OCK S PIN
                    ⟨lock(k), mds, mem⟩w ⇝w ⟨lock(k), mds, mem⟩w

   Then, the operational semantics for unlock(k) is given by two rules, of which only one,
L OCK R EL, will ever be used by programs that follow locking discipline. This rule requires
that the mode state mds is consistent with the present thread having previously acquired the
lock k: In short, it should have all the assumptions, but none of the guarantees, associated
with the variables governed by the lock. To specify this, we define the following helper:
Definition 3.3 (Mode state is consistent with holding a lock k).

        lock-held-mds-correct mds k ≜
            ∀x. (x ∈ varsNoW k −→ x ∈
                                    / mds GuarNoW ∧ x ∈ mds AsmNoW) ∧
                 (x ∈ varsNoRW k −→ x ∈
                                      / mds GuarNoRW ∧ x ∈ mds AsmNoRW)
   3 All three of ev
                     Lock , TrueLock , FalseLock are parameters that are set by the user of the theory, with the proviso
that their choice of parameters satisfy that evLock (TrueLock ) and ¬evLock (FalseLock ) hold as required.


                                                          22
  With that condition satisfied, the L OCK R EL rule specifies that an unlock(k) will proceed
successfully, to enact lock release on the memory and mode state as expected:

      lock-held-mds-correct mds k     mem′ = mem[Lock k 7→ FalseLock ]
                                 mds′ = mds ⊖ k
                                                                             L OCK R EL
               ⟨unlock(k), mds, mem⟩w ⇝w ⟨stop, mds′ , mem′ ⟩w

   To ensure that the While evaluation semantics is defined for all possible configurations,
the L OCK I NVALID rule defines a stuttering evaluation step for attempts to unlock(k) that
violate the locking discipline due to not having previously acquired the lock k:

                      ¬ lock-held-mds-correct mds k
                                                                    L OCK I NVALID
           ⟨unlock(k), mds, mem⟩w ⇝w ⟨unlock(k), mds, mem⟩w

   As mode state is nominally a form of ghost state, having the operational semantics appear
to depend on it in this manner is rather unusual. To remove the semantics’ reliance on ghost
state, the program developer must use a check for local-mode-compliance (Definition 2.11)
that only ever admits programs that satisfy the lock-held-mds-correct check whenever at-
tempting to unlock(k). For such programs, the operational semantics is equivalent to one
that (1) omits the lock-held-mds-correct check from the L OCK R EL rule, and (2) omits the
L OCK I NVALID rule from the While-language semantics entirely. An example of such a
check is included in our Isabelle/HOL supplement.

3.2   Restrictions on locking disciplines
Here we lay out some cleanliness conditions on locking disciplines, giving particular focus
to those relevant to our locking semantics (Section 3.1), and to our verification efforts for
While’s global compositionality property (Section 3.3) and our compiler (Section 5).
   Of these, only one is a hard consequence of the underlying CVDNI theory we presented
in Section 2: The per-thread CVDNI property com-secure (Definition 2.7) effectively com-
pels us to enforce that secrets are never allowed to leak into the locking state. Otherwise,
mode state would become tainted upon any attempt to acquire a lock whose status is secret,
which would violate com-secure’s requirement that modes-equality must be maintained at
all times (note the =mds enforced by strong-low-bisim-mm, Definition 2.4). To ensure that
com-secure will always treat the locking state as an untrusted sink, we impose the following
requirement on the L parameter supplied by the program developer:

Proposition 3.4 (L must permanently assign Low classification to all lock-variables k).

                             ∀k mem. L mem (Lock k) = Low

   The remaining restrictions are consequences of various simplifications of convenience.
   First, note that the type signature of the lock-interp parameter (given in Section 3.1) only
allows locks to govern program variables, not other locks. We justify this simplification with
the fact that if some lock k governed lock k′ , then k would already have to be held whenever
acquiring k′ —otherwise, the change to k′ would violate a no-write assumption implied by
the locking discipline. This, however, would make k′ entirely redundant with k.


                                              23
   Second, the lock acquisition and release semantics we gave in Section 3.1 is rather sim-
plified, in that releasing a lock will drop the assumptions of all its variables from the mode
state, even if another lock for that variable is still held! Thus, we signal that it only works
for disciplines wherein no more than one lock governs each program variable, by asserting:
Proposition 3.5 (No variable can be managed by more than one lock).
                  ∀v k. v ∈ varsNoW k ∪ varsNoRW k −→
                       (∀k′ . v ∈ varsNoW k′ ∪ varsNoRW k′ −→ k′ = k)
We believe that it would be feasible to relax Proposition 3.5, by generalising While’s lock-
ing semantics to allow disciplines wherein multiple locks must be held to access a given
variable. To satisfy CVDNI-preserving refinement (particularly Definition 2.13), a compiler
would need to preserve the lock memory operations that implement the more sophisticated
bookkeeping needed, as ours does for the current, much simpler locking semantics.
   Next, we assume that the program developer has not specified any “vacuous” locks
(i.e. ones that govern no variables), and that all locks grant at most one of AsmNoW or
AsmNoRW (i.e. not both) on any given variable. These two assumptions allow us to exclude
various pathological cases from our reasoning in Section 3.3 and Section 5, respectively:
Proposition 3.6 (Every lock governs access to some variable).
                            ∀k. varsNoW k ∪ varsNoRW k ̸= 0/
Proposition 3.7 (The lock interpretation sets for any given lock k do not overlap).
                            ∀k. varsNoW k ∩ varsNoRW k = 0/
   The final two restrictions simplify the possible interactions between locks and control
variables: We disallow locks from being control variables, and require variables to be gov-
erned by the same lock as their control variables. In particular, they will help us establish
(in Section 5.4) that the compiler produces programs that satisfy local-mode-compliance.
   First, recall we mentioned that, as part of local-mode-compliance (Definition 2.11), the
doesnt-read-(or-modify) assertions entail that any guarantees not to access some variable v
will effectively apply also to all of v’s control variables. Disallowing lock-variables from
being control variables thus ensures that lock(k) and unlock(k), because they only access
lock-variable k, cannot violate doesnt-read-(or-modify) for any program-variables:
Proposition 3.8 (Lock-variables k cannot be control variables).
                                                   /C
                                      ∀k. (Lock k) ∈
   Finally, requiring variables to be governed by the same lock as their control variables
effectively ensures they are always locked simultaneously. Apart from making it easier for
programs to satisfy local-mode-compliance, this also naturally prevents leaks caused by
other threads changing a variable’s classification to Low when it still contains High data:
Proposition 3.9 (Variables are always governed by the same lock as their control variables).


         ∀c v k. Var c ∈ C vars (Var v) −→ (c ∈ varsNoW k = v ∈ varsNoW k) ∧
                                             (c ∈ varsNoRW k = v ∈ varsNoRW k)

                                              24
3.3     Proof of global modes compatibility as an invariant
This section will present proof that global-modes-compatibility (Definition 2.12) holds as
an invariant for concurrent While programs (Section 3.3) when initialised to have no locks
held (Section 3.4). Consequently, it is sufficient for a developer to use a local compliance
check (Sison, 2020) to obtain the sound-mode-use condition (Definition 2.10) needed for
per-thread security proofs to be compositional via Theorem 2.8.
   Recall from Section 2.2 that this compatibility requirement formalises that for all reach-
able global configurations of a concurrent program, any assumptions made by any of the
threads must be met by corresponding guarantees made by all of the other threads:
Definition 2.12 (Global modes compatibility).

global-modes-compatibility gc ≜ ∀mdss ∈ reachable-mds-lists gc. compatible-modes mdss
where
      reachable-mds-lists gc ≜
           {mdss | ∃cms′ mem′ sched. gc 99Ksched (cms′ , mem′ ) ∧ map mds cms′ = mdss}
      compatible-modes mdss ≜ ∀i x. i < length mdss −→
           (x ∈ mdss[i] AsmNoRW −→
                (∀ j < length mdss. j ̸= i −→ x ∈ mdss[ j] GuarNoRW)) ∧
           (x ∈ mdss[i] AsmNoW −→
                (∀ j < length mdss. j ̸= i −→ x ∈ mdss[ j] GuarNoW))

   The approach to establish global-modes-compatibility here will be to define three mode
management requirements that taken together imply compatible-modes, and to prove them
invariant for concurrent While programs when initialised such that they hold to begin with.
   The first of these pertains to variables whose access is governed by some lock, according
to the locking discipline. To define it, we need, alongside lock-held-mds-correct (Defini-
tion 3.3) from Section 3.1, a predicate that specifies the correct mode state for not holding
a lock k: It should make all of the guarantees, and have none of the assumptions associated
with the variables governed by k.4 Stated formally:
Definition 3.10 (Mode state is consistent with not holding a lock k).

        lock-not-held-mds-correct mds k ≜
          ∀x. (x ∈ varsNoW k −→ x ∈ mds GuarNoW ∧ x ∈
                                                    / mds AsmNoW) ∧
              (x ∈ varsNoRW k −→ x ∈ mds GuarNoRW ∧ x ∈
                                                      / mds AsmNoRW)

Note that our simplifying exclusion of “vacuous” locks (Proposition 3.6) en-
sures we never have to deal with a case where lock-held-mds-correct mds k and
lock-not-held-mds-correct mds k hold simultaneously.
   The requirement on global configurations regarding these lock-managed variables is then
as follows: If and only if a given lock is held by anybody, then exactly one thread has a
mode state consistent with holding it; furthermore, all other threads will have a mode state
consistent with not holding it. Formally, with mdss gc ≜ map mds (cms gc):
  4 Note that this not merely the negation of lock-held-mds-correct mds k (Definition 3.3)!



                                                    25
Definition 3.11 (Lock-managed variable modes are compatible with memory).
                lock-managed-modes-mem-compatible gc ≜
                         ∀k. if (evLock ((mem gc) k)) then
                             ∃!i. i < length (cms gc) ∧
                                  lock-held-mds-correct (mdss gc)[i] k ∧
                                  (∀ j < length (cms gc). i ̸= j −→
                                       lock-not-held-mds-correct (mdss gc)[ j] k)
                             else ∀i < length (cms gc).
                                  lock-not-held-mds-correct (mdss gc)[i] k
   The second requirement pertains to variables whose access is entirely ungoverned by any
locks in the locking discipline. For these we specify a more direct check that if any thread
in the global configuration has an assumption about access to any of these variables, then
all other threads must be providing the corresponding guarantee to that assumption:
Definition 3.12 (Unmanaged variable modes are compatible).
  unmanaged-var-modes-compatible gc ≜ ∀i x. i < length (mdss gc) −→
                [
        (x ∈
           /             varsNoRW k −→
               k::Lock
               (x ∈ (mdss gc)[i] AsmNoRW −→
                     (∀ j < length (mdss gc). j ̸= i −→ x ∈ (mdss gc)[ j] GuarNoRW))) ∧
                [
        (x ∈
           /             varsNoW k −→
               k::Lock
               (x ∈ (mdss gc)[i] AsmNoW −→
                     (∀ j < length (mdss gc). j ̸= i −→ x ∈ (mdss gc)[ j] GuarNoW)))
   Also proved invariant is a third, minor property that enforces globally that no assumptions
or guarantees are ever recorded regarding access to lock-variables:
Definition 3.13 (No assumptions and guarantees on lock variables).
                  no-lock-mds mds ≜ ∀l m. Lock l ∈
                                                 / mds m
                no-lock-mds-gc gc ≜ ∀mds ∈ set (mdss gc). no-lock-mds mds
This follows trivially from (1) our simplification (discussed in Section 3.2) only to allow
locks to protect access to program variables and not other locks, and (2) the resulting fact
that no While primitives ever touch any mode state pertaining to lock variables. Thus,
further details on this third management requirement will be elided.
   We then have straightforwardly from their definitions that together, these three mode
management requirements imply compatible modes for a given global configuration:
Lemma 3.14 (Management requirements ensure compatibility).
  lock-managed-modes-mem-compatible gc   unmanaged-var-modes-compatible gc
                               no-lock-mds-gc gc
                                    compatible-modes (mdss gc)

                                                 26
   Proofs of invariance then proceed by induction over the single-step evaluation semantics
of an arbitrary thread taking a step to progress the system to a new global configuration.
   For the first management requirement (Definition 3.11):

Lemma 3.15 (Single-step preservation of lock-managed-modes-mem-compatible).

                    lock-managed-modes-mem-compatible (cms, mem)
                   ⟨ci , mdsi , mem⟩w ⇝w ⟨c′i , mds′i , mem′ ⟩w    i < length cms
                         cms′ = cms[i := (c′i , mds′i )]   cms[i] = (ci , mdsi )
                   lock-managed-modes-mem-compatible (cms′ , mem′ )

Proof. By induction over the single-threaded evaluation semantics of the program at index
i that is taking a step.
   lock(k) preserves the property because it only allows a thread to set lock k’s memory if
it is not already set – it would then become the single unique thread whose mode state is
consistent with holding k. Otherwise, the mode states and memory remain unchanged.
   Similarly, unlock(k) preserves the property because its only possible change is to unset
lock k’s memory, and return the unique thread holding lock k to a mode state consistent with
not holding k.
   The other While commands preserve the property because they do not touch the mode
state nor any lock-variables.

  For the second management requirement (Definition 3.12):

Lemma 3.16 (Single-step preservation of unmanaged-var-modes-compatible).

                       unmanaged-var-modes-compatible (cms, mem)
                   ⟨ci , mdsi , mem⟩w ⇝w ⟨c′i , mds′i , mem′ ⟩w    i < length cms
                             ′            ′       ′
                         cms = cms[i := (ci , mdsi )]      cms[i] = (ci , mdsi )
                      unmanaged-var-modes-compatible (cms′ , mem′ )

Proof. Again, by induction over the single-threaded evaluation semantics of the program at
index i that is taking a step.
   We prove and use lemmas that lock(k) and unlock(k) do not touch any mode state per-
taining to variables that are unmanaged by any locks, and that the remaining While com-
mands do not touch the mode state at all. Therefore evaluation steps cannot possibly have
any effect on the compatibility of modes on these variables.

   These single-step evaluation results lift easily to invariance results over the global multi-
step evaluation semantics quantified over arbitrary schedules. These invariance results, with
the fact that the management requirements ensure compatibility (Lemma 3.14), yield in a
straightforward manner the desired global compatibility invariance theorem:

Theorem 3.17 (Mode management requirements ensure global compatibility).

  lock-managed-modes-mem-compatible gc   unmanaged-var-modes-compatible gc
                               no-lock-mds-gc gc
                               global-modes-compatibility gc


                                              27
3.4   Initial conditions ensuring global modes compatibility
We now define conditions on memory and mode state consistent with no locks being held,
and show that initialising a system under these conditions is enough to satisfy the global
compatibility part (Definition 2.12) of the sound-mode-use side condition (Definition 2.10)
of the compositionality theorem for our security property (Theorem 2.8).
   We define the following predicate for initial memory:

Definition 3.18 (A requirement for initial memory that no locks are held).

                        no-locks-held mem ≜ ∀k. ¬evLock (mem k)

   We then define an initial mode state mds0 :: Mode ⇒ Var set that provides all guarantees
demanded by the lock interpretation parameters varsNoW, varsNoRW (described in Sec-
tion 3.1) for all lock variables in the system, and makes no assumptions:

Definition 3.19 (Initial mode state mds0 ).
                                                         [
                mds0 ≜ λ m. case m of GuarNoW ⇒                   varsNoW k
                                                        k::Lock
                                                            [
                                        | GuarNoRW ⇒                varsNoRW k
                                                          k::Lock
                                        | AsmNoW ⇒ 0/
                                        | AsmNoRW ⇒ 0/

   We are then able to show that these conditions are enough to satisfy the requirements we
just showed (in Section 3.3) ensure global modes compatibility for While:

Lemma 3.20 (Initialising with no-locks-held, mds0 ensures global modes compatibility).

                 no-locks-held mem        ∀(c, mds) ∈ set cms. mds = mds0
                          global-modes-compatibility (cms, mem)

Proof. Theorem 3.17 obliges us to show that the mode management conditions (Definitions
3.11, 3.12, and 3.13) hold. This follows straightforwardly from all the relevant definitions.



4     Target language: RISC with mutex locks
Here we introduce RISC with mutex locks (hereafter RISC), the target of our compiler.
This is a generic RISC-style assembly language based on the RISC architecture targeted by
the compilation scheme of Tedesco et al. (2016). A RISC program text is a list of RISC
instructions I, each optionally associated with a label:

                      I ::= [l :]B
                      B ::= Load r v | Store v r | Jmp l | Jz l r | Nop
                            MoveK r n | MoveR r r | Op ⊕ r r
                            LockAcq k | LockRel k

                                              28
   Here we fix the types of the constant values n :: Val, binary arithmetic operators ⊕ ::
Val ⇒ Val ⇒ Val, shared program variables v :: Var, and shared lock variables k :: Lock to be
the same as those for the source While language being compiled. Thus, the only new types
here compared to Section 3 are for the register identifiers r :: Reg, and labels l :: Lab.
   RISC has a small-step operational semantics that is largely unchanged from Tedesco et al.
(2016), in that each step updates a distinguished program counter register, which captures
the current thread’s program location as an index into its RISC program text. The instruc-
tions MoveK, MoveR, Load, and Store, for moving values to and between the registers
and shared memory, and the “no-op” instruction Nop, all increment the program counter;
the “jump if zero” instruction Jz l r updates it to the index of the instruction at l if r contains
zero (else increments it); the unconditional Jmp l does so unconditionally.
   Modifying this instruction set from Tedesco et al. (2016), we then customise the Op
instruction, and add LockAcq k and LockRel k instructions, to have semantics mirroring
those of ⊕, lock(k), and unlock(k) from While respectively. Whereas the RISC equivalents
for the L OCK ACQ and L OCK R EL evaluation rules (described by Section 3.1 for the While
language) increment the program counter, those for L OCK S PIN and L OCK I NVALID leave it
unchanged. There is no RISC evaluation rule that changes the program text.
   Although it has only direct-addressing Load and Store instructions, our RISC target lan-
guage is adequate for implementing all features of While present in Section 3, with the big-
step semantics of exp replaced by small-step operations on registers. We relegate RISC’s
full formal semantics to this paper’s supplement Isabelle/HOL material.
   Our defining LockAcq k and LockRel k to have the same operational semantics on shared
memory and mode state as While’s lock(k) and unlock(k) has two consequences:

    • Our compiler will expect the program developer to supply the details of the locking
      discipline for the While program being compiled, so as to be able to ensure that the
      RISC program it produces follows the same discipline.

    • We then have that global compatibility is invariant for RISC execution, by a near-
      identical argument to the one we presented in Section 3.3, when initialised with the
      conditions we presented in Section 3.4. This presents one option for obtaining RISC-
      level composition of per-thread noninterference properties; however, invoking it di-
      rectly will not be necessary when using the compositional whole-system secure re-
      finement method of Section 2.5. (The alternative options and their application will be
      demonstrated further, respectively in Section 5.4, Section 6.3.)

   As for While in Section 3, we instantiate here for RISC the CVDNI theory of Murray
et al. (2016b) as recalled in Section 2.2, assuming that the underlying concurrency model
(e.g. OS, scheduler etc.) prevents one thread from reading the program text of another. For
RISC, we furthermore assume that the context switching mechanism ensures effectively
that no thread can read or interfere with the contents of the registers (including the pro-
gram counter) when active for another thread. Based on these assumptions, we model
all three of the program counter register’s value pc :: nat, RISC program text P :: I list,
and register bank regs :: Reg ⇒ Val, as thread-private state in the local configuration triple:
⟨((pc, P), regs), mds, mem⟩r . (We use the subscript r to distinguish RISC triples.)




                                                29
5     Verified secure compiler for mixed-sensitivity concurrent
      While programs
This section presents the C OVERN wr-compiler: the first compiler proved to preserve proofs
of noninterference for mixed-sensitivity concurrent programs. By using assume–guarantee
modes (Mantel et al., 2011) and the decomposition principle of Section 2.4 to prove it
introduces (resp.) no race conditions or timing leaks, we demonstrate the applicability to
compiler verification of the CVDNI-preserving refinement notion of Section 2.3 originally
posed by Murray et al. (2016b). Here the decomposition principle (Figure 4) is crucial
because, in separating the concern of preventing new timing leaks, it avoids directly having
to prove the cube-shaped refinement diagram (Figure 3) arising from its need to preserve a
2-safety hyperproperty (Terauchi & Aiken, 2005; Clarkson & Schneider, 2010).
   To preserve security for mixed-sensitivity concurrent programs, CVDNI-preserving re-
finement demands small-step preservation of the contents of all shared memory locations
including those that control value-dependent classifications and implement locks. As it is
unusual for verified compilers to make such promises, we show that a valid approach is to
take advantage of CVDNI’s assume–guarantee framework to:

    1. test and preserve any absence of race conditions implied (via the framework) by
       mutex lock-based synchronisation of access to such locations, and then

    2. use this absence of race conditions to establish the small-step preservation of their
       contents demanded for security-preserving refinement.

In doing so, we prove that some optimisations the wr-compiler performs with its knowledge
of the locking discipline—it avoids unnecessary Loads and recalculation of common subex-
pressions over shared memory when locked—are safe to allow without violating CVDNI.
   In preserving CVDNI, the wr-compiler preserves security proofs that are produced by
the program verification techniques of Sison (2020) for While with mutex locks, which in
turn were adapted from Murray et al. (2016b,c). We will present such an application of our
compiler, to a case study program verified using these techniques, in Section 6.
   Section 5.1 will focus on the wr-compiler’s particular adaptations to CVDNI (beyond
the fault-resilient noninterference targeted by the original compilation scheme of Tedesco
et al. (2016)), in the form of static checks and invariants that (resp.) test for and maintain
the absence of race conditions on lock-protected shared variables. Section 5.2 formalises
a ban, preserved by the wr-compiler, on secret-dependent control flow. Section 5.3 then
presents formal proof (structured by our decomposition principle of Section 2.4) that the wr-
compiler implements CVDNI-preserving refinement. Section 5.4 ultimately presents proofs
of overall security preservation results useful to users of the wr-compiler: Namely, it can
be used either to preserve security down to RISC for an entire concurrent While-language
program, or to preserve the per-thread security for threads that will be run alongside others
written directly in the RISC-language.

5.1    Preserving race-free expression evaluation
Recall from Section 2.3 that CVDNI-preserving refinement (Murray et al., 2016b) demands
that all shared memory contents be preserved, between each target- and source-language

                                             30
configuration that it relates. This is security critical for mixed-sensitivity concurrent pro-
grams, as it ensures that any future influence of those contents on value-dependent classifi-
cations (via control variables) or readability by other threads (in the case of the While and
RISC languages, via lock variables) is preserved.
  The wr-compiler’s approach to preserving the contents of shared memory is to ensure:

   1. That values calculated by expressions are preserved by compilation—that is, they
      have the same value when written back to shared memory (or conditionally branched
      on) by the RISC program, as they did in the original While program; and

   2. That expression evaluation is race-free—that is, free of any race conditions with other
      threads that would render the calculated expression inaccurate.
      To this end, the wr-compiler requires of the original While program that whenever
      each thread attempts to evaluate an expression, it must hold locks ensuring the stabil-
      ity of all variables referenced by the expression.

Thus, its knowledge and enforcement of the locking discipline is crucial, not only to show
that its optimisations preserve CVDNI, but that any meaningful operation over shared mem-
ory preserves it. It therefore tests for and rejects programs that exhibit potential race condi-
tions due to their failure to follow locking discipline—these result in a failed compilation.
   The wr-compiler tracks two kinds of information to achieve these outcomes: the contents
of registers as expressions over shared variables, and assumptions on access to variables by
other threads. The structures the wr-compiler uses to do this are, respectively:

    • A register record Φ :: RegRec ≜ Reg ⇀ exp. This draws inspiration from that used
      by the compilation scheme of Tedesco et al. (2016) (originally of type Reg ⇀ Var)
      to avoid generating unnecessary Load instructions to registers that already contain a
      variable; in addition, here we extend it to track entire expressions on shared variables.

    • An assumption record S :: AsmRec ≜ (Var set × Var set) that tracks which variables
      at a given point in the source While program are “stable” due to having, respectively,
      an AsmNoW or AsmNoRW assumption.

   The wr-compiler’s main function compile-cmd then outputs every register–assumption
record pair (or compilation record) C = (Φ, S ) :: CompRec ≜ RegRec × AsmRec associated
with the program state before execution of each instruction in the output RISC program.5
A typical invocation to compile some c :: cmd takes an initial compilation record C, and
returns the CompRec-annotated RISC program PCs :: (I × CompRec) list (i.e. map fst PCs
recovers an unannotated RISC text), and a final compilation record C′ :

Example 5.1 (Example invocation of the C OVERN wr-compiler).

                          (PCs, l ′ , nl′ ,C′ , failed) = compile-cmd C l nl c

  The remainder of this section will focus on formal properties of the compilation records
output alongside each RISC text: Section 5.1.1 will elaborate on checks enforced on input
  5 For readability, we will use regrec, asmrec to denote a CompRec’s (resp.) fst, snd projections.




                                                     31
programs with the help of AsmRecs, and Section 5.1.2 will present a resulting property that
RegRecs track stable expressions, needed to prove security preservation (in Section 5.3).
   Remaining details (e.g. l, l ′ , nl, nl ′ for label allocation) will be relegated to appendices.
We note here only that (1) compile-cmd may return True for failed to reject the input pro-
gram, such as when it detects a race condition (described further in Section 5.1.1), or if
expression depth exceeds the limit assumed by the register allocation scheme model (elided
to Appendix B); also, (2) relative to the label allocation scheme (elided to Appendix A)
we proved that the control flow of each program fragment compiled by the wr-compiler
remains self-contained even when composed sequentially with other such fragments.

5.1.1   Requirements on inputs to the wr-compiler
We define a shared variable v to be recorded as assumed stable if it and all its control
variables (i.e. C vars v) cannot presently be written to by another thread—that is, if they are
recorded as having either of AsmNoW or AsmNoRW active on them. Formally:
Definition 5.1 (Stability of variable v according to assumption record S ).

     var-stable S v ≜ v ∈ (fst S ∪ snd S ) ∧ (∀v′ ∈ C vars v. v′ ∈ (fst S ∪ snd S ))

   For register record entries to be of any help in ensuring consistency of While and RISC
expression evaluation, we exclude expression evaluation on race-prone variables by lifting
the concept of stability to register records. The following predicate asserts internal con-
sistency of the compilation record C created by compile-cmd, in the sense that the register
record may only map to expressions that mention variables that are recorded as stable by
the assumption record accompanying it. (Here, ran denotes the range of a map.)
Definition 5.2 (Stability of the register record in compilation record C).

    regrec-stable C ≜ ∀e ∈ ran (regrec C). (∀v ∈ exp-vars e. var-stable (asmrec C) v)

   We then implement a collection of stability-checks :: cmd × CompRec ⇒ bool (called
no-unstable-exprs in Sison & Murray (2019)) as a recursive function on the structure of
While programs, that compile-cmd will use to ensure the following requirements of the
given cmd if started with a configuration consistent with the given CompRec:

    • The first two requirements ensure that programs comply with the locking discipline:

          – The requirement regarding reading from shared variables establishes the main
            outcome of freedom from race conditions we described at the beginning of Sec-
            tion 5.1: The program must not refer to expressions on any unstable variables.
            As a matter of convenience, instead of introducing a dedicated primitive to the
            While language for reading atomically from a single (otherwise-unstable) de-
            vice memory location, in our case study model of Section 6 we model such
            interactions using a simple assignment x := y protected by a “read-atomicity”
            lock on a shared memory location y that models the hardware interface.6
   6 When such atomic hardware primitives exist on a given architecture, we expect it would be straightforward

for source languages to expose them and oblige their architecture-specific compilers to compile them to that
single atomic instruction in the target language’s semantics, which would eliminate the need for such locks.


                                                     32
           – If the program assigns to an unstable shared variable, then it must not be a lock-
             governed one according to the locking discipline. This prevents the violation of
             any guarantees not to write to the variable (due to not holding its lock).

    • The remaining two requirements follow some simplifying assertions, originally made
      by the security type system of Murray et al. (2016b), that ensure mode state remains
      consistent after conditional branching and looping:

           – The two sides of any if-conditional branches in the program must both end with,
             effectively, the same set of locks held—to be precise, judging by their effect on
             the mode state, as captured by the assumption record.
           – For similar reasons, we require any while-loops in the program to restore the
             original set of locks held on loop entry (again, as captured by the assumption
             record) on loop termination.

        We believe these to be reasonable simplifications given that, in our setting, the set of
        variables governed by each lock does not change at runtime in such a way that would
        require access to them to be lock protected (or not) in a conditional manner.

   Together, regrec-stable C and stability-checks c C make up the main two requirements of
a predicate compile-cmd-input-reqs C l nl c imposed on the input arguments to compile-cmd.
(Its other two requirements reflect that the terminated While program stop has no valid com-
pilation, and that the initial label, if provided, must be valid—see Appendix A.) If any of
these requirements are violated, compile-cmd rejects the program with failed = True:
Definition 5.3 (Requirements on inputs to compile-cmd).

        compile-cmd-input-reqs C l nl c ≜ stability-checks c C ∧ regrec-stable C ∧
                                                c ̸= stop ∧ (∀x. l = Some x −→ x < nl)

5.1.2    Proof that all tracked register contents are stable
Imposing the predicate compile-cmd-input-reqs (Definition 5.3) gives us enough informa-
tion to prove a lemma that compile-cmd only ever outputs stable register records, that attest
to the fact that registers contain the results of evaluating expressions on stable variables.
   Stated more precisely, every RISC program returned by a successful invocation of
compile-cmd is annotated by CompRecs all with stable register records, and furthermore
that the final CompRec’s register record is also stable:
Lemma 5.4 (Successful compilations output only stable register records).

    (PCs, l ′ , nl′ ,C′ , False) = compile-cmd C l nl c   compile-cmd-input-reqs C l nl c

          (∀pc < length PCs. regrec-stable (map snd PCs)[pc]) ∧ regrec-stable C′

Proof. By induction on the structure of the While language program c, making reference
to the implementation of compile-cmd.
   For cases that must compile expressions, we furthermore prove and make use of a lemma
by induction on the structure of expressions, making reference to the implementation of the

                                                 33
expression compiler function compile-expr called by compile-cmd. In essence, we prove
that (sub)expressions appearing in register records must be stable, for two reasons:
   First, they are always only ever subexpressions over variables that must have been stable
in the input program when their contents were first loaded into registers.
   Second, when compiling an unlock(k), the wr-compiler will always flush all register
records that make reference to any variables that the unlock(k) makes unstable.

5.2   Preserving a ban on secret-dependent control flow
The wr-compiler assumes that input While programs have no conditional branches on
High-sensitivity values (High-branching), and therefore no secret-dependent control flow.
This is a restriction commonly applied as a means to prevent all implicit flows, including
timing leaks. This restriction will then be preserved by the wr-compiler for its output
RISC programs, reflected primarily in the design of the concrete coupling invariant Iwr
(see Section 5.3.3).
   Specifically, the wr-compiler assumes that the confidentiality of input While programs
is witnessed by a strong low-bisimulation modulo modes with an extra requirement (sup-
plied as a parameter, as in Section 2.2) that effectively disallows any present or past High-
branching. Relying on the fact that a low-bisimulation already asserts Low-equivalence of
memories, the extra requirement asserts that it furthermore pairs only configurations at the
same program location, and that any if-conditional expressions must evaluate to the same
value in both configurations’ memories. Here, the helper function leftmost-cmd gives the
leftmost in a sequence of ;-separated While-language commands:

Definition 5.5 (An extra requirement for low-bisimulations B to ban High-branching).

 no-high-branching B ≜
 ∀c c′ mds mem mem′ . (⟨c, mds, mem⟩w , ⟨c′ , mds, mem′ ⟩w ) ∈ B −→ c = c′ ∧
      (∀e c1 c2 . leftmost-cmd c = if e then c1 else c2 fi −→ evexp mem e = evexp mem′ e)

  Then, in Section 5.4, we will prove that the wr-compiler produces confidential RISC
programs with no secret-dependent control flow, as witnessed by a low-bisimulation that
asserts a similar extra requirement for RISC programs. In effect, this is the pc-security
notion of Molnar et al. (2006), but also explicitly equating the program text:

Definition 5.6 (A pc-security–like requirement for RISC bisimulations B).

pc-security B ≜ ∀pc pc′ P P′ regs regs′ mds mem mem′ .
(⟨((pc, P), regs), mds, mem⟩r , ⟨((pc′ , P′ ), regs′ ), mds, mem′ ⟩r ) ∈ B −→ pc = pc′ ∧ P = P′

5.3   Use of the decomposition principle
Having covered the most relevant aspects of the wr-compiler’s implementation, we now
present the refinement relation Rwr (in Section 5.3.1), pacing function abs-stepswr (in Sec-
tion 5.3.2), and concrete coupling invariant Iwr (in Section 5.3.3), parameters we use to ap-
ply the decomposition principle we presented in Section 2.4 to prove (in Section 5.3.4) that



                                              34
successful compilations are legitimised by secure-refinement (Definition 2.15)—the desired
confidentiality-preserving notion of refinement for mixed-sensitivity concurrent programs.
   The strategy laid out by the decomposition principle will be to prove that these param-
eters satisfy decomp-refinement-safe (Definition 2.19) for a targeted class of input While-
language programs—ones with no secret-dependent control flow, as we specified in Sec-
tion 5.2—meaning (for such programs) we can use the parameters to enforce that wr-
compiler introduces no secret-dependent inconsistencies in termination, timing behaviour,
or assume–guarantee modes.
   In doing so we avoid a direct proof of the cube-shaped refinement diagram (Figure 3)
of Murray et al. (2016b)—which would have involved reasoning about both Rwr and Iwr
at once—and instead prove (with the assistance of abs-stepswr ) a square-shaped refinement
diagram for Rwr (Figure 4a) more typically found in compiler verification.

5.3.1   Refinement relation Rwr and its invariants
In this section we introduce the refinement relation Rwr that characterises compilation of
programs from While to RISC using the wr-compiler, and prove it satisfies the two proper-
ties demanded of Rwr (alone) by formal secure-refinement (Definition 2.15):

   1. Preservation of modes and all contents of shared memory (preserves-modes-mem,
      Definition 2.13), and

   2. Closedness under changes by other threads (closed-others, Definition 2.14).

An actual proof of refinement (using the square-shaped diagram of Figure 4a) for Rwr will
be deferred to Section 5.3.2, which introduces the abs-stepswr function pacing it.
   Just like the earlier example of a secure refinement relation (in Figure 2), the refinement
relation Rwr pairs abstract (here, While-language) with concrete (here, RISC-language)
program configurations. For example, the if expr case of Rwr relates the expression-
evaluation part of the While command if e then c1 else c2 fi, with the corresponding part of
the RISC program obtained by running compile-cmd on it, including the conditional jump
Jz after expression evaluation. (This case is depicted in Figure 10, and a relevant excerpt
of the compile-cmd implementation provided in Figure 11 for comparison, both on page 63
of Appendix C. An informal description of all the cases of Rwr , their purpose, and the
invariants they maintain, can also be found in Appendix C.)
   We define almost all the cases of Rwr to assert at least one successful run of compile-cmd
(where failed = False). We then define a guard that we impose to restrict the scope of
Rwr only to consider local program configurations consistent with the relevant compilation
record produced by compile-cmd. In short, this ensures the actual values in the register bank
regs equal any expression the register record says they should have, as evaluated under the
current mem; and furthermore, that the assumption record is consistent with the AsmNoW
and AsmNoRW modes in the actual mds. Formally:




                                             35
Definition 5.7 (Configuration consistency requirements for compiled commands).

compiled-cmd-config-consistent C regs mds mem ≜
  regrec-mem-consistent (regrec C) regs mem ∧ asmrec-mds-consistent (asmrec C) mds
where
  regrec-mem-consistent Φ regs mem ≜ ∀r e. Φ r = Some e −→ regs r = evexp mem e
        (Consistency between register record, register bank, and shared memory)
  asmrec-mds-consistent S mds ≜ S = (mds AsmNoW, mds AsmNoRW)
        (Consistency between an assumption record and a mode state)

   Apart from using compiled-cmd-config-consistent to restrict the scope of Rwr in this
manner, we will also impose it in Section 5.3.4 as initial configuration requirements for
compiled programs: Only configurations obeying them may be used to initialise a RISC
program compiled by the wr-compiler with initial CompRec C.
   The cases of Rwr also tend to assert regrec-stable (Definition 5.2), which we already
proved holds for all compilation records produced by the wr-compiler (Lemma 5.4).
   Finally, whenever a case of Rwr is inductive (e.g. the if expr case, for its nested calls
to compile-cmd for each of its “then” and “else” branches) it quantifies over all configura-
tions that obey compiled-cmd-config-consistent (Definition 5.7) and regrec-stable (Defini-
tion 5.2) relative to the initial compilation record given to each nested call to compile-cmd.
   With Rwr thus specified, we can now prove the two requirements for secure-refinement
that pertain to Rwr alone: preserves-modes-mem (Definition 2.13), and closed-others (Def-
inition 2.14). In short, preserves-modes-mem is largely enforced by the definition of Rwr ,
but closed-others relies in part on Rwr only ever talking about stable register records:
Lemma 5.8 (Rwr preserves modes and memory).

                                 preserves-modes-mem Rwr

Proof. By induction on the structure of Rwr .
  For all cases of (lcw , lcr ) ∈ Rwr , lcw =mem
                                             mds lcr is either asserted directly by the guards or
obtainable from the inductive hypothesis.

Lemma 5.9 (Rwr is closed under changes by others).

                                      closed-others Rwr

Proof. By induction on the structure of Rwr .
   Changes by others (Definition 2.14) only modify writable variables the same way for
both configurations, so preservation of =memmds is immediate. Also, regrec-mem-consistent
is unaffected because by Lemma 5.4, compile-cmd only creates regrec-stable records—
i.e. referring to no writable variables. No other Rwr guards mention shared memory.

5.3.2     Refinement pacing function abs-stepswr
In this section we nominate a pacing function, abs-stepswr , specifying the number of eval-
uation steps with which a While program should simulate each step of the RISC program

                                               36
to which the wr-compiler compiled it. Using the square-shaped “refinement preservation”
diagram of Figure 4a (part of Definition 2.18), we then prove that the Rwr relation we in-
troduced in Section 5.3.1 is a refinement when “paced” by abs-stepswr in this manner.
   Here we define abs-stepswr to depend only on the current program location; consequently,
as long as the wr-compiler introduces no secret-dependent control flow, it will also intro-
duce no timing leaks—that is, no secret-dependent variations to the pacing of the program,
as disallowed by Figure 4b (part of Definition 2.19)—which we will be obliged to prove in
Section 5.3.4. To this end, abs-stepswr primarily looks at the form of the RISC instruction
(sometimes While command) about to be executed, dividing them into three categories:
    • Instructions output by compile-expr: Load, Op, and MoveK. For these, abs-stepswr
      returns 1 if the leftmost-cmd (the leftmost in a sequence of ;-separated commands)
      of the While program is “while e do c od”, to allow it to step to “if e then (c ;
      while e do c od) else stop fi” concurrently with the first RISC step of the compiled
      expression itself. Otherwise, abs-stepswr returns 0, to indicate the While program
      standing still while the RISC program takes new steps to evaluate the expression.
    • “Epilogue” steps: Jmp and Nop when used for control flow at the end of a smaller
      compiled program in the context of a larger one. For these, abs-stepswr returns 0.
    • All other RISC instructions are assumed to proceed at a lockstep pace with the While
      command they were compiled from, and for these abs-stepswr returns 1.
  Having nominated abs-stepswr and Rwr , we now have the parameters over which we are
obliged, by secure-refinement-decomp (Definition 2.18), to prove refinement preservation
(Figure 4a). To this end, we prove firstly that every step of execution of a RISC program,
produced by the wr-compiler from a While program, maintains the consistency demanded
by compiled-cmd-config-consistent between configurations and compilation records:
Lemma 5.10 (Successfully compiled programs maintain config consistency requirements).

 (PCs, l ′ , nl′ ,C′ , failed) = compile-cmd C l nl c      compile-cmd-input-reqs C l nl c
  failed = False            pc < length PCs     P = map fst PCs           Cs = map snd PCs
                     compiled-cmd-config-consistent Cs[pc] regs mds mem
                   ⟨((pc, P), regs), mds, mem⟩r ⇝r ⟨((pc′ , P), regs′ ), mds′ , mem′ ⟩r )

compiled-cmd-config-consistent (if pc′ < length P then Cs[pc′ ] else C′ ) regs′ mds′ mem′
Proof. Unfolding Definition 5.7, we in fact prove it separately for regrec-mem-consistent
and asmrec-mds-consistent, both times by induction on the structure of While program c.
   In each case, we use the simplifiers for the compile-cmd implementation to yield the
corresponding RISC program fragment in question, and then prove the lemma for each of the
possible locations of pc in the compiled program. For both proofs, there is some trickiness
in accounting for (and ruling out) which destination pc′ must be considered for each of these
cases of pc, particularly for those While programs that compile to RISC programs that may
have jumps in them.
   Control flow trickiness aside, the intuition for regrec-mem-consistent is that it tests the
correctness of the compilation of expressions. For this we prove a sublemma for mainte-
nance of compiled-cmd-config-consistent, by induction on the structure of expressions e

                                              37
that are encountered in the While programs if e then c1 else c2 fi, while e do c′ od, and
v := e. Additionally, unlock(k) flushes register record entries mentioning variables that are
to become unstable, and while e do c′ od conservatively flushes entries to force evaluation
of the loop condition expression. This is safe trivially because flushing entries can never
make a consistent register record inconsistent. The rest of the cases for c are straightfor-
ward because they do not touch the register record.
   Then for asmrec-mds-consistent, the substantial part of the proof is as a test of the cor-
rectness of the compiler’s bookkeeping of assumptions being consistent with the semantics
of lock(k) and unlock(k). The other cases for c do not touch the mode state.

  Also, we must prove a correctness lemma for the expression compiler:

Lemma 5.11 (Correctness of the expression compiler).

          (PCs, r,C′ , False) = compile-expr C A l e =⇒ (regrec C′ ) r = Some e

Proof. By induction on the structure of expressions e, using the simplification rules for
the implementation of compile-expr, and also relying on assumptions of correctness of the
register allocation scheme supplied by the instantiator of the theory.

  Armed with these facts, we can now prove the main refinement preservation result:

Lemma 5.12 (Rwr is a refinement paced by abs-stepswr ).

                ∀lcw lcr . (lcw , lcr ) ∈ Rwr −→ (∀lc′r . lcr ⇝r lc′r −→
                                   (abs-stepswr lcw lcr )
                     (∃lc′w . lcw ⇝w                        lc′w ∧ (lc′w , lc′r ) ∈ Rwr ))

Proof. By induction on the structure of Rwr . (Refer to Appendix C for an informal descrip-
tion of all cases of Rwr .)
   The base case stop is immediate, as it pertains to a terminated While and RISC program.
The base cases that proceed in one step to a terminating program configuration (skip nop,
assign store, lock acq, lock rel) are fairly straightforward because after dealing with
the single step, the resulting obligation can then be handled by the stop case. This leaves
the last remaining base case assign expr, which proceeds in one step either to itself, or
to assign store. In all these cases, we use Lemma 5.10 to obtain the preservation of
the guards demanded by the Rwr introduction rule for the destination configuration of the
step. Particularly, the assign store case must make use of regrec-mem-consistent and
the correctness of compile-expr (Lemma 5.11) to ensure that once the evaluated expression
is written back to shared memory, lc′w =mem     ′
                                          mds lcr holds as demanded by the stop case.
   The inductive cases that concern expression evaluation (if expr, while expr) are much
like assign expr in that they have the possibility of progressing in one step to themselves.
Unlike assign expr however, their other possibility is a conditional jump based on the
result of that expression. Again we use Lemma 5.11 to obtain that the result is an accurate
calculation of the expression, and this time we prove by the two different cases whether
if expr ends up in if c1 or if c2, or if while expr ends up in while inner or at
stop (having jumped to the exit label). In these cases, the guards over which the inductive
references to Rwr have been quantified are versatile enough to discharge themselves (when


                                                 38
* expr steps to itself), or to discharge any reachable initial starting state for the nested
compiled RISC program, given that Lemma 5.10 ensures the invariance of these guards.
   This just leaves the inductive cases that pertain to configurations inside a nested com-
piled RISC program (if c1, if c2, while inner), or at the end of one (epilogue step,
while loop). In these cases, the inductive hypotheses obtained from the inductive refer-
ence to Rwr are always enough to satisfy the guards demanded by the possible destination
cases. Like in the proof of Lemma 5.10, the trickiness mostly comes from accounting for
all the possible cases of control flow (ruling out spurious destinations) that need to be con-
sidered.

5.3.3   Concrete coupling invariant Iwr
The next element needed is the concrete coupling invariant Iwr . Recall from Section 5.2
that the no-high-branching requirement (Definition 5.5) ensures that input While programs
have no secret-dependent control flow; here we choose Iwr to ensure that the wr-compiler
has not introduced any new secret-dependent control flow in the output RISC program.
   We define Iwr formally to assert that the witness strong low-bisimulation (modulo
modes) to be derived for the output program only pairs local configurations that are at the
same location pc = pc′ of the same RISC program P = P′ :

Definition 5.13 (Concrete coupling invariant Iwr for compiled programs).

Iwr ≜ {(⟨((pc, P), regs), mds, mem⟩r , ⟨((pc′ , P′ ), regs′ ), mds′ , mem′ ⟩r ) | (pc, P) = (pc′ , P′ )}

   From this definition, pc-security (Definition 5.6) is clearly immediate for any concrete
bisimulation B C of B R Iwr (Definition 2.16) derived using Iwr .

5.3.4   Proof of CVDNI-preserving refinement
With Rwr , abs-stepswr , and Iwr nominated, we are ready to prove confidentiality-
preserving refinement using the decomposition principle secure-refinement-decomp (Defi-
nition 2.18).
   To this end, we now prove the suitability of these three parameters, for While programs
that do not branch on High-sensitivity values (as we specified earlier, in Section 5.2):

Lemma 5.14 (Rwr , abs-stepswr , Iwr are safe for secure-refinement decomposition).

                      strong-low-bisim-mm B             no-high-branching B
                       decomp-refinement-safe B Rwr Iwr abs-stepswr

Proof. Unfolding Definition 2.19 gives us the following obligations. (See also Figure 4.)
   For consistent stopping behaviour, we prove a lemma that RISC programs stop if and only
if their pc is outside the program text P, i.e. pc > length P. Because Iwr equates pc and P
for the two configurations, then clearly both have identical stopping behaviour.
   For consistency of change in timing behaviour, abs-stepswr depends only on While and
RISC program locations, and no-high-branching and Iwr forces them (respectively) to be
equal for the local configurations under consideration.


                                                  39
   For closedness of Iwr under lockstep execution, the only non-straightforward cases to
consider are conditional branching, and the locking primitives. For conditional branching,
we use no-high-branching for B with memory preservation via Rwr (Lemma 5.8) to ensure
that the conditional branching outcome is the same on both sides.
   Finally, as the only operations that touch mode state, the locking primitives are the only
non-straightforward cases for modes-equality maintenance under lockstep execution. As all
lock memory is classified Low (Proposition 3.4), we use strong-low-bisim-mm for B with
memory preservation via Rwr to ensure the RISC configurations behave consistently.

Lemma 5.15 (Rwr , abs-stepswr , Iwr meet decomposed secure-refinement requirements).

                    strong-low-bisim-mm B         no-high-branching B
                   secure-refinement-decomp B Rwr Iwr abs-stepswr

Proof. Unfolding Definition 2.18, the obligations pertaining only to Rwr and abs-stepswr
are discharged by Lemma 5.12, Lemma 5.9, and Lemma 5.8. Pertaining to Iwr : Clearly
Iwr is symmetric, and furthermore it is cg-consistent (Definition 2.6) because the ac-
tions over which Iwr must be closed modify only the shared memory, and Iwr places
only restrictions on the program text and current location. The final obligation (regarding
decomp-refinement-safe) is discharged by Lemma 5.14.

   From this it follows immediately via Theorem 2.20 that Rwr with the help of Iwr de-
scribes a confidentiality-preserving refinement for non-High-branching While programs:

Corollary 5.16 (Rwr is a secure refinement for non-High-branching programs).

                    strong-low-bisim-mm B         no-high-branching B
                              secure-refinement B Rwr Iwr

   Finally we prove that successful compilation produces a RISC program related by Rwr to
its input While program, when started with corresponding (same mds, mem) and reasonable
(according to compiled-cmd-config-consistent) initial configurations:

Theorem 5.17 (Successful compilations are refinements in Rwr ).

    (PCs, l ′ , nl′ ,C′ , failed) = compile-cmd C l nl c   compile-cmd-input-reqs C l nl c
failed = False            compiled-cmd-config-consistent C regs mds mem     P = map fst PCs

                    (⟨c, mds, mem⟩w , ⟨((0, P), regs), mds, mem⟩r ) ∈ Rwr

Proof. By induction on the structure of the While-language.
   The compiler input and initial configuration conditions we impose allow us to have each
of skip, cmd ; cmd, if exp then cmd else cmd fi, while exp do cmd od, v := exp, lock(k),
and unlock(k) and their compiled output meet the guards of the introduction rules for the
cases skip, seq, if expr, while expr, assign expr, lock acq, and lock rel of Rwr
(described further in Appendix C) that we designed for them, respectively.




                                             40
5.4     Proof of compositional noninterference preservation
Going beyond the level of detail of our presentation in Sison & Murray (2019), we now
present the final few steps to obtain preservation of whole-system security for concurrent
compositions of RISC threads when all are obtained via compilation by the wr-compiler
(Section 5.4.1). In addition to this, we obtain preservation of per-thread compositional
security for each program thread compiled, and other properties that may be useful for their
composition with RISC threads proved secure directly at the RISC level (Section 5.4.2).

5.4.1    Whole-system security preservation
To use the whole-system refinement theorem (Theorem 2.23), we are obliged to show that,
in addition to establishing a secure-refinement (Definition 2.15, which we just showed
in Section 5.3), the wr-compiler also preserves local-mode-compliance as demanded by
compositional-refinement (Definition 2.22). Then, as we noted in Section 2.5, there is
no need for us to prove preservation of the non-compositional global-modes-compatibility
condition—the whole-system refinement theorem takes care of that.
   The local compliance preservation result follows from a property of the refinement rela-
tion, Rwr . Here, “respects-own-guarantees” is from Definition 2.11:
Lemma 5.18 (Each step from a RISC configuration in Rwr respects its own guarantees).

                   (⟨c, mds, mem⟩w , ⟨((pc, P), regs), mds, mem⟩r ) ∈ Rwr

                      respects-own-guarantees (((pc, P), regs), mds)

Proof. By induction on the structure of Rwr .
   Knowing that the While command does not access lock-governed variables without hold-
ing the relevant lock (via the stability-checks asserted as part of compile-cmd-input-reqs by
every relevant case of Rwr ), we are obliged to show that the RISC instruction paired to it by
Rwr similarly respects the guarantee modes implied by the locking discipline (as specified
in Section 3.1). We do so with a mixed Isar/“apply”-style proof that exercises the relevant
cases of the RISC semantics, using lemmas about control flow under sequential composition
(mentioned in Section 5.1; see also Appendix A). Propositions 3.8 and 3.9 also play a role
in excluding certain cases from consideration.

Lemma 5.19 (Refinements in Rwr ensure local mode compliance).

                   (⟨c, mds, mem⟩w , ⟨((pc, P), regs), mds, mem⟩r ) ∈ Rwr

                    local-mode-compliance ⟨((pc, P), regs), mds, mem⟩r

Proof. Unfolding Definition 2.11, we must show that what was proved by Lemma 5.18
holds for every RISC configuration reachable from ⟨((pc, P), regs), mds, mem⟩r .
   First, we prove a lemma that establishes that every such reachable RISC configuration is
also paired by Rwr to some While configuration. Specifically, we prove that Rwr is closed
under a notion of “pairwise reachability under mode-permitted havoc”, wherein:
   1. Every one step by the RISC program is matched by either zero or one step by the
      While program, as specified by abs-stepswr (Section 5.3.2).

                                             41
   2. Between each evaluation step, arbitrary changes are allowed to occur to the memory
      locations judged by the mode state to be writable (Definition 2.5).

   Because all such RISC configurations reachable from the initial one are in Rwr , it then
follows from Lemma 5.18 that they respect their own guarantees, as required.

   We then initialise the compiler with an empty C0 :: CompRec that knows nothing about
the register contents, and does not assume any variables to be stable:

Definition 5.20 (Empty compilation record C0 ).

                                  C0 ≜ ((λ . None), (0,
                                                     / 0))
                                                        /

  With these definitions we have the desired consistency result:

Lemma 5.21 (Initial C0 , mds0 are consistent with no-locks-held).

       no-locks-held mem =⇒ compiled-cmd-config-consistent C0 regs mds0 mem

Proof. This is straightforward by unfolding Definitions 5.7, 3.18, 3.19, and 5.20, also rely-
ing on the cleanliness conditions Proposition 3.5 and Proposition 3.7 on locking disciplines
specified in Section 3.2.

   We now have enough information to derive a whole-system security result, for concurrent
RISC programs obtained by running the wr-compiler on any list “cs” of secure While com-
mands (one for each thread in the program). As we explained in Section 5.2, the C OVERN
wr-compiler’s preservation of security is only for programs with no-high-branching (Def-
inition 5.5); furthermore, so that we can derive global compatibility for multiple of these
programs run concurrently as threads (as per Section 3.4), we will impose no-locks-held
(Definition 3.18) as an initial condition. Therefore, the security preservation theorem
we choose to prove here demands that every thread of the input While program be
            no-high-branching
com-secureno-locks-held       (Definition 2.7, with additional requirements as specified). It
then promises that the output program is sys-secureno-locks-held :

Theorem 5.22 (Secure threads compiled by the wr-compiler form a secure system).

length cmsr = length cs ∧
∀i < length cmsr . ∃l nl PCs l ′ nl′ C′ regs.
  com-secureno-high-branching
            no-locks-held     (cs[i], mds0 ) ∧
  (∀mem. no-locks-held mem −→ local-mode-compliance ⟨c, mds0 , mem⟩w ) ∧
  (PCs, l ′ , nl′ ,C′ , False) = compile-cmd C0 l nl cs[i] ∧ compile-cmd-input-reqs C0 l nl cs[i] ∧
  cmsr [i] = (((0, map fst PCs), regs), mds0 )

                                   sys-secureno-locks-held cmsr

Proof. We invoke Theorem 2.23, supplying:

    • no-locks-held for the INIT parameter at both While and RISC level.


                                                 42
    • Ball , Rwr , Iwr to be respectively the witness bisimulation, refinement relation, and
      coupling invariant for all compiled threads, where we define Ball to be the arbitrary
      union of all strong low-bisimulations modulo modes that disallow high-branching:

               Ball ≜       { B | strong-low-bisim-mm B ∧ no-high-branching B }
                        [


    • mds0 to be the initial mode state for all While threads in cs.
The first thing we must prove is that the original program satisfies sound-mode-use (Defi-
nition 2.10) when initialised with mds0 and no-locks-held; we have the local part from this
theorem’s local-mode-compliance assumption, and the global part from Lemma 3.20.
   We then discharge the demands of compositional-refinement Ball Rwr Iwr (Defini-
tion 2.22) using Corollary 5.16, Lemma 5.19, and by unfolding Definition 5.13.
   It only remains for us to show that the initial RISC–While and While–While config-
uration pairs of interest are captured respectively by Rwr and Ball . We obtain the former
using this theorem’s assumptions and Lemma 5.21 to discharge the guards of Theorem 5.17.
Finally, we use the assumption that the original program is com-secureno-high-branching
                                                                            no-locks-held and
unfold Definition 2.7 to obtain that there exists some strong-low-bisim-mm B that enforces
no-high-branching for every configuration pair with low-equal memories (modulo mds0 )
and no-locks-held initially; therefore, these state pairs must all be captured by Ball .

5.4.2   Per-thread compositional security preservation
For system developers who may want to run programs compiled from While to RISC con-
currently with other programs written directly in RISC, per-thread security preservation re-
sults may be useful. To compose the security proofs for those threads, direct RISC-level
lemmas for the “sound-mode-use” side conditions of the compositionality theorem (Theo-
rem 2.8) will also be needed. We therefore present these as an alternative method to obtain
compositional security results for RISC programs, applicable when only partially produced
by compilation from While by the wr-compiler.
  Given the facts we established in Section 5.3, we have straightforwardly that such pro-
grams’ executions are captured by the bisimulation derived from B, Rwr , Iwr , when started
with reasonable initial configurations corresponding to those paired by B:
Lemma 5.23 (Programs witnessed by B are captured by B C of B Rwr Iwr once compiled).

            strong-low-bisim-mm B          (⟨c, mds, mem1 ⟩w , ⟨c, mds, mem2 ⟩w ) ∈ B
            ′    ′ ′
     (PCs, l , nl ,C , failed) = compile-cmd C l nl c    compile-cmd-input-reqs C l nl c
failed = False        compiled-cmd-config-consistent C regs mds mem1           P = map fst PCs
                        compiled-cmd-config-consistent C regs mds mem2

        (⟨((0, P), regs), mds, mem1 ⟩r , ⟨((0, P), regs), mds, mem2 ⟩r ) ∈ B C of B Rwr Iwr
Proof. Straightforward from the definition of B C of (Definition 2.16), using Theorem 5.17
to show membership of Rwr , and the definition of strong-low-bisim-mm (Definition 2.4)
to show that the memories are low-equal modulo modes, as required by B C of. Finally,
membership of Iwr (Definition 5.13) follows from the fact that the paired configurations
are at the same location (program counter 0) of the same program P.

                                               43
   We are ready to state the per-thread security preservation result formally. Given an input
While command that satisfies com-secureno-high-branching
                                            no-locks-held   with mds0 initially, it promises
                                                                  pc-security
that the RISC program output by the wr-compiler is com-secureno-locks-held    with mds0 :

Theorem 5.24 (Preservation of per-thread confidentiality by the wr-compiler).

                              com-secureno-high-branching
                                        no-locks-held     (c, mds0 )
          ′    ′ ′
   (PCs, l , nl ,C , False) = compile-cmd C0 l nl c       compile-cmd-input-reqs C0 l nl c

                  com-securepc-security
                            no-locks-held (((0, map fst PCs), regs), mds0 )

Proof. We are given by com-secureno-high-branching
                                    no-locks-held   (Definition 2.7) that for low-equal start-
ing configurations (modulo modes) of c with no locks held, there exists some witness B
satisfying both strong-low-bisim-mm and no-high-branching.
   From this and Lemma 5.23 we have that the output program’s corresponding execution
is captured by a RISC semantics-level relation B C of B Rwr Iwr derived from this B, with
Lemma 5.21 discharging the compiled-cmd-config-consistent requirements.
   Corollary 5.16 then gives us that secure-refinement B Rwr Iwr holds,
and from this and strong-low-bisim-mm B using Theorem 2.17 we have
strong-low-bisim-mm (B C of B Rwr Iwr ). This is enough to show com-securepc-security
                                                                                  no-locks-held
for the RISC program, by Definition 2.7; as Section 5.3.3 noted, pc-security (Definition 5.6)
is immediate from the definition of Iwr .

   To prove a whole-system security result at the RISC level for the compiled program, we
must also prove sound-mode-use (Definition 2.10). To that end, we prove a local and global
result for RISC programs output by the wr-compiler when given a secure While program.
The former follows from the local compliance result in the preceding section:

Lemma 5.25 (Threads compiled by the wr-compiler obey local compliance).

   (PCs, l ′ , nl′ ,C′ , False) = compile-cmd C0 l nl c    compile-cmd-input-reqs C0 l nl c
                                          no-locks-held mem

              local-mode-compliance ⟨((0, map fst PCs), regs), mds0 , mem⟩r

Proof. We use Theorem 5.17 and Lemma 5.21 to obtain membership in Rwr , which then
allows us to use Lemma 5.19.

  Then we prove invariance of global modes compatibility (as in Section 3.3) for compiled
RISC programs, due to RISC’s identical semantics to While regarding locking and modes:

Lemma 5.26 (Initialising RISC with no-locks-held, mds0 ensures global compatibility).

          no-locks-held mem        ∀(((pc, P), regs), mds) ∈ set cmsr . mds = mds0
                          global-modes-compatibility (cmsr , mem)

Proof. We firstly prove versions of Lemma 3.15, Lemma 3.16, and Theorem 3.17 for RISC,
following exactly the same reasoning as we did in Section 3.3 for While. This is because
the RISC instructions LockAcq k and LockRel k are (like lock(k) and unlock(k) in While)

                                              44
the only ones in their language that modify mode state, and their semantics regarding mode
state and lock memory are identical to those of the lock(k) and unlock(k) commands. The
present result then follows for the same reason that Lemma 3.20 did for While.

   With this result, it is now possible to invoke Theorem 2.8 to compose RISC-level per-
thread security and mode compliance, whether they were obtained via the wr-compiler
(using Theorem 5.24 and Lemma 5.25, respectively), or proved directly at RISC level.
   We remark that, for programs wholly compiled by the wr-compiler, Theorem 5.22
can be subsumed by a whole-system preservation result that no longer demands
local-mode-compliance for each thread, due to our ability to obtain it directly at RISC level:

Theorem 5.27 (Secure threads compiled by the wr-compiler form a secure system).

 ∀i < length cmsr . ∃c l nl PCs l ′ nl′ C′ regs.
    com-secureno-high-branching
              no-locks-held     (c, mds0 ) ∧
    (PCs, l ′ , nl′ ,C′ , False) = compile-cmd C0 l nl c ∧ compile-cmd-input-reqs C0 l nl c ∧
    cmsr [i] = (((0, map fst PCs), regs), mds0 )

                                  sys-secureno-locks-held cmsr

Proof. By Theorem 2.8 and unfolding Definition 2.10, we are required to prove security and
local mode compliance for every thread of the compiled RISC program, and global modes
compatibility between them all as a whole, assuming no-locks-held and using mds0 initially.
These requirements are immediate using Theorem 5.24, Lemma 5.25, and Lemma 5.26.


6    Case study: Cross Domain Desktop Compositor input handler
This section presents—as the main case study for the C OVERN wr-compiler—a mixed-
sensitivity concurrent program whose source-level noninterference properties are preserved
by verified secure compilation down to an assembly-level model.
   The Cross Domain Desktop Compositor (CDDC) of Beaumont et al. (2016) is a desktop
device that gives trusted users the option of replacing multiple monitors, keyboards, and
mice with a single multi-level secure user interface (via a single monitor, keyboard, and
mouse, as depicted in Figure 5a) when using several desktop computers simultaneously.
   Here we present as case study a program (replacing customised hardware) that handles
the incoming mouse and keyboard inputs to the CDDC. This program has served as a par-
ticularly good case study, because it features both of the characteristics for which proving
information-flow security is this work’s main focus:

    • Concurrency—here, between software components whose execution is interleaved
      (by the seL4 operating-system microkernel (Klein et al., 2014)), and that interact via
      shared memory.

    • Mixed-sensitivity reuse—here, of system resources (notably the input devices) and
      memory locations, for input whose sensitivity level can be different at different times.



                                               45
(a) CDDC hardware use-case setup.                    (b) CDDC hardware architecture.
The bar painted at the top of the screen indicates   The HID switch—implemented in software on
the computer set to receive all keyboard events.     top of seL4—runs on an ARM Cortex A9 core,
Mouse events are delivered to the owner of the       and operates a compositor device implemented
topmost window underneath the mouse cursor.          (as in Beaumont et al. (2016)) using an FPGA.

Figure 5: Functional schematics for Cross Domain Desktop Compositor hardware.
Reproduced from Murray et al. (2018).


   By exercising the C OVERN wr-compiler on a While model of this case study, we show
this compiler verification-based approach to be feasible for obtaining the preservation of
noninterference properties proved at While level, straightforwardly and for little extra effort,
down to a RISC model of the program.
   The section will proceed as follows. Following an overview in Section 6.1 of the main
characteristics of the case study, Section 6.2 presents the formal security properties proved
about its While model—as our focus is its compilation, further details on this model and
the proof techniques used to prove these properties at While level are left to Sison (2020).
Section 6.3 then presents the formal preservation of security properties down to a RISC
model, obtained from running the verified wr-compiler of Section 5 on the While model.

6.1     Overview of the case study
The case study is a software implementation of the human interface device (HID) switch in
the CDDC (see Figure 5b). In short, this part of the CDDC is responsible for determining
the destination of all HID input (keyboard and mouse device) events, and ensuring that the
user remains informed of that destination (by operating a video compositor device, which
renders display elements for that purpose on a shared monitor, as depicted in Figure 5a).

6.1.1    Information-flow security
The HID switch’s responsibilities are security critical, as the CDDC is intended to provide
an interface to multiple desktop computers belonging to different security domains; hence,
the user of the CDDC is expected to choose the sensitivity of the data they input, based on
the computer to which they expect it to be delivered. Furthermore, part of the CDDC’s func-
tionality is to allow users to choose which computer they are interacting with, by clicking on
(accordingly responsive) display elements using the mouse. Thus, the desired information-


                                                 46
Figure 6: Functional schematic of seL4 component architecture for CDDC HID switch.
Reproduced from Murray et al. (2018).


flow security property for the HID switch is that, in providing this functionality, it never
delivers inputs to a destination contrary to the user’s expectations.
   We simplify analysis to the classic High ̸→ Low security policy over the basic two-point
{High, Low} security lattice, and model the HID switch to service only two potential desti-
nation computers.7 One computer is designated as belonging to the High security domain,
and is the only legitimate destination for High-sensitivity input events; the other is desig-
nated as belonging to the Low security domain. The hardware and connections that the
S WITCH component uses to forward events to these computers are modelled as shared vari-
ables classified statically: one High, the other Low (as depicted in Figure 7b). The attacker
is then considered to be an entity that can read at any time from the Low-classified one.

6.1.2    Shared-variable concurrency
   The software implementation (replacing the original FPGA-based implementation (Beau-
mont et al., 2016)) of the CDDC’s HID switch is a system of software components written
in C, that all run in user mode on top of the seL4 microkernel (Klein et al., 2014).
   Here, we have abstracted from the seL4-based C implementation’s details, to model in the
While language the basic functionality of its three main software components (as depicted
in Figure 6) as a shared-variable concurrent program of three threads:
     • The I NPUT driver is responsible for taking events from input-device interfaces and
       placing them on an input-event buffer for consumption by the S WITCH (Figure 7a).
   7 Aside from presenting a more minimal case study, any verification for an arbitrary security lattice can be

reduced to multiple applications of verification to the basic High ̸→ Low policy, with the locations reclassified
appropriately. Furthermore, the design of the CDDC’s HID switch program is symmetrical for each user.


                                                      47
l o c k ( hid_read_atomicity_lock ) ;
temp : = hid_keyboard_available ;                      i f ( current_event_type = KEYBOARD ) t h e n
u n l o c k ( hid_read_atomicity_lock ) ;                 i f ( active_domain = DOM_LOW ) t h e n
i f ( temp ! = 0 ) t h e n                                   output_event_buffer0 : =
    l o c k ( input_event_lock ) ;                                ,→ current_event_data
    input_event_data : = 0 ;                              else
    input_event_type : = KEYBOARD ;                          output_event_buffer1 : =
    input_event_data : =                                          ,→ current_event_data
            ,→ hid_keyboard_source ;                      fi
    u n l o c k ( input_event_lock )                   else
else                                                      skip
    skip                                               fi
fi
                                                   (b) Delivery to output device by S WITCH.
(a) Receipt from input device by I NPUT driver.    The output-event buffers 0 and 1 are statically
The hid keyboard source variable is value-         classified Low and High respectively (modelling
dependently classified by the value of its sole    an attacker-controlled computer that receives all
control variable, indicated domain (mod-           data written to buffer 0).
elling trusted user input to the keyboard).

Figure 7: Examples of external device interactions by the CDDC HID switch, as modelled
in While—here, for the keyboard events. The full model is in the Isabelle/HOL supplement.


    • The S WITCH is responsible for inspecting all input events on the buffer from the I N -
      PUT driver, querying the compositor device (as modelled in Figure 8a) and OVERLAY
      driver to determine if any constitute a user-directed change to the destination of sub-
      sequent events, and if so, updating the compositor device to display that change (as
      modelled in Figure 8b). Finally, it is responsible for delivering all events to their
      destination computer via the appropriate output-device interface (Figure 7b).

    • The OVERLAY driver is responsible for servicing remote procedure calls (RPCs, made
      by the S WITCH) that query a subset of the compositor-device interface, regarding the
      position of certain mouse-clickable elements the compositor is rendering as part of
      a visual overlay on the trusted user’s video monitor. (As no mixed-sensitivity reuse
      occurs in this part of the model, we leave its details to the Isabelle/HOL supplement.)

The device interfaces, shared buffers (for input events and RPC mechanisms), and local
variables used by each component are all modelled as program variables in shared memory.
Consequently in the While model, mutex locks are used to model all synchronisation and
restriction of concurrent access by the components to those variables.
   So that we do not need to add separate While semantics for interacting with private as
opposed to shared memory, we model thread-private memory as shared program variables
protected by a permanently held lock acquired at initialisation time (e.g. as in Figure 9a).
We consider this to be a stand-in for the memory isolation properties established by the
underlying operating system between the program threads that it hosts.

6.1.3   Mixed-sensitivity reuse
Inherently to the CDDC’s role as a multi-level secure user interface, its HID switch receives
data of differing sensitivity levels (at different times) from a single set of input device mem-


                                                  48
compositor_cursor_position : =                      i f ( switch_state_mouse_down = 0 &&
    ,→ current_event_data ;                                current_event_data = MOUSE_DOWN &&
                                                           active_domain ! = cursor_domain ) t h e n
l o c k ( compositor_read_atomicity_lock ) ;           active_domain : = cursor_domain ;
cursor_domain : =                                      l o c k ( input_event_lock ) ;
        ,→ compositor_domain_under_cursor ;            input_event_data : = 0 ;
u n l o c k ( compositor_read_atomicity_lock ) ;       input_event_type : = NONE ;
                                                       hid_keyboard_source : = 0 ;
i f ( cursor_domain = DOM_INVALID ) t h e n            indicated_domain : = active_domain ;
   cursor_domain : = active_domain                     u n l o c k ( input_event_lock )
else                                                else
   skip                                                skip
fi                                                  fi

(a) Querying the compositor to determine the        (b) Instructing the compositor to indicate a
topmost domain under the mouse cursor.              change to the active domain.

  Figure 8: Excerpts of the S WITCH component interfacing with the compositor device.

                                                        l o c k ( input_event_lock ) ;
/ * Permanently grab t h i s l o c k * /                i f ( indicated_domain = active_domain )
l o c k ( switch_private_lock ) ;                       then
current_event_data : = 0 ;                                  current_event_type : =
current_event_type : = NONE ;                                       ,→ input_event_type ;
                                                            current_event_data : =
l o c k ( input_event_lock ) ;                                      ,→ input_event_data
input_event_data : = 0 ;                                else
hid_keyboard_source : = 0 ;                                 skip
indicated_domain : = active_domain ;                    fi ;
u n l o c k ( input_event_lock )                        u n l o c k ( input_event_lock )


(a) Initialising private variables, input-event         (b) Copying from the input-event buffer to pri-
buffer, and compositor-indicated domain, to an          vate variables. The security analysis shows
arbitrary initial value for active domain. Ze-          that repeating the previous event is a safe
roing the data fields prevents leaking any High-        course of action when the environment mis-
sensitivity data they might initially contain.          behaves by violating indicated domain =
                                                        active domain.

   Figure 9: Excerpts of the S WITCH component interacting with the input-event buffer.


ory locations (e.g. as modelled in Figure 7a, for the keyboard events), rather than from those
of distinct device sets for each sensitivity level.
   Furthermore, the HID switch propagates all input event data (regardless of sensitivity)
through a single set of memory locations (the input-event buffer and S WITCH-internal copies
of its contents, as modelled in Figure 9), rather than duplicating those memory locations for
each security domain. Consequently in the While model, all of these memory locations that
are subject to mixed-sensitivity reuse are assigned value-dependent classifications, reflecting
the trusted user’s expectation of the sensitivity level of the data they contain:

    • To model a user that we trust to type sensitive information into the keyboard only
      when the compositor device indicates the High domain computer is active (i.e. set to
      receive all keyboard events), we have the I NPUT driver draw keyboard events from
      a shared variable named hid keyboard source (as depicted in Figure 7a) that has
      classification dependent on a control variable indicated domain modelling the rel-

                                                   49
        evant state of the compositor (here, DOM HIGH is a designated constant):
                             (
                              High, if indicated domain = DOM HIGH
                              Low, otherwise.

      • In contrast, as clicking on composited user interface elements has the potential abil-
        ity to change the future indicated domain (which, as a control variable, is never
        allowed to receive any High-sensitivity data), the model trusts the user not to encode
        sensitive information into the mouse input in any way. Thus, the I NPUT driver always
        draws mouse events from a statically Low-classified shared variable.
        Consequently, as the data portion input event data of the input-event buffer8
        between the I NPUT driver and S WITCH may carry either keyboard data of value-
        dependent sensitivity or Low-sensitivity mouse data, we assign it a classification de-
        pendent on the values of both its control portion and the indicated domain:
        (
          High, if input event type = KEYBOARD ∧ indicated domain = DOM HIGH
          Low, otherwise.

      • Finally, we model the seL4-based S WITCH component’s copying of the event from the
        buffer into its own local variables, giving its data portion a classification dependent on
        its own private view of the currently active domain (modelled as active domain):
         (
           High, if current event type = KEYBOARD ∧ active domain = DOM HIGH
           Low, otherwise.

        To ensure active domain remains authoritative with what is composited by
        the CDDC into the display, in the While model the S WITCH initialises
        indicated domain to match the initial value of active domain (as depicted in Fig-
        ure 9a), updates it whenever active domain changes (as depicted in Figure 8b), and
        checks at runtime that active domain = indicated domain when copying data
        from the buffer to its own private variables (as depicted in Figure 9b).

   The CVDNI properties’ (1) value dependence on control variables, (2) quantification over
all initial values for the control variables and (3) assumptions of environmental havoc on
write-unprotected shared variables between evaluation steps (Definition 2.6) then ensure
noninterference between High inputs and Low-classified sinks, regardless of the initial and
dynamically changing sensitivity of all such locations subject to mixed-sensitivity reuse.

6.2     CVDNI properties of the While model to be preserved
This section will now give a brief formal exposition of the security properties of the CDDC
HID switch’s While-language model that our compiler will preserve down to RISC.
   As the per-thread proof techniques for While that we used for the case study are outside
the scope of this paper, we note only that they consist of an adaptation to mutex locks by
   8 We model in While only a single-place buffer, which could easily be extended to a buffer of arbitrary size

by duplicating the same basic pattern of access, classification, and lock-protection, for multiple places.


                                                     50
Sison (2020) of a security type system and local mode compliance check developed by
Murray et al. (2016b,c). Nevertheless, we have provided their full formalisation in our
Isabelle/HOL supplement, and we refer the reader to these prior works on their design, and
particularly to Sison (2020) for further discussion on their application to this case study.
   In short, from applying local type checks on the While-language commands for each of
the three software components (I NPUT, S WITCH, and OVERLAY) to obtain per-thread secu-
rity (com-secure, Definition 2.7) and modes compliance (local-mode-compliance, Defini-
tion 2.11), we have from Theorem 2.8 that the concurrent program of all three components
satisfies the whole-system security property (sys-secure, Definition 2.9) as instantiated to
specify that no locks are held initially.
   So that we can use the approach we gave in Section 3 to obtain the global modes compati-
bility part of the sound-mode-use side-condition (Definition 2.10), we specify no-locks-held
(Definition 3.18) as the INIT requirement on memory, and use the initial mode state mds0
(Definition 3.19) for all of the components in the system.
   This no-locks-held predicate and mds0 are both defined relative to a lock interpretation
parameter that we supply (as required by Section 3.1) for the CDDC model. The locks in
the CDDC model fall under the following categories:
    • The locks coordinating inter-component interactions grant exclusive read–write ac-
      cess to the shared variables they govern.
    • There are also locks granting the S WITCH and I NPUT components exclusive read–
      write access to a set of “private” variables each, for internal use. The components
      acquire these prior to entering their main loop, and never release them.
    • Finally the model uses read-atomicity locks—a practice introduced in Section 5.1.1.
      These grant exclusive write access to shared variables used to model hardware inter-
      faces, to make explicit an assumption (normally implicit in the atomicity of expres-
      sion evaluation in the While language) that these variables will not have their value
      changed by the environment during a simple assignment from those variables.
      Note that these read-atomicity locks are not needed to prove confidentiality for the
      While model, but rather we add them to satisfy the requirements demanded by the
      wr-compiler so that it can preserve confidentiality (via small-step semantic preserva-
      tion) down to the RISC model.
   The While-language proof techniques we apply to each thread of the program yield
com-secureno-high-branching , a stronger version of the per-thread CVDNI property that en-
forces no-high-branching (Definition 5.5). Furthermore, we have trivially from the def-
inition of com-secure (Definition 2.7) that if a program is secure without imposing any
initial conditions, then it remains secure if we impose any INIT parameter arbitrarily.
Therefore, for each thread we have com-secureno-high-branching
                                                 no-locks-held   (Definition 2.7, with INIT ≜
no-locks-held and EXTRA ≜ no-high-branching):
Lemmas 6.1 (Per-thread confidentiality results for CDDC While model).
                                 no-high-branching
                       com-secureno-locks-held     (OVERLAY, mds0 )
                                 no-high-branching
                       com-secureno-locks-held     (I NPUT, mds0 )
                                 no-high-branching
                       com-secureno-locks-held     (S WITCH, mds0 )

                                             51
   From this and Theorem 2.8, using local compliance checks and Lemma 3.20 to discharge
the sound-mode-use (Definition 2.10) side condition, we have a whole-system confidential-
ity theorem for the system of all three components running concurrently:
Theorem 6.2 (Whole-system confidentiality result for the CDDC While model).

       sys-secureno-locks-held [(OVERLAY, mds0 ), (I NPUT, mds0 ), (S WITCH, mds0 )]

6.3   Confidentiality-preserving compilation to RISC model
We now turn to applying the C OVERN wr-compiler of Section 5 to our While-language
model of the CDDC’s HID switch; we then have automatically that it preserves the security
properties presented in Section 6.2 down to the compiler’s RISC-language output.
   The wr-compiler is executable in the Isabelle proof assistant. Using Isabelle’s eval
tactic, we execute the wr-compiler’s main function, compile-cmd (whose implementation
was described in Section 5.1) on the While-language models for all three of the CDDC’s
I NPUT driver, S WITCH, and OVERLAY driver components, to obtain their RISC-language
compilations. (Recall from Section 5.1 that we obtain the RISC text trivially as the map fst
of the CompRec-annotated RISC program, which is the fst output of compile-cmd.)
Definition 6.3 (RISC-language program texts of CDDC model’s components).

          OVERLAYRISC ≜ map fst (fst (compile-cmd C0 None 0 OVERLAY))
              I NPUTRISC ≜ map fst (fst (compile-cmd C0 None 0 I NPUT))
            S WITCHRISC ≜ map fst (fst (compile-cmd C0 None 0 S WITCH))

  Our approach to obtain per-thread confidentiality for each of these RISC texts will be to
use the theorem of its preservation by the wr-compiler (Theorem 5.24). Recall, this was:
Theorem 5.24 (Preservation of per-thread confidentiality by the wr-compiler).

                              com-secureno-high-branching
                                        no-locks-held     (c, mds0 )
          ′    ′ ′
   (PCs, l , nl ,C , False) = compile-cmd C0 l nl c       compile-cmd-input-reqs C0 l nl c

                  com-securepc-security
                            no-locks-held (((0, map fst PCs), regs), mds0 )

   Then, for compile-cmd to execute successfully (i.e. to return failed = False), the model
must pass the stability-checks discussed in Section 5.1. All three of OVERLAY, I NPUT, and
S WITCH pass the checks (1) because they use locks to protect the atomicity of reads from
(otherwise unstable) variables used to model hardware interfaces, and (2) as a consequence
of having passed the local security and mode compliance checks mentioned in Section 6.2.
   We are now in a position to prove a whole-system confidentiality result for the compiled
RISC model—here, with each thread’s register bank initialised to zero: regs0 ≜ (λ . 0).
Theorem 6.4 (Whole-system confidentiality result for the CDDC RISC model).

                sys-secureno-locks-held [(((0, OVERLAYRISC ), regs0 ), mds0 ),
                                       (((0, I NPUTRISC ), regs0 ), mds0 ),
                                       (((0, S WITCHRISC ), regs0 ), mds0 )]

                                             52
Proof. A few approaches are available; we obtained formal proofs of this theorem in Is-
abelle/HOL using all three of the following alternatives (unfolding Definition 6.3):
   Option 1. Use either of Theorem 5.22 or Theorem 5.27, both of which estab-
lished whole-system security for RISC outputs of the wr-compiler when executed on
            no-high-branching
com-secureno-locks-held       While programs (which we have here from Lemmas 6.1). This is
the easiest option to take for programs that are already verified in the While language, and
then compiled successfully to RISC by the wr-compiler. It is possible to take here because
all of OVERLAYRISC , I NPUTRISC , and S WITCHRISC were obtained in this manner.
   Option 2. Use Theorem 5.24 and Lemma 5.25 to obtain com-securepc-security no-locks-held and
local-mode-compliance (resp.) for each of OVERLAYRISC , I NPUTRISC , and S WITCHRISC ,
then use Theorem 2.8 directly to obtain sys-secureno-locks-held . This option can be used
for systems where some of the threads are written directly in RISC; for such threads,
com-securepc-security
            no-locks-held and local-mode-compliance would need to be proved directly at
RISC level. However, Lemma 5.26 still discharges the global-modes-compatibility require-
ment for RISC, provided all threads are initialised with mds0 and no-locks-held.
   Option 3. Use Theorem 2.23 directly. This option can be used for systems where all the
RISC threads are secure refinements (according to Definition 2.15) of the threads of some
While program that satisfied sound-mode-use with no-locks-held initially, but some were
obtained by other means than the wr-compiler (i.e. not all via the refinement Rwr ).


7     Related work
First in Section 7.1, we describe other recent and related works that address concerns of
noninterference proof compositionality in a concurrent setting (of the kind we tackled in
Section 3). The remaining sections focus on related works on verified compilation: The
works in Section 7.2 and Section 7.3, like ours, focus on compilation preserving a form of
noninterference. In Section 7.4 we describe our work’s relationship with varieties of robust
property preservation, and other compilation verification efforts in Section 7.5.

7.1   Compositionality of concurrent noninterference proofs
Alternative approaches exist to establishing the non-compositional global modes compati-
bility condition we proved as invariant to concurrent While executions in Section 3. For the
precursor (non–value-dependent) notion of concurrent noninterference to CVDNI, Mantel
et al. (2011) originally proposed that such a condition be met by a non-compositional may
happen in parallel analysis (e.g. Masticola & Ryder (1993)). Then, instead of demanding
the explicit declaration of the sorts of guarantees implied by locking discipline (as we do),
Mantel et al. (2015) proposed automating their inference and proof of the compatibility con-
dition using a reachability analysis making use of dynamic pushdown networks. We leave
adapting and implementing such an approach for our CVDNI setting to future work.
   We note also that, like the CVDNI theory and our work of Section 3, recent work by Fru-
min et al. (2021) concerns compositionality of machine-checked proof efforts for noninter-
ference in a concurrent setting that are obtained potentially via a variety of proof techniques.
They model more fine-grained synchronisation than we do here, via atomic compare-and-
swap operations that can be used to implement mutex locking primitives. However, they


                                              53
do not study compilation as a means of preserving such proofs, which is the focus of our
work here. We believe that the CVDNI refinement notions we presented could support cer-
tain cases of compilation between different synchronisation primitives, provided only new
thread-private state is needed (like the registers in RISC), and the shared variable interactions
can be proved as preserved. For example, we expect mutex locking primitives (with slightly
different semantics to ours here) could feasibly be refined to a compare-and-swap–based
implementation in this way—this we also leave to future work.

7.2    Noninterference-preserving compilation
Tedesco et al. (2016) present a type-directed compilation scheme that preserves a fault-
resilient noninterference property. The compilation scheme of our wr-compiler was in-
spired by theirs. Like our com-secure CVDNI security property that wr-compiler pre-
serves, Tedesco et al.’s security property is also strong bisimulation-based (Sabelfeld &
Sands, 2000). But where our property accounts (via mode states) for controlled interference
by other threads, theirs instead quantifies over all possible interference by the environment
with the memory contents. While this simplifies their task of proving that their security
property is preserved under compilation—as it need not require the compiler to preserve
the contents of memory—it means their security property cannot capture value-dependent
noninterference. In contrast, our wr-compiler must obey our secure-refinement notion’s
requirement that memory contents are preserved.
   The line of work most relevant to ours is that which was conducted (concurrently) by
Barthe et al. (2020), wherein they achieved the remarkable result of proving that a modifi-
cation of the CompCert C compiler (Leroy, 2009) preserves the cryptographic constant-time
class of noninterference (2-safety) properties. Their proof approach was to use various no-
tions of constant-time simulation (CT-simulation) first presented by Barthe et al. (2018),
originally intended for application to the Jasmin compiler (Almeida et al., 2017). Although
not targeting programs with concurrency or mixed-sensitivity reuse (as our work does),
CT-simulation shares in common with the refinement notions used by this paper that it in
essence rests on a simulation diagram that is cube-shaped, as it must preserve a 2-safety hy-
perproperty. We submit that Barthe et al. (2020) broadly validates the argument we made in
Sison & Murray (2019), that decomposing such cube-shaped diagrams into square-shaped
ones is what will make them feasible to apply to the verification of fully fledged compilers
like CompCert—noting that they described the only compilation pass they proved with their
non-decomposed, cube-shaped diagram as “not especially pleasant because the diagrams
are difficult to exploit” (Barthe et al., 2020).
   Note that the refinement theory of Barthe et al. (2018, 2020) preserves security via re-
finement phrased in terms of forward simulation (Leroy, 2009)—that is, each step of the
abstract program must be simulated by the target program. In contrast, our theory presented
here is instead targeted towards preserving refinement via backward simulations,9 in which
each step of the concrete (compiled) program must be simulated by the abstract program.
This difference arises because in our setting we need to account for leakage that might occur
   9 Again, as commonly referred to in the compiler verification literature from Leroy (2009) onwards. This is

not to be confused with the “backward simulations” of concurrency verification (Lynch & Vaandrager, 1996)
and data refinement (de Roever & Engelhardt, 1998; Cavalcanti & Naumann, 2002), where the refined program
instead simulates the original, and where simulation proceeds from the end of the program back to the beginning.


                                                      54
and be visible only in intermediate states. In their setting, in contrast, leakage that occurs in
intermediate states remains visible forever in the concrete program semantics via a leakage
trace. It remains unclear whether we could have adopted a similar approach in our work,
thereby enabling a (simpler) forward simulation argument. In particular, it is not clear what
the semantics of leakage traces should be for a language that supports both value-dependent
classification and shared-memory concurrency as ours does.

7.3   Concurrency-compositional noninterference-preserving compilation
Neither of the above consider per-thread compositional compilation of concurrent, shared
memory programs, nor value-dependent noninterference policies – the focus of our theory
and compiler. Barthe et al. (2010, 2007a) however did aim to preserve noninterference of
multithreaded programs by compilation, extending a prior (security) type-preserving com-
pilation approach (Barthe et al., 2004, 2007b). Their noninterference property however
was termination- and timing-insensitive, so preventing internal timing leaks relied on the
scheduler disallowing certain interleavings between threads. Also, their type-preservation
argument was derived from a big-step semantics preservation property for their compiler.
Here we instead rely on preservation of a small-step semantics (specifically memory con-
tents), which is necessary for us to preserve value-dependent security under compilation, as
well as to avoid imposing non-standard requirements on the scheduler.

7.4   Robust property preservation
Other recent works have improved on fully abstract compilation (surveyed by Patrignani
et al. (2019)) by mapping out the spectrum (Abate et al., 2019) or developing specific forms
(Patrignani & Garg, 2019) of robust property preservation, concerned with robustness of
source program (hyper)properties to concrete adversarial contexts. Like Tedesco et al.
(2016), these works differ from ours in quantifying over a wider range of hostile interfer-
ence. They also focus prominently on changes to data types, which we do not support.
Thus, as a 2-safety hyperproperty quantifying over a lesser range of interference, we expect
CVDNI-preservation to be implied by R2HSP (robust 2-hypersafety preservation), but do
not expect it to imply any other secure compilation criterion on Abate et al.’s spectrum.
   While recently Patrignani & Garg (2019) instantiated their robustly safe compilation for
shared-memory fork-join concurrent programs, it only preserves (1-)safety properties. Pre-
viously however, Patrignani & Garg (2017) proved their trace-preserving compilation pre-
serves k-safety hyperproperties (Clarkson & Schneider, 2010), including noninterference
properties. However, it disallows the removal or addition of trace entries, which would be
necessary to change the passage of time as seen in the observable trace events. Thus it ex-
cludes the sorts of changes to pacing carried out by our compiler (regulated by abs-steps)
and studied as optimisations by the two other works (Tedesco et al., 2016; Barthe et al.,
2020) on timing-sensitive security-preserving compilation mentioned above.

7.5   Compiler verification in general
Finally, there has been much work on large-scale verified compilation (Leroy, 2009; Ku-
mar et al., 2014) some of which has also treated compilation of shared-memory concurrent


                                               55
programs (Lochbihler, 2018) including taking weak-memory consistency into account (Pod-
kopaev et al., 2019). Our work here does not consider the effects of weak-memory models.
In particular, such models are often defined axiomatically rather than operationally. Our
notion of secure refinement and our decomposition principle (Definitions 2.15 and 2.18,
respectively) are defined assuming an operational semantics for the source and target lan-
guages.
   Our work differs to prior work on verified concurrent compilation, in that it formalises
and proves a compiler’s ability to use information about the application’s locking protocol,
both to exclude unsafe access to shared variables, and conversely to know when it is safe to
allow optimisations on shared variables that would typically be excluded.


8    Conclusion
To our knowledge, we have presented the first mechanised verification that a compiler pre-
serves concurrent, value-dependent noninterference. To this end, we provided a general
decomposition principle for compositional, secure refinement. Although our compiler is
a proof-of-concept targeting simple source and target languages, we nevertheless applied
it to produce a verified assembly-level model of an input-handling system for the CDDC
(Beaumont et al., 2016), a nontrivial mixed-sensitivity concurrent program.
   We expect this decomposition principle to remain applicable in reducing noninterference-
refinement proof efforts for compilers that overcome the specific limitations of ours here.
For example, a compiler that inserts padding to equalise the time taken on either side of a
High-branch—which may change when it expands expressions into multiple instructions—
may instantiate the decomposition principle with a more sophisticated concrete coupling
invariant that does not require pc-security.
   This work serves to demonstrate that verified security-preserving compilation for mixed-
sensitivity concurrent programs is now within reach, by augmenting traditional proof obli-
gations for verified compilation (e.g. square-shaped semantics preservation) with those spe-
cific to security (e.g. absence of termination- and timing-leaks) as depicted in Figure 4. We
hope that this work paves the way for future large-scale verified security-preserving compi-
lation efforts.

Acknowledgements
We would like to thank our anonymous referees, and to thank again all those who provided
feedback on the conference version of this paper (Sison & Murray, 2019) and on Robert
Sison’s PhD thesis (Sison, 2020). This paper describes research that was conducted during
Robert’s PhD candidature at UNSW Sydney and CSIRO’s Data61, which was funded by an
Australian Government Research Training Program (RTP) Scholarship and a CSIRO Data61
Research Project Award. We thank the Trustworthy Systems group at CSIRO’s Data61 for
cultivating an excellent working and learning environment.

Conflicts of Interest
None



                                             56
References
Abate, C., Blanco, R., Garg, D., Hritcu, C., Patrignani, M. and Thibault, J. (2019) Journey
  beyond full abstraction: Exploring robust property preservation for secure compilation.
  32nd IEEE Computer Security Foundations Symposium, CSF 2019, Hoboken, NJ, USA,
  June 25-28, 2019 pp. 256–271. IEEE.

Almeida, J. B., Barbosa, M., Barthe, G., Blot, A., Grégoire, B., Laporte, V., Oliveira, T.,
  Pacheco, H., Schmidt, B. and Strub, P.-Y. (2017) Jasmin: High-assurance and high-
  speed cryptography. Proceedings of the 2017 ACM SIGSAC Conference on Computer
  and Communications Security. CCS ’17, pp. 1807–1823. ACM.

Barthe, G., Basu, A. and Rezk, T. (2004) Security types preserving compilation: (extended
  abstract). Steffen, B. and Levi, G. (eds), Verification, Model Checking, and Abstract
  Interpretation, 5th International Conference, VMCAI 2004, Venice, Italy, January 11-13,
  2004, Proceedings. Lecture Notes in Computer Science 2937, pp. 2–15. Springer.

Barthe, G., Rezk, T., Russo, A. and Sabelfeld, A. (2007a) Security of multithreaded pro-
  grams by compilation. Biskup, J. and López, J. (eds), Computer Security - ESORICS
  2007, 12th European Symposium On Research In Computer Security, Dresden, Germany,
  September 24-26, 2007, Proceedings. Lecture Notes in Computer Science 4734, pp. 2–
  18. Springer.

Barthe, G., Rezk, T. and Basu, A. (2007b) Security types preserving compilation. Comput.
  Lang. Syst. Struct. 33(2):35–59.

Barthe, G., Rezk, T., Russo, A. and Sabelfeld, A. (2010) Security of multithreaded programs
  by compilation. ACM Trans. Inf. Syst. Secur. 13(3):21:1–21:32.

Barthe, G., Grégoire, B. and Laporte, V. (2018) Secure compilation of side-channel coun-
  termeasures: The case of cryptographic “constant-time”. 31st IEEE Computer Security
  Foundations Symposium, CSF 2018, Oxford, United Kingdom, July 9-12, 2018 pp. 328–
  343. IEEE Computer Society.

Barthe, G., Blazy, S., Grégoire, B., Hutin, R., Laporte, V., Pichardie, D. and Trieu, A. (2020)
  Formal verification of a constant-time preserving C compiler. Proc. ACM Program. Lang.
  4(POPL):7:1–7:30.

Beaumont, M., McCarthy, J. and Murray, T. (2016) The cross domain desktop compositor:
  Using hardware-based video compositing for a multi-level secure user interface. Schwab,
  S., Robertson, W. K. and Balzarotti, D. (eds), Proceedings of the 32nd Annual Conference
  on Computer Security Applications, ACSAC 2016, Los Angeles, CA, USA, December 5-9,
  2016 pp. 533–545. ACM.

Cavalcanti, A. and Naumann, D. A. (2002) Forward simulation for data refinement of
  classes. Eriksson, L.-H. and Lindsay, P. A. (eds), FME 2002:Formal Methods—Getting
  IT Right pp. 471–490. Springer Berlin Heidelberg.

Clarkson, M. R. and Schneider, F. B. (2010)            Hyperproperties.     J. Comput. Secur.
  18(6):1157–1210.

                                              57
de Roever, W. P. and Engelhardt, K. (1998) Data Refinement: Model-oriented Proof Theo-
  ries and their Comparison. Cambridge Tracts in Theoretical Computer Science, vol. 46.
  Cambridge University Press.

Focardi, R., Gorrieri, R. and Panini, V. (1995) The security checker: a semantics-based
  tool for the verification of security properties. Proceedings The Eighth IEEE Computer
  Security Foundations Workshop pp. 60–69.

Frumin, D., Krebbers, R. and Birkedal, L. (2021) Compositional non-interference for fine-
  grained concurrent programs. 42nd IEEE Symposium on Security and Privacy (S&P’21),
  to appear; CoRR abs/1910.00905.

Jones, C. B. (1981) Development Methods for Computer Programs including a Notion of
  Interference. D.Phil. thesis, University of Oxford.

Kaufmann, T., Pelletier, H., Vaudenay, S. and Villegas, K. (2016) When constant-time
  source yields variable-time binary: Exploiting curve25519-donna built with msvc 2015.
  Cryptology and Network Security pp. 573–582. Springer International Publishing.

Klein, G., Andronick, J., Elphinstone, K., Murray, T., Sewell, T., Kolanski, R. and Heiser,
  G. (2014) Comprehensive formal verification of an OS microkernel. ACM Transactions
  on Computer Systems 32(1):2:1–2:70.

Kumar, R., Myreen, M., Norrish, M. and Owens, S. (2014) CakeML: A verified implemen-
  tation of ML. Peter Sewell (ed), ACM SIGPLAN-SIGACT Symposium on Principles of
  Programming Languages pp. 179–191. ACM Press.

Leroy, X. (2009) A formally verified compiler back-end. J. Autom. Reason. 43(4):363–446.

Lochbihler, A. (2018) Mechanising a type-safe model of multithreaded java with a verified
  compiler. Journal of Automated Reasoning 61(1):243–332.

Lynch, N. and Vaandrager, F. (1996) Forward and backward simulations. Inf. Comput.
  128(1):1–25.

Mantel, H., Sands, D. and Sudbrock, H. (2011) Assumptions and guarantees for composi-
 tional noninterference. IEEE Computer Security Foundations Symposium pp. 218–232.
 IEEE.

Mantel, H., Müller-Olm, M., Perner, M. and Wenner, A. (2015) Using dynamic pushdown
 networks to automate a modular information-flow analysis. 25th International Sympo-
 sium on Logic Based Program Synthesis and Transformation (LOPSTR).

Masticola, S. P. and Ryder, B. G. (1993) Non-concurrency analysis. Proceedings of the
 Fourth ACM SIGPLAN Symposium on Principles and Practice of Parallel Programming.
 PPOPP ’93, pp. 129–138. ACM.

Molnar, D., Piotrowski, M., Schultz, D. and Wagner, D. (2006) The program counter secu-
 rity model: Automatic detection and removal of control-flow side channel attacks. Pro-
 ceedings of the 8th International Conference on Information Security and Cryptology.
 ICISC’05, pp. 156–168. Springer-Verlag.

                                            58
Murray, T. (2015) On high-assurance information-flow-secure programming languages.
 ACM SIGPLAN Workshop on Programming Languages and Analysis for Security pp. 43–
 48.
Murray, T., Sison, R., Pierzchalski, E. and Rizkallah, C. (2016a) Compositional
 security-preserving refinement for concurrent imperative programs. Archive of For-
 mal Proofs June. http://isa-afp.org/entries/Dependent_SIFUM_Refinement.
 shtml, Formal proof development.
Murray, T., Sison, R., Pierzchalski, E. and Rizkallah, C. (2016b) Compositional verification
 and refinement of concurrent value-dependent noninterference. IEEE 29th Computer
 Security Foundations Symposium, CSF 2016, Lisbon, Portugal, June 27 - July 1, 2016
 pp. 417–431. IEEE Computer Society.
Murray, T., Sison, R., Pierzchalski, E. and Rizkallah, C. (2016c) A dependent security type
 system for concurrent imperative programs. Archive of Formal Proofs June. http://
 isa-afp.org/entries/Dependent_SIFUM_Type_Systems.html, Formal proof de-
 velopment.
Murray, T., Sison, R. and Engelhardt, K. (2018) C OVERN: A logic for compositional ver-
 ification of information flow control. European Symposium on Security and Privacy pp.
 16–30. IEEE.
Patrignani, M. and Garg, D. (2017) Secure Compilation and Hyperproperty Preservation.
  IEEE 30th Computer Security Foundations Symposium, CSF 2017, Santa Barbara, USA,
  August 21 - 25, 2017. CSF’17.
Patrignani, M. and Garg, D. (2019) Robustly safe compilation. Programming Languages
  and Systems pp. 469–498. Springer International Publishing.
Patrignani, M., Ahmed, A. and Clarke, D. (2019) Formal approaches to secure compi-
  lation: A survey of fully abstract compilation and related work. ACM Comput. Surv.
  51(6):125:1–125:36.
Podkopaev, A., Lahav, O. and Vafeiadis, V. (2019) Bridging the gap between program-
  ming languages and hardware weak memory models. Proc. ACM Program. Lang.
  3(POPL):69:1–69:31.
Sabelfeld, A. and Sands, D. (2000) Probabilistic noninterference for multi-threaded pro-
  grams. Proceedings of the 13th IEEE Workshop on Computer Security Foundations.
  CSFW ’00, pp. 200–. IEEE Computer Society.
Sison, R. (2020) Proving Confidentiality and Its Preservation Under Compilation for
  Mixed-Sensitivity Concurrent Programs. PhD thesis, University of New South Wales,
  Sydney. http://doi.org/10.26190/5fab5c0a76454.
Sison, R. and Murray, T. (2019) Verifying That a Compiler Preserves Concurrent Value-
  Dependent Information-Flow Security. Harrison, J., O’Leary, J. and Tolmach, A. (eds),
  10th International Conference on Interactive Theorem Proving (ITP 2019). Leibniz In-
  ternational Proceedings in Informatics (LIPIcs) 141, pp. 27:1–27:19. Schloss Dagstuhl–
  Leibniz-Zentrum fuer Informatik.

                                            59
Staples, M., Jeffery, R., Andronick, J., Murray, T., Klein, G. and Kolanski, R. (2014) Pro-
  ductivity for proof engineering. Empirical Software Engineering and Measurement p.
  15.

Tedesco, F. D., Sands, D. and Russo, A. (2016) Fault-resilient non-interference. IEEE 29th
  Computer Security Foundations Symposium, CSF 2016, Lisbon, Portugal, June 27 - July
  1, 2016 pp. 401–416. IEEE Computer Society.

Terauchi, T. and Aiken, A. (2005) Secure information flow as a safety problem. Hankin, C.
  and Siveroni, I. (eds), Static Analysis pp. 352–367. Springer Berlin Heidelberg.

Volpano, D. and Smith, G. (1998) Probabilistic noninterference in a concurrent lan-
  guage. Proceedings. 11th IEEE Computer Security Foundations Workshop (Cat.
  No.98TB100238) pp. 34–43.



A    Label allocation and sequential composability
The wr-compiler fixes the label type Lab ≜ nat to allow it to ensure freshness merely by
using the highest natural number reached so far on a “next label” counter (the argument nl
in Example 5.1); it then increments the counter before passing it to subsequent calls, and
outputs the next available unused label on return (the return value nl′ in the example).
   Relative to this scheme, we prove that two consecutively compiled RISC programs—in
the sense that the relevant outputs from the first call are fed directly into the second call—
only ever jump to locations within themselves (and not in the other).
   Specifically, we define two RISC programs P1 , P2 to be joinable if they are both:

    • joinable-forward: P1 only ever jumps to labels that are either

         – labelling an instruction in P1 itself, or
         – the label of the very first instruction in P2 .

    • joinable-backward: P2 does not jump to any of the labels of instructions in P1 .

The lemma we prove then says that two RISC programs output by consecutive invocations
of the wr-compiler are joinable.
   Proving that the control flow of programs compiled by the wr-compiler always remains
self-contained in this manner facilitates reasoning about their sequential composition.


B    Register allocation scheme model
Like Tedesco et al. (2016) we generalise over the (user-supplied) register allocation scheme,
and assume there are enough registers to service the maximum depth of expressions in the
source program. We leave for future work the modelling and analysis of a compiler phase
that spills register contents to memory, in order to make this assumption unnecessary.
   Here we model the (user-supplied) register allocation scheme with two functions
reg alloc and reg alloc cached on the register record Φ (see Section 5.1) and the set A


                                               60
of registers whose contents are needed to evaluate the current expression. To avoid loading
from memory unnecessarily, the compiler may first call reg alloc cached Φ A v to identify
a register that Φ records as already containing the variable v. When the compiler needs a
fresh register, it will call reg alloc Φ A. Neither function is allowed to allocate a register
in A, so the allocator is permitted to fail if it cannot find any suitable register. However,
registers typically become available again as expression evaluation is resolved.


C      Informal descriptions of cases of refinement relation Rwr
C.1     Base cases
      • stop: This case relates a terminated While program with a terminated RISC program
        (i.e. one where the program counter is at the length of the program text).

      • skip nop: This case relates the While program skip with the configuration where
        the program counter is at the start of the RISC program [Nop].

      • assign expr: This case relates the expression evaluation part (for the expression
        e) of the While program v := e with the corresponding part of the RISC program
        obtained by compiling it with the wr-compiler.

      • assign store: As for assign expr, but for the very last Store instruction that
        commits the result of the expression evaluation back to shared memory variable v.
        It asserts additionally that v must be stable if lock-governed, and non-lock-governed
        otherwise. This prevents threads from violating the locking discipline (see Sec-
        tion 3.1).

      • lock acq: This case relates lock(k) with LockAcq k.

      • lock rel: This case relates unlock(k) with LockRel k.

C.2     Inductive cases
      • seq: This case relates the While program c1 ; c2 with the concatenation P1 @P2 of the
        RISC programs P1 and P2 that are respectively the outputs of successful consecutive
        compilation (see Appendix A) of c1 and c2 by the wr-compiler. It is intended for
        cases where the While (resp. RISC) program is currently in c1 (resp. P1 ).
        It is an inductive case of Rwr , in that:

           – c1 is required to be related by Rwr to the present location in P1 .
           – For all local configurations that obey the compiled-cmd-config-consistent re-
             quirements, c2 is required to be related by Rwr to the first instruction of P2 . This
             quantification ensures that Rwr remains closed when execution progresses from
             the first program to the second program.

        It asserts that P1 and P2 are joinable (Appendix A), which is particularly relevant here
        to ensure that P1 can only jump to locations within or at the end of itself (i.e. the start
        of P2 ).

                                                    61
• join: This case relates a While program c with an offset pc > length P1 into a RISC
  program P1 @P2 , assuming the inductive hypothesis that c is related by Rwr with the
  offset pc − length P1 into the RISC program P2 alone.
  It is intended primarily for cases where the While (resp. RISC) program is currently
  in the c2 (resp. P2 ) of some consecutively compiled c1 ; c2 (resp. P1 concatenated with
  P2 ) but applies more broadly to allow any prepend of dead, unreachable instructions
  onto the front of a RISC program without breaking Rwr .
  It also asserts that P1 and P2 are joinable, which is important here to ensure that P2
  cannot jump back into P1 .

• if expr: This case relates the expression evaluation part (for the expression e) of
  the While program if e then c1 else c2 fi with the corresponding part (including the
  conditional jump Jz at the end of expression evaluation) of the RISC program obtained
  by compiling it with the wr-compiler.
  It relies on both c1 and c2 being related by Rwr to its compiled RISC
  counterparts when started with initialisation states judged valid by
  compiled-cmd-config-consistent.
  This case is depicted in full in Figure 10, on page 63; for comparison, Figure 11
  depicts the relevant part of the compile-cmd implementation.

• if c1: This case relates some While program c′1 reachable from c1 with the cor-
  responding part within the c1 part of the RISC program obtained by compiling
  if e then c1 else c2 fi with the wr-compiler.
  It relies on c1 being related by Rwr to its compiled RISC counterpart at the appropriate
  program counter offset.

• if c2: As for if c1, but for c2 .

• epilogue step: This case relates a terminated While program to the silent control
  flow steps navigating to the end of a RISC program from the end of the “then” and
  “else” branches of a compiled if-conditional.
  It works only for the “epilogue” step forms: Jmp and Nop (see Section 5.3.2).
  It is inductive in that it asserts closedness of Rwr over pairwise reachability from the
  pair currently under consideration—the only case to do so directly.

• while expr: This case relates the While program (while e do c od)’s initial interme-
  diate step to if e then (c ; while e do c od) else stop fi, and its expression evaluation
  part, with the expression evaluation and conditional jump of the RISC program that
  while e do c od was compiled to by compile-cmd.
  It relies on c being related by Rwr to its compiled RISC counterpart when started with
  initialisation states judged valid by compiled-cmd-config-consistent.

• while inner: This case relates some program cI ; while e do c od reachable from
  c ; while e do c od to the loop body part of the RISC program compiled from
  while e do c od.


                                          62
       It relies on cI being related by Rwr to its compiled RISC counterpart at the appropriate
       program counter offset.
       It also carries around the same reliance on c being related by Rwr to
       its compiled RISC counterpart for all initialisation states judged valid by
       compiled-cmd-config-consistent.

    • while loop: This case handles epilogue steps for the inner loop body program, and
      the final jump back to the beginning of the While-loop.
       It requires Rwr to relate the terminated While program to the end of the compiled
       loop body, and furthermore also carries around the same reliance on c being related
       by Rwr to its compiled RISC counterpart for all initialisation states judged valid by
       compiled-cmd-config-consistent.



                      c = if e then c1 else c2 fi        compile-cmd-input-reqs C l nl c
       ′       ′
(PCs, l , nl2 ,C , False) = compile-cmd C l nl c                  (Pe , r,C1 , False) = compile-expr C ∅ l e
  (P1 , l1 , nl1 ,C2 , False) = compile-cmd C1 None (Suc (Suc nl)) c1                    pc ≤ length Pe
  (P2 , l2 , nl2 ,C3 , False) = compile-cmd C1 (Some nl) nl1 c2                  Cpc = (map snd PCs)[pc]
              compiled-cmd-config-consistent Cpc regs mds mem                    regrec-stable Cpc
    ∀mds′ mem′ regs′ . compiled-cmd-config-consistent C1 regs′ mds′ mem′ ∧ regrec-stable C1
                    −→ ((⟨c1 , mds′ , mem′ ⟩w , ⟨((0, map fst P1 ), regs′ ), mds′ , mem′ ⟩r ) ∈ Rwr ∧
                           (⟨c2 , mds′ , mem′ ⟩w , ⟨((0, map fst P2 ), regs′ ), mds′ , mem′ ⟩r ) ∈ Rwr )
                     (⟨c, mds, mem⟩w , ⟨((pc, map fst PCs), regs), mds, mem⟩r ) ∈ Rwr


Figure 10: Introduction rule for case if expr of refinement relation Rwr .
This case pertains to the expression-evaluation part of an if-conditional compiled by
compile-cmd (see Figure 11). Variables ignored are in gray.


compile_cmd C l nl (If e c1 c2 ) =
  (let (Pe , r, C1 , faile ) = (compile_expr C {} l e);
       (br, nl’) = (nl, Suc nl); (ex, nl’’) = (nl’, Suc nl’);
       (P1 , l1 , nl1 , C2 , fail1 ) = (compile_cmd C1 None nl’’ c1 );
       (P2 , l2 , nl2 , C3 , fail2 ) = (compile_cmd C1 (Some br) nl1 c2 );
       (* Pre−compilation check ensures asmrec C2 = asmrec C3 *)
       C’ = (regrec C2 ⊓R regrec C3 , asmrec C2 )
   in (Pe @ [((if Pe = [] then l else None, Jz br r), C1 )] @
       P1 @ [((l1 , Jmp ex), C2 )] @ P2 @ [((l2 , Nop’), C3 )],
       Some ex, nl2 , C’, faile ∨ fail1 ∨ fail2 ))

Figure 11: Excerpt of wr-compiler implementation: case for if-conditionals.
This case of the Isabelle/HOL function compile-cmd compiles the While command
if e then c1 else c2 fi. Here, @ denotes concatenation between two RISC program texts,
and Φ ⊓R Φ′ denotes the subset of mappings on which the register records Φ and Φ′ agree.


                                                      63
